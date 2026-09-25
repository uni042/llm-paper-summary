#!/usr/bin/env python3
"""Apply an optional Scheduled Chat quarantine command carried by the write health probe.

This is an update-only recovery lane for environments that can update an existing
GitHub file but may be prevented from creating a new status-only descriptor or
run-state request.  The probe file itself remains the transport-health evidence;
the optional command is narrowly limited to releasing one currently owned
Research/Audit claim as blocked.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import derive_worker_run_state as run_state  # noqa: E402

PROBE_REL = Path(".survey/work-queue/transport/health-probe.json")
RESULTS_REL = Path(".survey/work-queue/transport/health-probe-results")
KIND = "github_write_health_probe"
ALLOWED_WORKERS = {"scheduled-chat-00", "scheduled-chat-30"}
ALLOWED_SLOTS = {"00", "30"}


def _read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return default


def _write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8")


def _digest(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _safe_probe_id(value: Any) -> str:
    probe_id = str(value or "").strip()
    if not probe_id or not run_state.claim_state.SAFE_ID_RE.fullmatch(probe_id):
        raise ValueError("probe_id must be a safe non-empty id")
    return probe_id


def _result_path(root: Path, probe_id: str) -> Path:
    return root / RESULTS_REL / f"{probe_id}.json"


def process(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    probe_path = root / PROBE_REL
    probe = _read(probe_path, {})
    if not isinstance(probe, dict):
        raise ValueError("health probe must be a JSON object")
    if probe.get("schema_version") != 1:
        raise ValueError("health probe schema_version must be 1")
    if probe.get("kind") != KIND:
        raise ValueError(f"health probe kind must be {KIND}")

    probe_id = _safe_probe_id(probe.get("probe_id"))
    probe_sha256 = _digest(probe)
    result_path = _result_path(root, probe_id)
    existing = _read(result_path, {})
    if isinstance(existing, dict) and existing:
        if existing.get("probe_id") == probe_id and existing.get("probe_sha256") == probe_sha256:
            reused = dict(existing)
            reused["reused"] = True
            return reused
        return {
            "schema_version": 1,
            "ok": False,
            "probe_id": probe_id,
            "probe_sha256": probe_sha256,
            "status": "result_identity_conflict",
            "result_path": result_path.relative_to(root).as_posix(),
            "next_action": "USE_A_NEW_UNIQUE_PROBE_ID_AFTER_REFRESHING_CANONICAL_STATE",
        }

    result: dict[str, Any] = {
        "schema_version": 1,
        "ok": True,
        "probe_id": probe_id,
        "probe_sha256": probe_sha256,
        "status": "probe_observed",
        "result_path": result_path.relative_to(root).as_posix(),
        "write_blocked_job": {"applied": False, "status": "none"},
        "next_action": "CONTINUE_NORMAL_TRANSPORT_DIAGNOSIS",
    }

    marker = probe.get("write_blocked_job")
    if marker is None:
        _write(result_path, result)
        return result

    worker_id = str(probe.get("worker_id") or "").strip()
    scheduled_slot = str(probe.get("scheduled_slot") or "").strip()
    if worker_id not in ALLOWED_WORKERS:
        result.update(
            ok=False,
            status="invalid_quarantine_identity",
            next_action="REFRESH_CANONICAL_JOB_AND_CLAIM",
            error="health-probe quarantine requires fixed Scheduled Chat worker identity",
        )
        _write(result_path, result)
        return result
    if scheduled_slot not in ALLOWED_SLOTS:
        result.update(
            ok=False,
            status="invalid_quarantine_identity",
            next_action="REFRESH_CANONICAL_JOB_AND_CLAIM",
            error="health-probe quarantine is available only to normal :00/:30 paper runs",
        )
        _write(result_path, result)
        return result

    try:
        normalized = run_state._normalize_write_blocked_job(marker, worker_id, scheduled_slot)
        request_id = f"health-probe-{probe_id}"
        applied = run_state._apply_write_blocked_job(
            root,
            {
                "request_id": request_id,
                "worker_id": worker_id,
                "write_blocked_job": normalized,
            },
        )
    except Exception as exc:
        result.update(
            ok=False,
            status="quarantine_not_applied",
            error=f"{type(exc).__name__}: {exc}",
            next_action="REFRESH_CANONICAL_JOB_AND_CLAIM",
        )
        _write(result_path, result)
        return result

    result["write_blocked_job"] = applied
    if applied.get("status") in {"blocked", "already_blocked"}:
        result["status"] = "quarantined"
        result["next_action"] = "CONTINUE_NEXT_RESEARCH_AUDIT"
    else:
        result["status"] = "quarantine_not_applied"
        result["ok"] = False
        result["next_action"] = "REFRESH_CANONICAL_JOB_AND_CLAIM"
    _write(result_path, result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = process(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
