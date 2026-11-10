#!/usr/bin/env python3
"""Maintain durable relevance ledgers for structured-reference Discovery candidates."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import tempfile
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import citation_graph

DEFAULT_UNRELATED_LEDGER = Path(".survey/work-queue/reference-curation/unrelated-papers.json")
DEFAULT_BORDERLINE_LEDGER = Path(".survey/work-queue/reference-curation/borderline-papers.json")
DEFAULT_LEDGER = DEFAULT_UNRELATED_LEDGER
CLEAR_JOURNAL_DIR = Path(".survey/work-queue/reference-curation/clear-transactions")
_MUTATION_MUTEX = threading.RLock()
_MUTATION_STATE = threading.local()


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _mutation_lock_path(ledger_paths: tuple[Path, ...]) -> Path:
    parent_paths = [str(path.resolve().parent) for path in ledger_paths]
    try:
        common_parent = Path(os.path.commonpath(parent_paths))
    except ValueError as exc:
        raise ValueError("relevance ledgers must share a filesystem root for locking") from exc
    return common_parent / ".reference-relevance.lock"


def _reference_curation_root(path: Path) -> Path | None:
    resolved = path.resolve()
    for parent in (resolved.parent, *resolved.parents):
        if (
            parent.name == "reference-curation"
            and parent.parent.name == "work-queue"
            and parent.parent.parent.name == ".survey"
        ):
            return parent.parent.parent.parent
    return None


@contextmanager
def ledger_mutation_lock(*ledger_paths: Path):
    """Serialize every ledger mutation across threads and processes.

    Nested calls on the owning thread are reentrant and must resolve to the same
    lock path. The OS lock is released automatically if a process exits.
    """
    if not ledger_paths:
        raise ValueError("at least one ledger path is required for locking")
    lock_path = _mutation_lock_path(tuple(ledger_paths))
    with _MUTATION_MUTEX:
        depth = getattr(_MUTATION_STATE, "depth", 0)
        if depth:
            if _MUTATION_STATE.path != lock_path:
                raise RuntimeError("nested relevance mutations must use the same shared lock")
            _MUTATION_STATE.depth = depth + 1
            try:
                yield
            finally:
                _MUTATION_STATE.depth -= 1
            return

        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a+b") as lock_file:
            lock_file.seek(0, os.SEEK_END)
            if lock_file.tell() == 0:
                lock_file.write(b"\0")
                lock_file.flush()
                os.fsync(lock_file.fileno())
            lock_file.seek(0)
            if os.name == "nt":
                import msvcrt

                while True:
                    try:
                        msvcrt.locking(lock_file.fileno(), msvcrt.LK_NBLCK, 1)
                        break
                    except OSError:
                        time.sleep(0.05)
            else:
                import fcntl

                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
            _MUTATION_STATE.depth = 1
            _MUTATION_STATE.path = lock_path
            try:
                root = _reference_curation_root(ledger_paths[0])
                if root is not None:
                    _recover_pending_clear_transactions(root)
                yield
            finally:
                _MUTATION_STATE.depth = 0
                _MUTATION_STATE.path = None
                if os.name == "nt":
                    import msvcrt

                    lock_file.seek(0)
                    msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)


def _purpose(classification: str) -> str:
    if classification == "unrelated":
        return "Durable exclusions for papers judged unrelated during structured-reference Discovery curation."
    if classification == "borderline":
        return "Default exclusions for papers judged borderline during structured-reference Discovery curation; entries may be explicitly reconsidered later."
    raise ValueError(f"unsupported classification: {classification}")


def _load(path: Path, *, classification: str) -> dict[str, Any]:
    if not path.exists():
        return {
            "schema_version": 1,
            "classification": classification,
            "purpose": _purpose(classification),
            "records": {},
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError(f"unsupported relevance-ledger schema: {path}")
    if not isinstance(payload.get("records"), dict):
        raise ValueError(f"relevance ledger is missing records: {path}")
    return payload


def _identity_set(canonical_id: str, identity_tokens: list[str] | None = None) -> tuple[str, set[str]]:
    normalized = citation_graph.normalized_identifiers({"canonical_id": canonical_id})
    canonical = normalized[0] if normalized else str(canonical_id).strip()
    if not canonical:
        raise ValueError("canonical_id is required")
    tokens = set(normalized)
    for token in identity_tokens or []:
        token_ids = citation_graph.normalized_identifiers({"canonical_id": token})
        tokens.update(token_ids or ([token.strip()] if token.strip() else []))
    tokens.add(canonical)
    return canonical, tokens


def normalized_relevance_tokens(
    canonical_id: str, identity_tokens: list[str] | None = None
) -> tuple[str, set[str]]:
    """Normalize a reviewed canonical ID and its explicit identity tokens."""
    canonical, _tokens = _identity_set(canonical_id)
    tokens: set[str] = set()
    for value in [canonical_id, *(identity_tokens or [])]:
        token = str(value).strip()
        if token.lower().startswith("id:"):
            token = token[3:].strip()
        if not token:
            continue
        normalized = citation_graph.normalized_identifiers({"canonical_id": token})
        tokens.update(normalized or [token])
    tokens.add(canonical)
    return canonical, tokens


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    """Atomically replace one ledger file with the supplied exact bytes."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_path, path)
        try:
            dir_fd = os.open(path.parent, os.O_RDONLY)
        except OSError:
            return
        try:
            os.fsync(dir_fd)
        except OSError:
            pass
        finally:
            os.close(dir_fd)
    finally:
        try:
            temp_path.unlink(missing_ok=True)
        except OSError:
            pass


