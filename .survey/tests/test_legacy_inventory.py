import importlib.util
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).parents[1] / "scripts" / "legacy_inventory.py"
SPEC = importlib.util.spec_from_file_location("legacy_inventory", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

class LegacyInventoryTests(unittest.TestCase):
    def test_classifies_by_path_without_marking_anything_deletable(self):
        cases = {
            ".survey/work-queue/claims/one.json": "A_LIVE_OR_RECOVERY",
            ".survey/work-queue/archive/transport/old.json": "B_HISTORY_CANDIDATE",
            ".survey/work-queue/fallback-inbox/item.json": "A_LIVE_OR_RECOVERY",
            "papers/inference/one.md": "PAPER_CONTENT_OUT_OF_SCOPE",
            ".survey/scripts/legacy_reader.py": "C_LEGACY_REVIEW_CANDIDATE",
            "unknown/data.bin": "E_UNCLASSIFIED",
        }
        for path, expected in cases.items():
            with self.subTest(path=path):
                classification, reason, _ = MODULE.classify_path(path)
                self.assertEqual(classification, expected)
                self.assertTrue(reason)
        self.assertNotIn("DELETE", {value[0] for value in
                                    (MODULE.classify_path(path) for path in cases)})

    def test_inventory_does_not_read_paper_or_queue_payloads_and_reports_marker_only(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "papers/inference").mkdir(parents=True)
            (root / ".survey/work-queue/claims").mkdir(parents=True)
            (root / ".survey/docs").mkdir(parents=True)
            (root / "papers/inference/paper.md").write_text("DO NOT SCAN legacy body", encoding="utf-8")
            (root / ".survey/work-queue/claims/claim.json").write_text('{"secret":"legacy"}', encoding="utf-8")
            (root / ".survey/docs/guide.md").write_text("old chat-inbox.json reader", encoding="utf-8")

            result = MODULE.inventory(root, "abc123")
            self.assertEqual(result["summary"]["paper_markdown_count"], 1)
            self.assertEqual(result["summary"]["legacy_text_hit_count"], 1)
            self.assertEqual(result["legacy_text_hits"], [
                {"path": ".survey/docs/guide.md", "line": 1, "marker": "chat-inbox.json"}
            ])
            rendered = str(result)
            self.assertNotIn("DO NOT SCAN", rendered)
            self.assertNotIn("secret", rendered)
            self.assertEqual(result["source_commit"], "abc123")
            self.assertTrue(result["read_only"])

    def test_report_is_stable_in_shape_and_counts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "ordinary.txt").write_text("data", encoding="utf-8")
            first = MODULE.inventory(root)
            second = MODULE.inventory(root)
            self.assertEqual(first["summary"], second["summary"])
            self.assertEqual(first["entries"], second["entries"])

if __name__ == "__main__":
    unittest.main()
