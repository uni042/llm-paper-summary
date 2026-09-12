#!/usr/bin/env python3
"""Inspect reusable workflow-v10 record banks and choose a safe direct-write bank.

This script is advisory for the Chat worker. Bank exhaustion is never a reason
for STOP_RUN when the complete payload can be durably checkpointed to ChatGPT Library.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from record_bank_config import BANK_IDS, BANK_ROOTS, SLOT_NAMES  # noqa: E402

PLACEHOLDER_ATTEMPT = "unused-bank-placeholder"
INBOX = Path(".survey/work-queue/submissions/chat-inbox.json")
RESULT = Path(".survey/work-queue/results/chat-inbox.json")
NEXT_JOBS = Path(".survey/work-queue/next-jobs.json")
JOBS = Path(".survey/work-queue/jobs")


def read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def ready_job_ids(repo_root: Path) -> set[str]:
    """Return every canonical ready job, not only the next-jobs priority window."""
    jobs_dir = repo_root / JOBS
    if jobs_dir.is_dir():
        ready: set[str] = set()
        for path in sorted(jobs_dir.glob("*.json")):
            job = read_object(path)
            if not job or job.get("status") != "ready" or not job.get("job_id"):
                continue
            ready.add(str(job["job_id"]))
        return ready

    # Compatibility fallback for isolated fixtures or legacy snapshots that do not
    # include the canonical job directory. next-jobs is only a priority window and
    # must never be preferred when the full job directory is available.
    value = read_object(repo_root / NEXT_JOBS)
    if not value:
        return set()
    jobs = value.get("next_jobs")
    if not isinstance(jobs, list):
        return set()
    return {
        str(job.get("job_id"))
        for job in jobs
        if isinstance(job, dict) and job.get("job_id") and job.get("status", "ready") == "ready"
    }


def current_transport(repo_root: Path) -> tuple[dict[str, Any] | None, bool]:
    inbox = read_object(repo_root / INBOX)
    result = read_object(repo_root / RESULT)
    if not inbox or not inbox.get("job_id"):
        return inbox, True
    settled = bool(result and result.get("job_id") == inbox.get("job_id"))
    return inbox, settled


def inspect_bank(repo_root: Path, bank: str, ready_ids: set[str], inbox: dict[str, Any] | None, settled: bool) -> dict[str, Any]:
    root = repo_root / BANK_ROOTS[bank]
    slot_state: list[dict[str, Any]] = []
    attempts: set[str] = set()
    jobs: set[str] = set()
    missing = False

    for slot in SLOT_NAMES:
        path = root / f"{slot}.json"
        payload = read_object(path)
        if payload is None:
            missing = True
            slot_state.append({"slot": slot, "state": "missing_or_invalid"})
            continue
        attempt_id = str(payload.get("attempt_id") or "")
        job_id = str(payload.get("job_id") or "")
        if attempt_id:
            attempts.add(attempt_id)
        if job_id:
            jobs.add(job_id)
        slot_state.append({"slot": slot, "attempt_id": attempt_id, "job_id": job_id})

    if missing:
        state = "dirty"
        reason = "one or more slot files are missing/invalid"
    elif attempts == {PLACEHOLDER_ATTEMPT}:
        state = "free"
        reason = "unused pre-created bank"
    elif len(attempts) != 1 or len(jobs) != 1:
        state = "dirty"
        reason = "slot attempt/job identifiers are mixed"
    else:
        attempt_id = next(iter(attempts))
        job_id = next(iter(jobs))
        active_here = bool(
            inbox
            and str(inbox.get("record_bank") or "a").lower() == bank
            and inbox.get("attempt_id") == attempt_id
            and inbox.get("job_id") == job_id
        )
        if active_here and not settled:
            state = "occupied"
            reason = "current reusable inbox still references this attempt without a matching result"
        elif job_id in ready_ids:
            state = "occupied"
            reason = "bank belongs to a job that is still ready/incomplete in the canonical job queue"
        else:
            state = "reusable"
            reason = "coherent old attempt is not an active/ready job"

    return {
        "bank": bank,
        "root": BANK_ROOTS[bank],
        "state": state,
        "reason": reason,
        "slots": slot_state,
    }


def inspect(repo_root: Path) -> dict[str, Any]:
    ready_ids = ready_job_ids(repo_root)
    inbox, settled = current_transport(repo_root)
    banks = [inspect_bank(repo_root, bank, ready_ids, inbox, settled) for bank in BANK_IDS]
    selectable = [b["bank"] for b in banks if b["state"] in {"free", "reusable"}]
    return {
        "schema_version": 1,
        "selected_bank": selectable[0] if selectable else None,
        "direct_bank_available": bool(selectable),
        "if_no_bank": "checkpoint complete logical payload to ChatGPT Library and continue; bank exhaustion is not STOP_RUN",
        "ready_job_ids": sorted(ready_ids),
        "current_inbox_job_id": inbox.get("job_id") if inbox else None,
        "current_inbox_settled": settled,
        "banks": banks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = inspect(Path(args.repo_root).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
