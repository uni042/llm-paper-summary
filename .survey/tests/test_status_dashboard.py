import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


def _load_module(repo_root: Path):
    path = repo_root / ".survey" / "scripts" / "build_status_dashboard.py"
    spec = importlib.util.spec_from_file_location("build_status_dashboard", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_dashboard_aggregates_24h_and_current_state(tmp_path):
    repo = tmp_path
    # Copy the implementation under test into a realistic repo layout.
    src = Path(__file__).parents[1] / "scripts" / "build_status_dashboard.py"
    dst = repo / ".survey" / "scripts" / "build_status_dashboard.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    _write(repo / ".survey/work-queue/next-jobs.json", {
        "counts": {
            "discovery": {"completed": 180},
            "audit": {"completed": 6},
            "research": {"completed": 144, "ready": 2, "blocked": 3, "deferred": 1, "superseded": 43},
        },
        "next_jobs": [
            {"type": "research", "canonical_id": "arXiv:2609.1", "title": "Paper A", "priority": 90},
            {"type": "research", "canonical_id": "arXiv:2609.2", "title": "Paper B", "priority": 80},
        ],
    })
    _write(repo / ".survey/work-queue/maintenance-cycle.json", {
        "cadence_runs": 24,
        "runs_since_maintenance": 14,
        "maintenance_pending": False,
        "last_maintenance_status": "passed",
        "last_consistency_status": "passed",
    })
    _write(repo / ".survey/work-queue/run-ledger.json", {
        "history_limit": 48,
        "entries": [
            {
                "run_key": "2026-09-11T15:30:00+09:00",
                "counts": {"research_completed": 2, "audit_completed": 1, "discovery_completed": 1, "blocked": 0, "new_jobs": 3, "new_papers": 2, "fallback_archived": 0},
                "terminal_transitions": [
                    {"type": "research", "canonical_id": "arxiv:old", "title": "Old Paper", "to": "completed"}
                ],
                "new_jobs": [],
                "new_paper_ids": ["arxiv:old1", "arxiv:old2"],
            },
            {
                "run_key": "2026-09-12T14:30:00+09:00",
                "counts": {"research_completed": 3, "audit_completed": 0, "discovery_completed": 1, "blocked": 1, "new_jobs": 2, "new_papers": 3, "fallback_archived": 1},
                "terminal_transitions": [
                    {"type": "research", "canonical_id": "arxiv:new", "title": "New Paper", "to": "completed"}
                ],
                "new_jobs": [
                    {"type": "research", "canonical_id": "arxiv:c1", "title": "Candidate 1", "status": "ready"},
                    {"type": "research", "canonical_id": "arxiv:c2", "title": "Candidate 2", "status": "ready"},
                ],
                "new_paper_ids": ["arxiv:n1", "arxiv:n2", "arxiv:n3"],
            },
        ],
    })
    _write(repo / ".survey/work-queue/discovery-state.json", {
        "history_limit": 24,
        "history": [
            {
                "run_key": "2026-09-12T13:00:00+09:00",
                "round": "r1",
                "axis": "SSD階層",
                "candidate_count": 10,
                "duplicate_filtered_count": 4,
                "novel_candidate_count": 6,
                "accepted_count": 5,
                "duplicate_ratio": 0.4,
                "accepted_canonical_ids": ["a", "b", "c", "d", "e"],
            },
            {
                "run_key": "2026-09-12T14:00:00+09:00",
                "round": "r2",
                "axis": "MoE expert",
                "candidate_count": 5,
                "duplicate_filtered_count": 1,
                "novel_candidate_count": 4,
                "accepted_count": 4,
                "duplicate_ratio": 0.2,
                "accepted_canonical_ids": ["f", "g", "h", "i"],
            },
        ],
    })

    module = _load_module(repo)
    now = datetime(2026, 9, 12, 6, 10, tzinfo=timezone.utc)  # 15:10 JST
    text = module.build_dashboard(repo, now=now)

    assert "# 運用ダッシュボード" in text
    assert "Research ready | **2**" in text
    assert "Research完了 | **3**" in text
    assert "Repo収録 | **3**" in text
    assert "探索評価候補 | **15**" in text
    assert "重複除外 | **5**" in text
    assert "Research候補採用 | **9**" in text
    assert "33.3%" in text
    assert "SSD階層" in text and "MoE expert" in text
    assert "New Paper" in text
    assert "Paper A" in text
    assert "履歴不足" in text


def test_dashboard_warns_when_candidate_stock_is_low(tmp_path):
    repo = tmp_path
    src = Path(__file__).parents[1] / "scripts" / "build_status_dashboard.py"
    dst = repo / ".survey" / "scripts" / "build_status_dashboard.py"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    _write(repo / ".survey/work-queue/next-jobs.json", {
        "counts": {"research": {"completed": 0, "ready": 1, "blocked": 0, "deferred": 0}},
        "next_jobs": [],
    })
    _write(repo / ".survey/work-queue/maintenance-cycle.json", {"maintenance_pending": False})
    _write(repo / ".survey/work-queue/run-ledger.json", {"entries": []})
    _write(repo / ".survey/work-queue/discovery-state.json", {"history": []})

    module = _load_module(repo)
    text = module.build_dashboard(repo, now=datetime(2026, 9, 12, 6, 10, tzinfo=timezone.utc))
    assert "CRITICAL" in text
    assert "candidate在庫が15未満" in text
