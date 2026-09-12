from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_status_dashboard  # noqa: E402


class StatusDashboardTest(unittest.TestCase):
    def _write_json(self, path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def test_build_dashboard_summarizes_latest_run_and_24h_funnel(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            survey = root / ".survey"
            self._write_json(
                survey / "work-queue/run-ledger.json",
                {
                    "schema_version": 2,
                    "history_limit": 192,
                    "updated_at": "2026-09-12T05:44:00+00:00",
                    "entries": [
                        {
                            "run_key": "2026-09-12T13:30:00+09:00",
                            "last_recorded_at": "2026-09-12T04:44:00+00:00",
                            "counts": {"research_completed": 2, "audit_completed": 1, "discovery_completed": 1, "blocked": 1, "new_jobs": 3, "new_papers": 2, "fallback_archived": 0},
                            "new_paper_ids": ["arXiv:1", "arXiv:2"],
                            "terminal_transitions": [
                                {"type": "research", "to": "completed", "canonical_id": "arXiv:1", "title": "Paper One"},
                                {"type": "research", "to": "completed", "canonical_id": "arXiv:2", "title": "Paper Two"},
                            ],
                        },
                        {
                            "run_key": "2026-09-12T14:30:00+09:00",
                            "last_recorded_at": "2026-09-12T05:44:00+00:00",
                            "counts": {"research_completed": 3, "audit_completed": 0, "discovery_completed": 1, "blocked": 0, "new_jobs": 4, "new_papers": 3, "fallback_archived": 0},
                            "new_paper_ids": ["arXiv:2", "arXiv:3", "arXiv:4"],
                            "terminal_transitions": [
                                {"type": "research", "to": "completed", "canonical_id": "arXiv:5", "title": "Paper Five"},
                                {"type": "research", "to": "completed", "canonical_id": "arXiv:6", "title": "Paper Six"},
                                {"type": "research", "to": "completed", "canonical_id": "arXiv:7", "title": "Paper Seven"},
                            ],
                        },
                        {
                            "run_key": "2026-09-10T12:30:00+09:00",
                            "last_recorded_at": "2026-09-10T03:40:00+00:00",
                            "counts": {"research_completed": 99, "audit_completed": 0, "discovery_completed": 0, "blocked": 0, "new_jobs": 0, "new_papers": 99, "fallback_archived": 0},
                            "new_paper_ids": ["arXiv:old"],
                            "terminal_transitions": [],
                        },
                    ],
                },
            )
            self._write_json(
                survey / "work-queue/discovery-state.json",
                {
                    "schema_version": 2,
                    "updated_at": "2026-09-12T05:45:00+00:00",
                    "history_limit": 256,
                    "history": [
                        {
                            "run_key": "2026-09-12T13:40:00+09:00",
                            "round": "normal-1",
                            "axis": "高重複軸",
                            "candidate_count": 5,
                            "duplicate_filtered_count": 4,
                            "novel_candidate_count": 1,
                            "accepted_count": 1,
                            "duplicate_ratio": 0.8,
                            "source_worker": "normal",
                        },
                        {
                            "run_key": "2026-09-12T14:45:00+09:00",
                            "round": "specialist-1",
                            "axis": "新着・隣接システム",
                            "candidate_count": 4,
                            "duplicate_filtered_count": 1,
                            "novel_candidate_count": 3,
                            "accepted_count": 3,
                            "duplicate_ratio": 0.25,
                            "source_worker": "specialist",
                        },
                        {
                            "run_key": "2026-09-10T10:00:00+09:00",
                            "round": "old",
                            "axis": "古い軸",
                            "candidate_count": 100,
                            "duplicate_filtered_count": 0,
                            "novel_candidate_count": 100,
                            "accepted_count": 100,
                            "duplicate_ratio": 0.0,
                            "source_worker": "specialist",
                        },
                    ],
                    "axes": {
                        "高重複軸": {"rounds": 4, "candidate_count": 20, "duplicate_filtered_count": 16, "accepted_count": 4, "duplicate_ratio": 0.8},
                        "新着・隣接システム": {"rounds": 5, "candidate_count": 25, "duplicate_filtered_count": 5, "accepted_count": 18, "duplicate_ratio": 0.2},
                    },
                },
            )
            self._write_json(
                survey / "work-queue/next-jobs.json",
                {
                    "counts": {"discovery": {"completed": 180}, "audit": {"completed": 6}, "research": {"completed": 143, "ready": 2, "deferred": 3, "blocked": 3, "superseded": 43}},
                    "generated_at": "2026-09-12T05:45:00+00:00",
                    "next_jobs": [
                        {"job_id": "r1", "type": "research", "priority": 86, "canonical_id": "arXiv:new1", "title": "Next One"},
                        {"job_id": "r2", "type": "research", "priority": 83, "canonical_id": "arXiv:new2", "title": "Next Two"},
                    ],
                },
            )
            self._write_json(survey / "work-queue/jobs/r1.json", {"job_id": "r1", "type": "research", "status": "ready", "repair_required": True, "title": "Next One", "canonical_id": "arXiv:new1"})
            self._write_json(survey / "work-queue/jobs/r2.json", {"job_id": "r2", "type": "research", "status": "ready", "title": "Next Two", "canonical_id": "arXiv:new2"})
            self._write_json(survey / "work-queue/jobs/b1.json", {"job_id": "b1", "type": "research", "status": "blocked", "title": "Blocked One"})
            self._write_json(survey / "work-queue/maintenance-cycle.json", {"cadence_runs": 24, "runs_since_maintenance": 7, "maintenance_pending": False})
            self._write_json(survey / "reports/consistency-latest.json", {"status": "passed", "generated_at": "2026-09-12T05:20:00+00:00"})
            self._write_json(survey / "work-queue/fallback-inbox/e1.json", {"schema_version": 1})

            first = build_status_dashboard.build_dashboard(root)
            second = build_status_dashboard.build_dashboard(root)

            self.assertEqual(first, second)
            self.assertIn("2026-09-12 14:45 JST", first)
            self.assertIn("candidate在庫 | **2 / 50**", first)
            self.assertIn("research完了 | **5**", first)
            self.assertIn("探索評価候補 | **9**", first)
            self.assertIn("重複除外 | **5**", first)
            self.assertIn("candidate採用 | **4**", first)
            self.assertIn("repo収録 | **4**", first)
            self.assertIn("直近の通常worker", first)
            self.assertIn("research完了 | 3", first)
            self.assertIn("直近の探索", first)
            self.assertIn("新着・隣接システム", first)
            self.assertIn("4候補 / 重複1 / 採用3", first)
            self.assertIn("repair待ち | **1**", first)
            self.assertIn("GitHub fallback inbox | **1**", first)
            self.assertIn("Library pending | **集計不能**", first)
            self.assertIn("履歴不足", first)
            self.assertIn("candidate在庫がcritical watermark未満", first)
            self.assertIn("高重複軸", first)


if __name__ == "__main__":
    unittest.main()
