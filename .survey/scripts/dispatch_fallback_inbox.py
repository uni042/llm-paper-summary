#!/usr/bin/env python3
"""Dispatch eligible fallback envelopes through the current workflow-v10 transport.

Research/Audit record bundles are converted directly into attempt-specific immutable
descriptors by ``replay_record_fallback``. The CLI drains multiple record bundles per
invocation so a temporary Library/GitHub transport outage does not take hours to recover.
The Python ``dispatch()`` API remains single-item by default for backwards compatibility.
Historical bundles containing the retired reusable ``chat-inbox.json`` remain readable,
but replay never recreates that fixed transport. Non-record envelopes keep their
single-dispatch semantics because some generic routes target mutable singleton inputs.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any

import fallback_transport as ft
import replay_record_fallback as record_replay

DEFAULT_DISPATCH_MAX_ITEMS = 1
DEFAULT_CLI_MAX_ITEMS = 50


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


def _is_record_fallback(value: dict[str, Any]) -> bool:
    """Route both current record bundles and incomplete legacy bundles to strict replay.

    A damaged historical Research/Audit envelope can retain only the retired
    ``chat-inbox.json`` write after partial loss. Treating that as a generic fallback
    would recreate the retired fixed transport. Strict record replay instead validates
    the five-slot invariant and quarantines the malformed envelope.
    """
    if record_replay.is_record_bundle(value):
        return True
    if value.get("kind") not in {"research", "audit"} and value.get("origin") != "claimed_worker":
        return False
    for write in value.get("writes") or []:
        if isinstance(write, dict) and write.get("path") == record_replay.CHAT_INBOX:
            return True
    return False


def _append_changed(target: list[str], seen: set[str], paths: Any) -> None:
    for path in paths or []:
        text = str(path)
        if text and text not in seen:
            seen.add(text)
            target.append(text)


def _batch_result(
    processed: list[dict[str, Any]],
    changed_paths: list[str],
    deferred: list[dict[str, str]],
    invalid: list[str],
) -> dict[str, Any]:
    if not processed:
        return {
            "action": "idle",
            "processed_count": 0,
            "processed": [],
            "changed_paths": changed_paths,
            "deferred": deferred,
            "invalid": invalid,
        }

    # Preserve the legacy top-level action expected by existing callers. When at least
    # one envelope created new work the invocation is a dispatch; otherwise every
    # processed record was an already-terminal acknowledgement.
    action = "dispatched" if any(row.get("action") == "dispatched" for row in processed) else "ack_terminal"
    first = processed[0]
    result: dict[str, Any] = {
        "action": action,
        "processed_count": len(processed),
        "processed": processed,
        "changed_paths": changed_paths,
        "deferred": deferred,
        "invalid": invalid,
        # Keep the historical single-item fields available for consumers that have not
        # migrated to ``processed`` yet.
        "envelope_id": first.get("envelope_id"),
        "archived": first.get("archived"),
    }
    for key in ("job_id", "descriptor", "record_bank"):
        if first.get(key) is not None:
            result[key] = first[key]
    return result


def dispatch(repo_root: Path, *, max_items: int = DEFAULT_DISPATCH_MAX_ITEMS) -> dict[str, Any]:
    if max_items < 1:
        raise ValueError("max_items must be >= 1")

    repo_root = repo_root.resolve()
    inbox_dir = repo_root / ft.FALLBACK_INBOX
    archive_dir = repo_root / ft.FALLBACK_ARCHIVE
    failed_dir = repo_root / ft.FALLBACK_FAILED
    inbox_dir.mkdir(parents=True, exist_ok=True)

    deferred: list[dict[str, str]] = []
    invalid: list[str] = []
    processed: list[dict[str, Any]] = []
    changed_paths: list[str] = []
    changed_seen: set[str] = set()
    generic_dispatched = False

    # Take a stable snapshot. A deferred entry is inspected at most once per invocation,
    # so it cannot spin or starve eligible envelopes later in the directory.
    for source in sorted(inbox_dir.glob("*.json")):
        if len(processed) >= max_items:
            break
        try:
            raw_object = _read_raw_object(source)
            if _is_record_fallback(raw_object):
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
                public_action = "ack_terminal" if replay["action"] == "ack_terminal" else "dispatched"
                row: dict[str, Any] = {
                    "action": public_action,
                    "envelope_id": raw_object.get("id"),
                    "job_id": replay.get("job_id"),
                    "archived": str(archived.relative_to(repo_root)),
                    "changed_paths": replay.get("changed_paths") or [],
                }
                if public_action == "dispatched":
                    row["descriptor"] = replay.get("descriptor")
                    row["record_bank"] = replay.get("record_bank")
                processed.append(row)
                _append_changed(changed_paths, changed_seen, row["changed_paths"])
                continue

            # Generic envelopes can target mutable singleton inputs. Preserve the old
            # one-at-a-time behavior for that route while still allowing record bundles
            # later in the same snapshot to drain.
            if generic_dispatched:
                deferred.append(
                    {
                        "id": str(raw_object.get("id") or source.stem),
                        "reason": "another generic fallback was already dispatched in this invocation",
                    }
                )
                continue

            envelope, canonical = ft.parse_envelope(source.read_bytes())
            if canonical != source.read_text(encoding="utf-8"):
                # Keep the immutable GitHub ledger canonical so duplicate checks do
                # not depend on whitespace/key ordering.
                source.write_text(canonical, encoding="utf-8")
            changed = ft.apply_envelope(repo_root, envelope)
            archived = move_exact(source, archive_dir)
            row = {
                "action": "dispatched",
                "envelope_id": envelope["id"],
                "changed_paths": changed,
                "archived": str(archived.relative_to(repo_root)),
            }
            processed.append(row)
            generic_dispatched = True
            _append_changed(changed_paths, changed_seen, changed)
        except Exception as exc:
            invalid.append(source.name)
            quarantine(source, failed_dir, exc)
            # Invalid entries never starve valid entries behind them.
            continue

    return _batch_result(processed, changed_paths, deferred, invalid)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-items", type=int, default=DEFAULT_CLI_MAX_ITEMS)
    args = parser.parse_args()
    result = dispatch(args.repo_root, max_items=args.max_items)
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
