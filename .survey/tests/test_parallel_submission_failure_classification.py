import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
BATCH = SCRIPTS / "process_immutable_submission_batch.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ParallelSubmissionFailureClassificationTests(unittest.TestCase):
    def test_processor_nonzero_without_durable_failure_result_is_fatal(self):
        batch = _load(BATCH, "batch_failure_classification_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            submission = repo / ".survey/work-queue/submissions/research/attempt-a.json"
            _write(submission, {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "status": "blocked",
                "reason": "synthetic",
            })
            effects = repo / "effects"
            effects.mkdir()

            original = batch._run_command
            try:
                batch._run_command = lambda *args, **kwargs: subprocess.CompletedProcess(
                    args=[], returncode=1, stdout="", stderr=""
                )
                with self.assertRaisesRegex(RuntimeError, "without durable failure result"):
                    batch.process_one(repo, submission, effects)
            finally:
                batch._run_command = original


if __name__ == "__main__":
    unittest.main()
