#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


TRANSIENT_REMOTE_MARKERS = (
    "internal server error",
    "service unavailable",
    "bad gateway",
    "gateway timeout",
    "http 500",
    "http 502",
    "http 503",
    "http 504",
    "rpc failed",
    "unexpected disconnect",
    "connection reset",
    "connection closed",
    "remote end hung up",
)

CONFLICT_MARKERS = (
    "non-fast-forward",
    "fetch first",
    "failed to update ref",
    "cannot lock ref",
)


def classify_push_failure(output: str) -> str:
    normalized = output.casefold()
    if any(marker in normalized for marker in TRANSIENT_REMOTE_MARKERS):
        return "transient_remote_error"
    if any(marker in normalized for marker in CONFLICT_MARKERS):
        return "push_conflict"
    return "push_failure"


def retry_delay(attempt: int, entropy: str) -> int:
    if attempt < 1:
        raise ValueError("attempt must be >= 1")
    digest = hashlib.sha256(f"{entropy}:{attempt}".encode("utf-8")).digest()
    jitter = digest[0] % 3
    return attempt * 2 + jitter


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Classify a failed git push and calculate a de-synchronized retry delay."
    )
    parser.add_argument("--attempt", required=True, type=int)
    parser.add_argument("--entropy", required=True)
    parser.add_argument("--stderr-file", required=True, type=Path)
    args = parser.parse_args()

    output = args.stderr_file.read_text(encoding="utf-8", errors="replace")
    print(
        classify_push_failure(output),
        retry_delay(args.attempt, args.entropy),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
