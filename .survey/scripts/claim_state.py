"""Shared repository-backed claim lease state helpers."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path
from typing import Any, Iterable

TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent", "failed", "cancelled"}
CLAIMABLE_TYPES = {"research", "audit"}


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def _read(path: Path) -> dict[str, Any] | None:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return obj if isinstance(obj, dict) else None


def _as_now(value: Any = None) -> dt.datetime:
    parsed = parse_time(value) if not isinstance(value, dt.datetime) else value
    if parsed is None:
        parsed = dt.datetime.now(dt.timezone.utc)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def current_claims(repo_root: Path, now: Any = None) -> dict[str, dict[str, Any]]:
    """Return one current claim per job, retaining expired claims on disk."""
    root = Path(repo_root) / ".survey/work-queue/claims"
    current = _as_now(now)
    out: dict[str, dict[str, Any]] = {}
    if not root.is_dir():
        return out
    for path in sorted(root.glob("*.json")):
        claim = _read(path)
        if not claim:
            continue
        job_id = str(claim.get("job_id") or path.stem)
        if not job_id:
            continue
        expires = parse_time(claim.get("expires_at"))
        row = dict(claim)
        row["job_id"] = job_id
        row["active"] = bool(expires and current < expires)
        row["expired"] = bool(expires and current >= expires)
        out[job_id] = row
    return out


def snapshot_claiming(jobs: Iterable[dict[str, Any]] | dict[str, dict[str, Any]], repo_root: Path, now: Any = None) -> dict[str, int]:
    """Summarize claimable ready research/audit jobs without changing lifecycle counts."""
    values = jobs.values() if isinstance(jobs, dict) else jobs
    ready = [
        job for job in values
        if isinstance(job, dict) and job.get("status") == "ready" and job.get("type") in CLAIMABLE_TYPES
    ]
    claims = current_claims(repo_root, now)
    active = sum(1 for job in ready if claims.get(str(job.get("job_id")), {}).get("active"))
    return {
        "ready_research_audit": len(ready),
        "actively_claimed": active,
        "claimable": len(ready) - active,
    }
