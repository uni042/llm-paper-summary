#!/usr/bin/env python3
"""Configurable importance scoring for Discovery and Research candidates.

Priority is deliberately independent from relevance. A low score never rejects a
paper; it only moves the paper later in the worklist. The machine-readable policy
lives in .survey/config/candidate-priority.json so weights can change without
rewriting queue code.
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(".survey/config/candidate-priority.json")
CACHE_PATH = Path(".survey/work-queue/candidate-priority-cache.json")


def _read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def load_config(repo_root: Path) -> dict[str, Any]:
    path = Path(repo_root) / CONFIG_PATH
    value = _read_json(path, None)
    # Unit/maintenance callers sometimes operate on a temporary repository root.
    # In that case reuse the policy shipped beside this module instead of reviving
    # the retired hard-coded scoring formula.
    if value is None:
        module_root = Path(__file__).resolve().parents[2]
        value = _read_json(module_root / CONFIG_PATH, None)
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        raise ValueError(f"invalid candidate priority config: {CONFIG_PATH}")
    return value


def load_cache(repo_root: Path) -> dict[str, Any]:
    value = _read_json(Path(repo_root) / CACHE_PATH, {})
    if not isinstance(value, dict):
        return {"schema_version": 1, "records": {}, "aliases": {}}
    records = value.get("records")
    aliases = value.get("aliases")
    if not isinstance(records, dict) or not isinstance(aliases, dict):
        return {"schema_version": 1, "records": {}, "aliases": {}}
    return value


def _parse_published(record: dict[str, Any]) -> tuple[dt.date | None, str | None]:
    raw = record.get("published") or record.get("publication_date") or record.get("publicationDate")
    if isinstance(raw, dt.datetime):
        return raw.date(), "day"
    if isinstance(raw, dt.date):
        return raw, "day"
    text = str(raw or "").strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
        try:
            return dt.date.fromisoformat(text), "day"
        except ValueError:
            return None, None
    if re.fullmatch(r"\d{4}-\d{2}", text):
        try:
            year, month = map(int, text.split("-"))
            return dt.date(year, month, 15), "month"
        except ValueError:
            return None, None
    if re.fullmatch(r"\d{4}", text):
        try:
            return dt.date(int(text), 7, 1), "year"
        except ValueError:
            return None, None
    year = record.get("year")
    if isinstance(year, int) and 1900 <= year <= 2200:
        return dt.date(year, 7, 1), "year"
    return None, None


def _venue_text(record: dict[str, Any]) -> str:
    values = []
    for field in ("venue", "publication", "publication_venue", "conference", "booktitle"):
        value = record.get(field)
        if isinstance(value, str) and value.strip():
            values.append(value.strip())
    return " | ".join(values)


def _venue_matches(text: str, aliases: list[Any]) -> str | None:
    if not text:
        return None
    folded = text.casefold()
    for raw in aliases:
        alias = str(raw or "").strip()
        if not alias:
            continue
        # Short acronyms must match as a token; otherwise "SC" would match "Science".
        if len(alias) <= 5 and re.fullmatch(r"[A-Za-z0-9]+", alias):
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(alias) + r"(?![A-Za-z0-9])", text, re.I):
                return alias
        elif alias.casefold() in folded:
            return alias
    return None


def citation_count(record: dict[str, Any]) -> int:
    for field in ("citation_count", "citationCount", "cited_by_count"):
        value = record.get(field)
        if isinstance(value, bool):
            continue
        try:
            return max(int(value), 0)
        except (TypeError, ValueError):
            continue
    return 0


def score_record(
    record: dict[str, Any],
    *,
    repo_root: Path,
    now: dt.datetime | dt.date | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    config = config or load_config(repo_root)
    if now is None:
        today = dt.datetime.now(dt.timezone.utc).date()
    elif isinstance(now, dt.datetime):
        today = now.astimezone(dt.timezone.utc).date() if now.tzinfo else now.date()
    else:
        today = now

    freshness = config.get("freshness") if isinstance(config.get("freshness"), dict) else {}
    venue_policy = config.get("prestigious_venue") if isinstance(config.get("prestigious_venue"), dict) else {}
    citation_policy = config.get("citations") if isinstance(config.get("citations"), dict) else {}

    published, precision = _parse_published(record)
    age_days = (today - published).days if published is not None else None
    max_age = int(freshness.get("max_age_days", 0) or 0)
    year_only_ok = freshness.get("year_only_is_fresh") is True
    is_fresh = bool(
        freshness.get("enabled", True)
        and published is not None
        and age_days is not None
        and 0 <= age_days <= max_age
        and (precision != "year" or year_only_ok)
    )
    freshness_score = int(freshness.get("score", 0) or 0) if is_fresh else 0

    venue_text = _venue_text(record)
    aliases = venue_policy.get("aliases") if isinstance(venue_policy.get("aliases"), list) else []
    matched_venue = _venue_matches(venue_text, aliases) if venue_policy.get("enabled", True) else None
    venue_score = int(venue_policy.get("score", 0) or 0) if matched_venue else 0

    count = citation_count(record)
    per_citation = float(citation_policy.get("score_per_citation", 0) or 0)
    raw_citation_score = max(count * per_citation, 0.0) if citation_policy.get("enabled", True) else 0.0
    cap = citation_policy.get("max_score")
    if cap is not None:
        raw_citation_score = min(raw_citation_score, max(float(cap), 0.0))
    citation_score = int(round(raw_citation_score))

    fallback = int(config.get("fallback_priority", 0) or 0)
    total = max(fallback + freshness_score + venue_score + citation_score, 0)
    return {
        "policy": str(config.get("policy_name") or "candidate-priority"),
        "freshness": freshness_score,
        "prestigious_venue": venue_score,
        "citations": citation_score,
        "citation_count": count,
        "total": total,
        "is_fresh": is_fresh,
        "freshness_age_days": age_days,
        "matched_prestigious_venue": matched_venue,
    }


def apply_priority(
    record: dict[str, Any],
    *,
    repo_root: Path,
    now: dt.datetime | dt.date | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out = dict(record)
    breakdown = score_record(out, repo_root=repo_root, now=now, config=config)
    out["priority"] = breakdown["total"]
    out["priority_breakdown"] = breakdown
    return out


def merge_cached_metadata(record: dict[str, Any], cache: dict[str, Any]) -> dict[str, Any]:
    out = dict(record)
    aliases = cache.get("aliases") if isinstance(cache.get("aliases"), dict) else {}
    records = cache.get("records") if isinstance(cache.get("records"), dict) else {}

    probes = []
    for field in ("canonical_id", "arxiv_id", "doi", "openreview_id", "semantic_scholar_id"):
        value = out.get(field)
        if not value:
            continue
        if field == "arxiv_id":
            probes.append("arXiv:" + str(value))
        elif field == "doi":
            probes.append("DOI:" + str(value))
        elif field == "openreview_id":
            probes.append("OpenReview:" + str(value))
        elif field == "semantic_scholar_id":
            probes.append("SemanticScholar:" + str(value))
        else:
            probes.append(str(value))
    identities = out.get("identity_tokens")
    if isinstance(identities, list):
        probes.extend(str(value) for value in identities if value)
    identifiers = out.get("identifiers")
    if isinstance(identifiers, list):
        probes.extend(str(value) for value in identifiers if value)

    key = None
    for probe in probes:
        if probe in records:
            key = probe
            break
        if probe in aliases and aliases[probe] in records:
            key = aliases[probe]
            break
    cached = records.get(key) if key else None
    if not isinstance(cached, dict):
        return out
    for field in (
        "published", "year", "venue", "citation_count", "citation_count_source",
        "citation_count_checked_at", "semantic_scholar_id", "title", "source_url",
    ):
        if cached.get(field) not in (None, ""):
            out[field] = cached[field]
    return out
