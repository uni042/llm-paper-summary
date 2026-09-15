import argparse
import importlib.util
import unittest
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
        seconds_to_run_deadline=None,
        scheduled_handoff_guard_seconds=600,
        worker_kind="normal",
        discovery_rounds_completed=0,
        discovery_min_rounds=4,
        discovery_exhausted=False,
        next_axis_available=False,
    )
    data.update(overrides)
    return argparse.Namespace(**data)


class ContinuationGateScheduleTests(unittest.TestCase):
    def test_normal_worker_uses_actual_start_deadline_instead_of_nearby_schedule_boundary(self):
        result = mod.decide(make_args(
            worker_kind="normal",
            seconds_to_next_scheduled_task=90,
            seconds_to_run_deadline=3600,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["handoff_time_source"], "run_deadline")
        self.assertEqual(result["effective_seconds_to_handoff"], 3600)
        self.assertNotIn("next_scheduled_task_within_handoff_guard", result["stop_reasons"])
        self.assertNotIn("run_deadline_within_handoff_guard", result["stop_reasons"])

    def test_normal_worker_run_deadline_guard_is_stop(self):
        result = mod.decide(make_args(
            worker_kind="normal",
            seconds_to_next_scheduled_task=3500,
            seconds_to_run_deadline=600,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertIn("run_deadline_within_handoff_guard", result["stop_reasons"])
        self.assertEqual(result["handoff_time_source"], "run_deadline")

    def test_schedule_boundary_is_compatibility_fallback_when_run_deadline_missing(self):
        result = mod.decide(make_args(seconds_to_next_scheduled_task=599))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertIn("next_scheduled_task_within_handoff_guard", result["stop_reasons"])
        self.assertEqual(result["handoff_time_source"], "next_scheduled_task")

    def test_unknown_handoff_time_keeps_existing_behavior(self):
        result = mod.decide(make_args(
            seconds_to_next_scheduled_task=None,
            seconds_to_run_deadline=None,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["handoff_time_source"], "unknown")

    def test_discovery_uses_actual_start_deadline_instead_of_nearby_schedule_boundary(self):
        result = mod.decide(make_args(
            worker_kind="discovery",
            discovery_rounds_completed=0,
            next_axis_available=True,
            seconds_to_next_scheduled_task=90,
            seconds_to_run_deadline=3600,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "DISCOVER_AGAIN")
        self.assertFalse(result["finalization_allowed"])
        self.assertEqual(result["handoff_time_source"], "run_deadline")
        self.assertEqual(result["effective_seconds_to_handoff"], 3600)
        self.assertNotIn("next_scheduled_task_within_handoff_guard", result["stop_reasons"])
        self.assertNotIn("run_deadline_within_handoff_guard", result["stop_reasons"])

    def test_discovery_run_deadline_guard_is_stop(self):
        result = mod.decide(make_args(
            worker_kind="discovery",
            discovery_rounds_completed=1,
            next_axis_available=True,
            seconds_to_next_scheduled_task=3500,
            seconds_to_run_deadline=600,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertTrue(result["finalization_allowed"])
        self.assertIn("run_deadline_within_handoff_guard", result["stop_reasons"])
        self.assertEqual(result["handoff_time_source"], "run_deadline")

    def test_discovery_one_round_requires_another_round_outside_guard(self):
        result = mod.decide(make_args(
            worker_kind="discovery",
            discovery_rounds_completed=1,
            next_axis_available=True,
            seconds_to_next_scheduled_task=90,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "DISCOVER_AGAIN")
        self.assertFalse(result["finalization_allowed"])
        self.assertEqual(result["minimum_rounds_remaining"], 3)

    def test_discovery_minimum_rounds_must_be_met_before_exhaustion_can_stop(self):
        result = mod.decide(make_args(
            worker_kind="discovery",
            discovery_rounds_completed=1,
            discovery_exhausted=True,
            next_axis_available=False,
            seconds_to_run_deadline=3500,
        ))
        self.assertEqual(result["decision"], "CONTINUE")
        self.assertEqual(result["required_action"], "DISCOVER_AGAIN")
        self.assertNotIn("discovery_exhausted_after_minimum_rounds", result["stop_reasons"])

    def test_discovery_can_stop_after_minimum_rounds_and_explicit_exhaustion(self):
        result = mod.decide(make_args(
            worker_kind="discovery",
            discovery_rounds_completed=4,
            discovery_exhausted=True,
            next_axis_available=False,
            independent_work=False,
            can_discover=False,
            seconds_to_run_deadline=2500,
        ))
        self.assertEqual(result["decision"], "STOP_RUN")
        self.assertTrue(result["finalization_allowed"])
        self.assertEqual(result["required_action"], "FINALIZE")
        self.assertIn("discovery_exhausted_after_minimum_rounds", result["stop_reasons"])


if __name__ == "__main__":
    unittest.main()
