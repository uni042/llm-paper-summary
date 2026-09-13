#!/usr/bin/env python3
"""Enforce Scheduled Chat claim lease policy at the fast-lane boundaries."""
from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
from pathlib import Path
from typing import Any

import claim_state

SCHEDULED_CHAT_MAX_LEASE_SECONDS = 5400


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp_name = tmp.name
    Path(temp_name).replace(path)


def _as_time(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=dt.timezone.utc)
        return value.astimezone(dt.timezone.utc)
    return claim_state.parse_time(value)


def _now(value: Any = None) -> dt.datetime:
    return _as_time(value) or dt.datetime.now(dt.timezone.utc)


def _iso(value: dt.datetime) -> str:
    return value.astimezone(dt.timezone.utc).replace(microsecond=0).isoformat()


def reject_oversized_scheduled_chat_requests(repo_root: Path, at: Any = None) -> int:
    root = Path(repo_root).resolve()
    now = _now(at)
    requests = root / ".survey/work-queue/claim-requests"
    results = root / ".survey/work-queue/claim-results"
    rejected = 0
    for path in sorted(requests.glob("*.json")) if requests.is_dir() else []:
        result_path = results / path.name
        if result_path.exists():
            continue
        request = _read(path)
        if not isinstance(request, dict) or request.get("worker_kind") != "scheduled_chat":
            continue
        lease = request.get("lease_seconds", SCHEDULED_CHAT_MAX_LEASE_SECONDS)
        if isinstance(lease, bool) or not isinstance(lease, int) or lease <= SCHEDULED_CHAT_MAX_LEASE_SECONDS:
            continue
        _write(result_path, {
            "schema_version": 1, "workflow_version": 10, "request_id": path.stem,
            "worker_id": request.get("worker_id"), "worker_kind": "scheduled_chat",
            "ok": False, "assignments": [],
            "error": f"scheduled_chat lease_seconds must be at most {SCHEDULED_CHAT_MAX_LEASE_SECONDS}; use heartbeat renewal instead",
            "processed_at": _iso(now),
        })
        rejected += 1
    return rejected


def normalize_legacy_scheduled_chat_claims(repo_root: Path, at: Any = None) -> int:
    root = Path(repo_root).resolve()
    now = _now(at)
    claims_root = root / ".survey/work-queue/claims"
    normalized = 0
    for path in sorted(claims_root.glob("*.json")) if claims_root.is_dir() else []:
        claim = _read(path)
        if not isinstance(claim, dict) or claim.get("worker_kind") != "scheduled_chat" or claim.get("released_at"):
            continue
        activity = _as_time(claim.get("heartbeat_at") or claim.get("claimed_at"))
        expires = _as_time(claim.get("expires_at"))
        if activity is None or expires is None:
            continue
        canonical_expiry = activity + dt.timedelta(seconds=SCHEDULED_CHAT_MAX_LEASE_SECONDS)
        if expires <= canonical_expiry:
            continue
        claim["expires_at"] = _iso(canonical_expiry)
        claim["lease_normalized_at"] = _iso(now)
        claim["lease_normalization_reason"] = "scheduled_chat_90m_cap"
        if now >= canonical_expiry:
            claim["invalidated_at"] = _iso(now)
            claim["invalidation_reason"] = "legacy_scheduled_chat_lease_exceeded_90m"
        _write(path, claim)
        normalized += 1
    return normalized


def normalize(repo_root: Path, at: Any = None) -> dict[str, int]:
    return {"rejected_requests": reject_oversized_scheduled_chat_requests(repo_root, at), "normalized_claims": normalize_legacy_scheduled_chat_claims(repo_root, at)}


def verify_descriptor_claim(repo_root: Path, descriptor: dict[str, Any], at: Any = None) -> None:
    root = Path(repo_root).resolve()
    job_id = descriptor.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        raise ValueError("descriptor job_id is required")
    claim = _read(root / ".survey/work-queue/claims" / f"{job_id}.json", {}) or {}
    if not claim:
        return
    if claim.get("attempt_id") and claim.get("attempt_id") != descriptor.get("attempt_id"):
        raise ValueError("stale attempt: descriptor attempt_id no longer owns current claim")
    if descriptor.get("claim_id") and claim.get("claim_id") and descriptor.get("claim_id") != claim.get("claim_id"):
        raise ValueError("stale attempt: descriptor claim_id no longer matches current claim")
    if descriptor.get("worker_id") and claim.get("worker_id") and descriptor.get("worker_id") != claim.get("worker_id"):
        raise ValueError("stale attempt: descriptor worker_id no longer owns current claim")
    if claim.get("invalidated_at") or claim.get("invalidation_reason"):
        raise ValueError("claim invalidated: " + str(claim.get("invalidation_reason") or "unspecified"))
    expires = _as_time(claim.get("expires_at"))
    if expires is not None and _now(at) >= expires:
        if claim.get("released_at"):
            return
        raise ValueError("claim lease expired before immutable descriptor publication")


def _submission_path(repo_root: Path, submission: Path) -> Path:
    root = Path(repo_root).resolve()
    path = Path(submission)
    if not path.is_absolute():
        path = root / path
    path = path.resolve()
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise ValueError("submission path must stay within repository") from exc
    parts = relative.parts
    if len(parts) != 5 or parts[:3] != (".survey", "work-queue", "submissions") or parts[3] not in {"research", "audit"} or path.suffix != ".json":
        raise ValueError("submission must be directly under submissions/research or submissions/audit")
    return path


def verify_submission(repo_root: Path, submission: Path, at: Any = None) -> None:
    root = Path(repo_root).resolve()
    path = _submission_path(root, submission)
    descriptor = _read(path)
    if not isinstance(descriptor, dict):
        raise ValueError("submission descriptor must be a JSON object")
    verify_descriptor_claim(root, descriptor, at)


def record_verification_failure(repo_root: Path, submission: Path, exc: Exception, at: Any = None) -> dict[str, Any] | None:
    root = Path(repo_root).resolve()
    try:
        path = _submission_path(root, submission)
        descriptor = _read(path)
    except Exception:
        return None
    if not isinstance(descriptor, dict):
        return None
    attempt_id, job_id = descriptor.get("attempt_id"), descriptor.get("job_id")
    kind = descriptor.get("kind") or path.parent.name
    if not isinstance(attempt_id, str) or not attempt_id or not isinstance(job_id, str) or not job_id or kind not in {"research", "audit"}:
        return None
    result_path = root / ".survey/work-queue/results" / kind / path.name
    existing = _read(result_path)
    if isinstance(existing, dict):
        if existing.get("attempt_id") == attempt_id and existing.get("job_id") == job_id:
            return existing
        raise ValueError("immutable result path already contains a conflicting attempt/job")
    result = {
        "schema_version": 1, "workflow_version": 10, "ok": False,
        "attempt_id": attempt_id, "job_id": job_id, "job_type": kind,
        "job_status": None, "artifact": None,
        "submission": path.relative_to(root).as_posix(),
        "error": f"{type(exc).__name__}: {exc}", "processed_at": _iso(_now(at)),
    }
    _write(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("normalize", "verify"))
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--submission", type=Path)
    args = parser.parse_args()
    if args.command == "normalize":
        print(json.dumps(normalize(args.repo_root), ensure_ascii=False, indent=2))
        return 0
    if args.submission is None:
        parser.error("--submission is required for verify")
    try:
        verify_submission(args.repo_root, args.submission)
    except Exception as exc:
        result = record_verification_failure(args.repo_root, args.submission, exc)
        print(json.dumps(result, ensure_ascii=False, indent=2) if result is not None else f"{type(exc).__name__}: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
