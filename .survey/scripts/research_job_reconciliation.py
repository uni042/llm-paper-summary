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
import re

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


def _inferred_paper_record(path: Path, repo_root: Path) -> dict[str, Any] | None:
    """Read one real paper file without requiring perfect frontmatter.

    Reconciliation must not become unavailable because one historical/imported
    Markdown predates the current metadata schema. The canonical repository
    quality/index builders may still report that metadata defect separately.
    """
    if path.name == "README.md" or path.name == "comparison.md":
        return None
    try:
        meta, body = survey.front(path)
    except Exception:
        meta, body = {}, path.read_text(encoding="utf-8", errors="replace")

    record = dict(meta or {})
    title = str(record.get("title") or "").strip()
    if not title:
        match = re.search(r"^#\s+(.+?)\s*$", body, re.MULTILINE)
        if match:
            title = match.group(1).strip()
            record["title"] = title

    canonical = str(record.get("canonical_id") or "").strip()
    if not canonical:
        probes = [
            str(record.get("source") or ""),
            str(record.get("source_url") or ""),
            body,
            path.name,
        ]
        for probe in probes:
            match = re.search(
                r"(?:arXiv:|arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5})(?:v\d+)?",
                probe,
                re.IGNORECASE,
            )
            if match:
                canonical = "arXiv:" + match.group(1)
                record["canonical_id"] = canonical
                record.setdefault("arxiv_id", match.group(1))
                break
        if not canonical:
            doi = str(record.get("doi") or "").strip()
            if doi:
                canonical = doi if doi.lower().startswith("doi:") else "DOI:" + doi
                record["canonical_id"] = canonical

    if not record.get("source") and canonical.startswith("arXiv:"):
        record["source"] = "https://arxiv.org/abs/" + canonical.split(":", 1)[1]

    rel = path.relative_to(repo_root).as_posix()
    identifiers = sorted(paper_identity.record_identifiers(record))
    if not identifiers and canonical:
        normalized = paper_identity.safe_norm_id(canonical)
        if normalized:
            identifiers = [normalized]
    stable_tokens = sorted(paper_identity.stable_identity_tokens(record))
    if not stable_tokens and identifiers:
        stable_tokens = ["id:" + identifier for identifier in identifiers]
    if not stable_tokens:
        return None
    return {
        "canonical_id": canonical or (identifiers[0] if identifiers else None),
        "path": rel,
        "identifiers": identifiers,
        "stable_identity_tokens": stable_tokens,
        "title": title,
    }


def build_paper_index(repo_root: Path) -> dict[str, Any]:
    """Build a stable-ID/path index from actual repository paper files only.

    Unlike the canonical paper-index builder, this reconciliation index is
    intentionally tolerant of historical Markdown missing current frontmatter:
    one malformed imported paper must not keep every stale Research job alive.
    """
    repo_root = Path(repo_root).resolve()
    by_path: dict[str, dict[str, Any]] = {}
    by_identifier: dict[str, dict[str, Any]] = {}
    by_token: dict[str, dict[str, Any]] = {}
    identifier_conflicts: dict[str, list[dict[str, Any]]] = {}
    token_conflicts: dict[str, list[dict[str, Any]]] = {}
    paper_count = 0

    def add_lookup(
        lookup: dict[str, dict[str, Any]],
        conflicts: dict[str, list[dict[str, Any]]],
        key: str,
        paper: dict[str, Any],
    ) -> None:
        conflict = conflicts.get(key)
        if conflict is not None:
            if all(item.get("path") != paper.get("path") for item in conflict):
                conflict.append(paper)
                conflict.sort(key=lambda item: str(item.get("path") or ""))
            return
        prior = lookup.get(key)
        if prior is None:
            lookup[key] = paper
            return
        if prior.get("path") == paper.get("path"):
            return
        conflicts[key] = sorted(
            [prior, paper],
            key=lambda item: str(item.get("path") or ""),
        )
        lookup.pop(key, None)

    for family in ("inference", "training", "survey"):
        folder = repo_root / "papers" / family
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*/*.md")):
            paper = _inferred_paper_record(path, repo_root)
            if paper is None:
                continue
            paper_count += 1
            by_path[paper["path"]] = paper
            for identifier in paper["identifiers"]:
                add_lookup(
                    by_identifier,
                    identifier_conflicts,
                    identifier,
                    paper,
                )
            for token in paper["stable_identity_tokens"]:
                add_lookup(by_token, token_conflicts, token, paper)

    return {
        "by_path": by_path,
        "by_identifier": by_identifier,
        "by_token": by_token,
        "identifier_conflicts": identifier_conflicts,
        "token_conflicts": token_conflicts,
        "paper_count": paper_count,
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

    by_token = paper_index.get("by_token") or {}
    token_conflicts = paper_index.get("token_conflicts") or {}
    matches: dict[str, dict[str, Any]] = {}
    for token in sorted(paper_identity.stable_identity_tokens(job)):
        conflict = token_conflicts.get(token)
        if isinstance(conflict, list):
            for paper in conflict:
                if isinstance(paper, dict):
                    matches[str(paper.get("path") or paper.get("canonical_id"))] = paper
            continue
        paper = by_token.get(token)
        if isinstance(paper, dict):
            matches[str(paper.get("path") or paper.get("canonical_id"))] = paper

    if len(matches) > 1:
        raise ValueError(
            "Research job identity resolves to multiple represented papers: "
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
