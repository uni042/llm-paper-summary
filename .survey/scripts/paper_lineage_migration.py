#!/usr/bin/env python3
"""Journaled, recoverable path migration for existing paper records."""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import identity_delta  # noqa: E402
import paper_identity  # noqa: E402
import survey  # noqa: E402

JOURNAL_DIR = "survey-state/lineage-migrations"
MAX_ENTRIES = 100
MAX_TOTAL_SOURCE_BYTES = 64 * 1024 * 1024
DURABLE_PHASES = (
    "prepared",
    "target-installed:0",
    "targets-installed",
    "old-stubbed:0",
    "snapshot-replaced",
    "complete",
)


class MigrationError(ValueError):
    pass


class RecoveryConflict(MigrationError):
    pass


def _root() -> Path:
    return survey.repository_root().resolve()


def current_worktree_sha() -> str:
    """Return the checked-out repository commit, never a baked-in release SHA."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", "HEAD"], cwd=_root(),
            check=True, capture_output=True, text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise MigrationError(f"cannot determine current worktree SHA: {exc}") from exc
    sha = result.stdout.strip().lower()
    if not re.fullmatch(r"[0-9a-f]{40}", sha):
        raise MigrationError("git rev-parse returned an invalid current worktree SHA")
    return sha


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def _unb64(value: str) -> bytes:
    return base64.b64decode(value.encode("ascii"), validate=True)


def _atomic_write(path: Path, data: bytes, *, exclusive: bool = False, temp_path: Path | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = temp_path or path.with_name(f".{path.name}.{uuid.uuid4().hex}.tmp")
    created = False
    try:
        fd = os.open(temporary, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        created = True
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        if exclusive:
            try:
                os.link(temporary, path)
            except OSError:
                if os.name != "nt" or path.exists() or path.is_symlink():
                    raise
                os.rename(temporary, path)
            temporary.unlink(missing_ok=True)
        else:
            os.replace(temporary, path)
        temporary = None
    finally:
        if created and temporary is not None:
            temporary.unlink(missing_ok=True)


def _write_journal(path: Path, journal: dict, *, initial: bool = False) -> None:
    data = (json.dumps(journal, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if initial:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    else:
        _atomic_write(path, data)


def _after_phase(_phase: str) -> None:
    """Test seam called only after the phase has been durably journaled."""


def _journal_path(root: Path, transaction_id: str) -> Path:
    if not re.fullmatch(r"[0-9a-f]{32}", transaction_id):
        raise MigrationError("transaction ID must be a 32-character lowercase hex value")
    state_root = survey.ROOT.resolve()
    journal_dir = state_root / JOURNAL_DIR
    if (state_root / "survey-state").is_symlink() or journal_dir.is_symlink():
        raise MigrationError("transaction journal directory must not contain symlinks")
    try:
        journal_dir.resolve(strict=False).relative_to(state_root)
    except ValueError as exc:
        raise MigrationError("transaction journal directory resolves outside survey state") from exc
    return journal_dir / f"{transaction_id}.json"


def find_active_transaction(root: Path | None = None) -> str | None:
    root = root or _root()
    state_root = survey.ROOT.resolve()
    if (state_root / "survey-state").is_symlink():
        raise RecoveryConflict("survey-state directory is a symlink")
    base = state_root / JOURNAL_DIR
    if base.is_symlink():
        raise RecoveryConflict("transaction journal directory is a symlink")
    try:
        base.resolve(strict=False).relative_to(state_root)
    except ValueError as exc:
        raise RecoveryConflict("transaction journal directory resolves outside survey state") from exc
    if not base.exists():
        return None
    active = []
    for path in sorted(base.glob("*.json")):
        try:
            journal = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as exc:
            raise RecoveryConflict(f"unreadable transaction journal: {path}") from exc
        if journal.get("status") == "in_progress":
            active.append(journal.get("transaction_id"))
    if len(active) > 1:
        raise RecoveryConflict("multiple in-progress migration transactions require explicit recovery")
    return active[0] if active else None


def _path(relative: str, field: str, *, must_exist: bool, target: bool = False) -> Path:
    if not isinstance(relative, str) or not relative or "\\" in relative:
        raise MigrationError(f"{field} must be a repository-relative POSIX path")
    parts = relative.split("/")
    if (len(parts) != 4 or parts[0] != "papers" or parts[1] not in survey.PAPER_FAMILIES
            or any(part in ("", ".", "..") for part in parts)
            or not parts[-1].lower().endswith(".md") or parts[-1].lower() == "readme.md"):
        raise MigrationError(f"{field} must match papers/<supported-family>/<lineage>/<file>.md")
    root = _root()
    candidate = root.joinpath(*parts)
    cursor = root
    for part in parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise MigrationError(f"{field} contains a symlink: {relative}")
    resolved = candidate.resolve(strict=must_exist)
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise MigrationError(f"{field} resolves outside the repository") from exc
    if must_exist and (not resolved.is_file() or candidate.is_symlink()):
        raise MigrationError(f"{field} must be a regular file")
    if target and (candidate.exists() or candidate.is_symlink()):
        raise MigrationError(f"target path is occupied: {relative}")
    if target and not candidate.parent.is_dir():
        raise MigrationError(f"target parent must already exist: {candidate.parent}")
    return candidate


def _frontmatter_aliases(meta: dict) -> tuple[str, ...]:
    aliases = {survey.norm_id(meta.get("canonical_id", ""))}
    for key, prefix in (("arxiv_id", "arXiv:"), ("doi", "DOI:"), ("openreview_id", "OpenReview:")):
        if meta.get(key):
            aliases.add(survey.norm_id(prefix + str(meta[key])))
    aliases.discard("")
    return tuple(sorted(aliases))


def _full_aliases(meta: dict) -> set[str]:
    return {survey.norm_id(alias) for alias in paper_identity.record_identifiers(meta)}


def _validate_deltas() -> int:
    """Run the current delta validator with repository-relative paper lookup.

    identity_delta.paper_record historically joins paper paths to survey.ROOT,
    which is the .survey state directory in production. Temporarily adapt that
    lookup here without changing the existing prepare/lookup/validate commands.
    """
    original = identity_delta.paper_record

    def repository_paper_record(relpath: str) -> dict:
        path = _path(relpath, "identity delta path", must_exist=True)
        meta, _ = survey.front(path)
        cid = survey.norm_id(meta["canonical_id"])
        identifiers = {cid}
        for key, prefix in (("arxiv_id", "arXiv:"), ("doi", "DOI:"), ("openreview_id", "OpenReview:")):
            if meta.get(key):
                identifiers.add(survey.norm_id(prefix + str(meta[key])))
        return {"schema_version": 1, "canonical_id": cid, "path": relpath,
                "identifiers": sorted(identifiers)}

    try:
        identity_delta.paper_record = repository_paper_record
        return identity_delta.validate_all()
    finally:
        identity_delta.paper_record = original


def _load_manifest(path: Path) -> dict:
    if path.is_symlink() or not path.is_file():
        raise MigrationError("manifest must be a regular non-symlink file")
    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise MigrationError(f"cannot read manifest: {exc}") from exc
    current_sha = current_worktree_sha()
    if not isinstance(manifest, dict) or manifest.get("source_main_sha") != current_sha:
        raise MigrationError("manifest source_main_sha does not match current worktree SHA")
    entries = manifest.get("entries")
    if not isinstance(entries, list) or not entries:
        raise MigrationError("manifest entries must be a non-empty list")
    if len(entries) > MAX_ENTRIES:
        raise MigrationError(f"manifest is limited to {MAX_ENTRIES} entries per transaction")
    manifest["_validated_source_main_sha"] = current_sha
    return manifest


def _latest_main_checkout_sha() -> str:
    """Require a clean checkout of the most recently fetched origin/main."""
    root = _root()
    head = current_worktree_sha()
    try:
        remote = subprocess.run(
            ["git", "rev-parse", "--verify", "refs/remotes/origin/main"],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout.strip().lower()
        status = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            cwd=root, check=True, capture_output=True, text=True,
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise MigrationError(f"cannot verify latest-main checkout: {exc}") from exc
    if not re.fullmatch(r"[0-9a-f]{40}", remote):
        raise MigrationError("origin/main does not resolve to a commit SHA")
    if head != remote:
        raise MigrationError(
            f"checkout is not the latest fetched origin/main (HEAD={head}, origin/main={remote}); fetch and recreate the isolated worktree"
        )
    if status:
        raise MigrationError("manifest refresh requires a clean isolated checkout")
    return head


def refresh_manifest(manifest_path: Path | str, output_path: Path | str,
                     report_path: Path | str) -> dict:
    """Repin an immutable reviewed manifest while retaining only unchanged papers.

    This does not update paper hashes or identity evidence. Changed or occupied
    entries are emitted in a review report and excluded from the refreshed batch.
    """
    root = _root()
    current_sha = _latest_main_checkout_sha()
    source_input = Path(manifest_path)
    destination_input = Path(output_path)
    report_input = Path(report_path)
    if source_input.is_symlink() or not source_input.is_file():
        raise MigrationError("manifest must be a regular non-symlink file")
    if destination_input.is_symlink() or report_input.is_symlink():
        raise MigrationError("output paths must not be symlinks")
    source_path = source_input.resolve(strict=True)
    destination_path = destination_input.resolve()
    report_file = report_input.resolve()
    if source_path == destination_path or source_path == report_file or destination_path == report_file:
        raise MigrationError("input manifest, refreshed manifest, and report must use distinct paths")
    for path, label in ((destination_path, "refreshed manifest"), (report_file, "refresh report")):
        try:
            path.relative_to(root)
        except ValueError:
            pass
        else:
            raise MigrationError(f"{label} must be outside the repository to avoid accidental staging")
        if path.exists() or path.is_symlink():
            raise MigrationError(f"{label} already exists: {path}")
        if not path.parent.is_dir():
            raise MigrationError(f"{label} parent directory does not exist: {path.parent}")
    try:
        original = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise MigrationError(f"cannot read manifest: {exc}") from exc
    entries = original.get("entries") if isinstance(original, dict) else None
    if not isinstance(entries, list) or not entries or len(entries) > MAX_ENTRIES:
        raise MigrationError(f"manifest entries must contain between 1 and {MAX_ENTRIES} items")
    if not re.fullmatch(r"[0-9a-f]{40}", str(original.get("source_main_sha", "")).lower()):
        raise MigrationError("original manifest source_main_sha must be a 40-character commit SHA")
    state_path = survey.ROOT / "survey-state/paper-identity-index.json"
    if state_path.is_symlink() or not state_path.is_file():
        raise MigrationError("format-3 identity snapshot must be a regular file")
    try:
        snapshot = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        raise MigrationError(f"identity snapshot is invalid: {exc}") from exc
    if snapshot.get("schema_version") != 3:
        raise MigrationError("identity snapshot must use schema version 3")

    retained: list[dict] = []
    rejected: list[dict] = []
    retained_bytes = 0
    for index, item in enumerate(entries):
        cid = item.get("canonical_id") if isinstance(item, dict) else None
        old_rel = item.get("old_path") if isinstance(item, dict) else None
        new_rel = item.get("new_path") if isinstance(item, dict) else None
        context = {"entry": index, "canonical_id": cid, "old_path": old_rel,
                   "new_path": new_rel}
        try:
            if not isinstance(item, dict):
                raise MigrationError("entry must be an object")
            old_path = _path(old_rel, f"entry {index} old_path", must_exist=True)
            new_path = _path(new_rel, f"entry {index} new_path", must_exist=False, target=True)
            source = old_path.read_bytes()
            source_hash = _sha(source)
            if item.get("expected_sha256") != source_hash:
                raise MigrationError("source paper bytes changed; re-review this entry")
            meta, _body = survey.front(old_path)
            normalized_cid = survey.norm_id(cid or "")
            if not normalized_cid or survey.norm_id(meta.get("canonical_id", "")) != normalized_cid:
                raise MigrationError("canonical ID changed; re-review this entry")
            raw_aliases = item.get("aliases")
            if not isinstance(raw_aliases, list) or not all(isinstance(value, str) for value in raw_aliases):
                raise MigrationError("manifest aliases must be a string list")
            aliases = tuple(sorted(survey.norm_id(value) for value in raw_aliases))
            direct_aliases = _frontmatter_aliases(meta)
            if not aliases or len(set(aliases)) != len(aliases) or aliases != direct_aliases:
                raise MigrationError("frontmatter aliases changed; re-review this entry")
            record = snapshot.get("papers", {}).get(normalized_cid)
            if (not record or record.get("path") != old_rel
                    or record.get("source_hash") != source_hash
                    or tuple(sorted(record.get("identifiers", []))) != aliases):
                raise MigrationError("identity snapshot changed; re-review this entry")
            if any(snapshot.get("identifier_to_canonical", {}).get(alias) != normalized_cid
                   for alias in aliases):
                raise MigrationError("identity alias mapping changed; re-review this entry")
            retained_bytes += len(source)
            retained.append(dict(item))
        except (MigrationError, OSError, ValueError, TypeError) as exc:
            rejected.append({**context, "reason": str(exc)})
    if retained_bytes > MAX_TOTAL_SOURCE_BYTES:
        raise MigrationError(f"retained papers exceed {MAX_TOTAL_SOURCE_BYTES} source bytes")
    report = {
        "schema_version": 1,
        "original_source_main_sha": original.get("source_main_sha"),
        "refreshed_source_main_sha": current_sha,
        "retained_count": len(retained),
        "rejected_count": len(rejected),
        "rejected_entries": rejected,
        "note": "Rejected entries require renewed identity/source review; hashes were never refreshed automatically.",
    }
    _atomic_write(report_file, (json.dumps(report, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), exclusive=True)
    if not retained:
        return {"refreshed": False, "source_main_sha": current_sha,
                "retained_count": 0, "rejected_count": len(rejected),
                "manifest": None, "report": str(report_file)}

    refreshed = dict(original)
    refreshed["source_main_sha"] = current_sha
    refreshed["entries"] = retained
    _atomic_write(destination_path, (json.dumps(refreshed, ensure_ascii=False, indent=2) + "\n").encode("utf-8"), exclusive=True)
    return {"refreshed": True, "source_main_sha": current_sha,
            "retained_count": len(retained), "rejected_count": len(rejected),
            "manifest": str(destination_path), "report": str(report_file)}


def _preflight(manifest_path: Path) -> dict:
    manifest = _load_manifest(manifest_path)
    root = _root()
    state_path = survey.ROOT / "survey-state/paper-identity-index.json"
    if state_path.is_symlink() or not state_path.is_file():
        raise MigrationError("format-3 identity snapshot must be a regular file")
    snapshot_before = state_path.read_bytes()
    try:
        snapshot = json.loads(snapshot_before.decode("utf-8"))
    except (UnicodeDecodeError, ValueError) as exc:
        raise MigrationError(f"identity snapshot is invalid JSON: {exc}") from exc
    if snapshot.get("schema_version") != 3:
        raise MigrationError("identity snapshot must use schema version 3")
    _validate_deltas()

    planned, moved_stubs, seen_old, seen_new, seen_aliases, seen_ids = [], [], set(), set(), {}, set()
    deltas = identity_delta.read_delta_files()
    for index, item in enumerate(manifest["entries"]):
        if not isinstance(item, dict):
            raise MigrationError(f"entry {index} must be an object")
        old_rel, new_rel = item.get("old_path"), item.get("new_path")
        old_path = _path(old_rel, f"entry {index} old_path", must_exist=True)
        new_path = _path(new_rel, f"entry {index} new_path", must_exist=False, target=True)
        old_key = os.path.normcase(old_rel)
        new_key = os.path.normcase(new_rel)
        if old_key == new_key or old_key in seen_old or new_key in seen_new:
            raise MigrationError(f"entry {index} repeats or aliases a path")
        seen_old.add(old_key); seen_new.add(new_key)
        if old_path.stat().st_dev != new_path.parent.stat().st_dev:
            raise MigrationError(f"entry {index} source and target must be on the same filesystem")
        source = old_path.read_bytes()
        source_hash = _sha(source)
        if item.get("expected_sha256") != source_hash:
            raise MigrationError(f"entry {index} source hash mismatch")
        meta, _body = survey.front(old_path)
        cid = survey.norm_id(item.get("canonical_id", ""))
        if not cid or survey.norm_id(meta.get("canonical_id", "")) != cid:
            raise MigrationError(f"entry {index} canonical ID mismatch")
        if cid in seen_ids:
            raise MigrationError(f"entry {index} duplicates a canonical ID")
        seen_ids.add(cid)
        aliases = tuple(sorted(survey.norm_id(value) for value in item.get("aliases", [])))
        direct_aliases = _frontmatter_aliases(meta)
        if not aliases or len(set(aliases)) != len(aliases) or aliases != direct_aliases:
            raise MigrationError(f"entry {index} alias list must exactly match frontmatter aliases")
        full_aliases = _full_aliases(meta)
        snapshot_record = snapshot.get("papers", {}).get(cid)
        if not snapshot_record or snapshot_record.get("path") != old_rel:
            raise MigrationError(f"entry {index} snapshot path does not match old_path")
        if snapshot_record.get("source_hash") != source_hash:
            raise MigrationError(f"entry {index} snapshot source hash mismatch")
        if tuple(sorted(snapshot_record.get("identifiers", []))) != aliases:
            raise MigrationError(f"entry {index} snapshot aliases mismatch")
        for alias in aliases:
            if snapshot.get("identifier_to_canonical", {}).get(alias) != cid:
                raise MigrationError(f"entry {index} snapshot alias conflict: {alias}")
            previous = seen_aliases.get(alias)
            if previous and previous != cid:
                raise MigrationError(f"entry {index} manifest alias collision: {alias}")
            seen_aliases[alias] = cid
        for delta in deltas:
            if delta.get("canonical_id") == cid:
                raise MigrationError(f"entry {index} has a pending identity delta for {cid}; compact first")
            if full_aliases.intersection(delta.get("identifiers", [])):
                raise MigrationError(f"entry {index} aliases conflict with a pending identity delta")
        if not set(aliases).issubset(full_aliases):
            raise MigrationError(f"entry {index} aliases are inconsistent with identity normalization")
        stub = f"# Moved\n\nThis paper record moved to {new_rel}.\n".encode("utf-8")
        moved_stubs.append(old_rel.split("/", 2)[-1])
        planned.append({
            "old_rel": old_rel, "new_rel": new_rel, "canonical_id": cid,
            "source": source, "source_hash": source_hash, "stub": stub,
            "old_path": old_path, "new_path": new_path,
        })
    if sum(len(item["source"]) for item in planned) > MAX_TOTAL_SOURCE_BYTES:
        raise MigrationError(f"transaction exceeds {MAX_TOTAL_SOURCE_BYTES} source bytes")

    records = survey.papers()
    existing_moved_stubs = set(snapshot.get("ignored_moved_stubs", []))
    seen_moved_stubs = set()
    paths_by_moved_suffix: dict[str, list[str]] = {}
    for record in records:
        paths_by_moved_suffix.setdefault(record["path"].split("/", 2)[-1], []).append(record["path"])
    for item in planned:
        suffix = item["old_rel"].split("/", 2)[-1]
        if suffix in existing_moved_stubs or suffix in seen_moved_stubs:
            raise MigrationError(f"moved-stub registration suffix is already occupied: {suffix}")
        seen_moved_stubs.add(suffix)
        other_paths = [path for path in paths_by_moved_suffix.get(suffix, []) if path != item["old_rel"]]
        if other_paths:
            raise MigrationError(f"moved-stub registration collides with paper path: {other_paths[0]}")

    seen_new_suffixes = set()
    for item in planned:
        new_suffix = item["new_rel"].split("/", 2)[-1]
        if new_suffix in existing_moved_stubs | seen_moved_stubs:
            raise MigrationError(f"target suffix conflicts with moved-stub registration: {new_suffix}")
        if new_suffix in seen_new_suffixes:
            raise MigrationError(f"batch target suffix is duplicated: {new_suffix}")
        seen_new_suffixes.add(new_suffix)
        other_paths = [path for path in paths_by_moved_suffix.get(new_suffix, [])
                       if path != item["old_rel"]]
        if other_paths:
            raise MigrationError(f"target suffix collides with current paper path: {other_paths[0]}")

    # Check the complete current inventory, including aliases not represented in the
    # compact snapshot (for example aliases inferred from source URLs).
    owner = {}
    for record in survey.papers():
        for alias in _full_aliases(record.get("meta", {})):
            prior = owner.get(alias)
            if prior and prior != record["canonical_id"]:
                raise MigrationError(f"current paper inventory has an alias collision: {alias}")
            owner[alias] = record["canonical_id"]
    for item in planned:
        for alias in _full_aliases(survey.front(item["old_path"])[0]):
            prior = owner.get(alias)
            if prior and prior != item["canonical_id"]:
                raise MigrationError(f"entry aliases conflict with current paper inventory: {alias}")

    by_path = {record["path"]: record for record in records}
    for item in planned:
        record = by_path.get(item["old_rel"])
        if not record or record["canonical_id"] != item["canonical_id"] or record["source_hash"] != item["source_hash"]:
            raise MigrationError(f"paper inventory does not match entry {item['old_rel']}")
        record["path"] = item["new_rel"]
    # survey.papers() orders records by their current filesystem paths. Moving
    # papers can change that order, so mirror the post-move order before serializing
    # the planned identity snapshot. Otherwise apply regenerates equivalent data
    # in a different insertion order and rejects its own preflight plan.
    records.sort(key=lambda record: record["path"])
    staged_snapshot = dict(snapshot)
    staged_snapshot["ignored_moved_stubs"] = sorted(set(snapshot.get("ignored_moved_stubs", [])) | set(moved_stubs))
    original_read = survey.read
    try:
        survey.read = lambda path, default=None: staged_snapshot if path == survey.STATE + "paper-identity-index.json" else original_read(path, default)
        snapshot_after = survey.identity(records)
    finally:
        survey.read = original_read
    snapshot_after_bytes = (json.dumps(snapshot_after, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8")
    return {
        "root": root, "state_path": state_path, "snapshot_before": snapshot_before,
        "snapshot_after": snapshot_after_bytes, "entries": planned,
        "source_main_sha": manifest["_validated_source_main_sha"],
    }


def _journal_base(plan: dict, transaction_id: str) -> dict:
    entries = []
    for index, item in enumerate(plan["entries"]):
        target_temp = item["new_path"].with_name(f".{item['new_path'].name}.{transaction_id}.target.tmp")
        stub_temp = item["old_path"].with_name(f".{item['old_path'].name}.{transaction_id}.stub.tmp")
        entries.append({
            "old_path": item["old_rel"], "new_path": item["new_rel"],
            "canonical_id": item["canonical_id"],
            "source_bytes": _b64(item["source"]), "source_sha256": item["source_hash"],
            "stub_bytes": _b64(item["stub"]), "stub_sha256": _sha(item["stub"]),
            "target_temp": target_temp.relative_to(_root()).as_posix(),
            "stub_temp": stub_temp.relative_to(_root()).as_posix(),
        })
    snapshot_temp = plan["state_path"].with_name(f".paper-identity-index.json.{transaction_id}.snapshot.tmp")
    return {
        "schema_version": 1,
        "transaction_id": transaction_id,
        "status": "in_progress",
        "phase": "prepared",
        "source_main_sha": plan["source_main_sha"],
        "snapshot_path": plan["state_path"].relative_to(survey.ROOT).as_posix(),
        "snapshot_before": _b64(plan["snapshot_before"]),
        "snapshot_before_sha256": _sha(plan["snapshot_before"]),
        "snapshot_after": _b64(plan["snapshot_after"]),
        "snapshot_after_sha256": _sha(plan["snapshot_after"]),
        "snapshot_temp": snapshot_temp.relative_to(survey.ROOT).as_posix(),
        "entries": entries,
    }


def apply_manifest(manifest_path: Path | str) -> dict:
    manifest_path = Path(manifest_path).resolve(strict=True)
    if find_active_transaction(_root()):
        raise RecoveryConflict("an earlier lineage migration is in progress; recover it first")
    plan = _preflight(manifest_path)
    if current_worktree_sha() != plan["source_main_sha"]:
        raise MigrationError("current worktree SHA changed after manifest validation")
    transaction_id = uuid.uuid4().hex
    journal_path = _journal_path(plan["root"], transaction_id)
    journal_path.parent.mkdir(parents=True, exist_ok=True)
    journal = _journal_base(plan, transaction_id)
    _write_journal(journal_path, journal, initial=True)
    _after_phase("prepared")
    try:
        if plan["state_path"].read_bytes() != plan["snapshot_before"]:
            raise MigrationError("identity snapshot changed after preflight")
        for index, item in enumerate(plan["entries"]):
            _path(item["new_rel"], f"entry {index} new_path", must_exist=False, target=True)
            if item["old_path"].read_bytes() != item["source"]:
                raise MigrationError(f"source changed after preflight: {item['old_rel']}")
            journal_entry = journal["entries"][index]
            target_temp = _root() / journal_entry["target_temp"]
            _atomic_write(item["new_path"], item["source"], exclusive=True, temp_path=target_temp)
            journal["phase"] = f"target-installed:{index}"
            _write_journal(journal_path, journal)
            _after_phase(journal["phase"])
        journal["phase"] = "targets-installed"
        _write_journal(journal_path, journal)
        _after_phase(journal["phase"])

        for index, item in enumerate(plan["entries"]):
            _path(item["old_rel"], f"entry {index} old_path", must_exist=True)
            if item["old_path"].read_bytes() != item["source"]:
                raise MigrationError(f"source changed before stub replacement: {item['old_rel']}")
            journal_entry = journal["entries"][index]
            stub_temp = _root() / journal_entry["stub_temp"]
            _atomic_write(item["old_path"], item["stub"], temp_path=stub_temp)
            journal["phase"] = f"old-stubbed:{index}"
            _write_journal(journal_path, journal)
            _after_phase(journal["phase"])

        staged = json.loads(plan["snapshot_before"].decode("utf-8"))
        staged["ignored_moved_stubs"] = sorted(set(staged.get("ignored_moved_stubs", [])) |
                                               {item["old_rel"].split("/", 2)[-1] for item in plan["entries"]})
        original_read = survey.read
        try:
            survey.read = lambda path, default=None: staged if path == survey.STATE + "paper-identity-index.json" else original_read(path, default)
            generated = survey.identity(survey.papers())
        finally:
            survey.read = original_read
        generated_bytes = (json.dumps(generated, ensure_ascii=False, indent=2, default=str) + "\n").encode("utf-8")
        if generated_bytes != plan["snapshot_after"]:
            raise MigrationError("regenerated snapshot differs from preflight plan")
        if plan["state_path"].read_bytes() != plan["snapshot_before"]:
            raise MigrationError("identity snapshot changed during migration")
        if plan["state_path"].is_symlink():
            raise MigrationError("identity snapshot became a symlink during migration")
        snapshot_temp = survey.ROOT / journal["snapshot_temp"]
        _atomic_write(plan["state_path"], generated_bytes, temp_path=snapshot_temp)
        journal["phase"] = "snapshot-replaced"
        _write_journal(journal_path, journal)
        _after_phase(journal["phase"])
        journal["status"] = "complete"
        journal["phase"] = "complete"
        _write_journal(journal_path, journal)
        _after_phase(journal["phase"])
    except Exception as exc:
        try:
            recover(plan["root"], transaction_id, "rollback")
        except Exception as rollback_exc:
            raise RecoveryConflict(f"apply failed ({exc}); rollback requires recovery: {rollback_exc}") from exc
        raise MigrationError(f"apply failed and was rolled back: {exc}") from exc
    return {"transaction_id": transaction_id, "status": "complete", "entry_count": len(plan["entries"])}


def _validated_journal_paths(journal: dict, transaction_id: str) -> tuple[Path, Path, list[tuple[Path, Path, Path, Path]]]:
    """Validate journal paths against paths derived only from the transaction ID and paper paths."""
    root = _root()
    snapshot_rel = "survey-state/paper-identity-index.json"
    if journal.get("snapshot_path") != snapshot_rel:
        raise RecoveryConflict("journal snapshot path does not match the fixed identity snapshot")
    expected_snapshot_temp = f"survey-state/.paper-identity-index.json.{transaction_id}.snapshot.tmp"
    if journal.get("snapshot_temp") != expected_snapshot_temp:
        raise RecoveryConflict("journal snapshot staging path does not match transaction")
    entries = journal.get("entries")
    if not isinstance(entries, list) or not entries or len(entries) > MAX_ENTRIES:
        raise RecoveryConflict("journal entries must be a bounded non-empty list")
    resolved = []
    for index, item in enumerate(entries):
        if not isinstance(item, dict):
            raise RecoveryConflict(f"journal entry {index} is not an object")
        old_rel, new_rel = item.get("old_path"), item.get("new_path")
        old_path = _path(old_rel, f"journal entry {index} old_path", must_exist=False)
        new_path = _path(new_rel, f"journal entry {index} new_path", must_exist=False)
        expected_target_temp = new_path.with_name(f".{new_path.name}.{transaction_id}.target.tmp")
        expected_stub_temp = old_path.with_name(f".{old_path.name}.{transaction_id}.stub.tmp")
        expected_target_rel = expected_target_temp.relative_to(root).as_posix()
        expected_stub_rel = expected_stub_temp.relative_to(root).as_posix()
        if item.get("target_temp") != expected_target_rel:
            raise RecoveryConflict(f"journal target staging path mismatch at entry {index}")
        if item.get("stub_temp") != expected_stub_rel:
            raise RecoveryConflict(f"journal stub staging path mismatch at entry {index}")
        resolved.append((old_path, new_path, expected_target_temp, expected_stub_temp))
    snapshot_path = survey.ROOT / snapshot_rel
    snapshot_temp = survey.ROOT / expected_snapshot_temp
    if (survey.ROOT / "survey-state").is_symlink():
        raise RecoveryConflict("survey-state directory is a symlink")
    return snapshot_path, snapshot_temp, resolved


def recover(root: Path | str, transaction_id: str, action: str) -> dict:
    if action != "rollback":
        raise MigrationError("only recovery action 'rollback' is supported")
    root = Path(root).resolve()
    journal_path = _journal_path(root, transaction_id)
    if not journal_path.is_file() or journal_path.is_symlink():
        raise MigrationError("transaction journal not found as a regular file")
    journal = json.loads(journal_path.read_text(encoding="utf-8"))
    current_sha = current_worktree_sha()
    if (journal.get("transaction_id") != transaction_id
            or journal.get("source_main_sha") != current_sha):
        raise RecoveryConflict("transaction journal identity or source pin mismatch")
    snapshot_path, snapshot_temp, validated_paths = _validated_journal_paths(journal, transaction_id)
    if snapshot_path.is_symlink() or not snapshot_path.is_file():
        raise RecoveryConflict("identity snapshot is not a regular file")
    before = _unb64(journal["snapshot_before"])
    after = _unb64(journal["snapshot_after"])
    if _sha(before) != journal["snapshot_before_sha256"] or _sha(after) != journal["snapshot_after_sha256"]:
        raise RecoveryConflict("transaction journal snapshot bytes failed hash verification")
    current_snapshot = snapshot_path.read_bytes()
    if current_snapshot not in (before, after):
        raise RecoveryConflict("snapshot bytes differ from both transaction versions")
    resolved_entries = []
    staged_paths = []
    for item, (old_path, new_path, target_temp, stub_temp) in zip(journal["entries"], validated_paths):
        source = _unb64(item["source_bytes"]); stub = _unb64(item["stub_bytes"])
        if _sha(source) != item["source_sha256"] or _sha(stub) != item["stub_sha256"]:
            raise RecoveryConflict("transaction journal paper bytes failed hash verification")
        old_value = old_path.read_bytes() if old_path.exists() else None
        new_value = new_path.read_bytes() if new_path.exists() else None
        if old_value not in (None, source, stub) or new_value not in (None, source):
            raise RecoveryConflict(f"paper bytes differ from transaction hashes: {item['old_path']} / {item['new_path']}")
        resolved_entries.append((old_path, new_path, source, stub, old_value, new_value))
        staged_paths.extend(((target_temp, source), (stub_temp, stub)))
    staged_paths.append((snapshot_temp, after))
    for staged_path, expected in staged_paths:
        if staged_path.is_symlink():
            raise RecoveryConflict(f"transaction staging path is a symlink: {staged_path}")
        if staged_path.exists() and staged_path.read_bytes() != expected:
            raise RecoveryConflict(f"transaction staging bytes differ from expected hash: {staged_path}")

    # Restore source paths before touching snapshots or target copies. If any write
    # fails, all remaining target copies are still available as recovery sources.
    for old_path, _new_path, source, _stub, old_value, _new_value in resolved_entries:
        if old_value != source:
            _atomic_write(old_path, source)
            if old_path.read_bytes() != source:
                raise RecoveryConflict(f"could not verify restored source bytes: {old_path}")
    if current_snapshot == after:
        _atomic_write(snapshot_path, before)
        if snapshot_path.read_bytes() != before:
            raise RecoveryConflict("restored snapshot bytes failed verification")
    for _old_path, new_path, source, _stub, _old_value, new_value in resolved_entries:
        if new_value == source:
            # The source path was restored and verified above, so this is now a
            # duplicate, never the only remaining source copy.
            if new_path.read_bytes() != source:
                raise RecoveryConflict(f"target changed during rollback: {new_path}")
            new_path.unlink()
    for staged_path, expected in staged_paths:
        if staged_path.exists():
            if staged_path.read_bytes() != expected:
                raise RecoveryConflict(f"transaction staging file changed during rollback: {staged_path}")
            staged_path.unlink()
    journal["status"] = "rolled_back"
    journal["phase"] = "rolled_back"
    _write_journal(journal_path, journal)
    return {"transaction_id": transaction_id, "status": "rolled_back"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    dry = sub.add_parser("dry-run")
    dry.add_argument("--manifest", required=True)
    apply = sub.add_parser("apply")
    apply.add_argument("--manifest", required=True)
    refresh = sub.add_parser("refresh-manifest")
    refresh.add_argument("--manifest", required=True, help="immutable reviewed source manifest")
    refresh.add_argument("--output", required=True, help="new refreshed manifest path")
    refresh.add_argument("--report", required=True, help="rejected-entry report path")
    recover_parser = sub.add_parser("recover")
    recover_parser.add_argument("--transaction", required=True)
    recover_parser.add_argument("--action", choices=("rollback",), required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "dry-run":
            plan = _preflight(Path(args.manifest).resolve(strict=True))
            result = {"valid": True, "entry_count": len(plan["entries"]),
                      "snapshot_sha256": _sha(plan["snapshot_after"])}
        elif args.command == "apply":
            result = apply_manifest(args.manifest)
        elif args.command == "refresh-manifest":
            result = refresh_manifest(args.manifest, args.output, args.report)
        else:
            result = recover(_root(), args.transaction, args.action)
        print(json.dumps(result, ensure_ascii=False))
        return 0
    except Exception as exc:
        print(f"{type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

