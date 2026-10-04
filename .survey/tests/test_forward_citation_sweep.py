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
                    "max_provider_errors_per_run": 3,
                    "request_spacing_seconds": 0,
                    "cadence": [{"max_paper_age_days": None, "rescan_days": 30}],
                }
            ),
            encoding="utf-8",
        )

    def test_url_seed_is_used_only_for_semantic_scholar_supported_hosts(self) -> None:
        record = forward_citation_sweep.citation_graph.PaperRecord(
            path="papers/inference/test/url.md",
            canonical_id="Custom:paper",
            identifiers=("Custom:paper",),
            meta={"source": "https://dl.acm.org/doi/10.1145/example"},
        )
        unsupported = forward_citation_sweep.citation_graph.PaperRecord(
            path="papers/inference/test/unsupported.md",
            canonical_id="Custom:unsupported",
            identifiers=("Custom:unsupported",),
            meta={"source": "https://example.org/paper"},
        )
        self.assertEqual(
            forward_citation_sweep._seed_identifier(record),
            "URL:https://dl.acm.org/doi/10.1145/example",
        )
        self.assertIsNone(forward_citation_sweep._seed_identifier(unsupported))

    def test_in_progress_seed_does_not_starve_never_scanned_seed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_fixture(root)
            second_paper = root / "papers/inference/test/paper2.md"
            second_paper.write_text(
                """---
canonical_id: arXiv:2401.00002
arxiv_id: 2401.00002
title: Second Seed
published: 2024-01-16
lineage: test-lineage
---
# Second Seed
""",
                encoding="utf-8",
            )
            state_path = root / ".survey/work-queue/forward-citation-sweep.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "seeds": {
                            "arXiv:2401.00001": {
                                "canonical_id": "arXiv:2401.00001",
                                "seed_identifier": "arXiv:2401.00001",
                                "supported": True,
                                "cycle_started_at": "2026-10-01T00:00:00+00:00",
                                "last_page_at": "2026-10-02T00:00:00+00:00",
                                "next_cursor": "100",
                                "rescan_days": 30,
                            }
                        },
                        "candidates": {},
                        "candidate_aliases": {},
                    }
                ),
                encoding="utf-8",
            )
            seen_sources = []

            def fake_fetcher(source_url, *, page_size=100, **kwargs):
                seen_sources.append(source_url)
                return lambda cursor: {"records": [], "next_cursor": None}

            with patch.object(
                forward_citation_sweep.discovery_provider_adapter,
                "semantic_scholar_fetcher",
                side_effect=fake_fetcher,
            ):
                result = forward_citation_sweep.sweep(
                    root,
                    now=dt.datetime(2026, 10, 3, tzinfo=dt.timezone.utc),
                    sleep_fn=lambda _: None,
                )

            self.assertEqual(result["selected_seed_count"], 1)
            self.assertIn("2401.00002", seen_sources[0])


    def test_provider_error_budget_rotates_failed_seed_instead_of_starving_pool(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_fixture(root)
            second_paper = root / "papers/inference/test/paper2.md"
            second_paper.write_text(
                """---
canonical_id: arXiv:2401.00002
arxiv_id: 2401.00002
title: Second Seed
published: 2024-01-16
lineage: test-lineage
---
# Second Seed
""",
                encoding="utf-8",
            )
            config_path = root / ".survey/config/forward-citation-sweep.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["max_provider_errors_per_run"] = 1
            config_path.write_text(json.dumps(config), encoding="utf-8")

            seen_sources = []

            def failing_fetcher(source_url, *, page_size=100, **kwargs):
                seen_sources.append(source_url)

                def fetch(cursor):
                    raise RuntimeError("provider unavailable")

                return fetch

            first_now = dt.datetime(2026, 10, 3, tzinfo=dt.timezone.utc)
            with patch.object(
                forward_citation_sweep.discovery_provider_adapter,
                "semantic_scholar_fetcher",
                side_effect=failing_fetcher,
            ):
                first = forward_citation_sweep.sweep(
                    root, now=first_now, sleep_fn=lambda _: None
                )
                second = forward_citation_sweep.sweep(
                    root,
                    now=first_now + dt.timedelta(hours=6),
                    sleep_fn=lambda _: None,
                )

            self.assertTrue(first["provider_error_budget_exhausted"])
            self.assertEqual(first["attempted_seed_count"], 1)
            self.assertTrue(second["provider_error_budget_exhausted"])
            self.assertEqual(second["attempted_seed_count"], 1)
            self.assertEqual(len(seen_sources), 2)
            self.assertIn("2401.00001", seen_sources[0])
            self.assertIn("2401.00002", seen_sources[1])

    def test_seed_specific_404_does_not_abort_remaining_selected_seeds(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_fixture(root)
            second_paper = root / "papers/inference/test/paper2.md"
            second_paper.write_text(
                """---
canonical_id: arXiv:2401.00002
arxiv_id: 2401.00002
title: Second Seed
published: 2024-01-16
lineage: test-lineage
---
# Second Seed
""",
                encoding="utf-8",
            )
            config_path = root / ".survey/config/forward-citation-sweep.json"
            config = json.loads(config_path.read_text(encoding="utf-8"))
            config["max_seeds_per_run"] = 2
            config["max_provider_errors_per_run"] = 1
            config_path.write_text(json.dumps(config), encoding="utf-8")

            calls = []

            def mixed_fetcher(source_url, *, page_size=100, **kwargs):
                calls.append(source_url)
                if "2401.00001" in source_url:
                    def fail(cursor):
                        raise forward_citation_sweep.discovery_provider_adapter.DiscoveryProviderError(
                            "not found", status_code=404
                        )
                    return fail
                return lambda cursor: {"records": [], "next_cursor": None}

            with patch.object(
                forward_citation_sweep.discovery_provider_adapter,
                "semantic_scholar_fetcher",
                side_effect=mixed_fetcher,
            ):
                result = forward_citation_sweep.sweep(
                    root,
                    now=dt.datetime(2026, 10, 3, tzinfo=dt.timezone.utc),
                    sleep_fn=lambda _: None,
                )

            self.assertEqual(result["attempted_seed_count"], 2)
            self.assertEqual(result["seed_errors"], 1)
            self.assertEqual(result["provider_errors"], 0)
            self.assertFalse(result["provider_error_budget_exhausted"])
            self.assertEqual(result["completed_cycles"], 1)
            self.assertEqual(len(calls), 2)


    def test_forward_pool_drops_candidates_already_present_in_backward_references(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.write_fixture(root)
            paper = root / "papers/inference/test/paper.md"
            paper.write_text(
                """---
canonical_id: arXiv:2401.00001
arxiv_id: 2401.00001
title: Seed Paper
published: 2024-01-15
lineage: test-lineage
references:
  - canonical_id: arXiv:2609.99999
    title: Shared Candidate
---
# Seed Paper
""",
                encoding="utf-8",
            )

            state_path = root / ".survey/work-queue/forward-citation-sweep.json"
            state_path.parent.mkdir(parents=True, exist_ok=True)
            state_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "seeds": {},
                        "candidates": {
                            "arXiv:2609.99999": {
                                "canonical_id": "arXiv:2609.99999",
                                "arxiv_id": "2609.99999",
                                "title": "Shared Candidate",
                            }
                        },
                        "candidate_aliases": {
                            "arXiv:2609.99999": "arXiv:2609.99999"
                        },
                    }
                ),
                encoding="utf-8",
            )

            def fake_fetcher(source_url, *, page_size=100, **kwargs):
                return lambda cursor: {
                    "records": [
                        {
                            "canonical_id": "arXiv:2609.99999",
                            "arxiv_id": "2609.99999",
                            "title": "Shared Candidate",
                        }
                    ],
                    "next_cursor": None,
                }

            with patch.object(
                forward_citation_sweep.discovery_provider_adapter,
                "semantic_scholar_fetcher",
                side_effect=fake_fetcher,
            ):
                result = forward_citation_sweep.sweep(
                    root,
                    now=dt.datetime(2026, 10, 3, tzinfo=dt.timezone.utc),
                    sleep_fn=lambda _: None,
                )

            self.assertEqual(result["candidate_count"], 0)
            self.assertEqual(result["backward_reference_candidates_removed"], 1)
            state = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(state["candidates"], {})
            self.assertEqual(state["candidate_aliases"], {})

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
                fourth = forward_citation_sweep.sweep(
                    root, now=first_now + dt.timedelta(days=31), sleep_fn=lambda _: None
                )

            self.assertEqual(first["candidate_count"], 1)
            self.assertEqual(first["completed_cycles"], 0)
            self.assertEqual(second["completed_cycles"], 1)
            self.assertEqual(third["selected_seed_count"], 0)
            self.assertEqual(fourth["selected_seed_count"], 1)
            self.assertEqual(cursors, [None, "100", None])

            state = json.loads(
                (root / ".survey/work-queue/forward-citation-sweep.json").read_text(encoding="utf-8")
            )
            candidate = next(iter(state["candidates"].values()))
            self.assertEqual(candidate["relation_count"], 1)
            self.assertEqual(candidate["citation_count"], 7)
            self.assertEqual(candidate["forward_seed_ids"], ["arXiv:2401.00001"])


if __name__ == "__main__":
    unittest.main()
