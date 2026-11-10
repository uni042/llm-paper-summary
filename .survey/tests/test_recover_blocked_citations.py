from __future__ import annotations

import sys
import unittest
from unittest.mock import patch
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

    def test_ieee_blockers_have_primary_pdf_routes(self) -> None:
        expected = {
            "DOI:10.1109/TPDS.2025.3590014",
            "DOI:10.1109/LCA.2024.3406038",
            "DOI:10.1109/HPCA61900.2025.00103",
        }
        self.assertTrue(expected.issubset(recovery.PRIMARY_PDF_OVERRIDES))
        self.assertIn(
            "https://microlab.ntua.gr/wp-content/uploads/2025/03/throttLLeM_HPCA25.pdf",
            recovery.primary_pdf_urls("DOI:10.1109/HPCA61900.2025.00103"),
        )

    def test_acm_doi_generically_derives_official_pdf_route(self) -> None:
        self.assertIn(
            "https://dl.acm.org/doi/pdf/10.1145/3315508.3329973",
            recovery.primary_pdf_urls("DOI:10.1145/3315508.3329973"),
        )

    def test_current_acm_blockers_have_primary_pdf_routes(self) -> None:
        expected = {
            "DOI:10.1145/3830422.3830427",
            "DOI:10.1145/3745756.3809243",
            "DOI:10.1145/3816440.3818602",
        }
        self.assertTrue(expected.issubset(recovery.PRIMARY_PDF_OVERRIDES))
        self.assertIn(
            "https://lca.ece.utexas.edu/pubs/li_sigopsreview26.pdf",
            recovery.primary_pdf_urls("DOI:10.1145/3830422.3830427"),
        )

    def test_verified_author_and_arxiv_fallbacks_cover_legacy_acm_blockers(self) -> None:
        self.assertIn(
            "https://www.eecs.harvard.edu/~htk/publication/2019-mapl-tillet-kung-cox.pdf",
            recovery.primary_pdf_urls("DOI:10.1145/3315508.3329973"),
        )
        self.assertIn(
            "https://madsys.cs.tsinghua.edu.cn/publication/ktransformers-unleashing-the-full-potential-of-cpu/gpu-hybrid-inference-for-moe-models/SOSP25-chen.pdf",
            recovery.primary_pdf_urls("DOI:10.1145/3731569.3764843"),
        )
        self.assertIn(
            "https://arxiv.org/pdf/2304.07493",
            recovery.primary_pdf_urls("DOI:10.1145/3579371.3589038"),
        )

        self.assertIn(
            "https://scale.snu.ac.kr/papers/2024-04-Conference-ASPLOS-AttAcc.pdf",
            recovery.primary_pdf_urls("DOI:10.1145/3620665.3640422"),
        )

    def test_twinpilots_has_author_hosted_primary_pdf_fallback(self) -> None:
        urls = recovery.primary_pdf_urls("DOI:10.1145/3688351.3689164")
        self.assertEqual(urls[0], "https://dl.acm.org/doi/pdf/10.1145/3688351.3689164")
        self.assertIn("https://jiangs.utasites.cloud/pubs/papers/Yu24-TwinPilots.pdf", urls)

    def test_transpim_has_verified_nsf_primary_pdf_fallback(self) -> None:
        urls = recovery.primary_pdf_urls("DOI:10.1109/HPCA53966.2022.00082")
        self.assertEqual(urls[0], "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=9773212")
        self.assertIn("https://par.nsf.gov/servlets/purl/10345536", urls)

    def test_crossref_reference_entries_preserve_doi_and_title_metadata(self) -> None:
        payload = {
            "message": {
                "reference": [
                    {
                        "DOI": "10.1000/example",
                        "article-title": "Example Repository Paper",
                        "author": "A. Author",
                        "year": "2025",
                    },
                    {
                        "unstructured": "B. Author. Another paper. arXiv:2303.06865.",
                    },
                ]
            }
        }
        with patch.object(recovery, "fetch_bytes", return_value=__import__("json").dumps(payload).encode()):
            entries, url = recovery.crossref_reference_entries("DOI:10.1145/1234.5678")
        self.assertEqual(len(entries), 2)
        self.assertIn("https://doi.org/10.1000/example", entries[0]["hrefs"])
        self.assertIn("Example Repository Paper", entries[0]["text"])
        self.assertIn("api.crossref.org", url)

    def test_non_acm_doi_uses_publisher_deposited_crossref_fallback(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as folder:
            root = Path(folder)
            paper = root / "papers/inference/example/paper.md"
            paper.parent.mkdir(parents=True)
            paper.write_text("placeholder", encoding="utf-8")
            meta = {
                "canonical_id": "DOI:10.3390/electronics15112475",
                "title": "A publisher DOI paper with a deposited bibliography",
            }
            with (
                patch.object(recovery, "load_records", return_value=[]),
                patch.object(recovery, "alias_index", return_value={}),
                patch.object(recovery, "paper_paths", return_value=[paper]),
                patch.object(recovery, "front", return_value=(meta, "")),
                patch.object(recovery, "primary_pdf_urls", return_value=[]),
                patch.object(
                    recovery, "crossref_reference_entries",
                    return_value=([{"text": "A. Author 2025 DOI:10.1000/example", "hrefs": []}], "https://api.crossref.org/works/example"),
                ) as crossref,
                patch.object(recovery, "coverage_report", return_value={"summary": {"incomplete": 0}}),
            ):
                result = recovery.backfill(root, limit=1, apply=False)
            self.assertEqual(result["attempted"], 1)
            self.assertEqual(result["completed"], 1)
            crossref.assert_called_once_with("DOI:10.3390/electronics15112475")

    def test_metadata_pdf_urls_keep_primary_pdf_and_exclude_non_pdf(self) -> None:
        meta = {
            "source": "https://danyangzhuo.com/papers/MICRO25-LLM265.pdf",
            "sources": [
                "https://danyangzhuo.com/papers/MICRO25-LLM265.pdf",
                "https://aclanthology.org/2026.findings-acl.1521/",
                "https://ojs.aaai.org/index.php/AAAI/article/download/34567/36722",
                "https://127.0.0.1/secret.pdf",
                "http://example.org/unsafe.pdf",
            ],
        }
        self.assertEqual(
            recovery.metadata_primary_pdf_urls(meta),
            [
                "https://danyangzhuo.com/papers/MICRO25-LLM265.pdf",
                "https://ojs.aaai.org/index.php/AAAI/article/download/34567/36722",
            ],
        )

    def test_partial_audit_with_date_but_no_total_is_retried_from_own_pdf(self) -> None:
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as folder:
            root = Path(folder)
            paper = root / "papers/inference/example/paper.md"
            paper.parent.mkdir(parents=True)
            paper.write_text("placeholder", encoding="utf-8")
            meta = {
                "canonical_id": "DOI:10.1145/3725843.3756078",
                "source": "https://danyangzhuo.com/papers/MICRO25-LLM265.pdf",
                "references": [{"canonical_id": "arXiv:2210.17323"}],
                "references_checked_at": "2026-10-22",
                "references_source": "selected_primary_pdf_references",
                # No references_total: insufficient for coverage_report PASS.
            }
            primary_url = meta["source"]
            with (
                patch.object(recovery, "load_records", return_value=[]),
                patch.object(recovery, "alias_index", return_value={}),
                patch.object(recovery, "paper_paths", return_value=[paper]),
                patch.object(recovery, "front", return_value=(meta, "")),
                patch.object(recovery, "primary_pdf_urls", return_value=[]),
                patch.object(recovery, "pdf_text", return_value="dummy full paper") as pdf,
                patch.object(recovery, "reference_section", return_value="References example"),
                patch.object(
                    recovery, "references_from_section",
                    return_value=([{"canonical_id": "arXiv:2210.17323"}], 34),
                ),
                patch.object(recovery, "coverage_report", return_value={"summary": {"incomplete": 0}}),
            ):
                result = recovery.backfill(root, limit=1, apply=False)
            self.assertEqual(result["attempted"], 1)
            self.assertEqual(result["completed"], 1)
            pdf.assert_called_once_with(primary_url)
            self.assertEqual(meta["references_total"], 34)

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
