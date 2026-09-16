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


def _canonical(value: object) -> str:
    return str(value or "").strip().casefold()


class StatusOrphanCandidateCoverageTest(unittest.TestCase):
    def test_emit_legacy_discovery_candidate_coverage(self) -> None:
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

        identity_payload = json.loads(
            (REPO_ROOT / ".survey/survey-state/paper-identity-index.json").read_text(
                encoding="utf-8"
            )
        )
        paper_by_identity: dict[str, str] = {}
        for primary, entry in (identity_payload.get("papers") or {}).items():
            if not isinstance(entry, dict):
                continue
            path = str(entry.get("path") or "")
            identities = [primary, *(entry.get("identifiers") or [])]
            for identity in identities:
                key = _canonical(identity)
                if key:
                    paper_by_identity[key] = path

        jobs_by_identity: dict[str, list[dict[str, object]]] = {}
        for job_id, job in jobs.items():
            payload = job["payload"]
            key = _canonical(payload.get("canonical_id"))
            if not key:
                continue
            jobs_by_identity.setdefault(key, []).append(
                {
                    "job_id": job_id,
                    "status": payload.get("status"),
                    "paper_path": payload.get("paper_path"),
                }
            )

        successful_submission_paths: set[Path] = set()
        for result in results:
            if result["payload"].get("ok") is not True:
                continue
            submission = evidence._submission_for_result(REPO_ROOT, result, submissions)
            if submission is not None:
                successful_submission_paths.add(submission["path"])

        successful_discovery_mentions: dict[str, list[str]] = {}
        for submission in submissions:
            if submission["kind"] != "discovery":
                continue
            if submission["path"] not in successful_submission_paths:
                continue
            for candidate in submission["payload"].get("candidates") or []:
                if not isinstance(candidate, dict):
                    continue
                key = _canonical(candidate.get("canonical_id"))
                if key:
                    successful_discovery_mentions.setdefault(key, []).append(
                        evidence._rel(REPO_ROOT, submission["path"])
                    )

        candidate_sources: dict[str, list[str]] = {}
        candidate_titles: dict[str, str] = {}
        for row in orphan_rows:
            for candidate in row["payload"].get("candidates") or []:
                if not isinstance(candidate, dict):
                    continue
                key = _canonical(candidate.get("canonical_id"))
                if not key:
                    continue
                candidate_sources.setdefault(key, []).append(
                    evidence._rel(REPO_ROOT, row["path"])
                )
                candidate_titles.setdefault(key, str(candidate.get("title") or ""))

        coverage = []
        uncovered = []
        for key in sorted(candidate_sources):
            jobs_for_candidate = jobs_by_identity.get(key, [])
            paper_path = paper_by_identity.get(key)
            later_successes = successful_discovery_mentions.get(key, [])
            recovered = bool(jobs_for_candidate or paper_path or later_successes)
            row = {
                "canonical_id": key,
                "title": candidate_titles.get(key, ""),
                "sources": candidate_sources[key],
                "job_matches": jobs_for_candidate,
                "paper_path": paper_path,
                "successful_discovery_mentions": later_successes,
                "recovered": recovered,
            }
            coverage.append(row)
            if not recovered:
                uncovered.append(row)

        summary = {
            "orphan_submission_count": len(orphan_rows),
            "unique_candidate_count": len(coverage),
            "recovered_candidate_count": len(coverage) - len(uncovered),
            "uncovered_candidate_count": len(uncovered),
            "uncovered": uncovered,
            "coverage": coverage,
        }
        print(
            "STATUS_ORPHAN_CANDIDATE_COVERAGE="
            + json.dumps(summary, ensure_ascii=False, sort_keys=True)
        )
        self.assertEqual(16, len(orphan_rows), orphan_rows)


if __name__ == "__main__":
    unittest.main()
