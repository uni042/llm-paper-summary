import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path


class IdentityDeltaTests(unittest.TestCase):
    def setUp(self):
        scripts = Path(__file__).resolve().parents[1] / "scripts"
        sys.path.insert(0, str(scripts))
        self.survey = importlib.import_module("survey")
        self.delta = importlib.import_module("identity_delta")
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        self.survey.ROOT = root
        self.delta.ROOT = root
        (root / "papers/inference/test").mkdir(parents=True)
        (root / "survey-state/identity-deltas").mkdir(parents=True)
        (root / "survey-state/paper-identity-index.json").write_text(
            json.dumps({
                "schema_version": 3,
                "active_count": 0,
                "papers": {},
                "identifier_to_canonical": {},
                "ignored_moved_stubs": []
            })
        )
        self.paper = root / "papers/inference/test/2026-2607.02043-kairos.md"
        self.paper.write_text("""---
canonical_id: arXiv:2607.02043
arxiv_id: 2607.02043
title: Kairos
summary: test
source: https://arxiv.org/abs/2607.02043
last_audited: null
audit_version: 0
---
body
""")

    def tearDown(self):
        self.tmp.cleanup()

    def test_prepare_lookup_validate_compact(self):
        rel = self.paper.relative_to(self.survey.ROOT).as_posix()
        out = self.delta.prepare(rel)
        self.assertTrue(out.endswith("arxiv/2607.02043.json"))
        hit = self.delta.logical_lookup("arXiv:2607.02043")
        self.assertEqual(hit[0], "arXiv:2607.02043")
        self.assertEqual(self.delta.validate_all(), 1)
        self.assertEqual(self.delta.compact(), 1)
        base = json.loads((self.survey.ROOT / "survey-state/paper-identity-index.json").read_text())
        self.assertIn("arXiv:2607.02043", base["papers"])
        self.assertEqual(self.delta.validate_all(), 0)


if __name__ == "__main__":
    unittest.main()
