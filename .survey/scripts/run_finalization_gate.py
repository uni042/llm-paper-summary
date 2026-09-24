#!/usr/bin/env python3
"""Deterministic final-response gate for Scheduled Chat survey workers.

This gate is intentionally separate from continuation_gate.py.  The continuation
policy decides whether the run should continue; this finalization gate decides
whether the worker is permitted to emit its final response at all.

A normal run receives a permit only after continuation_gate has returned
STOP_RUN with finalization_allowed=true and no active assignment or asynchronous
result remains. Explicit hard stops may finalize only after the caller has
confirmed a safe durable handoff. Pending asynchronous results never authorize
an idle sleep loop: the worker must run one bounded wait microtask, then recheck
the same durable target until it becomes terminal or a safe hard-stop handoff applies.
"""
from __future__ import annotations

import argparse
import json

import worker_quota_policy


PRODUCTIVE_WAIT_RECHECK_SECONDS = 0

WAIT_MICROTASKS = (
    "inspect_same_worker_async_transport",
    "lightweight_validate_recent_completed_paper",
    "cleanup_terminal_library_pdf_cache",
    "read_only_queue_consistency_check",
    "organize_current_paper_evidence",
)

FINALIZATION_ACTIONS = frozenset({"FINALIZE", "FINALIZE_AFTER_SAFE_HANDOFF"})


def _assert_finalization_invariants(*, permit: bool, decision: str, next_action: str) -> None:
    """Keep the machine decision, permit, and action mutually consistent.

    Finalization is fail-closed: only an issued permit may produce a finalization
    action. Any future continuation action is therefore non-finalizing by
    default, even before a dedicated human-readable message is added for it.
    """
    if permit:
        if decision != "MAY_FINALIZE":
            raise RuntimeError(
                "finalization invariant violated: issued permit requires MAY_FINALIZE"
            )
        if next_action not in FINALIZATION_ACTIONS:
            raise RuntimeError(
                "finalization invariant violated: issued permit requires a finalization action"
            )
        return

    if decision != "MUST_CONTINUE":
        raise RuntimeError(
            "finalization invariant violated: missing permit requires MUST_CONTINUE"
        )
    if next_action in FINALIZATION_ACTIONS:
        raise RuntimeError(
            "finalization invariant violated: finalization action requires an issued permit"
        )


