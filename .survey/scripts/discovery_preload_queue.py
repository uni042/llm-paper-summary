#!/usr/bin/env python3
"""Durable Discovery preload queue.

The queue pre-runs schema-v3 Discovery prechecks in the background, then lets a
real worker adopt one preloaded window. Adoption never reuses the preload proof
as-is: process_discovery_precheck.py re-filters the cached records against the
current identity snapshot and emits a fresh run-specific precheck result.

Durable state is split into immutable entry descriptors plus small claim and
ingested markers so concurrent workers never need to rewrite one shared queue
file.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

import worker_identity
from record_bank_config import BANK_IDS, BANK_ROOTS, bank_for_sequence

QUEUE_ROOT = Path(".survey/work-queue/discovery-preload")
ENTRIES = QUEUE_ROOT / "entries"
CLAIMS = QUEUE_ROOT / "claims"
INGESTED = QUEUE_ROOT / "ingested"
PRECHECK_REQUESTS = Path(".survey/work-queue/discovery-precheck/requests")
PRECHECK_RESULTS = Path(".survey/work-queue/discovery-precheck/results")
DISCOVERY_STATE = Path(".survey/work-queue/discovery-state.json")

DEFAULT_TARGET = 32
DEFAULT_MAX_NEW = 8
DEFAULT_TARGET_UNSEEN = 20
DEFAULT_PAGE_SIZE = 20
DEFAULT_MAX_PAGES = 25
CLAIM_LEASE_SECONDS = 90 * 60
REFRESH_BUCKET_SECONDS = 6 * 60 * 60
PRELOAD_MAX_AGE_SECONDS = REFRESH_BUCKET_SECONDS
ARTIFACT_RETENTION_SECONDS = 24 * 60 * 60
MAX_FAILED_ATTEMPTS_PER_SOURCE_BUCKET = 2


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _parse_time(value: Any) -> dt.datetime | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        parsed = dt.datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(dt.timezone.utc)


def _safe_fragment(value: str) -> str:
    out = "".join(ch if ch.isalnum() or ch in "._-" else "-" for ch in value)
    return out[:80].strip("-") or "discovery"


def _source_key(provider: str, source_url: str) -> str:
    raw = f"{provider.strip().casefold()}|{source_url.strip()}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:20]


def _direction(provider: str, source_url: str, explicit: Any = None) -> str:
    value = str(explicit or "").strip().casefold()
    if value in {"backward", "forward", "normal"}:
        return value
    provider_key = provider.strip().casefold()
    if provider_key in {
        "repository_references",
        "repository_reference_pool",
        "openalex_references",
        "open_alex_references",
    }:
        return "backward"
    try:
        parsed = urlparse(source_url)
    except ValueError:
        return "normal"
    path = parsed.path.rstrip("/").casefold()
    if path.endswith("/references"):
        return "backward"
    if path.endswith("/citations"):
        return "forward"
    if provider_key in {"openalex", "open_alex"} and parsed.netloc.casefold() == "api.openalex.org":
        filters = ",".join(parse_qs(parsed.query, keep_blank_values=True).get("filter", []))
        if any(part.strip().casefold().startswith("cites:") for part in filters.split(",")):
            return "forward"
    return "normal"


def _refresh_bucket(now: dt.datetime) -> int:
    return int(now.timestamp()) // REFRESH_BUCKET_SECONDS


def _result_path(entry: dict[str, Any]) -> Path:
    return PRECHECK_RESULTS / f"{entry['precheck_request_id']}.json"


def _claim_path(preload_id: str) -> Path:
    return CLAIMS / f"{preload_id}.json"


def _ingested_path(preload_id: str) -> Path:
    return INGESTED / f"{preload_id}.json"


def _active_claim(root: Path, preload_id: str, now: dt.datetime) -> dict[str, Any] | None:
    claim = _read(root / _claim_path(preload_id), {})
    if not isinstance(claim, dict) or not claim:
        return None
    expires = _parse_time(claim.get("lease_expires_at"))
    if expires is None or expires <= now:
        return None
    return claim


def _status(root: Path, entry: dict[str, Any], now: dt.datetime) -> str:
    preload_id = str(entry.get("preload_id") or "")
    if not preload_id:
        return "INVALID"
    if (root / _ingested_path(preload_id)).is_file():
        return "INGESTED"
    if _active_claim(root, preload_id, now) is not None:
        return "CLAIMED"
    created_at = _parse_time(entry.get("created_at"))
    if created_at is None:
        return "INVALID"
    if (now - created_at).total_seconds() > PRELOAD_MAX_AGE_SECONDS:
        return "STALE"
    result_path = root / _result_path(entry)
    result = _read(result_path, {})
    if isinstance(result, dict) and result:
        if result.get("ok") is True and result.get("evaluation_allowed") is True:
            return "PRECHECKED"
        # A persisted terminal failure is not pending stock. It must not count
        # toward the warm target or be offered to a real worker.
        return "FAILED"
    request = root / PRECHECK_REQUESTS / f"{entry.get('precheck_request_id')}.json"
    if request.is_file():
        return "READY"
    return "INVALID"


def _source_specs(root: Path) -> list[dict[str, Any]]:
    state = _read(root / DISCOVERY_STATE, {}) or {}
    history = state.get("history") if isinstance(state.get("history"), list) else []
    specs: dict[str, dict[str, Any]] = {}

    def add(
        provider: str,
        source_url: str,
        direction: str,
        *,
        axis: str,
        seed_canonical_id: str | None = None,
        score: float = 0.0,
    ) -> None:
        provider = str(provider or "").strip()
        source_url = str(source_url or "").strip()
        if not provider or not source_url:
            return
        key = _source_key(provider, source_url)
        prior = specs.get(key)
        row = {
            "source_key": key,
            "provider": provider,
            "source_url": source_url,
            "citation_direction": direction,
            "axis": axis or f"preload-{direction}",
            "seed_canonical_id": seed_canonical_id,
            "score": float(score),
        }
        if prior is None or float(row["score"]) > float(prior.get("score", 0.0)):
            specs[key] = row

    add(
        "repository_references",
        "repository://structured-references",
        "backward",
        axis="preload-backward-structured-references",
        score=10_000.0,
    )

    for recency, row in enumerate(reversed(history)):
        if not isinstance(row, dict):
            continue
        provider = str(row.get("provider") or "").strip()
        source_url = str(row.get("source_url") or "").strip()
        if not provider or not source_url:
            continue
        direction = _direction(provider, source_url, row.get("citation_direction"))
        accepted = row.get("accepted_count", 0)
        novel = row.get("novel_candidate_count", row.get("candidate_count", 0))
        accepted_n = float(accepted) if isinstance(accepted, (int, float)) and not isinstance(accepted, bool) else 0.0
        novel_n = float(novel) if isinstance(novel, (int, float)) and not isinstance(novel, bool) else 0.0
        recent_bonus = max(200.0 - float(recency), 0.0) / 100.0
        # Citation sources dominate. Productive normal-search sources remain warm only
        # as a gap-fill reserve after a worker has completed both citation directions.
        route_bonus = 100.0 if direction in {"backward", "forward"} else 0.0
        score = route_bonus + 10.0 * accepted_n + novel_n + recent_bonus
        if direction == "normal" and accepted_n <= 0:
            continue
        add(
            provider,
            source_url,
            direction,
            axis=str(row.get("axis") or f"preload-{direction}"),
            seed_canonical_id=str(row.get("seed_canonical_id") or "").strip() or None,
            score=score,
        )

    values = list(specs.values())
    direction_rank = {"backward": 0, "forward": 1, "normal": 2}
    values.sort(
        key=lambda row: (
            direction_rank.get(str(row.get("citation_direction")), 9),
            -float(row.get("score", 0.0)),
            str(row.get("source_key")),
        )
    )
    return values


def _entries(root: Path) -> list[dict[str, Any]]:
    folder = root / ENTRIES
    if not folder.is_dir():
        return []
    out: list[dict[str, Any]] = []
    for path in sorted(folder.glob("*.json")):
        value = _read(path, {})
        if isinstance(value, dict) and value.get("preload_id") == path.stem:
            out.append(value)
    return out


def _expire_stale_claims(root: Path, now: dt.datetime) -> list[str]:
    folder = root / CLAIMS
    expired: list[str] = []
    if not folder.is_dir():
        return expired
    for path in folder.glob("*.json"):
        claim = _read(path, {})
        expires = _parse_time(claim.get("lease_expires_at")) if isinstance(claim, dict) else None
        if expires is not None and expires > now:
            continue
        preload_id = path.stem
        try:
            path.unlink()
            expired.append(preload_id)
        except OSError:
            pass
    return expired


def _gc_old_artifacts(root: Path, now: dt.datetime) -> list[str]:
    """Remove preload-only transport artifacts after their bounded retention window.

    A real run-specific precheck result is the durable submission proof. Background
    preload seed requests/results are acceleration artifacts and may be removed once
    they are old enough that their refresh bucket cannot be reused.
    """
    removed: list[str] = []
    for entry in _entries(root):
        preload_id = str(entry.get("preload_id") or "")
        created_at = _parse_time(entry.get("created_at"))
        if not preload_id or created_at is None:
            continue
        if (now - created_at).total_seconds() <= ARTIFACT_RETENTION_SECONDS:
            continue
        if _active_claim(root, preload_id, now) is not None:
            continue
        request_id = str(entry.get("precheck_request_id") or "")
        paths = [
            root / ENTRIES / f"{preload_id}.json",
            root / CLAIMS / f"{preload_id}.json",
            root / INGESTED / f"{preload_id}.json",
        ]
        if request_id:
            paths.extend(
                [
                    root / PRECHECK_REQUESTS / f"{request_id}.json",
                    root / PRECHECK_RESULTS / f"{request_id}.json",
                ]
            )
        for path in paths:
            try:
                path.unlink()
            except FileNotFoundError:
                pass
        removed.append(preload_id)
    return removed


def _latest_for_source(
    root: Path,
    entries: list[dict[str, Any]],
    source_key: str,
    bucket: int,
) -> dict[str, Any] | None:
    matches = [
        row
        for row in entries
        if row.get("source_key") == source_key and int(row.get("refresh_bucket", -1)) == bucket
    ]
    if not matches:
        return None
    matches.sort(key=lambda row: int(row.get("sequence", 0)))
    return matches[-1]


def _failed_attempts_for_source_bucket(
    root: Path,
    entries: list[dict[str, Any]],
    source_key: str,
    bucket: int,
) -> int:
    now = _utcnow()
    return sum(
        1
        for row in entries
        if str(row.get("source_key") or "") == source_key
        and int(row.get("refresh_bucket", -1)) == bucket
        and _status(root, row, now) == "FAILED"
    )


def _next_cursor_for_entry(root: Path, entry: dict[str, Any]) -> tuple[bool, str | None]:
    result = _read(root / _result_path(entry), {})
    if not isinstance(result, dict) or not result:
        return False, None
    if result.get("ok") is not True:
        # Retry a failed fixed-source window with a fresh immutable preload
        # identity rather than leaving that source dead until the next bucket.
        cursor = entry.get("initial_cursor")
        return True, cursor if isinstance(cursor, str) else None
    if result.get("provider_exhausted") is True:
        return False, None
    cursor = result.get("next_cursor")
    if cursor is None:
        return False, None
    if not isinstance(cursor, str):
        return False, None
    return True, cursor


def _make_entry(
    spec: dict[str, Any],
    *,
    bucket: int,
    sequence: int,
    initial_cursor: str | None,
    stock_bank: str,
    now: dt.datetime,
) -> dict[str, Any]:
    source_key = str(spec["source_key"])
    token = json.dumps(
        {
            "source_key": source_key,
            "bucket": bucket,
            "sequence": sequence,
            "initial_cursor": initial_cursor,
            "stock_bank": stock_bank,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()[:20]
    preload_id = f"preload-{digest}"
    request_id = f"preload-{digest}"
    return {
        "schema_version": 1,
        "preload_id": preload_id,
        "source_key": source_key,
        "provider": spec["provider"],
        "source_url": spec["source_url"],
        "citation_direction": spec["citation_direction"],
        "axis": spec["axis"],
        "seed_canonical_id": spec.get("seed_canonical_id"),
        "refresh_bucket": bucket,
        "sequence": sequence,
        "initial_cursor": initial_cursor,
        "target_unseen": DEFAULT_TARGET_UNSEEN,
        "page_size": DEFAULT_PAGE_SIZE,
        "max_pages": DEFAULT_MAX_PAGES,
        "precheck_request_id": request_id,
        "stock_bank": stock_bank,
        "stock_lane": "discovery",
        "created_at": now.isoformat(),
    }


def _request_for_entry(entry: dict[str, Any]) -> dict[str, Any]:
    preload_id = str(entry["preload_id"])
    return {
        "schema_version": 3,
        "operation": "precheck_discovery_candidates",
        "request_id": entry["precheck_request_id"],
        "collector_id": _safe_fragment(f"discovery-preload-{entry['citation_direction']}"),
        "run_key": f"preload:{preload_id}",
        "axis": entry["axis"],
        "provider": entry["provider"],
        "source_url": entry["source_url"],
        "target_unseen": entry["target_unseen"],
        "page_size": entry["page_size"],
        "max_pages": entry["max_pages"],
        "initial_cursor": entry.get("initial_cursor"),
        "preload_seed": True,
        "preload_id": preload_id,
        "stock_bank": entry.get("stock_bank"),
        "stock_lane": "discovery",
    }


def _stock_bank_targets(target: int) -> tuple[str, ...]:
    """Return the canonical banks that must carry one Discovery window."""
    target = max(int(target), 0)
    return BANK_IDS[: min(target, len(BANK_IDS))]


def _direction_floor_targets(target: int) -> dict[str, int]:
    """Reserve citation stock plus a small normal-search fallback buffer."""
    target = max(int(target), 0)
    if target <= 1:
        return {"backward": target, "forward": 0, "normal": 0}
    citation_floor = max(target // 3, 1)
    normal_floor = target // 8
    return {
        "backward": citation_floor,
        "forward": citation_floor,
        "normal": normal_floor,
    }


def _prioritize_specs(
    specs: list[dict[str, Any]],
    deficits: dict[str, int],
) -> list[dict[str, Any]]:
    """Interleave citation directions while either reserved floor is deficient."""
    groups = {
        direction: [row for row in specs if row.get("citation_direction") == direction]
        for direction in ("backward", "forward", "normal")
    }
    prioritized: list[dict[str, Any]] = []
    used: set[str] = set()
    max_len = max((len(rows) for rows in groups.values()), default=0)
    for index in range(max_len):
        for direction in ("backward", "forward", "normal"):
            if deficits.get(direction, 0) <= 0:
                continue
            rows = groups[direction]
            if index >= len(rows):
                continue
            row = rows[index]
            prioritized.append(row)
            used.add(str(row.get("source_key") or ""))
    prioritized.extend(
        row for row in specs if str(row.get("source_key") or "") not in used
    )
    return prioritized


def top_up(root: Path, *, target: int = DEFAULT_TARGET, max_new: int = DEFAULT_MAX_NEW) -> dict[str, Any]:
    root = root.resolve()
    now = _utcnow()
    expired = _expire_stale_claims(root, now)
    garbage_collected = _gc_old_artifacts(root, now)
    entries = _entries(root)
    available_rows = [
        row for row in entries if _status(root, row, now) in {"READY", "PRECHECKED"}
    ]
    available = len(available_rows)
    target_banks = _stock_bank_targets(target)
    bank_available = {
        bank: sum(
            1
            for row in available_rows
            if str(row.get("stock_bank") or "").lower() == bank
        )
        for bank in BANK_IDS
    }
    bank_deficits = [bank for bank in target_banks if bank_available.get(bank, 0) <= 0]
    direction_available = {
        direction: sum(
            1
            for row in available_rows
            if str(row.get("citation_direction") or "") == direction
        )
        for direction in ("backward", "forward", "normal")
    }
    direction_targets = _direction_floor_targets(target)
    direction_deficits = {
        direction: max(direction_targets.get(direction, 0) - direction_available.get(direction, 0), 0)
        for direction in ("backward", "forward", "normal")
    }
    needed = max(
        target - available,
        sum(direction_deficits.values()),
        len(bank_deficits),
        0,
    )
    budget = min(needed, max(max_new, 0))
    if budget == 0:
        return {
            "target": target,
            "available": available,
            "direction_available": direction_available,
            "direction_targets": direction_targets,
            "bank_available": bank_available,
            "bank_target": len(target_banks),
            "bank_deficits": bank_deficits,
            "created": [],
            "expired_claims": expired,
            "garbage_collected": garbage_collected,
        }

    bucket = _refresh_bucket(now)
    specs = _prioritize_specs(_source_specs(root), direction_deficits)
    created: list[str] = []
    created_bank_counts = {bank: 0 for bank in BANK_IDS}
    missing_banks = list(bank_deficits)
    made_progress = True

    while len(created) < budget and made_progress:
        made_progress = False
        for spec in specs:
            if len(created) >= budget:
                break
            direction = str(spec.get("citation_direction") or "")
            base_slots_remaining = max(target - (available + len(created)), 0)
            if (
                base_slots_remaining <= 0
                and direction_deficits.get(direction, 0) <= 0
                and not missing_banks
            ):
                # Once the total target is full, only create deliberate
                # backward/forward floor repairs. Never grow the queue in an
                # unrelated direction just because another direction is short.
                continue
            source_key = str(spec["source_key"])
            latest = _latest_for_source(root, entries, source_key, bucket)
            if latest is None:
                sequence = 0
                initial_cursor = None
            else:
                latest_status = _status(root, latest, now)
                if (
                    latest_status == "FAILED"
                    and _failed_attempts_for_source_bucket(root, entries, source_key, bucket)
                    >= MAX_FAILED_ATTEMPTS_PER_SOURCE_BUCKET
                ):
                    continue
                can_continue, next_cursor = _next_cursor_for_entry(root, latest)
                if not can_continue:
                    continue
                sequence = int(latest.get("sequence", 0)) + 1
                initial_cursor = next_cursor

            if missing_banks:
                stock_bank = missing_banks.pop(0)
            else:
                # Once every bank has a Discovery window, spread any deliberate
                # overfill evenly in the same canonical bank order.
                stock_bank = min(
                    BANK_IDS,
                    key=lambda bank: (
                        bank_available.get(bank, 0) + created_bank_counts.get(bank, 0),
                        BANK_IDS.index(bank),
                    ),
                )
            entry = _make_entry(
                spec,
                bucket=bucket,
                sequence=sequence,
                initial_cursor=initial_cursor,
                stock_bank=stock_bank,
                now=now,
            )
            entry_path = root / ENTRIES / f"{entry['preload_id']}.json"
            request_path = root / PRECHECK_REQUESTS / f"{entry['precheck_request_id']}.json"
            if entry_path.exists() or request_path.exists():
                continue
            _write(entry_path, entry)
            _write(request_path, _request_for_entry(entry))
            entries.append(entry)
            created.append(entry["preload_id"])
            created_bank_counts[stock_bank] = created_bank_counts.get(stock_bank, 0) + 1
            if direction_deficits.get(direction, 0) > 0:
                direction_deficits[direction] -= 1
            made_progress = True

    return {
        "target": target,
        "available_before": available,
        "direction_available_before": direction_available,
        "direction_targets": direction_targets,
        "bank_available_before": bank_available,
        "bank_target": len(target_banks),
        "bank_deficits_before": bank_deficits,
        "created": created,
        "created_count": len(created),
        "expired_claims": expired,
        "garbage_collected": garbage_collected,
    }


def available_preloads(
    root: Path,
    *,
    direction: str | None = None,
    limit: int = 32,
) -> list[dict[str, Any]]:
    root = root.resolve()
    now = _utcnow()
    # Availability reads are intentionally side-effect free. Expired claims are
    # treated as unclaimed by _active_claim(); top_up/maintenance removes their
    # stale marker files.
    rows: list[dict[str, Any]] = []
    for entry in _entries(root):
        if _status(root, entry, now) != "PRECHECKED":
            continue
        if direction and str(entry.get("citation_direction") or "") != direction:
            continue
        result = _read(root / _result_path(entry), {})
        if not isinstance(result, dict) or result.get("ok") is not True:
            continue
        rows.append(
            {
                "preload_id": entry["preload_id"],
                "citation_direction": entry.get("citation_direction"),
                "provider": entry.get("provider"),
                "source_url": entry.get("source_url"),
                "axis": entry.get("axis"),
                "seed_canonical_id": entry.get("seed_canonical_id"),
                "initial_cursor": entry.get("initial_cursor"),
                "target_unseen": entry.get("target_unseen"),
                "page_size": entry.get("page_size"),
                "max_pages": entry.get("max_pages"),
                "preload_result_path": _result_path(entry).as_posix(),
                "preload_unseen_result_count": result.get("unseen_result_count"),
                "stock_bank": entry.get("stock_bank"),
                "stock_lane": "discovery",
                "created_at": entry.get("created_at"),
            }
        )
    rows.sort(key=lambda row: (str(row.get("created_at") or ""), str(row.get("preload_id") or "")))
    return rows[: max(limit, 0)]


def pick_available(root: Path, *, direction: str | None) -> dict[str, Any] | None:
    rows = available_preloads(root, direction=direction, limit=1)
    return rows[0] if rows else None


def claim_and_load(root: Path, request: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    root = root.resolve()
    preload_id = str(request.get("preload_id") or "").strip()
    worker_id = str(request.get("worker_id") or "").strip()
    run_key = str(request.get("run_key") or "").strip()
    request_id = str(request.get("request_id") or "").strip()
    if not preload_id:
        raise ValueError("preload_id is required")
    if not worker_id:
        raise ValueError("worker_id is required when adopting a Discovery preload")
    if not worker_identity.is_supported_worker_id(worker_id):
        raise ValueError("worker_id must be scheduled-chat-00, scheduled-chat-30, or worker-N")
    if not run_key or run_key.startswith("preload:"):
        raise ValueError("a real run_key is required when adopting a Discovery preload")
    entry_path = root / ENTRIES / f"{preload_id}.json"
    entry = _read(entry_path, {})
    if not isinstance(entry, dict) or entry.get("preload_id") != preload_id:
        raise ValueError("Discovery preload entry does not exist")
    if (root / _ingested_path(preload_id)).is_file():
        raise ValueError("Discovery preload entry is already ingested")

    for field in ("provider", "source_url", "axis"):
        if str(request.get(field) or "") != str(entry.get(field) or ""):
            raise ValueError(f"Discovery preload {field} does not match the entry")
    entry_stock_bank = str(entry.get("stock_bank") or "").lower()
    if entry_stock_bank in BANK_ROOTS:
        request_stock_bank = str(request.get("stock_bank") or "").lower()
        if request_stock_bank != entry_stock_bank:
            raise ValueError("Discovery preload stock_bank does not match the entry")
    if request.get("initial_cursor") != entry.get("initial_cursor"):
        raise ValueError("Discovery preload initial_cursor does not match the entry")
    if int(request.get("page_size") or 0) != int(entry.get("page_size") or 0):
        raise ValueError("Discovery preload page_size does not match the entry")

    preload_result = _read(root / _result_path(entry), {})
    if (
        not isinstance(preload_result, dict)
        or preload_result.get("ok") is not True
        or preload_result.get("evaluation_allowed") is not True
    ):
        raise ValueError("Discovery preload result is not ready")
    if str(preload_result.get("run_key") or "") != f"preload:{preload_id}":
        raise ValueError("Discovery preload result identity is inconsistent")

    now = _utcnow()
    claim_path = root / _claim_path(preload_id)
    current = _active_claim(root, preload_id, now)
    if current is not None:
        same = (
            str(current.get("worker_id") or "") == worker_id
            and str(current.get("run_key") or "") == run_key
            and str(current.get("request_id") or "") == request_id
        )
        if not same:
            raise ValueError("Discovery preload entry is actively claimed by another worker")
    lease_expires = now + dt.timedelta(seconds=CLAIM_LEASE_SECONDS)
    claim = {
        "schema_version": 1,
        "preload_id": preload_id,
        "worker_id": worker_id,
        "run_key": run_key,
        "request_id": request_id,
        "claimed_at": current.get("claimed_at") if current else now.isoformat(),
        "lease_expires_at": lease_expires.isoformat(),
        "preload_result_path": _result_path(entry).as_posix(),
        "stock_bank": entry.get("stock_bank"),
        "stock_lane": "discovery",
    }
    _write(claim_path, claim)
    return entry, preload_result


def mark_ingested(root: Path, *, preload_id: str, run_key: str, source_submission: str | None = None) -> bool:
    root = root.resolve()
    preload_id = str(preload_id or "").strip()
    if not preload_id:
        return False
    entry = _read(root / ENTRIES / f"{preload_id}.json", {})
    if not isinstance(entry, dict) or entry.get("preload_id") != preload_id:
        return False
    target = root / _ingested_path(preload_id)
    if target.exists():
        return False
    _write(
        target,
        {
            "schema_version": 1,
            "preload_id": preload_id,
            "run_key": str(run_key or ""),
            "source_submission": source_submission,
            "ingested_at": _utcnow().isoformat(),
        },
    )
    try:
        (root / _claim_path(preload_id)).unlink()
    except FileNotFoundError:
        pass
    return True


def summary(root: Path) -> dict[str, Any]:
    root = root.resolve()
    now = _utcnow()
    expired = _expire_stale_claims(root, now)
    counts: dict[str, int] = {}
    directions: dict[str, dict[str, int]] = {}
    banks: dict[str, dict[str, int]] = {bank: {} for bank in BANK_IDS}
    for entry in _entries(root):
        status = _status(root, entry, now)
        counts[status] = counts.get(status, 0) + 1
        direction = str(entry.get("citation_direction") or "unknown")
        row = directions.setdefault(direction, {})
        row[status] = row.get(status, 0) + 1
        stock_bank = str(entry.get("stock_bank") or "").lower()
        if stock_bank in banks:
            bank_row = banks[stock_bank]
            bank_row[status] = bank_row.get(status, 0) + 1
    ready_banks = sum(
        1
        for bank in BANK_IDS
        if banks[bank].get("READY", 0) + banks[bank].get("PRECHECKED", 0) > 0
    )
    return {
        "target": DEFAULT_TARGET,
        "counts": counts,
        "directions": directions,
        "banks": banks,
        "discovery_stock_banks_ready": ready_banks,
        "discovery_stock_bank_target": len(BANK_IDS),
        "expired_claims_released": expired,
        "claim_lease_seconds": CLAIM_LEASE_SECONDS,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)

    top = sub.add_parser("top-up")
    top.add_argument("--target", type=int, default=DEFAULT_TARGET)
    top.add_argument("--max-new", type=int, default=DEFAULT_MAX_NEW)

    available = sub.add_parser("available")
    available.add_argument("--direction", choices=("backward", "forward", "normal"))
    available.add_argument("--limit", type=int, default=32)

    sub.add_parser("summary")
    args = parser.parse_args()

    if args.command == "top-up":
        result = top_up(args.repo_root, target=max(args.target, 0), max_new=max(args.max_new, 0))
    elif args.command == "available":
        result = {
            "items": available_preloads(
                args.repo_root,
                direction=args.direction,
                limit=max(args.limit, 0),
            )
        }
    else:
        result = summary(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
