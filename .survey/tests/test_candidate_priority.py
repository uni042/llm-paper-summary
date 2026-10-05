from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import candidate_priority  # noqa: E402
import refresh_candidate_priority  # noqa: E402


class CandidatePriorityTest(unittest.TestCase):
    def policy(self):
        return {
            "schema_version": 1,
            "policy_name": "test",
            "freshness": {
                "enabled": True,
                "window_mode": "rolling_months",
                "months": 12,
                "score": 10,
                "cited_score": 100,
                "year_only_is_fresh": False,
            },
            "prestigious_venue": {
                "enabled": True,
                "score": 10,
                "aliases": ["OSDI", "NeurIPS"],
            },
            "citations": {
                "enabled": True,
                "score_per_citation": 1,
                "max_score": None,
            },
            "fallback_priority": 0,
        }

    def test_fresh_venue_and_citations_are_additive_and_unbounded(self):
        got = candidate_priority.score_record(
            {"published": "2026-09-01", "venue": "OSDI", "citation_count": 140},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=self.policy(),
        )
        self.assertEqual(got["freshness"], 100)
        self.assertEqual(got["prestigious_venue"], 10)
        self.assertEqual(got["citations"], 140)
        self.assertEqual(got["total"], 250)

    def test_recent_cited_gets_attention_equivalent_boost(self):
        cited = candidate_priority.score_record(
            {"published": "2026-09-01", "citation_count": 1},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=self.policy(),
        )
        uncited = candidate_priority.score_record(
            {"published": "2026-09-01", "citation_count": 0},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=self.policy(),
        )
        self.assertTrue(cited["is_recent_cited"])
        self.assertEqual(cited["freshness"], 100)
        self.assertEqual(cited["total"], 101)
        self.assertFalse(uncited["is_recent_cited"])
        self.assertEqual(uncited["freshness"], 10)
        self.assertEqual(uncited["total"], 10)

    def test_recent_window_matches_survey_list_month_buckets(self):
        november = candidate_priority.score_record(
            {"published": "2025-11-01", "citation_count": 0},
            repo_root=Path("."),
            now=dt.date(2026, 10, 31),
            config=self.policy(),
        )
        october = candidate_priority.score_record(
            {"published": "2025-10-31", "citation_count": 0},
            repo_root=Path("."),
            now=dt.date(2026, 10, 1),
            config=self.policy(),
        )
        self.assertTrue(november["is_fresh"])
        self.assertFalse(october["is_fresh"])

    def test_old_highly_cited_paper_can_outrank_fresh_uncited_paper(self):
        old = candidate_priority.score_record(
            {"published": "2020-01-01", "citation_count": 500},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=self.policy(),
        )
        fresh = candidate_priority.score_record(
            {"published": "2026-10-01"},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=self.policy(),
        )
        self.assertGreater(old["total"], fresh["total"])

    def test_year_only_metadata_does_not_claim_freshness(self):
        got = candidate_priority.score_record(
            {"year": 2026, "citation_count": 2},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=self.policy(),
        )
        self.assertFalse(got["is_fresh"])
        self.assertEqual(got["total"], 2)

    def test_embedded_provider_metadata_seeds_priority_cache_without_lookup(self):
        cache = {
            "schema_version": 1,
            "records": {},
            "aliases": {},
            "lookup_failures": {
                "arXiv:2609.00001": {
                    "status": "error",
                    "checked_at": "2026-10-01T00:00:00+00:00",
                }
            },
        }
        rows = [
            {
                "_lookup_id": "arXiv:2609.00001",
                "canonical_id": "arXiv:2609.00001",
                "arxiv_id": "2609.00001",
                "title": "Forward candidate",
                "published": "2026-09-30",
                "venue": "OSDI",
                "citation_count": 17,
                "citation_count_source": "semantic_scholar",
                "last_seen_at": "2026-10-03T17:38:36+00:00",
            }
        ]
        seeded = refresh_candidate_priority._seed_cache_from_embedded_metadata(
            cache, rows
        )
        self.assertEqual(seeded, 1)
        stored = cache["records"]["arXiv:2609.00001"]
        self.assertEqual(stored["citation_count"], 17)
        self.assertEqual(
            stored["citation_count_checked_at"],
            "2026-10-03T17:38:36+00:00",
        )
        self.assertNotIn("arXiv:2609.00001", cache["lookup_failures"])

        self.assertEqual(
            refresh_candidate_priority._seed_cache_from_embedded_metadata(
                cache, rows
            ),
            0,
        )

    def test_weights_are_configuration_driven(self):
        policy = self.policy()
        policy["freshness"]["score"] = 7
        policy["freshness"]["cited_score"] = 7
        policy["prestigious_venue"]["score"] = 3
        policy["citations"]["score_per_citation"] = 2
        got = candidate_priority.score_record(
            {"published": "2026-10-01", "venue": "NeurIPS 2026", "citation_count": 5},
            repo_root=Path("."),
            now=dt.date(2026, 10, 3),
            config=policy,
        )
        self.assertEqual(got["total"], 20)


if __name__ == "__main__":
    unittest.main()
