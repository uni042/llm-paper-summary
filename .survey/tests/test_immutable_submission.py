import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "immutable_submission.py"
SELECTOR = Path(__file__).parents[1] / "scripts" / "select_record_bank.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _slot_payload(slot, attempt_id, job_id):
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": slot,
        "attempt_id": attempt_id,
        "job_id": job_id,
        "data": {},
    }


class ImmutableSubmissionTests(unittest.TestCase):
    def test_two_descriptors_coexist_and_validate_independently(self):
        self.assertTrue(SCRIPT.exists(), "immutable_submission.py must exist")
        module = _load(SCRIPT, "immutable_submission")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            descriptors = []
            for bank, attempt_id, job_id in (
                ("a", "attempt-a", "job-a"),
                ("b", "attempt-b", "job-b"),
            ):
                root = f".survey/work-queue/records/chat-record{'-' + bank if bank != 'a' else ''}"
                refs = []
                for slot in ("metadata", "problem_method", "evaluation", "results", "positioning"):
                    path = repo / root / f"{slot}.json"
                    payload = _slot_payload(slot, attempt_id, job_id)
                    _write(path, payload)
                    refs.append({
                        "slot": slot,
                        "path": path.relative_to(repo).as_posix(),
                        "blob_sha": module.git_blob_sha(path.read_bytes()),
                    })
                descriptor_path = repo / f".survey/work-queue/submissions/research/{attempt_id}.json"
                descriptor = {
                    "schema_version": 1,
                    "transport_version": 10,
                    "kind": "research",
                    "attempt_id": attempt_id,
                    "job_id": job_id,
                    "record_bank": bank,
                    "paper_path": f"papers/inference/test/{job_id}.md",
                    "record_slots": refs,
                }
                _write(descriptor_path, descriptor)
                descriptors.append((descriptor_path, descriptor))

            pending = module.pending_descriptors(repo)
            self.assertEqual({row["attempt_id"] for row in pending}, {"attempt-a", "attempt-b"})
            for path, expected in descriptors:
                loaded = module.load_descriptor(path)
                self.assertEqual(loaded["job_id"], expected["job_id"])
                validated = module.validate_descriptor(repo, loaded)
                self.assertEqual(validated["record_bank"], expected["record_bank"])

    def test_matching_result_removes_descriptor_from_pending(self):
        self.assertTrue(SCRIPT.exists(), "immutable_submission.py must exist")
        module = _load(SCRIPT, "immutable_submission_result")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            path = repo / ".survey/work-queue/submissions/research/attempt-a.json"
            _write(path, {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "record_bank": "a",
                "paper_path": "papers/inference/test/job-a.md",
                "record_slots": [],
            })
            result = module.result_path_for(repo, path)
            _write(result, {"schema_version": 1, "attempt_id": "attempt-a", "job_id": "job-a", "ok": True})
            self.assertEqual(module.pending_descriptors(repo), [])

    def test_selector_keeps_bank_occupied_while_immutable_submission_is_unresolved(self):
        self.assertTrue(SCRIPT.exists(), "immutable_submission.py must exist")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            scripts = repo / ".survey/scripts"
            scripts.mkdir(parents=True, exist_ok=True)
            (scripts / "select_record_bank.py").write_text(SELECTOR.read_text(encoding="utf-8"), encoding="utf-8")

            # The selector imports record_bank_config from its script directory.
            config_src = Path(__file__).parents[1] / "scripts" / "record_bank_config.py"
            (scripts / "record_bank_config.py").write_text(config_src.read_text(encoding="utf-8"), encoding="utf-8")
            registry_src = Path(__file__).parents[1] / "work-queue" / "records" / "bank-registry.json"
            registry_dst = repo / ".survey/work-queue/records/bank-registry.json"
            registry_dst.parent.mkdir(parents=True, exist_ok=True)
            registry_dst.write_text(registry_src.read_text(encoding="utf-8"), encoding="utf-8")

            for bank, root in {
                "a": ".survey/work-queue/records/chat-record",
                "b": ".survey/work-queue/records/chat-record-b",
                "c": ".survey/work-queue/records/chat-record-c",
                "d": ".survey/work-queue/records/chat-record-d",
                "e": ".survey/work-queue/records/chat-record-e",
                "f": ".survey/work-queue/records/chat-record-f",
                "g": ".survey/work-queue/records/chat-record-g",
                "h": ".survey/work-queue/records/chat-record-h",
            }.items():
                attempt = "attempt-live" if bank == "a" else "unused-bank-placeholder"
                job = "job-live" if bank == "a" else "unused-bank-placeholder"
                for slot in ("metadata", "problem_method", "evaluation", "results", "positioning"):
                    _write(repo / root / f"{slot}.json", _slot_payload(slot, attempt, job))

            _write(repo / ".survey/work-queue/jobs/job-live.json", {
                "job_id": "job-live",
                "type": "research",
                "status": "ready",
            })
            _write(repo / ".survey/work-queue/submissions/research/attempt-live.json", {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-live",
                "job_id": "job-live",
                "record_bank": "a",
                "paper_path": "papers/inference/test/job-live.md",
                "record_slots": [],
            })

            selector = _load(scripts / "select_record_bank.py", "selector_with_immutable")
            result = selector.inspect(repo)
            bank_a = next(row for row in result["banks"] if row["bank"] == "a")
            self.assertEqual(bank_a["state"], "occupied")
            self.assertIn("immutable", bank_a["reason"])
            self.assertNotEqual(result["selected_bank"], "a")


if __name__ == "__main__":
    unittest.main()
