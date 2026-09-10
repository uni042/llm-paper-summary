#!/usr/bin/env python3
"""Reconcile maintenance-cycle state with newer durable maintenance reports.

This is intentionally conservative: it only copies fields from reports that are
newer than the corresponding report timestamp already recorded in the state.
It never changes cadence counters, run keys, maintenance sequence, or pending
state.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def newer(report_time: Any, recorded_time: Any) -> bool:
    report_dt = parse_time(report_time)
    recorded_dt = parse_time(recorded_time)
    if report_dt is None:
        return False
    return recorded_dt is None or report_dt > recorded_dt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    root = Path(args.repo_root)
    state_path = root / ".survey/work-queue/maintenance-cycle.json"
    consistency_path = root / ".survey/reports/consistency-latest.json"
    gc_path = root / ".survey/reports/full-gc-latest.json"

    state = load_json(state_path)
    if state is None:
        print(json.dumps({"action": "skipped", "reason": "maintenance_state_unreadable"}))
        return 0

    changed_fields: list[str] = []
    consistency = load_json(consistency_path)
    if consistency and newer(consistency.get("checked_at"), state.get("last_consistency_checked_at")):
        status = consistency.get("status")
        checked_at = consistency.get("checked_at")
        if status is not None:
            state["last_consistency_status"] = status
            # This field represents the currently known maintenance/consistency health.
            state["last_maintenance_status"] = "passed" if status == "passed" else "issues_found"
            state["last_maintenance_status_source"] = "consistency_report"
            changed_fields.extend([
                "last_consistency_status",
                "last_maintenance_status",
                "last_maintenance_status_source",
            ])
        state["last_consistency_checked_at"] = checked_at
        changed_fields.append("last_consistency_checked_at")

    gc = load_json(gc_path)
    if gc and newer(gc.get("checked_at"), state.get("last_gc_checked_at")):
        state["last_gc_checked_at"] = gc.get("checked_at")
        state["last_gc_deleted"] = gc.get("deleted_count", state.get("last_gc_deleted", 0))
        changed_fields.extend(["last_gc_checked_at", "last_gc_deleted"])

    if not changed_fields:
        print(json.dumps({"action": "noop", "changed": False}))
        return 0

    state["state_reconciled_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
    state["state_reconcile_source"] = "newer_durable_report"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "action": "reconciled",
        "changed": True,
        "fields": sorted(set(changed_fields)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
