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
    def test_dump_unverified_completed_and_unmatched_submissions(self):
        evidence = _load_evidence()
        jobs = evidence._collect_jobs(ROOT)
        submissions = evidence._collect_submissions(ROOT)
        results = evidence._collect_results(ROOT)
        verified = evidence._verified_completions(ROOT, jobs, submissions, results)
        verified_discovery = evidence._verified_discovery_rows(ROOT, jobs, submissions, results)

        verified_job_ids = {row["job_id"] for row in verified}
        verified_submission_paths = {str(row["submission"]["path"].relative_to(ROOT)) for row in verified}
        verified_submission_paths.update(
            str(row["submission"]["path"].relative_to(ROOT)) for row in verified_discovery
        )

        results_by_job = defaultdict(list)
        for row in results:
            results_by_job[row["job_id"]].append(row)
        submissions_by_job = defaultdict(list)
        for row in submissions:
            submissions_by_job[row["job_id"]].append(row)

        reason_counts = Counter()
        reason_versions = defaultdict(Counter)
        reason_samples = defaultdict(list)

        for job_id, job in sorted(jobs.items()):
            payload = job["payload"]
            status = str(payload.get("status") or "").lower()
            if job["kind"] not in {"research", "audit"} or status != "completed" or job_id in verified_job_ids:
                continue

            version = str(payload.get("workflow_version") or "missing")
            job_results = results_by_job.get(job_id, [])
            success_results = [
                row for row in job_results
                if row["payload"].get("ok") is True
                and str(row["payload"].get("job_status") or "").lower() == "completed"
                and row["kind"] in {job["kind"], "unknown"}
            ]
            reason = None
            detail = {}
            if not success_results:
                reason = "no_success_result"
                detail = {
                    "results": len(job_results),
                    "result_states": [
                        {
                            "ok": row["payload"].get("ok"),
                            "job_status": row["payload"].get("job_status"),
                            "kind": row["kind"],
                            "path": str(row["path"].relative_to(ROOT)),
                        }
                        for row in job_results[:3]
                    ],
                }
            else:
                matching = []
                for result in success_results:
                    submission = evidence._submission_for_result(ROOT, result, submissions)
                    if submission is not None and submission["job_id"] == job_id:
                        matching.append((result, submission))
                if not matching:
                    reason = "success_result_without_matching_submission"
                    detail = {
                        "success_results": [str(row["path"].relative_to(ROOT)) for row in success_results[:3]],
                        "submissions": [str(row["path"].relative_to(ROOT)) for row in submissions_by_job.get(job_id, [])[:3]],
                    }
                elif job["kind"] == "research" and not any(
                    evidence._paper_path(ROOT, result["payload"], submission["payload"], payload)
                    for result, submission in matching
                ):
                    reason = "research_paper_unresolvable"
                    detail = {
                        "job_paper_path": payload.get("paper_path"),
                        "matching": [
                            {
                                "result": str(result["path"].relative_to(ROOT)),
                                "submission": str(submission["path"].relative_to(ROOT)),
                                "artifact": result["payload"].get("artifact"),
                                "submission_paper_path": submission["payload"].get("paper_path"),
                            }
                            for result, submission in matching[:3]
                        ],
                    }
                elif not any((result["processed_at"] or job["completed_at"]) is not None for result, _ in matching):
                    reason = "completion_timestamp_missing"
                else:
                    reason = "other_verification_mismatch"

            reason_counts[reason] += 1
            reason_versions[reason][version] += 1
            if len(reason_samples[reason]) < 15:
                reason_samples[reason].append({
                    "job_id": job_id,
                    "kind": job["kind"],
                    "workflow_version": version,
                    "canonical_id": payload.get("canonical_id"),
                    "paper_path": payload.get("paper_path"),
                    "artifact_submission": payload.get("artifact_submission"),
                    **detail,
                })

        unmatched_counts = Counter()
        unmatched_versions = defaultdict(Counter)
        unmatched_samples = defaultdict(list)
        for submission in submissions:
            rel = str(submission["path"].relative_to(ROOT))
            if rel in verified_submission_paths:
                continue
            job_id = submission["job_id"]
            job = jobs.get(job_id)
            kind = submission["kind"]
            if job_id in verified_job_ids:
                bucket = f"{kind}:job_verified_via_other_submission"
                version = str(job["payload"].get("workflow_version") or "missing") if job else "missing"
            elif job is None:
                stats = submission["payload"].get("discovery_stats")
                if kind == "discovery" and isinstance(stats, dict) and stats.get("run_key") and stats.get("round"):
                    bucket = "discovery:durable_round_without_job"
                else:
                    bucket = f"{kind}:job_missing"
                version = "missing"
            else:
                status = str(job["payload"].get("status") or "missing").lower()
                bucket = f"{kind}:job_{status}_not_verified"
                version = str(job["payload"].get("workflow_version") or "missing")

            unmatched_counts[bucket] += 1
            unmatched_versions[bucket][version] += 1
            if len(unmatched_samples[bucket]) < 12:
                unmatched_samples[bucket].append({
                    "path": rel,
                    "job_id": job_id,
                    "attempt_id": submission["payload"].get("attempt_id"),
                    "job_status": None if job is None else job["payload"].get("status"),
                    "worker_id": submission["payload"].get("worker_id"),
                })

        report = {
            "completed_unverified_total": sum(reason_counts.values()),
            "completed_unverified_by_reason": dict(reason_counts),
            "completed_unverified_versions": {k: dict(v) for k, v in reason_versions.items()},
            "completed_unverified_samples": dict(reason_samples),
            "unmatched_submission_total": sum(unmatched_counts.values()),
            "unmatched_submission_by_bucket": dict(unmatched_counts),
            "unmatched_submission_versions": {k: dict(v) for k, v in unmatched_versions.items()},
            "unmatched_submission_samples": dict(unmatched_samples),
        }
        self.fail("DIAGNOSTIC\n" + json.dumps(report, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    unittest.main()
