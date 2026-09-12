#!/usr/bin/env python3
"""Refresh the frozen-training membership baseline after authorized edits.

The Training family is frozen against adding/removing paper entries during normal
survey operation. Existing paper bodies and README/index files remain editable;
stored blob SHAs are historical references rather than content locks.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


POLICY = (
    "No new training paper entries. Existing training papers and README/index files may be edited; "
    "stored blob SHAs are historical baseline references only."
)


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
        "schema_version": 2,
        "source_commit": args.source,
        "policy": POLICY,
        "files": files,
    }
    target = root / ".survey/survey-state/frozen-training.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"frozen_training_files={len(files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
