from __future__ import annotations

import sys
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import survey  # noqa: E402
from survey import _render_paper_list, _render_taxonomy_list  # noqa: E402


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

    def test_canonical_readme_links_to_paper_kept_in_legacy_directory(self) -> None:
        row = self._record("legacy-paper", 2026, 9)
        row["path"] = "papers/inference/03-kv-cache/legacy-paper.md"
        rendered = _render_paper_list(
            [row],
            {row["path"]: 0},
            Path("papers/inference/07-kv-cache-optimization-compression"),
        )

        self.assertIn("../03-kv-cache/legacy-paper.md", "\n".join(rendered))

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

    def test_moved_stub_is_excluded_from_views_indexes_catalog_and_comparison(self) -> None:
        old_rel = "inference/99-other-inference-systems/2024-2401.00001-moved.md"
        new_rel = "inference/07-kv-cache-optimization-compression/2024-2401.00001-moved.md"
        normal_rel = "inference/11-llm-serving-scheduling-disaggregation/2025-2501.00002-normal.md"

        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            (repo / ".survey/survey-state").mkdir(parents=True)
            for rel in (old_rel, new_rel, normal_rel):
                (repo / "papers" / rel).parent.mkdir(parents=True, exist_ok=True)
            (repo / "papers" / old_rel).write_text(
                f"# Moved\n\nThis paper record moved to papers/{new_rel}.\n", encoding="utf-8"
            )
            for rel, canonical_id, title in (
                (new_rel, "arXiv:2401.00001", "moved-paper"),
                (normal_rel, "arXiv:2501.00002", "normal-paper"),
            ):
                (repo / "papers" / rel).write_text(
                    f"---\ncanonical_id: {canonical_id}\narxiv_id: {canonical_id.removeprefix('arXiv:')}\n"
                    f"title: {title}\nsummary: {title} summary\npublished: 2024-01-01\n---\nBody.\n",
                    encoding="utf-8",
                )
            snapshot = {"schema_version": 3, "ignored_moved_stubs": [old_rel.split("/", 1)[1]]}
            (repo / ".survey/survey-state/paper-identity-index.json").write_text(
                json.dumps(snapshot), encoding="utf-8"
            )
            (repo / "README.md").write_text("現在の論文収録数: **0本**（推論0本 + 学習0本 + サーベイ0本）\n", encoding="utf-8")
            (repo / "papers/README.md").write_text("収録論文: **0本**。\n", encoding="utf-8")
            (repo / "papers/inference/README.md").write_text("収録論文: **0本**\n", encoding="utf-8")
            (repo / "papers/inference/07-kv-cache-optimization-compression/README.md").write_text("", encoding="utf-8")
            (repo / "papers/inference/11-llm-serving-scheduling-disaggregation/README.md").write_text("", encoding="utf-8")

            with patch.object(survey, "ROOT", repo / ".survey"):
                views = survey.paper_views()
                self.assertEqual({row["path"] for row in views}, {f"papers/{new_rel}", f"papers/{normal_rel}"})
                self.assertEqual(len(views), 2)

                by_family = survey.render_indexes(views, now=datetime(2026, 9, 11, tzinfo=ZoneInfo("Asia/Tokyo")))
                survey._update_catalog_counts(by_family)
                survey.render_comparison(survey.papers())

            inference_index = (repo / "papers/inference/README.md").read_text(encoding="utf-8")
            kv_index = (repo / "papers/inference/07-kv-cache-optimization-compression/README.md").read_text(encoding="utf-8")
            moved_lineage_readme = repo / "papers/inference/99-other-inference-systems/README.md"
            catalog = (repo / "papers/README.md").read_text(encoding="utf-8")
            root_readme = (repo / "README.md").read_text(encoding="utf-8")
            comparison = (repo / "papers/inference/comparison.md").read_text(encoding="utf-8")
            self.assertIn("推論論文：**2本**", inference_index)
            self.assertIn("| [07-kv-cache-optimization-compression](07-kv-cache-optimization-compression/README.md) | 1 |", inference_index)
            self.assertIn("| [11-llm-serving-scheduling-disaggregation](11-llm-serving-scheduling-disaggregation/README.md) | 1 |", inference_index)
            self.assertIn("moved-paper", kv_index)
            self.assertFalse(moved_lineage_readme.exists())
            self.assertNotIn("2024-2401.00001-moved.md", inference_index)
            self.assertNotIn("99-other-inference-systems/", comparison)
            self.assertIn("07-kv-cache-optimization-compression/2024-2401.00001-moved.md", comparison)
            self.assertIn("normal-paper", comparison)
            self.assertIn("収録論文: **2本**。", catalog)
            self.assertIn("現在の論文収録数: **2本**", root_readme)


if __name__ == "__main__":
    unittest.main()
