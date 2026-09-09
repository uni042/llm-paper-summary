#!/usr/bin/env python3
"""Deterministic stop/continue gate for the Scheduled Chat survey worker.

This intentionally decides only whether the *whole run* may stop. Job-local
failures must be checkpointed/blocked and the worker should continue with any
independent work.
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

    if args.platform_limit:
        reasons.append("platform_limit_reached")
    if not args.github_read:
        reasons.append("github_read_unavailable_for_repo_state")
    if args.unpublished_completed_result and not args.result_durable:
        reasons.append("completed_result_not_durably_preserved")
    if args.global_dependency and not args.independent_work:
        reasons.append("all_remaining_work_blocked_by_global_dependency")

    decision = "STOP_RUN" if reasons else "CONTINUE"

    write_scope = "none"
    write_action = "normal"
    if args.write_failed:
        if args.probe == "success":
            write_scope = "target_or_payload_specific"
            write_action = "checkpoint_affected_job_then_continue; github_writes_remain_allowed"
        elif args.probe == "failure":
            write_scope = "run_wide_github_write_unavailable"
            write_action = "disable_further_github_writes_this_run; checkpoint_results_then_continue_read_work"
        else:
            write_scope = "unclassified"
            write_action = "run_fixed_health_probe_once_before_classifying"

    return {
        "decision": decision,
        "stop_reasons": reasons,
        "write_failure_scope": write_scope,
        "write_action": write_action,
        "rule": "Job-local failure is never by itself a whole-run stop condition.",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--github-read", type=yn, default=True)
    ap.add_argument("--result-durable", type=yn, default=True)
    ap.add_argument("--unpublished-completed-result", type=yn, default=False)
    ap.add_argument("--platform-limit", type=yn, default=False)
    ap.add_argument("--global-dependency", type=yn, default=False)
    ap.add_argument("--independent-work", type=yn, default=True)
    ap.add_argument("--write-failed", type=yn, default=False)
    ap.add_argument("--probe", choices=("success", "failure", "not-run"), default="not-run")
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
