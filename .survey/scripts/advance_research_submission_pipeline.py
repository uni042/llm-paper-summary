#!/usr/bin/env python3
"""Advance passing Research/Audit preflights into immutable submissions.

The preflight result is the authoritative quality decision. This helper removes
the worker round-trip between a passing preflight and descriptor creation while
preserving the durable preflight result and immutable descriptor boundaries.

Legacy completed-submission request files remain supported. A malformed or
stale request is isolated into a content-hashed failure record so one poison
request cannot stop later requests from being materialized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import prepare_completed_submission  # noqa: E402

PREFLIGHT_RESULTS = Path(".survey/work-queue/research-preflight/results")
COMPLETED_REQUESTS = Path(".survey/work-queue/completed-submission-requests")
SUBMISSIONS = Path(".survey/work-queue/submissions")
FAILURES = Path(".survey/work-queue/completed-submission-failures")
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,159}$")


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("JSON payload must be an object")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def _safe_id(value: Any, field: str) -> str:
    out = str(value or "").strip()
    if not SAFE_ID_RE.fullmatch(out):
        raise ValueError(f"{field} must be a safe non-empty identifier")
    return out


def _failure_path(repo: Path, stage: str, source: Path, attempt_id: str | None = None) -> Path:
    identity = attempt_id or source.stem
    identity = re.sub(r"[^A-Za-z0-9._-]+", "-", identity).strip("-") or "unknown"
    return repo / FAILURES / f"{stage}-{identity}.json"


def _record_failure(repo: Path, *, stage: str, source: Path, exc: Exception, attempt_id: str | None = None) -> Path:
    source = source.resolve()
    try:
        source_rel = source.relative_to(repo.resolve()).as_posix()
    except ValueError:
        source_rel = str(source)
    source_sha = hashlib.sha256(source.read_bytes()).hexdigest() if source.is_file() else None
    path = _failure_path(repo, stage, source, attempt_id)
    error = f"{type(exc).__name__}: {exc}"
    try:
        existing = _read_object(path)
    except Exception:
        existing = {}
    if existing.get("source_sha256") == source_sha and existing.get("error") == error and existing.get("source") == source_rel:
        return path
    _write_json(path, {
        "schema_version": 1,
        "stage": stage,
        "source": source_rel,
        "source_sha256": source_sha,
        "attempt_id": attempt_id,
        "error": error,
        "quarantined_at": _now(),
        "next_action": "Repair or supersede only this exact source payload. Other completed-submission requests may continue.",
    })
    return path


def _clear_failure(repo: Path, stage: str, source: Path, attempt_id: str | None = None) -> None:
    path = _failure_path(repo, stage, source, attempt_id)
    if path.exists():
        path.unlink()


def _existing_attempt_ids(repo: Path) -> set[str]:
    attempts: set[str] = set()
    for kind in ("research", "audit"):
        root = repo / SUBMISSIONS / kind
        if not root.is_dir():
            continue
        for path in root.glob("*.json"):
            try:
                value = _read_object(path)
            except Exception:
                continue
            attempt_id = value.get("attempt_id")
            if isinstance(attempt_id, str) and SAFE_ID_RE.fullmatch(attempt_id):
                attempts.add(attempt_id)
    return attempts


def _normalize_completed_payload(path: Path, value: dict[str, Any]) -> dict[str, Any]:
    kind = value.get("kind")
    if kind not in {"research", "audit"}:
        raise ValueError("kind must be research or audit")
    attempt_id = _safe_id(value.get("attempt_id"), "attempt_id")
    if path.stem != attempt_id:
        raise ValueError(f"request filename must equal attempt_id: {path.stem} != {attempt_id}")
    job_id = _safe_id(value.get("job_id"), "job_id")
    record_bank = str(value.get("record_bank") or "").strip().lower()
    if not record_bank:
        raise ValueError("record_bank is required")
    preflight_result = str(value.get("preflight_result") or "").strip()
    if not preflight_result.startswith(".survey/work-queue/research-preflight/results/") or not preflight_result.endswith(".json"):
        raise ValueError("preflight_result must point to research-preflight/results/*.json")
    payload: dict[str, Any] = {"kind": kind, "attempt_id": attempt_id, "job_id": job_id, "record_bank": record_bank, "preflight_result": preflight_result}
    for field in ("paper_path", "expected_blob_sha"):
        item = value.get(field)
        if item not in (None, ""):
            if not isinstance(item, str):
                raise ValueError(f"{field} must be a string when present")
            payload[field] = item
    return payload


def _payload_from_passed_preflight(path: Path, result: dict[str, Any]) -> dict[str, Any]:
    if result.get("ok") is not True or result.get("preflight_passed") is not True:
        raise ValueError("preflight result is not a passing result")
    kind = result.get("kind")
    if kind not in {"research", "audit"}:
        raise ValueError("passing preflight kind must be research or audit")
    payload: dict[str, Any] = {
        "kind": kind,
        "attempt_id": _safe_id(result.get("attempt_id"), "attempt_id"),
        "job_id": _safe_id(result.get("job_id"), "job_id"),
        "record_bank": str(result.get("record_bank") or "").strip().lower(),
        "preflight_result": path.as_posix(),
    }
    if not payload["record_bank"]:
        raise ValueError("passing preflight record_bank is required")
    for field in ("paper_path", "expected_blob_sha"):
        item = result.get(field)
        if item not in (None, ""):
            if not isinstance(item, str):
                raise ValueError(f"passing preflight {field} must be a string when present")
            payload[field] = item
    return payload


def _build_descriptor_from_payload(repo: Path, payload: dict[str, Any]) -> dict[str, Any]:
    preflight_result = Path(payload["preflight_result"])
    expected_blob_sha = prepare_completed_submission._expected_blob_sha_from_preflight(repo, preflight_result, payload.get("expected_blob_sha"))
    descriptor = prepare_completed_submission.build(
        repo,
        kind=payload["kind"],
        attempt_id=payload["attempt_id"],
        job_id=payload["job_id"],
        record_bank=payload["record_bank"],
        paper_path=payload.get("paper_path"),
        expected_blob_sha=expected_blob_sha,
    )
    prepare_completed_submission.verify_preflight_result(repo, descriptor, preflight_result)
    return descriptor


def _descriptor_path(repo: Path, payload: dict[str, Any]) -> Path:
    return repo / SUBMISSIONS / payload["kind"] / f"{payload['attempt_id']}.json"


def _write_descriptor(repo: Path, payload: dict[str, Any], descriptor: dict[str, Any]) -> bool:
    path = _descriptor_path(repo, payload)
    if path.exists():
        current = _read_object(path)
        if current != descriptor:
            raise ValueError(f"immutable descriptor already exists with different content: {path}")
        return False
    return _write_json(path, descriptor)


def _generated_completed_request(payload: dict[str, Any]) -> dict[str, Any]:
    out = {
        "kind": payload["kind"], "attempt_id": payload["attempt_id"], "job_id": payload["job_id"],
        "record_bank": payload["record_bank"], "preflight_result": payload["preflight_result"],
        "generated_by": "research-preflight-pipeline",
    }
    for field in ("paper_path", "expected_blob_sha"):
        if payload.get(field) not in (None, ""):
            out[field] = payload[field]
    return out


def materialize_passed_preflights(repo: Path, summary: dict[str, Any]) -> None:
    root = repo / PREFLIGHT_RESULTS
    if not root.is_dir():
        return
    settled_attempts = _existing_attempt_ids(repo)
    latest: dict[str, tuple[str, Path, dict[str, Any]]] = {}
    for path in sorted(root.glob("*.json")):
        try:
            result = _read_object(path)
        except Exception:
            continue
        if result.get("ok") is not True or result.get("preflight_passed") is not True:
            continue
        attempt_id = str(result.get("attempt_id") or "")
        if not SAFE_ID_RE.fullmatch(attempt_id):
            continue
        rank = (str(result.get("checked_at") or ""), path.name)
        current = latest.get(attempt_id)
        if current is None or rank > (current[0], current[1].name):
            latest[attempt_id] = (rank[0], path, result)

    for attempt_id, (_, result_path, result) in sorted(latest.items()):
        if attempt_id in settled_attempts:
            summary["already_settled"].append(attempt_id)
            _clear_failure(repo, "preflight", result_path, attempt_id)
            request_path = repo / COMPLETED_REQUESTS / f"{attempt_id}.json"
            if request_path.exists():
                _clear_failure(repo, "request", request_path)
            continue
        try:
            rel_result = result_path.relative_to(repo).as_posix()
            payload = _payload_from_passed_preflight(Path(rel_result), result)
            output = _descriptor_path(repo, payload)
            if output.exists():
                summary["already_settled"].append(output.relative_to(repo).as_posix())
                continue
            descriptor = _build_descriptor_from_payload(repo, payload)
            request_path = repo / COMPLETED_REQUESTS / f"{attempt_id}.json"
            generated = _generated_completed_request(payload)
            if not request_path.exists():
                if _write_json(request_path, generated):
                    summary["generated_requests"].append(request_path.relative_to(repo).as_posix())
            elif _read_object(request_path) != generated:
                summary["request_conflicts"].append(request_path.relative_to(repo).as_posix())
            if _write_descriptor(repo, payload, descriptor):
                summary["built_descriptors"].append(output.relative_to(repo).as_posix())
            settled_attempts.add(attempt_id)
            _clear_failure(repo, "preflight", result_path, attempt_id)
        except Exception as exc:
            failure = _record_failure(repo, stage="preflight", source=result_path, exc=exc, attempt_id=attempt_id)
            summary["quarantined"].append(failure.relative_to(repo).as_posix())


def drain_completed_requests(repo: Path, summary: dict[str, Any]) -> None:
    root = repo / COMPLETED_REQUESTS
    if not root.is_dir():
        return
    settled_attempts = _existing_attempt_ids(repo)
    for request_path in sorted(root.glob("*.json")):
        if request_path.stem in settled_attempts:
            summary["already_settled"].append(request_path.stem)
            _clear_failure(repo, "request", request_path)
            continue
        attempt_id: str | None = None
        try:
            payload = _normalize_completed_payload(request_path, _read_object(request_path))
            attempt_id = payload["attempt_id"]
            output = _descriptor_path(repo, payload)
            if output.exists():
                summary["already_settled"].append(output.relative_to(repo).as_posix())
                _clear_failure(repo, "request", request_path, attempt_id)
                continue
            descriptor = _build_descriptor_from_payload(repo, payload)
            if _write_descriptor(repo, payload, descriptor):
                summary["built_descriptors"].append(output.relative_to(repo).as_posix())
            settled_attempts.add(attempt_id)
            _clear_failure(repo, "request", request_path, attempt_id)
        except Exception as exc:
            failure = _record_failure(repo, stage="request", source=request_path, exc=exc, attempt_id=attempt_id)
            summary["quarantined"].append(failure.relative_to(repo).as_posix())


def advance(repo: Path, *, mode: str = "all") -> dict[str, Any]:
    repo = Path(repo).resolve()
    summary: dict[str, Any] = {
        "ok": True, "mode": mode, "generated_requests": [], "built_descriptors": [],
        "already_settled": [], "request_conflicts": [], "quarantined": [],
    }
    if mode in {"all", "preflight"}:
        materialize_passed_preflights(repo, summary)
    if mode in {"all", "completed"}:
        drain_completed_requests(repo, summary)
    for key in ("generated_requests", "built_descriptors", "already_settled", "request_conflicts", "quarantined"):
        summary[key] = sorted(set(summary[key]))
    summary["next_action"] = "dispatch_submission_drain_once" if summary["built_descriptors"] else "no_new_descriptor"
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--mode", choices=("all", "preflight", "completed"), default="all")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    summary = advance(args.repo_root, mode=args.mode)
    output = json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(output, encoding="utf-8")
    print(output, end="")
    if summary["quarantined"]:
        print("[WORKER-GUIDE] malformed/stale completed-submission inputs were isolated; continue with unaffected requests and repair only the listed failures", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
