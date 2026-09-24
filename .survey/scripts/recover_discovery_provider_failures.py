#!/usr/bin/env python3
"""Create one canonical provider-failover request for failed normal Discovery search.

The failed request/result remain immutable evidence.  This helper creates a NEW
schema-v3 request only for a foreground Semantic Scholar search failure that can be
mapped to the same textual query on OpenAlex.  Citation requests and preload seeds
are never rewritten or silently rerouted.

The replacement request is deterministic per parent request, so retries and push
races are idempotent.  Verification treats the parent as recovered only after the
replacement has an ok=true, evaluation_allowed=true result.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qs, urlencode, urlparse

REQUEST_ROOT = Path(".survey/work-queue/discovery-precheck/requests")
RESULT_ROOT = Path(".survey/work-queue/discovery-precheck/results")
FAILOVER_PROVIDER = "openalex"
RETRYABLE_ERROR_TOKENS = (
    "http error 429",
    "http 429",
    "rate-limit",
    "rate limit",
    "rate-limit retries exhausted",
    "semantic scholar page fetch failed",
    "unsupported semantic scholar paper endpoint",
)


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write_create_only(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing != text:
            raise ValueError(f"refusing to overwrite mismatched failover request: {path}")
        return
    path.write_text(text, encoding="utf-8")


def _request_paths(repo_root: Path, requests_file: Path | None) -> list[Path]:
    root = repo_root.resolve()
    if requests_file is None:
        folder = root / REQUEST_ROOT
        return sorted(path.relative_to(root) for path in folder.glob("*.json")) if folder.is_dir() else []
    return [
        Path(line.strip())
        for line in requests_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _query_from_semantic_scholar(source_url: str) -> str | None:
    try:
        parsed = urlparse(source_url)
    except ValueError:
        return None
    if parsed.netloc.casefold() not in {"api.semanticscholar.org", "www.semanticscholar.org", "semanticscholar.org"}:
        return None
    path = parsed.path.rstrip("/").casefold()
    if path.endswith("/citations") or path.endswith("/references"):
        return None
    if "search" not in path:
        return None
    qs = parse_qs(parsed.query, keep_blank_values=True)
    query = (qs.get("query") or qs.get("q") or [""])[0].strip()
    return query or None


def _retryable(request: dict[str, Any], result: dict[str, Any]) -> tuple[bool, str | None]:
    if request.get("preload_seed") is True or request.get("preload_id"):
        return False, None
    if str(request.get("provider") or "").strip().casefold() not in {"semantic_scholar", "semanticscholar", "s2"}:
        return False, None
    if result.get("ok") is True:
        return False, None
    if str(result.get("decision") or "") != "FIX_REQUEST":
        return False, None
    query = _query_from_semantic_scholar(str(request.get("source_url") or ""))
    if not query:
        return False, None
    error = str(result.get("error") or "").casefold()
    if not any(token in error for token in RETRYABLE_ERROR_TOKENS):
        return False, None
    return True, query


def _child_id(parent_request_id: str, query: str) -> str:
    digest = hashlib.sha256(
        f"{parent_request_id}\n{FAILOVER_PROVIDER}\n{query}".encode("utf-8")
    ).hexdigest()[:24]
    return f"auto-provider-failover-{digest}"


def _child_request(parent: dict[str, Any], query: str) -> dict[str, Any]:
    parent_id = str(parent["request_id"])
    child_id = _child_id(parent_id, query)
    source_url = "https://api.openalex.org/works?" + urlencode({"search": query})
    collector = str(parent.get("collector_id") or parent_id)
    payload: dict[str, Any] = {
        "schema_version": 3,
        "operation": "precheck_discovery_candidates",
        "request_id": child_id,
        "collector_id": f"{collector}-openalex-failover"[:160],
        "run_key": str(parent.get("run_key") or ""),
        "axis": str(parent.get("axis") or "normal-search") + " [OpenAlex provider failover]",
        "provider": FAILOVER_PROVIDER,
        "source_url": source_url,
        "target_unseen": int(parent.get("target_unseen") or 20),
        "page_size": min(max(int(parent.get("page_size") or 20), 1), 100),
        "max_pages": min(max(int(parent.get("max_pages") or 1), 1), 25),
        "initial_cursor": None,
        "provider_failover_parent_request_id": parent_id,
        "provider_failover_from": str(parent.get("provider") or "semantic_scholar"),
        "provider_failover_index": 1,
    }
    for key in ("worker_id", "worker_kind", "scheduled_slot", "actual_invocation_start"):
        value = parent.get(key)
        if value not in (None, ""):
            payload[key] = value
    return payload


def _child_status(root: Path, child: dict[str, Any]) -> str:
    request_id = str(child["request_id"])
    result = _read(root / RESULT_ROOT / f"{request_id}.json", {})
    if isinstance(result, dict) and result.get("ok") is True and result.get("evaluation_allowed") is True:
        return "success"
    if isinstance(result, dict) and result:
        return "failed"
    return "pending"


def recover(
    repo_root: Path,
    request_paths: Iterable[Path],
    *,
    create: bool,
) -> dict[str, Any]:
    root = repo_root.resolve()
    retry_paths: list[str] = []
    rows: list[dict[str, Any]] = []
    unresolved = 0

    for rel in request_paths:
        path = rel if rel.is_absolute() else root / rel
        request = _read(path, {})
        if not isinstance(request, dict):
            unresolved += 1
            rows.append({"request": str(rel), "status": "invalid_request"})
            continue
        request_id = str(request.get("request_id") or path.stem)
        result = _read(root / RESULT_ROOT / f"{request_id}.json", {})
        if isinstance(result, dict) and result.get("ok") is True:
            rows.append({"request_id": request_id, "status": "success"})
            continue

        eligible, query = _retryable(request, result if isinstance(result, dict) else {})
        if not eligible or query is None:
            unresolved += 1
            rows.append({"request_id": request_id, "status": "unresolved_non_failover"})
            continue

        child = _child_request(request, query)
        child_id = str(child["request_id"])
        child_rel = REQUEST_ROOT / f"{child_id}.json"
        if create:
            _write_create_only(root / child_rel, child)
        status = _child_status(root, child)
        if status == "success":
            rows.append({
                "request_id": request_id,
                "status": "recovered_by_provider_failover",
                "failover_request_id": child_id,
            })
            continue
        if status == "pending":
            retry_paths.append(child_rel.as_posix())
            rows.append({
                "request_id": request_id,
                "status": "provider_failover_pending",
                "failover_request_id": child_id,
            })
            continue
        unresolved += 1
        rows.append({
            "request_id": request_id,
            "status": "provider_failover_failed",
            "failover_request_id": child_id,
        })

    return {
        "ok": unresolved == 0 and not retry_paths,
        "unresolved_count": unresolved,
        "pending_failover_count": len(retry_paths),
        "retry_request_paths": retry_paths,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--requests-file", type=Path)
    parser.add_argument("--output-requests-file", type=Path)
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    paths = _request_paths(args.repo_root, args.requests_file)
    result = recover(args.repo_root, paths, create=not args.verify_only)
    if args.output_requests_file is not None:
        args.output_requests_file.parent.mkdir(parents=True, exist_ok=True)
        args.output_requests_file.write_text(
            "".join(f"{path}\n" for path in result["retry_request_paths"]),
            encoding="utf-8",
        )
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    if args.verify_only:
        return 0 if result["unresolved_count"] == 0 and result["pending_failover_count"] == 0 else 1
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
