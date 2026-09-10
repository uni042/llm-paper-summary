#!/usr/bin/env python3
"""Move one Google Drive fallback envelope into the immutable GitHub intake queue.

Unlike v1-v3, this importer never expands an envelope into reusable record-bank
or Chat inbox files.  It only validates the envelope and creates/recognizes one
immutable file under `.survey/work-queue/fallback-inbox/`.  The normal survey
helper later serializes dispatch.  Therefore Drive recovery and ChatGPT Library
recovery may run independently without racing on fixed transport paths.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import fallback_transport as ft
import import_drive_outbox as drive


def pull(args: argparse.Namespace) -> int:
    service = drive.drive_service()
    pending_id = drive.folder_id("DRIVE_PENDING_FOLDER_ID")
    failed_id = drive.os.environ.get("DRIVE_FAILED_FOLDER_ID", "").strip()
    repo_root = Path(args.repo_root).resolve()
    manifest: dict[str, Any] = {
        "schema_version": 4,
        "accepted": [],
        "failed": [],
    }

    # Intake at most one valid logical envelope per importer run. Invalid entries
    # are quarantined and do not block later valid entries.
    for meta in drive.list_pending(service, pending_id):
        name = meta.get("name", meta["id"])
        if not str(name).lower().endswith(".json"):
            message = "pending outbox accepts .json envelopes only"
            manifest["failed"].append({"drive_file_id": meta["id"], "name": name, "error": message})
            if failed_id:
                drive.move_file(service, meta, failed_id)
            continue

        try:
            raw = drive.download_bytes(service, meta["id"])
            envelope, canonical = ft.parse_envelope(raw)
            intake = ft.intake(repo_root, envelope, canonical)
            changed_paths = [intake["path"]] if intake["status"] == "created" else []
            manifest["accepted"].append(
                {
                    "drive_file_id": meta["id"],
                    "name": name,
                    "envelope_id": envelope["id"],
                    "sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
                    "intake_status": intake["status"],
                    "changed_paths": changed_paths,
                    "parents": meta.get("parents", []),
                }
            )
            break
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            manifest["failed"].append({"drive_file_id": meta["id"], "name": name, "error": message})
            if failed_id:
                drive.move_file(service, meta, failed_id)

    Path(args.manifest).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "accepted": len(manifest["accepted"]),
                "failed": len(manifest["failed"]),
                "created": sum(1 for x in manifest["accepted"] if x.get("intake_status") == "created"),
                "deduplicated": sum(1 for x in manifest["accepted"] if x.get("intake_status") != "created"),
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
    return pull(args) if args.command == "pull" else drive.ack(args)


if __name__ == "__main__":
    raise SystemExit(main())
