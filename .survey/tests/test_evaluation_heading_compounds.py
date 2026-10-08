from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import audit_paper_quality as quality


class EvaluationHeadingTests(unittest.TestCase):
    def test_compound_evaluation_titles(self) -> None:
        paragraph = "同じ推論条件で処理速度と品質を比較した。" * 35
        for heading in ("評価条件と結果", "評価結果と解釈", "実験結果", "性能比較"):
            with self.subTest(heading=heading):
                text = "# Example\n\n## " + heading + "\n" + paragraph
                result = quality._quality_metrics(text)
                self.assertGreaterEqual(result["evaluation_chars"], 500)

    def test_limitation_is_not_evaluation(self) -> None:
        paragraph = "検証できない条件と今後の課題。" * 40
        result = quality._quality_metrics("# Example\n\n## 評価上の制約\n" + paragraph)
        self.assertEqual(result["evaluation_chars"], 0)
        self.assertGreater(result["limitation_chars"], 500)


if __name__ == "__main__":
    unittest.main()
