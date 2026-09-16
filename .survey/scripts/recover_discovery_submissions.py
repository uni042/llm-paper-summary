#!/usr/bin/env python3
"""Ingest and recover self-describing root-level Discovery round submissions.

A specialist Discovery round is an immutable candidate payload with durable round
identity. It does not need a pre-issued worker-facing Discovery job: queue_worker creates
a deterministic internal ingest job for that submission. This script also repairs older
rounds that already received ``unknown job_id`` or ``job already terminal`` results.
Research/Audit submissions are never rebound here.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import queue_worker


def _configure(root: Path) -> None:
    queue_worker.ROOT = root.resolve()
    queue_worker.QUEUE = queue_worker.ROOT / "work-queue"
    queue_worker.JOBS = queue_worker.QUEUE / "jobs"
    queue_worker.SUBMISSIONS = queue_worker.QUEUE / "submissions"
    queue_worker.RESULTS = queue_worker.QUEUE / "results"
    queue_worker.STATE = queue_worker.QUEUE / "state.json"
    queue_worker.ARCHIVE = queue_worker.QUEUE / "archive"
    queue_worker.DISCOVERY_STATE = queue_worker.QUEUE / "discovery-state.json"


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _result_allows_recovery(existing_result: dict) -> bool:
    """Allow new rounds plus the two known stale Discovery failure modes."""
    if not existing_result:
        return True
    if existing_result.get("ok") is True:
        return False
    error = str(existing_result.get("error") or "")
    return "job already terminal" in error or "unknown job_id" in error or "job_id required" in error


def _eligible_template_job(sub: dict, existing_result: dict) -> tuple[bool, dict]:
    submitted_job_id = sub.get("job_id")
    explicit_round = sub.get("operation") == "submit_discovery_round"
    if not isinstance(submitted_job_id, str) or not submitted_job_id:
        return explicit_round, {}

    old_job_path = queue_worker.JOBS / f"{submitted_job_id}.json"
    if not old_job_path.exists():
        # Self-describing legacy specialist rounds used synthetic job ids. The immutable
        # candidate payload, not the synthetic id, is the authority for safe replay.
        return True, {}

    old_job = _read(old_job_path, {}) or {}
    if old_job.get("type") != "discovery":
        return False, {}
    if old_job.get("status") in queue_worker.TERMINAL:
        return True, old_job

    # A live real Discovery job still belongs to the normal queue worker. Do not race it.
    return False, old_job


def recover(root: Path) -> dict[str, Any]:
    _configure(root)
    queue_worker.SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    queue_worker.RESULTS.mkdir(parents=True, exist_ok=True)
    st = queue_worker.load_state()
    recovered: list[dict[str, Any]] = []

    for submission_path in sorted(queue_worker.SUBMISSIONS.glob("*.json")):
        result_path = queue_worker.RESULTS / submission_path.name
        existing_result = _read(result_path, {}) or {}
        if not _result_allows_recovery(existing_result):
            continue

        sub = _read(submission_path, {}) or {}
        if not queue_worker.is_discovery_round_submission(sub):
            continue
        eligible, template_job = _eligible_template_job(sub, existing_result)
        if not eligible:
            continue

        source_submission = submission_path.relative_to(queue_worker.ROOT).as_posix()
        replay = dict(sub)
        replay["_file"] = source_submission
        target = queue_worker.process_discovery_round_submission(replay, st, template_job=template_job)

        submitted_job_id = sub.get("job_id") if isinstance(sub.get("job_id"), str) else None
        result = {
            "schema_version": 1,
            "workflow_version": 10,
            "submission": source_submission,
            "ok": True,
            "operation": "submit_discovery_round",
            "recovered": bool(existing_result),
            "ingested": True,
            "submitted_job_id": submitted_job_id,
            "job_id": target["job_id"],
            "job_type": "discovery",
            "job_status": target.get("status"),
            "artifact": None,
        }
        queue_worker.write_json(result_path, result)
        recovered.append({
            "submission": source_submission,
            "submitted_job_id": submitted_job_id,
            "job_id": target["job_id"],
            "research_jobs_added": int((target.get("result_summary") or {}).get("research_jobs_added", 0) or 0),
        })

    # Preserve the normal worker-facing Discovery lane independently of ingest jobs.
    queue_worker.ensure_discovery_job()
    queue_worker.save_state(st)
    return {"recovered_count": len(recovered), "recovered": recovered}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".survey"))
    args = parser.parse_args()
    print(json.dumps(recover(args.root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
