#!/usr/bin/env python3
"""Prepare one survey run's startup state in a single local operation.

This helper is intentionally local-only. It aggregates capability inspection, mode
selection, route checking, run-record creation, and (when determinable) lease
preparation. The caller must publish the reported files in one non-force remote
change and re-fetch them before treating the run or lease as active.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


TRISTATE = ("true", "false", "unknown")
RUN_ID_RE = re.compile(r"[A-Za-z0-9_-]{1,100}\Z")


def _read_json(root: Path, relative: str, default: Any = None) -> Any:
    path = root / relative
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _json_bytes(data: Any) -> bytes:
    return (json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n").encode("utf-8")


def _atomic_write(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=path.name + ".", suffix=".tmp", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _write_bundle(root: Path, changes: dict[str, Any]) -> None:
    """Best-effort all-or-rollback local write; remote publication is still required."""
    originals: dict[Path, bytes | None] = {}
    paths = [root / rel for rel in changes]
    for path in paths:
        originals[path] = path.read_bytes() if path.exists() else None
    try:
        for rel, data in changes.items():
            _atomic_write(root / rel, _json_bytes(data))
    except Exception:
        for path, original in originals.items():
            try:
                if original is None:
                    if path.exists():
                        path.unlink()
                else:
                    _atomic_write(path, original)
            except Exception:
                pass
        raise


def _load_survey(root: Path):
    path = root / "scripts" / "survey.py"
    if not path.is_file():
        raise FileNotFoundError(f"Missing helper: {path}")
    spec = importlib.util.spec_from_file_location("survey_bootstrap_dependency", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load helper: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _tristate(value: str) -> bool | None:
    if value == "true":
        return True
    if value == "false":
        return False
    if value == "unknown":
        return None
    raise ValueError(value)


def inspect_capabilities(root: Path, github_read: str, github_write: str) -> dict[str, Any]:
    state_layout = root / "survey-state" / "state-layout.json"
    repository_files = state_layout.is_file() and (root / "scripts" / "survey.py").is_file()
    local_read = False
    local_write = False
    if repository_files:
        try:
            state_layout.read_bytes()
            local_read = True
        except OSError:
            pass
        try:
            probe_dir = root / "survey-state"
            fd, probe = tempfile.mkstemp(prefix=".bootstrap-write-probe-", dir=probe_dir)
            os.close(fd)
            Path(probe).unlink()
            local_write = True
        except OSError:
            pass
    return {
        "python": True,
        "dependencies": True,
        "repository_files": repository_files,
        "git_checkout": (root / ".git").exists(),
        "local_read": local_read,
        "local_write": local_write,
        "github_read": _tristate(github_read),
        "github_write": _tristate(github_write),
    }


def _default_next_action(mode: str, route_result: str | None) -> str:
    if mode == "nightly":
        return "read nightly procedure and perform the integrity workflow"
    if mode == "morning":
        return "read morning procedure and perform update checks"
    if mode == "planning":
        return "read planning procedure and reconcile the daily plan"
    if route_result == "recover_planning":
        return "acquire planning ownership, recover the current daily plan, then return to reading"
    if route_result == "stale_slot":
        return "do not rewind the current plan; finish this stale scheduled slot safely"
    return "reconcile the current plan and continue selected reading/audit work"


def _auto_resource(mode: str, route_result: str | None, period_start: str | None) -> str | None:
    if mode == "nightly":
        return "maintenance"
    if mode == "planning" or (mode == "reading" and route_result == "recover_planning"):
        if not period_start:
            raise ValueError("period-start is required for automatic planning lease")
        return f"planning:{period_start}"
    return None


def prepare_bootstrap(
    *,
    root: Path,
    run_id: str,
    scheduled_at: str,
    started_at: str,
    workflow_commit: str,
    nightly_hour: int,
    morning_hour: int,
    morning_minute: int,
    planning_hour: int,
    planning_minute: int,
    period_start: str | None = None,
    lease_resource: str | None = None,
    auto_lease: bool = False,
    github_read: str = "unknown",
    github_write: str = "unknown",
    stage: str = "bootstrap",
    next_action: str | None = None,
    apply: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    if not RUN_ID_RE.fullmatch(run_id):
        raise ValueError("Unsafe run ID")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", workflow_commit):
        raise ValueError("workflow-commit must be a commit-like hex identifier")

    layout = _read_json(root, "survey-state/state-layout.json")
    if not isinstance(layout, dict):
        raise ValueError("state-layout.json is required")
    workflow_version = layout.get("workflow_version")
    if not isinstance(workflow_version, int) or workflow_version < 1:
        raise ValueError("state-layout.json has no valid workflow_version")
    paths = layout.get("paths", {})
    runs_dir = paths.get("runs_dir", "survey-state/runs/")
    leases_path = paths.get("leases", "survey-state/leases.json")
    runtime_path = paths.get("runtime", "survey-state/runtime.json")

    survey = _load_survey(root)
    survey.timestamp(scheduled_at)
    survey.timestamp(started_at)
    mode = survey.select_mode(
        scheduled_at,
        nightly_hour,
        morning_hour,
        morning_minute,
        planning_hour,
        planning_minute,
    )

    runtime = _read_json(root, runtime_path, {}) or {}
    plan = _read_json(root, runtime.get("current_plan_path", ""), {}) if runtime.get("current_plan_path") else {}
    route_result = None
    if mode == "reading" and period_start:
        route_result = survey.route(plan or {}, scheduled_at, period_start)

    capabilities = inspect_capabilities(root, github_read, github_write)
    run_path = f"{runs_dir.rstrip('/')}/{run_id}.json"
    if (root / run_path).exists():
        raise ValueError("Run ID already exists")

    resource = lease_resource
    if auto_lease and resource is None:
        resource = _auto_resource(mode, route_result, period_start)

    run_record: dict[str, Any] = {
        "run_id": run_id,
        "started_at": started_at,
        "scheduled_at": scheduled_at,
        "mode": mode,
        "stage": stage,
        "status": "running",
        "last_progress_at": started_at,
        "next_action": next_action or _default_next_action(mode, route_result),
        "capabilities": capabilities,
        "workflow_commit": workflow_commit,
        "workflow_version": workflow_version,
    }
    if runtime.get("current_plan_id"):
        run_record["plan_id"] = runtime["current_plan_id"]
    if route_result:
        run_record["route"] = route_result

    changes: dict[str, Any] = {run_path: run_record}
    if resource:
        leases = _read_json(root, leases_path, {"schema_version": 1, "items": {}})
        leases = survey.lease(leases or {"schema_version": 1, "items": {}}, resource, run_id, started_at, "acquire")
        changes[leases_path] = leases
        run_record["lease_resource"] = resource

    if apply:
        if not capabilities["local_read"] or not capabilities["local_write"]:
            raise PermissionError("Local repository state is not readable/writable")
        _write_bundle(root, changes)
        saved_run = _read_json(root, run_path)
        if saved_run != run_record:
            raise RuntimeError("Local run-record verification failed")
        if resource:
            saved_lease = _read_json(root, leases_path, {"items": {}}).get("items", {}).get(resource)
            if not saved_lease or saved_lease.get("run_id") != run_id:
                raise RuntimeError("Local lease verification failed")

    return {
        "result": "prepared" if apply else "preview",
        "run_id": run_id,
        "mode": mode,
        "route": route_result,
        "lease_resource": resource,
        "workflow_version": workflow_version,
        "capabilities": capabilities,
        "files_to_publish": list(changes.keys()),
        "remote_publication_required": True,
        "remote_verification": {
            "run_path": run_path,
            "lease_path": leases_path if resource else None,
            "expected_run_id": run_id,
            "expected_lease_owner": run_id if resource else None,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--scheduled-at", required=True)
    parser.add_argument("--started-at", required=True)
    parser.add_argument("--workflow-commit", required=True)
    parser.add_argument("--nightly-hour", type=int, choices=range(24), required=True)
    parser.add_argument("--morning-hour", type=int, choices=range(24), required=True)
    parser.add_argument("--morning-minute", type=int, choices=range(60), required=True)
    parser.add_argument("--planning-hour", type=int, choices=range(24), required=True)
    parser.add_argument("--planning-minute", type=int, choices=range(60), required=True)
    parser.add_argument("--period-start")
    parser.add_argument("--lease-resource")
    parser.add_argument("--auto-lease", action="store_true")
    parser.add_argument("--github-read", choices=TRISTATE, default="unknown")
    parser.add_argument("--github-write", choices=TRISTATE, default="unknown")
    parser.add_argument("--stage", default="bootstrap")
    parser.add_argument("--next-action")
    parser.add_argument("--apply", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = prepare_bootstrap(
        root=args.root,
        run_id=args.run_id,
        scheduled_at=args.scheduled_at,
        started_at=args.started_at,
        workflow_commit=args.workflow_commit,
        nightly_hour=args.nightly_hour,
        morning_hour=args.morning_hour,
        morning_minute=args.morning_minute,
        planning_hour=args.planning_hour,
        planning_minute=args.planning_minute,
        period_start=args.period_start,
        lease_resource=args.lease_resource,
        auto_lease=args.auto_lease,
        github_read=args.github_read,
        github_write=args.github_write,
        stage=args.stage,
        next_action=args.next_action,
        apply=args.apply,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"result": "error", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False), file=sys.stderr)
        raise
