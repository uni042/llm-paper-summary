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
                {"run_key": "2026-09-12T13:07:12+09:00", "round": "specialist-r1", "axis": "SSD階層", "candidate_count": 10, "duplicate_filtered_count": 4, "novel_candidate_count": 6, "accepted_count": 5},
                {"run_key": "2026-09-12T14:06:41+09:00", "round": "specialist-r2", "axis": "MoE expert", "candidate_count": 5, "duplicate_filtered_count": 1, "novel_candidate_count": 4, "accepted_count": 4},
            ]})
            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 12, 6, 10, tzinfo=timezone.utc))
            for expected in ("# 運用ダッシュボード", "Research ready | **2**", "Research完了 | **3**", "Repo収録 | **3**", "探索評価候補 | **15**", "重複除外 | **5**", "Research候補採用 | **9**", "33.3%", "SSD階層", "MoE expert", "New Paper", "Paper A", "履歴不足"):
                self.assertIn(expected, text)

    def test_dashboard_separates_specialist_discovery_and_groups_it_by_hourly_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _install_script(repo)
            _write(repo / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"completed": 206, "ready": 176, "blocked": 0, "deferred": 3}},
                "next_jobs": [],
            })
            _write(repo / ".survey/work-queue/maintenance-cycle.json", {
                "cadence_runs": 24, "runs_since_maintenance": 9,
                "maintenance_pending": False, "last_maintenance_status": "passed",
                "last_consistency_status": "passed",
            })
            # The ledger bucket is intentionally polluted by helper events from the
            # specialist worker. STATUS must not report those as normal-worker discovery.
            _write(repo / ".survey/work-queue/run-ledger.json", {"entries": [
                {
                    "run_key": "2026-09-13T10:30:00+09:00",
                    "counts": {
                        "research_completed": 2,
                        "audit_completed": 0,
                        "discovery_completed": 4,
                        "blocked": 0,
                        "new_jobs": 7,
                        "new_papers": 2,
                        "fallback_archived": 0,
                    },
                    "terminal_transitions": [
                        {"type": "research", "canonical_id": "arXiv:a", "title": "A", "to": "completed"},
                        {"type": "research", "canonical_id": "arXiv:b", "title": "B", "to": "completed"},
                    ],
                    "new_jobs": [],
                    "new_paper_ids": ["arXiv:a", "arXiv:b"],
                },
            ]})
            _write(repo / ".survey/work-queue/discovery-state.json", {"history": [
                {"run_key": "2026-09-13T09:28:10+09:00", "round": "specialist-s1", "source_submission": "work-queue/submissions/discovery-specialist-s1.json", "axis": "SSD", "candidate_count": 4, "duplicate_filtered_count": 1, "novel_candidate_count": 3, "accepted_count": 2},
                {"run_key": "2026-09-13T09:28:10+09:00", "round": "specialist-s2", "source_submission": "work-queue/submissions/discovery-specialist-s2.json", "axis": "MoE", "candidate_count": 5, "duplicate_filtered_count": 2, "novel_candidate_count": 3, "accepted_count": 3},
                {"run_key": "2026-09-13T09:57:59+09:00", "round": "specialist-s2b", "source_submission": "work-queue/submissions/discovery-specialist-s2b.json", "axis": "Runtime", "candidate_count": 3, "duplicate_filtered_count": 1, "novel_candidate_count": 2, "accepted_count": 1},
                {"run_key": "2026-09-13T10:16:01+09:00", "round": "specialist-s3", "source_submission": "work-queue/submissions/discovery-specialist-s3.json", "axis": "Scheduling", "candidate_count": 6, "duplicate_filtered_count": 4, "novel_candidate_count": 2, "accepted_count": 2},
                {"run_key": "2026-09-13T10:16:01+09:00", "round": "specialist-s4", "source_submission": "work-queue/submissions/discovery-specialist-s4.json", "axis": "SpecDecode", "candidate_count": 5, "duplicate_filtered_count": 1, "novel_candidate_count": 4, "accepted_count": 3},
                {"run_key": "2026-09-13T10:16:01+09:00", "round": "specialist-s5", "source_submission": "work-queue/submissions/discovery-specialist-s5.json", "axis": "Hierarchical memory", "candidate_count": 7, "duplicate_filtered_count": 2, "novel_candidate_count": 5, "accepted_count": 4},
                {"run_key": "2026-09-13T10:16:01+09:00", "round": "specialist-s6", "source_submission": "work-queue/submissions/discovery-specialist-s6.json", "axis": "Network", "candidate_count": 4, "duplicate_filtered_count": 1, "novel_candidate_count": 3, "accepted_count": 2},
            ]})
            module = _load_module(repo)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 13, 1, 50, tzinfo=timezone.utc))

            self.assertIn("Candidate在庫（Research ready） | **176**", text)
            self.assertNotIn("176 / 50", text)
            self.assertIn("## 直近の通常worker", text)
            self.assertIn("Research完了 | **2**", text)
            self.assertIn("通常worker Discovery round | **0**", text)
            self.assertNotIn("Discovery完了 | **4**", text)
            self.assertNotIn("新規job | **7**", text)

            self.assertIn("## 直近の探索専用worker", text)
            self.assertIn("Run: **2026-09-13T10:00:00+09:00**", text)
            self.assertIn("探索round | **4**", text)
            self.assertIn("評価候補 | **22**", text)
            self.assertIn("重複除外 | **8**", text)
            self.assertIn("Novel候補 | **14**", text)
            self.assertIn("Research候補採用 | **11**", text)
            self.assertIn("探索専用worker run（stats観測） | **2**", text)
            self.assertIn("探索専用worker round（stats観測） | **7**", text)
            self.assertIn("### 直近5探索専用worker run", text)
            self.assertIn("2026-09-13T10:00:00+09:00 — 4 round", text)
            self.assertIn("2026-09-13T09:00:00+09:00 — 3 round", text)
            self.assertNotIn("2026-09-13T09:57:59+09:00 — 1 round", text)

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
