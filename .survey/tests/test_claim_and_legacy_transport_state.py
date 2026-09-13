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

    def test_legacy_transport_requires_ok_true_not_just_matching_job(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            inbox_path = root / select_record_bank.INBOX
            result_path = root / select_record_bank.RESULT
            inbox = {"job_id": "job-a", "attempt_id": "attempt-a", "record_bank": "b"}
            write_json(inbox_path, inbox)

            write_json(result_path, {"job_id": "job-a", "ok": False, "repair_required": True})
            _, settled = select_record_bank.current_transport(root)
            self.assertFalse(settled)

            write_json(result_path, {"job_id": "job-a", "ok": True})
            _, settled = select_record_bank.current_transport(root)
            self.assertTrue(settled)

            write_json(result_path, {"job_id": "job-b", "ok": True})
            _, settled = select_record_bank.current_transport(root)
            self.assertFalse(settled)

    def test_duplicate_claim_lease_policy_module_is_removed(self):
        self.assertFalse((SCRIPTS / "claim_lease_policy.py").exists())


if __name__ == "__main__":
    unittest.main()
