import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def configure(root: Path):
    queue_worker.ROOT = root / ".survey"
    queue_worker.QUEUE = queue_worker.ROOT / "work-queue"
    queue_worker.JOBS = queue_worker.QUEUE / "jobs"
    queue_worker.SUBMISSIONS = queue_worker.QUEUE / "submissions"
    queue_worker.RESULTS = queue_worker.QUEUE / "results"
    queue_worker.STATE = queue_worker.QUEUE / "state.json"
    queue_worker.ARCHIVE = queue_worker.QUEUE / "archive"
    queue_worker.DISCOVERY_STATE = queue_worker.QUEUE / "discovery-state.json"


def state():
    return {
        "schema_version": 1,
        "workflow_version": 10,
        "stats": {
            "discovered": 0,
            "selected": 0,
            "research_completed": 0,
            "audit_completed": 0,
            "rejected": 0,
        },
    }


class DiscoverySubmissionRecoveryTests(unittest.TestCase):
    def test_terminal_discovery_submission_rebinds_to_existing_ready_discovery_job(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            configure(root)
            write_json(queue_worker.JOBS / "job-old.json", {
                "job_id": "job-old",
                "type": "discovery",
                "lane": "discovery",
                "status": "completed",
            })
            write_json(queue_worker.JOBS / "job-new.json", {
                "job_id": "job-new",
                "type": "discovery",
                "lane": "discovery",
                "status": "ready",
                "priority": 50,
            })
            write_json(queue_worker.SUBMISSIONS / "stale.json", {
                "job_id": "job-old",
                "candidates": [],
            })

            queue_worker.process_submissions(state())

            result = json.loads((queue_worker.RESULTS / "stale.json").read_text(encoding="utf-8"))
            rebound = json.loads((queue_worker.JOBS / "job-new.json").read_text(encoding="utf-8"))
            old = json.loads((queue_worker.JOBS / "job-old.json").read_text(encoding="utf-8"))
            self.assertTrue(result["ok"])
            self.assertEqual(result["submitted_job_id"], "job-old")
            self.assertEqual(result["job_id"], "job-new")
            self.assertEqual(rebound["status"], "completed")
            self.assertEqual(old["status"], "completed")

    def test_terminal_discovery_submission_creates_recovery_job_when_none_is_active(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            configure(root)
            write_json(queue_worker.JOBS / "job-old.json", {
                "job_id": "job-old",
                "type": "discovery",
                "lane": "discovery",
                "status": "completed",
            })
            write_json(queue_worker.SUBMISSIONS / "stale.json", {
                "job_id": "job-old",
                "candidates": [],
            })

            queue_worker.process_submissions(state())

            result = json.loads((queue_worker.RESULTS / "stale.json").read_text(encoding="utf-8"))
            self.assertTrue(result["ok"])
            self.assertEqual(result["submitted_job_id"], "job-old")
            self.assertNotEqual(result["job_id"], "job-old")
            recovered = json.loads((queue_worker.JOBS / f"{result['job_id']}.json").read_text(encoding="utf-8"))
            self.assertEqual(recovered["type"], "discovery")
            self.assertEqual(recovered["status"], "completed")


if __name__ == "__main__":
    unittest.main()
