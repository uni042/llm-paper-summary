import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).parents[1] / "scripts"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _install_scripts(repo: Path):
    dst = repo / ".survey/scripts"
    dst.mkdir(parents=True, exist_ok=True)
    for name in (
        "process_immutable_submission.py",
        "immutable_submission.py",
        "record_bank_config.py",
        "queue_worker.py",
        "claim_state.py",
        "survey.py",
    ):
        src = SCRIPTS / name
        (dst / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    registry_src = Path(__file__).parents[1] / "work-queue" / "records" / "bank-registry.json"
    registry_dst = repo / ".survey/work-queue/records/bank-registry.json"
    registry_dst.parent.mkdir(parents=True, exist_ok=True)
    registry_dst.write_text(registry_src.read_text(encoding="utf-8"), encoding="utf-8")


def _status_descriptor(*, status="rejected", attempt="attempt-a", job="job-a", reason="source was withdrawn"):
    return {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "status": status,
        "attempt_id": attempt,
        "job_id": job,
        "claim_id": "claim-a",
        "worker_id": "worker-a",
        "worker_kind": "scheduled_chat",
        "paper_path": f"papers/inference/test/{job}.md",
        "reason": reason,
    }


class NonArtifactImmutableStatusTests(unittest.TestCase):
    def test_rejected_blocked_and_deferred_validate_without_record_bank(self):
        module = _load(SCRIPTS / "immutable_submission.py", "immutable_nonartifact_validate")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            for status in ("rejected", "blocked", "deferred"):
                with self.subTest(status=status):
                    descriptor = _status_descriptor(status=status)
                    validated = module.validate_descriptor(repo, descriptor)
                    self.assertEqual(validated["status"], status)
                    self.assertEqual(validated["reason"], "source was withdrawn")
                    self.assertNotIn("record_bank", validated)
                    self.assertNotIn("record_slots", validated)

    def test_nonartifact_status_requires_reason_and_rejects_partial_record_transport(self):
        module = _load(SCRIPTS / "immutable_submission.py", "immutable_nonartifact_invalid")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            missing_reason = _status_descriptor(reason="")
            with self.assertRaisesRegex(ValueError, "reason"):
                module.validate_descriptor(repo, missing_reason)

            partial = _status_descriptor()
            partial["record_bank"] = "a"
            with self.assertRaisesRegex(ValueError, "status-only"):
                module.validate_descriptor(repo, partial)

    def test_completed_submission_still_requires_registered_bank_and_five_slots(self):
        module = _load(SCRIPTS / "immutable_submission.py", "immutable_completed_strict")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            descriptor = _status_descriptor(status="completed")
            descriptor.pop("reason")
            with self.assertRaisesRegex(ValueError, "record_bank"):
                module.validate_descriptor(repo, descriptor)

    def test_failed_result_is_retryable_and_same_claim_rejected_job_reconciles(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_nonartifact_retry")

            descriptor = _status_descriptor()
            submission = repo / ".survey/work-queue/submissions/research/attempt-a.json"
            _write(submission, descriptor)
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a",
                "type": "research",
                "status": "rejected",
                "priority": 80,
                "completed_at": "2026-09-13T00:00:00+00:00",
                "blocker": "longer canonical rejection reason from an earlier durable path",
            })
            _write(repo / ".survey/work-queue/claims/job-a.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "claim_id": "claim-a",
                "worker_id": "worker-a",
                "worker_kind": "scheduled_chat",
                "expires_at": "2026-09-13T01:00:00+00:00",
            })
            result_path = repo / ".survey/work-queue/results/research/attempt-a.json"
            _write(result_path, {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": False,
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "job_type": "research",
                "job_status": None,
                "artifact": None,
                "submission": ".survey/work-queue/submissions/research/attempt-a.json",
                "error": "ValueError: record_bank must be registered",
                "processed_at": "2026-09-13T00:30:00+00:00",
            })

            result = module.process(repo, submission)

            self.assertTrue(result["ok"])
            self.assertTrue(result.get("reconciled"))
            self.assertEqual(result["job_status"], "rejected")
            self.assertIsNone(result["artifact"])
            persisted = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertTrue(persisted["ok"])
            self.assertEqual(persisted["job_status"], "rejected")

    def test_ready_job_accepts_status_only_rejection_without_rendering_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_nonartifact_ready")

            descriptor = _status_descriptor()
            submission = repo / ".survey/work-queue/submissions/research/attempt-a.json"
            _write(submission, descriptor)
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "research", "status": "ready", "priority": 80,
            })
            _write(repo / ".survey/work-queue/claims/job-a.json", {
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "claim_id": "claim-a",
                "worker_id": "worker-a",
                "worker_kind": "scheduled_chat",
                "expires_at": "2099-01-01T00:00:00+00:00",
            })

            result = module.process(repo, submission)

            self.assertTrue(result["ok"])
            self.assertEqual(result["job_status"], "rejected")
            self.assertIsNone(result["artifact"])
            job = json.loads((repo / ".survey/work-queue/jobs/job-a.json").read_text(encoding="utf-8"))
            self.assertEqual(job["status"], "rejected")
            self.assertEqual(job["blocker"], "source was withdrawn")
            self.assertEqual(job.get("status_submission"), ".survey/work-queue/submissions/research/attempt-a.json")

    def test_invalidated_legacy_claim_rejects_late_submission(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_invalidated_claim")

            descriptor = _status_descriptor()
            submission = repo / ".survey/work-queue/submissions/research/attempt-a.json"
            _write(submission, descriptor)
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "research", "status": "ready", "priority": 80,
            })
            _write(repo / ".survey/work-queue/claims/job-a.json", {
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "claim_id": "claim-a",
                "worker_id": "worker-a",
                "worker_kind": "scheduled_chat",
                "claimed_at": "2026-09-13T00:00:00+00:00",
                "expires_at": "2026-09-13T01:30:00+00:00",
                "lease_invalidated_at": "2026-09-13T03:00:00+00:00",
                "lease_invalidation_reason": "legacy scheduled_chat lease exceeded 5400-second cap",
            })

            with self.assertRaisesRegex(ValueError, "invalidated"):
                module.process(repo, submission)

            job = json.loads((repo / ".survey/work-queue/jobs/job-a.json").read_text(encoding="utf-8"))
            self.assertEqual(job["status"], "ready")


if __name__ == "__main__":
    unittest.main()
