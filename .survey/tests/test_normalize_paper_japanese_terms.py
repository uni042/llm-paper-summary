import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "normalize_paper_japanese_terms.py"
spec = importlib.util.spec_from_file_location("normalize_paper_japanese_terms", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


class JapaneseTerminologyNormalizerTests(unittest.TestCase):
    def test_replaces_lowercase_generic_terms_but_preserves_named_systems_and_urls(self):
        text = (
            "prefill memory bandwidthを削減し、Expert Pipeline Schedulerを使う。"
            " https://example.com/memory \x60prefill memory\x60"
        )
        value = mod.replace_generic_terms(text)
        self.assertIn("プリフィル メモリ 帯域", value)
        self.assertIn("Expert Pipeline Scheduler", value)
        self.assertIn("https://example.com/memory", value)
        self.assertIn("\x60prefill memory\x60", value)

    def test_only_repairs_paper_body_when_japanese_ratio_is_current_failure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "papers/inference/x/paper.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                """---
canonical_id: arXiv:2601.00001
title: Example
summary: 日本語の概要。
list_summary: memory bandwidth token expert pipeline model compute serving throughput latencyを改善する方式。
source: https://arxiv.org/abs/2601.00001
---
# Example

memory bandwidth token expert pipeline model compute serving throughput latency
memory bandwidth token expert pipeline model compute serving throughput latency
日本語の説明を組み合わせて処理する。
""",
                encoding="utf-8",
            )
            before = mod.audit_paper_quality.audit_file(path, root)
            self.assertEqual(before.status, "FAIL")
            changed, list_changed = mod.normalize_file(path, root, True)
            after = mod.audit_paper_quality.audit_file(path, root)
            self.assertTrue(changed)
            self.assertTrue(list_changed)
            self.assertGreater(after.japanese_ratio, before.japanese_ratio)


if __name__ == "__main__":
    unittest.main()
