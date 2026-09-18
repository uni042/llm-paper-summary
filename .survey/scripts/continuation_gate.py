#!/usr/bin/env python3
"""Deterministic stop/continue gate for Scheduled Chat survey workers.

The gate decides whether the whole run may stop and, for the discovery-specialist
worker, whether the next action must be another discovery round. Transport
backlogs, claim-result propagation delay, and job-local failures are not stop
conditions when repository state remains readable and no explicit hard condition
holds.

Hourly Scheduled Chat workers use a one-hour run window measured from the actual
invocation start. The nominal :00/:30 schedule boundary is retained only as a
compatibility fallback when a caller cannot provide the actual-start deadline.
"""
from __future__ import annotations

import argparse
import json


ASYNC_WAIT_POLL_SECONDS = 10


def yn(value: str) -> bool:
    value = value.strip().lower()
    if value in {"yes", "y", "true", "1"}:
        return True
    if value in {"no", "n", "false", "0"}:
        return False
    raise argparse.ArgumentTypeError("expected yes/no")


def decide(args: argparse.Namespace) -> dict[str, object]:
    reasons: list[str] = []
    fallback_writable = bool(args.library_writable)
    any_durable_transport = bool(args.github_write or fallback_writable)

    worker_kind = str(getattr(args, "worker_kind", "normal") or "normal").strip().lower()
    claim_state_checked = bool(getattr(args, "claim_state_checked", False) or getattr(args, "claim_result_pending", False))
    discovery_rounds_completed = max(int(getattr(args, "discovery_rounds_completed", 0) or 0), 0)
    rounds_since_last_novel_raw = getattr(args, "discovery_rounds_since_last_novel", None)
    discovery_reset_progress_known = rounds_since_last_novel_raw is not None
    discovery_rounds_since_last_novel = (
        max(int(rounds_since_last_novel_raw or 0), 0)
        if discovery_reset_progress_known
        else 0
    )
    discovery_min_rounds = max(int(getattr(args, "discovery_min_rounds", 4) or 4), 1)
    discovery_exhausted = bool(getattr(args, "discovery_exhausted", False))
    next_axis_available = bool(getattr(args, "next_axis_available", False))
    minimum_rounds_remaining = max(discovery_min_rounds - discovery_rounds_since_last_novel, 0)

    if args.platform_limit:
        reasons.append("platform_limit_reached")

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

    if (
        effective_seconds_to_handoff is not None
        and effective_seconds_to_handoff <= handoff_guard
        and handoff_reason is not None
    ):
        reasons.append(handoff_reason)

    if not args.github_read:
        reasons.append("github_read_unavailable_for_repo_state")

    if args.unpublished_completed_result:
        durable = bool(args.result_durable or any_durable_transport)
        if not durable:
            reasons.append("completed_result_not_durably_preserved")

    if args.offline_seed_required:
        seed_durable = bool(args.seed_durable or any_durable_transport)
        if not seed_durable:
            reasons.append("required_spillover_seed_not_durably_preserved")

    independent_work = bool(
        args.independent_work
        or args.spillover_work
        or (args.can_discover and any_durable_transport)
    )

    transient_claim_wait = bool(claim_state_checked and args.claim_result_pending and args.github_read)
    if args.global_dependency and not independent_work and not transient_claim_wait:
        reasons.append("all_remaining_work_blocked_after_fallback_consideration")

    hard_stop = bool(reasons)
    if worker_kind == "discovery" and not hard_stop:
        if not discovery_reset_progress_known or discovery_rounds_since_last_novel < discovery_min_rounds:
            decision = "CONTINUE"
            required_action = "DISCOVER_AGAIN"
            finalization_allowed = False
        elif discovery_exhausted and not next_axis_available and not independent_work:
            reasons.append("discovery_exhausted_after_minimum_rounds")
            decision = "STOP_RUN"
            required_action = "FINALIZE"
            finalization_allowed = True
        else:
            decision = "CONTINUE"
            required_action = "DISCOVER_AGAIN" if (next_axis_available or args.can_discover) else "REFRESH_AND_CONTINUE"
            finalization_allowed = False
    else:
        if reasons:
            decision = "STOP_RUN"
            required_action = "FINALIZE"
            finalization_allowed = True
        elif not claim_state_checked:
            decision = "CONTINUE"
            required_action = "CHECK_CLAIM_STATE"
            finalization_allowed = False
        elif transient_claim_wait:
            decision = "CONTINUE"
            required_action = "WAIT_FOR_CLAIM_RESULT"
            finalization_allowed = False
        else:
            decision = "CONTINUE"
            required_action = "CONTINUE_WORK"
            finalization_allowed = False

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
                write_action = "disable_further_github_writes_this_run; do_not_start_uncheckpointable_new_work"
        else:
            write_scope = "unclassified"
            write_action = "run_fixed_health_probe_once_before_classifying"

    claim_wait_action = "none"
    claim_wait_seconds = 0
    if transient_claim_wait:
        claim_wait_seconds = ASYNC_WAIT_POLL_SECONDS
        claim_wait_action = (
            "keep_same_request_id; do_not_issue_another_claim; wait_10_real_seconds; "
            "refresh_latest_head_and_matching_claim_result; if_available_check_survey_claim_fast; "
            "if_result_still_pending_wait_10_real_seconds_again; repeat_until_result_or_terminal_hard_stop"
        )

    return {
        "decision": decision,
        "required_action": required_action,
        "finalization_allowed": finalization_allowed,
        "stop_reasons": reasons,
        "worker_kind": worker_kind,
        "discovery_rounds_completed": discovery_rounds_completed,
        "discovery_rounds_since_last_novel": discovery_rounds_since_last_novel,
        "discovery_reset_progress_known": discovery_reset_progress_known,
        "discovery_min_rounds": discovery_min_rounds,
        "minimum_rounds_remaining": minimum_rounds_remaining,
        "discovery_exhausted": discovery_exhausted,
        "next_axis_available": next_axis_available,
        "write_failure_scope": write_scope,
        "write_action": write_action,
        "claim_state_checked": claim_state_checked,
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
        "scheduled_handoff_active": bool(
            effective_seconds_to_handoff is not None
            and effective_seconds_to_handoff <= handoff_guard
        ),
        "rule": (
            "A single transport failure, pending claim result, pending backlog, bank exhaustion, "
            "or discovery submission is never by itself a whole-run stop condition. Normal workers "
            "must explicitly confirm the latest claim state before ordinary work/finalization. Required "
            "claim results are polled every 10 real seconds using the same request identity until "
            "terminal or a canonical hard stop. Hourly Scheduled Chat workers prefer an actual-"
            "invocation-start + 3600 second run deadline over the nominal schedule boundary. "
            "Discovery specialist runs may use exhaustion as a voluntary stop reason only when "
            "reset-aware progress since the latest novel candidate is explicitly supplied and "
            "satisfies the minimum progression floor; hard handoff/platform/durability/read "
            "failures override that floor."
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
    ap.add_argument("--claim-state-checked", type=yn, default=False)
    ap.add_argument("--claim-result-pending", type=yn, default=False)
    ap.add_argument("--write-failed", type=yn, default=False)
    ap.add_argument("--probe", choices=("success", "failure", "not-run"), default="not-run")
    ap.add_argument("--seconds-to-run-deadline", type=int, default=None)
    ap.add_argument("--seconds-to-next-scheduled-task", type=int, default=None)
    ap.add_argument("--scheduled-handoff-guard-seconds", type=int, default=600)
    ap.add_argument("--worker-kind", choices=("normal", "discovery"), default="normal")
    ap.add_argument("--discovery-rounds-completed", type=int, default=0)
    ap.add_argument("--discovery-rounds-since-last-novel", type=int, default=None)
    ap.add_argument("--discovery-min-rounds", type=int, default=4)
    ap.add_argument("--discovery-exhausted", type=yn, default=False)
    ap.add_argument("--next-axis-available", type=yn, default=False)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
