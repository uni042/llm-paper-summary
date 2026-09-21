from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "derive_worker_run_state.py"
spec = importlib.util.spec_from_file_location("derive_worker_run_state", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def write_json(root: Path, rel: str, value: object) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")


def request(worker_id: str = "scheduled-chat-00", slot: str = "00") -> dict:
    start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=1)
    return {
        "schema_version": 1,
        "request_id": "snap-1",
        "run_key": "run-1",
        "worker_id": worker_id,
        "worker_kind": "scheduled_chat",
        "scheduled_slot": slot,
        "actual_invocation_start": start.isoformat(),
        "runtime_condition": "none",
    }


def test_normal_route_is_derived_from_inventory(tmp_path: Path):
    write_json(
        tmp_path,
        ".survey/work-queue/next-jobs.json",
        {
            "claiming": {"ready_research_audit": 60, "claimable": 60},
            "counts": {"research": {"ready": 60}, "audit": {"ready": 0}},
        },
    )
    write_json(tmp_path, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
    result = mod.derive(tmp_path, request())
    assert result["candidate_inventory"] == 60
    assert result["work_mode"] == "research"
    assert result["claim_state_checked"] is True
    assert result["submission_state_checked"] is True


def test_0830_slot_forces_maintenance_route(tmp_path: Path):
    write_json(
        tmp_path,
        ".survey/work-queue/next-jobs.json",
        {"claiming": {"ready_research_audit": 100, "claimable": 100}},
    )
    write_json(tmp_path, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})
    result = mod.derive(tmp_path, request("scheduled-chat-30", "0830"))
    assert result["work_mode"] == "maintenance"
    assert result["gate"]["stop_reasons"] == ["scheduled_0830_maintenance_route"]


def test_request_rejects_cross_worker_slot(tmp_path: Path):
    path = tmp_path / "snap-1.json"
    value = request("scheduled-chat-00", "30")
    path.write_text(json.dumps(value), encoding="utf-8")
    try:
        mod._normalize_request(path, value)
    except ValueError as exc:
        assert "scheduled-chat-00" in str(exc)
    else:
        raise AssertionError("cross-worker scheduled slot must be rejected")
