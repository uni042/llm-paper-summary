#!/usr/bin/env python3
"""Process exactly one immutable workflow-v10 research/audit submission."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import immutable_submission  # noqa: E402
import queue_worker  # noqa: E402


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _configure_queue_worker(repo_root: Path) -> None:
    root = repo_root / ".survey"
    queue_worker.ROOT = root
    queue_worker.QUEUE = root / "work-queue"
    queue_worker.JOBS = queue_worker.QUEUE / "jobs"
    queue_worker.SUBMISSIONS = queue_worker.QUEUE / "submissions"
    queue_worker.RESULTS = queue_worker.QUEUE / "results"
    queue_worker.STATE = queue_worker.QUEUE / "state.json"
    queue_worker.ARCHIVE = queue_worker.QUEUE / "archive"
    queue_worker.DISCOVERY_STATE = queue_worker.QUEUE / "discovery-state.json"


def _descriptor_path(repo_root: Path, path: Path) -> Path:
    path = Path(path)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve()
    try:
        relative = path.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("submission path must stay within repository") from exc
    parts = relative.parts
    if len(parts) != 5 or parts[:3] != (".survey", "work-queue", "submissions"):
        raise ValueError("submission must be directly under submissions/research or submissions/audit")
    if parts[3] not in {"research", "audit"} or path.suffix != ".json":
        raise ValueError("submission must be a research/audit JSON descriptor")
    return path


def render_descriptor(repo_root: Path, descriptor: dict[str, Any]) -> str:
    """Render one validated descriptor without mutating the reusable chat inbox."""
    import assemble_research_record as assemble

    record: dict[str, Any] = {}
    total_bytes = 0
    for ref in descriptor["record_slots"]:
        slot = str(ref["slot"])
        path = repo_root / str(ref["path"])
        raw = path.read_bytes()
        limit = assemble.MAX_SLOT_BYTES[slot]
        if len(raw) > limit:
            raise ValueError(f"record slot too large: {ref['path']} ({len(raw)} bytes > {limit})")
        payload = json.loads(raw.decode("utf-8"))
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ValueError(f"{ref['path']} data must be an object")
        record[slot] = data
        total_bytes += len(raw)

    record = assemble.normalize_preferred_terms(record)
    assemble.ensure_explanatory_summary(record)
    assemble.validate_record(record)
    markdown = assemble.render_paper(record)
    if len(markdown.strip()) < 500:
        raise ValueError("rendered research artifact is unexpectedly short")
    return markdown


def _verify_claim(repo_root: Path, descriptor: dict[str, Any]) -> None:
    claim_path = repo_root / ".survey/work-queue/claims" / f"{descriptor['job_id']}.json"
    claim = _read(claim_path, {}) or {}
    if not claim:
        # Fallback/recovery payloads may arrive after the lease file has been GC'd.
        return
    current_attempt = claim.get("attempt_id")
    if current_attempt and current_attempt != descriptor["attempt_id"]:
        raise ValueError(
            f"stale attempt: current claim uses {current_attempt}, descriptor uses {descriptor['attempt_id']}"
        )
    descriptor_claim = descriptor.get("claim_id")
    if descriptor_claim and claim.get("claim_id") and descriptor_claim != claim.get("claim_id"):
        raise ValueError("stale attempt: descriptor claim_id no longer matches current claim")
    descriptor_worker = descriptor.get("worker_id")
    if descriptor_worker and claim.get("worker_id") and descriptor_worker != claim.get("worker_id"):
        raise ValueError("stale attempt: descriptor worker_id no longer owns current claim")


def _precheck_paper(repo_root: Path, descriptor: dict[str, Any]) -> None:
    paper = repo_root / descriptor["paper_path"]
    expected = descriptor.get("expected_blob_sha")
    if not paper.exists():
        return
    if not expected:
        raise ValueError("expected_blob_sha is required when updating an existing paper")
    current = immutable_submission.git_blob_sha(paper.read_bytes())
    if current != expected:
        raise ValueError(f"paper blob changed: expected {expected}, current {current}")


def _refresh_snapshot(repo_root: Path) -> None:
    snap = queue_worker.queue_snapshot()
    path = repo_root / ".survey/work-queue/next-jobs.json"
    old = _read(path, {}) or {}
    old_cmp = dict(old)
    old_cmp.pop("generated_at", None)
    if old_cmp == snap:
        snap["generated_at"] = old.get("generated_at", queue_worker.now())
    else:
        snap["generated_at"] = queue_worker.now()
    queue_worker.write_json(path, snap)


def _matching_result(result_path: Path, descriptor: dict[str, Any]) -> dict[str, Any] | None:
    result = _read(result_path, {}) or {}
    if (
        result.get("attempt_id") == descriptor.get("attempt_id")
        and result.get("job_id") == descriptor.get("job_id")
    ):
        return result
    if result_path.exists() and result:
        raise ValueError("immutable result path already contains a conflicting attempt/job")
    return None


def _clear_repair_state(job: dict[str, Any]) -> None:
    """Clear validation-isolation metadata after a successful retry."""
    job.pop("repair_required", None)
    job.pop("validation_error", None)
    job.pop("last_validation_failed_at", None)


def record_failure(repo_root: Path, submission_path: Path, exc: Exception) -> dict[str, Any] | None:
    """Persist a terminal attempt result so invalid descriptors do not occupy a bank forever."""
    repo_root = Path(repo_root).resolve()
    try:
        submission_path = _descriptor_path(repo_root, submission_path)
        raw = immutable_submission.load_descriptor(submission_path)
    except Exception:
        return None

    attempt_id = raw.get("attempt_id")
    job_id = raw.get("job_id")
    kind = raw.get("kind") or submission_path.parent.name
    if not isinstance(attempt_id, str) or not attempt_id:
        return None
    if not isinstance(job_id, str) or not job_id:
        return None
    if kind not in {"research", "audit"}:
        kind = submission_path.parent.name

    result_path = immutable_submission.result_path_for(repo_root, submission_path)
    existing = _read(result_path, {}) or {}
    if existing:
        if existing.get("attempt_id") == attempt_id and existing.get("job_id") == job_id:
            return existing
        raise ValueError("immutable result path already contains a conflicting attempt/job")

    result = {
        "schema_version": 1,
        "workflow_version": 10,
        "ok": False,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "job_type": kind,
        "job_status": None,
        "artifact": None,
        "submission": submission_path.relative_to(repo_root).as_posix(),
        "error": f"{type(exc).__name__}: {exc}",
        "processed_at": _now(),
    }
    queue_worker.write_json(result_path, result)
    return result


def process(repo_root: Path, submission_path: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    submission_path = _descriptor_path(repo_root, submission_path)
    raw = immutable_submission.load_descriptor(submission_path)
    descriptor = immutable_submission.validate_descriptor(repo_root, raw)
    relative_submission = submission_path.relative_to(repo_root).as_posix()
    result_path = immutable_submission.result_path_for(repo_root, submission_path)

    existing = _matching_result(result_path, descriptor)
    if existing is not None:
        reused = dict(existing)
        reused["reused"] = True
        return reused

    _configure_queue_worker(repo_root)
    job_path = repo_root / ".survey/work-queue/jobs" / f"{descriptor['job_id']}.json"
    job = _read(job_path, {}) or {}
    if not job:
        raise ValueError(f"unknown job_id: {descriptor['job_id']}")
    if job.get("type") != descriptor["kind"]:
        raise ValueError(f"job type {job.get('type')} does not match descriptor kind {descriptor['kind']}")

    _verify_claim(repo_root, descriptor)

    if job.get("status") in queue_worker.TERMINAL:
        if job.get("artifact_submission") == relative_submission:
            result = {
                "schema_version": 1,
                "workflow_version": 10,
                "ok": True,
                "attempt_id": descriptor["attempt_id"],
                "job_id": descriptor["job_id"],
                "job_type": descriptor["kind"],
                "job_status": job.get("status"),
                "artifact": {"paper": descriptor["paper_path"]} if job.get("status") == "completed" else None,
                "submission": relative_submission,
                "reconciled": True,
                "processed_at": _now(),
            }
            queue_worker.write_json(result_path, result)
            return result
        raise ValueError(f"job already terminal under a different attempt: {job.get('status')}")

    sub = dict(descriptor)
    sub["_file"] = relative_submission
    status = descriptor.get("status", "completed")
    sub["status"] = status
    if status == "completed":
        _precheck_paper(repo_root, descriptor)
        sub["content"] = render_descriptor(repo_root, descriptor)

    st = queue_worker.load_state()
    mutable_job = dict(job)
    mutable_job["_path"] = job_path
    artifact = None
    if descriptor["kind"] == "research":
        if status == "completed":
            artifact = queue_worker.apply_artifact(sub, mutable_job)
        queue_worker.process_research(sub, mutable_job, st)
    else:
        if status == "completed":
            artifact = queue_worker.apply_artifact(sub, mutable_job)
        queue_worker.process_audit(sub, mutable_job, st)

    if status == "completed":
        _clear_repair_state(mutable_job)

    queue_worker.update_job(mutable_job)
    queue_worker.save_state(st)
    _refresh_snapshot(repo_root)

    final_job = _read(job_path, {}) or {}
    result = {
        "schema_version": 1,
        "workflow_version": 10,
        "ok": True,
        "attempt_id": descriptor["attempt_id"],
        "job_id": descriptor["job_id"],
        "job_type": descriptor["kind"],
        "job_status": final_job.get("status"),
        "artifact": artifact,
        "submission": relative_submission,
        "processed_at": _now(),
    }
    queue_worker.write_json(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--submission", type=Path, required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    try:
        result = process(repo_root, args.submission)
    except Exception as exc:
        result = record_failure(repo_root, args.submission, exc)
        if result is not None:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
