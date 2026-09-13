#!/usr/bin/env python3
"""List immutable descriptors that still need a durable matching result.

This is the backlog-drain view used by the serialized submission workflow. Both a
successful and a failed exact result settle one immutable attempt; failed attempts
are repaired by a new descriptor rather than replaying the same immutable input on
every unrelated submission run.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import immutable_submission


def _read(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None


def unsettled_paths(repo_root: Path) -> list[str]:
    root = Path(repo_root).resolve()
    out: list[str] = []
    submissions = root / ".survey/work-queue/submissions"
    results = root / ".survey/work-queue/results"

    for kind in sorted(immutable_submission.KINDS):
        folder = submissions / kind
        for descriptor_path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
            descriptor = _read(descriptor_path)
            result = _read(results / kind / descriptor_path.name)
            if (
                isinstance(descriptor, dict)
                and immutable_submission.result_matches_identity(result, descriptor)
            ):
                # Exact success and exact durable failure are both settled attempts.
                continue
            out.append(descriptor_path.relative_to(root).as_posix())
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    for path in unsettled_paths(args.repo_root):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
