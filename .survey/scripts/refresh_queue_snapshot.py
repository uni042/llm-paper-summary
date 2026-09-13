#!/usr/bin/env python3
"""Refresh next-jobs.json without running queue mutation/reconciliation work."""
from __future__ import annotations

import argparse
import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import claim_state


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp = Path(tmp.name)
    temp.replace(path)


def build_snapshot(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    jobs_dir = repo_root / ".survey/work-queue/jobs"
    jobs: list[dict[str, Any]] = []
    for path in sorted(jobs_dir.glob("*.json")) if jobs_dir.is_dir() else []:
        job = _read(path, {})
        if not isinstance(job, dict):
            continue
        row = dict(job)
        row.setdefault("job_id", path.stem)
        jobs.append(row)

    counts: dict[str, dict[str, int]] = {}
    for job in jobs:
        kind = str(job.get("type") or "unknown")
        status = str(job.get("status") or "unknown")
        counts.setdefault(kind, {})
        counts[kind][status] = counts[kind].get(status, 0) + 1

    claims = claim_state.current_claims(repo_root)
    claiming = claim_state.snapshot_claiming(jobs, repo_root)
    ready = [
        job for job in jobs
        if job.get("status") == "ready"
        and not (
            job.get("type") in claim_state.CLAIMABLE_TYPES
            and claims.get(str(job.get("job_id")), {}).get("active")
        )
    ]
    ready.sort(key=lambda job: (
        -int(job.get("priority") or 0),
        str(job.get("created_at") or ""),
        str(job.get("job_id") or ""),
    ))
    visible = ready[:8]
    if not any(job.get("type") == "discovery" for job in visible):
        discovery = next((job for job in ready if job.get("type") == "discovery"), None)
        if discovery is not None:
            visible.append(discovery)

    return {
        "counts": counts,
        "claiming": claiming,
        "next_jobs": [{
            key: job.get(key)
            for key in (
                "job_id", "type", "lane", "priority", "canonical_id", "title",
                "source_url", "paper_path", "instructions", "completion",
            )
        } for job in visible],
    }


def refresh(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    path = repo_root / ".survey/work-queue/next-jobs.json"
    snapshot = build_snapshot(repo_root)
    old = _read(path, {}) or {}
    old_cmp = dict(old)
    old_cmp.pop("generated_at", None)
    if old_cmp == snapshot:
        snapshot["generated_at"] = old.get("generated_at", _now())
    else:
        snapshot["generated_at"] = _now()
    _write(path, snapshot)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(refresh(args.repo_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
