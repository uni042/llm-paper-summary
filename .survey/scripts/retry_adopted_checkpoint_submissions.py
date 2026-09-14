#!/usr/bin/env python3
"""Retry stale Library fallback attempts through the claim that adopted their checkpoint.

A historical Library envelope can be archived after its original immutable descriptor
fails claim fencing because the job was re-claimed before recovery.  Claim recovery
records the original Library path in the newer released claim's ``checkpoint_ref``.
That pointer is the durable proof that the newer claim adopted the already-read record.

This helper never weakens immutable processor claim fencing.  Instead it rebinds only
the transport identity (attempt/claim/worker) of the archived five-slot payload to the
newer adopting claim, materializes a fresh immutable descriptor, records provenance
back to the source Library envelope, pins the exact slot blobs, and publishes it.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

import drain_fallback_recovery as recovery
import process_immutable_submission_batch as submission_batch
import replay_record_fallback as replay

QUEUE = Path(".survey/work-queue")
LIBRARY_PENDING_PREFIX = "/LLM-survey-outbox/pending/"
TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent"}
STALE_ERROR = "stale attempt:"


def _read(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None
    return value if isinstance(value, dict) else None


def _archive_from_checkpoint(repo_root: Path, checkpoint_ref: Any) -> Path | None:
    if not isinstance(checkpoint_ref, str) or not checkpoint_ref.startswith(LIBRARY_PENDING_PREFIX):
        return None
    name = checkpoint_ref[len(LIBRARY_PENDING_PREFIX):]
    if not name or "/" in name or "\\" in name or not name.endswith(".json"):
        return None
    path = repo_root / QUEUE / "fallback-archive" / name
    return path if path.is_file() else None


def _source_matches_descriptor(
    envelope: dict[str, Any],
    descriptor: dict[str, Any],
) -> bool:
    for key in ("job_id", "attempt_id", "kind"):
        if envelope.get(key) != descriptor.get(key):
            return False
    for key in ("claim_id", "worker_id"):
        expected = descriptor.get(key)
        if expected is not None and envelope.get(key) != expected:
            return False
    return True


def eligible_adoptions(repo_root: Path) -> list[dict[str, Any]]:
    """Return stale failed descriptors whose newer released claim adopted the source checkpoint."""
    repo_root = Path(repo_root).resolve()
    rows: list[dict[str, Any]] = []
    for kind in ("audit", "research"):
        results_dir = repo_root / QUEUE / "results" / kind
        if not results_dir.is_dir():
            continue
        for result_path in sorted(results_dir.glob("*.json")):
            result = _read(result_path)
            if not result or result.get("ok") is not False:
                continue
            error = result.get("error")
            if not isinstance(error, str) or STALE_ERROR not in error:
                continue

            descriptor_path = repo_root / QUEUE / "submissions" / kind / result_path.name
            descriptor = _read(descriptor_path)
            if not descriptor:
                continue
            if (
                descriptor.get("job_id") != result.get("job_id")
                or descriptor.get("attempt_id") != result.get("attempt_id")
                or descriptor.get("kind") != kind
            ):
                continue

            job_id = descriptor.get("job_id")
            if not isinstance(job_id, str) or not job_id:
                continue
            job = _read(repo_root / QUEUE / "jobs" / f"{job_id}.json")
            if not job or job.get("status") in TERMINAL:
                continue

            claim = _read(repo_root / QUEUE / "claims" / f"{job_id}.json")
            if not claim or not claim.get("released_at") or claim.get("lease_invalidated_at"):
                continue
            new_attempt = claim.get("attempt_id")
            new_claim = claim.get("claim_id")
            new_worker = claim.get("worker_id")
            if not all(isinstance(value, str) and value for value in (new_attempt, new_claim, new_worker)):
                continue
            if new_attempt == descriptor.get("attempt_id"):
                continue

            archive_path = _archive_from_checkpoint(repo_root, claim.get("checkpoint_ref"))
            if archive_path is None:
                continue
            envelope = _read(archive_path)
            if not envelope or not _source_matches_descriptor(envelope, descriptor):
                continue
            expected_ref = f"{LIBRARY_PENDING_PREFIX}{envelope.get('id')}.json"
            if claim.get("checkpoint_ref") != expected_ref:
                continue

            rows.append(
                {
                    "kind": kind,
                    "job_id": job_id,
                    "source_attempt_id": descriptor.get("attempt_id"),
                    "source_descriptor": descriptor_path,
                    "source_result": result_path,
                    "source_envelope": envelope,
                    "source_archive": archive_path,
                    "claim": claim,
                }
            )
    return rows


def rebind_envelope(envelope: dict[str, Any], claim: dict[str, Any]) -> dict[str, Any]:
    """Copy a five-slot fallback and replace only transport ownership with the adopting claim."""
    rebound = copy.deepcopy(envelope)
    job_id = str(envelope["job_id"])
    attempt_id = str(claim["attempt_id"])
    rebound["claim_id"] = str(claim["claim_id"])
    rebound["worker_id"] = str(claim["worker_id"])
    rebound["attempt_id"] = attempt_id
    if isinstance(claim.get("worker_kind"), str) and claim.get("worker_kind"):
        rebound["worker_kind"] = claim["worker_kind"]

    for write in rebound.get("writes") or []:
        if not isinstance(write, dict):
            continue
        path = write.get("path")
        content = write.get("content")
        if not isinstance(path, str) or not any(path.startswith(prefix) for prefix in replay.BANK_PATH_PREFIXES):
            continue
        if not isinstance(content, str):
            continue
        payload = json.loads(content)
        if not isinstance(payload, dict):
            continue
        payload["job_id"] = job_id
        payload["attempt_id"] = attempt_id
        reservation = payload.get("reservation")
        if isinstance(reservation, dict):
            reservation["claim_id"] = rebound["claim_id"]
            reservation["worker_id"] = rebound["worker_id"]
            reservation["attempt_id"] = attempt_id
        write["content"] = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    return rebound


def _annotate_descriptor(
    repo_root: Path,
    descriptor_path: str,
    source_envelope: dict[str, Any],
) -> None:
    path = repo_root / descriptor_path
    descriptor = _read(path)
    if descriptor is None:
        raise ValueError(f"rebound descriptor is missing: {descriptor_path}")
    descriptor["source_fallback_envelope_id"] = source_envelope["id"]
    descriptor["source_attempt_id"] = source_envelope["attempt_id"]
    if source_envelope.get("claim_id"):
        descriptor["source_claim_id"] = source_envelope["claim_id"]
    path.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def retry_one(repo_root: Path, row: dict[str, Any], *, parallelism: int = 4) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    rebound = rebind_envelope(row["source_envelope"], row["claim"])
    materialized = replay.materialize(repo_root, rebound)
    if materialized.get("action") != "materialized":
        return {
            "job_id": row["job_id"],
            "source_attempt_id": row["source_attempt_id"],
            "action": materialized.get("action"),
            "reason": materialized.get("reason"),
        }
    descriptor = materialized.get("descriptor")
    if not isinstance(descriptor, str) or not descriptor:
        raise ValueError("rebound replay did not return a descriptor")
    _annotate_descriptor(repo_root, descriptor, row["source_envelope"])
    changed = list(materialized.get("changed_paths") or [])
    if descriptor not in changed:
        changed.append(descriptor)
    recovery.pin_materialized_record(
        repo_root,
        {
            "envelope_id": f"rebind-{row['source_envelope']['id']}-{row['claim']['attempt_id']}",
            "changed_paths": changed,
        },
    )
    settled = recovery.settle_descriptor(repo_root, descriptor, parallelism=parallelism)
    return {
        "job_id": row["job_id"],
        "source_attempt_id": row["source_attempt_id"],
        "attempt_id": row["claim"]["attempt_id"],
        "descriptor": descriptor,
        "action": "retried",
        "failures": int(settled.get("failures", 0) or 0),
    }


def run(repo_root: Path, *, max_items: int = 200, parallelism: int = 4) -> dict[str, Any]:
    repo_root = Path(repo_root).resolve()
    if max_items < 1:
        raise ValueError("max_items must be >= 1")
    selected = eligible_adoptions(repo_root)
    rows: list[dict[str, Any]] = []
    for row in selected[:max_items]:
        rows.append(retry_one(repo_root, row, parallelism=parallelism))
    return {
        "eligible": len(selected),
        "processed": len(rows),
        "failures": sum(int(row.get("failures", 0) or 0) for row in rows),
        "results": rows,
        "limit_reached": len(selected) > max_items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-items", type=int, default=200)
    parser.add_argument("--parallelism", type=int, default=4)
    args = parser.parse_args()
    summary = run(args.repo_root, max_items=args.max_items, parallelism=args.parallelism)
    print(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    return 1 if summary["failures"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
