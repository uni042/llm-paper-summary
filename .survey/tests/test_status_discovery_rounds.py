import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).parents[2]
RENDER_SCRIPT = ROOT / ".survey/scripts/render_status_dashboard.py"
EVIDENCE_SCRIPT = ROOT / ".survey/scripts/build_status_dashboard.py"


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def _load_renderer(repo: Path):
    scripts = repo / ".survey/scripts"
    scripts.mkdir(parents=True, exist_ok=True)
    (scripts / "build_status_dashboard.py").write_text(
        EVIDENCE_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8"
    )
    dst = scripts / "render_status_dashboard.py"
    dst.write_text(RENDER_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")
    spec = importlib.util.spec_from_file_location("render_status_dashboard_round_test", dst)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _write_round(
    repo: Path,
    *,
    filename: str,
    job_id: str,
    run_key: str,
    round_id: str,
    axis: str,
    canonical_id: str,
) -> str:
    path = f".survey/work-queue/submissions/{filename}"
    _write_json(
        repo / path,
        {
            "job_id": job_id,
            "candidates": [{"canonical_id": canonical_id}],
            "discovery_stats": {
                "run_key": run_key,
                "round": round_id,
                "axis": axis,
                "candidate_count": 1,
            },
        },
    )
    return path


class DiscoveryRoundStatusTests(unittest.TestCase):
    def test_latest_discovery_run_counts_distinct_durable_rounds_independently_of_results(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            job_id = "job-discovery-shared"
            run_key = "2026-09-15T20:00:00+09:00"
            _write_json(
                repo / f".survey/work-queue/jobs/{job_id}.json",
                {
                    "job_id": job_id,
                    "type": "discovery",
                    "status": "completed",
                    "completed_at": "2026-09-15T11:05:09+00:00",
                },
            )

            first = _write_round(
                repo,
                filename="20260915T2006JST-discovery-specialist-a-1.json",
                job_id=job_id,
                run_key=run_key,
                round_id="specialist-a-1",
                axis="axis-a",
                canonical_id="arXiv:2609.00001",
            )
            _write_round(
                repo,
                filename="20260915T2008JST-discovery-specialist-b-2.json",
                job_id=job_id,
                run_key=run_key,
                round_id="specialist-b-2",
                axis="axis-b",
                canonical_id="arXiv:2609.00002",
            )
            _write_round(
                repo,
                filename="20260915T2010JST-discovery-specialist-c-3.json",
                job_id=job_id,
                run_key=run_key,
                round_id="specialist-c-3",
                axis="axis-c",
                canonical_id="arXiv:2609.00003",
            )

            # The processor emits one job-level result for the shared discovery job.
            # That result proves processing success for the job, but it must not be
            # required to prove that each immutable round record exists.
            _write_json(
                repo / ".survey/work-queue/results/20260915T2006JST-discovery-specialist-a-1.json",
                {
                    "ok": True,
                    "job_id": job_id,
                    "job_type": "discovery",
                    "job_status": "completed",
                    "processed_at": "2026-09-15T11:05:09+00:00",
                    "submission": first,
                },
            )

            text = _load_renderer(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 11, 14, tzinfo=timezone.utc)
            )
            discovery = text.split("#### Discovery (:00)", 1)[1].split("### 現在処理中", 1)[0]

            self.assertIn("耐久探索round: **3件**", discovery)
            self.assertIn("個別result照合: **1件**", discovery)
            self.assertIn("specialist-a-1", discovery)
            self.assertIn("specialist-b-2", discovery)
            self.assertIn("specialist-c-3", discovery)
            self.assertIn("axis-a", discovery)
            self.assertIn("axis-b", discovery)
            self.assertIn("axis-c", discovery)
            self.assertNotIn("未完了または未検証", discovery)

    def test_round_count_deduplicates_same_run_key_and_round_identity(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            job_id = "job-discovery-duplicate"
            run_key = "2026-09-15T20:00:00+09:00"
            _write_json(
                repo / f".survey/work-queue/jobs/{job_id}.json",
                {"job_id": job_id, "type": "discovery", "status": "completed"},
            )
            for index in (1, 2):
                _write_round(
                    repo,
                    filename=f"20260915T200{index}JST-discovery-duplicate-{index}.json",
                    job_id=job_id,
                    run_key=run_key,
                    round_id="same-round-1",
                    axis="same-axis",
                    canonical_id=f"arXiv:2609.1000{index}",
                )

            text = _load_renderer(repo).build_dashboard(
                repo, now=datetime(2026, 9, 15, 11, 14, tzinfo=timezone.utc)
            )
            discovery = text.split("#### Discovery (:00)", 1)[1].split("### 現在処理中", 1)[0]
            self.assertIn("耐久探索round: **1件**", discovery)
            self.assertIn("round識別子重複submission: **1件**", discovery)


if __name__ == "__main__":
    unittest.main()
