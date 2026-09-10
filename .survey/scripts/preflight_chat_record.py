#!/usr/bin/env python3
"""Preflight the reusable Chat structured-record transport without publishing it.

The preflight deliberately reuses assemble_research_record.assemble() inside a temporary
repository tree so validation rules stay identical to the renderer path.  On validation
failure it can soft-isolate only the affected job: write a machine-readable result and
reopen that job for repair while allowing the worker run to continue.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import assemble_research_record as base  # noqa: E402


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def copy_transport(repo_root: Path, temp_root: Path) -> dict:
    inbox = read_json(repo_root / base.FIXED_INBOX)
    dst_inbox = temp_root / base.FIXED_INBOX
    dst_inbox.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(repo_root / base.FIXED_INBOX, dst_inbox)

    refs = inbox.get("record_slots") or []
    for ref in refs:
        if not isinstance(ref, dict):
            continue
        rel = ref.get("path")
        if not isinstance(rel, str):
            continue
        src = repo_root / rel
        dst = temp_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src.is_file():
            shutil.copy2(src, dst)
    return inbox


def isolate_invalid_job(repo_root: Path, inbox: dict, error: str) -> None:
    result_path = repo_root / ".survey/work-queue/results/chat-inbox.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "workflow_version": 10,
                "submission": "work-queue/submissions/chat-inbox.json",
                "ok": False,
                "job_id": inbox.get("job_id"),
                "validation_error": error,
                "repair_required": True,
                "isolated_at": now(),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    job_id = inbox.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return
    job_path = repo_root / ".survey/work-queue/jobs" / f"{job_id}.json"
    if not job_path.is_file():
        return
    try:
        job = read_json(job_path)
    except Exception:
        return
    job["status"] = "ready"
    job.pop("completed_at", None)
    job.pop("artifact_submission", None)
    job["repair_required"] = True
    job["validation_error"] = error
    job["last_validation_failed_at"] = now()
    job_path.write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def preflight(repo_root: Path, isolate: bool) -> dict:
    inbox = read_json(repo_root / base.FIXED_INBOX)
    if inbox.get("record_slots") is None:
        return {"valid": True, "skipped": True, "reason": "no structured record_slots"}

    try:
        with tempfile.TemporaryDirectory(prefix="survey-preflight-") as td:
            temp_root = Path(td)
            copy_transport(repo_root, temp_root)
            base.assemble(temp_root)
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        if isolate:
            isolate_invalid_job(repo_root, inbox, error)
        return {
            "valid": False,
            "job_id": inbox.get("job_id"),
            "error": error,
            "isolated": isolate,
        }

    return {"valid": True, "job_id": inbox.get("job_id"), "isolated": False}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--report")
    ap.add_argument("--isolate-invalid", action="store_true")
    ap.add_argument("--strict", action="store_true", help="return non-zero on validation failure")
    args = ap.parse_args()

    result = preflight(Path(args.repo_root).resolve(), isolate=args.isolate_invalid)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(text, end="")
    if args.report:
        Path(args.report).write_text(text, encoding="utf-8")
    if args.strict and not result.get("valid"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
