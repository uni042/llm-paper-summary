import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "survey-claim-fast.yml"


class ClaimFastLaneScopeTests(unittest.TestCase):
    def test_fast_lane_keeps_claim_safety_steps(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for script in (
            "normalize_research_paper_paths.py",
            "apply_library_checkpoint_barriers.py",
            "claim_worker_with_banks.py",
            "repair_claim_bank_recovery.py",
            "enrich_claim_record_routes.py",
        ):
            with self.subTest(script=script):
                self.assertIn(script, text)

    def test_fast_lane_excludes_dashboard_and_status_work(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for forbidden in (
            "refresh_queue_snapshot.py",
            "ensure_dashboard_history.py",
            "render_status_dashboard.py",
            "append_research_throughput_status.py",
            "refine_status_observability.py",
            "STATUS.md",
            ".survey/work-queue/next-jobs.json",
            ".survey/work-queue/run-ledger.json",
            ".survey/work-queue/discovery-state.json",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
