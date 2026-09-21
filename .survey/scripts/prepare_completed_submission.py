#!/usr/bin/env python3
"""Build a completed immutable descriptor from the reserved record bank."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from immutable_submission import TRANSPORT_VERSION, validate_descriptor
from record_bank_config import BANK_ROOTS, SLOT_NAMES


def _blob_sha(repo: Path, rel: str) -> str:
    result = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], cwd=repo, text=True, capture_output=True, check=False)
    sha = result.stdout.strip()
    if result.returncode != 0 or len(sha) != 40:
        raise ValueError(f"record slot must be committed before submission: {rel}")
    return sha


def build(repo: Path, *, kind: str, attempt_id: str, job_id: str, record_bank: str, paper_path: str | None = None, expected_blob_sha: str | None = None) -> dict:
    repo = repo.resolve()
    bank = record_bank.lower()
    if bank not in BANK_ROOTS:
        raise ValueError("record_bank must be registered")
    root = BANK_ROOTS[bank]
    descriptor = {
        "schema_version": 1,
        "transport_version": TRANSPORT_VERSION,
        "kind": kind,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "status": "completed",
        "record_bank": bank,
        "record_slots": [
            {"slot": slot, "path": f"{root}/{slot}.json", "blob_sha": _blob_sha(repo, f"{root}/{slot}.json")}
            for slot in SLOT_NAMES
        ],
    }
    if paper_path:
        descriptor["paper_path"] = paper_path
    if expected_blob_sha:
        descriptor["expected_blob_sha"] = expected_blob_sha
    return validate_descriptor(repo, descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--kind", required=True, choices=("research", "audit"))
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--record-bank", required=True)
    parser.add_argument("--paper-path")
    parser.add_argument("--expected-blob-sha")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    descriptor = build(args.repo_root, kind=args.kind, attempt_id=args.attempt_id, job_id=args.job_id, record_bank=args.record_bank, paper_path=args.paper_path, expected_blob_sha=args.expected_blob_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[WORKER-GUIDE] completed descriptor validated and written; commit this exact output without manual edits")
    print(json.dumps({"ok": True, "next_action": "commit_exact_descriptor_then_wait_for_submission_result", "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
