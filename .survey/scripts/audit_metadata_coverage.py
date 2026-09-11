#!/usr/bin/env python3
"""Report completion of the canonical paper frontmatter metadata."""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml


REQUIRED = (
    "canonical_id", "title", "summary", "authors", "published", "publication",
    "publication_type", "publication_status", "source", "sources", "implementation",
    "code", "last_checked",
)


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    _, raw, body = text.split("---", 2)
    return yaml.safe_load(raw) or {}, body


def findings(path: Path, root: Path) -> list[str]:
    meta, body = frontmatter(path)
    if body.lstrip().startswith("# Moved"):
        return []
    missing = [
        key for key in REQUIRED
        if key not in meta or (key != "code" and meta.get(key) in (None, "", []))
    ]
    if meta.get("arxiv_id"):
        categories = meta.get("arxiv_categories")
        if not isinstance(categories, dict) or not categories.get("primary"):
            missing.append("arxiv_categories.primary")
        elif not isinstance(categories.get("cross_list", []), list):
            missing.append("arxiv_categories.cross_list")
    authors = meta.get("authors")
    if "authors" in meta and (not isinstance(authors, list) or not authors):
        missing.append("authors:list")
    sources = meta.get("sources")
    if "sources" in meta and (not isinstance(sources, list) or not sources):
        missing.append("sources:list")
    return sorted(set(missing))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--json-out")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    result: dict = {
        "schema_version": 1,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "required_fields": list(REQUIRED),
        "families": {},
    }
    total = complete = 0
    for family in ("inference", "training", "survey"):
        rows = []
        for path in sorted((root / "papers" / family).rglob("*.md")):
            if path.name in {"README.md", "comparison.md"}:
                continue
            missing = findings(path, root)
            _, body = frontmatter(path)
            if body.lstrip().startswith("# Moved"):
                continue
            rows.append({"path": path.relative_to(root).as_posix(), "missing": missing})
        bad = [row for row in rows if row["missing"]]
        result["families"][family] = {
            "total": len(rows),
            "complete": len(rows) - len(bad),
            "incomplete": bad,
        }
        total += len(rows)
        complete += len(rows) - len(bad)
    result["summary"] = {"total": total, "complete": complete, "incomplete": total - complete}
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_out:
        out = root / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 1 if args.strict and total != complete else 0


if __name__ == "__main__":
    raise SystemExit(main())
