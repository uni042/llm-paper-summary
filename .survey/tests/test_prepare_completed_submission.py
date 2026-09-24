import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "scripts" / "prepare_completed_submission.py"
SCRIPTS = Path(__file__).parents[1] / "scripts"


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PrepareCompletedSubmissionTests(unittest.TestCase):
    def test_preflight_expected_blob_sha_overrides_completed_request_value(self):
        module = _load(SCRIPT, "prepare_completed_submission_expected_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            result = repo / ".survey/work-queue/research-preflight/results/pf.json"
            result.parent.mkdir(parents=True)
            result.write_text(json.dumps({"expected_blob_sha": None}), encoding="utf-8")
            self.assertIsNone(
                module._expected_blob_sha_from_preflight(repo, result, "1" * 40)
            )
            result.write_text(
                json.dumps({"expected_blob_sha": "2" * 40}), encoding="utf-8"
            )
            self.assertEqual(
                module._expected_blob_sha_from_preflight(repo, result, "1" * 40),
                "2" * 40,
            )

    def test_legacy_preflight_can_fall_back_to_completed_request_value(self):
        module = _load(SCRIPT, "prepare_completed_submission_legacy_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            result = repo / ".survey/work-queue/research-preflight/results/pf.json"
            result.parent.mkdir(parents=True)
            result.write_text(json.dumps({"ok": True}), encoding="utf-8")
            self.assertEqual(
                module._expected_blob_sha_from_preflight(repo, result, "3" * 40),
                "3" * 40,
            )

    def test_builder_emits_valid_ordered_slot_refs(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "test"], cwd=repo, check=True)
            scripts = repo / ".survey/scripts"
            scripts.mkdir(parents=True)
            for name in ("immutable_submission.py", "record_bank_config.py", "paper_path_resolver.py", "prepare_completed_submission.py"):
                (scripts / name).write_text((SCRIPTS / name).read_text(encoding="utf-8"), encoding="utf-8")
            module = _load(scripts / "prepare_completed_submission.py", "prepare_completed_submission_test")
            root = repo / ".survey/work-queue/records/chat-record"
            root.mkdir(parents=True)
            for slot in module.SLOT_NAMES:
                payload = {"schema_version": 1, "transport_version": 10, "slot": slot, "attempt_id": "attempt-a", "job_id": "job-a", "data": {}}
                (root / f"{slot}.json").write_text(json.dumps(payload) + "\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, capture_output=True)
            result = module.build(repo, kind="research", attempt_id="attempt-a", job_id="job-a", record_bank="a", paper_path="papers/inference/test/a.md")
            self.assertEqual([r["slot"] for r in result["record_slots"]], list(module.SLOT_NAMES))
            self.assertTrue(all(len(r["blob_sha"]) == 40 for r in result["record_slots"]))
            self.assertEqual(result["status"], "completed")


if __name__ == "__main__":
    unittest.main()
