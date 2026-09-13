import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
WORKFLOWS = ROOT / ".github" / "workflows"


class WorkflowLaneSeparationTests(unittest.TestCase):
    def _text(self, name):
        path = WORKFLOWS / name
        self.assertTrue(path.exists(), f"missing workflow: {name}")
        return path.read_text(encoding="utf-8")

    def test_claim_fast_lane_is_short_and_isolated(self):
        text = self._text("survey-claim-fast.yml")
        self.assertIn("group: survey-claim-main", text)
        self.assertIn(".survey/work-queue/claim-requests/*.json", text)
        self.assertIn("claim_worker.py", text)
        self.assertIn("refresh_queue_snapshot.py", text)
        for forbidden in (
            "dispatch_fallback_inbox.py",
            "queue_worker.py --root",
            "dedupe_queue.py",
            "blocked_retry.py",
            "backfill_citations.py",
            "backfill_citation_pdfs.py",
            "recover_blocked_citations.py",
            "survey.py --root .survey build",
            "full_gc.py",
        ):
            self.assertNotIn(forbidden, text)

    def test_submission_fast_lane_processes_only_changed_immutable_descriptors(self):
        text = self._text("survey-submission-fast.yml")
        self.assertIn("group: survey-submission-main", text)
        self.assertIn(".survey/work-queue/submissions/research/*.json", text)
        self.assertIn(".survey/work-queue/submissions/audit/*.json", text)
        self.assertIn("process_immutable_submission.py", text)
        self.assertNotIn("queue_worker.py --root", text)
        self.assertNotIn("dispatch_fallback_inbox.py", text)
        self.assertNotIn("backfill_citations.py", text)

    def test_submission_fast_lane_persists_failure_result_before_failing(self):
        text = self._text("survey-submission-fast.yml")
        self.assertIn("processing_failed=0", text)
        self.assertIn("if ! python .survey/scripts/process_immutable_submission.py", text)
        self.assertIn(".survey/work-queue/results/research", text)
        self.assertIn(".survey/work-queue/results/audit", text)
        self.assertIn("Immutable submission failure result was persisted to main.", text)

    def test_background_helper_no_longer_owns_claim_or_immutable_submission_triggers(self):
        text = self._text("survey-helper.yml")
        self.assertIn("group: survey-background-main", text)
        self.assertNotIn(".survey/work-queue/claim-requests/*.json", text)
        self.assertNotIn(".survey/work-queue/submissions/research/*.json", text)
        self.assertNotIn(".survey/work-queue/submissions/audit/*.json", text)
        self.assertNotIn("Allocate repository-backed worker claims", text)
        self.assertNotIn("claim_worker.py --repo-root", text)

    def test_heavy_writer_workflows_share_background_lock_not_fast_lanes(self):
        for name in ("maintenance.yml", "citation-graph-backfill.yml", "rebuild-paper-indexes.yml"):
            text = self._text(name)
            self.assertIn("group: survey-background-main", text, name)
            self.assertNotIn("group: survey-claim-main", text, name)
            self.assertNotIn("group: survey-submission-main", text, name)


if __name__ == "__main__":
    unittest.main()
