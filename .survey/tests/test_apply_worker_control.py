from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "apply_worker_control.py"


def load_module():
    spec = importlib.util.spec_from_file_location("apply_worker_control_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ApplyWorkerControlTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_module()

    def _fixture(self, root: Path):
        now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
        rows = [
            ("job-front", "claim-front", "attempt-front", 3),
            ("job-standby", "claim-standby", "attempt-standby", 4),
        ]
        for job_id, claim_id, attempt_id, order in rows:
            write_json(
                root / ".survey/work-queue/jobs" / f"{job_id}.json",
                {"schema_version": 1, "job_id": job_id, "type": "research", "status": "ready"},
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
                    "pipeline_order": order,
                    "claimed_at": now.isoformat(),
                    "expires_at": (now + dt.timedelta(hours=2)).isoformat(),
                },
            )
        guard = self.mod.foreground_guard("job-front", "claim-front", "attempt-front")
        write_json(
            root / self.mod.CONTROL_DIR / "scheduled-chat-30.json",
            {
                "schema_version": 1,
                "kind": self.mod.KIND,
                "worker_id": "scheduled-chat-30",
                "seq": 1,
                "command": self.mod.COMMAND,
                "foreground_guard": guard,
            },
        )

    def test_minimal_update_only_control_quarantines_canonical_foreground_only(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._fixture(root)
            result = self.mod.process_control(root, "scheduled-chat-30")
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "quarantined")
            self.assertEqual(result["next_action"], "CONTINUE_NEXT_RESEARCH_AUDIT")
            front = json.loads((root / ".survey/work-queue/jobs/job-front.json").read_text())
            standby = json.loads((root / ".survey/work-queue/jobs/job-standby.json").read_text())
            claim = json.loads((root / ".survey/work-queue/claims/job-front.json").read_text())
            self.assertEqual(front["status"], "blocked")
            self.assertEqual(standby["status"], "ready")
            self.assertIn("released_at", claim)

    def test_guard_mismatch_never_quarantines_new_foreground(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._fixture(root)
            control_path = root / self.mod.CONTROL_DIR / "scheduled-chat-30.json"
            control = json.loads(control_path.read_text())
            control["foreground_guard"] = "0" * 64
            write_json(control_path, control)
            result = self.mod.process_control(root, "scheduled-chat-30")
            self.assertFalse(result["ok"])
            self.assertEqual(result["status"], "foreground_guard_mismatch")
            job = json.loads((root / ".survey/work-queue/jobs/job-front.json").read_text())
            self.assertEqual(job["status"], "ready")

    def test_same_sequence_is_idempotent_after_result_is_durable(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._fixture(root)
            first = self.mod.process_control(root, "scheduled-chat-30")
            second = self.mod.process_control(root, "scheduled-chat-30")
            self.assertEqual(first["control_digest"], second["control_digest"])
            self.assertTrue(second["reused"])

    def test_control_cannot_target_other_worker(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._fixture(root)
            path = root / self.mod.CONTROL_DIR / "scheduled-chat-30.json"
            control = json.loads(path.read_text())
            control["worker_id"] = "scheduled-chat-00"
            write_json(path, control)
            with self.assertRaises(ValueError):
                self.mod.process_control(root, "scheduled-chat-30")


if __name__ == "__main__":
    unittest.main()
