#!/usr/bin/env python3
"""Build a ranked Discovery pool from structured references in collected papers.

The pool is intentionally local and durable:
- every structured reference in papers/{inference,training,survey} is considered;
- references already represented by collected papers are removed;
- papers durably marked unrelated are removed;
- borderline papers are removed by default but can be explicitly reconsidered;
- remaining candidates are ranked by how many collected papers point to them.

This module is also used by discovery_provider_adapter as the
"repository_references" schema-v3 provider.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import citation_graph

SOURCE_URL = "repository://structured-references"
DEFAULT_UNRELATED_LEDGER = Path(".survey/work-queue/reference-curation/unrelated-papers.json")
DEFAULT_BORDERLINE_LEDGER = Path(".survey/work-queue/reference-curation/borderline-papers.json")
# Backward-compatible alias for the first implementation.
DEFAULT_LEDGER = DEFAULT_UNRELATED_LEDGER


def _candidate_record(ref: Any, canonical_id: str, identities: list[str]) -> dict[str, Any]:
    raw = ref if isinstance(ref, dict) else {}
    record: dict[str, Any] = {
        "canonical_id": canonical_id,
        "identity_tokens": list(dict.fromkeys(identities)),
    }
    for identity in identities:
        if identity.startswith("arXiv:"):
            record.setdefault("arxiv_id", identity.split(":", 1)[1])
            record.setdefault("source_url", f"https://arxiv.org/abs/{identity.split(':', 1)[1]}")
        elif identity.startswith("DOI:"):
            record.setdefault("doi", identity.split(":", 1)[1])
            record.setdefault("source_url", f"https://doi.org/{identity.split(':', 1)[1]}")
        elif identity.startswith("OpenReview:"):
            record.setdefault("openreview_id", identity.split(":", 1)[1])
            record.setdefault("source_url", f"https://openreview.net/forum?id={identity.split(':', 1)[1]}")
    for field in ("title", "source_url", "year", "published"):
        value = raw.get(field) if isinstance(raw, dict) else None
        if value not in (None, ""):
            record[field] = value
    return record


def _load_ledger_tokens(path: Path, *, label: str) -> set[str]:
    if not path.is_file():
        return set()
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"{label} ledger has unsupported schema: {path}")
    rows = payload.get("records")
    if not isinstance(rows, dict):
        raise ValueError(f"{label} ledger is missing records: {path}")
    tokens: set[str] = set()
    for key, row in rows.items():
        if isinstance(key, str) and key:
            tokens.add(key)
        if not isinstance(row, dict):
            continue
        values = row.get("identity_tokens")
        if isinstance(values, list):
            tokens.update(v for v in values if isinstance(v, str) and v)
        tokens.update(citation_graph.normalized_identifiers(row))
    return tokens


def _reference_progress_counts(
    papers: list[Any],
    *,
    represented: set[str],
    unrelated: set[str],
    borderline: set[str],
) -> dict[str, int]:
    """Count the full structured-reference mountain with mutually exclusive states."""
    buckets: dict[str, set[str]] = {}
    alias_to_key: dict[str, str] = {}

    def merge_keys(keys: set[str]) -> str:
        target = sorted(keys)[0]
        for other in sorted(keys - {target}):
            tokens = buckets.pop(other)
            buckets[target].update(tokens)
            for token in tokens:
                alias_to_key[token] = target
        return target

    for source in papers:
        refs = source.meta.get("references")
        if not isinstance(refs, list):
            continue
        for ref in refs:
            identities = citation_graph.reference_identifiers(ref)
            if not identities:
                continue
            matched_keys = {alias_to_key[i] for i in identities if i in alias_to_key}
            if not matched_keys:
                key = identities[0]
                buckets[key] = set(identities)
            elif len(matched_keys) == 1:
                key = next(iter(matched_keys))
                buckets[key].update(identities)
            else:
                key = merge_keys(matched_keys)
                buckets[key].update(identities)
            for identity in identities:
                alias_to_key[identity] = key

    represented_count = 0
    unrelated_count = 0
    borderline_count = 0
    remaining_count = 0
    for tokens in buckets.values():
        if tokens & represented:
            represented_count += 1
        elif tokens & unrelated:
            unrelated_count += 1
        elif tokens & borderline:
            borderline_count += 1
        else:
            remaining_count += 1

    total_count = len(buckets)
    return {
        "reference_total_count": total_count,
        "reference_processed_count": total_count - remaining_count,
        "reference_remaining_count": remaining_count,
        "reference_represented_count": represented_count,
        "reference_unrelated_count": unrelated_count,
        "reference_borderline_count": borderline_count,
    }


def build_reference_pool(
    repo_root: Path,
    *,
    unrelated_ledger_path: Path | None = None,
    borderline_ledger_path: Path | None = None,
    include_borderline: bool = False,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    unrelated_path = (
        Path(unrelated_ledger_path)
        if unrelated_ledger_path is not None
        else repo_root / DEFAULT_UNRELATED_LEDGER
    )
    borderline_path = (
        Path(borderline_ledger_path)
        if borderline_ledger_path is not None
        else repo_root / DEFAULT_BORDERLINE_LEDGER
    )

    papers = citation_graph.load_records(repo_root)
    represented: set[str] = set()
    for paper in papers:
        represented.update(paper.identifiers)
    unrelated = _load_ledger_tokens(unrelated_path, label="unrelated-paper")
    borderline = (
        set()
        if include_borderline
        else _load_ledger_tokens(borderline_path, label="borderline-paper")
    )
    progress = _reference_progress_counts(
        papers,
        represented=represented,
        unrelated=unrelated,
        borderline=borderline,
    )

    buckets: dict[str, dict[str, Any]] = {}
    alias_to_key: dict[str, str] = {}

    def merge_keys(keys: set[str]) -> str:
        target = sorted(keys)[0]
        target_bucket = buckets[target]
        for other in sorted(keys - {target}):
            source = buckets.pop(other)
            target_bucket["identity_tokens"].update(source["identity_tokens"])
            target_bucket["linked_from"].update(source["linked_from"])
            target_bucket["linked_from_titles"].update(source["linked_from_titles"])
            target_bucket["linked_from_lineages"].update(source["linked_from_lineages"])
            for field in ("title", "source_url", "year", "published", "arxiv_id", "doi", "openreview_id"):
                if not target_bucket["record"].get(field) and source["record"].get(field):
                    target_bucket["record"][field] = source["record"][field]
            for token in source["identity_tokens"]:
                alias_to_key[token] = target
        return target

    for source in papers:
        refs = source.meta.get("references")
        if not isinstance(refs, list):
            continue
        seen_source_keys: set[str] = set()
        for ref in refs:
            identities = citation_graph.reference_identifiers(ref)
            if not identities:
                continue
            if any(identity in represented for identity in identities):
                continue
            if any(identity in unrelated for identity in identities):
                continue
            if any(identity in borderline for identity in identities):
                continue

            matched_keys = {alias_to_key[i] for i in identities if i in alias_to_key}
            if not matched_keys:
                key = identities[0]
                buckets[key] = {
                    "record": _candidate_record(ref, key, identities),
                    "identity_tokens": set(identities),
                    "linked_from": set(),
                    "linked_from_titles": set(),
                    "linked_from_lineages": set(),
                }
            elif len(matched_keys) == 1:
                key = next(iter(matched_keys))
            else:
                key = merge_keys(matched_keys)

            bucket = buckets[key]
            bucket["identity_tokens"].update(identities)
            for identity in identities:
                alias_to_key[identity] = key

            if key not in seen_source_keys:
                bucket["linked_from"].add(source.path)
                source_title = str(source.meta.get("title") or "").strip()
                if source_title:
                    bucket["linked_from_titles"].add(source_title)
                lineage = str(source.meta.get("lineage") or "").strip()
                if lineage:
                    bucket["linked_from_lineages"].add(lineage)
                seen_source_keys.add(key)

            fresh = _candidate_record(ref, key, identities)
            for field, value in fresh.items():
                if field in {"canonical_id", "identity_tokens"}:
                    continue
                if not bucket["record"].get(field) and value not in (None, ""):
                    bucket["record"][field] = value

    candidates: list[dict[str, Any]] = []
    for key, bucket in buckets.items():
        record = dict(bucket["record"])
        record["canonical_id"] = key
        record["identity_tokens"] = sorted(bucket["identity_tokens"])
        record["relation_count"] = len(bucket["linked_from"])
        record["linked_from"] = sorted(bucket["linked_from"])
        record["linked_from_titles"] = sorted(bucket["linked_from_titles"])
        record["linked_from_lineages"] = sorted(bucket["linked_from_lineages"])
        candidates.append(record)

    candidates.sort(
        key=lambda row: (
            -int(row.get("relation_count") or 0),
            -len(row.get("linked_from_lineages") or []),
            str(row.get("canonical_id") or "").casefold(),
        )
    )
    if progress["reference_remaining_count"] != len(candidates):
        raise RuntimeError(
            "structured-reference progress census disagrees with candidate pool: "
            f"{progress['reference_remaining_count']} != {len(candidates)}"
        )
    return {
        "schema_version": 1,
        "source_url": SOURCE_URL,
        "paper_count": len(papers),
        "represented_identity_count": len(represented),
        "unrelated_identity_count": len(unrelated),
        "borderline_identity_count": len(borderline),
        "borderline_excluded": not include_borderline,
        **progress,
        "candidate_count": len(candidates),
        "candidates": candidates,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--ledger", help="deprecated alias of --unrelated-ledger")
    ap.add_argument("--unrelated-ledger")
    ap.add_argument("--borderline-ledger")
    ap.add_argument(
        "--include-borderline",
        action="store_true",
        help="explicit reconsideration mode; default Discovery excludes borderline papers",
    )
    ap.add_argument("--offset", type=int, default=0)
    ap.add_argument("--limit", type=int, default=20)
    args = ap.parse_args()
    if args.offset < 0 or args.limit <= 0:
        ap.error("offset must be >= 0 and limit must be > 0")
    if args.ledger and args.unrelated_ledger:
        ap.error("use only one of --ledger and --unrelated-ledger")

    root = Path(args.root).resolve()
    unrelated = (
        Path(args.unrelated_ledger or args.ledger).resolve()
        if (args.unrelated_ledger or args.ledger)
        else root / DEFAULT_UNRELATED_LEDGER
    )
    borderline = (
        Path(args.borderline_ledger).resolve()
        if args.borderline_ledger
        else root / DEFAULT_BORDERLINE_LEDGER
    )
    pool = build_reference_pool(
        root,
        unrelated_ledger_path=unrelated,
        borderline_ledger_path=borderline,
        include_borderline=args.include_borderline,
    )
    selected = pool["candidates"][args.offset:args.offset + args.limit]
    out = {
        **{k: v for k, v in pool.items() if k != "candidates"},
        "offset": args.offset,
        "limit": args.limit,
        "returned": len(selected),
        "candidates": selected,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    print(
        f"[WORKER-GUIDE][探索状況] 構造化references 総候補 {pool['reference_total_count']}件 / "
        f"処理済み {pool['reference_processed_count']}件 / 未処理 {pool['reference_remaining_count']}件 / "
        f"収録済み {pool['reference_represented_count']}件 / 無関係 {pool['reference_unrelated_count']}件 / "
        f"微妙 {pool['reference_borderline_count']}件 / offset {args.offset}",
        file=sys.stderr,
    )
    print(
        f"[WORKER-GUIDE][完了] 構造化referencesから未処理候補 {pool['candidate_count']} 件を構築しました。",
        file=sys.stderr,
    )
    print(
        "[WORKER-GUIDE][次] 上位候補を軽量評価してください。対象外は mark-unrelated、"
        "関連性や価値が微妙なら mark-borderline で先に永続記録し、"
        "関連ありだけ通常のDiscovery precheck/submission経路へ進めます。",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
