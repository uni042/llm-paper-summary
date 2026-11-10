from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import render_status_dashboard_core as status  # noqa: E402


class ForwardCitationCoverageStatusTest(unittest.TestCase):
    def test_status_uses_durable_forward_sweep_state(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / ".survey/work-queue/forward-citation-sweep.json"
            path.parent.mkdir(parents=True)
            path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "updated_at": "2026-10-03T14:00:00+00:00",
                        "paper_count": 4,
                        "due_seed_count_before_run": 3,
                        "candidate_count": 7,
                        "seeds": {
                            "a": {
                                "supported": True,
                                "completed_cycles": 1,
                                "last_completed_at": "2026-10-03T13:00:00+00:00",
                            },
                            "b": {
                                "supported": True,
                                "cycle_started_at": "2026-10-03T14:00:00+00:00",
                                "last_error": "rate limit",
                            },
                            "c": {
                                "supported": True,
                            },
                            "d": {
                                "supported": False,
                            },
                        },
                    }
                ),
                encoding="utf-8",
            )

            snapshot = status._forward_citation_coverage(root)
            self.assertTrue(snapshot["available"])
            self.assertEqual(snapshot["supported"], 3)
            self.assertEqual(snapshot["unsupported"], 1)
            self.assertEqual(snapshot["completed"], 1)
            self.assertEqual(snapshot["in_progress"], 1)
            self.assertEqual(snapshot["never_started"], 1)
            self.assertEqual(snapshot["candidate_count"], 7)
            self.assertEqual(snapshot["errors"], 1)

            rendered = "\n".join(status._render_forward_citation_coverage(snapshot))
            self.assertIn("全収録論文の前方引用巡回", rendered)
            self.assertIn("初回カバレッジ完了率: **33.3%**", rendered)
            self.assertIn("| provider巡回不能 | **1** |", rendered)


if __name__ == "__main__":
    unittest.main()
