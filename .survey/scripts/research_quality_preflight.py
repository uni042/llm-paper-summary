#!/usr/bin/env python3
"""Worker-owned quality preflight for Research/Audit completed publications."""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import immutable_submission  # noqa: E402
import paper_quality_gate  # noqa: E402
import prepare_completed_submission  # noqa: E402
import process_immutable_submission  # noqa: E402

SCHEMA_VERSION = 1
OPERATION = "research_quality_preflight"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
SELF_REVIEW_KEYS = (
    "primary_source_read_to_end",
    "no_unverified_inference",
    "summary_and_list_summary_specific",
    "headline_result_grounded",
    "method_end_to_end_explained",
    "evaluation_conditions_and_baselines_explicit",
    "results_conditions_and_interpretation_explicit",
    "limitations_and_positioning_specific",
)


class PreflightRequestError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise PreflightRequestError(f"preflight request is unreadable: {path}") from exc
    if not isinstance(value, dict):
        raise PreflightRequestError("preflight request must be a JSON object")
    return value


def _safe_id(value: Any, field: str) -> str:
    out = str(value or "").strip()
    if not SAFE_ID_RE.fullmatch(out):
        raise PreflightRequestError(f"{field} must be a safe non-empty identifier")
    return out


def _validate_request(path: Path) -> dict[str, Any]:
    request = _read_object(path)
    if request.get("schema_version") != SCHEMA_VERSION:
        raise PreflightRequestError(f"schema_version must be {SCHEMA_VERSION}")
    if request.get("operation") != OPERATION:
        raise PreflightRequestError(f"operation must be {OPERATION!r}")

    request_id = _safe_id(request.get("request_id"), "request_id")
    if path.stem != request_id:
        raise PreflightRequestError("request_id must match the request filename stem")
    kind = request.get("kind")
    if kind not in {"research", "audit"}:
        raise PreflightRequestError("kind must be research or audit")
    attempt_id = _safe_id(request.get("attempt_id"), "attempt_id")
    job_id = _safe_id(request.get("job_id"), "job_id")
    record_bank = str(request.get("record_bank") or "").strip().lower()
    if not record_bank:
        raise PreflightRequestError("record_bank is required")

    review = request.get("self_review")
    if not isinstance(review, dict):
        raise PreflightRequestError("self_review is required")
    missing = [key for key in SELF_REVIEW_KEYS if review.get(key) is not True]
    if missing:
        raise PreflightRequestError(
            "self_review must explicitly pass every item before automated preflight: "
            + ", ".join(missing)
        )

    out = {
        "schema_version": SCHEMA_VERSION,
        "operation": OPERATION,
        "request_id": request_id,
        "kind": kind,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "record_bank": record_bank,
        "self_review": {key: True for key in SELF_REVIEW_KEYS},
    }
    for field in ("paper_path", "expected_blob_sha"):
        value = request.get(field)
        if value not in (None, ""):
            if not isinstance(value, str):
                raise PreflightRequestError(f"{field} must be a string when present")
            out[field] = value
    return out


def _identity(request: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "operation": OPERATION,
        "request_id": request.get("request_id"),
        "kind": request.get("kind"),
        "attempt_id": request.get("attempt_id"),
        "job_id": request.get("job_id"),
        "record_bank": request.get("record_bank"),
        "paper_path": request.get("paper_path"),
        "expected_blob_sha": request.get("expected_blob_sha"),
    }


def _canonical_expected_blob_sha(repo_root: Path, paper_path: str | None) -> str | None:
    """Derive optimistic-concurrency identity from the actual paper, never from a slot SHA."""
    if not paper_path:
        return None
    paper = repo_root / paper_path
    if not paper.is_file():
        return None
    return immutable_submission.git_blob_sha(paper.read_bytes())


