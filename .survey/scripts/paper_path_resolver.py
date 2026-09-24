#!/usr/bin/env python3
"""Deterministically assign safe paper paths when discovery omitted one."""
from __future__ import annotations

import hashlib
import re
import unicodedata
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

import paper_taxonomy

DEFAULT_INFERENCE_DIR = "papers/inference/99-other-inference-systems"
_ARXIV_ID_RE = re.compile(r"(?i)(?:arxiv:)?(\d{4}\.\d{4,5})(?:v\d+)?$")
_ARXIV_URL_RE = re.compile(r"(?i)arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?(?:\.pdf)?(?:[?#].*)?$")
_YEAR_RE = re.compile(r"\b(20\d{2})\b")


def validate_paper_path(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("paper_path must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not value.startswith("papers/") or not value.endswith(".md"):
        raise ValueError("paper_path must be a Markdown path under papers/")
    return path.as_posix()


def _arxiv_id(record: Mapping[str, Any]) -> str | None:
    for key in ("canonical_id", "arxiv_id"):
        value = record.get(key)
        if not isinstance(value, str):
            continue
        match = _ARXIV_ID_RE.search(value.strip())
        if match:
            return match.group(1)
    for key in ("source_url", "source"):
        value = record.get(key)
        if not isinstance(value, str):
            continue
        match = _ARXIV_URL_RE.search(value.strip())
        if match:
            return match.group(1)
    return None


def _slug(value: Any, *, max_length: int = 120) -> str:
    text = str(value or "").strip()
    normalized = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    slug = slug[:max_length].rstrip("-")
    return slug or "paper"


def _year(record: Mapping[str, Any], arxiv_id: str | None) -> str:
    if arxiv_id is not None:
        return f"20{arxiv_id[:2]}"
    for key in ("published", "publication_date", "created_at"):
        value = record.get(key)
        if not isinstance(value, str):
            continue
        match = _YEAR_RE.search(value)
        if match:
            return match.group(1)
    return "0000"


def resolve_paper_path(record: Mapping[str, Any], *, repo_root: Path | None = None) -> str:
    """Return an explicit path unchanged, otherwise derive a stable inference path.

    A registered lineage hint is honored. Missing or unknown lineage hints fall back
    to 99-other so path resolution never invents a physical directory.
    """
    explicit = record.get("paper_path")
    if explicit is not None:
        return validate_paper_path(explicit)

    requested_lineage = str(record.get("lineage") or "").strip()
    lineage = paper_taxonomy.canonical_lineage(
        "inference",
        requested_lineage or paper_taxonomy.DEFAULT_INFERENCE_LINEAGE,
        repo_root=repo_root,
    )
    inference_dir = f"papers/inference/{lineage}"

    arxiv_id = _arxiv_id(record)
    year = _year(record, arxiv_id)
    title_slug = _slug(record.get("title"))
    if arxiv_id is not None:
        identity = arxiv_id
    else:
        seed = str(record.get("canonical_id") or record.get("source_url") or record.get("title") or "paper")
        identity = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:12]
    return f"{inference_dir}/{year}-{identity}-{title_slug}.md"
