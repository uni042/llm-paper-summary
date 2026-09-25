#!/usr/bin/env python3
"""Apply minimal update-only Scheduled Chat worker-control commands.

The worker updates one pre-existing control file.  The command intentionally carries
no job/claim/attempt ids.  GitHub Actions resolves the worker's canonical foreground
claim and verifies a SHA-256 guard exported by hot-dispatch before changing state.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import claim_state  # noqa: E402
import derive_worker_run_state as run_state  # noqa: E402
import hot_dispatch  # noqa: E402

CONTROL_DIR = Path(".survey/work-queue/transport/worker-control")
RESULTS_DIR = Path(".survey/work-queue/transport/worker-control-results")
KIND = "scheduled_chat_worker_control"
COMMAND = "quarantine_foreground"
WORKERS = {"scheduled-chat-00", "scheduled-chat-30"}


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


def foreground_guard(job_id: str, claim_id: str, attempt_id: str) -> str:
    raw = "\0".join((job_id, claim_id, attempt_id)).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def _digest(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def _foreground(root: Path, worker_id: str) -> dict[str, str] | None:
    now = dt.datetime.now(dt.timezone.utc)
    claims = claim_state.current_claims(root, now)
    rows: list[tuple[int, str, str, dict[str, str]]] = []
    for job_id, current in claims.items():
        if not current.get("active") or str(current.get("worker_id") or "") != worker_id:
            continue
        kind = str(current.get("kind") or "")
        claim_id = str(current.get("claim_id") or "")
        attempt_id = str(current.get("attempt_id") or "")
        if kind not in {"research", "audit"} or not claim_id or not attempt_id:
            continue
        job = _read(root / ".survey/work-queue/jobs" / f"{job_id}.json", {})
        if (
            not isinstance(job, dict)
            or job.get("status") != "ready"
            or job.get("type") not in {"research", "audit"}
            or run_state._descriptor_for_attempt(root, kind, attempt_id) is not None
        ):
            continue
        order = current.get("pipeline_order")
        normalized_order = (
            int(order)
            if isinstance(order, int) and not isinstance(order, bool) and int(order) >= 0
            else 1_000_000_000
        )
        payload = {
            "job_id": str(job_id),
            "claim_id": claim_id,
            "attempt_id": attempt_id,
            "kind": kind,
        }
        rows.append(
            (
                normalized_order,
                str(current.get("claimed_at") or ""),
                str(job_id),
                payload,
            )
        )
    rows.sort(key=lambda row: (row[0], row[1], row[2]))
    return rows[0][3] if rows else None


def process_control(root: Path, worker_id: str) -> dict[str, Any]:
    root = Path(root).resolve()
    if worker_id not in WORKERS:
        raise ValueError("unsupported fixed Scheduled Chat worker")
    path = root / CONTROL_DIR / f"{worker_id}.json"
    control = _read(path, {})
    if not isinstance(control, dict):
        raise ValueError("worker control must be a JSON object")
    if control.get("schema_version") != 1 or control.get("kind") != KIND:
        raise ValueError("invalid worker control schema/kind")
    if str(control.get("worker_id") or "") != worker_id:
        raise ValueError("worker control filename/worker_id mismatch")

    seq = control.get("seq")
    if isinstance(seq, bool) or not isinstance(seq, int) or seq < 0:
        raise ValueError("worker control seq must be a non-negative integer")
    command = str(control.get("command") or "")
    if seq == 0 and command == "idle":
        return {
            "schema_version": 1,
            "ok": True,
            "worker_id": worker_id,
            "seq": 0,
            "status": "idle",
            "next_action": "NONE",
        }
    if seq <= 0 or command != COMMAND:
        raise ValueError(f"worker control command must be {COMMAND} with seq > 0")

    expected_guard = str(control.get("foreground_guard") or "").strip().lower()
    if len(expected_guard) != 64 or any(ch not in "0123456789abcdef" for ch in expected_guard):
        raise ValueError("foreground_guard must be a lowercase SHA-256 hex digest")

    control_digest = _digest(control)
    result_path = root / RESULTS_DIR / f"{worker_id}-{seq}.json"
    existing = _read(result_path, {})
    if isinstance(existing, dict) and existing:
        if existing.get("control_digest") == control_digest:
            reused = dict(existing)
            reused["reused"] = True
            return reused
        return {
            "schema_version": 1,
            "ok": False,
            "worker_id": worker_id,
            "seq": seq,
            "status": "sequence_identity_conflict",
            "next_action": "REFRESH_CONTROL_FILE_AND_INCREMENT_SEQ",
        }

    foreground = _foreground(root, worker_id)
    result: dict[str, Any] = {
        "schema_version": 1,
        "ok": False,
        "worker_id": worker_id,
        "seq": seq,
        "control_digest": control_digest,
        "result_path": result_path.relative_to(root).as_posix(),
        "status": "quarantine_not_applied",
        "next_action": "REFRESH_HOT_DISPATCH_AND_RETRY_OR_USE_HEALTH_PROBE",
    }
    if foreground is None:
        result.update(status="no_foreground", next_action="CONTINUE_NEXT_RESEARCH_AUDIT")
        _write(result_path, result)
        return result

    actual_guard = foreground_guard(
        foreground["job_id"],
        foreground["claim_id"],
        foreground["attempt_id"],
    )
    if actual_guard != expected_guard:
        result.update(
            status="foreground_guard_mismatch",
            actual_foreground_guard=actual_guard,
            next_action="REFRESH_HOT_DISPATCH_BEFORE_ANY_RETRY",
        )
        _write(result_path, result)
        return result

    marker = {
        "job_id": foreground["job_id"],
        "claim_id": foreground["claim_id"],
        "attempt_id": foreground["attempt_id"],
        "reason": run_state.WRITE_BLOCKED_REASON,
    }
    applied = run_state._apply_write_blocked_job(
        root,
        {
            "request_id": f"worker-control-{worker_id}-{seq}",
            "worker_id": worker_id,
            "write_blocked_job": marker,
        },
    )
    result["write_blocked_job"] = applied
    if applied.get("status") in {"blocked", "already_blocked"}:
        result.update(
            ok=True,
            status="quarantined",
            next_action="CONTINUE_NEXT_RESEARCH_AUDIT",
        )
        hot_dispatch.refresh(root)
    _write(result_path, result)
    return result


def process(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    results: dict[str, Any] = {}
    for worker_id in sorted(WORKERS):
        path = root / CONTROL_DIR / f"{worker_id}.json"
        if not path.is_file():
            continue
        try:
            results[worker_id] = process_control(root, worker_id)
        except Exception as exc:
            results[worker_id] = {
                "schema_version": 1,
                "ok": False,
                "worker_id": worker_id,
                "status": "control_error",
                "error": f"{type(exc).__name__}: {exc}",
                "next_action": "FIX_WORKER_CONTROL",
            }
    return {"schema_version": 1, "workers": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    args = parser.parse_args()
    result = process(args.repo_root)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
