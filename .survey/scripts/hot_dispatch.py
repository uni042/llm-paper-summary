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
DISCOVERY_FRONTIER_TARGET = 3
# Kept in the index schema for read compatibility. Candidate count no longer
# disables a prepared lane; direct-start availability is stock-driven.
DIRECT_ROUTE_GUARD_BAND = 0


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


def _latest_discovery_completion(
    jobs: dict[str, dict[str, Any]],
) -> dt.datetime | None:
    latest: dt.datetime | None = None
    for job in jobs.values():
        if job.get("type") != "discovery" or job.get("status") != "completed":
            continue
        completed = claim_state.parse_time(job.get("completed_at"))
        if completed is not None and (latest is None or completed > latest):
            latest = completed
    return latest


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
    resume_affinities: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for current in shared_preload_pool.waiting_claims(claims, repo_root=root):
        job_id = str(current.get("job_id") or "")
        claim_id = str(current.get("claim_id") or "")
        attempt_id = str(current.get("attempt_id") or "")
        job = jobs.get(job_id)
        affinity = (resume_affinities or {}).get(job_id)
        if affinity and affinity.get("sticky_to_worker") is True:
            continue
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


def _submission_descriptor_exists(root: Path, kind: str, attempt_id: str) -> bool:
    if kind not in {"research", "audit"} or not attempt_id:
        return False
    folder = root / ".survey/work-queue/submissions" / kind
    canonical = folder / f"{attempt_id}.json"
    if canonical.is_file():
        return True
    if not folder.is_dir():
        return False
    for path in folder.glob("*.json"):
        value = _read(path, {})
        if isinstance(value, dict) and value.get("attempt_id") == attempt_id:
            return True
    return False


