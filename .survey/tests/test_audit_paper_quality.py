#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_paper_quality.py"
SPEC = importlib.util.spec_from_file_location("audit_paper_quality", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class PaperIntegrityAuditTests(unittest.TestCase):
    def _write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def _valid(self) -> str:
        return """---
canonical_id: arXiv:2601.00001
title: Example
source: https://arxiv.org/abs/2601.00001
summary: 日本語で研究内容を説明する要約である。
list_summary: 本研究は限られたメモリ環境で転送待ちを減らすために配置を調整する方式を提案する。
---

# Example

## 概要

本研究は限られたメモリ環境で発生する転送待ちを減らす方式を扱う。
提案手法は実行状態に応じて配置を調整し、不要な転送を減らす。
"""

    def test_readme_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "README.md", "# Index\n")
            self.assertFalse(AUDIT.is_paper_summary(path))

    def test_moved_stub_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            path = self._write(Path(td), "old.md", "# Moved\n\nSee new path.\n")
            self.assertFalse(AUDIT.is_paper_summary(path))

    def test_valid_publication_integrity_passes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "paper.md", self._valid())
            result = AUDIT.audit_file(path, root)
            self.assertNotEqual(result.status, "FAIL")

    def test_missing_required_frontmatter_key_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "paper.md", self._valid().replace("summary: 日本語で研究内容を説明する要約である。\n", ""))
            result = AUDIT.audit_file(path, root)
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("frontmatter.summary" in x for x in result.failures))

    def test_unbalanced_fence_fails(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = self._write(root, "paper.md", self._valid() + "\n\x60\x60\x60python\nprint('x')\n")
            result = AUDIT.audit_file(path, root)
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("コードフェンス" in x for x in result.failures))

    def test_old_quantity_thresholds_are_retired(self) -> None:
        self.assertEqual(AUDIT.DEFAULT_MIN_BYTES, 0)
        self.assertEqual(AUDIT.DEFAULT_MIN_PROSE_CHARS, 0)
        self.assertEqual(AUDIT.DEFAULT_MIN_PARAGRAPHS, 0)
        self.assertEqual(AUDIT.DEFAULT_MIN_METHOD_PARAGRAPHS, 0)
        self.assertEqual(AUDIT.DEFAULT_MIN_COMPONENT_PARAGRAPHS, 0)

    def test_japanese_ratio_threshold_is_retained(self) -> None:
        self.assertEqual(AUDIT.DEFAULT_MIN_JAPANESE_RATIO, 0.70)
        self.assertEqual(AUDIT.DEFAULT_WARN_JAPANESE_RATIO, 0.80)

    def test_english_heavy_prose_fails_japanese_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            text = self._valid().replace(
                "本研究は限られたメモリ環境で発生する転送待ちを減らす方式を扱う。\n提案手法は実行状態に応じて配置を調整し、不要な転送を減らす。",
                "This method schedules requests dynamically and moves cache between memory tiers while reducing latency and throughput overhead."
            )
            path = self._write(root, "paper.md", text)
            result = AUDIT.audit_file(path, root)
            self.assertEqual(result.status, "FAIL")
            self.assertTrue(any("日本語比率" in x for x in result.failures))


if __name__ == "__main__":
    unittest.main()
