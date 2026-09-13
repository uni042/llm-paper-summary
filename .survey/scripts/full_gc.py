#!/usr/bin/env python3
"""GC terminal jobs and settled one-shot transport artifacts for workflow v10.

Current reusable transport, live fallback state, record banks, papers, docs,
scripts, workflows, and update-worker state are never candidates. Historical
submissions/results/payloads do not keep terminal jobs alive forever.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from pathlib import Path

TERMINAL = {"completed", "superseded", "rejected", "failed", "cancelled", "blocked_permanent"}
LIVE_REFERENCE_PATHS = [
    ".survey/work-queue/next-jobs.json",
    ".survey/work-queue/fallback-inbox",
    ".survey/work-queue/fallback-failed",
    ".survey/work-queue/transport",
    ".survey/work-queue/submissions/chat-inbox.json",
    ".survey/work-queue/results/chat-inbox.json",
    ".survey/update-worker",
]
FIXED_TRANSPORT = {
    ".survey/work-queue/submissions/chat-inbox.json",
    ".survey/work-queue/results/chat-inbox.json",
    ".survey/work-queue/payloads/chat-payload.md",
}


def now_utc():
    return dt.datetime.now(dt.timezone.utc)


def parse_time(value):
    if not value or not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(dt.timezone.utc)
    except ValueError:
        return None


def git_last_change(root, path):
    try:
        rel = str(path.relative_to(root))
        out = subprocess.check_output(
            ["git", "log", "-1", "--format=%cI", "--", rel],
            cwd=root,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
        return parse_time(out)
    except Exception:
        return None


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def object_time(obj):
    if not isinstance(obj, dict):
        return None
    for key in (
        "completed_at", "superseded_at", "rejected_at", "failed_at",
        "processed_at", "submitted_at", "assigned_at", "expires_at", "updated_at", "created_at",
    ):
        value = parse_time(obj.get(key))
        if value:
            return value
    return None


def file_time(root, path):
    return object_time(read_json(path)) or git_last_change(root, path)


def older_than(ts, days, now):
    return bool(ts and now - ts >= dt.timedelta(days=days))


def read_text_safe(path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


def live_reference_text(root):
    chunks = []
    for rel in LIVE_REFERENCE_PATHS:
        path = root / rel
        if path.is_file():
            chunks.append(read_text_safe(path))
        elif path.is_dir():
            for child in path.rglob("*.json"):
                chunks.append(read_text_safe(child))
    return "\n".join(chunks)


def collect_settled_transport(root, retention_days, now):
    candidates = []
    skipped = []
    submissions = root / ".survey/work-queue/submissions"
    results = root / ".survey/work-queue/results"
    planned = set()

    if submissions.is_dir():
        for sub in sorted(submissions.glob("*.json")):
            rel = sub.relative_to(root).as_posix()
            if rel in FIXED_TRANSPORT:
                continue
            result = results / sub.name
            if not result.is_file():
                skipped.append({"path": rel, "reason": "submission_not_settled"})
                continue
            timestamps = [ts for ts in (file_time(root, sub), file_time(root, result)) if ts]
            newest = max(timestamps) if timestamps else None
            if not older_than(newest, retention_days, now):
                continue
            for path, kind in ((sub, "settled_submission"), (result, "settled_result")):
                candidates.append({"path": path, "kind": kind, "timestamp": newest.isoformat() if newest else None})
                planned.add(path.resolve())

    if results.is_dir():
        for result in sorted(results.glob("*.json")):
            rel = result.relative_to(root).as_posix()
            if rel in FIXED_TRANSPORT or result.resolve() in planned:
                continue
            if (submissions / result.name).exists():
                continue
            ts = file_time(root, result)
            if older_than(ts, retention_days, now):
                candidates.append({"path": result, "kind": "orphan_result", "timestamp": ts.isoformat() if ts else None})
                planned.add(result.resolve())

    # Only remaining submissions may keep a named legacy payload alive.
    remaining_refs = []
    if submissions.is_dir():
        for sub in submissions.glob("*.json"):
            if sub.resolve() not in planned:
                remaining_refs.append(read_text_safe(sub))
    remaining_text = "\n".join(remaining_refs)

    payloads = root / ".survey/work-queue/payloads"
    if payloads.is_dir():
        for payload in sorted(payloads.glob("*.md")):
            rel = payload.relative_to(root).as_posix()
            if rel in FIXED_TRANSPORT:
                continue
            if rel in remaining_text or payload.name in remaining_text:
                skipped.append({"path": rel, "reason": "payload_still_referenced"})
                continue
            ts = git_last_change(root, payload)
            if older_than(ts, retention_days, now):
                candidates.append({"path": payload, "kind": "orphan_payload", "timestamp": ts.isoformat() if ts else None})

    return candidates, skipped


def collect_terminal_jobs(root, retention_days, now):
    refs = live_reference_text(root)
    candidates = []
    skipped = []
    jobs = root / ".survey/work-queue/jobs"
    if not jobs.is_dir():
        return candidates, skipped
    for path in sorted(jobs.glob("job-*.json")):
        obj = read_json(path)
        if not isinstance(obj, dict):
            skipped.append({"path": path.relative_to(root).as_posix(), "reason": "invalid_json"})
            continue
        if obj.get("status") not in TERMINAL:
            continue
        job_id = str(obj.get("job_id") or path.stem)
        ts = object_time(obj) or git_last_change(root, path)
        if not older_than(ts, retention_days, now):
            continue
        if job_id and job_id in refs:
            skipped.append({"path": path.relative_to(root).as_posix(), "reason": "still_live_referenced"})
            continue
        candidates.append({"path": path, "kind": "terminal_job", "timestamp": ts.isoformat() if ts else None})
    return candidates, skipped


def collect_claim_artifacts(root, retention_days, now):
    """Collect only settled claim history; ready-job claims and pending IO live."""
    base = root / ".survey/work-queue"
    claims_root = base / "claims"
    jobs_root = base / "jobs"
    candidates = []
    skipped = []
    if claims_root.is_dir():
        for path in sorted(claims_root.glob("*.json")):
            claim = read_json(path)
            job_id = str((claim or {}).get("job_id") or path.stem)
            job = read_json(jobs_root / f"{job_id}.json")
            if not isinstance(job, dict) or job.get("status") not in TERMINAL:
                skipped.append({"path": path.relative_to(root).as_posix(), "reason": "current_ready_or_unknown_job"})
                continue
            ts = object_time(claim) or git_last_change(root, path)
            if older_than(ts, retention_days, now):
                candidates.append({"path": path, "kind": "terminal_claim", "timestamp": ts.isoformat() if ts else None})

    requests = base / "claim-requests"
    results = base / "claim-results"
    if requests.is_dir():
        for request in sorted(requests.glob("*.json")):
            result = results / request.name
            request_obj = read_json(request)
            result_obj = read_json(result) if result.is_file() else None
            # A result without an explicit processed_at is still in-flight from
            # GC's perspective; allocator output may be rewritten by a rerun.
            processed = parse_time((result_obj or {}).get("processed_at"))
            if not result.is_file() or processed is None:
                skipped.append({"path": request.relative_to(root).as_posix(), "reason": "claim_request_not_settled"})
                continue
            times = [ts for ts in (object_time(request_obj), processed) if ts]
            newest = max(times) if times else None
            if not older_than(newest, retention_days, now):
                continue
            candidates.extend([
                {"path": request, "kind": "settled_claim_request", "timestamp": newest.isoformat() if newest else None},
                {"path": result, "kind": "settled_claim_result", "timestamp": newest.isoformat() if newest else None},
            ])
    if results.is_dir():
        for result in sorted(results.glob("*.json")):
            if (requests / result.name).exists():
                continue
            result_obj = read_json(result)
            processed = parse_time((result_obj or {}).get("processed_at"))
            if processed and older_than(processed, retention_days, now):
                candidates.append({"path": result, "kind": "orphan_claim_result", "timestamp": processed.isoformat()})
    return candidates, skipped


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--job-retention-days", type=int, default=7)
    parser.add_argument("--transport-retention-days", type=int, default=1)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    now = now_utc()

    transport, transport_skipped = collect_settled_transport(root, args.transport_retention_days, now)
    jobs, job_skipped = collect_terminal_jobs(root, args.job_retention_days, now)
    claim_artifacts, claim_skipped = collect_claim_artifacts(root, args.job_retention_days, now)
    candidates = transport + jobs + claim_artifacts
    deleted = []
    counts = {}
    for item in candidates:
        counts[item["kind"]] = counts.get(item["kind"], 0) + 1
        if args.apply:
            item["path"].unlink(missing_ok=True)
            deleted.append(item["path"].relative_to(root).as_posix())

    result = {
        "schema_version": 3,
        "checked_at": now.isoformat(),
        "mode": "apply" if args.apply else "dry_run",
        "job_retention_days": args.job_retention_days,
        "transport_retention_days": args.transport_retention_days,
        "candidate_count": len(candidates),
        "candidate_counts_by_kind": counts,
        "deleted_count": len(deleted),
        "deleted": deleted,
        "skipped": transport_skipped + job_skipped + claim_skipped,
        "live_reference_paths": LIVE_REFERENCE_PATHS,
        "protected": [
            "papers/**", ".survey/docs/**", ".survey/scripts/**", ".github/workflows/**",
            ".survey/survey-state/paper-identity-index.json", ".survey/survey-state/identity-deltas/**",
            ".survey/survey-state/frozen-training.json", ".survey/work-queue/next-jobs.json",
            ".survey/work-queue/state.json", ".survey/work-queue/maintenance-cycle.json",
            ".survey/work-queue/discovery-state.json", ".survey/work-queue/run-ledger.json",
            ".survey/work-queue/claim-requests/**", ".survey/work-queue/claim-results/**", ".survey/work-queue/claims/**",
            ".survey/work-queue/records/**", ".survey/work-queue/transport/**",
            ".survey/work-queue/fallback-inbox/**", ".survey/work-queue/fallback-archive/**",
            ".survey/work-queue/fallback-failed/**", ".survey/work-queue/submissions/chat-inbox.json",
            ".survey/work-queue/results/chat-inbox.json", ".survey/work-queue/payloads/chat-payload.md",
            ".survey/update-worker/**",
        ],
    }
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.report:
        report = args.report if args.report.is_absolute() else root / args.report
        report.parent.mkdir(parents=True, exist_ok=True)
        report.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
