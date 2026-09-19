#!/usr/bin/env python3
"""Provider-backed Discovery page fetchers.

The adapter keeps one search result set fixed and exposes it as
fetch_page(cursor) -> {"records": [...], "next_cursor": ...} for
discovery_search_filter.collect_until_unseen().
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse
from urllib.request import Request, urlopen

import reference_pool

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

    def fetch_page(cursor: str | None) -> dict[str, Any]:
        index = int(cursor or "0")
        if index < 0:
            raise DiscoveryProviderError("repository reference cursor must be non-negative")
        chunk = records[index:index + page_size]
        next_index = index + len(chunk)
        next_cursor = str(next_index) if next_index < len(records) else None
        return {
            "records": chunk,
            "next_cursor": next_cursor,
            "page_url": source_url,
            "position": index,
            "pool_candidate_count": len(records),
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
    raise DiscoveryProviderError(f"unsupported Discovery provider: {provider!r}")
