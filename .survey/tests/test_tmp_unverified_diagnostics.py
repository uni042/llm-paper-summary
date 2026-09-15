import importlib.util
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).parents[2]
SCRIPT = ROOT / ".survey" / "scripts" / "build_status_dashboard.py"


def _load_evidence():
    spec = importlib.util.spec_from_file_location("build_status_dashboard_diag", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class HistoricalEvidenceDiagnostics(unittest.TestCase):
    def test_dump_historical_and_actionable_gaps(self):
        evidence = _load_evidence()
        jobs = evidence._collect_jobs(ROOT)
        submissions = evidence._collect_submissions(ROOT)
        results = evidence._collect_results(ROOT)
        verified = evidence._verified_completions(ROOT, jobs, submissions, results)
        verified_discovery = evidence._verified_discovery_rows(ROOT, jobs, submissions, results)

        verified_job_ids = {row["job_id"] for row in verified}
        verified_submission_paths = {row["submission"]["path"] for row in verified}
        verified_submission_paths.update(row["submission"]["path"] for row in verified_discovery)

        results_by_job = defaultdict(list)
        results_by_attempt = defaultdict(list)
        for row in results:
            results_by_job[row["job_id"]].append(row)
            attempt = str(row["payload"].get("attempt_id") or "")
            if attempt:
                results_by_attempt[attempt].append(row)
        submissions_by_job = defaultdict(list)
        for row in submissions:
            submissions_by_job[row["job_id"]].append(row)

        first_result = min((row["processed_at"] for row in results if row["processed_at"] is not None), default=None)

        legacy_counts = Counter()
        legacy_versions = Counter()
        legacy_completion_times = []
        for job_id, job in sorted(jobs.items()):
            payload = job["payload"]
            if job["kind"] not in {"research", "audit"}:
                continue
            if str(payload.get("status") or "").lower() != "completed" or job_id in verified_job_ids:
                continue
            if results_by_job.get(job_id):
                continue

            legacy_counts[f"kind:{job['kind']}"] += 1
            legacy_versions[str(payload.get("workflow_version") or "missing")] += 1
            if job["completed_at"] is not None:
                legacy_completion_times.append(job["completed_at"])

            paper_path = evidence._resolve_repo_path(ROOT, payload.get("paper_path"))
            legacy_counts["paper_exists" if paper_path is not None and paper_path.is_file() else "paper_missing"] += 1
            legacy_counts["matching_submission_exists" if submissions_by_job.get(job_id) else "matching_submission_missing"] += 1

            artifact_submission = evidence._resolve_repo_path(ROOT, payload.get("artifact_submission"))
            legacy_counts[
                "declared_artifact_submission_exists"
                if artifact_submission is not None and artifact_submission.is_file()
                else "declared_artifact_submission_missing"
            ] += 1

            if first_result is not None and job["completed_at"] is not None:
                legacy_counts["completed_before_first_result" if job["completed_at"] < first_result else "completed_at_or_after_first_result"] += 1

        actionable = []
        harmless_counts = Counter()
        for submission in submissions:
            if submission["path"] in verified_submission_paths:
                continue
            job_id = submission["job_id"]
            job = jobs.get(job_id)
            kind = submission["kind"]

            if job_id in verified_job_ids:
                harmless_counts[f"{kind}:job_verified_via_other_submission"] += 1
                continue
            if job is None:
                stats = submission["payload"].get("discovery_stats")
                if kind == "discovery" and isinstance(stats, dict) and stats.get("run_key") and stats.get("round"):
                    harmless_counts["discovery:durable_round_without_job"] += 1
                    continue
            if kind == "discovery" and job is not None and str(job["payload"].get("status") or "").lower() == "completed":
                stats = submission["payload"].get("discovery_stats")
                if isinstance(stats, dict) and stats.get("run_key") and stats.get("round"):
                    harmless_counts["discovery:durable_round_with_completed_job_without_result"] += 1
                    continue

            attempt_id = str(submission["payload"].get("attempt_id") or "")
            matching_results = list(results_by_attempt.get(attempt_id, [])) if attempt_id else []
            if not matching_results:
                matching_results = list(results_by_job.get(job_id, []))

            payload = {} if job is None else job["payload"]
            paper_path = evidence._resolve_repo_path(ROOT, payload.get("paper_path")) if job is not None else None
            actionable.append({
                "submission": str(submission["path"].relative_to(ROOT)),
                "kind": kind,
                "job_id": job_id,
                "attempt_id": attempt_id or None,
                "job_status": None if job is None else payload.get("status"),
                "workflow_version": None if job is None else payload.get("workflow_version"),
                "canonical_id": None if job is None else payload.get("canonical_id"),
                "job_paper_path": None if job is None else payload.get("paper_path"),
                "job_paper_exists": bool(paper_path is not None and paper_path.is_file()),
                "submission_paper_path": submission["payload"].get("paper_path"),
                "submission_keys": sorted(submission["payload"].keys()),
                "matching_results": [
                    {
                        "path": str(row["path"].relative_to(ROOT)),
                        "ok": row["payload"].get("ok"),
                        "job_status": row["payload"].get("job_status"),
                        "error": row["payload"].get("error"),
                        "submission": row["payload"].get("submission"),
                        "artifact": row["payload"].get("artifact"),
                    }
                    for row in matching_results
                ],
            })

        report = {
            "first_result_processed_at": None if first_result is None else first_result.isoformat(),
            "legacy_completed_without_any_result_total": sum(v for k, v in legacy_counts.items() if k.startswith("kind:")),
            "legacy_counts": dict(legacy_counts),
            "legacy_versions": dict(legacy_versions),
            "legacy_completed_at_min": None if not legacy_completion_times else min(legacy_completion_times).isoformat(),
            "legacy_completed_at_max": None if not legacy_completion_times else max(legacy_completion_times).isoformat(),
            "harmless_unmatched_submission_counts": dict(harmless_counts),
            "actionable_unmatched_submission_total": len(actionable),
            "actionable_unmatched_submissions": actionable,
        }
        self.fail("DIAGNOSTIC\n" + json.dumps(report, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    unittest.main()
