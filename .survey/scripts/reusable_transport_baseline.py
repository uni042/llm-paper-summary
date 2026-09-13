#!/usr/bin/env python3
"""Snapshot and restore the fixed reusable Chat transport around fallback replay.

The background helper temporarily maps one fallback envelope onto the legacy fixed
``chat-inbox.json`` transport.  The inbox/payload are transient in that case, and
the fallback result must not be left paired with the original inbox after the
transient inputs are restored.

A baseline result is preserved only when it is structurally paired with the
baseline inbox by ``job_id``.  Existing mismatched results are treated as absent so
this helper cannot perpetuate a previously corrupted inbox/result pair.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

INBOX = Path(".survey/work-queue/submissions/chat-inbox.json")
RESULT = Path(".survey/work-queue/results/chat-inbox.json")
PAYLOAD = Path(".survey/work-queue/payloads/chat-payload.md")
MANIFEST = "manifest.json"


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def _capture(root: Path, rel: Path) -> dict[str, Any]:
    path = root / rel
    if not path.is_file():
        return {"exists": False, "content": None}
    return {"exists": True, "content": path.read_text(encoding="utf-8")}


def _restore_entry(root: Path, rel: Path, entry: Any) -> None:
    path = root / rel
    if not isinstance(entry, dict) or not entry.get("exists"):
        path.unlink(missing_ok=True)
        return
    content = entry.get("content")
    if not isinstance(content, str):
        raise ValueError(f"snapshot content is invalid for {rel.as_posix()}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def _coherent_result_baseline(root: Path) -> dict[str, Any]:
    result_entry = _capture(root, RESULT)
    if not result_entry.get("exists"):
        return result_entry

    inbox = _read_json(root / INBOX)
    result = _read_json(root / RESULT)
    inbox_job = inbox.get("job_id") if inbox else None
    result_job = result.get("job_id") if result else None
    if not isinstance(inbox_job, str) or not inbox_job or result_job != inbox_job:
        return {
            "exists": False,
            "content": None,
            "normalized_from_mismatch": True,
            "inbox_job_id": inbox_job,
            "result_job_id": result_job,
        }
    return result_entry


def snapshot(repo_root: Path, snapshot_dir: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    destination = Path(snapshot_dir).resolve()
    destination.mkdir(parents=True, exist_ok=True)

    manifest = {
        "schema_version": 1,
        "files": {
            INBOX.as_posix(): _capture(root, INBOX),
            RESULT.as_posix(): _coherent_result_baseline(root),
            PAYLOAD.as_posix(): _capture(root, PAYLOAD),
        },
    }
    (destination / MANIFEST).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "action": "snapshot",
        "snapshot_dir": str(destination),
        "result_normalized": bool(
            manifest["files"][RESULT.as_posix()].get("normalized_from_mismatch")
        ),
    }


def _fallback_action(report_path: Path | None) -> str | None:
    if report_path is None:
        return None
    report = _read_json(report_path)
    action = report.get("action") if report else None
    return action if isinstance(action, str) else None


def restore(repo_root: Path, snapshot_dir: Path, fallback_report: Path | None = None) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    source = Path(snapshot_dir).resolve()
    manifest = _read_json(source / MANIFEST)
    if not manifest or manifest.get("schema_version") != 1:
        raise ValueError("reusable transport baseline manifest is missing or invalid")
    files = manifest.get("files")
    if not isinstance(files, dict):
        raise ValueError("reusable transport baseline files map is invalid")

    # Fixed inputs are always transient working copies inside survey-helper.
    _restore_entry(root, INBOX, files.get(INBOX.as_posix()))
    _restore_entry(root, PAYLOAD, files.get(PAYLOAD.as_posix()))

    action = _fallback_action(Path(fallback_report) if fallback_report is not None else None)
    restored_result = False
    if action == "dispatched":
        # A fallback dispatch temporarily owns the fixed result path as well. Restore
        # the original coherent result (or original absence) with the original inbox.
        _restore_entry(root, RESULT, files.get(RESULT.as_posix()))
        restored_result = True

    return {
        "action": "restore",
        "fallback_action": action,
        "restored_result": restored_result,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    snap = sub.add_parser("snapshot")
    snap.add_argument("--repo-root", default=".")
    snap.add_argument("--snapshot-dir", required=True)

    restore_parser = sub.add_parser("restore")
    restore_parser.add_argument("--repo-root", default=".")
    restore_parser.add_argument("--snapshot-dir", required=True)
    restore_parser.add_argument("--fallback-report")

    args = parser.parse_args()
    if args.command == "snapshot":
        result = snapshot(Path(args.repo_root), Path(args.snapshot_dir))
    else:
        report = Path(args.fallback_report) if args.fallback_report else None
        result = restore(Path(args.repo_root), Path(args.snapshot_dir), report)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
