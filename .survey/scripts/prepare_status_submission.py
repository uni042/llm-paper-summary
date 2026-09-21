#!/usr/bin/env python3
"""Prepare a canonical status-only immutable submission before durable save.

Workers may collect retrieval context in a draft object, but blocked/deferred/rejected
submissions must never persist record-transport fields. This command is the single
mechanical boundary for preparing those descriptors: it strips transport-only fields,
validates the resulting descriptor with the canonical validator, and writes JSON only
after validation succeeds.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from immutable_submission import NONARTIFACT_STATUSES, validate_descriptor  # noqa: E402

TRANSPORT_FIELDS = ("record_bank", "record_slots", "paper_path", "expected_blob_sha")


def prepare(repo_root: Path, draft: dict) -> tuple[dict, list[str]]:
    if not isinstance(draft, dict):
        raise ValueError("status submission draft must be a JSON object")
    status = draft.get("status")
    if status not in NONARTIFACT_STATUSES:
        raise ValueError("prepare_status_submission only accepts blocked/deferred/rejected")

    cleaned = dict(draft)
    removed = [field for field in TRANSPORT_FIELDS if field in cleaned]
    for field in removed:
        cleaned.pop(field, None)

    normalized = validate_descriptor(repo_root, cleaned)
    return normalized, removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("draft", type=Path, help="JSON draft to canonicalize")
    parser.add_argument("output", type=Path, help="destination descriptor path")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()

    draft = json.loads(args.draft.read_text(encoding="utf-8"))
    normalized, removed = prepare(args.repo_root.resolve(), draft)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(normalized, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if removed:
        print("[WORKER-GUIDE] removed forbidden status-only transport fields: " + ", ".join(removed))
    print(f"[WORKER-GUIDE] status-only descriptor validated; next_action=save {args.output.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
