#!/usr/bin/env python3
"""Apply immutable reference-relevance requests through the canonical ledger helper."""
from __future__ import annotations

import argparse
import hashlib
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
CLEAR_OPERATION = "clear_relevance"


class RequestValidationError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(_json_bytes(payload))
    tmp.replace(path)


def _json_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _string_list(payload: dict[str, Any], key: str) -> list[str]:
    value = payload.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise RequestValidationError(f"{key} must be a list of strings")
    return [item for item in value if item.strip()]


def _validate_request(path: Path, payload: Any, repo_root: Path | None = None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise RequestValidationError("request must be a JSON object")
    if type(payload.get("schema_version")) is not int or payload.get("schema_version") != 1:
        raise RequestValidationError("schema_version must be 1")

    raw_operation = payload.get("operation")
    if raw_operation == CLEAR_OPERATION:
        for key in ("request_id", "operation", "canonical_id", "reason"):
            if type(payload.get(key)) is not str:
                raise RequestValidationError(f"{key} must be a string for clear_relevance")
        if type(payload.get("identity_tokens")) is not list or any(type(item) is not str for item in payload["identity_tokens"]):
            raise RequestValidationError("identity_tokens must be a list of strings for clear_relevance")

    request_id = str(payload.get("request_id") or "").strip()
    if not request_id:
        raise RequestValidationError("request_id is required")
    if request_id != path.stem:
        raise RequestValidationError("request_id must match the request filename")

    operation = str(payload.get("operation") or "").strip()
    if operation not in SUPPORTED_OPERATIONS and operation != CLEAR_OPERATION:
        raise RequestValidationError("operation must be mark_unrelated, mark_borderline, or clear_relevance")

    canonical_id = str(payload.get("canonical_id") or "").strip()
    if not canonical_id:
        raise RequestValidationError("canonical_id is required")

    reason = str(payload.get("reason") or "").strip()
    if not reason:
        raise RequestValidationError("reason is required")

    title = payload.get("title")
    if title is not None and not isinstance(title, str):
        raise RequestValidationError("title must be a string when provided")

    reconsidered = payload.get("reconsidered_from_borderline", False)
    if not isinstance(reconsidered, bool):
        raise RequestValidationError("reconsidered_from_borderline must be boolean when provided")

    identity_tokens = _string_list(payload, "identity_tokens")
    root_review_proof = payload.get("root_review_proof")
    if operation == CLEAR_OPERATION:
        if len(reason) < 20:
            raise RequestValidationError("clear_relevance reason must be paper-specific and at least 20 characters")
        if not identity_tokens:
            raise RequestValidationError("clear_relevance requires verified identity_tokens")
        if not isinstance(root_review_proof, dict) or set(root_review_proof) != {"review_id", "review_path", "review_sha256"}:
            raise RequestValidationError("clear_relevance requires root_review_proof")
        if any(type(root_review_proof.get(key)) is not str or not root_review_proof[key].strip() for key in ("review_id", "review_path", "review_sha256")):
            raise RequestValidationError("root_review_proof fields must be non-empty strings")
        review_id = root_review_proof["review_id"].strip()
        review_path = root_review_proof["review_path"].strip()
        review_sha256 = root_review_proof["review_sha256"].strip().lower()
        if len(review_sha256) != 64 or any(char not in "0123456789abcdef" for char in review_sha256):
            raise RequestValidationError("root_review_proof review_sha256 must be a SHA-256 hex digest")
        proof_path = Path(review_path)
        expected_prefix = Path(".survey/work-queue/reference-curation/reviews")
        if proof_path.is_absolute() or proof_path.parts[:-1] != expected_prefix.parts or proof_path.suffix.lower() != ".json" or len(proof_path.parts) != len(expected_prefix.parts) + 1:
            raise RequestValidationError("root_review_proof review_path must identify a direct JSON child of the repository reviews directory")
        if repo_root is None:
            raise RequestValidationError("repository root is required to validate root_review_proof")
        root = repo_root.resolve()
        review_file = root / proof_path
        if any(part.is_symlink() for part in [root / Path(*proof_path.parts[:index]) for index in range(1, len(proof_path.parts) + 1)]) or not review_file.is_file() or review_file.resolve().parent != (root / expected_prefix).resolve():
            raise RequestValidationError("root_review_proof review artifact must be an existing non-symlink repository file")
        artifact_bytes = review_file.read_bytes()
        if hashlib.sha256(artifact_bytes).hexdigest() != review_sha256:
            raise RequestValidationError("root_review_proof review artifact SHA-256 mismatch")
        try:
            artifact = json.loads(artifact_bytes.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise RequestValidationError("root_review_proof artifact must be valid JSON") from exc
        artifact_keys = {"schema_version", "record_type", "review_id", "action", "root_decision", "canonical_id", "verified_aliases"}
        if not isinstance(artifact, dict) or set(artifact) != artifact_keys or type(artifact.get("schema_version")) is not int or artifact["schema_version"] != 1:
            raise RequestValidationError("root_review_proof artifact has an unsupported schema")
        if any(type(artifact.get(key)) is not str for key in ("record_type", "review_id", "action", "root_decision", "canonical_id")) or artifact["record_type"] != "reference_relevance_clear_review" or artifact["action"] != CLEAR_OPERATION or artifact["root_decision"] not in {"move", "retain_related", "accept"}:
            raise RequestValidationError("root_review_proof artifact does not record a positive root review decision")
        proof_aliases = artifact.get("verified_aliases")
        if type(proof_aliases) is not list or not proof_aliases or any(type(item) is not str for item in proof_aliases):
            raise RequestValidationError("root_review_proof verified_aliases must be a non-empty list of strings")
        if artifact["review_id"] != review_id:
            raise RequestValidationError("root_review_proof review_id does not match its artifact")
        reviews_dir = root / expected_prefix
        for candidate in reviews_dir.glob("*.json"):
            if candidate.is_symlink():
                raise RequestValidationError("review directory contains a symlink")
            try:
                candidate_payload = json.loads(candidate.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                continue
            if candidate != review_file and isinstance(candidate_payload, dict) and candidate_payload.get("review_id") == review_id:
                raise RequestValidationError("root_review_proof review_id must be unique in the review directory")
        proof_canonical = artifact["canonical_id"]
        canonical, request_tokens = reference_relevance_ledger.normalized_relevance_tokens(
            canonical_id, identity_tokens
        )
        proof_canonical_normalized, proof_tokens = reference_relevance_ledger.normalized_relevance_tokens(
            proof_canonical, proof_aliases
        )
        if canonical != proof_canonical_normalized or request_tokens != proof_tokens:
            raise RequestValidationError("root_review_proof canonical_id or verified_aliases do not match the request")
        root_review_proof = {
            "review_id": review_id,
            "review_path": proof_path.as_posix(),
            "review_sha256": review_sha256,
            "root_decision": artifact["root_decision"],
            "canonical_id": canonical,
            "verified_aliases": sorted(proof_tokens),
        }

    return {
        **payload,
        "request_id": request_id,
        "operation": operation,
        "canonical_id": canonical_id,
        "reason": reason,
        "title": title.strip() if isinstance(title, str) and title.strip() else None,
        "identity_tokens": identity_tokens,
        "linked_from": _string_list(payload, "linked_from"),
        "reconsidered_from_borderline": reconsidered,
        **({"root_review_proof": root_review_proof} if operation == CLEAR_OPERATION else {}),
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
    repo_root = repo_root.resolve()
    unrelated_path = repo_root / UNRELATED_LEDGER
    borderline_path = repo_root / BORDERLINE_LEDGER
    with reference_relevance_ledger.ledger_mutation_lock(unrelated_path, borderline_path):
        return _process_request_locked(repo_root, request_path)


def _process_request_locked(repo_root: Path, request_path: Path) -> dict[str, Any]:
    request_id = request_path.stem
    result_path = repo_root / RESULT_DIR / f"{request_id}.json"
    request_bytes = request_path.read_bytes()
    request_sha256 = hashlib.sha256(request_bytes).hexdigest()
    clear_transaction_path = repo_root / reference_relevance_ledger.CLEAR_JOURNAL_DIR / f"{request_id}.json"
    reference_relevance_ledger.validate_clear_transaction_request(
        clear_transaction_path,
        request_id=request_id,
        request_sha256=request_sha256,
    )
    if result_path.exists():
        existing_bytes = result_path.read_bytes()
        existing = json.loads(existing_bytes.decode("utf-8"))
        if isinstance(existing, dict) and existing.get("request_operation") == CLEAR_OPERATION and existing.get("ok") is True and existing.get("request_sha256") != request_sha256:
            raise ValueError("existing clear_relevance result does not match the immutable request")
        return {
            "request_id": request_id,
            "status": "already_processed",
            "ok": bool(existing.get("ok")) if isinstance(existing, dict) else False,
            "result_path": str(result_path.relative_to(repo_root)),
        }
    try:
        raw = json.loads(request_bytes.decode("utf-8"))
        request = _validate_request(request_path, raw, repo_root)
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
    if request["operation"] == CLEAR_OPERATION:
        cleared = reference_relevance_ledger.clear_relevance(
            unrelated_path,
            borderline_path,
            canonical_id=request["canonical_id"],
            identity_tokens=request["identity_tokens"],
            request_id=request["request_id"],
            request_sha256=request_sha256,
        )
        result = {
            "schema_version": 1,
            "operation": "reference_relevance_result",
            "ok": True,
            "request_id": request["request_id"],
            "request_operation": CLEAR_OPERATION,
            "request_sha256": request_sha256,
            "canonical_id": cleared["canonical_id"],
            "reason": request["reason"],
            "identity_tokens": cleared["identity_tokens"],
            "removed_rows": cleared["removed_rows"],
            "root_review_proof": request["root_review_proof"],
            "processed_at": _now(),
            "worker_id": request.get("worker_id"),
            "run_key": request.get("run_key"),
            "next_action": "CONTINUE_APPROVED_REVIEW",
            "instructions": (
                "Reviewed negative relevance rows were cleared. This does not add a positive "
                "classification or restore a retired paper. Continue only the approved review or recovery."
            ),
        }
        try:
            expected_result_bytes = _json_bytes(result)
            reference_relevance_ledger.record_clear_result(
                cleared["transaction_path"],
                request_id=request["request_id"],
                request_sha256=request_sha256,
                result_sha256=hashlib.sha256(expected_result_bytes).hexdigest(),
            )
            _write_json(result_path, result)
        except Exception:
            reference_relevance_ledger.rollback_clear_transaction(
                cleared["transaction_path"],
                unrelated_path=unrelated_path,
                borderline_path=borderline_path,
                request_id=request["request_id"],
                request_sha256=request_sha256,
            )
            raise
        reference_relevance_ledger.finalize_clear_transaction(
            cleared["transaction_path"],
            unrelated_path=unrelated_path,
            borderline_path=borderline_path,
            request_id=request["request_id"],
            request_sha256=request_sha256,
            result_path=result_path,
        )
        return {
            "request_id": request["request_id"],
            "status": "processed",
            "ok": True,
            "request_operation": CLEAR_OPERATION,
            "canonical_id": cleared["canonical_id"],
            "removed_row_count": len(cleared["removed_rows"]),
            "result_path": str(result_path.relative_to(repo_root)),
        }

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
            reconsidered_from_borderline=request["reconsidered_from_borderline"],
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
        "reconsidered_from_borderline": request["reconsidered_from_borderline"],
        "borderline_recheck_count": row.get("borderline_recheck_count"),
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


def process_pending(repo_root: Path, max_requests: int | None = None) -> dict[str, Any]:
    request_dir = repo_root / REQUEST_DIR
    request_dir.mkdir(parents=True, exist_ok=True)
    outcomes: list[dict[str, Any]] = []
    retryable_errors: list[dict[str, str]] = []

    processed_requests = 0
    for request_path in sorted(request_dir.glob("*.json")):
        # Existing immutable results are already terminal. They must not consume
        # the bounded processing budget, otherwise a stable alphabetical prefix
        # can starve every unsettled request behind it forever.
        result_path = repo_root / RESULT_DIR / f"{request_path.stem}.json"
        if result_path.exists():
            outcomes.append(process_request(repo_root, request_path))
            continue

        if max_requests is not None and processed_requests >= max(0, max_requests):
            break
        processed_requests += 1
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
    parser.add_argument("--max-requests", type=int, default=None)
    args = parser.parse_args()

    summary = process_pending(Path(args.repo_root).resolve(), args.max_requests)
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
