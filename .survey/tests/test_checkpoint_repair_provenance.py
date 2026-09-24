import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import apply_library_checkpoint_barriers  # noqa: E402
import repair_claim_bank_recovery  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class CheckpointRepairProvenanceTests(unittest.TestCase):
    def test_repairable_checkpoint_is_demoted_not_deleted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-checkpointed-repair"
            checkpoint_ref = "/LLM-survey-outbox/pending/envelope.json"
            request_path = root / ".survey/work-queue/claim-requests/req.json"
            write_json(request_path, {
                "schema_version": 1,
                "request_id": "req",
                "checkpointed_jobs": [{"job_id": job_id, "checkpoint_ref": checkpoint_ref}],
            })
            with patch.object(apply_library_checkpoint_barriers, "_repairable_jobs", return_value={job_id}), \
                 patch.object(apply_library_checkpoint_barriers, "_persisted_barriers", return_value={}):
                result = apply_library_checkpoint_barriers.apply(root)

            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertNotIn("checkpointed_jobs", request)
            self.assertEqual(request["repair_checkpointed_jobs"], [
                {"job_id": job_id, "checkpoint_ref": checkpoint_ref}
            ])
            self.assertEqual(result["repair_barriers_demoted"], 1)

    def test_repair_recovery_can_restore_checkpoint_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-checkpointed-repair"
            checkpoint_ref = "/LLM-survey-outbox/pending/envelope.json"
            write_json(root / ".survey/work-queue/claim-requests/req.json", {
                "schema_version": 1,
                "request_id": "req",
                "repair_checkpointed_jobs": [
                    {"job_id": job_id, "checkpoint_ref": checkpoint_ref}
                ],
            })
            claim = {"job_id": job_id, "request_id": "req"}
            self.assertEqual(
                repair_claim_bank_recovery._repair_checkpoint_ref(root, claim),
                checkpoint_ref,
            )

    def test_unrepairable_checkpoint_remains_hard_allocation_barrier(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            job_id = "job-still-checkpointed"
            checkpoint_ref = "/LLM-survey-outbox/pending/envelope.json"
            request_path = root / ".survey/work-queue/claim-requests/req.json"
            write_json(request_path, {
                "schema_version": 1,
                "request_id": "req",
                "checkpointed_jobs": [{"job_id": job_id, "checkpoint_ref": checkpoint_ref}],
            })
            with patch.object(apply_library_checkpoint_barriers, "_repairable_jobs", return_value=set()), \
                 patch.object(apply_library_checkpoint_barriers, "_persisted_barriers", return_value={}):
                apply_library_checkpoint_barriers.apply(root)

            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(request["checkpointed_jobs"], [
                {"job_id": job_id, "checkpoint_ref": checkpoint_ref}
            ])
            self.assertNotIn("repair_checkpointed_jobs", request)


if __name__ == "__main__":
    unittest.main()
