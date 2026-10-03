from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import candidate_priority  # noqa: E402


class CandidatePriorityTest(unittest.TestCase):
    def policy(self):
        return {
            "schema_version": 1,
            "policy_name": "test",
            "freshness": {
                "enabled": True,
                "max_age_days": 120,
                "score": 100,
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

    def test_weights_are_configuration_driven(self):
        policy = self.policy()
        policy["freshness"]["score"] = 7
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
