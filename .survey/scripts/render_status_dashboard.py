#!/usr/bin/env python3
"""Render STATUS.md with current durable-evidence normalization and diagnostics."""
from __future__ import annotations

import importlib.util
from datetime import timedelta
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
_ORIGINAL_COLLECT_SUBMISSIONS = _core.evidence._collect_submissions
_ORIGINAL_DIRECT_EVIDENCE_METRICS = _core._direct_evidence_metrics
_ORIGINAL_RENDER_DIRECT_METRIC_DETAILS = _core._render_direct_metric_details


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


def _collect_submissions(repo_root: Path) -> list[dict[str, Any]]:
    """Normalize durable submission kind and recover generic Scheduled Chat run time."""
    rows = _ORIGINAL_COLLECT_SUBMISSIONS(repo_root)
    claims_by_id: dict[str, dict[str, Any]] = {}
    for _, claim in _core.evidence._iter_json(repo_root / ".survey/work-queue/claims"):
        claim_id = str(claim.get("claim_id") or "").strip()
        if claim_id:
            claims_by_id[claim_id] = claim

    for row in rows:
        # build_status_dashboard._kind historically recognized Discovery only when
        # "discovery" appeared in the filename. Current workflow-v10 stores rounds
        # under submissions/discovery/ with arbitrary round names, so the directory
        # is the durable kind signal when no explicit kind exists.
        if row.get("kind") == "unknown" and "discovery" in {
            part.lower() for part in row["path"].parts
        }:
            row["kind"] = "discovery"

        if row.get("worker_run_time") is not None:
            continue
        if str(row.get("worker_id") or "") not in _GENERIC_SURVEY_WORKERS:
            continue
        claim_id = str(row["payload"].get("claim_id") or "").strip()
        claim = claims_by_id.get(claim_id)
        if claim is None:
            continue
        if str(claim.get("worker_id") or "") != row["worker_id"]:
            continue
        if str(claim.get("attempt_id") or "") != str(row["payload"].get("attempt_id") or ""):
            continue
        row["worker_run_time"] = _scheduled_half_hour_from_claimed_at(claim.get("claimed_at"))
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
        and not (row["kind"] == "discovery" and _core._discovery_round_identity(row) is not None)
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
    metrics["orphan_submission_paths"] = sorted(
        str(path.relative_to(repo_root))
        for path in _current_orphan_submission_paths(repo_root, submissions, results, jobs)
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
_core._direct_evidence_metrics = _direct_evidence_metrics
_core._render_direct_metric_details = _render_direct_metric_details

build_dashboard = _core.build_dashboard
main = _core.main


if __name__ == "__main__":
    raise SystemExit(main())
