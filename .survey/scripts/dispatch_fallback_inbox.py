#!/usr/bin/env python3
"""Dispatch one eligible immutable fallback envelope through the normal transport.

All external fallback outboxes first converge on `.survey/work-queue/fallback-inbox/`.
This dispatcher is the only component that expands an ingested envelope into the
reusable record bank, Chat inbox, offline seed, or update-worker files.  It runs
inside the same GitHub Actions concurrency group as the survey/update workers,
so Drive and Library recovery cannot race each other on fixed transport files.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import fallback_transport as ft


def move_exact(source: Path, destination_dir: Path) -> Path:
    destination_dir.mkdir(parents=True, exist_ok=True)
    target = destination_dir / source.name
    if target.exists():
        if target.read_bytes() == source.read_bytes():
            source.unlink()
            return target
        raise ValueError(f"destination conflict for {source.name}")
    shutil.move(str(source), str(target))
    return target


def quarantine(source: Path, failed_dir: Path, error: Exception) -> None:
    failed_dir.mkdir(parents=True, exist_ok=True)
    target = failed_dir / source.name
    if target.exists():
        target = failed_dir / f"{source.stem}.duplicate-invalid{source.suffix}"
    shutil.move(str(source), str(target))
    reason = target.with_suffix(target.suffix + ".error.json")
    reason.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source": source.name,
                "error": f"{type(error).__name__}: {error}",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def dispatch(repo_root: Path) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    inbox_dir = repo_root / ft.FALLBACK_INBOX
    archive_dir = repo_root / ft.FALLBACK_ARCHIVE
    failed_dir = repo_root / ft.FALLBACK_FAILED
    inbox_dir.mkdir(parents=True, exist_ok=True)

    deferred: list[dict[str, str]] = []
    invalid: list[str] = []

    for source in sorted(inbox_dir.glob("*.json")):
        try:
            envelope, canonical = ft.parse_envelope(source.read_bytes())
            if canonical != source.read_text(encoding="utf-8"):
                # Keep the immutable GitHub ledger canonical so duplicate checks
                # across Drive/Library do not depend on whitespace/key ordering.
                source.write_text(canonical, encoding="utf-8")

            terminal = ft.terminal_job_id(repo_root, envelope)
            if terminal:
                archived = move_exact(source, archive_dir)
                return {
                    "action": "ack_terminal",
                    "envelope_id": envelope["id"],
                    "job_id": terminal,
                    "archived": str(archived.relative_to(repo_root)),
                    "deferred": deferred,
                    "invalid": invalid,
                }

            ready, reason = ft.dependency_state(repo_root, envelope)
            if not ready:
                deferred.append({"id": envelope["id"], "reason": reason or "dependency"})
                continue

            if ft.is_chat_envelope(envelope) and not ft.chat_transport_settled(repo_root):
                deferred.append({"id": envelope["id"], "reason": "chat transport still processing"})
                continue

            changed = ft.apply_envelope(repo_root, envelope)
            if any(write["path"] == ft.CHAT_INBOX for write in envelope["writes"]):
                # The previous reusable result belongs to the previous inbox.
                # Removing it here lets the current workflow assemble/process the
                # newly dispatched Chat transport in the same Actions run.
                (repo_root / ft.CHAT_RESULT).unlink(missing_ok=True)

            archived = move_exact(source, archive_dir)
            return {
                "action": "dispatched",
                "envelope_id": envelope["id"],
                "changed_paths": changed,
                "archived": str(archived.relative_to(repo_root)),
                "deferred": deferred,
                "invalid": invalid,
            }
        except Exception as exc:
            invalid.append(source.name)
            quarantine(source, failed_dir, exc)
            # Invalid entries never starve valid entries behind them.
            continue

    return {
        "action": "idle",
        "deferred": deferred,
        "invalid": invalid,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = dispatch(args.repo_root)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