def _row_identity(key: str, row: Any) -> tuple[str, set[str]]:
    metadata = row if isinstance(row, dict) else {}
    raw_canonical = metadata.get("canonical_id") or key
    canonical, tokens = normalized_relevance_tokens(str(raw_canonical))
    tokens.update(normalized_relevance_tokens(key)[1])
    raw_tokens = metadata.get("identity_tokens") or []
    if not isinstance(raw_tokens, list):
        raise ValueError(f"invalid identity_tokens for ledger row {key}")
    for value in raw_tokens:
        if not isinstance(value, str):
            raise ValueError(f"invalid identity token for ledger row {key}")
        tokens.update(normalized_relevance_tokens(value)[1])
    return canonical, tokens


def _clear_ledger_bytes(payload: dict[str, Any]) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def validate_clear_transaction_request(
    transaction_path: Path, *, request_id: str, request_sha256: str
) -> None:
    """Fail closed if a pending journal belongs to another request version."""
    if not transaction_path.exists():
        return
    journal = json.loads(transaction_path.read_text(encoding="utf-8"))
    if (
        not isinstance(journal, dict)
        or journal.get("schema_version") != 1
        or journal.get("operation") != "clear_relevance"
        or transaction_path.stem != request_id
        or journal.get("request_id") != request_id
        or journal.get("request_sha256") != request_sha256
    ):
        raise ValueError("clear_relevance journal does not match the immutable request")


def _recover_pending_clear_transactions(repo_root: Path) -> None:
    """Finalize committed-result journals or restore interrupted ledger writes.

    Called only while the shared cross-process ledger lock is held.
    """
    journal_dir = repo_root / CLEAR_JOURNAL_DIR
    if not journal_dir.exists():
        return
    unrelated_path = repo_root / DEFAULT_UNRELATED_LEDGER
    borderline_path = repo_root / DEFAULT_BORDERLINE_LEDGER
    request_dir = repo_root / ".survey/work-queue/reference-curation/requests"
    result_dir = repo_root / ".survey/work-queue/reference-curation/results"
    for transaction_path in sorted(journal_dir.glob("*.json")):
        journal = json.loads(transaction_path.read_text(encoding="utf-8"))
        if not isinstance(journal, dict) or journal.get("schema_version") != 1 or journal.get("operation") != "clear_relevance":
            raise ValueError(f"unsupported clear_relevance transaction journal: {transaction_path.name}")
        request_id = journal.get("request_id")
        request_sha = journal.get("request_sha256")
        if type(request_id) is not str or transaction_path.stem != request_id or type(request_sha) is not str:
            raise ValueError("clear_relevance transaction identity is invalid")
        request_path = request_dir / f"{request_id}.json"
        if not request_path.is_file() or hashlib.sha256(request_path.read_bytes()).hexdigest() != request_sha:
            raise ValueError("clear_relevance transaction request hash mismatch")
        result_path = result_dir / f"{request_id}.json"
        if result_path.exists():
            result_bytes = result_path.read_bytes()
            if hashlib.sha256(result_bytes).hexdigest() != journal.get("result_sha256"):
                raise ValueError("clear_relevance immutable result hash mismatch during recovery")
            result = json.loads(result_bytes.decode("utf-8"))
            if not isinstance(result, dict) or result.get("request_id") != request_id or result.get("request_operation") != "clear_relevance" or result.get("request_sha256") != request_sha or result.get("ok") is not True:
                raise ValueError("clear_relevance committed result does not match its journal")
            finalize_clear_transaction(
                transaction_path,
                unrelated_path=unrelated_path,
                borderline_path=borderline_path,
                request_id=request_id,
                request_sha256=request_sha,
                result_path=result_path,
            )
        else:
            _restore_clear_journal(
                transaction_path,
                unrelated_path=unrelated_path,
                borderline_path=borderline_path,
                request_id=request_id,
                request_sha256=request_sha,
                remove_journal=True,
            )


