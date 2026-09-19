#!/usr/bin/env python3
"""Filter already represented or previously rejected papers from Discovery search.

This module is the retrieval-stage counterpart to the final Discovery duplicate gate.
It consumes the compact ``work-queue/discovery-identities`` snapshot generated from
``queue_worker.existing_candidate_keys()``, its paper-level alias resolver, and the
separately derived Discovery candidate-evaluation rejection ledger. All are applied
before expensive candidate evaluation. The final duplicate gate remains authoritative
and unchanged.
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
    """Raised when an authoritative Discovery exclusion source cannot be trusted."""


PageFetcher = Callable[[str | None], dict[str, Any]]
DEFAULT_PREFETCH_UNSEEN = 20
REJECTION_LEDGER_SOURCE = "immutable_discovery_submissions.rejected_candidates"


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


def _load_represented_resolver(snapshot_dir: Path, manifest: dict[str, Any]) -> dict[str, Any] | None:
    """Load the optional paper-level alias resolver published by schema-v2 snapshots."""
    name = manifest.get("represented_resolver_file")
    if name is None:
        return None
    if not isinstance(name, str) or not name.strip() or Path(name).name != name:
        raise SnapshotUnavailableError("Discovery identity manifest has an invalid represented resolver path")
    path = Path(snapshot_dir) / name
    if not path.is_file():
        raise SnapshotUnavailableError(f"Manifest-listed represented-paper resolver is missing: {name}")
    try:
        resolver = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SnapshotUnavailableError(f"Represented-paper resolver is unreadable: {path}") from exc
    if not isinstance(resolver, dict):
        raise SnapshotUnavailableError("Represented-paper resolver must be an object")
    if not isinstance(resolver.get("papers"), dict):
        raise SnapshotUnavailableError("Represented-paper resolver is missing papers")
    if not isinstance(resolver.get("alias_to_paper"), dict):
        raise SnapshotUnavailableError("Represented-paper resolver is missing aliases")
    if not isinstance(resolver.get("title_hash_to_paper"), dict):
        raise SnapshotUnavailableError("Represented-paper resolver is missing title hashes")
    return resolver


def _load_rejection_tokens(snapshot_dir: Path, rejection_ledger_path: Path | None = None) -> set[str]:
    path = Path(rejection_ledger_path) if rejection_ledger_path is not None else Path(snapshot_dir).parent / "discovery-rejections.json"
    if not path.exists():
        return set()
    try:
        ledger = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SnapshotUnavailableError(f"Discovery rejection ledger is unreadable: {path}") from exc
    if not isinstance(ledger, dict):
        raise SnapshotUnavailableError("Discovery rejection ledger must be an object")
    if ledger.get("source") != REJECTION_LEDGER_SOURCE:
        raise SnapshotUnavailableError("Discovery rejection ledger has an unexpected source")
    records = ledger.get("records")
    if not isinstance(records, dict):
        raise SnapshotUnavailableError("Discovery rejection ledger is missing records")

    tokens: set[str] = set()
    for primary, record in records.items():
        if isinstance(primary, str) and primary:
            tokens.add(primary)
        if not isinstance(record, dict):
            continue
        values = record.get("identity_tokens")
        if isinstance(values, list):
            tokens.update(value for value in values if isinstance(value, str) and value)
    return tokens


def existing_identity_token(
    record: dict[str, Any],
    *,
    snapshot_dir: Path,
    manifest: dict[str, Any],
    cache: dict[str, set[str]],
) -> str | None:
    """Return one matching authoritative represented-paper token, or ``None``."""
    for token in sorted(paper_identity.identity_tokens(record)):
        name = shard_name(token)
        if token in _load_shard(snapshot_dir, manifest, name, cache):
            return token
    return None


def filter_search_batch(
    records: list[dict[str, Any]],
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path | None = None,
    target_unseen: int = 0,
    provider_has_more: bool = False,
    unseen_before_batch: int = 0,
) -> dict[str, Any]:
    """Filter one provider result page before candidate evaluation.

    Papers already represented in the repository and papers durably rejected by prior
    candidate evaluation are both excluded. Exact token checks run first; the represented-
    paper resolver then catches alias/title variants, including only high-confidence ID-less
    fuzzy title matches. The same alias rules also collapse duplicate provider records within
    one batch before they enter the candidate buffer.
    """
    if target_unseen < 0 or unseen_before_batch < 0:
        raise ValueError("target_unseen and unseen_before_batch must be non-negative")
    if not isinstance(records, list) or any(not isinstance(record, dict) for record in records):
        raise TypeError("records must be a list of objects")

    snapshot_dir = Path(snapshot_dir)
    manifest = _load_manifest(snapshot_dir)
    resolver = _load_represented_resolver(snapshot_dir, manifest)
    rejection_tokens = _load_rejection_tokens(snapshot_dir, rejection_ledger_path)
    cache: dict[str, set[str]] = {}
    unseen: list[dict[str, Any]] = []
    duplicate_tokens: list[str] = []
    represented_paper_keys: list[str] = []
    represented_match_types: list[str] = []
    rejection_filtered_tokens: list[str] = []
    unresolved_identity_count = 0
    intra_batch_duplicate_filtered_count = 0
    intra_batch_alias_duplicate_filtered_count = 0
    seen_batch_tokens: set[str] = set()
    seen_batch_records: list[dict[str, Any]] = []

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

        represented_match = paper_identity.match_represented_paper(record, resolver) if resolver else None
        if represented_match:
            represented_paper_keys.append(str(represented_match["paper_key"]))
            represented_match_types.append(str(represented_match["match_type"]))
            continue

        rejected_match = next(iter(sorted(tokens & rejection_tokens)), None)
        if rejected_match:
            rejection_filtered_tokens.append(rejected_match)
            continue

        primary = paper_identity.primary_identity_key(record)
        if primary and primary in seen_batch_tokens:
            intra_batch_duplicate_filtered_count += 1
            continue
        if seen_batch_records:
            batch_resolver = paper_identity.build_represented_resolver(seen_batch_records)
            if paper_identity.match_represented_paper(record, batch_resolver):
                intra_batch_duplicate_filtered_count += 1
                intra_batch_alias_duplicate_filtered_count += 1
                continue
        if primary:
            seen_batch_tokens.add(primary)
        seen_batch_records.append(record)
        unseen.append(record)

    unseen_accumulated_count = unseen_before_batch + len(unseen)
    needs_more = target_unseen > 0 and unseen_accumulated_count < target_unseen
    return {
        "results": unseen,
        "raw_search_result_count": len(records),
        "retrieval_duplicate_filtered_count": len(duplicate_tokens),
        "retrieval_duplicate_tokens": duplicate_tokens,
        "represented_paper_match_filtered_count": len(represented_paper_keys),
        "represented_paper_keys": represented_paper_keys,
        "represented_paper_match_types": represented_match_types,
        "rejection_ledger_filtered_count": len(rejection_filtered_tokens),
        "rejection_ledger_filtered_tokens": rejection_filtered_tokens,
        "intra_batch_duplicate_filtered_count": intra_batch_duplicate_filtered_count,
        "intra_batch_alias_duplicate_filtered_count": intra_batch_alias_duplicate_filtered_count,
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
    rejection_ledger_path: Path | None = None,
    target_unseen: int = DEFAULT_PREFETCH_UNSEEN,
    initial_cursor: str | None = None,
    max_pages: int = 100,
) -> dict[str, Any]:
    """Fetch/filter provider pages until an unseen-result buffer is ready.

    ``fetch_page(cursor)`` returns an object with a ``records`` list and a
    ``next_cursor`` value. Intermediate pages are filtered and accumulated internally;
    the caller receives only the final buffer once ``target_unseen`` has been reached or
    the provider is exhausted. The default threshold is twenty unseen papers.
    """
    if target_unseen <= 0:
        raise ValueError("target_unseen must be greater than zero")
    if max_pages <= 0:
        raise ValueError("max_pages must be greater than zero")

    snapshot_dir = Path(snapshot_dir)
    manifest = _load_manifest(snapshot_dir)
    _load_represented_resolver(snapshot_dir, manifest)
    _load_rejection_tokens(snapshot_dir, rejection_ledger_path)

    cursor = initial_cursor
    seen_cursors: set[str] = set()
    seen_primary_identities: set[str] = set()
    seen_result_records: list[dict[str, Any]] = []
    results: list[dict[str, Any]] = []
    duplicate_tokens: list[str] = []
    represented_paper_keys: list[str] = []
    represented_match_types: list[str] = []
    rejection_filtered_tokens: list[str] = []
    raw_search_result_count = 0
    retrieval_duplicate_filtered_count = 0
    represented_paper_match_filtered_count = 0
    rejection_ledger_filtered_count = 0
    intra_batch_duplicate_filtered_count = 0
    intra_batch_alias_duplicate_filtered_count = 0
    cross_page_duplicate_filtered_count = 0
    cross_page_alias_duplicate_filtered_count = 0
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

        filtered = filter_search_batch(
            records,
            snapshot_dir=snapshot_dir,
            rejection_ledger_path=rejection_ledger_path,
        )
        pages_fetched += 1
        raw_search_result_count += filtered["raw_search_result_count"]
        retrieval_duplicate_filtered_count += filtered["retrieval_duplicate_filtered_count"]
        duplicate_tokens.extend(filtered["retrieval_duplicate_tokens"])
        represented_paper_match_filtered_count += filtered["represented_paper_match_filtered_count"]
        represented_paper_keys.extend(filtered["represented_paper_keys"])
        represented_match_types.extend(filtered["represented_paper_match_types"])
        rejection_ledger_filtered_count += filtered["rejection_ledger_filtered_count"]
        rejection_filtered_tokens.extend(filtered["rejection_ledger_filtered_tokens"])
        intra_batch_duplicate_filtered_count += filtered["intra_batch_duplicate_filtered_count"]
        intra_batch_alias_duplicate_filtered_count += filtered["intra_batch_alias_duplicate_filtered_count"]
        unresolved_identity_count += filtered["unresolved_identity_count"]

        for record in filtered["results"]:
            primary = paper_identity.primary_identity_key(record)
            if primary and primary in seen_primary_identities:
                cross_page_duplicate_filtered_count += 1
                continue
            if seen_result_records:
                run_resolver = paper_identity.build_represented_resolver(seen_result_records)
                if paper_identity.match_represented_paper(record, run_resolver):
                    cross_page_duplicate_filtered_count += 1
                    cross_page_alias_duplicate_filtered_count += 1
                    continue
            if primary:
                seen_primary_identities.add(primary)
            seen_result_records.append(record)
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
        "represented_paper_match_filtered_count": represented_paper_match_filtered_count,
        "represented_paper_keys": represented_paper_keys,
        "represented_paper_match_types": represented_match_types,
        "rejection_ledger_filtered_count": rejection_ledger_filtered_count,
        "rejection_ledger_filtered_tokens": rejection_filtered_tokens,
        "intra_batch_duplicate_filtered_count": intra_batch_duplicate_filtered_count,
        "intra_batch_alias_duplicate_filtered_count": intra_batch_alias_duplicate_filtered_count,
        "cross_page_duplicate_filtered_count": cross_page_duplicate_filtered_count,
        "cross_page_alias_duplicate_filtered_count": cross_page_alias_duplicate_filtered_count,
        "unresolved_identity_count": unresolved_identity_count,
        "unseen_result_count": len(results),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-dir", type=Path, default=Path(".survey/work-queue/discovery-identities"))
    parser.add_argument("--rejection-ledger", type=Path)
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
        rejection_ledger_path=args.rejection_ledger,
        target_unseen=args.target_unseen,
        provider_has_more=args.provider_has_more,
        unseen_before_batch=args.unseen_before_batch,
    )
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
