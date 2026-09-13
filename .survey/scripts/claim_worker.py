"""Allocate renewable repository-backed claim leases for ready research/audit jobs."""
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
DEFAULT_LEASE_SECONDS = 5400
MIN_LEASE_SECONDS = 300
MAX_LEASE_SECONDS = 43200
MAX_CHECKPOINTED_JOBS = 128
LIBRARY_CHECKPOINT_PREFIX = "/LLM-survey-outbox/pending/"


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


def _normalize_checkpointed_jobs(raw: Any) -> list[dict[str, str]]:
    if raw is None:
        return []
    if not isinstance(raw, list) or len(raw) > MAX_CHECKPOINTED_JOBS:
        raise ValueError(f"checkpointed_jobs must be a list with at most {MAX_CHECKPOINTED_JOBS} items")
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"checkpointed_jobs[{index}] must be an object")
        job_id = _safe(item.get("job_id"), f"checkpointed_jobs[{index}].job_id")
        checkpoint_ref = item.get("checkpoint_ref")
        if (
            not isinstance(checkpoint_ref, str)
            or len(checkpoint_ref) > 512
            or not checkpoint_ref.startswith(LIBRARY_CHECKPOINT_PREFIX)
            or not checkpoint_ref.endswith(".json")
            or ".." in Path(checkpoint_ref).parts
        ):
            raise ValueError(
                f"checkpointed_jobs[{index}].checkpoint_ref must be a JSON path under {LIBRARY_CHECKPOINT_PREFIX}"
            )
        if job_id in seen:
            raise ValueError("checkpointed_jobs must not repeat job_id")
        seen.add(job_id)
        normalized.append({"job_id": job_id, "checkpoint_ref": checkpoint_ref})
    return normalized


