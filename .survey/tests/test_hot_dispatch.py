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
            research_contract = index["research"][0]["direct_take_contract"]
            self.assertTrue(research_contract["create_only"])
            self.assertEqual(
                research_contract["payload_base"]["operation"],
                "direct_take_research",
            )
            self.assertEqual(
                set(research_contract["required_runtime_fields"]),
                {
                    "request_id",
                    "worker_id",
                    "scheduled_slot",
                    "run_key",
                    "actual_invocation_start",
                    "requested_at",
                },
            )
            discovery_packet = index["discovery"]["backward"][0]
            self.assertEqual(discovery_packet["preload_id"], "preload-hot")
            discovery_contract = discovery_packet["direct_take_contract"]
            self.assertTrue(discovery_contract["create_only"])
            self.assertEqual(
                discovery_contract["payload_base"]["operation"],
                "direct_take_discovery",
            )
            self.assertTrue(discovery_contract["payload_base"]["direct_take"])
            self.assertEqual(
                discovery_contract["payload_base"]["preload_id"],
                "preload-hot",
            )
            self.assertEqual(
                discovery_contract["payload_base"]["work_mode_at_start"],
                "discovery",
            )
            self.assertEqual(
                set(discovery_contract["required_runtime_fields"]),
                {
                    "request_id",
                    "worker_id",
                    "scheduled_slot",
                    "run_key",
                    "actual_invocation_start",
                    "claimed_at",
                    "lease_expires_at",
                },
            )
            self.assertTrue((root / hot_dispatch.INDEX).is_file())

    def test_index_exposes_same_worker_active_claim_for_zero_wait_resume(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            job_id = "job-carryover-resume"
            write_json(
                root / ".survey/work-queue/jobs" / f"{job_id}.json",
                {
                    "job_id": job_id,
                    "type": "research",
                    "status": "ready",
                    "title": "Carry-over paper",
                    "depends_on_job_ids": [job_id],
                },
            )
            write_json(
                root / ".survey/work-queue/claims" / f"{job_id}.json",
                {
                    "schema_version": 1,
                    "claim_id": "claim-carryover",
                    "job_id": job_id,
                    "worker_id": "scheduled-chat-30",
                    "worker_kind": "scheduled_chat",
                    "attempt_id": "attempt-carryover",
                    "claimed_at": current.isoformat(),
                    "expires_at": (current + dt.timedelta(hours=2)).isoformat(),
                    "kind": "research",
                    "pipeline_order": 0,
                    "run_key": "old-run",
                    "scheduled_slot": "30",
                    "actual_invocation_start": current.isoformat(),
                },
            )

            index = hot_dispatch.build_index(root)
            packets = index["research_resume"]["scheduled-chat-30"]
            self.assertEqual(len(packets), 1)
            self.assertEqual(packets[0]["job_id"], job_id)
            self.assertEqual(packets[0]["pipeline_role"], "foreground")
            self.assertTrue(packets[0]["resume_without_new_claim"])
            self.assertTrue(packets[0]["work_start_allowed"])
            self.assertFalse(packets[0]["record_write_allowed"])
            self.assertEqual(
                packets[0]["status_only_submission_path"],
                ".survey/work-queue/submissions/research/attempt-carryover.json",
            )
            self.assertEqual(
                packets[0]["source_unavailable_next_action"],
                "WRITE_STATUS_ONLY_BLOCKED_DESCRIPTOR_THEN_CONTINUE_STANDBY",
            )
            self.assertEqual(
                packets[0]["status_only_descriptor_base"],
                {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": "research",
                    "attempt_id": "attempt-carryover",
                    "job_id": job_id,
                    "claim_id": "claim-carryover",
                    "worker_id": "scheduled-chat-30",
                },
            )

            recovery = packets[0]["platform_content_write_recovery"]
            self.assertTrue(recovery["create_only"])
            self.assertTrue(recovery["continue_after_durable_create"])
            self.assertEqual(recovery["retry_policy"], "blocked_retry_7d")
            self.assertEqual(
                recovery["submission_path"],
                ".survey/work-queue/submissions/research/attempt-carryover.json",
            )
            self.assertEqual(recovery["descriptor"]["status"], "blocked")
            self.assertEqual(
                recovery["descriptor"]["reason"],
                "platform_content_write_rejected_after_bundle_fallback",
            )
            self.assertNotIn("record_bank", recovery["descriptor"])
            self.assertNotIn("record_slots", recovery["descriptor"])

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

    def test_stale_discovery_temporarily_overrides_research_route_near_threshold(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            research_packets = [{"claim_id": "claim-hot"}]
            discovery_packets = {
                "backward": [{"preload_id": "preload-hot", "preload_unseen_result_count": 20}],
                "forward": [],
                "normal": [],
            }
            with (
                mock.patch.object(hot_dispatch, "_utcnow", return_value=current),
                mock.patch.object(
                    hot_dispatch,
                    "_candidate_inventory",
                    return_value=claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD + 11,
                ),
                mock.patch.object(
                    hot_dispatch,
                    "_latest_discovery_completion",
                    return_value=current - dt.timedelta(hours=3),
                ),
                mock.patch.object(hot_dispatch, "_research_packets", return_value=research_packets),
                mock.patch.object(hot_dispatch, "_discovery_packets", return_value=discovery_packets),
                mock.patch.object(
                    hot_dispatch.shared_preload_pool,
                    "sync_research_bank_sidecars",
                    return_value={},
                ),
            ):
                index = hot_dispatch.build_index(root)

            self.assertEqual(index["suggested_work_mode"], "discovery")
            self.assertTrue(index["discovery_refresh_due"])
            self.assertGreaterEqual(
                index["discovery_age_seconds"],
                claim_window_policy.DISCOVERY_REFRESH_INTERVAL_SECONDS,
            )
            self.assertTrue(index["direct_start_allowed"])

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

            refill_request = root / hot_dispatch.CLAIM_REQUESTS / Path(direct["canonical_claim_result_path"]).name
            self.assertTrue(refill_request.is_file())
            refill_request.unlink()
            recovered = hot_dispatch.process_research_takes(root)
            self.assertEqual(len(recovered["created_refill_requests"]), 1)
            self.assertTrue(refill_request.is_file())

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

    def test_accounted_discovery_round_no_longer_consumes_frontier_capacity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            run_key = "run-frontier-release"
            for preload_id, request_id, auto_frontier in (
                ("preload-primary", "request-primary", False),
                ("preload-done", "request-done", True),
                ("preload-open", "request-open", True),
            ):
                write_json(
                    root / hot_dispatch.DISCOVERY_CLAIMS / f"{preload_id}.json",
                    {
                        "schema_version": 1,
                        "operation": "direct_take_discovery",
                        "direct_take": True,
                        "preload_id": preload_id,
                        "worker_id": "worker-78",
                        "run_key": run_key,
                        "request_id": request_id,
                        "claimed_at": current.isoformat(),
                        "lease_expires_at": (current + dt.timedelta(minutes=30)).isoformat(),
                        "auto_frontier": auto_frontier,
                    },
                )
            write_json(
                root / ".survey/work-queue/discovery-state.json",
                {
                    "schema_version": 3,
                    "history": [
                        {
                            "run_key": run_key,
                            "precheck_request_id": "request-done",
                            "round_accounted": True,
                        }
                    ],
                },
            )

            active = hot_dispatch._active_direct_discovery_claims(
                root,
                worker_id="worker-78",
                run_key=run_key,
            )
            self.assertEqual(
                {row["request_id"] for row in active},
                {"request-primary", "request-open"},
            )


    def test_direct_discovery_take_pre_reserves_bounded_work_frontier(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            primary_id = "preload-frontier-primary"
            primary_request_id = "frontier-primary-request"
            write_json(
                root / hot_dispatch.DISCOVERY_ENTRIES / f"{primary_id}.json",
                {
                    "preload_id": primary_id,
                    "axis": "primary-backward",
                    "provider": "repository_references",
                    "source_url": "repository://structured-references",
                    "citation_direction": "backward",
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 25,
                    "initial_cursor": None,
                },
            )
            write_json(
                root / hot_dispatch.DISCOVERY_CLAIMS / f"{primary_id}.json",
                {
                    "schema_version": 1,
                    "operation": "direct_take_discovery",
                    "direct_take": True,
                    "preload_id": primary_id,
                    "worker_id": "worker-78",
                    "run_key": "run-frontier",
                    "request_id": primary_request_id,
                    "requested_at": current.isoformat(),
                    "preload_result_path": ".survey/work-queue/discovery-precheck/results/preload-primary.json",
                    "discovery_bank": "a",
                    "discovery_slot_path": discovery_slot_path("a"),
                    "scheduled_slot": "adhoc",
                    "actual_invocation_start": current.isoformat(),
                    "candidate_inventory_at_start": 100,
                    "work_mode_at_start": "discovery",
                    "research_discovery_threshold": claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD,
                    "hot_dispatch_generated_at": current.isoformat(),
                },
            )

            packets = []
            for index, bank in enumerate(("b", "c"), start=1):
                preload_id = f"preload-frontier-{index}"
                entry = {
                    "preload_id": preload_id,
                    "axis": f"frontier-forward-{index}",
                    "provider": "semantic_scholar",
                    "source_url": f"https://example.invalid/citations/{index}",
                    "citation_direction": "forward",
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 25,
                    "initial_cursor": None,
                }
                write_json(
                    root / hot_dispatch.DISCOVERY_ENTRIES / f"{preload_id}.json",
                    entry,
                )
                packets.append(
                    {
                        **entry,
                        "discovery_bank": bank,
                        "discovery_slot_path": discovery_slot_path(bank),
                        "preload_result_path": (
                            f".survey/work-queue/discovery-precheck/results/{preload_id}.json"
                        ),
                        "preload_unseen_result_count": 20,
                        "created_at": current.isoformat(),
                    }
                )

            def available(_root, *, direction=None, limit=32):
                if direction == "forward":
                    return packets[:limit]
                return []

            with mock.patch.object(
                hot_dispatch.discovery_preload_queue,
                "available_preloads",
                side_effect=available,
            ):
                result = hot_dispatch.materialize_discovery_prechecks(root)

            self.assertEqual(result["frontier_target"], 3)
            self.assertEqual(result["frontier_reserved"], 2)
            self.assertEqual(result["created"], 3)

            for packet in packets:
                preload_id = packet["preload_id"]
                claim = json.loads(
                    (root / hot_dispatch.DISCOVERY_CLAIMS / f"{preload_id}.json")
                    .read_text(encoding="utf-8")
                )
                self.assertTrue(claim["auto_frontier"])
                self.assertEqual(claim["frontier_parent_preload_id"], primary_id)
                self.assertEqual(claim["run_key"], "run-frontier")
                self.assertTrue(
                    (root / hot_dispatch.PRECHECK_REQUESTS / f"{claim['request_id']}.json")
                    .is_file()
                )

            primary_direct = json.loads(
                (root / hot_dispatch.DIRECT_DISCOVERY_RESULTS / f"{primary_id}.json")
                .read_text(encoding="utf-8")
            )
            self.assertTrue(primary_direct["frontier_work_available"])
            self.assertEqual(primary_direct["frontier_target"], 3)
            self.assertEqual(
                {row["preload_id"] for row in primary_direct["reserved_frontier"]},
                {packet["preload_id"] for packet in packets},
            )


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
            self.assertEqual(result["candidate_inventory"], 400)
            self.assertEqual(result["work_mode"], "discovery")
            self.assertEqual(result["route_source"], "hot_dispatch_direct_start")



    def test_cold_backward_fallback_exposes_productive_forward_start_lookahead(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()

            def available(_root, *, direction=None, limit=32):
                if direction != "forward":
                    return []
                return [{
                    "preload_id": "preload-forward-lookahead",
                    "discovery_bank": "b",
                    "discovery_slot_path": discovery_slot_path("b"),
                    "citation_direction": "forward",
                    "provider": "semantic_scholar",
                    "source_url": "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2303.06865/citations",
                    "axis": "preload-forward",
                    "initial_cursor": None,
                    "target_unseen": 20,
                    "page_size": 20,
                    "max_pages": 25,
                    "preload_result_path": ".survey/work-queue/discovery-precheck/results/preload-forward-lookahead.json",
                    "preload_unseen_result_count": 20,
                    "created_at": current.isoformat(),
                }][:limit]

            with mock.patch.object(
                hot_dispatch.discovery_preload_queue,
                "available_preloads",
                side_effect=available,
            ):
                index = hot_dispatch.refresh(root)

            self.assertEqual(index["suggested_work_mode"], "discovery")
            self.assertEqual(index["discovery_primary_direction"], "backward")
            self.assertFalse(index["direct_start_allowed"])
            self.assertTrue(index["fallback_start_allowed"])
            self.assertTrue(index["zero_wait_start_allowed"])
            self.assertTrue(index["zero_wait_content_start_allowed"])
            self.assertEqual(
                index["discovery_start_lookahead"]["preload_id"],
                "preload-forward-lookahead",
            )
            self.assertIn(
                ".survey/work-queue/discovery-preload/claims/",
                index["discovery_start_lookahead"]["take_path"],
            )


    def test_discovery_cold_start_exposes_zero_wait_fixed_source_fallback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with mock.patch.object(
                hot_dispatch.discovery_preload_queue,
                "available_preloads",
                return_value=[],
            ):
                index = hot_dispatch.refresh(root)

            self.assertEqual(index["suggested_work_mode"], "discovery")
            self.assertFalse(index["direct_start_allowed"])
            self.assertTrue(index["fallback_start_allowed"])
            self.assertTrue(index["zero_wait_start_allowed"])
            self.assertFalse(index["zero_wait_content_start_allowed"])
            self.assertIsNone(index["discovery_start_lookahead"])
            self.assertTrue(index["idle_gap_guard"]["passive_wait_forbidden"])
            self.assertEqual(
                index["discovery_fallback"]["source_url"],
                "repository://structured-references",
            )
    def test_index_exposes_expired_partial_record_as_same_worker_recovery_take(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            current = now()
            job_id = "job-recovery-resume"
            claim_id = "claim-preload-recovery"
            write_json(
                root / ".survey/work-queue/jobs" / f"{job_id}.json",
                {
                    "job_id": job_id,
                    "type": "research",
                    "status": "ready",
                    "title": "Interrupted paper",
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
                    "attempt_id": "attempt-preload-recovery",
                    "claimed_at": current.isoformat(),
                    "preloaded_at": current.isoformat(),
                    "expires_at": (current + dt.timedelta(hours=12)).isoformat(),
                    "kind": "research",
                    "depends_on_job_ids": [job_id],
                    "preload_pool": True,
                    "pool_order": 17,
                },
            )
            from record_bank_config import BANK_ROOTS, SLOT_NAMES
            for index, slot in enumerate(SLOT_NAMES):
                write_json(
                    root / BANK_ROOTS["m"] / f"{slot}.json",
                    {
                        "schema_version": 1,
                        "transport_version": 10,
                        "slot": slot,
                        "attempt_id": "attempt-old-interrupted",
                        "job_id": job_id,
                        "data": {"draft": "kept"} if index == 0 else {},
                        "reservation": {
                            "claim_id": "claim-old-interrupted",
                            "worker_id": "scheduled-chat-00",
                            "worker_kind": "scheduled_chat",
                        },
                    },
                )

            index = hot_dispatch.build_index(root)
            recovery = index["research_recovery_resume"]["scheduled-chat-00"][0]
            self.assertEqual(recovery["claim_id"], claim_id)
            self.assertEqual(recovery["recovery_source_attempt_id"], "attempt-old-interrupted")
            self.assertEqual(recovery["recovery_source_record_bank"], "m")
            self.assertTrue(recovery["resume_requires_direct_take"])
            self.assertEqual(
                recovery["direct_take_contract"]["payload_base"]["claim_id"],
                claim_id,
            )
            self.assertNotIn(job_id, [row["job_id"] for row in index["research"]])


if __name__ == "__main__":
    unittest.main()
