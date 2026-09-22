import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).parents[1] / "scripts"
SCRIPT = SCRIPTS / "research_quality_preflight.py"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ResearchPreflightQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = _load(SCRIPT, "research_quality_preflight_test")

    def _request(self, path: Path):
        payload = {
            "schema_version": 1,
            "operation": "research_quality_preflight",
            "request_id": path.stem,
            "kind": "research",
            "attempt_id": "attempt-a",
            "job_id": "job-a",
            "record_bank": "a",
            "paper_path": "papers/inference/test/a.md",
            "self_review": {key: True for key in self.module.SELF_REVIEW_KEYS},
        }
        path.write_text(json.dumps(payload), encoding="utf-8")
        return payload

    def _descriptor(self):
        return {
            "schema_version": 1,
            "transport_version": 10,
            "kind": "research",
            "attempt_id": "attempt-a",
            "job_id": "job-a",
            "status": "completed",
            "record_bank": "a",
            "paper_path": "papers/inference/test/a.md",
            "record_slots": [
                {
                    "slot": "metadata",
                    "path": ".survey/work-queue/records/chat-record/metadata.json",
                    "blob_sha": "1" * 40,
                },
            ],
        }

    def _quality(self, status, failures=None, warnings=None):
        return self.module.paper_quality_gate.quality.PaperResult(
            path="papers/inference/test/a.md",
            status=status,
            file_bytes=6000,
            prose_chars=3000,
            paragraphs=12,
            method_paragraphs=5,
            method_components=2,
            method_detection="explicit",
            japanese_ratio=0.9,
            japanese_chars=900,
            latin_chars=100,
            bare_english_terms=[],
            failures=list(failures or []),
            warnings=list(warnings or []),
        )

    def test_preflight_reuses_repository_quality_defaults(self):
        args = self.module.paper_quality_gate._default_args()
        quality = self.module.paper_quality_gate.quality
        self.assertEqual(args.min_bytes, quality.DEFAULT_MIN_BYTES)
        self.assertEqual(args.min_prose_chars, quality.DEFAULT_MIN_PROSE_CHARS)
        self.assertEqual(args.min_paragraphs, quality.DEFAULT_MIN_PARAGRAPHS)
        self.assertEqual(args.min_method_paragraphs, quality.DEFAULT_MIN_METHOD_PARAGRAPHS)
        self.assertEqual(args.min_component_paragraphs, quality.DEFAULT_MIN_COMPONENT_PARAGRAPHS)
        self.assertEqual(args.min_japanese_ratio, quality.DEFAULT_MIN_JAPANESE_RATIO)
        self.assertEqual(args.warn_japanese_ratio, quality.DEFAULT_WARN_JAPANESE_RATIO)
        self.assertIn("書誌情報", quality.EXCLUDED_SECTIONS)

    def test_self_review_requires_every_item(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "attempt-a-q1.json"
            payload = self._request(path)
            payload["self_review"][self.module.SELF_REVIEW_KEYS[-1]] = False
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaisesRegex(self.module.PreflightRequestError, "self_review"):
                self.module._validate_request(path)

    def test_quality_failure_becomes_repair_state_before_submission(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            request = repo / "attempt-a-q1.json"
            self._request(request)
            descriptor = self._descriptor()
            with mock.patch.object(self.module.prepare_completed_submission, "build", return_value=descriptor), \
                 mock.patch.object(self.module.process_immutable_submission, "render_descriptor", return_value="# Paper\n\n本文"), \
                 mock.patch.object(self.module.process_immutable_submission, "_precheck_paper"), \
                 mock.patch.object(
                     self.module.paper_quality_gate,
                     "inspect_rendered_paper",
                     return_value=self._quality("FAIL", ["手法説明が不足"]),
                 ):
                result = self.module.process_request(repo, request)
            self.assertTrue(result["ok"])
            self.assertFalse(result["preflight_passed"])
            self.assertTrue(result["repair_required"])
            self.assertEqual(result["decision"], "REPAIR_BEFORE_SUBMISSION")
            self.assertIn("手法説明が不足", result["validation_errors"])

    def test_quality_pass_is_bound_to_exact_descriptor_fingerprint(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            request = repo / "attempt-a-q1.json"
            self._request(request)
            descriptor = self._descriptor()
            with mock.patch.object(self.module.prepare_completed_submission, "build", return_value=descriptor), \
                 mock.patch.object(self.module.process_immutable_submission, "render_descriptor", return_value="# Paper\n\n本文"), \
                 mock.patch.object(self.module.process_immutable_submission, "_precheck_paper"), \
                 mock.patch.object(
                     self.module.paper_quality_gate,
                     "inspect_rendered_paper",
                     return_value=self._quality("PASS"),
                 ):
                result = self.module.process_request(repo, request)
            self.assertTrue(result["preflight_passed"])
            self.assertEqual(
                result["descriptor_sha256"],
                self.module.prepare_completed_submission.descriptor_fingerprint(descriptor),
            )

            result_path = repo / ".survey/work-queue/research-preflight/results/attempt-a-q1.json"
            result_path.parent.mkdir(parents=True)
            result_path.write_text(json.dumps(result), encoding="utf-8")
            self.module.prepare_completed_submission.verify_preflight_result(repo, descriptor, result_path)

            changed = dict(descriptor)
            changed["record_slots"] = [
                {
                    "slot": "metadata",
                    "path": ".survey/work-queue/records/chat-record/metadata.json",
                    "blob_sha": "2" * 40,
                },
            ]
            with self.assertRaisesRegex(ValueError, "stale"):
                self.module.prepare_completed_submission.verify_preflight_result(repo, changed, result_path)


if __name__ == "__main__":
    unittest.main()
