#!/usr/bin/env python3
"""Apply descriptor/result deltas to the advisory worker-run index.

This helper is deliberately best-effort. Index or automatic-snapshot failures never
replace the canonical run-state request fast lane and must not fail submission work.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import derive_worker_run_state  # noqa: E402
import worker_run_index  # noqa: E402


def _paths(path: Path | None) -> list[Path]:
    if path is None or not path.is_file():
        return []
    out: list[Path] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value:
            out.append(Path(value))
    return out


def update(
    root: Path,
    *,
    descriptors: list[Path],
    results: list[Path],
    auto_snapshot: bool,
) -> dict[str, Any]:
    root = Path(root).resolve()
    summary: dict[str, Any] = {
        "schema_version": 1,
        "ok": True,
        "descriptor_updates": [],
        "result_updates": [],
        "automatic_snapshots": [],
        "errors": [],
    }
    affected: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    causes: dict[tuple[str, str, str, str], list[str]] = {}

    for path in descriptors:
        try:
            item = worker_run_index.apply_descriptor(root, path)
            item["path"] = path.as_posix()
            summary["descriptor_updates"].append(item)
        except Exception as exc:
            summary["errors"].append({
                "path": path.as_posix(), "stage": "descriptor", "error": f"{type(exc).__name__}: {exc}"
            })

    for path in results:
        try:
            item = worker_run_index.apply_result(root, path)
            item["path"] = path.as_posix()
            summary["result_updates"].append(item)
            identity = item.get("identity")
            if item.get("updated") is True and isinstance(identity, dict):
                key = tuple(str(identity.get(field) or "") for field in worker_run_index.RUN_FIELDS)
                if all(key):
                    affected[key] = identity
                    causes.setdefault(key, []).append(path.as_posix())
        except Exception as exc:
            summary["errors"].append({
                "path": path.as_posix(), "stage": "result", "error": f"{type(exc).__name__}: {exc}"
            })

    if auto_snapshot:
        for key in sorted(affected):
            identity = affected[key]
            try:
                output = derive_worker_run_state.emit_automatic_snapshot(
                    root,
                    identity,
                    source_events=sorted(set(causes.get(key, []))),
                )
                if output is not None:
                    summary["automatic_snapshots"].append(output)
            except Exception as exc:
                summary["errors"].append({
                    "path": None,
                    "stage": "automatic_snapshot",
                    "identity": identity,
                    "error": f"{type(exc).__name__}: {exc}",
                })
    summary["ok"] = not summary["errors"]
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--descriptors-file", type=Path)
    parser.add_argument("--results-file", type=Path)
    parser.add_argument("--auto-snapshot", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    summary = update(
        args.repo_root,
        descriptors=_paths(args.descriptors_file),
        results=_paths(args.results_file),
        auto_snapshot=args.auto_snapshot,
    )
    text = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(text, encoding="utf-8")
    print(text, end="")
    # Cache/snapshot acceleration is never allowed to block the canonical pipeline.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
