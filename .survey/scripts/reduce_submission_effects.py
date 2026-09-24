#!/usr/bin/env python3
"""Fold descriptor-local immutable submission effects into shared queue state once."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import queue_worker  # noqa: E402

COUNTER_FIELDS = ("research_completed", "audit_completed", "rejected")


def _read(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise ValueError(f"invalid submission effect JSON: {path}") from exc


def _configure(repo_root: Path) -> None:
    repo_root = Path(repo_root).resolve()
    root = repo_root / ".survey"
    queue_worker.ROOT = root
    queue_worker.QUEUE = root / "work-queue"
    queue_worker.JOBS = queue_worker.QUEUE / "jobs"
    queue_worker.SUBMISSIONS = queue_worker.QUEUE / "submissions"
    queue_worker.RESULTS = queue_worker.QUEUE / "results"
    queue_worker.STATE = queue_worker.QUEUE / "state.json"
    queue_worker.ARCHIVE = queue_worker.QUEUE / "archive"
    queue_worker.DISCOVERY_STATE = queue_worker.QUEUE / "discovery-state.json"


def _validate_effect(path: Path, value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"submission effect must be an object: {path}")
    if value.get("schema_version") != 1:
        raise ValueError(f"submission effect schema_version must be 1: {path}")
    job_id = value.get("job_id")
    attempt_id = value.get("attempt_id")
    if not isinstance(job_id, str) or not job_id:
        raise ValueError(f"submission effect requires job_id: {path}")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise ValueError(f"submission effect requires attempt_id: {path}")

    out = dict(value)
    for field in COUNTER_FIELDS:
        raw = value.get(field, 0)
        if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
            raise ValueError(f"submission effect {field} must be a non-negative integer: {path}")
        out[field] = raw
    if not isinstance(value.get("views_dirty", False), bool):
        raise ValueError(f"submission effect views_dirty must be boolean: {path}")
    out["views_dirty"] = bool(value.get("views_dirty", False))
    return out


def _refresh_snapshot(repo_root: Path) -> None:
    snapshot = queue_worker.queue_snapshot()
    path = Path(repo_root).resolve() / ".survey/work-queue/next-jobs.json"
    old = queue_worker.read_json(path, {}) or {}
    old_cmp = dict(old)
    old_cmp.pop("generated_at", None)
    if old_cmp == snapshot:
        snapshot["generated_at"] = old.get("generated_at", queue_worker.now())
    else:
        snapshot["generated_at"] = queue_worker.now()
    queue_worker.write_json(path, snapshot)


def reduce_effects(repo_root: Path, effects_dir: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    effects_dir = Path(effects_dir)
    if not effects_dir.is_absolute():
        effects_dir = repo_root / effects_dir

    _configure(repo_root)
    effects: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    if effects_dir.is_dir():
        for path in sorted(effects_dir.glob("*.json")):
            effect = _validate_effect(path, _read(path))
            identity = (effect["job_id"], effect["attempt_id"])
            if identity in seen:
                raise ValueError(
                    f"duplicate submission effect for job/attempt: {effect['job_id']} / {effect['attempt_id']}"
                )
            seen.add(identity)
            effects.append(effect)

    state = queue_worker.load_state()
    stats = state.setdefault("stats", {})
    totals = {field: 0 for field in COUNTER_FIELDS}
    views_dirty = False
    for effect in effects:
        for field in COUNTER_FIELDS:
            totals[field] += effect[field]
        views_dirty = views_dirty or effect["views_dirty"]

    for field, amount in totals.items():
        stats[field] = int(stats.get(field, 0) or 0) + amount
    if views_dirty:
        state.setdefault("maintenance", {})["views_dirty"] = True

    queue_worker.save_state(state)
    _refresh_snapshot(repo_root)
    return {
        "effects": len(effects),
        **totals,
        "views_dirty": views_dirty,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--effects-dir", type=Path, required=True)
    args = parser.parse_args()
    summary = reduce_effects(args.repo_root, args.effects_dir)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