def _research_resume_packets(
    root: Path,
    *,
    jobs: dict[str, dict[str, Any]],
    claims: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Expose already-owned unsubmitted work for zero-wait cross-run resume."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for job_id, current in claims.items():
        if not current.get("active") or current.get("worker_kind") != "scheduled_chat":
            continue
        worker_id = str(current.get("worker_id") or "")
        if not worker_identity.is_supported_worker_id(worker_id):
            continue
        claim_id = str(current.get("claim_id") or "")
        attempt_id = str(current.get("attempt_id") or "")
        kind = str(current.get("kind") or "")
        job = jobs.get(job_id)
        if (
            not claim_id
            or not attempt_id
            or kind not in {"research", "audit"}
            or not isinstance(job, dict)
            or job.get("status") != "ready"
            or job.get("type") not in {"research", "audit"}
            or _submission_descriptor_exists(root, kind, attempt_id)
        ):
            continue
        slot_paths = current.get("record_slot_paths")
        route_ready = bool(
            isinstance(slot_paths, dict)
            and slot_paths
            and all(isinstance(value, str) and value for value in slot_paths.values())
        )
        packet: dict[str, Any] = {
            "claim_id": claim_id,
            "job_id": job_id,
            "attempt_id": attempt_id,
            "kind": kind,
            "worker_id": worker_id,
            "claimed_at": current.get("claimed_at"),
            "pipeline_order": current.get("pipeline_order"),
            "source_run_key": current.get("run_key"),
            "source_scheduled_slot": current.get("scheduled_slot"),
            "source_actual_invocation_start": current.get("actual_invocation_start"),
            "claim_path": (CLAIMS / f"{job_id}.json").as_posix(),
            "job_path": (JOBS / f"{job_id}.json").as_posix(),
            "job": job,
            "resume_without_new_claim": True,
            "work_start_allowed": True,
            "record_write_allowed": route_ready,
            "status_only_submission_path": (
                Path(".survey/work-queue/submissions") / kind / f"{attempt_id}.json"
            ).as_posix(),
            "status_only_allowed_statuses": ["blocked", "deferred", "rejected"],
            "status_only_descriptor_base": {
                "schema_version": 1,
                "transport_version": 10,
                "kind": kind,
                "attempt_id": attempt_id,
                "job_id": job_id,
                "claim_id": claim_id,
                "worker_id": worker_id,
            },
            "platform_content_write_recovery": {
                "trigger": "record_slot_update_and_quality_preflight_bundle_rejected",
                "create_only": True,
                "submission_path": (
                    Path(".survey/work-queue/submissions") / kind / f"{attempt_id}.json"
                ).as_posix(),
                "descriptor": {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": kind,
                    "attempt_id": attempt_id,
                    "job_id": job_id,
                    "claim_id": claim_id,
                    "worker_id": worker_id,
                    "status": "blocked",
                    "reason": "platform_content_write_rejected_after_bundle_fallback",
                },
                "continue_after_durable_create": True,
                "retry_policy": "blocked_retry_7d",
                "on_status_only_write_rejected": {
                    "next_action": "UPDATE_HEALTH_PROBE_THEN_WRITE_MINIMAL_RUN_STATE_QUARANTINE",
                    "health_probe_path": ".survey/work-queue/transport/health-probe.json",
                    "health_probe_operation": "update_existing_file_once",
                    "health_probe_requires_latest_blob_sha": True,
                    "run_state_runtime_condition": "none",
                    "write_blocked_job_base": {
                        "job_id": job_id,
                        "claim_id": claim_id,
                        "attempt_id": attempt_id,
                        "reason": "platform_content_write_rejected_after_bundle_fallback",
                    },
                    "carry_intended_status_reason_as": "source_reason",
                    "continue_after_quarantine_result": True,
                },
            },
            "source_unavailable_next_action": (
                "WRITE_STATUS_ONLY_BLOCKED_DESCRIPTOR_THEN_CONTINUE_STANDBY"
            ),
        }
        for key in (
            "record_bank",
            "record_bank_root",
            "record_slot_paths",
            "record_bank_fallback",
            "direct_take",
            "direct_take_marker",
            "stock_bank",
            "stock_lane",
        ):
            if key in current:
                packet[key] = current[key]
        grouped.setdefault(worker_id, []).append(packet)

    for rows in grouped.values():
        rows.sort(key=lambda item: (
            int(item.get("pipeline_order"))
            if isinstance(item.get("pipeline_order"), int)
            and not isinstance(item.get("pipeline_order"), bool)
            and int(item.get("pipeline_order")) >= 0
            else 1_000_000_000,
            str(item.get("claimed_at") or ""),
            str(item.get("job_id") or ""),
        ))
        for position, item in enumerate(rows, start=1):
            item["pipeline_position"] = position
            item["pipeline_role"] = "foreground" if position == 1 else "standby"
    return {worker_id: grouped[worker_id] for worker_id in sorted(grouped)}


def _research_recovery_resume_packets(
    root: Path,
    *,
    jobs: dict[str, dict[str, Any]],
    claims: dict[str, dict[str, Any]],
    resume_affinities: dict[str, dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    """Expose pool claims that carry durable unfinished work for their old worker."""
    grouped: dict[str, list[dict[str, Any]]] = {}
    for current in shared_preload_pool.waiting_claims(claims, repo_root=root):
        job_id = str(current.get("job_id") or "")
        affinity = resume_affinities.get(job_id)
        if not affinity:
            continue
        worker_id = str(affinity.get("worker_id") or "")
        if not worker_identity.is_supported_worker_id(worker_id):
            continue
        job = jobs.get(job_id)
        claim_id = str(current.get("claim_id") or "")
        attempt_id = str(current.get("attempt_id") or "")
        kind = str(current.get("kind") or (job or {}).get("type") or "")
        if (
            not claim_id
            or not attempt_id
            or kind not in {"research", "audit"}
            or not isinstance(job, dict)
            or job.get("status") != "ready"
            or job.get("type") not in {"research", "audit"}
            or job.get("repair_required") is True
        ):
            continue
        packet = {
            "claim_id": claim_id,
            "job_id": job_id,
            "attempt_id": attempt_id,
            "kind": kind,
            "worker_id": worker_id,
            "pool_order": current.get("pool_order"),
            "preloaded_at": current.get("preloaded_at") or current.get("claimed_at"),
            "stock_bank": _stock_bank(current),
            "take_path": (DIRECT_RESEARCH_TAKES / f"{claim_id}.json").as_posix(),
            "take_result_path": (DIRECT_RESEARCH_RESULTS / f"{claim_id}.json").as_posix(),
            "claim_path": (CLAIMS / f"{job_id}.json").as_posix(),
            "job_path": (JOBS / f"{job_id}.json").as_posix(),
            "job": job,
            "resume_recovery": True,
            "resume_requires_direct_take": False,
            "recovery_transport": "run_state_auto_claim",
            "resume_without_new_claim": False,
            "work_start_allowed": True,
            "record_write_allowed": False,
            "recovery_source_worker_id": worker_id,
            "recovery_source_claim_id": affinity.get("source_claim_id"),
            "recovery_source_attempt_id": affinity.get("source_attempt_id"),
            "recovery_source_record_bank": affinity.get("source_record_bank"),
            "recovery_source_record_bank_root": affinity.get("source_record_bank_root"),
            "recovery_source_record_slot_paths": affinity.get("source_record_slot_paths"),
            "recovery_nonempty_slot_count": affinity.get("nonempty_slot_count"),
        }
        grouped.setdefault(worker_id, []).append(packet)

    for rows in grouped.values():
        rows.sort(key=lambda item: (
            int(item.get("pool_order"))
            if isinstance(item.get("pool_order"), int)
            and not isinstance(item.get("pool_order"), bool)
            else 1_000_000_000,
            str(item.get("preloaded_at") or ""),
            str(item.get("job_id") or ""),
        ))
    return {worker_id: grouped[worker_id] for worker_id in sorted(grouped)}


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
    latest_discovery_at = _latest_discovery_completion(jobs)
    discovery_age_seconds = (
        max(0, int((now - latest_discovery_at).total_seconds()))
        if latest_discovery_at is not None
        else None
    )
    discovery_refresh_due = claim_window_policy.discovery_refresh_due(
        inventory,
        discovery_age_seconds=discovery_age_seconds,
    )
    suggested = claim_window_policy.select_work_mode(
        inventory,
        discovery_age_seconds=discovery_age_seconds,
    )
    resume_affinities = shared_preload_pool.unfinished_resume_affinities(root)
    research_packets = _research_packets(
        root,
        jobs=jobs,
        claims=claims,
        resume_affinities=resume_affinities,
    )
    research_resume = _research_resume_packets(root, jobs=jobs, claims=claims)
    research_recovery_resume = _research_recovery_resume_packets(
        root,
        jobs=jobs,
        claims=claims,
        resume_affinities=resume_affinities,
    )
    discovery_packets = _discovery_packets(root)
    discovery_primary_direction = "backward"
    discovery_primary_packets = discovery_packets.get(discovery_primary_direction) or []
    discovery_fallback = discovery_preload_queue.fallback_source(
        root,
        direction=discovery_primary_direction,
    )
    discovery_start_lookahead = next(
        (
            packet
            for packet in (discovery_packets.get("forward") or [])
            if int(packet.get("preload_unseen_result_count") or 0) > 0
        ),
        None,
    )
    primary_preload_id = str(
        discovery_primary_packets[0].get("preload_id") or ""
    ) if discovery_primary_packets else ""
    discovery_start_frontier: list[dict[str, Any]] = []
    seen_frontier_ids = {primary_preload_id} if primary_preload_id else set()
    for direction in ("forward", "backward", "normal"):
        for packet in discovery_packets.get(direction) or []:
            preload_id = str(packet.get("preload_id") or "")
            if (
                not preload_id
                or preload_id in seen_frontier_ids
                or int(packet.get("preload_unseen_result_count") or 0) <= 0
            ):
                continue
            discovery_start_frontier.append(packet)
            seen_frontier_ids.add(preload_id)
            if len(discovery_start_frontier) >= DISCOVERY_FRONTIER_TARGET - 1:
                break
        if len(discovery_start_frontier) >= DISCOVERY_FRONTIER_TARGET - 1:
            break
    generated_at = _iso(now)
    recovery_packets = [
        packet
        for rows in research_recovery_resume.values()
        for packet in rows
    ]
    for packet in recovery_packets:
        packet["run_state_recovery_contract"] = {
            "transport": "auto_recovery_claim",
            "requires_worker_direct_take": False,
            "worker_id": packet.get("worker_id"),
            "job_id": packet.get("job_id"),
            "source_attempt_id": packet.get("recovery_source_attempt_id"),
            "source_record_bank": packet.get("recovery_source_record_bank"),
            "trigger": "persist_or_reuse_current_run_state_request",
        }

    for packet in research_packets:
        if all(packet.get(key) for key in ("take_path", "claim_id", "job_id", "attempt_id")):
            packet["direct_take_contract"] = {
                "create_only": True,
                "path": packet["take_path"],
                "lease_seconds": claim_worker.DEFAULT_LEASE_SECONDS,
                "payload_base": {
                    "schema_version": 1,
                    "operation": "direct_take_research",
                    "claim_id": packet["claim_id"],
                    "job_id": packet["job_id"],
                    "attempt_id": packet["attempt_id"],
                    "claim_window": claim_window_policy.DEFAULT_CLAIM_WINDOW,
                    "candidate_inventory_at_start": inventory,
                    "work_mode_at_start": "research",
                    "research_discovery_threshold": threshold,
                    "hot_dispatch_generated_at": generated_at,
                },
                "required_runtime_fields": [
                    "request_id",
                    "worker_id",
                    "scheduled_slot",
                    "run_key",
                    "actual_invocation_start",
                    "requested_at",
                ],
            }
    for direction_packets in discovery_packets.values():
        for packet in direction_packets:
            if all(
                packet.get(key)
                for key in (
                    "take_path",
                    "preload_id",
                    "discovery_bank",
                    "discovery_slot_path",
                    "preload_result_path",
                )
            ):
                packet["direct_take_contract"] = {
                    "create_only": True,
                    "path": packet["take_path"],
                    "lease_seconds": discovery_preload_queue.CLAIM_LEASE_SECONDS,
                    "payload_base": {
                        "schema_version": 1,
                        "operation": "direct_take_discovery",
                        "direct_take": True,
                        "preload_id": packet["preload_id"],
                        "discovery_bank": packet["discovery_bank"],
                        "discovery_slot_path": packet["discovery_slot_path"],
                        "preload_result_path": packet["preload_result_path"],
                        "candidate_inventory_at_start": inventory,
                        "work_mode_at_start": "discovery",
                        "research_discovery_threshold": threshold,
                        "hot_dispatch_generated_at": generated_at,
                    },
                    "required_runtime_fields": [
                        "request_id",
                        "worker_id",
                        "scheduled_slot",
                        "run_key",
                        "actual_invocation_start",
                        "claimed_at",
                        "lease_expires_at",
                    ],
                }

    lane_available = {
        "research": bool(recovery_packets or research_packets),
        # A fresh Discovery invocation always starts by attempting backward
        # references. Forward/normal stock is still exposed below, but must not
        # falsely advertise direct-start readiness for the primary round.
        "discovery": bool(discovery_primary_packets),
    }
    zero_wait_content_start_allowed = bool(
        (recovery_packets or research_packets)
        if suggested == "research"
        else (
            any(
                int(packet.get("preload_unseen_result_count") or 0) > 0
                for packet in discovery_primary_packets
            )
            or discovery_start_lookahead is not None
        )
    )
    return {
        "schema_version": 1,
        "generated_at": generated_at,
        "candidate_inventory": inventory,
        "research_discovery_threshold": threshold,
        "suggested_work_mode": suggested,
        "latest_discovery_completion_at": (
            _iso(latest_discovery_at) if latest_discovery_at is not None else None
        ),
        "discovery_age_seconds": discovery_age_seconds,
        "discovery_refresh_due": discovery_refresh_due,
        "discovery_refresh_interval_seconds": claim_window_policy.DISCOVERY_REFRESH_INTERVAL_SECONDS,
        "discovery_refresh_max_inventory": claim_window_policy.DISCOVERY_REFRESH_MAX_INVENTORY,
        "direct_start_allowed": lane_available[suggested],
        "zero_wait_start_allowed": bool(
            lane_available[suggested]
            or (suggested == "discovery" and discovery_fallback is not None)
        ),
        "fallback_start_allowed": bool(
            suggested == "discovery" and discovery_fallback is not None
        ),
        "zero_wait_content_start_allowed": zero_wait_content_start_allowed,
        "discovery_primary_direction": (
            discovery_primary_direction if suggested == "discovery" else None
        ),
        "discovery_start_lookahead": (
            discovery_start_lookahead if suggested == "discovery" else None
        ),
        "discovery_frontier_target": DISCOVERY_FRONTIER_TARGET,
        "discovery_start_frontier": (
            discovery_start_frontier if suggested == "discovery" else []
        ),
        "frontier_auto_reserve": suggested == "discovery",
        "discovery_fallback": discovery_fallback if suggested == "discovery" else None,
        "idle_gap_guard": {
            "passive_wait_forbidden": True,
            "rule": (
                "An asynchronous request must never be the worker's only remaining activity. "
                "Prefer PRECHECKED Discovery stock. A direct Discovery take automatically reserves a bounded "
                "same-run work frontier before its formal precheck becomes the only visible activity; evaluate "
                "the already published cached candidates while canonical precheck/run-state results proceed. "
                "If the primary backward packet is absent, start the published fixed-source schema-v3 fallback "
                "and use discovery_start_frontier for immediate cached candidate work."
            ),
        },
        "route_guard_band": DIRECT_ROUTE_GUARD_BAND,
        "lane_available": lane_available,
        "rule": (
            "This is a rebuildable acceleration index. Candidate inventory selects the base work mode; "
            "a bounded freshness override may select Discovery when its last durable completion is stale, "
            "it never disables the prepared Research or Discovery lane. A create-only take reserves one prepared item "
            "immediately, while canonical run-state/precheck/claim publication continues asynchronously. "
            "same-worker active unsubmitted Research/Audit claims are exposed in research_resume and take precedence "
            "over creating a new take, so content work can resume immediately while canonical route repair proceeds; "
            "coherent unsubmitted record banks whose old claim expired are exposed in research_recovery_resume for their "
            "original worker; these packets do not require a worker-side direct-take write. The normal run-state request "
            "causes auto_claim_from_run_state to issue a deterministic job-pinned canonical claim, after which "
            "expired-same-job recovery retags the preserved slots before unrelated fresh FIFO work; "
            "resume packets also expose the canonical status-only submission path/template so a single unreadable paper "
            "can be durably terminalized and the next standby can start without ending the run; "
            "direct_start_allowed requires prepared stock for the fresh invocation's primary route (backward for Discovery), "
            "rather than unrelated forward/normal stock; zero_wait_start_allowed additionally covers the Discovery fixed-source cold-start fallback. "
            "zero_wait_content_start_allowed distinguishes merely starting an asynchronous fallback from having cached candidate work available now. "
            "discovery_start_frontier publishes up to two additional productive packets beside the primary packet; the first direct take causes the "
            "Discovery precheck lane to reserve enough same-run packets to keep a bounded three-round frontier populated before formal results settle. "
            "Each prepared Research/Discovery packet embeds direct_take_contract with the canonical create-only path, schema payload_base, "
            "lease duration and the exact runtime fields still required from the worker, so workers never reconstruct a direct-take schema from prose. "
            "When the backward packet is absent, issue discovery_fallback immediately and use discovery_start_frontier for cached candidate evaluation "
            "without waiting for run-state; formal submission remains gated by each run-specific schema-v3 precheck/receipt."
        ),
        "research": research_packets,
        "research_resume": research_resume,
        "research_recovery_resume": research_recovery_resume,
        "discovery": discovery_packets,
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
        or inventory < 0
        or isinstance(threshold, bool)
        or not isinstance(threshold, int)
        or threshold != claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD
        or str(value.get("work_mode_at_start") or "") != "research"
    ):
        raise ValueError("direct Research route metadata is invalid")
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


def _ensure_research_refill_request(
    root: Path,
    take: dict[str, Any],
    now: dt.datetime,
) -> tuple[str | None, Path]:
    refill_id = _research_refill_request_id(take)
    refill_path = root / CLAIM_REQUESTS / f"{refill_id}.json"
    canonical_result = CLAIM_RESULTS / f"{refill_id}.json"
    created: str | None = None
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
        created = refill_path.relative_to(root).as_posix()
    return created, canonical_result


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
            "ready_for_submission",
            "recovery_required",
        }:
            continue
        if isinstance(existing, dict) and existing.get("status") == "canonicalizing":
            try:
                take = _normalize_research_take(path, _read(path, {}))
                now = _utcnow()
                current = claim_state.current_claims(root, now).get(take["job_id"])
                if (
                    isinstance(current, dict)
                    and current.get("active") is True
                    and current.get("worker_id") == take["worker_id"]
                    and current.get("claim_id") == take["claim_id"]
                    and current.get("attempt_id") == take["attempt_id"]
                ):
                    created, canonical_result = _ensure_research_refill_request(root, take, now)
                    if created is not None:
                        created_refills.append(created)
                    desired = dict(existing)
                    desired["canonical_claim_result_path"] = canonical_result.as_posix()
                    if desired != existing:
                        _write(result_path, desired)
            except Exception:
                # Preserve the durable canonicalizing identity; canonical recovery
                # will classify genuinely invalid markers without destroying resume state.
                failures += 1
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

            created_refill, canonical_result = _ensure_research_refill_request(root, take, now)
            if created_refill is not None:
                created_refills.append(created_refill)

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
        or inventory < 0
        or isinstance(threshold, bool)
        or not isinstance(threshold, int)
        or threshold != claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD
        or str(value.get("work_mode_at_start") or "") != "discovery"
    ):
        raise ValueError("direct Discovery route metadata is invalid")
    return {**value, "preload_id": preload_id, "worker_id": worker_id, "run_key": run_key, "request_id": request_id}


def _frontier_request_id(claim: dict[str, Any], preload_id: str) -> str:
    material = "\n".join(
        (
            str(claim.get("worker_id") or ""),
            str(claim.get("run_key") or ""),
            str(claim.get("preload_id") or ""),
            preload_id,
        )
    )
    return "frontier-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _accounted_discovery_precheck_ids(root: Path, run_key: str) -> set[str]:
    state = _read(root / ".survey/work-queue/discovery-state.json", {}) or {}
    history = state.get("history") if isinstance(state.get("history"), list) else []
    return {
        str(row.get("precheck_request_id") or "")
        for row in history
        if isinstance(row, dict)
        and str(row.get("run_key") or "") == run_key
        and (row.get("round_accounted") is True or row.get("round_complete") is True)
        and str(row.get("precheck_request_id") or "")
    }


def _active_direct_discovery_claims(
    root: Path,
    *,
    worker_id: str,
    run_key: str,
) -> list[dict[str, Any]]:
    now = _utcnow()
    rows: list[dict[str, Any]] = []
    accounted = _accounted_discovery_precheck_ids(root, run_key)
    folder = root / DISCOVERY_CLAIMS
    if not folder.is_dir():
        return rows
    for path in sorted(folder.glob("*.json")):
        value = _read(path, {})
        if not isinstance(value, dict) or not (
            value.get("direct_take") is True
            or value.get("operation") == "direct_take_discovery"
        ):
            continue
        if value.get("worker_id") != worker_id or value.get("run_key") != run_key:
            continue
        if str(value.get("request_id") or "") in accounted:
            # Completed rounds no longer consume the bounded in-flight frontier.
            # This opens capacity immediately for the next prepared packet.
            continue
        claimed = claim_state.parse_time(value.get("claimed_at") or value.get("requested_at"))
        expires = claim_state.parse_time(value.get("lease_expires_at"))
        if claimed is not None and expires is None:
            expires = claimed + dt.timedelta(seconds=discovery_preload_queue.CLAIM_LEASE_SECONDS)
        if claimed is None or expires is None or expires <= now:
            continue
        rows.append(value)
    return rows


def _productive_frontier_packets(
    root: Path,
    *,
    primary_preload_id: str,
    primary_direction: str,
    limit: int,
) -> list[dict[str, Any]]:
    if limit <= 0:
        return []
    if primary_direction == "backward":
        directions = ("forward", "backward", "normal")
    elif primary_direction == "forward":
        directions = ("backward", "forward", "normal")
    else:
        directions = ("backward", "forward", "normal")
    rows: list[dict[str, Any]] = []
    seen = {primary_preload_id}
    for direction in directions:
        for packet in discovery_preload_queue.available_preloads(
            root,
            direction=direction,
            limit=MAX_DISCOVERY_PACKETS_PER_DIRECTION,
        ):
            preload_id = str(packet.get("preload_id") or "")
            if (
                not preload_id
                or preload_id in seen
                or int(packet.get("preload_unseen_result_count") or 0) <= 0
            ):
                continue
            rows.append(packet)
            seen.add(preload_id)
            if len(rows) >= limit:
                return rows
    return rows


def _ensure_discovery_frontier_claims(
    root: Path,
    claim: dict[str, Any],
) -> list[dict[str, Any]]:
    """Reserve work-bearing successor packets before the current precheck can become an idle gap."""
    worker_id = str(claim["worker_id"])
    run_key = str(claim["run_key"])
    active = _active_direct_discovery_claims(
        root,
        worker_id=worker_id,
        run_key=run_key,
    )
    active_request_ids = {
        str(row.get("request_id") or "")
        for row in active
        if str(row.get("request_id") or "")
    }
    async_state = derive_worker_run_state._discovery_async_state(root, run_key)
    active_request_ids.update(
        str(value)
        for value in async_state.get("discovery_inflight_precheck_ids") or []
        if str(value)
    )
    capacity = max(DISCOVERY_FRONTIER_TARGET - len(active_request_ids), 0)
    if capacity <= 0:
        return []

    entry = _read(root / DISCOVERY_ENTRIES / f"{claim['preload_id']}.json", {})
    primary_direction = str(
        entry.get("citation_direction")
        or discovery_preload_queue._direction(
            str(entry.get("provider") or ""),
            str(entry.get("source_url") or ""),
            entry.get("citation_direction"),
        )
        or "backward"
    )
    packets = _productive_frontier_packets(
        root,
        primary_preload_id=str(claim["preload_id"]),
        primary_direction=primary_direction,
        limit=capacity,
    )
    now = _utcnow()
    reserved: list[dict[str, Any]] = []
    for packet in packets:
        preload_id = str(packet["preload_id"])
        claim_path = root / DISCOVERY_CLAIMS / f"{preload_id}.json"
        if claim_path.exists():
            continue
        request_id = _frontier_request_id(claim, preload_id)
        payload = {
            "schema_version": 1,
            "operation": "direct_take_discovery",
            "direct_take": True,
            "preload_id": preload_id,
            "worker_id": worker_id,
            "run_key": run_key,
            "request_id": request_id,
            "claimed_at": _iso(now),
            "requested_at": _iso(now),
            "lease_expires_at": _iso(
                now + dt.timedelta(seconds=discovery_preload_queue.CLAIM_LEASE_SECONDS)
            ),
            "preload_result_path": packet.get("preload_result_path"),
            "discovery_bank": packet.get("discovery_bank"),
            "discovery_slot_path": packet.get("discovery_slot_path"),
            "scheduled_slot": claim.get("scheduled_slot"),
            "actual_invocation_start": claim.get("actual_invocation_start"),
            "candidate_inventory_at_start": claim.get("candidate_inventory_at_start"),
            "work_mode_at_start": "discovery",
            "research_discovery_threshold": claim.get("research_discovery_threshold"),
            "hot_dispatch_generated_at": claim.get("hot_dispatch_generated_at"),
            "auto_frontier": True,
            "frontier_parent_preload_id": claim.get("preload_id"),
        }
        _write(claim_path, payload)
        reserved.append(
            {
                **packet,
                "request_id": request_id,
                "claim_path": claim_path.relative_to(root).as_posix(),
                "auto_frontier": True,
            }
        )
    return reserved


def _reserved_discovery_frontier(
    root: Path,
    claim: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    folder = root / DISCOVERY_CLAIMS
    if not folder.is_dir():
        return rows
    for path in sorted(folder.glob("*.json")):
        value = _read(path, {})
        if not isinstance(value, dict):
            continue
        if (
            value.get("auto_frontier") is not True
            or value.get("frontier_parent_preload_id") != claim.get("preload_id")
            or value.get("worker_id") != claim.get("worker_id")
            or value.get("run_key") != claim.get("run_key")
        ):
            continue
        preload_id = str(value.get("preload_id") or "")
        entry = _read(root / DISCOVERY_ENTRIES / f"{preload_id}.json", {})
        if not isinstance(entry, dict) or entry.get("preload_id") != preload_id:
            continue
        rows.append(
            {
                "preload_id": preload_id,
                "request_id": value.get("request_id"),
                "discovery_bank": value.get("discovery_bank"),
                "discovery_slot_path": value.get("discovery_slot_path"),
                "preload_result_path": value.get("preload_result_path"),
                "formal_precheck_result_path": (
                    PRECHECK_RESULTS / f"{value.get('request_id')}.json"
                ).as_posix(),
                "citation_direction": entry.get("citation_direction"),
                "axis": entry.get("axis"),
                "work_start_allowed": True,
                "submission_allowed": False,
            }
        )
    return rows


def _pending_discovery_direct_result(
    claim: dict[str, Any],
    *,
    reserved_frontier: list[dict[str, Any]] | None = None,
    processed_at: str | None = None,
    early_ack: bool = False,
) -> dict[str, Any]:
    frontier = list(reserved_frontier or [])
    value = {
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
        "formal_precheck_result_path": (
            PRECHECK_RESULTS / f"{claim['request_id']}.json"
        ).as_posix(),
        "frontier_target": DISCOVERY_FRONTIER_TARGET,
        "reserved_frontier": frontier,
        "frontier_work_available": bool(frontier),
        "processed_at": processed_at or _iso(_utcnow()),
    }
    if early_ack:
        value["early_ack"] = True
    return value


def acknowledge_discovery_takes(repo_root: Path) -> dict[str, Any]:
    """Publish a lightweight direct-take result before formal precheck work."""
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
        if direct_result.exists():
            reused += 1
            continue
        try:
            claim = _normalize_direct_discovery_claim(path, raw)
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
                direct_result,
                _pending_discovery_direct_result(
                    claim,
                    reserved_frontier=[],
                    early_ack=True,
                ),
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
                    "early_ack": True,
                },
            )
    return {"created": created, "reused": reused, "failures": failures}


