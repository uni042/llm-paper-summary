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
POLICY = {"enabled": True, "mode": "quarantine", "audit_stride": 3, "max_audit_per_build": 2}


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
        self.assertEqual(stats["audit_count"], 2)
        self.assertEqual(len(selected), 12)
        self.assertEqual(sum(bool(x.get("prefilter_audit")) for x in selected), 2)
        self.assertEqual(json.dumps(rows, sort_keys=True), original)
        restored, _ = mod.triage_worklist(rows, {"enabled": False, "mode": "off"})
        self.assertEqual(restored, rows)
        self.assertEqual(mod.triage_worklist(rows, POLICY)[0], selected)

    def test_shadow_preserves_order(self):
        rows = [{"title": "Tomato phenotyping", "canonical_id": "x"}]
        selected, stats = mod.triage_worklist(rows, {**POLICY, "mode": "shadow"})
        self.assertEqual(selected, rows)
        self.assertEqual(stats["quarantine_count"], 1)

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
