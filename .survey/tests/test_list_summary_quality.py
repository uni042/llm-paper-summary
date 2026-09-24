from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_list_summary_quality import audit_file  # noqa: E402

MODULE_PATH = SCRIPTS / "list_summary.py"


class ListSummaryQualityTests(unittest.TestCase):
    def _module(self):
        self.assertTrue(MODULE_PATH.exists(), "list_summary.py must exist")
        spec = importlib.util.spec_from_file_location("list_summary", MODULE_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def test_quality_ignores_proper_names_in_language_ratio(self) -> None:
        mod = self._module()
        text = "AgentSysBenchはDeepResearch、HuggingGPT、WebAgent、GUIAgent、Claude Codeを含むエージェント処理を比較し、システム性能の差を測るベンチマークである。"
        result = mod.audit_list_summary(text)
        self.assertNotEqual(result.status, "FAIL")
        self.assertFalse(any("日本語比率" in item for item in result.failures))

    def test_quality_rejects_bare_english_term(self) -> None:
        mod = self._module()
        text = "本研究はrequest処理の待ち時間を減らすため、要求順序を変更してGPU利用率を高める方式を提案し、複数条件で効果を評価する。"
        result = mod.audit_list_summary(text)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("英語専門語" in item for item in result.failures))

    def test_quality_accepts_clean_single_line_summary(self) -> None:
        mod = self._module()
        text = "本研究は要求処理の待ち時間を減らすため、要求順序とキャッシュ配置を動的に調整し、GPU利用率を高める方式を提案する。"
        result = mod.audit_list_summary(text)
        self.assertNotEqual(result.status, "FAIL")
        self.assertFalse(result.failures)

    def test_audit_uses_explicit_frontmatter_value(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers" / "example.md"
            paper.parent.mkdir(parents=True)
            explicit = "本研究は明示された一覧文だけを監査し、本文からの自動生成を行わない方式を採用する方針である。"
            paper.write_text(
                "---\n"
                "title: Example\n"
                "summary: 古いfallback用の説明文は一覧監査で使わない。\n"
                f"list_summary: {explicit}\n"
                "---\n"
                "# Example\n\n"
                "> 本文にある別の文章は監査対象の一覧文ではない。\n\n"
                "## 概要\n\n本文由来のfallbackは禁止する。\n",
                encoding="utf-8",
            )
            result = audit_file(paper, root)

        self.assertEqual(result.summary, explicit)
        self.assertNotEqual(result.status, "FAIL")

    def test_audit_fails_when_explicit_frontmatter_value_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers" / "example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                "---\n"
                "title: Example\n"
                "summary: 本文にない情報を推測せず明示した一覧文を使う。\n"
                "---\n"
                "# Example\n\n"
                "> 本文には十分な長さがあるが、一文要約としては使わない。\n",
                encoding="utf-8",
            )
            result = audit_file(paper, root)

        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("list_summary" in failure for failure in result.failures))


if __name__ == "__main__":
    unittest.main()
