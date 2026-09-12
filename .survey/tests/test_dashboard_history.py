import importlib.util
import json
from pathlib import Path


def _load():
    path = Path(__file__).parents[1] / "scripts" / "ensure_dashboard_history.py"
    spec = importlib.util.spec_from_file_location("ensure_dashboard_history", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_history_limits_are_raised_without_dropping_entries(tmp_path):
    ledger_path = tmp_path / ".survey/work-queue/run-ledger.json"
    discovery_path = tmp_path / ".survey/work-queue/discovery-state.json"
    ledger_path.parent.mkdir(parents=True)
    ledger_path.write_text(json.dumps({"history_limit": 48, "entries": [{"run_key": "a"}]}), encoding="utf-8")
    discovery_path.write_text(json.dumps({"history_limit": 24, "history": [{"round": "r1"}]}), encoding="utf-8")

    module = _load()
    changed = module.ensure_history_limits(tmp_path)

    assert set(changed) == {
        ".survey/work-queue/run-ledger.json",
        ".survey/work-queue/discovery-state.json",
    }
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    discovery = json.loads(discovery_path.read_text(encoding="utf-8"))
    assert ledger["history_limit"] == 384
    assert discovery["history_limit"] == 384
    assert ledger["entries"] == [{"run_key": "a"}]
    assert discovery["history"] == [{"round": "r1"}]


def test_history_migration_is_idempotent(tmp_path):
    ledger_path = tmp_path / ".survey/work-queue/run-ledger.json"
    discovery_path = tmp_path / ".survey/work-queue/discovery-state.json"
    ledger_path.parent.mkdir(parents=True)
    ledger_path.write_text(json.dumps({"history_limit": 500, "entries": []}), encoding="utf-8")
    discovery_path.write_text(json.dumps({"history_limit": 384, "history": []}), encoding="utf-8")

    module = _load()
    assert module.ensure_history_limits(tmp_path) == []
    assert json.loads(ledger_path.read_text(encoding="utf-8"))["history_limit"] == 500
    assert json.loads(discovery_path.read_text(encoding="utf-8"))["history_limit"] == 384
