#!/usr/bin/env python3
"""Move provably settled fast-lane transport files out of hot queue directories.

Archival is conservative and best-effort. Unresolved, pending, retryable, malformed,
or identity-mismatched items remain in place. Git history plus archive paths preserve
auditability; canonical immutable submissions/results are never moved by this helper.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

TERMINAL = {"completed", "blocked", "deferred", "rejected"}


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(dt.timezone.utc)


def _same_identity(left: dict[str, Any], right: dict[str, Any], fields: tuple[str, ...]) -> bool:
    return all(left.get(field) == right.get(field) for field in fields)


def _move(source: Path, target: Path, *, apply: bool) -> tuple[bool, str]:
    if not apply:
        return True, "dry_run"
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        try:
            if target.read_bytes() == source.read_bytes():
                source.unlink()
                return True, "deduplicated"
        except OSError as exc:
            return False, f"archive compare failed: {exc}"
        return False, "archive target exists with different content"
    try:
        source.replace(target)
    except OSError as exc:
        return False, f"archive move failed: {exc}"
    return True, "moved"


def _canonical_descriptor(root: Path, attempt_id: str) -> tuple[str, Path, dict[str, Any]] | None:
    for kind in ("research", "audit"):
        path = root / ".survey/work-queue/submissions" / kind / f"{attempt_id}.json"
        value = _read(path, {})
        if isinstance(value, dict) and value.get("attempt_id") == attempt_id:
            return kind, path, value
    return None


def _archive_completed_requests(root: Path, *, apply: bool, out: dict[str, Any]) -> None:
    hot = root / ".survey/work-queue/completed-submission-requests"
    if not hot.is_dir():
        return
    archive = hot / "archive"
    for path in sorted(hot.glob("*.json")):
        request = _read(path, {})
        if not isinstance(request, dict):
            out["skipped"].append({"path": path.relative_to(root).as_posix(), "reason": "malformed"})
            continue
        attempt_id = str(request.get("attempt_id") or "")
        descriptor_info = _canonical_descriptor(root, attempt_id)
        if descriptor_info is None:
            out["skipped"].append({"path": path.relative_to(root).as_posix(), "reason": "descriptor_not_settled"})
            continue
        kind, _descriptor_path, descriptor = descriptor_info
        if kind != request.get("kind") or not _same_identity(request, descriptor, ("attempt_id", "job_id")):
            out["skipped"].append({"path": path.relative_to(root).as_posix(), "reason": "descriptor_identity_mismatch"})
            continue
        ok, reason = _move(path, archive / path.name, apply=apply)
        (out["archived"] if ok else out["errors"]).append({
            "path": path.relative_to(root).as_posix(), "kind": "completed_submission_request", "detail": reason
        })


def _archive_preflight(root: Path, *, apply: bool, result_retention_hours: float, out: dict[str, Any]) -> None:
    base = root / ".survey/work-queue/research-preflight"
    requests = base / "requests"
    results = base / "results"
    archive_requests = base / "archive" / "requests"
    archive_results = base / "archive" / "results"
    now = dt.datetime.now(dt.timezone.utc)

    if requests.is_dir():
        for request_path in sorted(requests.glob("*.json")):
            request = _read(request_path, {})
            result_path = results / request_path.name
            result = _read(result_path, {})
            if not isinstance(request, dict) or not isinstance(result, dict):
                out["skipped"].append({"path": request_path.relative_to(root).as_posix(), "reason": "preflight_unsettled"})
                continue
            if not _same_identity(request, result, ("request_id", "attempt_id", "job_id", "kind")):
                out["skipped"].append({"path": request_path.relative_to(root).as_posix(), "reason": "preflight_identity_mismatch"})
                continue
            ok, reason = _move(request_path, archive_requests / request_path.name, apply=apply)
            (out["archived"] if ok else out["errors"]).append({
                "path": request_path.relative_to(root).as_posix(), "kind": "preflight_request", "detail": reason
            })

    if not results.is_dir():
        return
    for result_path in sorted(results.glob("*.json")):
        result = _read(result_path, {})
        if not isinstance(result, dict):
            out["skipped"].append({"path": result_path.relative_to(root).as_posix(), "reason": "malformed_preflight_result"})
            continue
        if result.get("ok") is not True or result.get("preflight_passed") is not True:
            # Repair/failure results can be needed by a carry-over worker. Leave them hot.
            continue
        checked_at = _time(result.get("checked_at"))
        if checked_at is None or (now - checked_at).total_seconds() < result_retention_hours * 3600:
            continue
        attempt_id = str(result.get("attempt_id") or "")
        descriptor_info = _canonical_descriptor(root, attempt_id)
        if descriptor_info is None:
            out["skipped"].append({"path": result_path.relative_to(root).as_posix(), "reason": "passing_preflight_without_descriptor"})
            continue
        kind, _descriptor_path, descriptor = descriptor_info
        if kind != result.get("kind") or not _same_identity(result, descriptor, ("attempt_id", "job_id")):
            out["skipped"].append({"path": result_path.relative_to(root).as_posix(), "reason": "preflight_descriptor_identity_mismatch"})
            continue
        ok, reason = _move(result_path, archive_results / result_path.name, apply=apply)
        (out["archived"] if ok else out["errors"]).append({
            "path": result_path.relative_to(root).as_posix(), "kind": "preflight_result", "detail": reason
        })


def _archive_claim_requests(root: Path, *, apply: bool, out: dict[str, Any]) -> None:
    """Archive only requests with a durable matching allocator result.

    Claim results and claim records remain canonical durable facts, so active and
    carry-over attempt identity is never lost.
    """
    requests = root / ".survey/work-queue/claim-requests"
    results = root / ".survey/work-queue/claim-results"
    archive = requests / "archive"
    if not requests.is_dir():
        return
    for request_path in sorted(requests.glob("*.json")):
        request = _read(request_path, {})
        result = _read(results / request_path.name, {})
        if not isinstance(request, dict) or not isinstance(result, dict):
            continue
        if _time(result.get("processed_at")) is None:
            continue
        if not _same_identity(request, result, ("request_id", "worker_id")):
            out["skipped"].append({
                "path": request_path.relative_to(root).as_posix(),
                "reason": "claim_result_identity_mismatch",
            })
            continue
        ok, reason = _move(request_path, archive / request_path.name, apply=apply)
        (out["archived"] if ok else out["errors"]).append({
            "path": request_path.relative_to(root).as_posix(),
            "kind": "claim_request",
            "detail": reason,
        })


def _archive_run_state_requests(root: Path, *, apply: bool, out: dict[str, Any]) -> None:
    base = root / ".survey/work-queue/run-state"
    requests = base / "requests"
    results = base / "results"
    archive = base / "archive" / "requests"
    if not requests.is_dir():
        return
    fields = ("request_id", "run_key", "worker_id", "scheduled_slot", "actual_invocation_start")
    for request_path in sorted(requests.glob("*.json")):
        request = _read(request_path, {})
        result = _read(results / request_path.name, {})
        if not isinstance(request, dict) or not isinstance(result, dict) or result.get("ok") is not True:
            out["skipped"].append({"path": request_path.relative_to(root).as_posix(), "reason": "run_state_unsettled"})
            continue
        if not _same_identity(request, result, fields):
            out["skipped"].append({"path": request_path.relative_to(root).as_posix(), "reason": "run_state_identity_mismatch"})
            continue
        ok, reason = _move(request_path, archive / request_path.name, apply=apply)
        (out["archived"] if ok else out["errors"]).append({
            "path": request_path.relative_to(root).as_posix(), "kind": "run_state_request", "detail": reason
        })


def compact(root: Path, *, apply: bool, preflight_result_retention_hours: float = 2.0) -> dict[str, Any]:
    root = Path(root).resolve()
    out: dict[str, Any] = {
        "schema_version": 1,
        "ok": True,
        "mode": "apply" if apply else "dry_run",
        "archived": [],
        "skipped": [],
        "errors": [],
    }
    stages = (
        lambda: _archive_completed_requests(root, apply=apply, out=out),
        lambda: _archive_preflight(
            root,
            apply=apply,
            result_retention_hours=max(float(preflight_result_retention_hours), 0.0),
            out=out,
        ),
        lambda: _archive_claim_requests(root, apply=apply, out=out),
        lambda: _archive_run_state_requests(root, apply=apply, out=out),
    )
    for stage in stages:
        try:
            stage()
        except Exception as exc:
            # Compaction must never block paper processing.
            out["errors"].append({"path": None, "kind": "stage", "detail": f"{type(exc).__name__}: {exc}"})
    out["ok"] = not out["errors"]
    out["archived_count"] = len(out["archived"])
    out["error_count"] = len(out["errors"])
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--preflight-result-retention-hours", type=float, default=2.0)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = compact(
        args.repo_root,
        apply=args.apply,
        preflight_result_retention_hours=args.preflight_result_retention_hours,
    )
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        path = args.report if args.report.is_absolute() else args.repo_root.resolve() / args.report
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(text, end="")
    # Best-effort by contract: errors are reported but do not fail the caller.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
