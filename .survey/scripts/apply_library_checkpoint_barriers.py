#!/usr/bin/env python3
"""Merge durable Library checkpoint barriers into unprocessed claim requests.

A Scheduled Chat worker may finish a Research/Audit job while direct GitHub artifact
transport is unavailable. In that case the full record is stored in ChatGPT Library
and the released GitHub claim keeps ``checkpoint_ref``. The queue job deliberately
remains ``ready`` until the Library payload is replayed, so a later worker must not
claim and re-read it in the meantime.

Workers are expected to echo their Library checkpoint registry in ``checkpointed_jobs``.
This script is the repository-side safety net: before claim allocation it merges every
valid checkpoint_ref already persisted on a non-terminal ready job into each unprocessed
claim request. Request-provided entries win, because they can point at a newer Library
attempt than the historical claim file.

A durable checkpoint has two independent meanings: the expensive paper read is already
complete, while the structured record may still need a repair claim after validation
failure. ``checkpointed_jobs`` is an allocation barrier for ordinary claims. For a
``repair_required`` job whose immutable failures are durable, this script moves the
entry to the internal ``repair_checkpointed_jobs`` provenance list instead of deleting
it. The allocator can then issue the repair claim, while the post-allocation recovery
pass can prove that the claim must reuse existing research rather than re-read the paper.
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path
from typing import Any

import claim_worker

SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")
LIBRARY_PENDING_PREFIX = "/LLM-survey-outbox/pending/"
MAX_CHECKPOINTED_JOBS = 128
TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent", "failed", "cancelled"}


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, obj: Any) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp_name = tmp.name
    Path(temp_name).replace(path)
    return True


def _valid_checkpoint_ref(value: Any) -> str | None:
    if not isinstance(value, str) or len(value) > 512:
        return None
    if not value.startswith(LIBRARY_PENDING_PREFIX) or not value.endswith(".json"):
        return None
    if ".." in Path(value).parts:
        return None
    return value


def _persisted_barriers(repo_root: Path) -> dict[str, str]:
    queue = repo_root / ".survey/work-queue"
    claims_root = queue / "claims"
    jobs_root = queue / "jobs"
    barriers: dict[str, str] = {}
    for path in sorted(claims_root.glob("*.json")) if claims_root.is_dir() else []:
        claim = _read(path)
        if not isinstance(claim, dict):
            continue
        job_id = claim.get("job_id")
        if not isinstance(job_id, str) or not SAFE_ID_RE.fullmatch(job_id) or path.stem != job_id:
            continue
        checkpoint_ref = _valid_checkpoint_ref(claim.get("checkpoint_ref"))
        if checkpoint_ref is None:
            continue
        job = _read(jobs_root / f"{job_id}.json")
        if not isinstance(job, dict) or job.get("job_id") != job_id:
            continue
        if job.get("status") in TERMINAL:
            continue
        if job.get("status") != "ready" or job.get("type") not in {"research", "audit"}:
            continue
        barriers[job_id] = checkpoint_ref
    return barriers


def _request_entries(raw: Any) -> list[dict[str, str]]:
    if not isinstance(raw, list):
        return []
    entries: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in raw:
        if not isinstance(item, dict):
            continue
        job_id = item.get("job_id")
        checkpoint_ref = _valid_checkpoint_ref(item.get("checkpoint_ref"))
        if not isinstance(job_id, str) or not SAFE_ID_RE.fullmatch(job_id) or checkpoint_ref is None:
            continue
        if job_id in seen:
            continue
        seen.add(job_id)
        entries.append({"job_id": job_id, "checkpoint_ref": checkpoint_ref})
    return entries


def _repairable_jobs(repo_root: Path) -> set[str]:
    descriptors = claim_worker._immutable_descriptors(repo_root)
    return claim_worker._repair_jobs_with_only_durable_failures(repo_root, descriptors)


def apply(repo_root: Path) -> dict[str, int]:
    repo_root = Path(repo_root).resolve()
    queue = repo_root / ".survey/work-queue"
    requests_root = queue / "claim-requests"
    results_root = queue / "claim-results"
    barriers = _persisted_barriers(repo_root)
    repairable_jobs = _repairable_jobs(repo_root)
    scanned = changed = protected = skipped_processed = repair_barriers_demoted = 0

    for path in sorted(requests_root.glob("*.json")) if requests_root.is_dir() else []:
        scanned += 1
        if (results_root / path.name).exists():
            skipped_processed += 1
            continue
        request = _read(path)
        if not isinstance(request, dict):
            continue

        raw_entries = _request_entries(request.get("checkpointed_jobs"))
        repair_entries = _request_entries(request.get("repair_checkpointed_jobs"))
        repair_by_job = {item["job_id"]: item for item in repair_entries}
        entries = []
        for item in raw_entries:
            if item["job_id"] in repairable_jobs:
                repair_by_job[item["job_id"]] = item
                repair_barriers_demoted += 1
            else:
                entries.append(item)

        seen = {item["job_id"] for item in entries}
        for job_id in sorted(barriers):
            if job_id in repairable_jobs:
                repair_by_job.setdefault(job_id, {"job_id": job_id, "checkpoint_ref": barriers[job_id]})
                continue
            if job_id in seen:
                continue
            entries.append({"job_id": job_id, "checkpoint_ref": barriers[job_id]})
            seen.add(job_id)
            protected += 1

        if len(entries) > MAX_CHECKPOINTED_JOBS or len(repair_by_job) > MAX_CHECKPOINTED_JOBS:
            raise RuntimeError("checkpoint barrier count exceeds claim contract limit")
        if entries:
            request["checkpointed_jobs"] = entries
        else:
            request.pop("checkpointed_jobs", None)
        if repair_by_job:
            request["repair_checkpointed_jobs"] = [repair_by_job[job_id] for job_id in sorted(repair_by_job)]
        else:
            request.pop("repair_checkpointed_jobs", None)
        if _write(path, request):
            changed += 1

    return {
        "persisted_barriers": len(barriers),
        "repairable_jobs": len(repairable_jobs),
        "requests_scanned": scanned,
        "requests_changed": changed,
        "barriers_merged": protected,
        "repair_barriers_demoted": repair_barriers_demoted,
        # Historical callers used this name before the operation was clarified as
        # demotion-to-provenance rather than deletion. Keep it as a compatibility alias.
        "repair_barriers_cleared": repair_barriers_demoted,
        "processed_requests_skipped": skipped_processed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(apply(args.repo_root), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
