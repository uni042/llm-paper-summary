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
from record_bank_config import BANK_IDS, BANK_ROOTS, SLOT_NAMES, discovery_slot_path  # noqa: E402


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
            self.assertIn(entry["discovery_bank"], BANK_IDS)
            self.assertEqual(request["discovery_bank"], entry["discovery_bank"])
            self.assertEqual(
                request["discovery_slot_path"],
                discovery_slot_path(entry["discovery_bank"]),
            )

        bound = preload._read_bank_bindings(self.root)
        self.assertEqual(len(bound), 2)
        for bank in BANK_IDS:
            self.assertTrue((self.root / discovery_slot_path(bank)).is_file())

    def test_discovery_sidecar_does_not_touch_research_slots(self) -> None:
        sentinel_bank = "a"
        sentinel_slot = SLOT_NAMES[0]
        sentinel_path = self.root / BANK_ROOTS[sentinel_bank] / f"{sentinel_slot}.json"
        sentinel = {
            "schema_version": 1,
            "transport_version": 10,
            "slot": sentinel_slot,
            "attempt_id": "attempt-reading",
            "job_id": "job-reading",
            "data": {"text": "research payload must survive Discovery rotation"},
        }
        write_json(sentinel_path, sentinel)

        forward = self._prepare_forward_result()
        self.assertEqual(
            json.loads(sentinel_path.read_text(encoding="utf-8")),
            sentinel,
        )

        available = preload.pick_available(self.root, direction="forward")
        self.assertIsNotNone(available)
        bank = available["discovery_bank"]
        request = {
            "request_id": "real-dual-bank",
            "worker_id": "worker-9",
            "run_key": "real-dual-run",
            "preload_id": forward["preload_id"],
            "provider": forward["provider"],
            "source_url": forward["source_url"],
            "axis": forward["axis"],
            "initial_cursor": forward["initial_cursor"],
            "page_size": forward["page_size"],
            "discovery_bank": bank,
            "discovery_slot_path": discovery_slot_path(bank),
        }
        preload.claim_and_load(self.root, request)

        sidecar = json.loads(
            (self.root / discovery_slot_path(bank)).read_text(encoding="utf-8")
        )
        self.assertIsNone(sidecar["preload_id"])
        self.assertEqual(
            json.loads(sentinel_path.read_text(encoding="utf-8")),
            sentinel,
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

    def test_compact_direct_take_hands_off_to_same_run_formal_request(self) -> None:
        entry = self._prepare_forward_result()
        available = preload.pick_available(self.root, direction="forward")
        self.assertIsNotNone(available)
        current = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
        claim_path = self.root / preload._claim_path(entry["preload_id"])
        write_json(
            claim_path,
            {
                "schema_version": 1,
                "operation": "direct_take_discovery",
                "request_id": "direct-take-reservation",
                "preload_id": entry["preload_id"],
                "worker_id": "worker-3",
                "run_key": "same-run",
                "requested_at": current.isoformat(),
                "discovery_bank": available["discovery_bank"],
                "discovery_slot_path": available["discovery_slot_path"],
            },
        )

        # A compact create-only reservation is immediately exclusive even before
        # the background lane rewrites it with an explicit lease.
        active = preload._active_claim(self.root, entry["preload_id"], current)
        self.assertIsNotNone(active)
        self.assertIsNone(preload.pick_available(self.root, direction="forward"))

        formal = {
            "request_id": "formal-precheck-request",
            "worker_id": "worker-3",
            "run_key": "same-run",
            "preload_id": entry["preload_id"],
            "provider": entry["provider"],
            "source_url": entry["source_url"],
            "axis": entry["axis"],
            "initial_cursor": entry["initial_cursor"],
            "page_size": entry["page_size"],
            "discovery_bank": available["discovery_bank"],
            "discovery_slot_path": available["discovery_slot_path"],
        }
        adopted_entry, loaded = preload.claim_and_load(self.root, formal)
        self.assertEqual(adopted_entry["preload_id"], entry["preload_id"])
        self.assertEqual(loaded["run_key"], f"preload:{entry['preload_id']}")
        canonical = json.loads(claim_path.read_text(encoding="utf-8"))
        self.assertEqual(canonical["request_id"], "formal-precheck-request")
        self.assertEqual(canonical["worker_id"], "worker-3")
        self.assertEqual(canonical["run_key"], "same-run")
        self.assertIn("lease_expires_at", canonical)

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


    def test_exhausted_repository_reference_source_restarts_from_zero(self) -> None:
        first = preload.top_up(self.root, target=1, max_new=1)
        self.assertEqual(first["created_count"], 1)
        entry = preload._entries(self.root)[0]
        self.assertEqual(entry["provider"], "repository_references")
        write_json(
            self.root / preload._result_path(entry),
            {
                "schema_version": 3,
                "operation": "precheck_discovery_candidates",
                "ok": True,
                "evaluation_allowed": True,
                "request_id": entry["precheck_request_id"],
                "run_key": f"preload:{entry['preload_id']}",
                "results": [],
                "allowed_records": [],
                "unseen_result_count": 0,
                "next_cursor": None,
                "provider_exhausted": True,
            },
        )
        write_json(
            self.root / preload._ingested_path(entry["preload_id"]),
            {
                "schema_version": 1,
                "preload_id": entry["preload_id"],
                "run_key": "finished-run",
            },
        )

        second = preload.top_up(self.root, target=1, max_new=1)
        self.assertEqual(second["available_before"], 0)
        self.assertEqual(second["created_count"], 1)
        replacement = next(
            row
            for row in preload._entries(self.root)
            if row["preload_id"] == second["created"][0]
        )
        self.assertIsNone(replacement["initial_cursor"])
        self.assertGreater(int(replacement["sequence"]), int(entry["sequence"]))


    def test_available_preloads_returns_empty_list_when_stock_is_empty(self) -> None:
        self.assertEqual(
            preload.available_preloads(self.root, direction="backward"),
            [],
        )

    def test_available_preloads_prefers_productive_window_over_empty_window(self) -> None:
        now = dt.datetime.now(dt.timezone.utc)
        source = {
            "source_key": "same-forward-source",
            "provider": "semantic_scholar",
            "source_url": "https://api.semanticscholar.org/graph/v1/paper/ARXIV:2303.06865/citations",
            "citation_direction": "forward",
            "axis": "forward test",
            "seed_canonical_id": "arXiv:2303.06865",
        }
        empty = preload._make_entry(
            source,
            bucket=preload._refresh_bucket(now),
            sequence=0,
            initial_cursor=None,
            now=now - dt.timedelta(seconds=1),
            discovery_bank="a",
        )
        productive = preload._make_entry(
            source,
            bucket=preload._refresh_bucket(now),
            sequence=1,
            initial_cursor="20",
            now=now,
            discovery_bank="b",
        )
        for entry, count in ((empty, 0), (productive, 20)):
            write_json(
                self.root / preload.ENTRIES / f"{entry['preload_id']}.json",
                entry,
            )
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
                    "results": [
                        {
                            "canonical_id": f"arXiv:2609.{index:05d}",
                            "title": f"Candidate {index}",
                            "source_url": f"https://arxiv.org/abs/2609.{index:05d}",
                        }
                        for index in range(count)
                    ],
                    "allowed_records": [],
                    "unseen_result_count": count,
                    "next_cursor": None,
                    "provider_exhausted": count == 0,
                },
            )
            preload._write_bank_binding(
                self.root,
                str(entry["discovery_bank"]),
                entry,
            )

        rows = preload.available_preloads(
            self.root,
            direction="forward",
            limit=2,
        )
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["preload_id"], productive["preload_id"])
        self.assertEqual(rows[0]["preload_unseen_result_count"], 20)
        self.assertEqual(rows[1]["preload_id"], empty["preload_id"])


    def test_fixed_source_fallback_reuses_preload_source_policy(self) -> None:
        backward = preload.fallback_source(self.root, direction="backward")
        self.assertIsNotNone(backward)
        self.assertEqual(backward["source_kind"], "fixed_source_fallback")
        self.assertEqual(backward["citation_direction"], "backward")
        self.assertEqual(backward["provider"], "repository_references")
        self.assertEqual(backward["source_url"], "repository://structured-references")
        self.assertEqual(backward["target_unseen"], preload.DEFAULT_TARGET_UNSEEN)

        forward = preload.fallback_source(self.root, direction="forward")
        self.assertIsNotNone(forward)
        self.assertEqual(forward["citation_direction"], "forward")
        self.assertEqual(forward["provider"], "semantic_scholar")

if __name__ == "__main__":
    unittest.main()