def record_clear_result(
    transaction_path: Path, *, request_id: str, request_sha256: str, result_sha256: str
) -> None:
    validate_clear_transaction_request(transaction_path, request_id=request_id, request_sha256=request_sha256)
    journal = json.loads(transaction_path.read_text(encoding="utf-8"))
    if type(result_sha256) is not str or len(result_sha256) != 64:
        raise ValueError("clear_relevance result hash is invalid")
    journal["result_sha256"] = result_sha256
    journal["phase"] = "result_prepared"
    _atomic_write_bytes(transaction_path, _clear_ledger_bytes(journal))


def _restore_clear_journal(
    transaction_path: Path,
    *,
    unrelated_path: Path,
    borderline_path: Path,
    request_id: str,
    request_sha256: str,
    remove_journal: bool,
) -> None:
    journal = json.loads(transaction_path.read_text(encoding="utf-8"))
    if not isinstance(journal, dict) or journal.get("schema_version") != 1 or journal.get("operation") != "clear_relevance":
        raise ValueError("unsupported clear_relevance transaction journal")
    if journal.get("request_id") != request_id or journal.get("request_sha256") != request_sha256:
        raise ValueError("clear_relevance transaction does not match the immutable request")
    expected_paths = {
        "unrelated": str(unrelated_path.resolve()),
        "borderline": str(borderline_path.resolve()),
    }
    if journal.get("ledger_paths") != expected_paths:
        raise ValueError("clear_relevance transaction ledger paths do not match")
    before = journal.get("before")
    after = journal.get("after")
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise ValueError("clear_relevance transaction journal is missing ledger snapshots")
    paths = {"unrelated": unrelated_path, "borderline": borderline_path}
    snapshots: dict[str, bytes | None] = {}
    for name, path in paths.items():
        old = before.get(name)
        new = after.get(name)
        if not isinstance(old, dict) or not isinstance(new, dict):
            raise ValueError(f"clear_relevance transaction snapshot is missing {name}")
        try:
            old_bytes = base64.b64decode(old["bytes_base64"], validate=True) if old["exists"] else None
        except (KeyError, ValueError) as exc:
            raise ValueError(f"invalid clear_relevance prior snapshot for {name}") from exc
        if old_bytes is not None and hashlib.sha256(old_bytes).hexdigest() != old.get("sha256"):
            raise ValueError(f"clear_relevance prior snapshot hash mismatch for {name}")
        if old_bytes is None and old.get("sha256") is not None:
            raise ValueError(f"clear_relevance absent prior snapshot has a hash for {name}")
        current = path.read_bytes() if path.exists() else None
        current_hash = hashlib.sha256(current).hexdigest() if current is not None else None
        allowed = {old.get("sha256"), new.get("sha256")}
        if current_hash not in allowed:
            raise ValueError(f"clear_relevance ledger changed outside its transaction: {name}")
        snapshots[name] = old_bytes

    for name, path in paths.items():
        old_bytes = snapshots[name]
        if old_bytes is None:
            path.unlink(missing_ok=True)
        else:
            current = path.read_bytes() if path.exists() else None
            if current != old_bytes:
                _atomic_write_bytes(path, old_bytes)
    if remove_journal:
        transaction_path.unlink(missing_ok=True)


