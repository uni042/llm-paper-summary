#!/usr/bin/env python3
"""Shared global FIFO preload pool for Research/Audit claims.

The pool is worker-agnostic. It owns ready jobs only until a real Scheduled Chat
request atomically adopts the oldest eligible entries. The global inventory target
counts both waiting pool claims and already-adopted Scheduled Chat claims.

Paper preload is sharded across the same 32 dual-purpose bank identities used by
Discovery. Each active Research/Audit inventory claim carries stock_bank and is
mirrored into that bank's research-preload.json sidecar. The sidecar is a rebuildable
index only: waiting/cold claims still do not reserve the bank's five record slots.
Hot record staging prefers the claim's stock bank and may fall back to another bank.

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
import claim_window_policy
import worker_quota_policy
from record_bank_config import (
    BANK_IDS,
    BANK_ROOTS,
    RESEARCH_PRELOAD_SLOT_NAME,
    bank_for_sequence,
    research_preload_slot_path,
)

POOL_WORKER_ID = "shared-preload-pool"
POOL_WORKER_KIND = "work"
POOL_TARGET = claim_window_policy.shared_pool_target()
DIRECT_RESEARCH_TAKES = Path(".survey/work-queue/direct-takes/research")
POOL_LEASE_SECONDS = 43200
POOL_RENEW_BEFORE_SECONDS = 21600
CLAIM_TYPES = {"research", "audit"}


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


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
        temp_name = tmp.name
    Path(temp_name).replace(path)


def _research_sidecar_payload(bank: str, rows: list[dict[str, Any]]) -> dict[str, Any]:
    items = []
    for value in sorted(rows, key=_pool_order):
        items.append(
            {
                "job_id": value.get("job_id"),
                "claim_id": value.get("claim_id"),
                "attempt_id": value.get("attempt_id"),
                "kind": value.get("kind"),
                "pool_order": value.get("pool_order"),
                "preloaded_at": value.get("preloaded_at") or value.get("claimed_at"),
                "worker_id": value.get("worker_id"),
                "worker_kind": value.get("worker_kind"),
                "preload_pool": value.get("preload_pool") is True,
                "pipeline_order": value.get("pipeline_order"),
            }
        )
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": RESEARCH_PRELOAD_SLOT_NAME,
        "bank": bank,
        "derived_from": "canonical active claim state",
        "items": items,
    }


def sync_research_bank_sidecars(
    repo_root: Path,
    claims: dict[str, dict[str, Any]],
) -> dict[str, int]:
    """Rebuild every bank's Research preload sidecar from canonical active claims."""
    root = Path(repo_root)
    rows_by_bank: dict[str, list[dict[str, Any]]] = {bank: [] for bank in BANK_IDS}
    for value in claims.values():
        if not _inventory_claim(value):
            continue
        bank = str(value.get("stock_bank") or "").lower()
        if bank not in rows_by_bank:
            order = value.get("pool_order")
            if isinstance(order, int) and not isinstance(order, bool) and order >= 0:
                bank = bank_for_sequence(order)
        if bank in rows_by_bank:
            rows_by_bank[bank].append(value)

    populated = 0
    item_count = 0
    for bank in BANK_IDS:
        rows = rows_by_bank[bank]
        if rows:
            populated += 1
            item_count += len(rows)
        _write(
            root / research_preload_slot_path(bank),
            _research_sidecar_payload(bank, rows),
        )
    return {
        "research_sidecar_banks": len(BANK_IDS),
        "research_stock_banks": populated,
        "research_stock_items": item_count,
    }


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


def fallback_stock_bank(job_id: str) -> str:
    """Assign direct-allocation Research stock deterministically when FIFO stock is empty."""
    material = str(job_id or "").strip().encode("utf-8")
    digest = int(hashlib.sha256(material).hexdigest()[:16], 16)
    return bank_for_sequence(digest)


