#!/usr/bin/env python3
"""Validate and render current structured research records."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from render_paper import render_paper  # noqa: E402

MAX_SLOT_BYTES = {
    "metadata": 16384,
    "problem_method": 16384,
    "evaluation": 12288,
    "results": 12288,
    "positioning": 8192,
}



def nonempty(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def prose_chars(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, str):
        return len(value.strip())
    if isinstance(value, list):
        total = 0
        for item in value:
            if isinstance(item, dict):
                total += prose_chars(item.get("description"))
                total += prose_chars(item.get("interpretation"))
                total += prose_chars(item.get("text"))
            else:
                total += prose_chars(item)
        return total
    if isinstance(value, dict):
        return sum(prose_chars(v) for v in value.values())
    return 0


def normalize_preferred_terms(value: Any, key: str | None = None) -> Any:
    """Compatibility no-op.

    Language/style rewriting belongs to the reading worker while primary-source
    context is available.  The GitHub publication path must not rewrite prose.
    """
    return value


def ensure_explanatory_summary(record: dict[str, Any]) -> None:
    """Compatibility no-op; publication code must not synthesize scientific prose."""
    return None


def validate_references(meta: dict[str, Any]) -> None:
    """Validate only the shape of reference metadata when it is present."""
    if "references" not in meta:
        return
    references = meta.get("references")
    if not isinstance(references, list):
        raise ValueError("metadata.references must be a list")
    seen: set[str] = set()
    for index, item in enumerate(references):
        if not isinstance(item, dict):
            raise ValueError(f"metadata.references[{index}] must be an object")
        identities = [
            str(item[key]).strip()
            for key in ("canonical_id", "arxiv_id", "doi", "openreview_id")
            if item.get(key) not in (None, "")
        ]
        if identities:
            dedupe_key = "|".join(sorted(x.lower() for x in identities))
            if dedupe_key in seen:
                raise ValueError(f"metadata.references[{index}] duplicates an earlier reference identity")
            seen.add(dedupe_key)


class RecordValidationError(ValueError):
    """Structured-record validation failure carrying all current issues."""

    def __init__(self, issues: list[str], *, aggregate: bool = False):
        self.issues = list(issues)
        message = self.issues[0]
        if aggregate and len(self.issues) > 1:
            message = "structured record validation failed: " + " | ".join(self.issues)
        super().__init__(message)


def collect_validation_issues(record: dict[str, Any]) -> list[str]:
    """Return publication-integrity issues only.

    Semantic depth, prose length, Japanese ratio, method completeness, result
    interpretation, and other paper-reading judgments are intentionally owned
    by the reading worker's self-review and are not GitHub publication gates.
    """
    issues: list[str] = []
    for slot in ("metadata", "problem_method", "evaluation", "results", "positioning"):
        if not isinstance(record.get(slot), dict):
            issues.append(f"{slot} must be an object")

    meta = record.get("metadata") if isinstance(record.get("metadata"), dict) else {}
    for key in ("canonical_id", "title", "source", "summary", "list_summary"):
        if not nonempty(meta.get(key)):
            issues.append(f"metadata.{key} is required for rendering/publication")

    if "sources" in meta and not isinstance(meta.get("sources"), list):
        issues.append("metadata.sources must be a list when present")
    if "arxiv_categories" in meta and meta.get("arxiv_categories") is not None:
        categories = meta.get("arxiv_categories")
        if not isinstance(categories, dict):
            issues.append("metadata.arxiv_categories must be an object when present")
        elif categories.get("cross_list") is not None and not isinstance(categories.get("cross_list"), list):
            issues.append("metadata.arxiv_categories.cross_list must be a list when present")
    try:
        validate_references(meta)
    except ValueError as exc:
        issues.append(str(exc))

    pm = record.get("problem_method") if isinstance(record.get("problem_method"), dict) else {}
    if "components" in pm and pm.get("components") is not None and not isinstance(pm.get("components"), list):
        issues.append("problem_method.components must be a list when present")

    rs = record.get("results") if isinstance(record.get("results"), dict) else {}
    key_results = rs.get("key_results")
    if key_results is not None:
        if not isinstance(key_results, list):
            issues.append("results.key_results must be a list when present")
        else:
            for index, item in enumerate(key_results):
                if not isinstance(item, dict):
                    issues.append(f"results.key_results[{index}] must be an object")

    return issues


def validate_record(record: dict[str, Any], *, collect_all: bool = False) -> None:
    issues = collect_validation_issues(record)
    if issues:
        raise RecordValidationError(issues, aggregate=collect_all)
