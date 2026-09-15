#!/usr/bin/env python3
"""Deterministic stop/continue gate for Scheduled Chat survey workers.

The gate decides whether the whole run may stop and, for the discovery-specialist
worker, whether the next action must be another discovery round. Transport
backlogs, claim-result propagation delay, and job-local failures are not stop
conditions when repository state remains readable and no explicit hard condition
holds.
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
    reasons: list[str] = []
    fallback_writable = bool(args.library_writable)
    any_durable_transport = bool(args.github_write or fallback_writable)

    worker_kind = str(getattr(args, "worker_kind", "normal") or "normal").strip().lower()
    discovery_rounds_completed = max(int(getattr(args, "discovery_rounds_completed", 0) or 0), 0)
    discovery_min_rounds = max(int(getattr(args, "discovery_min_rounds", 4) or 4), 1)
    discovery_exhausted = bool(getattr(args, "discovery_exhausted", False))
    next_axis_available = bool(getattr(args, "next_axis_available", False))
    minimum_rounds_remaining = max(discovery_min_rounds - discovery_rounds_completed, 0)

    if args.platform_limit:
        reasons.append("platform_limit_reached")

    seconds_to_next = getattr(args, "seconds_to_next_scheduled_task", None)
    handoff_guard = int(getattr(args, "scheduled_handoff_guard_seconds", 600))
    if seconds_to_next is not None and int(seconds_to_next) <= handoff_guard:
        reasons.append("next_scheduled_task_within_handoff_guard")

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

    # A freshly written claim request whose matching result has not propagated
    # yet is a transient synchronization state, not proof that all remaining
    # work is globally blocked. Keep the run alive so the same request/result
    # pair can be re-read. A second claim request must not be issued meanwhile.
    transient_claim_wait = bool(args.claim_result_pending and args.github_read)
    if args.global_dependency and not independent_work and not transient_claim_wait:
        reasons.append("all_remaining_work_blocked_after_fallback_consideration")

    # Discovery-specialist runs have an explicit progression floor. This is not
    # a quota or an automatic stop at N rounds: it only prevents the model from
    # treating one durable submission as completion. Hard stop reasons above
    # always win (handoff guard, platform limit, unreadable canonical state,
    # or inability to durably preserve required work).
    hard_stop = bool(reasons)
    if worker_kind == "discovery" and not hard_stop:
        if discovery_rounds_completed < discovery_min_rounds:
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
        decision = "STOP_RUN" if reasons else "CONTINUE"
        required_action = "FINALIZE" if decision == "STOP_RUN" else "CONTINUE_WORK"
        finalization_allowed = decision == "STOP_RUN"

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
    if transient_claim_wait:
        claim_wait_action = (
            "keep_same_request_id; do_not_issue_another_claim; refresh_latest_head_and_"
            "matching_claim_result; if_available_check_survey_claim_fast_until_terminal"
        )

    return {
        "decision": decision,
        "required_action": required_action,
        "finalization_allowed": finalization_allowed,
        "stop_reasons": reasons,
        "worker_kind": worker_kind,
        "discovery_rounds_completed": discovery_rounds_completed,
        "discovery_min_rounds": discovery_min_rounds,
        "minimum_rounds_remaining": minimum_rounds_remaining,
        "discovery_exhausted": discovery_exhausted,
        "next_axis_available": next_axis_available,
        "write_failure_scope": write_scope,
        "write_action": write_action,
        "claim_result_pending": bool(args.claim_result_pending),
        "claim_wait_action": claim_wait_action,
        "fallback_writable": fallback_writable,
        "durable_transport_available": any_durable_transport,
        "independent_work_after_fallback": independent_work,
        "seconds_to_next_scheduled_task": seconds_to_next,
        "scheduled_handoff_guard_seconds": handoff_guard,
        "scheduled_handoff_active": bool(
            seconds_to_next is not None and int(seconds_to_next) <= handoff_guard
        ),
        "rule": (
            "A single transport failure, pending claim result, pending backlog, bank exhaustion, "
            "or discovery submission is never by itself a whole-run stop condition. Discovery "
            "specialist runs must satisfy their minimum progression floor before exhaustion can "
            "be a voluntary stop reason; hard handoff/platform/durability/read failures override "
            "that floor."
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
    ap.add_argument("--seconds-to-next-scheduled-task", type=int, default=None)
    ap.add_argument("--scheduled-handoff-guard-seconds", type=int, default=600)
    ap.add_argument("--worker-kind", choices=("normal", "discovery"), default="normal")
    ap.add_argument("--discovery-rounds-completed", type=int, default=0)
    ap.add_argument("--discovery-min-rounds", type=int, default=4)
    ap.add_argument("--discovery-exhausted", type=yn, default=False)
    ap.add_argument("--next-axis-available", type=yn, default=False)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
