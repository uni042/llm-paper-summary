#!/usr/bin/env python3
"""Maintenance-time health checks for the survey repository.

The 24-run maintenance cycle uses this module after GC.  It deliberately limits
self-repair to derived/snapshot state that can be reconstructed from canonical
files.  Ambiguous queue or record-bank inconsistencies are reported rather than
mutated.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import subprocess
from collections import defaultdict
from pathlib import Path
from typing import Any

TERMINAL = {"completed", "superseded", "rejected", "failed", "cancelled", "blocked_permanent"}
ACTIVE_DUPLICATE_STATUSES = {"ready", "processing", "in_progress"}
VISIBLE_JOB_FIELDS = (
    "job_id", "type", "lane", "priority", "canonical_id", "title",
    "source_url", "paper_path", "instructions", "completion",
)
DEFAULT_SLOTS = ["metadata", "problem_method", "evaluation", "results", "positioning"]
FRESHNESS_TOLERANCE = dt.timedelta(minutes=10)


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def iso_now() -> str:
    return now_utc().replace(microsecond=0).isoformat()


def parse_time(value: Any) -> dt.datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def read_json(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def finding(severity: str, code: str, detail: str, **extra: Any) -> dict[str, Any]:
    row: dict[str, Any] = {"severity": severity, "code": code, "detail": detail}
    row.update(extra)
    return row


def _load_jobs(root: Path) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]], bool]:
    jobs: dict[str, dict[str, Any]] = {}
    findings: list[dict[str, Any]] = []
    safe_to_repair = True
    job_root = root / ".survey/work-queue/jobs"
    if not job_root.is_dir():
        return jobs, [finding("error", "job_directory_missing", str(job_root))], False

    for path in sorted(job_root.glob("job-*.json")):
        obj = read_json(path)
        if not isinstance(obj, dict):
            findings.append(finding("error", "invalid_job_json", "Job JSON could not be parsed", path=path.relative_to(root).as_posix()))
            safe_to_repair = False
            continue
        job_id = obj.get("job_id")
        if not isinstance(job_id, str) or not job_id:
            findings.append(finding("error", "job_id_missing", "Job has no valid job_id", path=path.relative_to(root).as_posix()))
            safe_to_repair = False
            continue
        if job_id in jobs:
            findings.append(finding("error", "duplicate_job_id", f"job_id {job_id} appears more than once", path=path.relative_to(root).as_posix()))
            safe_to_repair = False
            continue
        if path.stem != job_id:
            findings.append(finding("warning", "job_filename_mismatch", f"filename {path.stem} differs from job_id {job_id}", path=path.relative_to(root).as_posix()))
        jobs[job_id] = obj
    return jobs, findings, safe_to_repair


def build_queue_snapshot(jobs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, dict[str, int]] = {}
    for job in jobs.values():
        job_type = str(job.get("type") or "unknown")
        status = str(job.get("status") or "unknown")
        counts.setdefault(job_type, {})
        counts[job_type][status] = counts[job_type].get(status, 0) + 1

    ready = [job for job in jobs.values() if job.get("status") == "ready"]
    ready.sort(key=lambda job: (-int(job.get("priority") or 0), str(job.get("created_at") or "")))
    visible = ready[:8]
    if not any(job.get("type") == "discovery" for job in visible):
        discovery = next((job for job in ready if job.get("type") == "discovery"), None)
        if discovery is not None:
            visible.append(discovery)
    return {
        "counts": counts,
        "next_jobs": [{key: job.get(key) for key in VISIBLE_JOB_FIELDS} for job in visible],
    }


def _snapshot_without_time(obj: Any) -> dict[str, Any]:
    if not isinstance(obj, dict):
        return {}
    out = dict(obj)
    out.pop("generated_at", None)
    return out


def _audit_duplicate_active_jobs(jobs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[str]] = defaultdict(list)
    for job_id, job in jobs.items():
        if job.get("status") not in ACTIVE_DUPLICATE_STATUSES:
            continue
        job_type = str(job.get("type") or "")
        if job_type not in {"research", "audit"}:
            continue
        canonical_id = str(job.get("canonical_id") or "").strip().casefold()
        if not canonical_id:
            continue
        grouped[(job_type, canonical_id)].append(job_id)
    findings = []
    for (job_type, canonical_id), job_ids in sorted(grouped.items()):
        if len(job_ids) > 1:
            findings.append(finding(
                "error", "duplicate_active_candidate",
                f"{job_type} has multiple active jobs for {canonical_id}",
                job_ids=sorted(job_ids), canonical_id=canonical_id, job_type=job_type,
            ))
    return findings


def _audit_fallback_overlap(root: Path) -> list[dict[str, Any]]:
    base = root / ".survey/work-queue"
    sets: dict[str, set[str]] = {}
    for name in ("fallback-inbox", "fallback-archive", "fallback-failed"):
        folder = base / name
        sets[name] = {path.name for path in folder.glob("*.json")} if folder.is_dir() else set()
    findings = []
    for left, right in (("fallback-inbox", "fallback-archive"), ("fallback-inbox", "fallback-failed")):
        overlap = sorted(sets[left] & sets[right])
        if overlap:
            findings.append(finding(
                "error", "fallback_id_overlap",
                f"The same fallback envelope exists in both {left} and {right}",
                files=overlap,
            ))
    return findings


def _audit_record_banks(root: Path) -> list[dict[str, Any]]:
    registry_path = root / ".survey/work-queue/records/bank-registry.json"
    registry = read_json(registry_path, {}) or {}
    banks = registry.get("banks") if isinstance(registry.get("banks"), dict) else {}
    slots = registry.get("slots") if isinstance(registry.get("slots"), list) else DEFAULT_SLOTS
    findings: list[dict[str, Any]] = []
    if not banks:
        return [finding("error", "bank_registry_missing", "No record banks are registered")]

    for bank_name, rel in sorted(banks.items()):
        bank_root = root / str(rel)
        present: list[str] = []
        job_ids: set[str] = set()
        attempts: set[str] = set()
        for slot in slots:
            path = bank_root / f"{slot}.json"
            if not path.exists():
                continue
            present.append(slot)
            obj = read_json(path)
            if not isinstance(obj, dict):
                findings.append(finding("error", "invalid_record_slot", "Record slot is not valid JSON", bank=bank_name, slot=slot))
                continue
            job_id = obj.get("job_id")
            attempt_id = obj.get("attempt_id")
            if isinstance(job_id, str) and job_id:
                job_ids.add(job_id)
            if isinstance(attempt_id, str) and attempt_id:
                attempts.add(attempt_id)
        if len(job_ids) > 1 or len(attempts) > 1:
            findings.append(finding(
                "error", "mixed_record_bank",
                "A record bank contains slots from more than one job/attempt",
                bank=bank_name, job_ids=sorted(job_ids), attempt_ids=sorted(attempts), slots=present,
            ))
        elif present and len(present) != len(slots):
            findings.append(finding(
                "warning", "partial_record_bank",
                "A record bank is only partially populated; this may be an in-flight write",
                bank=bank_name, slots=present,
            ))
    return findings


def audit_queue(root: Path, repair_snapshot: bool = False) -> dict[str, Any]:
    root = root.resolve()
    jobs, findings, safe_to_repair = _load_jobs(root)
    findings.extend(_audit_duplicate_active_jobs(jobs))
    findings.extend(_audit_fallback_overlap(root))
    findings.extend(_audit_record_banks(root))

    expected = build_queue_snapshot(jobs)
    snapshot_path = root / ".survey/work-queue/next-jobs.json"
    current = read_json(snapshot_path, {}) or {}
    drift = _snapshot_without_time(current) != expected
    repaired = False
    if drift:
        if repair_snapshot and safe_to_repair:
            repaired_snapshot = dict(expected)
            repaired_snapshot["generated_at"] = iso_now()
            write_json(snapshot_path, repaired_snapshot)
            repaired = True
        else:
            findings.append(finding(
                "warning" if safe_to_repair else "error",
                "queue_snapshot_drift",
                "next-jobs.json does not match the job files",
            ))
    return {
        "job_count": len(jobs),
        "snapshot_drift": drift,
        "snapshot_repaired": repaired,
        "snapshot_repair_safe": safe_to_repair,
        "counts": expected["counts"],
        "findings": findings,
    }


def _walk_failures(value: Any, out: set[str], prefix: str = "") -> None:
    if isinstance(value, dict):
        if str(value.get("status") or "").upper() == "FAIL":
            identity = value.get("path") or value.get("file") or value.get("canonical_id") or value.get("title")
            if identity:
                out.add(str(identity))
            elif prefix:
                out.add(prefix)
        for key, child in value.items():
            _walk_failures(child, out, f"{prefix}.{key}" if prefix else str(key))
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _walk_failures(child, out, f"{prefix}[{index}]")


def extract_failures(report: Any) -> list[str]:
    failures: set[str] = set()
    _walk_failures(report, failures)
    return sorted(failures)


def compare_quality_failures(current_reports: dict[str, Any], previous_report: Any) -> dict[str, Any]:
    previous_failures = {}
    if isinstance(previous_report, dict):
        quality = previous_report.get("quality")
        if isinstance(quality, dict) and isinstance(quality.get("failures"), dict):
            previous_failures = quality["failures"]
    initialized = not bool(previous_failures)

    failures: dict[str, list[str]] = {}
    new_failures: dict[str, list[str]] = {}
    resolved: dict[str, list[str]] = {}
    for name, report in current_reports.items():
        current = extract_failures(report)
        previous = sorted(str(x) for x in previous_failures.get(name, [])) if isinstance(previous_failures.get(name, []), list) else []
        failures[name] = current
        if initialized:
            new_failures[name] = []
        else:
            new_failures[name] = sorted(set(current) - set(previous))
        resolved[name] = sorted(set(previous) - set(current))
    return {
        "baseline_initialized": initialized,
        "failures": failures,
        "new_failures": new_failures,
        "resolved_failures": resolved,
    }


def _paper_is_moved_stub(path: Path) -> bool:
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False
    body = text
    if text.startswith("---\n"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            body = parts[2]
    for line in body.splitlines():
        if line.strip():
            return line.lstrip().lower().startswith("# moved")
    return False


def current_paper_count(root: Path) -> int:
    count = 0
    for family in ("inference", "training", "survey"):
        folder = root / "papers" / family
        if not folder.is_dir():
            continue
        for path in folder.glob("*/*.md"):
            if path.name in {"README.md", "comparison.md"} or _paper_is_moved_stub(path):
                continue
            count += 1
    return count


def latest_paper_commit(root: Path) -> dt.datetime | None:
    pathspecs = [
        ":(glob)papers/inference/*/*.md", ":(exclude,glob)papers/inference/*/README.md",
        ":(glob)papers/training/*/*.md", ":(exclude,glob)papers/training/*/README.md",
        ":(glob)papers/survey/*/*.md", ":(exclude,glob)papers/survey/*/README.md",
    ]
    try:
        proc = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", *pathspecs],
            cwd=root, text=True, capture_output=True, check=False,
        )
    except OSError:
        return None
    if proc.returncode != 0:
        return None
    return parse_time(proc.stdout.strip())


def evaluate_coverage_report(
    kind: str,
    report: Any,
    latest_paper_time: dt.datetime | None,
    current_paper_count: int,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    if not isinstance(report, dict):
        return {
            "kind": kind, "checked_at": None, "total": None, "incomplete": None,
            "findings": [finding("error", f"{kind}_report_missing", f"{kind} coverage report is missing or invalid")],
        }
    summary = report.get("summary") if isinstance(report.get("summary"), dict) else {}
    total = summary.get("total")
    incomplete = summary.get("incomplete")
    checked = parse_time(report.get("checked_at"))
    if isinstance(incomplete, int) and incomplete > 0:
        findings.append(finding(
            "error", f"{kind}_coverage_incomplete",
            f"{kind} coverage has {incomplete} incomplete paper(s)", incomplete=incomplete,
        ))
    if isinstance(total, int) and total != current_paper_count:
        findings.append(finding(
            "warning", f"{kind}_report_count_mismatch",
            f"{kind} coverage total {total} differs from current paper count {current_paper_count}",
            report_total=total, current_paper_count=current_paper_count,
        ))
    if checked is None:
        findings.append(finding("error", f"{kind}_checked_at_missing", f"{kind} report has no valid checked_at"))
    elif latest_paper_time is not None and latest_paper_time > checked + FRESHNESS_TOLERANCE:
        findings.append(finding(
            "warning", f"{kind}_report_stale",
            f"{kind} report predates the latest paper-content commit",
            checked_at=checked.isoformat(), latest_paper_commit=latest_paper_time.isoformat(),
        ))
    return {
        "kind": kind,
        "checked_at": checked.isoformat() if checked else None,
        "total": total,
        "incomplete": incomplete,
        "findings": findings,
    }


def _load_optional_json(path: Path | None) -> Any:
    if path is None:
        return None
    return read_json(path)


def _read_index_drift(path: Path | None) -> list[str]:
    if path is None or not path.exists():
        return []
    return sorted({line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()})


def run_health(
    root: Path,
    *,
    current_quality_reports: dict[str, Any],
    previous_report: Any = None,
    repair_snapshot: bool = False,
    repaired_index_files: list[str] | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, Any]] = []

    queue = audit_queue(root, repair_snapshot=repair_snapshot)
    findings.extend(queue["findings"])

    quality = compare_quality_failures(current_quality_reports, previous_report)
    for scope, paths in quality["new_failures"].items():
        if paths:
            findings.append(finding(
                "error", "quality_regression",
                f"New {scope} quality failures appeared since the previous maintenance baseline",
                scope=scope, paths=paths,
            ))

    paper_count = current_paper_count(root)
    latest_commit = latest_paper_commit(root)
    citation = evaluate_coverage_report(
        "citation", read_json(root / ".survey/reports/citation-coverage-latest.json"), latest_commit, paper_count
    )
    metadata = evaluate_coverage_report(
        "metadata", read_json(root / ".survey/reports/metadata-coverage-latest.json"), latest_commit, paper_count
    )
    findings.extend(citation["findings"])
    findings.extend(metadata["findings"])

    errors = [x for x in findings if x.get("severity") == "error"]
    warnings = [x for x in findings if x.get("severity") == "warning"]
    return {
        "schema_version": 1,
        "checked_at": iso_now(),
        "status": "passed" if not errors else "issues_found",
        "error_count": len(errors),
        "warning_count": len(warnings),
        "paper_count": paper_count,
        "latest_paper_commit": latest_commit.isoformat() if latest_commit else None,
        "queue": {key: value for key, value in queue.items() if key != "findings"},
        "derived_indexes": {
            "repaired_files": sorted(repaired_index_files or []),
            "repair_count": len(repaired_index_files or []),
        },
        "quality": quality,
        "coverage": {"citation": citation, "metadata": metadata},
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--paper-quality", type=Path, required=True)
    parser.add_argument("--list-quality", type=Path, required=True)
    parser.add_argument("--overview-quality", type=Path, required=True)
    parser.add_argument("--index-drift-file", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--repair-snapshot", action="store_true")
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()

    root = args.root.resolve()
    report_path = args.report if args.report.is_absolute() else root / args.report
    previous = read_json(report_path)
    quality_reports = {
        "paper": _load_optional_json(args.paper_quality),
        "list_summary": _load_optional_json(args.list_quality),
        "overview": _load_optional_json(args.overview_quality),
    }
    missing = [name for name, report in quality_reports.items() if report is None]
    result = run_health(
        root,
        current_quality_reports=quality_reports,
        previous_report=previous,
        repair_snapshot=args.repair_snapshot,
        repaired_index_files=_read_index_drift(args.index_drift_file),
    )
    for name in missing:
        result["findings"].append(finding("error", "quality_report_missing", f"{name} quality report is missing", scope=name))
    if missing:
        result["error_count"] = sum(1 for x in result["findings"] if x.get("severity") == "error")
        result["warning_count"] = sum(1 for x in result["findings"] if x.get("severity") == "warning")
        result["status"] = "issues_found"

    write_json(report_path, result)
    print(json.dumps({
        "status": result["status"],
        "errors": result["error_count"],
        "warnings": result["warning_count"],
        "queue_snapshot_repaired": result["queue"]["snapshot_repaired"],
        "index_repairs": result["derived_indexes"]["repair_count"],
    }, ensure_ascii=False))
    return 1 if args.fail_on_error and result["status"] != "passed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
