from __future__ import annotations

import datetime as dt
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))


def load(name: str):
    path = SCRIPTS / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


preflight = load("research_quality_preflight")
pipeline = load("advance_research_submission_pipeline")
processor = load("process_immutable_submission")


class RunIdentityTransportTests(unittest.TestCase):
    def test_preflight_accepts_complete_scheduled_identity_and_normalizes_time(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pre-1.json"
            start = dt.datetime.now(dt.timezone(dt.timedelta(hours=9)))
            payload = {
                "schema_version": 1,
                "operation": "research_quality_preflight",
                "request_id": "pre-1",
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "record_bank": "a",
                "worker_id": "scheduled-chat-00",
                "run_key": "2026-09-23T11:00+09:00/run",
                "scheduled_slot": "00",
                "actual_invocation_start": start.isoformat(),
                "self_review": {key: True for key in preflight.SELF_REVIEW_KEYS},
            }
            path.write_text(json.dumps(payload), encoding="utf-8")
            normalized = preflight._validate_request(path)
            self.assertEqual(normalized["worker_id"], "scheduled-chat-00")
            self.assertEqual(normalized["run_key"], payload["run_key"])
            self.assertTrue(normalized["actual_invocation_start"].endswith("+00:00"))

    def test_partial_scheduled_identity_is_rejected_but_legacy_absence_is_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "pre-1.json"
            base = {
                "schema_version": 1,
                "operation": "research_quality_preflight",
                "request_id": "pre-1",
                "kind": "research",
                "attempt_id": "attempt-a",
                "job_id": "job-a",
                "record_bank": "a",
                "self_review": {key: True for key in preflight.SELF_REVIEW_KEYS},
            }
            path.write_text(json.dumps(base), encoding="utf-8")
            self.assertNotIn("worker_id", preflight._validate_request(path))
            base["worker_id"] = "scheduled-chat-00"
            path.write_text(json.dumps(base), encoding="utf-8")
            with self.assertRaisesRegex(preflight.PreflightRequestError, "complete"):
                preflight._validate_request(path)

    def test_pipeline_carries_identity_into_audit_request_payload(self):
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        result = {
            "ok": True,
            "preflight_passed": True,
            "kind": "research",
            "attempt_id": "attempt-a",
            "job_id": "job-a",
            "record_bank": "a",
            "worker_id": "scheduled-chat-30",
            "run_key": "run-30",
            "scheduled_slot": "30",
            "actual_invocation_start": start,
        }
        payload = pipeline._payload_from_passed_preflight(Path(".survey/work-queue/research-preflight/results/pre-a.json"), result)
        audit = pipeline._generated_completed_request(payload)
        for field in ("worker_id", "run_key", "scheduled_slot", "actual_invocation_start"):
            self.assertEqual(audit[field], result[field])

    def test_submission_result_preserves_run_identity(self):
        descriptor = {
            "attempt_id": "attempt-a",
            "job_id": "job-a",
            "kind": "research",
            "worker_id": "scheduled-chat-00",
            "run_key": "run-a",
            "scheduled_slot": "00",
            "actual_invocation_start": dt.datetime.now(dt.timezone.utc).isoformat(),
        }
        result = processor._success_result(
            descriptor,
            ".survey/work-queue/submissions/research/attempt-a.json",
            job_status="completed",
            artifact={"paper": "papers/a.md"},
        )
        for field in ("worker_id", "run_key", "scheduled_slot", "actual_invocation_start"):
            self.assertEqual(result[field], descriptor[field])


if __name__ == "__main__":
    unittest.main()
