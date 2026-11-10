#!/usr/bin/env python3
"""Decide whether one queue push should republish the status dashboard.

Ingress-only worker writes are intentionally ignored. The authoritative follow-up
Actions commit (claim allocation, submission result, queue mutation, etc.) will
publish the dashboard instead, avoiding an extra main commit in the middle of a
parallel worker hand-off. Merge commits are republished conservatively because
``git diff-tree`` may emit no paths for them without parent-expansion flags.
"""
from __future__ import annotations

import argparse
import sys


SELF_COMMIT_PREFIX = "chore: refresh survey status dashboard"
INGRESS_ONLY_PREFIXES = (
    ".survey/work-queue/claim-requests/",
    ".survey/work-queue/records/",
    ".survey/work-queue/submissions/research/",
    ".survey/work-queue/submissions/audit/",
    ".survey/work-queue/fallback-inbox/",
    ".survey/work-queue/transport/",
)


def should_publish(paths: list[str], commit_message: str) -> bool:
    message = commit_message.strip()
    if message.startswith(SELF_COMMIT_PREFIX):
        return False
    if message.startswith("Merge "):
        return True
    for raw in paths:
        path = raw.strip()
        if not path or path == "STATUS.md":
            continue
        if any(path.startswith(prefix) for prefix in INGRESS_ONLY_PREFIXES):
            continue
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--commit-message", default="")
    args = parser.parse_args()
    paths = [line.strip() for line in sys.stdin if line.strip()]
    print("true" if should_publish(paths, args.commit_message) else "false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
