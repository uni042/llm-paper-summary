#!/usr/bin/env python3
"""Validate and render current structured research records."""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from japanese_style import (  # noqa: E402
    DEFAULT_MIN_JAPANESE_RATIO,
    JP_CLASS,
    PREFERRED_TERMS,
    TERM_PATTERNS,
    find_bare_english,
    japanese_ratio,
    record_prose_text,
)
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


def _protect_parenthetical_formal_names(text: str) -> tuple[str, list[str]]:
    """Protect allowed formal English names in parentheses after Japanese prose."""
    protected: list[str] = []

    def repl(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"__FORMAL_NAME_{len(protected) - 1}__"

    pattern = re.compile(rf"(?<=[{JP_CLASS}])(?:（[^（）]*[A-Za-z][^（）]*）|\([^()]*[A-Za-z][^()]*\))")
    return pattern.sub(repl, text), protected


def _restore_parenthetical_formal_names(text: str, protected: list[str]) -> str:
    for index, original in enumerate(protected):
        text = text.replace(f"__FORMAL_NAME_{index}__", original)
    return text


def normalize_preferred_terms(value: Any, key: str | None = None) -> Any:
    """Normalize ordinary English prose terms before final validation/rendering."""
    protected_keys = {
        "canonical_id", "arxiv_id", "doi", "openreview_id", "source", "sources",
        "code", "paper_path", "attempt_id", "job_id", "published", "title",
        "authors", "publication", "publication_type", "publication_status", "lineage",
        "arxiv_categories", "references", "references_checked_at", "references_source",
        "references_total",
    }
    if key in protected_keys:
        return value
    if isinstance(value, str):
        if value.startswith(("http://", "https://")):
            return value
        text, protected = _protect_parenthetical_formal_names(value)
        for canonical, pattern in TERM_PATTERNS.items():
            preferred = PREFERRED_TERMS[canonical][0].split("／", 1)[0]
            text = pattern.sub(preferred, text)
        return _restore_parenthetical_formal_names(text, protected)
    if isinstance(value, list):
        return [normalize_preferred_terms(item, key=key) for item in value]
    if isinstance(value, dict):
        return {k: normalize_preferred_terms(v, key=k) for k, v in value.items()}
    return value


def ensure_explanatory_summary(record: dict[str, Any]) -> None:
    """Extend an undersized summary only from already supplied scientific prose."""
    meta = record.get("metadata") or {}
    if prose_chars(meta.get("summary")) >= 180:
        return
    pm = record.get("problem_method") or {}
    summary = str(meta.get("summary") or "").strip()
    candidates: list[str] = []
    for source in (pm.get("problem"), pm.get("novelty")):
        if not isinstance(source, str):
            continue
        candidates.extend(part.strip() for part in re.split(r"(?<=。)", source) if part.strip())
    for sentence in candidates:
        if sentence not in summary:
            summary = (summary + " " + sentence).strip()
        if prose_chars(summary) >= 220:
            break
    meta["summary"] = summary
    record["metadata"] = meta


def validate_references(meta: dict[str, Any]) -> None:
    if "references" not in meta:
        raise ValueError("metadata.references is required; use [] after checking a reference section with no normalized identifiers")
    references = meta.get("references")
    if not isinstance(references, list):
        raise ValueError("metadata.references must be a list")
    if not nonempty(meta.get("references_checked_at")):
        raise ValueError("metadata.references_checked_at is required")
    if not nonempty(meta.get("references_source")):
        raise ValueError("metadata.references_source is required")
    total = meta.get("references_total")
    if not isinstance(total, int) or isinstance(total, bool) or total < 0:
        raise ValueError("metadata.references_total must be a non-negative integer")
    if total < len(references):
        raise ValueError("metadata.references_total cannot be smaller than metadata.references length")

    seen: set[str] = set()
    for index, item in enumerate(references):
        if not isinstance(item, dict):
            raise ValueError(f"metadata.references[{index}] must be an object")
        identities = [
            str(item[key]).strip()
            for key in ("canonical_id", "arxiv_id", "doi", "openreview_id")
            if item.get(key) not in (None, "")
        ]
        if not identities:
            raise ValueError(f"metadata.references[{index}] requires a normalized identity")
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
    """Return every independently checkable current record-validation issue."""
    issues: list[str] = []
    meta = record.get("metadata") or {}
    pm = record.get("problem_method") or {}
    ev = record.get("evaluation") or {}
    rs = record.get("results") or {}
    pos = record.get("positioning") or {}

    for key in (
        "canonical_id", "title", "summary", "source", "sources", "authors",
        "publication", "topics", "implementation", "last_checked",
    ):
        if not nonempty(meta.get(key)):
            issues.append(f"metadata.{key} is required")
    if "code" not in meta:
        issues.append("metadata.code is required; use null when no official URL was confirmed")
    if prose_chars(meta.get("summary")) < 180:
        issues.append("metadata.summary must be explanatory, not a one-line abstract")
    if not nonempty(meta.get("publication_type")):
        issues.append("metadata.publication_type is required")
    if not nonempty(meta.get("published")):
        issues.append("metadata.published is required")
    if not nonempty(meta.get("publication_status")):
        issues.append("metadata.publication_status is required")
    if meta.get("arxiv_id"):
        categories = meta.get("arxiv_categories")
        if not isinstance(categories, dict) or not nonempty(categories.get("primary")):
            issues.append("metadata.arxiv_categories.primary is required for arXiv papers")
        elif categories.get("cross_list") is not None and not isinstance(categories.get("cross_list"), list):
            issues.append("metadata.arxiv_categories.cross_list must be a list")
    if not nonempty(meta.get("hardware_evaluation")):
        issues.append("metadata.hardware_evaluation is required")
    if not nonempty(meta.get("quality_effect")):
        issues.append("metadata.quality_effect is required")
    try:
        validate_references(meta)
    except ValueError as exc:
        issues.append(str(exc))

    for key in ("problem", "novelty", "method_overview", "components", "system_design"):
        if not nonempty(pm.get(key)):
            issues.append(f"problem_method.{key} is required")
    if prose_chars(pm.get("problem")) < 250:
        issues.append("problem_method.problem must explain the bottleneck and why prior approaches are insufficient")
    if prose_chars(pm.get("novelty")) < 180:
        issues.append("problem_method.novelty must explain the paper-specific idea")
    if prose_chars(pm.get("method_overview")) < 500:
        issues.append("problem_method.method_overview must explain the end-to-end mechanism")
    components = pm.get("components")
    if not isinstance(components, list) or len(components) < 2:
        issues.append("problem_method.components requires at least two major mechanisms")
    if isinstance(components, list):
        for index, item in enumerate(components):
            if not isinstance(item, dict) or not nonempty(item.get("name")) or not nonempty(item.get("description")):
                issues.append(f"problem_method.components[{index}] requires name and description")
                continue
            if prose_chars(item.get("description")) < 240:
                issues.append(f"problem_method.components[{index}].description is too short")

    if not (nonempty(ev.get("hardware")) or nonempty(ev.get("software")) or nonempty(ev.get("methodology"))):
        issues.append("evaluation requires hardware/software/methodology evidence")
    if not nonempty(ev.get("scope")):
        issues.append("evaluation.scope is required to distinguish real-hardware/simulation and generalization limits")

    key_results = rs.get("key_results")
    if not isinstance(key_results, list) or not key_results:
        issues.append("results.key_results requires at least one quantitative result")
    if not nonempty(rs.get("overview")) or prose_chars(rs.get("overview")) < 180:
        issues.append("results.overview must explain the main result and its practical meaning")
    if isinstance(key_results, list):
        for index, item in enumerate(key_results):
            if not isinstance(item, dict):
                issues.append(f"results.key_results[{index}] must be an object")
                continue
            missing = [k for k in ("metric", "value", "baseline", "condition", "interpretation") if not nonempty(item.get(k))]
            if missing:
                issues.append(f"results.key_results[{index}] missing: " + ", ".join(missing))
    if not nonempty(rs.get("negative_results")):
        issues.append("results.negative_results is required; record degradation and boundary conditions")
    if not nonempty(rs.get("interpretation")):
        issues.append("results.interpretation is required; explain why gains change across conditions")
    if not nonempty(rs.get("quality_impact")):
        issues.append("results.quality_impact is required; distinguish lossless from approximate methods")

    for key in ("limitations", "differences", "implementation_status", "research_positioning"):
        if not nonempty(pos.get(key)):
            issues.append(f"positioning.{key} is required")

    prose = record_prose_text(record)
    ratio, jp_chars, latin_chars = japanese_ratio(prose)
    if ratio < DEFAULT_MIN_JAPANESE_RATIO:
        issues.append(
            f"Japanese-first prose ratio is too low: {ratio:.1%} "
            f"< {DEFAULT_MIN_JAPANESE_RATIO:.0%} (Japanese={jp_chars}, Latin={latin_chars})"
        )
    bare = find_bare_english(prose)
    if bare:
        preview = ", ".join(f"{hit.term}->{hit.preferred} x{hit.count}" for hit in bare[:12])
        issues.append(
            "Japanese-first terminology violation; replace ordinary English prose "
            f"with Japanese/katakana or put the formal English name only in the first parentheses: {preview}"
        )
    return issues


def validate_record(record: dict[str, Any], *, collect_all: bool = False) -> None:
    issues = collect_validation_issues(record)
    if issues:
        raise RecordValidationError(issues, aggregate=collect_all)
