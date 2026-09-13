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
            _write(repo / ".survey/work-queue/claims/job-r1.json", {
                "job_id": "job-r1",
                "claimed_at": "2026-09-13T03:00:00+00:00",
                "expires_at": "2026-09-13T05:00:00+00:00",
            })
            module = _load_module(repo)
            text = module.render_section(repo, now=datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc))
            self.assertIn("## Research throughput health", text)
            self.assertIn("Research ready | **180**", text)
            self.assertIn("Active claims | **23**", text)
            self.assertIn("Claimable | **157**", text)
            self.assertIn(":00補助worker mode | **NORMAL-WORKER ASSIST (RESEARCH/AUDIT)**", text)
            self.assertIn("ready > 50 → 通常worker補助", text)
            self.assertIn("Worker routing snapshot", text)
            self.assertIn("next-jobs.json", text)
            self.assertIn("transport batch上限", text)
            self.assertIn("24-run maintenance counter", text)
            self.assertIn("Latest research completed | **1**", text)
            self.assertIn("Oldest active claim age | **60 min**", text)
            self.assertIn("HIGH-BACKLOG RESEARCH-ONLY", text)
            self.assertIn("LOW", text)
            self.assertIn("最低3件", text)

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
            self.assertIn(":00補助worker mode | **DISCOVERY SPECIALIST**", text)
            self.assertIn("ready ≤ 50 → 探索専用", text)

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
            self.assertIn("Latest research completed | **3**", text)
            self.assertIn(":00補助worker mode | **DISCOVERY SPECIALIST**", text)
            self.assertNotIn("throughput LOW", text)

    def test_append_replaces_previous_section_instead_of_duplicating(self):
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
            status.write_text("# Status\n\n", encoding="utf-8")
            now = datetime(2026, 9, 13, 4, 0, tzinfo=timezone.utc)
            module.append_section(repo, status, now=now)
            module.append_section(repo, status, now=now)
            text = status.read_text(encoding="utf-8")
            self.assertEqual(text.count("## Research throughput health"), 1)
            self.assertEqual(text.count("### Worker routing snapshot"), 1)


if __name__ == "__main__":
    unittest.main()
