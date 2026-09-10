#!/usr/bin/env python3
"""Materialize deterministic research jobs from a Drive-delivered spillover seed.

This is a recovery transport only. Scheduled Chat may discover candidates while
GitHub writes are unavailable, save this seed to the Drive outbox, and continue
researching those candidates using the deterministic job IDs produced here.
GitHub remains canonical once the seed is imported.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import queue_worker as queue  # noqa: E402

MAX_CANDIDATES = 5
SEED_REL = Path("work-queue/transport/offline-job-seed.json")


def read_object(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def configure_queue(root: Path) -> None:
    queue.ROOT = root
    queue.QUEUE = root / "work-queue"
    queue.JOBS = queue.QUEUE / "jobs"
    queue.SUBMISSIONS = queue.QUEUE / "submissions"
    queue.RESULTS = queue.QUEUE / "results"
    queue.STATE = queue.QUEUE / "state.json"
    queue.ARCHIVE = queue.QUEUE / "archive"


def apply(root: Path) -> dict:
    configure_queue(root)
    path = root / SEED_REL
    if not path.exists():
        return {"seed_present": False, "created": [], "skipped": []}

    seed = read_object(path)
    if seed.get("schema_version") != 1 or int(seed.get("transport_version") or 0) != 10:
        raise ValueError("offline job seed requires schema_version=1 and transport_version=10")
    seed_id = seed.get("seed_id")
    if not isinstance(seed_id, str) or not seed_id.strip():
        raise ValueError("offline job seed requires non-empty seed_id")
    candidates = seed.get("candidates")
    if not isinstance(candidates, list):
        raise ValueError("offline job seed candidates must be a list")
    if len(candidates) > MAX_CANDIDATES:
        raise ValueError(f"offline job seed accepts at most {MAX_CANDIDATES} candidates")

    seen = queue.existing_candidate_keys()
    created: list[str] = []
    skipped: list[dict] = []
    for candidate in sorted(candidates, key=lambda x: int(x.get("priority") or 0), reverse=True):
        if not isinstance(candidate, dict):
            raise ValueError("each offline candidate must be an object")
        key = queue.candidate_key(candidate)
        if not key:
            skipped.append({"reason": "missing_candidate_key"})
            continue
        priority = int(candidate.get("priority") or 0)
        if priority < 40:
            skipped.append({"key": key, "reason": "priority_below_40"})
            continue
        deterministic_job_id = queue.stable_id("job-research", key)
        if key in seen or (queue.JOBS / f"{deterministic_job_id}.json").exists():
            skipped.append({"key": key, "job_id": deterministic_job_id, "reason": "already_known"})
            continue
        if queue.make_research_job(candidate, f"offline-seed:{seed_id}"):
            created.append(deterministic_job_id)
            seen.add(key)

    result = {
        "seed_present": True,
        "seed_id": seed_id,
        "created": created,
        "skipped": skipped,
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
