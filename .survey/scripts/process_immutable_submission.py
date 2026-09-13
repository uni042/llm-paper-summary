#!/usr/bin/env python3
"""Process exactly one immutable workflow-v10 research/audit submission."""
from __future__ import annotations

import argparse
import hashlib
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
    """Render one validated descriptor from its exact committed slot blobs."""
    import assemble_research_record as assemble

    record: dict[str, Any] = {}
    total_bytes = 0
    for ref in descriptor["record_slots"]:
        slot = str(ref["slot"])
        payload = immutable_submission.read_record_slot(repo_root, ref)
        raw_size = len(json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        limit = assemble.MAX_SLOT_BYTES[slot]
        if raw_size > limit:
            raise ValueError(f"record slot too large: {ref['path']} ({raw_size} bytes > {limit})")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ValueError(f"{ref['path']} data must be an object")
        record[slot] = data
        total_bytes += raw_size

    record = assemble.normalize_preferred_terms(record)
    assemble.ensure_explanatory_summary(record)
    assemble.validate_record(record, collect_all=True)
    markdown = assemble.render_paper(record)
    if len(markdown.strip()) < 500:
        raise ValueError("rendered research artifact is unexpectedly short")
    return markdown


def _verify_claim(repo_root: Path, descriptor: dict[str, Any]) -> bool:
    """Validate a surviving claim record and report whether one was available."""
    claim_path = repo_root / ".survey/work-queue/claims" / f"{descriptor['job_id']}.json"
    claim = _read(claim_path, {}) or {}
    if not claim:
        # Fallback/recovery payloads may arrive after the lease file has been GC'd.
        return False
    if claim.get("lease_invalidated_at"):
        raise ValueError("stale attempt: claim lease was invalidated before durable submission")
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
    return True


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
    """Reuse only successful matching results; matching failures remain retryable."""
    result = _read(result_path, {}) or {}
    if immutable_submission.result_matches_identity(result, descriptor):
        return result if immutable_submission.result_is_success_for(result, descriptor) else None
    if result_path.exists() and result:
        raise ValueError("immutable result path already contains a conflicting attempt/job")
    return None


def _clear_repair_state(job: dict[str, Any]) -> None:
    """Clear validation-isolation metadata after a successful retry."""
    job.pop("repair_required", None)
    job.pop("validation_error", None)
    job.pop("validation_errors", None)
    job.pop("last_validation_failed_at", None)


def _success_result(
    descriptor: dict[str, Any],
    relative_submission: str,
    *,
    job_status: str | None,
    artifact: dict[str, Any] | None,
    reconciled: bool = False,
) -> dict[str, Any]:
    result = {
        "schema_version": 1,
        "workflow_version": 10,
        "ok": True,
        "attempt_id": descriptor["attempt_id"],
        "job_id": descriptor["job_id"],
        "job_type": descriptor["kind"],
        "job_status": job_status,
        "artifact": artifact,
        "submission": relative_submission,
        "processed_at": _now(),
    }
    if reconciled:
        result["reconciled"] = True
    return result


def _empty_effect_state() -> dict[str, Any]:
    return {
        "stats": {
            "research_completed": 0,
            "audit_completed": 0,
            "rejected": 0,
        },
        "maintenance": {"views_dirty": False},
    }


def _effect_payload(descriptor: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    stats = state.get("stats") if isinstance(state.get("stats"), dict) else {}
    maintenance = state.get("maintenance") if isinstance(state.get("maintenance"), dict) else {}
    return {
        "schema_version": 1,
        "job_id": descriptor["job_id"],
        "attempt_id": descriptor["attempt_id"],
        "research_completed": int(stats.get("research_completed", 0) or 0),
        "audit_completed": int(stats.get("audit_completed", 0) or 0),
        "rejected": int(stats.get("rejected", 0) or 0),
        "views_dirty": bool(maintenance.get("views_dirty", False)),
    }


def _reconciled_effect_state(descriptor: dict[str, Any]) -> dict[str, Any]:
    """Reconstruct effects when a prior local mutation reached terminal state before result write."""
    state = _empty_effect_state()
    status = descriptor.get("status", "completed")
    if status == "completed":
        if descriptor["kind"] == "research":
            state["stats"]["research_completed"] = 1
        else:
            state["stats"]["audit_completed"] = 1
        state["maintenance"]["views_dirty"] = True
    elif status == "rejected" and descriptor["kind"] == "research":
        state["stats"]["rejected"] = 1
    return state


def _write_effect(path: Path | None, descriptor: dict[str, Any], state: dict[str, Any]) -> None:
    if path is None:
        return
    queue_worker.write_json(Path(path), _effect_payload(descriptor, state))


def _record_unidentified_failure(
    repo_root: Path,
    submission_path: Path,
    exc: Exception,
) -> dict[str, Any] | None:
    """Persist a path+digest tombstone when attempt/job identity cannot be trusted."""
    try:
        raw_bytes = submission_path.read_bytes()
    except OSError:
        return None

    relative_submission = submission_path.relative_to(repo_root).as_posix()
    digest = hashlib.sha256(raw_bytes).hexdigest()
    result_path = immutable_submission.result_path_for(repo_root, submission_path)
    existing = _read(result_path, {}) or {}
    if existing:
        if (
            existing.get("submission") == relative_submission
            and existing.get("descriptor_sha256") == digest
        ):
            return existing
        raise ValueError("immutable result path already contains a conflicting unidentified descriptor")

    result = {
        "schema_version": 1,
        "workflow_version": 10,
        "ok": False,
        "attempt_id": None,
        "job_id": None,
        "job_type": submission_path.parent.name,
        "job_status": None,
        "artifact": None,
        "submission": relative_submission,
        "descriptor_sha256": digest,
        "error": f"{type(exc).__name__}: {exc}",
        "processed_at": _now(),
    }
    queue_worker.write_json(result_path, result)
    return result


def record_failure(repo_root: Path, submission_path: Path, exc: Exception) -> dict[str, Any] | None:
    """Persist durable processor failure state for one immutable submission."""
    repo_root = Path(repo_root).resolve()
    try:
        submission_path = _descriptor_path(repo_root, submission_path)
    except Exception:
        return None

    try:
        raw = immutable_submission.load_descriptor(submission_path)
    except Exception:
        return _record_unidentified_failure(repo_root, submission_path, exc)

    attempt_id = raw.get("attempt_id")
    job_id = raw.get("job_id")
    kind = raw.get("kind") or submission_path.parent.name
    if not isinstance(attempt_id, str) or not attempt_id:
        return _record_unidentified_failure(repo_root, submission_path, exc)
    if not isinstance(job_id, str) or not job_id:
        return _record_unidentified_failure(repo_root, submission_path, exc)
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
    validation_errors = list(getattr(exc, "issues", []) or [])
    if validation_errors:
        result["validation_errors"] = validation_errors
    queue_worker.write_json(result_path, result)
    return result


def process(
    repo_root: Path,
    submission_path: Path,
    *,
    defer_shared_state: bool = False,
    effect_path: Path | None = None,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    if defer_shared_state and effect_path is None:
        raise ValueError("effect_path is required when defer_shared_state is enabled")

    submission_path = _descriptor_path(repo_root, submission_path)
    raw = immutable_submission.load_descriptor(submission_path)
    descriptor = immutable_submission.validate_descriptor(repo_root, raw)
    relative_submission = submission_path.relative_to(repo_root).as_posix()
    result_path = immutable_submission.result_path_for(repo_root, submission_path)

    existing = _matching_result(result_path, descriptor)
    if existing is not None:
        if defer_shared_state:
            _write_effect(effect_path, descriptor, _empty_effect_state())
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

    claim_verified = _verify_claim(repo_root, descriptor)
    status = descriptor.get("status", "completed")

    if job.get("status") in queue_worker.TERMINAL:
        if status == "completed" and job.get("artifact_submission") == relative_submission:
            result = _success_result(
                descriptor,
                relative_submission,
                job_status=job.get("status"),
                artifact={"paper": descriptor["paper_path"]},
                reconciled=True,
            )
            queue_worker.write_json(result_path, result)
            if defer_shared_state:
                _write_effect(effect_path, descriptor, _reconciled_effect_state(descriptor))
            return result
        if (
            status == "rejected"
            and job.get("status") == "rejected"
            and (claim_verified or job.get("status_submission") == relative_submission)
        ):
            if job.get("status_submission") != relative_submission:
                job["status_submission"] = relative_submission
                queue_worker.write_json(job_path, job)
            result = _success_result(
                descriptor,
                relative_submission,
                job_status="rejected",
                artifact=None,
                reconciled=True,
            )
            queue_worker.write_json(result_path, result)
            if defer_shared_state:
                _write_effect(effect_path, descriptor, _reconciled_effect_state(descriptor))
            return result
        raise ValueError(f"job already terminal under a different attempt: {job.get('status')}")

    sub = dict(descriptor)
    sub["_file"] = relative_submission
    sub["status"] = status
    if status == "completed":
        _precheck_paper(repo_root, descriptor)
        sub["content"] = render_descriptor(repo_root, descriptor)

    st = _empty_effect_state() if defer_shared_state else queue_worker.load_state()
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
    else:
        mutable_job["status_submission"] = relative_submission

    queue_worker.update_job(mutable_job)
    if defer_shared_state:
        _write_effect(effect_path, descriptor, st)
    else:
        queue_worker.save_state(st)
        _refresh_snapshot(repo_root)

    final_job = _read(job_path, {}) or {}
    result = _success_result(
        descriptor,
        relative_submission,
        job_status=final_job.get("status"),
        artifact=artifact,
    )
    queue_worker.write_json(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--submission", type=Path, required=True)
    parser.add_argument("--defer-shared-state", action="store_true")
    parser.add_argument("--effect-file", type=Path)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    try:
        result = process(
            repo_root,
            args.submission,
            defer_shared_state=args.defer_shared_state,
            effect_path=args.effect_file,
        )
    except Exception as exc:
        if args.defer_shared_state and args.effect_file is not None:
            args.effect_file.unlink(missing_ok=True)
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
