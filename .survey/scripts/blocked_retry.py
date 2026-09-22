#!/usr/bin/env python3
"""Retry policy for temporarily blocked research jobs.

GitHub Actions is the queue/state writer. This helper observes research jobs that
queue_worker marked as blocked, counts each distinct blocked event once, and
requeues retrieval failures after a seven-day cooldown.

Primary-source retrieval failure is not a permanent-exclusion signal. After five
distinct blocked events spanning at least 28 days, automatic periodic retries are
suspended by keeping the job blocked with a durable dormant marker. The job is
not promoted to blocked_permanent or rejected by this helper.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


RETRY_DELAY_SECONDS = 7 * 24 * 60 * 60
DORMANT_AFTER_ATTEMPTS = 5
DORMANT_MIN_AGE_SECONDS = 28 * 24 * 60 * 60

# Backward-compatible name for callers/tests that imported the old constant.
# Reaching this number no longer means permanent exclusion.
MAX_BLOCKED_ATTEMPTS = DORMANT_AFTER_ATTEMPTS


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
    recorded = job.get("last_recorded_blocked_event")
    if isinstance(recorded, str) and recorded.strip():
        return recorded.strip()
    return "legacy:" + str(job.get("blocker") or job.get("job_id") or "unknown")


def first_blocked_time(job: dict) -> datetime | None:
    history = job.get("block_history")
    if isinstance(history, list):
        for item in history:
            if not isinstance(item, dict):
                continue
            value = parse_time(item.get("blocked_at"))
            if value is not None:
                return value
    for key in ("first_blocked_at", "last_blocked_at", "blocked_at", "completed_at"):
        value = parse_time(job.get(key))
        if value is not None:
            return value
    return None


def should_suspend_periodic_retry(job: dict, reference_time: datetime) -> bool:
    attempts = int(job.get("blocked_attempts", 0) or 0)
    if attempts < DORMANT_AFTER_ATTEMPTS:
        return False
    first = first_blocked_time(job)
    if first is None:
        return False
    return (reference_time - first).total_seconds() >= DORMANT_MIN_AGE_SECONDS


def mark_retry_dormant(job: dict, reference_time: datetime) -> None:
    job["status"] = "blocked"
    job["blocked_retry_dormant"] = True
    job["blocked_retry_state"] = "dormant"
    job["blocked_dormant_at"] = iso(reference_time)
    job.pop("retry_not_before", None)
    job.pop("retry_queued_at", None)
    # Temporary retrieval failure must not retain an automatic permanent marker.
    job.pop("blocked_permanent_at", None)


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
    blocked_at = str(job.get("completed_at") or job.get("blocked_at") or iso(reference_time))
    history.append(
        {
            "attempt": attempts,
            "blocked_at": blocked_at,
            "reason": job.get("blocker"),
        }
    )
    job["block_history"] = history
    if not job.get("first_blocked_at"):
        job["first_blocked_at"] = blocked_at
    job["last_blocked_at"] = blocked_at
    job.pop("retry_queued_at", None)
    job.pop("blocked_retry_dormant", None)
    job.pop("blocked_retry_state", None)
    job.pop("blocked_dormant_at", None)

    if should_suspend_periodic_retry(job, reference_time):
        mark_retry_dormant(job, reference_time)
    else:
        job["retry_not_before"] = iso(reference_time + timedelta(seconds=RETRY_DELAY_SECONDS))
    return True


def maybe_requeue(job: dict, reference_time: datetime) -> bool:
    if job.get("blocked_retry_dormant") is True or job.get("blocked_retry_state") == "dormant":
        return False

    if should_suspend_periodic_retry(job, reference_time):
        mark_retry_dormant(job, reference_time)
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
        "dormant": 0,
        # Kept for compatibility with dashboards/callers. This policy never
        # auto-promotes a retrieval failure to permanent exclusion.
        "permanent": 0,
        "changed": 0,
    }

    for path in sorted(jobs_dir.glob("*.json")):
        job = read_json(path)
        if job.get("type") != "research" or job.get("status") != "blocked":
            continue
        result["observed"] += 1

        if job.get("blocked_retry_dormant") is True or job.get("blocked_retry_state") == "dormant":
            continue

        changed = False

        is_new_event = record_new_block_event(job, reference_time)
        if is_new_event:
            changed = True
            result["new_block_events"] += 1
        elif maybe_requeue(job, reference_time):
            changed = True

        if not changed:
            continue

        if job.get("blocked_retry_dormant") is True:
            result["dormant"] += 1
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
