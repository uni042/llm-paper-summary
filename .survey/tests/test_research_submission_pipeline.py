import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PIPELINE = SCRIPTS / "advance_research_submission_pipeline.py"
ROOT = Path(__file__).resolve().parents[2]


def _load():
    spec = importlib.util.spec_from_file_location("advance_research_submission_pipeline_test", PIPELINE)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ResearchSubmissionPipelineTests(unittest.TestCase):
    def setUp(self):
        self.module = _load()

    def test_poison_completed_request_is_quarantined_without_blocking_valid_request(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            requests = repo / ".survey/work-queue/completed-submission-requests"
            requests.mkdir(parents=True)
            (requests / "broken.json").write_text("{broken\n", encoding="utf-8")
            _write(requests / "attempt-good.json", {
                "kind": "research", "attempt_id": "attempt-good", "job_id": "job-good",
                "record_bank": "a", "paper_path": "papers/inference/good.md",
                "preflight_result": ".survey/work-queue/research-preflight/results/pf-good.json",
            })
            descriptor = {
                "schema_version": 1, "transport_version": 10, "kind": "research",
                "attempt_id": "attempt-good", "job_id": "job-good", "status": "completed",
            }
            with mock.patch.object(self.module, "_build_descriptor_from_payload", return_value=descriptor):
                summary = self.module.advance(repo, mode="completed")

            output = repo / ".survey/work-queue/submissions/research/attempt-good.json"
            failure = repo / ".survey/work-queue/completed-submission-failures/request-broken.json"
            self.assertTrue(output.is_file())
            self.assertTrue(failure.is_file())
            self.assertIn(output.relative_to(repo).as_posix(), summary["built_descriptors"])
            self.assertIn(failure.relative_to(repo).as_posix(), summary["quarantined"])

            first_failure = failure.read_text(encoding="utf-8")
            with mock.patch.object(self.module, "_build_descriptor_from_payload", return_value=descriptor):
                self.module.advance(repo, mode="completed")
            self.assertEqual(first_failure, failure.read_text(encoding="utf-8"))

    def test_passing_preflight_auto_materializes_request_and_descriptor(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            result = repo / ".survey/work-queue/research-preflight/results/pf-pass.json"
            _write(result, {
                "operation": "research_quality_preflight", "ok": True, "preflight_passed": True,
                "checked_at": "2026-09-23T01:00:00+00:00", "kind": "audit",
                "attempt_id": "attempt-pass", "job_id": "job-pass", "record_bank": "b",
                "paper_path": "papers/inference/pass.md",
            })
            descriptor = {
                "schema_version": 1, "transport_version": 10, "kind": "audit",
                "attempt_id": "attempt-pass", "job_id": "job-pass", "status": "completed",
            }
            with mock.patch.object(self.module, "_build_descriptor_from_payload", return_value=descriptor):
                summary = self.module.advance(repo, mode="preflight")

            request = repo / ".survey/work-queue/completed-submission-requests/attempt-pass.json"
            output = repo / ".survey/work-queue/submissions/audit/attempt-pass.json"
            self.assertTrue(request.is_file())
            self.assertTrue(output.is_file())
            self.assertEqual(json.loads(request.read_text(encoding="utf-8"))["generated_by"], "research-preflight-pipeline")
            self.assertEqual(summary["next_action"], "dispatch_submission_drain_once")

    def test_failed_preflight_does_not_materialize_descriptor(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            result = repo / ".survey/work-queue/research-preflight/results/pf-fail.json"
            _write(result, {"ok": True, "preflight_passed": False, "attempt_id": "attempt-fail"})
            summary = self.module.advance(repo, mode="preflight")
            self.assertEqual(summary["built_descriptors"], [])
            self.assertFalse((repo / ".survey/work-queue/submissions").exists())

    def test_workflows_use_one_batch_dispatch_and_optional_submission_target(self):
        preflight = (ROOT / ".github/workflows/survey-research-quality-preflight.yml").read_text(encoding="utf-8")
        builder = (ROOT / ".github/workflows/survey-completed-builder-fast.yml").read_text(encoding="utf-8")
        submission = (ROOT / ".github/workflows/survey-submission-fast.yml").read_text(encoding="utf-8")
        self.assertIn("advance_research_submission_pipeline.py", preflight)
        self.assertEqual(preflight.count("gh workflow run survey-submission-fast.yml"), 1)
        self.assertNotIn("while IFS= read -r submission", builder)
        self.assertEqual(builder.count("gh workflow run survey-submission-fast.yml"), 1)
        self.assertIn("required: false", submission)
        self.assertIn('[ -n "${MANUAL_SUBMISSION:-}" ]', submission)
        self.assertIn("list_unsettled_immutable_submissions.py", submission)


if __name__ == "__main__":
    unittest.main()
