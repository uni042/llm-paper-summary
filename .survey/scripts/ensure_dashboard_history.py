#!/usr/bin/env python3
"""Ensure durable dashboard source histories are long enough for 7-day reporting.

The existing writers respect each state's persisted history_limit. Keeping this as a
small idempotent migration avoids coupling dashboard retention to queue semantics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MIN_HISTORY_LIMIT = 384
STATE_PATHS = (
    ".survey/work-queue/run-ledger.json",
    ".survey/work-queue/discovery-state.json",
)


def ensure_history_limits(repo_root: Path, minimum: int = MIN_HISTORY_LIMIT) -> list[str]:
    changed: list[str] = []
    for rel in STATE_PATHS:
        path = repo_root / rel
        if not path.is_file():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        current = data.get("history_limit")
        if isinstance(current, int) and current >= minimum:
            continue
        data["history_limit"] = minimum
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changed.append(rel)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--minimum", type=int, default=MIN_HISTORY_LIMIT)
    args = parser.parse_args()
    changed = ensure_history_limits(Path(args.repo_root).resolve(), args.minimum)
    print(json.dumps({"changed": changed, "minimum": args.minimum}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
