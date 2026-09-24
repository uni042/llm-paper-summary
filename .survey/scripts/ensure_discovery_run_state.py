#!/usr/bin/env python3
"""Repair a missing run-state request from durable Discovery precheck identity.

A foreground Discovery precheck already proves the worker/run identity and that the
invocation entered Discovery.  If the worker omitted its initial run-state request,
materialize a deterministic recovery request so continuation/finalization remains
machine-enforced.  The recovered route preserves Discovery mode; candidate inventory
is observed when the recovery snapshot is first derived and is explicitly marked as
non-exact start telemetry.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

import derive_worker_run_state
import worker_identity

PRECHECK_REQUESTS = Path(".survey/work-queue/discovery-precheck/requests")
RUN_STATE_REQUESTS = Path(".survey/work-queue/run-state/requests")
ARCHIVED_RUN_STATE_REQUESTS = Path(".survey/work-queue/archive/transport/run-state/requests")


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write_create_only(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing == text:
            return
        raise ValueError(f"refusing to overwrite existing recovery request: {path}")
    path.write_text(text, encoding="utf-8")


def _request_id(worker_id: str, run_key: str, scheduled_slot: str, actual_invocation_start: str) -> str:
    material = "\n".join((worker_id, run_key, scheduled_slot, actual_invocation_start))
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:24]
    return f"auto-recover-discovery-runstate-{digest}"


def _existing_run_request(root: Path, worker_id: str, run_key: str) -> str | None:
    for rel_root in (RUN_STATE_REQUESTS, ARCHIVED_RUN_STATE_REQUESTS):
        folder = root / rel_root
        if not folder.is_dir():
            continue
        for path in folder.glob("*.json"):
            value = _read(path, {})
            if not isinstance(value, dict):
                continue
            if (
                str(value.get("worker_id") or "") == worker_id
                and str(value.get("run_key") or "") == run_key
            ):
                return path.relative_to(root).as_posix()
    return None


def ensure_precheck_request(root: Path, precheck_path: Path) -> dict[str, Any]:
    root = root.resolve()
    path = precheck_path if precheck_path.is_absolute() else root / precheck_path
    value = _read(path, {})
    if not isinstance(value, dict):
        return {"status": "skipped", "reason": "invalid_precheck_json", "path": str(precheck_path)}

    run_key = str(value.get("run_key") or "").strip()
    if not run_key or run_key.startswith("preload:") or value.get("preload_seed") is True:
        return {"status": "skipped", "reason": "not_foreground_discovery_run", "path": str(precheck_path)}

    worker_id = str(value.get("worker_id") or "").strip()
    scheduled_slot = str(value.get("scheduled_slot") or "").strip()
    actual_invocation_start = str(value.get("actual_invocation_start") or "").strip()
    started_at = derive_worker_run_state._time(actual_invocation_start)
    if (
        not worker_identity.is_supported_worker_id(worker_id)
        or not worker_identity.identity_slot_valid(worker_id, scheduled_slot)
        or started_at is None
    ):
        return {
            "status": "skipped",
            "reason": "precheck_missing_recoverable_run_identity",
            "path": str(precheck_path),
        }

    now = dt.datetime.now(dt.timezone.utc)
    age_seconds = (now - started_at.astimezone(dt.timezone.utc)).total_seconds()
    if age_seconds > 7200 or age_seconds < -300:
        return {
            "status": "skipped",
            "reason": "run_outside_active_recovery_window",
            "path": str(precheck_path),
            "age_seconds": int(age_seconds),
        }

    existing = _existing_run_request(root, worker_id, run_key)
    if existing:
        return {
            "status": "reused",
            "worker_id": worker_id,
            "run_key": run_key,
            "request_path": existing,
        }

    request_id = _request_id(worker_id, run_key, scheduled_slot, actual_invocation_start)
    request_rel = RUN_STATE_REQUESTS / f"{request_id}.json"
    request = {
        "schema_version": 1,
        "request_id": request_id,
        "run_key": run_key,
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "scheduled_slot": scheduled_slot,
        "actual_invocation_start": actual_invocation_start,
        "runtime_condition": "none",
        "runtime_condition_confirmed": False,
        "runtime_condition_attempts": 0,
        "runtime_condition_detail": "",
        "route_recovery_source": "discovery_precheck_identity",
        "recovered_work_mode_at_start": "discovery",
        "source_discovery_precheck_request_id": str(value.get("request_id") or path.stem),
    }
    _write_create_only(root / request_rel, request)
    return {
        "status": "created",
        "worker_id": worker_id,
        "run_key": run_key,
        "request_id": request_id,
        "request_path": request_rel.as_posix(),
    }


def ensure_paths(root: Path, paths: Iterable[Path]) -> dict[str, Any]:
    rows = [ensure_precheck_request(root, path) for path in paths]
    return {
        "created": [row for row in rows if row.get("status") == "created"],
        "reused": [row for row in rows if row.get("status") == "reused"],
        "skipped": [row for row in rows if row.get("status") == "skipped"],
    }


def _paths_file(path: Path) -> list[Path]:
    if not path.is_file():
        return []
    return [
        Path(line.strip())
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def ensure_from_submission(root: Path, source_submission: str) -> dict[str, Any]:
    root = root.resolve()
    raw = Path(str(source_submission))
    submission_path = raw if raw.is_absolute() else root / raw
    if not submission_path.is_file() and raw.parts[:1] != (".survey",):
        submission_path = root / ".survey" / raw
    submission = _read(submission_path, {})
    if not isinstance(submission, dict):
        return {"created": [], "reused": [], "skipped": [{"status": "skipped", "reason": "submission_missing"}]}
    discovery_precheck = (
        submission.get("discovery_precheck")
        if isinstance(submission.get("discovery_precheck"), dict)
        else {}
    )
    request_id = str(discovery_precheck.get("request_id") or "").strip()
    if not request_id:
        return {"created": [], "reused": [], "skipped": [{"status": "skipped", "reason": "submission_missing_precheck_identity"}]}
    return ensure_paths(root, [PRECHECK_REQUESTS / f"{request_id}.json"])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--requests-file", type=Path)
    parser.add_argument("--submission")
    args = parser.parse_args()

    if args.submission:
        result = ensure_from_submission(args.repo_root, args.submission)
    elif args.requests_file is not None:
        result = ensure_paths(args.repo_root, _paths_file(args.requests_file))
    else:
        root = args.repo_root.resolve()
        folder = root / PRECHECK_REQUESTS
        paths = sorted(folder.glob("*.json")) if folder.is_dir() else []
        result = ensure_paths(root, [path.relative_to(root) for path in paths])

    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