def _message_for_action(
    *,
    next_action: str,
    permit: bool,
    decision: str,
    pending: dict[str, bool],
) -> str:
    """Render guidance without ever inferring permission from an unknown action."""
    _assert_finalization_invariants(
        permit=permit,
        decision=decision,
        next_action=next_action,
    )

    if permit:
        if next_action == "FINALIZE_AFTER_SAFE_HANDOFF":
            return "安全なhandoffを確認済みのhard stopとして最終化します。"
        return "最終化許可が成立したため通常の最終通知へ進みます。"

    if next_action == "CHECK_CLAIM_STATE":
        return "最新のclaim request/result対応を確認し、pendingなら同一request_idの待機へ進みます。"
    if next_action == "CHECK_SUBMISSION_STATE":
        return "最新のimmutable descriptorと対応するsubmission result/Actions状態を確認します。"
    if next_action == "RUN_WAIT_MICROTASK_AND_RECHECK":
        if pending["claim_result"]:
            return (
                "claim resultが処理中です。sleepや固定間隔pollingは行わず、同じrequestを起動したSurvey claim fast laneの"
                "Actions状態、job/step、同一workerのtransport healthを確認し、待機ミクロタスクを1件処理してから同じrequest_idを再確認します。"
            )
        return (
            "必要な非同期結果が処理中です。runを終了せず、短い待機ミクロタスクを1件処理してから"
            "同じ耐久targetを再確認します。結果がterminalになるまでこの作業サイクルを繰り返します。"
        )
    if next_action == "CONTINUE_ASSIGNED_WORK":
        return "有効なassignmentの未完了作業を続行し、耐久保存地点まで進めます。"
    if next_action == "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY":
        return (
            "foregroundのResearch/Auditを継続しながらstandbyを補充します。"
            "補充結果はforeground作業の同期障壁にせず、現在のassignmentを止めません。"
        )
    if next_action == "RECOVER_DISCOVERY_SUBMISSION":
        return "開始済みDiscovery roundの失敗を正規recovery_stepsで回収し、最終化せず同じroundを完了させます。"
    if next_action == "CONTINUE_DISCOVERY_PIPELINE":
        return (
            "非同期Discovery resultだけを待たず、事前装填済みlookahead roundのcached候補を軽量評価します。"
            "正式precheckが完了するまでsubmissionは行いません。"
        )
    if next_action == "CONTINUE_DISCOVERY_ROUND":
        return "成功済みDiscovery precheckの評価・submissionを完了し、開始済みroundを終端まで進めます。"
    if next_action == "CLAIM_NEXT_RESEARCH_AUDIT":
        return (
            "Research/Auditの最低成功完了数に未達です。最終化せず、最新queue/claim stateから"
            "既確保standbyをforegroundへ昇格し、必要ならclaim windowを補充してResearch/Auditを継続します。本文処理はforeground 1件だけです。"
        )
    if next_action == "WAIT_FOR_READY_RESEARCH_AUDIT":
        return (
            "claim可能なResearch/Auditの再出現を待ちながら待機ミクロタスクを実行し、"
            "最新queueを再確認します。これ自体をrun終了理由にはしません。"
        )
    if next_action == "DISCOVER_AGAIN":
        return "Discoveryの最低ラウンド数に未達です。最終化せず、次の正規Discovery roundへ進みます。"
    if next_action == "RUN_0830_MAINTENANCE":
        return "08:30 maintenanceの未完了作業を続行し、正規の完了条件まで進めます。"
    if next_action == "COMPLETE_SAFE_HANDOFF_THEN_RECHECK":
        return "hard stopの安全なhandoffを完了し、最終化条件を再確認します。"
    if next_action in {"CONTINUE_WORK", "REFRESH_AND_CONTINUE"}:
        return "最終化せず、最新canonical stateから次の独立作業を実行します。"

    return (
        f"最終化許可は発行されていません（next_action={next_action}）。"
        "未知または新規の継続アクションとして安全側に倒し、最新canonical stateに従って作業を継続します。"
    )


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
    work_mode = str(getattr(args, "work_mode", "unknown") or "unknown").strip().lower()
    research_completed = max(
        int(getattr(args, "research_audit_completed_this_invocation", 0) or 0), 0
    )
    research_minimum = max(
        int(getattr(args, "research_minimum_completions", worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS) or worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS), 1
    )
    discovery_completed = max(
        int(getattr(args, "discovery_rounds_completed", 0) or 0), 0
    )
    discovery_minimum = max(
        int(getattr(args, "discovery_min_rounds", worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS) or worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS), 1
    )

    pending = {
        "claim_result": bool(args.claim_result_pending),
        "submission_result": bool(args.submission_result_pending),
        "ack_result": bool(args.ack_result_pending),
        "discovery_precheck_result": bool(getattr(args, "discovery_precheck_result_pending", False)),
        "discovery_submission_result": bool(getattr(args, "discovery_submission_result_pending", False)),
    }
    discovery_evaluation_pending = bool(getattr(args, "discovery_evaluation_pending", False))
    discovery_recovery_required = bool(getattr(args, "discovery_recovery_required", False))
    discovery_pipeline_work_available = bool(
        getattr(args, "discovery_pipeline_work_available", False)
    )
    continuation_required_action = str(
        getattr(args, "continuation_required_action", "") or ""
    ).strip().upper()
    discovery_round_in_progress = bool(
        pending["discovery_precheck_result"]
        or pending["discovery_submission_result"]
        or discovery_evaluation_pending
        or discovery_recovery_required
    )
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
    if discovery_round_in_progress and not (hard_stop and handoff_safe):
        blocking_reasons.append("discovery_round_in_progress")

    if hard_stop and not handoff_safe:
        blocking_reasons.append("hard_stop_handoff_not_safe")

    if not hard_stop:
        if work_mode == "research" and research_completed < research_minimum:
            blocking_reasons.append("research_minimum_not_met")
        elif work_mode == "discovery" and discovery_completed < discovery_minimum:
            blocking_reasons.append("discovery_minimum_not_met")

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
        elif (
            continuation_required_action
            in {
                "RECOVER_DISCOVERY_SUBMISSION",
                "CONTINUE_DISCOVERY_ROUND",
                "CONTINUE_DISCOVERY_PIPELINE",
                "CONTINUE_ASSIGNED_WORK",
                "CONTINUE_ASSIGNED_WORK_AND_REFILL_STANDBY",
                "CLAIM_NEXT_RESEARCH_AUDIT",
                "WAIT_FOR_READY_RESEARCH_AUDIT",
                "DISCOVER_AGAIN",
                "RUN_0830_MAINTENANCE",
            }
            and not hard_stop
        ):
            next_action = continuation_required_action
            wait_seconds = 0
        elif (
            discovery_pipeline_work_available
            and work_mode == "discovery"
            and wait_targets
            and not hard_stop
        ):
            next_action = "CONTINUE_DISCOVERY_PIPELINE"
            wait_seconds = 0
        elif wait_targets and not hard_stop:
            next_action = "RUN_WAIT_MICROTASK_AND_RECHECK"
            wait_seconds = PRODUCTIVE_WAIT_RECHECK_SECONDS
        elif active_assignment:
            next_action = "CONTINUE_ASSIGNED_WORK"
            wait_seconds = 0
        elif discovery_recovery_required:
            next_action = "RECOVER_DISCOVERY_SUBMISSION"
            wait_seconds = 0
        elif discovery_evaluation_pending:
            next_action = "CONTINUE_DISCOVERY_ROUND"
            wait_seconds = 0
        elif "research_minimum_not_met" in blocking_reasons:
            next_action = "CLAIM_NEXT_RESEARCH_AUDIT"
            wait_seconds = 0
        elif "discovery_minimum_not_met" in blocking_reasons:
            next_action = "DISCOVER_AGAIN"
            wait_seconds = 0
        elif hard_stop and not handoff_safe:
            next_action = "COMPLETE_SAFE_HANDOFF_THEN_RECHECK"
            wait_seconds = 0
        else:
            next_action = "CONTINUE_WORK"
            wait_seconds = 0

    next_action_message = _message_for_action(
        next_action=next_action,
        permit=permit,
        decision=decision,
        pending=pending,
    )

    progress_notice = next_action_message if next_action == "RUN_WAIT_MICROTASK_AND_RECHECK" else ""
    productive_wait_required = bool(next_action == "RUN_WAIT_MICROTASK_AND_RECHECK")

    return {
        "decision": decision,
        "finalization_permit": {
            "issued": permit,
        },
        "blocking_reasons": blocking_reasons,
        "next_action": next_action,
        "wait_seconds": wait_seconds,
        "wait_targets": wait_targets,
        "productive_wait_required": productive_wait_required,
        "productive_wait_polling": False,
        "productive_wait_recheck_after_each_task": productive_wait_required,
        "wait_microtasks": list(WAIT_MICROTASKS) if productive_wait_required else [],
        "continuation_decision": continuation_decision,
        "continuation_finalization_allowed": finalization_allowed,
        "active_assignment": active_assignment,
        "active_assignment_handoff_safe": active_assignment_handoff_safe,
        "claim_state_checked": claim_state_checked,
        "submission_state_checked": submission_state_checked,
        "discovery_precheck_result_pending": pending["discovery_precheck_result"],
        "discovery_submission_result_pending": pending["discovery_submission_result"],
        "discovery_evaluation_pending": discovery_evaluation_pending,
        "discovery_recovery_required": discovery_recovery_required,
        "discovery_pipeline_work_available": discovery_pipeline_work_available,
        "continuation_required_action": continuation_required_action,
        "discovery_round_in_progress": discovery_round_in_progress,
        "next_action_message": next_action_message,
        "progress_notice": progress_notice,
        "hard_stop": hard_stop,
        "handoff_safe": handoff_safe,
        "work_mode": work_mode,
        "research_audit_completed_this_invocation": research_completed,
        "research_minimum_completions": research_minimum,
        "discovery_rounds_completed": discovery_completed,
        "discovery_min_rounds": discovery_minimum,
        "rule": (
            "The permit controls run finalization only; it does not suppress user-facing reports. Normal finalization requires "
            "explicit checks of the latest claim and submission states. Pending claim/submission/ACK/Discovery precheck/Discovery submission "
            "results require a productive wait loop: run one bounded wait microtask and recheck the same durable target, with no fixed sleep or polling interval, until the "
            "required result reaches terminal state or an explicit hard stop is safely handed off. "
            "Pending claim results also require fast-lane monitoring (Actions/job/step and same-worker transport health) as part of that productive loop. "
            "handoff_safe may be true for a pending asynchronous result only after the durable request/submission identity, "
            "expected result path, current pending state, and exact next canonical action have been preserved for the next run. "
            "As defense in depth, normal Research/Audit finalization is independently refused while "
            f"the {research_minimum}-success floor is unmet, and normal Discovery finalization is refused while "
            f"the {discovery_minimum}-round floor is unmet, even if an incorrect STOP_RUN is supplied."
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
    ap.add_argument("--discovery-precheck-result-pending", type=yn, default=False)
    ap.add_argument("--discovery-submission-result-pending", type=yn, default=False)
    ap.add_argument("--discovery-evaluation-pending", type=yn, default=False)
    ap.add_argument("--discovery-recovery-required", type=yn, default=False)
    ap.add_argument("--discovery-pipeline-work-available", type=yn, default=False)
    ap.add_argument("--continuation-required-action", default="")
    ap.add_argument("--hard-stop", type=yn, default=False)
    ap.add_argument("--handoff-safe", type=yn, default=False)
    ap.add_argument(
        "--work-mode",
        choices=("unknown", "research", "discovery", "maintenance"),
        default="unknown",
    )
    ap.add_argument("--research-audit-completed-this-invocation", type=int, default=0)
    ap.add_argument("--research-minimum-completions", type=int, default=worker_quota_policy.RESEARCH_AUDIT_MINIMUM_COMPLETIONS)
    ap.add_argument("--discovery-rounds-completed", type=int, default=0)
    ap.add_argument("--discovery-min-rounds", type=int, default=worker_quota_policy.DISCOVERY_MINIMUM_ROUNDS)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
