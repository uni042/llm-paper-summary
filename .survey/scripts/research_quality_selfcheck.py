#!/usr/bin/env python3
"""Synchronous no-state Research/Audit quality self-check before async preflight.

This helper reuses the same structured-record assembly path and paper-quality
criteria as research_quality_preflight.py. It does not create request, result,
submission, or queue-state files.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

import paper_quality_gate
import prepare_completed_submission
import process_immutable_submission


def _quality_payload(result: Any) -> dict[str, Any]:
    if is_dataclass(result):
        return asdict(result)
    return {
        "status": getattr(result, "status", None),
        "failures": list(getattr(result, "failures", []) or []),
        "warnings": list(getattr(result, "warnings", []) or []),
    }


def _issues(exc: Exception) -> list[str]:
    issues = list(getattr(exc, "issues", []) or [])
    return issues or [f"{type(exc).__name__}: {exc}"]


def check(
    repo_root: Path,
    *,
    kind: str,
    attempt_id: str,
    job_id: str,
    record_bank: str,
    paper_path: str | None = None,
) -> dict[str, Any]:
    """Inspect the current record-bank snapshot without mutating durable state."""
    root = Path(repo_root).resolve()
    try:
        descriptor = prepare_completed_submission.build(
            root,
            kind=kind,
            attempt_id=attempt_id,
            job_id=job_id,
            record_bank=record_bank,
            paper_path=paper_path,
            expected_blob_sha=None,
        )
        rendered = process_immutable_submission.render_descriptor(root, descriptor)
        process_immutable_submission._precheck_paper(
            root,
            descriptor,
            rendered_content=rendered,
        )
    except Exception as exc:
        return {
            "ok": True,
            "selfcheck_passed": False,
            "repair_required": True,
            "decision": "REPAIR_BEFORE_ASYNC_PREFLIGHT",
            "stage": "structured_record",
            "validation_errors": _issues(exc),
            "next_action": (
                "Repair only the affected record slots from primary-source evidence, "
                "repeat this synchronous self-check, and do not create the asynchronous "
                "research-preflight request until the self-check passes."
            ),
        }

    quality_result = paper_quality_gate.inspect_rendered_paper(
        root,
        descriptor["paper_path"],
        rendered,
    )
    quality = _quality_payload(quality_result)
    if quality_result.status == "FAIL":
        return {
            "ok": True,
            "selfcheck_passed": False,
            "repair_required": True,
            "decision": "REPAIR_BEFORE_ASYNC_PREFLIGHT",
            "stage": "rendered_paper_quality",
            "paper_path": descriptor["paper_path"],
            "record_slots": descriptor.get("record_slots"),
            "validation_errors": list(quality_result.failures),
            "quality": quality,
            "next_action": (
                "Repair only the affected record slots from primary-source evidence, "
                "repeat this synchronous self-check, and do not create the asynchronous "
                "research-preflight request until the self-check passes."
            ),
        }

    return {
        "ok": True,
        "selfcheck_passed": True,
        "repair_required": False,
        "decision": "READY_FOR_ASYNC_PREFLIGHT",
        "stage": "passed",
        "paper_path": descriptor["paper_path"],
        "record_slots": descriptor.get("record_slots"),
        "quality": quality,
        "next_action": (
            "Run the normal worker semantic self-review, then create the asynchronous "
            "research-preflight request. This self-check does not replace exact-blob "
            "preflight and does not authorize publication by itself."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--kind", choices=("research", "audit"), required=True)
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--record-bank", required=True)
    parser.add_argument("--paper-path")
    args = parser.parse_args()
    result = check(
        args.repo_root,
        kind=args.kind,
        attempt_id=args.attempt_id,
        job_id=args.job_id,
        record_bank=args.record_bank,
        paper_path=args.paper_path,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("selfcheck_passed") else 2


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
