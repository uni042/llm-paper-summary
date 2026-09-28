#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import paper_quality_gate as gate  # noqa: E402


class PaperQualityGateTests(unittest.TestCase):
    def test_rejects_short_candidate_without_writing_target(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".survey").mkdir()
            target = root / "papers/inference/example.md"
            with self.assertRaisesRegex(ValueError, "paper quality gate failed"):
                gate.validate_rendered_paper(root, "papers/inference/example.md", "# 短い要約\n")
            self.assertFalse(target.exists())
            self.assertFalse((root / ".survey/.quality-gate-tmp").exists())

    def test_uses_same_default_thresholds_as_maintenance_audit(self) -> None:
        args = gate._default_args()
        self.assertEqual(args.min_bytes, gate.quality.DEFAULT_MIN_BYTES)
        self.assertEqual(args.min_prose_chars, gate.quality.DEFAULT_MIN_PROSE_CHARS)
        self.assertEqual(args.min_paragraphs, gate.quality.DEFAULT_MIN_PARAGRAPHS)
        self.assertEqual(args.min_method_paragraphs, gate.quality.DEFAULT_MIN_METHOD_PARAGRAPHS)
        self.assertEqual(args.min_component_paragraphs, gate.quality.DEFAULT_MIN_COMPONENT_PARAGRAPHS)
        self.assertEqual(args.min_japanese_ratio, gate.quality.DEFAULT_MIN_JAPANESE_RATIO)
        self.assertEqual(args.warn_japanese_ratio, gate.quality.DEFAULT_WARN_JAPANESE_RATIO)


    def test_rejects_reused_long_prose_across_papers(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".survey").mkdir()
            existing = root / "papers/inference/old.md"
            existing.parent.mkdir(parents=True, exist_ok=True)
            shared1 = (
                "この段落は品質ゲートの検証用であり、複数の論文にそのまま再利用された長文定型文を模擬する。"
                "論文固有の機構や評価条件ではなく、一般的な説明だけを十分な長さまで繰り返しているため、"
                "別の論文へ貼り付けても成立してしまう。こうした文章が複数段落にわたって共有される場合、"
                "完成したResearch本文としては扱わず、一次資料に基づく固有説明へ書き直す必要がある。"
            )
            shared2 = (
                "もう一つの共有段落も、方式名や変数名、処理順、対象ハードウェア、比較条件といった固有情報を持たない。"
                "このような一般論が長いまま複数の論文で一致すると、見かけの説明量だけが増え、実際の読解結果を反映しない。"
                "そこで品質ゲートは見出しや表ではなく散文段落を比較し、十分に長い一致が複数ある場合だけ明確な失敗として扱う。"
                "短い定型句や書誌情報だけでは失敗にしない。"
            )
            existing.write_text(f"# 既存論文\n\n{shared1}\n\n{shared2}\n", encoding="utf-8")
            candidate = (
                "# 候補論文\n\n"
                + shared1
                + "\n\n"
                + shared2
                + "\n\n"
                + "候補固有の説明として、入力から出力までの処理と評価条件を別途詳しく記述する。"
            )
            result = gate.inspect_rendered_paper(
                root,
                "papers/inference/candidate.md",
                candidate,
            )
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("長文定型文の再利用を検出" in item for item in result.failures))


    def test_rejects_reused_long_prose_across_papers(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            existing = root / "papers/inference/existing.md"
            existing.parent.mkdir(parents=True)
            repeated_a = "これは論文固有でない長い定型段落です。" * 20
            repeated_b = "評価条件や主要結果の説明も別論文へそのまま貼れる定型文です。" * 20
            existing.write_text(
                "# 既存論文\n\n" + repeated_a + "\n\n" + repeated_b + "\n",
                encoding="utf-8",
            )
            candidate = (
                "# 候補論文\n\n"
                + repeated_a
                + "\n\n"
                + repeated_b
                + "\n\n"
                + ("この論文だけの固有説明です。" * 20)
                + "\n"
            )
            result = gate.inspect_rendered_paper(
                root,
                "papers/inference/candidate.md",
                candidate,
            )
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("長文定型文の再利用を検出" in x for x in result.failures))

    def test_ignores_shared_headings_tables_and_short_phrases(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            existing = root / "papers/inference/existing.md"
            existing.parent.mkdir(parents=True)
            existing.write_text(
                "# 既存論文\n\n## 評価\n\n| 項目 | 値 |\n|---|---|\n| GPU | A100 |\n\n"
                + ("既存論文だけの固有説明です。" * 20)
                + "\n",
                encoding="utf-8",
            )
            candidate = (
                "# 候補論文\n\n## 評価\n\n| 項目 | 値 |\n|---|---|\n| GPU | H100 |\n\n"
                + ("候補論文だけの別の固有説明です。" * 20)
                + "\n"
            )
            result = gate.inspect_rendered_paper(
                root,
                "papers/inference/candidate.md",
                candidate,
            )
            self.assertFalse(any("長文定型文の再利用を検出" in x for x in result.failures))


if __name__ == "__main__":
    unittest.main()
