#!/usr/bin/env python3
"""Select quality-audit targets added after the legacy-paper baseline."""
from __future__ import annotations

import subprocess
from pathlib import Path

PAPER_AUDIT_BASELINE = "c566e8afb54617375d01db261b1a609a9ef90524"
PAPER_PATHS = ("papers/inference", "papers/training", "papers/survey")


def added_paper_paths(repo_root: Path, baseline_commit: str = PAPER_AUDIT_BASELINE) -> set[str]:
    """Return paper paths introduced after baseline without reading paper contents."""
    root = Path(repo_root).resolve()
    ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", baseline_commit, "HEAD"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    if ancestor.returncode != 0:
        detail = ancestor.stderr.strip() or "baseline is not an ancestor of HEAD"
        raise RuntimeError(f"Cannot determine paper audit scope: {detail}")

    result = subprocess.run(
        [
            "git",
            "diff",
            "--diff-filter=A",
            "--name-only",
            "--no-renames",
            baseline_commit,
            "HEAD",
            "--",
            *PAPER_PATHS,
        ],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Cannot determine paper audit scope: " + result.stderr.strip())
    return {
        line.strip().replace("\\", "/")
        for line in result.stdout.splitlines()
        if line.strip().endswith(".md")
    }
