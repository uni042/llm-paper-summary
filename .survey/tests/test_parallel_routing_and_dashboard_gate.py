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


class SpecialistOverflowRoutingTests(unittest.TestCase):
    def test_canonical_docs_route_specialist_to_research_above_50(self):
        specialist = (DOCS / "discovery-specialist-worker.md").read_text(encoding="utf-8")
        buffer_policy = (DOCS / "candidate-buffer-policy.md").read_text(encoding="utf-8")

        for name, text in (
            ("discovery-specialist-worker.md", specialist),
            ("candidate-buffer-policy.md", buffer_policy),
        ):
            with self.subTest(document=name):
                self.assertIn("candidate_inventory > 50", text)

        self.assertIn("overflow research mode", specialist)
        self.assertIn("通常論文workerと同じ", specialist)
        self.assertNotIn(
            "candidate在庫が50本、100本、それ以上でも、在庫数だけを理由に探索を弱めたり停止したりしない",
            specialist,
        )

    def test_repository_tests_watch_overflow_policy_documents(self):
        text = REPOSITORY_TESTS.read_text(encoding="utf-8")
        self.assertGreaterEqual(text.count(".survey/docs/survey-workflow/discovery-specialist-worker.md"), 2)
        self.assertGreaterEqual(text.count(".survey/docs/survey-workflow/candidate-buffer-policy.md"), 2)


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

    def test_status_workflow_is_direct_builder_only(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("build_status_dashboard.py", text)
        self.assertNotIn("append_research_throughput_status.py", text)
        self.assertNotIn("refine_status_observability.py", text)

    def test_fast_lanes_keep_compatibility_shims_inert_after_direct_build(self):
        for workflow in (CLAIM_WORKFLOW, SUBMISSION_WORKFLOW):
            text = workflow.read_text(encoding="utf-8")
            with self.subTest(workflow=workflow.name):
                self.assertIn("build_status_dashboard.py --repo-root . --output STATUS.md", text)
                self.assertIn("append_research_throughput_status.py --repo-root . --status STATUS.md", text)
                self.assertIn("STATUS.md", text)

    def test_background_helper_keeps_compatibility_shims_inert_after_direct_build(self):
        text = HELPER_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("refresh_status_dashboard", text)
        self.assertIn("status_publish_gate.py", text)
        self.assertIn("build_status_dashboard.py --repo-root . --output STATUS.md", text)
        self.assertIn("append_research_throughput_status.py --repo-root . --status STATUS.md", text)
        self.assertIn("refine_status_observability.py --repo-root . --status STATUS.md", text)
        self.assertIn("git add STATUS.md .survey/work-queue/run-ledger.json .survey/work-queue/discovery-state.json", text)
        self.assertIn("git commit --amend --no-edit", text)


if __name__ == "__main__":
    unittest.main()
