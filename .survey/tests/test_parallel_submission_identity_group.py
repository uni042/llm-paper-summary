import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
BATCH = SCRIPTS / "process_immutable_submission_batch.py"
IMMUTABLE = SCRIPTS / "immutable_submission.py"


def _load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _write(path: Path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class ParallelSubmissionIdentityGroupTests(unittest.TestCase):
    def test_same_canonical_identity_connects_different_job_and_paper_targets(self):
        immutable = _load(IMMUTABLE, "immutable_identity_group_test")
        batch = _load(BATCH, "batch_identity_group_test")
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            descriptors = []
            for suffix in ("a", "b"):
                slot = repo / f"records/{suffix}/metadata.json"
                payload = {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": "metadata",
                    "attempt_id": f"attempt-{suffix}",
                    "job_id": f"job-{suffix}",
                    "data": {"canonical_id": "arXiv:2603.07917"},
                }
                _write(slot, payload)
                descriptor = repo / f"descriptor-{suffix}.json"
                _write(descriptor, {
                    "job_id": f"job-{suffix}",
                    "attempt_id": f"attempt-{suffix}",
                    "paper_path": f"papers/inference/{suffix}.md",
                    "record_slots": [{
                        "slot": "metadata",
                        "path": slot.relative_to(repo).as_posix(),
                        "blob_sha": immutable.git_blob_sha(slot.read_bytes()),
                    }],
                })
                descriptors.append(descriptor)

            groups = batch.group_descriptor_paths(repo, descriptors)
            self.assertEqual(len(groups), 1)
            self.assertEqual(len(groups[0]), 2)


if __name__ == "__main__":
    unittest.main()
