import importlib.util
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path


def _load():
    path = Path(__file__).parents[1] / "scripts" / "maintenance_health.py"
    spec = importlib.util.spec_from_file_location("maintenance_health", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class MaintenanceHealthTests(unittest.TestCase):
    def test_queue_snapshot_is_repaired_after_job_gc(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs = root / ".survey/work-queue/jobs"
            _write(jobs / "job-r1.json", {
                "job_id": "job-r1", "type": "research", "status": "ready",
                "priority": 80, "canonical_id": "arXiv:2601.00001", "created_at": "2026-09-12T00:00:00+00:00",
            })
            _write(root / ".survey/work-queue/next-jobs.json", {
                "counts": {"research": {"ready": 1, "completed": 99}},
                "next_jobs": [],
                "generated_at": "2026-09-01T00:00:00+00:00",
            })

            module = _load()
            result = module.audit_queue(root, repair_snapshot=True)
            snapshot = json.loads((root / ".survey/work-queue/next-jobs.json").read_text(encoding="utf-8"))

            self.assertTrue(result["snapshot_repaired"])
            self.assertEqual(snapshot["counts"], {"research": {"ready": 1}})
            self.assertEqual(snapshot["next_jobs"][0]["job_id"], "job-r1")

    def test_duplicate_ready_research_canonical_is_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            jobs = root / ".survey/work-queue/jobs"
            for suffix in ("a", "b"):
                _write(jobs / f"job-{suffix}.json", {
                    "job_id": f"job-{suffix}", "type": "research", "status": "ready",
                    "priority": 50, "canonical_id": "arXiv:2601.12345",
                    "created_at": f"2026-09-12T00:00:0{1 if suffix == 'a' else 2}+00:00",
                })
            _write(root / ".survey/work-queue/next-jobs.json", {"counts": {}, "next_jobs": []})

            module = _load()
            result = module.audit_queue(root, repair_snapshot=False)
            codes = {(x["severity"], x["code"]) for x in result["findings"]}
            self.assertIn(("error", "duplicate_active_candidate"), codes)

    def test_quality_regression_reports_only_new_failures(self):
        module = _load()
        current = {
            "paper": {"results": [
                {"path": "papers/a.md", "status": "FAIL"},
                {"path": "papers/b.md", "status": "FAIL"},
                {"path": "papers/c.md", "status": "PASS"},
            ]},
            "list_summary": {"results": []},
            "overview": {"results": []},
        }
        previous = {"quality": {"failures": {
            "paper": ["papers/a.md"], "list_summary": [], "overview": []
        }}}
        result = module.compare_quality_failures(current, previous)
        self.assertEqual(result["new_failures"]["paper"], ["papers/b.md"])
        self.assertEqual(result["resolved_failures"]["paper"], [])

    def test_freshness_detects_stale_and_incomplete_reports(self):
        module = _load()
        latest = datetime(2026, 9, 12, 12, 0, tzinfo=timezone.utc)
        report = {
            "checked_at": "2026-09-12T10:00:00+00:00",
            "summary": {"total": 10, "complete": 9, "incomplete": 1},
        }
        result = module.evaluate_coverage_report("citation", report, latest, current_paper_count=10)
        codes = {x["code"] for x in result["findings"]}
        self.assertIn("citation_coverage_incomplete", codes)
        self.assertIn("citation_report_stale", codes)


if __name__ == "__main__":
    unittest.main()
