import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_status_dashboard.py"


def _load_module(repo_root: Path):
    path = repo_root / ".survey" / "scripts" / "build_status_dashboard.py"
    spec = importlib.util.spec_from_file_location("build_status_dashboard", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_text(path: Path, text="x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _install_script(repo: Path):
    dst = repo / ".survey" / "scripts" / "build_status_dashboard.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")


class StatusDashboardTests(unittest.TestCase):
    def test_recent_reading_uses_completed_jobs_not_aggregate_ledger(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _install_script(repo)
            _write_json(repo / ".survey/work-queue/run-ledger.json", {
                "entries": [{
                    "run_key": "2026-09-15T18:30:00+09:00",
                    "counts": {"research_completed": 0, "audit_completed": 0},
                }]
            })
            _write_json(repo / ".survey/work-queue/jobs/job-research-a.json", {
                "id": "job-research-a",
                "type": "research",
                "canonical_id": "arXiv:2609.99999",
                "title": "Direct Evidence Paper",
                "status": "completed",
                "completed_at": "2026-09-15T09:38:20+00:00",
                "paper_path": "papers/inference/direct-evidence-paper.md",
                "artifact_submission": ".survey/work-queue/submissions/research/attempt-a.json",
            })
            _write_json(repo / ".survey/work-queue/submissions/research/attempt-a.json", {
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-research-a",
                "worker_id": "scheduled-chat-paper-20260915T1830JST",
            })
            _write_text(repo / "papers/inference/direct-evidence-paper.md", "# Direct Evidence Paper")
            _write_json(repo / ".survey/work-queue/next-jobs.json", {"next_jobs": []})

            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc))

            self.assertIn("## 1. ここ数時間で論文読解・サーベイができているか", text)
            self.assertIn("直近6時間 Research完了 | **1**", text)
            self.assertIn("Direct Evidence Paper", text)
            self.assertIn("job=completed / submission=存在 / paper=存在", text)
            self.assertNotIn("直近6時間 Research完了 | **0**", text)

    def test_terminal_job_never_counts_as_current_work_even_if_claim_unexpired(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _install_script(repo)
            _write_json(repo / ".survey/work-queue/jobs/job-research-done.json", {
                "id": "job-research-done",
                "type": "research",
                "title": "Already Done",
                "status": "completed",
                "completed_at": "2026-09-15T09:37:00+00:00",
            })
            _write_json(repo / ".survey/work-queue/claims/job-research-done.json", {
                "job_id": "job-research-done",
                "claim_id": "claim-done",
                "worker_id": "scheduled-chat-paper-20260915T1830JST",
                "kind": "research",
                "claimed_at": "2026-09-15T09:35:00+00:00",
                "expires_at": "2026-09-15T11:05:00+00:00",
            })
            _write_json(repo / ".survey/work-queue/jobs/job-research-live.json", {
                "id": "job-research-live",
                "type": "research",
                "canonical_id": "arXiv:2609.12345",
                "title": "Currently Reading",
                "status": "ready",
            })
            _write_json(repo / ".survey/work-queue/claims/job-research-live.json", {
                "job_id": "job-research-live",
                "claim_id": "claim-live",
                "worker_id": "scheduled-chat-paper-20260915T1830JST",
                "kind": "research",
                "claimed_at": "2026-09-15T09:40:00+00:00",
                "expires_at": "2026-09-15T11:10:00+00:00",
            })
            _write_json(repo / ".survey/work-queue/next-jobs.json", {"next_jobs": []})

            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc))

            self.assertIn("## 3. 今何をやっているか", text)
            self.assertIn("Currently Reading", text)
            current_section = text.split("## 3. 今何をやっているか", 1)[1]
            self.assertNotIn("Already Done", current_section)

    def test_latest_task_proof_comes_from_immutable_submission_and_terminal_job(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _install_script(repo)
            _write_json(repo / ".survey/work-queue/jobs/job-research-proof.json", {
                "id": "job-research-proof",
                "type": "research",
                "canonical_id": "arXiv:2601.17768",
                "title": "LLM-42",
                "status": "completed",
                "completed_at": "2026-09-15T09:38:20+00:00",
                "paper_path": "papers/inference/llm42.md",
                "artifact_submission": ".survey/work-queue/submissions/research/attempt-proof.json",
            })
            _write_json(repo / ".survey/work-queue/submissions/research/attempt-proof.json", {
                "kind": "research",
                "attempt_id": "attempt-proof",
                "job_id": "job-research-proof",
                "worker_id": "scheduled-chat-paper-20260915T1830JST",
            })
            _write_text(repo / "papers/inference/llm42.md", "# LLM-42")
            _write_json(repo / ".survey/work-queue/submissions/20260915T1808JST-discovery-specialist.json", {
                "job_id": "job-discovery-proof",
                "candidates": [{"canonical_id": "arXiv:2609.04895", "title": "Cache-Aware Router"}],
                "discovery_stats": {
                    "run_key": "2026-09-15T18:00:00+09:00",
                    "round": "specialist-moe-cache-router-1",
                    "axis": "2026年9月新着・MoE expert cache・cache-aware routing",
                    "candidate_count": 1,
                    "duplicate_filtered_count": 0,
                },
            })
            _write_json(repo / ".survey/work-queue/next-jobs.json", {"next_jobs": []})

            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc))

            self.assertIn("## 2. 直近タスクが成功している証拠", text)
            self.assertIn("18:30 通常worker", text)
            self.assertIn("scheduled-chat-paper-20260915T1830JST", text)
            self.assertIn("LLM-42", text)
            self.assertIn("完了job + immutable submission + paper", text)
            self.assertIn("18:00 探索worker", text)
            self.assertIn("MoE expert cache", text)
            self.assertIn("immutable discovery submission", text)


if __name__ == "__main__":
    unittest.main()
