import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_status_dashboard.py"


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_text(path: Path, text="x"):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load(repo: Path):
    dst = repo / ".survey/scripts/build_status_dashboard.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("build_status_dashboard_direct", dst)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _research_success(repo: Path, *, job_id="job-r", attempt="attempt-r",
                      worker="scheduled-chat-paper-20260915T1830JST",
                      completed="2026-09-15T09:38:20+00:00",
                      canonical="arXiv:2609.12345", title="Verified Paper"):
    paper = f"papers/inference/{job_id}.md"
    submission = f".survey/work-queue/submissions/research/{attempt}.json"
    result = f".survey/work-queue/results/research/{attempt}.json"
    _write_json(repo / f".survey/work-queue/jobs/{job_id}.json", {
        "job_id": job_id, "type": "research", "canonical_id": canonical,
        "title": title, "status": "completed", "completed_at": completed,
        "paper_path": paper, "artifact_submission": submission,
    })
    _write_json(repo / submission, {
        "kind": "research", "attempt_id": attempt, "job_id": job_id,
        "worker_id": worker, "paper_path": paper,
    })
    _write_json(repo / result, {
        "ok": True, "attempt_id": attempt, "job_id": job_id,
        "job_type": "research", "job_status": "completed",
        "artifact": {"paper": paper}, "submission": submission,
        "processed_at": completed,
    })
    _write_text(repo / paper, "# paper")


