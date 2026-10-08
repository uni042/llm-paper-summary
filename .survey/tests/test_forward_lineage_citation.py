"""Mechanical-first citation percentile and forward-source lineage tests."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import forward_lineage_citation as graph
import discovery_relevance_prefilter as filter_rules


class ForwardLineageCitationTests(unittest.TestCase):
    def setUp(self):
        self.papers = [
            SimpleNamespace(
                path=f"papers/inference/01-offload/seed-{i}.md",
                canonical_id=f"arXiv:2501.{i:05d}",
                identifiers=(f"arXiv:2501.{i:05d}", f"DOI:10.10/{i}"),
            ) for i in range(1, 5)
        ] + [
            SimpleNamespace(
                path="papers/training/02-parallel/seed-other.md",
                canonical_id="arXiv:2401.10000",
                identifiers=("arXiv:2401.10000",),
            )
        ]
        self.ids, self.paths = graph.seed_indexes(self.papers)

    def test_distinct_same_folder_forward_seeds(self):
        row = {
            "forward_seed_ids": ["arXiv:2501.00001", "DOI:10.10/2", "arXiv:2501.00003", "arXiv:2401.10000"],
        }
        counts = graph.forward_lineage_counts(
            row, self.ids, self.paths, source_kind="forward_citation_candidate",
        )
        self.assertEqual(counts["inference/01-offload"], 3)
        self.assertEqual(counts["training/02-parallel"], 1)

    def test_backward_edge_does_not_claim_forward_citations(self):
        backward = {"linked_from": [p.path for p in self.papers]}
        counts = graph.forward_lineage_counts(
            backward, self.ids, self.paths, source_kind="reference_review_candidate",
        )
        self.assertEqual(counts, {})

    def test_old_forward_records_can_use_forward_paths(self):
        counts = graph.forward_lineage_counts(
            {"linked_from": [self.papers[0].path, self.papers[1].path]},
            self.ids, self.paths, source_kind="forward_citation_candidate",
        )
        self.assertEqual(counts["inference/01-offload"], 2)

    def test_forward_citation_count_beats_topic_and_global_citations(self):
        rows = [
            {"canonical_id": f"other-{i}", "title": "GPU KV Cache LLM Inference", "priority": 9999, "citation_count": 20000}
            for i in range(99)
        ]
        rows.append({
            "canonical_id": "supported",
            "title": "A New Systems Method",
            "forward_lineage_citation_max": 3,
            "forward_lineage_citation_total": 3,
        })
        policy = {
            "enabled": True, "mode": "quarantine", "max_audit_per_build": 0,
            "relevance_quota": {
                "enabled": True, "mode": "quarantine", "retain_percent": 1,
                "min_candidates": 0,
            },
        }
        selected, stats = filter_rules.triage_worklist(rows, policy)
        self.assertEqual([row["canonical_id"] for row in selected], ["supported"])
        self.assertEqual(stats["quota_eligible_count"], 100)
        self.assertEqual(stats["quota_target_count"], 1)
        self.assertEqual(stats["forward_lineage_3plus_count"], 1)

    def test_mechanical_rules_first_fractional_percentage(self):
        base = [{"canonical_id": f"p{i}", "title": f"Neutral Method {i}"} for i in range(100)]
        discarded = [{"canonical_id": f"t{i}", "title": f"Tomato phenotyping in crops {i}"} for i in range(20)]
        policy = {
            "enabled": True, "mode": "quarantine", "max_audit_per_build": 0,
            "relevance_quota": {
                "enabled": True, "mode": "quarantine", "retain_percent": 2.5,
                "min_candidates": 0,
            },
        }
        selected, metrics = filter_rules.triage_worklist(base + discarded, policy)
        self.assertEqual(metrics["rule_quarantine_count"], 20)
        self.assertEqual(metrics["quota_eligible_count"], 100)
        self.assertEqual(metrics["quota_target_count"], 3)
        self.assertEqual(len(selected), 3)

    def test_forward_edges_survive_backward_first_alias_dedup(self):
        from unittest.mock import patch
        import build_worker_worklist as wl
        import reference_pool
        import forward_citation_state
        import citation_graph
        import candidate_priority

        candidate_id = "arXiv:2601.12345"
        backward = {
            "canonical_id": candidate_id, "title": "Mixed source systems",
            "identity_tokens": [candidate_id], "relation_count": 1,
            "linked_from": [self.papers[0].path],
        }
        forward = {
            "canonical_id": candidate_id, "title": "Mixed source systems",
            "forward_seed_ids": [p.canonical_id for p in self.papers[:3]],
            "linked_from": [p.path for p in self.papers[:3]],
        }

        def score(row, **_):
            return {**row, "priority": 100 if "relation_count" in row else 1}

        with patch.object(reference_pool, "build_reference_pool",
                          return_value={"candidates": [backward]}), \\
             patch.object(forward_citation_state, "load",
                          return_value={"candidates": {candidate_id: forward}}), \\
             patch.object(citation_graph, "load_records", return_value=self.papers), \\
             patch.object(reference_pool, "_load_ledger_tokens", return_value=set()), \\
             patch.object(candidate_priority, "load_cache", return_value={}), \\
             patch.object(candidate_priority, "load_config", return_value={}), \\
             patch.object(wl, "_score_row", side_effect=score):
            found, total = wl._discovery_candidates(Path("/unused"))
        self.assertEqual(total, 1)
        self.assertEqual(found[0]["source_kind"], "reference_review_candidate")
        self.assertEqual(found[0]["forward_lineage_citation_max"], 3)
        self.assertEqual(found[0]["forward_lineage_citation_total"], 3)

    def test_percentage_limit_includes_audit_without_shrinking_shortlist(self):
        rows = [{"canonical_id": f"n{i}", "title": f"Baseline Technical Method {i}"} for i in range(100)]
        policy = {
            "enabled": True, "mode": "quarantine",
            "audit_stride": 50, "max_audit_per_build": 30,
            "relevance_quota": {"enabled": True, "mode": "quarantine",
                                "retain_percent": 5, "min_candidates": 0},
        }
        selected, stats = filter_rules.triage_worklist(rows, policy)
        self.assertEqual(len(selected), 5)
        self.assertEqual(stats["audit_count"], 1)
        self.assertEqual(stats["quota_target_count"], 5)
        self.assertEqual(stats["reviewable_count"], 5)

    def test_turn_off_returns_exact_source_order(self):
        rows = [
            {"canonical_id": "z", "title": "GPU KV Cache Inference", "forward_lineage_citation_max": 4},
            {"canonical_id": "a", "title": "Tomato phenotyping"},
        ]
        output, stats = filter_rules.triage_worklist(rows, {"enabled": False, "mode": "off"})
        self.assertEqual(output, rows)
        self.assertEqual(stats["quarantine_count"], 0)


if __name__ == "__main__":
    unittest.main()
