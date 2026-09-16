#!/usr/bin/env python3
"""Shared paper-identity normalization for discovery and final duplicate guards."""
from __future__ import annotations

import re
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


def norm_title(value: Any) -> str | None:
    if not value:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip().casefold()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text or None


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
    for value in record.get("identifiers") or []:
        normalized = safe_norm_id(value)
        if normalized:
            ids.add(normalized)
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
