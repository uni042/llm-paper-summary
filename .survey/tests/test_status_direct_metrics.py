import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_status_dashboard.py"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _write_text(path: Path, text: str = "# paper") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _load_renderer():
    spec = importlib.util.spec_from_file_location("render_status_dashboard_direct_metrics", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_research_success(repo: Path) -> None:
    paper = "papers/inference/01-offload/verified.md"
    submission = ".survey/work-queue/submissions/research/attempt-ok.json"
    result = ".survey/work-queue/results/research/attempt-ok.json"
    completed = "2026-09-15T23:30:00+00:00"
    _write_json(repo / ".survey/work-queue/jobs/job-ok.json", {
        "job_id": "job-ok", "type": "research", "status": "completed",
        "canonical_id": "arXiv:2609.99991", "title": "Verified",
        "url": "https://arxiv.org/abs/2609.99991", "completed_at": completed,
        "paper_path": paper,
    })
    _write_json(repo / submission, {
        "kind": "research", "attempt_id": "attempt-ok", "job_id": "job-ok",
        "worker_id": "scheduled-chat-paper-20260916T0830JST", "paper_path": paper,
    })
    _write_json(repo / result, {
        "ok": True, "attempt_id": "attempt-ok", "job_id": "job-ok",
        "job_type": "research", "job_status": "completed",
        "submission": submission, "artifact": {"paper": paper},
        "processed_at": completed,
    })
    _write_text(repo / paper)


# Keep the compact top summary and the longer lower-page diagnostics tied to the same durable fixture.
class DirectStatusMetricTests(unittest.TestCase):
    def test_adds_compact_top_metrics_and_detailed_direct_evidence_metrics(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            now = datetime(2026, 9, 16, 0, 0, tzinfo=timezone.utc)
            _write_research_success(repo)

            # Four nonterminal Research jobs: two share one canonical_id, one is claimed,
            # and one lacks canonical/title/source URL entirely.
            _write_json(repo / ".survey/work-queue/jobs/job-a.json", {
                "job_id": "job-a", "type": "research", "status": "ready",
                "canonical_id": "arXiv:2609.10001", "title": "Candidate A",
                "url": "https://arxiv.org/abs/2609.10001",
            })
            _write_json(repo / ".survey/work-queue/jobs/job-a-dup.json", {
                "job_id": "job-a-dup", "type": "research", "status": "ready",
                "canonical_id": "ARXIV:2609.10001", "title": "Candidate A duplicate",
            })
            _write_json(repo / ".survey/work-queue/jobs/job-b.json", {
                "job_id": "job-b", "type": "research", "status": "claimed",
                "canonical_id": "arXiv:2609.10002", "title": "Candidate B",
                "source_url": "https://example.test/paper-b",
            })
            _write_json(repo / ".survey/work-queue/jobs/job-missing.json", {
                "job_id": "job-missing", "type": "research", "status": "ready",
            })
            _write_json(repo / ".survey/work-queue/claims/job-b.json", {
                "job_id": "job-b", "worker_id": "worker-live",
                "claimed_at": "2026-09-15T23:50:00+00:00",
                "heartbeat_at": "2026-09-15T23:58:00+00:00",
                "expires_at": "2026-09-16T01:00:00+00:00",
            })

            # One completed Research job is inconsistent: immutable submission exists,
            # but there is no success result and the referenced paper does not exist.
            _write_json(repo / ".survey/work-queue/jobs/job-broken.json", {
                "job_id": "job-broken", "type": "research", "status": "completed",
                "canonical_id": "arXiv:2609.10003", "title": "Broken",
                "completed_at": "2026-09-15T23:20:00+00:00",
                "paper_path": "papers/inference/01-offload/missing.md",
            })
            _write_json(repo / ".survey/work-queue/submissions/research/attempt-broken.json", {
                "kind": "research", "attempt_id": "attempt-broken", "job_id": "job-broken",
                "worker_id": "scheduled-chat-paper-20260916T0830JST",
                "paper_path": "papers/inference/01-offload/missing.md",
            })

            # Orphan durable records are direct consistency anomalies.
            _write_json(repo / ".survey/work-queue/submissions/research/orphan-submission.json", {
                "kind": "research", "attempt_id": "orphan-sub", "job_id": "missing-job-sub",
            })
            _write_json(repo / ".survey/work-queue/results/research/orphan-result.json", {
                "ok": True, "attempt_id": "orphan-result", "job_id": "missing-job-result",
                "job_type": "research", "job_status": "completed",
                "processed_at": "2026-09-15T23:40:00+00:00",
            })

            # A second real paper file proves the physical paper-file count is independent
            # from verified completion count. README/comparison files must not be counted.
            _write_text(repo / "papers/training/02-systems/physical-only.md")
            _write_text(repo / "papers/inference/README.md")
            _write_text(repo / "papers/training/comparison.md")

            text = _load_renderer().build_dashboard(repo, now=now)

            top, rest = text.split("## 件数サマリー", 1)
            self.assertIn("## 重要指標", top)
            self.assertIn("| 収録候補論文 | **2** |", top)
            self.assertIn("| 未claim Research job | **3** |", top)
            self.assertIn("| 直近24hの検証済みResearch収録 | **1** |", top)
            self.assertIn("| 最終検証済みResearch収録 | **09-16 08:30:00 JST（30分前）** |", top)
            self.assertIn("| 整合性異常 | **4** |", top)

            self.assertIn("## 耐久証拠の詳細集計", rest)
            details = rest.split("## 耐久証拠の詳細集計", 1)[1]
            self.assertIn("| ready | **3** |", details)
            self.assertIn("| claimed | **1** |", details)
            self.assertIn("| 重複canonical_idグループ | **1** |", details)
            self.assertIn("| 重複分のResearch job | **1** |", details)
            self.assertIn("| canonical_id欠損 | **1** |", details)
            self.assertIn("| title欠損 | **1** |", details)
            self.assertIn("| source URL欠損 | **2** |", details)
            self.assertIn("| inference/training配下の論文Markdown実体 | **2** |", details)
            self.assertIn("| 成功result未照合のimmutable submission | **2** |", details)
            self.assertIn("| completed Research/Audit jobで検証済み完了なし | **1** |", details)
            self.assertIn("| 対応jobなしsubmission | **1** |", details)
            self.assertIn("| 対応jobなし成功result | **1** |", details)
            self.assertIn("| 対応submissionなし成功result | **1** |", details)

            # Detailed/long tables stay below the existing evidence section.
            self.assertGreater(text.index("## 耐久証拠の詳細集計"), text.index("## 詳細証拠"))


if __name__ == "__main__":
    unittest.main()
