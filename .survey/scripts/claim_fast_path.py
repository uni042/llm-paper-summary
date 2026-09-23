#!/usr/bin/env python3
"""Run the canonical claim fast path with recovery work only when needed.

This is shared by the standalone claim workflow and the run-state initial-claim
pipeline. It keeps allocation safety intact while avoiding per-request syntax
compilation, repository-wide route enrichment, and unconditional repair scans.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import apply_library_checkpoint_barriers
import claim_worker_with_banks
import derive_worker_run_state
import normalize_research_paper_paths
import repair_claim_bank_recovery

CLAIM_RESULTS = Path(".survey/work-queue/claim-results")
JOBS = Path(".survey/work-queue/jobs")


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _digest(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


def _result_snapshot(root: Path) -> dict[str, str]:
    folder = root / CLAIM_RESULTS
    if not folder.is_dir():
        return {}
    return {
        path.relative_to(root).as_posix(): _digest(path)
        for path in folder.glob("*.json")
        if path.is_file()
    }


def _changed_results(root: Path, before: dict[str, str]) -> list[Path]:
    folder = root / CLAIM_RESULTS
    if not folder.is_dir():
        return []
    changed: list[Path] = []
    for path in sorted(folder.glob("*.json")):
        rel = path.relative_to(root).as_posix()
        if before.get(rel) != _digest(path):
            changed.append(path.relative_to(root))
    return changed


def _needs_paper_path_normalization(root: Path) -> bool:
    folder = root / JOBS
    if not folder.is_dir():
        return False
    for path in folder.glob("*.json"):
        value = _read(path, {})
        if not isinstance(value, dict) or value.get("type") != "research":
            continue
        if value.get("paper_path") is None and any(
            isinstance(value.get(key), str) and str(value.get(key)).strip()
            for key in ("canonical_id", "source_url", "title")
        ):
            return True
    return False


def _repair_needed(root: Path, result_paths: list[Path]) -> bool:
    for rel in result_paths:
        value = _read(root / rel, {})
        if not isinstance(value, dict):
            continue
        for assignment in value.get("assignments") or []:
            if not isinstance(assignment, dict):
                continue
            job = assignment.get("job")
            if isinstance(job, dict) and job.get("repair_required") is True:
                return True
            job_id = assignment.get("job_id")
            if isinstance(job_id, str):
                live = _read(root / JOBS / f"{job_id}.json", {})
                if isinstance(live, dict) and live.get("repair_required") is True:
                    return True
    return False


def process(repo_root: Path) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    before = _result_snapshot(root)

    normalization: dict[str, Any] = {"skipped": True}
    if _needs_paper_path_normalization(root):
        normalization = normalize_research_paper_paths.normalize(root, apply=True)
        normalization["skipped"] = False

    barriers = apply_library_checkpoint_barriers.apply(root)
    allocation = claim_worker_with_banks.process_requests(root)
    allocation.update(claim_worker_with_banks.maintain_shared_pool(root))
    changed = _changed_results(root, before)

    repair: dict[str, Any] = {"skipped": True}
    if changed and _repair_needed(root, changed):
        repair = repair_claim_bank_recovery.repair_allocated_claims(root)
        repair["skipped"] = False
        changed = _changed_results(root, before)

    state_update: dict[str, Any] = {
        "observed_claim_results": 0,
        "touched_runs": 0,
        "generated_results": [],
        "canonical_fallback_runs": [],
    }
    if changed:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as tmp:
            for rel in changed:
                tmp.write(rel.as_posix() + "\n")
            changed_file = Path(tmp.name)
        try:
            state_update = derive_worker_run_state.apply_claim_result_deltas(root, changed_file)
        finally:
            changed_file.unlink(missing_ok=True)

    return {
        "ok": True,
        "normalization": normalization,
        "checkpoint_barriers": barriers,
        "allocation": allocation,
        "repair": repair,
        "changed_claim_results": [path.as_posix() for path in changed],
        "run_state_update": state_update,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = process(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
