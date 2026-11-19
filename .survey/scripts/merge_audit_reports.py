#!/usr/bin/env python3
"""Merge a partial (subset) audit report with the previous full report.

Companion to select_maintenance_audit_paths.py (redesign Phase 1, item B4).
The daily maintenance audits only re-audit the changed-plus-rotation subset
and write a partial report. This script produces the durable report by
carrying forward previous entries for papers that were neither re-audited
today nor changed since the watermark commit, so downstream consumers
(maintenance_health regression comparison, STATUS) keep seeing the latest
known per-paper state for the whole collection.

If the previous report is missing or malformed, the partial report is
written through unchanged (the next full-coverage rotation still restores
complete state within one rotation period for changed papers, and the
health check treats an empty baseline as initialization).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--partial", type=Path, required=True)
    ap.add_argument("--previous", type=Path, required=True)
    ap.add_argument("--changed-file", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    partial = load_json(args.partial)
    if partial is None:
        raise SystemExit(f"partial audit report is unreadable: {args.partial}")
    partial_results = partial.get("results")
    if not isinstance(partial_results, list):
        raise SystemExit(f"partial audit report has no results list: {args.partial}")

    changed = {
        line.strip()
        for line in args.changed_file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    audited_paths = {
        str(entry.get("path"))
        for entry in partial_results
        if isinstance(entry, dict) and entry.get("path")
    }

    previous = load_json(args.previous)
    carried: list[dict[str, Any]] = []
    if previous is not None and isinstance(previous.get("results"), list):
        for entry in previous["results"]:
            if not isinstance(entry, dict):
                continue
            path = entry.get("path")
            if not path:
                continue
            if str(path) in audited_paths or str(path) in changed:
                continue
            carried.append(entry)

    merged = dict(partial)
    merged["results"] = sorted(
        [*partial_results, *carried],
        key=lambda entry: str(entry.get("path") or "") if isinstance(entry, dict) else "",
    )
    merged["coverage"] = {
        "mode": "changed_plus_rotation_merged" if carried or previous is not None else "partial_only",
        "audited_today": len(partial_results),
        "carried_forward": len(carried),
        "total": len(merged["results"]),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        f"merged audit report: audited={len(partial_results)} "
        f"carried={len(carried)} total={len(merged['results'])} -> {args.out}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
