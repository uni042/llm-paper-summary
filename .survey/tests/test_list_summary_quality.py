from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "list_summary.py"


class ListSummaryAuditTests(unittest.TestCase):
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
        self.assertFalse(any("日本語比率" in x for x in result.failures))

    def test_quality_rejects_bare_english_term(self) -> None:
        mod = self._module()
        text = "本研究はrequest処理の待ち時間を減らすため、要求順序を変更してGPU利用率を高める方式を提案し、複数条件で効果を評価する。"
        result = mod.audit_list_summary(text)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("英語専門語" in x for x in result.failures))

    def test_quality_accepts_clean_single_line_summary(self) -> None:
        mod = self._module()
        text = "本研究は要求処理の待ち時間を減らすため、要求順序とキャッシュ配置を動的に調整し、GPU利用率を高める方式を提案する。"
        result = mod.audit_list_summary(text)
        self.assertNotEqual(result.status, "FAIL")
        self.assertFalse(result.failures)


if __name__ == "__main__":
    unittest.main()
