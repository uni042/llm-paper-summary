#!/usr/bin/env python3
"""Minimal initial-claim path that adopts already-preloaded Research/Audit claims.

This path is intentionally narrow. It is used only for the first claim request of a
run-state invocation when the shared preload FIFO already contains enough coherent,
bank-reserved claims to fill the requested variable claim window. Any condition that
would require queue-wide repair, direct allocation, checkpoint reconciliation, or
bank recovery declines the fast path before mutation so the canonical claim path can
handle it.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
from pathlib import Path
from typing import Any

import claim_state
import claim_window_policy
import claim_worker
import derive_worker_run_state
import shared_preload_pool
from record_bank_config import BANK_ROOTS, SLOT_NAMES, canonical_slot_paths


class InitialClaimFastPathUnavailable(RuntimeError):
    """The narrow preload-adopt path cannot safely handle the current state."""


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        tmp_name = tmp.name
    Path(tmp_name).replace(path)


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def _reservation_is_clean(root: Path, claim: dict[str, Any]) -> bool:
    bank = str(claim.get("record_bank") or "").lower()
    if bank not in BANK_ROOTS or claim.get("record_bank_fallback"):
        return False
    if claim.get("record_bank_root") != BANK_ROOTS[bank]:
        return False
    if claim.get("record_slot_paths") != canonical_slot_paths(bank):
        return False

    for slot in SLOT_NAMES:
        payload = _read(root / BANK_ROOTS[bank] / f"{slot}.json")
        reservation = payload.get("reservation") if isinstance(payload, dict) else None
        if not (
            isinstance(payload, dict)
            and payload.get("slot") == slot
            and payload.get("job_id") == claim.get("job_id")
            and payload.get("attempt_id") == claim.get("attempt_id")
            and payload.get("data") == {}
            and isinstance(reservation, dict)
            and reservation.get("claim_id") == claim.get("claim_id")
        ):
            return False
    return True


def _retag_reservation(root: Path, claim: dict[str, Any]) -> None:
    bank = str(claim["record_bank"]).lower()
    desired = {
        "claim_id": claim["claim_id"],
        "worker_id": claim.get("worker_id"),
        "worker_kind": claim.get("worker_kind"),
    }
    for slot in SLOT_NAMES:
        path = root / BANK_ROOTS[bank] / f"{slot}.json"
        payload = _read(path)
        if not isinstance(payload, dict):
            raise RuntimeError(f"validated record reservation disappeared: {path}")
        payload["reservation"] = desired
        _write(path, payload)


def _select_candidates(
    root: Path,
    *,
    request: dict[str, Any],
    claims: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if any(
        current.get("active")
        and claim_worker._same_worker_lineage(
            current.get("worker_id"),
            current.get("worker_kind"),
            request["worker_id"],
            request["worker_kind"],
        )
        for current in claims.values()
    ):
        raise InitialClaimFastPathUnavailable("worker already has an active claim")

    checkpointed = set(claim_worker._checkpoint_map(request))
    requested = set(request["job_ids"]) if request["job_ids"] is not None else None
    target = claim_window_policy.normalize_window(int(request["claim_window"]))
    selected: list[dict[str, Any]] = []
    jobs_by_id: dict[str, dict[str, Any]] = {}

    for current in shared_preload_pool.waiting_claims(claims):
        job_id = str(current.get("job_id") or "")
        if not job_id:
            continue
        job = _read(root / ".survey/work-queue/jobs" / f"{job_id}.json")
        if not isinstance(job, dict) or job.get("job_id") != job_id:
            raise InitialClaimFastPathUnavailable(f"preloaded job metadata missing: {job_id}")
        if job.get("status") != "ready" or job.get("type") not in request["job_types"]:
            continue
        if requested is not None and job_id not in requested:
            continue
        if job_id in checkpointed:
            continue
        if job.get("repair_required") is True:
            raise InitialClaimFastPathUnavailable(f"repair-required pool claim needs canonical recovery: {job_id}")
        dependencies = claim_state.normalize_dependencies(
            job_id,
            job["depends_on_job_ids"] if "depends_on_job_ids" in job else job.get("dependencies"),
        )
        if dependencies is None or list(current.get("depends_on_job_ids") or []) != dependencies:
            raise InitialClaimFastPathUnavailable(f"preloaded dependency state changed: {job_id}")
        if str(current.get("kind") or "") != str(job.get("type") or ""):
            raise InitialClaimFastPathUnavailable(f"preloaded job type changed: {job_id}")
        if not _reservation_is_clean(root, current):
            raise InitialClaimFastPathUnavailable(f"preloaded record bank is not a clean reservation: {job_id}")
        selected.append(current)
        jobs_by_id[job_id] = job
        if len(selected) >= target:
            break

    if len(selected) < target:
        raise InitialClaimFastPathUnavailable(
            f"shared preload pool has {len(selected)} eligible claims for target window {target}"
        )
    return selected, jobs_by_id


def _apply_run_state_delta(root: Path, result_path: Path) -> dict[str, Any]:
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
        tmp.write(result_path.relative_to(root).as_posix() + "\n")
        changed = Path(tmp.name)
    try:
        return derive_worker_run_state.apply_claim_result_deltas(root, changed)
    finally:
        changed.unlink(missing_ok=True)


def process(repo_root: Path, request_path: Path, at: Any = None) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    request_path = Path(request_path)
    if not request_path.is_absolute():
        request_path = root / request_path
    result_path = root / ".survey/work-queue/claim-results" / f"{request_path.stem}.json"
    if result_path.exists():
        raise InitialClaimFastPathUnavailable("claim result already exists")

    raw = _read(request_path)
    try:
        request = claim_worker._normalize_request(request_path, raw)
    except Exception as exc:
        raise InitialClaimFastPathUnavailable(f"initial claim request is not canonical: {exc}") from exc
    if request["worker_kind"] != "scheduled_chat" or not bool((raw or {}).get("auto_initial_claim")):
        raise InitialClaimFastPathUnavailable("request is not an automatic initial scheduled-chat claim")
    if request.get("checkpointed_jobs"):
        raise InitialClaimFastPathUnavailable("checkpoint barriers require canonical claim allocation")

    now = claim_state._as_now(at)
    claims = claim_state.current_claims(root, now)
    selected, jobs_by_id = _select_candidates(root, request=request, claims=claims)
    selected_ids = [str(item["job_id"]) for item in selected]

    adopted = shared_preload_pool.adopt(
        root,
        claims=claims,
        jobs_by_id=jobs_by_id,
        request=request,
        now=now,
        needed=len(selected),
        next_pipeline_order=0,
        checkpointed_ids=set(),
        requested_job_ids=set(request["job_ids"]) if request["job_ids"] is not None else None,
    )
    adopted_ids = [str(item["job_id"]) for item in adopted]
    if adopted_ids != selected_ids:
        raise RuntimeError(
            f"prevalidated FIFO adoption changed during mutation: expected={selected_ids} actual={adopted_ids}"
        )

    for claim in adopted:
        _retag_reservation(root, claim)

    assignments = [
        claim_worker._assignment(jobs_by_id[str(claim["job_id"])], claim)
        for claim in adopted
    ]
    assignments, foreground_job_id, standby_job_ids = claim_worker._decorate_claim_window(
        assignments,
        claim_window=int(request["claim_window"]),
    )
    result_payload = {
        "schema_version": 1,
        "workflow_version": 10,
        "request_id": request["request_id"],
        "worker_id": request["worker_id"],
        "worker_kind": request["worker_kind"],
        **{field: request[field] for field in claim_worker.RUN_IDENTITY_FIELDS if field in request},
        "ok": True,
        "assignments": assignments,
        "processed_at": _iso(now),
        "checkpoint_released": 0,
        "claim_window": int(request["claim_window"]),
        "claim_refill_threshold": claim_window_policy.refill_threshold(int(request["claim_window"])),
        "active_claim_count": len(assignments),
        "claim_window_remaining": max(int(request["claim_window"]) - len(assignments), 0),
        "foreground_job_id": foreground_job_id,
        "standby_job_ids": standby_job_ids,
        "shared_pool_adopted_count": len(adopted),
        "reason": "scheduled_chat_initial_preload_fast_path",
        "allocation_path": "preloaded_fifo_adopt_only",
    }
    _write(result_path, result_payload)
    state_update = _apply_run_state_delta(root, result_path)
    return {
        "ok": True,
        "processed": 1,
        "assigned": len(assignments),
        "claim_window": int(request["claim_window"]),
        "foreground_job_id": foreground_job_id,
        "standby_job_ids": standby_job_ids,
        "changed_claim_results": [result_path.relative_to(root).as_posix()],
        "run_state_update": state_update,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--request", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(process(args.repo_root, args.request), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
