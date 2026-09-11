#!/usr/bin/env python3
"""Resolve metadata-backfill checkpoint merge conflicts conservatively.

This is a one-shot integration helper. Existing main paper bodies win; missing
frontmatter metadata is filled from the checkpoint. Training papers use the
checkpoint copy so the frozen-training baseline can remain exact. Runtime queue
state and derived views are handled by the calling workflow, not here.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
from typing import Any

import yaml


def run(*args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def show(stage: int, path: str) -> str | None:
    proc = run("git", "show", f":{stage}:{path}", check=False)
    return proc.stdout if proc.returncode == 0 else None


def parse_doc(text: str | None) -> tuple[dict[str, Any], str]:
    if text is None:
        return {}, ""
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    return yaml.safe_load(parts[1]) or {}, parts[2].lstrip("\n")


def empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


BACKFILL_KEYS = (
    "canonical_id",
    "arxiv_id",
    "doi",
    "openreview_id",
    "arxiv_categories",
    "title",
    "summary",
    "authors",
    "authors_affiliations",
    "published",
    "publication",
    "publication_type",
    "publication_status",
    "publication_version",
    "lineage",
    "topics",
    "importance",
    "hardware_evaluation",
    "hardware_details",
    "quality_effect",
    "storage_targets",
    "bottlenecks",
    "evidence_locations",
    "source",
    "sources",
    "code",
    "implementation",
    "implementation_status",
    "evaluation_type",
    "verified_arxiv_version",
    "source_last_revision",
    "last_checked",
    "last_verified",
)


def merge_paper(path: str) -> None:
    ours = show(2, path)
    theirs = show(3, path)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if ours is None and theirs is not None:
        target.write_text(theirs, encoding="utf-8")
        return
    if theirs is None and ours is not None:
        target.write_text(ours, encoding="utf-8")
        return
    if ours is None or theirs is None:
        raise RuntimeError(f"cannot resolve paper stages: {path}")

    ours_meta, ours_body = parse_doc(ours)
    theirs_meta, _ = parse_doc(theirs)
    merged = dict(ours_meta)

    for key in BACKFILL_KEYS:
        if key in theirs_meta and (key not in merged or empty(merged.get(key))):
            merged[key] = theirs_meta[key]

    # Keep explicit nulls for fields whose omission has different semantics.
    for key in ("doi", "openreview_id", "code"):
        if key in theirs_meta and key not in merged:
            merged[key] = theirs_meta[key]

    front = yaml.safe_dump(
        merged,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
        width=1000,
    ).rstrip()
    output = f"---\n{front}\n---\n\n{ours_body.lstrip()}"
    if not output.endswith("\n"):
        output += "\n"
    target.write_text(output, encoding="utf-8")


def checkout(side: str, path: str) -> None:
    run("git", "checkout", f"--{side}", "--", path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", required=False)
    parser.parse_args()

    raw = run("git", "diff", "--name-only", "--diff-filter=U").stdout
    conflicts = [line for line in raw.splitlines() if line.strip()]
    unresolved: list[str] = []

    for path in conflicts:
        if path.startswith(".survey/work-queue/") or path == ".survey/survey-state/paper-identity-index.json":
            checkout("ours", path)
        elif path.startswith("papers/training/") and path.endswith(".md") and not path.endswith("/README.md"):
            checkout("theirs", path)
        elif path.startswith("papers/") and path.endswith(".md") and not path.endswith("/README.md") and path != "papers/inference/comparison.md":
            merge_paper(path)
        elif path == "README.md" or path.endswith("/README.md") or path == "papers/inference/comparison.md":
            checkout("ours", path)
        elif (
            path.startswith(".survey/scripts/")
            or path.startswith(".survey/tests/")
            or path.startswith(".survey/templates/")
            or path.startswith(".survey/docs/survey-workflow/")
            or path == ".survey/survey-state/frozen-training.json"
            or path == ".survey/reports/metadata-coverage-latest.json"
        ):
            checkout("theirs", path)
        else:
            unresolved.append(path)
            continue
        run("git", "add", "--", path)

    if unresolved:
        print("Unresolved conflict paths:", file=sys.stderr)
        for path in unresolved:
            print(f"- {path}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
