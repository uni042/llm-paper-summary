#!/usr/bin/env python3
"""Build a completed immutable descriptor from the reserved record bank."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from immutable_submission import TRANSPORT_VERSION, validate_descriptor
from record_bank_config import BANK_ROOTS, SLOT_NAMES


def _blob_sha(repo: Path, rel: str) -> str:
    result = subprocess.run(["git", "rev-parse", f"HEAD:{rel}"], cwd=repo, text=True, capture_output=True, check=False)
    sha = result.stdout.strip()
    if result.returncode != 0 or len(sha) != 40:
        raise ValueError(f"record slot must be committed before submission: {rel}")
    return sha


def descriptor_fingerprint(descriptor: dict) -> str:
    """Return a stable digest for the exact validated descriptor candidate."""
    payload = json.dumps(
        descriptor,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _load_preflight_result(repo: Path, preflight_result: Path) -> dict:
    repo = repo.resolve()
    path = Path(preflight_result)
    if not path.is_absolute():
        path = repo / path
    path = path.resolve()
    try:
        relative = path.relative_to(repo).as_posix()
    except ValueError as exc:
        raise ValueError("preflight result must stay within repository") from exc
    if not relative.startswith(".survey/work-queue/research-preflight/results/") or path.suffix != ".json":
        raise ValueError("preflight result must live under research-preflight/results")
    try:
        result = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError) as exc:
        raise ValueError(f"preflight result is unreadable: {relative}") from exc
    if not isinstance(result, dict):
        raise ValueError("preflight result must be a JSON object")
    return result


def _expected_blob_sha_from_preflight(repo: Path, preflight_result: Path, fallback: str | None) -> str | None:
    """Use the exact preflight-bound paper guard when the result records it.

    Older preflight results did not persist this field, so only those legacy
    results may fall back to the completed-request value.
    """
    result = _load_preflight_result(repo, preflight_result)
    if "expected_blob_sha" not in result:
        return fallback
    value = result.get("expected_blob_sha")
    if value in (None, ""):
        return None
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{40}", value):
        raise ValueError("preflight expected_blob_sha must be a 40-character lowercase Git SHA or null")
    return value


def verify_preflight_result(repo: Path, descriptor: dict, preflight_result: Path) -> dict:
    """Require a passing self-preflight for the exact descriptor/slot blobs."""
    result = _load_preflight_result(repo, preflight_result)
    if result.get("operation") != "research_quality_preflight":
        raise ValueError("preflight result operation mismatch")
    if result.get("ok") is not True or result.get("preflight_passed") is not True:
        raise ValueError("preflight has not passed; repair the record and run a new preflight")
    for field in ("kind", "attempt_id", "job_id", "record_bank", "paper_path"):
        if result.get(field) != descriptor.get(field):
            raise ValueError(f"preflight result {field} does not match completed descriptor")
    expected = descriptor_fingerprint(descriptor)
    if result.get("descriptor_sha256") != expected:
        raise ValueError("preflight result is stale: record slots or descriptor fields changed after the check")
    if result.get("record_slots") != descriptor.get("record_slots"):
        raise ValueError("preflight result is stale: record slot blobs changed after the check")
    return result


def build(repo: Path, *, kind: str, attempt_id: str, job_id: str, record_bank: str, paper_path: str | None = None, expected_blob_sha: str | None = None) -> dict:
    repo = repo.resolve()
    bank = record_bank.lower()
    if bank not in BANK_ROOTS:
        raise ValueError("record_bank must be registered")
    root = BANK_ROOTS[bank]
    descriptor = {
        "schema_version": 1,
        "transport_version": TRANSPORT_VERSION,
        "kind": kind,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "status": "completed",
        "record_bank": bank,
        "record_slots": [
            {"slot": slot, "path": f"{root}/{slot}.json", "blob_sha": _blob_sha(repo, f"{root}/{slot}.json")}
            for slot in SLOT_NAMES
        ],
    }
    if paper_path:
        descriptor["paper_path"] = paper_path
    if expected_blob_sha:
        descriptor["expected_blob_sha"] = expected_blob_sha
    return validate_descriptor(repo, descriptor)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--kind", required=True, choices=("research", "audit"))
    parser.add_argument("--attempt-id", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument("--record-bank", required=True)
    parser.add_argument("--paper-path")
    parser.add_argument("--expected-blob-sha")
    parser.add_argument("--preflight-result", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    expected_blob_sha = _expected_blob_sha_from_preflight(
        args.repo_root,
        args.preflight_result,
        args.expected_blob_sha,
    )
    descriptor = build(
        args.repo_root,
        kind=args.kind,
        attempt_id=args.attempt_id,
        job_id=args.job_id,
        record_bank=args.record_bank,
        paper_path=args.paper_path,
        expected_blob_sha=expected_blob_sha,
    )
    verify_preflight_result(args.repo_root, descriptor, args.preflight_result)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(descriptor, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("[WORKER-GUIDE] exact-blob quality preflight verified; completed descriptor validated and written")
    print(json.dumps({
        "ok": True,
        "next_action": "commit_exact_descriptor_then_wait_for_submission_result",
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
