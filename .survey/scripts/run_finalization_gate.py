#!/usr/bin/env python3
"""Deterministic final-response gate for Scheduled Chat survey workers.

This gate is intentionally separate from continuation_gate.py.  The continuation
policy decides whether the run should continue; this finalization gate decides
whether the worker is permitted to emit its final response at all.

A normal run receives a permit only after continuation_gate has returned
STOP_RUN with finalization_allowed=true and no active assignment or asynchronous
result remains. Explicit hard stops may finalize only after the caller has
confirmed a safe durable handoff. Pending asynchronous results expose a fixed
10-second real-time polling interval and must be rechecked until terminal so
callers cannot replace deterministic waiting with ad-hoc early termination.
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
    continuation_decision = str(args.continuation_decision).strip().upper()
    finalization_allowed = bool(args.continuation_finalization_allowed)
    active_assignment = bool(args.active_assignment)
    active_assignment_handoff_safe = bool(args.active_assignment_handoff_safe)
    claim_state_checked = bool(getattr(args, "claim_state_checked", False) or getattr(args, "claim_result_pending", False))
    submission_state_checked = bool(
        getattr(args, "submission_state_checked", False)
        or getattr(args, "submission_result_pending", False)
    )
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

    if not claim_state_checked and not (hard_stop and handoff_safe):
        blocking_reasons.append("claim_state_not_checked")
    if not submission_state_checked and not (hard_stop and handoff_safe):
        blocking_reasons.append("submission_state_not_checked")

    if active_assignment and not (hard_stop and handoff_safe and active_assignment_handoff_safe):
        blocking_reasons.append("active_assignment_requires_work")

    pending_blocks = bool(wait_targets) and not (hard_stop and handoff_safe)
    if pending_blocks:
        blocking_reasons.extend(f"{target}_pending" for target in wait_targets)

    if hard_stop and not handoff_safe:
        blocking_reasons.append("hard_stop_handoff_not_safe")

    permit = not blocking_reasons
    if permit:
        decision = "MAY_FINALIZE"
        next_action = "FINALIZE_AFTER_SAFE_HANDOFF" if hard_stop else "FINALIZE"
        wait_seconds = 0
    else:
        decision = "MUST_CONTINUE"
        if not claim_state_checked and not hard_stop:
            next_action = "CHECK_CLAIM_STATE"
            wait_seconds = 0
        elif not submission_state_checked and not hard_stop:
            next_action = "CHECK_SUBMISSION_STATE"
            wait_seconds = 0
        elif wait_targets and not hard_stop:
            next_action = "WAIT_10_SECONDS_AND_RECHECK"
            wait_seconds = ASYNC_WAIT_POLL_SECONDS
        elif active_assignment:
            next_action = "CONTINUE_ASSIGNED_WORK"
            wait_seconds = 0
        elif hard_stop and not handoff_safe:
            next_action = "COMPLETE_SAFE_HANDOFF_THEN_RECHECK"
            wait_seconds = 0
        else:
            next_action = "CONTINUE_WORK"
            wait_seconds = 0

    if next_action == "CHECK_CLAIM_STATE":
        next_action_message = "最新のclaim request/result対応を確認し、pendingなら同一request_idの待機へ進みます。"
    elif next_action == "CHECK_SUBMISSION_STATE":
        next_action_message = "最新のimmutable descriptorと対応するsubmission result/Actions状態を確認します。"
    elif next_action == "WAIT_10_SECONDS_AND_RECHECK":
        next_action_message = (
            "必要な非同期結果が処理中です。この処理が完了または明示的hard stopになるまで"
            "この処理中はrunを終了しません。同じ対象を10秒ごとに待機・再確認します。"
        )
    elif next_action == "CONTINUE_ASSIGNED_WORK":
        next_action_message = "有効なassignmentの未完了作業を続行し、耐久保存地点まで進めます。"
    elif next_action == "COMPLETE_SAFE_HANDOFF_THEN_RECHECK":
        next_action_message = "hard stopの安全なhandoffを完了し、最終化条件を再確認します。"
    elif next_action == "CONTINUE_WORK":
        next_action_message = "最終化せず、最新canonical stateから次の独立作業を実行します。"
    elif next_action == "FINALIZE_AFTER_SAFE_HANDOFF":
        next_action_message = "安全なhandoffを確認済みのhard stopとして最終化します。"
    else:
        next_action_message = "最終化許可が成立したため通常の最終通知へ進みます。"

    progress_notice = next_action_message if next_action == "WAIT_10_SECONDS_AND_RECHECK" else ""

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
        "claim_state_checked": claim_state_checked,
        "submission_state_checked": submission_state_checked,
        "next_action_message": next_action_message,
        "progress_notice": progress_notice,
        "hard_stop": hard_stop,
        "handoff_safe": handoff_safe,
        "rule": (
            "Final response is forbidden without an issued permit. Normal finalization also requires "
            "explicit checks of the latest claim and submission states. Pending claim/submission/ACK "
            "results require 10-second real-time polling of the same target, repeated until the "
            "required result reaches terminal state or an explicit hard stop is safely handed off."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--continuation-decision", choices=("CONTINUE", "STOP_RUN"), required=True)
    ap.add_argument("--continuation-finalization-allowed", type=yn, required=True)
    ap.add_argument("--active-assignment", type=yn, default=False)
    ap.add_argument("--active-assignment-handoff-safe", type=yn, default=False)
    ap.add_argument("--claim-state-checked", type=yn, default=False)
    ap.add_argument("--claim-result-pending", type=yn, default=False)
    ap.add_argument("--submission-state-checked", type=yn, default=False)
    ap.add_argument("--submission-result-pending", type=yn, default=False)
    ap.add_argument("--ack-result-pending", type=yn, default=False)
    ap.add_argument("--hard-stop", type=yn, default=False)
    ap.add_argument("--handoff-safe", type=yn, default=False)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
