import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "append_research_throughput_status.py"


def _load_module(repo_root: Path):
    path = repo_root / ".survey" / "scripts" / "append_research_throughput_status.py"
    spec = importlib.util.spec_from_file_location("append_research_throughput_status", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _install_script(repo: Path):
    dst = repo / ".survey" / "scripts" / "append_research_throughput_status.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")


class ResearchThroughputStatusTests(unittest.TestCase):
    def test_high_backlog_section_reports_claiming_low_throughput_and_research_assist(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 180, "completed": 210}},
                "claiming": {"ready_research_audit": 180, "actively_claimed": 23, "claimable": 157},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {"run_key": "2026-09-13T11:30:00+09:00", "counts": {"research_completed": 0}},
                {"run_key": "2026-09-13T12:30:00+09:00", "counts": {"research_completed": 1}},
            ]})
            _write(repo / ".survey/work-queue/jobs/job-r1.json", {
                "job_id": "job-r1",
                "type": "research",
                "status": "ready",
            })
            _write(repo / ".survey/work-queue/claims/job-r1.json", {
                "job_id": "job-r1",
                "claimed_at": "2026-09-13T03:00:00+00:00",
                "expires_at": "2026-09-13T05:00:00+00:00",
            })
            module = _load_module(repo)
            text = module.render_section(repo, now=datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc))
            self.assertIn("## ワーカー稼働状況", text)
            self.assertIn("未処理候補（Research ready） | **180**", text)
            self.assertIn("処理中（Active claims） | **23**", text)
            self.assertIn("今すぐ着手可能（Claimable） | **157**", text)
            self.assertIn(":00 補助worker | **通常worker補助（Research/Audit）**", text)
            self.assertIn("50本を超える間は`:00` workerも論文精読側", text)
            self.assertIn("最新通常runのResearch完了 | **1**", text)
            self.assertIn("最古の有効claimの経過時間 | **60 min**", text)
            self.assertIn("処理速度 | **LOW**", text)
            self.assertIn("最低3件", text)
            self.assertIn("claim-fast → 予約bank → attempt固有immutable descriptor → submission-fast", text)
            self.assertIn("claim-fast / submission-fast / background", text)
            self.assertIn("旧固定 `chat-inbox.json` は通常経路では使いません", text)

    def test_oldest_active_claim_age_ignores_unexpired_claim_for_terminal_job(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 1}},
                "claiming": {"ready_research_audit": 1, "actively_claimed": 1, "claimable": 0},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            _write(repo / ".survey/work-queue/jobs/job-old.json", {
                "job_id": "job-old",
                "type": "research",
                "status": "completed",
            })
            _write(repo / ".survey/work-queue/jobs/job-live.json", {
                "job_id": "job-live",
                "type": "research",
                "status": "ready",
            })
            _write(repo / ".survey/work-queue/claims/job-old.json", {
                "job_id": "job-old",
                "claimed_at": "2026-09-13T02:00:00+00:00",
                "expires_at": "2026-09-13T05:20:00+00:00",
            })
            _write(repo / ".survey/work-queue/claims/job-live.json", {
                "job_id": "job-live",
                "claimed_at": "2026-09-13T03:30:00+00:00",
                "expires_at": "2026-09-13T05:00:00+00:00",
            })
            module = _load_module(repo)
            text = module.render_section(repo, now=datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc))
            self.assertIn("最古の有効claimの経過時間 | **30 min**", text)
            self.assertNotIn("120 min", text)

    def test_auxiliary_worker_returns_to_discovery_at_50_or_below(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 50}},
                "claiming": {"ready_research_audit": 50, "actively_claimed": 3, "claimable": 47},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {"run_key": "2026-09-13T12:30:00+09:00", "counts": {"research_completed": 3}},
            ]})
            module = _load_module(repo)
            text = module.render_section(repo, now=datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc))
            self.assertIn(":00 補助worker | **Discovery優先**", text)
            self.assertIn("50本以下になるとDiscovery優先へ戻ります", text)

    def test_three_completed_is_not_flagged_low(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 40}},
                "claiming": {"ready_research_audit": 40, "actively_claimed": 3, "claimable": 37},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {"run_key": "2026-09-13T12:30:00+09:00", "counts": {"research_completed": 3}},
            ]})
            module = _load_module(repo)
            text = module.render_section(repo, now=datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc))
            self.assertIn("最新通常runのResearch完了 | **3**", text)
            self.assertIn(":00 補助worker | **Discovery優先**", text)
            self.assertIn("処理速度 | **OK**", text)
            self.assertNotIn("throughput LOW", text)

    def test_append_places_worker_status_before_24h_summary_and_replaces_previous_section(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 0}},
                "claiming": {"ready_research_audit": 0, "actively_claimed": 0, "claimable": 0},
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            module = _load_module(repo)
            status = repo / "STATUS.md"
            status.write_text(
                "# 運用ダッシュボード\n\n"
                "## 現在の状態\n\n"
                "| 次回保守までの通常run | **12 / 24** |\n\n"
                "state\n\n"
                "## 直近24時間の処理量\n\n"
                "| 探索専用worker run（毎時枠） | **2** |\n"
                "| 探索専用worker round（stats観測） | **7** |\n\n"
                "metrics\n\n"
                "## 参考情報\n\n"
                "### 直近の探索専用worker\n\n"
                "### 探索専用workerの探索効率（直近24時間）\n\n"
                "### 直近5探索専用worker run\n",
                encoding="utf-8",
            )
            now = datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc)
            module.append_section(repo, status, now=now)
            module.append_section(repo, status, now=now)
            text = status.read_text(encoding="utf-8")
            self.assertEqual(text.count("## ワーカー稼働状況"), 1)
            self.assertLess(text.index("## ワーカー稼働状況"), text.index("## 直近24時間の処理量"))
            self.assertLess(text.index("## 現在の状態"), text.index("## ワーカー稼働状況"))
            self.assertIn("保守カウンタ（通常run）", text)
            self.assertIn(":00 補助worker Discovery run（毎時枠）", text)
            self.assertIn(":00 補助worker Discovery round（stats観測）", text)
            self.assertIn("### 直近の:00 補助worker Discovery", text)
            self.assertIn("### :00 補助workerのDiscovery効率（直近24時間）", text)
            self.assertIn("### 直近5件の:00 補助worker Discovery run", text)
            self.assertNotIn("探索専用worker", text)


if __name__ == "__main__":
    unittest.main()
