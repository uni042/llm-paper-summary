from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "auto_claim_from_run_state.py"
spec = importlib.util.spec_from_file_location("auto_claim_from_run_state_test", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def eligible_result():
    return {
        "schema_version": 1,
        "ok": True,
        "request_id": "run-state-1",
        "run_key": "run-1",
        "worker_id": "scheduled-chat-30",
        "scheduled_slot": "30",
        "actual_invocation_start": "2026-09-23T06:30:00+00:00",
        "snapshot_origin": "request-fast-lane",
        "work_mode": "research",
        "candidate_inventory": 100,
        "claim_window": 8,
        "active_assignment": False,
        "claim_result_pending": False,
        "research_audit_completed_this_invocation": 0,
        "submitted_attempt_ids": [],
        "seconds_to_run_deadline": 3500,
        "gate": {
            "decision": "CONTINUE",
            "required_action": "CLAIM_NEXT_RESEARCH_AUDIT",
            "finalization_allowed": False,
        },
    }


class AutoInitialClaimTests(unittest.TestCase):
    def test_eligible_initial_snapshot_creates_and_processes_one_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / ".survey/work-queue/run-state/results/run-state-1.json"
            write_json(source, eligible_result())
            changed = root / "changed.txt"
            changed.write_text(".survey/work-queue/run-state/results/run-state-1.json\n", encoding="utf-8")

            def fake_initial_fast_path(repo_root, request_path):
                requests = list((root / ".survey/work-queue/claim-requests").glob("*.json"))
                self.assertEqual(len(requests), 1)
                self.assertEqual(request_path, requests[0])
                request = json.loads(requests[0].read_text(encoding="utf-8"))
                write_json(
                    root / ".survey/work-queue/claim-results" / requests[0].name,
                    {
                        "ok": True,
                        "request_id": request["request_id"],
                        "worker_id": request["worker_id"],
                        "run_key": request["run_key"],
                        "scheduled_slot": request["scheduled_slot"],
                        "actual_invocation_start": request["actual_invocation_start"],
                        "assignments": [{
                            "job_id": "job-a",
                            "attempt_id": "attempt-a",
                            "claim_id": "claim-a",
                        }],
                    },
                )
                return {"ok": True, "changed_claim_results": [requests[0].name]}

            with (
                mock.patch.object(mod.initial_claim_fast_path, "process", side_effect=fake_initial_fast_path) as fast,
                mock.patch.object(mod.claim_fast_path, "process") as fallback,
            ):
                summary = mod.process(root, changed)

            self.assertEqual(len(summary["created"]), 1)
            fast.assert_called_once()
            fallback.assert_not_called()
            requests = list((root / ".survey/work-queue/claim-requests").glob("*.json"))
            request = json.loads(requests[0].read_text(encoding="utf-8"))
            self.assertEqual(request["worker_id"], "scheduled-chat-30")
            self.assertEqual(request["run_key"], "run-1")
            self.assertEqual(request["claim_window"], 8)
            self.assertTrue(request["auto_initial_claim"])

            updated = json.loads(source.read_text(encoding="utf-8"))
            auto = updated["auto_initial_claim"]
            self.assertEqual(auto["status"], "allocated")
            self.assertEqual(auto["assignment_count"], 1)
            self.assertEqual(auto["attempt_ids"], ["attempt-a"])
            self.assertEqual(auto["job_ids"], ["job-a"])

    def test_run_state_claim_window_is_propagated_and_fast_path_can_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            value["claim_window"] = 6
            source = root / ".survey/work-queue/run-state/results/run-state-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(".survey/work-queue/run-state/results/run-state-1.json\n", encoding="utf-8")

            def canonical(repo_root):
                request = next((root / ".survey/work-queue/claim-requests").glob("*.json"))
                payload = json.loads(request.read_text(encoding="utf-8"))
                self.assertEqual(payload["claim_window"], 6)
                write_json(
                    root / ".survey/work-queue/claim-results" / request.name,
                    {"ok": True, "assignments": [], "request_id": payload["request_id"]},
                )
                return {"ok": True}

            with (
                mock.patch.object(
                    mod.initial_claim_fast_path,
                    "process",
                    side_effect=mod.initial_claim_fast_path.InitialClaimFastPathUnavailable("pool shortfall"),
                ) as initial,
                mock.patch.object(mod.claim_fast_path, "process", side_effect=canonical) as fallback,
            ):
                summary = mod.process(root, changed)

            initial.assert_called_once()
            fallback.assert_called_once()
            self.assertEqual(summary["claim_fast_path"]["mode"], "canonical-fallback")
            self.assertEqual(summary["claim_fast_path"]["fallback_reason"], "pool shortfall")

    def test_existing_same_run_claim_transport_prevents_duplicate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            source = root / ".survey/work-queue/run-state/results/run-state-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(".survey/work-queue/run-state/results/run-state-1.json\n", encoding="utf-8")
            write_json(
                root / ".survey/work-queue/claim-requests/existing.json",
                {
                    "worker_id": value["worker_id"],
                    "run_key": value["run_key"],
                    "scheduled_slot": value["scheduled_slot"],
                    "actual_invocation_start": value["actual_invocation_start"],
                },
            )

            with (
                mock.patch.object(mod.initial_claim_fast_path, "process") as initial,
                mock.patch.object(mod.claim_fast_path, "process") as fast,
            ):
                summary = mod.process(root, changed)

            initial.assert_not_called()
            fast.assert_not_called()
            self.assertEqual(summary["created"], [])
            self.assertEqual(summary["skipped"][0]["reason"], "run_already_has_claim_transport")

    def test_carryover_active_assignment_runs_fast_recovery_and_publishes_resume_packet(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            value["active_assignment"] = True
            value["gate"]["required_action"] = "CONTINUE_ASSIGNED_WORK"
            source = root / ".survey/work-queue/run-state/results/run-state-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(".survey/work-queue/run-state/results/run-state-1.json\n", encoding="utf-8")

            def recover(repo_root):
                write_json(
                    root / ".survey/work-queue/hot-dispatch.json",
                    {
                        "research_resume": {
                            "scheduled-chat-30": [{
                                "job_id": "job-old",
                                "claim_id": "claim-old",
                                "attempt_id": "attempt-old",
                                "pipeline_role": "foreground",
                                "work_start_allowed": True,
                                "record_write_allowed": True,
                            }]
                        }
                    },
                )
                return {"ok": True}

            with (
                mock.patch.object(mod.initial_claim_fast_path, "process") as initial,
                mock.patch.object(mod.claim_fast_path, "process", side_effect=recover) as fast,
            ):
                summary = mod.process(root, changed)

            initial.assert_not_called()
            fast.assert_called_once()
            self.assertFalse(summary["resume_recovery"]["skipped"])
            updated = json.loads(source.read_text(encoding="utf-8"))
            resume = updated["auto_resume_recovery"]
            self.assertEqual(resume["status"], "ready")
            self.assertEqual(resume["assignment_count"], 1)
            self.assertEqual(resume["foreground"]["attempt_id"], "attempt-old")

    def test_noninitial_snapshot_is_not_auto_claimed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            value["submitted_attempt_ids"] = ["attempt-old"]
            source = root / ".survey/work-queue/run-state/results/run-state-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(".survey/work-queue/run-state/results/run-state-1.json\n", encoding="utf-8")

            with (
                mock.patch.object(mod.initial_claim_fast_path, "process") as initial,
                mock.patch.object(mod.claim_fast_path, "process") as fast,
            ):
                summary = mod.process(root, changed)

            initial.assert_not_called()
            fast.assert_not_called()
            self.assertEqual(summary["created"], [])
            self.assertEqual(summary["skipped"][0]["reason"], "not_initial_research_claim_eligible")


if __name__ == "__main__":
    unittest.main()
