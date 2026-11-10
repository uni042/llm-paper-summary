import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
PROCESSOR = SCRIPTS / "process_immutable_submission.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class ParallelSubmissionReconciliationTests(unittest.TestCase):
    def test_preexisting_terminal_job_reconciliation_has_zero_shared_effect(self):
        processor = _load(PROCESSOR, "processor_reconciliation_test")
        for descriptor in (
            {"kind": "research", "status": "completed"},
            {"kind": "audit", "status": "completed"},
            {"kind": "research", "status": "rejected"},
        ):
            state = processor._reconciled_effect_state(descriptor)
            self.assertEqual(state["stats"]["research_completed"], 0)
            self.assertEqual(state["stats"]["audit_completed"], 0)
            self.assertEqual(state["stats"]["rejected"], 0)
            self.assertFalse(state["maintenance"]["views_dirty"])


if __name__ == "__main__":
    unittest.main()
