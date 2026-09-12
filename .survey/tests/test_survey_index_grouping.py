from __future__ import annotations

import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from survey import _render_taxonomy_list  # noqa: E402


class SurveyIndexGroupingTest(unittest.TestCase):
    def _record(self, name: str, year: int, month: int) -> dict:
        return {
            "path": f"papers/inference/example/{name}.md",
            "title": name,
            "summary": f"{name} summary",
            "year": year,
            "month": month,
            "implementation": None,
        }

    def test_recent_cited_papers_are_featured_and_older_papers_use_rolling_year_buckets(self) -> None:
        rows = [
            self._record("recent-cited-low", 2026, 8),
            self._record("recent-cited-high", 2026, 7),
            self._record("recent-uncited", 2026, 9),
            self._record("two-years-cited", 2025, 8),
            self._record("two-years-boundary", 2024, 10),
            self._record("three-years-boundary", 2024, 9),
        ]
        citations = {
            "papers/inference/example/recent-cited-low.md": 1,
            "papers/inference/example/recent-cited-high.md": 3,
            "papers/inference/example/recent-uncited.md": 0,
            "papers/inference/example/two-years-cited.md": 2,
            "papers/inference/example/two-years-boundary.md": 0,
            "papers/inference/example/three-years-boundary.md": 1,
        }

        rendered = _render_taxonomy_list(
            rows,
            citations,
            Path("papers/inference/example"),
            now=datetime(2026, 9, 11, tzinfo=ZoneInfo("Asia/Tokyo")),
        )

        attention_heading = "### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）"
        recent_heading = "### 直近12か月・未被引用（2025-10〜2026-09）"
        two_year_heading = "### 2年前（2024-10〜2025-09）"
        three_year_heading = "### 3年前（2023-10〜2024-09）"
        self.assertLess(rendered.index(attention_heading), rendered.index(recent_heading))
        self.assertLess(rendered.index(recent_heading), rendered.index(two_year_heading))
        self.assertLess(rendered.index(two_year_heading), rendered.index(three_year_heading))
        self.assertNotIn("### 1年以上前", rendered)
        self.assertNotIn("### その他", rendered)

        attention = rendered[rendered.index(attention_heading):rendered.index(recent_heading)]
        self.assertLess(attention.index("recent-cited-high"), attention.index("recent-cited-low"))
        self.assertNotIn("recent-uncited", attention)

        recent = rendered[rendered.index(recent_heading):rendered.index(two_year_heading)]
        self.assertIn("recent-uncited", recent)
        self.assertNotIn("recent-cited-low", recent)

        two_years = rendered[rendered.index(two_year_heading):rendered.index(three_year_heading)]
        self.assertIn("two-years-cited", two_years)
        self.assertIn("two-years-boundary", two_years)
        self.assertNotIn("three-years-boundary", two_years)
        self.assertLess(two_years.index("two-years-cited"), two_years.index("two-years-boundary"))

        three_years = rendered[rendered.index(three_year_heading):]
        self.assertIn("three-years-boundary", three_years)
        self.assertNotIn("two-years-boundary", three_years)

    def test_paper_entries_use_mobile_friendly_vertical_blocks(self) -> None:
        row = self._record("mobile-paper", 2026, 9)
        rendered = _render_taxonomy_list(
            [row],
            {row["path"]: 2},
            Path("papers/inference/example"),
            now=datetime(2026, 9, 11, tzinfo=ZoneInfo("Asia/Tokyo")),
        )

        self.assertNotIn("| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |", rendered)
        self.assertIn("- **2026-09 · [mobile-paper](mobile-paper.md)**", rendered)
        self.assertIn("実装：— ・ リポジトリ内被引用：2", rendered)
        self.assertIn("mobile-paper summary", rendered)


if __name__ == "__main__":
    unittest.main()
