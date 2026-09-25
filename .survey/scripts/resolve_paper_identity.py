#!/usr/bin/env python3
"""Resolve a paper stable identity to the already represented repository path.

This is intentionally read-only. Importers must run it before deciding between
create and update so a stale intended_path cannot create a duplicate paper.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import paper_identity
import research_job_reconciliation


def query_record(args: argparse.Namespace) -> dict[str, Any]:
    row: dict[str, Any] = {}
    if args.canonical_id:
        row["canonical_id"] = args.canonical_id
    if args.arxiv_id:
        row["arxiv_id"] = args.arxiv_id
    if args.doi:
        row["doi"] = args.doi
    if args.openreview_id:
        row["openreview_id"] = args.openreview_id
    if args.source_url:
        row["source_url"] = args.source_url
    if args.title:
        row["title"] = args.title
    return row


def resolve(repo_root: Path, record: dict[str, Any]) -> dict[str, Any]:
    identifiers = sorted(paper_identity.record_identifiers(record))
    if not identifiers:
        raise ValueError(
            "stable paper identity required: canonical_id/arxiv_id/doi/"
            "openreview_id/source_url"
        )

    index = research_job_reconciliation.build_paper_index(repo_root)
    matches: dict[str, dict[str, Any]] = {}
    for identifier in identifiers:
        paper = index["by_identifier"].get(identifier)
        if paper is not None:
            matches[str(paper["path"])] = paper

    if len(matches) > 1:
        raise ValueError(
            "identity resolves to multiple represented paper paths: "
            + ", ".join(sorted(matches))
        )

    paper = next(iter(matches.values()), None)
    return {
        "schema_version": 1,
        "status": "represented" if paper is not None else "not_found",
        "query_identifiers": identifiers,
        "paper_path": paper.get("path") if paper else None,
        "canonical_id": paper.get("canonical_id") if paper else None,
        "matched_identifiers": paper.get("identifiers", []) if paper else [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--canonical-id")
    parser.add_argument("--arxiv-id")
    parser.add_argument("--doi")
    parser.add_argument("--openreview-id")
    parser.add_argument("--source-url")
    parser.add_argument("--title")
    args = parser.parse_args()

    result = resolve(args.repo_root.resolve(), query_record(args))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
