#!/usr/bin/env python3
"""Build the repository inventory consumed by check_repository.py."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--output", required=True)
    ap.add_argument("--source-commit", default="working-tree")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    files = []
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if ".git" in rel.parts or "__pycache__" in rel.parts or ".venv" in rel.parts:
            continue
        if path.name.endswith((".pyc", ".tmp")):
            continue
        files.append({"path": rel.as_posix(), "sha": blob_sha(path.read_bytes())})
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"source_commit": args.source_commit, "files": files}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"inventory_files={len(files)} output={out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
