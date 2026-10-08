#!/usr/bin/env python3
from __future__ import annotations

import hashlib
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
        self.assertTrue(args.enforce_explanation_floor)


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

    def _research_markdown(
        self,
        *,
        method_repeats: int = 140,
        evaluation_repeats: int = 110,
        self_review: str | None = None,
    ) -> str:
        attestation = ""
        if self_review is not None:
            attestation = (
                'quality_self_review_version: "2026-10-07-v1"\n'
                f"quality_self_review_passed: {self_review}\n"
            )
        return (
            "---\n"
            "canonical_id: arXiv:2699.99999\n"
            "title: 品質ゲート検証\n"
            "source: https://arxiv.org/abs/2699.99999\n"
            "summary: 新規Researchの説明不足を防ぐ品質ゲート検証用要約。\n"
            "list_summary: 本研究は具体的な処理と評価条件を説明する検証用論文である。\n"
            + attestation
            + "---\n\n"
            "# 品質ゲート検証\n\n"
            "## 概要\n\n"
            + ("この論文固有の問題設定と既存方式の不足を具体的に説明する。" * 90)
            + "\n\n## 手法\n\n"
            + ("入力を観測し固有の判断規則で処理して出力を更新する。" * method_repeats)
            + "\n\n## 評価\n\n"
            + ("同一条件の比較対象に対して指標を測定し結果の意味を説明する。" * evaluation_repeats)
            + "\n\n## 限界・実装状況\n\n"
            + ("資源不足や分布変化では利得が縮小し追加費用が増える。" * 30)
            + "\n"
        )

    def test_explanation_floor_rejects_short_method_even_when_body_is_long(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".survey").mkdir()
            content = self._research_markdown(method_repeats=15, evaluation_repeats=110)
            result = gate.inspect_rendered_paper(root, "papers/inference/candidate.md", content)
            self.assertEqual(result.status, "FAIL")
            self.assertGreaterEqual(result.prose_chars, gate.quality.QUALITY_MIN_BODY_CHARS)
            self.assertLess(result.method_chars, gate.quality.QUALITY_MIN_METHOD_CHARS)
            self.assertTrue(any("手法説明量" in item for item in result.failures))

    def test_explanation_floor_accepts_sufficient_body_method_and_evaluation(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".survey").mkdir()
            content = self._research_markdown()
            result = gate.inspect_rendered_paper(root, "papers/inference/candidate.md", content)
            self.assertFalse(any("説明不足トリガー" in item for item in result.failures))
            self.assertGreaterEqual(result.prose_chars, gate.quality.QUALITY_MIN_BODY_CHARS)
            self.assertGreaterEqual(result.method_chars, gate.quality.QUALITY_MIN_METHOD_CHARS)
            self.assertGreaterEqual(result.evaluation_chars, gate.quality.QUALITY_MIN_EVALUATION_CHARS)
            self.assertGreaterEqual(result.limitation_chars, gate.quality.QUALITY_WARN_LIMITATION_CHARS)

    def test_present_self_review_attestation_must_be_true(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / ".survey").mkdir()
            content = self._research_markdown(self_review="false")
            result = gate.inspect_rendered_paper(root, "papers/inference/candidate.md", content)
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("quality_self_review_passed" in item for item in result.failures))

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


    def test_reaudit_exempts_only_verified_same_paper_from_reuse(self) -> None:
        """A revision may retain its original paragraphs, but not another paper's."""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            original = root / "papers/inference/verified.md"
            original.parent.mkdir(parents=True, exist_ok=True)
            shared_a = "同一論文の修復前から保持されている固有の設計根拠と処理手順。" * 13
            shared_b = "修復前の表と比較対象を説明する固有の日本語散文を記録する。" * 13
            body = shared_a + "\n\n" + shared_b + "\n"
            original_text = (
                "---\ncanonical_id: arXiv:2503.18893\n"
                "title: 同一論文\nsource: https://arxiv.org/abs/2503.18893\n"
                "summary: 同一論文の解説\nlist_summary: 研究の要点を記録する。\n"
                "---\n\n# 同一論文\n\n" + body
            )
            original.write_text(original_text, encoding="utf-8")
            source_bytes = original.read_bytes()
            blob_sha = hashlib.sha1(
                f"blob {len(source_bytes)}\0".encode("ascii") + source_bytes
            ).hexdigest()
            meta = (
                "---\ncanonical_id: arXiv:2503.18893\n"
                "title: 同一論文\nsource: https://arxiv.org/abs/2503.18893\n"
                "summary: 修正論文\nlist_summary: 修正内容を要約する。\n"
                "under16kb_reaudit_target_path: papers/inference/verified.md\n"
                f"under16kb_reaudit_source_git_blob_sha: '{blob_sha}'\n"
                "---\n\n# 同一論文\n\n"
            )
            pending_path = ".survey/import-inbox/pending/research/revision.md"
            revision = meta + body + "\n\n" + ("修正後の一次資料に基づく新規評価の説明。" * 30)
            self.assertEqual(gate._boilerplate_reuse_failures(root, pending_path, revision), [])

            # A false source blob must not bypass the shared-paragraph check.
            bad_sha = revision.replace(blob_sha, "0" * 40)
            self.assertTrue(
                any("長文定型文の再利用を検出" in item for item in
                    gate._boilerplate_reuse_failures(root, pending_path, bad_sha))
            )

            # A different canonical identity must not bypass the check.
            bad_id = revision.replace(
                "canonical_id: arXiv:2503.18893",
                "canonical_id: arXiv:2503.18894",
            )
            self.assertTrue(
                any("長文定型文の再利用を検出" in item for item in
                    gate._boilerplate_reuse_failures(root, pending_path, bad_id))
            )

            # Even a verified revision still rejects text lifted from another paper.
            another = root / "papers/inference/other.md"
            copied_a = "独立した研究のためだけに書かれた全く異なる説明段落。" * 16
            copied_b = "異なる実験条件を説明する長い別の研究の日本語本文。" * 16
            another.write_text(
                "---\ncanonical_id: arXiv:2401.00001\n---\n"
                + copied_a + "\n\n" + copied_b + "\n",
                encoding="utf-8",
            )
            mixed = revision + "\n\n" + copied_a + "\n\n" + copied_b
            self.assertTrue(
                any("papers/inference/other.md" in item for item in
                    gate._boilerplate_reuse_failures(root, pending_path, mixed))
            )


if __name__ == "__main__":
    unittest.main()
