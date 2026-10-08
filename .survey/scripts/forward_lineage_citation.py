#!/usr/bin/env python3
"""Lineage-local citation evidence from forward citation edges only.

Candidate -> cited curated paper is an observed edge in the forward sweep.
Do not infer this signal from backward-reference linked_from records.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Iterable


def lineage_from_path(path: Any) -> str | None:
    parts = str(path or "").replace("\\", "/").split("/")
    if len(parts) < 4 or parts[0] != "papers":
        return None
    if parts[1] not in ("inference", "training", "survey"):
        return None
    if not parts[2] or parts[2].lower() in ("readme.md", "comparison.md"):
        return None
    return "/".join(parts[1:3])


def seed_indexes(papers: Iterable[Any]) -> tuple[dict[str, str], dict[str, str]]:
    """Map exact curated canonical IDs and paper paths to fine-grained folders."""
    by_id: dict[str, str] = {}
    by_path: dict[str, str] = {}
    for paper in papers:
        lineage = lineage_from_path(paper.path)
        if lineage is None:
            continue
        by_id[str(paper.canonical_id)] = lineage
        by_path[str(paper.path)] = lineage
    return by_id, by_path


def forward_lineage_counts(
    row: dict[str, Any],
    by_id: dict[str, str],
    by_path: dict[str, str],
    *,
    source_kind: str,
) -> dict[str, int]:
    """Count distinct cited survey seeds within each curated directory.

    The forward sweep provides forward_seed_ids; legacy forward-only rows
    may use linked_from paths. Backward rows must never use linked_from here:
    those edges point in the opposite direction.
    """
    if source_kind != "forward_citation_candidate":
        return {}
    source_ids = row.get("forward_seed_ids")
    seeds = {str(v) for v in source_ids if v} if isinstance(source_ids, list) else set()
    if seeds:
        counts = Counter(by_id[seed] for seed in seeds if seed in by_id)
    else:
        linked = row.get("linked_from")
        paths = {str(v) for v in linked if v} if isinstance(linked, list) else set()
        counts = Counter(by_path[path] for path in paths if path in by_path)
    return dict(sorted(counts.items()))


def forward_lineage_bonus(max_same_lineage: Any) -> int:
    """A single generic citation has no bonus; 2+ corroborating seeds do.

    Cap protects other relevance signals from citation-only domination.
    """
    try:
        n = max(int(max_same_lineage), 0)
    except (TypeError, ValueError):
        return 0
    return min(120, 25 * max(n - 1, 0))
