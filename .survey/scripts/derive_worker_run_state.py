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
from pathlib import Path
from typing import Any

import claim_state
import continuation_gate
import select_discovery_direction

REQUESTS = Path(".survey/work-queue/run-state/requests")
RESULTS = Path(".survey/work-queue/run-state/results")
ALLOWED_WORKERS = {
    "scheduled-chat-00": "00",
    "scheduled-chat-30": "30",
}
RUNTIME_CONDITIONS = {
    "none",
    "handoff_guard",
    "github_read_unavailable",
    "durable_transports_unavailable",
    "platform_context_limit",
    "transport_unrecoverable",
}


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
    if worker_id not in ALLOWED_WORKERS:
        raise ValueError("worker_id must be scheduled-chat-00 or scheduled-chat-30")
    if scheduled_slot not in {"00", "30", "0830"}:
        raise ValueError("scheduled_slot must be 00, 30, or 0830")
    if worker_id == "scheduled-chat-00" and scheduled_slot != "00":
        raise ValueError("scheduled-chat-00 must use scheduled_slot=00")
    if worker_id == "scheduled-chat-30" and scheduled_slot not in {"30", "0830"}:
        raise ValueError("scheduled-chat-30 must use scheduled_slot=30 or 0830")
    run_key = str(value.get("run_key") or "").strip()
    if not run_key:
        raise ValueError("run_key is required")
    started_at = _time(value.get("actual_invocation_start"))
    if started_at is None:
        raise ValueError("actual_invocation_start must be an offset-aware timestamp")
    runtime_condition = str(value.get("runtime_condition") or "none").strip()
    if runtime_condition not in RUNTIME_CONDITIONS:
        raise ValueError("unsupported runtime_condition")
    runtime_condition_confirmed = value.get("runtime_condition_confirmed") is True
    runtime_condition_attempts = value.get("runtime_condition_attempts", 0)
    if isinstance(runtime_condition_attempts, bool) or not isinstance(runtime_condition_attempts, int):
        raise ValueError("runtime_condition_attempts must be an integer")
    runtime_condition_detail = str(value.get("runtime_condition_detail") or "").strip()
    return {
        "schema_version": 1,
        "request_id": request_id,
        "run_key": run_key,
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "scheduled_slot": scheduled_slot,
        "actual_invocation_start": started_at.astimezone(dt.timezone.utc).isoformat(),
        "runtime_condition": runtime_condition,
        "runtime_condition_confirmed": runtime_condition_confirmed,
        "runtime_condition_attempts": max(runtime_condition_attempts, 0),
        "runtime_condition_detail": runtime_condition_detail,
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
    result_root = root / RESULTS
    if not result_root.is_dir():
        return None
    rows: list[tuple[str, int, str]] = []
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
    result_root = root / ".survey/work-queue/claim-results"
    if result_root.is_dir():
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
    pending: list[tuple[dt.datetime, str]] = []
    submitted: list[tuple[dt.datetime, str]] = []
    terminal: list[tuple[dt.datetime, str]] = []

    for attempt_id, claimed_at in attempts.items():
        found_descriptor = False
        for kind in ("research", "audit"):
            descriptor_path = _descriptor_for_attempt(root, kind, attempt_id)
            if descriptor_path is None:
                continue
            found_descriptor = True
            submitted.append((claimed_at, attempt_id))
            result = _read(root / ".survey/work-queue/results" / kind / descriptor_path.name, {})
            if not isinstance(result, dict) or result.get("attempt_id") != attempt_id:
                pending.append((claimed_at, attempt_id))
                continue
            if result.get("ok") is False and result.get("retryable") is True:
                pending.append((claimed_at, attempt_id))
                continue
            processed_at = _time(result.get("processed_at")) or claimed_at
            status = str(result.get("job_status") or "none").lower()
            if (
                result.get("ok") is True
                and status == "completed"
                and processed_at >= started_at
            ):
                completed += 1
            if status in {"completed", "blocked", "deferred", "rejected"}:
                terminal.append((processed_at, status))
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
    }


