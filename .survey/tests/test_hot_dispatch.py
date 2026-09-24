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

import claim_window_policy  # noqa: E402
import derive_worker_run_state  # noqa: E402
import hot_dispatch  # noqa: E402
import shared_preload_pool  # noqa: E402
from record_bank_config import discovery_slot_path  # noqa: E402


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


class HotDispatchTests(unittest.TestCase):
    def test_index_exposes_prepared_research_and_discovery_without_actions(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            job_id = "job-research-hot"
            claim_id = "claim-preload-hot"
            write_json(
                root / ".survey/work-queue/jobs" / f"{job_id}.json",
                {
                    "job_id": job_id,
                    "type": "research",
                    "status": "ready",
                    "priority": 90,
                    "title": "Hot paper",
                    "source_url": "https://example.invalid/paper",
                    "depends_on_job_ids": [job_id],
                },
            )
            write_json(
                root / ".survey/work-queue/claims" / f"{job_id}.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "claim_id": claim_id,
                    "job_id": job_id,
                    "worker_id": shared_preload_pool.POOL_WORKER_ID,
                    "worker_kind": shared_preload_pool.POOL_WORKER_KIND,
                    "attempt_id": "attempt-preload-hot",
                    "claimed_at": current.isoformat(),
                    "preloaded_at": current.isoformat(),
                    "expires_at": (current + dt.timedelta(hours=12)).isoformat(),
                    "kind": "research",
                    "depends_on_job_ids": [job_id],
                    "preload_pool": True,
                    "pool_order": 3,
                },
            )

            def available(_root, *, direction=None, limit=32):
                if direction != "backward":
                    return []
                return [{
                    "preload_id": "preload-hot",
                    "discovery_bank": "a",
                    "discovery_slot_path": discovery_slot_path("a"),
                    "citation_direction": "backward",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "axis": "preload-backward",
                    "initial_cursor": "20",
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 25,
                    "preload_result_path": ".survey/work-queue/discovery-precheck/results/preload-hot.json",
                    "preload_unseen_result_count": 20,
                    "created_at": current.isoformat(),
                }][:limit]

            with mock.patch.object(
                hot_dispatch.discovery_preload_queue,
                "available_preloads",
                side_effect=available,
            ):
                index = hot_dispatch.refresh(root)

            self.assertEqual(index["candidate_inventory"], 1)
            self.assertEqual(index["suggested_work_mode"], "discovery")
            self.assertTrue(index["direct_start_allowed"])
            self.assertEqual(index["research"][0]["claim_id"], claim_id)
            self.assertEqual(index["research"][0]["job"]["title"], "Hot paper")
            self.assertEqual(index["discovery"]["backward"][0]["preload_id"], "preload-hot")
            self.assertTrue((root / hot_dispatch.INDEX).is_file())

    def test_threshold_proximity_never_disables_a_stocked_selected_lane(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            research_packets = [{"claim_id": "claim-hot"}]
            discovery_packets = {
                "backward": [{"preload_id": "preload-hot"}],
                "forward": [],
                "normal": [],
            }
            for inventory, expected_mode in (
                (claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD - 1, "discovery"),
                (claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD, "research"),
                (claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD + 1, "research"),
            ):
                with (
                    mock.patch.object(hot_dispatch, "_candidate_inventory", return_value=inventory),
                    mock.patch.object(hot_dispatch, "_research_packets", return_value=research_packets),
                    mock.patch.object(hot_dispatch, "_discovery_packets", return_value=discovery_packets),
                    mock.patch.object(
                        hot_dispatch.shared_preload_pool,
                        "sync_research_bank_sidecars",
                        return_value={},
                    ),
                ):
                    index = hot_dispatch.build_index(root)
                self.assertEqual(index["suggested_work_mode"], expected_mode)
                self.assertTrue(index["direct_start_allowed"])
                self.assertEqual(index["route_guard_band"], 0)
                self.assertEqual(
                    index["lane_available"],
                    {"research": True, "discovery": True},
                )

    def test_direct_research_marker_reserves_pool_claim_and_creates_async_refill(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            job_id = "job-research-direct"
            claim_id = "claim-preload-direct"
            attempt_id = "attempt-preload-direct"
            write_json(
                root / ".survey/work-queue/jobs" / f"{job_id}.json",
                {
                    "job_id": job_id,
                    "type": "research",
                    "status": "ready",
                    "priority": 90,
                    "title": "Direct paper",
                    "source_url": "https://example.invalid/direct",
                    "depends_on_job_ids": [job_id],
                },
            )
            write_json(
                root / ".survey/work-queue/claims" / f"{job_id}.json",
                {
                    "schema_version": 1,
                    "workflow_version": 10,
                    "claim_id": claim_id,
                    "job_id": job_id,
                    "worker_id": shared_preload_pool.POOL_WORKER_ID,
                    "worker_kind": shared_preload_pool.POOL_WORKER_KIND,
                    "attempt_id": attempt_id,
                    "claimed_at": current.isoformat(),
                    "preloaded_at": current.isoformat(),
                    "expires_at": (current + dt.timedelta(hours=12)).isoformat(),
                    "kind": "research",
                    "depends_on_job_ids": [job_id],
                    "preload_pool": True,
                    "pool_order": 4,
                },
            )
            marker = root / hot_dispatch.DIRECT_RESEARCH_TAKES / f"{claim_id}.json"
            write_json(
                marker,
                {
                    "schema_version": 1,
                    "operation": "direct_take_research",
                    "claim_id": claim_id,
                    "job_id": job_id,
                    "attempt_id": attempt_id,
                    "request_id": "direct-take-test",
                    "worker_id": "worker-77",
                    "scheduled_slot": "adhoc",
                    "run_key": "run-direct",
                    "actual_invocation_start": current.isoformat(),
                    "requested_at": current.isoformat(),
                    "claim_window": 12,
                    "candidate_inventory_at_start": 1,
                    "work_mode_at_start": "research",
                    "research_discovery_threshold": claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD,
                    "hot_dispatch_generated_at": current.isoformat(),
                },
            )

            # The marker itself removes this claim from every normal FIFO adopter
            # before the background canonicalizer has touched the claim file.
            claims = {
                job_id: dict(
                    json.loads((root / ".survey/work-queue/claims" / f"{job_id}.json").read_text()),
                    active=True,
                    expired=False,
                )
            }
            self.assertEqual(
                shared_preload_pool.waiting_claims(claims, repo_root=root),
                [],
            )

            result = hot_dispatch.process_research_takes(root)
            self.assertEqual(result["processed"], 1)
            stored = json.loads(
                (root / ".survey/work-queue/claims" / f"{job_id}.json").read_text(encoding="utf-8")
            )
            self.assertEqual(stored["worker_id"], "worker-77")
            self.assertEqual(stored["run_key"], "run-direct")
            self.assertFalse(stored["preload_pool"])
            self.assertTrue(stored["direct_take"])

            direct = json.loads(
                (root / hot_dispatch.DIRECT_RESEARCH_RESULTS / f"{claim_id}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(direct["status"], "canonicalizing")
            self.assertTrue(direct["work_start_allowed"])
            self.assertFalse(direct["record_write_allowed"])

            refill = root / direct["canonical_claim_result_path"]
            write_json(
                refill,
                {
                    "ok": True,
                    "processed_at": current.isoformat(),
                    "assignments": [{
                        "job_id": job_id,
                        "claim_id": claim_id,
                        "attempt_id": attempt_id,
                        "record_bank": "e",
                    }],
                },
            )
            final = hot_dispatch.finalize_research_takes(root)
            self.assertEqual(final["updated"], 1)
            direct = json.loads(
                (root / hot_dispatch.DIRECT_RESEARCH_RESULTS / f"{claim_id}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(direct["status"], "ready_for_submission")
            self.assertTrue(direct["record_write_allowed"])
            self.assertEqual(direct["assignment"]["record_bank"], "e")

    def test_direct_discovery_claim_materializes_formal_precheck_behind_evaluation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            preload_id = "preload-direct-discovery"
            request_id = "direct-discovery-test"
            write_json(
                root / hot_dispatch.DISCOVERY_ENTRIES / f"{preload_id}.json",
                {
                    "preload_id": preload_id,
                    "axis": "preload-backward",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 25,
                    "initial_cursor": "40",
                },
            )
            write_json(
                root / hot_dispatch.DISCOVERY_CLAIMS / f"{preload_id}.json",
                {
                    "schema_version": 1,
                    "operation": "direct_take_discovery",
                    "preload_id": preload_id,
                    "worker_id": "worker-78",
                    "run_key": "run-discovery",
                    "request_id": request_id,
                    "requested_at": current.isoformat(),
                    "preload_result_path": ".survey/work-queue/discovery-precheck/results/preload-seed.json",
                    "discovery_bank": "a",
                    "discovery_slot_path": discovery_slot_path("a"),
                    "scheduled_slot": "adhoc",
                    "actual_invocation_start": current.isoformat(),
                    "candidate_inventory_at_start": 1000,
                    "work_mode_at_start": "discovery",
                    "research_discovery_threshold": claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD,
                    "hot_dispatch_generated_at": current.isoformat(),
                },
            )

            result = hot_dispatch.materialize_discovery_prechecks(root)
            self.assertEqual(result["created"], 1)
            request = json.loads(
                (root / hot_dispatch.PRECHECK_REQUESTS / f"{request_id}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(request["schema_version"], 3)
            self.assertEqual(request["preload_id"], preload_id)
            self.assertEqual(request["worker_id"], "worker-78")
            self.assertTrue(request["direct_take"])

            direct = json.loads(
                (root / hot_dispatch.DIRECT_DISCOVERY_RESULTS / f"{preload_id}.json")
                .read_text(encoding="utf-8")
            )
            self.assertEqual(direct["status"], "precheck_pending")
            self.assertTrue(direct["work_start_allowed"])
            self.assertFalse(direct["submission_allowed"])

    def test_run_state_accepts_direct_route_without_waiting_for_current_inventory(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            # Canonical state currently looks like Research, while the durable
            # hot-start request freezes the invocation's earlier Discovery route.
            write_json(
                root / ".survey/work-queue/next-jobs.json",
                {"claiming": {"ready_research_audit": 400, "claimable": 400}},
            )
            raw = {
                "schema_version": 1,
                "request_id": "direct-route-test",
                "run_key": "direct-route-run",
                "worker_id": "worker-79",
                "scheduled_slot": "adhoc",
                "actual_invocation_start": current.isoformat(),
                "runtime_condition": "none",
                "candidate_inventory_at_start": 400,
                "work_mode_at_start": "discovery",
                "research_discovery_threshold": claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD,
                "hot_dispatch_generated_at": current.isoformat(),
            }
            request_path = root / ".survey/work-queue/run-state/requests/direct-route-test.json"
            write_json(request_path, raw)
            request = derive_worker_run_state._normalize_request(request_path, raw)
            result = derive_worker_run_state.derive(root, request)
            self.assertEqual(result["candidate_inventory"], 100)
            self.assertEqual(result["work_mode"], "discovery")
            self.assertEqual(result["route_source"], "hot_dispatch_direct_start")


if __name__ == "__main__":
    unittest.main()
