from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".survey/scripts"
sys.path.insert(0, str(SCRIPTS))

import refresh_queue_snapshot  # noqa: E402


class QueueSnapshotRefreshTests(unittest.TestCase):
    def test_refresh_rewrites_only_derived_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            repo_root = Path(td)
            queue = repo_root / ".survey/work-queue"
            jobs = queue / "jobs"
            jobs.mkdir(parents=True)
            (jobs / "job-research-ready.json").write_text(
                json.dumps(
                    {
                        "job_id": "job-research-ready",
                        "type": "research",
                        "lane": "research",
                        "status": "ready",
                        "priority": 90,
                        "created_at": "2026-09-14T00:00:00+00:00",
                    }
                ),
                encoding="utf-8",
            )
            state = queue / "state.json"
            state.write_text('{"sentinel":"keep"}\n', encoding="utf-8")
            snapshot = queue / "next-jobs.json"
            snapshot.write_text('{"counts":{},"next_jobs":[],"generated_at":"old"}\n', encoding="utf-8")

            refreshed = refresh_queue_snapshot.refresh(repo_root)

            self.assertEqual(
                [row["job_id"] for row in refreshed["next_jobs"]],
                ["job-research-ready"],
            )
            self.assertEqual(state.read_text(encoding="utf-8"), '{"sentinel":"keep"}\n')
            persisted = json.loads(snapshot.read_text(encoding="utf-8"))
            self.assertEqual(persisted["next_jobs"], refreshed["next_jobs"])
            self.assertIn("generated_at", persisted)

    def test_survey_helper_rebase_recovers_only_derived_snapshot_conflicts(self) -> None:
        workflow = (ROOT / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertIn("git diff --name-only --diff-filter=U", workflow)
        self.assertIn(".survey/work-queue/next-jobs.json", workflow)
        self.assertIn("python .survey/scripts/refresh_queue_snapshot.py --repo-root .", workflow)
        self.assertIn("git rebase --abort", workflow)
        self.assertIn("git rebase --skip", workflow)


if __name__ == "__main__":
    unittest.main()
