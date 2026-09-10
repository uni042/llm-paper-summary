#!/usr/bin/env python3
"""Recover one archived research envelope whose completed job lacks its paper.

Fallback recovery may encounter an old queue job marked completed even though its
canonical Markdown artifact was never materialized. Such an envelope must not be
lost merely because the queue state is terminal. This helper replays one archived
complete research bundle through a currently safe record bank, leaving the
immutable archive untouched.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fallback_transport as ft


def recover(repo_root: Path) -> dict:
    repo_root = repo_root.resolve()
    archive = repo_root / ft.FALLBACK_ARCHIVE
    if not archive.is_dir():
        return {"action": "idle", "reason": "archive_missing"}

    for source in sorted(archive.glob("*.json")):
        try:
            envelope, _canonical = ft.parse_envelope(source.read_bytes())
        except Exception:
            continue
        if not ft.has_record_slots(envelope):
            continue
        payload = ft.chat_payload(envelope)
        if not payload:
            continue
        job_id = payload.get("job_id")
        paper_path = payload.get("paper_path")
        if not isinstance(job_id, str) or not job_id:
            continue
        if not isinstance(paper_path, str) or not paper_path:
            continue
        if (repo_root / paper_path).is_file():
            continue

        job = ft.read_object(repo_root / ".survey" / "work-queue" / "jobs" / f"{job_id}.json")
        if not job or job.get("status") != "completed":
            continue
        if not ft.chat_transport_settled(repo_root):
            return {"action": "deferred", "job_id": job_id, "reason": "chat transport still processing"}

        remapped, reason = ft.remap_research_bank(repo_root, envelope)
        if remapped is None:
            return {"action": "deferred", "job_id": job_id, "reason": reason}
        changed = ft.apply_envelope(repo_root, remapped)
        if any(write["path"] == ft.CHAT_INBOX for write in remapped["writes"]):
            (repo_root / ft.CHAT_RESULT).unlink(missing_ok=True)
        return {
            "action": "replayed_missing_artifact",
            "envelope_id": envelope["id"],
            "job_id": job_id,
            "paper_path": paper_path,
            "bank_selection": reason,
            "changed_paths": changed,
        }

    return {"action": "idle", "reason": "no_missing_completed_research_artifact"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(recover(args.repo_root), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
