from __future__ import annotations

import sys
import tempfile
import unittest
from io import BytesIO
from urllib.error import HTTPError
from unittest.mock import patch
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import backfill_paper_metadata  # noqa: E402


class BackfillPaperMetadataTests(unittest.TestCase):
    def test_incomplete_import_is_completed_from_existing_text_and_arxiv_facts(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            paper = root / "papers/inference/99-other-inference-systems/2026-2609.99991-test.md"
            paper.parent.mkdir(parents=True)
            paper.write_text(
                """---
canonical_id: "arXiv:2609.99991"
arxiv_id: "2609.99991"
title: "Imported Test Paper"
list_summary: "既存の一文解説をそのまま再利用してメタデータを補完するためのテスト論文である。"
source: "https://arxiv.org/abs/2609.99991"
---

# Imported Test Paper

## 一文解説
既存の一文解説をそのまま再利用してメタデータを補完するためのテスト論文である。

## 概要
本文。
""",
                encoding="utf-8",
            )
            meta, body = backfill_paper_metadata.parse_frontmatter(paper)
            self.assertTrue(backfill_paper_metadata.metadata_needs_backfill(meta, body))

            changed, added = backfill_paper_metadata.backfill(
                paper,
                {
                    "2609.99991": {
                        "authors": ["Example Author"],
                        "published": "2026-09-01",
                        "arxiv_categories": {"primary": "cs.LG", "cross_list": []},
                        "abs_url": "https://arxiv.org/abs/2609.99991",
                        "pdf_url": "https://arxiv.org/pdf/2609.99991",
                    }
                },
                "2026-09-26",
            )

            self.assertTrue(changed)
            self.assertIn("summary(existing-one-line)", added)
            meta, body = backfill_paper_metadata.parse_frontmatter(paper)
            self.assertEqual(meta["summary"], meta["list_summary"])
            self.assertEqual(meta["authors"], ["Example Author"])
            self.assertEqual(meta["publication"], "arXiv")
            self.assertEqual(meta["publication_type"], "プレプリント")
            self.assertEqual(meta["publication_status"], "arXiv preprint")
            self.assertEqual(meta["arxiv_categories"]["primary"], "cs.LG")
            self.assertIsNone(meta["code"])
            self.assertEqual(meta["last_checked"], "2026-09-26")
            self.assertFalse(backfill_paper_metadata.metadata_needs_backfill(meta, body))

    def test_body_one_line_can_fill_missing_list_and_summary(self) -> None:
        meta = {
            "canonical_id": "arXiv:2609.99992",
            "arxiv_id": "2609.99992",
            "title": "Legacy Import",
        }
        body = """# Legacy Import

## 一文解説
チャット退避から戻した旧形式本文に残っている説明を再利用する。
"""
        self.assertEqual(
            backfill_paper_metadata.body_one_line_summary(body),
            "チャット退避から戻した旧形式本文に残っている説明を再利用する。",
        )
        self.assertTrue(backfill_paper_metadata.metadata_needs_backfill(meta, body))


    def test_arxiv_fetch_falls_back_after_http_error(self) -> None:
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2609.99991v1</id>
    <published>2026-09-01T00:00:00Z</published>
    <author><name>Example Author</name></author>
    <arxiv:primary_category term="cs.LG"/>
    <category term="cs.LG"/>
  </entry>
</feed>"""
        class Response:
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return xml

        calls = []
        def fake_urlopen(req, timeout=60):
            calls.append(req.full_url)
            if req.full_url.startswith("https://export.arxiv.org/"):
                raise HTTPError(req.full_url, 406, "Not Acceptable", {}, BytesIO())
            return Response()

        with patch.object(backfill_paper_metadata, "urlopen", side_effect=fake_urlopen):
            with patch.object(backfill_paper_metadata.time, "sleep"):
                result = backfill_paper_metadata.fetch_arxiv(["2609.99991"])

        self.assertIn("2609.99991", result)
        self.assertEqual(result["2609.99991"]["authors"], ["Example Author"])
        self.assertTrue(any(url.startswith("https://arxiv.org/api/query?") for url in calls))


    def test_arxiv_fetch_falls_back_to_html_metadata(self) -> None:
        html = b"""<html><head>
<meta name="citation_author" content="Example Author">
<meta name="citation_author" content="Second Author">
<meta name="citation_date" content="2026/09/01">
<meta name="citation_keywords" content="Machine Learning (cs.LG); Artificial Intelligence (cs.AI)">
</head><body></body></html>"""

        class Response:
            def __init__(self, payload):
                self.payload = payload
            def __enter__(self):
                return self
            def __exit__(self, *args):
                return False
            def read(self):
                return self.payload

        def fake_urlopen(req, timeout=60):
            url = req.full_url
            if "/api/query?" in url:
                raise HTTPError(url, 406, "Not Acceptable", {}, BytesIO())
            if url == "https://arxiv.org/html/2609.99991":
                return Response(html)
            raise AssertionError(url)

        with patch.object(backfill_paper_metadata, "urlopen", side_effect=fake_urlopen):
            with patch.object(backfill_paper_metadata.time, "sleep"):
                result = backfill_paper_metadata.fetch_arxiv(["2609.99991"])

        row = result["2609.99991"]
        self.assertEqual(row["authors"], ["Example Author", "Second Author"])
        self.assertEqual(row["published"], "2026-09-01")
        self.assertEqual(row["arxiv_categories"]["primary"], "cs.LG")
        self.assertEqual(row["arxiv_categories"]["cross_list"], ["cs.AI"])


if __name__ == "__main__":
    unittest.main()
