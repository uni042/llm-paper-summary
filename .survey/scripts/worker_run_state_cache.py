#!/usr/bin/env python3
"""Small rebuildable index for Scheduled Chat run-state derivation.

This file is a performance cache only. Canonical claims, immutable descriptors,
submission results, and run-state results remain authoritative. Missing or invalid
cache entries must be rebuilt by derive_worker_run_state.py from durable facts.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

CACHE_ROOT = Path(".survey/work-queue/run-state/cache")
LATEST_ROOT = Path(".survey/work-queue/run-state/latest")
FACT_CLOCK = Path(".survey/work-queue/run-state/fact-clock.json")
ALLOWED_WORKERS = {"scheduled-chat-00", "scheduled-chat-30"}
TERMINAL = {"completed", "blocked", "deferred", "rejected"}


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
    path.write_text(text, encoding="utf-8")
    return True


def _fact_clock(root: Path) -> dict[str, Any]:
    value = _read(root / FACT_CLOCK, {})
    if not isinstance(value, dict) or value.get("schema_version") != 1:
        value = {"schema_version": 1, "workers": {}}
    if not isinstance(value.get("workers"), dict):
        value["workers"] = {}
    return value


def fact_generation(root: Path, worker_id: str) -> int:
    clock = _fact_clock(root)
    row = clock.get("workers", {}).get(worker_id)
    if not isinstance(row, dict):
        return 0
    return int(row.get("generation", 0) or 0)


def bump_fact_clock(root: Path, worker_ids: set[str], reason: str) -> dict[str, int]:
    clock = _fact_clock(root)
    workers = clock.setdefault("workers", {})
    now = dt.datetime.now(dt.timezone.utc).isoformat()
    out: dict[str, int] = {}
    for worker_id in sorted(worker_ids):
        if worker_id not in ALLOWED_WORKERS:
            continue
        row = workers.get(worker_id)
        if not isinstance(row, dict):
            row = {}
        generation = int(row.get("generation", 0) or 0) + 1
        workers[worker_id] = {
            "generation": generation,
            "updated_at": now,
            "reason": reason,
        }
        out[worker_id] = generation
    if out:
        _write(root / FACT_CLOCK, clock)
    return out


def cache_path(root: Path, worker_id: str) -> Path:
    return root / CACHE_ROOT / f"{worker_id}.json"


def load_cache(root: Path, worker_id: str) -> dict[str, Any] | None:
    if worker_id not in ALLOWED_WORKERS:
        return None
    value = _read(cache_path(root, worker_id), {})
    if not isinstance(value, dict):
        return None
    if value.get("schema_version") != 1 or value.get("worker_id") != worker_id:
        return None
    if not isinstance(value.get("generation"), int) or not isinstance(value.get("runs"), dict):
        return None
    return value


def _new_cache(worker_id: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "worker_id": worker_id,
        "generation": 0,
        "updated_at": None,
        "runs": {},
    }


def _save_cache(root: Path, cache: dict[str, Any]) -> bool:
    worker_id = str(cache.get("worker_id") or "")
    if worker_id not in ALLOWED_WORKERS:
        raise ValueError("unsupported worker cache")
    path = cache_path(root, worker_id)
    existing = load_cache(root, worker_id)
    if existing is not None and int(existing.get("generation", 0)) > int(cache.get("generation", 0)):
        raise ValueError("refusing to roll run-state cache backward")
    cache["updated_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    return _write(path, cache)


def _identity_from_request(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "worker_id": request["worker_id"],
        "run_key": request["run_key"],
        "scheduled_slot": request["scheduled_slot"],
        "actual_invocation_start": request["actual_invocation_start"],
    }


def get_run(root: Path, request: dict[str, Any]) -> dict[str, Any] | None:
    worker_id = str(request.get("worker_id") or "")
    cache = load_cache(root, worker_id)
    if cache is None:
        return None
    run = cache.get("runs", {}).get(str(request.get("run_key") or ""))
    if not isinstance(run, dict):
        return None
    for field in ("worker_id", "run_key", "scheduled_slot", "actual_invocation_start"):
        if run.get(field) != request.get(field):
            return None
    if run.get("cache_valid") is not True:
        return None
    if int(cache.get("fact_generation", -1) or -1) != fact_generation(root, worker_id):
        return None
    if not isinstance(run.get("claims"), dict) or not isinstance(run.get("submission"), dict):
        return None
    return run


def _attempt_facts_from_submission(submission: dict[str, Any]) -> dict[str, dict[str, Any]]:
    facts = submission.get("attempt_facts")
    if isinstance(facts, dict):
        return {
            str(key): dict(value)
            for key, value in facts.items()
            if isinstance(key, str) and key and isinstance(value, dict)
        }
    attempts: dict[str, dict[str, Any]] = {}
    for attempt_id in submission.get("submitted_attempt_ids") or []:
        if isinstance(attempt_id, str) and attempt_id:
            attempts[attempt_id] = {"attempt_id": attempt_id, "submitted": True}
    for attempt_id in submission.get("pending_attempt_ids") or []:
        if isinstance(attempt_id, str) and attempt_id:
            attempts.setdefault(attempt_id, {"attempt_id": attempt_id})["pending"] = True
    for attempt_id in submission.get("completed_attempt_ids") or []:
        if isinstance(attempt_id, str) and attempt_id:
            attempts.setdefault(attempt_id, {"attempt_id": attempt_id})["completed"] = True
    return attempts


def store_canonical_snapshot(
    root: Path,
    request: dict[str, Any],
    *,
    candidate_inventory: int,
    work_mode: str,
    claims: dict[str, Any],
    submission: dict[str, Any],
) -> int:
    worker_id = request["worker_id"]
    cache = load_cache(root, worker_id) or _new_cache(worker_id)
    runs = cache.setdefault("runs", {})
    previous = runs.get(request["run_key"])
    generation = int(cache.get("generation", 0)) + 1
    run = {
        **_identity_from_request(request),
        "cache_valid": True,
        "candidate_inventory": int(candidate_inventory),
        "work_mode": work_mode,
        "claims": dict(claims),
        "submission": {key: value for key, value in submission.items() if key != "attempt_facts"},
        "attempts": _attempt_facts_from_submission(submission),
        "generation": generation,
        "rebuilt_from_canonical": True,
    }
    if isinstance(previous, dict):
        run["first_cached_at"] = previous.get("first_cached_at") or cache.get("updated_at")
    else:
        run["first_cached_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    runs[request["run_key"]] = run
    cache["generation"] = generation
    cache["fact_generation"] = fact_generation(root, worker_id)
    _prune_runs(cache)
    _save_cache(root, cache)
    return generation


def update_claims(root: Path, request: dict[str, Any], claims: dict[str, Any]) -> int | None:
    worker_id = request["worker_id"]
    cache = load_cache(root, worker_id)
    if cache is None:
        return None
    run = cache.get("runs", {}).get(request["run_key"])
    if not isinstance(run, dict) or run.get("cache_valid") is not True:
        return None
    if run.get("claims") == claims:
        return int(run.get("generation", cache.get("generation", 0)))
    clock = bump_fact_clock(root, {worker_id}, "claim-state")
    generation = int(cache.get("generation", 0)) + 1
    run["claims"] = dict(claims)
    run["generation"] = generation
    cache["generation"] = generation
    cache["fact_generation"] = clock.get(worker_id, fact_generation(root, worker_id))
    _save_cache(root, cache)
    return generation

def _descriptor_identity(descriptor: dict[str, Any]) -> dict[str, Any] | None:
    worker_id = descriptor.get("worker_id")
    run_key = descriptor.get("run_key")
    slot = descriptor.get("scheduled_slot")
    start = descriptor.get("actual_invocation_start")
    if worker_id not in ALLOWED_WORKERS or not isinstance(run_key, str) or not run_key:
        return None
    if slot not in {"00", "30", "0830"} or parse_time(start) is None:
        return None
    if worker_id == "scheduled-chat-00" and slot != "00":
        return None
    if worker_id == "scheduled-chat-30" and slot not in {"30", "0830"}:
        return None
    return {
        "worker_id": worker_id,
        "run_key": run_key,
        "scheduled_slot": slot,
        "actual_invocation_start": start,
    }


def _result_for_descriptor(root: Path, descriptor_path: Path, descriptor: dict[str, Any]) -> dict[str, Any] | None:
    kind = descriptor.get("kind") or descriptor_path.parent.name
    result = _read(root / ".survey/work-queue/results" / str(kind) / descriptor_path.name, {})
    if not isinstance(result, dict):
        return None
    if result.get("attempt_id") != descriptor.get("attempt_id") or result.get("job_id") != descriptor.get("job_id"):
        return None
    return result


def _recompute_submission(run: dict[str, Any]) -> None:
    start = parse_time(run.get("actual_invocation_start"))
    assert start is not None
    attempts = run.get("attempts") if isinstance(run.get("attempts"), dict) else {}
    ordered = sorted(
        (value for value in attempts.values() if isinstance(value, dict) and value.get("submitted")),
        key=lambda value: (
            str(value.get("claimed_at") or ""),
            str(value.get("attempt_id") or ""),
        ),
    )
    pending = [value for value in ordered if value.get("pending") is True]
    completed = []
    terminal = []
    retryable = []
    repair_required = []
    for value in ordered:
        processed = parse_time(value.get("processed_at"))
        if value.get("retryable") is True:
            retryable.append(value)
        if value.get("repair_required") is True:
            repair_required.append(value)
        if value.get("completed") is True and processed is not None and processed >= start:
            completed.append(value)
        status = str(value.get("job_status") or "none").lower()
        if status in TERMINAL and processed is not None:
            terminal.append((processed, status))
    pipeline_ahead = 0
    if pending:
        earliest = min(ordered.index(value) for value in pending)
        pipeline_ahead = max(len(ordered) - earliest - 1, 0)
    terminal.sort()
    run["submission"] = {
        "research_audit_completed_this_invocation": len(completed),
        "submission_state_checked": True,
        "submission_result_pending": bool(pending),
        "pipeline_ahead_count": pipeline_ahead,
        "last_terminal_job_status": terminal[-1][1] if terminal else "none",
        "submitted_attempt_ids": [str(value.get("attempt_id")) for value in ordered],
        "pending_attempt_ids": [str(value.get("attempt_id")) for value in pending],
        "completed_attempt_ids": [str(value.get("attempt_id")) for value in completed],
        "retryable_attempt_ids": [str(value.get("attempt_id")) for value in retryable],
        "repair_required_attempt_ids": [str(value.get("attempt_id")) for value in repair_required],
    }

def observe_descriptors(root: Path, descriptor_paths: list[Path]) -> dict[str, list[str]]:
    """Apply descriptor/result deltas to cached runs with fail-safe invalidation.

    The durable fact clock is advanced *before* cache mutation. If cache updating then
    fails, get_run() rejects the older cache generation and the next derivation falls
    back to canonical durable facts instead of trusting stale state.
    """
    root = root.resolve()
    touched: dict[str, set[str]] = {}
    loaded: dict[str, dict[str, Any]] = {}
    parsed: list[tuple[Path, dict[str, Any], str, str, list[str]]] = []

    def cache_for(worker_id: str) -> dict[str, Any] | None:
        if worker_id not in loaded:
            value = load_cache(root, worker_id)
            if value is not None:
                loaded[worker_id] = value
        return loaded.get(worker_id)

    affected_workers: set[str] = set()
    for raw_path in descriptor_paths:
        path = raw_path if raw_path.is_absolute() else root / raw_path
        descriptor = _read(path, {})
        if not isinstance(descriptor, dict):
            continue
        attempt_id = str(descriptor.get("attempt_id") or "")
        job_id = str(descriptor.get("job_id") or "")
        if not attempt_id:
            continue
        identity = _descriptor_identity(descriptor)
        candidate_workers: list[str] = []
        if identity is not None:
            candidate_workers = [identity["worker_id"]]
        else:
            for worker_id in sorted(ALLOWED_WORKERS):
                cache = cache_for(worker_id)
                if cache is None:
                    continue
                if any(
                    isinstance(run, dict)
                    and attempt_id in (run.get("attempts") or {})
                    for run in cache.get("runs", {}).values()
                ):
                    candidate_workers.append(worker_id)
        if candidate_workers:
            parsed.append((path, descriptor, attempt_id, job_id, candidate_workers))
            affected_workers.update(candidate_workers)

    clock_generations = (
        bump_fact_clock(root, affected_workers, "immutable-submission")
        if affected_workers
        else {}
    )
    changed_workers: set[str] = set()

    for path, descriptor, attempt_id, job_id, candidate_workers in parsed:
        identity = _descriptor_identity(descriptor)
        result = _result_for_descriptor(root, path, descriptor)
        for worker_id in candidate_workers:
            cache = cache_for(worker_id)
            if cache is None:
                continue
            runs = cache.get("runs") if isinstance(cache.get("runs"), dict) else {}
            for run_key, run in runs.items():
                if not isinstance(run, dict) or run.get("cache_valid") is not True:
                    continue
                attempts = run.setdefault("attempts", {})
                if not isinstance(attempts, dict):
                    continue
                identity_matches = identity is not None and run_key == identity["run_key"]
                if not identity_matches and attempt_id not in attempts:
                    continue
                fact = dict(attempts.get(attempt_id) or {})
                before = json.dumps(fact, sort_keys=True, ensure_ascii=False)
                fact.update({
                    "attempt_id": attempt_id,
                    "job_id": job_id,
                    "kind": descriptor.get("kind"),
                    "submitted": True,
                    "descriptor_path": path.relative_to(root).as_posix(),
                    "worker_id": worker_id,
                    "run_key": descriptor.get("run_key"),
                })
                if not fact.get("claimed_at"):
                    fact["claimed_at"] = run.get("actual_invocation_start")
                if result is None:
                    fact["pending"] = True
                    fact["retryable"] = False
                    fact["repair_required"] = False
                    fact.pop("processed_at", None)
                    fact.pop("job_status", None)
                    fact.pop("completed", None)
                else:
                    status = str(result.get("job_status") or "none").lower()
                    retryable = result.get("ok") is False and result.get("retryable") is True
                    fact["processed_at"] = result.get("processed_at")
                    fact["job_status"] = status
                    fact["retryable"] = retryable
                    fact["repair_required"] = result.get("repair_required") is True
                    # Preserve established semantics: only a missing result or an
                    # explicitly retryable result is submission-result pending.
                    fact["pending"] = retryable
                    fact["completed"] = bool(result.get("ok") is True and status == "completed")
                attempts[attempt_id] = fact
                after = json.dumps(fact, sort_keys=True, ensure_ascii=False)
                if after != before:
                    touched.setdefault(worker_id, set()).add(run_key)
                    changed_workers.add(worker_id)

    for worker_id in changed_workers:
        cache = loaded[worker_id]
        generation = int(cache.get("generation", 0)) + 1
        for run_key in touched.get(worker_id, set()):
            run = cache["runs"][run_key]
            claims = run.get("claims") if isinstance(run.get("claims"), dict) else {}
            active_jobs = list(claims.get("active_job_ids") or [])
            submitted_jobs = {
                str(fact.get("job_id"))
                for fact in run.get("attempts", {}).values()
                if isinstance(fact, dict) and fact.get("submitted")
            }
            active_jobs = [job for job in active_jobs if job not in submitted_jobs]
            claims["active_job_ids"] = sorted(active_jobs)
            claims["active_assignment"] = bool(active_jobs)
            run["claims"] = claims
            _recompute_submission(run)
            run["generation"] = generation
            run["rebuilt_from_canonical"] = False
        cache["generation"] = generation
        cache["fact_generation"] = clock_generations.get(
            worker_id, fact_generation(root, worker_id)
        )
        _save_cache(root, cache)

    return {worker: sorted(keys) for worker, keys in touched.items()}

def cached_request(root: Path, worker_id: str, run_key: str) -> dict[str, Any] | None:
    cache = load_cache(root, worker_id)
    if cache is None:
        return None
    run = cache.get("runs", {}).get(run_key)
    if not isinstance(run, dict) or run.get("cache_valid") is not True:
        return None
    return {
        "schema_version": 1,
        "request_id": "auto-pending",
        "run_key": run["run_key"],
        "worker_id": run["worker_id"],
        "worker_kind": "scheduled_chat",
        "scheduled_slot": run["scheduled_slot"],
        "actual_invocation_start": run["actual_invocation_start"],
        "runtime_condition": "none",
        "runtime_condition_confirmed": False,
        "runtime_condition_attempts": 0,
        "runtime_condition_detail": "",
    }


def generation_for(root: Path, worker_id: str, run_key: str) -> int:
    cache = load_cache(root, worker_id)
    if cache is None:
        return 0
    run = cache.get("runs", {}).get(run_key)
    if not isinstance(run, dict):
        return 0
    return int(run.get("generation", cache.get("generation", 0)) or 0)


def auto_result_id(worker_id: str, run_key: str, generation: int) -> str:
    digest = hashlib.sha256(f"{worker_id}\0{run_key}".encode("utf-8")).hexdigest()[:16]
    return f"auto-{digest}-g{max(int(generation), 0):08d}"


def write_latest_pointer(root: Path, result_path: Path, result: dict[str, Any]) -> bool:
    worker_id = str(result.get("worker_id") or "")
    if worker_id not in ALLOWED_WORKERS:
        return False
    path = root / LATEST_ROOT / f"{worker_id}.json"
    current = _read(path, {})
    current_start = parse_time(current.get("actual_invocation_start")) if isinstance(current, dict) else None
    new_start = parse_time(result.get("actual_invocation_start"))
    current_generation = int(current.get("snapshot_generation", -1) or -1) if isinstance(current, dict) else -1
    new_generation = int(result.get("snapshot_generation", 0) or 0)
    if current_start is not None and new_start is not None:
        if current_start > new_start:
            return False
        if current_start == new_start and current_generation > new_generation:
            return False
    payload = {
        "schema_version": 1,
        "worker_id": worker_id,
        "run_key": result.get("run_key"),
        "scheduled_slot": result.get("scheduled_slot"),
        "actual_invocation_start": result.get("actual_invocation_start"),
        "request_id": result.get("request_id"),
        "result_path": result_path.relative_to(root).as_posix(),
        "snapshot_generation": new_generation,
        "processed_at": result.get("processed_at"),
    }
    return _write(path, payload)


def _prune_runs(cache: dict[str, Any], keep: int = 8) -> None:
    runs = cache.get("runs")
    if not isinstance(runs, dict) or len(runs) <= keep:
        return
    rows = []
    for key, run in runs.items():
        if not isinstance(run, dict):
            continue
        start = parse_time(run.get("actual_invocation_start")) or dt.datetime.min.replace(tzinfo=dt.timezone.utc)
        pending = bool((run.get("submission") or {}).get("submission_result_pending"))
        active = bool((run.get("claims") or {}).get("active_assignment"))
        rows.append((pending or active, start, key))
    rows.sort(reverse=True)
    keep_keys = {key for _, _, key in rows[:keep]}
    for key in list(runs):
        if key not in keep_keys:
            runs.pop(key, None)
