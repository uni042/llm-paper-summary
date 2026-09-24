from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
MODULE_PATH = SCRIPTS / "list_summary.py"


class ListSummaryTests(unittest.TestCase):
    def _module(self):
        self.assertTrue(MODULE_PATH.exists(), "list_summary.py must exist")
        spec = importlib.util.spec_from_file_location("list_summary", MODULE_PATH)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def test_compacts_lead_overview_and_normalizes_japanese_terms(self):
        mod = self._module()
        body = """# Example

> 本研究はrequestごとにtoken列を処理する際、cache転送がlatencyのボトルネックになる問題を扱う。複数GPUへcacheをdynamicに配置し、必要なtokenだけをprefetchして転送待ちを減らす。さらに長い説明が続き、一覧には不要な評価条件や補足事項を詳しく説明する。

## 書誌情報
"""
        text = mod.compact_list_summary(body, "fallback summary")
        self.assertGreaterEqual(len(text), 45)
        self.assertLessEqual(len(text), 180)
        self.assertNotIn("\n", text)
        self.assertNotRegex(text, r"\b(?:request|token|cache|latency|dynamic|prefetch)\b")
        self.assertIn("リクエスト", text)
        self.assertIn("トークン", text)

    def test_worker_authored_lead_beats_overview_fallback(self):
        mod = self._module()
        worker = "本研究はKVキャッシュの次回利用時刻を予測して保持期限を動的に決め、再計算とGPUメモリ占有を同時に抑える方式を提案する。"
        body = f"""# Example

> {worker}

## 概要

長い背景説明が続く。ここは単体ページ向けの詳しい概要であり、一覧用の一文を自動生成する材料としては使わない。
"""
        text = mod.compact_list_summary(body)
        self.assertEqual(text, worker)
        self.assertNotIn("長い背景説明", text)

    def test_preserves_worker_lead_sentences_within_limit(self):
        mod = self._module()
        first = "本研究は複数の要求が同時に到着する推論環境で、待ち時間とGPU利用率を同時に改善するため、要求順序とキャッシュ配置を動的に調整する方式を提案する。"
        second = "次に評価条件や補足事項も短く説明する。"
        body = f"# Example\n\n> {first}{second}\n"
        text = mod.compact_list_summary(body)
        self.assertTrue(text.startswith(first))
        self.assertIn("評価条件", text)
        self.assertLessEqual(len(text), 180)

    def test_background_only_first_sentence_does_not_hide_method(self):
        mod = self._module()
        background = "長いエージェント処理では再利用できるKVキャッシュが増え続け、限られたGPUメモリでは保持対象を適切に選ばないと再計算と待ち時間が増える。"
        method = "提案手法は各キャッシュの次回利用時刻を予測し、再利用までの時間に応じて保持期限を動的に決めることで、不要な保持と早すぎる追い出しを減らす。"
        result = "評価では既存方式よりキャッシュ再利用率と処理性能を改善した。"
        body = f"# Example\n\n## 概要\n\n{background}{method}{result}\n"
        text = mod.compact_list_summary(body)
        self.assertLessEqual(len(text), 180)
        self.assertIn("予測", text)
        self.assertIn("保持期限", text)
        self.assertTrue("KVキャッシュ" in text or "キャッシュ" in text)

    def test_explicit_overview_section_beats_metadata_fallback(self):
        mod = self._module()
        body = """# Example

## 概要

本研究はGPUメモリ不足に対し、必要な重みだけを先読みして転送量を減らす方式を提案する。複数の実機条件で待ち時間を減らし、限られたメモリでも処理を継続できるようにする。

## 手法
本文。
"""
        text = mod.compact_list_summary(body, "メタデータ側の古い説明だけを使ってはいけない。")
        self.assertIn("GPUメモリ不足", text)
        self.assertNotIn("メタデータ側", text)

    def test_protects_method_names_while_translating_generic_terms(self):
        mod = self._module()
        body = """# Example

> EVICTとLayerSkipはdraft modelを使ったspeculative decodingのverification costを減らし、target modelのlatencyを抑える手法である。複数条件で既存方式より待ち時間を短縮する。
"""
        text = mod.compact_list_summary(body)
        self.assertIn("EVICT", text)
        self.assertIn("LayerSkip", text)
        self.assertNotIn("層kip", text)
        self.assertIn("下書きモデル", text)
        self.assertIn("投機的復号", text)
        self.assertIn("検証コスト", text)
        self.assertIn("対象モデル", text)
        self.assertNotIn("latency", text.lower())

    def test_quality_ignores_proper_names_in_language_ratio(self):
        mod = self._module()
        text = "AgentSysBenchはDeepResearch、HuggingGPT、WebAgent、GUIAgent、Claude Codeを含むエージェント処理を比較し、システム性能の差を測るベンチマークである。"
        result = mod.audit_list_summary(text)
        self.assertNotEqual(result.status, "FAIL")
        self.assertFalse(any("日本語比率" in x for x in result.failures))

    def test_quality_rejects_bare_english_term(self):
        mod = self._module()
        text = "本研究はrequest処理の待ち時間を減らすため、要求順序を変更してGPU利用率を高める方式を提案し、複数条件で効果を評価する。"
        result = mod.audit_list_summary(text)
        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("英語専門語" in x for x in result.failures))

    def test_quality_accepts_clean_single_line_summary(self):
        mod = self._module()
        text = "本研究は要求処理の待ち時間を減らすため、要求順序とキャッシュ配置を動的に調整し、GPU利用率を高める方式を提案する。"
        result = mod.audit_list_summary(text)
        self.assertNotEqual(result.status, "FAIL")
        self.assertFalse(result.failures)


if __name__ == "__main__":
    unittest.main()
