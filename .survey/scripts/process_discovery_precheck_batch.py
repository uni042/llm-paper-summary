#!/usr/bin/env python3
"""Process foreground Discovery prechecks concurrently in one checkout.

The workflow keeps publication to main serialized. This helper parallelizes only
per-request precheck computation. process_discovery_precheck serializes the short
preload claim/bank mutation critical section with PRELOAD_CLAIM_LOCK.
"""
from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, Iterable

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import process_discovery_precheck  # noqa: E402

MIN_PARALLELISM = 1
MAX_PARALLELISM = 8
DEFAULT_PARALLELISM = 4
REQUEST_ROOT = Path(".survey/work-queue/discovery-precheck/requests")
RESULT_ROOT = Path(".survey/work-queue/discovery-precheck/results")


def bounded_parallelism(value: int) -> int:
    return max(MIN_PARALLELISM, min(MAX_PARALLELISM, int(value)))


def _normalize_request_path(repo_root: Path, path: Path) -> Path:
    repo_root = Path(repo_root).resolve()
    absolute = Path(path)
    if not absolute.is_absolute():
        absolute = repo_root / absolute
    absolute = absolute.resolve()
    try:
        relative = absolute.relative_to(repo_root)
    except ValueError as exc:
        raise ValueError("Discovery precheck request must stay within repository") from exc
    if relative.parent != REQUEST_ROOT or relative.suffix != ".json":
        raise ValueError(f"unsupported Discovery precheck request path: {relative.as_posix()}")
    return absolute


def result_path_for(repo_root: Path, request_path: Path) -> Path:
    request = _normalize_request_path(repo_root, request_path)
    return Path(repo_root).resolve() / RESULT_ROOT / request.name


def run_parallel_requests(
    request_paths: Iterable[Path],
    *,
    worker: Callable[[Path], Any],
    parallelism: int = DEFAULT_PARALLELISM,
) -> list[Any]:
    paths = [Path(path) for path in request_paths]
    if not paths:
        return []
    output: list[Any] = [None] * len(paths)
    max_workers = min(bounded_parallelism(parallelism), len(paths))
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(worker, path): index for index, path in enumerate(paths)}
        for future in as_completed(futures):
            output[futures[future]] = future.result()
    return output


def process_one(
    repo_root: Path,
    request_path: Path,
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    request_path = _normalize_request_path(repo_root, request_path)
    result_path = result_path_for(repo_root, request_path)
    if result_path.is_file():
        return {
            "request": request_path.relative_to(repo_root).as_posix(),
            "result": result_path.relative_to(repo_root).as_posix(),
            "ok": True,
            "already_settled": True,
        }

    try:
        result = process_discovery_precheck.process_request(
            request_path,
            snapshot_dir=Path(snapshot_dir),
            rejection_ledger_path=Path(rejection_ledger_path),
            repo_root=repo_root,
        )
        ok = result.get("ok") is True
    except Exception as exc:
        result = process_discovery_precheck.failure_result(request_path, exc)
        ok = False

    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return {
        "request": request_path.relative_to(repo_root).as_posix(),
        "result": result_path.relative_to(repo_root).as_posix(),
        "ok": ok,
        "already_settled": False,
    }


def process_batch(
    repo_root: Path,
    request_paths: Iterable[Path],
    *,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
    parallelism: int = DEFAULT_PARALLELISM,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    normalized = [_normalize_request_path(repo_root, path) for path in request_paths]
    seen: set[Path] = set()
    for path in normalized:
        if path in seen:
            raise ValueError(f"duplicate Discovery precheck request: {path}")
        seen.add(path)

    rows = run_parallel_requests(
        normalized,
        worker=lambda path: process_one(
            repo_root,
            path,
            snapshot_dir=snapshot_dir,
            rejection_ledger_path=rejection_ledger_path,
        ),
        parallelism=parallelism,
    )
    failures = [row for row in rows if isinstance(row, dict) and row.get("ok") is not True]
    return {
        "requests": len(rows),
        "failures": len(failures),
        "parallelism": min(bounded_parallelism(parallelism), max(len(rows), 1)),
        "results": rows,
    }


def _read_request_list(path: Path) -> list[Path]:
    return [Path(line.strip()) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def run_cli(
    *,
    repo_root: Path,
    requests_file: Path,
    snapshot_dir: Path,
    rejection_ledger_path: Path,
    parallelism: int = DEFAULT_PARALLELISM,
) -> int:
    try:
        summary = process_batch(
            Path(repo_root),
            _read_request_list(Path(requests_file)),
            snapshot_dir=Path(snapshot_dir),
            rejection_ledger_path=Path(rejection_ledger_path),
            parallelism=parallelism,
        )
    except Exception as exc:
        print(f"Fatal Discovery precheck batch failure: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["failures"] else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--requests-file", type=Path, required=True)
    parser.add_argument("--snapshot-dir", type=Path, required=True)
    parser.add_argument("--rejection-ledger", type=Path, required=True)
    parser.add_argument("--parallelism", type=int, default=DEFAULT_PARALLELISM)
    args = parser.parse_args()
    return run_cli(
        repo_root=args.repo_root,
        requests_file=args.requests_file,
        snapshot_dir=args.snapshot_dir,
        rejection_ledger_path=args.rejection_ledger,
        parallelism=args.parallelism,
    )


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
