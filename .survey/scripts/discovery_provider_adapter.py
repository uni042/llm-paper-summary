#!/usr/bin/env python3
"""Provider-backed Discovery page fetchers.

The adapter keeps one search result set fixed and exposes it as
fetch_page(cursor) -> {"records": [...], "next_cursor": ...} for
discovery_search_filter.collect_until_unseen().
"""
from __future__ import annotations

import json
import re
import sys
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable
from urllib.error import HTTPError
from urllib.parse import parse_qs, quote, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

import paper_identity
import reference_pool

DEFAULT_FIELDS = "paperId,title,url,year,authors,venue,citationCount,externalIds,publicationDate,abstract"
S2_API_HOST = "api.semanticscholar.org"
S2_WEB_HOSTS = {"www.semanticscholar.org", "semanticscholar.org"}
S2_MAX_RATE_LIMIT_RETRIES = 4
S2_RATE_LIMIT_BASE_SECONDS = 2.0
S2_RATE_LIMIT_MAX_SECONDS = 30.0
S2_PAPER_BATCH_URL = "https://api.semanticscholar.org/graph/v1/paper/batch"
S2_EXPLICIT_FIELDS = "paperId,title,url,year,authors,venue,citationCount,externalIds,publicationDate,abstract"
OPENREVIEW_NOTES_URL = "https://api2.openreview.net/notes"
EXPLICIT_ID_MAX_ITEMS = 100
EXPLICIT_ID_NETWORK_RETRIES = 2
ARXIV_ABS_URL = "https://arxiv.org/abs/"
ACL_ANTHOLOGY_URL = "https://aclanthology.org/"


class DiscoveryProviderError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class _ArxivMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.values: dict[str, list[str]] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "meta":
            return
        values = {key.casefold(): value for key, value in attrs if value is not None}
        name = str(values.get("name") or values.get("property") or "").strip().casefold()
        content = str(values.get("content") or "").strip()
        if name and content:
            self.values.setdefault(name, []).append(content)


def _arxiv_abs_record(requested_id: str, html: str) -> dict[str, Any] | None:
    match = re.fullmatch(r"DOI:10\.48550/arxiv\.(\d{4}\.\d{4,5})", requested_id, re.I)
    if not match:
        return None
    arxiv_id = match.group(1)
    parser = _ArxivMetaParser()
    parser.feed(html)
    title_values = parser.values.get("citation_title") or parser.values.get("dc.title") or []
    title = title_values[0].strip() if title_values else ""
    if not title:
        return None
    cited_ids = parser.values.get("citation_arxiv_id") or []
    if cited_ids and all(value.casefold() != arxiv_id.casefold() for value in cited_ids):
        return None

    record: dict[str, Any] = {
        "canonical_id": "arXiv:" + arxiv_id,
        "arxiv_id": arxiv_id,
        "identifiers": [requested_id],
        "title": title,
        "source_url": ARXIV_ABS_URL + arxiv_id,
    }
    authors = parser.values.get("citation_author") or parser.values.get("dc.creator") or []
    if authors:
        record["authors"] = authors
    abstract_values = parser.values.get("citation_abstract") or parser.values.get("dc.description") or []
    if abstract_values:
        record["abstract"] = abstract_values[0]
    date_values = parser.values.get("citation_date") or parser.values.get("citation_publication_date") or []
    if date_values:
        record["published"] = date_values[0]
        year = re.search(r"\b(19|20)\d{2}\b", date_values[0])
        if year:
            record["year"] = int(year.group(0))
    doi_values = parser.values.get("citation_doi") or []
    if doi_values:
        record["doi"] = doi_values[0]
    return record


