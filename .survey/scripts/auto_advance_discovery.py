#!/usr/bin/env python3
"""Advance a completed Discovery run directly onto the next prepared bank.

A successful Discovery ingestion already updates discovery-state.json.  This helper
uses that canonical state immediately, publishes a fresh run-state snapshot, and,
when the continuation gate says DISCOVER_AGAIN, reserves the oldest PRECHECKED
preload for the selector's next direction.  The reservation is materialized into a
run-specific schema-v3 precheck request, and that formal precheck is executed inline
before the recovery transaction is published.

The worker may begin lightweight evaluation from the reserved preload immediately;
when the inline precheck succeeds the same transaction also unlocks submission, so
later Discovery rounds do not wait for the periodic precheck collector.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import build_discovery_identity_snapshot
import build_discovery_rejection_ledger
import claim_window_policy
import derive_worker_run_state
import discovery_preload_queue
import ensure_discovery_run_state
import hot_dispatch
import process_discovery_precheck
import worker_identity

RUN_STATE_REQUESTS = Path(".survey/work-queue/run-state/requests")
RUN_STATE_RESULTS = Path(".survey/work-queue/run-state/results")


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


def _utcnow() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def _submission_path(root: Path, value: Any) -> Path | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    path = Path(raw)
    if path.is_absolute():
        return None
    if path.parts[:1] == (".survey",):
        candidate = root / path
    else:
        candidate = root / ".survey" / path
    try:
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return None
    return candidate


def _recovered_runs(root: Path, report: dict[str, Any]) -> list[dict[str, str]]:
    rows: dict[tuple[str, str], dict[str, str]] = {}
    for item in report.get("recovered") or []:
        if not isinstance(item, dict):
            continue
        path = _submission_path(root, item.get("submission"))
        if path is None:
            continue
        submission = _read(path, {})
        if not isinstance(submission, dict):
            continue
        stats = submission.get("discovery_stats") if isinstance(submission.get("discovery_stats"), dict) else {}
        worker_id = str(submission.get("worker_id") or "").strip()
        run_key = str(submission.get("run_key") or stats.get("run_key") or "").strip()
        if not worker_identity.is_supported_worker_id(worker_id) or not run_key:
            continue
        rows[(worker_id, run_key)] = {
            "worker_id": worker_id,
            "run_key": run_key,
            "source_submission": path.relative_to(root).as_posix(),
        }
    return [rows[key] for key in sorted(rows)]


def _fallback_run_request(root: Path, worker_id: str, run_key: str) -> dict[str, Any] | None:
    request_root = root / RUN_STATE_REQUESTS
    candidates: list[tuple[dt.datetime, dict[str, Any]]] = []
    if request_root.is_dir():
        for path in request_root.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict):
                continue
            if str(value.get("worker_id") or "") != worker_id or str(value.get("run_key") or "") != run_key:
                continue
            slot = str(value.get("scheduled_slot") or "")
            started = derive_worker_run_state._time(value.get("actual_invocation_start"))
            if not worker_identity.identity_slot_valid(worker_id, slot) or started is None:
                continue
            candidates.append((started, value))
    if not candidates:
        return None
    candidates.sort(key=lambda item: item[0], reverse=True)
    return dict(candidates[0][1])


def _run_request(root: Path, worker_id: str, run_key: str) -> dict[str, Any] | None:
    cached = derive_worker_run_state.run_state_cache.cached_request(root, worker_id, run_key)
    if isinstance(cached, dict):
        return cached
    return _fallback_run_request(root, worker_id, run_key)


def _snapshot_id(worker_id: str, run_key: str, source_submission: str, preload_id: str | None) -> str:
    material = "\n".join((worker_id, run_key, source_submission, str(preload_id or "no-preload")))
    return "auto-discovery-advance-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _next_request_id(worker_id: str, run_key: str, preload_id: str) -> str:
    material = "\n".join((worker_id, run_key, preload_id))
    return "auto-next-discovery-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _fallback_request_id(worker_id: str, run_key: str, direction: str, source_url: str) -> str:
    material = "\n".join((worker_id, run_key, direction, source_url))
    return "auto-next-discovery-fallback-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]


def _make_fallback_precheck_request(
    state: dict[str, Any],
    request: dict[str, Any],
    source: dict[str, Any],
    *,
    request_id: str,
    source_submission: str,
) -> dict[str, Any]:
    direction = str(source.get("citation_direction") or "discovery")
    return {
        "schema_version": 3,
        "operation": "precheck_discovery_candidates",
        "request_id": request_id,
        "provider": source["provider"],
        "source_url": source["source_url"],
        "collector_id": f"auto-next-fallback-{direction}-{request_id[-12:]}",
        "run_key": state["run_key"],
        "worker_id": state["worker_id"],
        "scheduled_slot": request["scheduled_slot"],
        "actual_invocation_start": request["actual_invocation_start"],
        "axis": source["axis"],
        "target_unseen": int(source.get("target_unseen") or 20),
        "page_size": int(source.get("page_size") or 20),
        "max_pages": int(source.get("max_pages") or 25),
        "initial_cursor": source.get("initial_cursor"),
        "auto_next_discovery": True,
        "fixed_source_fallback": True,
        "source_submission": source_submission,
    }


def _make_claim(
    state: dict[str, Any],
    request: dict[str, Any],
    preload: dict[str, Any],
    *,
    request_id: str,
    source_submission: str,
) -> dict[str, Any]:
    now = _utcnow()
    return {
        "schema_version": 1,
        "operation": "direct_take_discovery",
        "direct_take": True,
        "auto_next_discovery": True,
        "preload_id": preload["preload_id"],
        "worker_id": state["worker_id"],
        "run_key": state["run_key"],
        "request_id": request_id,
        "requested_at": _iso(now),
        "claimed_at": _iso(now),
        "lease_expires_at": _iso(
            now + dt.timedelta(seconds=discovery_preload_queue.CLAIM_LEASE_SECONDS)
        ),
        "preload_result_path": preload["preload_result_path"],
        "discovery_bank": preload["discovery_bank"],
        "discovery_slot_path": preload["discovery_slot_path"],
        "scheduled_slot": request["scheduled_slot"],
        "actual_invocation_start": request["actual_invocation_start"],
        "candidate_inventory_at_start": int(state["candidate_inventory"]),
        "work_mode_at_start": "discovery",
        "research_discovery_threshold": claim_window_policy.RESEARCH_DISCOVERY_THRESHOLD,
        "hot_dispatch_generated_at": _iso(now),
        "source_submission": source_submission,
    }


def _publish_snapshot(
    root: Path,
    request: dict[str, Any],
    state: dict[str, Any],
    *,
    source_submission: str,
    auto_next: dict[str, Any] | None,
) -> str:
    preload_id = str((auto_next or {}).get("preload_id") or "") or None
    snapshot_id = _snapshot_id(
        str(state["worker_id"]),
        str(state["run_key"]),
        source_submission,
        preload_id,
    )
    result = dict(state)
    result["request_id"] = snapshot_id
    result["snapshot_origin"] = "discovery-recovery-fast-lane"
    result["auto_generated"] = True
    result["snapshot_generation"] = derive_worker_run_state.run_state_cache.generation_for(
        root,
        str(state["worker_id"]),
        str(state["run_key"]),
    )
    if auto_next is not None:
        result["auto_next_discovery"] = auto_next
    result_path = root / RUN_STATE_RESULTS / f"{snapshot_id}.json"
    _write(result_path, result)
    derive_worker_run_state.run_state_cache.write_latest_pointer(root, result_path, result)
    return result_path.relative_to(root).as_posix()


def _direct_result(root: Path, preload_id: str) -> dict[str, Any]:
    value = _read(root / hot_dispatch.DIRECT_DISCOVERY_RESULTS / f"{preload_id}.json", {})
    return value if isinstance(value, dict) else {}


def _process_formal_precheck(root: Path, request_id: str) -> dict[str, Any]:
    request_path = root / hot_dispatch.PRECHECK_REQUESTS / f"{request_id}.json"
    result_path = root / hot_dispatch.PRECHECK_RESULTS / f"{request_id}.json"
    existing = _read(result_path, {})
    if isinstance(existing, dict) and str(existing.get("request_id") or "") == request_id:
        return existing

    with tempfile.TemporaryDirectory(prefix="survey-next-discovery-") as td:
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


def advance(repo_root: Path, recovery_report: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    report = _read(Path(recovery_report), {})
    if not isinstance(report, dict):
        raise ValueError("recovery report must be a JSON object")

    advanced: list[dict[str, Any]] = []
    snapshots: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []

    # A completed round must immediately free one slot in the bounded Discovery
    # frontier. Refill/materialize before deriving the next action so a worker
    # never reaches an idle decision point merely because the previous round just
    # became durable. Newly materialized precheck requests are published by the
    # recovery workflow in the same transaction and processed by the precheck lane.
    frontier_maintenance = hot_dispatch.materialize_discovery_prechecks(root)

    for run in _recovered_runs(root, report):
        worker_id = run["worker_id"]
        run_key = run["run_key"]
        request = _run_request(root, worker_id, run_key)
        if request is None:
            # A foreground Discovery precheck carries the same immutable run
            # identity. Repair an omitted initial run-state request before giving
            # up, so submission completion can still derive DISCOVER_AGAIN and
            # advance the same invocation automatically.
            ensure_discovery_run_state.ensure_from_submission(
                root,
                run["source_submission"],
            )
            request = _run_request(root, worker_id, run_key)
        if request is None:
            skipped.append({**run, "reason": "run_state_identity_unavailable_after_recovery"})
            continue

        state = derive_worker_run_state.derive(root, request)
        gate = state.get("gate") if isinstance(state.get("gate"), dict) else {}
        required_action = str(gate.get("required_action") or state.get("next_action") or "")
        auto_next: dict[str, Any] | None = None

        if (
            state.get("work_mode") == "discovery"
            and required_action == "DISCOVER_AGAIN"
            and int(state.get("seconds_to_run_deadline") or 0) > 600
            and request.get("scheduled_slot") != "0830"
        ):
            selector = state.get("discovery_selector") if isinstance(state.get("discovery_selector"), dict) else {}
            direction = str(selector.get("next_direction") or "")
            preload = (
                discovery_preload_queue.pick_available(root, direction=direction)
                if direction in {"backward", "forward", "normal"}
                else None
            )
            if isinstance(preload, dict) and preload.get("preload_id"):
                preload_id = str(preload["preload_id"])
                request_id = _next_request_id(worker_id, run_key, preload_id)
                claim_path = root / hot_dispatch.DISCOVERY_CLAIMS / f"{preload_id}.json"
                _write(
                    claim_path,
                    _make_claim(
                        state,
                        request,
                        preload,
                        request_id=request_id,
                        source_submission=run["source_submission"],
                    ),
                )
                materialized = hot_dispatch.materialize_discovery_prechecks(root)
                direct = _direct_result(root, preload_id)
                if direct.get("ok") is True and direct.get("work_start_allowed") is True:
                    precheck = _process_formal_precheck(root, request_id)
                    finalized = hot_dispatch.finalize_discovery_takes(root)
                    direct = _direct_result(root, preload_id)
                    precheck_ready = bool(
                        precheck.get("ok") is True
                        and precheck.get("evaluation_allowed") is True
                    )
                    auto_next = {
                        "status": str(direct.get("status") or "precheck_pending"),
                        "work_start_allowed": True,
                        "submission_allowed": direct.get("submission_allowed") is True,
                        "preload_id": preload_id,
                        "direction": direction,
                        "discovery_bank": preload.get("discovery_bank"),
                        "discovery_slot_path": preload.get("discovery_slot_path"),
                        "preload_result_path": direct.get("preload_result_path"),
                        "request_id": request_id,
                        "formal_precheck_result_path": direct.get("formal_precheck_result_path"),
                        "formal_precheck_ready": precheck_ready,
                        "inline_precheck": True,
                        "receipt": precheck.get("receipt"),
                        "source_submission": run["source_submission"],
                    }
                    advanced.append(
                        {
                            "worker_id": worker_id,
                            "run_key": run_key,
                            "direction": direction,
                            "preload_id": preload_id,
                            "request_id": request_id,
                            "materialized": materialized,
                            "finalized": finalized,
                            "formal_precheck_ok": precheck.get("ok") is True,
                            "formal_precheck_ready": precheck_ready,
                        }
                    )
                else:
                    skipped.append(
                        {
                            **run,
                            "reason": "direct_take_materialization_failed",
                            "preload_id": preload_id,
                        }
                    )
            else:
                source = discovery_preload_queue.fallback_source(root, direction=direction)
                if isinstance(source, dict) and source.get("provider") and source.get("source_url"):
                    request_id = _fallback_request_id(
                        worker_id, run_key, direction, str(source["source_url"])
                    )
                    request_path = root / hot_dispatch.PRECHECK_REQUESTS / f"{request_id}.json"
                    _write(
                        request_path,
                        _make_fallback_precheck_request(
                            state, request, source,
                            request_id=request_id,
                            source_submission=run["source_submission"],
                        ),
                    )
                    precheck = _process_formal_precheck(root, request_id)
                    precheck_ready = bool(
                        precheck.get("ok") is True
                        and precheck.get("evaluation_allowed") is True
                    )
                    auto_next = {
                        "status": "ready_for_evaluation" if precheck_ready else "recovery_required",
                        "work_start_allowed": precheck_ready,
                        "submission_allowed": precheck_ready,
                        "source_kind": "fixed_source_fallback",
                        "preload_id": None,
                        "direction": direction,
                        "request_id": request_id,
                        "formal_precheck_result_path": (
                            hot_dispatch.PRECHECK_RESULTS / f"{request_id}.json"
                        ).as_posix(),
                        "formal_precheck_ready": precheck_ready,
                        "inline_precheck": True,
                        "receipt": precheck.get("receipt"),
                        "source_submission": run["source_submission"],
                    }
                    advanced.append({
                        "worker_id": worker_id,
                        "run_key": run_key,
                        "direction": direction,
                        "preload_id": None,
                        "source_kind": "fixed_source_fallback",
                        "request_id": request_id,
                        "formal_precheck_ok": precheck.get("ok") is True,
                        "formal_precheck_ready": precheck_ready,
                    })
                else:
                    skipped.append({**run, "reason": "no_matching_prechecked_bank_or_fallback_source"})
        else:
            skipped.append(
                {
                    **run,
                    "reason": f"gate:{required_action or 'unknown'}",
                }
            )

        refreshed = derive_worker_run_state.derive(root, request)
        snapshot_path = _publish_snapshot(
            root,
            request,
            refreshed,
            source_submission=run["source_submission"],
            auto_next=auto_next,
        )
        snapshots.append(
            {
                "worker_id": worker_id,
                "run_key": run_key,
                "result_path": snapshot_path,
                "required_action": (refreshed.get("gate") or {}).get("required_action"),
                "auto_next_preload_id": (auto_next or {}).get("preload_id"),
            }
        )

    return {
        "ok": True,
        "recovered_runs": len(_recovered_runs(root, report)),
        "frontier_maintenance": frontier_maintenance,
        "advanced": advanced,
        "snapshots": snapshots,
        "skipped": skipped,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--recovery-report", type=Path, required=True)
    args = parser.parse_args()
    result = advance(args.repo_root, args.recovery_report)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
