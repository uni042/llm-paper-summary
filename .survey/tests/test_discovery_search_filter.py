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


if __name__ == "__main__":
    unittest.main()
