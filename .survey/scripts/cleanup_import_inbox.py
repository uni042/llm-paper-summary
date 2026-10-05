#!/usr/bin/env python3
"""Recover or discard stale Library-import failures.

This is intentionally conservative:
- delete malformed/non-contract pending Research junk;
- delete blocked Research copies when the paper is already represented;
- requeue one clean, complete Research retry, then discard a second failure;
- use the existing Discovery recovery helpers first;
- requeue one legacy Discovery failure, then discard a second failure;
- for provider-only gaps, retry when a stronger alias exists and otherwise
  leave a compact tombstone before deleting the bulky blocked payload.

The goal is to keep the durable inbox bounded without silently losing the fact
that a hard failure was discarded.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import process_library_import_inbox as inbox


CLEANUP_RESULTS = inbox.INBOX / "results/cleanup"
PROVIDER_DISCARD_RESULTS = inbox.INBOX / "results/discovery-provider"
RESEARCH_RETRY_PREFIX = "retry-research-"
DISCOVERY_RETRY_PREFIX = "retry-legacy-block-"


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def _safe_retry_name(prefix: str, source: Path) -> str:
    token = hashlib.sha256(source.as_posix().encode("utf-8")).hexdigest()[:12]
    suffix = source.suffix
    stem = source.stem
    max_stem = max(32, 210 - len(prefix) - len(token) - len(suffix))
    return f"{prefix}{token}--{stem[:max_stem]}{suffix}"


def _move_retry(source: Path, target_dir: Path, prefix: str) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / _safe_retry_name(prefix, source)
    if target.exists():
        if target.read_bytes() != source.read_bytes():
            raise RuntimeError(f"retry collision: {target}")
        source.unlink(missing_ok=True)
        return target
    source.replace(target)
    return target


def _research_success_ids(repo_root: Path) -> set[str]:
    out: set[str] = set()
    root = repo_root / inbox.RESULT_RESEARCH
    if not root.is_dir():
        return out
    for path in root.glob("*.json"):
        try:
            payload = inbox.read_json(path)
        except Exception:
            continue
        if str(payload.get("status") or "") not in {"imported", "already_represented"}:
            continue
        canonical_id = str(payload.get("canonical_id") or "").strip()
        if canonical_id:
            out.add(canonical_id)
    return out


def _record_cleanup(repo_root: Path, source: Path, status: str, detail: dict[str, Any]) -> None:
    """Keep a bounded cleanup audit without replacing old clutter with new clutter."""
    target = repo_root / CLEANUP_RESULTS / "latest.json"
    try:
        current = json.loads(target.read_text(encoding="utf-8")) if target.is_file() else {}
    except (json.JSONDecodeError, OSError):
        current = {}
    events = current.get("events")
    if not isinstance(events, list):
        events = []
    events.append(
        {
            "status": status,
            "source_path": inbox.repo_relative(source, repo_root),
            "processed_at": inbox.now(),
            **detail,
        }
    )
    _write_json(
        target,
        {
            "schema_version": 1,
            "artifact_type": "import_cleanup",
            "updated_at": inbox.now(),
            "events": events[-500:],
        },
    )


def cleanup_pending_research_junk(repo_root: Path) -> int:
    root = repo_root / inbox.PENDING_RESEARCH
    if not root.is_dir():
        return 0
    deleted = 0
    for source in sorted(root.iterdir()):
        if not source.is_file() or source.suffix == ".md":
            continue
        preview = source.read_text(encoding="utf-8", errors="replace")[:300]
        _record_cleanup(
            repo_root,
            source,
            "discarded_pending_research_junk",
            {"size_bytes": source.stat().st_size, "preview": preview},
        )
        source.unlink(missing_ok=True)
        deleted += 1
    return deleted


def recover_blocked_research(repo_root: Path) -> dict[str, int]:
    root = repo_root / inbox.BLOCKED_RESEARCH
    pending = repo_root / inbox.PENDING_RESEARCH
    counts = {"stale_deleted": 0, "requeued": 0, "hard_deleted": 0}
    if not root.is_dir():
        return counts

    success_ids = _research_success_ids(repo_root)
    for source in sorted(root.glob("*.md")):
        raw = source.read_text(encoding="utf-8", errors="replace")
        try:
            meta = inbox.parse_frontmatter(raw)
            normalized_raw, normalized_meta = inbox.normalize_research_audit_metadata(raw, meta)
            canonical_id = str(normalized_meta.get("canonical_id") or "").strip()
        except Exception as exc:
            _record_cleanup(
                repo_root,
                source,
                "discarded_blocked_research_invalid",
                {"error": f"{type(exc).__name__}: {exc}"},
            )
            source.unlink(missing_ok=True)
            counts["hard_deleted"] += 1
            continue

        if canonical_id in success_ids:
            _record_cleanup(
                repo_root,
                source,
                "deleted_stale_blocked_research",
                {"canonical_id": canonical_id},
            )
            source.unlink(missing_ok=True)
            counts["stale_deleted"] += 1
            continue

        if source.name.startswith(RESEARCH_RETRY_PREFIX):
            _record_cleanup(
                repo_root,
                source,
                "discarded_research_after_retry",
                {"canonical_id": canonical_id},
            )
            source.unlink(missing_ok=True)
            counts["hard_deleted"] += 1
            continue

        failures = inbox.research_metadata_failures(source, normalized_meta, repo_root)
        if failures:
            _record_cleanup(
                repo_root,
                source,
                "discarded_blocked_research_metadata",
                {"canonical_id": canonical_id, "failures": failures},
            )
            source.unlink(missing_ok=True)
            counts["hard_deleted"] += 1
            continue

        # Do not duplicate the normal importer's expensive identity and quality
        # checks here. A complete blocked artifact gets one bounded retry; the
        # canonical importer then performs identity resolution, normalization and
        # the full quality gate. If it blocks again, the retry-prefix rule above
        # discards it on the next cleanup pass.
        source.write_text(normalized_raw, encoding="utf-8")
        target = _move_retry(source, pending, RESEARCH_RETRY_PREFIX)
        _record_cleanup(
            repo_root,
            target,
            "requeued_blocked_research",
            {"canonical_id": canonical_id, "retry_path": inbox.repo_relative(target, repo_root)},
        )
        counts["requeued"] += 1

    return counts


def _has_retry_evidence(repo_root: Path, source: Path, prefix: str) -> bool:
    patterns = [
        repo_root / inbox.PENDING_DISCOVERY,
        repo_root / inbox.WAITING_DISCOVERY,
        repo_root / inbox.RESULT_DISCOVERY,
    ]
    needle = f"--{source.stem}"
    for root in patterns:
        if not root.is_dir():
            continue
        for path in root.iterdir():
            if path.is_file() and path.name.startswith(prefix) and needle in path.stem:
                return True
    return False


def recover_blocked_discovery(repo_root: Path) -> dict[str, int]:
    counts = {
        "existing_recovery_requeued": 0,
        "legacy_requeued": 0,
        "stale_deleted": 0,
        "hard_deleted": 0,
    }

    counts["existing_recovery_requeued"] += inbox.recover_retryable_precheck_provenance_blocks(repo_root)
    counts["existing_recovery_requeued"] += inbox.recover_candidate_provider_gap_blocks(repo_root)
    inbox.recover_provider_gap_alias_blocks(repo_root)

    blocked = repo_root / inbox.BLOCKED_DISCOVERY
    pending = repo_root / inbox.PENDING_DISCOVERY
    if blocked.is_dir():
        for source in sorted(blocked.glob("*.json")):
            try:
                payload = inbox.read_json(source)
                records = inbox.discovery_records(payload)
                if not records:
                    raise ValueError("empty discovery records")
            except Exception as exc:
                _record_cleanup(
                    repo_root,
                    source,
                    "discarded_blocked_discovery_invalid",
                    {"error": f"{type(exc).__name__}: {exc}"},
                )
                source.unlink(missing_ok=True)
                counts["hard_deleted"] += 1
                continue

            if any(
                _has_retry_evidence(repo_root, source, prefix)
                for prefix in ("retry-precheck-", "retry-provider-gap-", DISCOVERY_RETRY_PREFIX)
            ):
                source.unlink(missing_ok=True)
                counts["stale_deleted"] += 1
                continue

            if source.name.startswith(("retry-precheck-", "retry-provider-gap-", DISCOVERY_RETRY_PREFIX)):
                _record_cleanup(
                    repo_root,
                    source,
                    "discarded_discovery_after_retry",
                    {"record_count": len(records), "run_key": payload.get("run_key")},
                )
                source.unlink(missing_ok=True)
                counts["hard_deleted"] += 1
                continue

            target = _move_retry(source, pending, DISCOVERY_RETRY_PREFIX)
            _record_cleanup(
                repo_root,
                target,
                "requeued_legacy_blocked_discovery",
                {
                    "record_count": len(records),
                    "run_key": payload.get("run_key"),
                    "retry_path": inbox.repo_relative(target, repo_root),
                },
            )
            counts["legacy_requeued"] += 1

    provider = repo_root / inbox.BLOCKED_DISCOVERY_PROVIDER
    if provider.is_dir():
        for source in sorted(provider.glob("*.json")):
            try:
                payload = inbox.read_json(source)
                records = inbox.discovery_records(payload)
            except Exception:
                source.unlink(missing_ok=True)
                counts["hard_deleted"] += 1
                continue

            if _has_retry_evidence(repo_root, source, "retry-provider-alias-"):
                source.unlink(missing_ok=True)
                counts["stale_deleted"] += 1
                continue

            tombstone = repo_root / PROVIDER_DISCARD_RESULTS / f"{source.stem}.json"
            _write_json(
                tombstone,
                {
                    "schema_version": 1,
                    "artifact_type": "discovery_provider_gap",
                    "status": "discarded_unresolved_provider",
                    "source_path": inbox.repo_relative(source, repo_root),
                    "processed_at": inbox.now(),
                    "record_count": len(records),
                    "canonical_ids": [
                        str(record.get("canonical_id") or "").strip()
                        for record in records
                        if str(record.get("canonical_id") or "").strip()
                    ],
                    "titles": [
                        str(record.get("title") or "").strip()
                        for record in records
                        if str(record.get("title") or "").strip()
                    ],
                    "provider_gap_ids": list(payload.get("provider_gap_ids") or []),
                },
            )
            source.unlink(missing_ok=True)
            counts["hard_deleted"] += 1

    return counts


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    summary = {
        "ok": True,
        "processed_at": inbox.now(),
        "pending_research_junk_deleted": cleanup_pending_research_junk(repo_root),
        "research": recover_blocked_research(repo_root),
        "discovery": recover_blocked_discovery(repo_root),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
