#!/usr/bin/env python3
"""Raise survey history retention needed by STATUS.md without lowering user state."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

MIN_RUN_LEDGER_HISTORY = 192
MIN_DISCOVERY_HISTORY = 256


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.is_file():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return value if isinstance(value, dict) else None


def ensure_minimum(path: Path, minimum: int) -> bool:
    state = read_json(path)
    if state is None:
        return False
    current = state.get("history_limit")
    if isinstance(current, int) and current >= minimum:
        return False
    state["history_limit"] = minimum
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


def ensure_retention(repo_root: Path) -> list[str]:
    root = Path(repo_root)
    changed: list[str] = []
    targets = [
        (root / ".survey/work-queue/run-ledger.json", MIN_RUN_LEDGER_HISTORY),
        (root / ".survey/work-queue/discovery-state.json", MIN_DISCOVERY_HISTORY),
    ]
    for path, minimum in targets:
        if ensure_minimum(path, minimum):
            changed.append(path.relative_to(root).as_posix())
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    changed = ensure_retention(Path(args.repo_root))
    print(json.dumps({"changed": changed}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
