#!/usr/bin/env python3
"""Allocate queue claims and atomically reserve workflow-v10 record banks.

The existing claim allocator remains authoritative for job ownership. This wrapper
runs inside the serialized ``survey-claim-main`` lane and adds a record-bank
reservation to each newly active research/audit claim. A reservation is encoded as
five coherent empty slot envelopes, so existing bank inspection/fallback code sees
the bank as occupied before a worker starts writing research content.
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


def _reserve_bank(root: Path, bank: str, claim: dict[str, Any]) -> None:
    bank_root = root / BANK_ROOTS[bank]
    for slot in SLOT_NAMES:
        _write(bank_root / f"{slot}.json", _reservation_payload(slot, claim))


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
    if changed:
        _write(result_path, result)


def reserve_active_claim_banks(repo_root: Path, at: Any = None) -> dict[str, int]:
    root = Path(repo_root).resolve()
    now = _as_time(at) or dt.datetime.now(dt.timezone.utc)
    claims = claim_state.current_claims(root, now)
    reserved = reused = fallback = 0

    used = {
        str(claim.get("record_bank")).lower()
        for claim in claims.values()
        if claim.get("active") and str(claim.get("record_bank") or "").lower() in BANK_ROOTS
    }

    for job_id in sorted(claims):
        current = claims[job_id]
        if not current.get("active"):
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

        bank = _available_bank(root, used)
        if bank is None:
            claim["record_bank"] = None
            claim["record_bank_fallback"] = "library"
            _write(claim_path, claim)
            _persist_assignment_bank(root, claim, None)
            fallback += 1
            continue

        claim["record_bank"] = bank
        claim.pop("record_bank_fallback", None)
        _reserve_bank(root, bank, claim)
        _write(claim_path, claim)
        _persist_assignment_bank(root, claim, bank)
        used.add(bank)
        reserved += 1

    return {"reserved": reserved, "reused": reused, "fallback": fallback}


def process_requests(repo_root: Path, at: Any = None) -> dict[str, int]:
    result = claim_worker.process_requests(repo_root, at=at)
    bank_result = reserve_active_claim_banks(repo_root, at=at)
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
