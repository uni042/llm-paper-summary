from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "audit_overview_results.py"


class OverviewResultQualityTests(unittest.TestCase):
    def _module(self):
        self.assertTrue(MODULE_PATH.exists(), "audit_overview_results.py must exist")
        spec = importlib.util.spec_from_file_location("audit_overview_results", MODULE_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def test_accepts_quantitative_representative_result(self):
        mod = self._module()
        overview = (
            "本研究はKVキャッシュの再利用時刻を予測して保持期限を動的に決める。"
            "評価では既存方式に比べて平均処理時間を32%短縮し、同じGPUメモリ容量で再計算を減らした。"
        )
        result = mod.audit_overview_text(overview)
        self.assertEqual(result.status, "PASS")
        self.assertTrue(result.has_result_signal)
        self.assertTrue(result.has_quantitative_signal)

    def test_accepts_explicit_qualitative_result_when_numbers_are_not_natural(self):
        mod = self._module()
        overview = (
            "本研究は複数の推論基盤を統一条件で比較する。"
            "代表結果として、長文脈では計算量よりKVキャッシュ転送が支配的になり、"
            "負荷によって最適な配置戦略が逆転することを示した。"
        )
        result = mod.audit_overview_text(overview)
        self.assertEqual(result.status, "PASS")
        self.assertTrue(result.has_result_signal)

    def test_rejects_overview_that_only_describes_problem_and_method(self):
        mod = self._module()
        overview = (
            "本研究はGPUメモリ不足を扱う。必要な重みをCPUから先読みし、"
            "実行順序に合わせてキャッシュへ配置する方式を提案する。"
        )
        result = mod.audit_overview_text(overview)
        self.assertEqual(result.status, "FAIL")
        self.assertFalse(result.has_result_signal)

    def test_extracts_only_overview_section(self):
        mod = self._module()
        body = """# Example

## 概要

GPUメモリ不足を扱い、必要な重みだけを先読みする方式を提案する。

## 評価

既存方式より2.1倍高速だった。
"""
        overview = mod.extract_overview(body)
        self.assertNotIn("2.1倍", overview)
        result = mod.audit_overview_text(overview)
        self.assertEqual(result.status, "FAIL")


if __name__ == "__main__":
    unittest.main()
