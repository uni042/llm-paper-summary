#!/usr/bin/env python3
"""Provider-backed Discovery page fetchers.

The adapter keeps one search result set fixed and exposes it as
fetch_page(cursor) -> {"records": [...], "next_cursor": ...} for
discovery_search_filter.collect_until_unseen().
"""
from __future__ import annotations

import json
import re
from typing import Any, Callable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

DEFAULT_FIELDS = "title,url,year,authors,externalIds,publicationDate,abstract"
S2_API_HOST = "api.semanticscholar.org"
S2_WEB_HOSTS = {"www.semanticscholar.org", "semanticscholar.org"}


class DiscoveryProviderError(RuntimeError):
    pass


def _paper_record(paper: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(paper, dict):
        return None
    title = str(paper.get("title") or "").strip()
    if not title:
        return None
    external = paper.get("externalIds") if isinstance(paper.get("externalIds"), dict) else {}
    record: dict[str, Any] = {
        "title": title,
        "source_url": paper.get("url") or None,
        "year": paper.get("year"),
        "published": paper.get("publicationDate") or None,
        "abstract": paper.get("abstract") or None,
    }
    arxiv = external.get("ArXiv")
    doi = external.get("DOI")
    if arxiv:
        record["canonical_id"] = f"arXiv:{str(arxiv).strip()}"
        record["arxiv_id"] = str(arxiv).strip()
        record["source_url"] = record["source_url"] or f"https://arxiv.org/abs/{str(arxiv).strip()}"
    elif doi:
        record["canonical_id"] = f"DOI:{str(doi).strip()}"
        record["doi"] = str(doi).strip()
    elif paper.get("paperId"):
        record["canonical_id"] = "SemanticScholar:" + str(paper["paperId"]).strip()
    authors = paper.get("authors")
    if isinstance(authors, list):
        names = []
        for author in authors:
            if isinstance(author, dict) and author.get("name"):
                names.append(str(author["name"]))
        if names:
            record["authors"] = names
    return record


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


def semantic_scholar_fetcher(
    source_url: str,
    *,
    page_size: int = 100,
    timeout: int = 30,
    opener: Callable[..., Any] = urlopen,
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
        try:
            with opener(req, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except Exception as exc:
            raise DiscoveryProviderError(f"Semantic Scholar page fetch failed at offset {offset}: {exc}") from exc
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
    raise DiscoveryProviderError(f"unsupported Discovery provider: {provider!r}")
