import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import immutable_submission  # noqa: E402


SLOTS = ("metadata", "problem_method", "evaluation", "results", "positioning")


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


class ImmutableBlobDurabilityTests(unittest.TestCase):
    def test_descriptor_reads_committed_blobs_after_bank_is_overwritten(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            git(repo, "init")
            git(repo, "config", "user.name", "test")
            git(repo, "config", "user.email", "test@example.com")

            bank_root = repo / ".survey/work-queue/records/chat-record"
            refs = []
            for slot in SLOTS:
                path = bank_root / f"{slot}.json"
                write_json(path, {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": "attempt-old",
                    "job_id": "job-old",
                    "data": {"marker": f"old-{slot}"},
                })
            git(repo, "add", ".")
            git(repo, "commit", "-m", "stage old immutable payload")

            for slot in SLOTS:
                relative = f".survey/work-queue/records/chat-record/{slot}.json"
                refs.append({
                    "slot": slot,
                    "path": relative,
                    "blob_sha": git(repo, "rev-parse", f"HEAD:{relative}"),
                })

            descriptor = {
                "schema_version": 1,
                "transport_version": 10,
                "kind": "research",
                "attempt_id": "attempt-old",
                "job_id": "job-old",
                "record_bank": "a",
                "paper_path": "papers/inference/test/job-old.md",
                "record_slots": refs,
            }

            for slot in SLOTS:
                path = bank_root / f"{slot}.json"
                write_json(path, {
                    "schema_version": 1,
                    "transport_version": 10,
                    "slot": slot,
                    "attempt_id": "attempt-new",
                    "job_id": "job-new",
                    "data": {"marker": f"new-{slot}"},
                })
            git(repo, "add", ".")
            git(repo, "commit", "-m", "overwrite reusable bank")

            validated = immutable_submission.validate_descriptor(repo, descriptor)
            self.assertEqual(validated["attempt_id"], "attempt-old")

            payload = immutable_submission.read_record_slot(repo, validated["record_slots"][0])
            self.assertEqual(payload["attempt_id"], "attempt-old")
            self.assertEqual(payload["job_id"], "job-old")
            self.assertEqual(payload["data"]["marker"], "old-metadata")


if __name__ == "__main__":
    unittest.main()
