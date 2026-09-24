#!/usr/bin/env python3
"""Validation and intake helpers for non-record survey fallback envelopes.

Research/Audit record bundles are owned by ``replay_record_fallback.py`` and never
flow through this generic writer. This module only handles allowlisted lightweight
JSON transport such as discovery/control submissions, offline seeds, and update
worker inputs. The external durable fallback is ChatGPT Library; GitHub fallback
inbox/archive files provide the immutable replay ledger.
"""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

GENERIC_PREFIXES = (
    ".survey/work-queue/submissions/",
    ".survey/work-queue/transport/",
    ".survey/update-worker/",
)
MAX_ENVELOPE_BYTES = 2 * 1024 * 1024
MAX_WRITES = 16
MAX_CONTENT_BYTES = 1024 * 1024
ENVELOPE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")

FALLBACK_INBOX = Path(".survey/work-queue/fallback-inbox")
FALLBACK_ARCHIVE = Path(".survey/work-queue/fallback-archive")
FALLBACK_FAILED = Path(".survey/work-queue/fallback-failed")


def validate_repo_path(raw: Any) -> str:
    if not isinstance(raw, str) or not raw:
        raise ValueError("write.path must be a non-empty string")
    path = PurePosixPath(raw)
    if path.is_absolute() or ".." in path.parts or "\\" in raw:
        raise ValueError(f"unsafe repository path: {raw!r}")
    normalized = str(path)
    if not normalized.endswith(".json"):
        raise ValueError(f"only JSON transport files are allowed: {normalized}")
    if not any(normalized.startswith(prefix) for prefix in GENERIC_PREFIXES):
        raise ValueError(f"path is outside generic fallback allowlist: {normalized}")
    return normalized


def validate_envelope(data: Any) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ValueError("envelope root must be an object")
    if data.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    envelope_id = data.get("id")
    if not isinstance(envelope_id, str) or not ENVELOPE_ID_RE.fullmatch(envelope_id):
        raise ValueError("id must match [A-Za-z0-9][A-Za-z0-9._-]{0,159}")
    writes = data.get("writes")
    if not isinstance(writes, list) or not writes:
        raise ValueError("writes must be a non-empty array")
    if len(writes) > MAX_WRITES:
        raise ValueError(f"too many writes; max={MAX_WRITES}")

    normalized_writes: list[dict[str, str]] = []
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
        if len(content.encode("utf-8")) > MAX_CONTENT_BYTES:
            raise ValueError(f"content too large for {path}")
        json.loads(content)
        normalized_writes.append({"path": path, "content": content})

    out = dict(data)
    out["id"] = envelope_id
    out["writes"] = normalized_writes
    return out


def canonical_text(envelope: dict[str, Any]) -> str:
    return json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def parse_envelope(raw: bytes | str) -> tuple[dict[str, Any], str]:
    if isinstance(raw, bytes):
        if len(raw) > MAX_ENVELOPE_BYTES:
            raise ValueError(f"envelope exceeds {MAX_ENVELOPE_BYTES} bytes")
        text = raw.decode("utf-8")
    else:
        text = raw
        if len(text.encode("utf-8")) > MAX_ENVELOPE_BYTES:
            raise ValueError(f"envelope exceeds {MAX_ENVELOPE_BYTES} bytes")
    envelope = validate_envelope(json.loads(text))
    return envelope, canonical_text(envelope)


def envelope_path(base: Path, envelope_id: str) -> Path:
    if not ENVELOPE_ID_RE.fullmatch(envelope_id):
        raise ValueError("invalid envelope id")
    return base / f"{envelope_id}.json"


def _canonical_existing(path: Path) -> str | None:
    try:
        _envelope, text = parse_envelope(path.read_bytes())
    except Exception:
        return None
    return text


def intake(repo_root: Path, envelope: dict[str, Any], text: str) -> dict[str, Any]:
    """Place one validated generic envelope in the GitHub fallback inbox idempotently."""
    repo_root = repo_root.resolve()
    validated = validate_envelope(envelope)
    canonical = canonical_text(validated)
    if canonical != text:
        text = canonical
    envelope_id = validated["id"]
    inbox = envelope_path(repo_root / FALLBACK_INBOX, envelope_id)
    archive = envelope_path(repo_root / FALLBACK_ARCHIVE, envelope_id)
    failed = envelope_path(repo_root / FALLBACK_FAILED, envelope_id)

    for path, state in ((archive, "already_archived"), (inbox, "already_pending")):
        if not path.exists():
            continue
        existing = _canonical_existing(path)
        if existing == text:
            return {"status": state, "path": str(path.relative_to(repo_root))}
        raise ValueError(f"envelope id conflict with {state}: {envelope_id}")

    if failed.exists():
        raise ValueError(f"envelope id was previously quarantined: {envelope_id}")

    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text(text, encoding="utf-8")
    return {"status": "created", "path": str(inbox.relative_to(repo_root))}


def apply_envelope(repo_root: Path, envelope: dict[str, Any]) -> list[str]:
    """Apply a validated generic envelope without allowing paths outside the repo."""
    envelope = validate_envelope(envelope)
    repo_root = repo_root.resolve()
    changed: list[str] = []
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
            changed.append(write["path"])
    return changed
