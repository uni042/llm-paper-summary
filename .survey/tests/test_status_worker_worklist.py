import importlib.util
import sys
from pathlib import Path
import unittest


SCRIPTS = Path(__file__).parents[1] / "scripts"
SCRIPT = SCRIPTS / "build_worker_worklist.py"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


def _load():
    spec = importlib.util.spec_from_file_location("build_worker_worklist_identity_test", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class WorkerWorklistIdentityTests(unittest.TestCase):
    def test_research_reservation_excludes_discovery_arxiv_doi_alias(self):
        module = _load()
        reserved = [
            {
                "canonical_id": "arXiv:2401.01234",
                "title": "Reserved Paper",
                "source_url": "https://arxiv.org/abs/2401.01234",
            }
        ]
        discovery = [
            {
                "canonical_id": "DOI:10.48550/arxiv.2401.01234",
                "identity_tokens": ["DOI:10.48550/arxiv.2401.01234"],
                "source_url": "https://doi.org/10.48550/arxiv.2401.01234",
            },
            {
                "canonical_id": "arXiv:2401.99999",
                "identity_tokens": ["arXiv:2401.99999"],
                "title": "Unique Discovery Paper",
            },
        ]

        remaining = module._exclude_reserved_identities(
            discovery,
            reserved_rows=reserved,
        )

        self.assertEqual(
            [row["canonical_id"] for row in remaining],
            ["arXiv:2401.99999"],
        )

    def test_research_rows_are_deduped_before_worker_split(self):
        module = _load()
        rows = [
            {
                "canonical_id": "DOI:10.48550/arxiv.2502.01234",
                "source_url": "https://doi.org/10.48550/arxiv.2502.01234",
            },
            {
                "canonical_id": "arXiv:2502.01234",
                "source_url": "https://arxiv.org/abs/2502.01234",
            },
            {
                "canonical_id": "arXiv:2502.09999",
                "source_url": "https://arxiv.org/abs/2502.09999",
            },
        ]

        deduped = module._dedupe_rows_by_identity(rows)
        assigned = module._split(deduped, limit=10)

        all_ids = [
            row["canonical_id"]
            for worker in ("00", "30")
            for row in assigned[worker]
        ]
        self.assertEqual(len(all_ids), 2)
        self.assertIn("arXiv:2502.09999", all_ids)
        self.assertEqual(
            sum(
                ident in {
                    "DOI:10.48550/arxiv.2502.01234",
                    "arXiv:2502.01234",
                }
                for ident in all_ids
            ),
            1,
        )


if __name__ == "__main__":
    unittest.main()
