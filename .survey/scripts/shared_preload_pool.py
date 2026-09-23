#!/usr/bin/env python3
"""Shared global FIFO preload pool for Research/Audit claims.

The pool is worker-agnostic. It owns ready jobs only until a real Scheduled Chat
request atomically adopts the oldest eligible entries. The global inventory target
counts both waiting pool claims and already-adopted Scheduled Chat claims, so a
target of 24 means six four-claim worker windows in total rather than 24 waiting
claims plus worker-local claims.

All mutation happens inside the existing claim fast path. GitHub Actions serializes
that path with the survey-claim-main concurrency group, and push-race retries rerun
allocation from the latest main, so two workers cannot adopt the same pool claim.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import claim_state

POOL_WORKER_ID = "shared-preload-pool"
POOL_WORKER_KIND = "work"
POOL_TARGET = 24
POOL_LEASE_SECONDS = 43200
POOL_RENEW_BEFORE_SECONDS = 21600
CLAIM_TYPES = {"research", "audit"}


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp_name = tmp.name
    Path(temp_name).replace(path)


def is_pool_claim(value: dict[str, Any]) -> bool:
    return bool(
        value.get("preload_pool") is True
        and value.get("worker_id") == POOL_WORKER_ID
        and value.get("worker_kind") == POOL_WORKER_KIND
    )


def _pool_order(value: dict[str, Any]) -> tuple[int, str, str]:
    order = value.get("pool_order")
    normalized = int(order) if isinstance(order, int) and not isinstance(order, bool) and order >= 0 else 10**12
    return (normalized, str(value.get("preloaded_at") or value.get("claimed_at") or ""), str(value.get("job_id") or ""))


def _claim_id(job_id: str, now: dt.datetime, order: int) -> str:
    material = f"{job_id}\n{_iso(now)}\n{order}\nshared-preload-pool"
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return f"claim-preload-{digest}"


def _attempt_id(claim_id: str) -> str:
    return "attempt-" + claim_id.removeprefix("claim-")


def _inventory_claim(value: dict[str, Any]) -> bool:
    if not value.get("active") or str(value.get("kind") or "") not in CLAIM_TYPES:
        return False
    return is_pool_claim(value) or value.get("worker_kind") == "scheduled_chat"


def waiting_claims(claims: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        (value for value in claims.values() if value.get("active") and is_pool_claim(value)),
        key=_pool_order,
    )


def adopt(
    repo_root: Path,
    *,
    claims: dict[str, dict[str, Any]],
    jobs_by_id: dict[str, dict[str, Any]],
    request: dict[str, Any],
    now: dt.datetime,
    needed: int,
    next_pipeline_order: int,
    checkpointed_ids: set[str],
    requested_job_ids: set[str] | None,
) -> list[dict[str, Any]]:
    """Atomically transfer the oldest eligible waiting claims to one worker."""
    if needed <= 0:
        return []

    candidates: list[dict[str, Any]] = []
    for current in waiting_claims(claims):
        job_id = str(current.get("job_id") or "")
        job = jobs_by_id.get(job_id)
        if not isinstance(job, dict) or job.get("status") != "ready":
            continue
        if job.get("type") not in request["job_types"]:
            continue
        if requested_job_ids is not None and job_id not in requested_job_ids:
            continue
        if job_id in checkpointed_ids:
            continue
        candidates.append(current)

    adopted: list[dict[str, Any]] = []
    new_expiry = _iso(now + dt.timedelta(seconds=int(request["lease_seconds"])))
    for offset, current in enumerate(candidates[:needed]):
        job_id = str(current["job_id"])
        claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
        claim["preloaded_at"] = claim.get("preloaded_at") or claim.get("claimed_at") or _iso(now)
        claim["preload_pool"] = False
        claim["preload_pool_adopted_at"] = _iso(now)
        claim["preload_pool_worker_id"] = POOL_WORKER_ID
        claim["worker_id"] = request["worker_id"]
        claim["worker_kind"] = request["worker_kind"]
        claim["request_id"] = request["request_id"]
        claim["claimed_at"] = _iso(now)
        claim["heartbeat_at"] = _iso(now)
        claim["expires_at"] = new_expiry
        claim["pipeline_order"] = next_pipeline_order + offset
        for field in ("run_key", "scheduled_slot", "actual_invocation_start"):
            if field in request:
                claim[field] = request[field]
            else:
                claim.pop(field, None)
        _write(Path(repo_root) / ".survey/work-queue/claims" / f"{job_id}.json", claim)
        claims[job_id] = dict(claim, active=True, expired=False)
        adopted.append(claim)
    return adopted


def maintain(
    repo_root: Path,
    *,
    claims: dict[str, dict[str, Any]],
    jobs: list[dict[str, Any]],
    submitted_jobs: set[str],
    now: dt.datetime,
    target: int = POOL_TARGET,
) -> dict[str, int]:
    """Keep the global active Research/Audit inventory at target without reordering it."""
    root = Path(repo_root)
    jobs_by_id = {str(job.get("job_id") or ""): job for job in jobs if isinstance(job, dict)}
    renewed = released = created = 0

    for job_id, current in list(claims.items()):
        if not current.get("active") or not is_pool_claim(current):
            continue
        job = jobs_by_id.get(job_id)
        if (
            not isinstance(job, dict)
            or job.get("status") != "ready"
            or job.get("type") not in CLAIM_TYPES
            or job_id in submitted_jobs
        ):
            claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
            claim["released_at"] = _iso(now)
            claim["expires_at"] = _iso(now)
            claim["preload_pool_release_reason"] = "job_not_pool_eligible"
            _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
            claims[job_id] = dict(claim, active=False, expired=True)
            released += 1
            continue

        expires = claim_state.parse_time(current.get("expires_at"))
        if expires is None or (expires - now).total_seconds() <= POOL_RENEW_BEFORE_SECONDS:
            claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
            claim["expires_at"] = _iso(now + dt.timedelta(seconds=POOL_LEASE_SECONDS))
            claim["heartbeat_at"] = _iso(now)
            _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
            claims[job_id] = dict(claim, active=True, expired=False)
            renewed += 1

    inventory_active = sum(1 for value in claims.values() if _inventory_claim(value))
    shortfall = max(int(target) - inventory_active, 0)

    active_job_ids = {
        str(job_id)
        for job_id, value in claims.items()
        if value.get("active")
    }
    available: list[dict[str, Any]] = []
    for job in jobs:
        if not isinstance(job, dict):
            continue
        job_id = str(job.get("job_id") or "")
        if not job_id or job_id in active_job_ids or job_id in submitted_jobs:
            continue
        if job.get("status") != "ready" or job.get("type") not in CLAIM_TYPES:
            continue
        dependencies = claim_state.normalize_dependencies(
            job_id,
            job["depends_on_job_ids"] if "depends_on_job_ids" in job else job.get("dependencies"),
        )
        if dependencies is None:
            continue
        available.append(job)
    available.sort(
        key=lambda item: (
            -int(item.get("priority") or 0),
            str(item.get("created_at") or ""),
            str(item.get("job_id") or ""),
        )
    )

    current_orders = [
        int(value["pool_order"])
        for value in claims.values()
        if value.get("active")
        and is_pool_claim(value)
        and isinstance(value.get("pool_order"), int)
        and not isinstance(value.get("pool_order"), bool)
        and int(value["pool_order"]) >= 0
    ]
    next_order = (max(current_orders) + 1) if current_orders else 0

    for offset, job in enumerate(available[:shortfall]):
        job_id = str(job["job_id"])
        order = next_order + offset
        claim_id = _claim_id(job_id, now, order)
        previous = claims.get(job_id)
        dependencies = claim_state.normalize_dependencies(
            job_id,
            job["depends_on_job_ids"] if "depends_on_job_ids" in job else job.get("dependencies"),
        )
        if dependencies is None:
            continue
        claim = {
            "schema_version": 1,
            "workflow_version": 10,
            "claim_id": claim_id,
            "job_id": job_id,
            "worker_id": POOL_WORKER_ID,
            "worker_kind": POOL_WORKER_KIND,
            "attempt_id": _attempt_id(claim_id),
            "claimed_at": _iso(now),
            "preloaded_at": _iso(now),
            "expires_at": _iso(now + dt.timedelta(seconds=POOL_LEASE_SECONDS)),
            "kind": job.get("type"),
            "depends_on_job_ids": dependencies,
            "preload_pool": True,
            "pool_order": order,
            "claim_source": "shared_preload_pool",
        }
        if previous and previous.get("claim_id") != claim_id:
            claim["previous_claim_id"] = previous.get("claim_id")
        _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
        claims[job_id] = dict(claim, active=True, expired=False)
        created += 1

    inventory_active = sum(1 for value in claims.values() if _inventory_claim(value))
    pool_waiting = sum(
        1 for value in claims.values()
        if value.get("active") and is_pool_claim(value)
    )
    return {
        "target": int(target),
        "created": created,
        "renewed": renewed,
        "released": released,
        "inventory_active": inventory_active,
        "pool_waiting": pool_waiting,
        "shortfall": max(int(target) - inventory_active, 0),
    }
