import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_status_dashboard.py"


def _write_job(repo: Path, job_id: str, *, kind: str = "research", status: str = "ready", canonical_id: str = "") -> None:
    path = repo / ".survey/work-queue/jobs" / f"{job_id}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "job_id": job_id,
        "type": kind,
        "status": status,
        "title": job_id,
    }
    if canonical_id:
        payload["canonical_id"] = canonical_id
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _load_renderer():
    spec = importlib.util.spec_from_file_location("render_status_dashboard_candidate_backlog", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DurableCandidateBacklogTests(unittest.TestCase):
    def test_top_summary_counts_only_durable_nonterminal_research_jobs(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)

            _write_job(repo, "job-a", canonical_id="arXiv:2609.00001")
            _write_job(repo, "job-a-duplicate", canonical_id="arXiv:2609.00001")
            _write_job(repo, "job-b", status="claimed", canonical_id="arXiv:2609.00002")
            _write_job(repo, "job-unknown", canonical_id="")
            _write_job(repo, "job-completed", status="completed", canonical_id="arXiv:2609.00003")
            _write_job(repo, "job-blocked", status="blocked", canonical_id="arXiv:2609.00004")
            _write_job(repo, "job-audit", kind="audit", canonical_id="arXiv:2609.00005")

            aggregate = repo / ".survey/work-queue/discovery-state.json"
            aggregate.parent.mkdir(parents=True, exist_ok=True)
            aggregate.write_text(json.dumps({"candidate_count": 999}), encoding="utf-8")

            text = _load_renderer().build_dashboard(
                repo, now=datetime(2026, 9, 16, 0, 0, tzinfo=timezone.utc)
            )

            top, _ = text.split("## 件数サマリー", 1)
            self.assertIn("## 現在の収録候補", top)
            self.assertIn("| canonical_id確認済みの一意な候補論文 | **2** |", top)
            self.assertIn("| canonical_idなしの候補Research job | **1** |", top)
            self.assertIn("| 非終端Research job合計 | **4** |", top)
            self.assertNotIn("999", top)
            self.assertLess(text.index("## 現在の収録候補"), text.index("## 件数サマリー"))


if __name__ == "__main__":
    unittest.main()
