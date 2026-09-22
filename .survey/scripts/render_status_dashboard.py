#!/usr/bin/env python3
"""Render STATUS.md with current durable-evidence normalization and diagnostics."""
from __future__ import annotations

import importlib.util
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import render_status_dashboard_core as _core
except ModuleNotFoundError as exc:
    if exc.name != "render_status_dashboard_core":
        raise
    core_path = Path.cwd() / ".survey" / "scripts" / "render_status_dashboard_core.py"
    if not core_path.is_file():
        raise
    spec = importlib.util.spec_from_file_location("render_status_dashboard_core", core_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load status renderer core from {core_path}") from exc
    _core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_core)


_GENERIC_SURVEY_WORKERS = {"scheduled-chat-llm-survey"}
_CURRENT_SCHEDULED_WORKERS = {"scheduled-chat-00": "00", "scheduled-chat-30": "30"}
_CURRENT_RUN_KEY_RE = re.compile(r"^scheduled-chat-(?:00|30)-(?P<stamp>\d{8}T\d{6})Z$")
_ORIGINAL_COLLECT_SUBMISSIONS = _core.evidence._collect_submissions
_ORIGINAL_DIRECT_EVIDENCE_METRICS = _core._direct_evidence_metrics
_ORIGINAL_RENDER_DIRECT_METRIC_DETAILS = _core._render_direct_metric_details
_ORIGINAL_DISCOVERY_ROUND_IDENTITY = _core._discovery_round_identity


def __getattr__(name: str) -> Any:
    return getattr(_core, name)


def _scheduled_half_hour_from_claimed_at(value: Any):
    claimed_at = _core.evidence._parse_dt(value)
    if claimed_at is None:
        return None
    local = claimed_at.astimezone(_core.evidence.JST)
    if local.minute < 30:
        local = (local - timedelta(hours=1)).replace(minute=30, second=0, microsecond=0)
    else:
        local = local.replace(minute=30, second=0, microsecond=0)
    return local.astimezone(claimed_at.tzinfo)


def _scheduled_slot_from_claimed_at(value: Any, worker_id: str):
    """Map a current fixed worker claim to the scheduled invocation slot.

    A :00 worker may claim repeatedly throughout HH:00-HH:59. A :30 worker may
    continue past the hour boundary, so claims before :30 belong to the previous
    HH:30 invocation. This groups all submissions from one invocation together
    without pretending each claim is a new run.
    """
    claimed_at = _core.evidence._parse_dt(value)
    if claimed_at is None:
        return None
    local = claimed_at.astimezone(_core.evidence.JST)
    slot = _CURRENT_SCHEDULED_WORKERS.get(worker_id)
    if slot == "00":
        local = local.replace(minute=0, second=0, microsecond=0)
    elif slot == "30":
        if local.minute < 30:
            local = (local - timedelta(hours=1)).replace(minute=30, second=0, microsecond=0)
        else:
            local = local.replace(minute=30, second=0, microsecond=0)
    else:
        return None
    return local.astimezone(claimed_at.tzinfo)


def _discovery_run_time_from_key(value: Any):
    """Parse both ISO legacy run keys and current scheduled-chat run keys."""
    parsed = _core.evidence._parse_dt(value)
    if parsed is not None:
        return parsed
    match = _CURRENT_RUN_KEY_RE.match(str(value or "").strip())
    if match is None:
        return None
    try:
        return datetime.strptime(match.group("stamp"), "%Y%m%dT%H%M%S").replace(
            tzinfo=timezone.utc
        )
    except ValueError:
        return None


def _discovery_round_identity(submission: dict[str, Any]) -> tuple[str, str] | None:
    """Accept both current and durable pre-v10 Discovery round identities."""
    identity = _ORIGINAL_DISCOVERY_ROUND_IDENTITY(submission)
    if identity is not None:
        return identity
    payload = submission["payload"]
    stats = payload.get("discovery_stats")
    if not isinstance(stats, dict):
        return None
    run_key = str(payload.get("run_key") or "").strip()
    round_id = str(stats.get("round") or "").strip()
    if not run_key or not round_id:
        return None
    return run_key, round_id


