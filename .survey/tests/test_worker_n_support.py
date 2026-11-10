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

import claim_worker
import research_quality_preflight
import worker_identity
import worker_run_state_cache

spec = importlib.util.spec_from_file_location("derive_worker_n", SCRIPTS / "derive_worker_run_state.py")
derive = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(derive)
spec2 = importlib.util.spec_from_file_location("auto_worker_n", SCRIPTS / "auto_claim_from_run_state.py")
auto_claim = importlib.util.module_from_spec(spec2)
assert spec2.loader is not None
spec2.loader.exec_module(auto_claim)


class WorkerNSupportTests(unittest.TestCase):
    def test_identity_rules(self):
        self.assertTrue(worker_identity.is_supported_worker_id("worker-1"))
        self.assertTrue(worker_identity.identity_slot_valid("worker-42", "adhoc"))
        self.assertFalse(worker_identity.identity_slot_valid("worker-42", "00"))
        self.assertFalse(worker_identity.is_supported_worker_id("worker-alpha"))

    def test_run_state_accepts_worker_n(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "run-worker-7.json"
            value = {
                "schema_version": 1, "request_id": "run-worker-7",
                "run_key": "run-worker-7-1", "worker_id": "worker-7",
                "worker_kind": "scheduled_chat", "scheduled_slot": "adhoc",
                "actual_invocation_start": dt.datetime.now(dt.timezone.utc).isoformat(),
                "runtime_condition": "none",
            }
            path.write_text(json.dumps(value), encoding="utf-8")
            self.assertEqual(derive._normalize_request(path, value)["scheduled_slot"], "adhoc")

    def test_claim_accepts_worker_n_identity(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "claim-worker-9.json"
            value = {
                "schema_version": 1, "request_id": "claim-worker-9",
                "worker_id": "worker-9", "worker_kind": "scheduled_chat",
                "requested_at": "2026-09-23T12:00:00+00:00", "max_jobs": 1,
                "claim_window": 4, "lease_seconds": 5400, "job_types": ["research", "audit"],
                "run_key": "run-worker-9-1", "scheduled_slot": "adhoc",
                "actual_invocation_start": "2026-09-23T12:00:00+00:00",
            }
            out = claim_worker._normalize_request(path, value)
            self.assertEqual(out["claim_window"], 4)
            self.assertEqual(out["scheduled_slot"], "adhoc")

    def test_preflight_accepts_worker_n_identity(self):
        out = research_quality_preflight._run_identity({
            "worker_id": "worker-11", "run_key": "run-worker-11-1",
            "scheduled_slot": "adhoc",
            "actual_invocation_start": "2026-09-23T12:00:00+00:00",
        })
        self.assertEqual(out["worker_id"], "worker-11")

    def test_cache_accepts_worker_n(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            req = {
                "worker_id": "worker-12", "run_key": "run-worker-12-1",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": "2026-09-23T12:00:00+00:00",
            }
            worker_run_state_cache.store_canonical_snapshot(
                root, req, candidate_inventory=60, work_mode="research",
                claims={
                    "claim_state_checked": True, "claim_result_pending": False,
                    "pending_claim_request_ids": [], "pending_claim_request_ages_seconds": {},
                    "pending_claim_requested_at": {}, "claim_result_pending_age_seconds": 0,
                    "claim_monitor_window_seconds": 60, "active_assignment": False,
                    "active_job_ids": [], "active_claim_count": 0, "claim_window": 4,
                    "claim_window_remaining": 4, "foreground_job_id": None, "standby_job_ids": [],
                },
                submission={
                    "research_audit_completed_this_invocation": 0, "submission_state_checked": True,
                    "submission_result_pending": False, "pipeline_ahead_count": 0,
                    "last_terminal_job_status": "none", "submitted_attempt_ids": [],
                    "pending_attempt_ids": [], "completed_attempt_ids": [],
                    "retryable_attempt_ids": [], "repair_required_attempt_ids": [], "attempt_facts": {},
                },
            )
            self.assertIsNotNone(worker_run_state_cache.get_run(root, req))

    def test_auto_initial_claim_accepts_worker_n(self):
        value = {
            "ok": True, "snapshot_origin": "request-fast-lane", "work_mode": "research",
            "worker_id": "worker-13", "run_key": "run-worker-13-1",
            "scheduled_slot": "adhoc", "actual_invocation_start": "2026-09-23T12:00:00+00:00",
            "active_assignment": False, "claim_result_pending": False,
            "research_audit_completed_this_invocation": 0, "submitted_attempt_ids": [],
            "seconds_to_run_deadline": 3500, "gate": {"required_action": "CLAIM_NEXT_RESEARCH_AUDIT"},
        }
        self.assertTrue(auto_claim._eligible(value))
        req = auto_claim._claim_request(value, "auto-worker-13")
        self.assertEqual(req["worker_id"], "worker-13")
        self.assertEqual(req["scheduled_slot"], "adhoc")


if __name__ == "__main__":
    unittest.main()
