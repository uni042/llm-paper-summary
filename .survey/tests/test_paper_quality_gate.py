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


if __name__ == "__main__":
    unittest.main()
