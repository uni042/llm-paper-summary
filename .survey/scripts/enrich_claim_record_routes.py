#!/usr/bin/env python3
"""Publish exact canonical record-bank paths into active claims and claim results.

Workers must not derive physical record paths from logical bank ids. Bank A is the
important counterexample: its canonical root is ``chat-record`` rather than
``chat-record-a``. This script makes the route explicit in the durable assignment
contract while leaving Library fallback assignments path-free.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import tempfile
from pathlib import Path
from typing import Any

import claim_state
from record_bank_config import BANK_ROOTS, canonical_slot_paths


def _read(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None


def _write(path: Path, value: Any) -> bool:
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    try:
        if path.read_text(encoding="utf-8") == text:
            return False
    except OSError:
        pass
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as tmp:
        tmp.write(text)
        temp_name = tmp.name
    Path(temp_name).replace(path)
    return True


def _apply_route(target: dict[str, Any], bank: str | None) -> bool:
    changed = False
    normalized = str(bank or "").lower()
    if normalized in BANK_ROOTS:
        root = BANK_ROOTS[normalized]
        paths = canonical_slot_paths(normalized)
        desired = {
            "record_bank": normalized,
            "record_bank_root": root,
            "record_slot_paths": paths,
        }
        for key, value in desired.items():
            if target.get(key) != value:
                target[key] = value
                changed = True
        if "record_bank_fallback" in target:
            target.pop("record_bank_fallback", None)
            changed = True
    else:
        for key in ("record_bank_root", "record_slot_paths"):
            if key in target:
                target.pop(key, None)
                changed = True
    return changed


def _is_active(claim: dict[str, Any], now: dt.datetime) -> bool:
    expires = claim_state.parse_time(claim.get("expires_at"))
    if expires is None:
        return False
    return expires > now


def enrich_routes(repo_root: Path, *, at: dt.datetime | None = None) -> dict[str, int]:
    root = Path(repo_root).resolve()
    now = at.astimezone(dt.timezone.utc) if at is not None else dt.datetime.now(dt.timezone.utc)
    claims_dir = root / ".survey/work-queue/claims"
    results_dir = root / ".survey/work-queue/claim-results"

    claims_changed = 0
    results_changed = 0
    assignments_changed = 0

    for claim_path in sorted(claims_dir.glob("*.json")) if claims_dir.is_dir() else []:
        claim = _read(claim_path)
        if not isinstance(claim, dict) or not _is_active(claim, now):
            continue
        job_id = claim.get("job_id")
        claim_id = claim.get("claim_id")
        request_id = claim.get("request_id")
        if not all(isinstance(value, str) and value for value in (job_id, claim_id, request_id)):
            continue

        bank = str(claim.get("record_bank") or "").lower()
        if bank not in BANK_ROOTS:
            bank = None
        if _apply_route(claim, bank) and _write(claim_path, claim):
            claims_changed += 1

        result_path = results_dir / f"{request_id}.json"
        result = _read(result_path)
        if not isinstance(result, dict) or not isinstance(result.get("assignments"), list):
            continue

        result_dirty = False
        for assignment in result["assignments"]:
            if not isinstance(assignment, dict):
                continue
            if assignment.get("job_id") != job_id or assignment.get("claim_id") != claim_id:
                continue
            if _apply_route(assignment, bank):
                assignments_changed += 1
                result_dirty = True
        if result_dirty and _write(result_path, result):
            results_changed += 1

    return {
        "claims_changed": claims_changed,
        "claim_results_changed": results_changed,
        "assignments_changed": assignments_changed,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(enrich_routes(args.repo_root), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
