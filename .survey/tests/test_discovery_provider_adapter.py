from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from urllib.parse import parse_qs, urlparse


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import discovery_provider_adapter  # noqa: E402


class _Response:
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


class DiscoveryProviderAdapterTest(unittest.TestCase):
    def test_semantic_scholar_search_url_uses_offset_pagination(self) -> None:
        calls = []

        def opener(request, timeout=30):
            parsed = urlparse(request.full_url)
            qs = parse_qs(parsed.query)
            calls.append(qs)
            offset = int(qs["offset"][0])
            if offset == 0:
                return _Response(
                    {
                        "offset": 0,
                        "next": 2,
                        "data": [
                            {
                                "paperId": "a" * 40,
                                "title": "Paper A",
                                "externalIds": {"ArXiv": "2609.10001"},
                                "url": "https://www.semanticscholar.org/paper/" + "a" * 40,
                            },
                            {
                                "paperId": "b" * 40,
                                "title": "Paper B",
                                "externalIds": {"DOI": "10.1000/test"},
                            },
                        ],
                    }
                )
            return _Response(
                {
                    "offset": 2,
                    "data": [
                        {
                            "paperId": "c" * 40,
                            "title": "Paper C",
                            "externalIds": {},
                        }
                    ],
                }
            )

        fetch = discovery_provider_adapter.semantic_scholar_fetcher(
            "https://www.semanticscholar.org/search?q=llm%20serving",
            page_size=2,
            opener=opener,
        )
        first = fetch(None)
        second = fetch(first["next_cursor"])

        self.assertEqual(first["next_cursor"], "2")
        self.assertIsNone(second["next_cursor"])
        self.assertEqual(first["records"][0]["canonical_id"], "arXiv:2609.10001")
        self.assertEqual(first["records"][1]["canonical_id"], "DOI:10.1000/test")
        self.assertTrue(second["records"][0]["canonical_id"].startswith("SemanticScholar:"))
        self.assertEqual(calls[0]["offset"], ["0"])
        self.assertEqual(calls[1]["offset"], ["2"])
        self.assertEqual(calls[0]["limit"], ["2"])

    def test_semantic_scholar_citations_unwraps_citing_paper(self) -> None:
        paper_id = "d" * 40

        def opener(request, timeout=30):
            return _Response(
                {
                    "offset": 0,
                    "data": [
                        {
                            "citingPaper": {
                                "paperId": "e" * 40,
                                "title": "Citing Paper",
                                "externalIds": {"ArXiv": "2609.20001"},
                            }
                        }
                    ],
                }
            )

        fetch = discovery_provider_adapter.semantic_scholar_fetcher(
            f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/citations",
            opener=opener,
        )
        page = fetch(None)
        self.assertEqual(page["records"][0]["canonical_id"], "arXiv:2609.20001")

    def test_openalex_search_uses_cursor_pagination(self) -> None:
        calls = []

        def opener(request, timeout=30):
            parsed = urlparse(request.full_url)
            qs = parse_qs(parsed.query)
            calls.append(qs)
            cursor = qs["cursor"][0]
            if cursor == "*":
                return _Response(
                    {
                        "meta": {"next_cursor": "cursor-2"},
                        "results": [
                            {
                                "id": "https://openalex.org/W1",
                                "display_name": "OpenAlex A",
                                "doi": "https://doi.org/10.1000/a",
                                "publication_year": 2026,
                            }
                        ],
                    }
                )
            return _Response(
                {
                    "meta": {"next_cursor": None},
                    "results": [
                        {
                            "id": "https://openalex.org/W2",
                            "display_name": "OpenAlex B",
                            "publication_year": 2026,
                        }
                    ],
                }
            )

        fetch = discovery_provider_adapter.openalex_fetcher(
            "https://api.openalex.org/works?search=llm+serving&filter=publication_year:2026",
            page_size=1,
            opener=opener,
        )
        first = fetch(None)
        second = fetch(first["next_cursor"])

        self.assertEqual(first["next_cursor"], "cursor-2")
        self.assertIsNone(second["next_cursor"])
        self.assertEqual(first["records"][0]["canonical_id"], "DOI:10.1000/a")
        self.assertEqual(second["records"][0]["canonical_id"], "OpenAlex:W2")
        self.assertEqual(calls[0]["cursor"], ["*"])
        self.assertEqual(calls[1]["cursor"], ["cursor-2"])
        self.assertEqual(calls[0]["per_page"], ["1"])

    def test_openalex_references_pages_fixed_reference_list(self) -> None:
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            if request.full_url == "https://api.openalex.org/works/W123":
                return _Response(
                    {
                        "referenced_works": [
                            "https://openalex.org/W10",
                            "https://openalex.org/W11",
                            "https://openalex.org/W12",
                        ]
                    }
                )
            parsed = urlparse(request.full_url)
            qs = parse_qs(parsed.query)
            ids = qs["filter"][0].split(":", 1)[1].split("|")
            return _Response(
                {
                    "meta": {"count": len(ids)},
                    "results": [
                        {"id": f"https://openalex.org/{ident}", "display_name": ident}
                        for ident in ids
                    ],
                }
            )

        fetch = discovery_provider_adapter.openalex_references_fetcher(
            "https://api.openalex.org/works/W123",
            page_size=2,
            opener=opener,
        )
        first = fetch(None)
        second = fetch(first["next_cursor"])
        self.assertEqual(first["next_cursor"], "2")
        self.assertIsNone(second["next_cursor"])
        self.assertEqual([r["canonical_id"] for r in first["records"]], ["OpenAlex:W10", "OpenAlex:W11"])
        self.assertEqual([r["canonical_id"] for r in second["records"]], ["OpenAlex:W12"])

    def test_make_fetcher_routes_repository_references(self) -> None:
        fetch = discovery_provider_adapter.make_fetcher(
            "repository_references",
            discovery_provider_adapter.reference_pool.SOURCE_URL,
            page_size=1,
        )
        self.assertTrue(callable(fetch))

    def test_rejects_unapproved_provider_host(self) -> None:
        with self.assertRaises(discovery_provider_adapter.DiscoveryProviderError):
            discovery_provider_adapter.semantic_scholar_fetcher(
                "https://example.com/search?q=llm"
            )


if __name__ == "__main__":
    unittest.main()
