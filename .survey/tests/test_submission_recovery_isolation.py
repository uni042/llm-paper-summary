import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import isolate_failed_immutable_submission as isolation  # noqa: E402


class SubmissionRecoveryIsolationTests(unittest.TestCase):
    def test_exact_partial_publication_is_classified_after_render_and_can_retry(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td).resolve()
            submission = repo / ".survey/work-queue/submissions/research/attempt-partial.json"
            submission.parent.mkdir(parents=True, exist_ok=True)
            submission.write_text("{}\n", encoding="utf-8")
            descriptor = {
                "kind": "research",
                "job_id": "job-partial",
                "attempt_id": "attempt-partial",
                "paper_path": "papers/inference/test/partial.md",
                "expected_blob_sha": "0" * 40,
            }
            result_path = repo / ".survey/work-queue/results/research/attempt-partial.json"
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(json.dumps({
                "ok": False,
                "job_id": descriptor["job_id"],
                "attempt_id": descriptor["attempt_id"],
                "error": "RuntimeError: interrupted after paper write",
            }) + "\n", encoding="utf-8")

            rendered = ("already rendered paper\n" * 40).rstrip() + "\n"
            events = []

            def render(*args, **kwargs):
                events.append(("render", None))
                return rendered

            def precheck(*args, **kwargs):
                events.append(("precheck", kwargs.get("rendered_content")))

            with (
                patch.object(isolation.immutable_submission, "load_descriptor", return_value=descriptor),
                patch.object(isolation.immutable_submission, "validate_descriptor", return_value=descriptor),
                patch.object(isolation.processor, "_configure_queue_worker"),
                patch.object(isolation.processor, "_verify_claim", return_value=True),
                patch.object(isolation.processor, "render_descriptor", side_effect=render),
                patch.object(isolation.processor, "_precheck_paper", side_effect=precheck),
                patch.object(isolation.processor.paper_quality_gate, "validate_rendered_paper"),
            ):
                result = isolation.isolate(repo, submission)

            self.assertEqual(events, [("render", None), ("precheck", rendered)])
            self.assertEqual(result["failure_class"], "post_validation_processing_failure")
            self.assertTrue(result["retryable"])
            persisted = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertTrue(persisted["retryable"])
            self.assertEqual(persisted["recovery_failures"], 1)


if __name__ == "__main__":
    unittest.main()
