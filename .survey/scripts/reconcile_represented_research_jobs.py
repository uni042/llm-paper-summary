#!/usr/bin/env python3
"""Supersede stale ready Research jobs when their paper already exists."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import research_job_reconciliation


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    result = research_job_reconciliation.reconcile(
        args.repo_root,
        dry_run=args.dry_run,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
