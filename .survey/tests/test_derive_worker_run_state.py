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
SCRIPT = SCRIPTS / "derive_worker_run_state.py"
spec = importlib.util.spec_from_file_location("derive_worker_run_state", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def write_json(root: Path, rel: str, value: object) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def request(worker_id: str = "scheduled-chat-00", slot: str = "00") -> dict:
    start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)
    return {
        "schema_version": 1,
        "request_id": "snap-1",
        "run_key": "run-1",
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "scheduled_slot": slot,
        "actual_invocation_start": start.isoformat(),
        "runtime_condition": "none",
    }


class DeriveWorkerRunStateTests(unittest.TestCase):
    def test_normal_route_is_derived_from_inventory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {
                    "claiming": {"ready_research_audit": 60, "claimable": 60},
                    "counts": {"research": {"ready": 60}, "audit": {"ready": 0}},
                },
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            result = mod.derive(root, request())
            self.assertEqual(result["candidate_inventory"], 60)
            self.assertEqual(result["work_mode"], "research")
            self.assertTrue(result["claim_state_checked"])
            self.assertTrue(result["submission_state_checked"])

    def test_0830_slot_forces_maintenance_route(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 100, "claimable": 100}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            result = mod.derive(root, request("scheduled-chat-30", "0830"))
            self.assertEqual(result["work_mode"], "maintenance")
            self.assertEqual(result["gate"]["decision"], "CONTINUE")
            self.assertEqual(result["gate"]["required_action"], "RUN_0830_MAINTENANCE")

    def test_unavailable_durable_transports_are_hard_stop(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["runtime_condition"] = "durable_transports_unavailable"
            value["runtime_condition_confirmed"] = True
            value["runtime_condition_attempts"] = 2
            value["runtime_condition_detail"] = "two failed durable transport recovery attempts"
            result = mod.derive(root, value)
            self.assertEqual(result["gate"]["decision"], "STOP_RUN")
            self.assertIn("all_remaining_work_blocked_after_fallback_consideration", result["gate"]["stop_reasons"])

    def test_single_transient_runtime_failure_is_downgraded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["runtime_condition"] = "github_read_unavailable"
            value["runtime_condition_confirmed"] = False
            value["runtime_condition_attempts"] = 1
            result = mod.derive(root, value)
            self.assertEqual(result["runtime_condition"], "none")
            self.assertIsNotNone(result["runtime_condition_ignored_reason"])

    def test_fresh_pending_claim_exposes_age_and_monitor_action(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            requested_at = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=20)
            write_json(
                root,
                ".survey/work-queue/claim-requests/claim-pending.json",
                {
                    "schema_version": 1,
                    "request_id": "claim-pending",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "requested_at": requested_at.isoformat(),
                    "max_jobs": 1,
                    "job_types": ["research", "audit"],
                },
            )
            result = mod.derive(root, value)
            self.assertTrue(result["claim_result_pending"])
            self.assertIn("claim-pending", result["pending_claim_request_ids"])
            self.assertGreaterEqual(result["claim_result_pending_age_seconds"], 0)
            self.assertLess(result["claim_result_pending_age_seconds"], 60)
            self.assertEqual(result["claim_monitor_window_seconds"], 60)
            self.assertEqual(result["gate"]["required_action"], "MONITOR_CLAIM_FAST_LANE")

    def test_old_pending_claim_falls_back_to_long_wait_monitoring(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=3)
            value["actual_invocation_start"] = start.isoformat()
            requested_at = dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=75)
            write_json(
                root,
                ".survey/work-queue/claim-requests/claim-old.json",
                {
                    "schema_version": 1,
                    "request_id": "claim-old",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "requested_at": requested_at.isoformat(),
                    "max_jobs": 1,
                    "job_types": ["research", "audit"],
                },
            )
            result = mod.derive(root, value)
            self.assertGreaterEqual(result["claim_result_pending_age_seconds"], 60)
            self.assertEqual(result["gate"]["required_action"], "WAIT_FOR_CLAIM_RESULT")

    def test_discovery_precheck_pending_is_tracked(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pre-1.json",
                {"request_id": "pre-1", "run_key": "run-1"},
            )
            result = mod.derive(root, request())
            self.assertTrue(result["discovery_precheck_result_pending"])
            self.assertEqual(result["gate"]["required_action"], "WAIT_FOR_DISCOVERY_PRECHECK_RESULT")

    def test_successful_precheck_without_submission_is_evaluation_pending(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pre-1.json",
                {"request_id": "pre-1", "run_key": "run-1"},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-1.json",
                {
                    "request_id": "pre-1",
                    "run_key": "run-1",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                },
            )
            result = mod.derive(root, request())
            self.assertTrue(result["discovery_evaluation_pending"])
            self.assertEqual(result["gate"]["required_action"], "CONTINUE_DISCOVERY_ROUND")

    def test_split_discovery_round_missing_part_remains_in_progress(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pre-1.json",
                {"request_id": "pre-1", "run_key": "run-1"},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-1.json",
                {
                    "request_id": "pre-1",
                    "run_key": "run-1",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/round-part-1.json",
                {
                    "operation": "submit_discovery_round",
                    "discovery_precheck": {"request_id": "pre-1"},
                    "discovery_stats": {
                        "run_key": "run-1",
                        "round": "round-1",
                        "axis": "forward",
                        "round_submission_index": 1,
                        "round_submission_count": 2,
                    },
                    "candidates": [],
                },
            )
            write_json(root, ".survey/work-queue/results/round-part-1.json", {"ok": True})
            result = mod.derive(root, request())
            self.assertTrue(result["discovery_evaluation_pending"])
            self.assertIn("pre-1", result["discovery_evaluation_request_ids"])
            self.assertEqual(result["gate"]["required_action"], "CONTINUE_DISCOVERY_ROUND")

    def test_prior_run_unresolved_submission_remains_pending(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            old = dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=2)
            write_json(
                root,
                ".survey/work-queue/claim-results/old.json",
                {
                    "worker_id": "scheduled-chat-00",
                    "assignments": [{"attempt_id": "attempt-old", "claimed_at": old.isoformat()}],
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-old.json",
                {"attempt_id": "attempt-old", "job_id": "job-old"},
            )
            result = mod.derive(root, request())
            self.assertTrue(result["submission_result_pending"])
            self.assertIn("attempt-old", result["pending_attempt_ids"])

    def test_unresolved_descriptor_survives_missing_claim_result(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-orphan.json",
                {
                    "attempt_id": "attempt-orphan",
                    "job_id": "job-orphan",
                    "worker_id": "scheduled-chat-00",
                },
            )
            result = mod.derive(root, request())
            self.assertTrue(result["submission_result_pending"])
            self.assertIn("attempt-orphan", result["pending_attempt_ids"])

    def test_cached_active_assignment_is_cleared_when_job_is_terminal(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/jobs/job-terminal.json",
                {"job_id": "job-terminal", "type": "research", "status": "blocked"},
            )
            write_json(
                root,
                ".survey/work-queue/run-state/cache/scheduled-chat-00.json",
                {
                    "schema_version": 1,
                    "worker_id": "scheduled-chat-00",
                    "generation": 1,
                    "fact_generation": 0,
                    "runs": {
                        "run-1": {
                            "worker_id": "scheduled-chat-00",
                            "run_key": "run-1",
                            "scheduled_slot": "00",
                            "actual_invocation_start": value["actual_invocation_start"],
                            "cache_valid": True,
                            "candidate_inventory": 60,
                            "work_mode": "research",
                            "claims": {
                                "claim_state_checked": True,
                                "claim_result_pending": False,
                                "pending_claim_request_ids": [],
                                "pending_claim_request_ages_seconds": {},
                                "pending_claim_requested_at": {},
                                "claim_result_pending_age_seconds": 0,
                                "claim_monitor_window_seconds": 60,
                                "active_assignment": True,
                                "active_job_ids": ["job-terminal"],
                            },
                            "submission": {
                                "research_audit_completed_this_invocation": 0,
                                "submission_state_checked": True,
                                "submission_result_pending": False,
                                "pipeline_ahead_count": 0,
                                "last_terminal_job_status": "blocked",
                                "submitted_attempt_ids": [],
                                "pending_attempt_ids": [],
                                "completed_attempt_ids": [],
                                "retryable_attempt_ids": [],
                                "repair_required_attempt_ids": [],
                            },
                            "attempts": {},
                            "generation": 1,
                        }
                    },
                },
            )
            result = mod.derive(root, value)
            self.assertEqual(result["run_state_source"], "incremental_cache")
            self.assertFalse(result["active_assignment"])
            self.assertEqual(result["active_job_ids"], [])
            self.assertEqual(result["gate"]["required_action"], "CLAIM_NEXT_RESEARCH_AUDIT")
            repaired_cache = json.loads(
                (root / ".survey/work-queue/run-state/cache/scheduled-chat-00.json").read_text(encoding="utf-8")
            )
            repaired_claims = repaired_cache["runs"]["run-1"]["claims"]
            self.assertFalse(repaired_claims["active_assignment"])
            self.assertEqual(repaired_claims["active_job_ids"], [])

    def test_request_rejects_cross_worker_slot(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "snap-1.json"
            value = request("scheduled-chat-00", "30")
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "scheduled-chat-00"):
                mod._normalize_request(path, value)


    def test_active_foreground_exposes_variable_standby_slots_and_requests_nonblocking_refill(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            now = dt.datetime.now(dt.timezone.utc)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 59}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/jobs/job-active.json",
                {"job_id": "job-active", "type": "research", "status": "ready"},
            )
            write_json(
                root,
                ".survey/work-queue/claims/job-active.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "job_id": "job-active",
                    "claim_id": "claim-active",
                    "attempt_id": "attempt-active",
                    "request_id": "req-active",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "kind": "research",
                    "pipeline_order": 0,
                    "claimed_at": now.isoformat(),
                    "expires_at": (now + dt.timedelta(hours=1)).isoformat(),
                },
            )
            result = mod.derive(root, value)
            self.assertTrue(result["active_assignment"])
            self.assertEqual(result["active_claim_count"], 1)
            self.assertEqual(result["claim_window"], mod.SCHEDULED_CHAT_CLAIM_WINDOW)
            self.assertEqual(result["claim_window_remaining"], mod.SCHEDULED_CHAT_CLAIM_WINDOW - 1)
            self.assertEqual(result["foreground_job_id"], "job-active")
            self.assertEqual(result["standby_job_ids"], [])
            self.assertEqual(
                result["gate"]["required_action"],
                "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY",
            )

if __name__ == "__main__":
    unittest.main()
