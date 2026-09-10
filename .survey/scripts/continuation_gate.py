#!/usr/bin/env python3
"""Deterministic stop/continue gate for the Scheduled Chat survey worker.

The gate decides only whether the whole run may stop. Transport backlogs and
job-local failures are not stop conditions when independent work can continue
and required state can be durably checkpointed in GitHub or ChatGPT Library.
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

    if args.platform_limit:
        reasons.append("platform_limit_reached")
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
    if args.global_dependency and not independent_work:
        reasons.append("all_remaining_work_blocked_after_fallback_consideration")

    decision = "STOP_RUN" if reasons else "CONTINUE"

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

    return {
        "decision": decision,
        "stop_reasons": reasons,
        "write_failure_scope": write_scope,
        "write_action": write_action,
        "fallback_writable": fallback_writable,
        "durable_transport_available": any_durable_transport,
        "independent_work_after_fallback": independent_work,
        "rule": "A single transport failure, pending backlog, or bank exhaustion is never by itself a whole-run stop condition.",
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
    ap.add_argument("--write-failed", type=yn, default=False)
    ap.add_argument("--probe", choices=("success", "failure", "not-run"), default="not-run")
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
