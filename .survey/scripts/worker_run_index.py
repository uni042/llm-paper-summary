#!/usr/bin/env python3
"""Advisory incremental index for Scheduled Chat run-state derivation.

The cache is never authoritative. Canonical claim/submission/result files remain the
source of truth and can rebuild this index at any time. Writes are monotonic: an
older submission result cannot roll an attempt back to an earlier state.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Iterable

CACHE_VERSION = 1
CACHE_ROOT = Path(".survey/work-queue/run-state/cache")
LATEST_ROOT = Path(".survey/work-queue/run-state/latest")
ALLOWED_WORKERS = {"scheduled-chat-00": {"00"}, "scheduled-chat-30": {"30", "0830"}}
RUN_FIELDS = ("worker_id", "run_key", "scheduled_slot", "actual_invocation_start")
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,255}$")
TERMINAL = {"completed", "blocked", "deferred", "rejected"}


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: Any) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists():
        try:
            if path.read_text(encoding="utf-8") == text:
                return False
        except OSError:
            pass
    path.write_text(text, encoding="utf-8")
    return True


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(dt.timezone.utc)


def normalize_identity(value: dict[str, Any], *, required: bool = True) -> dict[str, str] | None:
    present = [field for field in RUN_FIELDS if value.get(field) not in (None, "")]
    if not present:
        if required:
            raise ValueError("run identity is required")
        return None
    if len(present) != len(RUN_FIELDS):
        raise ValueError("run identity fields must be provided together")
    worker_id = str(value["worker_id"]).strip()
    run_key = str(value["run_key"]).strip()
    slot = str(value["scheduled_slot"]).strip()
    started_raw = str(value["actual_invocation_start"]).strip()
    if worker_id not in ALLOWED_WORKERS:
        raise ValueError("worker_id must be scheduled-chat-00 or scheduled-chat-30")
    if slot not in ALLOWED_WORKERS[worker_id]:
        raise ValueError("scheduled_slot does not match worker_id")
    if not run_key or len(run_key) > 256:
        raise ValueError("run_key must be a non-empty string <= 256 characters")
    started = parse_time(started_raw)
    if started is None:
        raise ValueError("actual_invocation_start must be an offset-aware timestamp")
    return {
        "worker_id": worker_id,
        "run_key": run_key,
        "scheduled_slot": slot,
        "actual_invocation_start": started.isoformat(),
    }


def identity_matches(left: dict[str, Any], right: dict[str, Any]) -> bool:
    try:
        a = normalize_identity(left)
        b = normalize_identity(right)
    except ValueError:
        return False
    return a == b


def _token(identity: dict[str, Any]) -> str:
    normalized = normalize_identity(identity)
    assert normalized is not None
    payload = "\0".join(normalized[field] for field in RUN_FIELDS).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()[:32]


def cache_path(root: Path, identity: dict[str, Any]) -> Path:
    normalized = normalize_identity(identity)
    assert normalized is not None
    return root / CACHE_ROOT / normalized["worker_id"] / f"{_token(normalized)}.json"


def latest_path(root: Path, worker_id: str) -> Path:
    if worker_id not in ALLOWED_WORKERS:
        raise ValueError("unsupported worker_id")
    return root / LATEST_ROOT / f"{worker_id}.json"


def load_cache(root: Path, identity: dict[str, Any]) -> dict[str, Any] | None:
    path = cache_path(Path(root).resolve(), identity)
    value = _read(path, {})
    if not isinstance(value, dict):
        return None
    if value.get("schema_version") != 1 or value.get("cache_version") != CACHE_VERSION:
        return None
    if value.get("canonical_complete") is not True:
        return None
    if not identity_matches(value, identity):
        return None
    if not isinstance(value.get("attempts"), dict):
        return None
    revision = value.get("revision")
    if isinstance(revision, bool) or not isinstance(revision, int) or revision < 1:
        return None
    return value


def _canonical_descriptor_for_attempt(root: Path, attempt_id: str) -> tuple[str, Path, dict[str, Any]] | None:
    for kind in ("research", "audit"):
        path = root / ".survey/work-queue/submissions" / kind / f"{attempt_id}.json"
        value = _read(path, {})
        if isinstance(value, dict) and value.get("attempt_id") == attempt_id:
            return kind, path, value
    return None


def _descriptor_for_attempt(root: Path, attempt_id: str) -> tuple[str, Path, dict[str, Any]] | None:
    canonical = _canonical_descriptor_for_attempt(root, attempt_id)
    if canonical is not None:
        return canonical
    # Legacy arbitrary descriptor names are a read-only fallback. This scan is used
    # only during canonical rebuild, never on the incremental hot path.
    for kind in ("research", "audit"):
        folder = root / ".survey/work-queue/submissions" / kind
        if not folder.is_dir():
            continue
        matches: list[tuple[Path, dict[str, Any]]] = []
        for path in folder.glob("*.json"):
            value = _read(path, {})
            if isinstance(value, dict) and value.get("attempt_id") == attempt_id:
                matches.append((path, value))
        if len(matches) == 1:
            path, value = matches[0]
            return kind, path, value
    return None


def _result_for_descriptor(root: Path, kind: str, descriptor_path: Path, attempt_id: str) -> dict[str, Any] | None:
    path = root / ".survey/work-queue/results" / kind / descriptor_path.name
    value = _read(path, {})
    if not isinstance(value, dict) or value.get("attempt_id") != attempt_id:
        return None
    return value


def _aggregate(cache: dict[str, Any]) -> dict[str, Any]:
    started = parse_time(cache.get("actual_invocation_start"))
    assert started is not None
    attempts = cache.get("attempts") if isinstance(cache.get("attempts"), dict) else {}
    submitted: list[tuple[int, str]] = []
    pending: list[tuple[int, str]] = []
    completed: list[str] = []
    retryable: list[str] = []
    terminal: list[tuple[dt.datetime, str, str]] = []
    for attempt_id, raw in attempts.items():
        if not isinstance(raw, dict) or raw.get("submitted") is not True:
            continue
        seq = raw.get("submitted_seq")
        if isinstance(seq, bool) or not isinstance(seq, int):
            seq = 0
        submitted.append((seq, attempt_id))
        status = str(raw.get("result_status") or "").lower()
        processed_at = parse_time(raw.get("result_processed_at"))
        ok = raw.get("result_ok")
        is_retryable = raw.get("retryable") is True
        if processed_at is None or (ok is False and is_retryable):
            pending.append((seq, attempt_id))
            if is_retryable:
                retryable.append(attempt_id)
            continue
        if ok is True and status == "completed" and processed_at >= started:
            completed.append(attempt_id)
        if status in TERMINAL:
            terminal.append((processed_at, status, attempt_id))
        elif ok is False and is_retryable:
            pending.append((seq, attempt_id))
            retryable.append(attempt_id)

    pipeline_ahead = 0
    if pending:
        earliest = min(seq for seq, _ in pending)
        pipeline_ahead = sum(1 for seq, _ in submitted if seq > earliest)
    terminal.sort()
    return {
        "research_audit_completed_this_invocation": len(completed),
        "submission_state_checked": True,
        "submission_result_pending": bool(pending),
        "pipeline_ahead_count": pipeline_ahead,
        "last_terminal_job_status": terminal[-1][1] if terminal else "none",
        "submitted_attempt_ids": [attempt for _, attempt in sorted(submitted)],
        "pending_attempt_ids": [attempt for _, attempt in sorted(pending)],
        "retryable_attempt_ids": sorted(retryable),
        "completed_attempt_ids_this_invocation": sorted(completed),
    }


def cached_submission_state(cache: dict[str, Any]) -> dict[str, Any]:
    return _aggregate(cache)


def cached_route(cache: dict[str, Any]) -> tuple[int, str] | None:
    inventory = cache.get("candidate_inventory")
    mode = cache.get("work_mode")
    if isinstance(inventory, int) and not isinstance(inventory, bool) and mode in {"research", "discovery", "maintenance"}:
        return max(inventory, 0), mode
    return None


def rebuild_cache(
    root: Path,
    identity: dict[str, Any],
    *,
    candidate_inventory: int,
    work_mode: str,
    attempts: dict[str, dt.datetime],
    claims: dict[str, Any],
) -> dict[str, Any]:
    root = Path(root).resolve()
    normalized = normalize_identity(identity)
    assert normalized is not None
    ordered = sorted(attempts.items(), key=lambda item: (item[1], item[0]))
    attempt_rows: dict[str, dict[str, Any]] = {}
    for seq, (attempt_id, claimed_at) in enumerate(ordered, start=1):
        row: dict[str, Any] = {
            "claimed_at": claimed_at.astimezone(dt.timezone.utc).isoformat(),
            "submitted": False,
            "submitted_seq": seq,
            "result_processed_at": None,
            "result_ok": None,
            "result_status": None,
            "retryable": False,
        }
        found = _descriptor_for_attempt(root, attempt_id)
        if found is not None:
            kind, descriptor_path, _descriptor = found
            row["submitted"] = True
            row["kind"] = kind
            row["descriptor_path"] = descriptor_path.relative_to(root).as_posix()
            result = _result_for_descriptor(root, kind, descriptor_path, attempt_id)
            if result is not None:
                row["result_processed_at"] = (
                    parse_time(result.get("processed_at")).isoformat()
                    if parse_time(result.get("processed_at")) is not None
                    else None
                )
                row["result_ok"] = result.get("ok")
                row["result_status"] = str(result.get("job_status") or "").lower() or None
                row["retryable"] = result.get("retryable") is True
        attempt_rows[attempt_id] = row

    previous = load_cache(root, normalized)
    previous_revision = int((previous or {}).get("revision") or 0)
    latest = _read(latest_path(root, normalized["worker_id"]), {})
    latest_revision = 0
    if isinstance(latest, dict) and identity_matches(latest, normalized):
        raw_generation = latest.get("snapshot_generation")
        if isinstance(raw_generation, int) and not isinstance(raw_generation, bool):
            latest_revision = max(raw_generation, 0)
    revision = max(previous_revision, latest_revision) + 1
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    cache: dict[str, Any] = {
        "schema_version": 1,
        "cache_version": CACHE_VERSION,
        "canonical_complete": True,
        **normalized,
        "candidate_inventory": max(int(candidate_inventory), 0),
        "work_mode": work_mode,
        "revision": revision,
        "rebuilt_at": now,
        "updated_at": now,
        "attempts": attempt_rows,
        "claim_state": dict(claims),
    }
    cache["submission_state"] = _aggregate(cache)
    _write(cache_path(root, normalized), cache)
    return cache


def update_claim_state(root: Path, identity: dict[str, Any], claims: dict[str, Any]) -> dict[str, Any] | None:
    root = Path(root).resolve()
    cache = load_cache(root, identity)
    if cache is None:
        return None
    current = cache.get("claim_state")
    if current == claims:
        return cache
    cache["claim_state"] = dict(claims)
    cache["revision"] = int(cache["revision"]) + 1
    cache["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    cache["submission_state"] = _aggregate(cache)
    _write(cache_path(root, identity), cache)
    return cache


def _descriptor_identity(descriptor: dict[str, Any]) -> dict[str, str] | None:
    try:
        return normalize_identity(descriptor, required=False)
    except ValueError:
        return None


def apply_descriptor(root: Path, descriptor_path: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    path = Path(descriptor_path)
    if not path.is_absolute():
        path = root / path
    descriptor = _read(path, {})
    if not isinstance(descriptor, dict):
        return {"updated": False, "reason": "unreadable_descriptor"}
    identity = _descriptor_identity(descriptor)
    if identity is None:
        return {"updated": False, "reason": "legacy_descriptor_without_run_identity"}
    cache = load_cache(root, identity)
    if cache is None:
        return {"updated": False, "reason": "no_canonical_cache", "identity": identity}
    attempt_id = str(descriptor.get("attempt_id") or "")
    rows = cache["attempts"]
    row = rows.get(attempt_id)
    if not isinstance(row, dict):
        job_id = str(descriptor.get("job_id") or "")
        claim = _read(root / ".survey/work-queue/claims" / f"{job_id}.json", {})
        claimed_at = parse_time(claim.get("claimed_at")) if isinstance(claim, dict) else None
        if not (
            isinstance(claim, dict)
            and claim.get("attempt_id") == attempt_id
            and claim.get("worker_id") == identity["worker_id"]
            and claimed_at is not None
        ):
            return {"updated": False, "reason": "attempt_not_in_canonical_cache", "identity": identity}
        row = {
            "claimed_at": claimed_at.isoformat(),
            "submitted": False,
            "submitted_seq": 0,
            "result_processed_at": None,
            "result_ok": None,
            "result_status": None,
            "retryable": False,
        }
        rows[attempt_id] = row
    relative = path.relative_to(root).as_posix()
    changed = row.get("submitted") is not True or row.get("descriptor_path") != relative
    if not changed:
        return {"updated": False, "reason": "already_indexed", "identity": identity}
    row["submitted"] = True
    ordered_attempts = sorted(
        (
            (parse_time(value.get("claimed_at")) or dt.datetime.max.replace(tzinfo=dt.timezone.utc), key)
            for key, value in rows.items()
            if isinstance(value, dict)
        ),
        key=lambda item: (item[0], item[1]),
    )
    for seq, (_claimed_at, key) in enumerate(ordered_attempts, start=1):
        rows[key]["submitted_seq"] = seq
    row["kind"] = descriptor.get("kind")
    row["descriptor_path"] = relative
    cache["revision"] = int(cache["revision"]) + 1
    cache["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    cache["submission_state"] = _aggregate(cache)
    _write(cache_path(root, identity), cache)
    return {"updated": True, "identity": identity, "attempt_id": attempt_id, "revision": cache["revision"]}


def apply_result(root: Path, result_path: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    path = Path(result_path)
    if not path.is_absolute():
        path = root / path
    result = _read(path, {})
    if not isinstance(result, dict):
        return {"updated": False, "reason": "unreadable_result"}
    attempt_id = str(result.get("attempt_id") or "")
    kind = str(result.get("job_type") or "")
    if kind not in {"research", "audit"} or not attempt_id:
        return {"updated": False, "reason": "result_identity_missing"}
    descriptor_path = root / ".survey/work-queue/submissions" / kind / path.name
    descriptor = _read(descriptor_path, {})
    if not isinstance(descriptor, dict) or descriptor.get("attempt_id") != attempt_id:
        found = _descriptor_for_attempt(root, attempt_id)
        if found is None:
            return {"updated": False, "reason": "descriptor_not_found"}
        kind, descriptor_path, descriptor = found
    identity = _descriptor_identity(descriptor)
    if identity is None:
        return {"updated": False, "reason": "legacy_descriptor_without_run_identity"}
    cache = load_cache(root, identity)
    if cache is None:
        return {"updated": False, "reason": "no_canonical_cache", "identity": identity}
    row = cache["attempts"].get(attempt_id)
    if not isinstance(row, dict):
        return {"updated": False, "reason": "attempt_not_in_canonical_cache", "identity": identity}

    incoming_time = parse_time(result.get("processed_at"))
    previous_time = parse_time(row.get("result_processed_at"))
    if incoming_time is None:
        return {"updated": False, "reason": "result_processed_at_missing", "identity": identity}
    if previous_time is not None and incoming_time < previous_time:
        return {"updated": False, "reason": "stale_result_ignored", "identity": identity}

    new_values = {
        "submitted": True,
        "kind": kind,
        "descriptor_path": descriptor_path.relative_to(root).as_posix(),
        "result_processed_at": incoming_time.isoformat(),
        "result_ok": result.get("ok"),
        "result_status": str(result.get("job_status") or "").lower() or None,
        "retryable": result.get("retryable") is True,
    }
    changed = any(row.get(key) != value for key, value in new_values.items())
    if not changed:
        return {"updated": False, "reason": "already_indexed", "identity": identity}
    row.update(new_values)
    cache["revision"] = int(cache["revision"]) + 1
    cache["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    cache["submission_state"] = _aggregate(cache)
    _write(cache_path(root, identity), cache)
    return {"updated": True, "identity": identity, "attempt_id": attempt_id, "revision": cache["revision"]}


def quick_consistency(root: Path, identity: dict[str, Any], cache: dict[str, Any], claims: dict[str, Any]) -> tuple[bool, str]:
    """Cheaply validate only currently relevant identities.

    This does not prove the cache correct; it detects the races that matter to liveness.
    Any mismatch falls back to a canonical rebuild.
    """
    root = Path(root).resolve()
    active_attempts = {
        str(item) for item in claims.get("active_attempt_ids", []) if isinstance(item, str) and item
    }
    cached_attempts = cache.get("attempts") if isinstance(cache.get("attempts"), dict) else {}
    if not active_attempts.issubset(set(cached_attempts)):
        return False, "active_attempt_missing_from_cache"

    for attempt_id, row in cached_attempts.items():
        if not isinstance(row, dict):
            return False, "malformed_attempt_cache"
        found = _canonical_descriptor_for_attempt(root, attempt_id) if row.get("submitted") is not True else None
        if found is not None:
            return False, "new_descriptor_not_indexed"
        if row.get("submitted") is not True:
            continue
        descriptor_path_text = row.get("descriptor_path")
        if not isinstance(descriptor_path_text, str):
            return False, "submitted_attempt_missing_descriptor_path"
        descriptor_path = root / descriptor_path_text
        kind = str(row.get("kind") or descriptor_path.parent.name)
        result = _result_for_descriptor(root, kind, descriptor_path, attempt_id)
        cached_time = parse_time(row.get("result_processed_at"))
        if result is None:
            if cached_time is not None:
                return False, "cached_result_missing_from_canonical_state"
            continue
        canonical_time = parse_time(result.get("processed_at"))
        if canonical_time != cached_time:
            return False, "canonical_result_newer_or_different"
        if result.get("ok") != row.get("result_ok"):
            return False, "canonical_result_outcome_mismatch"
        if (result.get("retryable") is True) != (row.get("retryable") is True):
            return False, "canonical_retryable_mismatch"
    return True, "ok"


def publish_latest(root: Path, result_path: Path, result: dict[str, Any], generation: int) -> bool:
    root = Path(root).resolve()
    identity = normalize_identity(result)
    assert identity is not None
    path = latest_path(root, identity["worker_id"])
    current = _read(path, {})
    current_generation = current.get("snapshot_generation") if isinstance(current, dict) else None
    if (
        isinstance(current, dict)
        and identity_matches(current, identity)
        and isinstance(current_generation, int)
        and current_generation > generation
    ):
        return False
    payload = {
        "schema_version": 1,
        **identity,
        "snapshot_generation": int(generation),
        "result_path": Path(result_path).as_posix(),
        "request_id": result.get("request_id"),
        "processed_at": result.get("processed_at"),
        "snapshot_origin": result.get("snapshot_origin", "run_state_request"),
    }
    return _write(path, payload)


def cache_generation(root: Path, identity: dict[str, Any]) -> int | None:
    cache = load_cache(root, identity)
    if cache is None:
        return None
    return int(cache["revision"])


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--show", type=Path, help="Show one cache selected by a JSON identity document")
    args = parser.parse_args()
    if args.show:
        identity = _read(args.show, {})
        cache = load_cache(args.repo_root.resolve(), identity)
        print(json.dumps(cache or {}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
