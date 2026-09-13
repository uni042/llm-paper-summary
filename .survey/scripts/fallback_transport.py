#!/usr/bin/env python3
"""Shared validation and GitHub intake helpers for survey fallback envelopes.

Google Drive and ChatGPT Library use the same immutable envelope format. Both
fallbacks recover by placing that envelope into a unique GitHub fallback inbox;
only the normal survey-helper workflow expands transport writes into reusable
record banks/inboxes. Cross-outbox recovery is serialized and duplicate envelope
IDs are globally idempotent.

Research envelopes keep their original immutable transport bundle in the intake
ledger, but dispatch may remap that bundle to a different safe record bank. This
prevents a delayed fallback replay from overwriting a newer uncheckpointed
partial attempt that happened to reuse the bank named when the envelope was
created.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from record_bank_config import BANK_PATH_PREFIXES, BANK_ROOTS, SLOT_NAMES
import claim_state

CHAT_INBOX = ".survey/work-queue/submissions/chat-inbox.json"
CHAT_RESULT = ".survey/work-queue/results/chat-inbox.json"
GENERIC_PREFIXES = (
    ".survey/work-queue/submissions/",
    ".survey/work-queue/transport/",
    ".survey/update-worker/",
)
ALLOWED_PREFIXES = BANK_PATH_PREFIXES + GENERIC_PREFIXES
MAX_ENVELOPE_BYTES = 2 * 1024 * 1024
MAX_WRITES = 16
MAX_CONTENT_BYTES = 1024 * 1024
ENVELOPE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
TERMINAL_JOB_STATES = claim_state.TERMINAL

FALLBACK_INBOX = Path(".survey/work-queue/fallback-inbox")
FALLBACK_ARCHIVE = Path(".survey/work-queue/fallback-archive")
FALLBACK_FAILED = Path(".survey/work-queue/fallback-failed")


def read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def validate_repo_path(raw: Any) -> str:
    if not isinstance(raw, str) or not raw:
        raise ValueError("write.path must be a non-empty string")
    p = PurePosixPath(raw)
    if p.is_absolute() or ".." in p.parts or "\\" in raw:
        raise ValueError(f"unsafe repository path: {raw!r}")
    normalized = str(p)
    if not normalized.endswith(".json"):
        raise ValueError(f"only JSON transport files are allowed: {normalized}")
    if not any(normalized.startswith(prefix) for prefix in ALLOWED_PREFIXES):
        raise ValueError(f"path is outside fallback allowlist: {normalized}")
    for prefix in BANK_PATH_PREFIXES:
        if normalized.startswith(prefix):
            if PurePosixPath(normalized).name not in {f"{slot}.json" for slot in SLOT_NAMES}:
                raise ValueError(f"unexpected record-bank file: {normalized}")
            break
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
    validate_logical_bundle(out)
    _validate_claimed_metadata(out)
    return out


def _validate_claimed_metadata(envelope: dict[str, Any]) -> None:
    if envelope.get("origin") != "claimed_worker":
        return
    for key in ("job_id", "claim_id", "worker_id", "attempt_id"):
        value = envelope.get(key)
        if not isinstance(value, str) or not ENVELOPE_ID_RE.fullmatch(value):
            raise ValueError(f"claimed envelope requires safe {key}")
    payload = chat_payload(envelope)
    if payload is None:
        raise ValueError("claimed envelope requires a chat-inbox payload")
    record_writes = [
        write for write in envelope["writes"]
        if any(write["path"].startswith(prefix) for prefix in BANK_PATH_PREFIXES)
    ]
    expected_names = {f"{slot}.json" for slot in SLOT_NAMES}
    if len(record_writes) != len(SLOT_NAMES) or {PurePosixPath(write["path"]).name for write in record_writes} != expected_names:
        raise ValueError("claimed envelope requires all five record slots")
    roots = {str(PurePosixPath(write["path"]).parent) for write in record_writes}
    if len(roots) != 1:
        raise ValueError("claimed envelope record slots must use one bank")
    for write in record_writes:
        slot = json.loads(write["content"])
        expected_slot = PurePosixPath(write["path"]).stem
        if (
            slot.get("slot") != expected_slot
            or slot.get("job_id") != envelope["job_id"]
            or slot.get("attempt_id") != envelope["attempt_id"]
            or slot.get("transport_version") != 10
        ):
            raise ValueError(f"claimed envelope slot identity mismatch: {expected_slot}")
    kind = envelope.get("kind")
    dependencies = envelope.get("depends_on_job_ids")
    if kind not in {"research", "audit"}:
        raise ValueError("claimed envelope kind must be research or audit")
    if not isinstance(dependencies, list) or envelope["job_id"] not in dependencies or any(
        not isinstance(value, str) or not ENVELOPE_ID_RE.fullmatch(value) for value in dependencies
    ):
        raise ValueError("claimed envelope depends_on_job_ids must include job_id")
    for key in ("job_id", "claim_id", "worker_id", "attempt_id"):
        if payload.get(key) != envelope[key]:
            raise ValueError(f"claimed envelope {key} does not match chat payload")
    if payload.get("kind") != kind or payload.get("depends_on_job_ids") != dependencies:
        raise ValueError("claimed envelope kind/dependencies do not match chat payload")


def claimed_envelope_state(repo_root: Path, envelope: dict[str, Any]) -> tuple[bool, str | None]:
    """Fence claimed completion against the immutable current claim.

    An expired claim remains valid until a newer assignment replaces the current
    claim file; a missing or superseded claim is never allowed to reach transport.
    """
    if envelope.get("origin") != "claimed_worker":
        return True, None
    _validate_claimed_metadata(envelope)
    job_id = envelope["job_id"]
    job_path = repo_root / ".survey/work-queue/jobs" / f"{job_id}.json"
    job = read_object(job_path)
    if job is None or job.get("job_id") != job_id or job_path.stem != job_id:
        return False, "canonical job identity is missing or unsafe"
    if job.get("type") != envelope.get("kind"):
        return False, "claimed envelope kind differs from canonical job type"
    canonical_dependencies = job.get("depends_on_job_ids") or job.get("dependencies")
    if isinstance(canonical_dependencies, list) and any(
        dependency not in envelope["depends_on_job_ids"] for dependency in canonical_dependencies
    ):
        return False, "claimed envelope dependencies differ from canonical job"
    current = claim_state.current_claims(repo_root).get(job_id)
    if current is None:
        return False, "missing current claim"
    for key in ("claim_id", "worker_id", "attempt_id"):
        if current.get(key) != envelope[key]:
            return False, f"superseded claim: current {key} differs"
    return True, None


def validate_logical_bundle(envelope: dict[str, Any]) -> None:
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
    """Place an envelope in the immutable GitHub fallback inbox idempotently."""
    repo_root = repo_root.resolve()
    envelope_id = envelope["id"]
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


def chat_payload(envelope: dict[str, Any]) -> dict[str, Any] | None:
    for write in envelope["writes"]:
        if write["path"] == CHAT_INBOX:
            try:
                value = json.loads(write["content"])
            except json.JSONDecodeError:
                return None
            return value if isinstance(value, dict) else None
    return None


def has_record_slots(envelope: dict[str, Any]) -> bool:
    return any(
        write["path"].startswith(prefix)
        for write in envelope["writes"]
        for prefix in BANK_PATH_PREFIXES
    )


def is_chat_envelope(envelope: dict[str, Any]) -> bool:
    return bool(has_record_slots(envelope) or any(w["path"] == CHAT_INBOX for w in envelope["writes"]))


def chat_transport_settled(repo_root: Path) -> bool:
    inbox = read_object(repo_root / CHAT_INBOX)
    if inbox is None:
        return True
    job_id = inbox.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return True
    result = read_object(repo_root / CHAT_RESULT)
    return bool(result and result.get("job_id") == job_id)


def dependency_state(repo_root: Path, envelope: dict[str, Any]) -> tuple[bool, str | None]:
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


def terminal_job_id(repo_root: Path, envelope: dict[str, Any]) -> str | None:
    payload = chat_payload(envelope)
    if payload is None:
        return None
    job_id = payload.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return None
    job = read_object(repo_root / ".survey" / "work-queue" / "jobs" / f"{job_id}.json")
    if job and job.get("status") in TERMINAL_JOB_STATES:
        return job_id
    return None


def _git_blob_sha(text: str) -> str:
    raw = text.encode("utf-8")
    header = f"blob {len(raw)}\0".encode("utf-8")
    return hashlib.sha1(header + raw).hexdigest()


def _record_identity(envelope: dict[str, Any]) -> tuple[str, str] | None:
    payload = chat_payload(envelope)
    if payload is None:
        return None
    job_id = payload.get("job_id")
    attempt_id = payload.get("attempt_id")
    if not isinstance(job_id, str) or not job_id or not isinstance(attempt_id, str) or not attempt_id:
        return None
    return job_id, attempt_id


def _checkpointed_intake_job_ids(repo_root: Path) -> set[str]:
    """Jobs whose complete fallback bundle is already durable in GitHub."""
    out: set[str] = set()
    for rel in (FALLBACK_INBOX, FALLBACK_ARCHIVE):
        root = repo_root / rel
        if not root.is_dir():
            continue
        for path in root.glob("*.json"):
            try:
                envelope, _text = parse_envelope(path.read_bytes())
            except Exception:
                continue
            if not has_record_slots(envelope):
                continue
            payload = chat_payload(envelope)
            job_id = payload.get("job_id") if payload else None
            if isinstance(job_id, str) and job_id:
                out.add(job_id)
    return out


def _choose_dispatch_bank(repo_root: Path, envelope: dict[str, Any]) -> tuple[str | None, str | None]:
    """Choose a bank without overwriting an uncheckpointed partial attempt."""
    identity = _record_identity(envelope)
    if identity is None:
        return None, "record bundle has no coherent job/attempt identity"
    job_id, attempt_id = identity

    # Import lazily to keep the common validation module lightweight.
    from select_record_bank import inspect  # noqa: WPS433

    state = inspect(repo_root)
    banks = state.get("banks") or []

    # Reusing a bank that already belongs coherently to the exact same attempt
    # is always safe; completing that attempt cannot destroy another job's data.
    for bank in banks:
        slots = bank.get("slots") or []
        if not slots:
            continue
        jobs = {slot.get("job_id") for slot in slots if slot.get("job_id")}
        attempts = {slot.get("attempt_id") for slot in slots if slot.get("attempt_id")}
        if jobs == {job_id} and attempts == {attempt_id}:
            return str(bank.get("bank")), "same_attempt"

    for bank in banks:
        if bank.get("state") in {"free", "reusable"}:
            return str(bank.get("bank")), str(bank.get("state"))

    # An occupied ready job may still be safely reclaimable if its complete
    # logical payload is already in the immutable GitHub fallback ledger. The
    # bank is then only a staging copy, not the unique durable result.
    checkpointed = _checkpointed_intake_job_ids(repo_root)
    if not chat_transport_settled(repo_root):
        return None, "reusable Chat transport is still busy"
    for bank in banks:
        if bank.get("state") != "occupied":
            continue
        slots = bank.get("slots") or []
        jobs = {slot.get("job_id") for slot in slots if slot.get("job_id")}
        if len(jobs) == 1 and next(iter(jobs)) in checkpointed:
            return str(bank.get("bank")), "occupied_but_durably_checkpointed"

    return None, "no safe record bank available yet"


def remap_research_bank(repo_root: Path, envelope: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    """Return a transient dispatch copy mapped to a currently safe record bank.

    The immutable intake/archive envelope is not modified. Only the working-tree
    writes used for this dispatch are rewritten, including chat-inbox paths and
    blob SHAs.
    """
    if not has_record_slots(envelope):
        return envelope, None

    bank, reason = _choose_dispatch_bank(repo_root, envelope)
    if bank is None:
        return None, reason
    if bank not in BANK_ROOTS:
        return None, f"selected unknown record bank: {bank}"

    slot_content: dict[str, str] = {}
    for write in envelope["writes"]:
        if not any(write["path"].startswith(prefix) for prefix in BANK_PATH_PREFIXES):
            continue
        payload = json.loads(write["content"])
        slot = payload.get("slot")
        if slot in SLOT_NAMES:
            slot_content[str(slot)] = write["content"]
    if set(slot_content) != set(SLOT_NAMES):
        raise ValueError("research envelope does not expose all five slot payloads")

    inbox = chat_payload(envelope)
    if inbox is None:
        raise ValueError("research envelope has no chat-inbox payload")
    inbox = dict(inbox)
    root = BANK_ROOTS[bank]
    refs: list[dict[str, str]] = []
    for slot in SLOT_NAMES:
        path = f"{root}/{slot}.json"
        refs.append({"slot": slot, "path": path, "blob_sha": _git_blob_sha(slot_content[slot])})
    inbox["record_bank"] = bank
    inbox["record_slots"] = refs
    inbox_text = json.dumps(inbox, ensure_ascii=False, indent=2) + "\n"

    remapped_writes: list[dict[str, str]] = []
    for slot in SLOT_NAMES:
        remapped_writes.append({"path": f"{root}/{slot}.json", "content": slot_content[slot]})
    for write in envelope["writes"]:
        if any(write["path"].startswith(prefix) for prefix in BANK_PATH_PREFIXES):
            continue
        if write["path"] == CHAT_INBOX:
            remapped_writes.append({"path": CHAT_INBOX, "content": inbox_text})
        else:
            remapped_writes.append(dict(write))

    out = dict(envelope)
    out["writes"] = remapped_writes
    return out, f"bank={bank}; reason={reason}"


def apply_envelope(repo_root: Path, envelope: dict[str, Any]) -> list[str]:
    changed: list[str] = []
    for write in envelope["writes"]:
        target = (repo_root / write["path"]).resolve()
        try:
            target.relative_to(repo_root.resolve())
        except ValueError as exc:
            raise ValueError(f"path escapes repository root: {write['path']}") from exc
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.exists() else None
        if old != write["content"]:
            target.write_text(write["content"], encoding="utf-8")
            changed.append(write["path"])
    return changed
