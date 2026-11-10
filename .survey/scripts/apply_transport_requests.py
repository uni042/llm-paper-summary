#!/usr/bin/env python3
"""Apply small transport control requests for workflow-v10.

The primary use is checkpoint-aware discovery replenishment: Scheduled Chat may
have durably saved one or more ready jobs to an external outbox while GitHub
still shows them as ready. Those jobs remain canonically incomplete, but they
must not prevent generation of the next independent discovery job.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import queue_worker as queue  # noqa: E402

REQUEST_REL = Path("work-queue/transport/request-jobs.json")
MAX_IGNORED_READY = 256


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def configure_queue(root: Path) -> None:
    queue.ROOT = root
    queue.QUEUE = root / "work-queue"
    queue.JOBS = queue.QUEUE / "jobs"
    queue.SUBMISSIONS = queue.QUEUE / "submissions"
    queue.RESULTS = queue.QUEUE / "results"
    queue.STATE = queue.QUEUE / "state.json"
    queue.ARCHIVE = queue.QUEUE / "archive"


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def create_discovery(request_id: str) -> str | None:
    jid = queue.stable_id("job", "checkpoint-aware-discovery", request_id)
    created = queue.add_job({
        "job_id": jid,
        "type": "discovery",
        "lane": "discovery",
        "priority": 50,
        "workflow_version": 10,
        "created_at": now(),
        "instructions": (
            "Search primary sources for strong LLM inference-system papers not already "
            "represented in the repository or fallback spillover backlog. Prefer recent "
            "work, but include an older important omission when clearly worthwhile. "
            "Return at most 5 candidates; weak filler is not required."
        ),
        "completion": "Submit 0-5 strong candidates. Empty is valid.",
    })
    return jid if created else None


def apply(root: Path) -> dict:
    configure_queue(root)
    path = root / REQUEST_REL
    if not path.exists():
        return {"request_present": False, "generated_ready_jobs": []}

    req = read_object(path)
    if req.get("schema_version") != 1:
        raise ValueError("request-jobs schema_version must be 1")
    if req.get("operation") != "ensure_discovery_excluding_checkpointed":
        return {"request_present": True, "ignored_operation": req.get("operation"), "generated_ready_jobs": []}
    request_id = req.get("request_id")
    if not isinstance(request_id, str) or not request_id.strip():
        raise ValueError("request_id is required")
    ignored = req.get("checkpointed_job_ids") or []
    if not isinstance(ignored, list) or not all(isinstance(x, str) and x for x in ignored):
        raise ValueError("checkpointed_job_ids must be a string array")
    if len(ignored) > MAX_IGNORED_READY:
        raise ValueError(f"too many checkpointed_job_ids; max={MAX_IGNORED_READY}")
    ignored_set = set(ignored)

    ready = [j for j in queue.iter_jobs() if j.get("status") == "ready"]
    actionable = [j for j in ready if j.get("job_id") not in ignored_set]
    if actionable:
        result = {
            "request_present": True,
            "request_id": request_id,
            "checkpointed_ready_ignored": sorted(j.get("job_id") for j in ready if j.get("job_id") in ignored_set),
            "actionable_ready_count": len(actionable),
            "generated_ready_jobs": [],
        }
        print(json.dumps(result, ensure_ascii=False))
        return result

    created = create_discovery(request_id)
    result = {
        "request_present": True,
        "request_id": request_id,
        "checkpointed_ready_ignored": sorted(j.get("job_id") for j in ready if j.get("job_id") in ignored_set),
        "actionable_ready_count": 0,
        "generated_ready_jobs": [created] if created else [],
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".survey"))
    args = parser.parse_args()
    apply(args.root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
