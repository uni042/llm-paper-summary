from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discovery_search_filter  # noqa: E402


class DiscoverySearchFilterTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.snapshot = Path(self.tmp.name) / "discovery-identities"
        self.snapshot.mkdir(parents=True)
        (self.snapshot / "_manifest.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "source": "queue_worker.existing_candidate_keys",
                    "code_search_is_authority": False,
                    "shards": {
                        "arxiv-2601.txt": 1,
                        "arxiv-2606.txt": 2,
                    },
                }
            ),
            encoding="utf-8",
        )
        (self.snapshot / "arxiv-2601.txt").write_text(
            "id:arXiv:2601.10729\n",
            encoding="utf-8",
        )
        (self.snapshot / "arxiv-2606.txt").write_text(
            "id:arXiv:2606.24467\nid:arXiv:2606.24506\n",
            encoding="utf-8",
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_filters_existing_papers_before_candidate_evaluation(self) -> None:
        page = [
            {
                "canonical_id": "arXiv:2606.24506",
                "title": "CrossPool: Efficient Multi-LLM Serving for Cold MoE Models",
            },
            {
                "source_url": "https://arxiv.org/abs/2606.24467",
                "title": "CompressKV",
            },
            {
                "arxiv_id": "2601.10729",
                "title": "ORBITFLOW",
            },
            {
                "arxiv_id": "2609.99999",
                "title": "Actually New Paper",
            },
        ]

        result = discovery_search_filter.filter_search_batch(
            page,
            snapshot_dir=self.snapshot,
            target_unseen=3,
            provider_has_more=True,
        )

        self.assertEqual([row["title"] for row in result["results"]], ["Actually New Paper"])
        self.assertEqual(result["raw_search_result_count"], 4)
        self.assertEqual(result["retrieval_duplicate_filtered_count"], 3)
        self.assertEqual(result["unseen_result_count"], 1)
        self.assertTrue(result["continue_search"])

    def test_does_not_continue_when_enough_unseen_results_exist(self) -> None:
        page = [
            {"arxiv_id": "2609.99998", "title": "New Paper A"},
            {"arxiv_id": "2609.99999", "title": "New Paper B"},
        ]

        result = discovery_search_filter.filter_search_batch(
            page,
            snapshot_dir=self.snapshot,
            target_unseen=2,
            provider_has_more=True,
        )

        self.assertEqual(result["unseen_result_count"], 2)
        self.assertFalse(result["continue_search"])

    def test_missing_snapshot_fails_closed(self) -> None:
        missing = Path(self.tmp.name) / "missing"

        with self.assertRaises(discovery_search_filter.SnapshotUnavailableError):
            discovery_search_filter.filter_search_batch(
                [{"arxiv_id": "2609.99999", "title": "Unknown"}],
                snapshot_dir=missing,
                target_unseen=1,
                provider_has_more=True,
            )

    def test_collector_fetches_multiple_pages_before_returning_unseen_buffer(self) -> None:
        pages = {
            None: {
                "records": [
                    {"arxiv_id": "2606.24506", "title": "CrossPool"},
                    {"arxiv_id": "2609.90001", "title": "New A"},
                ],
                "next_cursor": "page-2",
            },
            "page-2": {
                "records": [
                    {"arxiv_id": "2601.10729", "title": "ORBITFLOW"},
                    {"arxiv_id": "2609.90001", "title": "New A duplicate"},
                    {"arxiv_id": "2609.90002", "title": "New B"},
                ],
                "next_cursor": "page-3",
            },
            "page-3": {
                "records": [
                    {"arxiv_id": "2609.90003", "title": "New C"},
                    {"arxiv_id": "2609.90004", "title": "New D"},
                ],
                "next_cursor": "page-4",
            },
            "page-4": {
                "records": [{"arxiv_id": "2609.90005", "title": "Should not be fetched"}],
                "next_cursor": None,
            },
        }
        calls: list[str | None] = []

        def fetch_page(cursor: str | None) -> dict[str, object]:
            calls.append(cursor)
            return pages[cursor]

        result = discovery_search_filter.collect_until_unseen(
            fetch_page,
            snapshot_dir=self.snapshot,
            target_unseen=3,
        )

        self.assertEqual(calls, [None, "page-2", "page-3"])
        self.assertEqual(
            [row["arxiv_id"] for row in result["results"]],
            ["2609.90001", "2609.90002", "2609.90003", "2609.90004"],
        )
        self.assertEqual(result["pages_fetched"], 3)
        self.assertEqual(result["raw_search_result_count"], 7)
        self.assertEqual(result["retrieval_duplicate_filtered_count"], 2)
        self.assertEqual(result["cross_page_duplicate_filtered_count"], 1)
        self.assertEqual(result["unseen_result_count"], 4)
        self.assertTrue(result["target_reached"])
        self.assertFalse(result["provider_exhausted"])
        self.assertEqual(result["next_cursor"], "page-4")

    def test_collector_collapses_same_new_paper_across_arxiv_and_doi_pages(self) -> None:
        pages = {
            None: {
                "records": [
                    {
                        "arxiv_id": "2609.93001",
                        "title": "Dual-Alias KV Cache Scheduling",
                        "authors": ["Alice Smith"],
                        "year": 2026,
                    }
                ],
                "next_cursor": "page-2",
            },
            "page-2": {
                "records": [
                    {
                        "doi": "10.5555/dual.alias.2026",
                        "title": "Dual Alias KV Cache Scheduling",
                        "authors": ["Alice Smith"],
                        "year": 2026,
                    },
                    {
                        "arxiv_id": "2609.93002",
                        "title": "Actually Distinct Paper",
                    },
                ],
                "next_cursor": None,
            },
        }
        calls: list[str | None] = []

        def fetch_page(cursor: str | None) -> dict[str, object]:
            calls.append(cursor)
            return pages[cursor]

        result = discovery_search_filter.collect_until_unseen(
            fetch_page,
            snapshot_dir=self.snapshot,
            target_unseen=3,
        )

        self.assertEqual(calls, [None, "page-2"])
        self.assertEqual(
            [row["title"] for row in result["results"]],
            ["Dual-Alias KV Cache Scheduling", "Actually Distinct Paper"],
        )
        self.assertEqual(result["cross_page_duplicate_filtered_count"], 1)
        self.assertEqual(result["cross_page_alias_duplicate_filtered_count"], 1)
        self.assertTrue(result["provider_exhausted"])

    def test_collector_returns_partial_buffer_when_provider_is_exhausted(self) -> None:
        calls: list[str | None] = []

        def fetch_page(cursor: str | None) -> dict[str, object]:
            calls.append(cursor)
            if cursor is None:
                return {
                    "records": [{"arxiv_id": "2609.91001", "title": "Only New"}],
                    "next_cursor": "last",
                }
            return {
                "records": [{"arxiv_id": "2606.24467", "title": "CompressKV"}],
                "next_cursor": None,
            }

        result = discovery_search_filter.collect_until_unseen(
            fetch_page,
            snapshot_dir=self.snapshot,
            target_unseen=5,
        )

        self.assertEqual(calls, [None, "last"])
        self.assertEqual([row["title"] for row in result["results"]], ["Only New"])
        self.assertEqual(result["unseen_result_count"], 1)
        self.assertFalse(result["target_reached"])
        self.assertTrue(result["provider_exhausted"])
        self.assertIsNone(result["next_cursor"])

    def test_collector_defaults_to_twenty_unseen_results(self) -> None:
        calls: list[str | None] = []

        def fetch_page(cursor: str | None) -> dict[str, object]:
            calls.append(cursor)
            page_number = 1 if cursor is None else int(cursor)
            start = (page_number - 1) * 5 + 1
            records = [
                {"arxiv_id": f"2609.{92000 + i:05d}", "title": f"New {i}"}
                for i in range(start, start + 5)
            ]
            return {
                "records": records,
                "next_cursor": str(page_number + 1),
            }

        result = discovery_search_filter.collect_until_unseen(
            fetch_page,
            snapshot_dir=self.snapshot,
        )

        self.assertEqual(calls, [None, "2", "3", "4"])
        self.assertEqual(result["target_unseen"], 20)
        self.assertEqual(result["unseen_result_count"], 20)
        self.assertTrue(result["target_reached"])
        self.assertEqual(result["next_cursor"], "5")


if __name__ == "__main__":
    unittest.main()
