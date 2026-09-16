from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = REPO_ROOT / ".survey" / "scripts"
sys.path.insert(0, str(SCRIPTS))

import build_status_dashboard as evidence  # noqa: E402
import render_status_dashboard as status  # noqa: E402


class StatusOrphanDiagnosticsTest(unittest.TestCase):
    def test_emit_current_orphan_submission_evidence(self) -> None:
        jobs = evidence._collect_jobs(REPO_ROOT)
        submissions = evidence._collect_submissions(REPO_ROOT)
        results = evidence._collect_results(REPO_ROOT)
        rejected = status._terminally_rejected_submission_paths(
            REPO_ROOT, submissions, results
        )

        orphan_rows = [
            row
            for row in submissions
            if (not row["job_id"] or row["job_id"] not in jobs)
            and row["path"] not in rejected
            and not (
                row["kind"] == "discovery"
                and status._discovery_round_identity(row) is not None
            )
        ]

        diagnostics = []
        for row in sorted(orphan_rows, key=lambda item: str(item["path"])):
            payload = row["payload"]
            attempt_id = str(payload.get("attempt_id") or "")
            result_rows = []
            for result in results:
                result_payload = result["payload"]
                result_attempt = str(result_payload.get("attempt_id") or "")
                explicit_submission = evidence._resolve_repo_path(
                    REPO_ROOT, result_payload.get("submission")
                )
                if (
                    explicit_submission == row["path"]
                    or (attempt_id and result_attempt == attempt_id)
                ):
                    result_rows.append(
                        {
                            "path": evidence._rel(REPO_ROOT, result["path"]),
                            "job_id": result["job_id"],
                            "attempt_id": result_attempt,
                            "ok": result_payload.get("ok"),
                            "job_status": result_payload.get("job_status"),
                            "failure_class": result_payload.get("failure_class"),
                            "retryable": result_payload.get("retryable"),
                            "submission": result_payload.get("submission"),
                        }
                    )

            diagnostics.append(
                {
                    "path": evidence._rel(REPO_ROOT, row["path"]),
                    "kind": row["kind"],
                    "job_id": row["job_id"],
                    "job_exists": row["job_id"] in jobs if row["job_id"] else False,
                    "attempt_id": attempt_id,
                    "status": payload.get("status"),
                    "transport_version": payload.get("transport_version"),
                    "worker_id": payload.get("worker_id"),
                    "paper_path": payload.get("paper_path"),
                    "source_attempt_id": payload.get("source_attempt_id"),
                    "source_fallback_envelope_id": payload.get("source_fallback_envelope_id"),
                    "legacy_publication_migration": payload.get("legacy_publication_migration"),
                    "matching_results": result_rows,
                }
            )

        print("STATUS_ORPHAN_DIAGNOSTICS=" + json.dumps(diagnostics, ensure_ascii=False, sort_keys=True))
        self.assertEqual(16, len(diagnostics), diagnostics)


if __name__ == "__main__":
    unittest.main()
