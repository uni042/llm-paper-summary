from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import audit_legacy_inventory as inventory


class LegacyInventoryTests(unittest.TestCase):
    def test_inventory_uses_reviewed_categories_and_content_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "papers/inference").mkdir(parents=True)
            (root / ".survey/scripts").mkdir(parents=True)
            (root / "papers/inference/legacy_notes.md").write_text(
                "A harmless paper page with no retired format marker.\n", encoding="utf-8"
            )
            (root / ".survey/scripts/reader.py").write_text(
                'CHAT_INBOX = ".survey/work-queue/submissions/chat-inbox.json"\n', encoding="utf-8"
            )
            (root / "unreviewed.txt").write_text("Needs classification.\n", encoding="utf-8")

            report = inventory.build_inventory(
                root,
                source_commit="a" * 40,
                classifications={
                    "papers/inference/legacy_notes.md": {
                        "class": "B",
                        "reason": "Published current-format paper retained as history.",
                    },
                    ".survey/scripts/reader.py": {
                        "class": "E",
                        "reason": "Reads a retired fixed inbox format.",
                    },
                },
            )

            rows = {row["path"]: row for row in report["files"]}
            self.assertEqual(rows["papers/inference/legacy_notes.md"]["classification"], "B")
            self.assertEqual(rows["papers/inference/legacy_notes.md"]["legacy_markers"], [])
            self.assertEqual(rows[".survey/scripts/reader.py"]["classification"], "E")
            self.assertIn("chat-inbox.json", rows[".survey/scripts/reader.py"]["legacy_markers"])
            self.assertIsNone(rows["unreviewed.txt"]["classification"])
            self.assertEqual(report["unclassified_count"], 1)
            self.assertEqual(report["legacy_remaining"], 2)
            self.assertEqual(report["status"], "review_required")

    def test_inventory_rejects_invalid_or_reasonless_classifications(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "record.json").write_text('{"status":"complete"}\n', encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "class must be one of"):
                inventory.build_inventory(
                    root, source_commit="b" * 40,
                    classifications={"record.json": {"class": "Z", "reason": "bad"}},
                )
            with self.assertRaisesRegex(ValueError, "reason is required"):
                inventory.build_inventory(
                    root, source_commit="b" * 40,
                    classifications={"record.json": {"class": "A", "reason": ""}},
                )


if __name__ == "__main__":
    unittest.main()
