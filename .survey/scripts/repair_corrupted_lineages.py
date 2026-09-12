#!/usr/bin/env python3
"""Repair lineage frontmatter corrupted by prose-term normalization.

The bug signature is intentionally narrow: a paper is changed only when its
current lineage exactly equals the result of applying the historical prose
normalizer to the canonical lineage slug encoded in its parent directory.
Legacy human-readable lineage labels are therefore left untouched.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from japanese_style import PREFERRED_TERMS, TERM_PATTERNS


LINEAGE_LINE = re.compile(r"(?m)^lineage:\s*(.+?)\s*$")
LINEAGE_DIR = re.compile(r"^\d+-(.+)$")


def _unquote_yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _historically_normalized_lineage(canonical: str) -> str:
    text = canonical
    for term, pattern in TERM_PATTERNS.items():
        preferred = PREFERRED_TERMS[term][0].split("／", 1)[0]
        text = pattern.sub(preferred, text)
    return text


def expected_lineage_repair(path: Path, current: str) -> str | None:
    """Return canonical lineage only for the exact historical bug signature."""
    match = LINEAGE_DIR.match(path.parent.name)
    if not match:
        return None
    canonical = match.group(1)
    corrupted = _historically_normalized_lineage(canonical)
    if corrupted != canonical and current == corrupted:
        return canonical
    return None


def repair_text(path: Path, text: str) -> tuple[str, bool]:
    if not text.startswith("---\n"):
        return text, False
    end = text.find("\n---\n", 4)
    if end < 0:
        return text, False
    frontmatter = text[4:end]
    match = LINEAGE_LINE.search(frontmatter)
    if not match:
        return text, False
    current = _unquote_yaml_scalar(match.group(1))
    replacement = expected_lineage_repair(path, current)
    if replacement is None:
        return text, False
    repaired_frontmatter = (
        frontmatter[: match.start()]
        + f"lineage: {replacement}"
        + frontmatter[match.end() :]
    )
    return "---\n" + repaired_frontmatter + text[end:], True


def candidate_papers(repo_root: Path):
    for section in ("inference", "training", "survey"):
        root = repo_root / "papers" / section
        if root.is_dir():
            yield from sorted(root.rglob("*.md"))


def repair_repository(repo_root: Path, *, write: bool) -> list[Path]:
    changed: list[Path] = []
    for path in candidate_papers(repo_root):
        source = path.read_text(encoding="utf-8")
        repaired, did_change = repair_text(path.relative_to(repo_root), source)
        if not did_change:
            continue
        changed.append(path)
        if write:
            path.write_text(repaired, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    changed = repair_repository(root, write=args.write)
    for path in changed:
        print(path.relative_to(root).as_posix())
    print(f"lineage_repairs={len(changed)}")
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
