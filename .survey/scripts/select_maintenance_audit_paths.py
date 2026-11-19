#!/usr/bin/env python3
"""Select the paper subset for daily maintenance audits and normalization.

Differential mode for survey-maintenance (redesign Phase 1, item B4):
instead of auditing every paper every day, the daily subset is

  * every paper changed since the last committed paper-quality report
    (the "watermark" commit: the most recent commit that touched the
    report file), compared against the current working tree so that
    uncommitted changes made earlier in the same maintenance run are
    included, UNION
  * a deterministic daily rotation slice (sha256 of the repo-relative
    path modulo --rotation-days), so every paper is fully re-audited at
    least once per rotation period even if it never changes.

If no watermark commit exists, the subset falls back to all papers.
The full paper list comes from `git ls-tree` so no paper bodies are read.
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def git(repo_root: Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, default=Path("."))
    ap.add_argument(
        "--report-path",
        default=".survey/reports/paper-quality-latest.json",
        help="Committed report whose last-touching commit is the watermark.",
    )
    ap.add_argument("--rotation-days", type=int, default=7)
    ap.add_argument("--out", type=Path, required=True, help="Subset file to write.")
    ap.add_argument(
        "--changed-out",
        type=Path,
        required=True,
        help="File to write with only the changed-since-watermark papers.",
    )
    args = ap.parse_args()
    repo_root = args.repo_root.resolve()

    all_papers = sorted(
        line.strip()
        for line in git(repo_root, "ls-tree", "-r", "--name-only", "HEAD", "--", "papers").splitlines()
        if line.strip().endswith(".md")
    )

    watermark = git(
        repo_root, "log", "-1", "--format=%H", "--", args.report_path
    ).strip()
    if watermark:
        changed = sorted(
            line.strip()
            for line in git(
                repo_root, "diff", "--name-only", watermark, "--", "papers"
            ).splitlines()
            if line.strip().endswith(".md")
        )
    else:
        changed = list(all_papers)

    rotation_index = datetime.now(timezone.utc).date().toordinal() % args.rotation_days
    rotation = [
        path
        for path in all_papers
        if int(hashlib.sha256(path.encode("utf-8")).hexdigest(), 16) % args.rotation_days
        == rotation_index
    ]

    subset = sorted(set(changed) | set(rotation))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(subset) + ("\n" if subset else ""), encoding="utf-8")
    args.changed_out.write_text(
        "\n".join(changed) + ("\n" if changed else ""), encoding="utf-8"
    )
    print(
        f"maintenance_audit_subset: total={len(all_papers)} changed={len(changed)} "
        f"rotation={len(rotation)} subset={len(subset)} "
        f"rotation_index={rotation_index}/{args.rotation_days} "
        f"watermark={watermark[:12] or 'none'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
