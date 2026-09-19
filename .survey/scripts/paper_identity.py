#!/usr/bin/env python3
"""Shared paper-identity normalization for discovery and final duplicate guards."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from difflib import SequenceMatcher
from typing import Any
from urllib.parse import unquote, urlparse, urlunparse

import survey


IDENTIFIER_FIELDS = (
    ("canonical_id", None),
    ("arxiv_id", "arXiv:"),
    ("doi", "DOI:"),
    ("openreview_id", "OpenReview:"),
)
URL_FIELDS = ("source_url", "source", "canonical_url")
FUZZY_TITLE_THRESHOLD = 0.94


def norm_title(value: Any) -> str | None:
    if not value:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip().casefold()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def resolver_norm_title(value: Any) -> str | None:
    """Normalize titles for paper-level alias matching without changing legacy tokens.

    Punctuation becomes a token boundary rather than being deleted, so ``cache-aware``
    and ``cache aware`` converge while the long-standing ``norm_title`` exact-token
    contract remains unchanged for the final duplicate gate.
    """
    if not value:
        return None
    text = unicodedata.normalize("NFKC", str(value)).casefold()
    text = re.sub(r"[_\W]+", " ", text, flags=re.UNICODE)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


def normalized_title_hash(value: Any) -> str | None:
    title = resolver_norm_title(value)
    if not title:
        return None
    return hashlib.sha256(title.encode("utf-8")).hexdigest()


def safe_norm_id(value: Any) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    if not text:
        return None
    if text.casefold().startswith("openreview:"):
        return "OpenReview:" + text.split(":", 1)[1]
    try:
        return survey.norm_id(text)
    except Exception:
        return text


def arxiv_alias_from_identifier(value: Any) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    match = re.fullmatch(r"(?:DOI:)?10\.48550/arxiv\.(\d{4}\.\d{4,5})", text, re.I)
    if not match:
        return None
    return safe_norm_id("arXiv:" + match.group(1))


def field_identifier(field: str, value: Any) -> str | None:
    if not value:
        return None
    prefix = dict(IDENTIFIER_FIELDS).get(field)
    text = str(value).strip()
    if not text:
        return None
    if prefix and not text.casefold().startswith(prefix.casefold()):
        text = prefix + text
    return safe_norm_id(text)


def ids_from_url(value: Any) -> set[str]:
    if not value:
        return set()
    raw = str(value).strip()
    out: set[str] = set()
    try:
        parsed = urlparse(raw)
    except Exception:
        return out
    host = parsed.netloc.casefold()
    path = unquote(parsed.path)
    if host.endswith("arxiv.org"):
        m = re.search(r"/(?:abs|html|pdf)/([^/?#]+)", path, re.I)
        if m:
            ident = m.group(1).removesuffix(".pdf")
            normalized = safe_norm_id("arXiv:" + ident)
            if normalized:
                out.add(normalized)
    if host in {"doi.org", "www.doi.org"}:
        body = path.lstrip("/")
        normalized = safe_norm_id("DOI:" + body) if body else None
        if normalized:
            out.add(normalized)
            arxiv_alias = arxiv_alias_from_identifier(normalized)
            if arxiv_alias:
                out.add(arxiv_alias)
    return out


def norm_url(value: Any) -> str | None:
    if not value:
        return None
    raw = str(value).strip()
    if not raw:
        return None
    try:
        parsed = urlparse(raw)
    except Exception:
        return raw.casefold()
    if not parsed.scheme or not parsed.netloc:
        return raw.casefold()
    normalized = parsed._replace(
        scheme=parsed.scheme.casefold(),
        netloc=parsed.netloc.casefold(),
        query="",
        fragment="",
    )
    return urlunparse(normalized).rstrip("/")


def record_identifiers(record: dict[str, Any]) -> set[str]:
    ids: set[str] = set()
    for field, _ in IDENTIFIER_FIELDS:
        normalized = field_identifier(field, record.get(field))
        if normalized:
            ids.add(normalized)
            arxiv_alias = arxiv_alias_from_identifier(normalized)
            if arxiv_alias:
                ids.add(arxiv_alias)
    for value in record.get("identifiers") or []:
        normalized = safe_norm_id(value)
        if normalized:
            ids.add(normalized)
            arxiv_alias = arxiv_alias_from_identifier(normalized)
            if arxiv_alias:
                ids.add(arxiv_alias)
    for field in URL_FIELDS:
        ids.update(ids_from_url(record.get(field)))
    return ids


def identity_tokens(record: dict[str, Any]) -> set[str]:
    tokens = {"id:" + ident for ident in record_identifiers(record)}
    for field in URL_FIELDS:
        normalized = norm_url(record.get(field))
        if normalized:
            tokens.add("url:" + normalized)
    title = norm_title(record.get("title"))
    if title:
        tokens.add("title:" + title)
    return tokens


def primary_identity_key(record: dict[str, Any]) -> str | None:
    for field, _ in IDENTIFIER_FIELDS:
        normalized = field_identifier(field, record.get(field))
        if normalized:
            return "id:" + normalized
    for field in URL_FIELDS:
        extracted = sorted(ids_from_url(record.get(field)))
        if extracted:
            return "id:" + extracted[0]
    for field in URL_FIELDS:
        normalized = norm_url(record.get(field))
        if normalized:
            return "url:" + normalized
    title = norm_title(record.get("title"))
    return "title:" + title if title else None


def _first_author(record: dict[str, Any]) -> str | None:
    authors = record.get("authors")
    if not authors:
        authors = record.get("author")
    if isinstance(authors, str):
        first = re.split(r"\s*(?:;|\band\b)\s*", authors.strip(), maxsplit=1, flags=re.I)[0]
    elif isinstance(authors, (list, tuple)) and authors:
        value = authors[0]
        if isinstance(value, dict):
            first = str(value.get("name") or value.get("full_name") or "").strip()
        else:
            first = str(value).strip()
    else:
        return None
    if not first:
        return None
    if "," in first:
        surname = first.split(",", 1)[0]
    else:
        parts = re.findall(r"[\w'-]+", first, flags=re.UNICODE)
        surname = parts[-1] if parts else ""
    surname = re.sub(r"[^\w'-]", "", surname.casefold()).strip("-'_")
    return surname or None


def _record_year(record: dict[str, Any]) -> int | None:
    for field in ("year", "published", "publication_date", "date"):
        value = record.get(field)
        if value is None:
            continue
        match = re.search(r"\b(19\d{2}|20\d{2})\b", str(value))
        if match:
            return int(match.group(1))
    return None


def _resolver_aliases(record: dict[str, Any]) -> set[str]:
    aliases = {token for token in identity_tokens(record) if not token.startswith("title:")}
    title_hash = normalized_title_hash(record.get("title"))
    if title_hash:
        aliases.add("title-hash:" + title_hash)
    return aliases


def build_represented_resolver(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a paper-level alias graph over represented/pending paper records.

    Resolver-normalized exact titles are aliases in addition to stable identifiers and
    normalized URLs, so arXiv/DOI/OpenReview/project representations converge to one
    represented-paper node before candidate evaluation without changing legacy title tokens.
    """
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise TypeError("records must be a list of objects")

    parent = list(range(len(records)))

    def find(index: int) -> int:
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def union(left: int, right: int) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[right_root] = left_root

    alias_owner: dict[str, int] = {}
    record_aliases: list[set[str]] = []
    for index, record in enumerate(records):
        aliases = _resolver_aliases(record)
        record_aliases.append(aliases)
        for alias in sorted(aliases):
            prior = alias_owner.get(alias)
            if prior is None:
                alias_owner[alias] = index
            else:
                union(index, prior)

    components: dict[int, list[int]] = {}
    for index in range(len(records)):
        components.setdefault(find(index), []).append(index)

    papers: dict[str, dict[str, Any]] = {}
    alias_to_paper: dict[str, str] = {}
    title_hash_to_paper: dict[str, str] = {}

    for indices in components.values():
        aliases: set[str] = set()
        titles: list[str] = []
        title_hashes: list[str] = []
        first_authors: list[str] = []
        years: list[int] = []
        strong_ids: list[str] = []
        for index in indices:
            record = records[index]
            aliases.update(record_aliases[index])
            strong_ids.extend(sorted("id:" + ident for ident in record_identifiers(record)))
            title = resolver_norm_title(record.get("title"))
            if title:
                titles.append(title)
            title_hash = normalized_title_hash(record.get("title"))
            if title_hash:
                title_hashes.append(title_hash)
            author = _first_author(record)
            if author:
                first_authors.append(author)
            year = _record_year(record)
            if year:
                years.append(year)

        primary_title_hash = sorted(set(title_hashes))[0] if title_hashes else None
        if primary_title_hash:
            paper_key = "paper:title:" + primary_title_hash
        elif strong_ids:
            paper_key = "paper:" + sorted(set(strong_ids))[0]
        elif aliases:
            paper_key = "paper:alias:" + hashlib.sha256("\n".join(sorted(aliases)).encode("utf-8")).hexdigest()
        else:
            paper_key = "paper:record:" + str(min(indices))

        profile = {
            "paper_key": paper_key,
            "aliases": sorted(aliases),
            "normalized_title": sorted(set(titles))[0] if titles else None,
            "normalized_title_hash": primary_title_hash,
            "first_author": sorted(set(first_authors))[0] if first_authors else None,
            "year": sorted(set(years))[0] if years else None,
            "record_count": len(indices),
        }
        papers[paper_key] = profile
        for alias in aliases:
            alias_to_paper[alias] = paper_key
        for title_hash in set(title_hashes):
            title_hash_to_paper[title_hash] = paper_key

    return {
        "schema_version": 1,
        "papers": papers,
        "alias_to_paper": alias_to_paper,
        "title_hash_to_paper": title_hash_to_paper,
        "fuzzy_title_threshold": FUZZY_TITLE_THRESHOLD,
    }


