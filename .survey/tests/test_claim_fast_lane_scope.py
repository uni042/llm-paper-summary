import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "survey-claim-fast.yml"
FAST_PATH = ROOT / ".survey" / "scripts" / "claim_fast_path.py"


class ClaimFastLaneScopeTests(unittest.TestCase):
    def test_fast_lane_uses_shared_claim_path_and_skips_redundant_hot_path_steps(self):
        workflow = WORKFLOW.read_text(encoding="utf-8")
        helper = FAST_PATH.read_text(encoding="utf-8")
        self.assertIn("claim_fast_path.py", workflow)
        self.assertNotIn("py_compile", workflow)
        self.assertNotIn("enrich_claim_record_routes.py", workflow)
        self.assertNotIn("repair_claim_bank_recovery.py", workflow)
        self.assertIn("apply_library_checkpoint_barriers", helper)
        self.assertIn("claim_worker_with_banks", helper)
        self.assertIn("_repair_needed", helper)
        self.assertIn("repair_claim_bank_recovery", helper)

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
