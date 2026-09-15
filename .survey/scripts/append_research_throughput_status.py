#!/usr/bin/env python3
"""Deprecated STATUS compatibility shim.

STATUS.md is generated exclusively by build_status_dashboard.py from direct,
durable evidence. This module intentionally computes and appends nothing.
"""
from __future__ import annotations

import argparse
from pathlib import Path


def render_section(repo_root: Path, now=None) -> str:
    return ""


def append_section(repo_root: Path, status_path: Path, now=None) -> None:
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--status", type=Path, default=Path("STATUS.md"))
    parser.parse_args()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
