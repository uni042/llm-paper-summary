from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "compact_worker_transport.py"
spec = importlib.util.spec_from_file_location("compact_worker_transport", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def write_json(root: Path, rel: str, value: object) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


class WorkerTransportCompactionTests(unittest.TestCase):
    def test_settled_completed_request_archives_but_unsettled_stays(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            preflight = ".survey/work-queue/research-preflight/results/pre-a.json"
            write_json(
                root,
                preflight,
                {
                    "request_id": "pre-a",
                    "ok": True,
                    "preflight_passed": True,
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "kind": "research",
                    "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
            )
            write_json(
                root,
                ".survey/work-queue/completed-submission-requests/attempt-a.json",
                {
                    "kind": "research",
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "preflight_result": preflight,
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-a.json",
                {"kind": "research", "attempt_id": "attempt-a", "job_id": "job-a"},
            )
            write_json(
                root,
                ".survey/work-queue/completed-submission-requests/attempt-pending.json",
                {
                    "kind": "research",
                    "attempt_id": "attempt-pending",
                    "job_id": "job-pending",
                    "preflight_result": ".survey/work-queue/research-preflight/results/missing.json",
                },
            )
            result = mod.compact(root, apply=True, min_age_seconds=7200)
            self.assertTrue(result["ok"])
            self.assertFalse((root / ".survey/work-queue/completed-submission-requests/attempt-a.json").exists())
            self.assertTrue((root / ".survey/work-queue/archive/transport/completed-submission-requests/attempt-a.json").is_file())
            self.assertTrue((root / ".survey/work-queue/completed-submission-requests/attempt-pending.json").is_file())

    def test_repair_preflight_is_never_archived(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).isoformat()
            write_json(
                root,
                ".survey/work-queue/research-preflight/requests/pre-r.json",
                {"request_id": "pre-r"},
            )
            write_json(
                root,
                ".survey/work-queue/research-preflight/results/pre-r.json",
                {
                    "request_id": "pre-r",
                    "ok": True,
                    "preflight_passed": False,
                    "repair_required": True,
                    "checked_at": old,
                },
            )
            mod.compact(root, apply=True, min_age_seconds=0)
            self.assertTrue((root / ".survey/work-queue/research-preflight/requests/pre-r.json").is_file())
            self.assertTrue((root / ".survey/work-queue/research-preflight/results/pre-r.json").is_file())

    def test_old_settled_run_state_archives_except_latest_pointer(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).isoformat()
            for name in ("old", "latest"):
                write_json(
                    root,
                    f".survey/work-queue/run-state/requests/{name}.json",
                    {"request_id": name, "run_key": f"run-{name}", "worker_id": "scheduled-chat-00"},
                )
                write_json(
                    root,
                    f".survey/work-queue/run-state/results/{name}.json",
                    {
                        "request_id": name,
                        "run_key": f"run-{name}",
                        "worker_id": "scheduled-chat-00",
                        "ok": True,
                        "processed_at": old,
                    },
                )
            write_json(
                root,
                ".survey/work-queue/run-state/latest/scheduled-chat-00.json",
                {
                    "result_path": ".survey/work-queue/run-state/results/latest.json",
                },
            )
            mod.compact(root, apply=True, min_age_seconds=0)
            self.assertFalse((root / ".survey/work-queue/run-state/requests/old.json").exists())
            self.assertTrue((root / ".survey/work-queue/archive/transport/run-state/results/old.json").is_file())
            self.assertTrue((root / ".survey/work-queue/run-state/results/latest.json").is_file())

    def test_old_auto_run_state_archives_but_latest_auto_snapshot_stays_hot(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).isoformat()
            for name, generation in (("auto-old", 1), ("auto-latest", 2)):
                write_json(
                    root,
                    f".survey/work-queue/run-state/results/{name}.json",
                    {
                        "request_id": name,
                        "run_key": "run-auto",
                        "worker_id": "scheduled-chat-00",
                        "scheduled_slot": "00",
                        "actual_invocation_start": old,
                        "ok": True,
                        "auto_generated": True,
                        "snapshot_generation": generation,
                        "processed_at": old,
                    },
                )
            write_json(
                root,
                ".survey/work-queue/run-state/latest/scheduled-chat-00.json",
                {
                    "result_path": ".survey/work-queue/run-state/results/auto-latest.json",
                },
            )
            mod.compact(root, apply=True, min_age_seconds=0)
            self.assertFalse((root / ".survey/work-queue/run-state/results/auto-old.json").exists())
            self.assertTrue((root / ".survey/work-queue/archive/transport/run-state/results/auto-old.json").is_file())
            self.assertTrue((root / ".survey/work-queue/run-state/results/auto-latest.json").is_file())

    def test_claim_transport_requires_every_assignment_terminal(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)).isoformat()
            write_json(root, ".survey/work-queue/claim-requests/settled.json", {"request_id": "settled"})
            write_json(
                root,
                ".survey/work-queue/claim-results/settled.json",
                {
                    "request_id": "settled",
                    "processed_at": old,
                    "assignments": [{"job_id": "job-done", "attempt_id": "attempt-done", "kind": "research"}],
                },
            )
            write_json(root, ".survey/work-queue/jobs/job-done.json", {"status": "completed"})
            write_json(root, ".survey/work-queue/claim-requests/live.json", {"request_id": "live"})
            write_json(
                root,
                ".survey/work-queue/claim-results/live.json",
                {
                    "request_id": "live",
                    "processed_at": old,
                    "assignments": [{"job_id": "job-live", "attempt_id": "attempt-live", "kind": "research"}],
                },
            )
            write_json(root, ".survey/work-queue/jobs/job-live.json", {"status": "in_progress"})
            mod.compact(root, apply=True, min_age_seconds=0)
            self.assertFalse((root / ".survey/work-queue/claim-requests/settled.json").exists())
            self.assertTrue((root / ".survey/work-queue/archive/transport/claim-results/settled.json").is_file())
            self.assertTrue((root / ".survey/work-queue/claim-requests/live.json").is_file())
            self.assertTrue((root / ".survey/work-queue/claim-results/live.json").is_file())

    def test_poison_history_does_not_stop_other_compaction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            poison = root / ".survey/work-queue/completed-submission-requests/poison.json"
            poison.parent.mkdir(parents=True, exist_ok=True)
            poison.write_text("{broken", encoding="utf-8")
            result = mod.compact(root, apply=True, min_age_seconds=0)
            self.assertTrue(result["ok"])
            self.assertTrue(poison.is_file())


if __name__ == "__main__":
    unittest.main()
