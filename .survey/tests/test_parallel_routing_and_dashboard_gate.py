import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / ".survey/docs/survey-workflow"
GATE = ROOT / ".survey/scripts/status_publish_gate.py"
WORKFLOW = ROOT / ".github/workflows/status-dashboard.yml"
HELPER_WORKFLOW = ROOT / ".github/workflows/survey-helper.yml"
CLAIM_WORKFLOW = ROOT / ".github/workflows/survey-claim-fast.yml"
SUBMISSION_WORKFLOW = ROOT / ".github/workflows/survey-submission-fast.yml"
REPOSITORY_TESTS = ROOT / ".github/workflows/repository-tests.yml"
CANONICAL_RENDER = "render_status_dashboard.py --repo-root . --output STATUS.md"
LEGACY_RENDER = "build_status_dashboard.py --repo-root . --output STATUS.md"


class SpecialistOverflowRoutingTests(unittest.TestCase):
    def test_canonical_router_routes_specialist_to_research_above_50(self):
        router = (DOCS / "worker-router.md").read_text(encoding="utf-8")
        self.assertIn("candidate_inventory > 50", router)
        self.assertIn("overflow research mode", router)
        self.assertIn("通常論文ワーカーと同じ研究処理", router)

    def test_repository_tests_watch_single_worker_router(self):
        text = REPOSITORY_TESTS.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count(".survey/docs/survey-workflow/worker-router.md"), 2)
        self.assertNotIn(".survey/docs/survey-workflow/discovery-specialist-worker.md", text)
        self.assertNotIn(".survey/docs/survey-workflow/candidate-buffer-policy.md", text)


class StatusPublishGateTests(unittest.TestCase):
    def run_gate(self, paths, message="survey: worker update"):
        self.assertTrue(GATE.is_file(), "status_publish_gate.py must exist")
        proc = subprocess.run(
            [sys.executable, str(GATE), "--commit-message", message],
            input="\n".join(paths) + "\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return proc.stdout.strip()

    def test_claim_request_ingress_does_not_publish_dashboard(self):
        self.assertEqual(
            self.run_gate([".survey/work-queue/claim-requests/req-a.json"]),
            "false",
        )

    def test_immutable_descriptor_ingress_does_not_publish_dashboard(self):
        self.assertEqual(
            self.run_gate([
                ".survey/work-queue/records/chat-record-a/metadata.json",
                ".survey/work-queue/submissions/research/attempt-a.json",
            ]),
            "false",
        )

    def test_authoritative_claim_result_publishes_dashboard(self):
        self.assertEqual(
            self.run_gate([
                ".survey/work-queue/claim-results/req-a.json",
                ".survey/work-queue/claims/job-a.json",
                ".survey/work-queue/next-jobs.json",
            ], message="survey-claim: allocate one-job claims and reserve banks"),
            "true",
        )

    def test_merge_commit_publishes_even_when_diff_tree_emits_no_paths(self):
        self.assertEqual(
            self.run_gate([], message="Merge workflow-v10 transport cleanup"),
            "true",
        )

    def test_dashboard_self_commit_does_not_republish(self):
        self.assertEqual(
            self.run_gate([
                "STATUS.md",
                ".survey/work-queue/run-ledger.json",
            ], message="chore: refresh survey status dashboard"),
            "false",
        )

    def test_status_workflow_uses_canonical_renderer_only(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("render_status_dashboard.py", text)
        self.assertNotIn(LEGACY_RENDER, text)
        self.assertNotIn("append_research_throughput_status.py", text)
        self.assertNotIn("refine_status_observability.py", text)

    def test_claim_fast_lane_defers_dashboard_rendering_to_status_lane(self):
        text = CLAIM_WORKFLOW.read_text(encoding="utf-8")
        self.assertNotIn(CANONICAL_RENDER, text)
        self.assertNotIn(LEGACY_RENDER, text)
        self.assertNotIn("append_research_throughput_status.py --repo-root . --status STATUS.md", text)
        self.assertNotIn("STATUS.md", text)
        self.assertIn(".survey/work-queue/claim-results", text)

    def test_submission_fast_lane_keeps_canonical_renderer_with_inert_compatibility_shims(self):
        text = SUBMISSION_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn(CANONICAL_RENDER, text)
        self.assertNotIn(LEGACY_RENDER, text)
        self.assertIn("append_research_throughput_status.py --repo-root . --status STATUS.md", text)
        self.assertIn("STATUS.md", text)

    def test_background_helper_uses_canonical_renderer_with_inert_compatibility_shims(self):
        text = HELPER_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("refresh_status_dashboard", text)
        self.assertIn("status_publish_gate.py", text)
        self.assertIn(CANONICAL_RENDER, text)
        self.assertNotIn(LEGACY_RENDER, text)
        self.assertIn("append_research_throughput_status.py --repo-root . --status STATUS.md", text)
        self.assertIn("refine_status_observability.py --repo-root . --status STATUS.md", text)
        self.assertIn("git add STATUS.md .survey/work-queue/run-ledger.json .survey/work-queue/discovery-state.json", text)
        self.assertIn("git commit --amend --no-edit", text)


if __name__ == "__main__":
    unittest.main()
