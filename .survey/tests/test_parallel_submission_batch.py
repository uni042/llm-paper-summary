import importlib.util
import json
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PROCESSOR = SCRIPTS / "process_immutable_submission.py"
BATCH = SCRIPTS / "process_immutable_submission_batch.py"
REDUCER = SCRIPTS / "reduce_submission_effects.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _state(research=3, audit=4, rejected=5, views_dirty=False):
    return {
        "schema_version": 1,
        "workflow_version": 9,
        "mode": "queue",
        "created_at": "2026-09-14T00:00:00+00:00",
        "updated_at": "2026-09-14T00:00:00+00:00",
        "policy": {},
        "stats": {
            "discovered": 10,
            "selected": 8,
            "research_completed": research,
            "audit_completed": audit,
            "rejected": rejected,
        },
        "maintenance": {"views_dirty": views_dirty},
    }


class ParallelSubmissionBatchTests(unittest.TestCase):
    def test_deferred_rejected_submission_emits_effect_without_mutating_shared_state(self):
        processor = _load(PROCESSOR, "processor_parallel_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            state_path = repo / ".survey/work-queue/state.json"
            initial = _state(rejected=7)
            _write(state_path, initial)
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "schema_version": 1,
                "workflow_version": 10,
                "job_id": "job-a",
                "type": "research",
                "status": "ready",
                "priority": 50,
            })
            submission = repo / ".survey/work-queue/submissions/research/attempt-a.json"
            _write(submission, {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "status": "rejected",
                "reason": "synthetic rejection",
            })
            effect = repo / "effects/attempt-a.json"

            result = processor.process(
                repo,
                submission,
                defer_shared_state=True,
                effect_path=effect,
            )

            self.assertTrue(result["ok"])
            self.assertEqual(json.loads(state_path.read_text(encoding="utf-8")), initial)
            emitted = json.loads(effect.read_text(encoding="utf-8"))
            self.assertEqual(emitted["job_id"], "job-a")
            self.assertEqual(emitted["attempt_id"], "attempt-a")
            self.assertEqual(emitted["research_completed"], 0)
            self.assertEqual(emitted["audit_completed"], 0)
            self.assertEqual(emitted["rejected"], 1)
            self.assertFalse(emitted["views_dirty"])

    def test_reducer_folds_effects_once_and_rebuilds_snapshot(self):
        self.assertTrue(REDUCER.is_file(), "reduce_submission_effects.py must exist")
        reducer = _load(REDUCER, "reducer_parallel_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/state.json", _state())
            _write(repo / ".survey/work-queue/jobs/job-ready.json", {
                "job_id": "job-ready",
                "type": "research",
                "status": "ready",
                "priority": 60,
                "created_at": "2026-09-14T00:00:00+00:00",
            })
            effects = repo / "effects"
            _write(effects / "a.json", {
                "schema_version": 1,
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "research_completed": 1,
                "audit_completed": 0,
                "rejected": 0,
                "views_dirty": True,
            })
            _write(effects / "b.json", {
                "schema_version": 1,
                "job_id": "job-b",
                "attempt_id": "attempt-b",
                "research_completed": 0,
                "audit_completed": 2,
                "rejected": 1,
                "views_dirty": False,
            })

            summary = reducer.reduce_effects(repo, effects)
            state = json.loads((repo / ".survey/work-queue/state.json").read_text(encoding="utf-8"))
            snapshot = json.loads((repo / ".survey/work-queue/next-jobs.json").read_text(encoding="utf-8"))

            self.assertEqual(summary["effects"], 2)
            self.assertEqual(state["stats"]["research_completed"], 4)
            self.assertEqual(state["stats"]["audit_completed"], 6)
            self.assertEqual(state["stats"]["rejected"], 6)
            self.assertTrue(state["maintenance"]["views_dirty"])
            self.assertEqual(snapshot["next_jobs"][0]["job_id"], "job-ready")

    def test_reducer_rejects_duplicate_attempt_effects(self):
        self.assertTrue(REDUCER.is_file(), "reduce_submission_effects.py must exist")
        reducer = _load(REDUCER, "reducer_duplicate_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/state.json", _state())
            effects = repo / "effects"
            payload = {
                "schema_version": 1,
                "job_id": "job-a",
                "attempt_id": "attempt-a",
                "research_completed": 1,
                "audit_completed": 0,
                "rejected": 0,
                "views_dirty": False,
            }
            _write(effects / "a.json", payload)
            _write(effects / "duplicate.json", payload)
            with self.assertRaisesRegex(ValueError, "duplicate submission effect"):
                reducer.reduce_effects(repo, effects)

    def test_different_jobs_overlap_but_same_job_is_sequential(self):
        self.assertTrue(BATCH.is_file(), "process_immutable_submission_batch.py must exist")
        batch = _load(BATCH, "batch_parallel_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            a1 = repo / "a1.json"
            a2 = repo / "a2.json"
            b1 = repo / "b1.json"
            _write(a1, {"job_id": "job-a"})
            _write(a2, {"job_id": "job-a"})
            _write(b1, {"job_id": "job-b"})

            lock = threading.Lock()
            active_by_job = {"job-a": 0, "job-b": 0}
            max_by_job = {"job-a": 0, "job-b": 0}
            total_active = 0
            max_total = 0
            started = threading.Barrier(2)

            def worker(path):
                nonlocal total_active, max_total
                job_id = json.loads(Path(path).read_text(encoding="utf-8"))["job_id"]
                with lock:
                    active_by_job[job_id] += 1
                    max_by_job[job_id] = max(max_by_job[job_id], active_by_job[job_id])
                    total_active += 1
                    max_total = max(max_total, total_active)
                if path in {a1, b1}:
                    started.wait(timeout=2)
                time.sleep(0.05)
                with lock:
                    active_by_job[job_id] -= 1
                    total_active -= 1
                return str(path)

            result = batch.run_parallel_grouped(
                repo,
                [a1, a2, b1],
                worker=worker,
                parallelism=2,
            )

            self.assertEqual(len(result), 3)
            self.assertGreaterEqual(max_total, 2)
            self.assertEqual(max_by_job["job-a"], 1)
            self.assertEqual(max_by_job["job-b"], 1)

    def test_parallelism_is_bounded_to_record_bank_capacity(self):
        self.assertTrue(BATCH.is_file(), "process_immutable_submission_batch.py must exist")
        batch = _load(BATCH, "batch_bounds_test")
        self.assertEqual(batch.bounded_parallelism(0), 1)
        self.assertEqual(batch.bounded_parallelism(4), 4)
        self.assertEqual(batch.bounded_parallelism(99), 8)


if __name__ == "__main__":
    unittest.main()
