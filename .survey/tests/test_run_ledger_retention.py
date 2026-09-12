from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import ensure_status_history  # noqa: E402


class StatusHistoryRetentionTest(unittest.TestCase):
    def test_existing_short_limits_are_raised_for_dashboard_history(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            work_queue = root / ".survey/work-queue"
            work_queue.mkdir(parents=True)
            (work_queue / "run-ledger.json").write_text(
                json.dumps({"schema_version": 2, "history_limit": 48, "entries": []}),
                encoding="utf-8",
            )
            (work_queue / "discovery-state.json").write_text(
                json.dumps({"schema_version": 2, "history_limit": 24, "history": []}),
                encoding="utf-8",
            )

            changed = ensure_status_history.ensure_retention(root)

            ledger = json.loads((work_queue / "run-ledger.json").read_text(encoding="utf-8"))
            discovery = json.loads((work_queue / "discovery-state.json").read_text(encoding="utf-8"))
            self.assertGreaterEqual(ledger["history_limit"], 192)
            self.assertGreaterEqual(discovery["history_limit"], 256)
            self.assertEqual(
                set(changed),
                {".survey/work-queue/run-ledger.json", ".survey/work-queue/discovery-state.json"},
            )
            self.assertEqual(ensure_status_history.ensure_retention(root), [])


if __name__ == "__main__":
    unittest.main()