def _fetch_arxiv_abs_record(
    requested_id: str,
    *,
    timeout: int,
    opener: Callable[..., Any],
    sleeper: Callable[[float], Any],
) -> tuple[dict[str, Any] | None, str | None]:
    match = re.fullmatch(r"DOI:10\.48550/arxiv\.(\d{4}\.\d{4,5})", requested_id, re.I)
    if not match:
        return None, None
    arxiv_id = match.group(1)
    request = Request(
        ARXIV_ABS_URL + arxiv_id,
        headers={
            "Accept": "text/html",
            "User-Agent": "llm-paper-summary-discovery/1.0",
        },
    )
    network_attempt = 0
    rate_attempt = 0
    while True:
        try:
            with opener(request, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
            return _arxiv_abs_record(requested_id, html), None
        except HTTPError as exc:
            if exc.code == 404:
                return None, None
            if exc.code == 429 and rate_attempt < S2_MAX_RATE_LIMIT_RETRIES:
                sleeper(_semantic_scholar_retry_delay(exc, rate_attempt))
                rate_attempt += 1
                continue
            if 500 <= exc.code <= 599 and network_attempt < EXPLICIT_ID_NETWORK_RETRIES:
                sleeper(min(1.0 * (2 ** network_attempt), S2_RATE_LIMIT_MAX_SECONDS))
                network_attempt += 1
                continue
            return None, f"official arXiv page lookup failed: {exc}"
        except (TimeoutError, ConnectionError, OSError) as exc:
            if network_attempt < EXPLICIT_ID_NETWORK_RETRIES:
                sleeper(min(1.0 * (2 ** network_attempt), S2_RATE_LIMIT_MAX_SECONDS))
                network_attempt += 1
                continue
            return None, f"official arXiv page lookup network error: {exc}"
        except Exception as exc:
            return None, f"official arXiv page lookup failed: {exc}"


def _acl_anthology_record(requested_id: str, html: str, anthology_id: str) -> dict[str, Any] | None:
    parser = _ArxivMetaParser()
    parser.feed(html)
    title_values = parser.values.get("citation_title") or parser.values.get("dc.title") or []
    title = title_values[0].strip() if title_values else ""
    if not title:
        return None

    doi_values = parser.values.get("citation_doi") or []
    doi = doi_values[0].strip() if doi_values else requested_id.split(":", 1)[1]
    if paper_identity.safe_norm_id("DOI:" + doi) != requested_id:
        return None
    record: dict[str, Any] = {
        "canonical_id": requested_id,
        "doi": doi,
        "identifiers": [requested_id],
        "title": title,
        "source_url": ACL_ANTHOLOGY_URL + anthology_id + "/",
    }
    authors = parser.values.get("citation_author") or parser.values.get("dc.creator") or []
    if authors:
        record["authors"] = authors
    abstract_values = parser.values.get("citation_abstract") or parser.values.get("dc.description") or []
    if abstract_values:
        record["abstract"] = abstract_values[0]
    date_values = parser.values.get("citation_publication_date") or parser.values.get("citation_date") or []
    if date_values:
        record["published"] = date_values[0]
    year_match = re.search(r"\b(19|20)\d{2}\b", date_values[0] if date_values else anthology_id)
    if year_match:
        record["year"] = int(year_match.group(0))
    return record


def _fetch_acl_anthology_record(
    requested_id: str,
    *,
    timeout: int,
    opener: Callable[..., Any],
    sleeper: Callable[[float], Any],
) -> tuple[dict[str, Any] | None, str | None]:
    match = re.fullmatch(r"DOI:10\.18653/v1/([A-Za-z0-9][A-Za-z0-9._-]{1,79})", requested_id, re.I)
    if not match:
        return None, None
    anthology_id = match.group(1)
    request = Request(
        ACL_ANTHOLOGY_URL + quote(anthology_id, safe="._-") + "/",
        headers={
            "Accept": "text/html",
            "User-Agent": "llm-paper-summary-discovery/1.0",
        },
    )
    network_attempt = 0
    rate_attempt = 0
    while True:
        try:
            with opener(request, timeout=timeout) as response:
                html = response.read().decode("utf-8", errors="replace")
            return _acl_anthology_record(requested_id, html, anthology_id), None
        except HTTPError as exc:
            if exc.code == 404:
                return None, None
            if exc.code == 429 and rate_attempt < S2_MAX_RATE_LIMIT_RETRIES:
                sleeper(_semantic_scholar_retry_delay(exc, rate_attempt))
                rate_attempt += 1
                continue
            if 500 <= exc.code <= 599 and network_attempt < EXPLICIT_ID_NETWORK_RETRIES:
                sleeper(min(1.0 * (2 ** network_attempt), S2_RATE_LIMIT_MAX_SECONDS))
                network_attempt += 1
                continue
            return None, f"official ACL Anthology page lookup failed: {exc}"
        except (TimeoutError, ConnectionError, OSError) as exc:
            if network_attempt < EXPLICIT_ID_NETWORK_RETRIES:
                sleeper(min(1.0 * (2 ** network_attempt), S2_RATE_LIMIT_MAX_SECONDS))
                network_attempt += 1
                continue
            return None, f"official ACL Anthology page lookup network error: {exc}"
        except Exception as exc:
            return None, f"official ACL Anthology page lookup failed: {exc}"

def _paper_record(paper: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(paper, dict):
        return None
    title = str(paper.get("title") or "").strip()
    if not title:
        return None
    external = paper.get("externalIds") if isinstance(paper.get("externalIds"), dict) else {}
    paper_id = str(paper.get("paperId") or "").strip() or None
    record: dict[str, Any] = {
        "title": title,
        "source_url": paper.get("url") or None,
        "year": paper.get("year"),
        "published": paper.get("publicationDate") or None,
        "venue": paper.get("venue") or None,
        "citation_count": max(int(paper.get("citationCount") or 0), 0),
        "citation_count_source": "semantic_scholar",
        "abstract": paper.get("abstract") or None,
        "identifiers": (["SemanticScholar:" + paper_id] if paper_id else []),
    }
    if paper_id:
        record["semantic_scholar_id"] = paper_id
    arxiv = str(external.get("ArXiv") or "").strip() or None
    doi = str(external.get("DOI") or "").strip() or None
    if arxiv:
        record["canonical_id"] = f"arXiv:{arxiv}"
        record["arxiv_id"] = arxiv
        record["source_url"] = f"https://arxiv.org/abs/{arxiv}"
    if doi:
        record["doi"] = doi
        if not arxiv:
            record["canonical_id"] = f"DOI:{doi}"
            record["source_url"] = f"https://doi.org/{doi}"
    if not record.get("canonical_id") and paper_id:
        record["canonical_id"] = "SemanticScholar:" + paper_id
    authors = paper.get("authors")
    if isinstance(authors, list):
        names = []
        for author in authors:
            if isinstance(author, dict) and author.get("name"):
                names.append(str(author["name"]))
        if names:
            record["authors"] = names
    return record



def _explicit_identifier(value: Any) -> tuple[str, str]:
    raw = str(value or "").strip()
    normalized = paper_identity.safe_norm_id(raw)
    if not normalized:
        raise DiscoveryProviderError("candidate identifier must be non-empty")
    if normalized.startswith("arXiv:"):
        suffix = normalized.split(":", 1)[1]
        if not re.fullmatch(r"(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})", suffix, re.I):
            raise DiscoveryProviderError(f"unsupported arXiv identifier: {raw!r}")
        return normalized, "semantic_scholar"
    if normalized.startswith("DOI:"):
        suffix = normalized.split(":", 1)[1]
        if not re.fullmatch(r"10\.\d{4,9}/\S+", suffix, re.I):
            raise DiscoveryProviderError(f"unsupported DOI identifier: {raw!r}")
        return normalized, "semantic_scholar"
    if normalized.startswith("SemanticScholar:"):
        suffix = normalized.split(":", 1)[1]
        if not re.fullmatch(r"[0-9a-f]{40}", suffix, re.I):
            raise DiscoveryProviderError(f"unsupported Semantic Scholar identifier: {raw!r}")
        return "SemanticScholar:" + suffix.casefold(), "semantic_scholar"
    if normalized.startswith("OpenReview:"):
        suffix = normalized.split(":", 1)[1]
        if not re.fullmatch(r"[A-Za-z0-9]{10}", suffix):
            raise DiscoveryProviderError(f"unsupported OpenReview identifier: {raw!r}")
        return normalized, "openreview"
    raise DiscoveryProviderError(f"unsupported candidate identifier: {raw!r}")


def _semantic_scholar_id(normalized: str) -> str:
    prefix, suffix = normalized.split(":", 1)
    if prefix == "arXiv":
        return "ARXIV:" + suffix
    if prefix == "SemanticScholar":
        return suffix
    return "DOI:" + suffix


def _explicit_json_request(
    request: Request,
    *,
    timeout: int,
    opener: Callable[..., Any],
    sleeper: Callable[[float], Any],
    not_found_is_empty: bool = False,
) -> Any:
    network_attempt = 0
    rate_attempt = 0
    while True:
        try:
            with opener(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code == 429 and rate_attempt < S2_MAX_RATE_LIMIT_RETRIES:
                sleeper(_semantic_scholar_retry_delay(exc, rate_attempt))
                rate_attempt += 1
                continue
            if not_found_is_empty and exc.code == 404:
                return None
            raise DiscoveryProviderError(
                f"explicit identifier lookup failed: {exc}",
                status_code=exc.code,
            ) from exc
        except (TimeoutError, ConnectionError, OSError) as exc:
            if network_attempt < EXPLICIT_ID_NETWORK_RETRIES:
                sleeper(min(1.0 * (2 ** network_attempt), S2_RATE_LIMIT_MAX_SECONDS))
                network_attempt += 1
                continue
            raise DiscoveryProviderError(f"explicit identifier lookup network error: {exc}") from exc
        except Exception as exc:
            raise DiscoveryProviderError(f"explicit identifier lookup failed: {exc}") from exc


def _identifier_matches_record(requested_id: str, record: dict[str, Any]) -> bool:
    return requested_id in paper_identity.record_identifiers(record)


def _openreview_record(note: Any, requested_id: str) -> dict[str, Any] | None:
    if not isinstance(note, dict):
        return None
    note_id = str(note.get("id") or "").strip()
    if paper_identity.safe_norm_id("OpenReview:" + note_id) != requested_id:
        return None
    content = note.get("content") if isinstance(note.get("content"), dict) else {}

    def value(name: str) -> Any:
        raw = content.get(name)
        return raw.get("value") if isinstance(raw, dict) and "value" in raw else raw

    title = str(value("title") or "").strip()
    if not title:
        return None
    record: dict[str, Any] = {
        "canonical_id": requested_id,
        "openreview_id": note_id,
        "title": title,
        "source_url": "https://openreview.net/forum?" + urlencode({"id": note_id}),
        "abstract": value("abstract") or None,
        "year": value("year"),
    }
    authors = value("authors") or value("author")
    if isinstance(authors, str):
        record["authors"] = [authors] if authors else []
    elif isinstance(authors, list):
        record["authors"] = [str(author) for author in authors if author]
    doi = value("doi") or value("DOI")
    if doi:
        record["doi"] = str(doi).strip()
    arxiv = value("arxiv_id") or value("arxiv")
    if arxiv:
        record["arxiv_id"] = str(arxiv).strip()
    return record


def lookup_identifiers(
    identifiers: list[str],
    *,
    timeout: int = 30,
    opener: Callable[..., Any] = urlopen,
    sleeper: Callable[[float], Any] = time.sleep,
) -> list[dict[str, Any]]:
    """Resolve a bounded list of stable paper IDs through fixed official APIs.

    Results remain in request order. Each row has requested_id, status (found,
    unresolved, or error), record, lookup_route, and an error message when useful.
    """
    if not isinstance(identifiers, list) or not 1 <= len(identifiers) <= EXPLICIT_ID_MAX_ITEMS:
        raise DiscoveryProviderError(f"identifiers must be a list of 1 to {EXPLICIT_ID_MAX_ITEMS} IDs")
    normalized: list[tuple[str, str]] = [_explicit_identifier(value) for value in identifiers]
    ids = [item[0] for item in normalized]
    if len(set(ids)) != len(ids):
        raise DiscoveryProviderError("duplicate candidate identifiers are not allowed")

    outcomes: dict[str, dict[str, Any]] = {}
    s2_ids = [identifier for identifier, provider in normalized if provider == "semantic_scholar"]
    if s2_ids:
        s2_api_ids = [_semantic_scholar_id(identifier) for identifier in s2_ids]
        batch_rows: list[Any] = []
        batch_error: str | None = None
        try:
            request = Request(
                S2_PAPER_BATCH_URL + "?" + urlencode({"fields": S2_EXPLICIT_FIELDS}),
                data=json.dumps({"ids": s2_api_ids}).encode("utf-8"),
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "User-Agent": "llm-paper-summary-discovery/1.0",
                },
                method="POST",
            )
            payload = _explicit_json_request(
                request, timeout=timeout, opener=opener, sleeper=sleeper
            )
            if not isinstance(payload, list):
                raise DiscoveryProviderError("Semantic Scholar batch response must be a list")
            batch_rows = payload
        except Exception as exc:
            batch_error = str(exc)

        for index, requested_id in enumerate(s2_ids):
            row = batch_rows[index] if index < len(batch_rows) else None
            record = _paper_record(row) if isinstance(row, dict) else None
            if record and _identifier_matches_record(requested_id, record):
                outcomes[requested_id] = {
                    "requested_id": requested_id,
                    "status": "found",
                    "record": record,
                    "lookup_route": "semantic_scholar_batch",
                    "error": None,
                }
                continue

            api_id = _semantic_scholar_id(requested_id)
            single_error = batch_error
            try:
                encoded_id = quote(api_id, safe="")
                single_request = Request(
                    "https://api.semanticscholar.org/graph/v1/paper/" + encoded_id + "?" + urlencode({"fields": S2_EXPLICIT_FIELDS}),
                    headers={"Accept": "application/json", "User-Agent": "llm-paper-summary-discovery/1.0"},
                )
                single_payload = _explicit_json_request(
                    single_request, timeout=timeout, opener=opener, sleeper=sleeper,
                    not_found_is_empty=True,
                )
                single_record = _paper_record(single_payload) if isinstance(single_payload, dict) else None
                if single_record and _identifier_matches_record(requested_id, single_record):
                    outcomes[requested_id] = {
                        "requested_id": requested_id,
                        "status": "found",
                        "record": single_record,
                        "lookup_route": "semantic_scholar_single",
                        "error": None,
                    }
                    continue
                mismatch = bool(single_record)
                outcomes[requested_id] = {
                    "requested_id": requested_id,
                    "status": "unresolved",
                    "record": None,
                    "lookup_route": "semantic_scholar_single",
                    "error": "provider identifier mismatch: returned a different paper" if mismatch else None,
                }
            except Exception as exc:
                outcomes[requested_id] = {
                    "requested_id": requested_id,
                    "status": "error",
                    "record": None,
                    "lookup_route": "semantic_scholar_single",
                    "error": str(exc) or single_error,
                }

    for requested_id, provider in normalized:
        if provider != "semantic_scholar" or not re.fullmatch(
            r"DOI:10\.48550/arxiv\.\d{4}\.\d{4,5}", requested_id, re.I
        ):
            continue
        previous = outcomes.get(requested_id)
        if previous and previous.get("status") == "found":
            continue
        record, error = _fetch_arxiv_abs_record(
            requested_id, timeout=timeout, opener=opener, sleeper=sleeper
        )
        if record and _identifier_matches_record(requested_id, record):
            outcomes[requested_id] = {
                "requested_id": requested_id,
                "status": "found",
                "record": record,
                "lookup_route": "arxiv_abs_html",
                "error": None,
            }
        else:
            outcomes[requested_id] = {
                "requested_id": requested_id,
                "status": "error" if error else "unresolved",
                "record": None,
                "lookup_route": "arxiv_abs_html",
                "error": error,
            }

    for requested_id, provider in normalized:
        if provider != "semantic_scholar" or not re.fullmatch(
            r"DOI:10\.18653/v1/[A-Za-z0-9][A-Za-z0-9._-]{1,79}", requested_id, re.I
        ):
            continue
        previous = outcomes.get(requested_id)
        if previous and previous.get("status") == "found":
            continue
        record, error = _fetch_acl_anthology_record(
            requested_id, timeout=timeout, opener=opener, sleeper=sleeper
        )
        if record and _identifier_matches_record(requested_id, record):
            outcomes[requested_id] = {
                "requested_id": requested_id,
                "status": "found",
                "record": record,
                "lookup_route": "acl_anthology_record",
                "error": None,
            }
        else:
            outcomes[requested_id] = {
                "requested_id": requested_id,
                "status": "error" if error else "unresolved",
                "record": None,
                "lookup_route": "acl_anthology_record",
                "error": error,
            }

    for requested_id, provider in normalized:
        if provider != "openreview":
            continue
        note_id = requested_id.split(":", 1)[1]
        request = Request(
            OPENREVIEW_NOTES_URL + "?" + urlencode({"id": note_id}),
            headers={"Accept": "application/json", "User-Agent": "llm-paper-summary-discovery/1.0"},
        )
        try:
            payload = _explicit_json_request(
                request, timeout=timeout, opener=opener, sleeper=sleeper,
                not_found_is_empty=True,
            )
            notes = payload.get("notes") if isinstance(payload, dict) else None
            note = next((item for item in notes or [] if isinstance(item, dict) and item.get("id") == note_id), None)
            record = _openreview_record(note, requested_id)
            if record and _identifier_matches_record(requested_id, record):
                outcomes[requested_id] = {
                    "requested_id": requested_id,
                    "status": "found",
                    "record": record,
                    "lookup_route": "openreview_notes",
                    "error": None,
                }
            else:
                mismatch = bool(notes)
                outcomes[requested_id] = {
                    "requested_id": requested_id,
                    "status": "unresolved",
                    "record": None,
                    "lookup_route": "openreview_notes",
                    "error": "provider identifier mismatch: returned a different paper" if mismatch else None,
                }
        except Exception as exc:
            outcomes[requested_id] = {
                "requested_id": requested_id,
                "status": "error",
                "record": None,
                "lookup_route": "openreview_notes",
                "error": str(exc),
            }
    return [outcomes[identifier] for identifier in ids]

def _normalize_semantic_scholar_source(source_url: str) -> str:
    parsed = urlparse(source_url)
    if parsed.scheme != "https":
        raise DiscoveryProviderError("Semantic Scholar source_url must use https")

    if parsed.netloc == S2_API_HOST:
        if not parsed.path.startswith("/graph/v1/paper/"):
            raise DiscoveryProviderError("unsupported Semantic Scholar API endpoint")
        return source_url

    if parsed.netloc not in S2_WEB_HOSTS:
        raise DiscoveryProviderError("unsupported provider host")

    qs = parse_qs(parsed.query)
    if parsed.path.rstrip("/") == "/search":
        query = (qs.get("q") or qs.get("query") or [""])[0].strip()
        if not query:
            raise DiscoveryProviderError("Semantic Scholar search URL is missing q/query")
        return "https://api.semanticscholar.org/graph/v1/paper/search?" + urlencode({"query": query})

    # Recognize paper URLs whose final path component is the stable Semantic Scholar paper id.
    parts = [p for p in parsed.path.split("/") if p]
    direction = None
    if parts and parts[-1] in {"citations", "references"}:
        direction = parts[-1]
        parts = parts[:-1]
    if "paper" in parts and direction and parts:
        paper_id = parts[-1]
        if not re.fullmatch(r"[A-Fa-f0-9]{40}", paper_id):
            raise DiscoveryProviderError("Semantic Scholar paper URL does not end in a 40-hex paper id")
        return f"https://api.semanticscholar.org/graph/v1/paper/{paper_id}/{direction}"

    raise DiscoveryProviderError(
        "unsupported Semantic Scholar web URL; use a /search?q=... URL or a paper citations/references URL"
    )


def _semantic_scholar_retry_delay(exc: HTTPError, attempt: int) -> float:
    retry_after = None
    headers = getattr(exc, "headers", None)
    if headers is not None:
        value = headers.get("Retry-After")
        if value is not None:
            try:
                retry_after = float(str(value).strip())
            except (TypeError, ValueError):
                retry_after = None
    if retry_after is not None and retry_after >= 0:
        return min(retry_after, S2_RATE_LIMIT_MAX_SECONDS)
    return min(
        S2_RATE_LIMIT_BASE_SECONDS * (2 ** max(attempt, 0)),
        S2_RATE_LIMIT_MAX_SECONDS,
    )


def semantic_scholar_fetcher(
    source_url: str,
    *,
    page_size: int = 100,
    timeout: int = 30,
    opener: Callable[..., Any] = urlopen,
    sleeper: Callable[[float], Any] = time.sleep,
) -> Callable[[str | None], dict[str, Any]]:
    """Build a page fetcher for one fixed Semantic Scholar result set."""
    if page_size <= 0 or page_size > 100:
        raise ValueError("page_size must be between 1 and 100")

    api_url = _normalize_semantic_scholar_source(source_url)
    parsed = urlparse(api_url)
    base_qs = parse_qs(parsed.query, keep_blank_values=True)
    base_qs.pop("offset", None)
    base_qs.pop("limit", None)
    base_qs["fields"] = [DEFAULT_FIELDS]

    path = parsed.path
    if path.endswith("/citations"):
        nested_key = "citingPaper"
    elif path.endswith("/references"):
        nested_key = "citedPaper"
    elif path.endswith("/paper/search"):
        nested_key = None
    else:
        raise DiscoveryProviderError("unsupported Semantic Scholar paper endpoint")

    def fetch_page(cursor: str | None) -> dict[str, Any]:
        offset = int(cursor or "0")
        if offset < 0:
            raise DiscoveryProviderError("cursor offset must be non-negative")
        qs = {k: list(v) for k, v in base_qs.items()}
        qs["offset"] = [str(offset)]
        qs["limit"] = [str(page_size)]
        query = urlencode([(k, item) for k, values in qs.items() for item in values])
        page_url = urlunparse(parsed._replace(query=query))
        req = Request(
            page_url,
            headers={
                "Accept": "application/json",
                "User-Agent": "llm-paper-summary-discovery/1.0",
            },
        )
        payload = None
        for attempt in range(S2_MAX_RATE_LIMIT_RETRIES + 1):
            try:
                with opener(req, timeout=timeout) as response:
                    payload = json.loads(response.read().decode("utf-8"))
                break
            except HTTPError as exc:
                if exc.code != 429 or attempt >= S2_MAX_RATE_LIMIT_RETRIES:
                    raise DiscoveryProviderError(
                        f"Semantic Scholar page fetch failed at offset {offset}: {exc}"
                    ) from exc
                delay = _semantic_scholar_retry_delay(exc, attempt)
                print(
                    "[WORKER-GUIDE][Discovery] Semantic Scholar rate limited "
                    f"at offset {offset}; retry {attempt + 1}/{S2_MAX_RATE_LIMIT_RETRIES} "
                    f"after {delay:.1f}s.",
                    file=sys.stderr,
                )
                sleeper(delay)
            except Exception as exc:
                raise DiscoveryProviderError(
                    f"Semantic Scholar page fetch failed at offset {offset}: {exc}"
                ) from exc
        if payload is None:
            raise DiscoveryProviderError(
                f"Semantic Scholar page fetch failed at offset {offset}: rate-limit retries exhausted"
            )
        if not isinstance(payload, dict) or not isinstance(payload.get("data"), list):
            raise DiscoveryProviderError("Semantic Scholar response is missing data[]")

        records: list[dict[str, Any]] = []
        for row in payload["data"]:
            paper = row.get(nested_key) if nested_key and isinstance(row, dict) else row
            record = _paper_record(paper)
            if record:
                records.append(record)

        next_value = payload.get("next")
        next_cursor = str(next_value) if isinstance(next_value, int) and next_value >= 0 else None
        return {
            "records": records,
            "next_cursor": next_cursor,
            "page_url": page_url,
            "position": offset,
        }

    return fetch_page



OPENALEX_HOST = "api.openalex.org"


def _openalex_record(work: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(work, dict):
        return None
    title = str(work.get("display_name") or work.get("title") or "").strip()
    if not title:
        return None
    openalex_id = str(work.get("id") or "").rstrip("/").split("/")[-1]
    doi = str(work.get("doi") or "").strip()
    if doi.startswith("https://doi.org/"):
        doi = doi[len("https://doi.org/"):]
    source_url = None
    primary = work.get("primary_location")
    if isinstance(primary, dict):
        source_url = primary.get("landing_page_url") or primary.get("pdf_url")
    locations = work.get("locations")
    arxiv_id = None
    if isinstance(locations, list):
        for location in locations:
            if not isinstance(location, dict):
                continue
            for field in ("landing_page_url", "pdf_url"):
                value = str(location.get(field) or "")
                match = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", value)
                if match:
                    arxiv_id = match.group(1)
                    source_url = source_url or f"https://arxiv.org/abs/{arxiv_id}"
                    break
            if arxiv_id:
                break

    record: dict[str, Any] = {
        "title": title,
        "source_url": source_url or (f"https://openalex.org/{openalex_id}" if openalex_id else None),
        "year": work.get("publication_year"),
        "published": work.get("publication_date") or None,
    }
    if arxiv_id:
        record["canonical_id"] = f"arXiv:{arxiv_id}"
        record["arxiv_id"] = arxiv_id
    elif doi:
        record["canonical_id"] = f"DOI:{doi}"
        record["doi"] = doi
    elif openalex_id:
        record["canonical_id"] = f"OpenAlex:{openalex_id}"

    authorships = work.get("authorships")
    if isinstance(authorships, list):
        names = []
        for authorship in authorships:
            author = authorship.get("author") if isinstance(authorship, dict) else None
            if isinstance(author, dict) and author.get("display_name"):
                names.append(str(author["display_name"]))
        if names:
            record["authors"] = names
    return record


def _validate_openalex_url(source_url: str, *, singleton: bool = False) -> tuple[Any, dict[str, list[str]]]:
    parsed = urlparse(source_url)
    if parsed.scheme != "https" or parsed.netloc != OPENALEX_HOST:
        raise DiscoveryProviderError("OpenAlex source_url must use https://api.openalex.org")
    if singleton:
        if not re.fullmatch(r"/works/W\d+", parsed.path):
            raise DiscoveryProviderError("OpenAlex references source_url must be a singleton /works/W... URL")
    elif parsed.path != "/works":
        raise DiscoveryProviderError("OpenAlex paginated source_url must use /works")
    return parsed, parse_qs(parsed.query, keep_blank_values=True)


def openalex_fetcher(
    source_url: str,
    *,
    page_size: int = 100,
    timeout: int = 30,
    opener: Callable[..., Any] = urlopen,
) -> Callable[[str | None], dict[str, Any]]:
    """Build a cursor-paginated fetcher for one fixed OpenAlex /works result set."""
    if page_size <= 0 or page_size > 100:
        raise ValueError("page_size must be between 1 and 100")
    parsed, base_qs = _validate_openalex_url(source_url)
    for key in ("cursor", "page", "per_page"):
        base_qs.pop(key, None)

    def fetch_page(cursor: str | None) -> dict[str, Any]:
        cursor_value = cursor if cursor is not None else "*"
        qs = {k: list(v) for k, v in base_qs.items()}
        qs["cursor"] = [cursor_value]
        qs["per_page"] = [str(page_size)]
        query = urlencode([(k, item) for k, values in qs.items() for item in values])
        page_url = urlunparse(parsed._replace(query=query))
        req = Request(
            page_url,
            headers={"Accept": "application/json", "User-Agent": "llm-paper-summary-discovery/1.0"},
        )
        try:
            with opener(req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise DiscoveryProviderError(f"OpenAlex page fetch failed at cursor {cursor_value!r}: {exc}") from exc
        results = payload.get("results") if isinstance(payload, dict) else None
        meta = payload.get("meta") if isinstance(payload, dict) else None
        if not isinstance(results, list) or not isinstance(meta, dict):
            raise DiscoveryProviderError("OpenAlex response is missing results[] or meta")
        records = []
        for work in results:
            record = _openalex_record(work)
            if record:
                records.append(record)
        next_value = meta.get("next_cursor")
        next_cursor = str(next_value) if isinstance(next_value, str) and next_value else None
        return {
            "records": records,
            "next_cursor": next_cursor,
            "page_url": page_url,
            "position": cursor_value,
        }

    return fetch_page


def openalex_references_fetcher(
    source_url: str,
    *,
    page_size: int = 100,
    timeout: int = 30,
    opener: Callable[..., Any] = urlopen,
) -> Callable[[str | None], dict[str, Any]]:
    """Page through one work's fixed referenced_works list in stable chunks."""
    if page_size <= 0 or page_size > 100:
        raise ValueError("page_size must be between 1 and 100")
    parsed, _ = _validate_openalex_url(source_url, singleton=True)
    req = Request(
        source_url,
        headers={"Accept": "application/json", "User-Agent": "llm-paper-summary-discovery/1.0"},
    )
    try:
        with opener(req, timeout=timeout) as response:
            work = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise DiscoveryProviderError(f"OpenAlex reference-list fetch failed: {exc}") from exc
    refs = work.get("referenced_works") if isinstance(work, dict) else None
    if not isinstance(refs, list):
        raise DiscoveryProviderError("OpenAlex work response is missing referenced_works[]")
    work_ids = []
    for value in refs:
        ident = str(value or "").rstrip("/").split("/")[-1]
        if re.fullmatch(r"W\d+", ident):
            work_ids.append(ident)

    def fetch_page(cursor: str | None) -> dict[str, Any]:
        index = int(cursor or "0")
        if index < 0:
            raise DiscoveryProviderError("reference cursor must be non-negative")
        chunk = work_ids[index:index + page_size]
        if not chunk:
            return {"records": [], "next_cursor": None, "position": index}
        filter_value = "|".join(chunk)
        url = "https://api.openalex.org/works?" + urlencode(
            {"filter": f"openalex:{filter_value}", "per_page": str(len(chunk))}
        )
        page_req = Request(
            url,
            headers={"Accept": "application/json", "User-Agent": "llm-paper-summary-discovery/1.0"},
        )
        try:
            with opener(page_req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise DiscoveryProviderError(f"OpenAlex referenced-work batch fetch failed at {index}: {exc}") from exc
        results = payload.get("results") if isinstance(payload, dict) else None
        if not isinstance(results, list):
            raise DiscoveryProviderError("OpenAlex referenced-work batch is missing results[]")
        records = []
        for item in results:
            record = _openalex_record(item)
            if record:
                records.append(record)
        next_index = index + len(chunk)
        next_cursor = str(next_index) if next_index < len(work_ids) else None
        return {"records": records, "next_cursor": next_cursor, "page_url": url, "position": index}

    return fetch_page


def repository_reference_pool_fetcher(
    source_url: str,
    *,
    page_size: int = 100,
    repo_root: Path | None = None,
    unrelated_ledger_path: Path | None = None,
    borderline_ledger_path: Path | None = None,
    include_borderline: bool = False,
) -> Callable[[str | None], dict[str, Any]]:
    """Page through the repository-wide structured-reference candidate pool."""
    if source_url != reference_pool.SOURCE_URL:
        raise DiscoveryProviderError(
            f"repository_references source_url must be {reference_pool.SOURCE_URL!r}"
        )
    if page_size <= 0 or page_size > 100:
        raise ValueError("page_size must be between 1 and 100")
    root = Path(repo_root or Path.cwd()).resolve()
    unrelated = (
        Path(unrelated_ledger_path)
        if unrelated_ledger_path is not None
        else root / reference_pool.DEFAULT_UNRELATED_LEDGER
    )
    borderline = (
        Path(borderline_ledger_path)
        if borderline_ledger_path is not None
        else root / reference_pool.DEFAULT_BORDERLINE_LEDGER
    )
    pool = reference_pool.build_reference_pool(
        root,
        unrelated_ledger_path=unrelated,
        borderline_ledger_path=borderline,
        include_borderline=include_borderline,
    )
    records = list(pool["candidates"])
    provider_progress = {
        key: int(pool[key])
        for key in (
            "reference_total_count",
            "reference_processed_count",
            "reference_remaining_count",
            "reference_represented_count",
            "reference_unrelated_count",
            "reference_borderline_count",
        )
    }
    status_reported = False

    def fetch_page(cursor: str | None) -> dict[str, Any]:
        nonlocal status_reported
        index = int(cursor or "0")
        if index < 0:
            raise DiscoveryProviderError("repository reference cursor must be non-negative")
        chunk = records[index:index + page_size]
        next_index = index + len(chunk)
        next_cursor = str(next_index) if next_index < len(records) else None
        if not status_reported:
            print(
                "[WORKER-GUIDE][探索状況] "
                f"構造化references 総候補 {provider_progress['reference_total_count']}件 / "
                f"処理済み {provider_progress['reference_processed_count']}件 / "
                f"未処理 {provider_progress['reference_remaining_count']}件 / "
                f"収録済み {provider_progress['reference_represented_count']}件 / "
                f"無関係 {provider_progress['reference_unrelated_count']}件 / "
                f"微妙 {provider_progress['reference_borderline_count']}件 / "
                f"今回offset {index}",
                file=sys.stderr,
            )
            status_reported = True
        return {
            "records": chunk,
            "next_cursor": next_cursor,
            "page_url": source_url,
            "position": index,
            "pool_candidate_count": len(records),
            "provider_progress": provider_progress,
        }

    return fetch_page

def make_fetcher(
    provider: str,
    source_url: str,
    *,
    page_size: int = 100,
    timeout: int = 30,
    opener: Callable[..., Any] = urlopen,
) -> Callable[[str | None], dict[str, Any]]:
    provider = str(provider or "").strip().casefold()
    if provider in {"semantic_scholar", "semanticscholar", "s2"}:
        return semantic_scholar_fetcher(
            source_url,
            page_size=page_size,
            timeout=timeout,
            opener=opener,
        )
    if provider in {"openalex", "open_alex"}:
        return openalex_fetcher(
            source_url,
            page_size=page_size,
            timeout=timeout,
            opener=opener,
        )
    if provider in {"openalex_references", "open_alex_references"}:
        return openalex_references_fetcher(
            source_url,
            page_size=page_size,
            timeout=timeout,
            opener=opener,
        )
    if provider in {"repository_references", "repository_reference_pool"}:
        return repository_reference_pool_fetcher(
            source_url,
            page_size=page_size,
        )
    raise DiscoveryProviderError(f"unsupported Discovery provider: {provider!r}")
