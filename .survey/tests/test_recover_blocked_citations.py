from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import recover_blocked_citations as recovery  # noqa: E402


class RecoverBlockedCitationsTest(unittest.TestCase):
    def test_verified_primary_pdf_overrides_cover_known_blockers(self) -> None:
        self.assertEqual(
            recovery.PRIMARY_PDF_OVERRIDES["DOI:10.1145/3688351.3689164"],
            "https://dl.acm.org/doi/pdf/10.1145/3688351.3689164",
        )
        self.assertIn("AAAI:39816", recovery.PRIMARY_PDF_OVERRIDES)
        self.assertIn("AAAI:39454", recovery.PRIMARY_PDF_OVERRIDES)
        self.assertIn("AAAI:39106", recovery.PRIMARY_PDF_OVERRIDES)

    def test_bibtex_blocks_keep_complete_entries(self) -> None:
        text = """
@article{first,
  title = {First Repository Paper},
  doi = {10.1000/first}
}

@misc{second,
  title = {Second Repository Paper},
  eprint = {2303.06865},
  archivePrefix = {arXiv}
}
"""
        blocks = recovery.bibtex_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertIn("10.1000/first", blocks[0])
        self.assertIn("2303.06865", blocks[1])

    def test_withdrawn_arxiv_source_has_version_fallbacks(self) -> None:
        urls = recovery.arxiv_source_urls("2602.04816")
        self.assertIn("https://export.arxiv.org/e-print/2602.04816", urls)
        self.assertIn("https://export.arxiv.org/e-print/2602.04816v3", urls)
        self.assertIn("https://arxiv.org/e-print/2602.04816v2", urls)
        self.assertIn("https://arxiv.org/e-print/2602.04816v1", urls)


if __name__ == "__main__":
    unittest.main()
