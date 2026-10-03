from __future__ import annotations

import datetime as dt
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import forward_citation_sweep  # noqa: E402


class ForwardCitationSweepTest(unittest.TestCase):
    def write_fixture(self, root: Path) -> None:
        paper = root / "papers/inference/test/paper.md"
        paper.parent.mkdir(parents=True)
        paper.write_text(
            """---
canonical_id: arXiv:2401.00001
arxiv_id: 2401.00001
title: Seed Paper
published: 2024-01-15
lineage: test-lineage
---
# Seed Paper
""",
            encoding="utf-8",
        )
        config = root / ".survey/config/forward-citation-sweep.json"
        config.parent.mkdir(parents=True)
        config.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "policy_name": "test",
                    "max_seeds_per_run": 1,
                    "max_pages_per_seed_per_run": 1,
                    "page_size": 100,
                    "request_spacing_seconds": 0,
                    "cadence": [{"max_paper_age_days": None, "rescan_days": 30}],
                }
            ),
            encoding="utf-8",
        )

    def test_cursor_resumes_until_cycle_completion_then_waits_for_rescan(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_fixture(root)
            cursors = []

            def fake_fetcher(source_url, *, page_size=100, **kwargs):
                def fetch(cursor):
                    cursors.append(cursor)
                    if cursor is None:
                        return {
                            "records": [
                                {
                                    "canonical_id": "arXiv:2609.99999",
                                    "arxiv_id": "2609.99999",
                                    "title": "New Citing Paper",
                                    "published": "2026-09-30",
                                    "venue": "OSDI",
                                    "citation_count": 7,
                                }
                            ],
                            "next_cursor": "100",
                        }
                    return {"records": [], "next_cursor": None}
                return fetch

            first_now = dt.datetime(2026, 10, 3, tzinfo=dt.timezone.utc)
            with patch.object(
                forward_citation_sweep.discovery_provider_adapter,
                "semantic_scholar_fetcher",
                side_effect=fake_fetcher,
            ):
                first = forward_citation_sweep.sweep(root, now=first_now, sleep_fn=lambda _: None)
                second = forward_citation_sweep.sweep(
                    root, now=first_now + dt.timedelta(hours=6), sleep_fn=lambda _: None
                )
                third = forward_citation_sweep.sweep(
                    root, now=first_now + dt.timedelta(days=1), sleep_fn=lambda _: None
                )

            self.assertEqual(first["candidate_count"], 1)
            self.assertEqual(first["completed_cycles"], 0)
            self.assertEqual(second["completed_cycles"], 1)
            self.assertEqual(third["selected_seed_count"], 0)
            self.assertEqual(cursors, [None, "100"])

            state = json.loads(
                (root / ".survey/work-queue/forward-citation-sweep.json").read_text(encoding="utf-8")
            )
            candidate = next(iter(state["candidates"].values()))
            self.assertEqual(candidate["relation_count"], 1)
            self.assertEqual(candidate["citation_count"], 7)
            self.assertEqual(candidate["forward_seed_ids"], ["arXiv:2401.00001"])


if __name__ == "__main__":
    unittest.main()
