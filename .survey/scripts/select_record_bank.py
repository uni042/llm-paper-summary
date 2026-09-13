#!/usr/bin/env python3
"""Inspect reusable workflow-v10 record banks and choose a safe direct-write bank.

This script is advisory for the Chat worker. Bank exhaustion is never a reason
for STOP_RUN when the complete payload can be durably checkpointed to ChatGPT Library.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import immutable_submission  # noqa: E402
from record_bank_config import BANK_IDS, BANK_ROOTS, SLOT_NAMES  # noqa: E402

PLACEHOLDER_ATTEMPT = "unused-bank-placeholder"
INBOX = Path(".survey/work-queue/submissions/chat-inbox.json")
RESULT = Path(".survey/work-queue/results/chat-inbox.json")
NEXT_JOBS = Path(".survey/work-queue/next-jobs.json")

SlotCapture = tuple[str, str, str, str]
Pair = tuple[str, str]


def read_object(path: Path) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None
    return value if isinstance(value, dict) else None


def ready_job_ids(repo_root: Path) -> set[str]:
    jobs_root = repo_root / ".survey/work-queue/jobs"
    ids: set[str] = set()
    if jobs_root.is_dir():
        for path in jobs_root.glob("*.json"):
            job = read_object(path)
            if isinstance(job, dict) and job.get("status") == "ready" and job.get("job_id"):
                ids.add(str(job["job_id"]))
        return ids
    value = read_object(repo_root / NEXT_JOBS)
    jobs = value.get("next_jobs") if value else None
    return {str(job.get("job_id")) for job in jobs or [] if isinstance(job, dict) and job.get("job_id")}


def current_transport(repo_root: Path) -> tuple[dict[str, Any] | None, bool]:
    inbox = read_object(repo_root / INBOX)
    result = read_object(repo_root / RESULT)
    if not inbox or not inbox.get("job_id"):
        return inbox, True
    settled = bool(result and result.get("job_id") == inbox.get("job_id"))
    return inbox, settled


def pending_immutable_bank_owners(repo_root: Path) -> dict[str, set[Pair]]:
    """Return unresolved immutable descriptors for diagnostics only."""
    owners: dict[str, set[Pair]] = {}
    submissions = repo_root / ".survey/work-queue/submissions"
    results = repo_root / ".survey/work-queue/results"
    for kind in ("research", "audit"):
        root = submissions / kind
        for path in sorted(root.glob("*.json")) if root.is_dir() else []:
            descriptor = read_object(path)
            if not descriptor:
                continue
            attempt_id = str(descriptor.get("attempt_id") or "")
            job_id = str(descriptor.get("job_id") or "")
            bank = str(descriptor.get("record_bank") or "").lower()
            if bank not in BANK_ROOTS or not attempt_id or not job_id:
                continue
            result = read_object(results / kind / path.name)
            if result and result.get("attempt_id") == attempt_id and result.get("job_id") == job_id:
                continue
            owners.setdefault(bank, set()).add((attempt_id, job_id))
    return owners


def immutable_descriptor_candidates(repo_root: Path) -> dict[Pair, list[dict[str, Any]]]:
    """Index immutable descriptors by attempt/job without trusting them yet."""
    out: dict[Pair, list[dict[str, Any]]] = {}
    submissions = repo_root / ".survey/work-queue/submissions"
    for kind in ("research", "audit"):
        root = submissions / kind
        for path in sorted(root.glob("*.json")) if root.is_dir() else []:
            descriptor = read_object(path)
            if not descriptor:
                continue
            bank = str(descriptor.get("record_bank") or "").lower()
            attempt_id = str(descriptor.get("attempt_id") or "")
            job_id = str(descriptor.get("job_id") or "")
            if bank not in BANK_ROOTS or not attempt_id or not job_id:
                continue
            candidate = dict(descriptor)
            candidate["_path"] = path.relative_to(repo_root).as_posix()
            out.setdefault((attempt_id, job_id), []).append(candidate)
    return out


def scan_bank(repo_root: Path, bank: str) -> dict[str, Any]:
    """Read current worktree slot identities and exact Git-style blob SHAs."""
    root = repo_root / BANK_ROOTS[bank]
    slots: list[dict[str, Any]] = []
    attempts: set[str] = set()
    jobs: set[str] = set()
    pairs: set[Pair] = set()
    captures: set[SlotCapture] = set()
    missing = False
    incomplete_identity = False

    for slot in SLOT_NAMES:
        path = root / f"{slot}.json"
        try:
            raw = path.read_bytes()
            payload = json.loads(raw.decode("utf-8"))
        except (FileNotFoundError, OSError, UnicodeError, json.JSONDecodeError):
            missing = True
            slots.append({"slot": slot, "state": "missing_or_invalid"})
            continue
        if not isinstance(payload, dict):
            missing = True
            slots.append({"slot": slot, "state": "missing_or_invalid"})
            continue

        attempt_id = str(payload.get("attempt_id") or "")
        job_id = str(payload.get("job_id") or "")
        blob_sha = immutable_submission.git_blob_sha(raw)
        if not attempt_id or not job_id:
            incomplete_identity = True
        if attempt_id:
            attempts.add(attempt_id)
        if job_id:
            jobs.add(job_id)
        if attempt_id and job_id:
            pair = (attempt_id, job_id)
            pairs.add(pair)
            captures.add((attempt_id, job_id, slot, blob_sha))
        slots.append({
            "slot": slot,
            "attempt_id": attempt_id,
            "job_id": job_id,
            "blob_sha": blob_sha,
        })

    return {
        "bank": bank,
        "root": BANK_ROOTS[bank],
        "slots": slots,
        "attempts": attempts,
        "jobs": jobs,
        "pairs": pairs,
        "captures": captures,
        "missing": missing,
        "incomplete_identity": incomplete_identity,
    }


def durable_slot_captures(
    repo_root: Path,
    candidates: dict[Pair, list[dict[str, Any]]],
    needed_pairs: set[Pair],
) -> set[SlotCapture]:
    """Return exact slot blobs protected by transport-valid immutable descriptors.

    Capture is path-independent after commit: a descriptor staged through bank A may
    protect a byte-identical duplicate currently sitting in bank G. Conversely, an
    edited repair slot under the same attempt/job is not protected until a new
    descriptor references that exact new blob SHA.
    """
    captured: set[SlotCapture] = set()
    for pair in sorted(needed_pairs):
        for candidate in candidates.get(pair, []):
            candidate = {key: value for key, value in candidate.items() if key != "_path"}
            try:
                validated = immutable_submission.validate_descriptor(repo_root, candidate)
            except (ValueError, OSError):
                continue
            if (validated.get("attempt_id"), validated.get("job_id")) != pair:
                continue
            for ref in validated.get("record_slots", []):
                slot = str(ref.get("slot") or "")
                blob_sha = str(ref.get("blob_sha") or "")
                if slot in SLOT_NAMES and blob_sha:
                    captured.add((pair[0], pair[1], slot, blob_sha))
    return captured


def inspect_bank(
    scan: dict[str, Any],
    ready_ids: set[str],
    inbox: dict[str, Any] | None,
    settled: bool,
    durable_slots: set[SlotCapture],
) -> dict[str, Any]:
    bank = str(scan["bank"])
    attempts: set[str] = scan["attempts"]
    jobs: set[str] = scan["jobs"]
    pairs: set[Pair] = scan["pairs"]
    current_slots: set[SlotCapture] = scan["captures"]
    all_slots_durable = bool(current_slots) and len(current_slots) == len(SLOT_NAMES) and current_slots <= durable_slots

    if scan["missing"]:
        state = "dirty"
        reason = "one or more slot files are missing/invalid"
    elif attempts == {PLACEHOLDER_ATTEMPT}:
        # Older pre-created banks intentionally omitted job_id. Keep that legacy
        # placeholder format free rather than treating the missing job identity as dirt.
        state = "free"
        reason = "unused pre-created bank"
    elif scan["incomplete_identity"]:
        state = "dirty"
        reason = "one or more slot files lack attempt/job identifiers"
    elif len(attempts) != 1 or len(jobs) != 1:
        if all_slots_durable:
            state = "reusable"
            reason = "mixed worktree is fully covered by durable immutable slot blobs"
        else:
            state = "dirty"
            reason = "slot attempt/job identifiers are mixed without complete immutable blob coverage"
    else:
        attempt_id = next(iter(attempts))
        job_id = next(iter(jobs))
        active_here = bool(
            inbox
            and str(inbox.get("record_bank") or "a").lower() == bank
            and inbox.get("attempt_id") == attempt_id
            and inbox.get("job_id") == job_id
        )
        if all_slots_durable:
            state = "reusable"
            reason = "all current slot blobs are durably captured by immutable descriptors"
        elif active_here and not settled:
            state = "occupied"
            reason = "current reusable inbox still references this attempt without a matching result"
        elif job_id in ready_ids:
            state = "occupied"
            reason = "bank belongs to a job that is still ready/incomplete in next-jobs"
        else:
            state = "reusable"
            reason = "coherent old attempt is not an active/ready job"

    return {
        "bank": bank,
        "root": scan["root"],
        "state": state,
        "reason": reason,
        "slots": scan["slots"],
    }


def inspect(repo_root: Path) -> dict[str, Any]:
    ready_ids = ready_job_ids(repo_root)
    inbox, settled = current_transport(repo_root)
    pending_owners = pending_immutable_bank_owners(repo_root)
    scans = [scan_bank(repo_root, bank) for bank in BANK_IDS]
    needed_pairs = {pair for scan in scans for pair in scan["pairs"]}
    candidates = immutable_descriptor_candidates(repo_root)
    durable_slots = durable_slot_captures(repo_root, candidates, needed_pairs)
    banks = [inspect_bank(scan, ready_ids, inbox, settled, durable_slots) for scan in scans]
    selectable = [b["bank"] for b in banks if b["state"] in {"free", "reusable"}]
    return {
        "schema_version": 1,
        "selected_bank": selectable[0] if selectable else None,
        "direct_bank_available": bool(selectable),
        "if_no_bank": "checkpoint complete logical payload to ChatGPT Library and continue; bank exhaustion is not STOP_RUN",
        "ready_job_ids": sorted(ready_ids),
        "current_inbox_job_id": inbox.get("job_id") if inbox else None,
        "current_inbox_settled": settled,
        "pending_immutable_banks": sorted(pending_owners),
        "banks": banks,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()
    result = inspect(Path(args.repo_root).resolve())
    print(json.dumps(result, ensure_ascii=False, indent=None if args.compact else 2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
