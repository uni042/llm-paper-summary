#!/usr/bin/env python3
"""Suppress duplicate discovery-generated research jobs before Chat sees them.

This is deliberately separate from queue_worker.py. The queue worker owns state
transitions; this guard repairs/filters research jobs against the canonical
identity snapshot, pending identity deltas, and current paper frontmatter.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import survey  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default: Any = None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> bool:
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def norm_title(value: Any) -> str | None:
    if not value:
        return None
    text = re.sub(r"\s+", " ", str(value)).strip().casefold()
    text = re.sub(r"[^\w\s]", "", text)
    return text or None


def safe_norm_id(value: Any) -> str | None:
    if not value:
        return None
    text = str(value).strip()
    try:
        return survey.norm_id(text)
    except Exception:
        return text


def ids_from_url(value: Any) -> set[str]:
    if not value:
        return set()
    raw = str(value).strip()
    out: set[str] = set()
    try:
        parsed = urlparse(raw)
    except Exception:
        return out
    host = parsed.netloc.casefold()
    path = unquote(parsed.path)
    if host.endswith("arxiv.org"):
        m = re.search(r"/(?:abs|html|pdf)/([^/?#]+)", path, re.I)
        if m:
            ident = m.group(1).removesuffix(".pdf")
            try:
                out.add(survey.norm_id("arXiv:" + ident))
            except Exception:
                pass
    if host in {"doi.org", "www.doi.org"}:
        body = path.lstrip("/")
        if body:
            try:
                out.add(survey.norm_id("DOI:" + body))
            except Exception:
                pass
    return out


def add_record(
    by_id: dict[str, tuple[str, str | None]],
    by_title: dict[str, tuple[str, str | None]],
    canonical: Any,
    identifiers: list[Any] | tuple[Any, ...] | set[Any] | None,
    path: Any,
    title: Any = None,
):
    cid = safe_norm_id(canonical)
    if not cid:
        return
    relpath = str(path) if path else None
    by_id[cid] = (cid, relpath)
    for ident in identifiers or []:
        nid = safe_norm_id(ident)
        if nid:
            by_id[nid] = (cid, relpath)
    nt = norm_title(title)
    if nt:
        by_title[nt] = (cid, relpath)


def build_identity(root: Path):
    by_id: dict[str, tuple[str, str | None]] = {}
    by_title: dict[str, tuple[str, str | None]] = {}

    snapshot = read_json(root / "survey-state" / "paper-identity-index.json", {}) or {}
    papers = snapshot.get("papers") or {}
    if isinstance(papers, dict):
        for canonical, rec in papers.items():
            if not isinstance(rec, dict):
                rec = {}
            add_record(by_id, by_title, canonical, rec.get("identifiers") or [], rec.get("path"))
    aliases = snapshot.get("identifier_to_canonical") or {}
    if isinstance(aliases, dict):
        for ident, canonical in aliases.items():
            cid = safe_norm_id(canonical)
            nid = safe_norm_id(ident)
            rec = papers.get(canonical, {}) if isinstance(papers, dict) else {}
            if cid and nid:
                by_id[nid] = (cid, rec.get("path") if isinstance(rec, dict) else None)

    delta_root = root / "survey-state" / "identity-deltas"
    if delta_root.exists():
        for p in sorted(delta_root.rglob("*.json")):
            rec = read_json(p, {}) or {}
            if isinstance(rec, dict):
                add_record(
                    by_id,
                    by_title,
                    rec.get("canonical_id"),
                    rec.get("identifiers") or [],
                    rec.get("path"),
                )

    # Current papers are the final fallback and also provide titles, which the
    # compact identity snapshot intentionally does not store.
    survey.ROOT = root
    for rec in survey.papers():
        add_record(
            by_id,
            by_title,
            rec.get("canonical_id"),
            rec.get("identifiers") or [],
            rec.get("path"),
            rec.get("title"),
        )
    return by_id, by_title


def duplicate_hit(job: dict, by_id, by_title):
    ids: set[str] = set()
    cid = safe_norm_id(job.get("canonical_id"))
    if cid:
        ids.add(cid)
    ids.update(ids_from_url(job.get("source_url")))
    for ident in ids:
        if ident in by_id:
            return by_id[ident], "identifier", ident
    title = norm_title(job.get("title"))
    if title and title in by_title:
        return by_title[title], "title", title
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(".survey"))
    args = parser.parse_args()
    root = args.root.resolve()
    jobs_dir = root / "work-queue" / "jobs"
    jobs_dir.mkdir(parents=True, exist_ok=True)
    by_id, by_title = build_identity(root)

    changed = []
    for path in sorted(jobs_dir.glob("*.json")):
        job = read_json(path, {}) or {}
        # Only discovery-created research jobs are safe to auto-suppress.
        # Audit/update work may intentionally target an existing paper.
        if job.get("status") != "ready" or job.get("type") != "research" or not job.get("parent_job_id"):
            continue
        hit = duplicate_hit(job, by_id, by_title)
        if not hit:
            continue
        (canonical, paper_path), matched_by, matched_value = hit
        job["status"] = "superseded"
        job["completed_at"] = now()
        job["superseded_reason"] = "duplicate already represented in repository"
        job["duplicate_of_canonical_id"] = canonical
        job["duplicate_of_path"] = paper_path
        job["duplicate_match"] = {"by": matched_by, "value": matched_value}
        if write_json(path, job):
            changed.append(job.get("job_id"))

    print(json.dumps({"suppressed_duplicate_jobs": changed, "count": len(changed)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
