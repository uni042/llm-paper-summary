#!/usr/bin/env python3
"""List immutable descriptors that still need a durable successful result.

Successful exact results settle an immutable attempt. Failed exact results remain
settled by default for backward compatibility, but failures explicitly classified as
retryable are returned to the drain queue until the bounded recovery budget is
exhausted. A narrowly-scoped compatibility retry also reopens historical bank-A
path failures after the validator learned the exact legacy alias, but only while the
same attempt still owns an active claim. Malformed descriptors are settled only by
a failure tombstone bound to the exact descriptor bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import claim_state
import immutable_submission
from record_bank_config import LEGACY_BANK_ROOTS, SLOT_NAMES

MAX_AUTO_RECOVERY_FAILURES = 3


def _read(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return None


def _digest(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _matching_failure_is_retryable(result: Any, descriptor: dict[str, Any]) -> bool:
    if not isinstance(result, dict):
        return False
    if not immutable_submission.result_matches_identity(result, descriptor):
        return False
    if result.get("ok") is not False or result.get("retryable") is not True:
        return False
    failures = result.get("recovery_failures", 0)
    if isinstance(failures, bool) or not isinstance(failures, int):
        return False
    return 0 <= failures < MAX_AUTO_RECOVERY_FAILURES


def _descriptor_owns_current_claim(
    descriptor: dict[str, Any],
    current_claims: dict[str, dict[str, Any]],
) -> bool:
    job_id = descriptor.get("job_id")
    attempt_id = descriptor.get("attempt_id")
    if not isinstance(job_id, str) or not job_id:
        return False
    if not isinstance(attempt_id, str) or not attempt_id:
        return False
    claim = current_claims.get(job_id)
    return bool(
        isinstance(claim, dict)
        and claim.get("active") is True
        and claim.get("attempt_id") == attempt_id
    )


def _matching_failure_is_legacy_bank_a_path_compatibility(
    result: Any,
    descriptor: dict[str, Any],
    current_claims: dict[str, dict[str, Any]],
) -> bool:
    """Reopen only the historical bank-A path mismatch for its active attempt.

    These descriptors were already durably written with valid blob identities but
    used ``chat-record-a`` while bank A's canonical root is ``chat-record``. They
    were classified non-retryable before the validator had explicit read
    compatibility. Once ownership moves to another attempt, the claim expires, or
    the job becomes terminal, the historical descriptor remains settled. No other
    non-retryable transport/state failure is reopened.
    """
    if not isinstance(result, dict):
        return False
    if not immutable_submission.result_matches_identity(result, descriptor):
        return False
    if result.get("ok") is not False:
        return False
    if str(descriptor.get("record_bank") or "").lower() != "a":
        return False
    if not _descriptor_owns_current_claim(descriptor, current_claims):
        return False

    legacy_root = LEGACY_BANK_ROOTS.get("a")
    refs = descriptor.get("record_slots")
    if not legacy_root or not isinstance(refs, list) or len(refs) != len(SLOT_NAMES):
        return False
    for slot, ref in zip(SLOT_NAMES, refs):
        if not isinstance(ref, dict):
            return False
        if ref.get("slot") != slot or ref.get("path") != f"{legacy_root}/{slot}.json":
            return False

    error = str(result.get("error") or "")
    return (
        "must use fixed path .survey/work-queue/records/chat-record/" in error
        and "slot " in error
    )


def unsettled_paths(repo_root: Path) -> list[str]:
    """List descriptors that still need processing without duplicating one attempt.

    Normally one claim attempt produces one immutable descriptor. A worker may,
    however, durably write a corrected descriptor before a previous retryable
    descriptor for the same job/attempt has been drained. Feeding both paths to
    the batch processor is unsafe and used to abort the whole fast lane.

    Recovery rule:
    - any exact successful result settles every descriptor for that job/attempt;
    - when exactly one descriptor for the identity has no exact result yet, process
      that descriptor and suppress older retryable-failure siblings for this drain;
    - otherwise preserve the old retry rules. Truly ambiguous multiple unresolved
      descriptors are deliberately returned together so the batch guard still fails
      loudly instead of guessing an order.
    """
    root = Path(repo_root).resolve()
    submissions = root / ".survey/work-queue/submissions"
    results = root / ".survey/work-queue/results"
    current_claims = claim_state.current_claims(root)

    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = {}
    ungrouped: list[str] = []

    for kind in sorted(immutable_submission.KINDS):
        folder = submissions / kind
        for descriptor_path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
            relative = descriptor_path.relative_to(root).as_posix()
            descriptor = _read(descriptor_path)
            result = _read(results / kind / descriptor_path.name)

            if not isinstance(descriptor, dict):
                digest = _digest(descriptor_path)
                if (
                    digest
                    and isinstance(result, dict)
                    and result.get("ok") is False
                    and result.get("submission") == relative
                    and result.get("descriptor_sha256") == digest
                ):
                    continue
                ungrouped.append(relative)
                continue

            job_id = descriptor.get("job_id")
            attempt_id = descriptor.get("attempt_id")
            if not isinstance(job_id, str) or not job_id or not isinstance(attempt_id, str) or not attempt_id:
                ungrouped.append(relative)
                continue

            state = "pending"
            if immutable_submission.result_matches_identity(result, descriptor):
                if isinstance(result, dict) and result.get("ok") is True:
                    state = "success"
                elif (
                    _matching_failure_is_retryable(result, descriptor)
                    or _matching_failure_is_legacy_bank_a_path_compatibility(
                        result,
                        descriptor,
                        current_claims,
                    )
                ):
                    state = "retryable_failure"
                else:
                    state = "settled_failure"

            grouped.setdefault((kind, job_id, attempt_id), []).append(
                {"path": relative, "state": state}
            )

    out: list[str] = list(ungrouped)
    for _identity, rows in sorted(grouped.items()):
        if any(row["state"] == "success" for row in rows):
            continue

        pending = [row["path"] for row in rows if row["state"] == "pending"]
        retryable = [row["path"] for row in rows if row["state"] == "retryable_failure"]

        if len(pending) == 1:
            out.append(pending[0])
            continue
        if len(pending) > 1:
            out.extend(pending)
            continue

        if len(retryable) == 1:
            out.append(retryable[0])
        elif len(retryable) > 1:
            out.extend(retryable)

    return sorted(out)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    for path in unsettled_paths(args.repo_root):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