def _normalize_request(path: Path, raw: Any) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("request must be an object")
    if raw.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
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
    if parsed_raw is None or parsed_raw.tzinfo is None or parsed_raw.utcoffset() != dt.timedelta(0):
        raise ValueError("requested_at must be UTC (Z or +00:00)")
    max_jobs = raw.get("max_jobs", DEFAULT_MAX_JOBS)
    if isinstance(max_jobs, bool) or not isinstance(max_jobs, int) or not 1 <= max_jobs <= 4:
        raise ValueError("max_jobs must be between 1 and 4")
    if worker_kind == "scheduled_chat" and max_jobs != 1:
        raise ValueError("scheduled_chat requests must use max_jobs=1")
    lease_seconds = raw.get("lease_seconds", DEFAULT_LEASE_SECONDS)
    if isinstance(lease_seconds, bool) or not isinstance(lease_seconds, int) or not MIN_LEASE_SECONDS <= lease_seconds <= MAX_LEASE_SECONDS:
        raise ValueError("lease_seconds must be between 300 and 43200")
    if worker_kind == "scheduled_chat" and lease_seconds > DEFAULT_LEASE_SECONDS:
        raise ValueError(f"scheduled_chat lease_seconds must be between {MIN_LEASE_SECONDS} and {DEFAULT_LEASE_SECONDS}")
    job_types = raw.get("job_types", ["research", "audit"])
    if not isinstance(job_types, list) or not job_types or any(kind not in JOB_TYPES for kind in job_types):
        raise ValueError("job_types must contain only research or audit")
    checkpointed_jobs = _normalize_checkpointed_jobs(raw.get("checkpointed_jobs"))
    return {
        "schema_version": 1, "request_id": request_id, "worker_id": worker_id,
        "worker_kind": worker_kind, "requested_at": _iso(requested_at),
        "max_jobs": max_jobs, "lease_seconds": lease_seconds,
        "job_types": sorted(set(job_types)),
        "checkpointed_jobs": checkpointed_jobs,
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
            job_id = obj.get("job_id")
            if not isinstance(job_id, str) or not SAFE_ID_RE.fullmatch(job_id) or path.stem != job_id:
                continue
            row = dict(obj)
            row.pop("_path", None)
            out.append(row)
    return out


def _immutable_descriptors(root: Path) -> list[dict[str, Any]]:
    """Return only durable immutable descriptors that are still pending processing."""
    out: list[dict[str, Any]] = []
    submissions = root / ".survey/work-queue/submissions"
    results = root / ".survey/work-queue/results"
    for kind in sorted(JOB_TYPES):
        folder = submissions / kind
        for path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
            value = _read(path)
            if not isinstance(value, dict):
                continue
            job_id = value.get("job_id")
            attempt_id = value.get("attempt_id")
            if not isinstance(job_id, str) or not SAFE_ID_RE.fullmatch(job_id):
                continue
            if not isinstance(attempt_id, str) or not SAFE_ID_RE.fullmatch(attempt_id):
                continue
            result = _read(results / kind / path.name)
            if (
                isinstance(result, dict)
                and result.get("job_id") == job_id
                and result.get("attempt_id") == attempt_id
                and result.get("ok") is True
            ):
                continue
            row = dict(value)
            row["kind"] = value.get("kind") or kind
            out.append(row)
    return out


def _release_durable_claims(
    root: Path,
    claims: dict[str, dict[str, Any]],
    descriptors: list[dict[str, Any]],
    now: dt.datetime,
) -> set[str]:
    """Release current claims whose exact attempt has a durable immutable descriptor."""
    durable_attempts = {
        (str(item.get("job_id")), str(item.get("attempt_id")))
        for item in descriptors
    }
    submitted_jobs = {str(item.get("job_id")) for item in descriptors}
    for job_id, current in list(claims.items()):
        attempt_id = current.get("attempt_id")
        if (job_id, str(attempt_id)) not in durable_attempts:
            continue
        if current.get("released_at"):
            continue
        claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
        claim["released_at"] = _iso(now)
        claim["expires_at"] = _iso(now)
        _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
        claims[job_id] = dict(claim, active=False, expired=True)
    return submitted_jobs


def _normalize_legacy_scheduled_chat_leases(
    root: Path,
    claims: dict[str, dict[str, Any]],
    now: dt.datetime,
) -> tuple[int, int]:
    """Cap pre-migration Scheduled Chat leases at 90 minutes from last activity."""
    normalized = invalidated = 0
    for job_id, current in list(claims.items()):
        if current.get("worker_kind") != "scheduled_chat" or current.get("released_at"):
            continue
        last_activity = _as_time(current.get("heartbeat_at") or current.get("claimed_at"))
        expires = _as_time(current.get("expires_at"))
        if last_activity is None or expires is None:
            continue
        capped_expiry = last_activity + dt.timedelta(seconds=DEFAULT_LEASE_SECONDS)
        if expires <= capped_expiry:
            continue

        claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
        claim.setdefault("legacy_lease_original_expires_at", _iso(expires))
        claim["expires_at"] = _iso(capped_expiry)
        claim["legacy_lease_normalized_at"] = _iso(now)
        expired = now >= capped_expiry
        if expired:
            claim["lease_invalidated_at"] = _iso(now)
            claim["lease_invalidation_reason"] = (
                f"legacy scheduled_chat lease exceeded {DEFAULT_LEASE_SECONDS}-second cap"
            )
            invalidated += 1
        _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
        claims[job_id] = dict(claim, active=not expired, expired=expired)
        normalized += 1
    return normalized, invalidated


def _checkpoint_map(request: dict[str, Any]) -> dict[str, str]:
    return {
        str(item["job_id"]): str(item["checkpoint_ref"])
        for item in request.get("checkpointed_jobs", [])
        if isinstance(item, dict) and item.get("job_id") and item.get("checkpoint_ref")
    }


def _release_worker_checkpointed_claims(
    root: Path,
    claims: dict[str, dict[str, Any]],
    request: dict[str, Any],
    now: dt.datetime,
) -> int:
    """Release only this worker's active claims backed by its durable Library refs.

    This is deliberately worker-local: the queue job remains ready and no global
    completion state is inferred from an unverified Library reference.
    """
    checkpoints = _checkpoint_map(request)
    released = 0
    for job_id, checkpoint_ref in checkpoints.items():
        current = claims.get(job_id)
        if not current or not current.get("active"):
            continue
        if (
            current.get("worker_id") != request["worker_id"]
            or current.get("worker_kind") != request["worker_kind"]
        ):
            continue
        claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
        claim["released_at"] = _iso(now)
        claim["expires_at"] = _iso(now)
        claim["checkpoint_ref"] = checkpoint_ref
        claim["checkpoint_release_request_id"] = request["request_id"]
        _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
        claims[job_id] = dict(claim, active=False, expired=True)
        released += 1
    return released


def _worker_has_active_claim(
    claims: dict[str, dict[str, Any]],
    *,
    worker_id: str,
    worker_kind: str,
) -> bool:
    return any(
        current.get("active")
        and current.get("worker_id") == worker_id
        and current.get("worker_kind") == worker_kind
        for current in claims.values()
    )


def _assignment(job: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "job_id": claim["job_id"], "claim_id": claim["claim_id"],
        "worker_id": claim["worker_id"], "worker_kind": claim["worker_kind"],
        "attempt_id": claim["attempt_id"], "claimed_at": claim.get("claimed_at"),
        "expires_at": claim["expires_at"], "kind": claim.get("kind", job.get("type")),
        "depends_on_job_ids": list(claim.get("depends_on_job_ids") or [claim["job_id"]]),
        "job": dict(job),
    }


def _dependencies(job_id: str, job: dict[str, Any]) -> list[str] | None:
    values = job["depends_on_job_ids"] if "depends_on_job_ids" in job else job.get("dependencies")
    return claim_state.normalize_dependencies(job_id, values)


def _result_path(root: Path, request_id: str) -> Path:
    return root / ".survey/work-queue/claim-results" / f"{request_id}.json"


def _renew_existing_result(
    *,
    root: Path,
    path: Path,
    result_path: Path,
    existing: Any,
    claims: dict[str, dict[str, Any]],
    now: dt.datetime,
) -> int:
    """Treat a fresh authenticated replay of one request as a lease heartbeat."""
    if not isinstance(existing, dict):
        return 0
    raw = _read(path)
    try:
        request = _normalize_request(path, raw)
    except Exception:
        return 0
    if (
        existing.get("request_id") != request["request_id"]
        or existing.get("worker_id") != request["worker_id"]
        or existing.get("worker_kind") != request["worker_kind"]
    ):
        return 0

    heartbeat_requested_at = _as_time(request.get("requested_at"))
    if heartbeat_requested_at is None or heartbeat_requested_at > now:
        return 0

    assignments = existing.get("assignments")
    if not isinstance(assignments, list):
        return 0
    renewed = 0
    new_expiry = _iso(now + dt.timedelta(seconds=request["lease_seconds"]))
    for item in assignments:
        if not isinstance(item, dict):
            continue
        job_id = item.get("job_id")
        claim_id = item.get("claim_id")
        if not isinstance(job_id, str) or not isinstance(claim_id, str):
            continue
        current = claims.get(job_id)
        if not current or not current.get("active"):
            continue
        if (
            current.get("claim_id") != claim_id
            or current.get("request_id") != request["request_id"]
            or current.get("worker_id") != request["worker_id"]
            or current.get("worker_kind") != request["worker_kind"]
        ):
            continue
        last_activity = _as_time(current.get("heartbeat_at") or current.get("claimed_at"))
        if last_activity is not None and heartbeat_requested_at <= last_activity:
            continue
        claim = {key: value for key, value in current.items() if key not in {"active", "expired"}}
        claim["expires_at"] = new_expiry
        claim["heartbeat_at"] = _iso(now)
        _write(root / ".survey/work-queue/claims" / f"{job_id}.json", claim)
        claims[job_id] = dict(claim, active=True, expired=False)
        item["expires_at"] = new_expiry
        renewed += 1

    if renewed:
        existing["heartbeat_at"] = _iso(now)
        _write(result_path, existing)
    return renewed


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
    descriptors = _immutable_descriptors(root)
    submitted_jobs = _release_durable_claims(root, claims, descriptors, now)
    leases_normalized, leases_invalidated = _normalize_legacy_scheduled_chat_leases(root, claims, now)
    claims = claim_state.current_claims(root, now)
    processed = reused = errors = assigned = renewed = checkpoint_released = 0
    for path in sorted(request_root.glob("*.json")):
        result_path = _result_path(root, path.stem)
        if result_path.exists():
            reused += 1
            existing = _read(result_path, {})
            for item in existing.get("assignments", []) if isinstance(existing, dict) else []:
                if isinstance(item, dict):
                    assigned += 1
            renewed += _renew_existing_result(
                root=root,
                path=path,
                result_path=result_path,
                existing=existing,
                claims=claims,
                now=now,
            )
            continue
        raw = _read(path)
        try:
            request = _normalize_request(path, raw)
        except Exception as exc:
            errors += 1
            _write(result_path, {
                "schema_version": 1, "workflow_version": 10, "request_id": path.stem,
                "ok": False, "assignments": [], "error": str(exc), "processed_at": _iso(now),
            })
            processed += 1
            continue

        jobs = _job_files(root)
        by_id = {str(item["job_id"]): item for item in jobs}
        recovered = []
        for job_id, current in claims.items():
            if current.get("request_id") == request["request_id"] and job_id in by_id:
                recovered.append(_assignment(by_id[job_id], current))
        if recovered:
            _write(result_path, {
                "schema_version": 1, "workflow_version": 10, "request_id": request["request_id"],
                "worker_id": request["worker_id"], "worker_kind": request["worker_kind"],
                "ok": True, "assignments": recovered, "processed_at": _iso(now),
            })
            assigned += len(recovered)
            processed += 1
            continue

        released_now = _release_worker_checkpointed_claims(root, claims, request, now)
        checkpoint_released += released_now

        if request["worker_kind"] == "scheduled_chat" and _worker_has_active_claim(
            claims,
            worker_id=request["worker_id"],
            worker_kind=request["worker_kind"],
        ):
            _write(result_path, {
                "schema_version": 1, "workflow_version": 10, "request_id": request["request_id"],
                "worker_id": request["worker_id"], "worker_kind": request["worker_kind"],
                "ok": True, "assignments": [], "processed_at": _iso(now),
                "reason": "worker already has an active unsubmitted claim",
                "checkpoint_released": released_now,
            })
            processed += 1
            continue

        checkpointed_ids = set(_checkpoint_map(request))
        available = []
        for item in jobs:
            job_id = str(item.get("job_id") or "")
            if item.get("status") != "ready" or item.get("type") not in request["job_types"]:
                continue
            if job_id in submitted_jobs or job_id in checkpointed_ids:
                continue
            dependencies = _dependencies(job_id, item)
            if dependencies is None:
                continue
            current = claims.get(job_id)
            if current and current.get("active"):
                continue
            available.append(item)
        available.sort(key=lambda item: (-int(item.get("priority") or 0), str(item.get("created_at") or ""), str(item.get("job_id") or "")))
        assignments = []
        for item in available[:request["max_jobs"]]:
            job_id = str(item["job_id"])
            dependencies = _dependencies(job_id, item)
            if dependencies is None:
                continue
            claim_id = _claim_id(request["request_id"], job_id)
            attempt_id = _attempt_id(claim_id)
            previous = claims.get(job_id)
            expires = now + dt.timedelta(seconds=request["lease_seconds"])
            claim = {
                "schema_version": 1, "workflow_version": 10,
                "claim_id": claim_id, "job_id": job_id,
                "worker_id": request["worker_id"], "worker_kind": request["worker_kind"],
                "attempt_id": attempt_id, "request_id": request["request_id"],
                "claimed_at": _iso(now), "expires_at": _iso(expires),
                "kind": item.get("type"),
                "depends_on_job_ids": dependencies,
            }
            if previous and previous.get("claim_id") != claim_id:
                claim["previous_claim_id"] = previous.get("claim_id")
            _write(claims_root / f"{job_id}.json", claim)
            claims[job_id] = dict(claim, active=True, expired=False)
            assignments.append({
                "job_id": job_id, "claim_id": claim_id, "worker_id": request["worker_id"],
                "worker_kind": request["worker_kind"], "attempt_id": attempt_id,
                "claimed_at": _iso(now), "expires_at": _iso(expires), "kind": item.get("type"),
                "depends_on_job_ids": dependencies, "job": dict(item),
            })
        _write(result_path, {
            "schema_version": 1, "workflow_version": 10, "request_id": request["request_id"],
            "worker_id": request["worker_id"], "worker_kind": request["worker_kind"],
            "ok": True, "assignments": assignments, "processed_at": _iso(now),
            "checkpoint_released": released_now,
        })
        assigned += len(assignments)
        processed += 1
    return {
        "processed": processed,
        "reused": reused,
        "errors": errors,
        "assigned": assigned,
        "renewed": renewed,
        "checkpoint_released": checkpoint_released,
        "leases_normalized": leases_normalized,
        "leases_invalidated": leases_invalidated,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(process_requests(args.repo_root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
