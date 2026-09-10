#!/usr/bin/env python3
"""Conservative GC for terminal workflow-v10 job artifacts.

The active queue, record banks, fallback transport, run ledger, papers, docs,
scripts, workflows, and update worker are never candidates. Only terminal job
files that are old enough and no longer referenced by live transport state are
eligible for deletion.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

TERMINAL = {"completed", "superseded", "rejected", "failed", "cancelled"}
PROTECTED_REFERENCE_PATHS = [
    ".survey/work-queue/next-jobs.json",
    ".survey/work-queue/fallback-inbox",
    ".survey/work-queue/fallback-failed",
    ".survey/work-queue/transport",
    ".survey/work-queue/records",
    ".survey/work-queue/payloads",
    ".survey/work-queue/submissions",
    ".survey/work-queue/results",
    ".survey/work-queue/run-ledger.json",
    ".survey/update-worker",
]


def now_utc(): return dt.datetime.now(dt.timezone.utc)

def parse_time(value):
    if not value or not isinstance(value, str): return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None: parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError: return None

def git_last_change(root, path):
    try:
        out = subprocess.check_output(["git", "log", "-1", "--format=%cI", "--", str(path.relative_to(root))], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
        return parse_time(out)
    except Exception: return None

def object_time(obj):
    if not isinstance(obj, dict): return None
    for key in ("completed_at", "superseded_at", "rejected_at", "failed_at", "updated_at", "created_at", "processed_at", "submitted_at"):
        value = parse_time(obj.get(key))
        if value: return value
    return None

def read_json(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except Exception: return None

def reference_text(root):
    chunks = []
    for rel in PROTECTED_REFERENCE_PATHS:
        p = root / rel
        if p.is_file():
            try: chunks.append(p.read_text(encoding="utf-8"))
            except Exception: pass
        elif p.is_dir():
            for f in p.rglob("*.json"):
                try: chunks.append(f.read_text(encoding="utf-8"))
                except Exception: pass
    return "\n".join(chunks)

def older_than(ts, days, now): return bool(ts and now - ts >= dt.timedelta(days=days))

def collect(root, job_retention_days):
    now = now_utc(); refs = reference_text(root); candidates = []; skipped = []
    jobs = root / ".survey/work-queue/jobs"
    if jobs.exists():
        for path in sorted(jobs.glob("job-*.json")):
            obj = read_json(path)
            if not isinstance(obj, dict):
                skipped.append({"path": str(path.relative_to(root)), "reason": "invalid_json"}); continue
            status = obj.get("status"); job_id = obj.get("job_id") or path.stem
            if status not in TERMINAL: continue
            ts = object_time(obj) or git_last_change(root, path)
            if not older_than(ts, job_retention_days, now): continue
            if job_id and job_id in refs:
                skipped.append({"path": str(path.relative_to(root)), "reason": "still_referenced"}); continue
            candidates.append({"path": path, "kind": "terminal_job", "timestamp": ts.isoformat() if ts else None})
    return candidates, skipped

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--job-retention-days", type=int, default=7)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(); root = args.repo_root.resolve()
    candidates, skipped = collect(root, args.job_retention_days); deleted = []
    if args.apply:
        for item in candidates:
            item["path"].unlink(missing_ok=True); deleted.append(item["path"].relative_to(root).as_posix())
    result = {
        "schema_version": 2, "checked_at": now_utc().isoformat(), "mode": "apply" if args.apply else "dry_run",
        "job_retention_days": args.job_retention_days, "candidate_count": len(candidates), "deleted_count": len(deleted),
        "deleted": deleted, "skipped": skipped,
        "protected": ["papers/**", ".survey/docs/**", ".survey/scripts/**", ".github/workflows/**", ".survey/survey-state/paper-identity-index.json", ".survey/survey-state/identity-deltas/**", ".survey/survey-state/frozen-training.json", ".survey/work-queue/next-jobs.json", ".survey/work-queue/state.json", ".survey/work-queue/maintenance-cycle.json", ".survey/work-queue/discovery-state.json", ".survey/work-queue/run-ledger.json", ".survey/work-queue/records/**", ".survey/work-queue/fallback-inbox/**", ".survey/work-queue/fallback-archive/**", ".survey/update-worker/**"]
    }
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        report = args.report if args.report.is_absolute() else root / args.report
        report.parent.mkdir(parents=True, exist_ok=True); report.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__": main()
