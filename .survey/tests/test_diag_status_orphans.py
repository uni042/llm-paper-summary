import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DiagnoseStatusOrphans(unittest.TestCase):
    def test_print_current_orphans(self):
        evidence = _load("diag_evidence", SCRIPTS / "build_status_dashboard.py")
        renderer = _load("diag_renderer", SCRIPTS / "render_status_dashboard.py")
        submissions = evidence._collect_submissions(ROOT)
        results = evidence._collect_results(ROOT)
        jobs = evidence._collect_jobs(ROOT)
        terminal = renderer._terminally_rejected_submission_paths(ROOT, submissions, results)
        orphans = sorted(
            str(row["path"].relative_to(ROOT))
            for row in submissions
            if (not row["job_id"] or row["job_id"] not in jobs)
            and row["path"] not in terminal
            and not (
                row["kind"] == "discovery"
                and renderer._discovery_round_identity(row) is not None
            )
        )
        self.fail("STATUS_ORPHANS=" + "|".join(orphans))


if __name__ == "__main__":
    unittest.main()
