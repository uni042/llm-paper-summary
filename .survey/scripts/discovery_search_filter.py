#!/usr/bin/env python3
"""Filter already represented papers from Discovery search-result batches.

This module is the retrieval-stage counterpart to the final Discovery duplicate gate.
It consumes the compact ``work-queue/discovery-identities`` snapshot generated from
``queue_worker.existing_candidate_keys()`` and removes known papers before expensive
candidate evaluation. The final duplicate gate remains authoritative and unchanged.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

import paper_identity
from build_discovery_identity_snapshot import shard_name


class SnapshotUnavailableError(RuntimeError):
    """Raised when the authoritative Discovery precheck snapshot cannot be trusted."""


PageFetcher = Callable[[str | None], dict[str, Any]]


def _load_manifest(snapshot_dir: Path) -> dict[str, Any]:
    snapshot_dir = Path(snapshot_dir)
    manifest_path = snapshot_dir / "_manifest.json"
    if not snapshot_dir.is_dir() or not manifest_path.is_file():
        raise SnapshotUnavailableError(f"Discovery identity snapshot is unavailable: {snapshot_dir}")
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SnapshotUnavailableError(f"Discovery identity manifest is unreadable: {manifest_path}") from exc
    if not isinstance(manifest, dict):
        raise SnapshotUnavailableError("Discovery identity manifest must be an object")
    if manifest.get("source") != "queue_worker.existing_candidate_keys":
        raise SnapshotUnavailableError("Discovery identity manifest has an unexpected source")
    if manifest.get("code_search_is_authority") is not False:
        raise SnapshotUnavailableError("Discovery identity manifest does not disable code-search authority")
    shards = manifest.get("shards")
    if not isinstance(shards, dict):
        raise SnapshotUnavailableError("Discovery identity manifest is missing shard metadata")
    return manifest


def _load_shard(
    snapshot_dir: Path,
    manifest: dict[str, Any],
    name: str,
    cache: dict[str, set[str]],
) -> set[str]:
    if name in cache:
        return cache[name]
    shards = manifest["shards"]
    if name not in shards:
        cache[name] = set()
        return cache[name]
    path = snapshot_dir / name
    if not path.is_file():
        raise SnapshotUnavailableError(f"Manifest-listed Discovery identity shard is missing: {name}")
    try:
        cache[name] = {line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()}
    except OSError as exc:
        raise SnapshotUnavailableError(f"Discovery identity shard is unreadable: {name}") from exc
    return cache[name]


def existing_identity_token(
    record: dict[str, Any],
    *,
    snapshot_dir: Path,
    manifest: dict[str, Any],
    cache: dict[str, set[str]],
) -> str | None:
    """Return one matching authoritative identity token, or ``None`` when unseen."""
    for token in sorted(paper_identity.identity_tokens(record)):
        name = shard_name(token)
        if token in _load_shard(snapshot_dir, manifest, name, cache):
            return token
    return None


def filter_search_batch(
    records: list[dict[str, Any]],
    *,
    snapshot_dir: Path,
    target_unseen: int = 0,
    provider_has_more: bool = False,
    unseen_before_batch: int = 0,
) -> dict[str, Any]:
    """Filter one provider result page before candidate evaluation.

    ``continue_search`` is true only when the caller still needs more unseen results and
    the current provider exposes another page/cursor. If the provider is exhausted while
    the target is still unmet, the caller should switch to another independent search
    axis rather than reintroducing filtered duplicates.
    """
    if target_unseen < 0 or unseen_before_batch < 0:
        raise ValueError("target_unseen and unseen_before_batch must be non-negative")
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise TypeError("records must be a list of objects")

    snapshot_dir = Path(snapshot_dir)
    manifest = _load_manifest(snapshot_dir)
    cache: dict[str, set[str]] = {}
    unseen: list[dict[str, Any]] = []
    duplicate_tokens: list[str] = []
    unresolved_identity_count = 0
    intra_batch_duplicate_filtered_count = 0
    seen_batch_tokens: set[str] = set()

    for record in records:
        tokens = paper_identity.identity_tokens(record)
        if not tokens:
            unresolved_identity_count += 1
        matched = existing_identity_token(
            record,
            snapshot_dir=snapshot_dir,
            manifest=manifest,
            cache=cache,
        )
        if matched:
            duplicate_tokens.append(matched)
            continue

        primary = paper_identity.primary_identity_key(record)
        if primary and primary in seen_batch_tokens:
            intra_batch_duplicate_filtered_count += 1
            continue
        if primary:
            seen_batch_tokens.add(primary)
        unseen.append(record)

    unseen_accumulated_count = unseen_before_batch + len(unseen)
    needs_more = target_unseen > 0 and unseen_accumulated_count < target_unseen
    return {
        "results": unseen,
        "raw_search_result_count": len(records),
        "retrieval_duplicate_filtered_count": len(duplicate_tokens),
        "retrieval_duplicate_tokens": duplicate_tokens,
        "intra_batch_duplicate_filtered_count": intra_batch_duplicate_filtered_count,
        "unresolved_identity_count": unresolved_identity_count,
        "unseen_result_count": len(unseen),
        "unseen_accumulated_count": unseen_accumulated_count,
        "provider_has_more": bool(provider_has_more),
        "continue_search": bool(needs_more and provider_has_more),
        "switch_axis": bool(needs_more and not provider_has_more),
    }


def collect_until_unseen(
    fetch_page: PageFetcher,
    *,
    snapshot_dir: Path,
    target_unseen: int = 20,
    initial_cursor: str | None = None,
    max_pages: int = 100,
) -> dict[str, Any]:
    """Fetch and filter provider pages until an unseen-result buffer is ready.

    ``fetch_page(cursor)`` must return an object with a ``records`` list and a
    ``next_cursor`` value. The collector owns pagination: intermediate provider pages are
    filtered and accumulated internally, and the caller receives only the final unseen
    buffer once ``target_unseen`` has been reached or the provider is exhausted.

    The last fetched page is kept whole. Therefore the returned buffer may be larger than
    ``target_unseen`` when that page crosses the threshold; unseen records are never
    discarded merely to hit an exact batch size.
    """
    if target_unseen <= 0:
        raise ValueError("target_unseen must be greater than zero")
    if max_pages <= 0:
        raise ValueError("max_pages must be greater than zero")

    snapshot_dir = Path(snapshot_dir)
    _load_manifest(snapshot_dir)

    cursor = initial_cursor
    seen_cursors: set[str] = set()
    seen_primary_identities: set[str] = set()
    results: list[dict[str, Any]] = []
    duplicate_tokens: list[str] = []
    raw_search_result_count = 0
    retrieval_duplicate_filtered_count = 0
    intra_batch_duplicate_filtered_count = 0
    cross_page_duplicate_filtered_count = 0
    unresolved_identity_count = 0
    pages_fetched = 0
    next_cursor: str | None = cursor
    provider_exhausted = False
    max_pages_reached = False

    while len(results) < target_unseen:
        if pages_fetched >= max_pages:
            max_pages_reached = True
            break

        page = fetch_page(cursor)
        if not isinstance(page, dict):
            raise TypeError("fetch_page must return an object")
        records = page.get("records")
        if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
            raise TypeError("fetch_page result must contain a records list of objects")
        next_value = page.get("next_cursor")
        if next_value is not None and not isinstance(next_value, str):
            raise TypeError("next_cursor must be a string or null")

        filtered = filter_search_batch(records, snapshot_dir=snapshot_dir)
        pages_fetched += 1
        raw_search_result_count += filtered["raw_search_result_count"]
        retrieval_duplicate_filtered_count += filtered["retrieval_duplicate_filtered_count"]
        duplicate_tokens.extend(filtered["retrieval_duplicate_tokens"])
        intra_batch_duplicate_filtered_count += filtered["intra_batch_duplicate_filtered_count"]
        unresolved_identity_count += filtered["unresolved_identity_count"]

        for record in filtered["results"]:
            primary = paper_identity.primary_identity_key(record)
            if primary and primary in seen_primary_identities:
                cross_page_duplicate_filtered_count += 1
                continue
            if primary:
                seen_primary_identities.add(primary)
            results.append(record)

        next_cursor = next_value
        if len(results) >= target_unseen:
            provider_exhausted = next_cursor is None
            break
        if next_cursor is None:
            provider_exhausted = True
            break
        if next_cursor == cursor or next_cursor in seen_cursors:
            raise ValueError(f"provider returned a repeated next_cursor: {next_cursor}")
        seen_cursors.add(next_cursor)
        cursor = next_cursor

    return {
        "results": results,
        "target_unseen": target_unseen,
        "target_reached": len(results) >= target_unseen,
        "provider_exhausted": provider_exhausted,
        "max_pages_reached": max_pages_reached,
        "next_cursor": next_cursor,
        "pages_fetched": pages_fetched,
        "raw_search_result_count": raw_search_result_count,
        "retrieval_duplicate_filtered_count": retrieval_duplicate_filtered_count,
        "retrieval_duplicate_tokens": duplicate_tokens,
        "intra_batch_duplicate_filtered_count": intra_batch_duplicate_filtered_count,
        "cross_page_duplicate_filtered_count": cross_page_duplicate_filtered_count,
        "unresolved_identity_count": unresolved_identity_count,
        "unseen_result_count": len(results),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", type=Path, default=Path(".survey/work-queue/discovery-identities"))
    parser.add_argument("--target-unseen", type=int, default=0)
    parser.add_argument("--unseen-before-batch", type=int, default=0)
    parser.add_argument("--provider-has-more", action="store_true")
    parser.add_argument("--input", type=Path, help="JSON array of search-result records; stdin when omitted")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8") if args.input else sys.stdin.read()
    records = json.loads(text)
    result = filter_search_batch(
        records,
        snapshot_dir=args.snapshot_dir,
        target_unseen=args.target_unseen,
        provider_has_more=args.provider_has_more,
        unseen_before_batch=args.unseen_before_batch,
    )
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