def _repair_result(
    request: dict[str, Any],
    descriptor: dict[str, Any],
    issues: list[str],
    *,
    stage: str,
    quality_result: Any | None = None,
) -> dict[str, Any]:
    result = {
        **_identity(request),
        "ok": True,
        "preflight_passed": False,
        "repair_required": True,
        "decision": "REPAIR_BEFORE_SUBMISSION",
        "stage": stage,
        "descriptor_sha256": prepare_completed_submission.descriptor_fingerprint(descriptor),
        "record_slots": descriptor.get("record_slots"),
        "validation_errors": list(issues),
        "checked_at": _now(),
        "next_action": (
            "Do not create a completed-submission request. Repair only the affected record slots "
            "from primary-source evidence, repeat the worker self-review, then create a NEW "
            "research-preflight request_id for the same attempt."
        ),
    }
    if quality_result is not None:
        result["quality"] = asdict(quality_result)
    return result


def process_request(repo_root: Path, request_path: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    request_path = Path(request_path)
    if not request_path.is_absolute():
        request_path = repo_root / request_path
    request = _validate_request(request_path)

    # Resolve the canonical paper path first without trusting a worker-supplied
    # expected_blob_sha. That field is an optimistic-concurrency guard for an
    # already-published paper; it must never be copied from a record-slot blob.
    descriptor = prepare_completed_submission.build(
        repo_root,
        kind=request["kind"],
        attempt_id=request["attempt_id"],
        job_id=request["job_id"],
        record_bank=request["record_bank"],
        paper_path=request.get("paper_path"),
        expected_blob_sha=None,
    )
    request["paper_path"] = descriptor["paper_path"]
    request["expected_blob_sha"] = _canonical_expected_blob_sha(
        repo_root, descriptor["paper_path"]
    )
    if request["expected_blob_sha"] is not None:
        descriptor = prepare_completed_submission.build(
            repo_root,
            kind=request["kind"],
            attempt_id=request["attempt_id"],
            job_id=request["job_id"],
            record_bank=request["record_bank"],
            paper_path=descriptor["paper_path"],
            expected_blob_sha=request["expected_blob_sha"],
        )

    try:
        rendered = process_immutable_submission.render_descriptor(repo_root, descriptor)
        process_immutable_submission._precheck_paper(
            repo_root,
            descriptor,
            rendered_content=rendered,
        )
    except Exception as exc:
        issues = list(getattr(exc, "issues", []) or [])
        if not issues:
            issues = [f"{type(exc).__name__}: {exc}"]
        return _repair_result(request, descriptor, issues, stage="structured_record")

    quality_result = paper_quality_gate.inspect_rendered_paper(
        repo_root,
        descriptor["paper_path"],
        rendered,
    )
    if quality_result.status == "FAIL":
        return _repair_result(
            request,
            descriptor,
            list(quality_result.failures),
            stage="rendered_paper_quality",
            quality_result=quality_result,
        )

    return {
        **_identity(request),
        "ok": True,
        "preflight_passed": True,
        "repair_required": False,
        "decision": "READY_FOR_SUBMISSION",
        "descriptor_sha256": prepare_completed_submission.descriptor_fingerprint(descriptor),
        "record_slots": descriptor.get("record_slots"),
        "quality": asdict(quality_result),
        "checked_at": _now(),
        "next_action": (
            "Create .survey/work-queue/completed-submission-requests/<attempt_id>.json "
            "and set preflight_result to this exact result path. Do not edit any record slot "
            "after this check; if a slot changes, run a new preflight first."
        ),
    }


def failure_result(request_path: Path, exc: Exception) -> dict[str, Any]:
    request: dict[str, Any] = {}
    try:
        request = _read_object(request_path)
    except Exception:
        pass
    return {
        **_identity(request),
        "ok": False,
        "preflight_passed": False,
        "repair_required": False,
        "decision": "FIX_PREFLIGHT_REQUEST",
        "error": f"{type(exc).__name__}: {exc}",
        "checked_at": _now(),
        "next_action": (
            "Fix the preflight request contract. Do not create a completed-submission request "
            "until a new preflight result has preflight_passed=true."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    request_path = args.request if args.request.is_absolute() else repo_root / args.request
    try:
        result = process_request(repo_root, request_path)
    except Exception as exc:
        result = failure_result(request_path, exc)

    result_path = args.result if args.result.is_absolute() else repo_root / args.result
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    # A quality FAIL is a normal repair state, not an Actions failure.
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