def match_represented_paper(
    record: dict[str, Any],
    resolver: dict[str, Any],
    *,
    fuzzy_title_threshold: float = FUZZY_TITLE_THRESHOLD,
) -> dict[str, Any] | None:
    """Return a high-confidence represented-paper match for one provider record.

    Stable aliases win first. Exact resolver-normalized title hashes are deterministic
    aliases. Fuzzy title matching is deliberately restricted to records without any stable
    ID and requires both first-author and year equality, which prevents an unknown DOI/arXiv
    ID from being discarded merely because its title resembles an existing paper.
    """
    if not isinstance(record, dict) or not isinstance(resolver, dict):
        raise TypeError("record and resolver must be objects")
    papers = resolver.get("papers") if isinstance(resolver.get("papers"), dict) else {}
    alias_to_paper = resolver.get("alias_to_paper") if isinstance(resolver.get("alias_to_paper"), dict) else {}
    title_hash_to_paper = resolver.get("title_hash_to_paper") if isinstance(resolver.get("title_hash_to_paper"), dict) else {}

    stable_aliases = sorted(token for token in identity_tokens(record) if not token.startswith("title:"))
    for alias in stable_aliases:
        paper_key = alias_to_paper.get(alias)
        if paper_key in papers:
            return {"paper_key": paper_key, "match_type": "stable_alias", "matched_alias": alias}

    title_hash = normalized_title_hash(record.get("title"))
    if title_hash:
        paper_key = title_hash_to_paper.get(title_hash)
        if paper_key in papers:
            return {"paper_key": paper_key, "match_type": "exact_title_hash", "matched_alias": "title-hash:" + title_hash}

    if record_identifiers(record):
        return None
    candidate_title = resolver_norm_title(record.get("title"))
    candidate_author = _first_author(record)
    candidate_year = _record_year(record)
    if not candidate_title or not candidate_author or not candidate_year:
        return None

    best: dict[str, Any] | None = None
    for paper_key, profile in papers.items():
        if not isinstance(profile, dict):
            continue
        if profile.get("first_author") != candidate_author or profile.get("year") != candidate_year:
            continue
        represented_title = profile.get("normalized_title")
        if not represented_title:
            continue
        similarity = SequenceMatcher(None, candidate_title, str(represented_title)).ratio()
        if similarity < fuzzy_title_threshold:
            continue
        if best is None or similarity > best["title_similarity"]:
            best = {
                "paper_key": paper_key,
                "match_type": "title_fuzzy_author_year",
                "title_similarity": similarity,
                "first_author": candidate_author,
                "year": candidate_year,
            }
    return best
