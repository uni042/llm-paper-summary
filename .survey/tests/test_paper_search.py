from __future__ import annotations

import importlib.util
import gzip
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "build_paper_search.py"
SPEC = importlib.util.spec_from_file_location("build_paper_search", SCRIPT)
search = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(search)


class PaperSearchBuilderTests(unittest.TestCase):
    def test_markdown_to_visible_text_excludes_links_tags_comments_and_frontmatter(self):
        raw = "---\ntitle: metadata-secret\n---\n本文 <b>重要</b> [リンク](https://invalid.test) <!-- hidden --> `code`"
        visible = search.visible_text(raw)
        self.assertIn("本文 重要 リンク code", visible)
        self.assertNotIn("metadata-secret", visible)
        self.assertNotIn("invalid.test", visible)
        self.assertNotIn("hidden", visible)

    def test_build_creates_fixed_scope_pages_and_removes_only_stale_manifest_files(self):
        temp_root = Path(__file__).resolve().parents[2] / ".tmp"
        temp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            root = Path(temp)
            (root / "papers/inference/07-kv-cache-optimization-compression").mkdir(parents=True)
            (root / "papers/training/optimization").mkdir(parents=True)
            (root / "papers/inference/07-kv-cache-optimization-compression/a.md").write_text(
                "---\ntitle: 日本語 <script>alert(1)</script>\nsummary: 短い概要\nlist_summary: compact text\n---\n## 概要\nsection-only term full detail\n\n## 方法\nmethod-only term\n", encoding="utf-8")
            (root / "papers/training/optimization/b.md").write_text(
                "---\ntitle: training\nsummary: 学習概要\n---\n別本文\n", encoding="utf-8")
            out = root / "_site"
            (out / "unrelated.txt").parent.mkdir(parents=True)
            (out / "unrelated.txt").write_text("keep", encoding="utf-8")
            stale = out / "old/index.html"
            stale.parent.mkdir(parents=True)
            stale.write_text("old", encoding="utf-8")
            (out / search.MANIFEST).write_text(json.dumps(["old/index.html"]), encoding="utf-8")

            result = search.build(root, out)

            for page in ("index.html", "inference/index.html", "training/index.html",
                         "survey/index.html", "inference/07-kv-cache-optimization-compression/index.html"):
                self.assertTrue((out / page).is_file(), page)
            self.assertFalse(stale.exists())
            self.assertEqual((out / "unrelated.txt").read_text(encoding="utf-8"), "keep")
            scope_path = out / "inference/07-kv-cache-optimization-compression/papers.json.gz"
            scope = json.loads(gzip.decompress(scope_path.read_bytes()).decode("utf-8"))
            self.assertEqual(len(scope["papers"]), 1)
            self.assertEqual(scope["papers"][0]["path"], "papers/inference/07-kv-cache-optimization-compression/a.md")
            self.assertIn("section-only term", scope["papers"][0]["body"])
            self.assertNotIn("metadata-secret", json.dumps(scope))
            self.assertIn("短い概要", scope["papers"][0]["summary"])
            self.assertIn("compact text", scope["papers"][0]["summary"])
            self.assertIn("section-only term full detail", scope["papers"][0]["summary"])
            self.assertNotIn("method-only term", scope["papers"][0]["summary"])
            self.assertLessEqual(len(scope["papers"][0]["summary_display"]), 240)
            self.assertEqual(result["scopes"], 6)
            html = (out / "inference/07-kv-cache-optimization-compression/index.html").read_text(encoding="utf-8")
            self.assertNotIn("<script>alert(1)</script>", html)
            self.assertIn('data-scope="inference/07-kv-cache-optimization-compression"', html)
            family_html = (out / "inference/index.html").read_text(encoding="utf-8")
            self.assertIn("07-kv-cache-optimization-compression/index.html", family_html)

    def test_output_cannot_be_repo_or_ancestor(self):
        temp_root = Path(__file__).resolve().parents[2] / ".tmp"
        temp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            root = Path(temp)
            with self.assertRaises(ValueError):
                search.build(root, root)
            with self.assertRaises(ValueError):
                search.build(root / "child", root)

    def test_nonempty_unmanaged_output_is_not_overwritten(self):
        temp_root = Path(__file__).resolve().parents[2] / ".tmp"
        temp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            root = Path(temp)
            out = root / "_site"
            out.mkdir()
            marker = out / "keep.txt"
            marker.write_text("keep", encoding="utf-8")
            with self.assertRaises(ValueError):
                search.build(root, out)
            self.assertEqual(marker.read_text(encoding="utf-8"), "keep")

    def test_readme_search_links_are_added_inside_generated_blocks(self):
        temp_root = Path(__file__).resolve().parents[2] / ".tmp"
        temp_root.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=temp_root) as temp:
            root = Path(temp)
            lineage = "07-kv-cache-optimization-compression"
            family_dir = root / "papers/inference"
            lineage_dir = family_dir / lineage
            lineage_dir.mkdir(parents=True)
            (root / "README.md").write_text("# root\n", encoding="utf-8")
            (root / "papers/README.md").write_text("# papers\n", encoding="utf-8")
            (family_dir / "README.md").write_text("# inference\n", encoding="utf-8")
            (lineage_dir / "README.md").write_text("# lineage\n", encoding="utf-8")
            rows = [{"family": "inference", "lineage": lineage}]

            with patch.object(search.survey, "ROOT", root):
                search.survey._update_catalog_counts({"inference": rows, "training": [], "survey": []})
                search.survey._render_family_overview("inference", rows)
                search.survey.block(f"papers/inference/{lineage}/README.md", search.survey._render_taxonomy_list(
                    [dict(rows[0], path=f"papers/inference/{lineage}/a.md", title="A", summary="", year=2026, month=1, implementation=None)],
                    {}, Path(f"papers/inference/{lineage}")))

            self.assertIn("[全収録論文を検索](https://uni042.github.io/llm-paper-summary/)", (root / "README.md").read_text(encoding="utf-8"))
            self.assertIn(f"[この区分だけ検索](https://uni042.github.io/llm-paper-summary/inference/)", (family_dir / "README.md").read_text(encoding="utf-8"))
            self.assertIn(f"[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/{lineage}/)", (lineage_dir / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
