#!/usr/bin/env python3
"""Import ChatGPT survey fallback envelopes from Google Drive.

The Drive folder is treated as an outbox, not as a repository mirror.
Each JSON envelope contains one or more writes to a small allowlist of
transport paths. This preserves the existing GitHub Actions pipeline:
Chat writes transport JSON -> Actions renders/validates -> repository changes.

Commands:
  pull     Download and apply pending envelopes to the working tree.
  ack      Move successfully pushed envelopes to the processed folder.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
from typing import Any

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

SCOPES = ["https://www.googleapis.com/auth/drive"]
ALLOWED_PREFIXES = (
    ".survey/work-queue/records/chat-record/",
    ".survey/work-queue/records/chat-record-b/",
    ".survey/work-queue/submissions/",
    ".survey/work-queue/transport/",
    ".survey/update-worker/",
)
MAX_ENVELOPE_BYTES = 2 * 1024 * 1024
MAX_WRITES = 16
MAX_CONTENT_BYTES = 1024 * 1024


def load_credentials():
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw:
        raise SystemExit("GOOGLE_SERVICE_ACCOUNT_JSON is required")
    info = json.loads(raw)
    return service_account.Credentials.from_service_account_info(info, scopes=SCOPES)


def drive_service():
    return build("drive", "v3", credentials=load_credentials(), cache_discovery=False)


def folder_id(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(f"{name} is required")
    return value


def list_pending(service, pending_id: str) -> list[dict[str, Any]]:
    files: list[dict[str, Any]] = []
    token = None
    while True:
        response = service.files().list(
            q=f"'{pending_id}' in parents and trashed = false",
            fields="nextPageToken,files(id,name,mimeType,size,modifiedTime,parents)",
            orderBy="createdTime,name",
            pageSize=100,
            pageToken=token,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
        ).execute()
        files.extend(response.get("files", []))
        token = response.get("nextPageToken")
        if not token:
            return files


def download_bytes(service, file_id: str) -> bytes:
    request = service.files().get_media(fileId=file_id, supportsAllDrives=True)
    buf = io.BytesIO()
    downloader = MediaIoBaseDownload(buf, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
        if buf.tell() > MAX_ENVELOPE_BYTES:
            raise ValueError(f"envelope exceeds {MAX_ENVELOPE_BYTES} bytes")
    return buf.getvalue()


def validate_repo_path(raw: str) -> str:
    if not isinstance(raw, str) or not raw:
        raise ValueError("write.path must be a non-empty string")
    p = PurePosixPath(raw)
    if p.is_absolute() or ".." in p.parts or "\\" in raw:
        raise ValueError(f"unsafe repository path: {raw!r}")
    normalized = str(p)
    if not normalized.endswith(".json"):
        raise ValueError(f"only JSON transport files are allowed: {normalized}")
    if not any(normalized.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise ValueError(f"path is outside Drive outbox allowlist: {normalized}")
    return normalized


def validate_envelope(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("envelope root must be an object")
    if data.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    envelope_id = data.get("id")
    if not isinstance(envelope_id, str) or not envelope_id.strip():
        raise ValueError("id must be a non-empty string")
    writes = data.get("writes")
    if not isinstance(writes, list) or not writes:
        raise ValueError("writes must be a non-empty array")
    if len(writes) > MAX_WRITES:
        raise ValueError(f"too many writes; max={MAX_WRITES}")

    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in writes:
        if not isinstance(item, dict):
            raise ValueError("each writes item must be an object")
        path = validate_repo_path(item.get("path"))
        if path in seen:
            raise ValueError(f"duplicate write path in one envelope: {path}")
        seen.add(path)
        content = item.get("content")
        if not isinstance(content, str):
            raise ValueError(f"content for {path} must be a string")
        encoded = content.encode("utf-8")
        if len(encoded) > MAX_CONTENT_BYTES:
            raise ValueError(f"content too large for {path}")
        json.loads(content)
        normalized.append({"path": path, "content": content})

    return {"schema_version": 1, "id": envelope_id.strip(), "writes": normalized}


def move_file(service, file_meta: dict[str, Any], destination_id: str) -> None:
    parents = ",".join(file_meta.get("parents", []))
    kwargs = {
        "fileId": file_meta["id"],
        "addParents": destination_id,
        "fields": "id,parents",
        "supportsAllDrives": True,
    }
    if parents:
        kwargs["removeParents"] = parents
    service.files().update(**kwargs).execute()


def pull(args: argparse.Namespace) -> int:
    service = drive_service()
    pending_id = folder_id("DRIVE_PENDING_FOLDER_ID")
    failed_id = os.environ.get("DRIVE_FAILED_FOLDER_ID", "").strip()
    repo_root = Path(args.repo_root).resolve()
    manifest: dict[str, Any] = {"schema_version": 1, "accepted": [], "failed": []}

    for meta in list_pending(service, pending_id):
        name = meta.get("name", meta["id"])
        if not str(name).lower().endswith(".json"):
            message = "skipped: pending outbox accepts .json envelopes only"
            manifest["failed"].append({"drive_file_id": meta["id"], "name": name, "error": message})
            if failed_id:
                move_file(service, meta, failed_id)
            continue
        try:
            raw = download_bytes(service, meta["id"])
            data = json.loads(raw.decode("utf-8"))
            envelope = validate_envelope(data)
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
        except Exception as exc:
            message = f"{type(exc).__name__}: {exc}"
            manifest["failed"].append({"drive_file_id": meta["id"], "name": name, "error": message})
            if failed_id:
                move_file(service, meta, failed_id)

    Path(args.manifest).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(
        {
            "accepted": len(manifest["accepted"]),
            "failed": len(manifest["failed"]),
            "changed_paths": sum(len(x["changed_paths"]) for x in manifest["accepted"]),
        },
        ensure_ascii=False,
    ))
    return 0


def ack(args: argparse.Namespace) -> int:
    processed_id = folder_id("DRIVE_PROCESSED_FOLDER_ID")
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    service = drive_service()
    moved = 0
    for item in manifest.get("accepted", []):
        file_id = item["drive_file_id"]
        meta = service.files().get(
            fileId=file_id,
            fields="id,parents",
            supportsAllDrives=True,
        ).execute()
        move_file(service, meta, processed_id)
        moved += 1
    print(json.dumps({"acknowledged": moved}))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("pull", "ack"))
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--manifest", default=".drive-outbox-manifest.json")
    args = parser.parse_args()
    return pull(args) if args.command == "pull" else ack(args)


if __name__ == "__main__":
    raise SystemExit(main())
