#!/usr/bin/env python3
"""Restore the latest failed immutable record into repair-required claim banks.

Repeated validation failures create more than one failed immutable descriptor for the
same research job. The primary allocator intentionally declines ambiguous descriptor
sets, which used to make a later repair claim fall through to a fresh empty bank. This
post-allocation pass resolves that ambiguity from the job's authoritative repair state
and the latest matching failed immutable result, then restores that exact five-slot
snapshot into the bank already reserved for the new claim.

Library checkpoint provenance is deliberately independent from claim eligibility. A
checkpoint proves that expensive reading is complete; ``repair_required`` may still
make a new claim necessary. ``apply_library_checkpoint_barriers.py`` therefore demotes
such barriers to ``repair_checkpointed_jobs``. This pass copies that provenance onto
the repair claim so downstream workers can distinguish "repair existing research" from
"read the paper again" even though a fresh claim/attempt identity was allocated.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
from typing import Any

import claim_state
import claim_worker_with_banks
import immutable_submission
from record_bank_config import BANK_ROOTS

REPAIR_TIMESTAMP_SKEW = dt.timedelta(seconds=10)
LIBRARY_PENDING_PREFIX = "/LLM-survey-outbox/pending/"


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _time(value: Any) -> dt.datetime | None:
    return claim_state.parse_time(value)


def _repair_checkpoint_ref(root: Path, claim: dict[str, Any]) -> str | None:
    request_id = claim.get("request_id")
    job_id = claim.get("job_id")
    if not isinstance(request_id, str) or not isinstance(job_id, str):
        return None
    request = _read(root / ".survey/work-queue/claim-requests" / f"{request_id}.json", {})
    if not isinstance(request, dict):
        return None
    entries = request.get("repair_checkpointed_jobs")
    if not isinstance(entries, list):
        return None
    for item in entries:
        if not isinstance(item, dict) or item.get("job_id") != job_id:
            continue
        ref = item.get("checkpoint_ref")
        if (
            isinstance(ref, str)
            and len(ref) <= 512
            and ref.startswith(LIBRARY_PENDING_PREFIX)
            and ref.endswith(".json")
            and ".." not in Path(ref).parts
        ):
            return ref
    return None


def _latest_failed_descriptor(root: Path, claim: dict[str, Any]):
    job_id = str(claim.get("job_id") or "")
    kind = str(claim.get("kind") or "research")
    job = _read(root / ".survey/work-queue/jobs" / f"{job_id}.json", {})
    if not isinstance(job, dict) or job.get("repair_required") is not True:
        return None
    if kind not in immutable_submission.KINDS:
        return None

    target_time = _time(job.get("last_validation_failed_at"))
    claim_time = _time(claim.get("claimed_at"))
    submissions = root / ".survey/work-queue/submissions" / kind
    results = root / ".survey/work-queue/results" / kind
    matches = []
    for path in sorted(submissions.glob("*.json")) if submissions.is_dir() else []:
        descriptor = _read(path)
        if not isinstance(descriptor, dict) or descriptor.get("job_id") != job_id:
            continue
        if descriptor.get("status", immutable_submission.COMPLETED_STATUS) != immutable_submission.COMPLETED_STATUS:
            continue
        result = _read(results / path.name)
        if not (
            immutable_submission.result_matches_identity(result, descriptor)
            and isinstance(result, dict)
            and result.get("ok") is False
        ):
            continue
        processed_at = _time(result.get("processed_at"))
        if processed_at is None:
            continue
        if claim_time is not None and processed_at > claim_time:
            continue
        try:
            normalized = immutable_submission.validate_descriptor(root, descriptor)
            payloads = {
                ref["slot"]: immutable_submission.read_record_slot(root, ref)
                for ref in normalized["record_slots"]
            }
        except Exception:
            continue
        matches.append((processed_at, path.relative_to(root).as_posix(), normalized, payloads))

    if not matches:
        return None

    if target_time is not None:
        nearby = [item for item in matches if abs(item[0] - target_time) <= REPAIR_TIMESTAMP_SKEW]
        if not nearby:
            return None
        distance = min(abs(item[0] - target_time) for item in nearby)
        nearest = [item for item in nearby if abs(item[0] - target_time) == distance]
        return nearest[0] if len(nearest) == 1 else None

    latest_time = max(item[0] for item in matches)
    latest = [item for item in matches if item[0] == latest_time]
    return latest[0] if len(latest) == 1 else None


def repair_allocated_claims(repo_root: Path, at: Any = None) -> dict[str, int]:
    root = Path(repo_root).resolve()
    now = _time(at) if at is not None else dt.datetime.now(dt.timezone.utc)
    if now is None:
        raise ValueError("invalid --at timestamp")

    repaired = skipped = checkpoint_provenance = 0
    for job_id, current in sorted(claim_state.current_claims(root, now).items()):
        if not current.get("active"):
            continue
        claim_path = root / ".survey/work-queue/claims" / f"{job_id}.json"
        claim = _read(claim_path)
        if not isinstance(claim, dict) or claim.get("claim_id") != current.get("claim_id"):
            continue
        if claim.get("record_bank_recovery"):
            continue
        bank = str(claim.get("record_bank") or "").lower()
        if bank not in BANK_ROOTS:
            continue

        candidate = _latest_failed_descriptor(root, claim)
        if candidate is None:
            continue
        _processed_at, source_submission, descriptor, payloads = candidate

        untouched = True
        for slot_path in (root / BANK_ROOTS[bank]).glob("*.json"):
            payload = _read(slot_path)
            if not isinstance(payload, dict) or payload.get("data") != {}:
                untouched = False
                break
            reservation = payload.get("reservation")
            if not isinstance(reservation, dict) or reservation.get("claim_id") != claim.get("claim_id"):
                untouched = False
                break
        if not untouched:
            skipped += 1
            continue

        claim_worker_with_banks._recover_bank_payloads(
            root,
            bank,
            claim,
            payloads,
            recovery_kind="repair-required-latest-immutable-descriptor",
            previous_attempts={str(descriptor["attempt_id"])},
            source_submission=source_submission,
        )
        checkpoint_ref = _repair_checkpoint_ref(root, claim)
        if checkpoint_ref is not None:
            claim["checkpoint_ref"] = checkpoint_ref
            claim["checkpoint_repair_source"] = "library-durable-research"
            claim["requires_full_reread"] = False
            checkpoint_provenance += 1
        claim_worker_with_banks._write(claim_path, claim)
        claim_worker_with_banks._persist_assignment_bank(root, claim, bank)
        repaired += 1

    return {
        "repaired": repaired,
        "skipped_nonempty": skipped,
        "checkpoint_provenance_restored": checkpoint_provenance,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--at")
    args = parser.parse_args()
    result = repair_allocated_claims(Path(args.repo_root), at=args.at)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
