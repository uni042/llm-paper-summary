#!/usr/bin/env python3
"""Bounded, evidence-pinned retirement of unsuitable paper records.

The apply command is intentionally explicit. Dry runs are read-only; apply requires
the exact clean source revision and uses the canonical immutable relevance request API.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from urllib.parse import unquote
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any

try:
    import fcntl
except ImportError:  # pragma: no cover - Windows uses msvcrt locking
    fcntl = None

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_identity  # noqa: E402
import paper_retirement_registry  # noqa: E402
import process_reference_relevance_requests as relevance_requests  # noqa: E402
import research_job_reconciliation  # noqa: E402
import survey  # noqa: E402

MAX_ENTRIES = 25
MAX_TOTAL_BYTES = 64 * 1024 * 1024


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
    if result.returncode:
        raise ValueError(result.stderr.strip() or "git preflight failed")
    return result.stdout.strip()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    _atomic_bytes(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def _atomic_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    cursor = path
    while cursor != cursor.parent:
        if _is_link(cursor):
            raise ValueError(f"refusing symlink state path: {path}")
        cursor = cursor.parent
    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(mode="wb", dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temp_path = Path(handle.name)
        os.replace(temp_path, path)
        temp_path = None
        _fsync_dir(path.parent)
    finally:
        if temp_path is not None:
            temp_path.unlink(missing_ok=True)


def _fsync_dir(path: Path) -> None:
    try:
        descriptor = os.open(path, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
    except OSError:
        # Windows does not expose directory fsync through the CRT; file data was
        # still fsynced before atomic replacement.
        return


def _durable_unlink(path: Path) -> None:
    path.unlink()
    _fsync_dir(path.parent)


def _is_link(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def _journal_digest(journal: dict[str, Any]) -> str:
    body = {key: value for key, value in journal.items() if key != "journal_sha256"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def _write_journal(path: Path, journal: dict[str, Any]) -> None:
    journal["journal_sha256"] = _journal_digest(journal)
    _atomic_json(path, journal)


def _phase_checkpoint(_phase: str) -> None:
    """Test seam for durable-phase crash simulation."""


@contextlib.contextmanager
def _transaction_lock(root: Path):
    root = root.resolve()
    lock_key = hashlib.sha256(str(root).casefold().encode("utf-8")).hexdigest()
    lock_path = Path(tempfile.gettempdir()) / f"codex-paper-retirement-{lock_key}.lock"
    if _is_link(lock_path):
        raise ValueError("paper-retirement lock path is a symlink")
    with lock_path.open("a+b") as handle:
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        try:
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                assert fcntl is not None
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except (OSError, BlockingIOError) as exc:
            raise ValueError("another paper-retirement transaction is active") from exc
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                assert fcntl is not None
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


def _confined_path(root: Path, relative: str, allowed: PurePosixPath) -> Path:
    if not isinstance(relative, str) or "\\" in relative or ":" in relative:
        raise ValueError("journal path must use normalized repository-relative POSIX syntax")
    parsed = PurePosixPath(relative)
    if parsed.is_absolute() or not parsed.parts or ".." in parsed.parts or not parsed.is_relative_to(allowed):
        raise ValueError(f"journal path escapes allowed namespace: {relative!r}")
    target = root.joinpath(*parsed.parts)
    current = target
    while current != root:
        if _is_link(current):
            raise ValueError(f"journal path has symlink ancestry: {relative}")
        current = current.parent
    resolved = target.resolve(strict=False)
    if not resolved.is_relative_to(root):
        raise ValueError(f"journal path resolves outside repository: {relative}")
    return target


def _markdown_destinations(markdown: str):
    patterns = (
        r"\]\(\s*(<[^>]+>|[^\s)]+)",
        r"(?m)^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|[^\s]+)",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, markdown):
            raw = match.group(1).strip()
            if raw.startswith("<") and raw.endswith(">"):
                raw = raw[1:-1]
            raw = re.sub(r"\\(.)", r"\1", raw)
            yield unquote(raw.split("#", 1)[0])


def preflight(root: Path, manifest_path: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("schema_version") != 1:
        raise ValueError("manifest schema_version must be 1")
    rows = manifest.get("entries")
    if not isinstance(rows, list) or not 1 <= len(rows) <= MAX_ENTRIES:
        raise ValueError(f"manifest must contain 1..{MAX_ENTRIES} entries")
    expected_commit = str(manifest.get("source_commit") or "")
    actual_commit = _git(root, "rev-parse", "HEAD")
    if expected_commit != actual_commit:
        raise ValueError("source_commit differs from current HEAD")
    if _git(root, "status", "--porcelain"):
        raise ValueError("retirement requires a clean worktree")
    registry = paper_retirement_registry.load_registry(root)
    _confined_path(root, paper_retirement_registry.REGISTRY_RELATIVE_PATH.as_posix(), PurePosixPath(".survey"))
    _confined_path(root, ".survey/survey-state/paper-identity-index.json", PurePosixPath(".survey"))
    aliases: dict[str, str] = {}
    total = 0
    checked = []
    active_index = research_job_reconciliation.build_paper_index(root)
    for index, entry in enumerate(rows):
        if not isinstance(entry, dict):
            raise ValueError("manifest entry must be an object")
        path_text = str(entry.get("path") or "")
        path = Path(path_text)
        if path.is_absolute() or ".." in path.parts or path.parts[:1] != ("papers",) or path.suffix != ".md":
            raise ValueError(f"unsafe paper path: {path_text}")
        unresolved_target = root / path
        if any(_is_link(part) for part in [unresolved_target, *unresolved_target.parents] if part.exists()):
            raise ValueError(f"paper path contains a symlink: {path_text}")
        target = unresolved_target.resolve(strict=True)
        if not target.is_relative_to((root / "papers").resolve()) or not target.is_file():
            raise ValueError(f"paper path escapes papers root or is a symlink: {path_text}")
        content = target.read_bytes()
        total += len(content)
        if total > MAX_TOTAL_BYTES:
            raise ValueError("manifest source bytes exceed 64 MiB")
        sha = hashlib.sha256(content).hexdigest()
        if sha != entry.get("source_sha256"):
            raise ValueError(f"source SHA-256 changed: {path_text}")
        blob = _git(root, "rev-parse", f"HEAD:{path.as_posix()}")
        if blob != entry.get("source_git_blob_sha"):
            raise ValueError(f"source Git blob changed: {path_text}")
        git_bytes = subprocess.run(["git", "show", f"HEAD:{path.as_posix()}"], cwd=root, capture_output=True)
        if git_bytes.returncode or hashlib.sha256(git_bytes.stdout).hexdigest() != sha:
            raise ValueError(f"worktree bytes differ from pinned Git blob: {path_text}")
        old_root = survey.ROOT
        try:
            survey.ROOT = root
            meta, _ = survey.front(target)
        finally:
            survey.ROOT = old_root
        canonical = str(meta.get("canonical_id") or "")
        if canonical != entry.get("canonical_id"):
            raise ValueError(f"canonical identity mismatch: {path_text}")
        if entry.get("classification") != "unrelated" or not str(entry.get("reason") or "").strip() or not str(entry.get("evidence") or "").strip() or not str(entry.get("retirement_id") or "").strip():
            raise ValueError("only unrelated records with retirement_id, reason, and evidence can be retired")
        verified = sorted(paper_identity.record_identifiers(meta))
        expected_aliases = sorted({paper_identity.safe_norm_id(str(v)) for v in entry.get("verified_aliases", []) if v})
        if not expected_aliases or set(expected_aliases) != set(verified):
            raise ValueError(f"verified aliases differ from current paper metadata: {path_text}")
        if paper_identity.safe_norm_id(canonical) not in expected_aliases:
            raise ValueError(f"canonical identity absent from verified aliases: {path_text}")
        for alias in expected_aliases:
            token = "id:" + alias
            conflict = active_index["token_conflicts"].get(token)
            owner_record = active_index["by_token"].get(token)
            if conflict and any(item.get("path") != path.as_posix() for item in conflict):
                raise ValueError(f"active paper identity collision: {alias}")
            if owner_record and owner_record.get("path") != path.as_posix():
                raise ValueError(f"active paper identity collision: {alias}")
            owner = aliases.setdefault(alias, canonical)
            if owner != canonical:
                raise ValueError(f"manifest alias collision: {alias}")
        for other in registry["records"].values():
            other_aliases = set(other["verified_aliases"])
            if set(expected_aliases) & other_aliases:
                raise ValueError(f"paper alias already retired: {path_text}")
        for other in (root / "papers").rglob("*.md"):
            if other == target:
                continue
            markdown = other.read_text(encoding="utf-8", errors="ignore")
            for linked in _markdown_destinations(markdown):
                if not linked or "://" in linked or linked.startswith("mailto:"):
                    continue
                linked_path = Path(linked.lstrip("/"))
                resolved_link = ((root / linked_path) if linked.startswith("/") else (other.parent / linked_path)).resolve()
                if resolved_link == target:
                    raise ValueError(f"inbound local markdown link requires reviewed rewrite: {path_text}")
        checked.append({**entry, "path": path.as_posix(), "original_path": path.as_posix(), "canonical_id": canonical, "verified_aliases": expected_aliases, "source_commit": actual_commit, "source_sha256": sha, "source_git_blob_sha": blob, "_source_bytes": len(content)})
    return {"schema_version": 1, "source_commit": actual_commit, "entry_count": len(checked), "source_bytes": total, "entries": checked}


def apply(root: Path, manifest_path: Path) -> dict[str, Any]:
    with _transaction_lock(root):
        return _apply_locked(root, manifest_path)


def _apply_locked(root: Path, manifest_path: Path) -> dict[str, Any]:
    root = root.resolve()
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    transaction_id = str(manifest.get("transaction_id") or "")
    if not transaction_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in transaction_id):
        raise ValueError("transaction_id with safe filename characters is required")
    journal_path = root / ".survey/survey-state/paper-retirement-journals" / f"{transaction_id}.json"
    _confined_path(root, journal_path.relative_to(root).as_posix(), PurePosixPath(".survey/survey-state/paper-retirement-journals"))
    manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
    if journal_path.exists():
        prior_journal = json.loads(journal_path.read_text(encoding="utf-8"))
        if prior_journal.get("manifest_sha256") != manifest_hash:
            raise ValueError("transaction id is already bound to a different plan")
        if prior_journal.get("phase") == "complete":
            _validate_recovery_journal(root, transaction_id, prior_journal)
            return {"ok": True, "transaction_id": transaction_id, "entry_count": len(prior_journal.get("entries", [])), "phase": "complete", "already_applied": True}
        raise ValueError(f"transaction journal is in phase {prior_journal.get('phase')}; recover or inspect before retry")
    plan = preflight(root, manifest_path)
    registry_path = root / paper_retirement_registry.REGISTRY_RELATIVE_PATH
    registry = paper_retirement_registry.load_registry(root)
    identity_path = root / ".survey/survey-state/paper-identity-index.json"
    old_identity_text = identity_path.read_bytes().decode("utf-8") if identity_path.exists() else None
    delta_root = root / ".survey/survey-state/identity-deltas"
    prior_deltas: list[dict[str, Any]] = []
    retired_ids = {row["canonical_id"] for row in plan["entries"]}
    retired_paths = {row["path"] for row in plan["entries"]}
    retired_aliases = {alias for row in plan["entries"] for alias in row["verified_aliases"]}
    if delta_root.exists():
        for delta_path in sorted(delta_root.rglob("*.json")):
            delta = json.loads(delta_path.read_text(encoding="utf-8"))
            matches = bool(
                delta.get("canonical_id") in retired_ids
                or delta.get("path") in retired_paths
                or set(delta.get("identifiers") or []) & retired_aliases
            )
            if matches:
                expected_aliases = next(row["verified_aliases"] for row in plan["entries"] if row["canonical_id"] == delta.get("canonical_id"))
                delta_aliases = sorted({paper_identity.safe_norm_id(str(value)) for value in delta.get("identifiers", []) if value})
                if delta.get("canonical_id") not in retired_ids or delta.get("path") not in retired_paths or delta_aliases != expected_aliases:
                    raise ValueError(f"identity delta alias/path conflict: {delta_path}")
                raw_delta = delta_path.read_bytes()
                prior_deltas.append({"path": delta_path.relative_to(root).as_posix(), "record": delta, "raw": raw_delta.decode("utf-8"), "sha256": hashlib.sha256(raw_delta).hexdigest()})
    prior_registry = json.loads(json.dumps(registry, ensure_ascii=False))
    journal = {"schema_version": 2, "transaction_id": transaction_id, "manifest_sha256": manifest_hash, "source_commit": plan["source_commit"], "phase": "prepared", "prior_registry_exists": registry_path.exists(), "prior_registry": prior_registry, "prior_registry_sha256": _canonical_json_sha(prior_registry), "prior_identity_index": old_identity_text, "prior_identity_index_sha256": hashlib.sha256(old_identity_text.encode("utf-8")).hexdigest() if old_identity_text is not None else None, "prior_deltas": prior_deltas, "entries": [{k: v for k, v in row.items() if not k.startswith("_")} for row in plan["entries"]]}
    _write_journal(journal_path, journal)
    _phase_checkpoint("prepared")
    try:
        for row in plan["entries"]:
            canonical = row["canonical_id"]
            request_id = str(row.get("relevance_request_id") or f"{transaction_id}-{hashlib.sha256(canonical.encode()).hexdigest()[:10]}")
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", request_id):
                raise ValueError(f"unsafe official relevance request id: {request_id!r}")
            request_path = root / relevance_requests.REQUEST_DIR / f"{request_id}.json"
            result_path = root / relevance_requests.RESULT_DIR / f"{request_id}.json"
            _confined_path(root, request_path.relative_to(root).as_posix(), PurePosixPath(".survey/work-queue/reference-curation/requests"))
            _confined_path(root, result_path.relative_to(root).as_posix(), PurePosixPath(".survey/work-queue/reference-curation/results"))
            if request_path.exists() or result_path.exists():
                raise ValueError(f"relevance request/result already exists: {request_id}")
            request = {"schema_version": 1, "request_id": request_id, "operation": "mark_unrelated", "canonical_id": canonical, "title": row.get("title"), "reason": row["reason"], "identity_tokens": ["id:" + alias for alias in row["verified_aliases"]]}
            _atomic_json(request_path, request)
            outcome = relevance_requests.process_request(root, request_path)
            if not outcome.get("ok"):
                raise ValueError(f"official unrelated request failed: {request_id}")
            row["relevance_request_id"] = request_id
            row["relevance_result_id"] = request_id
            registry["records"][canonical] = {k: row[k] for k in ("retirement_id", "canonical_id", "verified_aliases", "original_path", "source_sha256", "source_git_blob_sha", "source_commit", "classification", "reason", "evidence", "relevance_request_id", "relevance_result_id") if k in row}
        journal["phase"] = "requests_written"
        _write_journal(journal_path, journal)
        _phase_checkpoint("requests_written")
        journal["after_registry"] = registry
        journal["after_registry_sha256"] = hashlib.sha256(json.dumps(registry, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
        _write_journal(journal_path, journal)
        _atomic_json(registry_path, registry)
        journal["phase"] = "registry_written"
        _write_journal(journal_path, journal)
        _phase_checkpoint("registry_written")
        for row in plan["entries"]:
            target = _confined_path(root, row["path"], PurePosixPath("papers"))
            if target.is_symlink() or not target.is_file() or hashlib.sha256(target.read_bytes()).hexdigest() != row["source_sha256"]:
                raise ValueError(f"paper changed while transaction held lock: {row['path']}")
            _durable_unlink(target)
            _phase_checkpoint("paper_deleted:" + row["canonical_id"])
        for row in prior_deltas:
            delta_path = _confined_path(root, row["path"], PurePosixPath(".survey/survey-state/identity-deltas"))
            if hashlib.sha256(delta_path.read_bytes()).hexdigest() != row["sha256"]:
                raise ValueError(f"identity delta changed while transaction held lock: {row['path']}")
            _durable_unlink(delta_path)
            _phase_checkpoint("delta_deleted:" + row["path"])
        old_root = survey.ROOT
        try:
            survey.ROOT = root / ".survey"
            rebuilt_index = survey.identity(survey.papers())
        finally:
            survey.ROOT = old_root
        index_bytes = (json.dumps(rebuilt_index, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8")
        journal["after_identity_index_sha256"] = hashlib.sha256(index_bytes).hexdigest()
        journal["phase"] = "papers_deleted"
        _write_journal(journal_path, journal)
        _phase_checkpoint("papers_deleted")
        _atomic_bytes(identity_path, index_bytes)
        journal["phase"] = "index_rebuilt"
        _write_journal(journal_path, journal)
        _phase_checkpoint("index_rebuilt")
        journal["phase"] = "complete"
        _write_journal(journal_path, journal)
        _phase_checkpoint("complete")
    except Exception:
        raise
    return {"ok": True, "transaction_id": transaction_id, "entry_count": plan["entry_count"], "phase": journal["phase"]}


def _canonical_json_sha(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()


def _validate_recovery_journal(root: Path, transaction_id: str, journal: Any) -> tuple[list[tuple[Path, bytes]], Path, Path]:
    phases = {"prepared", "requests_written", "registry_written", "papers_deleted", "index_rebuilt", "complete", "rolled_back"}
    if not isinstance(journal, dict) or journal.get("schema_version") != 2 or journal.get("transaction_id") != transaction_id:
        raise ValueError("retirement journal identity/schema mismatch")
    if journal.get("phase") not in phases or journal.get("journal_sha256") != _journal_digest(journal):
        raise ValueError("retirement journal phase or integrity hash is invalid")
    if not re.fullmatch(r"[0-9a-f]{64}", str(journal.get("manifest_sha256") or "")):
        raise ValueError("retirement journal manifest fingerprint is invalid")
    commit = str(journal.get("source_commit") or "")
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("retirement journal source commit is invalid")
    _git(root, "cat-file", "-e", commit + "^{commit}")
    entries = journal.get("entries")
    if not isinstance(entries, list) or not 1 <= len(entries) <= MAX_ENTRIES:
        raise ValueError("retirement journal entries are invalid")
    prior = paper_retirement_registry.validate_registry(journal.get("prior_registry"))
    if journal.get("prior_registry_sha256") != _canonical_json_sha(prior):
        raise ValueError("retirement journal prior registry hash is invalid")
    if not isinstance(journal.get("prior_registry_exists"), bool):
        raise ValueError("retirement journal prior registry presence flag is invalid")
    prior_identity = journal.get("prior_identity_index")
    if prior_identity is None:
        if journal.get("prior_identity_index_sha256") is not None:
            raise ValueError("retirement journal prior index hash has no object")
    elif isinstance(prior_identity, str):
        try:
            parsed_index = json.loads(prior_identity)
        except json.JSONDecodeError as exc:
            raise ValueError("retirement journal prior index is invalid JSON") from exc
        if not isinstance(parsed_index, dict) or hashlib.sha256(prior_identity.encode("utf-8")).hexdigest() != journal.get("prior_identity_index_sha256"):
            raise ValueError("retirement journal prior index hash is invalid")
    else:
        raise ValueError("retirement journal prior index type is invalid")
    entry_by_canonical: dict[str, dict[str, Any]] = {}
    restore_bytes: list[tuple[Path, bytes]] = []
    for row in entries:
        if not isinstance(row, dict):
            raise ValueError("retirement journal entry is not an object")
        canonical = row.get("canonical_id")
        path_text = row.get("path")
        aliases = row.get("verified_aliases")
        if not isinstance(canonical, str) or canonical in entry_by_canonical or not isinstance(aliases, list):
            raise ValueError("retirement journal entry identity is invalid")
        normalized_aliases = sorted({paper_identity.safe_norm_id(str(alias)) for alias in aliases if alias})
        if not normalized_aliases or paper_identity.safe_norm_id(canonical) not in normalized_aliases:
            raise ValueError("retirement journal aliases are invalid")
        if row.get("source_commit") != commit or not re.fullmatch(r"[0-9a-f]{64}", str(row.get("source_sha256") or "")) or not re.fullmatch(r"[0-9a-f]{40}", str(row.get("source_git_blob_sha") or "")):
            raise ValueError("retirement journal pinned source identity is invalid")
        if not isinstance(row.get("retirement_id"), str) or not row.get("retirement_id"):
            raise ValueError("retirement journal id is invalid")
        target = _confined_path(root, path_text, PurePosixPath("papers"))
        blob = _git(root, "rev-parse", f"{commit}:{PurePosixPath(path_text).as_posix()}")
        if blob != row.get("source_git_blob_sha"):
            raise ValueError("retirement journal source Git blob mismatch")
        source = subprocess.run(["git", "show", f"{commit}:{PurePosixPath(path_text).as_posix()}"], cwd=root, capture_output=True)
        if source.returncode or hashlib.sha256(source.stdout).hexdigest() != row.get("source_sha256"):
            raise ValueError("retirement journal source SHA mismatch")
        if target.exists() and target.read_bytes() != source.stdout:
            raise ValueError(f"refusing to overwrite changed paper during restore: {path_text}")
        entry_by_canonical[canonical] = row
        restore_bytes.append((target, source.stdout))
    delta_rows = journal.get("prior_deltas")
    if not isinstance(delta_rows, list):
        raise ValueError("retirement journal deltas are invalid")
    delta_targets: list[Path] = []
    for delta in delta_rows:
        if not isinstance(delta, dict) or not isinstance(delta.get("record"), dict) or not isinstance(delta.get("raw"), str):
            raise ValueError("retirement journal delta record is invalid")
        delta_path = _confined_path(root, delta.get("path"), PurePosixPath(".survey/survey-state/identity-deltas"))
        try:
            raw_record = json.loads(delta["raw"])
        except json.JSONDecodeError as exc:
            raise ValueError("retirement journal delta JSON is invalid") from exc
        if raw_record != delta["record"] or hashlib.sha256(delta["raw"].encode("utf-8")).hexdigest() != delta.get("sha256"):
            raise ValueError("retirement journal delta hash is invalid")
        owner = entry_by_canonical.get(raw_record.get("canonical_id"))
        if owner is None or raw_record.get("path") != owner.get("path"):
            raise ValueError("retirement journal delta ownership is invalid")
        delta_aliases = sorted({paper_identity.safe_norm_id(str(alias)) for alias in raw_record.get("identifiers", []) if alias})
        owner_aliases = sorted({paper_identity.safe_norm_id(str(alias)) for alias in owner["verified_aliases"]})
        if delta_aliases != owner_aliases:
            raise ValueError("retirement journal delta alias ownership is invalid")
        if delta_path.exists() and hashlib.sha256(delta_path.read_bytes()).hexdigest() != delta.get("sha256"):
            raise ValueError("identity delta changed since retirement; refusing restore")
        delta_targets.append(delta_path)
    after_registry = journal.get("after_registry")
    if after_registry is not None:
        after_registry = paper_retirement_registry.validate_registry(after_registry)
        if journal.get("after_registry_sha256") != _canonical_json_sha(after_registry):
            raise ValueError("retirement journal after registry hash is invalid")
        for canonical, row in entry_by_canonical.items():
            installed = after_registry["records"].get(canonical)
            if not installed or installed.get("retirement_id") != row.get("retirement_id") or installed.get("source_sha256") != row.get("source_sha256") or installed.get("original_path") != row.get("path"):
                raise ValueError("retirement journal after registry ownership is invalid")
    elif journal.get("after_registry_sha256") is not None:
        raise ValueError("retirement journal after registry hash has no object")
    prior_aliases = {
        paper_identity.safe_norm_id(alias)
        for row in prior["records"].values()
        for alias in row["verified_aliases"]
    }
    new_aliases = {paper_identity.safe_norm_id(alias) for row in entry_by_canonical.values() for alias in row["verified_aliases"]}
    if prior_aliases & new_aliases:
        raise ValueError("retirement journal prior registry already owns a candidate alias")
    registry_path = root / paper_retirement_registry.REGISTRY_RELATIVE_PATH
    current_registry = paper_retirement_registry.load_registry(root)
    current_registry_sha = _canonical_json_sha(current_registry)
    allowed_registry_hashes = {journal.get("prior_registry_sha256"), journal.get("after_registry_sha256")}
    if current_registry_sha not in allowed_registry_hashes:
        raise ValueError("current registry is neither the pinned before nor after snapshot")
    identity_path = root / ".survey/survey-state/paper-identity-index.json"
    current_index_sha = hashlib.sha256(identity_path.read_bytes()).hexdigest() if identity_path.exists() else None
    allowed_index_hashes = {journal.get("prior_identity_index_sha256"), journal.get("after_identity_index_sha256")}
    if current_index_sha not in allowed_index_hashes:
        raise ValueError("current identity index is not a pinned transaction snapshot")
    if journal.get("after_identity_index_sha256") is not None and not re.fullmatch(r"[0-9a-f]{64}", str(journal["after_identity_index_sha256"])):
        raise ValueError("retirement journal after identity index hash is invalid")
    if journal.get("phase") in {"papers_deleted", "index_rebuilt", "complete"} and journal.get("after_identity_index_sha256") is None:
        raise ValueError("retirement journal lacks the expected rebuilt identity index hash")
    # Validate every destination before the first recovery write, including
    # symlink parents inserted after deletion.
    for target, _ in restore_bytes:
        _confined_path(root, target.relative_to(root).as_posix(), PurePosixPath("papers"))
    for target in delta_targets:
        _confined_path(root, target.relative_to(root).as_posix(), PurePosixPath(".survey/survey-state/identity-deltas"))
    _confined_path(root, paper_retirement_registry.REGISTRY_RELATIVE_PATH.as_posix(), PurePosixPath(".survey"))
    _confined_path(root, ".survey/survey-state/paper-identity-index.json", PurePosixPath(".survey"))
    return restore_bytes, registry_path, identity_path


def recover(root: Path, transaction_id: str, action: str) -> dict[str, Any]:
    with _transaction_lock(root):
        return _recover_locked(root, transaction_id, action)


def _recover_locked(root: Path, transaction_id: str, action: str) -> dict[str, Any]:
    root = root.resolve()
    if action != "restore" or not transaction_id or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in transaction_id):
        raise ValueError("recover requires action=restore and a safe transaction_id")
    journal_path = _confined_path(root, f".survey/survey-state/paper-retirement-journals/{transaction_id}.json", PurePosixPath(".survey/survey-state/paper-retirement-journals"))
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    restore_bytes, registry_path, identity_path = _validate_recovery_journal(root, transaction_id, journal)
    if journal.get("phase") == "rolled_back":
        return {"ok": True, "transaction_id": transaction_id, "phase": "rolled_back", "already_restored": True}
    for target, content in restore_bytes:
        _confined_path(root, target.relative_to(root).as_posix(), PurePosixPath("papers"))
        _atomic_bytes(target, content)
    prior = journal["prior_registry"]
    if journal["prior_registry_exists"]:
        _atomic_json(registry_path, prior)
    else:
        _durable_unlink(registry_path) if registry_path.exists() else None
    for delta in journal["prior_deltas"]:
        delta_path = _confined_path(root, delta["path"], PurePosixPath(".survey/survey-state/identity-deltas"))
        _atomic_bytes(delta_path, delta["raw"].encode("utf-8"))
    prior_identity = journal["prior_identity_index"]
    if isinstance(prior_identity, str):
        _atomic_bytes(identity_path, prior_identity.encode("utf-8"))
    elif identity_path.exists():
        _durable_unlink(identity_path)
    journal["phase"] = "rolled_back"
    _write_journal(journal_path, journal)
    return {"ok": True, "transaction_id": transaction_id, "phase": "rolled_back", "restored_papers": len(restore_bytes)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("dry-run", "apply", "recover"))
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--transaction-id")
    parser.add_argument("--action", choices=("restore",))
    args = parser.parse_args()
    if args.command == "recover":
        result = recover(args.repo_root, args.transaction_id or "", args.action or "")
    else:
        if args.manifest is None:
            parser.error("--manifest is required for dry-run and apply")
        result = preflight(args.repo_root, args.manifest) if args.command == "dry-run" else apply(args.repo_root, args.manifest)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
