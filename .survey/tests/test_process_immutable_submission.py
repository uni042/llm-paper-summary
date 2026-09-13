import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS = Path(__file__).parents[1] / "scripts"
SLOTS = ("metadata", "problem_method", "evaluation", "results", "positioning")


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
        if src.exists():
            (dst / name).write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    registry_src = Path(__file__).parents[1] / "work-queue" / "records" / "bank-registry.json"
    registry_dst = repo / ".survey/work-queue/records/bank-registry.json"
    registry_dst.parent.mkdir(parents=True, exist_ok=True)
    registry_dst.write_text(registry_src.read_text(encoding="utf-8"), encoding="utf-8")


def _make_descriptor(repo: Path, module, *, attempt="attempt-a", job="job-a", bank="a", expected_blob_sha=None):
    bank_root = ".survey/work-queue/records/chat-record" if bank == "a" else f".survey/work-queue/records/chat-record-{bank}"
    refs = []
    for slot in SLOTS:
        path = repo / bank_root / f"{slot}.json"
        _write(path, {
            "schema_version": 1,
            "transport_version": 10,
            "slot": slot,
            "attempt_id": attempt,
            "job_id": job,
            "data": {},
        })
        refs.append({
            "slot": slot,
            "path": path.relative_to(repo).as_posix(),
            "blob_sha": module.immutable_submission.git_blob_sha(path.read_bytes()),
        })
    descriptor = {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "attempt_id": attempt,
        "job_id": job,
        "record_bank": bank,
        "paper_path": f"papers/inference/test/{job}.md",
        "record_slots": refs,
    }
    if expected_blob_sha is not None:
        descriptor["expected_blob_sha"] = expected_blob_sha
    path = repo / f".survey/work-queue/submissions/research/{attempt}.json"
    _write(path, descriptor)
    return path


class ProcessImmutableSubmissionTests(unittest.TestCase):
    def test_processes_only_requested_descriptor_and_is_idempotent(self):
        self.assertTrue((SCRIPTS / "process_immutable_submission.py").exists(), "processor must exist")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_one")
            first = _make_descriptor(repo, module, attempt="attempt-a", job="job-a", bank="a")
            second = _make_descriptor(repo, module, attempt="attempt-b", job="job-b", bank="b")
            for job in ("job-a", "job-b"):
                _write(repo / f".survey/work-queue/jobs/{job}.json", {
                    "job_id": job,
                    "type": "research",
                    "status": "ready",
                    "priority": 80,
                    "created_at": "2026-09-13T00:00:00+00:00",
                })
            _write(repo / ".survey/work-queue/claims/job-a.json", {
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "claim_id": "claim-a",
                "worker_id": "worker-a",
                "worker_kind": "scheduled_chat",
                "expires_at": "2099-01-01T00:00:00+00:00",
            })

            fake_markdown = "# Paper\n\n" + ("日本語の検証本文です。" * 80)
            with mock.patch.object(module, "render_descriptor", return_value=fake_markdown), \
                 mock.patch.object(module.queue_worker, "apply_artifact", return_value={"paper": "papers/inference/test/job-a.md"}):
                result1 = module.process(repo, first)
                result2 = module.process(repo, first)

            self.assertTrue(result1["ok"])
            self.assertTrue(result2["ok"])
            self.assertTrue(result2.get("reused"))
            self.assertEqual(json.loads((repo / ".survey/work-queue/jobs/job-a.json").read_text())["status"], "completed")
            self.assertEqual(json.loads((repo / ".survey/work-queue/jobs/job-b.json").read_text())["status"], "ready")
            self.assertFalse((repo / ".survey/work-queue/results/research/attempt-b.json").exists())
            self.assertTrue(second.exists())

    def test_rejects_descriptor_when_current_claim_belongs_to_newer_attempt(self):
        self.assertTrue((SCRIPTS / "process_immutable_submission.py").exists(), "processor must exist")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_stale")
            path = _make_descriptor(repo, module, attempt="attempt-old", job="job-a")
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "research", "status": "ready", "priority": 80,
            })
            _write(repo / ".survey/work-queue/claims/job-a.json", {
                "job_id": "job-a", "attempt_id": "attempt-new", "claim_id": "claim-new",
                "worker_id": "worker-new", "worker_kind": "scheduled_chat",
                "expires_at": "2099-01-01T00:00:00+00:00",
            })
            with self.assertRaisesRegex(ValueError, "stale attempt"):
                module.process(repo, path)
            self.assertEqual(json.loads((repo / ".survey/work-queue/jobs/job-a.json").read_text())["status"], "ready")

    def test_stale_expected_paper_sha_is_rejected_before_publication(self):
        self.assertTrue((SCRIPTS / "process_immutable_submission.py").exists(), "processor must exist")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_sha")
            paper = repo / "papers/inference/test/job-a.md"
            paper.parent.mkdir(parents=True, exist_ok=True)
            paper.write_text("old paper\n", encoding="utf-8")
            path = _make_descriptor(repo, module, attempt="attempt-a", job="job-a", expected_blob_sha="0" * 40)
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "research", "status": "ready", "priority": 80,
            })
            _write(repo / ".survey/work-queue/claims/job-a.json", {
                "job_id": "job-a", "attempt_id": "attempt-a", "claim_id": "claim-a",
                "worker_id": "worker-a", "worker_kind": "scheduled_chat",
                "expires_at": "2099-01-01T00:00:00+00:00",
            })
            fake_markdown = "# Paper\n\n" + ("日本語の検証本文です。" * 80)
            with mock.patch.object(module, "render_descriptor", return_value=fake_markdown):
                with self.assertRaisesRegex(ValueError, "paper blob changed"):
                    module.process(repo, path)
            self.assertEqual(paper.read_text(encoding="utf-8"), "old paper\n")

    def test_main_persists_failure_result_before_returning_nonzero(self):
        self.assertTrue((SCRIPTS / "process_immutable_submission.py").exists(), "processor must exist")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_scripts(repo)
            module = _load(repo / ".survey/scripts/process_immutable_submission.py", "processor_failure")
            path = _make_descriptor(repo, module, attempt="attempt-fail", job="job-a")
            argv = [
                "process_immutable_submission.py",
                "--repo-root", str(repo),
                "--submission", str(path.relative_to(repo)),
            ]
            with mock.patch.object(module, "process", side_effect=ValueError("synthetic validation failure")), \
                 mock.patch.object(sys, "argv", argv):
                rc = module.main()
            self.assertNotEqual(rc, 0)
            result_path = repo / ".survey/work-queue/results/research/attempt-fail.json"
            self.assertTrue(result_path.exists())
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertFalse(result["ok"])
            self.assertEqual(result["attempt_id"], "attempt-fail")
            self.assertEqual(result["job_id"], "job-a")
            self.assertIn("synthetic validation failure", result["error"])


if __name__ == "__main__":
    unittest.main()
