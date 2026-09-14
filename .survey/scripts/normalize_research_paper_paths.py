#!/usr/bin/env python3
"""Persist deterministic paper paths for Research jobs that still carry null paths."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from paper_path_resolver import resolve_paper_path


def _read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def _write_object(path: Path, value: dict[str, Any]) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _has_identity(job: dict[str, Any]) -> bool:
    return any(
        isinstance(job.get(key), str) and bool(str(job.get(key)).strip())
        for key in ("canonical_id", "source_url", "title")
    )


def normalize(repo_root: Path, *, apply: bool = False) -> dict[str, Any]:
    """Fill missing Research ``paper_path`` fields without changing explicit paths.

    The resolver intentionally uses the repository's final ``99-other`` inference
    bucket when discovery did not classify a paper. Jobs without any stable identity
    are reported and left untouched rather than receiving a collision-prone fabricated
    path.
    """
    repo_root = Path(repo_root).resolve()
    jobs_root = repo_root / ".survey/work-queue/jobs"
    updated_paths: list[str] = []
    unresolved_paths: list[str] = []
    scanned = 0

    if not jobs_root.is_dir():
        return {
            "schema_version": 1,
            "scanned_research_jobs": 0,
            "updated": 0,
            "unresolved": 0,
            "updated_paths": [],
            "unresolved_paths": [],
            "apply": bool(apply),
        }

    for path in sorted(jobs_root.glob("*.json")):
        job = _read_object(path)
        if job is None or job.get("type") != "research":
            continue
        scanned += 1
        if job.get("paper_path") is not None:
            continue
        relative = path.relative_to(repo_root).as_posix()
        if not _has_identity(job):
            unresolved_paths.append(relative)
            continue
        try:
            paper_path = resolve_paper_path(job)
        except (TypeError, ValueError):
            unresolved_paths.append(relative)
            continue
        if apply:
            job["paper_path"] = paper_path
            _write_object(path, job)
        updated_paths.append(relative)

    return {
        "schema_version": 1,
        "scanned_research_jobs": scanned,
        "updated": len(updated_paths),
        "unresolved": len(unresolved_paths),
        "updated_paths": updated_paths,
        "unresolved_paths": unresolved_paths,
        "apply": bool(apply),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="return a non-zero status when any Research job cannot be normalized",
    )
    args = parser.parse_args()
    result = normalize(args.repo_root, apply=args.apply)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if args.strict and result["unresolved"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