def rollback_clear_transaction(
    transaction_path: Path,
    *,
    unrelated_path: Path,
    borderline_path: Path,
    request_id: str,
    request_sha256: str,
) -> None:
    if transaction_path.exists():
        _restore_clear_journal(
            transaction_path,
            unrelated_path=unrelated_path,
            borderline_path=borderline_path,
            request_id=request_id,
            request_sha256=request_sha256,
            remove_journal=True,
        )


def finalize_clear_transaction(
    transaction_path: Path,
    *,
    unrelated_path: Path,
    borderline_path: Path,
    request_id: str,
    request_sha256: str,
    result_path: Path,
) -> None:
    """Remove a completed transaction journal after its immutable result exists."""
    if not transaction_path.exists():
        return
    journal = json.loads(transaction_path.read_text(encoding="utf-8"))
    if journal.get("request_id") != request_id or journal.get("request_sha256") != request_sha256:
        raise ValueError("clear_relevance transaction does not match the immutable request")
    expected_paths = {
        "unrelated": str(unrelated_path.resolve()),
        "borderline": str(borderline_path.resolve()),
    }
    if not isinstance(journal, dict) or journal.get("ledger_paths") != expected_paths:
        raise ValueError("clear_relevance transaction ledger paths do not match")
    after = journal.get("after")
    if not isinstance(after, dict):
        raise ValueError("clear_relevance transaction journal is missing expected ledger state")
    for name, path in (("unrelated", unrelated_path), ("borderline", borderline_path)):
        entry = after.get(name)
        if not isinstance(entry, dict):
            raise ValueError(f"clear_relevance transaction expected state is missing {name}")
        current = path.read_bytes() if path.exists() else None
        current_hash = hashlib.sha256(current).hexdigest() if current is not None else None
        if current_hash != entry.get("sha256"):
            raise ValueError(f"clear_relevance ledger differs from completed transaction: {name}")
    result_bytes = result_path.read_bytes()
    if hashlib.sha256(result_bytes).hexdigest() != journal.get("result_sha256"):
        raise ValueError("clear_relevance result hash does not match transaction")
    result = json.loads(result_bytes.decode("utf-8"))
    if not isinstance(result, dict) or result.get("ok") is not True or result.get("request_id") != request_id or result.get("request_operation") != "clear_relevance" or result.get("request_sha256") != request_sha256:
        raise ValueError("clear_relevance result does not match transaction")
    transaction_path.unlink(missing_ok=True)