def _inventory_claim(value: dict[str, Any]) -> bool:
    if not value.get("active") or str(value.get("kind") or "") not in CLAIM_TYPES:
        return False
    return is_pool_claim(value) or value.get("worker_kind") == "scheduled_chat"


def reserved_direct_take_claim_ids(repo_root: Path) -> set[str]:
    """Return pool claim IDs reserved by create-only direct-take markers.

    A marker is authoritative for exclusivity before the background claim lane has
    rewritten the canonical pool claim. This lets a worker start reading immediately
    without allowing a concurrent legacy claim request to adopt the same paper.
    """
    root = Path(repo_root).resolve() / DIRECT_RESEARCH_TAKES
    if not root.is_dir():
        return set()
    reserved: set[str] = set()
    for path in root.glob("*.json"):
        value = _read(path, {})
        claim_id = str(value.get("claim_id") or "") if isinstance(value, dict) else ""
        if claim_id and path.stem == claim_id:
            reserved.add(claim_id)
    return reserved


def waiting_claims(
    claims: dict[str, dict[str, Any]],
    *,
    repo_root: Path | None = None,
) -> list[dict[str, Any]]:
    reserved = reserved_direct_take_claim_ids(repo_root) if repo_root is not None else set()
    return sorted(
        (
            value
            for value in claims.values()
            if value.get("active")
            and is_pool_claim(value)
            and str(value.get("claim_id") or "") not in reserved
        ),
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
    for current in waiting_claims(claims, repo_root=repo_root):
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

    block_size = worker_quota_policy.AUDIT_STARVATION_BLOCK_SIZE
    block_start = next_pipeline_order - (next_pipeline_order % block_size)
    prior_rows = sorted(
        (
            current
            for current in claims.values()
            if current.get("active")
            and current.get("worker_id") == request["worker_id"]
            and current.get("worker_kind") == request["worker_kind"]
            and isinstance(current.get("pipeline_order"), int)
            and not isinstance(current.get("pipeline_order"), bool)
            and block_start <= int(current["pipeline_order"]) < next_pipeline_order
        ),
        key=lambda current: int(current["pipeline_order"]),
    )
    prior_kinds = [str(current.get("kind") or "") for current in prior_rows]
    candidates = worker_quota_policy.order_with_audit_fairness(
        candidates,
        starting_position=next_pipeline_order,
        prior_kinds=prior_kinds,
        kind_field="kind",
        limit=needed,
        reserve_missing_audit_slot=True,
    )

    adopted: list[dict[str, Any]] = []
    new_expiry = _iso(now + dt.timedelta(seconds=int(request["lease_seconds"])))
    for offset, current in enumerate(candidates):
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
    sync_research_bank_sidecars(repo_root, claims)
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
        order = current.get("pool_order")
        desired_stock_bank = (
            bank_for_sequence(int(order))
            if isinstance(order, int) and not isinstance(order, bool) and int(order) >= 0
            else None
        )
        route_missing = (
            desired_stock_bank is not None
            and str(current.get("stock_bank") or "").lower() != desired_stock_bank
        )
        if (
            expires is None
            or (expires - now).total_seconds() <= POOL_RENEW_BEFORE_SECONDS
            or route_missing
        ):
            claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
            claim["expires_at"] = _iso(now + dt.timedelta(seconds=POOL_LEASE_SECONDS))
            claim["heartbeat_at"] = _iso(now)
            if desired_stock_bank is not None:
                claim["stock_bank"] = desired_stock_bank
                claim["stock_lane"] = "research"
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
            "stock_bank": bank_for_sequence(order),
            "stock_lane": "research",
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
    sidecars = sync_research_bank_sidecars(root, claims)
    return {
        "target": int(target),
        "created": created,
        "renewed": renewed,
        "released": released,
        "inventory_active": inventory_active,
        "pool_waiting": pool_waiting,
        **sidecars,
        "research_stock_bank_target": len(BANK_IDS),
        "shortfall": max(int(target) - inventory_active, 0),
    }
