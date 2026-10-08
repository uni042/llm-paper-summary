"""Verify prefilter changes the worklist, not canonical candidate population."""
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
SPEC = importlib.util.spec_from_file_location("build_worker_worklist_prefilter_test", SCRIPTS / "build_worker_worklist.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


class PrefilterWorklistTests(unittest.TestCase):
    def test_only_selection_changes_and_config_rollback_restores(self):
        good = {"canonical_id": "arXiv:2601.00001", "title": "GPU KV Cache Offloading for LLM Inference", "priority": 10}
        other = {"canonical_id": "arXiv:2601.00002", "title": "Tomato Cluster Phenotyping", "priority": 99}
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            cfg = root / ".survey/config/discovery-relevance-prefilter.json"
            cfg.parent.mkdir(parents=True)
            cfg.write_text(json.dumps({"schema_version": 1, "enabled": True, "mode": "quarantine", "audit_stride": 50, "max_audit_per_build": 2}), encoding="utf-8")
            with mock.patch.object(mod, "_research_candidates", return_value=([], 0, [])), mock.patch.object(mod, "_discovery_candidates", return_value=([good, other], 2)):
                result = mod.build(root, limit=5)
            self.assertEqual(result["00"]["discovery_review"]["pending_total"], 2)
            self.assertEqual(result["00"]["discovery_review"]["prefilter"]["quarantine_count"], 1)
            ids = [x["canonical_id"] for worker in result.values() for x in worker["discovery_review"]["rows"]]
            self.assertEqual(ids, ["arXiv:2601.00001"])
            cfg.write_text(json.dumps({"schema_version": 1, "enabled": False, "mode": "off"}), encoding="utf-8")
            with mock.patch.object(mod, "_research_candidates", return_value=([], 0, [])), mock.patch.object(mod, "_discovery_candidates", return_value=([good, other], 2)):
                restored = mod.build(root, limit=5)
            ids = [x["canonical_id"] for worker in restored.values() for x in worker["discovery_review"]["rows"]]
            self.assertEqual(set(ids), {"arXiv:2601.00001", "arXiv:2601.00002"})


if __name__ == "__main__":
    unittest.main()