def _clear_relevance_locked(
    unrelated_path: Path,
    borderline_path: Path,
    *,
    canonical_id: str,
    identity_tokens: list[str],
    request_id: str,
    request_sha256: str,
) -> dict[str, Any]:
    """Remove only explicitly reviewed matching rows from both exclusion ledgers.

    Both ledgers are read and checked before mutation. If a write fails, exact
    prior bytes (or prior absence) are restored before the error is propagated.
    """
    canonical, target_tokens = normalized_relevance_tokens(canonical_id, identity_tokens)
    paths = (("unrelated", unrelated_path), ("borderline", borderline_path))
    transaction_path = unrelated_path.parents[3] / CLEAR_JOURNAL_DIR / f"{request_id}.json"
    if transaction_path.exists():
        _restore_clear_journal(
            transaction_path,
            unrelated_path=unrelated_path,
            borderline_path=borderline_path,
            request_id=request_id,
            request_sha256=request_sha256,
            remove_journal=True,
        )
    snapshots: dict[Path, bytes | None] = {}
    payloads: dict[Path, dict[str, Any]] = {}
    for classification, path in paths:
        snapshots[path] = path.read_bytes() if path.exists() else None
        payload = _load(path, classification=classification)
        payloads[path] = payload

    owners: dict[str, set[str]] = {}
    rows_by_path: dict[Path, list[tuple[str, Any, str, set[str]]]] = {}
    for _classification, path in paths:
        rows = []
        for key, row in payloads[path]["records"].items():
            if not isinstance(key, str):
                raise ValueError("relevance ledger contains a non-string record key")
            row_canonical, row_tokens = _row_identity(key, row)
            rows.append((key, row, row_canonical, row_tokens))
            for token in row_tokens:
                owners.setdefault(token, set()).add(row_canonical)
        rows_by_path[path] = rows

    candidate_tokens: set[str] = set(target_tokens)
    for rows in rows_by_path.values():
        for _key, _row, row_canonical, row_tokens in rows:
            if row_canonical == canonical or row_tokens.intersection(target_tokens):
                candidate_tokens.update(row_tokens)
    collisions = {
        token: sorted(token_owners)
        for token, token_owners in owners.items()
        if len(token_owners) > 1 and token in candidate_tokens
    }
    if collisions:
        raise ValueError(f"cross-canonical alias ownership collision: {collisions}")
    mismatched_owners = {
        token: sorted(owners[token])
        for token in candidate_tokens
        if token in owners and owners[token] != {canonical}
    }
    if mismatched_owners:
        raise ValueError(f"reviewed token is owned by a different canonical ID: {mismatched_owners}")

    removed_rows: list[dict[str, Any]] = []
    changed_payloads: dict[Path, dict[str, Any]] = {}
    for classification, path in paths:
        records = payloads[path]["records"]
        updated_records = dict(records)
        for key, row, row_canonical, row_tokens in rows_by_path[path]:
            if row_canonical == canonical or row_tokens.intersection(target_tokens):
                removed_rows.append({"ledger": classification, "key": key, "row": row})
                updated_records.pop(key, None)
        if len(updated_records) != len(records):
            updated = dict(payloads[path])
            updated["records"] = updated_records
            updated["updated_at"] = _now()
            updated["record_count"] = len(updated_records)
            changed_payloads[path] = updated

    write_paths = [path for _classification, path in paths if path in changed_payloads]
    after_bytes: dict[Path, bytes | None] = {}
    for _classification, path in paths:
        after_bytes[path] = (
            _clear_ledger_bytes(changed_payloads[path]) if path in changed_payloads else snapshots[path]
        )
    journal = {
        "schema_version": 1,
        "operation": "clear_relevance",
        "request_id": request_id,
        "request_sha256": request_sha256,
        "ledger_paths": {
            classification: str(path.resolve()) for classification, path in paths
        },
        "before": {
            classification: {
                "exists": snapshots[path] is not None,
                "sha256": hashlib.sha256(snapshots[path]).hexdigest() if snapshots[path] is not None else None,
                "bytes_base64": base64.b64encode(snapshots[path]).decode("ascii") if snapshots[path] is not None else "",
            }
            for classification, path in paths
        },
        "after": {
            classification: {
                "exists": after_bytes[path] is not None,
                "sha256": hashlib.sha256(after_bytes[path]).hexdigest() if after_bytes[path] is not None else None,
            }
            for classification, path in paths
        },
    }
    journal_written = False
    try:
        _atomic_write_bytes(transaction_path, _clear_ledger_bytes(journal))
        journal_written = True
        for path in write_paths:
            _atomic_write_bytes(path, after_bytes[path] or b"")
    except Exception as write_error:
        rollback_errors: list[str] = []
        if journal_written:
            try:
                rollback_clear_transaction(
                    transaction_path,
                    unrelated_path=unrelated_path,
                    borderline_path=borderline_path,
                    request_id=request_id,
                    request_sha256=request_sha256,
                )
            except Exception as rollback_error:
                rollback_errors.append(f"transaction journal: {type(rollback_error).__name__}: {rollback_error}")
        if rollback_errors:
            raise RuntimeError(
                f"clear_relevance write failed ({type(write_error).__name__}: {write_error}); "
                f"ledger rollback also failed: {'; '.join(rollback_errors)}"
            ) from write_error
        raise

    removed_rows.sort(key=lambda item: (item["ledger"], item["key"]))
    return {
        "canonical_id": canonical,
        "identity_tokens": sorted(target_tokens),
        "removed_rows": removed_rows,
        "transaction_path": transaction_path,
    }


