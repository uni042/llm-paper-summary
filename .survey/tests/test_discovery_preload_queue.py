#!/usr/bin/env python3
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

import discovery_preload_queue as preload  # noqa: E402
import process_discovery_precheck as precheck  # noqa: E402
from record_bank_config import BANK_IDS, BANK_ROOTS  # noqa: E402


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class DiscoveryPreloadQueueTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        write_json(
            self.root / preload.DISCOVERY_STATE,
            {
                "schema_version": 3,
                "history": [
                    {
                        "run_key": "old-run",
                        "round": "forward-flexgen",
                        "axis": "forward FlexGen citations",
                        "provider": "semantic_scholar",
                        "source_url": (
                            "https://api.semanticscholar.org/graph/v1/paper/"
                            "ARXIV:2303.06865/citations"
                        ),
                        "citation_direction": "forward",
                        "seed_canonical_id": "arXiv:2303.06865",
                        "candidate_count": 20,
                        "novel_candidate_count": 12,
                        "accepted_count": 5,
                        "round_accounted": True,
                    }
                ],
            },
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def _prepare_forward_result(self) -> dict:
        created = preload.top_up(self.root, target=2, max_new=2)
        self.assertEqual(created["created_count"], 2)
        entries = preload._entries(self.root)
        forward = next(row for row in entries if row["citation_direction"] == "forward")
        records = [
            {
                "canonical_id": f"arXiv:2609.{index:05d}",
                "title": f"Cached paper {index}",
                "source_url": f"https://arxiv.org/abs/2609.{index:05d}",
            }
            for index in range(20)
        ]
        write_json(
            self.root / preload._result_path(forward),
            {
                "schema_version": 3,
                "operation": "precheck_discovery_candidates",
                "ok": True,
                "evaluation_allowed": True,
                "decision": "READY_FOR_EVALUATION",
                "request_id": forward["precheck_request_id"],
                "run_key": f"preload:{forward['preload_id']}",
                "axis": forward["axis"],
                "provider": forward["provider"],
                "source_url": forward["source_url"],
                "unseen_result_count": 20,
                "results": records,
                "allowed_records": [],
                "next_cursor": "20",
                "provider_exhausted": False,
            },
        )
        return forward

    def test_top_up_builds_backward_and_forward_stock(self) -> None:
        result = preload.top_up(self.root, target=2, max_new=2)
        self.assertEqual(result["created_count"], 2)
        entries = preload._entries(self.root)
        self.assertEqual({row["citation_direction"] for row in entries}, {"backward", "forward"})
        for entry in entries:
            request = json.loads(
                (self.root / preload.PRECHECK_REQUESTS / f"{entry['precheck_request_id']}.json")
                .read_text(encoding="utf-8")
            )
            self.assertTrue(request["preload_seed"])
            self.assertEqual(request["preload_id"], entry["preload_id"])
            self.assertEqual(request["page_size"], 20)
            self.assertEqual(request["target_unseen"], 20)
            self.assertTrue(request["run_key"].startswith("preload:"))
            self.assertEqual(request["stock_bank"], entry["stock_bank"])
            self.assertEqual(request["stock_lane"], "discovery")
        self.assertEqual(
            {row["stock_bank"] for row in entries},
            set(BANK_IDS[:2]),
        )

    def test_bank_coverage_refills_in_canonical_order(self) -> None:
        first = preload.top_up(self.root, target=2, max_new=1)
        self.assertEqual(first["created_count"], 1)
        entry = preload._entries(self.root)[0]
        self.assertEqual(entry["stock_bank"], BANK_IDS[0])
        write_json(
            self.root / preload._result_path(entry),
            {
                "schema_version": 3,
                "operation": "precheck_discovery_candidates",
                "ok": True,
                "evaluation_allowed": True,
                "decision": "READY_FOR_EVALUATION",
                "request_id": entry["precheck_request_id"],
                "run_key": f"preload:{entry['preload_id']}",
                "axis": entry["axis"],
                "provider": entry["provider"],
                "source_url": entry["source_url"],
                "unseen_result_count": 20,
                "results": [],
                "allowed_records": [],
                "next_cursor": "20",
                "provider_exhausted": False,
            },
        )

        second = preload.top_up(self.root, target=2, max_new=1)
        self.assertEqual(second["available_before"], 1)
        self.assertEqual(second["created_count"], 1)
        entries = preload._entries(self.root)
        self.assertEqual(
            {row["stock_bank"] for row in entries},
            set(BANK_IDS[:2]),
        )

    def test_failed_preload_does_not_count_as_stock_and_is_replaced(self) -> None:
        first = preload.top_up(self.root, target=1, max_new=1)
        self.assertEqual(first["created_count"], 1)
        entry = preload._entries(self.root)[0]
        write_json(
            self.root / preload._result_path(entry),
            {
                "schema_version": 3,
                "operation": "precheck_discovery_candidates",
                "ok": False,
                "request_id": entry["precheck_request_id"],
                "run_key": f"preload:{entry['preload_id']}",
                "error": "synthetic transient provider failure",
            },
        )
        self.assertEqual(preload._status(self.root, entry, dt.datetime.now(dt.timezone.utc)), "FAILED")

        second = preload.top_up(self.root, target=1, max_new=1)
        self.assertEqual(second["available_before"], 0)
        self.assertEqual(second["created_count"], 1)
        self.assertNotEqual(second["created"][0], entry["preload_id"])

    def test_claim_is_exclusive_then_expired_claim_is_reusable(self) -> None:
        entry = self._prepare_forward_result()
        available = preload.pick_available(self.root, direction="forward")
        self.assertIsNotNone(available)
        request = {
            "request_id": "real-request-1",
            "worker_id": "worker-1",
            "run_key": "real-run-1",
            "preload_id": entry["preload_id"],
            "provider": entry["provider"],
            "source_url": entry["source_url"],
            "axis": entry["axis"],
            "initial_cursor": entry["initial_cursor"],
            "page_size": entry["page_size"],
            "stock_bank": entry["stock_bank"],
            "stock_lane": "discovery",
        }
        preload.claim_and_load(self.root, request)

        competing = dict(request)
        competing.update(
            {
                "request_id": "real-request-2",
                "worker_id": "worker-2",
                "run_key": "real-run-2",
            }
        )
        with self.assertRaisesRegex(ValueError, "actively claimed"):
            preload.claim_and_load(self.root, competing)

        claim_path = self.root / preload._claim_path(entry["preload_id"])
        claim = json.loads(claim_path.read_text(encoding="utf-8"))
        claim["lease_expires_at"] = (
            dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=1)
        ).isoformat()
        write_json(claim_path, claim)
        _, loaded = preload.claim_and_load(self.root, competing)
        self.assertEqual(loaded["run_key"], f"preload:{entry['preload_id']}")

        self.assertTrue(
            preload.mark_ingested(
                self.root,
                preload_id=entry["preload_id"],
                run_key="real-run-2",
                source_submission=".survey/work-queue/submissions/round.json",
            )
        )
        self.assertFalse((self.root / preload._claim_path(entry["preload_id"])).exists())
        self.assertIsNone(preload.pick_available(self.root, direction="forward"))

    def test_old_prechecked_window_becomes_stale(self) -> None:
        entry = self._prepare_forward_result()
        entry_path = self.root / preload.ENTRIES / f"{entry['preload_id']}.json"
        stored = json.loads(entry_path.read_text(encoding="utf-8"))
        stored["created_at"] = (
            dt.datetime.now(dt.timezone.utc)
            - dt.timedelta(seconds=preload.PRELOAD_MAX_AGE_SECONDS + 1)
        ).isoformat()
        write_json(entry_path, stored)
        now = dt.datetime.now(dt.timezone.utc)
        self.assertEqual(preload._status(self.root, stored, now), "STALE")
        self.assertIsNone(preload.pick_available(self.root, direction="forward"))

    def test_adoption_reuses_cached_window_without_initializing_live_provider(self) -> None:
        entry = self._prepare_forward_result()
        request = {
            "schema_version": 3,
            "operation": "precheck_discovery_candidates",
            "request_id": "real-precheck",
            "collector_id": "real-collector",
            "run_key": "real-run",
            "axis": entry["axis"],
            "provider": entry["provider"],
            "source_url": entry["source_url"],
            "target_unseen": 20,
            "page_size": entry["page_size"],
            "max_pages": entry["max_pages"],
            "initial_cursor": entry["initial_cursor"],
            "preload_id": entry["preload_id"],
            "preload_seed": False,
            "worker_id": "worker-7",
            "stock_bank": entry["stock_bank"],
            "stock_lane": "discovery",
        }
        snapshot = self.root / "snapshot"
        write_json(snapshot / "_manifest.json", {"source_commit": "abc123"})
        rejection = self.root / "rejections.json"
        write_json(rejection, {})

        def collect(fetch_page, **kwargs):
            page = fetch_page(kwargs.get("initial_cursor"))
            self.assertEqual(len(page["records"]), 20)
            return {
                "results": list(page["records"]),
                "pages_fetched": 1,
                "next_cursor": page["next_cursor"],
                "target_reached": True,
                "provider_exhausted": False,
                "max_pages_reached": False,
                "raw_search_result_count": 20,
                "retrieval_duplicate_filtered_count": 0,
                "represented_paper_match_filtered_count": 0,
                "rejection_ledger_filtered_count": 0,
                "intra_batch_duplicate_filtered_count": 0,
                "intra_batch_alias_duplicate_filtered_count": 0,
                "cross_page_duplicate_filtered_count": 0,
                "cross_page_alias_duplicate_filtered_count": 0,
                "unresolved_identity_count": 0,
                "unseen_result_count": 20,
                "provider_progress": None,
            }

        with mock.patch.object(
            precheck.discovery_provider_adapter,
            "make_fetcher",
            side_effect=AssertionError("live provider must not initialize on a full preload hit"),
        ), mock.patch.object(
            precheck.discovery_search_filter,
            "collect_until_unseen",
            side_effect=collect,
        ):
            result = precheck._process_v3(
                request,
                snapshot_dir=snapshot,
                rejection_ledger_path=rejection,
                repo_root=self.root,
            )

        self.assertTrue(result["preload_cache_used"])
        self.assertEqual(result["preload_cached_pages_used"], 1)
        self.assertEqual(result["preload_live_pages_fetched"], 0)
        self.assertEqual(result["run_key"], "real-run")
        self.assertEqual(result["preload_id"], entry["preload_id"])
        self.assertEqual(result["stock_bank"], entry["stock_bank"])
        self.assertEqual(result["stock_lane"], "discovery")


if __name__ == "__main__":
    unittest.main()
