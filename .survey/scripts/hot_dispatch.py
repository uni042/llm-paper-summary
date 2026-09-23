#!/usr/bin/env python3
"""Build and reconcile the zero-wait hot dispatch surface for survey workers.

The hot-dispatch index is a rebuildable acceleration artifact.  It exposes already
prepared Research/Audit pool claims and Discovery preload windows in one read.  A
worker reserves one item with a create-only GitHub write and may immediately start
content work.  Canonical claim allocation, record-bank reservation, run-state
publication and Discovery run-specific precheck continue asynchronously and remain
the submission authority.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import claim_state
import claim_window_policy
import claim_worker
import claim_worker_with_banks
import discovery_preload_queue
import derive_worker_run_state
import shared_preload_pool
import worker_identity
from record_bank_config import BANK_IDS, bank_for_sequence, discovery_slot_path

INDEX = Path(".survey/work-queue/hot-dispatch.json")
DIRECT_RESEARCH_TAKES = Path(".survey/work-queue/direct-takes/research")
DIRECT_RESEARCH_RESULTS = Path(".survey/work-queue/direct-take-results/research")
DIRECT_DISCOVERY_RESULTS = Path(".survey/work-queue/direct-take-results/discovery")
CLAIM_REQUESTS = Path(".survey/work-queue/claim-requests")
CLAIM_RESULTS = Path(".survey/work-queue/claim-results")
CLAIMS = Path(".survey/work-queue/claims")
JOBS = Path(".survey/work-queue/jobs")
PRECHECK_REQUESTS = Path(".survey/work-queue/discovery-precheck/requests")
PRECHECK_RESULTS = Path(".survey/work-queue/discovery-precheck/results")
DISCOVERY_ENTRIES = Path(".survey/work-queue/discovery-preload/entries")
DISCOVERY_CLAIMS = Path(".survey/work-queue/discovery-preload/claims")

MAX_RESEARCH_PACKETS = 64
MAX_DISCOVERY_PACKETS_PER_DIRECTION = 16
DIRECT_ROUTE_GUARD_BAND = claim_window_policy.DEFAULT_CLAIM_WINDOW * 2


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


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


def _jobs(root: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    folder = root / JOBS
    if not folder.is_dir():
        return out
    for path in folder.glob("*.json"):
        value = _read(path, {})
        if not isinstance(value, dict):
            continue
        job_id = str(value.get("job_id") or path.stem)
        if not job_id or path.stem != job_id:
            continue
        out[job_id] = value
    return out


def _candidate_inventory(jobs: dict[str, dict[str, Any]]) -> int:
    return sum(
        1
        for job in jobs.values()
        if job.get("status") == "ready" and job.get("type") in {"research", "audit"}
    )


def _stock_bank(claim: dict[str, Any]) -> str:
    bank = str(claim.get("stock_bank") or "").lower()
    if bank in BANK_IDS:
        return bank
    order = claim.get("pool_order")
    if isinstance(order, int) and not isinstance(order, bool) and order >= 0:
        return bank_for_sequence(order)
    return shared_preload_pool.fallback_stock_bank(str(claim.get("job_id") or ""))


def _research_packets(
    root: Path,
    *,
    jobs: dict[str, dict[str, Any]],
    claims: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for current in shared_preload_pool.waiting_claims(claims, repo_root=root):
        job_id = str(current.get("job_id") or "")
        claim_id = str(current.get("claim_id") or "")
        attempt_id = str(current.get("attempt_id") or "")
        job = jobs.get(job_id)
        if (
            not job_id
            or not claim_id
            or not attempt_id
            or not isinstance(job, dict)
            or job.get("status") != "ready"
            or job.get("type") not in {"research", "audit"}
            or job.get("repair_required") is True
        ):
            continue
        dependencies = claim_state.normalize_dependencies(
            job_id,
            job["depends_on_job_ids"] if "depends_on_job_ids" in job else job.get("dependencies"),
        )
        if dependencies is None or list(current.get("depends_on_job_ids") or []) != dependencies:
            continue
        packets.append(
            {
                "claim_id": claim_id,
                "job_id": job_id,
                "attempt_id": attempt_id,
                "kind": str(current.get("kind") or job.get("type") or ""),
                "pool_order": current.get("pool_order"),
                "preloaded_at": current.get("preloaded_at") or current.get("claimed_at"),
                "stock_bank": _stock_bank(current),
                "take_path": (DIRECT_RESEARCH_TAKES / f"{claim_id}.json").as_posix(),
                "take_result_path": (DIRECT_RESEARCH_RESULTS / f"{claim_id}.json").as_posix(),
                "job_path": (JOBS / f"{job_id}.json").as_posix(),
                "job": job,
            }
        )
        if len(packets) >= MAX_RESEARCH_PACKETS:
            break
    return packets


def _discovery_packets(root: Path) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {}
    for direction in ("backward", "forward", "normal"):
        rows = discovery_preload_queue.available_preloads(
            root,
            direction=direction,
            limit=MAX_DISCOVERY_PACKETS_PER_DIRECTION,
        )
        packets: list[dict[str, Any]] = []
        for row in rows:
            preload_id = str(row.get("preload_id") or "")
            if not preload_id:
                continue
            item = dict(row)
            item["take_path"] = (DISCOVERY_CLAIMS / f"{preload_id}.json").as_posix()
            item["take_result_path"] = (DIRECT_DISCOVERY_RESULTS / f"{preload_id}.json").as_posix()
            packets.append(item)
        out[direction] = packets
    return out


def build_index(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    now = _utcnow()
    jobs = _jobs(root)
    claims = claim_state.current_claims(root, now)

    # Keep the historical per-bank Research sidecars alive as a secondary inspection
    # surface.  Missing stock_bank fields are deterministically reconstructed from
    # pool_order by sync_research_bank_sidecars().
    shared_preload_pool.sync_research_bank_sidecars(root, claims)

    inventory = _candidate_inventory(jobs)
    threshold = claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD
    suggested = "research" if inventory >= threshold else "discovery"
    margin = abs(inventory - threshold)
    return {
        "schema_version": 1,
        "generated_at": _iso(now),
        "candidate_inventory": inventory,
        "research_discovery_threshold": threshold,
        "suggested_work_mode": suggested,
        "direct_start_allowed": margin > DIRECT_ROUTE_GUARD_BAND,
        "route_guard_band": DIRECT_ROUTE_GUARD_BAND,
        "rule": (
            "This is a rebuildable acceleration index. A create-only take reserves one prepared item immediately; "
            "canonical run-state/precheck/claim publication continues asynchronously. If direct_start_allowed is false, "
            "fall back to the normal synchronous run-state route before starting new work."
        ),
        "research": _research_packets(root, jobs=jobs, claims=claims),
        "discovery": _discovery_packets(root),
    }


def refresh(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    value = build_index(root)
    _write(root / INDEX, value)
    return value


def _safe_request_id(value: Any) -> str:
    value = str(value or "")
    if not claim_worker.SAFE_ID_RE.fullmatch(value):
        raise ValueError("request_id must be a safe transport identifier")
    return value


def _normalize_research_take(path: Path, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("direct Research take must be an object")
    if value.get("schema_version") != 1 or value.get("operation") != "direct_take_research":
        raise ValueError("direct Research take requires schema_version=1 and operation=direct_take_research")
    claim_id = str(value.get("claim_id") or "")
    if not claim_id or path.stem != claim_id:
        raise ValueError("claim_id must match the marker filename")
    job_id = str(value.get("job_id") or "")
    attempt_id = str(value.get("attempt_id") or "")
    if not job_id or not attempt_id:
        raise ValueError("job_id and attempt_id are required")
    worker_id = str(value.get("worker_id") or "")
    scheduled_slot = str(value.get("scheduled_slot") or "")
    if not worker_identity.is_supported_worker_id(worker_id):
        raise ValueError("unsupported worker_id")
    worker_identity.validate_identity_slot(worker_id, scheduled_slot)
    run_key = str(value.get("run_key") or "")
    if not run_key:
        raise ValueError("run_key is required")
    start = claim_state.parse_time(value.get("actual_invocation_start"))
    if start is None:
        raise ValueError("actual_invocation_start must be offset-aware")
    requested = claim_state.parse_time(value.get("requested_at"))
    if requested is None:
        raise ValueError("requested_at must be offset-aware")
    request_id = _safe_request_id(value.get("request_id"))
    inventory = value.get("candidate_inventory_at_start")
    threshold = value.get("research_discovery_threshold")
    if (
        isinstance(inventory, bool)
        or not isinstance(inventory, int)
        or isinstance(threshold, bool)
        or not isinstance(threshold, int)
        or threshold != claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD
        or inventory < threshold
        or str(value.get("work_mode_at_start") or "") != "research"
    ):
        raise ValueError("direct Research route is inconsistent with the current mode threshold")
    raw_window = value.get("claim_window", claim_window_policy.DEFAULT_CLAIM_WINDOW)
    claim_window = claim_window_policy.normalize_window(raw_window)
    return {
        **value,
        "claim_id": claim_id,
        "job_id": job_id,
        "attempt_id": attempt_id,
        "worker_id": worker_id,
        "scheduled_slot": scheduled_slot,
        "run_key": run_key,
        "actual_invocation_start": _iso(start),
        "requested_at": _iso(requested),
        "request_id": request_id,
        "claim_window": claim_window,
    }


def _research_refill_request_id(take: dict[str, Any]) -> str:
    material = "\n".join(
        str(take.get(key) or "")
        for key in ("claim_id", "worker_id", "run_key", "actual_invocation_start")
    )
    return "direct-refill-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _next_pipeline_order(claims: dict[str, dict[str, Any]], take: dict[str, Any]) -> int:
    orders: list[int] = []
    for current in claims.values():
        if not current.get("active") or current.get("worker_kind") != "scheduled_chat":
            continue
        if current.get("worker_id") != take["worker_id"]:
            continue
        order = current.get("pipeline_order")
        if isinstance(order, int) and not isinstance(order, bool) and order >= 0:
            orders.append(order)
    return max(orders, default=-1) + 1


def process_research_takes(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    marker_root = root / DIRECT_RESEARCH_TAKES
    result_root = root / DIRECT_RESEARCH_RESULTS
    marker_root.mkdir(parents=True, exist_ok=True)
    result_root.mkdir(parents=True, exist_ok=True)
    processed = failures = 0
    created_refills: list[str] = []

    for path in sorted(marker_root.glob("*.json")):
        result_path = result_root / path.name
        existing = _read(result_path, {})
        if isinstance(existing, dict) and existing.get("status") in {
            "canonicalizing",
            "ready_for_submission",
            "recovery_required",
        }:
            continue
        try:
            take = _normalize_research_take(path, _read(path, {}))
            now = _utcnow()
            claims = claim_state.current_claims(root, now)
            current = claims.get(take["job_id"])
            if (
                not isinstance(current, dict)
                or current.get("active") is not True
                or not shared_preload_pool.is_pool_claim(current)
                or current.get("claim_id") != take["claim_id"]
                or current.get("attempt_id") != take["attempt_id"]
            ):
                raise ValueError("prepared Research claim is no longer the reserved pool identity")
            job = _read(root / JOBS / f"{take['job_id']}.json", {})
            if (
                not isinstance(job, dict)
                or job.get("status") != "ready"
                or job.get("type") not in {"research", "audit"}
                or job.get("repair_required") is True
            ):
                raise ValueError("prepared Research job is no longer direct-take eligible")

            claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
            claim["preload_pool"] = False
            claim["preload_pool_adopted_at"] = _iso(now)
            claim["preload_pool_worker_id"] = shared_preload_pool.POOL_WORKER_ID
            claim["worker_id"] = take["worker_id"]
            claim["worker_kind"] = "scheduled_chat"
            claim["request_id"] = take["request_id"]
            claim["claimed_at"] = _iso(now)
            claim["heartbeat_at"] = _iso(now)
            claim["expires_at"] = _iso(now + dt.timedelta(seconds=claim_worker.DEFAULT_LEASE_SECONDS))
            claim["pipeline_order"] = _next_pipeline_order(claims, take)
            claim["run_key"] = take["run_key"]
            claim["scheduled_slot"] = take["scheduled_slot"]
            claim["actual_invocation_start"] = take["actual_invocation_start"]
            claim["stock_bank"] = _stock_bank(current)
            claim["stock_lane"] = "research"
            claim["direct_take"] = True
            claim["direct_take_marker"] = path.relative_to(root).as_posix()
            _write(root / CLAIMS / f"{take['job_id']}.json", claim)

            refill_id = _research_refill_request_id(take)
            refill_path = root / CLAIM_REQUESTS / f"{refill_id}.json"
            canonical_result = CLAIM_RESULTS / f"{refill_id}.json"
            if not refill_path.exists() and not (root / canonical_result).exists():
                _write(
                    refill_path,
                    {
                        "schema_version": 1,
                        "request_id": refill_id,
                        "worker_id": take["worker_id"],
                        "worker_kind": "scheduled_chat",
                        "requested_at": _iso(now),
                        "max_jobs": 1,
                        "claim_window": take["claim_window"],
                        "lease_seconds": claim_worker.DEFAULT_LEASE_SECONDS,
                        "job_types": ["research", "audit"],
                        "run_key": take["run_key"],
                        "scheduled_slot": take["scheduled_slot"],
                        "actual_invocation_start": take["actual_invocation_start"],
                        "direct_take_refill": True,
                        "source_direct_take_claim_id": take["claim_id"],
                    },
                )
                created_refills.append(refill_path.relative_to(root).as_posix())

            _write(
                result_path,
                {
                    "schema_version": 1,
                    "operation": "direct_take_research",
                    "ok": True,
                    "claim_id": take["claim_id"],
                    "job_id": take["job_id"],
                    "attempt_id": take["attempt_id"],
                    "worker_id": take["worker_id"],
                    "run_key": take["run_key"],
                    "status": "canonicalizing",
                    "work_start_allowed": True,
                    "record_write_allowed": False,
                    "canonical_claim_result_path": canonical_result.as_posix(),
                    "processed_at": _iso(now),
                },
            )
            processed += 1
        except Exception as exc:
            failures += 1
            _write(
                result_path,
                {
                    "schema_version": 1,
                    "operation": "direct_take_research",
                    "ok": False,
                    "claim_id": path.stem,
                    "status": "recovery_required",
                    "work_start_allowed": False,
                    "record_write_allowed": False,
                    "error": f"{type(exc).__name__}: {exc}",
                    "processed_at": _iso(_utcnow()),
                },
            )

    return {
        "processed": processed,
        "failures": failures,
        "created_refill_requests": created_refills,
    }


def finalize_research_takes(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    updated = 0
    result_root = root / DIRECT_RESEARCH_RESULTS
    if not result_root.is_dir():
        return {"updated": 0}
    for path in sorted(result_root.glob("*.json")):
        value = _read(path, {})
        if not isinstance(value, dict) or value.get("ok") is not True:
            continue
        canonical_rel = str(value.get("canonical_claim_result_path") or "")
        if not canonical_rel:
            continue
        canonical = _read(root / canonical_rel, {})
        if not isinstance(canonical, dict) or canonical.get("ok") is not True:
            continue
        assignment = next(
            (
                item
                for item in canonical.get("assignments") or []
                if isinstance(item, dict)
                and item.get("job_id") == value.get("job_id")
                and item.get("claim_id") == value.get("claim_id")
            ),
            None,
        )
        if assignment is None:
            continue
        desired = dict(value)
        desired["status"] = "ready_for_submission"
        desired["canonical_claim_ready"] = True
        desired["record_write_allowed"] = True
        desired["assignment"] = assignment
        desired["canonicalized_at"] = str(canonical.get("processed_at") or _iso(_utcnow()))
        if desired != value:
            _write(path, desired)
            updated += 1
    return {"updated": updated}


def _normalize_direct_discovery_claim(path: Path, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or not (
        value.get("direct_take") is True
        or value.get("operation") == "direct_take_discovery"
    ):
        raise ValueError("not a direct Discovery take")
    preload_id = str(value.get("preload_id") or "")
    if not preload_id or path.stem != preload_id:
        raise ValueError("preload_id must match the claim filename")
    worker_id = str(value.get("worker_id") or "")
    if not worker_identity.is_supported_worker_id(worker_id):
        raise ValueError("unsupported worker_id")
    run_key = str(value.get("run_key") or "")
    if not run_key or run_key.startswith("preload:"):
        raise ValueError("real run_key is required")
    request_id = _safe_request_id(value.get("request_id"))
    claimed = claim_state.parse_time(value.get("claimed_at") or value.get("requested_at"))
    expires = claim_state.parse_time(value.get("lease_expires_at"))
    if claimed is not None and expires is None:
        expires = claimed + dt.timedelta(seconds=discovery_preload_queue.CLAIM_LEASE_SECONDS)
    if claimed is None or expires is None or expires <= _utcnow():
        raise ValueError("direct Discovery claim lease is missing or expired")
    inventory = value.get("candidate_inventory_at_start")
    threshold = value.get("research_discovery_threshold")
    if (
        isinstance(inventory, bool)
        or not isinstance(inventory, int)
        or isinstance(threshold, bool)
        or not isinstance(threshold, int)
        or threshold != claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD
        or inventory >= threshold
        or str(value.get("work_mode_at_start") or "") != "discovery"
    ):
        raise ValueError("direct Discovery route is inconsistent with the current mode threshold")
    return {**value, "preload_id": preload_id, "worker_id": worker_id, "run_key": run_key, "request_id": request_id}


def materialize_discovery_prechecks(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    claim_root = root / DISCOVERY_CLAIMS
    result_root = root / DIRECT_DISCOVERY_RESULTS
    result_root.mkdir(parents=True, exist_ok=True)
    created = reused = failures = 0

    for path in sorted(claim_root.glob("*.json")) if claim_root.is_dir() else []:
        raw = _read(path, {})
        if not isinstance(raw, dict) or not (
            raw.get("direct_take") is True
            or raw.get("operation") == "direct_take_discovery"
        ):
            continue
        direct_result = result_root / path.name
        try:
            claim = _normalize_direct_discovery_claim(path, raw)
            request_path = root / PRECHECK_REQUESTS / f"{claim['request_id']}.json"
            precheck_result_path = root / PRECHECK_RESULTS / f"{claim['request_id']}.json"
            if precheck_result_path.exists():
                reused += 1
                continue
            if request_path.exists():
                reused += 1
                continue
            entry = _read(root / DISCOVERY_ENTRIES / f"{claim['preload_id']}.json", {})
            if not isinstance(entry, dict) or entry.get("preload_id") != claim["preload_id"]:
                raise ValueError("Discovery preload entry is missing")
            bank = str(claim.get("discovery_bank") or "").lower()
            if bank not in BANK_IDS:
                raise ValueError("direct Discovery take requires a valid discovery_bank")
            slot_path = str(claim.get("discovery_slot_path") or "")
            if slot_path != discovery_slot_path(bank):
                raise ValueError("direct Discovery take slot path does not match its bank")
            _write(
                request_path,
                {
                    "schema_version": 3,
                    "operation": "precheck_discovery_candidates",
                    "request_id": claim["request_id"],
                    "collector_id": f"direct-{claim['request_id']}"[:160],
                    "run_key": claim["run_key"],
                    "axis": entry["axis"],
                    "provider": entry["provider"],
                    "source_url": entry["source_url"],
                    "target_unseen": int(entry.get("target_unseen") or discovery_preload_queue.DEFAULT_TARGET_UNSEEN),
                    "page_size": int(entry.get("page_size") or discovery_preload_queue.DEFAULT_PAGE_SIZE),
                    "max_pages": int(entry.get("max_pages") or discovery_preload_queue.DEFAULT_MAX_PAGES),
                    "initial_cursor": entry.get("initial_cursor"),
                    "preload_id": claim["preload_id"],
                    "preload_seed": False,
                    "worker_id": claim["worker_id"],
                    "discovery_bank": bank,
                    "discovery_slot_path": slot_path,
                    "direct_take": True,
                },
            )
            _write(
                direct_result,
                {
                    "schema_version": 1,
                    "operation": "direct_take_discovery",
                    "ok": True,
                    "preload_id": claim["preload_id"],
                    "request_id": claim["request_id"],
                    "worker_id": claim["worker_id"],
                    "run_key": claim["run_key"],
                    "status": "precheck_pending",
                    "work_start_allowed": True,
                    "submission_allowed": False,
                    "preload_result_path": str(claim.get("preload_result_path") or ""),
                    "formal_precheck_result_path": (PRECHECK_RESULTS / f"{claim['request_id']}.json").as_posix(),
                    "processed_at": _iso(_utcnow()),
                },
            )
            created += 1
        except Exception as exc:
            failures += 1
            _write(
                direct_result,
                {
                    "schema_version": 1,
                    "operation": "direct_take_discovery",
                    "ok": False,
                    "preload_id": path.stem,
                    "status": "recovery_required",
                    "work_start_allowed": False,
                    "submission_allowed": False,
                    "error": f"{type(exc).__name__}: {exc}",
                    "processed_at": _iso(_utcnow()),
                },
            )
    return {"created": created, "reused": reused, "failures": failures}


def finalize_discovery_takes(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    updated = 0
    result_root = root / DIRECT_DISCOVERY_RESULTS
    if not result_root.is_dir():
        return {"updated": 0}
    for path in sorted(result_root.glob("*.json")):
        value = _read(path, {})
        if not isinstance(value, dict) or value.get("ok") is not True:
            continue
        request_id = str(value.get("request_id") or "")
        if not request_id:
            continue
        formal = _read(root / PRECHECK_RESULTS / f"{request_id}.json", {})
        if not isinstance(formal, dict) or formal.get("request_id") != request_id:
            continue
        desired = dict(value)
        if formal.get("ok") is True and formal.get("evaluation_allowed") is True:
            desired["status"] = "ready_for_submission"
            desired["submission_allowed"] = True
            desired["receipt"] = formal.get("receipt")
        elif formal.get("ok") is False:
            desired["status"] = "recovery_required"
            desired["submission_allowed"] = False
            desired["error"] = formal.get("error")
        else:
            continue
        desired["formal_precheck_ready_at"] = str(formal.get("progress_observed_at") or _iso(_utcnow()))
        if desired != value:
            _write(path, desired)
            updated += 1
    return {"updated": updated}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("refresh")
    sub.add_parser("process-research")
    sub.add_parser("finalize-research")
    sub.add_parser("materialize-discovery")
    sub.add_parser("finalize-discovery")
    args = parser.parse_args()

    if args.command == "refresh":
        result = refresh(args.repo_root)
    elif args.command == "process-research":
        result = process_research_takes(args.repo_root)
    elif args.command == "finalize-research":
        result = finalize_research_takes(args.repo_root)
    elif args.command == "materialize-discovery":
        result = materialize_discovery_prechecks(args.repo_root)
    elif args.command == "finalize-discovery":
        result = finalize_discovery_takes(args.repo_root)
    else:  # pragma: no cover
        raise AssertionError(args.command)

    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