def clear_relevance(
    unrelated_path: Path,
    borderline_path: Path,
    *,
    canonical_id: str,
    identity_tokens: list[str],
    request_id: str,
    request_sha256: str,
) -> dict[str, Any]:
    with ledger_mutation_lock(unrelated_path, borderline_path):
        return _clear_relevance_locked(
            unrelated_path,
            borderline_path,
            canonical_id=canonical_id,
            identity_tokens=identity_tokens,
            request_id=request_id,
            request_sha256=request_sha256,
        )


def _write(path: Path, payload: dict[str, Any]) -> None:
    payload["updated_at"] = _now()
    payload["record_count"] = len(payload["records"])
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)


def _remove_matching(path: Path, *, classification: str, tokens: set[str]) -> bool:
    if not path.exists():
        return False
    payload = _load(path, classification=classification)
    records = payload["records"]
    removed = False
    for key, row in list(records.items()):
        row_tokens = {str(key)}
        if isinstance(row, dict):
            row_tokens.update(str(v) for v in (row.get("identity_tokens") or []) if str(v))
            row_tokens.update(citation_graph.normalized_identifiers(row))
        if tokens.intersection(row_tokens):
            records.pop(key, None)
            removed = True
    if removed:
        _write(path, payload)
    return removed


def _mark_locked(
    path: Path,
    *,
    classification: str,
    canonical_id: str,
    title: str | None = None,
    reason: str,
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    opposite_path: Path | None = None,
    opposite_classification: str | None = None,
    reconsidered_from_borderline: bool = False,
) -> dict[str, Any]:
    canonical, tokens = _identity_set(canonical_id, identity_tokens)
    payload = _load(path, classification=classification)
    records = payload["records"]

    existing_key = next(
        (
            key
            for key, row in records.items()
            if isinstance(row, dict)
            and tokens.intersection(set(row.get("identity_tokens") or []) | {str(key)})
        ),
        canonical,
    )
    old = records.get(existing_key) if isinstance(records.get(existing_key), dict) else {}
    first_checked = old.get("first_checked_at") or _now()
    source_paths = set(old.get("linked_from") or [])
    source_paths.update(linked_from or [])
    try:
        borderline_recheck_count = max(int(old.get("borderline_recheck_count") or 0), 0)
    except (TypeError, ValueError):
        borderline_recheck_count = 0
    if classification == "borderline" and reconsidered_from_borderline:
        borderline_recheck_count += 1

    row = {
        "classification": classification,
        "canonical_id": canonical,
        "identity_tokens": sorted(tokens | set(old.get("identity_tokens") or [])),
        "reason": str(reason).strip(),
        "first_checked_at": first_checked,
        "last_checked_at": _now(),
        "linked_from": sorted(str(v) for v in source_paths if str(v).strip()),
    }
    if classification == "borderline":
        row["borderline_recheck_count"] = borderline_recheck_count
        if reconsidered_from_borderline:
            row["last_reconsidered_at"] = row["last_checked_at"]
        elif old.get("last_reconsidered_at"):
            row["last_reconsidered_at"] = old["last_reconsidered_at"]
    if title or old.get("title"):
        row["title"] = str(title or old.get("title")).strip()

    if existing_key != canonical:
        records.pop(existing_key, None)
    records[canonical] = row
    payload["classification"] = classification
    payload["purpose"] = _purpose(classification)
    _write(path, payload)

    if opposite_path is not None and opposite_classification is not None:
        _remove_matching(
            opposite_path,
            classification=opposite_classification,
            tokens=set(row["identity_tokens"]),
        )
    return row


def mark(
    path: Path,
    *,
    classification: str,
    canonical_id: str,
    title: str | None = None,
    reason: str,
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    opposite_path: Path | None = None,
    opposite_classification: str | None = None,
    reconsidered_from_borderline: bool = False,
) -> dict[str, Any]:
    lock_paths = (path, opposite_path) if opposite_path is not None else (path,)
    with ledger_mutation_lock(*lock_paths):
        return _mark_locked(
            path,
            classification=classification,
            canonical_id=canonical_id,
            title=title,
            reason=reason,
            identity_tokens=identity_tokens,
            linked_from=linked_from,
            opposite_path=opposite_path,
            opposite_classification=opposite_classification,
            reconsidered_from_borderline=reconsidered_from_borderline,
        )


