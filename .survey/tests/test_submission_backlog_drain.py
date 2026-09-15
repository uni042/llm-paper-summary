import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
LISTER = SCRIPTS / "list_unsettled_immutable_submissions.py"
PROCESSOR = SCRIPTS / "process_immutable_submission.py"
WORKFLOW = Path(__file__).resolve().parents[2] / ".github/workflows/survey-submission-fast.yml"


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def descriptor(job_id: str, attempt_id: str, kind: str = "research"):
    return {
        "schema_version": 1,
        "transport_version": 10,
        "kind": kind,
        "job_id": job_id,
        "attempt_id": attempt_id,
        "status": "blocked",
        "reason": "synthetic backlog-drain fixture",
    }


class SubmissionBacklogDrainTests(unittest.TestCase):
    def run_lister(self, root: Path):
        self.assertTrue(LISTER.is_file(), "list_unsettled_immutable_submissions.py must exist")
        proc = subprocess.run(
            [sys.executable, str(LISTER), "--repo-root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return [line for line in proc.stdout.splitlines() if line]

    def test_lister_drains_pending_mismatch_and_explicit_retryable_failures(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            submissions = root / ".survey/work-queue/submissions/research"
            results = root / ".survey/work-queue/results/research"

            pending = descriptor("job-pending", "attempt-pending")
            success = descriptor("job-success", "attempt-success")
            legacy_failed = descriptor("job-legacy-failed", "attempt-legacy-failed")
            retryable = descriptor("job-retryable", "attempt-retryable")
            nonretryable = descriptor("job-nonretryable", "attempt-nonretryable")
            exhausted = descriptor("job-exhausted", "attempt-exhausted")
            mismatch = descriptor("job-mismatch", "attempt-mismatch")

            for name, value in (
                ("pending.json", pending),
                ("success.json", success),
                ("legacy-failed.json", legacy_failed),
                ("retryable.json", retryable),
                ("nonretryable.json", nonretryable),
                ("exhausted.json", exhausted),
                ("mismatch.json", mismatch),
            ):
                write_json(submissions / name, value)

            write_json(results / "success.json", {
                "job_id": "job-success", "attempt_id": "attempt-success", "ok": True,
            })
            write_json(results / "legacy-failed.json", {
                "job_id": "job-legacy-failed", "attempt_id": "attempt-legacy-failed", "ok": False,
                "error": "legacy durable failure",
            })
            write_json(results / "retryable.json", {
                "job_id": "job-retryable", "attempt_id": "attempt-retryable", "ok": False,
                "error": "post-validation processing interruption",
                "retryable": True,
                "recovery_failures": 1,
            })
            write_json(results / "nonretryable.json", {
                "job_id": "job-nonretryable", "attempt_id": "attempt-nonretryable", "ok": False,
                "error": "record validation failure",
                "retryable": False,
                "failure_class": "content_validation",
            })
            write_json(results / "exhausted.json", {
                "job_id": "job-exhausted", "attempt_id": "attempt-exhausted", "ok": False,
                "error": "repeated post-validation processing interruption",
                "retryable": True,
                "recovery_failures": 3,
            })
            write_json(results / "mismatch.json", {
                "job_id": "other-job", "attempt_id": "other-attempt", "ok": True,
            })

            self.assertEqual(self.run_lister(root), [
                ".survey/work-queue/submissions/research/mismatch.json",
                ".survey/work-queue/submissions/research/pending.json",
                ".survey/work-queue/submissions/research/retryable.json",
            ])

    def test_invalid_json_without_result_is_still_drainable_for_isolation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".survey/work-queue/submissions/audit/bad.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{broken\n", encoding="utf-8")
            self.assertEqual(
                self.run_lister(root),
                [".survey/work-queue/submissions/audit/bad.json"],
            )

    def test_malformed_descriptor_failure_tombstone_settles_exact_bytes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".survey/work-queue/submissions/audit/bad.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("{broken\n", encoding="utf-8")

            proc = subprocess.run(
                [
                    sys.executable,
                    str(PROCESSOR),
                    "--repo-root",
                    str(root),
                    "--submission",
                    str(path),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(proc.returncode, 1)

            result_path = root / ".survey/work-queue/results/audit/bad.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertFalse(result["ok"])
            self.assertEqual(
                result["descriptor_sha256"],
                hashlib.sha256(path.read_bytes()).hexdigest(),
            )
            self.assertEqual(self.run_lister(root), [])

            path.write_text("{different-broken\n", encoding="utf-8")
            self.assertEqual(
                self.run_lister(root),
                [".survey/work-queue/submissions/audit/bad.json"],
            )

    def test_workflow_sweeps_backlog_periodically_without_unrelated_push(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("list_unsettled_immutable_submissions.py", text)
        self.assertNotIn("git diff-tree --no-commit-id --name-only -r \"$GITHUB_SHA\"", text)
        self.assertIn("Drain all unsettled immutable descriptors", text)
        self.assertIn("schedule:", text)
        self.assertIn("cron:", text)


if __name__ == "__main__":
    unittest.main()
