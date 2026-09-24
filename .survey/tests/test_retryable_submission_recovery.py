import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import isolate_failed_immutable_submission as isolation  # noqa: E402
import list_unsettled_immutable_submissions as lister  # noqa: E402

WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/survey-submission-fast.yml"


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def descriptor(job_id: str, attempt_id: str):
    return {
        "kind": "research",
        "job_id": job_id,
        "attempt_id": attempt_id,
        "paper_path": f"papers/inference/test/{job_id}.md",
    }


class RetryableSubmissionRecoveryTests(unittest.TestCase):
    def test_lister_returns_only_explicitly_retryable_matching_failures(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            submissions = root / ".survey/work-queue/submissions/research"
            results = root / ".survey/work-queue/results/research"
            fixtures = {
                "retryable": (False, True, 1),
                "nonretryable": (False, False, 0),
                "exhausted": (False, True, 3),
                "success": (True, False, 0),
                "legacy": (False, None, 0),
            }
            for name, (ok, retryable, failures) in fixtures.items():
                desc = descriptor(f"job-{name}", f"attempt-{name}")
                write_json(submissions / f"{name}.json", desc)
                result = {
                    "job_id": desc["job_id"],
                    "attempt_id": desc["attempt_id"],
                    "ok": ok,
                }
                if retryable is not None:
                    result["retryable"] = retryable
                    result["recovery_failures"] = failures
                write_json(results / f"{name}.json", result)

            self.assertEqual(
                lister.unsettled_paths(root),
                [".survey/work-queue/submissions/research/retryable.json"],
            )

    def test_retry_classification_stops_after_three_failed_recoveries(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td).resolve()
            submission = root / ".survey/work-queue/submissions/research/attempt-a.json"
            desc = descriptor("job-a", "attempt-a")
            write_json(submission, desc)
            result_path = root / ".survey/work-queue/results/research/attempt-a.json"
            write_json(result_path, {
                "job_id": desc["job_id"],
                "attempt_id": desc["attempt_id"],
                "ok": False,
            })

            first = isolation._persist_failure_classification(
                root, submission, desc,
                failure_class="post_validation_processing_failure",
                retryable=True,
            )
            second = isolation._persist_failure_classification(
                root, submission, desc,
                failure_class="post_validation_processing_failure",
                retryable=True,
            )
            third = isolation._persist_failure_classification(
                root, submission, desc,
                failure_class="post_validation_processing_failure",
                retryable=True,
            )

            self.assertTrue(first["retryable"])
            self.assertTrue(second["retryable"])
            self.assertFalse(third["retryable"])
            self.assertEqual(third["failure_class"], "recovery_exhausted")
            self.assertEqual(third["recovery_failures"], 3)
            self.assertEqual(lister.unsettled_paths(root), [])

    def test_submission_fast_lane_has_periodic_backlog_sweep(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("schedule:", text)
        self.assertIn("cron: '7/10 * * * *'", text)
        self.assertIn("list_unsettled_immutable_submissions.py", text)
        self.assertIn("Immutable submission failure result was persisted to main.", text)


if __name__ == "__main__":
    unittest.main()
