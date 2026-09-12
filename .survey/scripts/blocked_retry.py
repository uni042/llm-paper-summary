#!/usr/bin/env python3
"""Retry policy for temporarily blocked research jobs.

GitHub Actions is the queue/state writer. This helper observes research jobs that
queue_worker marked as ``blocked``, counts each distinct blocked event once, and
requeues the job after a cooldown. Repeated blocking is promoted to
``blocked_permanent`` so a bad source cannot loop forever.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


MAX_BLOCKED_ATTEMPTS = 3
RETRY_DELAY_SECONDS = 3600


def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def blocked_event_id(job: dict) -> str:
    completed_at = job.get("completed_at")
    if isinstance(completed_at, str) and completed_at.strip():
        return completed_at.strip()
    blocked_at = job.get("blocked_at")
    if isinstance(blocked_at, str) and blocked_at.strip():
        return blocked_at.strip()
    return "legacy:" + str(job.get("blocker") or job.get("job_id") or "unknown")


def promote_permanent(job: dict, reference_time: datetime) -> None:
    job["status"] = "blocked_permanent"
    job["blocked_permanent_at"] = iso(reference_time)
    job.pop("retry_not_before", None)
    job.pop("retry_queued_at", None)
    if not job.get("completed_at"):
        job["completed_at"] = iso(reference_time)


def record_new_block_event(job: dict, reference_time: datetime) -> bool:
    event_id = blocked_event_id(job)
    if job.get("last_recorded_blocked_event") == event_id:
        return False

    attempts = int(job.get("blocked_attempts", 0) or 0) + 1
    job["blocked_attempts"] = attempts
    job["last_recorded_blocked_event"] = event_id
    history = job.get("block_history")
    if not isinstance(history, list):
        history = []
    history.append(
        {
            "attempt": attempts,
            "blocked_at": str(job.get("completed_at") or job.get("blocked_at") or iso(reference_time)),
            "reason": job.get("blocker"),
        }
    )
    job["block_history"] = history
    job["last_blocked_at"] = history[-1]["blocked_at"]
    job.pop("retry_queued_at", None)

    if attempts >= MAX_BLOCKED_ATTEMPTS:
        promote_permanent(job, reference_time)
    else:
        job["retry_not_before"] = iso(reference_time + timedelta(seconds=RETRY_DELAY_SECONDS))
    return True


def maybe_requeue(job: dict, reference_time: datetime) -> bool:
    attempts = int(job.get("blocked_attempts", 0) or 0)
    if attempts >= MAX_BLOCKED_ATTEMPTS:
        promote_permanent(job, reference_time)
        return True

    retry_not_before = parse_time(job.get("retry_not_before"))
    if retry_not_before is None or reference_time < retry_not_before:
        return False

    job["status"] = "ready"
    job["retry_queued_at"] = iso(reference_time)
    job.pop("retry_not_before", None)
    job.pop("completed_at", None)
    return True


def process_blocked_research_jobs(root: Path, reference_time: datetime | None = None) -> dict:
    reference_time = (reference_time or utc_now()).astimezone(timezone.utc)
    jobs_dir = root / "work-queue" / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "observed": 0,
        "new_block_events": 0,
        "requeued": 0,
        "permanent": 0,
        "changed": 0,
    }

    for path in sorted(jobs_dir.glob("*.json")):
        job = read_json(path)
        if job.get("type") != "research" or job.get("status") != "blocked":
            continue
        result["observed"] += 1

        before_status = job.get("status")
        changed = False

        attempts = int(job.get("blocked_attempts", 0) or 0)
        if attempts >= MAX_BLOCKED_ATTEMPTS:
            promote_permanent(job, reference_time)
            changed = True
        else:
            is_new_event = record_new_block_event(job, reference_time)
            if is_new_event:
                changed = True
                result["new_block_events"] += 1
            elif maybe_requeue(job, reference_time):
                changed = True

        if not changed:
            continue

        if before_status != "blocked_permanent" and job.get("status") == "blocked_permanent":
            result["permanent"] += 1
        elif job.get("status") == "ready":
            result["requeued"] += 1
        result["changed"] += 1
        write_json(path, job)

    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".survey"))
    args = parser.parse_args()
    result = process_blocked_research_jobs(args.root.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
