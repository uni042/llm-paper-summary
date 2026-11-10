from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import refresh_due  # noqa: E402


class RefreshDueTest(unittest.TestCase):
    def test_missing_state_is_due(self):
        with tempfile.TemporaryDirectory() as td:
            self.assertTrue(
                refresh_due.is_due(Path(td) / "missing.json", max_age_seconds=3000)
            )

    def test_fresh_and_stale_state(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "state.json"
            now = dt.datetime(2026, 10, 3, 16, 0, tzinfo=dt.timezone.utc)
            path.write_text(
                json.dumps({"updated_at": "2026-10-03T15:30:01+00:00"}),
                encoding="utf-8",
            )
            self.assertFalse(
                refresh_due.is_due(path, max_age_seconds=3000, now=now)
            )
            path.write_text(
                json.dumps({"updated_at": "2026-10-03T14:00:00+00:00"}),
                encoding="utf-8",
            )
            self.assertTrue(
                refresh_due.is_due(path, max_age_seconds=3000, now=now)
            )


if __name__ == "__main__":
    unittest.main()
