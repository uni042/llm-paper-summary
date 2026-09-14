import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).parents[2]
LEDGER_SCRIPT = REPO_ROOT / ".survey" / "scripts" / "record_run_ledger.py"
STATUS_SCRIPT = REPO_ROOT / ".survey" / "scripts" / "append_research_throughput_status.py"
SUBMISSION_WORKFLOW = REPO_ROOT / ".github" / "workflows" / "survey-submission-fast.yml"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RunLedgerCompletionMetricTests(unittest.TestCase):
    def test_merge_event_does_not_double_count_same_terminal_transition(self):
        module = _load_module(LEDGER_SCRIPT, "record_run_ledger_dedupe")
        entry = {
            "events": [],
            "signals": [],
            "counts": {},
            "terminal_transitions": [],
            "new_jobs": [],
            "new_paper_ids": [],
            "new_discovery_results": [],
            "new_fallback_archive_files": [],
        }
        transition = {
            "job_id": "job-r1",
            "type": "research",
            "canonical_id": "arxiv:2601.00001",
            "title": "Example",
            "from": "ready",
            "to": "completed",
        }
        base_event = {
            "recorded_at": "2026-09-14T00:00:00+00:00",
            "github": {},
            "signals": ["research_completed"],
            "counts": {"research_completed": 1},
            "terminal_transitions": [transition],
            "new_jobs": [],
            "new_paper_ids": [],
            "new_discovery_results": [],
            "new_fallback_archive_files": [],
        }
        first = dict(base_event, event_id="fast:1")
        second = dict(base_event, event_id="helper:1")
        module.merge_event(entry, first)
        module.merge_event(entry, second)
        self.assertEqual(entry["counts"]["research_completed"], 1)
        self.assertEqual(len(entry["terminal_transitions"]), 1)

    def test_snapshot_observes_nested_fast_lane_result_files(self):
        module = _load_module(LEDGER_SCRIPT, "record_run_ledger_nested_results")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            result = root / ".survey" / "work-queue" / "results" / "research" / "job-r1.json"
            result.parent.mkdir(parents=True)
            result.write_text("{}\n", encoding="utf-8")
            snapshot = module.collect_snapshot(root)
            self.assertIn(
                ".survey/work-queue/results/research/job-r1.json",
                snapshot["result_files"],
            )

    def test_fast_submission_records_ledger_around_terminalization(self):
        text = SUBMISSION_WORKFLOW.read_text(encoding="utf-8")
        snapshot_at = text.index("record_run_ledger.py snapshot")
        process_at = text.index("process_immutable_submission_batch.py")
        record_at = text.index("record_run_ledger.py record")
        ledger_add_at = text.index(".survey/work-queue/run-ledger.json")
        self.assertLess(snapshot_at, process_at)
        self.assertLess(process_at, record_at)
        self.assertLess(record_at, ledger_add_at)

    def test_status_latest_normal_run_ignores_0830_update_worker(self):
        module = _load_module(STATUS_SCRIPT, "research_throughput_status_latest_normal")
        entries = [
            {
                "run_key": "2026-09-14T07:30:00+09:00",
                "counts": {"research_completed": 3},
            },
            {
                "run_key": "2026-09-14T08:30:00+09:00",
                "counts": {"research_completed": 0},
            },
        ]
        latest = module._latest_normal_run(entries, {})
        self.assertEqual(latest["run_key"], "2026-09-14T07:30:00+09:00")
        self.assertEqual(latest["counts"]["research_completed"], 3)


if __name__ == "__main__":
    unittest.main()
