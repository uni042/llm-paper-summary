#!/usr/bin/env python3
"""Apply immutable reference-relevance requests through the canonical ledger helper."""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import reference_relevance_ledger

REQUEST_DIR = Path(".survey/work-queue/reference-curation/requests")
RESULT_DIR = Path(".survey/work-queue/reference-curation/results")
UNRELATED_LEDGER = Path(".survey/work-queue/reference-curation/unrelated-papers.json")
BORDERLINE_LEDGER = Path(".survey/work-queue/reference-curation/borderline-papers.json")
SUPPORTED_OPERATIONS = {
    "mark_unrelated": "unrelated",
    "mark_borderline": "borderline",
}


class RequestValidationError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def _string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise RequestValidationError(f"{key} must be a list of strings")
    return [item for item in value if item.strip()]


def _validate_request(path: Path, payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise RequestValidationError("request must be a JSON object")
    if payload.get("schema_version") != 1:
        raise RequestValidationError("schema_version must be 1")

    request_id = str(payload.get("request_id") or "").strip()
    if not request_id:
        raise RequestValidationError("request_id is required")
    if request_id != path.stem:
        raise RequestValidationError("request_id must match the request filename")

    operation = str(payload.get("operation") or "").strip()
    if operation not in SUPPORTED_OPERATIONS:
        raise RequestValidationError("operation must be mark_unrelated or mark_borderline")

    canonical_id = str(payload.get("canonical_id") or "").strip()
    if not canonical_id:
        raise RequestValidationError("canonical_id is required")

    reason = str(payload.get("reason") or "").strip()
    if not reason:
        raise RequestValidationError("reason is required")

    title = payload.get("title")
    if title is not None and not isinstance(title, str):
        raise RequestValidationError("title must be a string when provided")

    return {
        **payload,
        "request_id": request_id,
        "operation": operation,
        "canonical_id": canonical_id,
        "reason": reason,
        "title": title.strip() if isinstance(title, str) and title.strip() else None,
        "identity_tokens": _string_list(payload, "identity_tokens"),
        "linked_from": _string_list(payload, "linked_from"),
    }


def _failure_result(request_id: str, error: Exception) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "operation": "reference_relevance_result",
        "ok": False,
        "request_id": request_id,
        "processed_at": _now(),
        "failure_class": "invalid_request",
        "error": str(error),
        "next_action": "FIX_REFERENCE_RELEVANCE_REQUEST",
        "recovery_steps": [
            "Do not edit the immutable failed request or result.",
            "Create a new request_id with a corrected schema-v1 reference-relevance request.",
            "Continue other candidate evaluation; one invalid relevance request does not stop the Discovery run.",
        ],
    }


def process_request(repo_root: Path, request_path: Path) -> dict[str, Any]:
    request_id = request_path.stem
    result_path = repo_root / RESULT_DIR / f"{request_id}.json"
    if result_path.exists():
        existing = json.loads(result_path.read_text(encoding="utf-8"))
        return {
            "request_id": request_id,
            "status": "already_processed",
            "ok": bool(existing.get("ok")),
            "result_path": str(result_path.relative_to(repo_root)),
        }

    try:
        raw = json.loads(request_path.read_text(encoding="utf-8"))
        request = _validate_request(request_path, raw)
    except (json.JSONDecodeError, RequestValidationError) as exc:
        result = _failure_result(request_id, exc)
        _write_json(result_path, result)
        return {
            "request_id": request_id,
            "status": "invalid_request",
            "ok": False,
            "result_path": str(result_path.relative_to(repo_root)),
        }

    unrelated_path = repo_root / UNRELATED_LEDGER
    borderline_path = repo_root / BORDERLINE_LEDGER
    kwargs = {
        "canonical_id": request["canonical_id"],
        "title": request["title"],
        "reason": request["reason"],
        "identity_tokens": request["identity_tokens"],
        "linked_from": request["linked_from"],
    }
    if request["operation"] == "mark_unrelated":
        row = reference_relevance_ledger.mark_unrelated(
            unrelated_path,
            **kwargs,
            borderline_path=borderline_path,
        )
    else:
        row = reference_relevance_ledger.mark_borderline(
            borderline_path,
            **kwargs,
            unrelated_path=unrelated_path,
        )

    result = {
        "schema_version": 1,
        "operation": "reference_relevance_result",
        "ok": True,
        "request_id": request["request_id"],
        "request_operation": request["operation"],
        "classification": SUPPORTED_OPERATIONS[request["operation"]],
        "canonical_id": row["canonical_id"],
        "record": row,
        "processed_at": _now(),
        "worker_id": request.get("worker_id"),
        "run_key": request.get("run_key"),
        "scheduled_slot": request.get("scheduled_slot"),
        "actual_invocation_start": request.get("actual_invocation_start"),
        "source_precheck_request_id": request.get("source_precheck_request_id"),
        "next_action": "CONTINUE_DISCOVERY_EVALUATION",
        "instructions": (
            "The canonical relevance ledger is updated. Continue the current Discovery "
            "round; do not re-evaluate or submit this classified candidate."
        ),
    }
    _write_json(result_path, result)
    return {
        "request_id": request_id,
        "status": "processed",
        "ok": True,
        "classification": result["classification"],
        "canonical_id": result["canonical_id"],
        "result_path": str(result_path.relative_to(repo_root)),
    }


def process_pending(repo_root: Path) -> dict[str, Any]:
    request_dir = repo_root / REQUEST_DIR
    request_dir.mkdir(parents=True, exist_ok=True)
    outcomes: list[dict[str, Any]] = []
    retryable_errors: list[dict[str, str]] = []

    for request_path in sorted(request_dir.glob("*.json")):
        try:
            outcomes.append(process_request(repo_root, request_path))
        except Exception as exc:
            retryable_errors.append(
                {
                    "request_id": request_path.stem,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    return {
        "ok": not retryable_errors,
        "processed_at": _now(),
        "request_count": len(outcomes) + len(retryable_errors),
        "processed_count": sum(row["status"] == "processed" for row in outcomes),
        "already_processed_count": sum(row["status"] == "already_processed" for row in outcomes),
        "invalid_request_count": sum(row["status"] == "invalid_request" for row in outcomes),
        "retryable_error_count": len(retryable_errors),
        "outcomes": outcomes,
        "retryable_errors": retryable_errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    summary = process_pending(Path(args.repo_root).resolve())
    print(json.dumps(summary, ensure_ascii=False))
    if not summary["ok"]:
        print(
            "[WORKER-GUIDE][待機] Some relevance requests hit retryable processing errors; "
            "successful siblings were still processed and the remaining requests should be retried.",
            file=sys.stderr,
        )
        return 1

    print(
        "[WORKER-GUIDE][完了] Reference relevance requests were drained.",
        file=sys.stderr,
    )
    print(
        "[WORKER-GUIDE][次] Discovery workers do not wait for this result after durably "
        "creating a valid request; continue candidate evaluation immediately.",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
