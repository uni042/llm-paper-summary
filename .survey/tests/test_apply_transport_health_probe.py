from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "apply_transport_health_probe.py"


def load_module():
    spec = importlib.util.spec_from_file_location("apply_transport_health_probe_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ApplyTransportHealthProbeTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def _fixture(self, root: Path):
        job_id = "job-probe"
        claim_id = "claim-probe"
        attempt_id = "attempt-probe"
        write_json(
            root / ".survey/work-queue/jobs" / f"{job_id}.json",
            {
                "schema_version": 1,
                "job_id": job_id,
                "type": "research",
                "status": "ready",
            },
        )
        write_json(
            root / ".survey/work-queue/claims" / f"{job_id}.json",
            {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": job_id,
                "claim_id": claim_id,
                "attempt_id": attempt_id,
                "worker_id": "scheduled-chat-30",
                "worker_kind": "scheduled_chat",
                "kind": "research",
                "expires_at": "2099-01-01T00:00:00+00:00",
            },
        )
        probe = {
            "schema_version": 1,
            "kind": "github_write_health_probe",
            "probe_id": "probe-update-only-1",
            "target_path": ".survey/work-queue/transport/health-probe.json",
            "worker_id": "scheduled-chat-30",
            "scheduled_slot": "30",
            "run_key": "run-probe",
            "actual_invocation_start": "2026-09-25T03:00:00+00:00",
            "write_blocked_job": {
                "job_id": job_id,
                "claim_id": claim_id,
                "attempt_id": attempt_id,
                "reason": self.mod.run_state.WRITE_BLOCKED_REASON,
                "source_reason": "primary_full_text_unavailable",
            },
        }
        write_json(root / self.mod.PROBE_REL, probe)
        return job_id, claim_id, attempt_id, probe

    def test_update_only_probe_blocks_job_releases_claim_and_preserves_source_reason(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id, _, _, _ = self._fixture(root)
            result = self.mod.process(root)
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "quarantined")
            self.assertEqual(result["next_action"], "CONTINUE_NEXT_RESEARCH_AUDIT")
            self.assertEqual(result["write_blocked_job"]["status"], "blocked")

            job = json.loads(
                (root / ".survey/work-queue/jobs" / f"{job_id}.json").read_text(encoding="utf-8")
            )
            claim = json.loads(
                (root / ".survey/work-queue/claims" / f"{job_id}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(job["status"], "blocked")
            self.assertEqual(job["blocker"], "primary_full_text_unavailable")
            self.assertEqual(
                job["write_blocked_transport_reason"],
                self.mod.run_state.WRITE_BLOCKED_REASON,
            )
            self.assertIn("retry_not_before", job)
            self.assertIn("released_at", claim)
            self.assertEqual(
                claim["release_reason"],
                self.mod.run_state.WRITE_BLOCKED_REASON,
            )

    def test_same_probe_is_idempotent_after_result_is_durable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._fixture(root)
            first = self.mod.process(root)
            second = self.mod.process(root)
            self.assertEqual(first["probe_id"], second["probe_id"])
            self.assertTrue(second["reused"])
            self.assertEqual(second["write_blocked_job"]["status"], "blocked")

    def test_wrong_worker_cannot_quarantine_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id, _, _, probe = self._fixture(root)
            probe["worker_id"] = "scheduled-chat-00"
            write_json(root / self.mod.PROBE_REL, probe)
            result = self.mod.process(root)
            self.assertFalse(result["ok"])
            self.assertEqual(result["status"], "quarantine_not_applied")
            job = json.loads(
                (root / ".survey/work-queue/jobs" / f"{job_id}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(job["status"], "ready")

    def test_plain_health_probe_remains_valid_without_quarantine_command(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root / self.mod.PROBE_REL,
                {
                    "schema_version": 1,
                    "kind": "github_write_health_probe",
                    "probe_id": "probe-only",
                    "target_path": ".survey/work-queue/transport/health-probe.json",
                },
            )
            result = self.mod.process(root)
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "probe_observed")
            self.assertEqual(result["write_blocked_job"]["status"], "none")


if __name__ == "__main__":
    unittest.main()
