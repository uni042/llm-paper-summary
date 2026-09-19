#!/usr/bin/env python3
"""Authoritative iterative Discovery retrieval precheck.

A Scheduled Chat worker writes one provider page/batch per immutable request.
The processor applies the canonical Discovery exclusion surface, carries the
unseen buffer forward through workflow-produced results, and tells the worker
whether it must fetch another page before candidate evaluation is allowed.
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
SCHEMA_VERSION = 2
DEFAULT_TARGET_UNSEEN = discovery_search_filter.DEFAULT_PREFETCH_UNSEEN
MAX_TARGET_UNSEEN = 100
MAX_PAGES = 100


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


def _safe_id(value: Any, field: str) -> str:
    out = str(value or "").strip()
    if not SAFE_REQUEST_ID.fullmatch(out):
        raise DiscoveryPrecheckRequestError(f"{field} must be a safe non-empty identifier")
    return out


def _validate_request(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("operation") != OPERATION:
        raise DiscoveryPrecheckRequestError(f"operation must be {OPERATION!r}")
    schema_version = request.get("schema_version")
    if isinstance(schema_version, bool) or not isinstance(schema_version, int) or schema_version < SCHEMA_VERSION:
        raise DiscoveryPrecheckRequestError(
            f"schema_version must be >= {SCHEMA_VERSION}; iterative precheck is mandatory"
        )

    request_id = _safe_id(request.get("request_id"), "request_id")
    collector_id = _safe_id(request.get("collector_id"), "collector_id")
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

    provider_has_more = request.get("provider_has_more")
    if not isinstance(provider_has_more, bool):
        raise DiscoveryPrecheckRequestError(
            "provider_has_more must be an explicit boolean so precheck can force pagination"
        )

    target_unseen = request.get("target_unseen", DEFAULT_TARGET_UNSEEN)
    if (
        isinstance(target_unseen, bool)
        or not isinstance(target_unseen, int)
        or target_unseen <= 0
        or target_unseen > MAX_TARGET_UNSEEN
    ):
        raise DiscoveryPrecheckRequestError(
            f"target_unseen must be an integer between 1 and {MAX_TARGET_UNSEEN}"
        )

    previous_request_id = request.get("previous_request_id")
    previous_receipt = request.get("previous_receipt")
    if previous_request_id is None and previous_receipt is None:
        previous_request_id = None
        previous_receipt = None
    elif previous_request_id is None or previous_receipt is None:
        raise DiscoveryPrecheckRequestError(
            "previous_request_id and previous_receipt must be provided together"
        )
    else:
        previous_request_id = _safe_id(previous_request_id, "previous_request_id")
        previous_receipt = str(previous_receipt or "").strip()
        if not previous_receipt.startswith("sha256:"):
            raise DiscoveryPrecheckRequestError("previous_receipt must be a sha256 receipt")
        if previous_request_id == request_id:
            raise DiscoveryPrecheckRequestError("previous_request_id must differ from request_id")

    return {
        "request_id": request_id,
        "collector_id": collector_id,
        "run_key": run_key,
        "axis": axis,
        "records": records,
        "provider_has_more": provider_has_more,
        "target_unseen": target_unseen,
        "previous_request_id": previous_request_id,
        "previous_receipt": previous_receipt,
    }


def _manifest_source_commit(snapshot_dir: Path) -> str | None:
    manifest = json.loads((snapshot_dir / "_manifest.json").read_text(encoding="utf-8"))
    value = manifest.get("source_commit")
    return str(value) if value else None


def _results_dir(request_path: Path) -> Path:
    request_path = Path(request_path)
    if request_path.parent.name == "requests":
        return request_path.parent.parent / "results"
    return request_path.parent / "results"


def _load_previous_result(request_path: Path, request: dict[str, Any]) -> dict[str, Any] | None:
    previous_request_id = request["previous_request_id"]
    if previous_request_id is None:
        return None

    path = _results_dir(request_path) / f"{previous_request_id}.json"
    if not path.is_file():
        raise DiscoveryPrecheckRequestError(
            f"previous precheck result does not exist yet: {previous_request_id}"
        )
    previous = _read_object(path)
    if previous.get("ok") is not True or previous.get("operation") != OPERATION:
        raise DiscoveryPrecheckRequestError("previous precheck result is not successful")
    if int(previous.get("schema_version") or 0) < SCHEMA_VERSION:
        raise DiscoveryPrecheckRequestError(
            "previous precheck result predates the iterative protocol; start a new collector"
        )
    if str(previous.get("request_id") or "") != previous_request_id:
        raise DiscoveryPrecheckRequestError("previous result request_id mismatch")
    if str(previous.get("receipt") or "") != request["previous_receipt"]:
        raise DiscoveryPrecheckRequestError("previous precheck receipt mismatch")
    for field in ("collector_id", "run_key", "axis"):
        if str(previous.get(field) or "") != str(request[field]):
            raise DiscoveryPrecheckRequestError(f"previous result {field} mismatch")
    if int(previous.get("target_unseen") or 0) != int(request["target_unseen"]):
        raise DiscoveryPrecheckRequestError("target_unseen may not change within one collector")
    if previous.get("evaluation_allowed") is not False or previous.get("decision") != "CONTINUE_FETCH":
        raise DiscoveryPrecheckRequestError(
            "previous result is already terminal for this collector; start a new collector instead"
        )
    results = previous.get("results")
    if not isinstance(results, list) or any(not isinstance(record, dict) for record in results):
        raise DiscoveryPrecheckRequestError("previous result has an invalid accumulated results buffer")
    pages_processed = previous.get("pages_processed")
    if isinstance(pages_processed, bool) or not isinstance(pages_processed, int) or pages_processed <= 0:
        raise DiscoveryPrecheckRequestError("previous result has invalid pages_processed")
    if pages_processed >= MAX_PAGES:
        raise DiscoveryPrecheckRequestError("previous collector already reached the page safety limit")
    return previous


def _allowed_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for record in records:
        tokens = sorted(paper_identity.identity_tokens(record))
        out.append(
            {
                "primary_identity": paper_identity.primary_identity_key(record),
                "identity_tokens": tokens,
                "record": record,
            }
        )
    return out


def _receipt(
    *,
    request_id: str,
    collector_id: str,
    previous_request_id: str | None,
    previous_receipt: str | None,
    run_key: str,
    axis: str,
    target_unseen: int,
    pages_processed: int,
    evaluation_allowed: bool,
    snapshot_source_commit: str | None,
    allowed_records: list[dict[str, Any]],
) -> str:
    payload = {
        "request_id": request_id,
        "collector_id": collector_id,
        "previous_request_id": previous_request_id,
        "previous_receipt": previous_receipt,
        "run_key": run_key,
        "axis": axis,
        "target_unseen": target_unseen,
        "pages_processed": pages_processed,
        "evaluation_allowed": evaluation_allowed,
        "snapshot_source_commit": snapshot_source_commit,
        "allowed_identity_tokens": [row["identity_tokens"] for row in allowed_records],
    }
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _counter(previous: dict[str, Any] | None, key: str) -> int:
    if not previous:
        return 0
    value = previous.get(key, 0)
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def process_request(
    request_path: Path,
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
) -> dict[str, Any]:
    request_path = Path(request_path)
    raw_request = _read_object(request_path)
    request = _validate_request(raw_request)
    previous = _load_previous_result(request_path, request)

    prior_results = list(previous.get("results") or []) if previous else []

    # Revalidate the carried buffer against the latest canonical snapshot/ledger.
    prior_filtered = discovery_search_filter.filter_search_batch(
        prior_results,
        snapshot_dir=Path(snapshot_dir),
        rejection_ledger_path=Path(rejection_ledger_path),
    )
    current_filtered = discovery_search_filter.filter_search_batch(
        request["records"],
        snapshot_dir=Path(snapshot_dir),
        rejection_ledger_path=Path(rejection_ledger_path),
    )

    # A second pass over the small unseen buffers provides the same page-to-page
    # identity/alias collapse that collect_until_unseen() performs internally.
    combined_input = list(prior_filtered["results"]) + list(current_filtered["results"])
    combined = discovery_search_filter.filter_search_batch(
        combined_input,
        snapshot_dir=Path(snapshot_dir),
        rejection_ledger_path=Path(rejection_ledger_path),
    )
    results = list(combined["results"])

    prior_revalidated_filtered_count = len(prior_results) - len(prior_filtered["results"])
    cross_page_duplicate_filtered_count = (
        len(prior_filtered["results"])
        + len(current_filtered["results"])
        - len(results)
    )

    pages_processed = _counter(previous, "pages_processed") + 1
    target_unseen = int(request["target_unseen"])
    target_reached = len(results) >= target_unseen
    max_pages_reached = pages_processed >= MAX_PAGES
    provider_exhausted = not bool(request["provider_has_more"])
    evaluation_allowed = bool(target_reached or provider_exhausted or max_pages_reached)
    decision = "READY_FOR_EVALUATION" if evaluation_allowed else "CONTINUE_FETCH"

    if target_reached:
        stop_reason = "TARGET_REACHED"
    elif provider_exhausted:
        stop_reason = "PROVIDER_EXHAUSTED"
    elif max_pages_reached:
        stop_reason = "MAX_PAGES_REACHED"
    else:
        stop_reason = None

    allowed = _allowed_records(results)
    source_commit = _manifest_source_commit(Path(snapshot_dir))
    receipt = _receipt(
        request_id=request["request_id"],
        collector_id=request["collector_id"],
        previous_request_id=request["previous_request_id"],
        previous_receipt=request["previous_receipt"],
        run_key=request["run_key"],
        axis=request["axis"],
        target_unseen=target_unseen,
        pages_processed=pages_processed,
        evaluation_allowed=evaluation_allowed,
        snapshot_source_commit=source_commit,
        allowed_records=allowed,
    )

    raw_search_result_count = _counter(previous, "raw_search_result_count") + len(request["records"])
    retrieval_duplicate_filtered_count = (
        _counter(previous, "retrieval_duplicate_filtered_count")
        + int(current_filtered["retrieval_duplicate_filtered_count"])
    )
    represented_paper_match_filtered_count = (
        _counter(previous, "represented_paper_match_filtered_count")
        + int(current_filtered["represented_paper_match_filtered_count"])
    )
    rejection_ledger_filtered_count = (
        _counter(previous, "rejection_ledger_filtered_count")
        + int(current_filtered["rejection_ledger_filtered_count"])
    )
    intra_batch_duplicate_filtered_count = (
        _counter(previous, "intra_batch_duplicate_filtered_count")
        + int(current_filtered["intra_batch_duplicate_filtered_count"])
    )
    cumulative_cross_page_duplicate_filtered_count = (
        _counter(previous, "cross_page_duplicate_filtered_count")
        + cross_page_duplicate_filtered_count
    )
    cumulative_prior_revalidated_filtered_count = (
        _counter(previous, "prior_revalidated_filtered_count")
        + prior_revalidated_filtered_count
    )

    if evaluation_allowed:
        next_action = (
            "Candidate evaluation is now allowed. Evaluate only records in results[]; do not re-add "
            "filtered records. When writing submit_discovery_round, reference this final precheck "
            "result_path and receipt."
        )
    else:
        next_action = (
            "Do not evaluate candidates yet. Fetch the next page/cursor/offset or the next equivalent "
            "search window for the SAME collector. Create a NEW immutable precheck request with "
            f"previous_request_id={request['request_id']!r}, previous_receipt={receipt!r}, the same "
            "collector_id/run_key/axis/target_unseen, and the next raw records. Repeat until the "
            "result decision is READY_FOR_EVALUATION."
        )

    return {
        "schema_version": SCHEMA_VERSION,
        "operation": OPERATION,
        "ok": True,
        "request_id": request["request_id"],
        "collector_id": request["collector_id"],
        "previous_request_id": request["previous_request_id"],
        "run_key": request["run_key"],
        "axis": request["axis"],
        "target_unseen": target_unseen,
        "pages_processed": pages_processed,
        "provider_has_more": bool(request["provider_has_more"]),
        "target_reached": target_reached,
        "provider_exhausted": provider_exhausted,
        "max_pages_reached": max_pages_reached,
        "stop_reason": stop_reason,
        "evaluation_allowed": evaluation_allowed,
        "decision": decision,
        "snapshot_source_commit": source_commit,
        "current_raw_search_result_count": len(request["records"]),
        "raw_search_result_count": raw_search_result_count,
        "current_unseen_result_count": int(current_filtered["unseen_result_count"]),
        "unseen_result_count": len(results),
        "retrieval_duplicate_filtered_count": retrieval_duplicate_filtered_count,
        "represented_paper_match_filtered_count": represented_paper_match_filtered_count,
        "rejection_ledger_filtered_count": rejection_ledger_filtered_count,
        "intra_batch_duplicate_filtered_count": intra_batch_duplicate_filtered_count,
        "cross_page_duplicate_filtered_count": cumulative_cross_page_duplicate_filtered_count,
        "prior_revalidated_filtered_count": cumulative_prior_revalidated_filtered_count,
        "results": results,
        "allowed_records": allowed,
        "receipt": receipt,
        "next_action": next_action,
    }


def failure_result(request_path: Path, exc: Exception) -> dict[str, Any]:
    request: dict[str, Any] = {}
    try:
        request = _read_object(request_path)
    except Exception:
        pass
    return {
        "schema_version": SCHEMA_VERSION,
        "operation": OPERATION,
        "ok": False,
        "request_id": request.get("request_id"),
        "collector_id": request.get("collector_id"),
        "run_key": request.get("run_key"),
        "axis": request.get("axis"),
        "error": f"{type(exc).__name__}: {exc}",
        "evaluation_allowed": False,
        "decision": "FIX_REQUEST",
        "next_action": (
            "Fix the precheck request and create a NEW immutable request file. "
            "Do not bypass iterative precheck and do not submit Discovery candidates directly."
        ),
        "recovery_steps": [
            "Keep the failed request unchanged.",
            "Use schema_version=2 and provide collector_id plus explicit provider_has_more.",
            "For the first page omit previous_request_id/previous_receipt.",
            "For later pages reference the immediately preceding successful CONTINUE_FETCH result.",
            "Continue until a workflow result says evaluation_allowed=true and decision=READY_FOR_EVALUATION.",
            "Evaluate only that final result.results[] and reference its result_path/receipt from the new Discovery submission.",
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
