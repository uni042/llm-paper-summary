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


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _install_script(repo: Path):
    dst = repo / ".survey" / "scripts" / "build_status_dashboard.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")


class StatusDashboardTests(unittest.TestCase):
    def test_dashboard_aggregates_24h_and_current_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"completed": 144, "ready": 2, "blocked": 3, "deferred": 1}},
                "next_jobs": [
                    {"type": "research", "canonical_id": "arXiv:2609.1", "title": "Paper A", "priority": 90},
                    {"type": "research", "canonical_id": "arXiv:2609.2", "title": "Paper B", "priority": 80},
                ],
            })
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "cadence_runs": 24, "runs_since_maintenance": 14,
                "maintenance_pending": False, "last_maintenance_status": "passed",
                "last_consistency_status": "passed",
            })
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {"run_key": "2026-09-11T14:30:00+09:00", "counts": {"research_completed": 2, "audit_completed": 1, "discovery_completed": 1, "blocked": 0, "new_jobs": 3, "new_papers": 2, "fallback_archived": 0}, "terminal_transitions": [], "new_jobs": [], "new_paper_ids": ["old1", "old2"]},
                {"run_key": "2026-09-12T14:30:00+09:00", "counts": {"research_completed": 3, "audit_completed": 0, "discovery_completed": 1, "blocked": 1, "new_jobs": 2, "new_papers": 3, "fallback_archived": 1}, "terminal_transitions": [{"type": "research", "canonical_id": "arxiv:new", "title": "New Paper", "to": "completed"}], "new_jobs": [{"type": "research", "canonical_id": "arxiv:c1", "title": "Candidate 1", "status": "ready"}, {"type": "research", "canonical_id": "arxiv:c2", "title": "Candidate 2", "status": "ready"}], "new_paper_ids": ["n1", "n2", "n3"]},
            ]})
            _write(repo / ".survey/work-queue/discovery-state.json", {"history": [
                {"run_key": "2026-09-12T13:00:00+09:00", "round": "r1", "axis": "SSD階層", "candidate_count": 10, "duplicate_filtered_count": 4, "novel_candidate_count": 6, "accepted_count": 5},
                {"run_key": "2026-09-12T14:00:00+09:00", "round": "r2", "axis": "MoE expert", "candidate_count": 5, "duplicate_filtered_count": 1, "novel_candidate_count": 4, "accepted_count": 4},
            ]})
            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 12, 6, 10, tzinfo=timezone.utc))
            for expected in ("# 運用ダッシュボード", "Research ready | **2**", "Research完了 | **3**", "Repo収録 | **3**", "探索評価候補 | **15**", "重複除外 | **5**", "Research候補採用 | **9**", "33.3%", "SSD階層", "MoE expert", "New Paper", "Paper A", "履歴不足"):
                self.assertIn(expected, text)

    def test_dashboard_warns_when_candidate_stock_is_low(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {"counts": {"research": {"completed": 0, "ready": 1, "blocked": 0, "deferred": 0}}, "next_jobs": []})
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {"maintenance_pending": False})
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
            _write(repo / ".survey/work-queue/discovery-state.json", {"history": []})
            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 12, 6, 10, tzinfo=timezone.utc))
            self.assertIn("CRITICAL", text)
            self.assertIn("candidate在庫が15未満", text)


if __name__ == "__main__":
    unittest.main()
