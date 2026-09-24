#!/usr/bin/env python3
"""Derive Scheduled Chat continuation state from durable repository facts.

Workers write a small immutable request under
.survey/work-queue/run-state/requests/<request_id>.json.  This helper derives the
mutable gate inputs from queue/claim/submission/discovery state instead of asking the
worker to invent many booleans.  The first successful snapshot for a run_key freezes
candidate_inventory/work_mode for the rest of that invocation.

Only one non-derived input remains: runtime_condition, an enum describing a concrete
platform/transport event that cannot be inferred from repository files.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import time
from pathlib import Path
from typing import Any

import claim_state
import claim_window_policy
import continuation_gate
import run_finalization_gate
import worker_quota_policy
import discovery_preload_queue
import select_discovery_direction
import worker_identity
import worker_run_state_cache as run_state_cache

REQUESTS = Path(".survey/work-queue/run-state/requests")
RESULTS = Path(".survey/work-queue/run-state/results")
READ_COUNT = 0
SCHEDULED_CHAT_CLAIM_WINDOW = claim_window_policy.DEFAULT_CLAIM_WINDOW
DISCOVERY_PIPELINE_WINDOW = 3
RESEARCH_PREFLIGHT_PIPELINE_WINDOW = 2

RUNTIME_CONDITIONS = {
    "none",
    "handoff_guard",
    "github_read_unavailable",
    "durable_transports_unavailable",
    "platform_context_limit",
    "transport_unrecoverable",
}
PLATFORM_CONTEXT_LIMIT_EVENT = "platform_tool_call_rejected"


def _read(path: Path, default: Any = None) -> Any:
    global READ_COUNT
    READ_COUNT += 1
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


def _time(value: Any) -> dt.datetime | None:
    return claim_state.parse_time(value)


def _normalize_request(path: Path, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("request must be a JSON object")
    if value.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    request_id = str(value.get("request_id") or "").strip()
    if not request_id or path.stem != request_id:
        raise ValueError("request_id must be non-empty and match filename stem")
    worker_id = str(value.get("worker_id") or "").strip()
    scheduled_slot = str(value.get("scheduled_slot") or "").strip()
    worker_identity.validate_identity_slot(worker_id, scheduled_slot)
    run_key = str(value.get("run_key") or "").strip()
    if not run_key:
        raise ValueError("run_key is required")
    raw_invocation_start = value.get("actual_invocation_start")
    started_at, start_recovery = run_state_cache.normalize_invocation_start(raw_invocation_start)
    if started_at is None:
        raise ValueError(
            "actual_invocation_start must be offset-aware and cannot be materially in the future"
        )
    runtime_condition = str(value.get("runtime_condition") or "none").strip()
    if runtime_condition not in RUNTIME_CONDITIONS:
        raise ValueError("unsupported runtime_condition")
    runtime_condition_confirmed = value.get("runtime_condition_confirmed") is True
    runtime_condition_attempts = value.get("runtime_condition_attempts", 0)
    if isinstance(runtime_condition_attempts, bool) or not isinstance(runtime_condition_attempts, int):
        raise ValueError("runtime_condition_attempts must be an integer")
    runtime_condition_detail = str(value.get("runtime_condition_detail") or "").strip()
    runtime_condition_event = str(value.get("runtime_condition_event") or "").strip()

    direct_inventory = value.get("candidate_inventory_at_start")
    direct_mode = str(value.get("work_mode_at_start") or "").strip()
    direct_threshold = value.get("research_discovery_threshold")
    direct_generated_at = str(value.get("hot_dispatch_generated_at") or "").strip()
    route_recovery_source = str(value.get("route_recovery_source") or "").strip()
    recovered_work_mode = str(value.get("recovered_work_mode_at_start") or "").strip()
    if route_recovery_source:
        recovery_modes = {
            "discovery_precheck_identity": "discovery",
            "research_preflight_identity": "research",
        }
        expected_mode = recovery_modes.get(route_recovery_source)
        if expected_mode is None:
            raise ValueError("unsupported route_recovery_source")
        if recovered_work_mode != expected_mode:
            raise ValueError(
                f"{route_recovery_source} run-state recovery must preserve {expected_mode} mode"
            )
        if scheduled_slot == "0830":
            raise ValueError("08:30 maintenance cannot use paper-work route recovery")
    direct_present = any(
        item not in (None, "")
        for item in (direct_inventory, direct_mode, direct_threshold, direct_generated_at)
    )
    direct_route: dict[str, Any] = {}
    if direct_present:
        if (
            isinstance(direct_inventory, bool)
            or not isinstance(direct_inventory, int)
            or direct_inventory < 0
        ):
            raise ValueError("candidate_inventory_at_start must be a non-negative integer")
        if direct_mode not in {"research", "discovery"}:
            raise ValueError("work_mode_at_start must be research or discovery")
        if (
            isinstance(direct_threshold, bool)
            or not isinstance(direct_threshold, int)
            or direct_threshold != claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD
        ):
            raise ValueError("research_discovery_threshold does not match the current policy")
        # Inventory is routing telemetry, not a transport capability gate. The
        # caller freezes the selected mode for the invocation; dual-purpose banks
        # keep Research and Discovery stock independently available.
        if scheduled_slot == "0830":
            raise ValueError("08:30 maintenance cannot use a direct paper-work route")
        generated = _time(direct_generated_at)
        if generated is None:
            raise ValueError("hot_dispatch_generated_at must be an offset-aware timestamp")
        direct_route = {
            "candidate_inventory_at_start": direct_inventory,
            "work_mode_at_start": direct_mode,
            "research_discovery_threshold": direct_threshold,
            "hot_dispatch_generated_at": generated.astimezone(dt.timezone.utc).isoformat(),
        }

    return {
        "schema_version": 1,
        "request_id": request_id,
        "run_key": run_key,
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "scheduled_slot": scheduled_slot,
        "actual_invocation_start": started_at.astimezone(dt.timezone.utc).isoformat(),
        "actual_invocation_start_original": (
            str(raw_invocation_start).strip() if start_recovery is not None else None
        ),
        "actual_invocation_start_recovery": start_recovery,
        "runtime_condition": runtime_condition,
        "runtime_condition_confirmed": runtime_condition_confirmed,
        "runtime_condition_attempts": max(runtime_condition_attempts, 0),
        "runtime_condition_detail": runtime_condition_detail,
        "runtime_condition_event": runtime_condition_event,
        "route_recovery_source": route_recovery_source,
        "recovered_work_mode_at_start": recovered_work_mode,
        **direct_route,
    }


def _next_jobs(root: Path) -> dict[str, Any]:
    return _read(root / ".survey/work-queue/next-jobs.json", {}) or {}


def _candidate_inventory(root: Path) -> int:
    snap = _next_jobs(root)
    claiming = snap.get("claiming") if isinstance(snap.get("claiming"), dict) else {}
    value = claiming.get("ready_research_audit")
    if isinstance(value, int) and not isinstance(value, bool):
        return max(value, 0)
    counts = snap.get("counts") if isinstance(snap.get("counts"), dict) else {}
    research = counts.get("research") if isinstance(counts.get("research"), dict) else {}
    audit = counts.get("audit") if isinstance(counts.get("audit"), dict) else {}
    return max(int(research.get("ready", 0) or 0), 0) + max(int(audit.get("ready", 0) or 0), 0)


def _frozen_route(root: Path, run_key: str) -> tuple[int, str] | None:
    rows: list[tuple[str, int, str]] = []
    roots = (
        root / RESULTS,
        root / ".survey/work-queue/archive/transport/run-state/results",
    )
    for result_root in roots:
        if not result_root.is_dir():
            continue
        for path in result_root.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict) or value.get("ok") is not True:
                continue
            if str(value.get("run_key") or "") != run_key:
                continue
            inventory = value.get("candidate_inventory")
            mode = value.get("work_mode")
            if isinstance(inventory, int) and mode in {"research", "discovery", "maintenance"}:
                rows.append((str(value.get("processed_at") or ""), inventory, mode))
    if not rows:
        return None
    rows.sort()
    _, inventory, mode = rows[0]
    return inventory, mode


def _run_attempts(root: Path, worker_id: str, started_at: dt.datetime) -> dict[str, dt.datetime]:
    # Track current-run assignments, carry-over active assignments, and any older
    # same-worker attempt whose terminal result was produced during this invocation.
    all_worker_attempts: dict[str, dt.datetime] = {}
    attempts: dict[str, dt.datetime] = {}
    for result_root in (
        root / ".survey/work-queue/claim-results",
        root / ".survey/work-queue/archive/transport/claim-results",
    ):
        if not result_root.is_dir():
            continue
        for path in result_root.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict) or value.get("worker_id") != worker_id:
                continue
            for item in value.get("assignments") or []:
                if not isinstance(item, dict):
                    continue
                attempt_id = item.get("attempt_id")
                claimed_at = _time(item.get("claimed_at"))
                if not isinstance(attempt_id, str) or not attempt_id or claimed_at is None:
                    continue
                all_worker_attempts[attempt_id] = claimed_at
                if claimed_at >= started_at:
                    attempts[attempt_id] = claimed_at

    now = dt.datetime.now(dt.timezone.utc)
    for current in claim_state.current_claims(root, now).values():
        if not isinstance(current, dict) or not current.get("active"):
            continue
        if current.get("worker_id") != worker_id:
            continue
        attempt_id = current.get("attempt_id")
        claimed_at = _time(current.get("claimed_at")) or started_at
        if isinstance(attempt_id, str) and attempt_id:
            all_worker_attempts.setdefault(attempt_id, claimed_at)
            attempts.setdefault(attempt_id, claimed_at)

    # Even if claim-results have already been compacted, an unresolved immutable
    # descriptor identifies its owning worker directly. Recover that pending attempt
    # from the descriptor itself rather than making liveness depend on claim history.
    descriptor_fallback_time = started_at - dt.timedelta(seconds=1)
    for kind in ("research", "audit"):
        submissions = root / ".survey/work-queue/submissions" / kind
        results = root / ".survey/work-queue/results" / kind
        if not submissions.is_dir():
            continue
        for path in submissions.glob("*.json"):
            descriptor = _read(path, {})
            if not isinstance(descriptor, dict) or descriptor.get("worker_id") != worker_id:
                continue
            attempt_id = descriptor.get("attempt_id")
            if not isinstance(attempt_id, str) or not attempt_id:
                continue
            result = _read(results / path.name, {})
            status = str(result.get("job_status") or "").lower() if isinstance(result, dict) else ""
            settled = bool(
                isinstance(result, dict)
                and result.get("attempt_id") == attempt_id
                and (
                    status in {"completed", "blocked", "deferred", "rejected"}
                    or (result.get("ok") is False and result.get("retryable") is not True)
                )
            )
            if settled:
                continue
            all_worker_attempts.setdefault(attempt_id, descriptor_fallback_time)
            attempts.setdefault(attempt_id, descriptor_fallback_time)

    # A descriptor may outlive its claim. Keep unresolved immutable submissions for
    # this worker visible across run boundaries so pending results cannot disappear.
    for kind in ("research", "audit"):
        submissions = root / ".survey/work-queue/submissions" / kind
        results = root / ".survey/work-queue/results" / kind
        if submissions.is_dir():
            for path in submissions.glob("*.json"):
                descriptor = _read(path, {})
                if not isinstance(descriptor, dict):
                    continue
                attempt_id = descriptor.get("attempt_id")
                if not isinstance(attempt_id, str) or attempt_id not in all_worker_attempts:
                    continue
                result = _read(results / path.name, {})
                status = str(result.get("job_status") or "").lower() if isinstance(result, dict) else ""
                settled = bool(
                    isinstance(result, dict)
                    and result.get("attempt_id") == attempt_id
                    and (
                        status in {"completed", "blocked", "deferred", "rejected"}
                        or (result.get("ok") is False and result.get("retryable") is not True)
                    )
                )
                if not settled:
                    attempts.setdefault(attempt_id, all_worker_attempts[attempt_id])

    # A carry-over claim may be submitted and released before the next run-state
    # snapshot. Recover it by exact attempt identity when its result was processed
    # during this invocation.
    for kind in ("research", "audit"):
        folder = root / ".survey/work-queue/results" / kind
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            result = _read(path, {})
            if not isinstance(result, dict):
                continue
            attempt_id = result.get("attempt_id")
            processed_at = _time(result.get("processed_at"))
            if (
                isinstance(attempt_id, str)
                and attempt_id in all_worker_attempts
                and processed_at is not None
                and processed_at >= started_at
            ):
                attempts.setdefault(attempt_id, all_worker_attempts[attempt_id])
    return attempts

def _descriptor_for_attempt(root: Path, kind: str, attempt_id: str) -> Path | None:
    """Resolve the canonical <attempt_id>.json descriptor, with read-only legacy fallback."""
    folder = root / ".survey/work-queue/submissions" / kind
    canonical = folder / f"{attempt_id}.json"
    if canonical.is_file():
        return canonical
    if not folder.is_dir():
        return None
    matches: list[Path] = []
    for path in folder.glob("*.json"):
        value = _read(path, {})
        if isinstance(value, dict) and value.get("attempt_id") == attempt_id:
            matches.append(path)
    return matches[0] if len(matches) == 1 else None


def _run_submission_state(
    root: Path,
    attempts: dict[str, dt.datetime],
    started_at: dt.datetime,
) -> dict[str, Any]:
    completed = 0
    completed_ids: list[str] = []
    retryable_ids: list[str] = []
    repair_required_ids: list[str] = []
    pending: list[tuple[dt.datetime, str]] = []
    submitted: list[tuple[dt.datetime, str]] = []
    terminal: list[tuple[dt.datetime, str]] = []
    facts: dict[str, dict[str, Any]] = {}

    for attempt_id, claimed_at in attempts.items():
        found_descriptor = False
        for kind in ("research", "audit"):
            descriptor_path = _descriptor_for_attempt(root, kind, attempt_id)
            if descriptor_path is None:
                continue
            found_descriptor = True
            submitted.append((claimed_at, attempt_id))
            fact: dict[str, Any] = {
                "attempt_id": attempt_id,
                "kind": kind,
                "claimed_at": claimed_at.astimezone(dt.timezone.utc).isoformat(),
                "submitted": True,
                "descriptor_path": descriptor_path.relative_to(root).as_posix(),
            }
            descriptor = _read(descriptor_path, {})
            if isinstance(descriptor, dict):
                fact["job_id"] = descriptor.get("job_id")
                fact["worker_id"] = descriptor.get("worker_id")
                fact["run_key"] = descriptor.get("run_key")
            result = _read(root / ".survey/work-queue/results" / kind / descriptor_path.name, {})
            if not isinstance(result, dict) or result.get("attempt_id") != attempt_id:
                pending.append((claimed_at, attempt_id))
                fact["pending"] = True
                fact["retryable"] = False
                facts[attempt_id] = fact
                continue
            retryable = result.get("ok") is False and result.get("retryable") is True
            if retryable:
                pending.append((claimed_at, attempt_id))
                retryable_ids.append(attempt_id)
                fact["pending"] = True
                fact["retryable"] = True
                fact["processed_at"] = result.get("processed_at")
                fact["job_status"] = str(result.get("job_status") or "none").lower()
                facts[attempt_id] = fact
                continue
            processed_at = _time(result.get("processed_at")) or claimed_at
            status = str(result.get("job_status") or "none").lower()
            fact["pending"] = False
            fact["retryable"] = False
            fact["repair_required"] = result.get("repair_required") is True
            fact["processed_at"] = processed_at.astimezone(dt.timezone.utc).isoformat()
            fact["job_status"] = status
            fact["completed"] = bool(result.get("ok") is True and status == "completed")
            if fact["repair_required"]:
                repair_required_ids.append(attempt_id)
            if fact["completed"] and processed_at >= started_at:
                completed += 1
                completed_ids.append(attempt_id)
            if status in {"completed", "blocked", "deferred", "rejected"}:
                terminal.append((processed_at, status))
            facts[attempt_id] = fact
        if not found_descriptor:
            continue

    pipeline_ahead_count = 0
    if pending:
        earliest_pending_time, _ = min(pending)
        pipeline_ahead_count = sum(1 for when, _ in submitted if when > earliest_pending_time)

    terminal.sort()
    return {
        "research_audit_completed_this_invocation": completed,
        "submission_state_checked": True,
        "submission_result_pending": bool(pending),
        "pipeline_ahead_count": pipeline_ahead_count,
        "last_terminal_job_status": terminal[-1][1] if terminal else "none",
        "submitted_attempt_ids": [attempt for _, attempt in sorted(submitted)],
        "pending_attempt_ids": [attempt for _, attempt in sorted(pending)],
        "completed_attempt_ids": sorted(set(completed_ids)),
        "retryable_attempt_ids": sorted(set(retryable_ids)),
        "repair_required_attempt_ids": sorted(set(repair_required_ids)),
        "attempt_facts": facts,
    }


def _research_preflight_overlap_states(root: Path) -> dict[str, dict[str, Any]]:
    """Classify the newest quality-preflight request for each Research/Audit attempt.

    A pending or passing exact-blob preflight means the paper content is frozen:
    there is no useful content work on that paper until Actions returns or the
    descriptor materializes. Such attempts may be parked temporarily so a standby
    paper can become the sole content foreground. A failed latest preflight is never
    parked; it must return to foreground repair.
    """
    request_root = root / ".survey/work-queue/research-preflight/requests"
    result_root = root / ".survey/work-queue/research-preflight/results"
    if not request_root.is_dir():
        return {}

    candidates: dict[str, list[dict[str, Any]]] = {}
    relative_paths: list[str] = []
    for path in request_root.glob("*.json"):
        request = _read(path, {})
        if not isinstance(request, dict):
            continue
        attempt_id = str(request.get("attempt_id") or "").strip()
        job_id = str(request.get("job_id") or "").strip()
        if not attempt_id or not job_id:
            continue
        relative = path.relative_to(root).as_posix()
        relative_paths.append(relative)
        result = _read(result_root / path.name, {})
        if not isinstance(result, dict) or result.get("request_id") != path.stem:
            state = "pending"
        elif result.get("ok") is True and result.get("preflight_passed") is True:
            state = "passed_waiting_descriptor"
        else:
            state = "repair_required"

        requested = _time(request.get("requested_at"))
        if requested is None:
            requested = _time(request.get("actual_invocation_start"))
        stem = path.stem
        revision = -1
        tail = stem.rsplit("-r", 1)
        if len(tail) == 2 and tail[1].isdigit():
            revision = int(tail[1])
        candidates.setdefault(attempt_id, []).append(
            {
                "attempt_id": attempt_id,
                "job_id": job_id,
                "worker_id": str(request.get("worker_id") or "").strip(),
                "run_key": str(request.get("run_key") or "").strip(),
                "kind": str(request.get("kind") or "").strip(),
                "request_id": stem,
                "request_path": relative,
                "requested_at": requested,
                "revision": revision,
                "state": state,
            }
        )

    introduction = _git_introduction_order(root, relative_paths)
    selected: dict[str, dict[str, Any]] = {}
    epoch = dt.datetime.min.replace(tzinfo=dt.timezone.utc)
    for attempt_id, rows in candidates.items():
        rows.sort(
            key=lambda row: (
                row.get("requested_at") or epoch,
                int(introduction.get(str(row.get("request_path") or ""), -1)),
                int(row.get("revision") or -1),
                str(row.get("request_id") or ""),
            )
        )
        selected[attempt_id] = rows[-1]
    return selected



def _claim_state(root: Path, worker_id: str, started_at: dt.datetime) -> dict[str, Any]:
    pending_requests: list[tuple[dt.datetime, str]] = []
    request_root = root / ".survey/work-queue/claim-requests"
    result_root = root / ".survey/work-queue/claim-results"
    now = dt.datetime.now(dt.timezone.utc)
    if request_root.is_dir():
        for path in request_root.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict) or value.get("worker_id") != worker_id:
                continue
            requested = _time(value.get("requested_at"))
            if requested is None or requested < started_at:
                continue
            if not (result_root / path.name).is_file():
                pending_requests.append((requested, path.stem))

    pending_request_ages = {
        request_id: max(int((now - requested).total_seconds()), 0)
        for requested, request_id in pending_requests
    }
    pending_request_times = {
        request_id: requested.astimezone(dt.timezone.utc).isoformat()
        for requested, request_id in pending_requests
    }
    pending_request_ids = [request_id for _, request_id in sorted(pending_requests)]
    oldest_pending_age = max(pending_request_ages.values(), default=0)

    claims = claim_state.current_claims(root, now)
    preflight_states = _research_preflight_overlap_states(root)
    owned_rows: list[dict[str, Any]] = []
    for job_id, current in claims.items():
        if not current.get("active") or current.get("worker_id") != worker_id:
            continue
        attempt_id = current.get("attempt_id")
        kind = str(current.get("kind") or "")
        descriptor_backed = bool(
            isinstance(attempt_id, str)
            and attempt_id
            and kind in {"research", "audit"}
            and _descriptor_for_attempt(root, kind, attempt_id) is not None
        )
        if descriptor_backed:
            continue
        order = current.get("pipeline_order")
        normalized_order = (
            int(order)
            if isinstance(order, int) and not isinstance(order, bool) and int(order) >= 0
            else 1_000_000_000
        )
        claimed_at = str(current.get("claimed_at") or "")
        preflight = (
            preflight_states.get(str(attempt_id))
            if isinstance(attempt_id, str) and attempt_id
            else None
        )
        # Never let a stale/corrupt preflight for another job or worker freeze this
        # claim. Attempt IDs are expected to be unique, but exact identity matching
        # keeps the overlap optimization fail-closed.
        if isinstance(preflight, dict) and (
            str(preflight.get("job_id") or "") != job_id
            or (
                str(preflight.get("worker_id") or "")
                and str(preflight.get("worker_id") or "") != worker_id
            )
            or (
                str(preflight.get("kind") or "")
                and str(preflight.get("kind") or "") != kind
            )
        ):
            preflight = None
        owned_rows.append(
            {
                "order": normalized_order,
                "claimed_at": claimed_at,
                "job_id": job_id,
                "attempt_id": str(attempt_id or ""),
                "preflight_state": str((preflight or {}).get("state") or ""),
                "preflight_request_id": str((preflight or {}).get("request_id") or ""),
            }
        )

    owned_rows.sort(
        key=lambda row: (
            int(row["order"]),
            str(row["claimed_at"]),
            str(row["job_id"]),
        )
    )
    frozen_states = {"pending", "passed_waiting_descriptor"}
    parked_rows = [
        row for row in owned_rows
        if str(row.get("preflight_state") or "") in frozen_states
    ]
    repair_rows = [
        row for row in owned_rows
        if str(row.get("preflight_state") or "") == "repair_required"
    ]
    active_rows = [
        row for row in owned_rows
        if str(row.get("preflight_state") or "") not in frozen_states
    ]
    active_job_ids = [str(row["job_id"]) for row in active_rows]
    active_claim_count = len(owned_rows)
    preflight_inflight_count = len(parked_rows)
    preflight_pipeline_capacity_remaining = max(
        RESEARCH_PREFLIGHT_PIPELINE_WINDOW - preflight_inflight_count,
        0,
    )
    return {
        "claim_state_checked": True,
        "claim_result_pending": bool(pending_requests),
        "pending_claim_request_ids": pending_request_ids,
        "pending_claim_request_ages_seconds": pending_request_ages,
        "pending_claim_requested_at": pending_request_times,
        "claim_result_pending_age_seconds": oldest_pending_age,
        "claim_monitor_window_seconds": 60,
        "active_assignment": bool(active_job_ids),
        "active_job_ids": active_job_ids,
        "active_claim_count": active_claim_count,
        "claim_window": SCHEDULED_CHAT_CLAIM_WINDOW,
        "claim_refill_threshold": claim_window_policy.refill_threshold(SCHEDULED_CHAT_CLAIM_WINDOW),
        "claim_window_remaining": max(SCHEDULED_CHAT_CLAIM_WINDOW - active_claim_count, 0),
        "foreground_job_id": active_job_ids[0] if active_job_ids else None,
        "standby_job_ids": active_job_ids[1:],
        "preflight_parked_job_ids": [str(row["job_id"]) for row in parked_rows],
        "preflight_parked_attempt_ids": [str(row["attempt_id"]) for row in parked_rows],
        "preflight_parked_states": {
            str(row["job_id"]): str(row["preflight_state"])
            for row in parked_rows
        },
        "preflight_parked_request_ids": {
            str(row["job_id"]): str(row["preflight_request_id"])
            for row in parked_rows
        },
        "preflight_repair_job_ids": [str(row["job_id"]) for row in repair_rows],
        "preflight_repair_attempt_ids": [str(row["attempt_id"]) for row in repair_rows],
        "preflight_inflight_count": preflight_inflight_count,
        "preflight_pipeline_window": RESEARCH_PREFLIGHT_PIPELINE_WINDOW,
        "preflight_pipeline_capacity_remaining": preflight_pipeline_capacity_remaining,
        "preflight_pipeline_saturated": preflight_pipeline_capacity_remaining == 0,
        # The window is an admission limit for starting more preflights, never a
        # license to edit an already frozen third request. If legacy/concurrent
        # state exceeds the bound, freeze all of them and report the overflow.
        "preflight_pipeline_overflow_count": max(
            preflight_inflight_count - RESEARCH_PREFLIGHT_PIPELINE_WINDOW,
            0,
        ),
    }


def _refresh_cached_claim_state(root: Path, value: dict[str, Any]) -> dict[str, Any] | None:
    """Refresh volatile cached claim fields against cheap canonical facts.

    The incremental cache is only an index. A submission delta can occasionally be
    missed (for example for a status-only terminal descriptor). In that case a
    terminal job must not remain an active assignment merely because the cache still
    contains the allocation produced by the earlier claim result.
    """
    claims = dict(value)

    active_jobs: list[str] = []
    for raw_job_id in claims.get("active_job_ids") or []:
        job_id = str(raw_job_id or "").strip()
        if not job_id:
            continue
        job = _read(root / ".survey/work-queue/jobs" / f"{job_id}.json", {})
        status = str(job.get("status") or "").lower() if isinstance(job, dict) else ""
        if status in {"completed", "blocked", "deferred", "rejected"}:
            continue
        active_jobs.append(job_id)
    claim_window = max(int(claims.get("claim_window") or SCHEDULED_CHAT_CLAIM_WINDOW), 1)
    claims["active_job_ids"] = active_jobs
    claims["active_assignment"] = bool(active_jobs)
    claims["active_claim_count"] = len(active_jobs)
    claims["claim_window"] = claim_window
    claims["claim_refill_threshold"] = claim_window_policy.refill_threshold(claim_window)
    claims["claim_window_remaining"] = max(claim_window - len(active_jobs), 0)
    claims["foreground_job_id"] = active_jobs[0] if active_jobs else None
    claims["standby_job_ids"] = active_jobs[1:]

    if claims.get("claim_result_pending") is not True:
        return claims
    requested = claims.get("pending_claim_requested_at")
    if not isinstance(requested, dict):
        return None
    now = dt.datetime.now(dt.timezone.utc)
    ages: dict[str, int] = {}
    for request_id, raw in requested.items():
        when = _time(raw)
        if when is None:
            return None
        ages[str(request_id)] = max(int((now - when).total_seconds()), 0)
    claims["pending_claim_request_ages_seconds"] = ages
    claims["claim_result_pending_age_seconds"] = max(ages.values(), default=0)
    claims["claim_result_pending"] = bool(ages)
    claims["pending_claim_request_ids"] = sorted(ages)
    return claims


def _discovery_rounds(root: Path, run_key: str) -> tuple[int, dict[str, Any]]:
    state = _read(root / ".survey/work-queue/discovery-state.json", {}) or {}
    history = state.get("history") if isinstance(state.get("history"), list) else []
    identities: set[str] = set()
    for row in history:
        if not isinstance(row, dict) or str(row.get("run_key") or "") != run_key:
            continue
        if not (row.get("round_accounted") is True or row.get("round_complete") is True):
            continue
        identity = str(row.get("round_identity") or row.get("round") or row.get("source_submission") or "")
        if identity:
            identities.add(identity)
    selector = select_discovery_direction.decide(state, run_key)
    return len(identities), selector


def _discovery_precheck_route_key(request: Any) -> tuple[str, str] | None:
    """Return a stable fixed-source identity for one schema-v3 precheck request."""
    if not isinstance(request, dict):
        return None
    provider = str(request.get("provider") or "").strip().casefold()
    source_url = str(request.get("source_url") or "").strip()
    if not provider or not source_url:
        return None
    return provider, source_url


def _git_introduction_order(root: Path, relative_paths: list[str]) -> dict[str, int]:
    """Return first-add commit order for selected durable artifacts.

    Discovery retries intentionally preserve failed immutable artifacts.  File
    contents alone therefore cannot distinguish a current failure from historical
    evidence that a later canonical attempt has already superseded.  The run-state
    workflow checks out full history (fetch-depth: 0), so use one local git query to
    order only the current run's relevant artifacts.  Non-git test fixtures fall
    back to exact fixed-source matching.
    """
    import subprocess

    paths = sorted({str(Path(path).as_posix()) for path in relative_paths if str(path).strip()})
    if not paths:
        return {}
    proc = subprocess.run(
        [
            "git",
            "log",
            "--reverse",
            "--diff-filter=A",
            "--format=commit:%H",
            "--name-only",
            "--",
            *paths,
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if proc.returncode != 0:
        return {}

    wanted = set(paths)
    order: dict[str, int] = {}
    commit_order = -1
    for raw in proc.stdout.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("commit:"):
            commit_order += 1
            continue
        if line in wanted and line not in order:
            order[line] = commit_order
    return order


def _iter_discovery_submission_paths(submission_root: Path) -> list[Path]:
    """Return current nested Discovery descriptors plus legacy root-level ones."""
    seen: set[str] = set()
    ordered: list[Path] = []
    canonical = submission_root / "discovery"
    if canonical.is_dir():
        for path in sorted(canonical.glob("*.json")):
            if path.name in seen:
                continue
            seen.add(path.name)
            ordered.append(path)
    if submission_root.is_dir():
        for path in sorted(submission_root.glob("*.json")):
            if path.name in seen:
                continue
            seen.add(path.name)
            ordered.append(path)
    return ordered


def _discovery_async_state(root: Path, run_key: str) -> dict[str, Any]:
    request_root = root / ".survey/work-queue/discovery-precheck/requests"
    precheck_result_root = root / ".survey/work-queue/discovery-precheck/results"
    submission_root = root / ".survey/work-queue/submissions"
    result_root = root / ".survey/work-queue/results"

    state = _read(root / ".survey/work-queue/discovery-state.json", {}) or {}
    history = state.get("history") if isinstance(state.get("history"), list) else []
    accounted_prechecks = {
        str(row.get("precheck_request_id") or "")
        for row in history
        if isinstance(row, dict)
        and str(row.get("run_key") or "") == run_key
        and (row.get("round_accounted") is True or row.get("round_complete") is True)
        and str(row.get("precheck_request_id") or "")
    }
    accounted_rounds = {
        str(row.get("round_identity") or row.get("round") or row.get("source_submission") or "")
        for row in history
        if isinstance(row, dict)
        and str(row.get("run_key") or "") == run_key
        and (row.get("round_accounted") is True or row.get("round_complete") is True)
        and str(row.get("round_identity") or row.get("round") or row.get("source_submission") or "")
    }

    pending_prechecks: list[str] = []
    evaluation_pending: list[str] = []
    recovery_required: list[str] = []
    superseded_failures: list[str] = []
    successful_prechecks: dict[str, dict[str, Any]] = {}
    precheck_requests: dict[str, dict[str, Any]] = {}
    failed_events: list[dict[str, Any]] = []
    progress_events: list[dict[str, Any]] = []
    submission_progress: dict[str, dict[str, Any]] = {}
    submission_rows: list[dict[str, Any]] = []

    if request_root.is_dir():
        for path in request_root.glob("*.json"):
            request = _read(path, {})
            if not isinstance(request, dict) or str(request.get("run_key") or "") != run_key:
                continue
            precheck_requests[path.stem] = request
            result_path = precheck_result_root / path.name
            result = _read(result_path, {})
            if not isinstance(result, dict) or result.get("request_id") != path.stem:
                pending_prechecks.append(path.stem)
                continue
            route_key = _discovery_precheck_route_key(request)
            relative_result = result_path.relative_to(root).as_posix()
            if result.get("ok") is True and result.get("evaluation_allowed") is True:
                successful_prechecks[path.stem] = result
                progress_events.append(
                    {
                        "target": f"precheck:{path.stem}",
                        "path": relative_result,
                        "route_key": route_key,
                    }
                )
            elif result.get("ok") is False:
                failed_events.append(
                    {
                        "target": f"precheck:{path.stem}",
                        "path": relative_result,
                        "route_key": route_key,
                        "precheck_id": path.stem,
                        "round_id": None,
                    }
                )

    pending_submissions: list[str] = []
    for path in _iter_discovery_submission_paths(submission_root):
        submission = _read(path, {})
        if not isinstance(submission, dict) or submission.get("operation") != "submit_discovery_round":
            continue
        stats = submission.get("discovery_stats") if isinstance(submission.get("discovery_stats"), dict) else {}
        submission_run_key = str(submission.get("run_key") or stats.get("run_key") or "")
        if submission_run_key != run_key:
            continue
        proof = submission.get("discovery_precheck") if isinstance(submission.get("discovery_precheck"), dict) else {}
        precheck_id = str(
            proof.get("request_id")
            or submission.get("precheck_request_id")
            or stats.get("precheck_request_id")
            or ""
        )
        round_id = str(stats.get("round") or "").strip() or None
        route_key = _discovery_precheck_route_key(precheck_requests.get(precheck_id))
        relative_submission = path.relative_to(root).as_posix()

        if precheck_id:
            progress = submission_progress.setdefault(
                precheck_id,
                {"expected": 1, "indices": set(), "paths": []},
            )
            expected = stats.get("round_submission_count", 1)
            index = stats.get("round_submission_index", 1)
            if isinstance(expected, int) and not isinstance(expected, bool):
                progress["expected"] = max(int(progress["expected"]), max(expected, 1))
            if isinstance(index, int) and not isinstance(index, bool) and index >= 1:
                progress["indices"].add(index)
            progress["paths"].append(path.stem)

        result_path = result_root / path.name
        result = _read(result_path, {})
        row = {
            "stem": path.stem,
            "submission_path": relative_submission,
            "result_path": result_path.relative_to(root).as_posix(),
            "precheck_id": precheck_id,
            "round_id": round_id,
            "route_key": route_key,
            "result": result,
        }
        submission_rows.append(row)

        if not result_path.is_file() or not isinstance(result, dict) or not result:
            pending_submissions.append(path.stem)
        elif result.get("ok") is False:
            failed_events.append(
                {
                    "target": f"submission:{path.stem}",
                    "path": row["result_path"],
                    "route_key": route_key,
                    "precheck_id": precheck_id or None,
                    "round_id": round_id,
                }
            )
        elif result.get("ok") is True:
            progress_events.append(
                {
                    "target": f"submission:{path.stem}",
                    "path": row["result_path"],
                    "route_key": route_key,
                }
            )

        if (
            (round_id and round_id in accounted_rounds)
            or (precheck_id and precheck_id in accounted_prechecks)
        ):
            progress_events.append(
                {
                    "target": f"accounted:{path.stem}",
                    "path": relative_submission,
                    "route_key": route_key,
                }
            )

    for request_id in successful_prechecks:
        if request_id in accounted_prechecks:
            continue
        progress = submission_progress.get(request_id)
        if progress is None:
            evaluation_pending.append(request_id)
            continue
        if len(progress["indices"]) < int(progress["expected"]):
            evaluation_pending.append(request_id)

    # Historical immutable failures must remain as audit evidence, but they must
    # not poison the continuation gate forever.  A failure is superseded once a
    # later canonical success/progress artifact exists in the same run.  When git
    # history is unavailable (unit-test fixtures), exact fixed-source replacement
    # provides a conservative fallback.
    paths_for_order = [str(event.get("path") or "") for event in failed_events + progress_events]
    introduction_order = _git_introduction_order(root, paths_for_order)
    successful_routes = {
        event.get("route_key")
        for event in progress_events
        if event.get("route_key") is not None
    }
    progress_orders = [
        introduction_order[path]
        for path in (str(event.get("path") or "") for event in progress_events)
        if path in introduction_order
    ]
    latest_progress_order = max(progress_orders, default=None)

    for event in failed_events:
        target = str(event["target"])
        precheck_id = str(event.get("precheck_id") or "")
        round_id = str(event.get("round_id") or "")
        if (
            (precheck_id and precheck_id in accounted_prechecks)
            or (round_id and round_id in accounted_rounds)
        ):
            superseded_failures.append(target)
            continue

        path = str(event.get("path") or "")
        failure_order = introduction_order.get(path)
        superseded = bool(
            failure_order is not None
            and latest_progress_order is not None
            and latest_progress_order > failure_order
        )
        if (
            not superseded
            and failure_order is None
            and event.get("route_key") is not None
            and event.get("route_key") in successful_routes
        ):
            superseded = True

        if superseded:
            superseded_failures.append(target)
        else:
            recovery_required.append(target)

    evaluation_queue: list[dict[str, Any]] = []
    for request_id in evaluation_pending:
        request = precheck_requests.get(request_id)
        result = successful_prechecks.get(request_id)
        if not isinstance(request, dict) or not isinstance(result, dict):
            continue
        allowed_records = result.get("allowed_records") if isinstance(result.get("allowed_records"), list) else []
        result_records = result.get("results") if isinstance(result.get("results"), list) else []
        direction = discovery_preload_queue._direction(
            str(request.get("provider") or ""),
            str(request.get("source_url") or ""),
            request.get("citation_direction"),
        )
        evaluation_queue.append(
            {
                "request_id": request_id,
                "request_path": (
                    Path(".survey/work-queue/discovery-precheck/requests") / f"{request_id}.json"
                ).as_posix(),
                "result_path": (
                    Path(".survey/work-queue/discovery-precheck/results") / f"{request_id}.json"
                ).as_posix(),
                "provider": request.get("provider"),
                "source_url": request.get("source_url"),
                "axis": request.get("axis"),
                "citation_direction": direction,
                "requested_at": request.get("requested_at"),
                "allowed_record_count": len(allowed_records),
                "result_record_count": len(result_records),
                "receipt": result.get("receipt"),
                "submission_root": ".survey/work-queue/submissions/discovery",
            }
        )
    evaluation_queue.sort(
        key=lambda row: (
            str(row.get("requested_at") or ""),
            str(row.get("request_id") or ""),
        )
    )

    inflight_precheck_ids = set(pending_prechecks) | set(evaluation_pending)
    pending_submission_set = set(pending_submissions)
    for row in submission_rows:
        if row.get("stem") in pending_submission_set and row.get("precheck_id"):
            inflight_precheck_ids.add(str(row["precheck_id"]))
    inflight_directions: set[str] = set()
    for precheck_id in inflight_precheck_ids:
        request = precheck_requests.get(precheck_id)
        if not isinstance(request, dict):
            continue
        direction = discovery_preload_queue._direction(
            str(request.get("provider") or ""),
            str(request.get("source_url") or ""),
            request.get("citation_direction"),
        )
        if direction in {"backward", "forward", "normal"}:
            inflight_directions.add(direction)

    return {
        "discovery_precheck_result_pending": bool(pending_prechecks),
        "pending_discovery_precheck_request_ids": sorted(pending_prechecks),
        "discovery_submission_result_pending": bool(pending_submissions),
        "pending_discovery_submission_ids": sorted(pending_submissions),
        "discovery_evaluation_pending": bool(evaluation_pending),
        "discovery_evaluation_request_ids": sorted(evaluation_pending),
        "discovery_evaluation_queue": evaluation_queue,
        "discovery_recovery_required": bool(recovery_required),
        "discovery_recovery_targets": sorted(recovery_required),
        "discovery_superseded_failure_targets": sorted(superseded_failures),
        "discovery_inflight_precheck_ids": sorted(inflight_precheck_ids),
        "discovery_inflight_round_count": len(inflight_precheck_ids),
        "discovery_inflight_directions": sorted(inflight_directions),
    }

def _independent_work(root: Path, work_mode: str, selector: dict[str, Any]) -> bool:
    if work_mode == "discovery":
        return bool(selector.get("next_direction"))
    snap = _next_jobs(root)
    claiming = snap.get("claiming") if isinstance(snap.get("claiming"), dict) else {}
    claimable = claiming.get("claimable")
    if isinstance(claimable, int) and not isinstance(claimable, bool):
        return claimable > 0
    return _candidate_inventory(root) > 0


def _next_work_packet(
    root: Path,
    *,
    worker_id: str,
    gate: dict[str, Any],
    finalization_gate: dict[str, Any],
    claims: dict[str, Any],
    discovery_async: dict[str, Any],
    discovery_preload: dict[str, Any] | None,
    discovery_fallback_source: dict[str, Any] | None,
    discovery_pipeline_preload: dict[str, Any] | None,
) -> dict[str, Any] | None:
    permit = bool((finalization_gate.get("finalization_permit") or {}).get("issued"))
    if permit:
        return None

    action = str(
        finalization_gate.get("next_action")
        or gate.get("required_action")
        or ""
    ).strip()
    if not action:
        return None

    if action == "CONTINUE_DISCOVERY_ROUND":
        queue = discovery_async.get("discovery_evaluation_queue")
        if isinstance(queue, list) and queue and isinstance(queue[0], dict):
            return {
                "kind": "discovery_evaluation",
                "action": action,
                **dict(queue[0]),
            }

    if action == "CONTINUE_DISCOVERY_PIPELINE" and isinstance(discovery_pipeline_preload, dict):
        return {
            "kind": "discovery_pipeline_preload",
            "action": action,
            **dict(discovery_pipeline_preload),
        }

    if action == "DISCOVER_AGAIN":
        if isinstance(discovery_preload, dict):
            return {
                "kind": "discovery_direct_take",
                "action": action,
                **dict(discovery_preload),
            }
        if isinstance(discovery_fallback_source, dict):
            return {
                "kind": "discovery_fixed_source_precheck",
                "action": action,
                **dict(discovery_fallback_source),
            }

    if action in {"CONTINUE_ASSIGNED_WORK", "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY"}:
        job_id = str(claims.get("foreground_job_id") or "")
        if job_id:
            job_path = Path(".survey/work-queue/jobs") / f"{job_id}.json"
            claim_path = Path(".survey/work-queue/claims") / f"{job_id}.json"
            job = _read(root / job_path, {}) or {}
            claim = _read(root / claim_path, {}) or {}
            packet: dict[str, Any] = {
                "kind": "research_audit_foreground",
                "action": action,
                "job_id": job_id,
                "job_path": job_path.as_posix(),
                "claim_path": claim_path.as_posix(),
            }
            if isinstance(job, dict):
                for key in ("type", "canonical_id", "title", "source_url", "paper_path"):
                    if job.get(key) is not None:
                        packet[key] = job.get(key)
            if isinstance(claim, dict):
                for key in ("claim_id", "attempt_id", "kind", "record_bank", "record_bank_root"):
                    if claim.get(key) is not None:
                        packet[key] = claim.get(key)
            if action == "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY":
                packet["refill_standby"] = True
            return packet

    if action == "CLAIM_NEXT_RESEARCH_AUDIT":
        return {
            "kind": "research_audit_claim",
            "action": action,
            "worker_id": worker_id,
            "hot_dispatch_path": ".survey/work-queue/hot-dispatch.json",
            "selection_order": [
                f"research_resume.{worker_id}[0]",
                "research[0]",
            ],
        }

    if action == "RECOVER_DISCOVERY_SUBMISSION":
        targets = discovery_async.get("discovery_recovery_targets")
        target = str(targets[0]) if isinstance(targets, list) and targets else ""
        packet: dict[str, Any] = {
            "kind": "discovery_recovery",
            "action": action,
            "target": target,
        }
        if target.startswith("submission:"):
            stem = target.split(":", 1)[1]
            packet["submission_path"] = (
                Path(".survey/work-queue/submissions/discovery") / f"{stem}.json"
            ).as_posix()
            packet["result_path"] = (
                Path(".survey/work-queue/results/discovery") / f"{stem}.json"
            ).as_posix()
        elif target.startswith("precheck:"):
            request_id = target.split(":", 1)[1]
            packet["precheck_request_path"] = (
                Path(".survey/work-queue/discovery-precheck/requests") / f"{request_id}.json"
            ).as_posix()
            packet["precheck_result_path"] = (
                Path(".survey/work-queue/discovery-precheck/results") / f"{request_id}.json"
            ).as_posix()
        return packet

    if action == "RUN_WAIT_MICROTASK_AND_RECHECK":
        return {
            "kind": "productive_wait",
            "action": action,
            "wait_targets": list(finalization_gate.get("wait_targets") or []),
            "wait_microtasks": list(finalization_gate.get("wait_microtasks") or []),
        }

    if action == "WAIT_FOR_READY_RESEARCH_AUDIT":
        return {
            "kind": "productive_wait",
            "action": action,
            "queue_path": ".survey/work-queue/next-jobs.json",
            "wait_microtasks": list(finalization_gate.get("wait_microtasks") or []),
        }

    return {
        "kind": "canonical_action",
        "action": action,
    }


def derive(root: Path, request: dict[str, Any], *, force_canonical: bool = False) -> dict[str, Any]:
    global READ_COUNT
    root = root.resolve()
    perf_started = time.perf_counter()
    read_started = READ_COUNT
    request = dict(request)
    raw_invocation_start = request.get("actual_invocation_start")
    started_at, start_recovery = run_state_cache.normalize_invocation_start(raw_invocation_start)
    if started_at is None:
        raise ValueError(
            "actual_invocation_start must be offset-aware and cannot be materially in the future"
        )
    request["actual_invocation_start"] = started_at.isoformat()
    if start_recovery is not None:
        request["actual_invocation_start_original"] = str(raw_invocation_start).strip()
        request["actual_invocation_start_recovery"] = start_recovery

    cached = None if force_canonical else run_state_cache.get_run(root, request)
    cached_claims = (
        _refresh_cached_claim_state(root, cached.get("claims", {}))
        if isinstance(cached, dict)
        else None
    )
    if cached is not None and cached_claims is None:
        cached = None
    cache_hit = cached is not None
    route_source = "incremental_cache" if cached is not None else "canonical_inventory"
    if cached is not None:
        inventory = int(cached["candidate_inventory"])
        work_mode = str(cached["work_mode"])
        submission = dict(cached["submission"])
        # Research preflight parking depends on durable request/result facts that
        # are intentionally outside the incremental cache. Re-derive only claim
        # state here so a newly pending/failed preflight can immediately park or
        # restore the correct content foreground without a full canonical rebuild.
        claims = (
            _claim_state(root, request["worker_id"], started_at)
            if work_mode == "research"
            else (cached_claims or {})
        )
        if claims != cached.get("claims"):
            # Persist cheap canonical reconciliation so a missed descriptor delta
            # cannot leave the durable performance cache advertising a terminal job
            # as active on every later snapshot.
            run_state_cache.update_claims(root, request, claims)
    else:
        frozen = _frozen_route(root, request["run_key"])
        direct_inventory = request.get("candidate_inventory_at_start")
        direct_mode = request.get("work_mode_at_start")
        recovered_mode = request.get("recovered_work_mode_at_start")
        recovery_source = request.get("route_recovery_source")
        if request["scheduled_slot"] == "0830":
            inventory = _candidate_inventory(root) if frozen is None else frozen[0]
            work_mode = "maintenance"
            route_source = "maintenance"
        elif frozen is not None:
            inventory, work_mode = frozen
            route_source = "frozen_run_state"
        elif (
            isinstance(direct_inventory, int)
            and not isinstance(direct_inventory, bool)
            and direct_mode in {"research", "discovery"}
        ):
            inventory = int(direct_inventory)
            work_mode = str(direct_mode)
            route_source = "hot_dispatch_direct_start"
        elif recovery_source == "discovery_precheck_identity" and recovered_mode == "discovery":
            # A durable Discovery precheck proves that this invocation had already
            # entered Discovery even if the worker omitted its initial run-state
            # request. Preserve that mode rather than re-routing from a later queue
            # inventory snapshot, which may have crossed the threshold meanwhile.
            inventory = _candidate_inventory(root)
            work_mode = "discovery"
            route_source = "discovery_precheck_recovery"
        elif recovery_source == "research_preflight_identity" and recovered_mode == "research":
            # A durable exact-blob Research/Audit preflight proves that this run
            # was already in Research mode. This recovery is used only when the
            # incremental cache and an earlier run-state snapshot are unavailable.
            inventory = _candidate_inventory(root)
            work_mode = "research"
            route_source = "research_preflight_recovery"
        else:
            inventory = _candidate_inventory(root)
            work_mode = "research" if inventory >= claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD else "discovery"
            route_source = "canonical_inventory"

        attempts = _run_attempts(root, request["worker_id"], started_at)
        submission = _run_submission_state(root, attempts, started_at)
        claims = _claim_state(root, request["worker_id"], started_at)
        run_state_cache.store_canonical_snapshot(
            root,
            request,
            candidate_inventory=inventory,
            work_mode=work_mode,
            claims=claims,
            submission=submission,
        )

    discovery_rounds, selector = _discovery_rounds(root, request["run_key"])
    discovery_async = _discovery_async_state(root, request["run_key"])
    selector_direction = str(selector.get("next_direction") or "")
    discovery_preload = None
    discovery_fallback_source = None
    if (
        work_mode == "discovery"
        and selector_direction in {"backward", "forward", "normal"}
    ):
        discovery_preload = discovery_preload_queue.pick_available(
            root,
            direction=selector_direction,
        )
        if discovery_preload is None:
            discovery_fallback_source = discovery_preload_queue.fallback_source(
                root,
                direction=selector_direction,
            )

    def decorate_discovery_packet(value: dict[str, Any] | None) -> dict[str, Any] | None:
        if not isinstance(value, dict) or not value.get("preload_id"):
            return None
        packet = dict(value)
        preload_id = str(packet["preload_id"])
        packet["take_path"] = (
            Path(".survey/work-queue/discovery-preload/claims") / f"{preload_id}.json"
        ).as_posix()
        packet["take_result_path"] = (
            Path(".survey/work-queue/direct-take-results/discovery") / f"{preload_id}.json"
        ).as_posix()
        return packet

    discovery_preload = decorate_discovery_packet(discovery_preload)

    now = dt.datetime.now(dt.timezone.utc)
    deadline = started_at + dt.timedelta(seconds=3600)
    seconds_to_deadline = max(int((deadline - now).total_seconds()), 0)

    discovery_pipeline_preload = None
    inflight_count = int(discovery_async.get("discovery_inflight_round_count") or 0)
    inflight_directions = set(discovery_async.get("discovery_inflight_directions") or [])
    async_wait_exists = bool(
        discovery_async.get("discovery_precheck_result_pending")
        or discovery_async.get("discovery_submission_result_pending")
    )
    pipeline_eligible = bool(
        work_mode == "discovery"
        and seconds_to_deadline > 600
        and async_wait_exists
        and not discovery_async.get("discovery_evaluation_pending")
        and not discovery_async.get("discovery_recovery_required")
        and inflight_count < DISCOVERY_PIPELINE_WINDOW
    )
    if pipeline_eligible:
        if selector_direction == "backward":
            directions = ["forward", "backward"]
        elif selector_direction == "forward":
            directions = ["backward", "forward"]
        else:
            directions = ["backward", "forward"]
        directions = sorted(
            directions,
            key=lambda direction: (direction in inflight_directions, directions.index(direction)),
        )
        for direction in directions:
            rows = discovery_preload_queue.available_preloads(
                root,
                direction=direction,
                limit=16,
            )
            productive = next(
                (
                    row
                    for row in rows
                    if int(row.get("preload_unseen_result_count") or 0) > 0
                ),
                None,
            )
            if productive is not None:
                discovery_pipeline_preload = decorate_discovery_packet(productive)
                break
    discovery_pipeline_work_available = discovery_pipeline_preload is not None
    requested_runtime = request["runtime_condition"]
    runtime = requested_runtime
    runtime_condition_ignored_reason = None
    if runtime == "handoff_guard":
        runtime = "none"
        runtime_condition_ignored_reason = "handoff_guard_is_derived_from_deadline"
    elif runtime in {"github_read_unavailable", "durable_transports_unavailable", "transport_unrecoverable"}:
        if not request.get("runtime_condition_confirmed") or int(request.get("runtime_condition_attempts") or 0) < 2:
            runtime = "none"
            runtime_condition_ignored_reason = "transient_runtime_condition_not_confirmed_after_two_attempts"
    elif runtime == "platform_context_limit":
        explicit_platform_rejection = bool(
            request.get("runtime_condition_confirmed")
            and int(request.get("runtime_condition_attempts") or 0) >= 1
            and request.get("runtime_condition_event") == PLATFORM_CONTEXT_LIMIT_EVENT
            and str(request.get("runtime_condition_detail") or "").strip()
        )
        if not explicit_platform_rejection:
            runtime = "none"
            runtime_condition_ignored_reason = (
                "platform_limit_requires_explicit_platform_tool_call_rejection_evidence"
            )

    # 600s is only a no-new-independent-work window. The final 180s is the
    # unconditional handoff condition.
    if seconds_to_deadline <= 180:
        runtime = "handoff_guard"
        runtime_condition_ignored_reason = None

    github_read = runtime != "github_read_unavailable"
    durable_unavailable = runtime == "durable_transports_unavailable"
    platform_limit = runtime == "platform_context_limit"
    transport_unrecoverable = runtime == "transport_unrecoverable"
    global_dependency = durable_unavailable or transport_unrecoverable
    independent_work = (
        False
        if global_dependency
        else _independent_work(root, work_mode, selector)
    )

    args = argparse.Namespace(
        github_read=github_read,
        github_write=not durable_unavailable,
        library_writable=not durable_unavailable,
        result_durable=True,
        seed_durable=True,
        unpublished_completed_result=False,
        offline_seed_required=False,
        platform_limit=platform_limit,
        global_dependency=global_dependency,
        independent_work=independent_work,
        active_assignment=claims["active_assignment"],
        active_claim_count=claims.get("active_claim_count", 0),
        claim_window=claims.get("claim_window", SCHEDULED_CHAT_CLAIM_WINDOW),
        claim_refill_threshold=claims.get(
            "claim_refill_threshold",
            claim_window_policy.refill_threshold(
                int(claims.get("claim_window") or SCHEDULED_CHAT_CLAIM_WINDOW)
            ),
        ),
        claim_window_remaining=claims.get("claim_window_remaining", SCHEDULED_CHAT_CLAIM_WINDOW),
        spillover_work=False,
        can_discover=work_mode == "discovery" and bool(selector.get("next_direction")),
        claim_state_checked=claims["claim_state_checked"],
        claim_result_pending=claims["claim_result_pending"],
        claim_result_pending_age_seconds=claims["claim_result_pending_age_seconds"],
        claim_monitor_window_seconds=claims["claim_monitor_window_seconds"],
        submission_state_checked=submission["submission_state_checked"],
        submission_result_pending=submission["submission_result_pending"],
        pipeline_ahead_count=submission["pipeline_ahead_count"],
        write_failed=False,
        probe="not-run",
        seconds_to_run_deadline=seconds_to_deadline,
        seconds_to_next_scheduled_task=None,
        scheduled_handoff_guard_seconds=600,
        candidate_inventory=inventory,
        work_mode=work_mode if work_mode in {"research", "discovery"} else "research",
        research_audit_completed_this_invocation=submission["research_audit_completed_this_invocation"],
        research_minimum_completions=worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS,
        last_terminal_job_status=submission["last_terminal_job_status"],
        discovery_rounds_completed=discovery_rounds,
        discovery_min_rounds=worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS,
        discovery_exhausted=False,
        next_axis_available=bool(selector.get("next_direction")),
        discovery_precheck_result_pending=discovery_async["discovery_precheck_result_pending"],
        discovery_submission_result_pending=discovery_async["discovery_submission_result_pending"],
        discovery_evaluation_pending=discovery_async["discovery_evaluation_pending"],
        discovery_recovery_required=discovery_async["discovery_recovery_required"],
        discovery_pipeline_work_available=discovery_pipeline_work_available,
    )
    if work_mode == "maintenance":
        maintenance = _read(root / ".survey/work-queue/maintenance-cycle.json", {}) or {}
        completed_at = _time(maintenance.get("last_maintenance_completed_at"))
        maintenance_complete = bool(
            maintenance.get("maintenance_pending") is False
            and completed_at is not None
            and completed_at >= started_at
        )
        gate = (
            {
                "decision": "STOP_RUN",
                "required_action": "FINALIZE",
                "finalization_allowed": True,
                "stop_reasons": ["scheduled_0830_maintenance_complete"],
                "work_mode": "maintenance",
            }
            if maintenance_complete
            else {
                "decision": "CONTINUE",
                "required_action": "RUN_0830_MAINTENANCE",
                "finalization_allowed": False,
                "stop_reasons": [],
                "work_mode": "maintenance",
            }
        )
    else:
        gate = continuation_gate.decide(args)

    finalization_gate = run_finalization_gate.decide(
        argparse.Namespace(
            continuation_decision=str(gate.get("decision") or "CONTINUE"),
            continuation_finalization_allowed=gate.get("finalization_allowed") is True,
            active_assignment=bool(claims.get("active_assignment")),
            active_assignment_handoff_safe=False,
            claim_state_checked=bool(claims.get("claim_state_checked")),
            claim_result_pending=bool(claims.get("claim_result_pending")),
            submission_state_checked=bool(submission.get("submission_state_checked")),
            submission_result_pending=bool(submission.get("submission_result_pending")),
            ack_result_pending=False,
            discovery_precheck_result_pending=bool(
                discovery_async.get("discovery_precheck_result_pending")
            ),
            discovery_submission_result_pending=bool(
                discovery_async.get("discovery_submission_result_pending")
            ),
            discovery_evaluation_pending=bool(
                discovery_async.get("discovery_evaluation_pending")
            ),
            discovery_recovery_required=bool(
                discovery_async.get("discovery_recovery_required")
            ),
            discovery_pipeline_work_available=discovery_pipeline_work_available,
            continuation_required_action=str(gate.get("required_action") or ""),
            hard_stop=bool(gate.get("hard_stop")),
            handoff_safe=False,
            work_mode=work_mode,
            research_audit_completed_this_invocation=int(
                submission.get("research_audit_completed_this_invocation") or 0
            ),
            research_minimum_completions=worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS,
            discovery_rounds_completed=discovery_rounds,
            discovery_min_rounds=worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS,
        )
    )

    finalization_permit_issued = bool(
        (finalization_gate.get("finalization_permit") or {}).get("issued")
    )
    next_work_packet = _next_work_packet(
        root,
        worker_id=str(request["worker_id"]),
        gate=gate,
        finalization_gate=finalization_gate,
        claims=claims,
        discovery_async=discovery_async,
        discovery_preload=discovery_preload,
        discovery_fallback_source=discovery_fallback_source,
        discovery_pipeline_preload=discovery_pipeline_preload,
    )

    public_submission = {key: value for key, value in submission.items() if key != "attempt_facts"}
    derive_ms = round((time.perf_counter() - perf_started) * 1000.0, 3)
    files_read = max(READ_COUNT - read_started, 0)
    snapshot_generation = run_state_cache.generation_for(root, request["worker_id"], request["run_key"])

    return {
        "schema_version": 1,
        "ok": True,
        "request_id": request["request_id"],
        "run_key": request["run_key"],
        "worker_id": request["worker_id"],
        "scheduled_slot": request["scheduled_slot"],
        "actual_invocation_start": request["actual_invocation_start"],
        "actual_invocation_start_original": request.get("actual_invocation_start_original"),
        "actual_invocation_start_recovery": request.get("actual_invocation_start_recovery"),
        "processed_at": now.isoformat(),
        "candidate_inventory": inventory,
        "work_mode": work_mode,
        "route_source": route_source,
        "route_recovery_source": request.get("route_recovery_source") or None,
        "candidate_inventory_at_start_exact": not bool(request.get("route_recovery_source")),
        "runtime_condition_requested": requested_runtime,
        "runtime_condition": runtime,
        "runtime_condition_confirmed": request.get("runtime_condition_confirmed", False),
        "runtime_condition_attempts": request.get("runtime_condition_attempts", 0),
        "runtime_condition_detail": request.get("runtime_condition_detail", ""),
        "runtime_condition_event": request.get("runtime_condition_event", ""),
        "runtime_condition_ignored_reason": runtime_condition_ignored_reason,
        "seconds_to_run_deadline": seconds_to_deadline,
        **claims,
        **public_submission,
        **discovery_async,
        "snapshot_generation": snapshot_generation,
        "run_state_source": "incremental_cache" if cache_hit else "canonical_rebuild",
        "run_state_files_read": files_read,
        "run_state_derive_ms": derive_ms,
        "discovery_rounds_completed": discovery_rounds,
        "discovery_selector": selector,
        "discovery_preload": discovery_preload,
        "discovery_fallback_source": discovery_fallback_source,
        "discovery_pipeline_preload": discovery_pipeline_preload,
        "discovery_pipeline_work_available": discovery_pipeline_work_available,
        "discovery_pipeline_window": DISCOVERY_PIPELINE_WINDOW,
        "idle_gap_forbidden": True,
        "independent_work": independent_work,
        "gate": gate,
        "finalization_gate": finalization_gate,
        "finalization_permit_issued": finalization_permit_issued,
        "run_termination_allowed": finalization_permit_issued,
        "run_phase": "finalizable" if finalization_permit_issued else "running",
        "continuation_next_action": gate.get("required_action"),
        "next_action": finalization_gate.get("next_action") or gate.get("required_action"),
        "next_work_packet": next_work_packet,
        "transport_rule": (
            "A GitHub file create/update API or connector is a valid repository write transport. "
            "Lack of local shell, Python execution, git push, or manual Actions dispatch is not evidence of write unavailability. "
            "Before declaring transport_unrecoverable or durable_transports_unavailable, attempt an actual write to the required canonical request/direct-take/submission path and record the concrete failure."
        ),
        "rule": (
            "Use this durable derived snapshot instead of manually inventing continuation-gate booleans. "
            "The first successful snapshot for run_key freezes candidate_inventory/work_mode. "
            "Active same-worker claims from a previous invocation are resumed rather than hidden by the new start time; "
            f"Research/Audit uses a configurable claim window (default {SCHEDULED_CHAT_CLAIM_WINDOW}): the oldest active claim is foreground and later active claims are standby; "
            f"Research exact-blob preflight is overlapped with content work using an admission window of {RESEARCH_PREFLIGHT_PIPELINE_WINDOW}; every pending/passed-without-descriptor attempt remains frozen regardless of overflow, and a failed latest preflight returns to pipeline-order foreground repair. "
            "only terminal results processed during this invocation count toward its completion quota. "
            "New Research/Audit descriptors use <attempt_id>.json; legacy arbitrary names are read-only compatible. "
            "The final handoff guard begins at 180 seconds remaining, while the 600-second window only forbids new independent work. "
            "runtime_condition must name a concrete observed platform/transport event; retriable read/transport conditions require confirmation after at least two failed recovery attempts. "
            "GitHub file create/update capability counts as GitHub write; absence of local script execution alone is never a transport hard stop, and an actual canonical-path write must be attempted before a write-unavailable handoff. "
            "platform_context_limit is accepted only with runtime_condition_event=platform_tool_call_rejected and a concrete observed-error detail; a single paper/source retrieval failure is never platform-context evidence. "
            "A pending claim exposes its request age; for the first 60 seconds the gate requires active Survey claim fast-lane monitoring rather than passive waiting. "
            "Discovery async state and carry-over immutable submissions remain visible across run boundaries. "
            "Discovery pending results do not mask already-evaluable rounds; evaluation/recovery work has priority over wait states. "
            f"Outside the 600-second no-new-work window, at most {DISCOVERY_PIPELINE_WINDOW} Discovery rounds may be in flight so a PRECHECKED citation window can be evaluated while an older precheck/submission settles. "
            "When work_mode=discovery, discovery_preload exposes the oldest PRECHECKED preload matching the canonical selector direction; "
            "it is only an acceleration hint and must be adopted through a new run-specific schema-v3 precheck request, never referenced directly by a submission. "
            "If that warm bank is absent, discovery_fallback_source exposes the same selector-compatible fixed source so the next schema-v3 precheck can start immediately without passive waiting. "
            "idle_gap_forbidden=true means an asynchronous result must not be treated as permission to stop or passively wait when a prepared/fallback next action exists. "
            "Top-level next_action is the finalization gate's canonical action, while continuation_next_action preserves the pre-finalization routing decision for diagnostics. "
            "When run_termination_allowed=false, next_work_packet identifies the concrete durable object to process next whenever one can be resolved; this running state is not a handoff condition. "
            "The incremental cache is only an index; missing, corrupt, or fact-generation-stale cache state is rebuilt from canonical durable facts. "
            "Every durable run-state snapshot embeds the finalization gate result for continuation and stopping decisions. "
            "Run-state does not suppress user-facing reports; termination reporting is governed by worker-router.md."
        ),
    }


def process_pending(root: Path) -> dict[str, Any]:
    root = root.resolve()
    bootstrap = {"rebuilt": 0, "failures": []}
    if any(
        run_state_cache.load_cache(root, worker_id) is None
        for worker_id in worker_identity.FIXED_SCHEDULED_WORKER_SLOTS
    ):
        bootstrap = rebuild_caches(root)
    request_root = root / REQUESTS
    result_root = root / RESULTS
    request_root.mkdir(parents=True, exist_ok=True)
    result_root.mkdir(parents=True, exist_ok=True)
    processed = errors = reused = 0
    for path in sorted(request_root.glob("*.json")):
        target = result_root / path.name
        if target.exists():
            reused += 1
            existing = _read(target, {})
            if isinstance(existing, dict) and existing.get("ok") is True:
                run_state_cache.write_latest_pointer(root, target, existing)
            continue
        try:
            request = _normalize_request(path, _read(path))
            result = derive(root, request)
            result["snapshot_origin"] = "request-fast-lane"
        except Exception as exc:
            errors += 1
            result = {
                "schema_version": 1,
                "ok": False,
                "request_id": path.stem,
                "error": f"{type(exc).__name__}: {exc}",
                "next_action": "FIX_RUN_STATE_REQUEST",
            }
        _write(target, result)
        if result.get("ok") is True:
            run_state_cache.write_latest_pointer(root, target, result)
        processed += 1
    return {"processed": processed, "errors": errors, "reused": reused, "cache_bootstrap_rebuilt": bootstrap.get("rebuilt", 0), "cache_bootstrap_failures": bootstrap.get("failures", [])}


def _descriptor_paths(path: Path) -> list[Path]:
    if not path.is_file():
        return []
    return [
        Path(line.strip())
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def auto_snapshot_from_descriptors(root: Path, descriptors_file: Path) -> dict[str, Any]:
    root = root.resolve()
    paths = _descriptor_paths(descriptors_file)
    cached_paths: list[Path] = []
    expected_runs: dict[tuple[str, str], dict[str, Any]] = {}
    fallback_required: list[str] = []

    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else root / raw_path
        descriptor = _read(path, {})
        if not isinstance(descriptor, dict):
            continue
        identity = run_state_cache._descriptor_identity(descriptor)
        if identity is None:
            continue
        request = {
            "schema_version": 1,
            "request_id": "auto-pending",
            "run_key": identity["run_key"],
            "worker_id": identity["worker_id"],
            "worker_kind": "scheduled_chat",
            "scheduled_slot": identity["scheduled_slot"],
            "actual_invocation_start": identity["actual_invocation_start"],
            "runtime_condition": "none",
            "runtime_condition_confirmed": False,
            "runtime_condition_attempts": 0,
            "runtime_condition_detail": "",
        }
        key = (identity["worker_id"], identity["run_key"])
        expected_runs[key] = request
        if run_state_cache.get_run(root, request) is None:
            fallback_required.append(f"{identity['worker_id']}:{identity['run_key']}")
            continue
        cached_paths.append(path.relative_to(root))

    touched = run_state_cache.observe_descriptors(root, cached_paths)
    generated: list[str] = []
    for worker_id, run_keys in sorted(touched.items()):
        for run_key in run_keys:
            request = expected_runs.get((worker_id, run_key))
            if request is None:
                request = run_state_cache.cached_request(root, worker_id, run_key)
            if request is None:
                fallback_required.append(f"{worker_id}:{run_key}")
                continue
            result = derive(root, request)
            generation = run_state_cache.generation_for(root, worker_id, run_key)
            request_id = run_state_cache.auto_result_id(worker_id, run_key, generation)
            result["request_id"] = request_id
            result["snapshot_generation"] = generation
            result["snapshot_origin"] = "submission-fast-lane"
            result["auto_generated"] = True
            target = root / RESULTS / f"{request_id}.json"
            _write(target, result)
            run_state_cache.write_latest_pointer(root, target, result)
            generated.append(target.relative_to(root).as_posix())
    return {
        "observed_descriptors": len(paths),
        "touched_runs": sum(len(items) for items in touched.values()),
        "generated_results": generated,
        "fallback_required": sorted(set(fallback_required)),
    }


def auto_snapshot_from_preflight_results(
    root: Path,
    results_file: Path,
) -> dict[str, Any]:
    """Publish fresh run-state snapshots for Research/Audit preflight outcomes."""
    root = root.resolve()
    paths = _descriptor_paths(results_file)
    affected: dict[tuple[str, str], dict[str, Any]] = {}
    ignored: list[str] = []

    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else root / raw_path
        value = _read(path, {})
        if (
            not isinstance(value, dict)
            or value.get("operation") != "research_quality_preflight"
        ):
            ignored.append(str(raw_path))
            continue
        worker_id = str(value.get("worker_id") or "").strip()
        run_key = str(value.get("run_key") or "").strip()
        scheduled_slot = str(value.get("scheduled_slot") or "").strip()
        started_at = _time(value.get("actual_invocation_start"))
        if (
            not worker_identity.is_supported_worker_id(worker_id)
            or not worker_identity.identity_slot_valid(worker_id, scheduled_slot)
            or not run_key
            or started_at is None
        ):
            ignored.append(str(raw_path))
            continue
        affected[(worker_id, run_key)] = {
            "schema_version": 1,
            "request_id": "auto-preflight-pending",
            "run_key": run_key,
            "worker_id": worker_id,
            "worker_kind": "scheduled_chat",
            "scheduled_slot": scheduled_slot,
            "actual_invocation_start": started_at.astimezone(dt.timezone.utc).isoformat(),
            "runtime_condition": "none",
            "runtime_condition_confirmed": False,
            "runtime_condition_attempts": 0,
            "runtime_condition_detail": "",
            "route_recovery_source": "research_preflight_identity",
            "recovered_work_mode_at_start": "research",
        }

    generated: list[str] = []
    fallback_recovery: list[str] = []
    for (worker_id, run_key), fallback_request in sorted(affected.items()):
        request = run_state_cache.cached_request(root, worker_id, run_key)
        if request is None:
            request = fallback_request
            fallback_recovery.append(f"{worker_id}:{run_key}")
        result = derive(root, request)
        generation = run_state_cache.generation_for(root, worker_id, run_key)
        request_id = run_state_cache.auto_result_id(worker_id, run_key, generation)
        result["request_id"] = request_id
        result["snapshot_generation"] = generation
        result["snapshot_origin"] = "research-preflight-fast-lane"
        result["auto_generated"] = True
        target = root / RESULTS / f"{request_id}.json"
        _write(target, result)
        run_state_cache.write_latest_pointer(root, target, result)
        generated.append(target.relative_to(root).as_posix())

    return {
        "observed_preflight_results": len(paths),
        "affected_runs": len(affected),
        "generated_results": generated,
        "fallback_recovery_runs": fallback_recovery,
        "ignored_paths": ignored,
    }


def apply_claim_result_deltas(root: Path, results_file: Path) -> dict[str, Any]:
    root = root.resolve()
    paths = _descriptor_paths(results_file)

    # Capture run identity directly from each newly written claim result before
    # touching the cache. This lets the claim fast lane publish a fresh run-state
    # snapshot even when the cache is missing or deliberately invalidated.
    expected_runs: dict[tuple[str, str], dict[str, Any]] = {}
    for raw_path in paths:
        path = raw_path if raw_path.is_absolute() else root / raw_path
        value = _read(path, {})
        if not isinstance(value, dict) or value.get("ok") is not True:
            continue
        worker_id = str(value.get("worker_id") or "")
        run_key = str(value.get("run_key") or "")
        scheduled_slot = str(value.get("scheduled_slot") or "")
        started_at = _time(value.get("actual_invocation_start"))
        if (
            not worker_identity.is_supported_worker_id(worker_id)
            or not worker_identity.identity_slot_valid(worker_id, scheduled_slot)
            or not run_key
            or started_at is None
        ):
            continue
        expected_runs[(worker_id, run_key)] = {
            "schema_version": 1,
            "request_id": "auto-claim-pending",
            "run_key": run_key,
            "worker_id": worker_id,
            "worker_kind": "scheduled_chat",
            "scheduled_slot": scheduled_slot,
            "actual_invocation_start": started_at.astimezone(dt.timezone.utc).isoformat(),
            "runtime_condition": "none",
            "runtime_condition_confirmed": False,
            "runtime_condition_attempts": 0,
            "runtime_condition_detail": "",
        }

    touched = run_state_cache.observe_claim_results(root, paths)
    generated: list[str] = []
    canonical_fallback_runs: list[str] = []

    for (worker_id, run_key), fallback_request in sorted(expected_runs.items()):
        request = run_state_cache.cached_request(root, worker_id, run_key)
        if request is None:
            request = fallback_request
            canonical_fallback_runs.append(f"{worker_id}:{run_key}")

        result = derive(root, request)
        generation = run_state_cache.generation_for(root, worker_id, run_key)
        request_id = run_state_cache.auto_result_id(worker_id, run_key, generation)
        result["request_id"] = request_id
        result["snapshot_generation"] = generation
        result["snapshot_origin"] = "claim-fast-lane"
        result["auto_generated"] = True
        target = root / RESULTS / f"{request_id}.json"
        _write(target, result)
        run_state_cache.write_latest_pointer(root, target, result)
        generated.append(target.relative_to(root).as_posix())

    return {
        "observed_claim_results": len(paths),
        "touched_runs": sum(len(items) for items in touched.values()),
        "workers": touched,
        "generated_results": generated,
        "canonical_fallback_runs": canonical_fallback_runs,
    }

def rebuild_caches(root: Path) -> dict[str, Any]:
    root = root.resolve()
    rows: dict[tuple[str, str], dict[str, Any]] = {}
    for result_root in (
        root / RESULTS,
        root / ".survey/work-queue/archive/transport/run-state/results",
    ):
        if not result_root.is_dir():
            continue
        for path in result_root.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict) or value.get("ok") is not True:
                continue
            worker_id = str(value.get("worker_id") or "")
            run_key = str(value.get("run_key") or "")
            slot = str(value.get("scheduled_slot") or "")
            start = value.get("actual_invocation_start")
            if (
                not worker_identity.is_supported_worker_id(worker_id)
                or not worker_identity.identity_slot_valid(worker_id, slot)
                or not run_key
                or _time(start) is None
            ):
                continue
            key = (worker_id, run_key)
            current = rows.get(key)
            if current is None or str(value.get("processed_at") or "") > str(current.get("processed_at") or ""):
                rows[key] = value

    ordered = sorted(
        rows.values(),
        key=lambda value: str(value.get("actual_invocation_start") or ""),
        reverse=True,
    )
    rebuilt = 0
    failures: list[str] = []
    per_worker: dict[str, int] = {}
    for value in ordered:
        worker_id = str(value["worker_id"])
        if per_worker.get(worker_id, 0) >= 8:
            continue
        request = {
            "schema_version": 1,
            "request_id": "maintenance-rebuild",
            "run_key": str(value["run_key"]),
            "worker_id": worker_id,
            "worker_kind": "scheduled_chat",
            "scheduled_slot": str(value["scheduled_slot"]),
            "actual_invocation_start": str(value["actual_invocation_start"]),
            "runtime_condition": "none",
            "runtime_condition_confirmed": False,
            "runtime_condition_attempts": 0,
            "runtime_condition_detail": "",
        }
        try:
            derive(root, request, force_canonical=True)
        except Exception as exc:
            failures.append(f"{worker_id}:{request['run_key']}:{type(exc).__name__}:{exc}")
            continue
        rebuilt += 1
        per_worker[worker_id] = per_worker.get(worker_id, 0) + 1
    return {"rebuilt": rebuilt, "failures": failures}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--auto-from-descriptors-file", type=Path)
    parser.add_argument("--claim-results-file", type=Path)
    parser.add_argument("--preflight-results-file", type=Path)
    parser.add_argument("--rebuild-cache", action="store_true")
    args = parser.parse_args()
    if args.auto_from_descriptors_file is not None:
        result = auto_snapshot_from_descriptors(args.repo_root, args.auto_from_descriptors_file)
    elif args.claim_results_file is not None:
        result = apply_claim_result_deltas(args.repo_root, args.claim_results_file)
    elif args.preflight_results_file is not None:
        result = auto_snapshot_from_preflight_results(args.repo_root, args.preflight_results_file)
    elif args.rebuild_cache:
        result = rebuild_caches(args.repo_root)
    else:
        result = process_pending(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided
    raise SystemExit(run_guided(main, script=__file__))
