#!/usr/bin/env python3
"""Deprecated STATUS compatibility shim.

STATUS.md is now a complete direct-evidence document produced by
build_status_dashboard.py. No post-processing, inferred metrics, checkpoint
estimates, or legacy observability rewrites are applied here.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def refine_text(repo_root: Path, text: str, now=None) -> str:
    return text


def refine_status(repo_root: Path, status_path: Path, now=None) -> None:
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--status", type=Path, default=Path("STATUS.md"))
    parser.parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
