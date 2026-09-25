#!/usr/bin/env python3
"""Match Research jobs against paper Markdown that is already represented.

This module is deliberately conservative:
- only real paper files under papers/{inference,training,survey} count;
- stable identifiers/source URLs and exact declared paper_path are accepted;
- title-only fuzzy matching is never used to close a Research job.

Normal-chat/Library imports can therefore make a paper represented without
fabricating a workflow-v10 Research submission/result. The corresponding ready
Research job is then safe to supersede as already represented.
"""
from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import paper_identity
import survey


def _survey_root(repo_root: Path) -> Path:
    repo_root = Path(repo_root).resolve()
    candidate = repo_root / ".survey"
    return candidate if candidate.is_dir() else repo_root


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def _write_json(path: Path, value: dict[str, Any]) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as tmp:
        tmp.write(text)
        staged = Path(tmp.name)
    staged.replace(path)


def build_paper_index(repo_root: Path) -> dict[str, Any]:
    """Build a stable-ID/path index from actual repository paper files only."""
    repo_root = Path(repo_root).resolve()
    old_root = survey.ROOT
    try:
        survey.ROOT = _survey_root(repo_root)
        papers = survey.papers()
    finally:
        survey.ROOT = old_root

    by_path: dict[str, dict[str, Any]] = {}
    by_identifier: dict[str, dict[str, Any]] = {}
    for paper in papers:
        record = dict(paper.get("meta") or {})
        record["canonical_id"] = paper.get("canonical_id")
        record["identifiers"] = paper.get("identifiers") or []
        record["title"] = paper.get("title")
        normalized = {
            "canonical_id": paper.get("canonical_id"),
            "path": paper.get("path"),
            "identifiers": sorted(paper_identity.record_identifiers(record)),
            "title": paper.get("title"),
        }
        path = str(paper.get("path") or "").strip()
        if path:
            by_path[path] = normalized
        for identifier in normalized["identifiers"]:
            prior = by_identifier.get(identifier)
            if prior is not None and prior.get("path") != normalized.get("path"):
                raise ValueError(
                    f"duplicate represented identifier {identifier}: "
                    f"{prior.get('path')} vs {normalized.get('path')}"
                )
            by_identifier[identifier] = normalized

    return {
        "by_path": by_path,
        "by_identifier": by_identifier,
        "paper_count": len(papers),
    }


def match_represented_research_job(
    job: dict[str, Any],
    paper_index: dict[str, Any],
) -> dict[str, Any] | None:
    """Return the represented paper for a Research job, or None.

    Matching is intentionally stricter than Discovery duplicate matching: direct
    reconciliation may terminate work, so a fuzzy title is insufficient.
    """
    if not isinstance(job, dict) or job.get("type") != "research":
        return None

    paper_path = str(job.get("paper_path") or "").strip().replace("\\", "/")
    by_path = paper_index.get("by_path") or {}
    if paper_path and paper_path in by_path:
        return dict(by_path[paper_path])

    by_identifier = paper_index.get("by_identifier") or {}
    matches: dict[str, dict[str, Any]] = {}
    for identifier in sorted(paper_identity.record_identifiers(job)):
        paper = by_identifier.get(identifier)
        if isinstance(paper, dict):
            matches[str(paper.get("path") or paper.get("canonical_id"))] = paper

    if len(matches) > 1:
        raise ValueError(
            "Research job identifiers resolve to multiple represented papers: "
            + ", ".join(sorted(matches))
        )
    return dict(next(iter(matches.values()))) if matches else None


def effective_status(job: dict[str, Any], paper_index: dict[str, Any]) -> str:
    """Return a derived status that hides stale ready jobs immediately."""
    status = str(job.get("status") or "")
    if (
        status == "ready"
        and job.get("type") == "research"
        and match_represented_research_job(job, paper_index) is not None
    ):
        return "superseded"
    return status


def reconcile(
    repo_root: Path,
    *,
    dry_run: bool = False,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Supersede ready Research jobs whose paper already exists.

    This does not create a fake completion result. A normal workflow-v10 Research
    completion remains "completed"; externally imported already-represented work
    becomes terminal "superseded" with explicit provenance.
    """
    repo_root = Path(repo_root).resolve()
    jobs_dir = repo_root / ".survey/work-queue/jobs"
    paper_index = build_paper_index(repo_root)
    changed: list[dict[str, Any]] = []
    stamp = timestamp or _now()

    if not jobs_dir.is_dir():
        return {"changed": 0, "jobs": [], "paper_count": paper_index["paper_count"]}

    for path in sorted(jobs_dir.glob("*.json")):
        job = _read_json(path)
        if job.get("type") != "research" or job.get("status") != "ready":
            continue
        paper = match_represented_research_job(job, paper_index)
        if paper is None:
            continue

        job["status"] = "superseded"
        job["superseded_at"] = stamp
        job["superseded_reason"] = "paper_already_represented"
        job["represented_paper_path"] = paper.get("path")
        job["represented_canonical_id"] = paper.get("canonical_id")
        job["reconciled_by"] = "reconcile_represented_research_jobs.py"
        if not dry_run:
            _write_json(path, job)
        changed.append(
            {
                "job_id": job.get("job_id") or path.stem,
                "canonical_id": job.get("canonical_id"),
                "represented_paper_path": paper.get("path"),
            }
        )

    return {
        "changed": len(changed),
        "jobs": changed,
        "paper_count": paper_index["paper_count"],
        "dry_run": dry_run,
    }
