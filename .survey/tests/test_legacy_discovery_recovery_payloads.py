import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import queue_worker  # noqa: E402


RECOVERY_PATHS = (
    REPO_ROOT / ".survey/work-queue/submissions/20260917T0710JST-discovery-recovery-legacy-invalid-1.json",
    REPO_ROOT / ".survey/work-queue/submissions/20260917T0710JST-discovery-recovery-legacy-invalid-2.json",
)
EXPECTED_IDS = {
    "arXiv:2505.11329",
    "arXiv:2605.28302",
    "arXiv:2606.24957",
    "arXiv:2608.25062",
    "arXiv:2609.08307",
    "arXiv:2609.12208",
}


class LegacyDiscoveryRecoveryPayloadTests(unittest.TestCase):
    def test_recovery_rounds_are_current_valid_and_cover_exactly_six_stranded_candidates(self):
        observed: set[str] = set()
        for path in RECOVERY_PATHS:
            payload = json.loads(path.read_text(encoding="utf-8"))
            self.assertTrue(queue_worker.is_discovery_round_submission(payload), path)
            candidates = payload.get("candidates") or []
            self.assertLessEqual(len(candidates), queue_worker.MAX_DISCOVERY_CANDIDATES)
            for candidate in candidates:
                canonical_id = candidate.get("canonical_id")
                self.assertIsInstance(canonical_id, str)
                self.assertNotIn(canonical_id, observed)
                observed.add(canonical_id)

        self.assertEqual(EXPECTED_IDS, observed)


if __name__ == "__main__":
    unittest.main()
