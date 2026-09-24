#!/usr/bin/env python3
"""Read-only inventory for legacy data cleanup.

The report contains paths and metadata only. Paper Markdown bodies and live JSON
payloads are never opened or copied into the report.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
from typing import Any

ARCHIVE_PARTS = {"archive", "archives", "fallback-archive", "fallback-failed", "failed-archive", "transport-archive"}
LIVE_QUEUE_PARTS = {
    "jobs", "claims", "claim-requests", "claim-results", "records",
    "research-preflight", "submissions", "results", "run-state",
    "fallback-inbox", "discovery-preload",
}
LEGACY_PATH_MARKERS = (
    "chat-inbox.json", "legacy_", "legacy-", "legacy.", "deprecated",
    "compat", "retired", "v1-",
)
TEXT_SUFFIXES = {".md", ".py", ".yml", ".yaml", ".toml", ".txt", ".json"}
LEGACY_PATTERNS = (
    ("chat-inbox.json", re.compile(r"chat-inbox[.]json", re.IGNORECASE)),
    ("legacy_ prefix", re.compile(r"legacy_", re.IGNORECASE)),
    ("legacy term", re.compile(r"(?<![A-Za-z0-9_])legacy(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("deprecated term", re.compile(r"(?<![A-Za-z0-9_])deprecated(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("compat term", re.compile(r"(?<![A-Za-z0-9_])compat(?:ibility)?(?![A-Za-z0-9_])", re.IGNORECASE)),
    ("old Japanese summary heading", re.compile(r"## *一文要約")),
    ("retired alias", re.compile(r"legacy-unbanked-to-library", re.IGNORECASE)),
    ("old queue filename", re.compile(r"queue-v10[.]md", re.IGNORECASE)),
)
IGNORED_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__"}

def classify_path(relative: str) -> tuple[str, str, bool]:
    """Return (class, explanation, write_freeze_required). Never means delete."""
    parts = Path(relative).parts
    lower_parts = tuple(part.lower() for part in parts)
    if len(parts) >= 2 and parts[0] == "papers" and relative.lower().endswith(".md"):
        return ("PAPER_CONTENT_OUT_OF_SCOPE",
                "Paper body is counted by path only; no content-quality review.", False)
    if ".survey" in parts and "work-queue" in parts:
        if any(part in ARCHIVE_PARTS for part in lower_parts):
            return ("B_HISTORY_CANDIDATE",
                    "Archive-named queue path; verify references and terminal status before any cleanup.", True)
        if any(part in LIVE_QUEUE_PARTS for part in lower_parts):
            return ("A_LIVE_OR_RECOVERY",
                    "Current queue or recovery namespace; preserve pending a write freeze and reference check.", True)
    if any(marker in relative.lower() for marker in LEGACY_PATH_MARKERS):
        return ("C_LEGACY_REVIEW_CANDIDATE",
                "Path name suggests retired format; confirm current producers/readers before disposition.", True)
    if relative.startswith(".survey/reports/"):
        return ("E_REVIEW",
                "Generated report may be reproducible but can be an active dashboard input.", False)
    if any(part in {"tmp", "temp", "cache", "caches"} for part in lower_parts):
        return ("D_REGENERABLE_CANDIDATE",
                "Temporary/cache path; confirm regeneration and references before removal.", False)
    return ("E_UNCLASSIFIED",
            "No safe path-only classification rule; inspect producer, reader, schema, and lifecycle.", False)

def is_scannable_text(relative: str) -> bool:
    path = Path(relative)
    if path.suffix.lower() not in TEXT_SUFFIXES or not path.parts:
        return False
    if path.parts[0] == "papers":
        return False
    if ".survey" in path.parts and "work-queue" in path.parts:
        return False
    if path.parts[0] == ".survey" and path.parts[1:2] not in (("scripts",), ("docs",)):
        return False
    if path.parts[0] not in {".survey", ".github"} and path.parts[0] not in {"README.md", "AGENTS.md"}:
        return False
    if "tests" in path.parts or relative == ".survey/scripts/legacy_inventory.py":
        return False
    return True

def inventory(root: Path, source_commit: str | None = None) -> dict[str, Any]:
    root = root.resolve()
    entries: list[dict[str, Any]] = []
    paper_count = 0
    text_hits: list[dict[str, Any]] = []
    counters: Counter[str] = Counter()
    total_bytes = 0

    for current, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = sorted(name for name in dirnames if name not in IGNORED_DIRS)
        filenames.sort()
        current_path = Path(current)
        for filename in filenames:
            path = current_path / filename
            relative = path.relative_to(root).as_posix()
            try:
                stat = path.lstat()
            except OSError as exc:
                entries.append({"path": relative, "classification": "E_UNREADABLE",
                                "reason": f"Could not stat path: {exc.__class__.__name__}",
                                "write_freeze_required": False})
                counters["E_UNREADABLE"] += 1
                continue
            if not (path.is_file() or path.is_symlink()):
                continue
            size = stat.st_size
            total_bytes += size
            classification, reason, freeze = classify_path(relative)
            entries.append({
                "path": relative,
                "kind": "symlink" if path.is_symlink() else "file",
                "size_bytes": size,
                "classification": classification,
                "reason": reason,
                "write_freeze_required": freeze,
            })
            counters[classification] += 1
            if classification == "PAPER_CONTENT_OUT_OF_SCOPE":
                paper_count += 1
            if is_scannable_text(relative) and path.is_file() and not path.is_symlink():
                try:
                    with path.open("r", encoding="utf-8") as handle:
                        for line_number, line in enumerate(handle, 1):
                            for label, pattern in LEGACY_PATTERNS:
                                if pattern.search(line):
                                    text_hits.append({"path": relative, "line": line_number, "marker": label})
                except (UnicodeDecodeError, OSError):
                    continue

    return {
        "inventory_version": 1,
        "source_commit": source_commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
        "content_read_policy": {
            "paper_markdown": "path and size only; body not opened",
            "work_queue_payloads": "path and size only; payload not opened",
            "scanned_text": "scripts and workflow documentation only; report stores marker and line, not source text",
        },
        "summary": {
            "file_count": len(entries),
            "total_bytes": total_bytes,
            "paper_markdown_count": paper_count,
            "classifications": dict(sorted(counters.items())),
            "legacy_text_hit_count": len(text_hits),
            "unresolved_triage_count": counters["C_LEGACY_REVIEW_CANDIDATE"] + counters["E_UNCLASSIFIED"] + counters["E_UNREADABLE"],
            "write_freeze_required_count": sum(1 for item in entries if item.get("write_freeze_required")),
        },
        "entries": entries,
        "legacy_text_hits": text_hits,
    }

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--output", type=Path, help="write JSON report here; stdout when omitted")
    parser.add_argument("--source-commit", help="commit SHA for this snapshot")
    args = parser.parse_args(argv)
    report = inventory(args.root, args.source_commit)
    rendered = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
