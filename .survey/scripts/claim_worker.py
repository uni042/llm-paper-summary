"""Allocate immutable repository-backed claim leases for ready research/audit jobs."""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import tempfile
from pathlib import Path
from typing import Any

import claim_state

SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
WORKER_KINDS = {"scheduled_chat", "work"}
JOB_TYPES = {"research", "audit"}
DEFAULT_MAX_JOBS = 1
DEFAULT_LEASE_SECONDS = 28800
MIN_LEASE_SECONDS = 300
MAX_LEASE_SECONDS = 43200


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def _as_time(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        return value.astimezone(dt.timezone.utc)
    return claim_state.parse_time(value)


def _write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp_name = tmp.name
    Path(temp_name).replace(path)


def _safe(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID_RE.fullmatch(value):
        raise ValueError(f"{label} must match [A-Za-z0-9][A-Za-z0-9._-]{{0,159}}")
    return value


def _normalize_request(path: Path, raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("request must be an object")
    request_id = _safe(raw.get("request_id"), "request_id")
    if path.stem != request_id:
        raise ValueError("request_id must match request filename")
    worker_id = _safe(raw.get("worker_id"), "worker_id")
    worker_kind = raw.get("worker_kind")
    if worker_kind not in WORKER_KINDS:
        raise ValueError("worker_kind must be scheduled_chat or work")
    requested_at_raw = raw.get("requested_at")
    requested_at = _as_time(requested_at_raw)
    if requested_at is None or not isinstance(requested_at_raw, str) or "T" not in requested_at_raw:
        raise ValueError("requested_at must be a valid UTC timestamp")
    try:
        parsed_raw = dt.datetime.fromisoformat(requested_at_raw.replace("Z", "+00:00"))
    except ValueError:
        parsed_raw = None
    if parsed_raw is None or parsed_raw.tzinfo is None:
        raise ValueError("requested_at must include a UTC offset")
    max_jobs = raw.get("max_jobs", DEFAULT_MAX_JOBS)
    if isinstance(max_jobs, bool) or not isinstance(max_jobs, int) or not 1 <= max_jobs <= 4:
        raise ValueError("max_jobs must be between 1 and 4")
    lease_seconds = raw.get("lease_seconds", DEFAULT_LEASE_SECONDS)
    if isinstance(lease_seconds, bool) or not isinstance(lease_seconds, int) or not MIN_LEASE_SECONDS <= lease_seconds <= MAX_LEASE_SECONDS:
        raise ValueError("lease_seconds must be between 300 and 43200")
    job_types = raw.get("job_types", ["research", "audit"])
    if not isinstance(job_types, list) or not job_types or any(kind not in JOB_TYPES for kind in job_types):
        raise ValueError("job_types must contain only research or audit")
    return {
        "schema_version": 1, "request_id": request_id, "worker_id": worker_id,
        "worker_kind": worker_kind, "requested_at": _iso(requested_at),
        "max_jobs": max_jobs, "lease_seconds": lease_seconds,
        "job_types": sorted(set(job_types)),
    }


def _claim_id(request_id: str, job_id: str) -> str:
    digest = hashlib.sha256(f"{request_id}\n{job_id}".encode("utf-8")).hexdigest()[:24]
    return f"claim-{digest}"


def _attempt_id(claim_id: str) -> str:
    return f"attempt-{claim_id.removeprefix('claim-')}"


def _job_files(root: Path) -> list[dict[str, Any]]:
    jobs = root / ".survey/work-queue/jobs"
    out = []
    for path in sorted(jobs.glob("*.json")) if jobs.is_dir() else []:
        obj = _read(path)
        if isinstance(obj, dict):
            row = dict(obj)
            row.setdefault("job_id", path.stem)
            out.append(row)
    return out


def _result_path(root: Path, request_id: str) -> Path:
    return root / ".survey/work-queue/claim-results" / f"{request_id}.json"


def process_requests(repo_root: Path, at: Any = None) -> dict[str, int]:
    root = Path(repo_root).resolve()
    now = _as_time(at) or dt.datetime.now(dt.timezone.utc)
    request_root = root / ".survey/work-queue/claim-requests"
    result_root = root / ".survey/work-queue/claim-results"
    claims_root = root / ".survey/work-queue/claims"
    request_root.mkdir(parents=True, exist_ok=True)
    result_root.mkdir(parents=True, exist_ok=True)
    claims_root.mkdir(parents=True, exist_ok=True)
    claims = claim_state.current_claims(root, now)
    processed = reused = errors = assigned = 0
    for path in sorted(request_root.glob("*.json")):
        result_path = _result_path(root, path.stem)
        if result_path.exists():
            reused += 1
            existing = _read(result_path, {})
            for item in existing.get("assignments", []) if isinstance(existing, dict) else []:
                if isinstance(item, dict):
                    assigned += 1
            continue
        raw = _read(path)
        try:
            request = _normalize_request(path, raw)
        except Exception as exc:
            errors += 1
            _write(result_path, {
                "schema_version": 1, "workflow_version": 10, "request_id": path.stem,
                "ok": False, "assignments": [], "error": str(exc),
            })
            processed += 1
            continue

        available = []
        for item in _job_files(root):
            job_id = str(item.get("job_id") or "")
            if item.get("status") != "ready" or item.get("type") not in request["job_types"]:
                continue
            current = claims.get(job_id)
            if current and current.get("active"):
                continue
            available.append(item)
        available.sort(key=lambda item: (-int(item.get("priority") or 0), str(item.get("created_at") or ""), str(item.get("job_id") or "")))
        assignments = []
        for item in available[:request["max_jobs"]]:
            job_id = str(item["job_id"])
            claim_id = _claim_id(request["request_id"], job_id)
            attempt_id = _attempt_id(claim_id)
            previous = claims.get(job_id)
            expires = now + dt.timedelta(seconds=request["lease_seconds"])
            claim = {
                "schema_version": 1, "workflow_version": 10,
                "claim_id": claim_id, "job_id": job_id,
                "worker_id": request["worker_id"], "worker_kind": request["worker_kind"],
                "attempt_id": attempt_id, "request_id": request["request_id"],
                "assigned_at": _iso(now), "expires_at": _iso(expires),
            }
            if previous and previous.get("claim_id") != claim_id:
                claim["previous_claim_id"] = previous.get("claim_id")
            _write(claims_root / f"{job_id}.json", claim)
            claims[job_id] = dict(claim, active=True, expired=False)
            assignments.append({
                "job_id": job_id, "claim_id": claim_id, "worker_id": request["worker_id"],
                "worker_kind": request["worker_kind"], "attempt_id": attempt_id,
                "assigned_at": _iso(now), "expires_at": _iso(expires),
            })
        _write(result_path, {
            "schema_version": 1, "workflow_version": 10, "request_id": request["request_id"],
            "worker_id": request["worker_id"], "worker_kind": request["worker_kind"],
            "ok": True, "assignments": assignments, "processed_at": _iso(now),
        })
        assigned += len(assignments)
        processed += 1
    return {"processed": processed, "reused": reused, "errors": errors, "assigned": assigned}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(process_requests(args.repo_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
