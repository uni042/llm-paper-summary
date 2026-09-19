#!/usr/bin/env python3
"""Authoritative Discovery retrieval precheck.

Schema v3 is the production path: a request supplies one fixed provider search-result
URL/API query, and this processor drives discovery_search_filter.collect_until_unseen()
across page 1, page 2, ... of that SAME result set before candidate evaluation.

Schema v2 remains readable only for already-created transitional requests.
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

import discovery_provider_adapter  # noqa: E402
import discovery_search_filter  # noqa: E402
import paper_identity  # noqa: E402

SAFE_REQUEST_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
OPERATION = "precheck_discovery_candidates"
SCHEMA_VERSION = 3
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


def _target(request: dict[str, Any]) -> int:
    target = request.get("target_unseen", DEFAULT_TARGET_UNSEEN)
    if isinstance(target, bool) or not isinstance(target, int) or target <= 0 or target > MAX_TARGET_UNSEEN:
        raise DiscoveryPrecheckRequestError(
            f"target_unseen must be an integer between 1 and {MAX_TARGET_UNSEEN}"
        )
    return target


def _base_fields(request: dict[str, Any]) -> dict[str, Any]:
    if request.get("operation") != OPERATION:
        raise DiscoveryPrecheckRequestError(f"operation must be {OPERATION!r}")
    request_id = _safe_id(request.get("request_id"), "request_id")
    collector_id = _safe_id(request.get("collector_id"), "collector_id")
    run_key = str(request.get("run_key") or "").strip()
    axis = str(request.get("axis") or "").strip()
    if not run_key:
        raise DiscoveryPrecheckRequestError("run_key is required")
    if not axis:
        raise DiscoveryPrecheckRequestError("axis is required")
    return {
        "request_id": request_id,
        "collector_id": collector_id,
        "run_key": run_key,
        "axis": axis,
        "target_unseen": _target(request),
    }


def _validate_v3_request(request: dict[str, Any]) -> dict[str, Any]:
    out = _base_fields(request)
    provider = str(request.get("provider") or "").strip()
    source_url = str(request.get("source_url") or "").strip()
    if not provider:
        raise DiscoveryPrecheckRequestError("schema-v3 request requires provider")
    if not source_url:
        raise DiscoveryPrecheckRequestError("schema-v3 request requires source_url")
    if "records" in request:
        raise DiscoveryPrecheckRequestError(
            "schema-v3 request must not contain worker-supplied records; precheck fetches provider pages itself"
        )
    page_size = request.get("page_size", 100)
    if isinstance(page_size, bool) or not isinstance(page_size, int) or page_size <= 0 or page_size > 100:
        raise DiscoveryPrecheckRequestError("page_size must be an integer between 1 and 100")
    max_pages = request.get("max_pages", MAX_PAGES)
    if isinstance(max_pages, bool) or not isinstance(max_pages, int) or max_pages <= 0 or max_pages > MAX_PAGES:
        raise DiscoveryPrecheckRequestError(f"max_pages must be an integer between 1 and {MAX_PAGES}")
    initial_cursor = request.get("initial_cursor")
    if initial_cursor is not None and not isinstance(initial_cursor, str):
        raise DiscoveryPrecheckRequestError("initial_cursor must be a string or null")
    out.update(
        {
            "schema_version": 3,
            "provider": provider,
            "source_url": source_url,
            "page_size": page_size,
            "max_pages": max_pages,
            "initial_cursor": initial_cursor,
        }
    )
    return out


def _validate_v2_request(request: dict[str, Any]) -> dict[str, Any]:
    out = _base_fields(request)
    records = request.get("records")
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise DiscoveryPrecheckRequestError("schema-v2 records must be a list of objects")
    if len(records) > 100:
        raise DiscoveryPrecheckRequestError("schema-v2 records may contain at most 100 search results")
    provider_has_more = request.get("provider_has_more")
    if not isinstance(provider_has_more, bool):
        raise DiscoveryPrecheckRequestError("schema-v2 provider_has_more must be an explicit boolean")

    previous_request_id = request.get("previous_request_id")
    previous_receipt = request.get("previous_receipt")
    if previous_request_id is None and previous_receipt is None:
        previous_request_id = previous_receipt = None
    elif previous_request_id is None or previous_receipt is None:
        raise DiscoveryPrecheckRequestError(
            "schema-v2 previous_request_id and previous_receipt must be provided together"
        )
    else:
        previous_request_id = _safe_id(previous_request_id, "previous_request_id")
        previous_receipt = str(previous_receipt or "").strip()
        if not previous_receipt.startswith("sha256:"):
            raise DiscoveryPrecheckRequestError("previous_receipt must be a sha256 receipt")
    out.update(
        {
            "schema_version": 2,
            "records": records,
            "provider_has_more": provider_has_more,
            "previous_request_id": previous_request_id,
            "previous_receipt": previous_receipt,
        }
    )
    return out


def _validate_request(request: dict[str, Any]) -> dict[str, Any]:
    version = request.get("schema_version")
    if isinstance(version, bool) or not isinstance(version, int):
        raise DiscoveryPrecheckRequestError("schema_version must be an integer")
    if version >= 3:
        return _validate_v3_request(request)
    if version == 2:
        return _validate_v2_request(request)
    raise DiscoveryPrecheckRequestError("schema_version must be >= 2")


def _manifest_source_commit(snapshot_dir: Path) -> str | None:
    manifest = json.loads((snapshot_dir / "_manifest.json").read_text(encoding="utf-8"))
    value = manifest.get("source_commit")
    return str(value) if value else None


def _results_dir(request_path: Path) -> Path:
    if request_path.parent.name == "requests":
        return request_path.parent.parent / "results"
    return request_path.parent / "results"


def _allowed_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for record in records:
        out.append(
            {
                "primary_identity": paper_identity.primary_identity_key(record),
                "identity_tokens": sorted(paper_identity.identity_tokens(record)),
                "record": record,
            }
        )
    return out


def _receipt(payload: dict[str, Any]) -> str:
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def _process_v3(
    request: dict[str, Any],
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
) -> dict[str, Any]:
    fetch_page = discovery_provider_adapter.make_fetcher(
        request["provider"],
        request["source_url"],
        page_size=request["page_size"],
    )
    collected = discovery_search_filter.collect_until_unseen(
        fetch_page,
        snapshot_dir=snapshot_dir,
        rejection_ledger_path=rejection_ledger_path,
        target_unseen=request["target_unseen"],
        initial_cursor=request["initial_cursor"],
        max_pages=request["max_pages"],
    )
    results = list(collected["results"])
    allowed = _allowed_records(results)
    source_commit = _manifest_source_commit(snapshot_dir)
    receipt = _receipt(
        {
            "schema_version": 3,
            "request_id": request["request_id"],
            "collector_id": request["collector_id"],
            "run_key": request["run_key"],
            "axis": request["axis"],
            "provider": request["provider"],
            "source_url": request["source_url"],
            "target_unseen": request["target_unseen"],
            "pages_fetched": collected["pages_fetched"],
            "snapshot_source_commit": source_commit,
            "allowed_identity_tokens": [row["identity_tokens"] for row in allowed],
        }
    )
    if collected["target_reached"]:
        stop_reason = "TARGET_REACHED"
    elif collected["provider_exhausted"]:
        stop_reason = "PROVIDER_EXHAUSTED"
    elif collected["max_pages_reached"]:
        stop_reason = "MAX_PAGES_REACHED"
    else:
        stop_reason = "COLLECTOR_STOPPED"

    return {
        "schema_version": 3,
        "operation": OPERATION,
        "ok": True,
        "request_id": request["request_id"],
        "collector_id": request["collector_id"],
        "run_key": request["run_key"],
        "axis": request["axis"],
        "provider": request["provider"],
        "source_url": request["source_url"],
        "target_unseen": request["target_unseen"],
        "page_size": request["page_size"],
        "pages_fetched": collected["pages_fetched"],
        "next_cursor": collected["next_cursor"],
        "target_reached": collected["target_reached"],
        "provider_exhausted": collected["provider_exhausted"],
        "max_pages_reached": collected["max_pages_reached"],
        "stop_reason": stop_reason,
        "evaluation_allowed": True,
        "decision": "READY_FOR_EVALUATION",
        "snapshot_source_commit": source_commit,
        "raw_search_result_count": collected["raw_search_result_count"],
        "retrieval_duplicate_filtered_count": collected["retrieval_duplicate_filtered_count"],
        "represented_paper_match_filtered_count": collected["represented_paper_match_filtered_count"],
        "rejection_ledger_filtered_count": collected["rejection_ledger_filtered_count"],
        "intra_batch_duplicate_filtered_count": collected["intra_batch_duplicate_filtered_count"],
        "intra_batch_alias_duplicate_filtered_count": collected["intra_batch_alias_duplicate_filtered_count"],
        "cross_page_duplicate_filtered_count": collected["cross_page_duplicate_filtered_count"],
        "cross_page_alias_duplicate_filtered_count": collected["cross_page_alias_duplicate_filtered_count"],
        "unresolved_identity_count": collected["unresolved_identity_count"],
        "unseen_result_count": collected["unseen_result_count"],
        "results": results,
        "allowed_records": allowed,
        "receipt": receipt,
        "next_action": (
            "Candidate evaluation is allowed. The precheck itself already followed page/cursor pagination "
            "within the single fixed source_url result set. Evaluate only results[] and reference this "
            "result_path/receipt from submit_discovery_round."
        ),
    }


def _load_previous_v2(request_path: Path, request: dict[str, Any]) -> dict[str, Any] | None:
    previous_request_id = request["previous_request_id"]
    if previous_request_id is None:
        return None
    path = _results_dir(request_path) / f"{previous_request_id}.json"
    if not path.is_file():
        raise DiscoveryPrecheckRequestError(f"previous precheck result does not exist yet: {previous_request_id}")
    previous = _read_object(path)
    if previous.get("ok") is not True or previous.get("operation") != OPERATION:
        raise DiscoveryPrecheckRequestError("previous precheck result is not successful")
    if int(previous.get("schema_version") or 0) != 2:
        raise DiscoveryPrecheckRequestError("schema-v2 request may only chain from schema-v2 result")
    if str(previous.get("request_id") or "") != previous_request_id:
        raise DiscoveryPrecheckRequestError("previous result request_id mismatch")
    if str(previous.get("receipt") or "") != request["previous_receipt"]:
        raise DiscoveryPrecheckRequestError("previous precheck receipt mismatch")
    for field in ("collector_id", "run_key", "axis"):
        if str(previous.get(field) or "") != str(request[field]):
            raise DiscoveryPrecheckRequestError(f"previous result {field} mismatch")
    if previous.get("evaluation_allowed") is not False or previous.get("decision") != "CONTINUE_FETCH":
        raise DiscoveryPrecheckRequestError("previous schema-v2 result is already terminal")
    return previous


def _process_v2(
    request_path: Path,
    request: dict[str, Any],
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
) -> dict[str, Any]:
    """Compatibility for already-created transitional page-batch requests."""
    previous = _load_previous_v2(request_path, request)
    prior_results = list(previous.get("results") or []) if previous else []
    prior_filtered = discovery_search_filter.filter_search_batch(
        prior_results,
        snapshot_dir=snapshot_dir,
        rejection_ledger_path=rejection_ledger_path,
    )
    current_filtered = discovery_search_filter.filter_search_batch(
        request["records"],
        snapshot_dir=snapshot_dir,
        rejection_ledger_path=rejection_ledger_path,
    )
    combined = discovery_search_filter.filter_search_batch(
        list(prior_filtered["results"]) + list(current_filtered["results"]),
        snapshot_dir=snapshot_dir,
        rejection_ledger_path=rejection_ledger_path,
    )
    results = list(combined["results"])
    pages_processed = int(previous.get("pages_processed") or 0) + 1 if previous else 1
    target_reached = len(results) >= request["target_unseen"]
    provider_exhausted = not request["provider_has_more"]
    max_pages_reached = pages_processed >= MAX_PAGES
    evaluation_allowed = target_reached or provider_exhausted or max_pages_reached
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
    source_commit = _manifest_source_commit(snapshot_dir)
    receipt = _receipt(
        {
            "schema_version": 2,
            "request_id": request["request_id"],
            "collector_id": request["collector_id"],
            "previous_request_id": request["previous_request_id"],
            "previous_receipt": request["previous_receipt"],
            "run_key": request["run_key"],
            "axis": request["axis"],
            "pages_processed": pages_processed,
            "evaluation_allowed": evaluation_allowed,
            "snapshot_source_commit": source_commit,
            "allowed_identity_tokens": [row["identity_tokens"] for row in allowed],
        }
    )
    return {
        "schema_version": 2,
        "operation": OPERATION,
        "ok": True,
        "request_id": request["request_id"],
        "collector_id": request["collector_id"],
        "previous_request_id": request["previous_request_id"],
        "run_key": request["run_key"],
        "axis": request["axis"],
        "target_unseen": request["target_unseen"],
        "pages_processed": pages_processed,
        "provider_has_more": request["provider_has_more"],
        "target_reached": target_reached,
        "provider_exhausted": provider_exhausted,
        "max_pages_reached": max_pages_reached,
        "stop_reason": stop_reason,
        "evaluation_allowed": evaluation_allowed,
        "decision": decision,
        "snapshot_source_commit": source_commit,
        "raw_search_result_count": (int(previous.get("raw_search_result_count") or 0) if previous else 0)
        + len(request["records"]),
        "retrieval_duplicate_filtered_count": (
            int(previous.get("retrieval_duplicate_filtered_count") or 0) if previous else 0
        ) + int(current_filtered["retrieval_duplicate_filtered_count"]),
        "represented_paper_match_filtered_count": (
            int(previous.get("represented_paper_match_filtered_count") or 0) if previous else 0
        ) + int(current_filtered["represented_paper_match_filtered_count"]),
        "rejection_ledger_filtered_count": (
            int(previous.get("rejection_ledger_filtered_count") or 0) if previous else 0
        ) + int(current_filtered["rejection_ledger_filtered_count"]),
        "intra_batch_duplicate_filtered_count": (
            int(previous.get("intra_batch_duplicate_filtered_count") or 0) if previous else 0
        ) + int(current_filtered["intra_batch_duplicate_filtered_count"]),
        "cross_page_duplicate_filtered_count": (
            int(previous.get("cross_page_duplicate_filtered_count") or 0) if previous else 0
        ) + len(prior_filtered["results"]) + len(current_filtered["results"]) - len(results),
        "unseen_result_count": len(results),
        "results": results,
        "allowed_records": allowed,
        "receipt": receipt,
        "next_action": (
            "Legacy schema-v2 result. Do not use this path for new Discovery work. "
            + (
                "Evaluate only results[] and migrate the next round to schema v3."
                if evaluation_allowed
                else "Finish this already-created chain only; new rounds must use schema v3 source_url pagination."
            )
        ),
    }


def process_request(
    request_path: Path,
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
) -> dict[str, Any]:
    request_path = Path(request_path)
    request = _validate_request(_read_object(request_path))
    snapshot_dir = Path(snapshot_dir)
    rejection_ledger_path = Path(rejection_ledger_path)
    if request["schema_version"] >= 3:
        return _process_v3(
            request,
            snapshot_dir=snapshot_dir,
            rejection_ledger_path=rejection_ledger_path,
        )
    return _process_v2(
        request_path,
        request,
        snapshot_dir=snapshot_dir,
        rejection_ledger_path=rejection_ledger_path,
    )


def failure_result(request_path: Path, exc: Exception) -> dict[str, Any]:
    request: dict[str, Any] = {}
    try:
        request = _read_object(request_path)
    except Exception:
        pass
    version = request.get("schema_version")
    schema = version if isinstance(version, int) and not isinstance(version, bool) else SCHEMA_VERSION
    return {
        "schema_version": schema,
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
            "Create a NEW schema-v3 precheck request with one fixed provider search source_url/API query. "
            "Do not supply hand-picked records and do not emulate pagination by changing the query."
        ),
        "recovery_steps": [
            "Keep the failed request unchanged.",
            "Use schema_version=3.",
            "Provide provider, source_url, collector_id, run_key, axis, and optional target_unseen/page_size.",
            "The source_url must identify one fixed result set; the precheck will fetch page 1, page 2, and later pages itself.",
            "If that result set is exhausted below target_unseen, accept the smaller buffer and start a separate Discovery round for a different query/axis.",
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
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
