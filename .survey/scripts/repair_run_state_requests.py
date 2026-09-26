#!/usr/bin/env python3
"""Repair legacy run-state request files that have a .json suffix but YAML text.

Only syntax is normalized. Semantic validation remains the responsibility of
derive_worker_run_state.py. Unparseable/non-object requests are never guessed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REQUESTS = Path(".survey/work-queue/run-state/requests")


def parse_legacy_object(text: str) -> dict[str, Any] | None:
    try:
        value = json.loads(text)
    except (json.JSONDecodeError, TypeError):
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError:
            return None
    return value if isinstance(value, dict) else None


def repair(repo_root: Path, *, apply: bool) -> dict[str, Any]:
    root = repo_root.resolve()
    folder = root / REQUESTS
    repaired: list[str] = []
    invalid: list[str] = []
    checked = 0

    if not folder.is_dir():
        return {"checked": 0, "repaired": [], "invalid": []}

    for path in sorted(folder.glob("*.json")):
        checked += 1
        raw = path.read_text(encoding="utf-8")
        try:
            value = json.loads(raw)
            if isinstance(value, dict):
                continue
        except json.JSONDecodeError:
            pass

        value = parse_legacy_object(raw)
        rel = path.relative_to(root).as_posix()
        if value is None:
            invalid.append(rel)
            continue

        canonical = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if apply:
            path.write_text(canonical, encoding="utf-8")
        repaired.append(rel)

    return {
        "checked": checked,
        "repaired": repaired,
        "invalid": invalid,
        "apply": apply,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    result = repair(args.repo_root, apply=args.apply)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result["invalid"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