def _claim_state(root: Path, worker_id: str, started_at: dt.datetime) -> dict[str, Any]:
    pending_requests: list[str] = []
    request_root = root / ".survey/work-queue/claim-requests"
    result_root = root / ".survey/work-queue/claim-results"
    if request_root.is_dir():
        for path in request_root.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict) or value.get("worker_id") != worker_id:
                continue
            requested = _time(value.get("requested_at"))
            if requested is None or requested < started_at:
                continue
            if not (result_root / path.name).is_file():
                pending_requests.append(path.stem)

    now = dt.datetime.now(dt.timezone.utc)
    claims = claim_state.current_claims(root, now)
    active: list[str] = []
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
        if not descriptor_backed:
            active.append(job_id)
    return {
        "claim_state_checked": True,
        "claim_result_pending": bool(pending_requests),
        "pending_claim_request_ids": sorted(pending_requests),
        "active_assignment": bool(active),
        "active_job_ids": sorted(active),
    }


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


def _discovery_async_state(root: Path, run_key: str) -> dict[str, Any]:
    request_root = root / ".survey/work-queue/discovery-precheck/requests"
    precheck_result_root = root / ".survey/work-queue/discovery-precheck/results"
    submission_root = root / ".survey/work-queue/submissions"
    result_root = root / ".survey/work-queue/results"

    pending_prechecks: list[str] = []
    evaluation_pending: list[str] = []
    recovery_required: list[str] = []
    successful_prechecks: dict[str, dict[str, Any]] = {}

    if request_root.is_dir():
        for path in request_root.glob("*.json"):
            request = _read(path, {})
            if not isinstance(request, dict) or str(request.get("run_key") or "") != run_key:
                continue
            result = _read(precheck_result_root / path.name, {})
            if not isinstance(result, dict) or result.get("request_id") != path.stem:
                pending_prechecks.append(path.stem)
                continue
            if result.get("ok") is True and result.get("evaluation_allowed") is True:
                successful_prechecks[path.stem] = result
            elif result.get("ok") is False:
                recovery_required.append(f"precheck:{path.stem}")

    submitted_prechecks: set[str] = set()
    pending_submissions: list[str] = []
    if submission_root.is_dir():
        for path in submission_root.glob("*.json"):
            submission = _read(path, {})
            if not isinstance(submission, dict) or submission.get("operation") != "submit_discovery_round":
                continue
            stats = submission.get("discovery_stats") if isinstance(submission.get("discovery_stats"), dict) else {}
            submission_run_key = str(submission.get("run_key") or stats.get("run_key") or "")
            if submission_run_key != run_key:
                continue
            precheck_id = str(submission.get("precheck_request_id") or stats.get("precheck_request_id") or "")
            if precheck_id:
                submitted_prechecks.add(precheck_id)
            result = _read(result_root / path.name, {})
            if not isinstance(result, dict):
                pending_submissions.append(path.stem)
            elif result.get("ok") is False:
                recovery_required.append(f"submission:{path.stem}")

    state = _read(root / ".survey/work-queue/discovery-state.json", {}) or {}
    history = state.get("history") if isinstance(state.get("history"), list) else []
    accounted_prechecks = {
        str(row.get("precheck_request_id") or "")
        for row in history
        if isinstance(row, dict)
        and str(row.get("run_key") or "") == run_key
        and (row.get("round_accounted") is True or row.get("round_complete") is True)
    }
    for request_id in successful_prechecks:
        if request_id not in submitted_prechecks and request_id not in accounted_prechecks:
            evaluation_pending.append(request_id)

    return {
        "discovery_precheck_result_pending": bool(pending_prechecks),
        "pending_discovery_precheck_request_ids": sorted(pending_prechecks),
        "discovery_submission_result_pending": bool(pending_submissions),
        "pending_discovery_submission_ids": sorted(pending_submissions),
        "discovery_evaluation_pending": bool(evaluation_pending),
        "discovery_evaluation_request_ids": sorted(evaluation_pending),
        "discovery_recovery_required": bool(recovery_required),
        "discovery_recovery_targets": sorted(recovery_required),
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


def derive(root: Path, request: dict[str, Any]) -> dict[str, Any]:
    root = root.resolve()
    started_at = _time(request["actual_invocation_start"])
    assert started_at is not None

    frozen = _frozen_route(root, request["run_key"])
    if request["scheduled_slot"] == "0830":
        inventory = _candidate_inventory(root) if frozen is None else frozen[0]
        work_mode = "maintenance"
    elif frozen is not None:
        inventory, work_mode = frozen
    else:
        inventory = _candidate_inventory(root)
        work_mode = "research" if inventory >= 50 else "discovery"

    attempts = _run_attempts(root, request["worker_id"], started_at)
    submission = _run_submission_state(root, attempts, started_at)
    claims = _claim_state(root, request["worker_id"], started_at)
    discovery_rounds, selector = _discovery_rounds(root, request["run_key"])
    discovery_async = _discovery_async_state(root, request["run_key"])

    now = dt.datetime.now(dt.timezone.utc)
    deadline = started_at + dt.timedelta(seconds=3600)
    seconds_to_deadline = max(int((deadline - now).total_seconds()), 0)
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
        if not request.get("runtime_condition_confirmed") or int(request.get("runtime_condition_attempts") or 0) < 1:
            runtime = "none"
            runtime_condition_ignored_reason = "platform_limit_not_confirmed"

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
        spillover_work=False,
        can_discover=work_mode == "discovery" and bool(selector.get("next_direction")),
        claim_state_checked=claims["claim_state_checked"],
        claim_result_pending=claims["claim_result_pending"],
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
        research_minimum_completions=3,
        last_terminal_job_status=submission["last_terminal_job_status"],
        discovery_rounds_completed=discovery_rounds,
        discovery_min_rounds=4,
        discovery_exhausted=False,
        next_axis_available=bool(selector.get("next_direction")),
        discovery_precheck_result_pending=discovery_async["discovery_precheck_result_pending"],
        discovery_submission_result_pending=discovery_async["discovery_submission_result_pending"],
        discovery_evaluation_pending=discovery_async["discovery_evaluation_pending"],
        discovery_recovery_required=discovery_async["discovery_recovery_required"],
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

    return {
        "schema_version": 1,
        "ok": True,
        "request_id": request["request_id"],
        "run_key": request["run_key"],
        "worker_id": request["worker_id"],
        "scheduled_slot": request["scheduled_slot"],
        "actual_invocation_start": request["actual_invocation_start"],
        "processed_at": now.isoformat(),
        "candidate_inventory": inventory,
        "work_mode": work_mode,
        "runtime_condition_requested": requested_runtime,
        "runtime_condition": runtime,
        "runtime_condition_confirmed": request.get("runtime_condition_confirmed", False),
        "runtime_condition_attempts": request.get("runtime_condition_attempts", 0),
        "runtime_condition_detail": request.get("runtime_condition_detail", ""),
        "runtime_condition_ignored_reason": runtime_condition_ignored_reason,
        "seconds_to_run_deadline": seconds_to_deadline,
        **claims,
        **submission,
        **discovery_async,
        "discovery_rounds_completed": discovery_rounds,
        "discovery_selector": selector,
        "independent_work": independent_work,
        "gate": gate,
        "next_action": gate.get("required_action"),
        "rule": (
            "Use this durable derived snapshot instead of manually inventing continuation-gate booleans. "
            "The first successful snapshot for run_key freezes candidate_inventory/work_mode. "
            "Active same-worker claims from a previous invocation are resumed rather than hidden by the new start time; "
            "only terminal results processed during this invocation count toward its completion quota. "
            "New Research/Audit descriptors use <attempt_id>.json; legacy arbitrary names are read-only compatible. "
            "The final handoff guard begins at 180 seconds remaining, while the 600-second window only forbids new independent work. "
            "runtime_condition must name a concrete observed platform/transport event; retriable read/transport conditions require confirmation after at least two failed recovery attempts. Discovery async state and carry-over immutable submissions remain visible across run boundaries."
        ),
    }


def process_pending(root: Path) -> dict[str, int]:
    root = root.resolve()
    request_root = root / REQUESTS
    result_root = root / RESULTS
    request_root.mkdir(parents=True, exist_ok=True)
    result_root.mkdir(parents=True, exist_ok=True)
    processed = errors = reused = 0
    for path in sorted(request_root.glob("*.json")):
        target = result_root / path.name
        if target.exists():
            reused += 1
            continue
        try:
            request = _normalize_request(path, _read(path))
            result = derive(root, request)
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
        processed += 1
    return {"processed": processed, "errors": errors, "reused": reused}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(process_pending(args.repo_root), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided
    raise SystemExit(run_guided(main, script=__file__))
