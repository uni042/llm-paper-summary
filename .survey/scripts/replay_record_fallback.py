#!/usr/bin/env python3
"""Convert durable research/audit fallback bundles to workflow-v10 immutable submissions.

This module is the compatibility boundary for historical Library envelopes that
contained five record slots plus the retired reusable ``chat-inbox.json`` payload.
New fallback envelopes may omit ``chat-inbox.json`` and carry paper/claim metadata at
the envelope root. In either case replay writes only a safe record bank and an
attempt-specific immutable descriptor; it never recreates the reusable Chat transport.
"""
from __future__ import annotations

import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

import claim_state
import immutable_submission
import select_record_bank
from record_bank_config import BANK_PATH_PREFIXES, BANK_ROOTS, SLOT_NAMES

CHAT_INBOX = ".survey/work-queue/submissions/chat-inbox.json"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
TERMINAL = claim_state.TERMINAL


def read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def is_record_bundle(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    writes = value.get("writes")
    if not isinstance(writes, list):
        return False
    return any(
        isinstance(write, dict)
        and isinstance(write.get("path"), str)
        and any(write["path"].startswith(prefix) for prefix in BANK_PATH_PREFIXES)
        for write in writes
    )


def _safe_id(value: Any, label: str, *, required: bool = True) -> str | None:
    if value is None and not required:
        return None
    if not isinstance(value, str) or not SAFE_ID_RE.fullmatch(value):
        raise ValueError(f"{label} must match [A-Za-z0-9][A-Za-z0-9._-]{{0,159}}")
    return value


def _safe_paper_path(value: Any) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("paper_path must be a non-empty string")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not value.startswith("papers/") or not value.endswith(".md"):
        raise ValueError("paper_path must be a Markdown path under papers/")
    return path.as_posix()


def _legacy_chat_payload(envelope: dict[str, Any]) -> dict[str, Any] | None:
    for write in envelope.get("writes") or []:
        if not isinstance(write, dict) or write.get("path") != CHAT_INBOX:
            continue
        content = write.get("content")
        if not isinstance(content, str):
            raise ValueError("legacy chat-inbox content must be a JSON string")
        value = json.loads(content)
        if not isinstance(value, dict):
            raise ValueError("legacy chat-inbox content must contain an object")
        return value
    return None


def _metadata(envelope: dict[str, Any]) -> dict[str, Any]:
    legacy = _legacy_chat_payload(envelope) or {}
    out: dict[str, Any] = {}
    for key in (
        "kind",
        "job_id",
        "claim_id",
        "worker_id",
        "worker_kind",
        "attempt_id",
        "depends_on_job_ids",
        "paper_path",
        "expected_blob_sha",
        "audit_required",
        "audit_flags",
        "audit_reason",
    ):
        root_value = envelope.get(key)
        legacy_value = legacy.get(key)
        if root_value is not None and legacy_value is not None and root_value != legacy_value:
            raise ValueError(f"legacy chat-inbox {key} differs from fallback envelope")
        value = root_value if root_value is not None else legacy_value
        if value is not None:
            out[key] = value
    return out


def _slot_payloads(envelope: dict[str, Any], job_id: str, attempt_id: str) -> dict[str, str]:
    slots: dict[str, str] = {}
    roots: set[str] = set()
    for write in envelope.get("writes") or []:
        if not isinstance(write, dict):
            continue
        path_text = write.get("path")
        if not isinstance(path_text, str) or not any(path_text.startswith(prefix) for prefix in BANK_PATH_PREFIXES):
            continue
        path = PurePosixPath(path_text)
        slot = path.stem
        if slot not in SLOT_NAMES or path.name != f"{slot}.json":
            raise ValueError(f"unexpected record slot path: {path_text}")
        content = write.get("content")
        if not isinstance(content, str):
            raise ValueError(f"record slot content must be a JSON string: {path_text}")
        payload = json.loads(content)
        if not isinstance(payload, dict):
            raise ValueError(f"record slot must contain an object: {path_text}")
        if payload.get("transport_version") != 10:
            raise ValueError(f"record slot transport_version must be 10: {slot}")
        if payload.get("slot") != slot:
            raise ValueError(f"record slot identity mismatch: {slot}")
        if payload.get("job_id") != job_id or payload.get("attempt_id") != attempt_id:
            raise ValueError(f"record slot job/attempt mismatch: {slot}")
        if slot in slots:
            raise ValueError(f"duplicate record slot: {slot}")
        slots[slot] = content
        roots.add(str(path.parent))
    if set(slots) != set(SLOT_NAMES) or len(slots) != len(SLOT_NAMES):
        raise ValueError("research/audit fallback requires all five record slots exactly once")
    if len(roots) != 1:
        raise ValueError("research/audit fallback record slots must originate from one bank")
    return slots


def _canonical_dependencies(job_id: str, value: Any) -> list[str]:
    normalized = claim_state.normalize_dependencies(job_id, value)
    if normalized is None:
        raise ValueError("depends_on_job_ids are invalid")
    return normalized


def _validate_job_and_claim(repo_root: Path, envelope: dict[str, Any], meta: dict[str, Any]) -> tuple[dict[str, Any], str | None]:
    kind = meta.get("kind")
    if kind not in {"research", "audit"}:
        raise ValueError("record fallback kind must be research or audit")
    job_id = _safe_id(meta.get("job_id"), "job_id")
    attempt_id = _safe_id(meta.get("attempt_id"), "attempt_id")
    assert job_id is not None and attempt_id is not None
    job_path = repo_root / ".survey/work-queue/jobs" / f"{job_id}.json"
    job = read_object(job_path)
    if job is None or job.get("job_id") != job_id:
        raise ValueError(f"canonical job is missing or invalid: {job_id}")
    if job.get("status") in TERMINAL:
        return job, str(job.get("status"))
    if job.get("type") != kind:
        raise ValueError("fallback kind differs from canonical job type")

    raw_dependencies = job["depends_on_job_ids"] if "depends_on_job_ids" in job else job.get("dependencies")
    canonical = _canonical_dependencies(job_id, raw_dependencies)
    submitted = _canonical_dependencies(job_id, meta.get("depends_on_job_ids"))
    if canonical != submitted:
        raise ValueError("fallback dependencies differ from canonical job")

    paper_path = _safe_paper_path(meta.get("paper_path") or job.get("paper_path"))
    canonical_paper = job.get("paper_path")
    if canonical_paper is not None and paper_path != canonical_paper:
        raise ValueError("fallback paper_path differs from canonical job")
    meta["paper_path"] = paper_path

    if envelope.get("origin") == "claimed_worker":
        claim_id = _safe_id(meta.get("claim_id"), "claim_id")
        worker_id = _safe_id(meta.get("worker_id"), "worker_id")
        current = claim_state.current_claims(repo_root).get(job_id)
        if current is None:
            raise ValueError("missing current claim")
        for key, expected in (("claim_id", claim_id), ("worker_id", worker_id), ("attempt_id", attempt_id)):
            if current.get(key) != expected:
                raise ValueError(f"superseded claim: current {key} differs")
    return job, None


def _choose_bank(repo_root: Path, job_id: str, attempt_id: str) -> str | None:
    state = select_record_bank.inspect(repo_root)
    for bank in state.get("banks") or []:
        slots = bank.get("slots") or []
        jobs = {slot.get("job_id") for slot in slots if slot.get("job_id")}
        attempts = {slot.get("attempt_id") for slot in slots if slot.get("attempt_id")}
        if jobs == {job_id} and attempts == {attempt_id}:
            return str(bank.get("bank"))
    for bank in state.get("banks") or []:
        if bank.get("state") in {"free", "reusable"}:
            return str(bank.get("bank"))
    return None


def _write_if_changed(path: Path, text: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def materialize(repo_root: Path, envelope: dict[str, Any]) -> dict[str, Any]:
    """Materialize one record fallback as slots plus an immutable descriptor."""
    repo_root = Path(repo_root).resolve()
    if envelope.get("schema_version") != 1:
        raise ValueError("schema_version must be 1")
    _safe_id(envelope.get("id"), "id")
    if not is_record_bundle(envelope):
        raise ValueError("fallback is not a research/audit record bundle")

    meta = _metadata(envelope)
    kind = meta.get("kind")
    if kind not in {"research", "audit"}:
        raise ValueError("record fallback kind must be research or audit")
    job_id_value = _safe_id(meta.get("job_id"), "job_id")
    attempt_id_value = _safe_id(meta.get("attempt_id"), "attempt_id")
    assert job_id_value is not None and attempt_id_value is not None
    job_id = job_id_value
    attempt_id = attempt_id_value

    # Validate the complete durable payload before deciding that a missing canonical
    # job is merely a dependency wait. This prevents malformed fallback from living
    # forever in the pending inbox while still allowing offline-seed research to wait
    # safely for its deterministic job to materialize.
    slots = _slot_payloads(envelope, job_id, attempt_id)
    job_path = repo_root / ".survey/work-queue/jobs" / f"{job_id}.json"
    job_probe = read_object(job_path)
    if job_probe is None:
        return {
            "action": "deferred",
            "job_id": job_id,
            "reason": f"canonical GitHub job not materialized yet: {job_id}",
            "changed_paths": [],
        }
    if job_probe.get("job_id") != job_id:
        raise ValueError(f"canonical job identity is invalid: {job_id}")

    _job, terminal_status = _validate_job_and_claim(repo_root, envelope, meta)
    if terminal_status is not None:
        return {
            "action": "ack_terminal",
            "job_id": job_id,
            "job_status": terminal_status,
            "changed_paths": [],
        }

    bank = _choose_bank(repo_root, job_id, attempt_id)
    if bank is None:
        return {
            "action": "deferred",
            "job_id": job_id,
            "reason": "no safe record bank available yet",
            "changed_paths": [],
        }

    changed: list[str] = []
    refs: list[dict[str, str]] = []
    bank_root = BANK_ROOTS[bank]
    for slot in SLOT_NAMES:
        text = slots[slot]
        path_text = f"{bank_root}/{slot}.json"
        if _write_if_changed(repo_root / path_text, text):
            changed.append(path_text)
        refs.append(
            {
                "slot": slot,
                "path": path_text,
                "blob_sha": immutable_submission.git_blob_sha(text.encode("utf-8")),
            }
        )

    descriptor: dict[str, Any] = {
        "schema_version": 1,
        "transport_version": 10,
        "kind": meta["kind"],
        "attempt_id": attempt_id,
        "job_id": job_id,
        "record_bank": bank,
        "paper_path": meta["paper_path"],
        "record_slots": refs,
    }
    for key in ("claim_id", "worker_id", "worker_kind", "expected_blob_sha", "audit_required", "audit_flags", "audit_reason"):
        if meta.get(key) is not None:
            descriptor[key] = meta[key]

    descriptor_text = json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n"
    descriptor_path = f".survey/work-queue/submissions/{meta['kind']}/{attempt_id}.json"
    target = repo_root / descriptor_path
    if target.exists() and target.read_text(encoding="utf-8") != descriptor_text:
        raise ValueError(f"immutable descriptor conflict: {descriptor_path}")
    if _write_if_changed(target, descriptor_text):
        changed.append(descriptor_path)

    return {
        "action": "materialized",
        "job_id": job_id,
        "record_bank": bank,
        "descriptor": descriptor_path,
        "changed_paths": changed,
    }
