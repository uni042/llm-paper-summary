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


derive = load("derive_worker_run_state")
cache = load("worker_run_state_cache")


def write_json(root: Path, rel: str, value: object) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value), encoding="utf-8")
    return path


def base_state(root: Path, inventory: int = 60) -> None:
    write_json(
        root,
        ".survey/work-queue/next-jobs.json",
        {
            "claiming": {"ready_research_audit": inventory, "claimable": inventory},
            "counts": {"research": {"ready": inventory}, "audit": {"ready": 0}},
        },
    )
    write_json(root, ".survey/work-queue/discovery-state.json", {"schema_version": 3, "history": []})


def request(worker: str, run_key: str, start: dt.datetime) -> dict:
    slot = "00" if worker == "scheduled-chat-00" else "30"
    return {
        "schema_version": 1,
        "request_id": f"snap-{worker[-2:]}-{run_key}",
        "run_key": run_key,
        "worker_id": worker,
        "worker_kind": "scheduled_chat",
        "scheduled_slot": slot,
        "actual_invocation_start": start.astimezone(dt.timezone.utc).isoformat(),
        "runtime_condition": "none",
        "runtime_condition_confirmed": False,
        "runtime_condition_attempts": 0,
        "runtime_condition_detail": "",
    }


def add_attempt(
    root: Path,
    *,
    worker: str,
    request_id: str,
    attempt_id: str,
    job_id: str,
    claimed_at: dt.datetime,
    result: dict | None,
    descriptor_identity: dict | None = None,
) -> Path:
    write_json(
        root,
        f".survey/work-queue/claim-results/{request_id}.json",
        {
            "worker_id": worker,
            "processed_at": claimed_at.isoformat(),
            "assignments": [
                {
                    "attempt_id": attempt_id,
                    "job_id": job_id,
                    "kind": "research",
                    "claimed_at": claimed_at.isoformat(),
                }
            ],
        },
    )
    descriptor = {
        "attempt_id": attempt_id,
        "job_id": job_id,
        "kind": "research",
    }
    if descriptor_identity:
        descriptor.update(descriptor_identity)
    path = write_json(root, f".survey/work-queue/submissions/research/{attempt_id}.json", descriptor)
    if result is not None:
        payload = {
            "attempt_id": attempt_id,
            "job_id": job_id,
            "job_type": "research",
            **result,
        }
        write_json(root, f".survey/work-queue/results/research/{attempt_id}.json", payload)
    return path


