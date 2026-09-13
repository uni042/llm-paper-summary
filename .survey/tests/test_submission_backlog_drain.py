import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
LISTER = SCRIPTS / "list_unsettled_immutable_submissions.py"
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

    def test_lister_drains_only_descriptors_without_exact_settled_result(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            submissions = root / ".survey/work-queue/submissions/research"
            results = root / ".survey/work-queue/results/research"

            pending = descriptor("job-pending", "attempt-pending")
            success = descriptor("job-success", "attempt-success")
            failed = descriptor("job-failed", "attempt-failed")
            mismatch = descriptor("job-mismatch", "attempt-mismatch")

            for name, value in (
                ("pending.json", pending),
                ("success.json", success),
                ("failed.json", failed),
                ("mismatch.json", mismatch),
            ):
                write_json(submissions / name, value)

            write_json(results / "success.json", {
                "job_id": "job-success", "attempt_id": "attempt-success", "ok": True,
            })
            write_json(results / "failed.json", {
                "job_id": "job-failed", "attempt_id": "attempt-failed", "ok": False,
                "error": "durable validation failure",
            })
            write_json(results / "mismatch.json", {
                "job_id": "other-job", "attempt_id": "other-attempt", "ok": True,
            })

            self.assertEqual(self.run_lister(root), [
                ".survey/work-queue/submissions/research/mismatch.json",
                ".survey/work-queue/submissions/research/pending.json",
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

    def test_workflow_sweeps_unsettled_backlog_instead_of_trigger_commit_only(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("list_unsettled_immutable_submissions.py", text)
        self.assertNotIn("git diff-tree --no-commit-id --name-only -r \"$GITHUB_SHA\"", text)
        self.assertIn("Drain all unsettled immutable descriptors", text)


if __name__ == "__main__":
    unittest.main()
