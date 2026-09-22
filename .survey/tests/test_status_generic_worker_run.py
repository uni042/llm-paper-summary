import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_status_dashboard.py"


def _write_json(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


class GenericSurveyWorkerRunTests(unittest.TestCase):
    def test_generic_worker_uses_matching_claim_as_run_evidence(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            scripts = repo / ".survey/scripts"
            scripts.mkdir(parents=True)
            for name in ("build_status_dashboard.py", "render_status_dashboard_core.py", "render_status_dashboard.py"):
                source = SCRIPT.parent / name
                (scripts / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            job_id = "job-research-generic"
            attempt_id = "attempt-generic"
            claim_id = "claim-generic"
            paper = "papers/inference/generic.md"
            submission = f".survey/work-queue/submissions/research/{attempt_id}.json"
            result = f".survey/work-queue/results/research/{attempt_id}.json"
            _write_json(repo / f".survey/work-queue/jobs/{job_id}.json", {
                "job_id": job_id, "type": "research", "status": "completed",
                "canonical_id": "arXiv:2609.99999", "title": "Generic Worker Paper",
                "paper_path": paper, "completed_at": "2026-09-17T06:44:33+00:00",
            })
            _write_json(repo / submission, {
                "kind": "research", "attempt_id": attempt_id, "job_id": job_id,
                "claim_id": claim_id, "worker_id": "scheduled-chat-llm-survey",
                "paper_path": paper,
            })
            _write_json(repo / f".survey/work-queue/claims/{job_id}.json", {
                "claim_id": claim_id, "attempt_id": attempt_id, "job_id": job_id,
                "worker_id": "scheduled-chat-llm-survey",
                "claimed_at": "2026-09-17T06:43:27+00:00",
                "expires_at": "2026-09-17T08:13:27+00:00",
            })
            _write_json(repo / result, {
                "ok": True, "attempt_id": attempt_id, "job_id": job_id,
                "job_type": "research", "job_status": "completed",
                "artifact": {"paper": paper}, "submission": submission,
                "processed_at": "2026-09-17T06:44:33+00:00",
            })
            path = repo / paper
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# paper", encoding="utf-8")

            spec = importlib.util.spec_from_file_location("status_generic_worker", scripts / "render_status_dashboard.py")
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 17, 6, 45, tzinfo=timezone.utc))

            self.assertIn("2026-09-17 15:30 JST", text)
            self.assertIn("scheduled-chat-llm-survey", text)
            self.assertIn("Generic Worker Paper", text)

    def test_current_fixed_worker_groups_multiple_claims_into_one_scheduled_run(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            scripts = repo / ".survey/scripts"
            scripts.mkdir(parents=True)
            for name in ("build_status_dashboard.py", "render_status_dashboard_core.py", "render_status_dashboard.py"):
                source = SCRIPT.parent / name
                (scripts / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            for index, minute in enumerate((5, 40), start=1):
                job_id = f"job-current-{index}"
                attempt_id = f"attempt-current-{index}"
                claim_id = f"claim-current-{index}"
                paper = f"papers/inference/current-{index}.md"
                submission = f".survey/work-queue/submissions/research/{attempt_id}.json"
                result = f".survey/work-queue/results/research/{attempt_id}.json"
                completed = f"2026-09-17T06:{minute:02d}:30+00:00"
                _write_json(repo / f".survey/work-queue/jobs/{job_id}.json", {
                    "job_id": job_id, "type": "research", "status": "completed",
                    "canonical_id": f"arXiv:2609.9900{index}", "title": f"Current Paper {index}",
                    "paper_path": paper, "completed_at": completed,
                })
                _write_json(repo / submission, {
                    "kind": "research", "attempt_id": attempt_id, "job_id": job_id,
                    "claim_id": claim_id, "worker_id": "scheduled-chat-00",
                    "paper_path": paper,
                })
                _write_json(repo / f".survey/work-queue/claims/{job_id}.json", {
                    "claim_id": claim_id, "attempt_id": attempt_id, "job_id": job_id,
                    "worker_id": "scheduled-chat-00",
                    "claimed_at": f"2026-09-17T06:{minute:02d}:00+00:00",
                    "expires_at": "2026-09-17T08:00:00+00:00",
                })
                _write_json(repo / result, {
                    "ok": True, "attempt_id": attempt_id, "job_id": job_id,
                    "job_type": "research", "job_status": "completed",
                    "artifact": {"paper": paper}, "submission": submission,
                    "processed_at": completed,
                })
                path = repo / paper
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# paper", encoding="utf-8")

            spec = importlib.util.spec_from_file_location("status_current_worker", scripts / "render_status_dashboard.py")
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 17, 6, 45, tzinfo=timezone.utc))

            self.assertIn("最新観測run: **2026-09-17 15:00 JST** / worker `scheduled-chat-00`", text)
            self.assertIn("immutable submission: **2件** / 検証済み成功: **2件**", text)

    def test_current_discovery_run_key_timestamp_is_recognized(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            scripts = repo / ".survey/scripts"
            scripts.mkdir(parents=True)
            for name in ("build_status_dashboard.py", "render_status_dashboard_core.py", "render_status_dashboard.py"):
                source = SCRIPT.parent / name
                (scripts / name).write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

            _write_json(repo / ".survey/work-queue/submissions/discovery/round-current.json", {
                "kind": "discovery",
                "operation": "submit_discovery_round",
                "candidates": [],
                "discovery_stats": {
                    "run_key": "scheduled-chat-00-20260917T060100Z",
                    "round": "round-current",
                    "axis": "current discovery",
                    "candidate_count": 0,
                },
            })

            spec = importlib.util.spec_from_file_location("status_current_discovery", scripts / "render_status_dashboard.py")
            module = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(module)
            text = module.build_dashboard(repo, now=datetime(2026, 9, 17, 6, 45, tzinfo=timezone.utc))

            self.assertIn("最新観測run: **2026-09-17 15:01 JST**", text)
            self.assertIn("耐久探索round: **1件**", text)


if __name__ == "__main__":
    unittest.main()
