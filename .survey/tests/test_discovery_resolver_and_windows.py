from __future__ import annotations

import importlib
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discovery_search_filter  # noqa: E402
import paper_identity  # noqa: E402
import queue_worker  # noqa: E402


class RepresentedPaperResolverTest(unittest.TestCase):
    def test_alias_graph_unifies_arxiv_doi_and_exact_title_under_one_paper_key(self) -> None:
        build = getattr(paper_identity, "build_represented_resolver", None)
        self.assertIsNotNone(build, "represented-paper resolver is not implemented")

        resolver = build([
            {
                "canonical_id": "arXiv:2601.12345",
                "doi": "10.5555/alias.2026.1",
                "title": "Alias Graphs for Efficient MoE Serving",
                "authors": ["Alice Smith", "Bob Jones"],
                "year": 2026,
            },
            {
                "canonical_id": "DOI:10.5555/alias.2026.1",
                "title": "Alias Graphs for Efficient MoE Serving",
                "authors": ["Smith, Alice"],
                "published": "2026-03-10",
            },
        ])

        self.assertEqual(len(resolver["papers"]), 1)
        arxiv_key = resolver["alias_to_paper"]["id:arXiv:2601.12345"]
        doi_key = resolver["alias_to_paper"]["id:DOI:10.5555/alias.2026.1"]
        self.assertEqual(arxiv_key, doi_key)
        profile = resolver["papers"][arxiv_key]
        self.assertEqual(profile["first_author"], "smith")
        self.assertEqual(profile["year"], 2026)
        self.assertTrue(profile["normalized_title_hash"])

    def test_idless_results_use_exact_title_hash_then_high_confidence_fuzzy_author_year(self) -> None:
        build = getattr(paper_identity, "build_represented_resolver", None)
        match = getattr(paper_identity, "match_represented_paper", None)
        self.assertIsNotNone(build, "represented-paper resolver is not implemented")
        self.assertIsNotNone(match, "represented-paper matcher is not implemented")

        resolver = build([
            {
                "canonical_id": "arXiv:2602.22222",
                "title": "Cache-Aware Expert Prefetch for Efficient MoE Serving",
                "authors": ["Alice Smith", "Bob Jones"],
                "year": 2026,
            }
        ])

        exact = match(
            {
                "title": "Cache Aware Expert Prefetch for Efficient MoE Serving",
                "authors": ["Alice Smith"],
                "year": 2026,
            },
            resolver,
        )
        self.assertIsNotNone(exact)
        self.assertEqual(exact["match_type"], "exact_title_hash")

        fuzzy = match(
            {
                "title": "Cache-Aware Expert Prefetching for Efficient MoE Serving",
                "authors": ["Smith, Alice"],
                "published": "2026-07-01",
            },
            resolver,
        )
        self.assertIsNotNone(fuzzy)
        self.assertEqual(fuzzy["match_type"], "title_fuzzy_author_year")
        self.assertGreaterEqual(fuzzy["title_similarity"], 0.94)

        wrong_author = match(
            {
                "title": "Cache-Aware Expert Prefetching for Efficient MoE Serving",
                "authors": ["Carol Brown"],
                "year": 2026,
            },
            resolver,
        )
        self.assertIsNone(wrong_author)

        identified = match(
            {
                "doi": "10.9999/actually-new",
                "title": "Cache-Aware Expert Prefetching for Efficient MoE Serving",
                "authors": ["Alice Smith"],
                "year": 2026,
            },
            resolver,
        )
        self.assertIsNone(identified, "fuzzy title matching must be restricted to ID-less results")

    def test_retrieval_filter_uses_resolver_before_candidate_evaluation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            snapshot = Path(td) / "discovery-identities"
            snapshot.mkdir()
            resolver = paper_identity.build_represented_resolver([
                {
                    "canonical_id": "arXiv:2602.22222",
                    "title": "Cache-Aware Expert Prefetch for Efficient MoE Serving",
                    "authors": ["Alice Smith"],
                    "year": 2026,
                }
            ])
            (snapshot / "_represented_papers.json").write_text(
                json.dumps(resolver, ensure_ascii=False),
                encoding="utf-8",
            )
            (snapshot / "_manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": 2,
                        "source": "queue_worker.existing_candidate_keys",
                        "code_search_is_authority": False,
                        "shards": {},
                        "represented_resolver_file": "_represented_papers.json",
                    }
                ),
                encoding="utf-8",
            )

            result = discovery_search_filter.filter_search_batch(
                [
                    {
                        "title": "Cache-Aware Expert Prefetching for Efficient MoE Serving",
                        "authors": ["Smith, Alice"],
                        "year": 2026,
                    },
                    {
                        "title": "Cache-Aware Expert Prefetching for Efficient MoE Serving",
                        "authors": ["Carol Brown"],
                        "year": 2026,
                    },
                ],
                snapshot_dir=snapshot,
            )

            self.assertEqual(result["represented_paper_match_filtered_count"], 1)
            self.assertEqual(result["represented_paper_match_types"], ["title_fuzzy_author_year"])
            self.assertEqual(len(result["results"]), 1)
            self.assertEqual(result["results"][0]["authors"], ["Carol Brown"])


