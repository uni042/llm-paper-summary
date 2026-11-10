#!/usr/bin/env python3
"""Auto-allocate the initial Research/Audit claim window from a fresh run-state snapshot.

The initial allocation of a fixed Scheduled Chat invocation or an ad-hoc worker-N
invocation is eligible. The claim allocator expands this request into one foreground
plus prefetched standby claims.
Later window refills keep using the normal worker decision point so Audit starvation
and per-paper continuation semantics remain unchanged.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any

import claim_fast_path
import claim_state
import claim_window_policy
import initial_claim_fast_path
import worker_identity

CLAIM_REQUESTS = Path(".survey/work-queue/claim-requests")
CLAIM_RESULTS = Path(".survey/work-queue/claim-results")
ARCHIVE = Path(".survey/work-queue/archive/transport")
HOT_DISPATCH = Path(".survey/work-queue/hot-dispatch.json")


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


def _paths_file(path: Path) -> list[Path]:
    if not path.is_file():
        return []
    return [
        Path(line.strip())
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _same_run(value: Any, result: dict[str, Any]) -> bool:
    if not isinstance(value, dict):
        return False
    left = claim_state.parse_time(value.get("actual_invocation_start"))
    right = claim_state.parse_time(result.get("actual_invocation_start"))
    return bool(
        value.get("worker_id") == result.get("worker_id")
        and value.get("run_key") == result.get("run_key")
        and value.get("scheduled_slot") == result.get("scheduled_slot")
        and left is not None
        and right is not None
        and left == right
    )


def _has_run_claim_transport(root: Path, result: dict[str, Any]) -> bool:
    folders = (
        root / CLAIM_REQUESTS,
        root / CLAIM_RESULTS,
        root / ARCHIVE / "claim-requests",
        root / ARCHIVE / "claim-results",
    )
    for folder in folders:
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            if _same_run(_read(path, {}), result):
                return True
    return False


def _eligible(result: dict[str, Any]) -> bool:
    gate = result.get("gate") if isinstance(result.get("gate"), dict) else {}
    return bool(
        result.get("ok") is True
        and result.get("snapshot_origin") == "request-fast-lane"
        and result.get("route_source") != "hot_dispatch_direct_start"
        and result.get("work_mode") == "research"
        and worker_identity.identity_slot_valid(result.get("worker_id"), result.get("scheduled_slot"))
        and result.get("scheduled_slot") != "0830"
        and gate.get("required_action") == "CLAIM_NEXT_RESEARCH_AUDIT"
        and result.get("active_assignment") is False
        and result.get("claim_result_pending") is False
        and int(result.get("research_audit_completed_this_invocation") or 0) == 0
        and not (result.get("submitted_attempt_ids") or [])
    )


def _carryover_resume_eligible(result: dict[str, Any]) -> bool:
    gate = result.get("gate") if isinstance(result.get("gate"), dict) else {}
    return bool(
        result.get("ok") is True
        and result.get("snapshot_origin") == "request-fast-lane"
        and result.get("work_mode") == "research"
        and worker_identity.identity_slot_valid(result.get("worker_id"), result.get("scheduled_slot"))
        and result.get("scheduled_slot") != "0830"
        and result.get("active_assignment") is True
        and gate.get("required_action") in {
            "CONTINUE_ASSIGNED_WORK",
            "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY",
        }
    )


def _recovery_packet(root: Path, result: dict[str, Any]) -> dict[str, Any] | None:
    """Return the oldest same-worker expired-record recovery packet for this run.

    Recovery is intentionally materialized by the run-state workflow instead of a
    Scheduled Chat direct-take write. This keeps the worker-side transport to the
    already-required run-state request while preserving the canonical claim/bank
    recovery path.
    """
    gate = result.get("gate") if isinstance(result.get("gate"), dict) else {}
    if not (
        result.get("ok") is True
        and result.get("snapshot_origin") == "request-fast-lane"
        and result.get("work_mode") == "research"
        and worker_identity.identity_slot_valid(result.get("worker_id"), result.get("scheduled_slot"))
        and result.get("scheduled_slot") != "0830"
        and result.get("active_assignment") is False
        and result.get("claim_result_pending") is False
        and gate.get("required_action") == "CLAIM_NEXT_RESEARCH_AUDIT"
    ):
        return None

    hot = _read(root / HOT_DISPATCH, {})
    recovery_map = hot.get("research_recovery_resume") if isinstance(hot, dict) else {}
    if not isinstance(recovery_map, dict):
        return None
    rows = recovery_map.get(str(result.get("worker_id") or ""), [])
    if not isinstance(rows, list):
        return None
    for packet in rows:
        if not isinstance(packet, dict):
            continue
        if (
            packet.get("resume_recovery") is True
            and packet.get("job_id")
            and packet.get("claim_id")
            and packet.get("attempt_id")
            and packet.get("work_start_allowed") is True
        ):
            return packet
    return None


def _recovery_request_id(result: dict[str, Any], packet: dict[str, Any]) -> str:
    material = "\n".join(
        str(value or "")
        for value in (
            result.get("worker_id"),
            result.get("run_key"),
            result.get("scheduled_slot"),
            result.get("actual_invocation_start"),
            packet.get("job_id"),
            packet.get("recovery_source_attempt_id"),
        )
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return f"auto-recovery-claim-{digest}"


def _request_id(result: dict[str, Any]) -> str:
    material = "\n".join(
        str(result.get(key) or "")
        for key in ("worker_id", "run_key", "scheduled_slot", "actual_invocation_start")
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return f"auto-initial-claim-{digest}"


def _claim_request(result: dict[str, Any], request_id: str) -> dict[str, Any]:
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    raw_window = result.get("claim_window")
    claim_window = claim_window_policy.normalize_window(
        claim_window_policy.DEFAULT_CLAIM_WINDOW if raw_window is None else raw_window
    )
    return {
        "schema_version": 1,
        "request_id": request_id,
        "worker_id": result["worker_id"],
        "worker_kind": "scheduled_chat",
        "requested_at": now,
        "max_jobs": 1,
        "claim_window": claim_window,
        "job_types": ["research", "audit"],
        "run_key": result["run_key"],
        "scheduled_slot": result["scheduled_slot"],
        "actual_invocation_start": result["actual_invocation_start"],
        "auto_initial_claim": True,
        "source_run_state_request_id": result.get("request_id"),
    }


def process(repo_root: Path, run_state_results_file: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    source_paths = _paths_file(run_state_results_file)
    created: list[dict[str, str]] = []
    skipped: list[dict[str, str]] = []
    resume_sources: list[Path] = []

    for raw in source_paths:
        path = raw if raw.is_absolute() else root / raw
        result = _read(path, {})
        if isinstance(result, dict) and _carryover_resume_eligible(result):
            resume_sources.append(path)

        recovery = _recovery_packet(root, result) if isinstance(result, dict) else None
        if recovery is not None:
            request_id = _recovery_request_id(result, recovery)
            request_rel = CLAIM_REQUESTS / f"{request_id}.json"
            result_rel = CLAIM_RESULTS / f"{request_id}.json"
            request_path = root / request_rel
            if request_path.exists() or (root / result_rel).exists():
                skipped.append({"path": str(raw), "reason": "deterministic_recovery_request_already_exists"})
                continue
            payload = _claim_request(result, request_id)
            payload["job_ids"] = [str(recovery["job_id"])]
            payload["auto_recovery_claim"] = True
            payload["recovery_source_claim_id"] = recovery.get("recovery_source_claim_id")
            payload["recovery_source_attempt_id"] = recovery.get("recovery_source_attempt_id")
            payload["recovery_source_record_bank"] = recovery.get("recovery_source_record_bank")
            _write(request_path, payload)
            result["auto_recovery_claim"] = {
                "requested": True,
                "request_id": request_id,
                "request_path": request_rel.as_posix(),
                "result_path": result_rel.as_posix(),
                "job_id": recovery["job_id"],
                "source_claim_id": recovery.get("recovery_source_claim_id"),
                "source_attempt_id": recovery.get("recovery_source_attempt_id"),
                "source_record_bank": recovery.get("recovery_source_record_bank"),
                "status": "allocating",
                "requires_worker_direct_take": False,
            }
            _write(path, result)
            created.append({
                "source_result": path.relative_to(root).as_posix(),
                "request_id": request_id,
                "request_path": request_rel.as_posix(),
                "result_path": result_rel.as_posix(),
                "metadata_key": "auto_recovery_claim",
                "claim_reason": "expired_record_recovery",
                "job_id": str(recovery["job_id"]),
            })
            continue

        if not isinstance(result, dict) or not _eligible(result):
            skipped.append({"path": str(raw), "reason": "not_initial_research_claim_eligible"})
            continue
        if _has_run_claim_transport(root, result):
            skipped.append({"path": str(raw), "reason": "run_already_has_claim_transport"})
            continue

        request_id = _request_id(result)
        request_rel = CLAIM_REQUESTS / f"{request_id}.json"
        result_rel = CLAIM_RESULTS / f"{request_id}.json"
        request_path = root / request_rel
        if request_path.exists():
            skipped.append({"path": str(raw), "reason": "deterministic_request_already_exists"})
            continue

        _write(request_path, _claim_request(result, request_id))
        result["auto_initial_claim"] = {
            "requested": True,
            "request_id": request_id,
            "request_path": request_rel.as_posix(),
            "result_path": result_rel.as_posix(),
            "status": "allocating",
        }
        _write(path, result)
        created.append({
            "source_result": path.relative_to(root).as_posix(),
            "request_id": request_id,
            "request_path": request_rel.as_posix(),
            "result_path": result_rel.as_posix(),
            "metadata_key": "auto_initial_claim",
            "claim_reason": "initial_research_claim",
        })

    fast_path: dict[str, Any] = {"skipped": True, "mode": "none"}
    if created:
        if len(created) == 1:
            try:
                fast_path = initial_claim_fast_path.process(
                    root,
                    root / created[0]["request_path"],
                )
                fast_path["skipped"] = False
                fast_path["mode"] = "initial-preload-adopt"
            except initial_claim_fast_path.InitialClaimFastPathUnavailable as exc:
                fast_path = claim_fast_path.process(root)
                fast_path["skipped"] = False
                fast_path["mode"] = "canonical-fallback"
                fast_path["fallback_reason"] = str(exc)
        else:
            fast_path = claim_fast_path.process(root)
            fast_path["skipped"] = False
            fast_path["mode"] = "canonical-fallback"
            fast_path["fallback_reason"] = "multiple initial claim requests require canonical batch allocation"

        for item in created:
            source_path = root / item["source_result"]
            source = _read(source_path, {})
            claim_result = _read(root / item["result_path"], {})
            assignments = claim_result.get("assignments") if isinstance(claim_result, dict) else []
            if not isinstance(assignments, list):
                assignments = []
            metadata_key = str(item.get("metadata_key") or "auto_initial_claim")
            auto = source.get(metadata_key) if isinstance(source.get(metadata_key), dict) else {}
            auto.update({
                "status": "allocated" if assignments else ("settled_no_assignment" if isinstance(claim_result, dict) else "pending"),
                "assignment_count": len(assignments),
                "attempt_ids": sorted(
                    str(row.get("attempt_id"))
                    for row in assignments
                    if isinstance(row, dict) and row.get("attempt_id")
                ),
                "job_ids": sorted(
                    str(row.get("job_id"))
                    for row in assignments
                    if isinstance(row, dict) and row.get("job_id")
                ),
            })
            if item.get("claim_reason") == "expired_record_recovery":
                target_job_id = str(item.get("job_id") or "")
                target = next(
                    (
                        row for row in assignments
                        if isinstance(row, dict) and str(row.get("job_id") or "") == target_job_id
                    ),
                    None,
                )
                auto["requires_worker_direct_take"] = False
                auto["record_write_allowed"] = bool(
                    isinstance(target, dict) and target.get("record_bank")
                )
                if isinstance(target, dict):
                    auto["claim_id"] = target.get("claim_id")
                    auto["attempt_id"] = target.get("attempt_id")
                    auto["record_bank"] = target.get("record_bank")
                    auto["record_bank_recovery"] = target.get("record_bank_recovery")
            source[metadata_key] = auto
            _write(source_path, source)

    resume_recovery: dict[str, Any] = {"skipped": True, "source_results": len(resume_sources)}
    if resume_sources:
        resume_recovery = claim_fast_path.process(root)
        resume_recovery["skipped"] = False
        resume_recovery["source_results"] = len(resume_sources)
        hot_index = _read(root / ".survey/work-queue/hot-dispatch.json", {})
        resume_map = hot_index.get("research_resume") if isinstance(hot_index, dict) else {}
        if not isinstance(resume_map, dict):
            resume_map = {}
        for path in resume_sources:
            source = _read(path, {})
            if not isinstance(source, dict):
                continue
            packets = resume_map.get(str(source.get("worker_id") or ""), [])
            if not isinstance(packets, list):
                packets = []
            source["auto_resume_recovery"] = {
                "status": "ready" if packets else "reconciled_no_active_resume",
                "assignment_count": len(packets),
                "foreground": packets[0] if packets else None,
                "assignments": packets,
                "rule": "resume foreground immediately; do not create a new claim",
            }
            _write(path, source)

    return {
        "ok": True,
        "source_results": len(source_paths),
        "created": created,
        "created_recovery": [
            item for item in created
            if item.get("claim_reason") == "expired_record_recovery"
        ],
        "skipped": skipped,
        "claim_fast_path": fast_path,
        "resume_recovery": resume_recovery,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--run-state-results-file", type=Path, required=True)
    args = parser.parse_args()
    result = process(args.repo_root, args.run_state_results_file)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
