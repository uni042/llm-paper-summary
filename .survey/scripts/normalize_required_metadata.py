#!/usr/bin/env python3
"""Repair nullable required paper frontmatter keys without reformatting Markdown."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


FAMILIES = ("inference", "training", "survey")
SKIP_NAMES = {"README.md", "comparison.md"}


def _split_frontmatter(text: str) -> tuple[str, str, str] | None:
    if not text.startswith("---\n"):
        return None
    try:
        _, raw, body = text.split("---", 2)
    except ValueError:
        return None
    return "---", raw, body


def normalize_text(text: str) -> tuple[str, list[str]]:
    parts = _split_frontmatter(text)
    if parts is None:
        return text, []
    _, raw, body = parts
    meta = yaml.safe_load(raw) or {}
    if not isinstance(meta, dict) or body.lstrip().startswith("# Moved"):
        return text, []

    changes: list[str] = []
    raw_lines = raw.splitlines()
    if "code" not in meta:
        insert_at = next(
            (i for i, line in enumerate(raw_lines) if line.startswith("implementation:")),
            None,
        )
        if insert_at is None:
            insert_at = next(
                (i for i, line in enumerate(raw_lines) if line.startswith("last_checked:")),
                len(raw_lines),
            )
        raw_lines.insert(insert_at, "code: null")
        changes.append("code")

    if not changes:
        return text, []
    normalized_raw = "\n".join(raw_lines)
    return f"---{normalized_raw}\n---{body}", changes


def normalize_repo(root: Path, *, apply: bool) -> list[dict[str, object]]:
    changed: list[dict[str, object]] = []
    for family in FAMILIES:
        base = root / "papers" / family
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name in SKIP_NAMES:
                continue
            original = path.read_text(encoding="utf-8")
            normalized, fields = normalize_text(original)
            if not fields:
                continue
            changed.append({
                "path": path.relative_to(root).as_posix(),
                "fields": fields,
            })
            if apply:
                path.write_text(normalized, encoding="utf-8")
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = Path(args.repo_root).resolve()
    changed = normalize_repo(root, apply=args.apply)
    print(json.dumps({
        "changed_count": len(changed),
        "changed": changed,
        "applied": bool(args.apply),
    }, ensure_ascii=False, indent=2))
    if args.check and changed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
