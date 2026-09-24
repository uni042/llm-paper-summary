#!/usr/bin/env python3
"""Build deterministic Library fallback dispositions from canonical GitHub state.

The Library transport is outside GitHub Actions, so GitHub cannot move Library files
itself. This script publishes a derived manifest with three disjoint dispositions:

* acknowledgements: this exact fallback payload (or an explicit provenance rebound)
  produced the canonical publication and may move pending/ -> processed/;
* superseded: the same canonical job was successfully published by a different
  immutable attempt, so this old payload is no longer needed and may move
  pending/ -> superseded/;
* waiting: publication/recovery is still unresolved and the payload must remain pending.

Archive presence alone is never sufficient for either terminal disposition.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
QUEUE_REL = Path(".survey/work-queue")
TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent"}


def _read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def _relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _waiting(
    envelope: dict[str, Any],
    archive_path: Path,
    reason: str,
    *,
    detail: str | None = None,
) -> dict[str, Any]:
    row: dict[str, Any] = {
        "envelope_id": str(envelope.get("id") or archive_path.stem),
        "job_id": envelope.get("job_id"),
        "attempt_id": envelope.get("attempt_id"),
        "kind": envelope.get("kind"),
        "reason": reason,
    }
    if detail:
        row["detail"] = detail
    return row


def _paper_path(
    envelope: dict[str, Any],
    descriptor: dict[str, Any],
    job: dict[str, Any],
) -> str | None:
    for raw in (descriptor.get("paper_path"), envelope.get("paper_path"), job.get("paper_path")):
        if not isinstance(raw, str) or not raw:
            continue
        path = Path(raw)
        if path.is_absolute() or ".." in path.parts or not raw.startswith("papers/"):
            continue
        return path.as_posix()
    return None


def _ack_row(
    repo_root: Path,
    archive_path: Path,
    envelope: dict[str, Any],
    descriptor_path: Path,
    result_path: Path,
    job_path: Path,
    *,
    paper_path: str | None,
    published_attempt_id: str | None = None,
) -> dict[str, Any]:
    envelope_id = str(envelope["id"])
    row: dict[str, Any] = {
        "envelope_id": envelope_id,
        "job_id": envelope["job_id"],
        "attempt_id": envelope["attempt_id"],
        "kind": envelope["kind"],
        "status": "reflected",
        "pending_path": f"/LLM-survey-outbox/pending/{envelope_id}.json",
        "processed_path": f"/LLM-survey-outbox/processed/{envelope_id}.json",
        "archive_path": _relative(repo_root, archive_path),
        "submission_path": _relative(repo_root, descriptor_path),
        "result_path": _relative(repo_root, result_path),
        "job_path": _relative(repo_root, job_path),
    }
    if published_attempt_id is not None:
        row["published_attempt_id"] = published_attempt_id
        row["rebound"] = True
    if paper_path is not None:
        row["paper_path"] = paper_path
    return row


def _superseded_row(
    repo_root: Path,
    archive_path: Path,
    envelope: dict[str, Any],
    descriptor_path: Path,
    result_path: Path,
    job_path: Path,
    *,
    canonical_attempt_id: str,
    paper_path: str | None,
) -> dict[str, Any]:
    envelope_id = str(envelope["id"])
    row: dict[str, Any] = {
        "envelope_id": envelope_id,
        "job_id": envelope["job_id"],
        "attempt_id": envelope["attempt_id"],
        "kind": envelope["kind"],
        "status": "superseded",
        "reason": "job_published_by_different_attempt",
        "canonical_attempt_id": canonical_attempt_id,
        "pending_path": f"/LLM-survey-outbox/pending/{envelope_id}.json",
        "superseded_path": f"/LLM-survey-outbox/superseded/{envelope_id}.json",
        "archive_path": _relative(repo_root, archive_path),
        "canonical_submission_path": _relative(repo_root, descriptor_path),
        "canonical_result_path": _relative(repo_root, result_path),
        "job_path": _relative(repo_root, job_path),
    }
    if paper_path is not None:
        row["paper_path"] = paper_path
    return row


def _rebound_ack(
    repo_root: Path,
    archive_path: Path,
    envelope: dict[str, Any],
) -> dict[str, Any] | None:
    """Prove that this source payload was published through a newer rebound descriptor."""
    queue = repo_root / QUEUE_REL
    if envelope.get("kind") != "research":
        return None
    job_id = envelope.get("job_id")
    source_attempt = envelope.get("attempt_id")
    envelope_id = envelope.get("id")
    if not all(isinstance(value, str) and value for value in (job_id, source_attempt, envelope_id)):
        return None

    job_path = queue / "jobs" / f"{job_id}.json"
    job = _read_object(job_path)
    if not job or job.get("status") != "completed":
        return None
    submission = job.get("artifact_submission")
    if not isinstance(submission, str) or not submission.startswith(".survey/work-queue/submissions/research/"):
        return None
    descriptor_path = repo_root / submission
    descriptor = _read_object(descriptor_path)
    if not descriptor:
        return None
    published_attempt = descriptor.get("attempt_id")
    if not isinstance(published_attempt, str) or not published_attempt or published_attempt == source_attempt:
        return None
    if (
        descriptor.get("kind") != "research"
        or descriptor.get("job_id") != job_id
        or descriptor.get("source_fallback_envelope_id") != envelope_id
        or descriptor.get("source_attempt_id") != source_attempt
    ):
        return None

    result_path = queue / "results" / "research" / f"{published_attempt}.json"
    result = _read_object(result_path)
    if not result or result.get("ok") is not True:
        return None
    if (
        result.get("job_id") != job_id
        or result.get("attempt_id") != published_attempt
        or result.get("job_status") != "completed"
        or result.get("submission") != submission
    ):
        return None
    artifact = result.get("artifact")
    if not isinstance(artifact, dict):
        return None
    paper_path = _paper_path(envelope, descriptor, job)
    if paper_path is None or artifact.get("paper") != paper_path or not (repo_root / paper_path).is_file():
        return None
    return _ack_row(
        repo_root,
        archive_path,
        envelope,
        descriptor_path,
        result_path,
        job_path,
        paper_path=paper_path,
        published_attempt_id=published_attempt,
    )


def _superseded_disposition(
    repo_root: Path,
    archive_path: Path,
    envelope: dict[str, Any],
) -> dict[str, Any] | None:
    """Prove that another successful immutable attempt made this fallback obsolete."""
    queue = repo_root / QUEUE_REL
    job_id = envelope.get("job_id")
    source_attempt = envelope.get("attempt_id")
    kind = envelope.get("kind")
    if not all(isinstance(value, str) and value for value in (job_id, source_attempt, kind)):
        return None
    if kind not in {"research", "audit"}:
        return None

    job_path = queue / "jobs" / f"{job_id}.json"
    job = _read_object(job_path)
    if not job or job.get("job_id") != job_id:
        return None
    job_status = job.get("status")
    if job_status not in {"completed", "rejected"}:
        return None

    ownership_field = "artifact_submission" if job_status == "completed" else "status_submission"
    submission = job.get(ownership_field)
    expected_prefix = f".survey/work-queue/submissions/{kind}/"
    if not isinstance(submission, str) or not submission.startswith(expected_prefix):
        return None
    descriptor_path = repo_root / submission
    descriptor = _read_object(descriptor_path)
    if not descriptor:
        return None
    canonical_attempt = descriptor.get("attempt_id")
    if (
        not isinstance(canonical_attempt, str)
        or not canonical_attempt
        or canonical_attempt == source_attempt
        or descriptor.get("job_id") != job_id
        or descriptor.get("kind") != kind
    ):
        return None

    result_path = queue / "results" / kind / descriptor_path.name
    result = _read_object(result_path)
    if not result or result.get("ok") is not True:
        return None
    if (
        result.get("job_id") != job_id
        or result.get("attempt_id") != canonical_attempt
        or result.get("job_status") != job_status
        or result.get("submission") != submission
    ):
        return None

    paper_path: str | None = None
    if job_status == "completed":
        artifact = result.get("artifact")
        if not isinstance(artifact, dict):
            return None
        paper_path = _paper_path(envelope, descriptor, job)
        if paper_path is None or artifact.get("paper") != paper_path:
            return None
        if kind == "research" and not (repo_root / paper_path).is_file():
            return None

    return _superseded_row(
        repo_root,
        archive_path,
        envelope,
        descriptor_path,
        result_path,
        job_path,
        canonical_attempt_id=canonical_attempt,
        paper_path=paper_path,
    )


def _evaluate_archive(repo_root: Path, archive_path: Path) -> tuple[str, dict[str, Any]]:
    queue = repo_root / QUEUE_REL
    envelope = _read_object(archive_path)
    if envelope is None:
        return "waiting", _waiting({}, archive_path, "archive_invalid")

    envelope_id = envelope.get("id")
    job_id = envelope.get("job_id")
    attempt_id = envelope.get("attempt_id")
    kind = envelope.get("kind")
    if not all(isinstance(value, str) and value for value in (envelope_id, job_id, attempt_id, kind)):
        return "waiting", _waiting(envelope, archive_path, "archive_identity_incomplete")
    if kind not in {"research", "audit"}:
        return "waiting", _waiting(envelope, archive_path, "unsupported_kind")

    rebound = _rebound_ack(repo_root, archive_path, envelope)
    if rebound is not None:
        return "ack", rebound

    superseded = _superseded_disposition(repo_root, archive_path, envelope)
    if superseded is not None:
        return "superseded", superseded

    descriptor_path = queue / "submissions" / kind / f"{attempt_id}.json"
    descriptor = _read_object(descriptor_path)
    if descriptor is None:
        return "waiting", _waiting(envelope, archive_path, "descriptor_missing")
    if (
        descriptor.get("job_id") != job_id
        or descriptor.get("attempt_id") != attempt_id
        or descriptor.get("kind") != kind
    ):
        return "waiting", _waiting(envelope, archive_path, "descriptor_identity_mismatch")

    result_path = queue / "results" / kind / f"{attempt_id}.json"
    result = _read_object(result_path)
    if result is None:
        return "waiting", _waiting(envelope, archive_path, "result_missing")
    if result.get("job_id") != job_id or result.get("attempt_id") != attempt_id:
        return "waiting", _waiting(envelope, archive_path, "result_identity_mismatch")
    if result.get("ok") is not True:
        return "waiting", _waiting(envelope, archive_path, "result_not_successful")

    relative_submission = _relative(repo_root, descriptor_path)
    if result.get("submission") != relative_submission:
        return "waiting", _waiting(envelope, archive_path, "result_submission_mismatch")

    job_path = queue / "jobs" / f"{job_id}.json"
    job = _read_object(job_path)
    if job is None or job.get("job_id") != job_id:
        return "waiting", _waiting(envelope, archive_path, "job_missing")
    job_status = job.get("status")
    if job_status not in TERMINAL:
        return "waiting", _waiting(envelope, archive_path, "job_not_terminal")
    if result.get("job_status") != job_status:
        return "waiting", _waiting(envelope, archive_path, "result_job_status_mismatch")

    descriptor_status = descriptor.get("status", "completed")
    paper_path = _paper_path(envelope, descriptor, job)
    if descriptor_status == "completed":
        if job_status != "completed":
            return "waiting", _waiting(envelope, archive_path, "completed_attempt_job_not_completed")
        if job.get("artifact_submission") != relative_submission:
            return "waiting", _waiting(envelope, archive_path, "job_owned_by_different_submission")
        artifact = result.get("artifact")
        if not isinstance(artifact, dict):
            return "waiting", _waiting(envelope, archive_path, "result_artifact_missing")
        if paper_path is None or artifact.get("paper") != paper_path:
            return "waiting", _waiting(envelope, archive_path, "paper_identity_mismatch")
        if kind == "research" and not (repo_root / paper_path).is_file():
            return "waiting", _waiting(envelope, archive_path, "paper_missing")
    elif descriptor_status == "rejected":
        if job_status != "rejected" or job.get("status_submission") != relative_submission:
            return "waiting", _waiting(envelope, archive_path, "rejected_attempt_not_canonical")
    else:
        status_submission = job.get("status_submission")
        if status_submission != relative_submission:
            return "waiting", _waiting(envelope, archive_path, "terminal_status_owned_by_different_submission")

    return "ack", _ack_row(
        repo_root,
        archive_path,
        envelope,
        descriptor_path,
        result_path,
        job_path,
        paper_path=paper_path,
    )


def build_manifest(repo_root: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    archive_root = repo_root / QUEUE_REL / "fallback-archive"
    acknowledgements: list[dict[str, Any]] = []
    superseded: list[dict[str, Any]] = []
    waiting: list[dict[str, Any]] = []

    paths = sorted(archive_root.glob("*.json")) if archive_root.is_dir() else []
    for archive_path in paths:
        category, row = _evaluate_archive(repo_root, archive_path)
        if category == "ack":
            acknowledgements.append(row)
        elif category == "superseded":
            superseded.append(row)
        else:
            waiting.append(row)

    sort_key = lambda row: (str(row.get("envelope_id")), str(row.get("attempt_id")))
    acknowledgements.sort(key=sort_key)
    superseded.sort(key=sort_key)
    waiting.sort(key=sort_key)
    return {
        "schema_version": SCHEMA_VERSION,
        "source": "github-canonical-publication-state",
        "acknowledgements": acknowledgements,
        "superseded": superseded,
        "waiting": waiting,
    }


def write_manifest(repo_root: Path, output: Path | None = None) -> bool:
    repo_root = Path(repo_root).resolve()
    target = Path(output) if output is not None else repo_root / QUEUE_REL / "library-ack-manifest.json"
    if not target.is_absolute():
        target = repo_root / target
    target.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(build_manifest(repo_root), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if target.exists() and target.read_text(encoding="utf-8") == text:
        return False
    target.write_text(text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".survey/work-queue/library-ack-manifest.json"),
    )
    args = parser.parse_args()
    changed = write_manifest(args.repo_root, args.output)
    manifest = build_manifest(args.repo_root)
    print(
        json.dumps(
            {
                "changed": changed,
                "acknowledgements": len(manifest["acknowledgements"]),
                "superseded": len(manifest["superseded"]),
                "waiting": len(manifest["waiting"]),
                "output": str(args.output),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())