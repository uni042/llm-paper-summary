#!/usr/bin/env python3
"""Drain replayable Research/Audit fallback records within one helper run.

A reusable record bank is a mutable path, while workflow-v10 descriptors reference
exact historical Git blobs. Therefore a replayed record must be committed before that
bank path is reused. This driver processes one record at a time:

1. replay one eligible Library/GitHub fallback envelope into a safe bank;
2. commit only the transport paths needed to pin those exact slot blobs;
3. synchronously process the immutable descriptor into its paper/job/result;
4. repeat until no further record fallback can make progress.

Publication changes intentionally remain uncommitted so the ordinary survey-helper
finalization can refresh derived indexes once and publish the complete result together.
Generic fallback envelopes are left for the existing serialized dispatcher step.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

import dispatch_fallback_inbox as dispatcher
import fallback_transport as ft
import process_immutable_submission_batch as submission_batch

DEFAULT_MAX_RECORDS = 200
DEFAULT_PARALLELISM = 4


def _relative(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _git(repo_root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=check,
    )


def _ensure_git_identity(repo_root: Path) -> None:
    _git(repo_root, "config", "user.name", "survey-helper[bot]")
    _git(repo_root, "config", "user.email", "survey-helper[bot]@users.noreply.github.com")


def dispatch_one_record(repo_root: Path) -> dict[str, Any]:
    """Replay at most one eligible record fallback, skipping generic/deferred records."""
    repo_root = Path(repo_root).resolve()
    inbox_dir = repo_root / ft.FALLBACK_INBOX
    archive_dir = repo_root / ft.FALLBACK_ARCHIVE
    failed_dir = repo_root / ft.FALLBACK_FAILED
    inbox_dir.mkdir(parents=True, exist_ok=True)

    deferred: list[dict[str, str]] = []
    invalid: list[str] = []

    for source in sorted(inbox_dir.glob("*.json")):
        try:
            raw = dispatcher._read_raw_object(source)
        except Exception as exc:
            invalid.append(source.name)
            dispatcher.quarantine(source, failed_dir, exc)
            continue

        if not dispatcher._is_record_fallback(raw):
            continue

        try:
            replay = dispatcher.record_replay.materialize(repo_root, raw)
        except Exception as exc:
            invalid.append(source.name)
            dispatcher.quarantine(source, failed_dir, exc)
            continue

        if replay.get("action") == "deferred":
            deferred.append(
                {
                    "id": str(raw.get("id") or source.stem),
                    "reason": str(replay.get("reason") or "record replay deferred"),
                }
            )
            continue

        archived = dispatcher.move_exact(source, archive_dir)
        action = "ack_terminal" if replay.get("action") == "ack_terminal" else "materialized"
        row: dict[str, Any] = {
            "action": action,
            "envelope_id": raw.get("id"),
            "job_id": replay.get("job_id"),
            "source": _relative(repo_root, source),
            "archived": _relative(repo_root, archived),
            "changed_paths": list(replay.get("changed_paths") or []),
            "deferred": deferred,
            "invalid": invalid,
        }
        if action == "materialized":
            row["descriptor"] = replay.get("descriptor")
            row["record_bank"] = replay.get("record_bank")
        return row

    return {
        "action": "idle",
        "deferred": deferred,
        "invalid": invalid,
    }


def pin_materialized_record(repo_root: Path, row: dict[str, Any]) -> None:
    """Commit only replay transport paths so bank blobs remain reachable after reuse."""
    repo_root = Path(repo_root).resolve()
    paths: list[str] = []
    for value in [*(row.get("changed_paths") or []), row.get("source"), row.get("archived")]:
        text = str(value or "")
        if text and text not in paths:
            paths.append(text)
    if not paths:
        raise ValueError("materialized fallback has no transport paths to pin")

    _ensure_git_identity(repo_root)
    _git(repo_root, "add", "-A", "--", *paths)
    quiet = _git(repo_root, "diff", "--cached", "--quiet", check=False)
    if quiet.returncode == 0:
        # Existing identical transport can be settled without manufacturing an empty
        # commit; its referenced blobs are already reachable from repository history.
        return
    if quiet.returncode != 1:
        raise RuntimeError("git diff --cached failed while pinning fallback record")

    envelope = str(row.get("envelope_id") or "unknown")
    result = _git(repo_root, "commit", "-m", f"survey-helper: pin fallback record {envelope}", check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "failed to commit fallback transport")


def settle_descriptor(
    repo_root: Path,
    descriptor: str,
    *,
    parallelism: int = DEFAULT_PARALLELISM,
) -> dict[str, Any]:
    """Synchronously publish one pinned immutable descriptor."""
    repo_root = Path(repo_root).resolve()
    with tempfile.TemporaryDirectory(prefix="survey-fallback-effects-") as td:
        return submission_batch.process_batch(
            repo_root,
            [Path(descriptor)],
            Path(td),
            parallelism=parallelism,
        )


def drain(
    repo_root: Path,
    *,
    max_records: int = DEFAULT_MAX_RECORDS,
    parallelism: int = DEFAULT_PARALLELISM,
) -> dict[str, Any]:
    if max_records < 1:
        raise ValueError("max_records must be >= 1")

    repo_root = Path(repo_root).resolve()
    summary: dict[str, Any] = {
        "processed": 0,
        "materialized": 0,
        "settled": 0,
        "ack_terminal": 0,
        "failures": 0,
        "deferred": [],
        "invalid": [],
        "limit_reached": False,
    }

    for _ in range(max_records):
        row = dispatch_one_record(repo_root)
        summary["deferred"] = row.get("deferred") or []
        summary["invalid"].extend(
            name for name in row.get("invalid") or [] if name not in summary["invalid"]
        )
        action = row.get("action")
        if action == "idle":
            break

        summary["processed"] += 1
        if action == "ack_terminal":
            summary["ack_terminal"] += 1
            continue
        if action != "materialized":
            raise RuntimeError(f"unexpected fallback recovery action: {action}")

        summary["materialized"] += 1
        pin_materialized_record(repo_root, row)
        descriptor = row.get("descriptor")
        if not isinstance(descriptor, str) or not descriptor:
            raise ValueError("materialized fallback is missing descriptor path")
        try:
            settled = settle_descriptor(repo_root, descriptor, parallelism=parallelism)
        except Exception as exc:
            summary["fatal_error"] = f"{type(exc).__name__}: {exc}"
            break
        summary["settled"] += 1
        summary["failures"] += int(settled.get("failures", 0) or 0)
    else:
        summary["limit_reached"] = True

    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-records", type=int, default=DEFAULT_MAX_RECORDS)
    parser.add_argument("--parallelism", type=int, default=DEFAULT_PARALLELISM)
    args = parser.parse_args()
    result = drain(
        args.repo_root,
        max_records=args.max_records,
        parallelism=args.parallelism,
    )
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 2 if result.get("fatal_error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
