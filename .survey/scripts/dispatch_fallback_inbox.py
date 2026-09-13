#!/usr/bin/env python3
"""Dispatch one eligible fallback envelope through the current workflow-v10 transport.

Research/Audit record bundles are converted directly into an attempt-specific
immutable descriptor by ``replay_record_fallback``. Historical bundles containing
the retired reusable ``chat-inbox.json`` remain readable, but replay never recreates
that fixed transport. Non-record envelopes use the generic allowlisted transport for
offline seeds, lightweight queue requests, and update-worker inputs.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import fallback_transport as ft
import replay_record_fallback as record_replay


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


def _read_raw_object(source: Path) -> dict[str, Any]:
    value = json.loads(source.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("fallback envelope root must be an object")
    return value


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
            raw_object = _read_raw_object(source)
            if record_replay.is_record_bundle(raw_object):
                replay = record_replay.materialize(repo_root, raw_object)
                if replay["action"] == "deferred":
                    deferred.append(
                        {
                            "id": str(raw_object.get("id") or source.stem),
                            "reason": str(replay.get("reason") or "record replay deferred"),
                        }
                    )
                    continue
                archived = move_exact(source, archive_dir)
                if replay["action"] == "ack_terminal":
                    return {
                        "action": "ack_terminal",
                        "envelope_id": raw_object.get("id"),
                        "job_id": replay.get("job_id"),
                        "archived": str(archived.relative_to(repo_root)),
                        "changed_paths": replay.get("changed_paths") or [],
                        "deferred": deferred,
                        "invalid": invalid,
                    }
                return {
                    "action": "dispatched",
                    "envelope_id": raw_object.get("id"),
                    "job_id": replay.get("job_id"),
                    "descriptor": replay.get("descriptor"),
                    "record_bank": replay.get("record_bank"),
                    "changed_paths": replay.get("changed_paths") or [],
                    "archived": str(archived.relative_to(repo_root)),
                    "deferred": deferred,
                    "invalid": invalid,
                }

            envelope, canonical = ft.parse_envelope(source.read_bytes())
            if canonical != source.read_text(encoding="utf-8"):
                # Keep the immutable GitHub ledger canonical so duplicate checks do
                # not depend on whitespace/key ordering.
                source.write_text(canonical, encoding="utf-8")
            changed = ft.apply_envelope(repo_root, envelope)
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
