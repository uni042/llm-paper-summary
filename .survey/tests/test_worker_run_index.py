from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import worker_run_index as mod  # noqa: E402


def write_json(root: Path, rel: str, value: object) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


class WorkerRunIndexTests(unittest.TestCase):
    def identity(self, worker: str = "scheduled-chat-00", slot: str = "00") -> dict[str, str]:
        start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=5)
        return {
            "worker_id": worker,
            "run_key": "run-shared",
            "scheduled_slot": slot,
            "actual_invocation_start": start.isoformat(),
        }

    def test_result_time_counts_current_invocation_not_claim_time(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            identity = self.identity()
            start = mod.parse_time(identity["actual_invocation_start"])
            assert start is not None
            claimed = start - dt.timedelta(hours=1)
            cache = mod.rebuild_cache(
                root,
                identity,
                candidate_inventory=80,
                work_mode="research",
                attempts={"attempt-a": claimed},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            descriptor = {
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "kind": "research",
                **identity,
            }
            descriptor_path = write_json(
                root, ".survey/work-queue/submissions/research/attempt-a.json", descriptor
            )
            self.assertTrue(mod.apply_descriptor(root, descriptor_path)["updated"])
            result_path = write_json(
                root,
                ".survey/work-queue/results/research/attempt-a.json",
                {
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "job_type": "research",
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": (start + dt.timedelta(seconds=10)).isoformat(),
                },
            )
            self.assertTrue(mod.apply_result(root, result_path)["updated"])
            cache = mod.load_cache(root, identity)
            assert cache is not None
            state = mod.cached_submission_state(cache)
            self.assertEqual(state["research_audit_completed_this_invocation"], 1)
            self.assertEqual(state["completed_attempt_ids_this_invocation"], ["attempt-a"])

    def test_descriptor_can_extend_start_of_run_cache_from_exact_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            identity = self.identity()
            start = mod.parse_time(identity["actual_invocation_start"])
            assert start is not None
            mod.rebuild_cache(
                root,
                identity,
                candidate_inventory=80,
                work_mode="research",
                attempts={},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            write_json(
                root,
                ".survey/work-queue/claims/job-new.json",
                {
                    "job_id": "job-new",
                    "attempt_id": "attempt-new",
                    "worker_id": identity["worker_id"],
                    "claimed_at": (start + dt.timedelta(seconds=30)).isoformat(),
                },
            )
            descriptor_path = write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-new.json",
                {
                    "attempt_id": "attempt-new",
                    "job_id": "job-new",
                    "kind": "research",
                    **identity,
                },
            )
            update = mod.apply_descriptor(root, descriptor_path)
            self.assertTrue(update["updated"])
            cache = mod.load_cache(root, identity)
            assert cache is not None
            self.assertTrue(cache["attempts"]["attempt-new"]["submitted"])
            self.assertEqual(
                cache["attempts"]["attempt-new"]["claimed_at"],
                (start + dt.timedelta(seconds=30)).isoformat(),
            )

    def test_rebuild_generation_does_not_roll_back_after_cache_loss(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            identity = self.identity()
            first = mod.rebuild_cache(
                root,
                identity,
                candidate_inventory=80,
                work_mode="research",
                attempts={},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            synthetic = {
                "schema_version": 1,
                "ok": True,
                "request_id": "snap-generation",
                "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                **identity,
            }
            mod.publish_latest(
                root,
                Path(".survey/work-queue/run-state/results/snap-generation.json"),
                synthetic,
                9,
            )
            mod.cache_path(root, identity).unlink()
            rebuilt = mod.rebuild_cache(
                root,
                identity,
                candidate_inventory=80,
                work_mode="research",
                attempts={},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            self.assertEqual(first["revision"], 1)
            self.assertEqual(rebuilt["revision"], 10)

    def test_old_result_cannot_roll_cache_back(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            identity = self.identity()
            start = mod.parse_time(identity["actual_invocation_start"])
            assert start is not None
            mod.rebuild_cache(
                root,
                identity,
                candidate_inventory=80,
                work_mode="research",
                attempts={"attempt-a": start},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            descriptor_path = write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-a.json",
                {"attempt_id": "attempt-a", "job_id": "job-a", "kind": "research", **identity},
            )
            mod.apply_descriptor(root, descriptor_path)
            result_path = write_json(
                root,
                ".survey/work-queue/results/research/attempt-a.json",
                {
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "job_type": "research",
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": (start + dt.timedelta(minutes=2)).isoformat(),
                },
            )
            mod.apply_result(root, result_path)
            write_json(
                root,
                ".survey/work-queue/results/research/attempt-a.json",
                {
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "job_type": "research",
                    "ok": False,
                    "job_status": None,
                    "retryable": True,
                    "processed_at": (start + dt.timedelta(minutes=1)).isoformat(),
                },
            )
            update = mod.apply_result(root, result_path)
            self.assertFalse(update["updated"])
            self.assertEqual(update["reason"], "stale_result_ignored")
            cache = mod.load_cache(root, identity)
            assert cache is not None
            state = mod.cached_submission_state(cache)
            self.assertEqual(state["research_audit_completed_this_invocation"], 1)
            self.assertFalse(state["submission_result_pending"])

    def test_parallel_workers_use_distinct_cache_files(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            left = self.identity("scheduled-chat-00", "00")
            right = self.identity("scheduled-chat-30", "30")
            mod.rebuild_cache(
                root,
                left,
                candidate_inventory=80,
                work_mode="research",
                attempts={},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            mod.rebuild_cache(
                root,
                right,
                candidate_inventory=80,
                work_mode="research",
                attempts={},
                claims={"active_assignment": False, "active_attempt_ids": []},
            )
            self.assertNotEqual(mod.cache_path(root, left), mod.cache_path(root, right))
            self.assertEqual(mod.load_cache(root, left)["worker_id"], "scheduled-chat-00")
            self.assertEqual(mod.load_cache(root, right)["worker_id"], "scheduled-chat-30")


if __name__ == "__main__":
    unittest.main()
