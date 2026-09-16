#!/usr/bin/env python3
"""Deterministic stop/continue gate for Scheduled Chat survey workers.

Normal Scheduled Chat completion is time-driven only.  Hourly workers receive a
one-hour run window measured from the actual invocation start; the nominal
schedule boundary is retained only as a compatibility fallback for older callers.

Discovery round counts, candidate counts, exhaustion claims, duplicate-only
rounds, backlog shape, and job-local completion are observations, never normal
run-stop conditions.  Canonical read/durability/platform failures are reported as
abnormal blockers and do not grant normal finalization permission.
"""
from __future__ import annotations

import argparse
import json


def yn(value: str) -> bool:
    value = value.strip().lower()
    if value in {"yes", "y", "true", "1"}:
        return True
    if value in {"no", "n", "false", "0"}:
        return False
    raise argparse.ArgumentTypeError("expected yes/no")


def decide(args: argparse.Namespace) -> dict[str, object]:
    blockers: list[str] = []
    stop_reasons: list[str] = []
    fallback_writable = bool(args.library_writable)
    any_durable_transport = bool(args.github_write or fallback_writable)

    worker_kind = str(getattr(args, "worker_kind", "normal") or "normal").strip().lower()
    discovery_rounds_completed = max(int(getattr(args, "discovery_rounds_completed", 0) or 0), 0)
    rounds_since_last_novel_raw = getattr(args, "discovery_rounds_since_last_novel", None)
    discovery_rounds_since_last_novel = (
        max(int(rounds_since_last_novel_raw or 0), 0)
        if rounds_since_last_novel_raw is not None
        else 0
    )
    discovery_exhausted = bool(getattr(args, "discovery_exhausted", False))
    next_axis_available = bool(getattr(args, "next_axis_available", False))

    if args.platform_limit:
        blockers.append("platform_limit_reached")

    seconds_to_next = getattr(args, "seconds_to_next_scheduled_task", None)
    seconds_to_deadline = getattr(args, "seconds_to_run_deadline", None)
    handoff_guard = int(getattr(args, "scheduled_handoff_guard_seconds", 600))

    if seconds_to_deadline is not None:
        effective_seconds_to_handoff = int(seconds_to_deadline)
        handoff_time_source = "run_deadline"
        handoff_reason = "run_deadline_within_handoff_guard"
    elif seconds_to_next is not None:
        effective_seconds_to_handoff = int(seconds_to_next)
        handoff_time_source = "next_scheduled_task"
        handoff_reason = "next_scheduled_task_within_handoff_guard"
    else:
        effective_seconds_to_handoff = None
        handoff_time_source = "unknown"
        handoff_reason = None

    time_handoff_active = bool(
        effective_seconds_to_handoff is not None
        and effective_seconds_to_handoff <= handoff_guard
        and handoff_reason is not None
    )
    if time_handoff_active:
        stop_reasons.append(str(handoff_reason))

    if not args.github_read:
        blockers.append("github_read_unavailable_for_repo_state")

    if args.unpublished_completed_result:
        durable = bool(args.result_durable or any_durable_transport)
        if not durable:
            blockers.append("completed_result_not_durably_preserved")

    if args.offline_seed_required:
        seed_durable = bool(args.seed_durable or any_durable_transport)
        if not seed_durable:
            blockers.append("required_spillover_seed_not_durably_preserved")

    independent_work = bool(
        args.independent_work
        or args.spillover_work
        or (args.can_discover and any_durable_transport)
    )

    transient_claim_wait = bool(args.claim_result_pending and args.github_read)
    if args.global_dependency and not independent_work and not transient_claim_wait:
        blockers.append("all_remaining_work_blocked_after_fallback_consideration")

    # The only normal STOP_RUN is the run-local handoff guard.  Non-time failures
    # remain abnormal blockers: callers should retry/recover or be externally
    # terminated, but must not turn them into a successful normal final response.
    if time_handoff_active:
        decision = "STOP_RUN"
        required_action = "FINALIZE"
        finalization_allowed = not blockers
    else:
        decision = "CONTINUE"
        finalization_allowed = False
        if blockers:
            required_action = "RECOVER_BLOCKER_AND_CONTINUE"
        elif worker_kind == "discovery":
            required_action = "DISCOVER_AGAIN" if (next_axis_available or args.can_discover) else "REFRESH_AXIS_AND_DISCOVER_AGAIN"
        else:
            required_action = "CONTINUE_WORK"

    write_scope = "none"
    write_action = "normal"
    if args.write_failed:
        if args.probe == "success":
            write_scope = "target_or_payload_specific"
            write_action = "checkpoint_affected_job_via_library_if_needed_then_continue; github_writes_remain_allowed"
        elif args.probe == "failure":
            write_scope = "run_wide_github_write_unavailable"
            if fallback_writable:
                write_action = "disable_further_github_writes_this_run; checkpoint_to_library; continue_ready_spillover_or_offline_discovery"
            else:
                write_action = "disable_further_github_writes_this_run; retry_or_preserve_unsaved_work; do_not_report_normal_completion"
        else:
            write_scope = "unclassified"
            write_action = "run_fixed_health_probe_once_before_classifying"

    claim_wait_action = "none"
    claim_wait_seconds = 0
    if transient_claim_wait:
        claim_wait_seconds = 30
        claim_wait_action = (
            "keep_same_request_id; do_not_issue_another_claim; wait_30_seconds; "
            "refresh_latest_head_and_matching_claim_result; if_available_check_survey_claim_fast; "
            "if_result_still_pending_wait_30_seconds_again; repeat_until_result_or_time_handoff"
        )

    return {
        "decision": decision,
        "required_action": required_action,
        "finalization_allowed": finalization_allowed,
        "stop_reasons": stop_reasons,
        "abnormal_blockers": blockers,
        "worker_kind": worker_kind,
        "discovery_rounds_completed": discovery_rounds_completed,
        "discovery_rounds_since_last_novel": discovery_rounds_since_last_novel,
        "discovery_reset_progress_known": rounds_since_last_novel_raw is not None,
        # Legacy observability fields are retained for callers, but quotas are disabled.
        "discovery_min_rounds": None,
        "minimum_rounds_remaining": 0,
        "discovery_exhausted": discovery_exhausted,
        "next_axis_available": next_axis_available,
        "write_failure_scope": write_scope,
        "write_action": write_action,
        "claim_result_pending": bool(args.claim_result_pending),
        "claim_wait_action": claim_wait_action,
        "claim_wait_seconds": claim_wait_seconds,
        "fallback_writable": fallback_writable,
        "durable_transport_available": any_durable_transport,
        "independent_work_after_fallback": independent_work,
        "seconds_to_run_deadline": seconds_to_deadline,
        "seconds_to_next_scheduled_task": seconds_to_next,
        "effective_seconds_to_handoff": effective_seconds_to_handoff,
        "handoff_time_source": handoff_time_source,
        "scheduled_handoff_guard_seconds": handoff_guard,
        "scheduled_handoff_active": time_handoff_active,
        "rule": (
            "Normal finalization is time-only: the actual-invocation-start run deadline handoff "
            "guard (or legacy schedule fallback when no deadline is supplied) is the sole normal "
            "STOP_RUN trigger. Discovery quotas, exhaustion, candidate counts, duplicate-only "
            "rounds, completed jobs, and backlog shape cannot end a run. Read/durability/platform "
            "failures are abnormal blockers and do not authorize normal finalization."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--github-read", type=yn, default=True)
    ap.add_argument("--github-write", type=yn, default=True)
    ap.add_argument("--library-writable", type=yn, default=False)
    ap.add_argument("--result-durable", type=yn, default=True)
    ap.add_argument("--seed-durable", type=yn, default=True)
    ap.add_argument("--unpublished-completed-result", type=yn, default=False)
    ap.add_argument("--offline-seed-required", type=yn, default=False)
    ap.add_argument("--platform-limit", type=yn, default=False)
    ap.add_argument("--global-dependency", type=yn, default=False)
    ap.add_argument("--independent-work", type=yn, default=True)
    ap.add_argument("--spillover-work", type=yn, default=False)
    ap.add_argument("--can-discover", type=yn, default=True)
    ap.add_argument("--claim-result-pending", type=yn, default=False)
    ap.add_argument("--write-failed", type=yn, default=False)
    ap.add_argument("--probe", choices=("success", "failure", "not-run"), default="not-run")
    ap.add_argument("--seconds-to-run-deadline", type=int, default=None)
    ap.add_argument("--seconds-to-next-scheduled-task", type=int, default=None)
    ap.add_argument("--scheduled-handoff-guard-seconds", type=int, default=600)
    ap.add_argument("--worker-kind", choices=("normal", "discovery"), default="normal")
    # Deprecated quota/exhaustion arguments remain accepted for compatibility but do not stop runs.
    ap.add_argument("--discovery-rounds-completed", type=int, default=0)
    ap.add_argument("--discovery-rounds-since-last-novel", type=int, default=None)
    ap.add_argument("--discovery-min-rounds", type=int, default=None)
    ap.add_argument("--discovery-exhausted", type=yn, default=False)
    ap.add_argument("--next-axis-available", type=yn, default=False)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
