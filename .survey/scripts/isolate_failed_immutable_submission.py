#!/usr/bin/env python3
"""Reopen only a job whose immutable structured record fails content validation.

This helper is intentionally conservative. It first verifies the immutable descriptor,
claim ownership, and existing-paper blob guard. Only after those transport/state checks
pass does it run the same renderer/validator used by publication. If that renderer fails,
the owning job is reopened with repair_required metadata; stale claims, blob races, and
other transport failures are left untouched.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import immutable_submission  # noqa: E402
import process_immutable_submission as processor  # noqa: E402


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def isolate(repo_root: Path, submission: Path) -> dict:
    repo_root = repo_root.resolve()
    submission = processor._descriptor_path(repo_root, submission)
    raw = immutable_submission.load_descriptor(submission)

    try:
        descriptor = immutable_submission.validate_descriptor(repo_root, raw)
        processor._configure_queue_worker(repo_root)
        processor._verify_claim(repo_root, descriptor)
        processor._precheck_paper(repo_root, descriptor)
    except Exception as exc:
        return {
            "isolated": False,
            "reason": "transport_or_state_failure",
            "error": f"{type(exc).__name__}: {exc}",
        }

    try:
        processor.render_descriptor(repo_root, descriptor)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        job_path = repo_root / ".survey/work-queue/jobs" / f"{descriptor['job_id']}.json"
        try:
            job = json.loads(job_path.read_text(encoding="utf-8"))
        except Exception as job_exc:
            return {
                "isolated": False,
                "reason": "job_unavailable",
                "error": f"{type(job_exc).__name__}: {job_exc}",
                "validation_error": error,
            }
        if not isinstance(job, dict):
            return {"isolated": False, "reason": "job_not_object", "validation_error": error}

        job["status"] = "ready"
        job.pop("completed_at", None)
        job.pop("artifact_submission", None)
        job["repair_required"] = True
        job["validation_error"] = error
        job["last_validation_failed_at"] = _now()
        _write(job_path, job)
        return {
            "isolated": True,
            "job_id": descriptor["job_id"],
            "attempt_id": descriptor["attempt_id"],
            "validation_error": error,
        }

    return {
        "isolated": False,
        "reason": "record_validation_passed",
        "job_id": descriptor["job_id"],
        "attempt_id": descriptor["attempt_id"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--submission", type=Path, required=True)
    args = parser.parse_args()
    result = isolate(args.repo_root, args.submission)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
