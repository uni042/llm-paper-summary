#!/usr/bin/env python3
"""Normalize nullable paper metadata fields without inventing values."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


PAPER_FAMILIES = ("inference", "training", "survey")
NULLABLE_DEFAULTS = {
    "code": None,
    # Presence is required structurally, but a missing historical audit must not
    # be rewritten as if a full scientific audit had actually been performed.
    "last_audited": None,
    "audit_version": 0,
}


def normalize_file(path: Path, apply: bool) -> bool:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        return False
    parts = raw.split("---", 2)
    meta = yaml.safe_load(parts[1]) or {}
    changed = False
    for key, value in NULLABLE_DEFAULTS.items():
        if key not in meta:
            meta[key] = value
            changed = True
    if changed and apply:
        frontmatter = yaml.safe_dump(
            meta,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False,
            width=1000,
        ).rstrip()
        path.write_text(f"---\n{frontmatter}\n---{parts[2]}", encoding="utf-8")
    return changed


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    changed = []
    for family in PAPER_FAMILIES:
        paper_root = root / "papers" / family
        if not paper_root.exists():
            continue
        for path in sorted(paper_root.rglob("*.md")):
            if path.name in {"README.md", "comparison.md"}:
                continue
            if normalize_file(path, args.apply):
                changed.append(path.relative_to(root).as_posix())
    print(f"normalized_nullable_metadata={len(changed)}")
    for path in changed:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
