#!/usr/bin/env python3
"""Backlog-safe Google Drive outbox importer for the survey workflow.

Key guarantees:
- accepts all pre-created v10 record banks A-H;
- imports at most one logical envelope per run;
- never overwrites a still-unprocessed reusable Chat inbox;
- invalid envelopes are quarantined without blocking later valid entries;
- busy research envelopes stay pending while independent update envelopes may pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import import_drive_outbox as base  # noqa: E402
from record_bank_config import BANK_PATH_PREFIXES, SLOT_NAMES  # noqa: E402

CHAT_INBOX = ".survey/work-queue/submissions/chat-inbox.json"
CHAT_RESULT = ".survey/work-queue/results/chat-inbox.json"
GENERIC_PREFIXES = (
    ".survey/work-queue/submissions/",
    ".survey/work-queue/transport/",
    ".survey/update-worker/",
)

# Extend the base validator to all pre-created banks while preserving the small
# transport-only allowlist.
base.ALLOWED_PREFIXES = BANK_PATH_PREFIXES + GENERIC_PREFIXES
_original_validate_repo_path = base.validate_repo_path


def validate_repo_path(raw: str) -> str:
    normalized = _original_validate_repo_path(raw)
    for prefix in BANK_PATH_PREFIXES:
        if normalized.startswith(prefix):
            if PurePosixPath(normalized).name not in {f"{slot}.json" for slot in SLOT_NAMES}:
                raise ValueError(f"unexpected record-bank file: {normalized}")
            break
    return normalized


base.validate_repo_path = validate_repo_path


def read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def chat_transport_settled(repo_root: Path) -> bool:
    """Return True only when the currently committed Chat inbox has a result.

    A matching result is considered settled even when ok=false. A failed
    submission must not permanently monopolize the reusable inbox; its failure
    is already durable in Git history/result state and later work may continue.
    """
    inbox = read_object(repo_root / CHAT_INBOX)
    if inbox is None:
        return True
    job_id = inbox.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return True
    result = read_object(repo_root / CHAT_RESULT)
    return bool(result and result.get("job_id") == job_id)


def is_chat_envelope(envelope: dict[str, Any]) -> bool:
    for write in envelope["writes"]:
        path = write["path"]
        if path == CHAT_INBOX or any(path.startswith(prefix) for prefix in BANK_PATH_PREFIXES):
            return True
    return False


def validate_logical_bundle(envelope: dict[str, Any]) -> None:
    """Prevent partial/multi-bank research bundles from entering the queue."""
    record_paths = [
        write["path"]
        for write in envelope["writes"]
        if any(write["path"].startswith(prefix) for prefix in BANK_PATH_PREFIXES)
    ]
    if not record_paths:
        return

    roots: set[str] = set()
    names: set[str] = set()
    for path in record_paths:
        p = PurePosixPath(path)
        roots.add(str(p.parent))
        names.add(p.name)
    if len(roots) != 1:
        raise ValueError("one research envelope must use exactly one record bank")
    expected = {f"{slot}.json" for slot in SLOT_NAMES}
    if names != expected or len(record_paths) != len(expected):
        raise ValueError("research envelope must contain all five record slots exactly once")
    if CHAT_INBOX not in {write["path"] for write in envelope["writes"]}:
        raise ValueError("research envelope with record slots must also contain chat-inbox.json")


def apply_envelope(repo_root: Path, envelope: dict[str, Any]) -> list[str]:
    changed_paths: list[str] = []
    for write in envelope["writes"]:
        target = (repo_root / write["path"]).resolve()
        try:
            target.relative_to(repo_root)
        except ValueError as exc:
            raise ValueError(f"path escapes repository root: {write['path']}") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.exists() else None
        if old != write["content"]:
            target.write_text(write["content"], encoding="utf-8")
            changed_paths.append(write["path"])
    return changed_paths


def pull(args: argparse.Namespace) -> int:
    service = base.drive_service()
    pending_id = base.folder_id("DRIVE_PENDING_FOLDER_ID")
    failed_id = base.os.environ.get("DRIVE_FAILED_FOLDER_ID", "").strip()
    repo_root = Path(args.repo_root).resolve()
    chat_idle = chat_transport_settled(repo_root)
    manifest: dict[str, Any] = {
        "schema_version": 2,
        "accepted": [],
        "failed": [],
        "deferred_busy": [],
    }

    # Oldest-first, but accept only one logical envelope. Invalid entries are
    # quarantined and a busy research entry does not block an independent
    # framework/model-update envelope behind it.
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
            validate_logical_bundle(envelope)
            if is_chat_envelope(envelope) and not chat_idle:
                manifest["deferred_busy"].append(
                    {"drive_file_id": meta["id"], "name": name, "reason": "chat transport still processing"}
                )
                continue
            changed_paths = apply_envelope(repo_root, envelope)
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

    Path(args.manifest).write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(
        {
            "accepted": len(manifest["accepted"]),
            "failed": len(manifest["failed"]),
            "deferred_busy": len(manifest["deferred_busy"]),
            "changed_paths": sum(len(x["changed_paths"]) for x in manifest["accepted"]),
        },
        ensure_ascii=False,
    ))
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
