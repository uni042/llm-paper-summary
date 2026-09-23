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

    def test_incremental_cache_rebuilds_after_deletion_without_changing_success_count(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            start = dt.datetime.fromisoformat(value["actual_invocation_start"])
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/claim-results/claim-1.json",
                {
                    "worker_id": "scheduled-chat-00",
                    "assignments": [
                        {
                            "attempt_id": "attempt-a",
                            "claimed_at": (start + dt.timedelta(seconds=1)).isoformat(),
                        }
                    ],
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-a.json",
                {"attempt_id": "attempt-a", "job_id": "job-a"},
            )
            write_json(
                root,
                ".survey/work-queue/results/research/attempt-a.json",
                {
                    "attempt_id": "attempt-a",
                    "job_id": "job-a",
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": (start + dt.timedelta(seconds=10)).isoformat(),
                },
            )

            first = mod.derive(root, value)
            self.assertEqual(first["state_source"], "canonical_rebuild")
            self.assertEqual(first["research_audit_completed_this_invocation"], 1)

            second_request = dict(value)
            second_request["request_id"] = "snap-2"
            second = mod.derive(root, second_request)
            self.assertEqual(second["state_source"], "incremental_cache")
            self.assertEqual(second["research_audit_completed_this_invocation"], 1)

            cache_path = mod.worker_run_index.cache_path(root, value)
            cache_path.unlink()
            third_request = dict(value)
            third_request["request_id"] = "snap-3"
            third = mod.derive(root, third_request)
            self.assertEqual(third["state_source"], "canonical_rebuild")
            self.assertEqual(third["research_audit_completed_this_invocation"], 1)

    def test_retryable_submission_remains_pending_in_cache(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            start = dt.datetime.fromisoformat(value["actual_invocation_start"])
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/claim-results/claim-1.json",
                {
                    "worker_id": "scheduled-chat-00",
                    "assignments": [
                        {"attempt_id": "attempt-r", "claimed_at": start.isoformat()}
                    ],
                },
            )
            write_json(
                root,
                ".survey/work-queue/submissions/research/attempt-r.json",
                {"attempt_id": "attempt-r", "job_id": "job-r"},
            )
            write_json(
                root,
                ".survey/work-queue/results/research/attempt-r.json",
                {
                    "attempt_id": "attempt-r",
                    "job_id": "job-r",
                    "ok": False,
                    "retryable": True,
                    "processed_at": (start + dt.timedelta(seconds=5)).isoformat(),
                },
            )
            first = mod.derive(root, value)
            self.assertTrue(first["submission_result_pending"])
            self.assertIn("attempt-r", first["retryable_attempt_ids"])
            second_request = dict(value)
            second_request["request_id"] = "snap-retry-2"
            second = mod.derive(root, second_request)
            self.assertEqual(second["state_source"], "incremental_cache")
            self.assertTrue(second["submission_result_pending"])
            self.assertIn("attempt-r", second["retryable_attempt_ids"])

    def test_automatic_snapshot_uses_same_gate_and_exact_run_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = request()
            start = dt.datetime.fromisoformat(value["actual_invocation_start"])
            write_json(
                root,
                ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 60, "claimable": 60}},
            )
            write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
            write_json(
                root,
                ".survey/work-queue/claim-results/claim-1.json",
                {
                    "worker_id": value["worker_id"],
                    "assignments": [
                        {"attempt_id": "attempt-auto", "claimed_at": start.isoformat()}
                    ],
                },
            )
            # First canonical snapshot creates the advisory cache.
            mod.derive(root, value)
            identity = {
                "worker_id": value["worker_id"],
                "run_key": value["run_key"],
                "scheduled_slot": value["scheduled_slot"],
                "actual_invocation_start": value["actual_invocation_start"],
            }
            descriptor = {
                "attempt_id": "attempt-auto",
                "job_id": "job-auto",
                "kind": "research",
                **identity,
            }
            descriptor_path = root / ".survey/work-queue/submissions/research/attempt-auto.json"
            write_json(root, descriptor_path.relative_to(root).as_posix(), descriptor)
            mod.worker_run_index.apply_descriptor(root, descriptor_path)
            result_path = root / ".survey/work-queue/results/research/attempt-auto.json"
            write_json(
                root,
                result_path.relative_to(root).as_posix(),
                {
                    "attempt_id": "attempt-auto",
                    "job_id": "job-auto",
                    "job_type": "research",
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": (start + dt.timedelta(seconds=20)).isoformat(),
                },
            )
            mod.worker_run_index.apply_result(root, result_path)
            output = mod.emit_automatic_snapshot(
                root,
                identity,
                source_events=[result_path.relative_to(root).as_posix()],
            )
            self.assertIsNotNone(output)
            auto = json.loads((root / output).read_text(encoding="utf-8"))
            self.assertEqual(auto["snapshot_origin"], "submission_auto")
            self.assertEqual(auto["worker_id"], value["worker_id"])
            self.assertEqual(auto["run_key"], value["run_key"])
            self.assertEqual(auto["research_audit_completed_this_invocation"], 1)
            self.assertIn(auto["gate"]["decision"], {"CONTINUE", "STOP_RUN"})
            latest = json.loads(
                (
                    root
                    / ".survey/work-queue/run-state/latest/scheduled-chat-00.json"
                ).read_text(encoding="utf-8")
            )
            self.assertEqual(latest["run_key"], value["run_key"])
            self.assertEqual(latest["result_path"], output)

    def test_request_rejects_cross_worker_slot(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "snap-1.json"
            value = request("scheduled-chat-00", "30")
            path.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "scheduled-chat-00"):
                mod._normalize_request(path, value)


if __name__ == "__main__":
    unittest.main()
