import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".survey" / "scripts" / "build_status_dashboard.py"
RENDER = ROOT / ".survey" / "scripts" / "render_status_dashboard.py"

spec = importlib.util.spec_from_file_location("build_status_dashboard", SCRIPT)
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)

spec2 = importlib.util.spec_from_file_location("render_status_dashboard", RENDER)
render = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(render)


class StatusOrphanDiagnostic(unittest.TestCase):
    def test_report_exact_orphan_submission_paths(self):
        jobs = evidence._collect_jobs(ROOT)
        submissions = evidence._collect_submissions(ROOT)
        orphan = [
            row for row in submissions
            if (not row["job_id"] or row["job_id"] not in jobs)
            and not (
                row["kind"] == "discovery"
                and render._discovery_round_identity(row) is not None
            )
        ]
        details = [
            {
                "path": str(row["path"].relative_to(ROOT)),
                "job_id": row["job_id"],
                "kind": row["kind"],
                "payload": row["payload"],
            }
            for row in orphan
        ]
        self.fail(f"ORPHAN_SUBMISSIONS={details!r}")


if __name__ == "__main__":
    unittest.main()