class DiscoverySearchWindowHistoryTest(unittest.TestCase):
    def _history_module(self):
        spec = importlib.util.find_spec("discovery_search_history")
        self.assertIsNotNone(spec, "persistent discovery search-window history is not implemented")
        return importlib.import_module("discovery_search_history")

    @staticmethod
    def _window(topic: str, *, raw: int = 0, unseen: int = 0) -> dict[str, object]:
        return {
            "topic": topic,
            "source": "arxiv",
            "date_range": "2026-09",
            "category": "cs.DC",
            "citation_direction": "none",
            "query_family": "moe-serving",
            "raw_result_count": raw,
            "unseen_result_count": unseen,
        }

    def test_history_persists_six_dimensional_windows_and_ranks_unscanned_then_high_unseen_rate(self) -> None:
        history = self._history_module()
        state: dict[str, object] = {}
        history.record_search_windows(
            state,
            [
                self._window("low-yield", raw=10, unseen=1),
                self._window("high-yield", raw=10, unseen=7),
            ],
            run_key="2026-09-17T06:00:00+09:00",
            round_name="round-1",
        )

        self.assertEqual(len(state["search_windows"]), 2)
        for row in state["search_windows"].values():
            for field in history.WINDOW_DIMENSIONS:
                self.assertIn(field, row)
            self.assertEqual(row["scan_count"], 1)

        ranked = history.rank_search_windows(
            [
                self._window("low-yield"),
                self._window("never-scanned"),
                self._window("high-yield"),
            ],
            state,
        )
        self.assertEqual(
            [row["topic"] for row in ranked],
            ["never-scanned", "high-yield", "low-yield"],
        )
        self.assertFalse(ranked[0]["history"]["scanned"])
        self.assertAlmostEqual(ranked[1]["history"]["unseen_rate"], 0.7)

    def test_queue_worker_persists_submission_search_windows_in_discovery_state(self) -> None:
        self._history_module()
        original_state = queue_worker.DISCOVERY_STATE
        try:
            with tempfile.TemporaryDirectory() as td:
                queue_worker.DISCOVERY_STATE = Path(td) / "discovery-state.json"
                sub = {
                    "_file": "work-queue/submissions/window-history.json",
                    "candidates": [],
                    "discovery_stats": {
                        "run_key": "2026-09-17T06:00:00+09:00",
                        "round": "window-history",
                        "axis": "moe-serving",
                        "candidate_count": 0,
                        "duplicate_filtered_count": 0,
                        "search_windows": [self._window("expert-prefetch", raw=12, unseen=5)],
                    },
                }

                self.assertTrue(queue_worker.record_discovery_stats(sub, accepted_count=0))
                state = json.loads(queue_worker.DISCOVERY_STATE.read_text(encoding="utf-8"))
                self.assertEqual(len(state["search_windows"]), 1)
                row = next(iter(state["search_windows"].values()))
                self.assertEqual(row["topic"], "expert-prefetch")
                self.assertEqual(row["raw_result_count"], 12)
                self.assertEqual(row["unseen_result_count"], 5)
                self.assertAlmostEqual(row["unseen_rate"], 5 / 12)
        finally:
            queue_worker.DISCOVERY_STATE = original_state


if __name__ == "__main__":
    unittest.main()
