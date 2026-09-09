#!/usr/bin/env python3
"""Assemble fixed Chat payload chunks transiently for queue_worker.py.

Chat writes several small, pre-created chunk files plus a small inbox manifest.
GitHub Actions verifies the exact Git blob SHA of every referenced chunk, assembles
those chunks into the legacy fixed payload only in the runner workspace, and then
queue_worker.py consumes that transient payload. The assembled file is restored
before commit, so the repository never stores the assembled long Markdown through
this transport path.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

MAX_CHUNKS = 8
MAX_CHUNK_BYTES = 8192
MAX_TOTAL_BYTES = MAX_CHUNKS * MAX_CHUNK_BYTES
CHUNK_PREFIX = ".survey/work-queue/payloads/chat-chunks/part-"
LEGACY_PAYLOAD = ".survey/work-queue/payloads/chat-payload.md"
FIXED_INBOX = ".survey/work-queue/submissions/chat-inbox.json"


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def expected_chunk_path(index: int) -> str:
    return f"{CHUNK_PREFIX}{index:02d}.md"


def validate_relpath(path_text: str) -> str:
    p = PurePosixPath(path_text)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"unsafe chunk path: {path_text}")
    return p.as_posix()


def assemble(repo_root: Path) -> bool:
    inbox_path = repo_root / FIXED_INBOX
    inbox = read_json(inbox_path)
    chunks = inbox.get("payload_chunks")
    if chunks is None:
        return False
    if inbox.get("payload_path") is not None:
        raise ValueError("use payload_chunks or payload_path, not both")
    if not isinstance(chunks, list) or not 1 <= len(chunks) <= MAX_CHUNKS:
        raise ValueError(f"payload_chunks must contain 1-{MAX_CHUNKS} entries")

    parts: list[str] = []
    total_bytes = 0
    for idx, item in enumerate(chunks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"payload_chunks[{idx - 1}] must be an object")
        path_text = item.get("path")
        expected_sha = item.get("blob_sha")
        if not isinstance(path_text, str) or not isinstance(expected_sha, str):
            raise ValueError("each payload chunk requires path and blob_sha strings")
        path_text = validate_relpath(path_text)
        wanted = expected_chunk_path(idx)
        if path_text != wanted:
            raise ValueError(f"chunks must use contiguous fixed slots in order; expected {wanted}")
        path = repo_root / path_text
        if not path.is_file():
            raise ValueError(f"missing payload chunk: {path_text}")
        raw = path.read_bytes()
        if len(raw) > MAX_CHUNK_BYTES:
            raise ValueError(f"payload chunk too large: {path_text} ({len(raw)} bytes)")
        actual_sha = git_blob_sha(raw)
        if actual_sha != expected_sha:
            raise ValueError(
                f"payload chunk blob mismatch for {path_text}: expected {expected_sha}, current {actual_sha}"
            )
        text = raw.decode("utf-8")
        if not text.endswith("\n"):
            text += "\n"
        parts.append(text)
        total_bytes += len(text.encode("utf-8"))

    if total_bytes < 500:
        raise ValueError("assembled payload is too short for completed research/audit")
    if total_bytes > MAX_TOTAL_BYTES:
        raise ValueError("assembled payload exceeds maximum transport size")

    assembled_path = repo_root / LEGACY_PAYLOAD
    assembled_path.write_text("".join(parts), encoding="utf-8")

    local_inbox = dict(inbox)
    local_inbox.pop("payload_chunks", None)
    local_inbox["payload_path"] = LEGACY_PAYLOAD
    inbox_path.write_text(json.dumps(local_inbox, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"assembled": True, "chunks": len(chunks), "bytes": total_bytes}, ensure_ascii=False))
    return True


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    assemble(repo_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
