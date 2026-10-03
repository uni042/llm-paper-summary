#!/usr/bin/env python3
"""Refresh candidate importance metadata without reading paper bodies.

The updater batches stable arXiv/DOI/Semantic Scholar identifiers through the
existing provider adapter, caches venue/citation metadata, and recomputes ready
Research job priority from the configurable policy. Missing metadata never drops a
candidate; it simply contributes zero until a later refresh succeeds.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
import time
from pathlib import Path
from typing import Any

import candidate_priority
import discovery_provider_adapter
import paper_identity
import reference_pool

CACHE_PATH = Path(".survey/work-queue/candidate-priority-cache.json")
FORWARD_SWEEP_PATH = Path(".survey/work-queue/forward-citation-sweep.json")
TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent"}


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: Any) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        name = tmp.name
    Path(name).replace(path)
    return True


def _now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _preferred_identifier(record: dict[str, Any]) -> str | None:
    ids = paper_identity.record_identifiers(record)
    for prefix in ("arXiv:", "DOI:", "SemanticScholar:"):
        matches = sorted(value for value in ids if value.startswith(prefix))
        if matches:
            return matches[0]
    return None


def _candidate_records(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    jobs_dir = root / ".survey/work-queue/jobs"
    if jobs_dir.is_dir():
        for path in sorted(jobs_dir.glob("*.json")):
            value = _read(path, {})
            if not isinstance(value, dict) or value.get("type") not in {"research", "audit"}:
                continue
            if value.get("status") in TERMINAL:
                continue
            rows.append(dict(value))

    pool = reference_pool.build_reference_pool(root)
    source = pool.get("candidates")
    if isinstance(source, list):
        rows.extend(dict(row) for row in source if isinstance(row, dict))

    forward = _read(root / FORWARD_SWEEP_PATH, {})
    candidates = forward.get("candidates") if isinstance(forward, dict) else None
    if isinstance(candidates, dict):
        rows.extend(dict(row) for row in candidates.values() if isinstance(row, dict))

    deduped: dict[str, dict[str, Any]] = {}
    for row in rows:
        ident = _preferred_identifier(row)
        if ident is None:
            continue
        previous = deduped.get(ident, {})
        merged = dict(previous)
        for key, value in row.items():
            if value not in (None, "", [], {}):
                merged[key] = value
        deduped[ident] = merged
    return [dict(record, _lookup_id=ident) for ident, record in sorted(deduped.items())]


def _cache_key_for(cache: dict[str, Any], identifier: str) -> str | None:
    records = cache.get("records") if isinstance(cache.get("records"), dict) else {}
    aliases = cache.get("aliases") if isinstance(cache.get("aliases"), dict) else {}
    if identifier in records:
        return identifier
    key = aliases.get(identifier)
    return key if isinstance(key, str) and key in records else None


def _is_due(
    row: dict[str, Any],
    cache: dict[str, Any],
    *,
    now: dt.datetime,
    config: dict[str, Any],
) -> bool:
    identifier = str(row["_lookup_id"])
    key = _cache_key_for(cache, identifier)
    cached = cache.get("records", {}).get(key) if key else None
    if not isinstance(cached, dict):
        failures = cache.get("lookup_failures") if isinstance(cache.get("lookup_failures"), dict) else {}
        failure = failures.get(identifier)
        if isinstance(failure, dict):
            failed_at = _parse_time(failure.get("checked_at"))
            cache_policy = config.get("cache") if isinstance(config.get("cache"), dict) else {}
            failure_ttl = int(cache_policy.get("failure_ttl_hours", 168) or 168)
            if failed_at is not None and (now - failed_at).total_seconds() < failure_ttl * 3600:
                return False
        return True
    checked = _parse_time(cached.get("citation_count_checked_at"))
    if checked is None:
        return True
    scored = candidate_priority.score_record(cached, repo_root=Path("."), now=now, config=config)
    cache_policy = config.get("cache") if isinstance(config.get("cache"), dict) else {}
    ttl_hours = (
        int(cache_policy.get("fresh_ttl_hours", 48) or 48)
        if scored.get("is_fresh")
        else int(cache_policy.get("default_ttl_hours", 168) or 168)
    )
    return (now - checked).total_seconds() >= ttl_hours * 3600


def _store_found(
    cache: dict[str, Any],
    requested_id: str,
    record: dict[str, Any],
    *,
    checked_at: str,
) -> None:
    records = cache.setdefault("records", {})
    aliases = cache.setdefault("aliases", {})
    primary = paper_identity.safe_norm_id(record.get("canonical_id")) or requested_id
    prior_key = _cache_key_for(cache, requested_id)
    prior = records.get(prior_key, {}) if prior_key else {}
    merged = dict(prior) if isinstance(prior, dict) else {}
    merged.update(record)
    merged["citation_count_checked_at"] = checked_at
    merged.setdefault("citation_count_source", "semantic_scholar")
    records[primary] = merged
    if prior_key and prior_key != primary:
        records.pop(prior_key, None)

    ids = set(paper_identity.record_identifiers(merged))
    ids.add(requested_id)
    ids.add(primary)
    for alias in ids:
        aliases[alias] = primary


def _refresh_ready_jobs(root: Path, cache: dict[str, Any], config: dict[str, Any], now: dt.datetime) -> int:
    changed = 0
    jobs_dir = root / ".survey/work-queue/jobs"
    if not jobs_dir.is_dir():
        return 0
    for path in sorted(jobs_dir.glob("*.json")):
        job = _read(path, {})
        if not isinstance(job, dict) or job.get("type") != "research" or job.get("status") != "ready":
            continue
        enriched = candidate_priority.merge_cached_metadata(job, cache)
        scored = candidate_priority.apply_priority(enriched, repo_root=root, now=now, config=config)
        new_job = dict(job)
        for field in (
            "published", "year", "venue", "citation_count", "citation_count_source",
            "citation_count_checked_at", "semantic_scholar_id",
        ):
            if scored.get(field) not in (None, ""):
                new_job[field] = scored[field]
        new_job["priority"] = scored["priority"]
        new_job["priority_breakdown"] = scored["priority_breakdown"]
        if new_job != job:
            _write(path, new_job)
            changed += 1
    return changed


def refresh(root: Path, *, max_papers: int | None = None, sleep_fn=time.sleep) -> dict[str, Any]:
    root = Path(root).resolve()
    config = candidate_priority.load_config(root)
    cache_policy = config.get("cache") if isinstance(config.get("cache"), dict) else {}
    if max_papers is None:
        max_papers = int(cache_policy.get("max_lookup_papers_per_run", 600) or 600)
    batch_size = min(
        int(cache_policy.get("max_lookup_batch", 100) or 100),
        discovery_provider_adapter.EXPLICIT_ID_MAX_ITEMS,
    )
    spacing = max(float(cache_policy.get("request_spacing_seconds", 2) or 0), 0.0)
    now = _now()

    cache = candidate_priority.load_cache(root)
    cache.setdefault("schema_version", 1)
    cache.setdefault("records", {})
    cache.setdefault("aliases", {})
    failures = cache.setdefault("lookup_failures", {})

    rows = _candidate_records(root)
    due = [row for row in rows if _is_due(row, cache, now=now, config=config)]
    selected = due[:max(max_papers, 0)]
    found = unresolved = errors = 0

    for start in range(0, len(selected), max(batch_size, 1)):
        batch = selected[start:start + batch_size]
        identifiers = [str(row["_lookup_id"]) for row in batch]
        outcomes = discovery_provider_adapter.lookup_identifiers(identifiers)
        checked_at = now.replace(microsecond=0).isoformat()
        for outcome in outcomes:
            requested_id = str(outcome.get("requested_id") or "")
            status = outcome.get("status")
            record = outcome.get("record")
            if status == "found" and isinstance(record, dict):
                _store_found(cache, requested_id, record, checked_at=checked_at)
                failures.pop(requested_id, None)
                found += 1
            elif status == "unresolved":
                failures[requested_id] = {
                    "status": "unresolved",
                    "checked_at": checked_at,
                    "error": outcome.get("error"),
                }
                unresolved += 1
            else:
                failures[requested_id] = {
                    "status": "error",
                    "checked_at": checked_at,
                    "error": outcome.get("error"),
                }
                errors += 1
        if start + batch_size < len(selected) and spacing:
            sleep_fn(spacing)

    cache["schema_version"] = 1
    cache["policy"] = config.get("policy_name")
    cache["updated_at"] = now.replace(microsecond=0).isoformat()
    cache["candidate_count_seen"] = len(rows)
    cache["due_count_before_run"] = len(due)
    cache_changed = _write(root / CACHE_PATH, cache)
    jobs_changed = _refresh_ready_jobs(root, cache, config, now)
    return {
        "candidate_count_seen": len(rows),
        "due_count_before_run": len(due),
        "selected_count": len(selected),
        "found": found,
        "unresolved": unresolved,
        "errors": errors,
        "cache_changed": cache_changed,
        "research_jobs_reprioritized": jobs_changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-papers", type=int, default=None)
    args = parser.parse_args()
    if args.max_papers is not None and args.max_papers < 0:
        parser.error("--max-papers must be >= 0")
    print(json.dumps(refresh(args.repo_root, max_papers=args.max_papers), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
