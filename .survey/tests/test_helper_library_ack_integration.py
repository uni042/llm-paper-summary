from pathlib import Path
import unittest


class HelperLibraryAckIntegrationTests(unittest.TestCase):
    def test_survey_helper_refreshes_library_ack_manifest_before_commit(self) -> None:
        root = Path(__file__).resolve().parents[2]
        workflow = (root / ".github/workflows/survey-helper.yml").read_text(encoding="utf-8")
        self.assertIn(".survey/scripts/library_ack_manifest.py", workflow)
        self.assertIn("Refresh Library publication acknowledgement manifest", workflow)
        self.assertIn("--output .survey/work-queue/library-ack-manifest.json", workflow)
        self.assertLess(
            workflow.index("Refresh Library publication acknowledgement manifest"),
            workflow.index("Commit background queue results"),
        )


if __name__ == "__main__":
    unittest.main()
