#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "audit_paper_quality.py"
SPEC = importlib.util.spec_from_file_location("audit_paper_quality", SCRIPT)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class PaperTargetDetectionTests(unittest.TestCase):
    def _write(self, root: Path, name: str, text: str) -> Path:
        path = root / name
        path.write_text(text, encoding="utf-8")
        return path

    def test_readme_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(Path(tmp), "README.md", "# Index\n")
            self.assertFalse(AUDIT.is_paper_summary(path))

    def test_plain_moved_stub_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(Path(tmp), "old.md", "# Moved\n\nSee new path.\n")
            self.assertFalse(AUDIT.is_paper_summary(path))

    def test_moved_stub_with_frontmatter_is_excluded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                Path(tmp),
                "old.md",
                "---\ncanonical_id: arXiv:1234.56789\n---\n\n# Moved\n\nSee new path.\n",
            )
            self.assertFalse(AUDIT.is_paper_summary(path))

    def test_real_paper_without_canonical_id_is_still_audited(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                Path(tmp),
                "paper.md",
                "---\ntitle: Example\n---\n\n# Example\n\n## 概要\n\n本文。\n",
            )
            self.assertTrue(AUDIT.is_paper_summary(path))

    def test_real_paper_without_frontmatter_is_still_audited(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(
                Path(tmp),
                "paper.md",
                "# Example\n\n## 概要\n\n本文。\n",
            )
            self.assertTrue(AUDIT.is_paper_summary(path))


class MethodHeadingCompatibilityTests(unittest.TestCase):
    def test_legacy_method_overview_heading_counts_as_method(self) -> None:
        lines = """# Example

## 手法のあらまし

### 1. 第一機構

第一機構では入力を観測して処理対象を決める。ここでは十分な長さの説明文を置く。

決定した対象を計算機へ配置し、不要な転送を減らす。これも独立した説明段落である。

### 2. 第二機構

第二機構では前段の結果を受け取り、次に必要な状態を選ぶ。ここも十分な長さにする。

選択結果が外れた場合は通常経路へ戻し、正しさを保つ。この段落も手法説明として数える。
""".splitlines()
        _, method_blocks, method_components = AUDIT.prose_blocks(lines)
        self.assertEqual(len(method_blocks), 4)
        self.assertEqual(sorted(len(v) for v in method_components.values()), [2, 2])

    def test_proposed_method_heading_counts_as_method(self) -> None:
        self.assertTrue(AUDIT.is_method_heading("提案手法"))
        self.assertTrue(AUDIT.is_method_heading("手法のあらまし"))
        self.assertTrue(AUDIT.is_method_heading("手法：全体像"))
        self.assertFalse(AUDIT.is_method_heading("評価手法"))


if __name__ == "__main__":
    unittest.main()
