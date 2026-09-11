#!/usr/bin/env python3
"""Refresh the intentional frozen-training blob baseline after authorized metadata edits."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("utf-8") + data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--source", default="metadata-backfill-2026-09-11")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    training = root / "papers" / "training"
    files: dict[str, str] = {}
    for path in sorted(training.rglob("*.md")):
        rel = path.relative_to(root).as_posix()
        files[rel] = blob_sha(path.read_bytes())
    payload = {
        "schema_version": 1,
        "source_commit": args.source,
        "policy": "Read-only baseline; change only with explicit user authorization.",
        "files": files,
    }
    target = root / ".survey/survey-state/frozen-training.json"
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"frozen_training_files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