def clear_borderline(
    path: Path,
    *,
    canonical_id: str,
    identity_tokens: list[str] | None = None,
) -> bool:
    """Remove a borderline exclusion after a reconsidered candidate is promoted."""
    _canonical, tokens = _identity_set(canonical_id, identity_tokens)
    with ledger_mutation_lock(path):
        return _remove_matching(path, classification="borderline", tokens=tokens)


def mark_unrelated(
    path: Path,
    *,
    canonical_id: str,
    title: str | None = None,
    reason: str = "outside survey scope",
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    borderline_path: Path | None = None,
) -> dict[str, Any]:
    return mark(
        path,
        classification="unrelated",
        canonical_id=canonical_id,
        title=title,
        reason=reason,
        identity_tokens=identity_tokens,
        linked_from=linked_from,
        opposite_path=borderline_path,
        opposite_classification="borderline" if borderline_path is not None else None,
    )


def mark_borderline(
    path: Path,
    *,
    canonical_id: str,
    title: str | None = None,
    reason: str = "borderline relevance or expected survey value",
    identity_tokens: list[str] | None = None,
    linked_from: list[str] | None = None,
    unrelated_path: Path | None = None,
    reconsidered_from_borderline: bool = False,
) -> dict[str, Any]:
    return mark(
        path,
        classification="borderline",
        canonical_id=canonical_id,
        title=title,
        reason=reason,
        identity_tokens=identity_tokens,
        linked_from=linked_from,
        opposite_path=unrelated_path,
        opposite_classification="unrelated" if unrelated_path is not None else None,
        reconsidered_from_borderline=reconsidered_from_borderline,
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="command", required=True)
    for name, default_reason in (
        ("mark-unrelated", "outside survey scope"),
        ("mark-borderline", "borderline relevance or expected survey value"),
    ):
        cmd = sub.add_parser(name)
        cmd.add_argument("--root", default=".")
        cmd.add_argument("--ledger")
        cmd.add_argument("--canonical-id", required=True)
        cmd.add_argument("--identity-token", action="append", default=[])
        cmd.add_argument("--title")
        cmd.add_argument("--reason", default=default_reason)
        cmd.add_argument("--source-path", action="append", default=[])
        if name == "mark-borderline":
            cmd.add_argument("--reconsidered-from-borderline", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    unrelated_path = root / DEFAULT_UNRELATED_LEDGER
    borderline_path = root / DEFAULT_BORDERLINE_LEDGER

    if args.command == "mark-unrelated":
        ledger = Path(args.ledger).resolve() if args.ledger else unrelated_path
        row = mark_unrelated(
            ledger,
            canonical_id=args.canonical_id,
            title=args.title,
            reason=args.reason,
            identity_tokens=args.identity_token,
            linked_from=args.source_path,
            borderline_path=borderline_path if ledger == unrelated_path else None,
        )
        label = "無関係"
    elif args.command == "mark-borderline":
        ledger = Path(args.ledger).resolve() if args.ledger else borderline_path
        row = mark_borderline(
            ledger,
            canonical_id=args.canonical_id,
            title=args.title,
            reason=args.reason,
            identity_tokens=args.identity_token,
            linked_from=args.source_path,
            unrelated_path=unrelated_path if ledger == borderline_path else None,
            reconsidered_from_borderline=bool(args.reconsidered_from_borderline),
        )
        label = "微妙"
    else:
        return 2

    print(json.dumps({"ok": True, "ledger": str(ledger), "record": row}, ensure_ascii=False))
    print(
        f"[WORKER-GUIDE][完了] {row['canonical_id']} を{label}論文台帳へ保存しました。",
        file=sys.stderr,
    )
    print(
        "[WORKER-GUIDE][次] 同じ識別子は通常の repository_references 探索から除外されます。"
        "次の候補の評価へ進んでください。",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
