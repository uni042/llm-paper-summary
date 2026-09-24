from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import ensure_discovery_run_state as ensure


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class EnsureDiscoveryRunStateTests(unittest.TestCase):
    def test_foreground_precheck_creates_deterministic_recovery_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            start = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
            precheck = root / ".survey/work-queue/discovery-precheck/requests/pre-1.json"
            write_json(
                precheck,
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "pre-1",
                    "run_key": "run-discovery",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "scheduled_slot": "00",
                    "actual_invocation_start": start.isoformat(),
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                },
            )

            first = ensure.ensure_paths(
                root,
                [Path(".survey/work-queue/discovery-precheck/requests/pre-1.json")],
            )
            self.assertEqual(len(first["created"]), 1)
            request_path = root / first["created"][0]["request_path"]
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["run_key"], "run-discovery")
            self.assertEqual(request["worker_id"], "scheduled-chat-00")
            self.assertEqual(request["scheduled_slot"], "00")
            self.assertEqual(request["route_recovery_source"], "discovery_precheck_identity")
            self.assertEqual(request["recovered_work_mode_at_start"], "discovery")

            second = ensure.ensure_paths(
                root,
                [Path(".survey/work-queue/discovery-precheck/requests/pre-1.json")],
            )
            self.assertEqual(second["created"], [])
            self.assertEqual(len(second["reused"]), 1)
            self.assertEqual(second["reused"][0]["request_path"], first["created"][0]["request_path"])

    def test_ready_precheck_refreshes_settled_run_state_and_blocks_finalization(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            start = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
            precheck_rel = Path(".survey/work-queue/discovery-precheck/requests/pre-ready.json")
            write_json(
                root / precheck_rel,
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "pre-ready",
                    "run_key": "run-ready",
                    "worker_id": "worker-45",
                    "worker_kind": "scheduled_chat",
                    "scheduled_slot": "adhoc",
                    "actual_invocation_start": start.isoformat(),
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                },
            )
            write_json(
                root / ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 0, "claimable": 0}},
            )
            write_json(
                root / ".survey/work-queue/discovery-state.json",
                {"schema_version": 3, "history": []},
            )

            initial = ensure.ensure_paths(root, [precheck_rel])
            self.assertEqual(len(initial["created"]), 1)
            initial_request = initial["created"][0]["request_path"]
            initial_stem = Path(initial_request).stem
            write_json(
                root / f".survey/work-queue/run-state/results/{initial_stem}.json",
                {
                    "schema_version": 1,
                    "ok": True,
                    "request_id": initial_stem,
                    "run_key": "run-ready",
                    "worker_id": "worker-45",
                    "work_mode": "discovery",
                },
            )
            write_json(
                root / ".survey/work-queue/discovery-precheck/results/pre-ready.json",
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": "pre-ready",
                    "run_key": "run-ready",
                    "ok": True,
                    "evaluation_allowed": True,
                    "decision": "READY_FOR_EVALUATION",
                    "results": [{"title": "candidate"}],
                },
            )

            refreshed = ensure.ensure_paths(root, [precheck_rel])
            self.assertEqual(len(refreshed["created"]), 1)
            refresh_path = refreshed["created"][0]["request_path"]
            self.assertNotEqual(refresh_path, initial_request)
            self.assertEqual(
                refreshed["created"][0]["reason"],
                "refresh_after_ready_for_evaluation",
            )

            processed = ensure.derive_worker_run_state.process_pending(root)
            self.assertGreaterEqual(processed["processed"], 1)
            refresh_stem = Path(refresh_path).stem
            result = json.loads(
                (root / f".survey/work-queue/run-state/results/{refresh_stem}.json").read_text(
                    encoding="utf-8"
                )
            )
            self.assertTrue(result["discovery_evaluation_pending"])
            self.assertEqual(result["gate"]["required_action"], "CONTINUE_DISCOVERY_ROUND")
            self.assertEqual(result["finalization_gate"]["decision"], "MUST_CONTINUE")
            self.assertFalse(result["finalization_permit_issued"])

    def test_preload_request_does_not_create_worker_run_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            precheck = root / ".survey/work-queue/discovery-precheck/requests/preload-x.json"
            write_json(
                precheck,
                {
                    "schema_version": 3,
                    "request_id": "preload-x",
                    "run_key": "preload:preload-x",
                    "preload_seed": True,
                },
            )
            result = ensure.ensure_paths(
                root,
                [Path(".survey/work-queue/discovery-precheck/requests/preload-x.json")],
            )
            self.assertEqual(result["created"], [])
            self.assertEqual(len(result["skipped"]), 1)
            self.assertFalse((root / ".survey/work-queue/run-state/requests").exists())

    def test_submission_can_repair_from_linked_precheck_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            start = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
            write_json(
                root / ".survey/work-queue/discovery-precheck/requests/pre-2.json",
                {
                    "schema_version": 3,
                    "request_id": "pre-2",
                    "run_key": "run-2",
                    "worker_id": "worker-7",
                    "worker_kind": "scheduled_chat",
                    "scheduled_slot": "adhoc",
                    "actual_invocation_start": start.isoformat(),
                },
            )
            write_json(
                root / ".survey/work-queue/submissions/round-2.json",
                {
                    "operation": "submit_discovery_round",
                    "worker_id": "worker-7",
                    "discovery_precheck": {"request_id": "pre-2"},
                    "discovery_stats": {"run_key": "run-2", "round": "round-2"},
                    "candidates": [],
                },
            )
            result = ensure.ensure_from_submission(
                root,
                "work-queue/submissions/round-2.json",
            )
            self.assertEqual(len(result["created"]), 1)
            self.assertEqual(result["created"][0]["run_key"], "run-2")


if __name__ == "__main__":
    unittest.main()
