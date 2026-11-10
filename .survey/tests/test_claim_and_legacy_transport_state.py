import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import claim_state  # noqa: E402
import select_record_bank  # noqa: E402


NOW = datetime(2026, 9, 13, 12, 0, tzinfo=timezone.utc)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ClaimAndLegacyTransportStateTests(unittest.TestCase):
    def test_release_and_invalidation_markers_make_future_lease_inactive(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            claims = root / ".survey/work-queue/claims"
            future = (NOW + timedelta(hours=3)).isoformat()
            write_json(claims / "normal.json", {"job_id": "normal", "expires_at": future})
            write_json(claims / "released.json", {
                "job_id": "released", "expires_at": future, "released_at": NOW.isoformat(),
            })
            write_json(claims / "invalidated.json", {
                "job_id": "invalidated", "expires_at": future, "lease_invalidated_at": NOW.isoformat(),
            })

            current = claim_state.current_claims(root, NOW)

            self.assertTrue(current["normal"]["active"])
            self.assertFalse(current["released"]["active"])
            self.assertTrue(current["released"]["released"])
            self.assertFalse(current["invalidated"]["active"])
            self.assertTrue(current["invalidated"]["invalidated"])

    def test_bank_selector_has_no_fixed_chat_transport_state(self):
        self.assertFalse(hasattr(select_record_bank, "INBOX"))
        self.assertFalse(hasattr(select_record_bank, "RESULT"))
        with tempfile.TemporaryDirectory() as td:
            inbox, settled = select_record_bank.current_transport(Path(td))
        self.assertIsNone(inbox)
        self.assertTrue(settled)

    def test_duplicate_claim_lease_policy_module_is_removed(self):
        self.assertFalse((SCRIPTS / "claim_lease_policy.py").exists())


if __name__ == "__main__":
    unittest.main()
