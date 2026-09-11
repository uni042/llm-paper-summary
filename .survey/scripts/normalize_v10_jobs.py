#!/usr/bin/env python3
"""Normalize ready queue jobs to the workflow-v10 structured-record contract.

queue_worker.py intentionally remains v9-compatible. This small compatibility layer
removes legacy "return Markdown" wording from ready research/audit jobs so Scheduled
Chat sees one unambiguous artifact contract. It also snapshots the current paper blob
for ready audit jobs so later writes retain optimistic-concurrency protection without
requiring Scheduled Chat to discover the SHA itself.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

RESEARCH_INSTRUCTIONS = (
    "Read the primary source in full. Produce a repository-quality structured research "
    "record covering problem, novelty, method, evaluation conditions, key quantitative "
    "results, limitations, implementation status, and relation to existing repository "
    "lineages. Preserve publication date/status, implementation and source URLs; for an "
    "arXiv paper, record its primary and cross-list categories from arXiv. Do not infer "
    "missing text from abstracts/search snippets. Follow workflow "
    "v10 fixed-slot transport; do not send completed Markdown from Scheduled Chat."
)
RESEARCH_COMPLETION = (
    "Submit the complete workflow-v10 five-slot structured research record and source "
    "evidence. If full text is unavailable, return blocked with retrieval evidence "
    "instead of guessing."
)
AUDIT_INSTRUCTIONS = (
    "Perform a formal audit using primary sources: identity/bibliography, authors/"
    "affiliations, publication state/final version, code, hardware/model/dataset/"
    "baselines, quantitative results, simulation vs real hardware, classification, "
    "arXiv primary/cross-list categories, differences and limitations. Return a complete "
    "workflow-v10 five-slot structured "
    "research record; do not send completed Markdown from Scheduled Chat."
)
AUDIT_COMPLETION = (
    "Submit the audited workflow-v10 five-slot structured research record. If the "
    "required primary evidence cannot be obtained, return blocked/deferred rather than "
    "guessing."
)


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_json(path: Path, obj: dict) -> bool:
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def valid_paper_path(value: object) -> str | None:
    if not isinstance(value, str) or not value.startswith("papers/"):
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        return None
    return path.as_posix()


def backfill_expected_blob_sha(root: Path, job: dict) -> None:
    """Pin the paper revision once, when a ready audit first receives no SHA.

    Never refresh an existing expected_blob_sha: preserving the original snapshot is
    what lets preflight detect that another worker changed the paper meanwhile.
    """
    if job.get("type") != "audit" or job.get("expected_blob_sha"):
        return
    paper = valid_paper_path(job.get("paper_path"))
    if paper is None:
        return
    target = root.parent / paper
    if not target.is_file():
        return
    job["expected_blob_sha"] = git_blob_sha(target.read_bytes())


def normalize(root: Path) -> int:
    changed = 0
    jobs = root / "work-queue" / "jobs"
    for path in sorted(jobs.glob("*.json")):
        job = read_json(path)
        if job.get("status") != "ready":
            continue
        kind = job.get("type")
        if kind == "research":
            job["instructions"] = RESEARCH_INSTRUCTIONS
            job["completion"] = RESEARCH_COMPLETION
        elif kind == "audit":
            job["instructions"] = AUDIT_INSTRUCTIONS
            job["completion"] = AUDIT_COMPLETION
            backfill_expected_blob_sha(root, job)
        else:
            continue
        job["workflow_version"] = 10
        job["artifact_transport"] = "structured_record_v10"
        if write_json(path, job):
            changed += 1
    print(json.dumps({"normalized_ready_jobs": changed}, ensure_ascii=False))
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", type=Path, default=Path(".survey"))
    args = ap.parse_args()
    normalize(args.root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
