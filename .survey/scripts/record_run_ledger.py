#!/usr/bin/env python3
"""Capture and record meaningful survey-helper state transitions.

The ledger is intentionally bounded and append-like. Scheduled no-op helper runs
do not change the ledger, avoiding a commit every ten minutes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
from typing import Any


DEFAULT_HISTORY_LIMIT = 48


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def collect_snapshot(root: Path) -> dict[str, Any]:
    survey = root / ".survey"
    jobs_dir = survey / "work-queue/jobs"
    jobs: dict[str, dict[str, Any]] = {}
    if jobs_dir.is_dir():
        for path in sorted(jobs_dir.glob("*.json")):
            data = load_json(path)
            if not data:
                continue
            job_id = str(data.get("job_id") or path.stem)
            jobs[job_id] = {
                "status": data.get("status"),
                "type": data.get("type"),
                "canonical_id": data.get("canonical_id"),
                "title": data.get("title"),
            }

    identity = load_json(survey / "survey-state/paper-identity-index.json") or {}
    papers = identity.get("papers") if isinstance(identity.get("papers"), dict) else {}

    results_dir = survey / "work-queue/results"
    result_files = sorted(
        p.relative_to(root).as_posix() for p in results_dir.glob("*.json")
    ) if results_dir.is_dir() else []

    archive_dir = survey / "work-queue/fallback-archive"
    archive_files = sorted(
        p.relative_to(root).as_posix() for p in archive_dir.glob("*.json")
    ) if archive_dir.is_dir() else []

    state = load_json(survey / "work-queue/maintenance-cycle.json") or {}
    return {
        "captured_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "jobs": jobs,
        "paper_ids": sorted(str(k) for k in papers.keys()),
        "active_count": identity.get("active_count"),
        "result_files": result_files,
        "fallback_archive_files": archive_files,
        "source_run_key": state.get("last_counted_run_key"),
    }


def write_snapshot(root: Path, output: Path) -> int:
    snapshot = collect_snapshot(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"action": "snapshot", "output": str(output)}))
    return 0


def terminal_transitions(before: dict[str, Any], after: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    before_jobs = before.get("jobs") if isinstance(before.get("jobs"), dict) else {}
    after_jobs = after.get("jobs") if isinstance(after.get("jobs"), dict) else {}
    for job_id, current in sorted(after_jobs.items()):
        if not isinstance(current, dict):
            continue
        current_status = current.get("status")
        previous = before_jobs.get(job_id)
        previous_status = previous.get("status") if isinstance(previous, dict) else None
        if current_status not in {"completed", "blocked"}:
            continue
        if previous_status == current_status:
            continue
        out.append({
            "job_id": job_id,
            "type": current.get("type"),
            "canonical_id": current.get("canonical_id"),
            "title": current.get("title"),
            "from": previous_status,
            "to": current_status,
        })
    return out


def record(root: Path, baseline_path: Path) -> int:
    before = load_json(baseline_path)
    if before is None:
        print(json.dumps({"action": "skipped", "reason": "baseline_unreadable"}))
        return 0
    after = collect_snapshot(root)

    transitions = terminal_transitions(before, after)
    before_jobs = before.get("jobs") if isinstance(before.get("jobs"), dict) else {}
    after_jobs = after.get("jobs") if isinstance(after.get("jobs"), dict) else {}
    new_job_ids = sorted(set(after_jobs) - set(before_jobs))
    new_jobs = [
        {"job_id": job_id, **after_jobs[job_id]}
        for job_id in new_job_ids
        if isinstance(after_jobs.get(job_id), dict)
    ]

    before_papers = set(before.get("paper_ids") or [])
    after_papers = set(after.get("paper_ids") or [])
    new_paper_ids = sorted(after_papers - before_papers)

    before_results = set(before.get("result_files") or [])
    after_results = set(after.get("result_files") or [])
    new_results = sorted(after_results - before_results)
    new_discovery_results = [p for p in new_results if "discovery" in Path(p).name.lower()]

    before_archive = set(before.get("fallback_archive_files") or [])
    after_archive = set(after.get("fallback_archive_files") or [])
    new_archive = sorted(after_archive - before_archive)

    completed = [t for t in transitions if t.get("to") == "completed"]
    blocked = [t for t in transitions if t.get("to") == "blocked"]
    research_completed = [t for t in completed if t.get("type") == "research"]
    audit_completed = [t for t in completed if t.get("type") == "audit"]
    discovery_completed = [t for t in completed if t.get("type") == "discovery"]

    meaningful = any([
        transitions,
        new_jobs,
        new_paper_ids,
        new_discovery_results,
        new_archive,
    ])
    if not meaningful:
        print(json.dumps({"action": "noop", "meaningful": False}))
        return 0

    workflow_run_id = os.environ.get("GITHUB_RUN_ID")
    workflow_attempt = os.environ.get("GITHUB_RUN_ATTEMPT", "1")
    event_id = f"{workflow_run_id}:{workflow_attempt}" if workflow_run_id else None
    now = dt.datetime.now(dt.timezone.utc).isoformat()

    signals: list[str] = []
    if research_completed:
        signals.append("research_completed")
    if audit_completed:
        signals.append("audit_completed")
    if discovery_completed or new_discovery_results or new_jobs:
        signals.append("discovery_or_queue_expanded")
    if blocked:
        signals.append("job_blocked")
    if new_archive:
        signals.append("fallback_archived")
    if new_paper_ids:
        signals.append("paper_materialized")

    entry = {
        "event_id": event_id,
        "recorded_at": now,
        "source_run_key": after.get("source_run_key") or before.get("source_run_key"),
        "github": {
            "event_name": os.environ.get("GITHUB_EVENT_NAME"),
            "workflow": os.environ.get("GITHUB_WORKFLOW"),
            "run_id": workflow_run_id,
            "run_attempt": workflow_attempt,
            "source_sha": os.environ.get("GITHUB_SHA"),
        },
        "signals": signals,
        "counts": {
            "research_completed": len(research_completed),
            "audit_completed": len(audit_completed),
            "discovery_completed": len(discovery_completed),
            "blocked": len(blocked),
            "new_jobs": len(new_jobs),
            "new_papers": len(new_paper_ids),
            "fallback_archived": len(new_archive),
        },
        "terminal_transitions": transitions,
        "new_jobs": new_jobs,
        "new_paper_ids": new_paper_ids,
        "new_discovery_results": new_discovery_results,
        "new_fallback_archive_files": new_archive,
        "paper_active_count_before": before.get("active_count"),
        "paper_active_count_after": after.get("active_count"),
        "last_successful_action": signals[-1] if signals else "queue_state_changed",
    }

    ledger_path = root / ".survey/work-queue/run-ledger.json"
    ledger = load_json(ledger_path) or {
        "schema_version": 1,
        "history_limit": DEFAULT_HISTORY_LIMIT,
        "updated_at": None,
        "entries": [],
    }
    limit = ledger.get("history_limit")
    if not isinstance(limit, int) or limit < 1:
        limit = DEFAULT_HISTORY_LIMIT
        ledger["history_limit"] = limit
    entries = ledger.get("entries")
    if not isinstance(entries, list):
        entries = []

    if event_id:
        entries = [e for e in entries if not (isinstance(e, dict) and e.get("event_id") == event_id)]
    entries.append(entry)
    ledger["entries"] = entries[-limit:]
    ledger["updated_at"] = now
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    ledger_path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({
        "action": "recorded",
        "event_id": event_id,
        "signals": signals,
        "counts": entry["counts"],
    }, ensure_ascii=False))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["snapshot", "record"])
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--snapshot", default="/tmp/survey-helper-baseline.json")
    args = parser.parse_args()

    root = Path(args.repo_root)
    snapshot_path = Path(args.snapshot)
    if args.command == "snapshot":
        return write_snapshot(root, snapshot_path)
    return record(root, snapshot_path)


if __name__ == "__main__":
    raise SystemExit(main())
