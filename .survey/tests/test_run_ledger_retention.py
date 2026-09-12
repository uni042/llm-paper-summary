from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import record_run_ledger  # noqa: E402


class RunLedgerRetentionTest(unittest.TestCase):
    def test_existing_short_history_limit_is_raised_for_seven_day_dashboard(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            survey = root / ".survey"
            jobs = survey / "work-queue/jobs"
            jobs.mkdir(parents=True)
            (survey / "work-queue/maintenance-cycle.json").write_text(
                json.dumps({"last_counted_run_key": "2026-09-12T14:30:00+09:00"}),
                encoding="utf-8",
            )
            (survey / "work-queue/run-ledger.json").write_text(
                json.dumps({"schema_version": 2, "history_limit": 48, "updated_at": None, "entries": []}),
                encoding="utf-8",
            )
            (jobs / "job-one.json").write_text(
                json.dumps({"job_id": "job-one", "type": "research", "status": "completed", "canonical_id": "arXiv:1", "title": "One"}),
                encoding="utf-8",
            )
            baseline = Path(td) / "baseline.json"
            baseline.write_text(
                json.dumps({
                    "captured_at": "2026-09-12T05:29:00+00:00",
                    "jobs": {},
                    "paper_ids": [],
                    "active_count": 0,
                    "result_files": [],
                    "fallback_archive_files": [],
                    "source_run_key": "2026-09-12T14:30:00+09:00",
                }),
                encoding="utf-8",
            )

            rc = record_run_ledger.record(root, baseline)
            self.assertEqual(rc, 0)
            ledger = json.loads((survey / "work-queue/run-ledger.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(ledger["history_limit"], 192)


if __name__ == "__main__":
    unittest.main()
