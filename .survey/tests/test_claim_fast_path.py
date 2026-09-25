from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
SCRIPT = SCRIPTS / "claim_fast_path.py"
spec = importlib.util.spec_from_file_location("claim_fast_path_test", SCRIPT)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ClaimFastPathTests(unittest.TestCase):
    def test_nonrepair_claim_skips_expensive_repair_scan(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            def allocate(_root):
                write_json(
                    root / ".survey/work-queue/claim-results/req-a.json",
                    {
                        "ok": True,
                        "assignments": [{"job_id": "job-a", "job": {"repair_required": False}}],
                    },
                )
                return {"assigned": 1}

            with (
                mock.patch.object(mod.apply_library_checkpoint_barriers, "apply", return_value={"requests_changed": 0}),
                mock.patch.object(mod.claim_worker_with_banks, "process_requests", side_effect=allocate),
                mock.patch.object(mod.repair_claim_bank_recovery, "repair_allocated_claims") as repair,
                mock.patch.object(mod.derive_worker_run_state, "apply_claim_result_deltas", return_value={"generated_results": []}) as state,
            ):
                result = mod.process(root)

            repair.assert_not_called()
            state.assert_called_once()
            self.assertTrue(result["repair"]["skipped"])
            self.assertEqual(result["changed_claim_results"], [".survey/work-queue/claim-results/req-a.json"])

    def test_repair_claim_runs_recovery_only_when_new_assignment_requires_it(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)

            def allocate(_root):
                write_json(
                    root / ".survey/work-queue/claim-results/req-r.json",
                    {
                        "ok": True,
                        "assignments": [{"job_id": "job-r", "job": {"repair_required": True}}],
                    },
                )
                return {"assigned": 1}

            with (
                mock.patch.object(mod.apply_library_checkpoint_barriers, "apply", return_value={"requests_changed": 0}),
                mock.patch.object(mod.claim_worker_with_banks, "process_requests", side_effect=allocate),
                mock.patch.object(mod.repair_claim_bank_recovery, "repair_allocated_claims", return_value={"repaired": 1}) as repair,
                mock.patch.object(mod.derive_worker_run_state, "apply_claim_result_deltas", return_value={"generated_results": []}),
            ):
                result = mod.process(root)

            repair.assert_called_once()
            self.assertFalse(result["repair"]["skipped"])
            self.assertEqual(result["repair"]["repaired"], 1)

    def test_fixed_worker_recovery_is_materialized_without_run_state_identity(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            packet = {
                "resume_recovery": True,
                "worker_id": "scheduled-chat-00",
                "job_id": "job-recover",
                "claim_id": "claim-pool-current",
                "attempt_id": "attempt-pool-current",
                "recovery_source_claim_id": "claim-old",
                "recovery_source_attempt_id": "attempt-old",
                "recovery_source_record_bank": "m",
            }
            with mock.patch.object(
                mod.hot_dispatch,
                "build_index",
                return_value={
                    "research_recovery_resume": {
                        "scheduled-chat-00": [packet],
                        "worker-7": [{**packet, "worker_id": "worker-7", "job_id": "job-adhoc"}],
                    }
                },
            ):
                result = mod._materialize_background_recovery_requests(root)

            self.assertEqual(len(result["created"]), 1)
            created = result["created"][0]
            self.assertEqual(created["worker_id"], "scheduled-chat-00")
            request = json.loads((root / created["request_path"]).read_text(encoding="utf-8"))
            self.assertTrue(request["auto_background_recovery"])
            self.assertEqual(request["job_ids"], ["job-recover"])
            self.assertEqual(request["recovery_pool_claim_id"], "claim-pool-current")
            self.assertEqual(request["recovery_source_attempt_id"], "attempt-old")
            self.assertEqual(request["recovery_source_record_bank"], "m")
            self.assertNotIn("run_key", request)
            self.assertNotIn("scheduled_slot", request)
            self.assertNotIn("actual_invocation_start", request)


if __name__ == "__main__":
    unittest.main()