class DirectEvidenceStatusTests(unittest.TestCase):
    def test_verified_research_ignores_conflicting_aggregate_files(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _research_success(repo)
            _write_json(repo / ".survey/work-queue/run-ledger.json", {
                "entries": [{"counts": {"research_completed": 0}}]
            })
            _write_json(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"completed": 999}}
            })
            _write_json(repo / ".survey/work-queue/discovery-state.json", {
                "research_completed": 999
            })

            text = _load(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)
            )
            self.assertIn("直近6時間 Research完了 | **1**", text)
            self.assertIn("result:", text)
            self.assertIn("submission:", text)
            self.assertIn("paper:", text)
            self.assertNotIn("**999**", text)
            self.assertIn("run-ledger", text)

    def test_completed_job_without_success_result_is_not_counted(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            paper = "papers/inference/unverified.md"
            submission = ".survey/work-queue/submissions/research/attempt-u.json"
            _write_json(repo / ".survey/work-queue/jobs/job-u.json", {
                "job_id": "job-u", "type": "research", "status": "completed",
                "completed_at": "2026-09-15T09:38:20+00:00",
                "paper_path": paper,
            })
            _write_json(repo / submission, {
                "kind": "research", "attempt_id": "attempt-u", "job_id": "job-u",
                "worker_id": "scheduled-chat-paper-20260915T1830JST",
                "paper_path": paper,
            })
            _write_text(repo / paper, "# paper")
            text = _load(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)
            )
            self.assertIn("直近6時間 Research完了 | **0**", text)
            self.assertIn("未完了または未検証", text)

    def test_latest_paper_worker_requires_result_submission_job_and_paper(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _research_success(
                repo, job_id="job-proof", attempt="attempt-proof",
                canonical="arXiv:2601.17768", title="LLM-42"
            )
            text = _load(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)
            )
            self.assertIn("2026-09-15 18:30 JST", text)
            self.assertIn("scheduled-chat-paper-20260915T1830JST", text)
            self.assertIn("検証済み成功: **1件**", text)
            self.assertIn("LLM-42", text)
            self.assertIn("result `", text)
            self.assertIn("/ paper `", text)

    def test_latest_discovery_success_requires_result_and_completed_job(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            submission = ".survey/work-queue/submissions/20260915T1808JST-discovery.json"
            result = ".survey/work-queue/results/20260915T1808JST-discovery.json"
            _write_json(repo / ".survey/work-queue/jobs/job-d.json", {
                "job_id": "job-d", "type": "discovery", "status": "completed",
                "completed_at": "2026-09-15T09:02:53+00:00",
            })
            _write_json(repo / submission, {
                "job_id": "job-d",
                "candidates": [{"canonical_id": "arXiv:2609.04895"}],
                "discovery_stats": {
                    "run_key": "2026-09-15T18:00:00+09:00",
                    "axis": "MoE expert cache",
                    "candidate_count": 1,
                },
            })
            _write_json(repo / result, {
                "ok": True, "job_id": "job-d", "job_type": "discovery",
                "job_status": "completed",
                "submission": "work-queue/submissions/20260915T1808JST-discovery.json",
            })
            text = _load(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)
            )
            self.assertIn("2026-09-15 18:00 JST", text)
            self.assertIn("検証済み成功result: **1件**", text)
            self.assertIn("候補: **1件**", text)
            self.assertIn("MoE expert cache", text)

    def test_active_work_excludes_terminal_claim_and_shows_nonterminal_heartbeat(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write_json(repo / ".survey/work-queue/jobs/job-done.json", {
                "job_id": "job-done", "type": "research", "title": "Already Done",
                "status": "completed", "completed_at": "2026-09-15T09:37:00+00:00",
            })
            _write_json(repo / ".survey/work-queue/claims/job-done.json", {
                "job_id": "job-done", "worker_id": "worker-old",
                "claimed_at": "2026-09-15T09:35:00+00:00",
                "heartbeat_at": "2026-09-15T09:42:00+00:00",
                "expires_at": "2026-09-15T11:05:00+00:00",
            })
            _write_json(repo / ".survey/work-queue/jobs/job-live.json", {
                "job_id": "job-live", "type": "research", "title": "Currently Reading",
                "status": "ready",
            })
            _write_json(repo / ".survey/work-queue/claims/job-live.json", {
                "job_id": "job-live", "worker_id": "scheduled-chat-paper-20260915T1830JST",
                "claimed_at": "2026-09-15T09:40:00+00:00",
                "heartbeat_at": "2026-09-15T09:43:00+00:00",
                "expires_at": "2026-09-15T11:10:00+00:00",
            })
            text = _load(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)
            )
            current = text.split("## 3. 今何をやっているか", 1)[1]
            self.assertIn("未失効かつ非terminal jobのclaim: **1件**", current)
            self.assertIn("直近15分にheartbeat記録あり: **1件**", current)
            self.assertIn("Currently Reading", current)
            self.assertNotIn("Already Done", current)
            self.assertIn("生存そのものまでは証明しない", current)

    def test_summary_splits_research_audit_discovery_and_moves_evidence_below(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _research_success(repo)

            _write_json(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "audit", "title": "Audit Item",
                "status": "completed", "completed_at": "2026-09-15T09:37:00+00:00",
            })
            _write_json(repo / ".survey/work-queue/submissions/audit/attempt-a.json", {
                "kind": "audit", "attempt_id": "attempt-a", "job_id": "job-a",
                "worker_id": "scheduled-chat-paper-20260915T1830JST",
            })
            _write_json(repo / ".survey/work-queue/results/audit/attempt-a.json", {
                "ok": True, "attempt_id": "attempt-a", "job_id": "job-a",
                "job_type": "audit", "job_status": "completed",
                "submission": ".survey/work-queue/submissions/audit/attempt-a.json",
                "processed_at": "2026-09-15T09:37:00+00:00",
            })

            discovery_submission = ".survey/work-queue/submissions/20260915T1800JST-discovery.json"
            _write_json(repo / ".survey/work-queue/jobs/job-d.json", {
                "job_id": "job-d", "type": "discovery", "status": "completed",
                "completed_at": "2026-09-15T09:02:53+00:00",
            })
            _write_json(repo / discovery_submission, {
                "job_id": "job-d",
                "candidates": [{"canonical_id": "arXiv:2609.04895"}],
                "discovery_stats": {
                    "run_key": "2026-09-15T18:00:00+09:00",
                    "axis": "MoE expert cache",
                    "candidate_count": 1,
                },
            })
            _write_json(repo / ".survey/work-queue/results/20260915T1800JST-discovery.json", {
                "ok": True, "job_id": "job-d", "job_type": "discovery",
                "job_status": "completed", "processed_at": "2026-09-15T09:02:53+00:00",
                "submission": "work-queue/submissions/20260915T1800JST-discovery.json",
            })

            for kind, job_id, title in [
                ("research", "job-live-r", "Reading Now"),
                ("audit", "job-live-a", "Auditing Now"),
                ("discovery", "job-live-d", "Searching Now"),
            ]:
                _write_json(repo / f".survey/work-queue/jobs/{job_id}.json", {
                    "job_id": job_id, "type": kind, "title": title, "status": "ready",
                })
                _write_json(repo / f".survey/work-queue/claims/{job_id}.json", {
                    "job_id": job_id, "worker_id": f"worker-{kind}",
                    "claimed_at": "2026-09-15T09:40:00+00:00",
                    "heartbeat_at": "2026-09-15T09:43:00+00:00",
                    "expires_at": "2026-09-15T11:10:00+00:00",
                })

            text = _load(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)
            )
            summary, details = text.split("## 詳細証拠", 1)
            self.assertIn("## 件数サマリー", summary)
            self.assertIn("| Research | **1** | **1** | **1** | **0** | **1** | **1** | — |", summary)
            self.assertIn("| Audit | **1** | **1** | **1** | **0** | **1** | **1** | — |", summary)
            self.assertIn("| Discovery | **1** | **1** | **1** | **0** | **1** | **1** | **1** |", summary)
            self.assertIn("| 合計 | **3** | **3** | **3** | **0** | **3** | **3** | **1** |", summary)
            self.assertNotIn("job-r", summary)
            self.assertNotIn("papers/inference", summary)
            self.assertIn("### Research", details)
            self.assertIn("### Audit", details)
            self.assertIn("### Discovery", details)
            self.assertIn("Reading Now", details)
            self.assertIn("Auditing Now", details)
            self.assertIn("Searching Now", details)

    def test_legacy_aggregate_changes_cannot_change_direct_count(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _research_success(repo, canonical="arXiv:2609.54321")
            module = _load(repo)
            now = datetime(2026, 9, 15, 9, 44, tzinfo=timezone.utc)

            _write_json(repo / ".survey/work-queue/run-ledger.json", {"research_completed": 0})
            first = module.build_dashboard(repo, now=now)
            _write_json(repo / ".survey/work-queue/run-ledger.json", {"research_completed": 5000})
            _write_json(repo / ".survey/work-queue/next-jobs.json", {"completed": 5000})
            second = module.build_dashboard(repo, now=now)

            marker = "直近6時間 Research完了 | **1**"
            self.assertIn(marker, first)
            self.assertIn(marker, second)
            self.assertNotIn("**5000**", second)


if __name__ == "__main__":
    unittest.main()