def materialize_discovery_prechecks(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    claim_root = root / DISCOVERY_CLAIMS
    result_root = root / DIRECT_DISCOVERY_RESULTS
    result_root.mkdir(parents=True, exist_ok=True)
    created = reused = failures = 0
    frontier_reserved = 0

    # Reserve a bounded same-run successor frontier before any formal precheck
    # result can become the worker's only visible activity. This is supply-side:
    # the worker does not need to decide to create the next packet after seeing
    # queued/in-progress Actions state.
    initial_paths = sorted(claim_root.glob("*.json")) if claim_root.is_dir() else []
    for path in initial_paths:
        raw = _read(path, {})
        if not isinstance(raw, dict) or not (
            raw.get("direct_take") is True
            or raw.get("operation") == "direct_take_discovery"
        ):
            continue
        if raw.get("auto_frontier") is True:
            continue
        try:
            claim = _normalize_direct_discovery_claim(path, raw)
            frontier_reserved += len(_ensure_discovery_frontier_claims(root, claim))
        except Exception:
            # The normal materialization pass below persists the canonical
            # recovery_required result for malformed/expired primary takes.
            pass

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
            entry = _read(root / DISCOVERY_ENTRIES / f"{claim['preload_id']}.json", {})
            if not isinstance(entry, dict) or entry.get("preload_id") != claim["preload_id"]:
                raise ValueError("Discovery preload entry is missing")
            bank = str(claim.get("discovery_bank") or "").lower()
            if bank not in BANK_IDS:
                raise ValueError("direct Discovery take requires a valid discovery_bank")
            slot_path = str(claim.get("discovery_slot_path") or "")
            if slot_path != discovery_slot_path(bank):
                raise ValueError("direct Discovery take slot path does not match its bank")

            reserved_frontier = _reserved_discovery_frontier(root, claim)
            existing_direct = _read(direct_result, {})
            if not isinstance(existing_direct, dict):
                existing_direct = {}
            if existing_direct.get("status") in {None, "precheck_pending"}:
                desired_direct = {
                    **existing_direct,
                    **_pending_discovery_direct_result(
                        claim,
                        reserved_frontier=reserved_frontier,
                        processed_at=str(existing_direct.get("processed_at") or "") or None,
                    ),
                }
                if existing_direct.get("early_ack") is True:
                    desired_direct["early_ack"] = True
                _write(direct_result, desired_direct)

            if precheck_result_path.exists():
                reused += 1
                continue
            if request_path.exists():
                reused += 1
                continue

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
    return {
        "created": created,
        "reused": reused,
        "failures": failures,
        "frontier_reserved": frontier_reserved,
        "frontier_target": DISCOVERY_FRONTIER_TARGET,
    }


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
    sub.add_parser("acknowledge-discovery")
    sub.add_parser("materialize-discovery")
    sub.add_parser("finalize-discovery")
    args = parser.parse_args()

    if args.command == "refresh":
        result = refresh(args.repo_root)
    elif args.command == "process-research":
        result = process_research_takes(args.repo_root)
    elif args.command == "finalize-research":
        result = finalize_research_takes(args.repo_root)
    elif args.command == "acknowledge-discovery":
        result = acknowledge_discovery_takes(args.repo_root)
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
