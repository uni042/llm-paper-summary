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

    def test_request_rejects_cross_worker_slot(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "snap-1.json"
            value = request("scheduled-chat-00", "30")
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "scheduled-chat-00"):
                mod._normalize_request(path, value)


if __name__ == "__main__":
    unittest.main()
