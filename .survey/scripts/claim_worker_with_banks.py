#!/usr/bin/env python3
"""Allocate queue claims and atomically reserve workflow-v10 record banks.

The existing claim allocator remains authoritative for job ownership. This wrapper
runs inside the serialized ``survey-claim-main`` lane and adds a record-bank
reservation only to claims allocated by the current invocation. A reservation is
encoded as five coherent empty slot envelopes, so existing bank inspection/fallback
code sees the bank as occupied before a worker starts writing research content.

Pre-reservation active claims that still lack persisted bank routing are migrated to
the durable Library fallback. This retires the rollout-era global fence: one legacy
claim no longer disables direct-bank allocation for every unrelated new claim.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
from pathlib import Path
from typing import Any

import claim_state
import claim_worker
import immutable_submission
import select_record_bank
from record_bank_config import BANK_ROOTS, SLOT_NAMES


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp_name = tmp.name
    Path(temp_name).replace(path)


def _as_time(value: Any) -> dt.datetime | None:
    if isinstance(value, dt.datetime):
        return value.astimezone(dt.timezone.utc)
    return claim_state.parse_time(value)


def _active_claim_ids(root: Path, now: dt.datetime) -> set[str]:
    return {
        str(claim.get("claim_id"))
        for claim in claim_state.current_claims(root, now).values()
        if claim.get("active") and claim.get("claim_id")
    }


def _reservation_payload(slot: str, claim: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": slot,
        "attempt_id": claim["attempt_id"],
        "job_id": claim["job_id"],
        "data": {},
        "reservation": {
            "claim_id": claim["claim_id"],
            "worker_id": claim.get("worker_id"),
            "worker_kind": claim.get("worker_kind"),
        },
    }


def _placeholder_payload(slot: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": slot,
        "attempt_id": select_record_bank.PLACEHOLDER_ATTEMPT,
        "job_id": select_record_bank.PLACEHOLDER_ATTEMPT,
        "data": {},
    }


def _reserve_bank(root: Path, bank: str, claim: dict[str, Any]) -> None:
    bank_root = root / BANK_ROOTS[bank]
    for slot in SLOT_NAMES:
        _write(bank_root / f"{slot}.json", _reservation_payload(slot, claim))


def _reclaim_expired_empty_reservations(root: Path, active_claim_ids: set[str]) -> int:
    """Return reservation-only banks to placeholders once their claim is inactive.

    Reclaim only when every slot is still the untouched empty reservation envelope.
    If a worker has written any real slot data, leave the bank alone for explicit
    recovery/inspection instead of guessing that partial research can be discarded.
    """
    reclaimed = 0
    for bank, relative_root in BANK_ROOTS.items():
        bank_root = root / relative_root
        reservation_ids: set[str] = set()
        untouched = True
        for slot in SLOT_NAMES:
            payload = _read(bank_root / f"{slot}.json")
            if not isinstance(payload, dict) or payload.get("data") != {}:
                untouched = False
                break
            reservation = payload.get("reservation")
            if not isinstance(reservation, dict) or not reservation.get("claim_id"):
                untouched = False
                break
            reservation_ids.add(str(reservation["claim_id"]))
        if not untouched or len(reservation_ids) != 1:
            continue
        reservation_id = next(iter(reservation_ids))
        if reservation_id in active_claim_ids:
            continue
        for slot in SLOT_NAMES:
            _write(bank_root / f"{slot}.json", _placeholder_payload(slot))
        reclaimed += 1
    return reclaimed


def _available_bank(root: Path, excluded: set[str]) -> str | None:
    state = select_record_bank.inspect(root)
    for item in state.get("banks", []):
        if not isinstance(item, dict):
            continue
        bank = str(item.get("bank") or "").lower()
        if bank in excluded:
            continue
        if bank in BANK_ROOTS and item.get("state") in {"free", "reusable"}:
            return bank
    return None


def _repair_job(root: Path, claim: dict[str, Any]) -> dict[str, Any] | None:
    job_id = str(claim.get("job_id") or "")
    job = _read(root / ".survey/work-queue/jobs" / f"{job_id}.json", {})
    if not isinstance(job, dict) or job.get("repair_required") is not True:
        return None
    return job


def _repair_bank_candidate(
    root: Path,
    claim: dict[str, Any],
    excluded: set[str],
) -> tuple[str, dict[str, dict[str, Any]], set[str]] | None:
    """Find one coherent retained bank for this repair job, or decline recovery.

    Repair recovery is intentionally conservative: the job must explicitly be in
    ``repair_required`` state, every fixed slot must still belong to that job, and
    exactly one occupied bank may match. Ambiguous or dirty ownership falls back to
    normal allocation rather than guessing which research record is authoritative.
    """
    job_id = str(claim.get("job_id") or "")
    if _repair_job(root, claim) is None:
        return None

    matches: list[tuple[str, dict[str, dict[str, Any]], set[str]]] = []
    state = select_record_bank.inspect(root)
    for item in state.get("banks", []):
        if not isinstance(item, dict) or item.get("state") != "occupied":
            continue
        bank = str(item.get("bank") or "").lower()
        if bank not in BANK_ROOTS or bank in excluded:
            continue

        payloads: dict[str, dict[str, Any]] = {}
        attempts: set[str] = set()
        valid = True
        for slot in SLOT_NAMES:
            payload = _read(root / BANK_ROOTS[bank] / f"{slot}.json")
            if (
                not isinstance(payload, dict)
                or payload.get("slot") != slot
                or payload.get("job_id") != job_id
                or "data" not in payload
            ):
                valid = False
                break
            payloads[slot] = payload
            if payload.get("attempt_id"):
                attempts.add(str(payload["attempt_id"]))
        if valid and len(payloads) == len(SLOT_NAMES):
            matches.append((bank, payloads, attempts))

    return matches[0] if len(matches) == 1 else None


def _repair_descriptor_candidate(
    root: Path,
    claim: dict[str, Any],
) -> tuple[str, dict[str, Any], dict[str, dict[str, Any]], set[str]] | None:
    """Load one unambiguous failed immutable record for a repair job.

    The descriptor/result pair must belong to the same job, carry an exact durable
    failure result, and still resolve all five immutable Git blobs. If more than one
    valid failed descriptor exists, decline recovery rather than guessing which
    research snapshot is authoritative.
    """
    if _repair_job(root, claim) is None:
        return None
    job_id = str(claim.get("job_id") or "")
    kind = str(claim.get("kind") or "research")
    if kind not in immutable_submission.KINDS:
        return None

    submissions = root / ".survey/work-queue/submissions" / kind
    results = root / ".survey/work-queue/results" / kind
    matches: list[tuple[str, dict[str, Any], dict[str, dict[str, Any]], set[str]]] = []
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
        try:
            normalized = immutable_submission.validate_descriptor(root, descriptor)
            payloads = {
                ref["slot"]: immutable_submission.read_record_slot(root, ref)
                for ref in normalized["record_slots"]
            }
        except Exception:
            continue
        attempts = {str(normalized["attempt_id"])}
        matches.append((path.relative_to(root).as_posix(), normalized, payloads, attempts))

    return matches[0] if len(matches) == 1 else None


def _recover_repair_payloads(
    root: Path,
    bank: str,
    claim: dict[str, Any],
    payloads: dict[str, dict[str, Any]],
    *,
    recovery_kind: str,
    previous_attempts: set[str],
    source_submission: str | None = None,
) -> None:
    """Retag retained repair data to the new claim without clearing its content."""
    reservation = {
        "claim_id": claim["claim_id"],
        "worker_id": claim.get("worker_id"),
        "worker_kind": claim.get("worker_kind"),
    }
    for slot in SLOT_NAMES:
        payload = dict(payloads[slot])
        payload["schema_version"] = 1
        payload["transport_version"] = 10
        payload["slot"] = slot
        payload["attempt_id"] = claim["attempt_id"]
        payload["job_id"] = claim["job_id"]
        payload["reservation"] = reservation
        _write(root / BANK_ROOTS[bank] / f"{slot}.json", payload)

    claim["record_bank"] = bank
    claim.pop("record_bank_fallback", None)
    claim["record_bank_recovery"] = recovery_kind
    claim["record_bank_recovery_attempt_ids"] = sorted(previous_attempts)
    if source_submission:
        claim["record_bank_recovery_submission"] = source_submission
    else:
        claim.pop("record_bank_recovery_submission", None)


def _persist_assignment_bank(root: Path, claim: dict[str, Any], bank: str | None) -> None:
    request_id = claim.get("request_id")
    if not isinstance(request_id, str) or not request_id:
        return
    result_path = root / ".survey/work-queue/claim-results" / f"{request_id}.json"
    result = _read(result_path)
    if not isinstance(result, dict):
        return
    assignments = result.get("assignments")
    if not isinstance(assignments, list):
        return
    changed = False
    for item in assignments:
        if not isinstance(item, dict):
            continue
        if item.get("job_id") != claim.get("job_id") or item.get("claim_id") != claim.get("claim_id"):
            continue
        if item.get("record_bank") != bank:
            item["record_bank"] = bank
            changed = True
        if bank is None and item.get("record_bank_fallback") != "library":
            item["record_bank_fallback"] = "library"
            changed = True
        elif bank is not None and "record_bank_fallback" in item:
            item.pop("record_bank_fallback", None)
            changed = True
        for key in (
            "record_bank_recovery",
            "record_bank_recovery_attempt_ids",
            "record_bank_recovery_submission",
        ):
            if key in claim and item.get(key) != claim[key]:
                item[key] = claim[key]
                changed = True
    if changed:
        _write(result_path, result)


def _persist_library_fallback(root: Path, claim: dict[str, Any]) -> None:
    claim_path = root / ".survey/work-queue/claims" / f"{claim['job_id']}.json"
    claim["record_bank"] = None
    claim["record_bank_fallback"] = "library"
    _write(claim_path, claim)
    _persist_assignment_bank(root, claim, None)


def _migrate_active_unbanked_claims(
    root: Path,
    claims: dict[str, dict[str, Any]],
    new_claim_ids: set[str],
) -> int:
    """Route surviving pre-reservation claims to Library without fencing other jobs."""
    migrated = 0
    for job_id in sorted(claims):
        current = claims[job_id]
        if not current.get("active") or current.get("claim_id") in new_claim_ids:
            continue
        if str(current.get("record_bank") or "").lower() in BANK_ROOTS:
            continue
        if current.get("record_bank_fallback") == "library":
            continue

        claim_path = root / ".survey/work-queue/claims" / f"{job_id}.json"
        claim = _read(claim_path)
        if not isinstance(claim, dict) or claim.get("claim_id") != current.get("claim_id"):
            continue
        claim["record_bank"] = None
        claim["record_bank_fallback"] = "library"
        claim["record_bank_migration"] = "legacy-unbanked-to-library"
        _write(claim_path, claim)
        _persist_assignment_bank(root, claim, None)
        current["record_bank"] = None
        current["record_bank_fallback"] = "library"
        current["record_bank_migration"] = "legacy-unbanked-to-library"
        migrated += 1
    return migrated


def reserve_new_claim_banks(
    repo_root: Path,
    *,
    new_claim_ids: set[str],
    at: Any = None,
) -> dict[str, int]:
    root = Path(repo_root).resolve()
    now = _as_time(at) or dt.datetime.now(dt.timezone.utc)
    claims = claim_state.current_claims(root, now)
    active_ids = {
        str(claim.get("claim_id"))
        for claim in claims.values()
        if claim.get("active") and claim.get("claim_id")
    }
    reclaimed = _reclaim_expired_empty_reservations(root, active_ids)
    migrated_unbanked = _migrate_active_unbanked_claims(root, claims, new_claim_ids)
    reserved = reused = recovered = recovered_from_descriptor = fallback = 0

    used = {
        str(claim.get("record_bank")).lower()
        for claim in claims.values()
        if claim.get("active") and str(claim.get("record_bank") or "").lower() in BANK_ROOTS
    }

    for job_id in sorted(claims):
        current = claims[job_id]
        if not current.get("active") or current.get("claim_id") not in new_claim_ids:
            continue
        claim_path = root / ".survey/work-queue/claims" / f"{job_id}.json"
        claim = _read(claim_path)
        if not isinstance(claim, dict):
            continue
        if claim.get("claim_id") != current.get("claim_id"):
            continue

        existing = str(claim.get("record_bank") or "").lower()
        if existing in BANK_ROOTS:
            reused += 1
            _persist_assignment_bank(root, claim, existing)
            continue

        repair = _repair_bank_candidate(root, claim, used)
        if repair is not None:
            bank, payloads, previous_attempts = repair
            _recover_repair_payloads(
                root,
                bank,
                claim,
                payloads,
                recovery_kind="repair-required-same-job",
                previous_attempts=previous_attempts,
            )
            _write(claim_path, claim)
            _persist_assignment_bank(root, claim, bank)
            used.add(bank)
            recovered += 1
            continue

        descriptor_repair = _repair_descriptor_candidate(root, claim)
        if descriptor_repair is not None:
            source_submission, _descriptor, payloads, previous_attempts = descriptor_repair
            bank = _available_bank(root, used)
            if bank is not None:
                _recover_repair_payloads(
                    root,
                    bank,
                    claim,
                    payloads,
                    recovery_kind="repair-required-immutable-descriptor",
                    previous_attempts=previous_attempts,
                    source_submission=source_submission,
                )
                _write(claim_path, claim)
                _persist_assignment_bank(root, claim, bank)
                used.add(bank)
                recovered_from_descriptor += 1
                continue

        bank = _available_bank(root, used)
        if bank is None:
            _persist_library_fallback(root, claim)
            fallback += 1
            continue

        claim["record_bank"] = bank
        claim.pop("record_bank_fallback", None)
        _reserve_bank(root, bank, claim)
        _write(claim_path, claim)
        _persist_assignment_bank(root, claim, bank)
        used.add(bank)
        reserved += 1

    return {
        "reserved": reserved,
        "reused": reused,
        "recovered": recovered,
        "recovered_from_descriptor": recovered_from_descriptor,
        "fallback": fallback,
        "reclaimed": reclaimed,
        "migrated_unbanked": migrated_unbanked,
    }


def process_requests(repo_root: Path, at: Any = None) -> dict[str, int]:
    root = Path(repo_root).resolve()
    now = _as_time(at) or dt.datetime.now(dt.timezone.utc)
    before_claim_ids = _active_claim_ids(root, now)
    result = claim_worker.process_requests(root, at=now)
    after_claim_ids = _active_claim_ids(root, now)
    bank_result = reserve_new_claim_banks(
        root,
        new_claim_ids=after_claim_ids - before_claim_ids,
        at=now,
    )
    return {**result, **{f"banks_{key}": value for key, value in bank_result.items()}}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()
    result = process_requests(Path(args.repo_root))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
