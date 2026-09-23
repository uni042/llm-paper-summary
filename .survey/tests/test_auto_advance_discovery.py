from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import auto_advance_discovery as advance
import claim_window_policy
import hot_dispatch
from record_bank_config import discovery_slot_path


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class AutoAdvanceDiscoveryTests(unittest.TestCase):
    def test_completed_round_claims_next_prechecked_bank_and_materializes_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
            report = root / "recovery.json"
            write_json(
                report,
                {
                    "recovered": [
                        {"submission": "work-queue/submissions/round-1.json"}
                    ]
                },
            )
            write_json(
                root / ".survey/work-queue/submissions/round-1.json",
                {
                    "operation": "submit_discovery_round",
                    "worker_id": "worker-78",
                    "discovery_stats": {
                        "run_key": "run-discovery",
                        "round": "round-1",
                        "axis": "backward",
                    },
                },
            )
            preload_id = "preload-next"
            write_json(
                root / hot_dispatch.DISCOVERY_ENTRIES / f"{preload_id}.json",
                {
                    "preload_id": preload_id,
                    "axis": "forward citations",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 25,
                    "initial_cursor": "40",
                },
            )
            request = {
                "schema_version": 1,
                "request_id": "cached",
                "worker_id": "worker-78",
                "worker_kind": "scheduled_chat",
                "run_key": "run-discovery",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": current.isoformat(),
                "runtime_condition": "none",
            }
            before = {
                "ok": True,
                "worker_id": "worker-78",
                "run_key": "run-discovery",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": current.isoformat(),
                "candidate_inventory": 100,
                "work_mode": "discovery",
                "seconds_to_run_deadline": 3000,
                "processed_at": current.isoformat(),
                "next_action": "DISCOVER_AGAIN",
                "gate": {"required_action": "DISCOVER_AGAIN"},
                "discovery_selector": {"next_direction": "forward"},
            }
            after = {
                **before,
                "next_action": "WAIT_FOR_DISCOVERY_PRECHECK_RESULT",
                "gate": {"required_action": "WAIT_FOR_DISCOVERY_PRECHECK_RESULT"},
                "discovery_precheck_result_pending": True,
            }
            preload = {
                "preload_id": preload_id,
                "discovery_bank": "a",
                "discovery_slot_path": discovery_slot_path("a"),
                "citation_direction": "forward",
                "provider": "repository_references",
                "source_url": "repository://structured-references",
                "axis": "forward citations",
                "initial_cursor": "40",
                "target_unseen": 20,
                "page_size": 20,
                "max_pages": 25,
                "preload_result_path": ".survey/work-queue/discovery-precheck/results/preload-next.json",
            }

            with mock.patch.object(
                advance.derive_worker_run_state.run_state_cache,
                "cached_request",
                return_value=request,
            ):
                with mock.patch.object(
                    advance.derive_worker_run_state,
                    "derive",
                    side_effect=[before, after],
                ):
                    with mock.patch.object(
                        advance.derive_worker_run_state.run_state_cache,
                        "generation_for",
                        return_value=7,
                    ):
                        with mock.patch.object(
                            advance.discovery_preload_queue,
                            "pick_available",
                            return_value=preload,
                        ):
                            result = advance.advance(root, report)

            self.assertEqual(len(result["advanced"]), 1)
            claim = json.loads(
                (root / hot_dispatch.DISCOVERY_CLAIMS / f"{preload_id}.json").read_text()
            )
            self.assertTrue(claim["direct_take"])
            self.assertTrue(claim["auto_next_discovery"])
            self.assertEqual(claim["worker_id"], "worker-78")
            self.assertEqual(claim["run_key"], "run-discovery")
            self.assertEqual(
                claim["research_discovery_threshold"],
                claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD,
            )

            request_id = result["advanced"][0]["request_id"]
            formal = json.loads(
                (root / hot_dispatch.PRECHECK_REQUESTS / f"{request_id}.json").read_text()
            )
            self.assertEqual(formal["schema_version"], 3)
            self.assertEqual(formal["preload_id"], preload_id)
            self.assertTrue(formal["direct_take"])

            direct = json.loads(
                (root / hot_dispatch.DIRECT_DISCOVERY_RESULTS / f"{preload_id}.json").read_text()
            )
            self.assertTrue(direct["work_start_allowed"])
            self.assertFalse(direct["submission_allowed"])

            snapshot_path = root / result["snapshots"][0]["result_path"]
            snapshot = json.loads(snapshot_path.read_text())
            self.assertEqual(snapshot["snapshot_origin"], "discovery-recovery-fast-lane")
            self.assertEqual(snapshot["auto_next_discovery"]["preload_id"], preload_id)
            self.assertTrue(snapshot["auto_next_discovery"]["work_start_allowed"])
            self.assertEqual(
                snapshot["gate"]["required_action"],
                "WAIT_FOR_DISCOVERY_PRECHECK_RESULT",
            )

    def test_no_new_bank_is_claimed_when_gate_does_not_allow_new_round(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
            report = root / "recovery.json"
            write_json(
                report,
                {"recovered": [{"submission": "work-queue/submissions/round-1.json"}]},
            )
            write_json(
                root / ".survey/work-queue/submissions/round-1.json",
                {
                    "operation": "submit_discovery_round",
                    "worker_id": "worker-79",
                    "discovery_stats": {"run_key": "run-stop", "round": "round-1", "axis": "backward"},
                },
            )
            request = {
                "schema_version": 1,
                "request_id": "cached",
                "worker_id": "worker-79",
                "worker_kind": "scheduled_chat",
                "run_key": "run-stop",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": current.isoformat(),
                "runtime_condition": "none",
            }
            state = {
                "ok": True,
                "worker_id": "worker-79",
                "run_key": "run-stop",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": current.isoformat(),
                "candidate_inventory": 100,
                "work_mode": "discovery",
                "seconds_to_run_deadline": 500,
                "processed_at": current.isoformat(),
                "next_action": "FINALIZE",
                "gate": {"required_action": "FINALIZE"},
                "discovery_selector": {"next_direction": "forward"},
            }
            with mock.patch.object(
                advance.derive_worker_run_state.run_state_cache,
                "cached_request",
                return_value=request,
            ):
                with mock.patch.object(
                    advance.derive_worker_run_state,
                    "derive",
                    side_effect=[state, state],
                ):
                    with mock.patch.object(
                        advance.derive_worker_run_state.run_state_cache,
                        "generation_for",
                        return_value=3,
                    ):
                        with mock.patch.object(
                            advance.discovery_preload_queue,
                            "pick_available",
                        ) as pick:
                            result = advance.advance(root, report)

            pick.assert_not_called()
            self.assertEqual(result["advanced"], [])
            self.assertFalse((root / hot_dispatch.DISCOVERY_CLAIMS).exists())
            self.assertEqual(result["snapshots"][0]["required_action"], "FINALIZE")


if __name__ == "__main__":
    unittest.main()
