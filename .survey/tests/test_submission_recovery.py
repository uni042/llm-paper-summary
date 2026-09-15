import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import recover_discovery_submissions as recovery  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def survey_root(root: Path) -> Path:
    return root / ".survey"


class DiscoverySubmissionRecoveryTests(unittest.TestCase):
    def test_terminal_discovery_submission_uses_dedicated_recovery_job(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sr = survey_root(root)
            jobs = sr / "work-queue/jobs"
            submissions = sr / "work-queue/submissions"
            results = sr / "work-queue/results"
            write_json(jobs / "job-old.json", {
                "job_id": "job-old",
                "type": "discovery",
                "lane": "discovery",
                "status": "completed",
            })
            write_json(jobs / "job-normal-ready.json", {
                "job_id": "job-normal-ready",
                "type": "discovery",
                "lane": "discovery",
                "status": "ready",
                "priority": 50,
            })
            write_json(submissions / "stale.json", {
                "job_id": "job-old",
                "candidates": [],
            })

            summary = recovery.recover(sr)

            result = json.loads((results / "stale.json").read_text(encoding="utf-8"))
            normal = json.loads((jobs / "job-normal-ready.json").read_text(encoding="utf-8"))
            old = json.loads((jobs / "job-old.json").read_text(encoding="utf-8"))
            recovered = json.loads((jobs / f"{result['job_id']}.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["recovered_count"], 1)
            self.assertTrue(result["ok"])
            self.assertTrue(result["recovered"])
            self.assertEqual(result["submitted_job_id"], "job-old")
            self.assertNotEqual(result["job_id"], "job-normal-ready")
            self.assertEqual(normal["status"], "ready")
            self.assertEqual(old["status"], "completed")
            self.assertTrue(recovered["recovery_only"])
            self.assertEqual(recovered["status"], "completed")

    def test_terminal_discovery_submission_creates_recovery_job_when_no_normal_job_exists(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sr = survey_root(root)
            jobs = sr / "work-queue/jobs"
            submissions = sr / "work-queue/submissions"
            results = sr / "work-queue/results"
            write_json(jobs / "job-old.json", {
                "job_id": "job-old",
                "type": "discovery",
                "lane": "discovery",
                "status": "completed",
            })
            write_json(submissions / "stale.json", {
                "job_id": "job-old",
                "candidates": [],
            })

            summary = recovery.recover(sr)

            result = json.loads((results / "stale.json").read_text(encoding="utf-8"))
            self.assertEqual(summary["recovered_count"], 1)
            self.assertTrue(result["ok"])
            self.assertEqual(result["submitted_job_id"], "job-old")
            self.assertNotEqual(result["job_id"], "job-old")
            recovered = json.loads((jobs / f"{result['job_id']}.json").read_text(encoding="utf-8"))
            self.assertEqual(recovered["type"], "discovery")
            self.assertTrue(recovered["recovery_only"])
            self.assertEqual(recovered["status"], "completed")
            active = [
                json.loads(path.read_text(encoding="utf-8"))
                for path in jobs.glob("*.json")
                if json.loads(path.read_text(encoding="utf-8")).get("status") == "ready"
            ]
            self.assertTrue(any(job.get("type") == "discovery" for job in active))

    def test_non_discovery_terminal_job_is_never_rebound(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            sr = survey_root(root)
            jobs = sr / "work-queue/jobs"
            submissions = sr / "work-queue/submissions"
            results = sr / "work-queue/results"
            write_json(jobs / "job-research.json", {
                "job_id": "job-research",
                "type": "research",
                "status": "completed",
            })
            write_json(submissions / "must-not-rebind.json", {
                "job_id": "job-research",
                "candidates": [],
            })

            summary = recovery.recover(sr)

            self.assertEqual(summary["recovered_count"], 0)
            self.assertFalse((results / "must-not-rebind.json").exists())
            research = json.loads((jobs / "job-research.json").read_text(encoding="utf-8"))
            self.assertEqual(research["status"], "completed")


if __name__ == "__main__":
    unittest.main()
