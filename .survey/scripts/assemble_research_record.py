#!/usr/bin/env python3
"""Assemble workflow-v10 fixed structured research slots and render transient Markdown."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from render_paper import render_paper  # noqa: E402

TRANSPORT_VERSION = 10
MAX_SLOT_BYTES = 8192
FIXED_INBOX = ".survey/work-queue/submissions/chat-inbox.json"
LEGACY_PAYLOAD = ".survey/work-queue/payloads/chat-payload.md"
SLOT_NAMES = ["metadata", "problem_method", "evaluation", "results", "positioning"]
BANK_ROOTS = {
    "a": ".survey/work-queue/records/chat-record",
    "b": ".survey/work-queue/records/chat-record-b",
}


def slots_for_bank(bank: str) -> list[tuple[str, str]]:
    root = BANK_ROOTS[bank]
    return [(name, f"{root}/{name}.json") for name in SLOT_NAMES]


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def safe_rel(path_text: str) -> str:
    p = PurePosixPath(path_text)
    if p.is_absolute() or ".." in p.parts:
        raise ValueError(f"unsafe path: {path_text}")
    return p.as_posix()


def assemble(repo_root: Path) -> bool:
    inbox_path = repo_root / FIXED_INBOX
    inbox = read_json(inbox_path)
    refs = inbox.get("record_slots")
    if refs is None:
        return False
    if inbox.get("payload_chunks") is not None or inbox.get("payload_path") is not None:
        raise ValueError("record_slots cannot be combined with legacy payload fields")
    bank = str(inbox.get("record_bank") or "a").lower()
    if bank not in BANK_ROOTS:
        raise ValueError("record_bank must be a or b")
    slots = slots_for_bank(bank)
    if not isinstance(refs, list) or len(refs) != len(slots):
        raise ValueError(f"record_slots must contain exactly {len(slots)} entries")

    attempt_id = inbox.get("attempt_id")
    job_id = inbox.get("job_id")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ValueError("attempt_id is required")
    if not isinstance(job_id, str) or not job_id:
        raise ValueError("job_id is required")

    record: dict[str, Any] = {}
    total_bytes = 0
    for index, ((slot_name, expected_path), ref) in enumerate(zip(slots, refs), start=1):
        if not isinstance(ref, dict):
            raise ValueError(f"record_slots[{index - 1}] must be an object")
        if ref.get("slot") != slot_name:
            raise ValueError(f"record_slots[{index - 1}] must declare slot={slot_name}")
        path_text = safe_rel(str(ref.get("path") or ""))
        if path_text != expected_path:
            raise ValueError(f"slot {slot_name} must use fixed path {expected_path}")
        expected_sha = ref.get("blob_sha")
        if not isinstance(expected_sha, str) or not expected_sha:
            raise ValueError(f"slot {slot_name} requires blob_sha")

        path = repo_root / path_text
        if not path.is_file():
            raise ValueError(f"missing record slot: {path_text}")
        raw = path.read_bytes()
        if len(raw) > MAX_SLOT_BYTES:
            raise ValueError(f"record slot too large: {path_text} ({len(raw)} bytes)")
        if git_blob_sha(raw) != expected_sha:
            raise ValueError(f"record slot blob mismatch: {path_text}")

        payload = json.loads(raw.decode("utf-8"))
        if not isinstance(payload, dict):
            raise ValueError(f"{path_text} must contain an object")
        if int(payload.get("transport_version") or 0) != TRANSPORT_VERSION:
            raise ValueError(f"{path_text} transport_version must be {TRANSPORT_VERSION}")
        if payload.get("slot") != slot_name:
            raise ValueError(f"{path_text} slot mismatch")
        if payload.get("attempt_id") != attempt_id or payload.get("job_id") != job_id:
            raise ValueError(f"{path_text} attempt_id/job_id mismatch")
        data = payload.get("data")
        if not isinstance(data, dict):
            raise ValueError(f"{path_text} data must be an object")
        record[slot_name] = data
        total_bytes += len(raw)

    markdown = render_paper(record)
    (repo_root / LEGACY_PAYLOAD).write_text(markdown, encoding="utf-8")

    local_inbox = dict(inbox)
    local_inbox.pop("record_slots", None)
    local_inbox["payload_path"] = LEGACY_PAYLOAD
    local_inbox["transport_version"] = TRANSPORT_VERSION
    inbox_path.write_text(json.dumps(local_inbox, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "assembled": True,
        "transport_version": TRANSPORT_VERSION,
        "bank": bank,
        "slots": len(slots),
        "structured_bytes": total_bytes,
        "rendered_bytes": len(markdown.encode("utf-8")),
    }, ensure_ascii=False))
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()
    assemble(Path(args.repo_root).resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
