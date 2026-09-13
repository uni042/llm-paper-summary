import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import immutable_submission  # noqa: E402
import select_record_bank  # noqa: E402
from record_bank_config import BANK_ROOTS, SLOT_NAMES  # noqa: E402


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", *args], cwd=repo, text=True, capture_output=True, check=True)
    return result.stdout.strip()


def slot_payload(slot: str, attempt: str, job: str):
    return {
        "schema_version": 1,
        "transport_version": 10,
        "slot": slot,
        "attempt_id": attempt,
        "job_id": job,
        "data": {"marker": f"{attempt}-{slot}"},
    }


def commit_attempt(repo: Path, *, bank: str, attempt: str, job: str) -> dict:
    root = repo / BANK_ROOTS[bank]
    for slot in SLOT_NAMES:
        write_json(root / f"{slot}.json", slot_payload(slot, attempt, job))
    git(repo, "add", ".")
    git(repo, "commit", "-m", f"stage {attempt}")

    refs = []
    for slot in SLOT_NAMES:
        relative = f"{BANK_ROOTS[bank]}/{slot}.json"
        refs.append({
            "slot": slot,
            "path": relative,
            "blob_sha": git(repo, "rev-parse", f"HEAD:{relative}"),
        })
    descriptor = {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "attempt_id": attempt,
        "job_id": job,
        "record_bank": bank,
        "paper_path": f"papers/inference/test/{job}.md",
        "record_slots": refs,
    }
    write_json(repo / f".survey/work-queue/submissions/research/{attempt}.json", descriptor)
    git(repo, "add", ".")
    git(repo, "commit", "-m", f"submit {attempt}")
    return descriptor


def seed_other_banks(repo: Path):
    for bank, root_text in BANK_ROOTS.items():
        if bank == "a":
            continue
        root = repo / root_text
        for slot in SLOT_NAMES:
            write_json(root / f"{slot}.json", slot_payload(slot, "unused-bank-placeholder", "unused-bank-placeholder"))


class ImmutableBankReleaseTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        git(self.repo, "init")
        git(self.repo, "config", "user.name", "test")
        git(self.repo, "config", "user.email", "test@example.com")
        seed_other_banks(self.repo)

    def tearDown(self):
        self.tmp.cleanup()

    def test_ready_job_bank_becomes_reusable_after_valid_immutable_descriptor(self):
        commit_attempt(self.repo, bank="a", attempt="attempt-a", job="job-a")
        write_json(self.repo / ".survey/work-queue/jobs/job-a.json", {
            "job_id": "job-a",
            "type": "research",
            "status": "ready",
        })

        result = select_record_bank.inspect(self.repo)
        bank_a = next(row for row in result["banks"] if row["bank"] == "a")
        self.assertEqual(bank_a["state"], "reusable")
        self.assertIn("immutable", bank_a["reason"])

    def test_invalid_descriptor_does_not_release_ready_job_bank(self):
        root = self.repo / BANK_ROOTS["a"]
        for slot in SLOT_NAMES:
            write_json(root / f"{slot}.json", slot_payload(slot, "attempt-a", "job-a"))
        write_json(self.repo / ".survey/work-queue/jobs/job-a.json", {
            "job_id": "job-a",
            "type": "research",
            "status": "ready",
        })
        write_json(self.repo / ".survey/work-queue/submissions/research/attempt-a.json", {
            "schema_version": 1,
            "transport_version": 10,
            "kind": "research",
            "attempt_id": "attempt-a",
            "job_id": "job-a",
            "record_bank": "a",
            "paper_path": "papers/inference/test/job-a.md",
            "record_slots": [],
        })

        result = select_record_bank.inspect(self.repo)
        bank_a = next(row for row in result["banks"] if row["bank"] == "a")
        self.assertEqual(bank_a["state"], "occupied")
        self.assertIn("ready", bank_a["reason"])

    def test_mixed_bank_is_reusable_when_every_attempt_is_durably_immutable(self):
        descriptor_a = commit_attempt(self.repo, bank="a", attempt="attempt-a", job="job-a")
        descriptor_b = commit_attempt(self.repo, bank="a", attempt="attempt-b", job="job-b")
        write_json(self.repo / ".survey/work-queue/jobs/job-a.json", {
            "job_id": "job-a", "type": "research", "status": "ready",
        })
        write_json(self.repo / ".survey/work-queue/jobs/job-b.json", {
            "job_id": "job-b", "type": "research", "status": "ready",
        })

        root = self.repo / BANK_ROOTS["a"]
        for index, slot in enumerate(SLOT_NAMES):
            source = descriptor_a if index % 2 == 0 else descriptor_b
            payload = immutable_submission.read_record_slot(self.repo, source["record_slots"][index])
            write_json(root / f"{slot}.json", payload)

        result = select_record_bank.inspect(self.repo)
        bank_a = next(row for row in result["banks"] if row["bank"] == "a")
        self.assertEqual(bank_a["state"], "reusable")
        self.assertIn("immutable", bank_a["reason"])

    def test_duplicate_bank_reuses_global_immutable_capture_from_another_bank(self):
        descriptor = commit_attempt(self.repo, bank="a", attempt="attempt-a", job="job-a")
        write_json(self.repo / ".survey/work-queue/jobs/job-a.json", {
            "job_id": "job-a", "type": "research", "status": "ready",
        })

        duplicate_root = self.repo / BANK_ROOTS["g"]
        for index, slot in enumerate(SLOT_NAMES):
            payload = immutable_submission.read_record_slot(self.repo, descriptor["record_slots"][index])
            write_json(duplicate_root / f"{slot}.json", payload)

        result = select_record_bank.inspect(self.repo)
        bank_g = next(row for row in result["banks"] if row["bank"] == "g")
        self.assertEqual(bank_g["state"], "reusable")
        self.assertIn("immutable", bank_g["reason"])


if __name__ == "__main__":
    unittest.main()
