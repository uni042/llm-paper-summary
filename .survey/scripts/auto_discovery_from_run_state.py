#!/usr/bin/env python3
"""Auto-adopt the initial Discovery preload from a fresh run-state snapshot.

Only the first Discovery round of an invocation is eligible. The run-state lane
already serialized and froze the invocation route; this helper consumes the selected
PRECHECKED preload, performs the run-specific schema-v3 precheck in the same workflow
run, then refreshes the not-yet-published run-state result so the worker can begin
candidate evaluation immediately.

Later Discovery rounds continue through the normal worker decision point. If no
matching preload is available, this helper does nothing and the existing Discovery
path remains authoritative.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import build_discovery_identity_snapshot
import build_discovery_rejection_ledger
import derive_worker_run_state
import process_discovery_precheck
import worker_identity

PRECHECK_REQUESTS = Path(".survey/work-queue/discovery-precheck/requests")
PRECHECK_RESULTS = Path(".survey/work-queue/discovery-precheck/results")


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


def _has_run_discovery_transport(root: Path, run_key: str) -> bool:
    for folder in (root / PRECHECK_REQUESTS, root / PRECHECK_RESULTS):
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            value = _read(path, {})
            if isinstance(value, dict) and str(value.get("run_key") or "") == run_key:
                return True
    return False


def _eligible(result: dict[str, Any]) -> bool:
    gate = result.get("gate") if isinstance(result.get("gate"), dict) else {}
    preload = result.get("discovery_preload") if isinstance(result.get("discovery_preload"), dict) else {}
    selector = result.get("discovery_selector") if isinstance(result.get("discovery_selector"), dict) else {}
    direction = str(selector.get("next_direction") or "")
    return bool(
        result.get("ok") is True
        and result.get("snapshot_origin") == "request-fast-lane"
        and result.get("work_mode") == "discovery"
        and worker_identity.identity_slot_valid(result.get("worker_id"), result.get("scheduled_slot"))
        and result.get("scheduled_slot") != "0830"
        and gate.get("required_action") == "DISCOVER_AGAIN"
        and int(result.get("discovery_rounds_completed") or 0) == 0
        and result.get("discovery_precheck_result_pending") is False
        and result.get("discovery_submission_result_pending") is False
        and result.get("discovery_evaluation_pending") is False
        and result.get("discovery_recovery_required") is False
        and int(result.get("seconds_to_run_deadline") or 0) > 600
        and bool(preload.get("preload_id"))
        and direction in {"backward", "forward", "normal"}
        and str(preload.get("citation_direction") or "") == direction
        and bool(preload.get("provider"))
        and bool(preload.get("source_url"))
        and bool(preload.get("axis"))
        and bool(preload.get("discovery_bank"))
        and bool(preload.get("discovery_slot_path"))
    )


def _request_id(result: dict[str, Any]) -> str:
    preload = result.get("discovery_preload") or {}
    material = "\n".join(
        str(value or "")
        for value in (
            result.get("worker_id"),
            result.get("run_key"),
            result.get("scheduled_slot"),
            result.get("actual_invocation_start"),
            preload.get("preload_id"),
        )
    )
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return f"auto-initial-discovery-{digest}"


def _precheck_request(result: dict[str, Any], request_id: str) -> dict[str, Any]:
    preload = dict(result["discovery_preload"])
    direction = str(preload.get("citation_direction") or "discovery")
    collector_digest = hashlib.sha256(
        f"{result['run_key']}\n{preload['preload_id']}".encode("utf-8")
    ).hexdigest()[:16]
    return {
        "schema_version": 3,
        "operation": "precheck_discovery_candidates",
        "request_id": request_id,
        "provider": preload["provider"],
        "source_url": preload["source_url"],
        "collector_id": f"auto-initial-{direction}-{collector_digest}",
        "run_key": result["run_key"],
        "axis": preload["axis"],
        "target_unseen": int(preload.get("target_unseen") or 20),
        "page_size": int(preload.get("page_size") or 20),
        "max_pages": int(preload.get("max_pages") or 8),
        "initial_cursor": preload.get("initial_cursor"),
        "preload_id": preload["preload_id"],
        "preload_seed": False,
        "worker_id": result["worker_id"],
        "discovery_bank": preload["discovery_bank"],
        "discovery_slot_path": preload["discovery_slot_path"],
        "auto_initial_discovery": True,
        "source_run_state_request_id": result.get("request_id"),
    }


def _run_state_request(source: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "request_id": str(source["request_id"]),
        "run_key": str(source["run_key"]),
        "worker_id": str(source["worker_id"]),
        "worker_kind": "scheduled_chat",
        "scheduled_slot": str(source["scheduled_slot"]),
        "actual_invocation_start": str(source["actual_invocation_start"]),
        "runtime_condition": str(source.get("runtime_condition_requested") or "none"),
        "runtime_condition_confirmed": source.get("runtime_condition_confirmed") is True,
        "runtime_condition_attempts": int(source.get("runtime_condition_attempts") or 0),
        "runtime_condition_detail": str(source.get("runtime_condition_detail") or ""),
    }


def _process_precheck(
    root: Path,
    request_path: Path,
    result_path: Path,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="survey-initial-discovery-") as td:
        temp = Path(td)
        snapshot_dir = temp / "identities"
        rejection_ledger = temp / "rejections.json"
        build_discovery_identity_snapshot.build_snapshot(
            root / ".survey",
            snapshot_dir,
        )
        build_discovery_rejection_ledger.build_ledger(
            root / ".survey",
            rejection_ledger,
        )
        try:
            result = process_discovery_precheck.process_request(
                request_path,
                snapshot_dir=snapshot_dir,
                rejection_ledger_path=rejection_ledger,
                repo_root=root,
            )
        except Exception as exc:
            result = process_discovery_precheck.failure_result(request_path, exc)
    _write(result_path, result)
    return result


def _refresh_source_result(
    root: Path,
    source_path: Path,
    source: dict[str, Any],
    *,
    request_id: str,
    request_rel: Path,
    result_rel: Path,
    precheck_result: dict[str, Any],
) -> dict[str, Any]:
    refreshed = derive_worker_run_state.derive(root, _run_state_request(source))
    refreshed["request_id"] = source["request_id"]
    refreshed["snapshot_origin"] = "request-fast-lane"
    ready = bool(
        precheck_result.get("ok") is True
        and precheck_result.get("evaluation_allowed") is True
    )
    refreshed["auto_initial_discovery"] = {
        "requested": True,
        "request_id": request_id,
        "request_path": request_rel.as_posix(),
        "result_path": result_rel.as_posix(),
        "preload_id": precheck_result.get("preload_id"),
        "status": "ready_for_evaluation" if ready else "recovery_required",
        "preload_cache_used": precheck_result.get("preload_cache_used") is True,
        "preload_cached_pages_used": int(precheck_result.get("preload_cached_pages_used") or 0),
        "preload_live_pages_fetched": int(precheck_result.get("preload_live_pages_fetched") or 0),
    }
    _write(source_path, refreshed)
    derive_worker_run_state.run_state_cache.write_latest_pointer(
        root,
        source_path,
        refreshed,
    )
    return refreshed


def process(repo_root: Path, run_state_results_file: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    source_paths = _paths_file(run_state_results_file)
    created: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []

    for raw in source_paths:
        source_path = raw if raw.is_absolute() else root / raw
        source = _read(source_path, {})
        if not isinstance(source, dict) or not _eligible(source):
            skipped.append({"path": str(raw), "reason": "not_initial_discovery_preload_eligible"})
            continue

        run_key = str(source["run_key"])
        if _has_run_discovery_transport(root, run_key):
            skipped.append({"path": str(raw), "reason": "run_already_has_discovery_transport"})
            continue

        request_id = _request_id(source)
        request_rel = PRECHECK_REQUESTS / f"{request_id}.json"
        result_rel = PRECHECK_RESULTS / f"{request_id}.json"
        request_path = root / request_rel
        result_path = root / result_rel

        if request_path.exists() or result_path.exists():
            skipped.append({"path": str(raw), "reason": "deterministic_request_already_exists"})
            continue

        _write(request_path, _precheck_request(source, request_id))
        precheck_result = _process_precheck(root, request_path, result_path)
        refreshed = _refresh_source_result(
            root,
            source_path,
            source,
            request_id=request_id,
            request_rel=request_rel,
            result_rel=result_rel,
            precheck_result=precheck_result,
        )
        auto = refreshed.get("auto_initial_discovery") or {}
        created.append(
            {
                "source_result": source_path.relative_to(root).as_posix(),
                "request_id": request_id,
                "request_path": request_rel.as_posix(),
                "result_path": result_rel.as_posix(),
                "status": auto.get("status"),
                "preload_id": auto.get("preload_id"),
                "next_action": refreshed.get("next_action"),
            }
        )

    return {
        "ok": True,
        "source_results": len(source_paths),
        "created": created,
        "skipped": skipped,
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
