from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from audit_list_summary_quality import audit_file  # noqa: E402


class ExplicitListSummaryAuditTests(unittest.TestCase):
    def test_audit_uses_explicit_frontmatter_value(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers" / "example.md"
            paper.parent.mkdir(parents=True)
            explicit = "本研究は明示された一覧文をそのまま監査し、本文からの自動生成を行わない方式を採用する方針である。"
            paper.write_text(
                "---\n"
                "title: Example\n"
                "summary: fallback summary in English\n"
                f"list_summary: {explicit}\n"
                "---\n"
                "# Example\n\n"
                "> 本文の引用には英語のrequestとtokenが含まれ、一覧文としては使わない。\n\n"
                "## 概要\n\n概要からのfallback summary is forbidden.\n",
                encoding="utf-8",
            )

            result = audit_file(paper, root)

        self.assertEqual(result.summary, explicit)
        self.assertEqual(result.status, "PASS")

    def test_missing_explicit_field_is_a_failure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers" / "example.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                "---\n"
                "title: Example\n"
                "summary: 本文にはない情報を推測せず一覧文を入力する運用を徹底する。\n"
                "---\n"
                "# Example\n\n"
                "> 本研究は明示された一覧文がない場合も本文から自動生成せず、欠落として扱う方式を採用する。\n",
                encoding="utf-8",
            )

            result = audit_file(paper, root)

        self.assertEqual(result.status, "FAIL")
        self.assertTrue(any("list_summary" in failure for failure in result.failures))


if __name__ == "__main__":
    unittest.main()
