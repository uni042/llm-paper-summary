#!/usr/bin/env python3
"""Deterministic final-response gate for Scheduled Chat survey workers.

This gate is intentionally separate from continuation_gate.py. The continuation
policy decides whether the run should continue; this finalization gate decides
whether the worker may emit a normal final response.

Normal finalization is reserved for the time handoff emitted by
continuation_gate.py. Non-time hard failures are abnormal blockers: even after a
safe durable handoff they must not be converted into a successful finalization
permit. Pending asynchronous results retain the fixed 30-second recheck loop.
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
    continuation_decision = str(args.continuation_decision).strip().upper()
    finalization_allowed = bool(args.continuation_finalization_allowed)
    active_assignment = bool(args.active_assignment)
    active_assignment_handoff_safe = bool(args.active_assignment_handoff_safe)
    hard_stop = bool(args.hard_stop)
    handoff_safe = bool(args.handoff_safe)

    pending = {
        "claim_result": bool(args.claim_result_pending),
        "submission_result": bool(args.submission_result_pending),
        "ack_result": bool(args.ack_result_pending),
    }
    wait_targets = [name for name, is_pending in pending.items() if is_pending]
    blocking_reasons: list[str] = []

    if continuation_decision != "STOP_RUN":
        blocking_reasons.append("continuation_decision_is_continue")
    if not finalization_allowed:
        blocking_reasons.append("continuation_gate_did_not_allow_finalization")

    # Hard-stop is reserved for abnormal failure signalling. A safe handoff protects
    # data but does not transform the failure into a successful normal completion.
    if hard_stop:
        blocking_reasons.append("non_time_hard_stop_is_abnormal")
        if not handoff_safe:
            blocking_reasons.append("hard_stop_handoff_not_safe")

    if active_assignment and not (hard_stop and handoff_safe and active_assignment_handoff_safe):
        blocking_reasons.append("active_assignment_requires_work")

    pending_blocks = bool(wait_targets) and not (hard_stop and handoff_safe)
    if pending_blocks:
        blocking_reasons.extend(f"{target}_pending" for target in wait_targets)

    permit = not blocking_reasons
    if permit:
        decision = "MAY_FINALIZE"
        next_action = "FINALIZE"
        wait_seconds = 0
    else:
        decision = "MUST_CONTINUE"
        if hard_stop:
            next_action = "REPORT_OR_RECOVER_ABNORMAL_BLOCKER_WITHOUT_NORMAL_FINALIZATION"
            wait_seconds = 0
        elif wait_targets:
            next_action = "WAIT_30_SECONDS_AND_RECHECK"
            wait_seconds = 30
        elif active_assignment:
            next_action = "CONTINUE_ASSIGNED_WORK"
            wait_seconds = 0
        else:
            next_action = "CONTINUE_WORK"
            wait_seconds = 0

    return {
        "decision": decision,
        "finalization_permit": {
            "issued": permit,
            "required_for_final_response": True,
        },
        "blocking_reasons": blocking_reasons,
        "next_action": next_action,
        "wait_seconds": wait_seconds,
        "wait_targets": wait_targets,
        "continuation_decision": continuation_decision,
        "continuation_finalization_allowed": finalization_allowed,
        "active_assignment": active_assignment,
        "active_assignment_handoff_safe": active_assignment_handoff_safe,
        "hard_stop": hard_stop,
        "handoff_safe": handoff_safe,
        "rule": (
            "A normal final response requires a time-driven STOP_RUN from continuation_gate plus "
            "no active assignment or pending result. Non-time hard failures remain abnormal and "
            "never receive a normal finalization permit, even after safe durable handoff."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--continuation-decision", choices=("CONTINUE", "STOP_RUN"), required=True)
    ap.add_argument("--continuation-finalization-allowed", type=yn, required=True)
    ap.add_argument("--active-assignment", type=yn, default=False)
    ap.add_argument("--active-assignment-handoff-safe", type=yn, default=False)
    ap.add_argument("--claim-result-pending", type=yn, default=False)
    ap.add_argument("--submission-result-pending", type=yn, default=False)
    ap.add_argument("--ack-result-pending", type=yn, default=False)
    ap.add_argument("--hard-stop", type=yn, default=False)
    ap.add_argument("--handoff-safe", type=yn, default=False)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
