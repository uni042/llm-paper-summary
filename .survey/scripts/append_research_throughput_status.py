#!/usr/bin/env python3
"""Deprecated STATUS compatibility shim with a stale-workflow migration guard.

Current workflows render STATUS.md through render_status_dashboard.py.  Older
workflow YAML already in flight can still execute build_status_dashboard.py
after checking out a newer main.  When that legacy layout is detected, this
shim immediately regenerates STATUS.md through the canonical renderer.

For an already-canonical STATUS.md (and for unrelated files), this remains a
no-op.  The historical throughput section is never appended.
"""
from __future__ import annotations

import argparse
from pathlib import Path


CANONICAL_MARKER = "## 件数サマリー"
LEGACY_MARKER = "## 1. ここ数時間で論文読解・サーベイが成功しているか"


def render_section(repo_root: Path, now=None) -> str:
    return ""


def append_section(repo_root: Path, status_path: Path, now=None) -> None:
    if not status_path.is_file():
        return

    text = status_path.read_text(encoding="utf-8")
    if CANONICAL_MARKER in text or LEGACY_MARKER not in text:
        return

    # Import lazily so this deprecated shim stays inert unless it encounters
    # the exact old dashboard layout produced by a stale workflow definition.
    from render_status_dashboard import build_dashboard

    status_path.write_text(
        build_dashboard(repo_root.resolve(), now=now),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--status", type=Path, default=Path("STATUS.md"))
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    status_path = args.status
    if not status_path.is_absolute():
        status_path = repo_root / status_path
    append_section(repo_root, status_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