def _collect_submissions(repo_root: Path) -> list[dict[str, Any]]:
    """Normalize current workflow-v10 worker/run evidence.

    Current Scheduled Chat worker IDs are stable across invocations, so run time
    cannot be recovered from worker_id itself. Match each submission to its
    durable claim (or claim-result assignment when the claim file was compacted)
    and group it into the worker's scheduled invocation slot.
    """
    rows = _ORIGINAL_COLLECT_SUBMISSIONS(repo_root)
    claims_by_id: dict[str, dict[str, Any]] = {}
    for _, claim in _core.evidence._iter_json(repo_root / ".survey/work-queue/claims"):
        claim_id = str(claim.get("claim_id") or "").strip()
        if claim_id:
            claims_by_id[claim_id] = claim

    # Claim-result assignments are immutable allocation evidence and survive
    # claim cleanup/rotation. Use them only as a fallback for run attribution.
    for _, result in _core.evidence._iter_json(repo_root / ".survey/work-queue/claim-results"):
        assignments = result.get("assignments")
        if not isinstance(assignments, list):
            continue
        for assignment in assignments:
            if not isinstance(assignment, dict):
                continue
            claim_id = str(assignment.get("claim_id") or "").strip()
            if claim_id and claim_id not in claims_by_id:
                claims_by_id[claim_id] = assignment

    for row in rows:
        parts = {part.lower() for part in row["path"].parts}
        if row.get("kind") == "unknown" and "discovery" in parts:
            row["kind"] = "discovery"

        stats = row["payload"].get("discovery_stats")
        if isinstance(stats, dict):
            run_key = stats.get("run_key") or row["payload"].get("run_key")
            parsed_run = _discovery_run_time_from_key(run_key)
            if parsed_run is not None:
                row["discovery_run_time"] = parsed_run

        if row.get("worker_run_time") is not None:
            continue

        worker_id = str(row.get("worker_id") or "")
        if worker_id not in _GENERIC_SURVEY_WORKERS and worker_id not in _CURRENT_SCHEDULED_WORKERS:
            continue

        claim_id = str(row["payload"].get("claim_id") or "").strip()
        claim = claims_by_id.get(claim_id)
        if claim is None:
            continue
        if str(claim.get("worker_id") or "") != worker_id:
            continue
        claim_attempt = str(claim.get("attempt_id") or "")
        submission_attempt = str(row["payload"].get("attempt_id") or "")
        if claim_attempt and submission_attempt and claim_attempt != submission_attempt:
            continue

        if worker_id in _CURRENT_SCHEDULED_WORKERS:
            row["worker_run_time"] = _scheduled_slot_from_claimed_at(
                claim.get("claimed_at"), worker_id
            )
        else:
            row["worker_run_time"] = _scheduled_half_hour_from_claimed_at(
                claim.get("claimed_at")
            )
    return rows

def _current_orphan_submission_paths(
    repo_root: Path,
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    jobs: dict[str, dict[str, Any]],
) -> set[Path]:
    terminally_rejected = _core._terminally_rejected_submission_paths(repo_root, submissions, results)
    return {
        row["path"]
        for row in submissions
        if (not row["job_id"] or row["job_id"] not in jobs)
        and row["path"] not in terminally_rejected
        and _core._discovery_round_identity(row) is None
    }


def _direct_evidence_metrics(
    repo_root: Path,
    *,
    jobs: dict[str, dict[str, Any]],
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    verified: list[dict[str, Any]],
    verified_discovery: list[dict[str, Any]],
    active: list[dict[str, Any]],
    now,
) -> dict[str, Any]:
    metrics = _ORIGINAL_DIRECT_EVIDENCE_METRICS(
        repo_root,
        jobs=jobs,
        submissions=submissions,
        results=results,
        verified=verified,
        verified_discovery=verified_discovery,
        active=active,
        now=now,
    )
    orphan_paths = _current_orphan_submission_paths(repo_root, submissions, results, jobs)
    old_orphan_count = metrics["consistency"]["orphan_submissions"]
    metrics["consistency"]["orphan_submissions"] = len(orphan_paths)
    metrics["consistency_total"] -= old_orphan_count - len(orphan_paths)
    metrics["orphan_submission_paths"] = sorted(
        str(path.relative_to(repo_root)) for path in orphan_paths
    )
    return metrics


def _render_direct_metric_details(metrics: dict[str, Any]) -> list[str]:
    lines = _ORIGINAL_RENDER_DIRECT_METRIC_DETAILS(metrics)
    orphan_paths = metrics.get("orphan_submission_paths") or []
    if orphan_paths:
        lines.extend([
            "### 対応jobなしsubmissionの診断対象",
            "",
            "上の異常件数と同一判定で抽出した耐久submission pathです。診断専用であり、submission/result自体は変更しません。",
            "",
        ])
        lines.extend(f"- `{path}`" for path in orphan_paths)
        lines.append("")
    return lines


_core.evidence._collect_submissions = _collect_submissions
_core._discovery_round_identity = _discovery_round_identity
_core._direct_evidence_metrics = _direct_evidence_metrics
_core._render_direct_metric_details = _render_direct_metric_details

build_dashboard = _core.build_dashboard
main = _core.main


if __name__ == "__main__":
    raise SystemExit(main())
