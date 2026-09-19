#!/usr/bin/env python3
"""Authoritative Discovery retrieval precheck.

A Scheduled Chat worker writes raw search records as an immutable request. This
processor applies the same canonical identity surface used by the final Discovery
duplicate gate before the worker is allowed to evaluate candidates.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import discovery_search_filter  # noqa: E402
import paper_identity  # noqa: E402

SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
OPERATION = "precheck_discovery_candidates"


class DiscoveryPrecheckRequestError(ValueError):
    pass


def _read_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise DiscoveryPrecheckRequestError(f"precheck request is unreadable: {path}") from exc
    if not isinstance(value, dict):
        raise DiscoveryPrecheckRequestError("precheck request must be a JSON object")
    return value


def _validate_request(request: dict[str, Any]) -> tuple[str, str, str, list[dict[str, Any]]]:
    if request.get("operation") != OPERATION:
        raise DiscoveryPrecheckRequestError(f"operation must be {OPERATION!r}")
    request_id = str(request.get("request_id") or "").strip()
    if not SAFE_REQUEST_ID.fullmatch(request_id):
        raise DiscoveryPrecheckRequestError("request_id must be a safe non-empty identifier")
    run_key = str(request.get("run_key") or "").strip()
    axis = str(request.get("axis") or "").strip()
    if not run_key:
        raise DiscoveryPrecheckRequestError("run_key is required")
    if not axis:
        raise DiscoveryPrecheckRequestError("axis is required")
    records = request.get("records")
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise DiscoveryPrecheckRequestError("records must be a list of objects")
    if len(records) > 100:
        raise DiscoveryPrecheckRequestError("records may contain at most 100 search results")
    return request_id, run_key, axis, records


def _manifest_source_commit(snapshot_dir: Path) -> str | None:
    manifest = json.loads((snapshot_dir / "_manifest.json").read_text(encoding="utf-8"))
    value = manifest.get("source_commit")
    return str(value) if value else None


def _allowed_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for record in records:
        tokens = sorted(paper_identity.identity_tokens(record))
        out.append({
            "primary_identity": paper_identity.primary_identity_key(record),
            "identity_tokens": tokens,
            "record": record,
        })
    return out


def _receipt(
    *,
    request_id: str,
    run_key: str,
    axis: str,
    snapshot_source_commit: str | None,
    allowed_records: list[dict[str, Any]],
) -> str:
    payload = {
        "request_id": request_id,
        "run_key": run_key,
        "axis": axis,
        "snapshot_source_commit": snapshot_source_commit,
        "allowed_identity_tokens": [
            row["identity_tokens"] for row in allowed_records
        ],
    }
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def process_request(
    request_path: Path,
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
) -> dict[str, Any]:
    request_path = Path(request_path)
    request = _read_object(request_path)
    request_id, run_key, axis, records = _validate_request(request)

    filtered = discovery_search_filter.filter_search_batch(
        records,
        snapshot_dir=Path(snapshot_dir),
        rejection_ledger_path=Path(rejection_ledger_path),
    )
    allowed = _allowed_records(filtered["results"])
    source_commit = _manifest_source_commit(Path(snapshot_dir))
    receipt = _receipt(
        request_id=request_id,
        run_key=run_key,
        axis=axis,
        snapshot_source_commit=source_commit,
        allowed_records=allowed,
    )
    return {
        "schema_version": 1,
        "operation": OPERATION,
        "ok": True,
        "request_id": request_id,
        "run_key": run_key,
        "axis": axis,
        "snapshot_source_commit": source_commit,
        "raw_search_result_count": filtered["raw_search_result_count"],
        "retrieval_duplicate_filtered_count": filtered["retrieval_duplicate_filtered_count"],
        "represented_paper_match_filtered_count": filtered["represented_paper_match_filtered_count"],
        "rejection_ledger_filtered_count": filtered["rejection_ledger_filtered_count"],
        "intra_batch_duplicate_filtered_count": filtered["intra_batch_duplicate_filtered_count"],
        "unseen_result_count": filtered["unseen_result_count"],
        "results": filtered["results"],
        "allowed_records": allowed,
        "receipt": receipt,
        "next_action": (
            "Evaluate only records in results[]. Do not re-add filtered records. "
            "When writing submit_discovery_round, include discovery_precheck.result_path "
            "and this receipt."
        ),
    }


def failure_result(request_path: Path, exc: Exception) -> dict[str, Any]:
    request = {}
    try:
        request = _read_object(request_path)
    except Exception:
        pass
    return {
        "schema_version": 1,
        "operation": OPERATION,
        "ok": False,
        "request_id": request.get("request_id"),
        "run_key": request.get("run_key"),
        "axis": request.get("axis"),
        "error": f"{type(exc).__name__}: {exc}",
        "next_action": (
            "Fix the precheck request and create a NEW immutable request file. "
            "Do not bypass precheck and do not submit Discovery candidates directly."
        ),
        "recovery_steps": [
            "Keep the failed request unchanged.",
            "Create a new discovery-precheck request containing the raw search records.",
            "Wait for its result with ok=true.",
            "Evaluate only result.results[].",
            "Reference that result_path and receipt from the new Discovery submission.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--snapshot-dir", type=Path, required=True)
    parser.add_argument("--rejection-ledger", type=Path, required=True)
    args = parser.parse_args()

    try:
        result = process_request(
            args.request,
            snapshot_dir=args.snapshot_dir,
            rejection_ledger_path=args.rejection_ledger,
        )
        rc = 0
    except Exception as exc:
        result = failure_result(args.request, exc)
        rc = 1

    args.result.parent.mkdir(parents=True, exist_ok=True)
    args.result.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
