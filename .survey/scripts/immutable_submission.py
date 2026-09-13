#!/usr/bin/env python3
"""Immutable workflow-v10 research/audit submission helpers."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402

SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
KINDS = {"research", "audit"}
TRANSPORT_VERSION = 10


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def _read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def load_descriptor(path: Path) -> dict[str, Any]:
    value = _read_object(Path(path))
    if value is None:
        raise ValueError(f"immutable submission must contain a JSON object: {path}")
    return value


def _safe_id(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SAFE_ID_RE.fullmatch(value):
        raise ValueError(f"{label} must match [A-Za-z0-9][A-Za-z0-9._-]{{0,159}}")
    return value


def _safe_rel(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{label} must be a non-empty repository-relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} must stay within the repository")
    return path.as_posix()


def result_path_for(repo_root: Path, descriptor_path: Path) -> Path:
    repo_root = Path(repo_root).resolve()
    descriptor_path = Path(descriptor_path)
    if not descriptor_path.is_absolute():
        descriptor_path = repo_root / descriptor_path
    kind = descriptor_path.parent.name
    if kind not in KINDS:
        raise ValueError("immutable descriptor must live under submissions/research or submissions/audit")
    return repo_root / ".survey/work-queue/results" / kind / descriptor_path.name


def _result_matches(path: Path, descriptor: dict[str, Any]) -> bool:
    result = _read_object(path)
    return bool(
        result
        and result.get("attempt_id") == descriptor.get("attempt_id")
        and result.get("job_id") == descriptor.get("job_id")
    )


def pending_descriptors(repo_root: Path) -> list[dict[str, Any]]:
    repo_root = Path(repo_root).resolve()
    out: list[dict[str, Any]] = []
    for kind in sorted(KINDS):
        root = repo_root / ".survey/work-queue/submissions" / kind
        for path in sorted(root.glob("*.json")) if root.is_dir() else []:
            descriptor = _read_object(path)
            if not descriptor:
                continue
            result_path = result_path_for(repo_root, path)
            if _result_matches(result_path, descriptor):
                continue
            row = dict(descriptor)
            row["_path"] = path.relative_to(repo_root).as_posix()
            out.append(row)
    return out


def validate_descriptor(repo_root: Path, descriptor: dict[str, Any]) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    if not isinstance(descriptor, dict):
        raise ValueError("descriptor must be an object")
    if descriptor.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    if descriptor.get("transport_version") != TRANSPORT_VERSION:
        raise ValueError(f"transport_version must be {TRANSPORT_VERSION}")
    kind = descriptor.get("kind")
    if kind not in KINDS:
        raise ValueError("kind must be research or audit")
    attempt_id = _safe_id(descriptor.get("attempt_id"), "attempt_id")
    job_id = _safe_id(descriptor.get("job_id"), "job_id")
    bank = str(descriptor.get("record_bank") or "").lower()
    if bank not in BANK_ROOTS:
        raise ValueError("record_bank must be registered")
    paper_path = _safe_rel(descriptor.get("paper_path"), "paper_path")
    if not paper_path.startswith("papers/") or not paper_path.endswith(".md"):
        raise ValueError("paper_path must be a Markdown path under papers/")
    expected_blob_sha = descriptor.get("expected_blob_sha")
    if expected_blob_sha is not None and (
        not isinstance(expected_blob_sha, str)
        or not re.fullmatch(r"[0-9a-f]{40}", expected_blob_sha)
    ):
        raise ValueError("expected_blob_sha must be a 40-character lowercase Git SHA when present")

    refs = descriptor.get("record_slots")
    if not isinstance(refs, list) or len(refs) != len(SLOT_NAMES):
        raise ValueError(f"record_slots must contain exactly {len(SLOT_NAMES)} entries")
    expected_root = BANK_ROOTS[bank]
    normalized_refs: list[dict[str, str]] = []
    for index, slot in enumerate(SLOT_NAMES):
        ref = refs[index]
        if not isinstance(ref, dict) or ref.get("slot") != slot:
            raise ValueError(f"record_slots[{index}] must declare slot={slot}")
        path_text = _safe_rel(ref.get("path"), f"record_slots[{index}].path")
        expected_path = f"{expected_root}/{slot}.json"
        if path_text != expected_path:
            raise ValueError(f"slot {slot} must use fixed path {expected_path}")
        blob_sha = ref.get("blob_sha")
        if not isinstance(blob_sha, str) or not re.fullmatch(r"[0-9a-f]{40}", blob_sha):
            raise ValueError(f"slot {slot} requires a 40-character lowercase blob_sha")
        target = repo_root / path_text
        if not target.is_file():
            raise ValueError(f"missing record slot: {path_text}")
        if git_blob_sha(target.read_bytes()) != blob_sha:
            raise ValueError(f"record slot blob mismatch: {path_text}")
        payload = _read_object(target)
        if not payload:
            raise ValueError(f"record slot must contain a JSON object: {path_text}")
        if payload.get("transport_version") != TRANSPORT_VERSION:
            raise ValueError(f"{path_text} transport_version must be {TRANSPORT_VERSION}")
        if payload.get("slot") != slot:
            raise ValueError(f"{path_text} slot mismatch")
        if payload.get("attempt_id") != attempt_id or payload.get("job_id") != job_id:
            raise ValueError(f"{path_text} attempt_id/job_id mismatch")
        normalized_refs.append({"slot": slot, "path": path_text, "blob_sha": blob_sha})

    out = dict(descriptor)
    out["kind"] = kind
    out["attempt_id"] = attempt_id
    out["job_id"] = job_id
    out["record_bank"] = bank
    out["paper_path"] = paper_path
    out["record_slots"] = normalized_refs
    return out
