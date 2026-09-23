#!/usr/bin/env python3
"""Archive settled worker transport artifacts out of hot queue directories.

Archival is conservative and best-effort. Immutable research/audit descriptors and
their canonical submission results are never moved by this helper.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path
from typing import Any

HOT = Path(".survey/work-queue")
ARCHIVE = HOT / "archive" / "transport"


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str):
        return None
    try:
        out = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if out.tzinfo is None:
        return None
    return out.astimezone(dt.timezone.utc)


def _old_enough(value: Any, now: dt.datetime, seconds: int) -> bool:
    parsed = _time(value)
    return parsed is not None and (now - parsed).total_seconds() >= seconds


def _move(root: Path, source: Path, relative_archive: Path, apply: bool) -> tuple[bool, str]:
    target = root / ARCHIVE / relative_archive
    if target.exists():
        if target.read_bytes() != source.read_bytes():
            return False, "archive_conflict"
        if apply:
            source.unlink()
        return True, "deduplicated"
    if apply:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
    return True, "archived"


def _matching_descriptor(root: Path, request: dict[str, Any]) -> Path | None:
    kind = request.get("kind")
    attempt_id = request.get("attempt_id")
    job_id = request.get("job_id")
    if kind not in {"research", "audit"} or not isinstance(attempt_id, str) or not attempt_id:
        return None
    path = root / HOT / "submissions" / kind / f"{attempt_id}.json"
    descriptor = _read(path, {})
    if not isinstance(descriptor, dict):
        return None
    if descriptor.get("attempt_id") != attempt_id or descriptor.get("job_id") != job_id or descriptor.get("kind") != kind:
        return None
    return path


def compact_completed_requests(root: Path, apply: bool) -> tuple[list[str], list[dict[str, str]]]:
    moved, skipped = [], []
    folder = root / HOT / "completed-submission-requests"
    if not folder.is_dir():
        return moved, skipped
    for path in sorted(folder.glob("*.json")):
        request = _read(path, {})
        if not isinstance(request, dict):
            skipped.append({"path": path.relative_to(root).as_posix(), "reason": "malformed"})
            continue
        descriptor = _matching_descriptor(root, request)
        preflight_path = root / str(request.get("preflight_result") or "")
        preflight = _read(preflight_path, {})
        if descriptor is None or not isinstance(preflight, dict):
            skipped.append({"path": path.relative_to(root).as_posix(), "reason": "unsettled"})
            continue
        if not (
            preflight.get("ok") is True
            and preflight.get("preflight_passed") is True
            and preflight.get("attempt_id") == request.get("attempt_id")
            and preflight.get("job_id") == request.get("job_id")
            and preflight.get("kind") == request.get("kind")
        ):
            skipped.append({"path": path.relative_to(root).as_posix(), "reason": "identity_or_preflight_mismatch"})
            continue
        ok, reason = _move(root, path, Path("completed-submission-requests") / path.name, apply)
        if ok:
            moved.append(path.relative_to(root).as_posix())
        else:
            skipped.append({"path": path.relative_to(root).as_posix(), "reason": reason})
    return moved, skipped


def compact_preflight(root: Path, apply: bool, min_age_seconds: int, now: dt.datetime) -> tuple[list[str], list[dict[str, str]]]:
    moved, skipped = [], []
    req_root = root / HOT / "research-preflight" / "requests"
    res_root = root / HOT / "research-preflight" / "results"
    if not req_root.is_dir():
        return moved, skipped
    for request_path in sorted(req_root.glob("*.json")):
        result_path = res_root / request_path.name
        request = _read(request_path, {})
        result = _read(result_path, {})
        if not isinstance(request, dict) or not isinstance(result, dict):
            continue
        if result.get("request_id") != request_path.stem or request.get("request_id") != request_path.stem:
            continue
        if result.get("repair_required") is True or result.get("ok") is not True or result.get("preflight_passed") is not True:
            continue
        descriptor = _matching_descriptor(root, result)
        if descriptor is None:
            continue
        if not _old_enough(result.get("checked_at"), now, min_age_seconds):
            continue
        pairs = [
            (request_path, Path("research-preflight/requests") / request_path.name),
            (result_path, Path("research-preflight/results") / result_path.name),
        ]
        if any((root / ARCHIVE / rel).exists() and (root / ARCHIVE / rel).read_bytes() != src.read_bytes() for src, rel in pairs):
            skipped.append({"path": request_path.relative_to(root).as_posix(), "reason": "archive_conflict"})
            continue
        for source, rel in pairs:
            ok, reason = _move(root, source, rel, apply)
            if ok:
                moved.append(source.relative_to(root).as_posix())
            else:
                skipped.append({"path": source.relative_to(root).as_posix(), "reason": reason})
    return moved, skipped


def _claim_assignment_settled(root: Path, assignment: dict[str, Any]) -> bool:
    job_id = str(assignment.get("job_id") or "")
    attempt_id = str(assignment.get("attempt_id") or "")
    kind = str(assignment.get("kind") or assignment.get("job_type") or "")
    if not job_id:
        return False
    job = _read(root / HOT / "jobs" / f"{job_id}.json", {})
    if isinstance(job, dict) and str(job.get("status") or "").lower() in {"completed", "blocked", "deferred", "rejected"}:
        return True
    if kind not in {"research", "audit"} or not attempt_id:
        return False
    descriptor_path = root / HOT / "submissions" / kind / f"{attempt_id}.json"
    descriptor = _read(descriptor_path, {})
    if not isinstance(descriptor, dict) or descriptor.get("attempt_id") != attempt_id or descriptor.get("job_id") != job_id:
        return False
    result = _read(root / HOT / "results" / kind / descriptor_path.name, {})
    if not isinstance(result, dict) or result.get("attempt_id") != attempt_id or result.get("job_id") != job_id:
        return False
    if result.get("ok") is False and result.get("retryable") is True:
        return False
    return str(result.get("job_status") or "").lower() in {"completed", "blocked", "deferred", "rejected"}


def compact_claim_transport(root: Path, apply: bool, min_age_seconds: int, now: dt.datetime) -> tuple[list[str], list[dict[str, str]]]:
    moved, skipped = [], []
    req_root = root / HOT / "claim-requests"
    res_root = root / HOT / "claim-results"
    if not req_root.is_dir():
        return moved, skipped
    for request_path in sorted(req_root.glob("*.json")):
        result_path = res_root / request_path.name
        request = _read(request_path, {})
        result = _read(result_path, {})
        if not isinstance(request, dict) or not isinstance(result, dict):
            continue
        if request.get("request_id") != request_path.stem or result.get("request_id") not in {None, request_path.stem}:
            continue
        if not _old_enough(result.get("processed_at"), now, min_age_seconds):
            continue
        assignments = result.get("assignments")
        if not isinstance(assignments, list):
            continue
        if any(not isinstance(item, dict) or not _claim_assignment_settled(root, item) for item in assignments):
            skipped.append({"path": request_path.relative_to(root).as_posix(), "reason": "claim_assignment_not_terminal"})
            continue
        pairs = [
            (request_path, Path("claim-requests") / request_path.name),
            (result_path, Path("claim-results") / result_path.name),
        ]
        if any((root / ARCHIVE / rel).exists() and (root / ARCHIVE / rel).read_bytes() != src.read_bytes() for src, rel in pairs):
            skipped.append({"path": request_path.relative_to(root).as_posix(), "reason": "archive_conflict"})
            continue
        for source, rel in pairs:
            ok, reason = _move(root, source, rel, apply)
            if ok:
                moved.append(source.relative_to(root).as_posix())
            else:
                skipped.append({"path": source.relative_to(root).as_posix(), "reason": reason})
    return moved, skipped


def compact_run_state(root: Path, apply: bool, min_age_seconds: int, now: dt.datetime) -> tuple[list[str], list[dict[str, str]]]:
    moved, skipped = [], []
    req_root = root / HOT / "run-state" / "requests"
    res_root = root / HOT / "run-state" / "results"
    latest_root = root / HOT / "run-state" / "latest"
    protected = set()
    if latest_root.is_dir():
        for path in latest_root.glob("*.json"):
            value = _read(path, {})
            if isinstance(value, dict) and isinstance(value.get("result_path"), str):
                protected.add(value["result_path"])
    if not req_root.is_dir():
        return moved, skipped
    for request_path in sorted(req_root.glob("*.json")):
        result_path = res_root / request_path.name
        result_rel = result_path.relative_to(root).as_posix()
        request = _read(request_path, {})
        result = _read(result_path, {})
        if result_rel in protected or not isinstance(request, dict) or not isinstance(result, dict):
            continue
        if not (
            request.get("request_id") == request_path.stem
            and result.get("request_id") == request_path.stem
            and result.get("run_key") == request.get("run_key")
            and result.get("worker_id") == request.get("worker_id")
            and result.get("ok") is True
        ):
            continue
        if not _old_enough(result.get("processed_at"), now, min_age_seconds):
            continue
        pairs = [
            (request_path, Path("run-state/requests") / request_path.name),
            (result_path, Path("run-state/results") / result_path.name),
        ]
        if any((root / ARCHIVE / rel).exists() and (root / ARCHIVE / rel).read_bytes() != src.read_bytes() for src, rel in pairs):
            skipped.append({"path": request_path.relative_to(root).as_posix(), "reason": "archive_conflict"})
            continue
        for source, rel in pairs:
            ok, reason = _move(root, source, rel, apply)
            if ok:
                moved.append(source.relative_to(root).as_posix())
            else:
                skipped.append({"path": source.relative_to(root).as_posix(), "reason": reason})
    return moved, skipped


def compact(root: Path, *, apply: bool, min_age_seconds: int = 7200) -> dict[str, Any]:
    root = root.resolve()
    now = dt.datetime.now(dt.timezone.utc)
    moved: list[str] = []
    skipped: list[dict[str, str]] = []
    for fn, args in (
        (compact_completed_requests, (root, apply)),
        (compact_claim_transport, (root, apply, min_age_seconds, now)),
        (compact_preflight, (root, apply, min_age_seconds, now)),
        (compact_run_state, (root, apply, min_age_seconds, now)),
    ):
        batch_moved, batch_skipped = fn(*args)
        moved.extend(batch_moved)
        skipped.extend(batch_skipped)
    return {
        "schema_version": 1,
        "ok": True,
        "mode": "apply" if apply else "dry_run",
        "min_age_seconds": min_age_seconds,
        "moved_count": len(moved),
        "moved": sorted(moved),
        "skipped": skipped,
        "rule": "Only identity-verified settled transport artifacts are archived. Retryable, repair-required, unresolved, active immutable submissions/results are never moved.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--min-age-seconds", type=int, default=7200)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    result = compact(args.repo_root, apply=args.apply, min_age_seconds=max(args.min_age_seconds, 0))
    text = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.report:
        path = args.report if args.report.is_absolute() else args.repo_root.resolve() / args.report
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
