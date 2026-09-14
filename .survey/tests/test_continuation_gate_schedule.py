import argparse
import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "continuation_gate.py"
spec = importlib.util.spec_from_file_location("continuation_gate", SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def make_args(**overrides):
    data = dict(
        github_read=True,
        github_write=True,
        library_writable=False,
        result_durable=True,
        seed_durable=True,
        unpublished_completed_result=False,
        offline_seed_required=False,
        platform_limit=False,
        global_dependency=False,
        independent_work=True,
        spillover_work=False,
        can_discover=True,
        claim_result_pending=False,
        write_failed=False,
        probe="not-run",
        seconds_to_next_scheduled_task=None,
        scheduled_handoff_guard_seconds=600,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


def test_stops_when_next_paired_task_is_within_guard():
    result = mod.decide(make_args(seconds_to_next_scheduled_task=599))
    assert result["decision"] == "STOP_RUN"
    assert "next_scheduled_task_within_handoff_guard" in result["stop_reasons"]


def test_guard_boundary_is_stop():
    result = mod.decide(make_args(seconds_to_next_scheduled_task=600))
    assert result["decision"] == "STOP_RUN"


def test_continues_when_next_paired_task_is_outside_guard():
    result = mod.decide(make_args(seconds_to_next_scheduled_task=601))
    assert result["decision"] == "CONTINUE"


def test_unknown_next_task_time_keeps_existing_behavior():
    result = mod.decide(make_args(seconds_to_next_scheduled_task=None))
    assert result["decision"] == "CONTINUE"
