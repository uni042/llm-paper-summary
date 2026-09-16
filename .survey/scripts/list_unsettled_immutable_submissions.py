#!/usr/bin/env python3
"""List immutable descriptors that still need a durable successful result.

Successful exact results settle an immutable attempt. Failed exact results remain
settled by default for backward compatibility, but failures explicitly classified as
retryable are returned to the drain queue until the bounded recovery budget is
exhausted. A narrowly-scoped compatibility retry also reopens historical bank-A
path failures after the validator learned the exact legacy alias. Malformed
descriptors are settled only by a failure tombstone bound to the exact descriptor
bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

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


def _matching_failure_is_legacy_bank_a_path_compatibility(
    result: Any,
    descriptor: dict[str, Any],
) -> bool:
    """Reopen only the historical bank-A path mismatch fixed by current code.

    These descriptors were already durably written with valid blob identities but
    used ``chat-record-a`` while bank A's canonical root is ``chat-record``. They
    were classified non-retryable before the validator had explicit read
    compatibility. No other non-retryable transport/state failure is reopened.
    """
    if not isinstance(result, dict):
        return False
    if not immutable_submission.result_matches_identity(result, descriptor):
        return False
    if result.get("ok") is not False:
        return False
    if str(descriptor.get("record_bank") or "").lower() != "a":
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
    root = Path(repo_root).resolve()
    out: list[str] = []
    submissions = root / ".survey/work-queue/submissions"
    results = root / ".survey/work-queue/results"

    for kind in sorted(immutable_submission.KINDS):
        folder = submissions / kind
        for descriptor_path in sorted(folder.glob("*.json")) if folder.is_dir() else []:
            relative = descriptor_path.relative_to(root).as_posix()
            descriptor = _read(descriptor_path)
            result = _read(results / kind / descriptor_path.name)

            if isinstance(descriptor, dict):
                if immutable_submission.result_matches_identity(result, descriptor):
                    if (
                        _matching_failure_is_retryable(result, descriptor)
                        or _matching_failure_is_legacy_bank_a_path_compatibility(result, descriptor)
                    ):
                        out.append(relative)
                    # Exact success, unrelated non-retryable failure, and exhausted
                    # bounded recovery remain settled attempts.
                    continue
            else:
                digest = _digest(descriptor_path)
                if (
                    digest
                    and isinstance(result, dict)
                    and result.get("ok") is False
                    and result.get("submission") == relative
                    and result.get("descriptor_sha256") == digest
                ):
                    continue

            out.append(relative)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    for path in unsettled_paths(args.repo_root):
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
