#!/usr/bin/env python3
"""Dependency-aware Google Drive outbox importer for survey spillover work.

This extends the backlog-safe v2 importer with cross-envelope dependency checks.
A research/audit bundle whose canonical GitHub job has not materialized yet is
left pending rather than submitted as an unknown job. This lets offline job
seeds and multiple completed research payloads accumulate safely while GitHub
writes are unavailable, even when they are split across fallback outboxes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import import_drive_outbox_v2 as v2  # noqa: E402

base = v2.base


def chat_payload(envelope: dict[str, Any]) -> dict[str, Any] | None:
    for write in envelope["writes"]:
        if write["path"] != v2.CHAT_INBOX:
            continue
        value = json.loads(write["content"])
        return value if isinstance(value, dict) else None
    return None


def has_record_slots(envelope: dict[str, Any]) -> bool:
    return any(
        write["path"].startswith(prefix)
        for write in envelope["writes"]
        for prefix in v2.BANK_PATH_PREFIXES
    )


def dependency_state(repo_root: Path, envelope: dict[str, Any]) -> tuple[bool, str | None]:
    """Return whether an envelope may be replayed against the current GitHub state."""
    if not has_record_slots(envelope):
        return True, None

    payload = chat_payload(envelope)
    if payload is None:
        return False, "record bundle has no chat-inbox payload"
    job_id = payload.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return False, "record bundle has no job_id"

    job_path = repo_root / ".survey" / "work-queue" / "jobs" / f"{job_id}.json"
    if not job_path.is_file():
        return False, f"canonical GitHub job not materialized yet: {job_id}"
    return True, None


def pull(args: argparse.Namespace) -> int:
    service = base.drive_service()
    pending_id = base.folder_id("DRIVE_PENDING_FOLDER_ID")
    failed_id = base.os.environ.get("DRIVE_FAILED_FOLDER_ID", "").strip()
    repo_root = Path(args.repo_root).resolve()
    chat_idle = v2.chat_transport_settled(repo_root)
    manifest: dict[str, Any] = {
        "schema_version": 3,
        "accepted": [],
        "failed": [],
        "deferred_busy": [],
        "deferred_dependency": [],
    }

    # Oldest-first. Invalid entries are quarantined. Busy or dependency-blocked
    # research entries remain pending while later independent control/update
    # envelopes may still pass.
    for meta in base.list_pending(service, pending_id):
        name = meta.get("name", meta["id"])
        if not str(name).lower().endswith(".json"):
            message = "pending outbox accepts .json envelopes only"
            manifest["failed"].append({"drive_file_id": meta["id"], "name": name, "error": message})
            if failed_id:
                base.move_file(service, meta, failed_id)
            continue

        try:
            raw = base.download_bytes(service, meta["id"])
            data = json.loads(raw.decode("utf-8"))
            envelope = base.validate_envelope(data)
            v2.validate_logical_bundle(envelope)

            ready, dependency_reason = dependency_state(repo_root, envelope)
            if not ready:
                manifest["deferred_dependency"].append(
                    {
                        "drive_file_id": meta["id"],
                        "name": name,
                        "reason": dependency_reason,
                    }
                )
                continue

            if v2.is_chat_envelope(envelope) and not chat_idle:
                manifest["deferred_busy"].append(
                    {
                        "drive_file_id": meta["id"],
                        "name": name,
                        "reason": "chat transport still processing",
                    }
                )
                continue

            changed_paths = v2.apply_envelope(repo_root, envelope)
            manifest["accepted"].append(
                {
                    "drive_file_id": meta["id"],
                    "name": name,
                    "envelope_id": envelope["id"],
                    "sha256": hashlib.sha256(raw).hexdigest(),
                    "changed_paths": changed_paths,
                    "parents": meta.get("parents", []),
                }
            )
            break
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            manifest["failed"].append({"drive_file_id": meta["id"], "name": name, "error": message})
            if failed_id:
                base.move_file(service, meta, failed_id)

    Path(args.manifest).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "accepted": len(manifest["accepted"]),
                "failed": len(manifest["failed"]),
                "deferred_busy": len(manifest["deferred_busy"]),
                "deferred_dependency": len(manifest["deferred_dependency"]),
                "changed_paths": sum(len(x["changed_paths"]) for x in manifest["accepted"]),
            },
            ensure_ascii=False,
        )
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("pull", "ack"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", default=".drive-outbox-manifest.json")
    args = parser.parse_args()
    return pull(args) if args.command == "pull" else base.ack(args)


if __name__ == "__main__":
    raise SystemExit(main())
