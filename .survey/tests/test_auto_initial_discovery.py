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
SCRIPT = SCRIPTS / "auto_discovery_from_run_state.py"
spec = importlib.util.spec_from_file_location("auto_discovery_from_run_state_test", SCRIPT)
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
        "request_id": "run-state-discovery-1",
        "run_key": "discovery-run-1",
        "worker_id": "scheduled-chat-00",
        "scheduled_slot": "00",
        "actual_invocation_start": "2026-09-23T16:00:00+00:00",
        "snapshot_origin": "request-fast-lane",
        "work_mode": "discovery",
        "candidate_inventory": 100,
        "seconds_to_run_deadline": 3500,
        "discovery_rounds_completed": 0,
        "discovery_precheck_result_pending": False,
        "discovery_submission_result_pending": False,
        "discovery_evaluation_pending": False,
        "discovery_recovery_required": False,
        "discovery_selector": {"next_direction": "forward"},
        "discovery_preload": {
            "preload_id": "preload-forward-1",
            "discovery_bank": "a",
            "discovery_slot_path": ".survey/work-queue/records/a/discovery-preload.json",
            "citation_direction": "forward",
            "provider": "semantic_scholar",
            "source_url": "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2303.06865/citations",
            "axis": "preload-forward-flexgen",
            "initial_cursor": None,
            "target_unseen": 20,
            "page_size": 20,
            "max_pages": 8,
        },
        "gate": {
            "decision": "CONTINUE",
            "required_action": "DISCOVER_AGAIN",
            "finalization_allowed": False,
        },
    }


class AutoInitialDiscoveryTests(unittest.TestCase):
    def test_eligible_initial_snapshot_adopts_and_prechecks_in_same_lane(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            source = root / ".survey/work-queue/run-state/results/run-state-discovery-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(
                ".survey/work-queue/run-state/results/run-state-discovery-1.json\n",
                encoding="utf-8",
            )

            precheck = {
                "schema_version": 3,
                "operation": "precheck_discovery_candidates",
                "ok": True,
                "request_id": "placeholder",
                "run_key": value["run_key"],
                "preload_id": value["discovery_preload"]["preload_id"],
                "evaluation_allowed": True,
                "decision": "READY_FOR_EVALUATION",
                "preload_cache_used": True,
                "preload_cached_pages_used": 1,
                "preload_live_pages_fetched": 0,
                "results": [],
            }

            def fake_process(request_path, **kwargs):
                request = json.loads(Path(request_path).read_text(encoding="utf-8"))
                out = dict(precheck)
                out["request_id"] = request["request_id"]
                return out

            fresh = dict(value)
            fresh["processed_at"] = "2026-09-23T16:00:01+00:00"
            fresh["discovery_evaluation_pending"] = True
            fresh["discovery_evaluation_request_ids"] = ["placeholder"]
            fresh["gate"] = {
                "decision": "CONTINUE",
                "required_action": "CONTINUE_DISCOVERY_ROUND",
                "finalization_allowed": False,
            }
            fresh["next_action"] = "CONTINUE_DISCOVERY_ROUND"

            with (
                mock.patch.object(mod.build_discovery_identity_snapshot, "build_snapshot") as snapshot,
                mock.patch.object(mod.build_discovery_rejection_ledger, "build_ledger") as ledger,
                mock.patch.object(
                    mod.process_discovery_precheck,
                    "process_request",
                    side_effect=fake_process,
                ) as process_precheck,
                mock.patch.object(
                    mod.derive_worker_run_state,
                    "derive",
                    return_value=fresh,
                ) as derive,
                mock.patch.object(
                    mod.derive_worker_run_state.run_state_cache,
                    "write_latest_pointer",
                ) as latest,
            ):
                summary = mod.process(root, changed)

            self.assertEqual(len(summary["created"]), 1)
            snapshot.assert_called_once()
            ledger.assert_called_once()
            process_precheck.assert_called_once()
            derive.assert_called_once()
            latest.assert_called_once()

            requests = list((root / mod.PRECHECK_REQUESTS).glob("*.json"))
            self.assertEqual(len(requests), 1)
            request = json.loads(requests[0].read_text(encoding="utf-8"))
            self.assertEqual(request["schema_version"], 3)
            self.assertEqual(request["run_key"], value["run_key"])
            self.assertEqual(request["worker_id"], value["worker_id"])
            self.assertEqual(request["preload_id"], "preload-forward-1")
            self.assertFalse(request["preload_seed"])
            self.assertTrue(request["auto_initial_discovery"])
            self.assertEqual(request["discovery_bank"], "a")

            result = json.loads(
                (root / mod.PRECHECK_RESULTS / requests[0].name).read_text(encoding="utf-8")
            )
            self.assertTrue(result["evaluation_allowed"])
            self.assertTrue(result["preload_cache_used"])

            updated = json.loads(source.read_text(encoding="utf-8"))
            self.assertEqual(updated["next_action"], "CONTINUE_DISCOVERY_ROUND")
            self.assertEqual(
                updated["auto_initial_discovery"]["status"],
                "ready_for_evaluation",
            )
            self.assertEqual(updated["auto_initial_discovery"]["preload_live_pages_fetched"], 0)

    def test_existing_same_run_precheck_prevents_duplicate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            source = root / ".survey/work-queue/run-state/results/run-state-discovery-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(
                ".survey/work-queue/run-state/results/run-state-discovery-1.json\n",
                encoding="utf-8",
            )
            write_json(
                root / mod.PRECHECK_REQUESTS / "existing.json",
                {
                    "schema_version": 3,
                    "request_id": "existing",
                    "run_key": value["run_key"],
                },
            )

            with mock.patch.object(mod.process_discovery_precheck, "process_request") as process_precheck:
                summary = mod.process(root, changed)

            process_precheck.assert_not_called()
            self.assertEqual(summary["created"], [])
            self.assertEqual(summary["skipped"][0]["reason"], "run_already_has_discovery_transport")

    def test_noninitial_round_is_not_auto_started(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            value["discovery_rounds_completed"] = 1
            source = root / ".survey/work-queue/run-state/results/run-state-discovery-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(
                ".survey/work-queue/run-state/results/run-state-discovery-1.json\n",
                encoding="utf-8",
            )

            with mock.patch.object(mod.process_discovery_precheck, "process_request") as process_precheck:
                summary = mod.process(root, changed)

            process_precheck.assert_not_called()
            self.assertEqual(summary["created"], [])
            self.assertEqual(
                summary["skipped"][0]["reason"],
                "not_initial_discovery_preload_eligible",
            )

    def test_missing_preload_keeps_normal_discovery_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            value = eligible_result()
            value["discovery_preload"] = None
            source = root / ".survey/work-queue/run-state/results/run-state-discovery-1.json"
            write_json(source, value)
            changed = root / "changed.txt"
            changed.write_text(
                ".survey/work-queue/run-state/results/run-state-discovery-1.json\n",
                encoding="utf-8",
            )

            with mock.patch.object(mod.process_discovery_precheck, "process_request") as process_precheck:
                summary = mod.process(root, changed)

            process_precheck.assert_not_called()
            self.assertEqual(summary["created"], [])
            self.assertEqual(
                summary["skipped"][0]["reason"],
                "not_initial_discovery_preload_eligible",
            )


if __name__ == "__main__":
    unittest.main()
