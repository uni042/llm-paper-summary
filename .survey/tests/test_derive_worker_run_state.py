from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import tempfile
import unittest
from unittest import mock
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
                    "claiming": {"ready_research_audit": 300, "claimable": 300},
                    "counts": {"research": {"ready": 300}, "audit": {"ready": 0}},
                },
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            result = mod.derive(root, request())
            self.assertEqual(result["candidate_inventory"], 300)
            self.assertEqual(result["work_mode"], "research")
            self.assertTrue(result["claim_state_checked"])
            self.assertTrue(result["submission_state_checked"])
            self.assertIn("GitHub file create/update API or connector", result["transport_rule"])
            self.assertIn("actual write", result["transport_rule"])
            self.assertIn("finalization_gate", result)
            self.assertFalse(result["finalization_permit_issued"])
            self.assertFalse(result["stop_permit"]["issued"])
            self.assertTrue(result["stop_permit_required"])
            self.assertFalse(result["run_termination_allowed"])
            self.assertTrue(result["continuation_contract"]["must_consume_next_work_packet"])
            self.assertEqual(result["finalization_gate"]["decision"], "MUST_CONTINUE")
            self.assertNotIn("final_response_allowed", result)
            self.assertNotIn("worker_execution_directive", result)

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
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
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
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["runtime_condition"] = "github_read_unavailable"
            value["runtime_condition_confirmed"] = False
            value["runtime_condition_attempts"] = 1
            result = mod.derive(root, value)
            self.assertEqual(result["runtime_condition"], "none")
            self.assertIsNotNone(result["runtime_condition_ignored_reason"])

    def test_platform_context_limit_without_explicit_tool_rejection_is_downgraded(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["runtime_condition"] = "platform_context_limit"
            value["runtime_condition_confirmed"] = True
            value["runtime_condition_attempts"] = 1
            value["runtime_condition_detail"] = "one paper primary full text could not be retrieved"
            result = mod.derive(root, value)
            self.assertEqual(result["runtime_condition"], "none")
            self.assertEqual(
                result["runtime_condition_ignored_reason"],
                "platform_limit_requires_explicit_platform_tool_call_rejection_evidence",
            )
            self.assertEqual(result["gate"]["decision"], "CONTINUE")
            self.assertEqual(result["gate"]["required_action"], "CLAIM_NEXT_RESEARCH_AUDIT")

    def test_platform_context_limit_requires_actual_platform_rejection_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["runtime_condition"] = "platform_context_limit"
            value["runtime_condition_confirmed"] = True
            value["runtime_condition_attempts"] = 1
            value["runtime_condition_event"] = mod.PLATFORM_CONTEXT_LIMIT_EVENT
            value["runtime_condition_detail"] = "platform rejected a required tool call because the context/output limit was reached"
            result = mod.derive(root, value)
            self.assertEqual(result["runtime_condition"], "platform_context_limit")
            self.assertEqual(result["runtime_condition_event"], mod.PLATFORM_CONTEXT_LIMIT_EVENT)
            self.assertEqual(result["gate"]["decision"], "STOP_RUN")
            self.assertIn("platform_limit_reached", result["gate"]["stop_reasons"])

    def test_bare_finalization_permit_without_approved_stop_reason_is_not_enough(self):
        permit = mod._build_stop_permit(
            finalization_permit_issued=True,
            work_mode="research",
            runtime_condition="none",
            runtime_condition_confirmed=False,
            runtime_condition_attempts=0,
            runtime_condition_event="",
            runtime_condition_detail="",
            gate={"stop_reasons": [], "handoff_window_active": False, "final_handoff_active": False},
            processed_at=dt.datetime.now(dt.timezone.utc).isoformat(),
        )
        self.assertFalse(permit["issued"])
        self.assertEqual(permit["denied_reason"], "no_router_approved_stop_reason")

    def test_finalization_action_is_rewritten_when_stop_permit_is_missing(self):
        packet = mod._next_work_packet(
            Path("."),
            worker_id="scheduled-chat-00",
            gate={"required_action": "FINALIZE"},
            finalization_gate={
                "finalization_permit": {"issued": True},
                "next_action": "FINALIZE",
            },
            claims={},
            discovery_async={},
            discovery_preload=None,
            discovery_fallback_source=None,
            discovery_pipeline_preload=None,
            run_termination_allowed=False,
        )
        self.assertEqual(packet["kind"], "canonical_action")
        self.assertEqual(packet["action"], "REFRESH_AND_CONTINUE")


    def test_claim_next_packet_prefers_concrete_direct_take_even_with_pending_request(self):
        packet = mod._next_work_packet(
            Path("."),
            worker_id="scheduled-chat-00",
            gate={"required_action": "CLAIM_NEXT_RESEARCH_AUDIT"},
            finalization_gate={
                "finalization_permit": {"issued": False},
                "next_action": "CLAIM_NEXT_RESEARCH_AUDIT",
            },
            claims={
                "claim_result_pending": True,
                "pending_claim_request_ids": ["pending-claim-1"],
            },
            discovery_async={},
            discovery_preload=None,
            discovery_fallback_source=None,
            discovery_pipeline_preload=None,
            run_termination_allowed=False,
            research_direct_packet={
                "claim_id": "claim-hot",
                "job_id": "job-hot",
                "attempt_id": "attempt-hot",
                "take_path": ".survey/work-queue/direct-takes/research/claim-hot.json",
                "job": {
                    "job_id": "job-hot",
                    "type": "research",
                    "status": "ready",
                },
            },
        )
        self.assertEqual(packet["kind"], "research_direct_take")
        self.assertEqual(packet["claim_id"], "claim-hot")
        self.assertTrue(packet["direct_take_before_claim_result"])
        self.assertEqual(packet["pending_claim_request_ids"], ["pending-claim-1"])

    def test_safe_time_window_issues_explicit_stop_permit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["actual_invocation_start"] = (
                dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=55)
            ).isoformat()
            result = mod.derive(root, value)
            self.assertTrue(result["finalization_permit_issued"])
            self.assertTrue(result["stop_permit"]["issued"])
            self.assertEqual(result["stop_permit"]["category"], "time_window")
            self.assertTrue(result["run_termination_allowed"])
            self.assertFalse(result["continuation_contract"]["must_consume_next_work_packet"])

    def test_confirmed_platform_limit_uses_observed_limit_stop_permit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["runtime_condition"] = "platform_context_limit"
            value["runtime_condition_confirmed"] = True
            value["runtime_condition_attempts"] = 1
            value["runtime_condition_event"] = mod.PLATFORM_CONTEXT_LIMIT_EVENT
            value["runtime_condition_detail"] = "platform rejected a required tool call because the acquisition/output cap was reached"
            result = mod.derive(root, value)
            self.assertTrue(result["stop_permit"]["issued"])
            self.assertEqual(result["stop_permit"]["category"], "observed_acquisition_limit")
            self.assertTrue(result["run_termination_allowed"])


    def test_fresh_pending_claim_exposes_age_and_monitor_action(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
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
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
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

    def test_nested_discovery_submission_pending_is_tracked(self):
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
                ".survey/work-queue/discovery-precheck/requests/pre-nested.json",
                {"request_id": "pre-nested", "run_key": "run-1"},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-nested.json",
                {
                    "request_id": "pre-nested",
                    "run_key": "run-1",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/discovery/nested-round.json",
                {
                    "operation": "submit_discovery_round",
                    "discovery_precheck": {"request_id": "pre-nested"},
                    "discovery_stats": {
                        "run_key": "run-1",
                        "round": "round-nested",
                        "axis": "backward",
                        "round_submission_index": 1,
                        "round_submission_count": 1,
                    },
                    "candidates": [],
                },
            )

            result = mod.derive(root, request())

            self.assertTrue(result["discovery_submission_result_pending"])
            self.assertEqual(result["pending_discovery_submission_ids"], ["nested-round"])
            self.assertFalse(result["discovery_evaluation_pending"])
            self.assertEqual(result["gate"]["required_action"], "WAIT_FOR_DISCOVERY_SUBMISSION_RESULT")
            self.assertFalse(result["finalization_permit_issued"])
            self.assertNotIn("final_response_allowed", result)
            self.assertNotIn("worker_execution_directive", result)

    def test_latest_failed_precheck_still_requires_recovery(self):
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
                ".survey/work-queue/discovery-precheck/requests/pre-failed.json",
                {
                    "request_id": "pre-failed",
                    "run_key": "run-1",
                    "provider": "semantic_scholar",
                    "source_url": "https://api.semanticscholar.org/graph/v1/paper/search?query=test",
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-failed.json",
                {
                    "request_id": "pre-failed",
                    "run_key": "run-1",
                    "ok": False,
                    "evaluation_allowed": False,
                    "error": "HTTP 429",
                },
            )
            result = mod.derive(root, request())
            self.assertTrue(result["discovery_recovery_required"])
            self.assertIn("precheck:pre-failed", result["discovery_recovery_targets"])
            self.assertEqual(result["gate"]["required_action"], "RECOVER_DISCOVERY_SUBMISSION")

    def test_failed_precheck_is_historical_after_later_successful_precheck(self):
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
                ".survey/work-queue/discovery-precheck/requests/pre-old.json",
                {
                    "request_id": "pre-old",
                    "run_key": "run-1",
                    "provider": "semantic_scholar",
                    "source_url": "https://api.semanticscholar.org/graph/v1/paper/search?query=old",
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-old.json",
                {"request_id": "pre-old", "run_key": "run-1", "ok": False},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pre-new.json",
                {
                    "request_id": "pre-new",
                    "run_key": "run-1",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-new.json",
                {
                    "request_id": "pre-new",
                    "run_key": "run-1",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                },
            )
            order = {
                ".survey/work-queue/discovery-precheck/results/pre-old.json": 0,
                ".survey/work-queue/discovery-precheck/results/pre-new.json": 1,
            }
            with mock.patch.object(mod, "_git_introduction_order", return_value=order):
                result = mod.derive(root, request())
            self.assertFalse(result["discovery_recovery_required"])
            self.assertIn("precheck:pre-old", result["discovery_superseded_failure_targets"])
            self.assertTrue(result["discovery_evaluation_pending"])
            self.assertEqual(result["gate"]["required_action"], "CONTINUE_DISCOVERY_ROUND")

    def test_newer_failure_is_not_hidden_by_older_success(self):
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
                ".survey/work-queue/discovery-precheck/requests/pre-old-success.json",
                {
                    "request_id": "pre-old-success",
                    "run_key": "run-1",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-old-success.json",
                {
                    "request_id": "pre-old-success",
                    "run_key": "run-1",
                    "ok": True,
                    "evaluation_allowed": True,
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pre-new-failed.json",
                {
                    "request_id": "pre-new-failed",
                    "run_key": "run-1",
                    "provider": "semantic_scholar",
                    "source_url": "https://api.semanticscholar.org/graph/v1/paper/search?query=new",
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/pre-new-failed.json",
                {"request_id": "pre-new-failed", "run_key": "run-1", "ok": False},
            )
            order = {
                ".survey/work-queue/discovery-precheck/results/pre-old-success.json": 0,
                ".survey/work-queue/discovery-precheck/results/pre-new-failed.json": 1,
            }
            with mock.patch.object(mod, "_git_introduction_order", return_value=order):
                result = mod.derive(root, request())
            self.assertTrue(result["discovery_recovery_required"])
            self.assertIn("precheck:pre-new-failed", result["discovery_recovery_targets"])
            self.assertEqual(result["gate"]["required_action"], "RECOVER_DISCOVERY_SUBMISSION")

    def test_failed_submission_is_superseded_by_successful_replacement_round(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {
                    "schema_version": 3,
                    "history": [
                        {
                            "run_key": "run-1",
                            "round": "round-replacement",
                            "round_accounted": True,
                            "precheck_request_id": "pre-replacement",
                        }
                    ],
                },
            )
            for precheck_id in ("pre-failed", "pre-replacement"):
                write_json(
                    root,
                    f".survey/work-queue/discovery-precheck/requests/{precheck_id}.json",
                    {
                        "request_id": precheck_id,
                        "run_key": "run-1",
                        "provider": "repository_references",
                        "source_url": "repository://structured-references",
                    },
                )
                write_json(
                    root,
                    f".survey/work-queue/discovery-precheck/results/{precheck_id}.json",
                    {
                        "request_id": precheck_id,
                        "run_key": "run-1",
                        "ok": True,
                        "evaluation_allowed": True,
                    },
                )

            write_json(
                root,
                ".survey/work-queue/submissions/failed-round.json",
                {
                    "operation": "submit_discovery_round",
                    "discovery_precheck": {"request_id": "pre-failed"},
                    "discovery_stats": {
                        "run_key": "run-1",
                        "round": "round-failed",
                        "axis": "backward",
                    },
                    "candidates": [],
                },
            )
            write_json(
                root,
                ".survey/work-queue/results/failed-round.json",
                {
                    "ok": False,
                    "error_code": "discovery_precheck_required",
                    "error": "workflow provenance required",
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/replacement-round.json",
                {
                    "operation": "submit_discovery_round",
                    "discovery_precheck": {"request_id": "pre-replacement"},
                    "discovery_stats": {
                        "run_key": "run-1",
                        "round": "round-replacement",
                        "axis": "backward",
                    },
                    "candidates": [],
                },
            )
            write_json(
                root,
                ".survey/work-queue/results/replacement-round.json",
                {"ok": True, "ingested": True},
            )

            result = mod.derive(root, request())
            self.assertFalse(result["discovery_recovery_required"])
            self.assertIn("submission:failed-round", result["discovery_superseded_failure_targets"])
            self.assertEqual(result["discovery_rounds_completed"], 1)
            self.assertEqual(result["gate"]["required_action"], "DISCOVER_AGAIN")

    def test_prior_run_unresolved_submission_remains_pending(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
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
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
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
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
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


    def test_research_preflight_recovery_preserves_research_mode_below_threshold(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 10, "claimable": 10}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {"schema_version": 3, "history": []},
            )
            value = request()
            value["route_recovery_source"] = "research_preflight_identity"
            value["recovered_work_mode_at_start"] = "research"
            result = mod.derive(root, value)
            self.assertEqual(result["candidate_inventory"], 10)
            self.assertEqual(result["work_mode"], "research")
            self.assertEqual(result["route_source"], "research_preflight_recovery")
            self.assertFalse(result["candidate_inventory_at_start_exact"])
            self.assertFalse(result["finalization_permit_issued"])
            self.assertNotEqual(result["gate"]["required_action"], "DISCOVER_AGAIN")


    def test_discovery_precheck_recovery_preserves_mode_even_after_inventory_crosses_threshold(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 300}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            value = request()
            value["route_recovery_source"] = "discovery_precheck_identity"
            value["recovered_work_mode_at_start"] = "discovery"
            result = mod.derive(root, value)
            self.assertEqual(result["candidate_inventory"], 300)
            self.assertEqual(result["work_mode"], "discovery")
            self.assertEqual(result["route_source"], "discovery_precheck_recovery")
            self.assertFalse(result["candidate_inventory_at_start_exact"])
            self.assertFalse(result["finalization_permit_issued"])
            self.assertEqual(result["finalization_gate"]["decision"], "MUST_CONTINUE")
            self.assertEqual(result["gate"]["required_action"], "DISCOVER_AGAIN")


    def test_pending_backward_precheck_exposes_productive_forward_lookahead(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {
                    "schema_version": 3,
                    "history": [
                        {
                            "run_key": "old-run",
                            "round": "forward-seed",
                            "axis": "forward citations",
                            "provider": "semantic_scholar",
                            "source_url": "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2303.06865/citations",
                            "citation_direction": "forward",
                            "seed_canonical_id": "arXiv:2303.06865",
                            "candidate_count": 20,
                            "novel_candidate_count": 10,
                            "accepted_count": 4,
                            "round_accounted": True,
                        }
                    ],
                },
            )
            created = mod.discovery_preload_queue.top_up(root, target=2, max_new=2)
            self.assertEqual(created["created_count"], 2)
            entries = mod.discovery_preload_queue._entries(root)
            forward = next(row for row in entries if row["citation_direction"] == "forward")
            records = [
                {
                    "canonical_id": f"arXiv:2609.{index:05d}",
                    "title": f"Forward cached {index}",
                    "source_url": f"https://arxiv.org/abs/2609.{index:05d}",
                }
                for index in range(20)
            ]
            write_json(
                root,
                mod.discovery_preload_queue._result_path(forward).as_posix(),
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                    "request_id": forward["precheck_request_id"],
                    "run_key": f"preload:{forward['preload_id']}",
                    "results": records,
                    "allowed_records": [],
                    "unseen_result_count": 20,
                    "next_cursor": "20",
                    "provider_exhausted": False,
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pending-backward.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "pending-backward",
                    "collector_id": "pending-backward",
                    "run_key": "run-1",
                    "axis": "backward",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "target_unseen": 20,
                },
            )

            result = mod.derive(root, request())
            self.assertTrue(result["discovery_precheck_result_pending"])
            self.assertEqual(result["discovery_inflight_round_count"], 1)
            self.assertIn("backward", result["discovery_inflight_directions"])
            self.assertTrue(result["discovery_pipeline_work_available"])
            self.assertEqual(
                result["discovery_pipeline_preload"]["citation_direction"],
                "forward",
            )
            self.assertIn(
                ".survey/work-queue/discovery-preload/claims/",
                result["discovery_pipeline_preload"]["take_path"],
            )
            contract = result["discovery_pipeline_preload"]["direct_take_contract"]
            self.assertTrue(contract["create_only"])
            self.assertEqual(
                contract["payload_base"]["operation"],
                "direct_take_discovery",
            )
            self.assertEqual(
                contract["payload_base"]["worker_id"],
                "scheduled-chat-00",
            )
            self.assertEqual(
                contract["payload_base"]["run_key"],
                "run-1",
            )
            self.assertEqual(
                contract["required_runtime_fields"],
                ["request_id", "claimed_at", "lease_expires_at"],
            )
            self.assertEqual(
                result["next_work_packet"]["direct_take_contract"],
                contract,
            )
            self.assertEqual(
                result["gate"]["required_action"],
                "CONTINUE_DISCOVERY_PIPELINE",
            )
            self.assertEqual(
                result["finalization_gate"]["next_action"],
                "CONTINUE_DISCOVERY_PIPELINE",
            )


    def test_evaluable_discovery_round_exposes_concrete_next_work_packet(self):
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
                ".survey/work-queue/discovery-precheck/requests/eval-1.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "eval-1",
                    "run_key": "run-1",
                    "worker_id": "scheduled-chat-00",
                    "scheduled_slot": "00",
                    "actual_invocation_start": request()["actual_invocation_start"],
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "axis": "backward",
                    "citation_direction": "backward",
                    "requested_at": "2026-01-01T00:00:00+00:00",
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/results/eval-1.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "eval-1",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                    "allowed_records": [{"canonical_id": "arXiv:2609.00001"}],
                    "results": [{"canonical_id": "arXiv:2609.00001"}],
                    "receipt": "sha256:test",
                },
            )

            result = mod.derive(root, request())
            self.assertFalse(result["run_termination_allowed"])
            self.assertEqual(result["run_phase"], "running")
            self.assertEqual(result["continuation_next_action"], "CONTINUE_DISCOVERY_ROUND")
            self.assertEqual(result["next_action"], "CONTINUE_DISCOVERY_ROUND")
            self.assertEqual(result["next_work_packet"]["kind"], "discovery_evaluation")
            self.assertEqual(result["next_work_packet"]["request_id"], "eval-1")
            self.assertEqual(
                result["next_work_packet"]["result_path"],
                ".survey/work-queue/discovery-precheck/results/eval-1.json",
            )
            self.assertEqual(result["next_work_packet"]["allowed_record_count"], 1)

    def test_pipeline_lookahead_next_work_packet_is_concrete(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {
                    "schema_version": 3,
                    "history": [
                        {
                            "run_key": "old-run",
                            "round": "forward-seed",
                            "axis": "forward citations",
                            "provider": "semantic_scholar",
                            "source_url": "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2303.06865/citations",
                            "citation_direction": "forward",
                            "seed_canonical_id": "arXiv:2303.06865",
                            "candidate_count": 20,
                            "novel_candidate_count": 10,
                            "accepted_count": 4,
                            "round_accounted": True,
                        }
                    ],
                },
            )
            created = mod.discovery_preload_queue.top_up(root, target=2, max_new=2)
            self.assertEqual(created["created_count"], 2)
            entries = mod.discovery_preload_queue._entries(root)
            forward = next(row for row in entries if row["citation_direction"] == "forward")
            write_json(
                root,
                mod.discovery_preload_queue._result_path(forward).as_posix(),
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                    "request_id": forward["precheck_request_id"],
                    "run_key": f"preload:{forward['preload_id']}",
                    "results": [{"canonical_id": f"arXiv:2609.{index:05d}"} for index in range(20)],
                    "allowed_records": [],
                    "unseen_result_count": 20,
                },
            )
            write_json(
                root,
                ".survey/work-queue/discovery-precheck/requests/pending-backward.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "pending-backward",
                    "collector_id": "pending-backward",
                    "run_key": "run-1",
                    "axis": "backward",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "target_unseen": 20,
                },
            )

            result = mod.derive(root, request())
            self.assertEqual(result["next_action"], "CONTINUE_DISCOVERY_PIPELINE")
            self.assertEqual(result["next_work_packet"]["kind"], "discovery_pipeline_preload")
            self.assertEqual(
                result["next_work_packet"]["preload_id"],
                result["discovery_pipeline_preload"]["preload_id"],
            )
            self.assertFalse(result["run_termination_allowed"])

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
                {"claiming": {"ready_research_audit": 300, "claimable": 299}},
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


    def test_pending_research_preflight_parks_paper_and_promotes_standby(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            started = dt.datetime.fromisoformat(value["actual_invocation_start"])
            claimed = started + dt.timedelta(seconds=5)
            expires = claimed + dt.timedelta(hours=1)

            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 298}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {"schema_version": 3, "history": []},
            )
            for order, suffix in enumerate(("a", "b")):
                job_id = f"job-{suffix}"
                attempt_id = f"attempt-{suffix}"
                write_json(
                    root,
                    f".survey/work-queue/jobs/{job_id}.json",
                    {"job_id": job_id, "type": "research", "status": "ready"},
                )
                write_json(
                    root,
                    f".survey/work-queue/claims/{job_id}.json",
                    {
                        "schema_version": 1,
                        "workflow_version": 10,
                        "job_id": job_id,
                        "claim_id": f"claim-{suffix}",
                        "attempt_id": attempt_id,
                        "request_id": "claim-window",
                        "worker_id": "scheduled-chat-00",
                        "worker_kind": "scheduled_chat",
                        "kind": "research",
                        "pipeline_order": order,
                        "claimed_at": claimed.isoformat(),
                        "expires_at": expires.isoformat(),
                        "run_key": "run-1",
                        "scheduled_slot": "00",
                        "actual_invocation_start": value["actual_invocation_start"],
                    },
                )

            preflight_id = "scheduled-chat-00-attempt-a-r1"
            write_json(
                root,
                f".survey/work-queue/research-preflight/requests/{preflight_id}.json",
                {
                    "schema_version": 1,
                    "operation": "research_quality_preflight",
                    "request_id": preflight_id,
                    "kind": "research",
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "record_bank": "a",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "run-1",
                    "scheduled_slot": "00",
                    "actual_invocation_start": value["actual_invocation_start"],
                    "requested_at": (claimed + dt.timedelta(seconds=10)).isoformat(),
                },
            )

            pending = mod.derive(root, value)
            self.assertEqual(pending["active_claim_count"], 2)
            self.assertEqual(pending["foreground_job_id"], "job-b")
            self.assertEqual(pending["preflight_parked_job_ids"], ["job-a"])
            self.assertEqual(
                pending["preflight_parked_states"]["job-a"],
                "pending",
            )
            self.assertTrue(pending["active_assignment"])

            write_json(
                root,
                f".survey/work-queue/research-preflight/results/{preflight_id}.json",
                {
                    "schema_version": 1,
                    "operation": "research_quality_preflight",
                    "request_id": preflight_id,
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "ok": True,
                    "preflight_passed": False,
                    "repair_required": True,
                    "checked_at": (claimed + dt.timedelta(seconds=20)).isoformat(),
                },
            )

            failed = mod.derive(root, value)
            self.assertEqual(failed["foreground_job_id"], "job-a")
            self.assertEqual(failed["preflight_parked_job_ids"], [])
            self.assertEqual(failed["active_claim_count"], 2)



    def test_auto_snapshot_from_preflight_fail_restores_repair_foreground(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            started = dt.datetime.fromisoformat(value["actual_invocation_start"])
            claimed = started + dt.timedelta(seconds=5)
            expires = claimed + dt.timedelta(hours=1)

            # Current inventory has dropped below the normal Research threshold;
            # the preflight identity must still preserve this invocation's mode.
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 20, "claimable": 18}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {"schema_version": 3, "history": []},
            )
            for order, suffix in enumerate(("a", "b")):
                write_json(
                    root,
                    f".survey/work-queue/jobs/job-{suffix}.json",
                    {"job_id": f"job-{suffix}", "type": "research", "status": "ready"},
                )
                write_json(
                    root,
                    f".survey/work-queue/claims/job-{suffix}.json",
                    {
                        "schema_version": 1,
                        "workflow_version": 10,
                        "job_id": f"job-{suffix}",
                        "claim_id": f"claim-{suffix}",
                        "attempt_id": f"attempt-{suffix}",
                        "request_id": "claim-window",
                        "worker_id": "scheduled-chat-00",
                        "worker_kind": "scheduled_chat",
                        "kind": "research",
                        "pipeline_order": order,
                        "claimed_at": claimed.isoformat(),
                        "expires_at": expires.isoformat(),
                        "run_key": "run-1",
                        "scheduled_slot": "00",
                        "actual_invocation_start": value["actual_invocation_start"],
                    },
                )

            preflight_id = "scheduled-chat-00-attempt-a-r1"
            request_path = (
                f".survey/work-queue/research-preflight/requests/{preflight_id}.json"
            )
            result_path = (
                f".survey/work-queue/research-preflight/results/{preflight_id}.json"
            )
            write_json(
                root,
                request_path,
                {
                    "schema_version": 1,
                    "operation": "research_quality_preflight",
                    "request_id": preflight_id,
                    "kind": "research",
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "record_bank": "a",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "run-1",
                    "scheduled_slot": "00",
                    "actual_invocation_start": value["actual_invocation_start"],
                    "requested_at": (claimed + dt.timedelta(seconds=10)).isoformat(),
                },
            )
            write_json(
                root,
                result_path,
                {
                    "schema_version": 1,
                    "operation": "research_quality_preflight",
                    "request_id": preflight_id,
                    "kind": "research",
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "record_bank": "a",
                    "worker_id": "scheduled-chat-00",
                    "run_key": "run-1",
                    "scheduled_slot": "00",
                    "actual_invocation_start": value["actual_invocation_start"],
                    "ok": True,
                    "preflight_passed": False,
                    "repair_required": True,
                    "checked_at": (claimed + dt.timedelta(seconds=20)).isoformat(),
                },
            )
            paths = root / "preflight-results.txt"
            paths.write_text(result_path + "\n", encoding="utf-8")

            auto = mod.auto_snapshot_from_preflight_results(root, paths)
            self.assertEqual(auto["observed_preflight_results"], 1)
            self.assertEqual(auto["affected_runs"], 1)
            self.assertEqual(
                auto["fallback_recovery_runs"],
                ["scheduled-chat-00:run-1"],
            )
            self.assertEqual(len(auto["generated_results"]), 1)

            snapshot = json.loads(
                (root / auto["generated_results"][0]).read_text(encoding="utf-8")
            )
            self.assertEqual(snapshot["work_mode"], "research")
            self.assertEqual(snapshot["route_source"], "research_preflight_recovery")
            self.assertEqual(snapshot["snapshot_origin"], "research-preflight-fast-lane")
            self.assertTrue(snapshot["auto_generated"])
            self.assertEqual(snapshot["foreground_job_id"], "job-a")
            self.assertEqual(snapshot["preflight_repair_job_ids"], ["job-a"])
            self.assertEqual(snapshot["preflight_parked_job_ids"], [])
            self.assertEqual(snapshot["standby_job_ids"], ["job-b"])
            self.assertFalse(snapshot["finalization_permit_issued"])


    def test_preflight_window_is_admission_limit_not_thaw_limit(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            started = dt.datetime.fromisoformat(value["actual_invocation_start"])
            claimed = started + dt.timedelta(seconds=5)
            expires = claimed + dt.timedelta(hours=1)

            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 296}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {"schema_version": 3, "history": []},
            )
            for order, suffix in enumerate(("a", "b", "c", "d")):
                job_id = f"job-{suffix}"
                attempt_id = f"attempt-{suffix}"
                write_json(
                    root,
                    f".survey/work-queue/jobs/{job_id}.json",
                    {"job_id": job_id, "type": "research", "status": "ready"},
                )
                write_json(
                    root,
                    f".survey/work-queue/claims/{job_id}.json",
                    {
                        "schema_version": 1,
                        "workflow_version": 10,
                        "job_id": job_id,
                        "claim_id": f"claim-{suffix}",
                        "attempt_id": attempt_id,
                        "request_id": "claim-window",
                        "worker_id": "scheduled-chat-00",
                        "worker_kind": "scheduled_chat",
                        "kind": "research",
                        "pipeline_order": order,
                        "claimed_at": claimed.isoformat(),
                        "expires_at": expires.isoformat(),
                        "run_key": "run-1",
                        "scheduled_slot": "00",
                        "actual_invocation_start": value["actual_invocation_start"],
                    },
                )

            # Simulate legacy/concurrent overshoot: three exact-blob preflights are
            # already pending although the normal admission window is two.
            for index, suffix in enumerate(("a", "b", "c"), start=1):
                preflight_id = f"scheduled-chat-00-attempt-{suffix}-r1"
                write_json(
                    root,
                    f".survey/work-queue/research-preflight/requests/{preflight_id}.json",
                    {
                        "schema_version": 1,
                        "operation": "research_quality_preflight",
                        "request_id": preflight_id,
                        "kind": "research",
                        "attempt_id": f"attempt-{suffix}",
                        "job_id": f"job-{suffix}",
                        "record_bank": suffix,
                        "worker_id": "scheduled-chat-00",
                        "run_key": "run-1",
                        "scheduled_slot": "00",
                        "actual_invocation_start": value["actual_invocation_start"],
                        "requested_at": (
                            claimed + dt.timedelta(seconds=10 + index)
                        ).isoformat(),
                    },
                )

            result = mod.derive(root, value)
            self.assertEqual(
                result["preflight_parked_job_ids"],
                ["job-a", "job-b", "job-c"],
            )
            self.assertEqual(result["preflight_inflight_count"], 3)
            self.assertEqual(result["preflight_pipeline_window"], 2)
            self.assertEqual(result["preflight_pipeline_capacity_remaining"], 0)
            self.assertTrue(result["preflight_pipeline_saturated"])
            self.assertEqual(result["preflight_pipeline_overflow_count"], 1)
            # No frozen paper is accidentally thawed just because it exceeded the
            # intended admission window; the next real content standby is promoted.
            self.assertEqual(result["foreground_job_id"], "job-d")
            self.assertEqual(result["active_job_ids"], ["job-d"])

    def test_preflight_identity_mismatch_does_not_freeze_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            started = dt.datetime.fromisoformat(value["actual_invocation_start"])
            claimed = started + dt.timedelta(seconds=5)
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 300, "claimable": 299}},
            )
            write_json(
                root,
                ".survey/work-queue/discovery-state.json",
                {"schema_version": 3, "history": []},
            )
            write_json(
                root,
                ".survey/work-queue/jobs/job-a.json",
                {"job_id": "job-a", "type": "research", "status": "ready"},
            )
            write_json(
                root,
                ".survey/work-queue/claims/job-a.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "job_id": "job-a",
                    "claim_id": "claim-a",
                    "attempt_id": "attempt-a",
                    "request_id": "claim-window",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "kind": "research",
                    "pipeline_order": 0,
                    "claimed_at": claimed.isoformat(),
                    "expires_at": (claimed + dt.timedelta(hours=1)).isoformat(),
                    "run_key": "run-1",
                    "scheduled_slot": "00",
                    "actual_invocation_start": value["actual_invocation_start"],
                },
            )
            preflight_id = "corrupt-attempt-a-r1"
            write_json(
                root,
                f".survey/work-queue/research-preflight/requests/{preflight_id}.json",
                {
                    "schema_version": 1,
                    "operation": "research_quality_preflight",
                    "request_id": preflight_id,
                    "kind": "research",
                    "attempt_id": "attempt-a",
                    "job_id": "job-other",
                    "record_bank": "a",
                    "worker_id": "worker-999",
                    "run_key": "other-run",
                    "scheduled_slot": "adhoc",
                    "actual_invocation_start": value["actual_invocation_start"],
                    "requested_at": (claimed + dt.timedelta(seconds=10)).isoformat(),
                },
            )

            result = mod.derive(root, value)
            self.assertEqual(result["foreground_job_id"], "job-a")
            self.assertEqual(result["preflight_parked_job_ids"], [])
            self.assertEqual(result["preflight_inflight_count"], 0)



if __name__ == "__main__":
    unittest.main()
