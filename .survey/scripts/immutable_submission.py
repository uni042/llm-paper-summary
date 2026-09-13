#!/usr/bin/env python3
"""Immutable workflow-v10 research/audit submission helpers."""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
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
COMPLETED_STATUS = "completed"
NONARTIFACT_STATUSES = {"blocked", "deferred", "rejected"}
STATUSES = {COMPLETED_STATUS, *NONARTIFACT_STATUSES}


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


def _safe_paper_path(value: Any, *, required: bool) -> str | None:
    if value is None and not required:
        return None
    paper_path = _safe_rel(value, "paper_path")
    if not paper_path.startswith("papers/") or not paper_path.endswith(".md"):
        raise ValueError("paper_path must be a Markdown path under papers/")
    return paper_path


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
        and result.get("ok") is True
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


def _git_blob_bytes(repo_root: Path, blob_sha: str) -> bytes | None:
    """Read an exact committed Git blob, independent of the current worktree path."""
    try:
        result = subprocess.run(
            ["git", "cat-file", "blob", blob_sha],
            cwd=repo_root,
            capture_output=True,
            check=False,
        )
    except OSError:
        return None
    return result.stdout if result.returncode == 0 else None


def read_record_slot_bytes(repo_root: Path, ref: dict[str, Any]) -> bytes:
    """Load the exact immutable slot bytes referenced by a descriptor.

    In production the submission workflow uses a full Git checkout, so old blobs stay
    readable even after the reusable bank path has been overwritten. The worktree
    fallback is intentionally strict and is only for isolated/pre-commit callers where
    the current file still has the declared blob SHA.
    """
    repo_root = Path(repo_root).resolve()
    path_text = _safe_rel(ref.get("path"), "record slot path")
    blob_sha = ref.get("blob_sha")
    if not isinstance(blob_sha, str) or not re.fullmatch(r"[0-9a-f]{40}", blob_sha):
        raise ValueError("record slot requires a 40-character lowercase blob_sha")

    raw = _git_blob_bytes(repo_root, blob_sha)
    if raw is not None:
        return raw

    target = repo_root / path_text
    if not target.is_file():
        raise ValueError(f"record slot blob is unavailable: {path_text} ({blob_sha})")
    raw = target.read_bytes()
    if git_blob_sha(raw) != blob_sha:
        raise ValueError(f"record slot blob is unavailable or mismatched: {path_text}")
    return raw


def read_record_slot(repo_root: Path, ref: dict[str, Any]) -> dict[str, Any]:
    """Decode one immutable record slot as a JSON object."""
    path_text = _safe_rel(ref.get("path"), "record slot path")
    raw = read_record_slot_bytes(repo_root, ref)
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"record slot blob must contain UTF-8 JSON: {path_text}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"record slot blob must contain a JSON object: {path_text}")
    return payload


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
    status = descriptor.get("status", COMPLETED_STATUS)
    if status not in STATUSES:
        raise ValueError("status must be completed, blocked, deferred, or rejected")

    out = dict(descriptor)
    out["kind"] = kind
    out["attempt_id"] = attempt_id
    out["job_id"] = job_id
    out["status"] = status

    if status in NONARTIFACT_STATUSES:
        reason = descriptor.get("reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError(f"{status} status requires a non-empty reason")
        if any(field in descriptor for field in ("record_bank", "record_slots", "expected_blob_sha")):
            raise ValueError(f"{status} is a status-only immutable descriptor; omit record transport fields")
        paper_path = _safe_paper_path(descriptor.get("paper_path"), required=False)
        if paper_path is not None:
            out["paper_path"] = paper_path
        else:
            out.pop("paper_path", None)
        out["reason"] = reason.strip()
        return out

    bank = str(descriptor.get("record_bank") or "").lower()
    if bank not in BANK_ROOTS:
        raise ValueError("record_bank must be registered")
    paper_path = _safe_paper_path(descriptor.get("paper_path"), required=True)
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
        normalized_ref = {"slot": slot, "path": path_text, "blob_sha": blob_sha}
        payload = read_record_slot(repo_root, normalized_ref)
        if payload.get("transport_version") != TRANSPORT_VERSION:
            raise ValueError(f"{path_text} transport_version must be {TRANSPORT_VERSION}")
        if payload.get("slot") != slot:
            raise ValueError(f"{path_text} slot mismatch")
        if payload.get("attempt_id") != attempt_id or payload.get("job_id") != job_id:
            raise ValueError(f"{path_text} attempt_id/job_id mismatch")
        normalized_refs.append(normalized_ref)

    out["record_bank"] = bank
    out["paper_path"] = paper_path
    out["record_slots"] = normalized_refs
    return out
