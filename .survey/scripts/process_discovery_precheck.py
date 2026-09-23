#!/usr/bin/env python3
"""Authoritative Discovery retrieval precheck.

Schema v3 is the production path: a request supplies one fixed provider search-result
URL/API query, and this processor drives discovery_search_filter.collect_until_unseen()
across page 1, page 2, ... of that SAME result set before candidate evaluation.

Historical schema-v1/v2 results remain readable by queue_worker for old submissions, but this processor accepts only new schema-v3 requests.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import discovery_provider_adapter  # noqa: E402
import discovery_preload_queue  # noqa: E402
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

    preload_id = request.get("preload_id")
    preload_seed = request.get("preload_seed") is True
    worker_id = str(request.get("worker_id") or "").strip()
    if preload_id is not None:
        preload_id = _safe_id(preload_id, "preload_id")
        if not preload_seed and not worker_id:
            raise DiscoveryPrecheckRequestError(
                "worker_id is required when adopting a Discovery preload"
            )

    out.update(
        {
            "schema_version": 3,
            "provider": provider,
            "source_url": source_url,
            "page_size": page_size,
            "max_pages": max_pages,
            "initial_cursor": initial_cursor,
            "preload_id": preload_id,
            "preload_seed": preload_seed,
            "worker_id": worker_id or None,
        }
    )
    return out


def _validate_request(request: dict[str, Any]) -> dict[str, Any]:
    version = request.get("schema_version")
    if version != SCHEMA_VERSION:
        raise DiscoveryPrecheckRequestError(
            f"schema_version must be exactly {SCHEMA_VERSION}; legacy request schemas are no longer executable"
        )
    return _validate_v3_request(request)


def _manifest_source_commit(snapshot_dir: Path) -> str | None:
    manifest = json.loads((snapshot_dir / "_manifest.json").read_text(encoding="utf-8"))
    value = manifest.get("source_commit")
    return str(value) if value else None


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
    repo_root: Path,
) -> dict[str, Any]:
    live_fetch_page = discovery_provider_adapter.make_fetcher(
        request["provider"],
        request["source_url"],
        page_size=request["page_size"],
    )

    preload_entry: dict[str, Any] | None = None
    preload_source_result: dict[str, Any] | None = None
    preload_cache_used = False
    preload_cached_pages_used = 0

    if request.get("preload_id") and not request.get("preload_seed"):
        preload_entry, preload_source_result = discovery_preload_queue.claim_and_load(
            repo_root,
            request,
        )
        served_cached_page = False

        def fetch_page(cursor: str | None) -> dict[str, Any]:
            nonlocal served_cached_page, preload_cache_used, preload_cached_pages_used
            if not served_cached_page and cursor == request.get("initial_cursor"):
                served_cached_page = True
                preload_cache_used = True
                preload_cached_pages_used = 1
                records = preload_source_result.get("results")
                if not isinstance(records, list):
                    raise DiscoveryPrecheckRequestError(
                        "Discovery preload result is missing results[]"
                    )
                next_cursor = preload_source_result.get("next_cursor")
                if next_cursor is not None and not isinstance(next_cursor, str):
                    raise DiscoveryPrecheckRequestError(
                        "Discovery preload result has invalid next_cursor"
                    )
                return {
                    "records": records,
                    "next_cursor": next_cursor,
                    "page_url": f"preload://{request['preload_id']}",
                    "position": cursor,
                    "provider_progress": preload_source_result.get("provider_progress"),
                }
            return live_fetch_page(cursor)
    else:
        fetch_page = live_fetch_page

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
            "preload_id": request.get("preload_id"),
            "preload_cache_used": preload_cache_used,
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
        "provider_progress": collected.get("provider_progress"),
        "progress_observed_at": datetime.now(timezone.utc).isoformat(),
        "preload_id": request.get("preload_id"),
        "preload_seed": bool(request.get("preload_seed")),
        "preload_cache_used": preload_cache_used,
        "preload_cached_pages_used": preload_cached_pages_used,
        "preload_live_pages_fetched": max(
            int(collected["pages_fetched"]) - preload_cached_pages_used,
            0,
        ),
        "preload_source_request_id": (
            preload_source_result.get("request_id")
            if isinstance(preload_source_result, dict)
            else None
        ),
        "results": results,
        "allowed_records": allowed,
        "receipt": receipt,
        "next_action": (
            (
                "Candidate evaluation is allowed. A Discovery preload supplied the first provider window; "
                "the cached records were re-filtered against this run's current identity snapshot and any "
                "shortfall was topped up from the same fixed source. "
            )
            if preload_cache_used
            else
            "Candidate evaluation is allowed. The precheck itself already followed page/cursor pagination "
            "within the single fixed source_url result set. "
        )
        + "Evaluate only results[] and reference this result_path/receipt from submit_discovery_round.",
    }


def process_request(
    request_path: Path,
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
    repo_root: Path = Path("."),
) -> dict[str, Any]:
    request_path = Path(request_path)
    request = _validate_request(_read_object(request_path))
    snapshot_dir = Path(snapshot_dir)
    rejection_ledger_path = Path(rejection_ledger_path)
    return _process_v3(
        request,
        snapshot_dir=snapshot_dir,
        rejection_ledger_path=rejection_ledger_path,
        repo_root=Path(repo_root),
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
        "preload_id": request.get("preload_id"),
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
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    try:
        result = process_request(
            args.request,
            snapshot_dir=args.snapshot_dir,
            rejection_ledger_path=args.rejection_ledger,
            repo_root=args.repo_root,
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
