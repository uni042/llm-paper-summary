#!/usr/bin/env python3
"""Classify and isolate one failed immutable structured-record submission.

Content validation failures reopen the owning job for a new repaired attempt. Guard or
state failures are not replayed automatically. Failures that occur only after the exact
record has passed descriptor/claim/blob guards and content rendering are safe to retry
with the same immutable job+attempt, up to a bounded recovery budget.
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

MAX_AUTO_RECOVERY_FAILURES = 3


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _persist_failure_classification(
    repo_root: Path,
    submission: Path,
    descriptor: dict,
    *,
    failure_class: str,
    retryable: bool,
) -> dict | None:
    """Annotate only the exact durable failure result for this immutable attempt."""
    result_path = immutable_submission.result_path_for(repo_root, submission)
    try:
        result = json.loads(result_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(result, dict) or result.get("ok") is not False:
        return None
    if not immutable_submission.result_matches_identity(result, descriptor):
        return None

    result["failure_class"] = failure_class
    result["retryable"] = bool(retryable)
    if retryable:
        previous = result.get("recovery_failures", 0)
        if isinstance(previous, bool) or not isinstance(previous, int) or previous < 0:
            previous = 0
        failures = previous + 1
        result["recovery_failures"] = failures
        result["last_recovery_failed_at"] = _now()
        if failures >= MAX_AUTO_RECOVERY_FAILURES:
            result["retryable"] = False
            result["failure_class"] = "recovery_exhausted"
            result["last_retryable_failure_class"] = failure_class
    _write(result_path, result)
    return result


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
        try:
            descriptor_for_result = raw if isinstance(raw, dict) else {}
            _persist_failure_classification(
                repo_root,
                submission,
                descriptor_for_result,
                failure_class="state_or_transport_guard",
                retryable=False,
            )
        except Exception:
            pass
        return {
            "isolated": False,
            "reason": "transport_or_state_failure",
            "retryable": False,
            "error": f"{type(exc).__name__}: {exc}",
        }

    try:
        processor.render_descriptor(repo_root, descriptor)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        validation_errors = list(getattr(exc, "issues", []) or [])
        _persist_failure_classification(
            repo_root,
            submission,
            descriptor,
            failure_class="content_validation",
            retryable=False,
        )
        job_path = repo_root / ".survey/work-queue/jobs" / f"{descriptor['job_id']}.json"
        try:
            job = json.loads(job_path.read_text(encoding="utf-8"))
        except Exception as job_exc:
            return {
                "isolated": False,
                "reason": "job_unavailable",
                "retryable": False,
                "error": f"{type(job_exc).__name__}: {job_exc}",
                "validation_error": error,
            }
        if not isinstance(job, dict):
            return {
                "isolated": False,
                "reason": "job_not_object",
                "retryable": False,
                "validation_error": error,
            }

        job["status"] = "ready"
        job.pop("completed_at", None)
        job.pop("artifact_submission", None)
        job["repair_required"] = True
        job["validation_error"] = error
        if validation_errors:
            job["validation_errors"] = validation_errors
        else:
            job.pop("validation_errors", None)
        job["last_validation_failed_at"] = _now()
        _write(job_path, job)
        return {
            "isolated": True,
            "job_id": descriptor["job_id"],
            "attempt_id": descriptor["attempt_id"],
            "retryable": False,
            "failure_class": "content_validation",
            "validation_error": error,
            **({"validation_errors": validation_errors} if validation_errors else {}),
        }

    classified = _persist_failure_classification(
        repo_root,
        submission,
        descriptor,
        failure_class="post_validation_processing_failure",
        retryable=True,
    )
    return {
        "isolated": False,
        "reason": "record_validation_passed",
        "job_id": descriptor["job_id"],
        "attempt_id": descriptor["attempt_id"],
        "retryable": bool(classified and classified.get("retryable") is True),
        "failure_class": (classified or {}).get("failure_class", "post_validation_processing_failure"),
        "recovery_failures": (classified or {}).get("recovery_failures"),
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
