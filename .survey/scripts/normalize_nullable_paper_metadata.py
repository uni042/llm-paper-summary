#!/usr/bin/env python3
"""Add required nullable metadata keys without reformatting paper frontmatter."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

CODE_KEY_RE = re.compile(r"(?m)^code\s*:")
LAST_CHECKED_RE = re.compile(r"(?m)^last_checked\s*:")


def normalize_text(text: str) -> tuple[str, bool]:
    if not text.startswith("---\n"):
        return text, False
    end = text.find("\n---", 4)
    if end < 0:
        return text, False
    frontmatter = text[4:end]
    if CODE_KEY_RE.search(frontmatter):
        return text, False

    match = LAST_CHECKED_RE.search(frontmatter)
    if match:
        insert_at = 4 + match.start()
    else:
        insert_at = end
    prefix = text[:insert_at]
    if prefix and not prefix.endswith("\n"):
        prefix += "\n"
    return prefix + "code: null\n" + text[insert_at:], True


def normalize_repo(repo_root: Path) -> list[str]:
    root = Path(repo_root).resolve()
    papers = root / "papers"
    changed: list[str] = []
    for path in sorted(papers.rglob("*.md")) if papers.is_dir() else []:
        original = path.read_text(encoding="utf-8")
        updated, did_change = normalize_text(original)
        if not did_change:
            continue
        path.write_text(updated, encoding="utf-8")
        changed.append(path.relative_to(root).as_posix())
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    for path in normalize_repo(args.repo_root):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
