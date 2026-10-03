import importlib.util
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).parents[1] / "scripts"
SCRIPT = SCRIPTS / "assemble_research_record.py"


def _load(path, name):
    if str(SCRIPTS) not in sys.path:
        sys.path.insert(0, str(SCRIPTS))
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PreferredTermNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = _load(SCRIPT, "assemble_research_record_normalize_test")

    def test_publication_path_preserves_worker_written_parenthetical_form(self):
        text = "混合専門家（Mixture-of-Experts; MoE）のroutingを改善する。"
        self.assertEqual(self.module.normalize_preferred_terms(text), text)

    def test_publication_path_does_not_rewrite_worker_prose(self):
        text = "このroutingはexpertを2個使う。"
        self.assertEqual(self.module.normalize_preferred_terms(text), text)


if __name__ == "__main__":
    unittest.main()
