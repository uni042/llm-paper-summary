#!/usr/bin/env python3
"""Render STATUS.md with compatibility handling for durable legacy Discovery failures."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from typing import Any

try:
    import render_status_dashboard_core as _core
except ModuleNotFoundError as exc:
    if exc.name != "render_status_dashboard_core":
        raise
    # Some status tests intentionally copy only this facade into a temporary repo.
    # In that harness, load the preserved core from the checked-out source tree.
    core_path = Path.cwd() / ".survey" / "scripts" / "render_status_dashboard_core.py"
    if not core_path.is_file():
        raise
    spec = importlib.util.spec_from_file_location("render_status_dashboard_core", core_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"unable to load status renderer core from {core_path}") from exc
    _core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_core)


_LEGACY_INVALID_DISCOVERY_ERROR = "ValueError: invalid submit_discovery_round payload"
_ORIGINAL_DIRECT_EVIDENCE_METRICS = _core._direct_evidence_metrics
_ORIGINAL_RENDER_DIRECT_METRIC_DETAILS = _core._render_direct_metric_details


def __getattr__(name: str) -> Any:
    """Delegate unchanged renderer helpers to the preserved core module."""
    return getattr(_core, name)


def _known_candidate_canonical_ids(
    repo_root: Path,
    jobs: dict[str, dict[str, Any]],
) -> set[str]:
    """Return candidate identities durably represented by jobs or the paper index."""
    known: set[str] = set()
    for job in jobs.values():
        canonical_id = str(job["payload"].get("canonical_id") or "").strip()
        if canonical_id:
            known.add(canonical_id.casefold())

    index_path = repo_root / ".survey" / "survey-state" / "paper-identity-index.json"
    try:
        index = json.loads(index_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        index = {}
    papers = index.get("papers") if isinstance(index, dict) else None
    if isinstance(papers, dict):
        for canonical_id in papers:
            value = str(canonical_id or "").strip()
            if value:
                known.add(value.casefold())
    return known


def _fully_recovered_invalid_discovery_submission_paths(
    repo_root: Path,
    submissions: list[dict[str, Any]],
    results: list[dict[str, Any]],
    jobs: dict[str, dict[str, Any]],
) -> set[Path]:
    """Identify old invalid Discovery submissions whose candidates all survived.

    The immutable failure remains in the repository. It stops being a *current*
    consistency anomaly only after every candidate in that failed submission is
    durably represented by a job or the canonical paper identity index. Missing
    or ambiguous candidate identity keeps the submission anomalous.
    """
    known = _known_candidate_canonical_ids(repo_root, jobs)
    resolved: set[Path] = set()

    for result in results:
        result_payload = result["payload"]
        if result_payload.get("ok") is not False:
            continue
        if str(result_payload.get("error") or "").strip() != _LEGACY_INVALID_DISCOVERY_ERROR:
            continue

        submission = _core.evidence._submission_for_result(repo_root, result, submissions)
        if submission is None or submission["kind"] != "discovery":
            continue
        if submission["job_id"] and submission["job_id"] in jobs:
            continue
        if _core._discovery_round_identity(submission) is not None:
            continue

        payload = submission["payload"]
        if payload.get("operation") != "submit_discovery_round":
            continue
        candidates = payload.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            continue

        canonical_ids: list[str] = []
        for candidate in candidates:
            if not isinstance(candidate, dict):
                canonical_ids = []
                break
            canonical_id = str(candidate.get("canonical_id") or "").strip()
            if not canonical_id:
                canonical_ids = []
                break
            canonical_ids.append(canonical_id.casefold())

        if canonical_ids and all(canonical_id in known for canonical_id in canonical_ids):
            resolved.add(submission["path"])

    return resolved


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
    resolved = _fully_recovered_invalid_discovery_submission_paths(
        repo_root,
        submissions,
        results,
        jobs,
    )
    if not resolved:
        return metrics

    consistency = dict(metrics["consistency"])
    resolved_count = min(len(resolved), int(consistency.get("orphan_submissions", 0) or 0))
    consistency["orphan_submissions"] = max(
        0,
        int(consistency.get("orphan_submissions", 0) or 0) - resolved_count,
    )
    metrics["consistency"] = consistency
    metrics["consistency_total"] = max(
        0,
        int(metrics.get("consistency_total", 0) or 0) - resolved_count,
    )
    return metrics


def _render_direct_metric_details(metrics: dict[str, Any]) -> list[str]:
    lines = _ORIGINAL_RENDER_DIRECT_METRIC_DETAILS(metrics)
    compatibility_note = (
        " 旧形式のDiscovery submissionが `invalid submit_discovery_round payload` で失敗した履歴は、"
        "そのsubmission内の全candidateが現在のjobまたはpaper identity indexで確認できる場合に限り、"
        "履歴として保持したまま現在の異常から除外します。"
    )
    for index, line in enumerate(lines):
        if line.startswith("直接矛盾を確認できる耐久レコードだけを異常とします。"):
            lines[index] = line + compatibility_note
        elif line.startswith("- **整合性異常**:"):
            lines[index] = line + compatibility_note
    return lines


# The preserved core owns the rendering flow; replace only the compatibility-sensitive
# hooks so all unrelated STATUS behavior remains byte-for-byte equivalent in code.
_core._direct_evidence_metrics = _direct_evidence_metrics
_core._render_direct_metric_details = _render_direct_metric_details

build_dashboard = _core.build_dashboard
main = _core.main


if __name__ == "__main__":
    raise SystemExit(main())
