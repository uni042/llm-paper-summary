from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from urllib.error import HTTPError
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


class _HtmlResponse(_Response):
    def read(self):
        return self.payload.encode("utf-8")


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

    def test_semantic_scholar_retries_http_429_with_retry_after(self) -> None:
        calls = 0
        sleeps = []

        def opener(request, timeout=30):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise HTTPError(
                    request.full_url,
                    429,
                    "Too Many Requests",
                    {"Retry-After": "7"},
                    None,
                )
            return _Response(
                {
                    "offset": 0,
                    "data": [
                        {
                            "paperId": "f" * 40,
                            "title": "Recovered after rate limit",
                            "externalIds": {"ArXiv": "2609.30001"},
                        }
                    ],
                }
            )

        fetch = discovery_provider_adapter.semantic_scholar_fetcher(
            "https://www.semanticscholar.org/search?q=llm%20serving",
            opener=opener,
            sleeper=sleeps.append,
        )
        page = fetch(None)

        self.assertEqual(calls, 2)
        self.assertEqual(sleeps, [7.0])
        self.assertEqual(page["records"][0]["canonical_id"], "arXiv:2609.30001")

    def test_semantic_scholar_429_without_header_uses_exponential_backoff(self) -> None:
        calls = 0
        sleeps = []

        def opener(request, timeout=30):
            nonlocal calls
            calls += 1
            if calls <= 2:
                raise HTTPError(
                    request.full_url,
                    429,
                    "Too Many Requests",
                    {},
                    None,
                )
            return _Response({"offset": 0, "data": []})

        fetch = discovery_provider_adapter.semantic_scholar_fetcher(
            "https://www.semanticscholar.org/search?q=llm%20serving",
            opener=opener,
            sleeper=sleeps.append,
        )
        page = fetch(None)

        self.assertEqual(calls, 3)
        self.assertEqual(sleeps, [2.0, 4.0])
        self.assertEqual(page["records"], [])

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


    def _lookup_ids(self, identifiers, *, opener, sleeper=lambda seconds: None):
        lookup = getattr(discovery_provider_adapter, "lookup_identifiers", None)
        if not callable(lookup):
            return [{"requested_id": value, "status": "missing_adapter", "record": None} for value in identifiers]
        return lookup(identifiers, opener=opener, sleeper=sleeper)

    def test_lookup_identifiers_batches_arxiv_and_doi_and_matches_exact_ids(self) -> None:
        calls = []

        def opener(request, timeout=30):
            calls.append(request)
            self.assertEqual(request.get_method(), "POST")
            parsed = urlparse(request.full_url)
            self.assertEqual(parsed.netloc, "api.semanticscholar.org")
            self.assertEqual(parsed.path, "/graph/v1/paper/batch")
            qs = parse_qs(parsed.query)
            self.assertIn("title", qs["fields"][0])
            self.assertIn("externalIds", qs["fields"][0])
            body = json.loads(request.data.decode("utf-8"))
            self.assertEqual(body["ids"], ["ARXIV:2609.10001", "DOI:10.1000/batch"])
            return _Response([
                {
                    "paperId": "a" * 40,
                    "title": "arXiv item",
                    "externalIds": {"ArXiv": "2609.10001", "DOI": "10.1000/batch"},
                    "url": "https://www.semanticscholar.org/paper/" + "a" * 40,
                },
                {
                    "paperId": "b" * 40,
                    "title": "DOI item",
                    "externalIds": {"DOI": "10.1000/batch"},
                    "url": "https://www.semanticscholar.org/paper/" + "b" * 40,
                },
            ])

        rows = self._lookup_ids(["arXiv:2609.10001", "DOI:10.1000/BATCH"], opener=opener)

        self.assertEqual(len(calls), 1)
        self.assertEqual([row["status"] for row in rows], ["found", "found"])
        self.assertEqual(rows[0]["requested_id"], "arXiv:2609.10001")
        self.assertEqual(rows[0]["record"]["canonical_id"], "arXiv:2609.10001")
        self.assertEqual(rows[0]["record"]["doi"], "10.1000/batch")
        self.assertEqual(rows[1]["record"]["canonical_id"], "DOI:10.1000/batch")
        self.assertEqual(rows[0]["lookup_route"], "semantic_scholar_batch")

    def test_lookup_identifiers_falls_back_to_single_id_after_batch_rejection(self) -> None:
        methods = []

        def opener(request, timeout=30):
            method = request.get_method()
            methods.append(method)
            if method == "POST":
                raise HTTPError(request.full_url, 405, "Method Not Allowed", {}, None)
            return _Response({
                "paperId": "c" * 40,
                "title": "Recovered by direct ID",
                "externalIds": {"ArXiv": "2609.10002"},
                "url": "https://www.semanticscholar.org/paper/" + "c" * 40,
            })

        rows = self._lookup_ids(["arXiv:2609.10002"], opener=opener)

        self.assertEqual(methods, ["POST", "GET"])
        self.assertEqual(rows[0]["status"], "found")
        self.assertEqual(rows[0]["lookup_route"], "semantic_scholar_single")
        self.assertEqual(rows[0]["record"]["canonical_id"], "arXiv:2609.10002")

    def test_arxiv_doi_uses_official_abs_page_when_semantic_scholar_misses(self) -> None:
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            if request.get_method() == "POST":
                return _Response([None])
            if request.full_url.startswith("https://api.semanticscholar.org/"):
                raise HTTPError(request.full_url, 404, "Not Found", {}, None)
            self.assertEqual(request.full_url, "https://arxiv.org/abs/2509.23324")
            self.assertEqual(request.get_header("User-agent"), "llm-paper-summary-discovery/1.0")
            return _HtmlResponse(
                '<html><head>'
                '<meta name="citation_title" content="Scaling LLM Test-Time Compute with Mobile NPU on Smartphones">'
                '<meta name="citation_author" content="A. Researcher">'
                '<meta name="citation_author" content="B. Researcher">'
                '<meta name="citation_abstract" content="A verified abstract.">'
                '<meta name="citation_date" content="2025/09/27">'
                '</head></html>'
            )

        rows = self._lookup_ids(["DOI:10.48550/arXiv.2509.23324"], opener=opener)

        self.assertEqual(len(calls), 3)
        self.assertEqual(rows[0]["status"], "found")
        self.assertEqual(rows[0]["lookup_route"], "arxiv_abs_html")
        self.assertEqual(rows[0]["record"]["canonical_id"], "arXiv:2509.23324")
        self.assertEqual(rows[0]["record"]["identifiers"], ["DOI:10.48550/arxiv.2509.23324"])
        self.assertEqual(rows[0]["record"]["source_url"], "https://arxiv.org/abs/2509.23324")
        self.assertEqual(rows[0]["record"]["title"], "Scaling LLM Test-Time Compute with Mobile NPU on Smartphones")
        self.assertEqual(rows[0]["record"]["authors"], ["A. Researcher", "B. Researcher"])
        self.assertEqual(rows[0]["record"]["abstract"], "A verified abstract.")
        self.assertEqual(rows[0]["record"]["year"], 2025)

    def test_lookup_identifiers_reads_openreview_note_by_exact_id(self) -> None:
        note_id = "Ab12Cd34Ef"
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            parsed = urlparse(request.full_url)
            self.assertEqual(parsed.netloc, "api2.openreview.net")
            self.assertEqual(parsed.path, "/notes")
            self.assertEqual(parse_qs(parsed.query), {"id": [note_id]})
            return _Response({
                "notes": [{
                    "id": note_id,
                    "tcdate": 1780000000000,
                    "content": {
                        "title": {"value": "OpenReview exact match"},
                        "abstract": {"value": "Full abstract."},
                        "authors": {"value": ["A. Author", "B. Author"]},
                    },
                }]
            })

        rows = self._lookup_ids(["OpenReview:" + note_id], opener=opener)

        self.assertEqual(len(calls), 1)
        self.assertEqual(rows[0]["status"], "found")
        self.assertEqual(rows[0]["lookup_route"], "openreview_notes")
        self.assertEqual(rows[0]["record"]["canonical_id"], "OpenReview:" + note_id)
        self.assertEqual(rows[0]["record"]["source_url"], "https://openreview.net/forum?id=" + note_id)
        self.assertEqual(rows[0]["record"]["title"], "OpenReview exact match")
        self.assertEqual(rows[0]["record"]["authors"], ["A. Author", "B. Author"])

    def test_openreview_http_error_preserves_status_code(self) -> None:
        note_id = "EQgEMAD4kv"
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            raise HTTPError(request.full_url, 403, "Forbidden", {}, None)

        rows = self._lookup_ids(["OpenReview:" + note_id], opener=opener)

        self.assertEqual(len(calls), 1)
        self.assertEqual(rows[0]["status"], "error")
        self.assertIn("403", rows[0]["error"])
        self.assertIn("Forbidden", rows[0]["error"])

    def test_lookup_identifiers_rejects_returned_id_mismatch(self) -> None:
        def opener(request, timeout=30):
            if request.get_method() == "POST":
                return _Response([{
                    "paperId": "d" * 40,
                    "title": "Wrong arXiv record",
                    "externalIds": {"ArXiv": "2609.99999"},
                }])
            return _Response({
                "paperId": "d" * 40,
                "title": "Wrong arXiv record",
                "externalIds": {"ArXiv": "2609.99999"},
            })

        rows = self._lookup_ids(["arXiv:2609.10003"], opener=opener)

        self.assertEqual(rows[0]["status"], "unresolved")
        self.assertIsNone(rows[0]["record"])
        self.assertIn("mismatch", rows[0]["error"].lower())

    def test_lookup_identifiers_isolates_one_direct_lookup_error(self) -> None:
        def opener(request, timeout=30):
            if request.get_method() == "POST":
                return _Response([None, None])
            if "2609.10004" in request.full_url:
                return _Response({
                    "paperId": "e" * 40,
                    "title": "Recovered first ID",
                    "externalIds": {"ArXiv": "2609.10004"},
                })
            raise OSError("temporary network outage")

        rows = self._lookup_ids(
            ["arXiv:2609.10004", "arXiv:2609.10005"],
            opener=opener,
        )

        self.assertEqual([row["status"] for row in rows], ["found", "error"])
        self.assertEqual(rows[0]["record"]["canonical_id"], "arXiv:2609.10004")
        self.assertIsNone(rows[1]["record"])
        self.assertIn("network", rows[1]["error"].lower())



    def test_acl_anthology_doi_uses_official_record_when_semantic_scholar_misses(self) -> None:
        calls = []

        def opener(request, timeout=30):
            calls.append(request.full_url)
            if request.get_method() == "POST":
                return _Response([None])
            if request.full_url.startswith("https://api.semanticscholar.org/"):
                raise HTTPError(request.full_url, 404, "Not Found", {}, None)
            self.assertEqual(request.full_url, "https://aclanthology.org/2023.emnlp-main.298/")
            return _HtmlResponse(
                '<html><head>'
                '<meta name="citation_title" content="GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints">'
                '<meta name="citation_author" content="Joshua Ainslie">'
                '<meta name="citation_author" content="James Lee-Thorp">'
                '<meta name="citation_abstract" content="Multi-query attention speeds up decoder inference; grouped-query attention generalizes it.">'
                '<meta name="citation_publication_date" content="2023/12">'
                '<meta name="citation_doi" content="10.18653/v1/2023.emnlp-main.298">'
                '</head></html>'
            )

        rows = self._lookup_ids(["DOI:10.18653/v1/2023.emnlp-main.298"], opener=opener)

        self.assertEqual(len(calls), 3)
        self.assertEqual(rows[0]["status"], "found")
        self.assertEqual(rows[0]["lookup_route"], "acl_anthology_record")
        self.assertEqual(rows[0]["record"]["canonical_id"], "DOI:10.18653/v1/2023.emnlp-main.298")
        self.assertEqual(rows[0]["record"]["doi"], "10.18653/v1/2023.emnlp-main.298")
        self.assertEqual(rows[0]["record"]["source_url"], "https://aclanthology.org/2023.emnlp-main.298/")
        self.assertEqual(rows[0]["record"]["title"], "GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints")
        self.assertEqual(rows[0]["record"]["authors"], ["Joshua Ainslie", "James Lee-Thorp"])
        self.assertEqual(rows[0]["record"]["year"], 2023)

if __name__ == "__main__":
    unittest.main()
