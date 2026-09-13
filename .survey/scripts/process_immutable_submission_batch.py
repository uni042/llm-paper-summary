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

import immutable_submission  # noqa: E402
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


def _absolute_descriptor(repo_root: Path, descriptor_path: Path) -> Path:
    repo_root = Path(repo_root).resolve()
    path = Path(descriptor_path)
    return path if path.is_absolute() else repo_root / path


def _canonical_identity_key(repo_root: Path, descriptor: dict[str, Any]) -> str | None:
    refs = descriptor.get("record_slots")
    if not isinstance(refs, list):
        return None
    metadata_ref = next(
        (ref for ref in refs if isinstance(ref, dict) and ref.get("slot") == "metadata"),
        None,
    )
    if metadata_ref is None:
        return None
    try:
        payload = immutable_submission.read_record_slot(repo_root, metadata_ref)
    except Exception:
        return None
    data = payload.get("data") if isinstance(payload, dict) else None
    canonical_id = data.get("canonical_id") if isinstance(data, dict) else None
    if not isinstance(canonical_id, str) or not canonical_id.strip():
        return None
    return f"identity:{canonical_id.strip().casefold()}"


def descriptor_resource_keys(repo_root: Path, descriptor_path: Path) -> frozenset[str]:
    """Return every repository resource that requires same-group serialization."""
    repo_root = Path(repo_root).resolve()
    absolute = _absolute_descriptor(repo_root, descriptor_path)
    value = _read_object(absolute)
    keys: set[str] = set()
    if isinstance(value, dict):
        identity_key = _canonical_identity_key(repo_root, value)
        if identity_key:
            keys.add(identity_key)
        paper_path = value.get("paper_path")
        if isinstance(paper_path, str) and paper_path.startswith("papers/") and ".." not in Path(paper_path).parts:
            keys.add(f"paper:{Path(paper_path).as_posix()}")
        job_id = value.get("job_id")
        if isinstance(job_id, str) and job_id:
            keys.add(f"job:{job_id}")
    if not keys:
        try:
            relative = absolute.resolve().relative_to(repo_root).as_posix()
        except ValueError:
            relative = absolute.resolve().as_posix()
        keys.add(f"path:{relative}")
    return frozenset(keys)


def descriptor_group_key(repo_root: Path, descriptor_path: Path) -> str:
    """Compatibility/debug key: prefer paper, then job, then any resource key."""
    keys = descriptor_resource_keys(repo_root, descriptor_path)
    for prefix in ("paper:", "job:", "identity:", "path:"):
        match = next((key for key in keys if key.startswith(prefix)), None)
        if match is not None:
            return match
    return sorted(keys)[0]


def _group_descriptor_indices(repo_root: Path, paths: list[Path]) -> list[list[int]]:
    """Union descriptors that share any job, paper, or canonical identity resource."""
    parents = list(range(len(paths)))

    def find(index: int) -> int:
        while parents[index] != index:
            parents[index] = parents[parents[index]]
            index = parents[index]
        return index

    def union(left: int, right: int) -> None:
        a, b = find(left), find(right)
        if a != b:
            parents[b] = a

    owner: dict[str, int] = {}
    for index, path in enumerate(paths):
        for resource in descriptor_resource_keys(repo_root, path):
            previous = owner.get(resource)
            if previous is None:
                owner[resource] = index
            else:
                union(index, previous)

    grouped: OrderedDict[int, list[int]] = OrderedDict()
    for index in range(len(paths)):
        grouped.setdefault(find(index), []).append(index)
    return list(grouped.values())


def group_descriptor_paths(repo_root: Path, descriptor_paths: Iterable[Path]) -> list[list[Path]]:
    paths = [Path(path) for path in descriptor_paths]
    return [[paths[index] for index in group] for group in _group_descriptor_indices(repo_root, paths)]


def run_parallel_grouped(
    repo_root: Path,
    descriptor_paths: Iterable[Path],
    *,
    worker: Callable[[Path], Any],
    parallelism: int = DEFAULT_PARALLELISM,
) -> list[Any]:
    """Run one connected mutation group sequentially while independent groups overlap."""
    repo_root = Path(repo_root).resolve()
    paths = [Path(path) for path in descriptor_paths]
    index_groups = _group_descriptor_indices(repo_root, paths)
    output: list[Any] = [None] * len(paths)

    def run_group(indices: list[int]) -> list[tuple[int, Any]]:
        rows: list[tuple[int, Any]] = []
        for index in indices:
            rows.append((index, worker(paths[index])))
        return rows

    max_workers = min(bounded_parallelism(parallelism), max(len(index_groups), 1))
    if not index_groups:
        return output
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = [pool.submit(run_group, indices) for indices in index_groups]
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
    descriptor_path = _absolute_descriptor(repo_root, descriptor_path)
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
        absolute = _absolute_descriptor(repo_root, path)
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
