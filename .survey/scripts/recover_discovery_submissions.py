#!/usr/bin/env python3
"""Ingest and recover stranded root-level Discovery submissions.

Two compatibility paths are intentionally distinct:

* current self-describing specialist rounds carry durable round identity and may be
  ingested without a pre-issued worker-facing Discovery job;
* older payloads without discovery_stats are replayed only when their original job
  still exists and is a terminal Discovery job.

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


def _create_legacy_recovery_job(source_submission: str, old_job: dict) -> dict:
    """Preserve the pre-v10.1 terminal-job replay contract for old payloads."""
    for sequence in range(1, 1000):
        job_id = queue_worker.stable_id("job", "discovery-recovery", source_submission, str(sequence))
        path = queue_worker.JOBS / f"{job_id}.json"
        if path.exists():
            existing = _read(path, {}) or {}
            if (
                existing.get("type") == "discovery"
                and existing.get("recovery_for_submission") == source_submission
                and existing.get("status") == "ready"
            ):
                existing["_path"] = path
                return existing
            continue
        queue_worker.add_job({
            "job_id": job_id,
            "type": "discovery",
            "lane": "discovery-ingest",
            "priority": int(old_job.get("priority") or 50),
            "status": "ready",
            "recovery_only": True,
            "recovery_for_submission": source_submission,
            "instructions": old_job.get("instructions") or (
                "Recovery-only Discovery job. Apply the already durable candidate payload; "
                "do not perform new research in this job."
            ),
            "completion": old_job.get("completion") or "Apply the durable Discovery candidate payload.",
        })
        created = _read(path, {}) or {}
        created["_path"] = path
        return created
    raise RuntimeError("unable to allocate a unique Discovery recovery job")


def _result_allows_recovery(existing_result: dict) -> bool:
    """Allow new rounds plus the known stale Discovery failure modes."""
    if not existing_result:
        return True
    if existing_result.get("ok") is True:
        return False
    error = str(existing_result.get("error") or "")
    return "job already terminal" in error or "unknown job_id" in error or "job_id required" in error


def _old_discovery_job(sub: dict) -> dict:
    submitted_job_id = sub.get("job_id")
    if not isinstance(submitted_job_id, str) or not submitted_job_id:
        return {}
    return _read(queue_worker.JOBS / f"{submitted_job_id}.json", {}) or {}


def _recover_self_describing_round(
    sub: dict,
    source_submission: str,
    existing_result: dict,
    st: dict,
) -> dict[str, Any] | None:
    if not queue_worker.is_discovery_round_submission(sub):
        return None

    submitted_job_id = sub.get("job_id") if isinstance(sub.get("job_id"), str) else None
    old_job = _old_discovery_job(sub)
    if old_job:
        if old_job.get("type") != "discovery":
            return None
        if old_job.get("status") not in queue_worker.TERMINAL:
            # A live real Discovery job still belongs to the normal queue worker.
            return None
    elif submitted_job_id is None and sub.get("operation") != "submit_discovery_round":
        return None

    replay = dict(sub)
    replay["_file"] = source_submission
    target = queue_worker.process_discovery_round_submission(replay, st, template_job=old_job)
    return {
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
        "research_jobs_added": int((target.get("result_summary") or {}).get("research_jobs_added", 0) or 0),
    }


def _recover_legacy_terminal_submission(
    sub: dict,
    source_submission: str,
    existing_result: dict,
    st: dict,
) -> dict[str, Any] | None:
    """Recover old candidate-only payloads only from a verifiable terminal Discovery job."""
    candidates = sub.get("candidates")
    if not isinstance(candidates, list):
        return None
    submitted_job_id = sub.get("job_id")
    if not isinstance(submitted_job_id, str) or not submitted_job_id:
        return None
    old_job = _old_discovery_job(sub)
    if old_job.get("type") != "discovery" or old_job.get("status") not in queue_worker.TERMINAL:
        return None

    target = _create_legacy_recovery_job(source_submission, old_job)
    replay = dict(sub)
    replay["submitted_job_id"] = submitted_job_id
    replay["job_id"] = target["job_id"]
    replay["_file"] = source_submission
    queue_worker.process_discovery(replay, target, st)
    queue_worker.update_job(target)

    return {
        "schema_version": 1,
        "workflow_version": 10,
        "submission": source_submission,
        "ok": True,
        "recovered": bool(existing_result) or True,
        "submitted_job_id": submitted_job_id,
        "job_id": target["job_id"],
        "job_type": "discovery",
        "job_status": "completed",
        "artifact": None,
        "research_jobs_added": int((target.get("result_summary") or {}).get("research_jobs_added", 0) or 0),
    }


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
        if not isinstance(sub, dict):
            continue
        source_submission = submission_path.relative_to(queue_worker.ROOT).as_posix()

        result = _recover_self_describing_round(sub, source_submission, existing_result, st)
        if result is None:
            result = _recover_legacy_terminal_submission(sub, source_submission, existing_result, st)
        if result is None:
            continue

        queue_worker.write_json(result_path, result)
        recovered.append({
            "submission": source_submission,
            "submitted_job_id": result.get("submitted_job_id"),
            "job_id": result["job_id"],
            "research_jobs_added": result.get("research_jobs_added", 0),
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
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
