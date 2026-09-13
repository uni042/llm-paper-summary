#!/usr/bin/env python3
"""Process immutable submissions concurrently across independent mutation targets."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Callable, Iterable

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import reduce_submission_effects  # noqa: E402

MIN_PARALLELISM = 1
MAX_PARALLELISM = 8
DEFAULT_PARALLELISM = 4


def bounded_parallelism(value: int) -> int:
    return max(MIN_PARALLELISM, min(MAX_PARALLELISM, int(value)))


def _read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def descriptor_group_key(repo_root: Path, descriptor_path: Path) -> str:
    """Group by paper first, then job, so shared mutation targets never overlap."""
    repo_root = Path(repo_root).resolve()
    descriptor_path = Path(descriptor_path)
    if not descriptor_path.is_absolute():
        descriptor_path = repo_root / descriptor_path
    value = _read_object(descriptor_path)
    if isinstance(value, dict):
        paper_path = value.get("paper_path")
        if isinstance(paper_path, str) and paper_path.startswith("papers/") and ".." not in Path(paper_path).parts:
            return f"paper:{Path(paper_path).as_posix()}"
        job_id = value.get("job_id")
        if isinstance(job_id, str) and job_id:
            return f"job:{job_id}"
    try:
        relative = descriptor_path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        relative = descriptor_path.resolve().as_posix()
    return f"path:{relative}"


def run_parallel_grouped(
    repo_root: Path,
    descriptor_paths: Iterable[Path],
    *,
    worker: Callable[[Path], Any],
    parallelism: int = DEFAULT_PARALLELISM,
) -> list[Any]:
    """Run one mutation-target group sequentially while independent groups overlap."""
    repo_root = Path(repo_root).resolve()
    paths = [Path(path) for path in descriptor_paths]
    groups: OrderedDict[str, list[tuple[int, Path]]] = OrderedDict()
    for index, path in enumerate(paths):
        key = descriptor_group_key(repo_root, path)
        groups.setdefault(key, []).append((index, path))

    output: list[Any] = [None] * len(paths)

    def run_group(items: list[tuple[int, Path]]) -> list[tuple[int, Any]]:
        rows: list[tuple[int, Any]] = []
        for index, path in items:
            rows.append((index, worker(path)))
        return rows

    max_workers = min(bounded_parallelism(parallelism), max(len(groups), 1))
    if not groups:
        return output
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(run_group, items) for items in groups.values()]
        for future in as_completed(futures):
            for index, value in future.result():
                output[index] = value
    return output


def _effect_path(effects_dir: Path, descriptor_path: Path) -> Path:
    token = hashlib.sha256(str(descriptor_path).encode("utf-8")).hexdigest()[:24]
    return effects_dir / f"effect-{token}.json"


def _run_command(command: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)
    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, file=sys.stderr, end="" if result.stderr.endswith("\n") else "\n")
    return result


def process_one(repo_root: Path, descriptor_path: Path, effects_dir: Path) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    descriptor_path = Path(descriptor_path)
    if not descriptor_path.is_absolute():
        descriptor_path = repo_root / descriptor_path
    try:
        relative = descriptor_path.resolve().relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise ValueError("descriptor path must stay within repository") from exc

    effect = _effect_path(effects_dir, Path(relative))
    processor = repo_root / ".survey/scripts/process_immutable_submission.py"
    isolation = repo_root / ".survey/scripts/isolate_failed_immutable_submission.py"
    command = [
        sys.executable,
        str(processor),
        "--repo-root",
        str(repo_root),
        "--submission",
        relative,
        "--defer-shared-state",
        "--effect-file",
        str(effect),
    ]
    result = _run_command(command, cwd=repo_root)
    if result.returncode == 0:
        return {"descriptor": relative, "ok": True, "returncode": 0}

    isolated = _run_command(
        [
            sys.executable,
            str(isolation),
            "--repo-root",
            str(repo_root),
            "--submission",
            relative,
        ],
        cwd=repo_root,
    )
    return {
        "descriptor": relative,
        "ok": False,
        "returncode": result.returncode,
        "isolation_returncode": isolated.returncode,
    }


def _validate_unique_inputs(repo_root: Path, paths: list[Path]) -> None:
    seen_paths: set[str] = set()
    seen_identity: set[tuple[str, str]] = set()
    for path in paths:
        absolute = path if path.is_absolute() else repo_root / path
        try:
            relative = absolute.resolve().relative_to(repo_root).as_posix()
        except ValueError as exc:
            raise ValueError("descriptor path must stay within repository") from exc
        if relative in seen_paths:
            raise ValueError(f"duplicate immutable descriptor path: {relative}")
        seen_paths.add(relative)
        value = _read_object(absolute)
        if not isinstance(value, dict):
            continue
        job_id = value.get("job_id")
        attempt_id = value.get("attempt_id")
        if isinstance(job_id, str) and job_id and isinstance(attempt_id, str) and attempt_id:
            identity = (job_id, attempt_id)
            if identity in seen_identity:
                raise ValueError(f"duplicate immutable job/attempt in batch: {job_id} / {attempt_id}")
            seen_identity.add(identity)


def process_batch(
    repo_root: Path,
    descriptor_paths: Iterable[Path],
    effects_dir: Path,
    *,
    parallelism: int = DEFAULT_PARALLELISM,
) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    effects_dir = Path(effects_dir)
    if not effects_dir.is_absolute():
        effects_dir = repo_root / effects_dir
    effects_dir.mkdir(parents=True, exist_ok=True)
    for stale in effects_dir.glob("*.json"):
        stale.unlink()

    paths = [Path(path) for path in descriptor_paths]
    _validate_unique_inputs(repo_root, paths)
    rows = run_parallel_grouped(
        repo_root,
        paths,
        worker=lambda path: process_one(repo_root, path, effects_dir),
        parallelism=parallelism,
    )
    reduction = reduce_submission_effects.reduce_effects(repo_root, effects_dir)
    failures = [row for row in rows if isinstance(row, dict) and not row.get("ok")]
    return {
        "descriptors": len(rows),
        "failures": len(failures),
        "results": rows,
        "reduction": reduction,
    }


def _read_descriptor_list(path: Path) -> list[Path]:
    rows: list[Path] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = line.strip()
        if value:
            rows.append(Path(value))
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--descriptors-file", type=Path, required=True)
    parser.add_argument("--effects-dir", type=Path, required=True)
    parser.add_argument("--parallelism", type=int, default=DEFAULT_PARALLELISM)
    args = parser.parse_args()

    descriptors = _read_descriptor_list(args.descriptors_file)
    summary = process_batch(
        args.repo_root,
        descriptors,
        args.effects_dir,
        parallelism=args.parallelism,
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if summary["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
