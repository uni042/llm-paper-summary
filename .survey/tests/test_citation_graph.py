from __future__ import annotations

import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from citation_graph import PaperRecord, build_graph, citation_counts_from_view_records  # noqa: E402


class CitationGraphTest(unittest.TestCase):
    def test_counts_each_source_target_pair_once_and_excludes_self(self) -> None:
        a = PaperRecord(
            path="papers/inference/a.md",
            canonical_id="arXiv:2303.06865",
            identifiers=("arXiv:2303.06865", "DOI:10.1000/a"),
            meta={
                "references": [
                    {"canonical_id": "arXiv:2401.00001", "arxiv_id": "2401.00001"},
                    {"doi": "10.1000/b"},
                    {"canonical_id": "arXiv:2303.06865"},
                ]
            },
        )
        b = PaperRecord(
            path="papers/training/b.md",
            canonical_id="arXiv:2401.00001",
            identifiers=("arXiv:2401.00001", "DOI:10.1000/b"),
            meta={"references": []},
        )
        outgoing, counts = build_graph([a, b])
        self.assertEqual(outgoing[a.path], {b.path})
        self.assertEqual(counts[b.path], 1)
        self.assertEqual(counts[a.path], 0)

    def test_arxiv_versions_and_multiple_identifiers_resolve_to_one_paper(self) -> None:
        views = [
            {
                "path": "papers/inference/a.md",
                "meta": {
                    "canonical_id": "arXiv:2303.06865",
                    "arxiv_id": "2303.06865",
                    "references": [
                        {"canonical_id": "arXiv:2401.00001v3"},
                        {"doi": "https://doi.org/10.1000/B"},
                    ],
                },
            },
            {
                "path": "papers/survey/b.md",
                "meta": {
                    "canonical_id": "arXiv:2401.00001",
                    "arxiv_id": "2401.00001v2",
                    "doi": "10.1000/b",
                    "references": [],
                },
            },
        ]
        counts = citation_counts_from_view_records(views)
        self.assertEqual(counts["papers/survey/b.md"], 1)

    def test_plain_body_mentions_are_irrelevant(self) -> None:
        views = [
            {
                "path": "papers/inference/a.md",
                "meta": {"canonical_id": "arXiv:2303.06865", "arxiv_id": "2303.06865", "references": []},
                "text": "本文で 2401.00001 に言及するだけ。",
            },
            {
                "path": "papers/inference/b.md",
                "meta": {"canonical_id": "arXiv:2401.00001", "arxiv_id": "2401.00001", "references": []},
                "text": "",
            },
        ]
        counts = citation_counts_from_view_records(views)
        self.assertEqual(counts["papers/inference/b.md"], 0)


if __name__ == "__main__":
    unittest.main()
