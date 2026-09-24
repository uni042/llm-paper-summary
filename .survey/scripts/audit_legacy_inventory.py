#!/usr/bin/env python3
"""Build a read-only, reviewable inventory for legacy-removal work."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

CLASSES = {"A", "B", "C", "D", "E"}
IGNORED_PARTS = {".git", ".venv", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}
LEGACY_MARKERS = {
    "fixed_chat_inbox": re.compile(r"chat-inbox\.json", re.IGNORECASE),
    "legacy_unbanked_migration": re.compile(r"legacy-unbanked-to-library", re.IGNORECASE),
    "legacy_lease_original": re.compile(r"legacy_lease_original_expires_at", re.IGNORECASE),
    "legacy_lease_normalized": re.compile(r"legacy_lease_normalized_at", re.IGNORECASE),
    "scheduled_chat_alias": re.compile(r"scheduled-chat-llm-survey", re.IGNORECASE),
    "old_record_bank_root": re.compile(r"chat-record-a(?:/|\\b)", re.IGNORECASE),
    "old_summary_heading": re.compile(r"^##\\s+一文要約\\s*$", re.MULTILINE),
    "transport_v9": re.compile(r"""["']transport_version["']\\s*:\\s*9\\b""", re.IGNORECASE),
}


def _git_blob_sha(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\\0"
    return hashlib.sha1(header + data).hexdigest()


def _safe_relative_path(raw: Any) -> str:
    if not isinstance(raw, str) or not raw:
        raise ValueError("classification paths must be non-empty strings")
    normalized = raw.replace("\\", "/")
    path = PurePosixPath(normalized)
    if path.is_absolute() or ".." in path.parts or normalized.startswith("./"):
        raise ValueError(f"classification path must be repository-relative: {raw!r}")
    return path.as_posix()


def _read_payload(path: Path) -> tuple[bytes, str]:
    if path.is_symlink():
        return os.readlink(path).encode("utf-8"), "symlink"
    return path.read_bytes(), "file"


def _classification_map(raw: Any) -> dict[str, dict[str, str]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("classifications must be a JSON object keyed by repository path")
    result: dict[str, dict[str, str]] = {}
    for path, entry in raw.items():
        safe_path = _safe_relative_path(path)
        if not isinstance(entry, dict):
            raise ValueError(f"classification for {safe_path} must be an object")
        category = entry.get("class")
        if category not in CLASSES:
            raise ValueError(f"{safe_path}: class must be one of A, B, C, D, E")
        reason = entry.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{safe_path}: reason is required for every classification")
        result[safe_path] = {"class": category, "reason": reason.strip()}
    return result


def _source_commit(root: Path, supplied: str | None) -> str:
    value = supplied
    if not value:
        try:
            value = subprocess.run(
                ["git", "-C", str(root), "rev-parse", "HEAD"],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
        except (OSError, subprocess.CalledProcessError) as exc:
            raise ValueError("--source-commit is required outside a Git checkout") from exc
    if not re.fullmatch(r"[0-9a-fA-F]{40}", value):
        raise ValueError("source_commit must be a full 40-character Git commit SHA")
    return value.lower()


def _legacy_markers(data: bytes) -> tuple[list[str], str]:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return [], "unscannable_binary"
    if "\\0" in text:
        return [], "unscannable_binary"
    hits = [name for name, pattern in LEGACY_MARKERS.items() if pattern.search(text)]
    return hits, "scanned"


def build_inventory(
    root: Path,
    *,
    source_commit: str,
    classifications: Any = None,
    exclude_paths: Iterable[str] = (),
) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"repository root is not a directory: {root}")
    commit = _source_commit(root, source_commit)
    reviewed = _classification_map(classifications)
    excluded = {_safe_relative_path(p) for p in exclude_paths}
    candidates = []
    for path in root.rglob("*"):
        relative = path.relative_to(root).as_posix()
        if any(part in IGNORED_PARTS for part in PurePosixPath(relative).parts):
            continue
        if relative in excluded or not (path.is_symlink() or path.is_file()):
            continue
        candidates.append((relative, path))
    present = {relative for relative, _ in candidates}
    stale = sorted(set(reviewed) - present)
    if stale:
        raise ValueError("classification path does not exist: " + ", ".join(stale[:10]))

    rows = []
    counts = {category: 0 for category in sorted(CLASSES)}
    unclassified_count = 0
    marker_count = 0
    unreviewed_marker_count = 0
    unscannable_count = 0
    for relative, path in sorted(candidates):
        data, kind = _read_payload(path)
        markers, scan_status = _legacy_markers(data)
        entry = reviewed.get(relative)
        category = entry["class"] if entry else None
        reason = entry["reason"] if entry else None
        if category is None:
            unclassified_count += 1
        else:
            counts[category] += 1
        marker_count += len(markers)
        if markers and category is None:
            unreviewed_marker_count += 1
        if scan_status != "scanned":
            unscannable_count += 1
        rows.append({
            "path": relative,
            "kind": kind,
            "size_bytes": len(data),
            "sha": _git_blob_sha(data),
            "classification": category,
            "classification_reason": reason,
            "legacy_markers": markers,
            "content_scan": scan_status,
        })

    legacy_remaining = (
        counts["C"] + counts["E"] + unclassified_count + unscannable_count
    )
    counts["UNREVIEWED"] = unclassified_count
    counts["UNSCANNABLE"] = unscannable_count
    return {
        "schema_version": 1,
        "source_commit": commit,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "review_required" if legacy_remaining or unreviewed_marker_count else "classified",
        "file_count": len(rows),
        "classification_counts": counts,
        "unclassified_count": unclassified_count,
        "legacy_marker_count": marker_count,
        "unreviewed_marker_count": unreviewed_marker_count,
        "unscannable_count": unscannable_count,
        "legacy_remaining": legacy_remaining,
        "cleanup_remaining": counts["D"],
        "files": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--source-commit")
    parser.add_argument("--classifications", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    policy = None
    if args.classifications:
        policy = json.loads(args.classifications.read_text(encoding="utf-8"))
    output_relative = None
    try:
        output_relative = args.output.resolve().relative_to(args.root.resolve()).as_posix()
    except ValueError:
        pass
    report = build_inventory(
        args.root,
        source_commit=args.source_commit,
        classifications=policy,
        exclude_paths=[output_relative] if output_relative else (),
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({
        "status": report["status"],
        "source_commit": report["source_commit"],
        "files": report["file_count"],
        "legacy_remaining": report["legacy_remaining"],
        "unreviewed_markers": report["unreviewed_marker_count"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
