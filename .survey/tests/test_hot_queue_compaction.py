from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import compact_worker_hot_queue as mod  # noqa: E402


def write_json(root: Path, rel: str, value: object) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


class HotQueueCompactionTests(unittest.TestCase):
    def test_only_provably_settled_items_are_archived(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/completed-submission-requests/attempt-settled.json",
                {"kind": "research", "attempt_id": "attempt-settled", "job_id": "job-settled"},
            )
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-settled.json",
                {"kind": "research", "attempt_id": "attempt-settled", "job_id": "job-settled"},
            )
            write_json(
                root,
                ".survey/work-queue/completed-submission-requests/attempt-pending.json",
                {"kind": "research", "attempt_id": "attempt-pending", "job_id": "job-pending"},
            )

            now = dt.datetime.now(dt.timezone.utc)
            run_identity = {
                "request_id": "snap-1",
                "worker_id": "scheduled-chat-00",
                "run_key": "run-1",
                "scheduled_slot": "00",
                "actual_invocation_start": (now - dt.timedelta(minutes=10)).isoformat(),
            }
            write_json(root, ".survey/work-queue/run-state/requests/snap-1.json", run_identity)
            write_json(
                root,
                ".survey/work-queue/run-state/results/snap-1.json",
                {**run_identity, "ok": True, "processed_at": now.isoformat()},
            )
            write_json(
                root,
                ".survey/work-queue/run-state/requests/snap-pending.json",
                {**run_identity, "request_id": "snap-pending"},
            )

            result = mod.compact(root, apply=True, preflight_result_retention_hours=0)
            self.assertTrue(result["ok"])
            self.assertFalse(
                (root / ".survey/work-queue/completed-submission-requests/attempt-settled.json").exists()
            )
            self.assertTrue(
                (
                    root
                    / ".survey/work-queue/completed-submission-requests/archive/attempt-settled.json"
                ).is_file()
            )
            self.assertTrue(
                (root / ".survey/work-queue/completed-submission-requests/attempt-pending.json").is_file()
            )
            self.assertFalse((root / ".survey/work-queue/run-state/requests/snap-1.json").exists())
            self.assertTrue((root / ".survey/work-queue/run-state/results/snap-1.json").is_file())
            self.assertTrue((root / ".survey/work-queue/run-state/requests/snap-pending.json").is_file())

    def test_settled_claim_request_moves_but_result_and_active_claim_stay(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            request = {
                "schema_version": 1,
                "request_id": "claim-1",
                "worker_id": "scheduled-chat-00",
            }
            write_json(root, ".survey/work-queue/claim-requests/claim-1.json", request)
            write_json(
                root,
                ".survey/work-queue/claim-results/claim-1.json",
                {
                    **request,
                    "ok": True,
                    "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                    "assignments": [
                        {
                            "job_id": "job-a",
                            "attempt_id": "attempt-a",
                            "worker_id": "scheduled-chat-00",
                        }
                    ],
                },
            )
            write_json(
                root,
                ".survey/work-queue/claims/job-a.json",
                {
                    "job_id": "job-a",
                    "attempt_id": "attempt-a",
                    "worker_id": "scheduled-chat-00",
                },
            )
            mod.compact(root, apply=True)
            self.assertTrue(
                (root / ".survey/work-queue/claim-requests/archive/claim-1.json").is_file()
            )
            self.assertTrue((root / ".survey/work-queue/claim-results/claim-1.json").is_file())
            self.assertTrue((root / ".survey/work-queue/claims/job-a.json").is_file())

    def test_preflight_pass_archives_only_after_descriptor_and_retention(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checked = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=3)
            request = {
                "request_id": "pre-1",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "kind": "research",
            }
            write_json(root, ".survey/work-queue/research-preflight/requests/pre-1.json", request)
            write_json(
                root,
                ".survey/work-queue/research-preflight/results/pre-1.json",
                {
                    **request,
                    "ok": True,
                    "preflight_passed": True,
                    "checked_at": checked.isoformat(),
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-a.json",
                {"attempt_id": "attempt-a", "job_id": "job-a", "kind": "research"},
            )

            repair = {
                "request_id": "pre-repair",
                "attempt_id": "attempt-b",
                "job_id": "job-b",
                "kind": "research",
            }
            write_json(root, ".survey/work-queue/research-preflight/requests/pre-repair.json", repair)
            write_json(
                root,
                ".survey/work-queue/research-preflight/results/pre-repair.json",
                {
                    **repair,
                    "ok": True,
                    "preflight_passed": False,
                    "repair_required": True,
                    "checked_at": checked.isoformat(),
                },
            )

            mod.compact(root, apply=True, preflight_result_retention_hours=2)
            self.assertTrue(
                (root / ".survey/work-queue/research-preflight/archive/requests/pre-1.json").is_file()
            )
            self.assertTrue(
                (root / ".survey/work-queue/research-preflight/archive/results/pre-1.json").is_file()
            )
            self.assertTrue(
                (root / ".survey/work-queue/research-preflight/results/pre-repair.json").is_file()
            )

    def test_malformed_history_does_not_stop_other_compaction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            malformed = root / ".survey/work-queue/completed-submission-requests/bad.json"
            malformed.parent.mkdir(parents=True, exist_ok=True)
            malformed.write_text("{bad", encoding="utf-8")
            write_json(
                root,
                ".survey/work-queue/completed-submission-requests/attempt-ok.json",
                {"kind": "audit", "attempt_id": "attempt-ok", "job_id": "job-ok"},
            )
            write_json(
                root,
                ".survey/work-queue/submissions/audit/attempt-ok.json",
                {"kind": "audit", "attempt_id": "attempt-ok", "job_id": "job-ok"},
            )
            result = mod.compact(root, apply=True, preflight_result_retention_hours=0)
            self.assertTrue(malformed.is_file())
            self.assertTrue(
                (
                    root
                    / ".survey/work-queue/completed-submission-requests/archive/attempt-ok.json"
                ).is_file()
            )
            self.assertEqual(result["error_count"], 0)


if __name__ == "__main__":
    unittest.main()