class IncrementalRunStateTests(unittest.TestCase):
    def test_cache_hit_avoids_full_history_and_cache_deletion_rebuilds(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            # Controlled large-history fixture: canonical reconstruction must inspect
            # these unrelated durable claim results, while the cache hit must not.
            for index in range(1000):
                write_json(
                    root,
                    f".survey/work-queue/claim-results/history-{index:04d}.json",
                    {
                        "worker_id": "other-worker",
                        "processed_at": (start - dt.timedelta(days=1)).isoformat(),
                        "assignments": [],
                    },
                )
            add_attempt(
                root,
                worker="scheduled-chat-00",
                request_id="claim-a",
                attempt_id="attempt-a",
                job_id="job-a",
                claimed_at=start + dt.timedelta(seconds=10),
                result={
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": (start + dt.timedelta(seconds=40)).isoformat(),
                },
            )
            req = request("scheduled-chat-00", "run-a", start)
            first = derive.derive(root, req)
            second = derive.derive(root, req)
            self.assertEqual(first["run_state_source"], "canonical_rebuild")
            self.assertEqual(second["run_state_source"], "incremental_cache")
            self.assertEqual(second["research_audit_completed_this_invocation"], 1)
            self.assertLess(second["run_state_files_read"], first["run_state_files_read"])
            print(
                "RUN_STATE_BENCH "
                f"history_claim_results=1001 "
                f"canonical_files={first['run_state_files_read']} "
                f"cache_files={second['run_state_files_read']} "
                f"canonical_ms={first['run_state_derive_ms']} "
                f"cache_ms={second['run_state_derive_ms']}"
            )

            (root / ".survey/work-queue/run-state/cache/scheduled-chat-00.json").unlink()
            rebuilt = derive.derive(root, req)
            self.assertEqual(rebuilt["run_state_source"], "canonical_rebuild")
            self.assertEqual(rebuilt["research_audit_completed_this_invocation"], 1)

    def test_parallel_workers_do_not_mix(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            for suffix, worker in (("a", "scheduled-chat-00"), ("b", "scheduled-chat-30")):
                add_attempt(
                    root,
                    worker=worker,
                    request_id=f"claim-{suffix}",
                    attempt_id=f"attempt-{suffix}",
                    job_id=f"job-{suffix}",
                    claimed_at=start + dt.timedelta(seconds=10),
                    result={
                        "ok": True,
                        "job_status": "completed",
                        "processed_at": (start + dt.timedelta(seconds=30)).isoformat(),
                    },
                )
            result00 = derive.derive(root, request("scheduled-chat-00", "run-00", start))
            result30 = derive.derive(root, request("scheduled-chat-30", "run-30", start))
            self.assertEqual(result00["research_audit_completed_this_invocation"], 1)
            self.assertEqual(result30["research_audit_completed_this_invocation"], 1)
            self.assertTrue((root / ".survey/work-queue/run-state/cache/scheduled-chat-00.json").is_file())
            self.assertTrue((root / ".survey/work-queue/run-state/cache/scheduled-chat-30.json").is_file())

    def test_legacy_carry_over_pending_result_updates_incrementally(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            old_claim = start - dt.timedelta(hours=2)
            descriptor = add_attempt(
                root,
                worker="scheduled-chat-00",
                request_id="claim-old",
                attempt_id="attempt-old",
                job_id="job-old",
                claimed_at=old_claim,
                result=None,
                descriptor_identity=None,
            )
            req = request("scheduled-chat-00", "run-current", start)
            pending = derive.derive(root, req)
            self.assertTrue(pending["submission_result_pending"])
            self.assertIn("attempt-old", pending["pending_attempt_ids"])

            write_json(
                root,
                ".survey/work-queue/results/research/attempt-old.json",
                {
                    "attempt_id": "attempt-old",
                    "job_id": "job-old",
                    "job_type": "research",
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
            )
            touched = cache.observe_descriptors(root, [descriptor])
            self.assertIn("run-current", touched["scheduled-chat-00"])
            updated = derive.derive(root, req)
            self.assertFalse(updated["submission_result_pending"])
            self.assertEqual(updated["research_audit_completed_this_invocation"], 1)

    def test_retryable_result_remains_pending(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            identity = {
                "worker_id": "scheduled-chat-00",
                "run_key": "run-r",
                "scheduled_slot": "00",
                "actual_invocation_start": start.isoformat(),
            }
            descriptor = add_attempt(
                root,
                worker="scheduled-chat-00",
                request_id="claim-r",
                attempt_id="attempt-r",
                job_id="job-r",
                claimed_at=start + dt.timedelta(seconds=5),
                result=None,
                descriptor_identity=identity,
            )
            req = request("scheduled-chat-00", "run-r", start)
            derive.derive(root, req)
            write_json(
                root,
                ".survey/work-queue/results/research/attempt-r.json",
                {
                    "attempt_id": "attempt-r",
                    "job_id": "job-r",
                    "job_type": "research",
                    "ok": False,
                    "retryable": True,
                    "job_status": None,
                    "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
            )
            cache.observe_descriptors(root, [descriptor])
            result = derive.derive(root, req)
            self.assertTrue(result["submission_result_pending"])
            self.assertIn("attempt-r", result["retryable_attempt_ids"])
            self.assertEqual(result["research_audit_completed_this_invocation"], 0)

    def test_submission_can_auto_publish_snapshot_without_new_request(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            req = request("scheduled-chat-00", "run-auto", start)
            derive.derive(root, req)

            identity = {
                "worker_id": "scheduled-chat-00",
                "run_key": "run-auto",
                "scheduled_slot": "00",
                "actual_invocation_start": start.isoformat(),
            }
            descriptor = add_attempt(
                root,
                worker="scheduled-chat-00",
                request_id="claim-auto",
                attempt_id="attempt-auto",
                job_id="job-auto",
                claimed_at=start + dt.timedelta(seconds=10),
                result={
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
                descriptor_identity=identity,
            )
            manifest = root / "descriptors.txt"
            manifest.write_text(descriptor.relative_to(root).as_posix() + "\n", encoding="utf-8")
            summary = derive.auto_snapshot_from_descriptors(root, manifest)
            self.assertEqual(len(summary["generated_results"]), 1)
            result_path = root / summary["generated_results"][0]
            auto = json.loads(result_path.read_text(encoding="utf-8"))
            self.assertTrue(auto["auto_generated"])
            self.assertEqual(auto["snapshot_origin"], "submission-fast-lane")
            self.assertEqual(auto["run_key"], "run-auto")
            self.assertEqual(auto["research_audit_completed_this_invocation"], 1)
            latest = json.loads((root / ".survey/work-queue/run-state/latest/scheduled-chat-00.json").read_text(encoding="utf-8"))
            self.assertEqual(latest["result_path"], result_path.relative_to(root).as_posix())

    def test_latest_pointer_never_rolls_back_snapshot_generation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            start = dt.datetime.now(dt.timezone.utc).isoformat()
            newer_path = write_json(root, ".survey/work-queue/run-state/results/newer.json", {})
            newer = {
                "worker_id": "scheduled-chat-00",
                "run_key": "run-same",
                "scheduled_slot": "00",
                "actual_invocation_start": start,
                "request_id": "newer",
                "snapshot_generation": 5,
                "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
            }
            cache.write_latest_pointer(root, newer_path, newer)

            older_path = write_json(root, ".survey/work-queue/run-state/results/older.json", {})
            older = dict(newer)
            older["request_id"] = "older"
            older["snapshot_generation"] = 4
            self.assertFalse(cache.write_latest_pointer(root, older_path, older))

            pointer = json.loads(
                (root / ".survey/work-queue/run-state/latest/scheduled-chat-00.json").read_text(encoding="utf-8")
            )
            self.assertEqual(pointer["request_id"], "newer")
            self.assertEqual(pointer["snapshot_generation"], 5)

    def test_fact_clock_mismatch_forces_canonical_rebuild(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            req = request("scheduled-chat-00", "run-clock", start)
            derive.derive(root, req)
            cache.bump_fact_clock(root, {"scheduled-chat-00"}, "test-external-mutation")
            result = derive.derive(root, req)
            self.assertEqual(result["run_state_source"], "canonical_rebuild")

    def test_claim_result_delta_updates_active_assignment_without_canonical_scan(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            req = request("scheduled-chat-00", "run-claim-delta", start)
            first = derive.derive(root, req)
            self.assertEqual(first["run_state_source"], "canonical_rebuild")
            claim_result = write_json(
                root,
                ".survey/work-queue/claim-results/claim-delta.json",
                {
                    "schema_version": 1,
                    "request_id": "claim-delta",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "run_key": "run-claim-delta",
                    "scheduled_slot": "00",
                    "actual_invocation_start": start.isoformat(),
                    "ok": True,
                    "assignments": [
                        {
                            "attempt_id": "attempt-delta",
                            "job_id": "job-delta",
                            "kind": "research",
                            "claimed_at": (start + dt.timedelta(seconds=10)).isoformat(),
                        }
                    ],
                    "processed_at": (start + dt.timedelta(seconds=10)).isoformat(),
                },
            )
            manifest = root / "claim-results.txt"
            manifest.write_text(claim_result.relative_to(root).as_posix() + "\n", encoding="utf-8")
            summary = derive.apply_claim_result_deltas(root, manifest)
            self.assertEqual(summary["touched_runs"], 1)
            updated = derive.derive(root, req)
            self.assertEqual(updated["run_state_source"], "incremental_cache")
            self.assertTrue(updated["active_assignment"])
            self.assertEqual(updated["active_job_ids"], ["job-delta"])
            self.assertLess(updated["run_state_files_read"], first["run_state_files_read"])

    def test_legacy_claim_result_invalidates_cache_instead_of_reviving_old_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            req = request("scheduled-chat-00", "run-legacy-claim", start)
            derive.derive(root, req)
            before_clock = cache.fact_generation(root, "scheduled-chat-00")
            legacy = write_json(
                root,
                ".survey/work-queue/claim-results/legacy.json",
                {
                    "schema_version": 1,
                    "request_id": "legacy",
                    "worker_id": "scheduled-chat-00",
                    "worker_kind": "scheduled_chat",
                    "ok": True,
                    "assignments": [],
                    "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
            )
            touched = cache.observe_claim_results(root, [legacy])
            self.assertEqual(touched, {})
            self.assertGreater(cache.fact_generation(root, "scheduled-chat-00"), before_clock)
            rebuilt = derive.derive(root, req)
            self.assertEqual(rebuilt["run_state_source"], "canonical_rebuild")

    def test_submission_auto_snapshot_without_existing_route_cache_falls_back_safely(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_state(root)
            start = dt.datetime.now(dt.timezone.utc) - dt.timedelta(minutes=2)
            identity = {
                "worker_id": "scheduled-chat-00",
                "run_key": "run-no-cache",
                "scheduled_slot": "00",
                "actual_invocation_start": start.isoformat(),
            }
            descriptor = add_attempt(
                root,
                worker="scheduled-chat-00",
                request_id="claim-no-cache",
                attempt_id="attempt-no-cache",
                job_id="job-no-cache",
                claimed_at=start + dt.timedelta(seconds=10),
                result={
                    "ok": True,
                    "job_status": "completed",
                    "processed_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                },
                descriptor_identity=identity,
            )
            manifest = root / "descriptors.txt"
            manifest.write_text(descriptor.relative_to(root).as_posix() + "\n", encoding="utf-8")
            summary = derive.auto_snapshot_from_descriptors(root, manifest)
            self.assertEqual(summary["generated_results"], [])
            self.assertIn("scheduled-chat-00:run-no-cache", summary["fallback_required"])


if __name__ == "__main__":
    unittest.main()
