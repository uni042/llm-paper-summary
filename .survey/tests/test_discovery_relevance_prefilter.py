"""Conservative Discovery relevance prefilter regression tests."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "discovery_relevance_prefilter.py"
spec = importlib.util.spec_from_file_location("discovery_relevance_prefilter", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)
POLICY = {"enabled": True, "mode": "quarantine"}


class RelevancePrefilterTests(unittest.TestCase):
    def test_agricultural_application_quarantined(self):
        self.assertEqual(mod.classify({"title": "Embedding of ripening topology into one-stage detection for tomato cluster phenotyping"}, POLICY)["verdict"], "quarantine")

    def test_chemistry_application_quarantined(self):
        self.assertEqual(mod.classify({"title": "Collective intelligence for AI-assisted chemical synthesis", "abstract": "Uses LLMs for chemistry"}, POLICY)["verdict"], "quarantine")

    def test_systems_mechanism_rescues_cross_domain(self):
        row = {"title": "GPU KV Cache Offloading for Low-Latency Medical Image LLM Serving", "abstract": "Accelerates inference serving"}
        self.assertEqual(mod.classify(row, POLICY)["verdict"], "review")
        self.assertEqual(mod.classify(row, POLICY)["reason"], "system_mechanism_rescue")

    def test_generic_methods_and_unknown_title_kept(self):
        for title in ("FlashAttention: Fast and Memory-Efficient Exact Attention", "Megatron-LM: Training Multi-Billion Parameter Language Models", "", "New Memory-Efficient Model Architecture"):
            self.assertEqual(mod.classify({"title": title}, POLICY)["verdict"], "review")

    def test_allowlist_rescues(self):
        row = {"title": "Tomato Cluster Phenotyping", "canonical_id": "x"}
        self.assertEqual(mod.classify(row, {**POLICY, "allow_canonical_ids": ["x"]})["verdict"], "review")

    def test_pool_unmodified_and_reversible(self):
        rows = [{"title": "FlashAttention", "canonical_id": f"a{i}"} for i in range(10)]
        rows += [{"title": "Tomato phenotyping", "canonical_id": f"x{i}"} for i in range(6)]
        original = json.dumps(rows, sort_keys=True)
        selected, stats = mod.triage_worklist(rows, POLICY)
        self.assertEqual(stats["quarantine_count"], 6)
        self.assertNotIn("audit_count", stats)
        self.assertEqual(len(selected), 10)
        self.assertFalse(any(x.get("prefilter_audit") for x in selected))
        self.assertEqual(json.dumps(rows, sort_keys=True), original)
        restored, _ = mod.triage_worklist(rows, {"enabled": False, "mode": "off"})
        self.assertEqual(restored, rows)
        self.assertEqual(mod.triage_worklist(rows, POLICY)[0], selected)

    def test_shadow_preserves_order(self):
        rows = [{"title": "Tomato phenotyping", "canonical_id": "x"}]
        selected, stats = mod.triage_worklist(rows, {**POLICY, "mode": "shadow"})
        self.assertEqual(selected, rows)
        self.assertEqual(stats["quarantine_count"], 1)


    def test_expanded_rules_shadow_does_not_remove_candidates(self):
        extended = {**POLICY, "expanded_rules": {"enabled": True, "mode": "shadow"}}
        rows = [
            {"title": "Stock Price Prediction with Machine Learning", "canonical_id": "market"},
            {"title": "FlashAttention: Faster GPU Memory-Efficient Inference", "canonical_id": "flash"},
            {"title": "Low-Latency GPU Offloading for Clinical Decision Support", "canonical_id": "medical"},
        ]
        chosen, stats = mod.triage_worklist(rows, extended)
        self.assertEqual(chosen, rows)
        self.assertEqual(stats["expanded_rule_shadow_count"], 1)
        self.assertEqual(stats["expanded_rule_applied_count"], 0)
        self.assertEqual(stats["expanded_rule_reason_counts"]["expanded_domain:financial_applications"], 1)

    def test_expanded_rules_reversible(self):
        rows = [{"title": "Weather Forecasting with Neural Networks", "canonical_id": "climate"}]
        extended = {**POLICY, "max_audit_per_build": 0, "expanded_rules": {"enabled": True, "mode": "quarantine"}}
        chosen, stats = mod.triage_worklist(rows, extended)
        self.assertEqual(chosen, [])
        self.assertEqual(stats["expanded_rule_applied_count"], 1)
        restored, _ = mod.triage_worklist(rows, {**extended, "expanded_rules": {"enabled": True, "mode": "shadow"}})
        self.assertEqual(restored, rows)

    def test_cross_domain_systems_evidence_rescued(self):
        extended = {**POLICY, "expanded_rules": {"enabled": True, "mode": "shadow"}}
        for title in (
            "KV-Cache Offloading for Video Summarization at Scale",
            "Distributed Training of GPU Models for Traffic Flow Prediction",
            "Optimizing LLM Inference Latency for Autonomous Driving",
        ):
            self.assertEqual(mod.classify_expansion({"title": title}, extended)["verdict"], "review")

    def test_expanded_rules_do_not_quarantine_published_title_corpus(self):
        import sys
        scripts = Path(__file__).resolve().parents[1] / "scripts"
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        import citation_graph
        root = Path(__file__).resolve().parents[2]
        papers = citation_graph.load_records(root)
        if not papers:
            self.skipTest("no published papers in fixture")
        extended = {**POLICY, "expanded_rules": {"enabled": True, "mode": "shadow"}}
        flagged = [
            (p.canonical_id, p.meta.get("title")) for p in papers
            if mod.classify_expansion({"title": p.meta.get("title")}, extended)["verdict"] == "quarantine"
        ]
        self.assertEqual(flagged, [], f"false-positive examples in collected papers: {flagged[:12]}")


    def test_expanded_active_stats_and_audit_are_coherent(self):
        sample = [
            {"canonical_id": "v1", "title": "Crop phenotyping with transformers"},
            {"canonical_id": "v2", "title": "Object Detection for Retail Products"},
            {"canonical_id": "v3", "title": "GPU KV-Cache Offloading for Image Classification"},
            {"canonical_id": "v4", "title": "Scheduling of GPU Kernels for Transformers"},
        ]
        p = {**POLICY, "max_audit_per_build": 0, "expanded_rules": {"enabled": True, "mode": "quarantine"}}
        selected, stats = mod.triage_worklist(sample, p)
        self.assertEqual(stats["rule_quarantine_count"], 1)
        self.assertEqual(stats["expanded_rule_applied_count"], 1)
        self.assertEqual(stats["quarantine_count"], 2)
        self.assertEqual(stats["reviewable_count"], 2)
        self.assertEqual(len(selected), 2)
        self.assertEqual([r["canonical_id"] for r in selected], ["v3", "v4"])
        resumed, prior_stats = mod.triage_worklist(sample, {**p, "expanded_rules": {"enabled": True, "mode": "shadow"}})
        self.assertEqual(prior_stats["expanded_rule_applied_count"], 0)
        self.assertEqual(prior_stats["expanded_rule_shadow_count"], 1)
        self.assertEqual(len(resumed), 3)


    def test_quartile_reduces_pool_and_prioritizes_systems(self):
        relevant = [
            {"canonical_id": f"sys-{i}", "title": f"GPU KV-Cache Offloading for LLM Inference Method {i}", "priority": 100}
            for i in range(9)
        ]
        unrelated = [
            {"canonical_id": f"other-{i}", "title": f"Applications of Text Statistics in Retail Study {i}", "priority": 1000}
            for i in range(31)
        ]
        rows = unrelated + relevant
        q = {**POLICY, "max_audit_per_build": 0, "relevance_quota": {"enabled": True, "mode": "quarantine", "retain_percent": 25, "min_candidates": 0}}
        before = json.dumps(rows, ensure_ascii=False, sort_keys=True)
        chosen, metrics = mod.triage_worklist(rows, q)
        self.assertEqual(metrics["unfiltered_count"], 40)
        self.assertEqual(metrics["quota_target_count"], 10)
        self.assertEqual(metrics["quota_quarantine_count"], 30)
        self.assertEqual(metrics["reviewable_count"], 10)
        self.assertEqual(len(chosen), 10)
        self.assertEqual(sum(str(r["canonical_id"]).startswith("sys-") for r in chosen), 9)
        self.assertEqual(json.dumps(rows, ensure_ascii=False, sort_keys=True), before)
        disabled, old_stats = mod.triage_worklist(rows, {**q, "relevance_quota": {"enabled": False}})
        self.assertEqual(disabled, rows)
        self.assertEqual(old_stats["quota_quarantine_count"], 0)

    def test_quartile_respects_allowlist(self):
        rows = [{"canonical_id": f"id-{i}", "title": f"Unrelated Article Number {i}"} for i in range(40)]
        q = {
            **POLICY, "max_audit_per_build": 0,
            "allow_canonical_ids": ["id-17"],
            "relevance_quota": {"enabled": True, "mode": "quarantine", "retain_percent": 25, "min_candidates": 0},
        }
        chosen, metrics = mod.triage_worklist(rows, q)
        self.assertEqual(len(chosen), 10)
        self.assertIn("id-17", {row["canonical_id"] for row in chosen})
        self.assertEqual(metrics["quota_quarantine_count"], 30)

    def test_quartile_shadow_and_active_states_differ(self):
        rows = [{"canonical_id": f"id-{i}", "title": f"Generic Article Number {i}"} for i in range(40)]
        q = {**POLICY, "max_audit_per_build": 0, "relevance_quota": {"enabled": True, "mode": "shadow", "retain_percent": 25, "min_candidates": 0}}
        selected, stats = mod.triage_worklist(rows, q)
        self.assertEqual(selected, rows)
        self.assertEqual(stats["quota_quarantine_count"], 0)
        self.assertEqual(stats["quota_target_count"], 10)

    def test_quartile_never_reinjects_deferred_even_with_legacy_audit_keys(self):
        rows = [
            {"canonical_id": f"id-{i}", "title": f"Generic Paper Number {i}", "priority": i}
            for i in range(100)
        ]
        q = {**POLICY, "audit_stride": 3, "max_audit_per_build": 5,
             "relevance_quota": {"enabled": True, "mode": "quarantine",
                                 "retain_percent": 25, "min_candidates": 0}}
        selected, stats = mod.triage_worklist(rows, q)
        self.assertEqual(len(selected), 25)
        self.assertEqual(stats["quota_quarantine_count"], 75)
        self.assertNotIn("audit_count", stats)
        self.assertFalse(any(x.get("prefilter_audit") for x in selected))
        self.assertEqual([r["priority"] for r in selected], list(range(99, 74, -1)))

    def test_missing_config_fail_open(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self.assertFalse(mod.load_policy(root)["enabled"])
            path = root / mod.CONFIG_PATH
            path.parent.mkdir(parents=True)
            path.write_text("garbage", encoding="utf-8")
            self.assertFalse(mod.load_policy(root)["enabled"])


if __name__ == "__main__":
    unittest.main()
