from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import backfill_citation_pdfs as pdfs  # noqa: E402


class PdfCitationFallbackTest(unittest.TestCase):
    def test_arxiv_and_acl_pdf_candidates_are_primary(self) -> None:
        meta = {
            "canonical_id": "arXiv:2608.00577",
            "arxiv_id": "2608.00577",
            "source": "https://aclanthology.org/2025.findings-acl.377/",
            "sources": [],
        }
        with patch.object(pdfs, "discover_pdf_urls", return_value=[]):
            urls = pdfs.candidate_pdf_urls(meta)
        self.assertIn("https://arxiv.org/pdf/2608.00577.pdf", urls)
        self.assertIn("https://aclanthology.org/2025.findings-acl.377.pdf", urls)

    def test_numbered_reference_section_splits_entries(self) -> None:
        section = """
[1] A. Author. First Paper. arXiv:2303.06865.
[2] B. Author. Second Paper. https://doi.org/10.1145/1234.5678.
[3] C. Author. Third Paper.
"""
        entries = pdfs.split_reference_entries(section)
        self.assertEqual(len(entries), 3)
        self.assertIn("2303.06865", entries[0])
        self.assertIn("10.1145/1234.5678", entries[1])

    def test_whole_section_title_match_recovers_merged_entries(self) -> None:
        section = "References\nA long citation to Exact Repository Paper Title for Testing Systems."
        refs, _ = pdfs.references_from_section(
            section,
            aliases={},
            title_targets=[
                (pdfs.normalize_title("Exact Repository Paper Title for Testing Systems"), "arXiv:9999.00001"),
            ],
        )
        self.assertEqual(refs, [{"canonical_id": "arXiv:9999.00001"}])


if __name__ == "__main__":
    unittest.main()
