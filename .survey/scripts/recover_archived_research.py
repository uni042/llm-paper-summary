#!/usr/bin/env python3
"""Recover one archived research envelope whose completed job lacks its paper.

Fallback recovery may encounter an old queue job marked completed even though its
canonical Markdown artifact was never materialized. Such an envelope must not be
lost merely because the queue state is terminal. This helper replays one archived
complete research bundle through a currently safe record bank, leaves the
immutable archive untouched, and transiently reopens that exact job so the normal
queue worker can apply the missing artifact.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import fallback_transport as ft


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def reopen_missing_artifact_job(repo_root: Path, job_id: str, paper_path: str) -> None:
    job_path = repo_root / ".survey" / "work-queue" / "jobs" / f"{job_id}.json"
    job = ft.read_object(job_path)
    if not job or job.get("status") != "completed":
        raise ValueError(f"recovery job is not completed: {job_id}")
    if (repo_root / paper_path).is_file():
        raise ValueError(f"recovery paper already exists: {paper_path}")

    job["status"] = "ready"
    job.pop("completed_at", None)
    job.pop("artifact_submission", None)
    job["artifact_recovery"] = {
        "reason": "completed_job_missing_canonical_paper",
        "paper_path": paper_path,
    }
    write_json(job_path, job)

    # The earlier terminal transition already incremented this counter. Rewind
    # one count so the normal queue worker's successful completion restores the
    # same aggregate rather than double-counting the recovered job.
    state_path = repo_root / ".survey" / "work-queue" / "state.json"
    state = ft.read_object(state_path)
    if state:
        stats = state.get("stats")
        if isinstance(stats, dict):
            current = stats.get("research_completed")
            if isinstance(current, int) and current > 0:
                stats["research_completed"] = current - 1
                write_json(state_path, state)


def recover(repo_root: Path) -> dict:
    repo_root = repo_root.resolve()
    archive = repo_root / ft.FALLBACK_ARCHIVE
    if not archive.is_dir():
        return {"action": "idle", "reason": "archive_missing"}

    for source in sorted(archive.glob("*.json")):
        try:
            envelope, _canonical = ft.parse_envelope(source.read_bytes())
        except Exception:
            continue
        if not ft.has_record_slots(envelope):
            continue
        payload = ft.chat_payload(envelope)
        if not payload:
            continue
        job_id = payload.get("job_id")
        paper_path = payload.get("paper_path")
        if not isinstance(job_id, str) or not job_id:
            continue
        if not isinstance(paper_path, str) or not paper_path:
            continue
        if (repo_root / paper_path).is_file():
            continue

        job = ft.read_object(repo_root / ".survey" / "work-queue" / "jobs" / f"{job_id}.json")
        if not job or job.get("status") != "completed":
            continue
        if not ft.chat_transport_settled(repo_root):
            return {"action": "deferred", "job_id": job_id, "reason": "chat transport still processing"}

        remapped, reason = ft.remap_research_bank(repo_root, envelope)
        if remapped is None:
            return {"action": "deferred", "job_id": job_id, "reason": reason}
        changed = ft.apply_envelope(repo_root, remapped)
        reopen_missing_artifact_job(repo_root, job_id, paper_path)
        if any(write["path"] == ft.CHAT_INBOX for write in remapped["writes"]):
            (repo_root / ft.CHAT_RESULT).unlink(missing_ok=True)
        return {
            "action": "replayed_missing_artifact",
            "envelope_id": envelope["id"],
            "job_id": job_id,
            "paper_path": paper_path,
            "bank_selection": reason,
            "changed_paths": changed,
        }

    return {"action": "idle", "reason": "no_missing_completed_research_artifact"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    print(json.dumps(recover(args.repo_root), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
