#!/usr/bin/env python3
"""Collect represented/pending paper records for the Discovery alias resolver."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import survey


def _read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def collect_represented_records(root: Path, jobs_dir: Path | None = None) -> list[dict[str, Any]]:
    """Return records from the same canonical sources used by duplicate prevention.

    The resulting list intentionally contains overlapping views. ``paper_identity`` folds
    those views into one represented-paper graph via stable identifiers and exact titles.
    This preserves aliases exposed by the identity index while retaining rich title/author/
    year metadata from live paper front matter for conservative ID-less fuzzy matching.
    """
    root = Path(root).resolve()
    jobs_dir = Path(jobs_dir) if jobs_dir is not None else root / "work-queue" / "jobs"
    records: list[dict[str, Any]] = []

    if jobs_dir.exists():
        for path in sorted(jobs_dir.glob("*.json")):
            record = _read_json(path, {}) or {}
            if isinstance(record, dict):
                records.append(dict(record))

    identity = _read_json(root / "survey-state" / "paper-identity-index.json", {}) or {}
    if isinstance(identity, dict):
        papers = identity.get("papers") or {}
        if isinstance(papers, dict):
            for canonical, record in papers.items():
                data = dict(record) if isinstance(record, dict) else {}
                data["canonical_id"] = canonical
                records.append(data)
        elif isinstance(papers, list):
            records.extend(dict(record) for record in papers if isinstance(record, dict))

        aliases = identity.get("identifier_to_canonical") or {}
        if isinstance(aliases, dict):
            for identifier, canonical in aliases.items():
                records.append(
                    {
                        "canonical_id": canonical,
                        "identifiers": [identifier],
                    }
                )

    delta_root = root / "survey-state" / "identity-deltas"
    if delta_root.exists():
        for path in sorted(delta_root.rglob("*.json")):
            record = _read_json(path, {}) or {}
            if isinstance(record, dict):
                records.append(dict(record))

    old_root = survey.ROOT
    try:
        survey.ROOT = root
        for paper in survey.papers():
            data = dict(paper.get("meta") or {})
            data["canonical_id"] = paper.get("canonical_id")
            data["identifiers"] = paper.get("identifiers") or []
            data["title"] = paper.get("title")
            records.append(data)
    finally:
        survey.ROOT = old_root

    return records
