import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RETIRED_HUMAN_DOCS = (
    "PAPER-ADDITION-WORKFLOW.md",
    ".survey/docs/survey-workflow/worker-router.md",
)


class RetiredHumanDocsTests(unittest.TestCase):
    def test_retired_github_worker_manuals_remain_absent(self):
        present = [rel for rel in RETIRED_HUMAN_DOCS if (ROOT / rel).exists()]
        self.assertEqual(
            present,
            [],
            "Human worker procedures are Library-first; retired GitHub manuals must remain absent: "
            + ", ".join(present),
        )

    def test_active_scripts_do_not_reference_retired_worker_router(self):
        offenders = []
        for path in sorted((ROOT / ".survey/scripts").glob("*.py")):
            text = path.read_text(encoding="utf-8")
            if "worker-router" in text:
                offenders.append(path.relative_to(ROOT).as_posix())
        self.assertEqual(
            offenders,
            [],
            "Active scripts must not direct recovery or execution to the retired worker-router: "
            + ", ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
