import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).parents[2]
THROUGHPUT_SCRIPT = ROOT / ".survey" / "scripts" / "append_research_throughput_status.py"
DASHBOARD_SCRIPT = ROOT / ".survey" / "scripts" / "build_status_dashboard.py"
REFINER_SCRIPT = ROOT / ".survey" / "scripts" / "refine_status_observability.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


class StatusObservabilityTests(unittest.TestCase):
    def test_worker_status_separates_latest_run_from_old_valid_leases(self):
        throughput = _load(THROUGHPUT_SCRIPT, "status_throughput_observability")
        refiner = _load(REFINER_SCRIPT, "status_refiner_worker_observability")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 3}},
                "claiming": {"ready_research_audit": 3, "actively_claimed": 3, "claimable": 0},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            for job_id in ("job-normal", "job-aux-current", "job-aux-old"):
                _write(repo / f".survey/work-queue/jobs/{job_id}.json", {
                    "job_id": job_id,
                    "type": "research",
                    "status": "ready",
                })
            _write(repo / ".survey/work-queue/claims/job-normal.json", {
                "job_id": "job-normal",
                "worker_id": "scheduled-chat-llm-survey-20260914T1830JST",
                "claimed_at": "2026-09-14T09:35:00+00:00",
                "expires_at": "2026-09-14T11:05:00+00:00",
            })
            _write(repo / ".survey/work-queue/claims/job-aux-current.json", {
                "job_id": "job-aux-current",
                "worker_id": "scheduled-chat-discovery-overflow-20260914T1800JST",
                "claimed_at": "2026-09-14T09:38:00+00:00",
                "expires_at": "2026-09-14T11:08:00+00:00",
            })
            _write(repo / ".survey/work-queue/claims/job-aux-old.json", {
                "job_id": "job-aux-old",
                "worker_id": "scheduled-chat-discovery-overflow-20260914T1700JST",
                "claimed_at": "2026-09-14T08:35:00+00:00",
                "expires_at": "2026-09-14T10:05:00+00:00",
            })

            now = datetime(2026, 9, 14, 9, 40, tzinfo=timezone.utc)
            base = throughput.render_section(repo, now=now)
            text = refiner.refine_text(repo, base, now=now)

            self.assertIn("有効claim（lease） | **3**", text)
            self.assertIn(":30 最新worker run | **2026-09-14T18:30:00+09:00**", text)
            self.assertIn(":30 最新run由来の有効claim | **1**", text)
            self.assertIn(":30 旧run由来の有効claim | **0**", text)
            self.assertIn(":00 最新worker run | **2026-09-14T18:00:00+09:00**", text)
            self.assertIn(":00 最新run由来の有効claim | **1**", text)
            self.assertIn(":00 旧run由来の有効claim | **1**", text)
            self.assertNotIn("処理中（Active claims）", text)
            self.assertIn("Scheduled Chatプロセスの生存そのものではありません", text)

    def test_dashboard_distinguishes_integrated_checkpointed_and_unique_read_papers(self):
        dashboard = _load(DASHBOARD_SCRIPT, "status_dashboard_observability")
        refiner = _load(REFINER_SCRIPT, "status_refiner_progress_observability")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"completed": 2, "ready": 2, "blocked": 0, "deferred": 0}},
                "next_jobs": [],
            })
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "maintenance_pending": False,
                "last_maintenance_status": "passed",
                "last_consistency_status": "passed",
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            _write(repo / ".survey/work-queue/discovery-state.json", {"history": []})

            jobs = (
                ("job-a", "arXiv:A", "completed"),
                ("job-b", "arXiv:B", "completed"),
                ("job-c1", "arXiv:C", "ready"),
                ("job-c2", "arXiv:C", "ready"),
            )
            for job_id, canonical_id, status in jobs:
                _write(repo / f".survey/work-queue/jobs/{job_id}.json", {
                    "job_id": job_id,
                    "type": "research",
                    "canonical_id": canonical_id,
                    "status": status,
                })

            _write(repo / ".survey/work-queue/claim-requests/request-1.json", {
                "checkpointed_jobs": [
                    {"job_id": "job-a", "checkpoint_ref": "/pending/a.json"},
                    {"job_id": "job-c1", "checkpoint_ref": "/pending/c1.json"},
                ]
            })
            _write(repo / ".survey/work-queue/claim-requests/request-2.json", {
                "checkpointed_jobs": [
                    {"job_id": "job-c2", "checkpoint_ref": "/pending/c2.json"},
                ]
            })

            now = datetime(2026, 9, 14, 9, 40, tzinfo=timezone.utc)
            base = dashboard.build_dashboard(repo, now=now)
            text = refiner.refine_text(repo, base, now=now)

            self.assertIn("GitHub反映済みResearch完了（job） | **2**", text)
            self.assertIn("耐久checkpoint済み・GitHub未反映（job） | **2**", text)
            self.assertIn("精読済みユニーク論文（推定） | **3**", text)
            self.assertNotIn("全文精読完了（累計）", text)
            self.assertIn("canonical IDで重複排除", text)

    def test_refinement_is_idempotent(self):
        refiner = _load(REFINER_SCRIPT, "status_refiner_idempotence")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _write(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "research", "canonical_id": "arXiv:A", "status": "completed"
            })
            base = (
                "# 運用ダッシュボード\n\n"
                "## 現在の状態\n\n"
                "| 指標 | 状態 |\n|---|---:|\n| 全文精読完了（累計） | **1** |\n\n"
                "### 要注意\n\n"
                "<!-- research-throughput-status:start -->\n"
                "## ワーカー稼働状況\n\n"
                "| 指標 | 状態 |\n|---|---:|\n"
                "| 未処理候補（Research ready） | **0** |\n"
                "| 処理中（Active claims） | **0** |\n"
                "| 今すぐ着手可能（Claimable） | **0** |\n"
                "<!-- research-throughput-status:end -->\n"
            )
            now = datetime(2026, 9, 14, 9, 40, tzinfo=timezone.utc)
            once = refiner.refine_text(repo, base, now=now)
            twice = refiner.refine_text(repo, once, now=now)
            self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
