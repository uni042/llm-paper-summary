#!/usr/bin/env python3
"""Deterministic stop/continue gate for Scheduled Chat survey workers.

The gate decides whether the whole run may stop for the common hourly paper
worker. The :00 and :30 schedules are identical. When candidate_inventory is
provided, the run-start candidate_inventory >= 50 selects Research/Audit and
candidate_inventory < 50 selects Discovery. The selected mode is frozen for the run;
callers must reuse the run-start routing value or pass the explicit work_mode on later checks. Existing per-mode quotas remain progression floors.
Transport backlogs, claim-result propagation delay, and job-local failures are not
stop conditions when repository state remains readable and no explicit hard
condition holds.

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

    candidate_inventory_raw = getattr(args, "candidate_inventory", None)
    candidate_inventory = (
        max(int(candidate_inventory_raw), 0)
        if candidate_inventory_raw is not None
        else None
    )
    explicit_work_mode = str(getattr(args, "work_mode", "auto") or "auto").strip().lower()
    if explicit_work_mode == "auto":
        if candidate_inventory is None:
            raise ValueError(
                "candidate_inventory is required when work_mode=auto; "
                "schedule labels and legacy worker kinds are not routing inputs"
            )
        work_mode = "research" if candidate_inventory >= 50 else "discovery"
        mode_source = "candidate_inventory"
    else:
        work_mode = explicit_work_mode
        mode_source = "explicit_work_mode"
    research_audit_completed_this_invocation = max(
        int(getattr(args, "research_audit_completed_this_invocation", 0) or 0),
        0,
    )
    research_minimum_completions = max(
        int(getattr(args, "research_minimum_completions", 3) or 3),
        1,
    )
    last_terminal_job_status = str(
        getattr(args, "last_terminal_job_status", "none") or "none"
    ).strip().lower()
    status_only_terminal = last_terminal_job_status in {"blocked", "deferred", "rejected"}
    claim_state_checked = bool(getattr(args, "claim_state_checked", False) or getattr(args, "claim_result_pending", False))
    submission_state_checked = bool(
        getattr(args, "submission_state_checked", False)
        or getattr(args, "submission_result_pending", False)
    )
    discovery_rounds_completed = max(int(getattr(args, "discovery_rounds_completed", 0) or 0), 0)
    discovery_min_rounds = max(int(getattr(args, "discovery_min_rounds", 4) or 4), 1)
    discovery_exhausted = bool(getattr(args, "discovery_exhausted", False))
    next_axis_available = bool(getattr(args, "next_axis_available", False))
    minimum_rounds_remaining = max(discovery_min_rounds - discovery_rounds_completed, 0)

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

    handoff_window_active = bool(
        effective_seconds_to_handoff is not None
        and effective_seconds_to_handoff <= handoff_guard
    )
    final_handoff_active = bool(
        effective_seconds_to_handoff is not None
        and effective_seconds_to_handoff <= 180
    )
    if final_handoff_active and handoff_reason is not None:
        reasons.append("run_deadline_within_final_180_second_handoff_guard")

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
        or (
            work_mode == "discovery"
            and args.can_discover
            and any_durable_transport
        )
    )
    active_assignment = bool(getattr(args, "active_assignment", False))

    transient_claim_wait = bool(claim_state_checked and args.claim_result_pending and args.github_read)
    claim_result_pending_age_seconds = max(
        int(getattr(args, "claim_result_pending_age_seconds", 0) or 0),
        0,
    )
    claim_monitor_window_seconds = max(
        int(getattr(args, "claim_monitor_window_seconds", 60) or 60),
        ASYNC_WAIT_POLL_SECONDS,
    )
    transient_submission_wait = bool(
        submission_state_checked
        and getattr(args, "submission_result_pending", False)
        and args.github_read
    )
    pipeline_ahead_count = max(int(getattr(args, "pipeline_ahead_count", 0) or 0), 0)
    discovery_precheck_result_pending = bool(getattr(args, "discovery_precheck_result_pending", False))
    discovery_submission_result_pending = bool(getattr(args, "discovery_submission_result_pending", False))
    discovery_evaluation_pending = bool(getattr(args, "discovery_evaluation_pending", False))
    discovery_recovery_required = bool(getattr(args, "discovery_recovery_required", False))
    discovery_round_in_progress = bool(
        discovery_precheck_result_pending
        or discovery_submission_result_pending
        or discovery_evaluation_pending
        or discovery_recovery_required
    )
    if (
        args.global_dependency
        and not independent_work
        and not transient_claim_wait
        and not transient_submission_wait
        and not discovery_round_in_progress
    ):
        reasons.append("all_remaining_work_blocked_after_fallback_consideration")

    hard_stop = bool(reasons)
    if reasons:
        decision = "STOP_RUN"
        required_action = "FINALIZE"
        finalization_allowed = True
    elif work_mode == "discovery":
        if discovery_precheck_result_pending:
            decision = "CONTINUE"
            required_action = "WAIT_FOR_DISCOVERY_PRECHECK_RESULT"
            finalization_allowed = False
        elif discovery_submission_result_pending:
            decision = "CONTINUE"
            required_action = "WAIT_FOR_DISCOVERY_SUBMISSION_RESULT"
            finalization_allowed = False
        elif discovery_recovery_required:
            decision = "CONTINUE"
            required_action = "RECOVER_DISCOVERY_SUBMISSION"
            finalization_allowed = False
        elif discovery_evaluation_pending:
            decision = "CONTINUE"
            required_action = "CONTINUE_DISCOVERY_ROUND"
            finalization_allowed = False
        elif handoff_window_active:
            reasons.append(handoff_reason or "handoff_window_no_new_discovery_round")
            reasons.append("handoff_window_no_new_discovery_round")
            decision = "STOP_RUN"
            required_action = "FINALIZE"
            finalization_allowed = True
        elif discovery_rounds_completed < discovery_min_rounds:
            decision = "CONTINUE"
            required_action = "DISCOVER_AGAIN"
            finalization_allowed = False
        else:
            decision = "CONTINUE"
            required_action = "DISCOVER_AGAIN" if (next_axis_available or args.can_discover) else "REFRESH_AND_CONTINUE"
            finalization_allowed = False
    else:
        if not claim_state_checked:
            decision = "CONTINUE"
            required_action = "CHECK_CLAIM_STATE"
            finalization_allowed = False
        elif transient_claim_wait:
            decision = "CONTINUE"
            required_action = (
                "MONITOR_CLAIM_FAST_LANE"
                if claim_result_pending_age_seconds < claim_monitor_window_seconds
                else "WAIT_FOR_CLAIM_RESULT"
            )
            finalization_allowed = False
        elif not submission_state_checked:
            decision = "CONTINUE"
            required_action = "CHECK_SUBMISSION_STATE"
            finalization_allowed = False
        elif transient_submission_wait:
            if handoff_window_active or pipeline_ahead_count >= 1 or not independent_work:
                decision = "CONTINUE"
                required_action = "WAIT_FOR_PREVIOUS_SUBMISSION_RESULT"
                finalization_allowed = False
            else:
                decision = "CONTINUE"
                required_action = "CLAIM_NEXT_RESEARCH_AUDIT"
                finalization_allowed = False
        elif active_assignment:
            decision = "CONTINUE"
            required_action = "CONTINUE_ASSIGNED_WORK"
            finalization_allowed = False
        elif handoff_window_active:
            reasons.append(handoff_reason or "handoff_window_no_new_research_audit_claim")
            reasons.append("handoff_window_no_new_research_audit_claim")
            decision = "STOP_RUN"
            required_action = "FINALIZE"
            finalization_allowed = True
        elif not independent_work:
            decision = "CONTINUE"
            required_action = "WAIT_FOR_READY_RESEARCH_AUDIT"
            finalization_allowed = False
        elif status_only_terminal or research_audit_completed_this_invocation < research_minimum_completions:
            decision = "CONTINUE"
            required_action = "CLAIM_NEXT_RESEARCH_AUDIT"
            finalization_allowed = False
        else:
            decision = "CONTINUE"
            required_action = "CONTINUE_WORK"
            finalization_allowed = False

    # Reasons added by the 600-second start-prohibition branch are canonical hard
    # stop reasons too. Recompute after routing so finalization sees the same state
    # that worker-router.md defines.
    hard_stop = bool(reasons)

    write_scope = "none"
    write_action = "normal"
    if args.write_failed:
        if args.probe == "success":
            write_scope = "target_or_payload_specific"
            write_action = "checkpoint_affected_job_via_library_if_needed_then_continue; github_writes_remain_allowed"
        elif args.probe == "failure":
            write_scope = "run_wide_github_write_unavailable"
            if fallback_writable:
                if work_mode == "research":
                    write_action = (
                        "disable_further_github_writes_this_run; checkpoint_current_assignment_to_library; "
                        "do_not_start_next_paper; keep_scheduled_task_enabled"
                    )
                else:
                    write_action = (
                        "disable_further_github_writes_this_run; checkpoint_current_discovery_payload_to_library; "
                        "continue_only_work_that_can_be_durably_preserved_without_bypassing_precheck; "
                        "keep_scheduled_task_enabled"
                    )
            else:
                write_action = (
                    "disable_further_github_writes_this_run; do_not_start_uncheckpointable_new_work; "
                    "keep_scheduled_task_enabled"
                )
        else:
            write_scope = "unclassified"
            write_action = "run_fixed_health_probe_once_before_classifying"

    claim_wait_action = "none"
    claim_wait_seconds = 0
    if transient_claim_wait:
        claim_wait_seconds = ASYNC_WAIT_POLL_SECONDS
        if required_action == "MONITOR_CLAIM_FAST_LANE":
            claim_wait_action = (
                "keep_same_request_id; do_not_issue_another_claim; inspect_survey_claim_fast_actions_run_for_request_commit; "
                "inspect_run_job_or_steps_if_queued_or_in_progress; inspect_same_worker_unsettled_submissions_retryable_repairs_and_active_claim_consistency; "
                "wait_10_real_seconds; refresh_latest_head_and_matching_claim_result; "
                "repeat_monitor_cycle_while_request_age_under_60_seconds; "
                "repeat_until_result_or_terminal_hard_stop"
            )
        else:
            claim_wait_action = (
                "keep_same_request_id; do_not_issue_another_claim; inspect_survey_claim_fast_actions_status_and_same_worker_transport_health; "
                "wait_10_real_seconds; refresh_latest_head_and_matching_claim_result; "
                "if_actions_failed_or_cancelled_follow_canonical_recovery_without_new_request; "
                "repeat_until_result_or_terminal_hard_stop"
            )

    submission_wait_action = "none"
    submission_wait_seconds = 0
    if required_action == "WAIT_FOR_PREVIOUS_SUBMISSION_RESULT":
        submission_wait_seconds = ASYNC_WAIT_POLL_SECONDS
        submission_wait_action = (
            "keep_same_submission_identity; do_not_duplicate_submission; wait_10_real_seconds; "
            "refresh_latest_head_and_matching_submission_result; if_available_check_survey_submission_fast; "
            "if_result_still_pending_wait_10_real_seconds_again; repeat_until_result_or_terminal_hard_stop"
        )

    discovery_wait_action = "none"
    discovery_wait_seconds = 0
    if required_action == "WAIT_FOR_DISCOVERY_PRECHECK_RESULT":
        discovery_wait_seconds = ASYNC_WAIT_POLL_SECONDS
        discovery_wait_action = (
            "keep_same_discovery_precheck_request; wait_10_real_seconds; refresh_latest_head_and_matching_precheck_result; "
            "periodic_discovery_precheck_recovery_will_reprocess_orphaned_requests; "
            "repeat_until_result_or_final_180_second_handoff"
        )
    elif required_action == "WAIT_FOR_DISCOVERY_SUBMISSION_RESULT":
        discovery_wait_seconds = ASYNC_WAIT_POLL_SECONDS
        discovery_wait_action = (
            "keep_same_discovery_submission; wait_10_real_seconds; refresh_latest_head_and_matching_discovery_result; "
            "periodic_discovery_submission_recovery_will_reprocess_orphaned_submissions; "
            "repeat_until_result_or_final_180_second_handoff"
        )

    progress_notice = ""
    if required_action == "MONITOR_CLAIM_FAST_LANE":
        progress_notice = (
            "担当確保結果の生成待ちです。待機中はSurvey claim fast laneのActions状態、job/step、"
            "同一workerの未解決submission・retryable repair・active claim整合を確認し、"
            "10秒後に最新mainと同じrequest_idのresultを再確認します。60秒未満はこの監視サイクルを継続し、runを終了しません。"
        )
    elif required_action == "WAIT_FOR_CLAIM_RESULT":
        progress_notice = (
            "担当確保結果が60秒以上pendingです。新しいrequestは発行せず、Survey claim fast laneのActions状態と"
            "同一workerのtransport healthを確認してから、同じrequest_idを10秒ごとに再確認します。"
        )
    elif required_action == "WAIT_FOR_PREVIOUS_SUBMISSION_RESULT":
        progress_notice = (
            "1本先行分を提出済みのため、さらに次へ進む前に1本前のsubmission resultを確認します。"
            "pendingなら同じsubmissionを10秒ごとに再確認します。"
        )
    elif required_action == "WAIT_FOR_DISCOVERY_PRECHECK_RESULT":
        progress_notice = (
            "開始済みDiscovery precheckのresultを待っています。残り600秒の開始禁止窓に入っても"
            "このroundは終了させず、最終180秒までは同じrequestを10秒ごとに再確認します。"
        )
    elif required_action == "WAIT_FOR_DISCOVERY_SUBMISSION_RESULT":
        progress_notice = (
            "開始済みDiscovery submissionのresultを待っています。残り600秒の開始禁止窓に入っても"
            "このroundは終了させず、最終180秒までは同じsubmissionを10秒ごとに再確認します。"
        )

    if required_action == "CHECK_CLAIM_STATE":
        next_action_message = "最新のclaim request/result対応を確認し、pendingなら同一request_idの監視サイクルへ進みます。"
    elif required_action in {"MONITOR_CLAIM_FAST_LANE", "WAIT_FOR_CLAIM_RESULT"}:
        next_action_message = progress_notice
    elif required_action == "CHECK_SUBMISSION_STATE":
        next_action_message = "最新のimmutable descriptorと対応するsubmission result/Actions状態を確認します。"
    elif required_action == "WAIT_FOR_PREVIOUS_SUBMISSION_RESULT":
        next_action_message = progress_notice
    elif required_action in {"WAIT_FOR_DISCOVERY_PRECHECK_RESULT", "WAIT_FOR_DISCOVERY_SUBMISSION_RESULT"}:
        next_action_message = progress_notice
    elif required_action == "CONTINUE_DISCOVERY_ROUND":
        next_action_message = "成功済みprecheckの評価・正規Discovery submissionまで、開始済みroundを完了させます。"
    elif required_action == "RECOVER_DISCOVERY_SUBMISSION":
        next_action_message = "失敗済みDiscovery precheck/submissionのrecovery_stepsに従い、同じroundを正規経路へ戻します。"
    elif required_action == "CLAIM_NEXT_RESEARCH_AUDIT":
        if transient_submission_wait and pipeline_ahead_count == 0:
            next_action_message = (
                "直前jobのdescriptorは耐久保存済みです。result待ちを1本だけ先送りし、"
                "最新queue/claim stateを再取得して次のResearch/Auditを1件claimします。"
                "descriptor-backed旧claimがactive表示でも、新claim処理の正規解放に任せます。"
            )
        else:
            next_action_message = (
                "前jobは終端しましたがrunは終了しません。最新queue/claim stateを再取得し、"
                "同一workerの未完了claimがないことを確認して次のResearch/Auditを1件claimします。"
            )
    elif required_action == "CONTINUE_ASSIGNED_WORK":
        next_action_message = "すでに担当確保済みのResearch/Auditを継続し、提出・結果確認または正規repairまで進めます。"
    elif required_action == "WAIT_FOR_READY_RESEARCH_AUDIT":
        next_action_message = "現在claim可能なResearch/Auditが0件です。空のclaim requestを出さず10秒待機し、最新queueを再確認します。run中にDiscoveryへ切り替えません。"
        progress_notice = next_action_message
    elif required_action == "CONTINUE_WORK":
        next_action_message = "最新queue/stateを再取得し、次の独立Research/Auditまたは許可された独立作業へ進みます。"
    elif required_action == "DISCOVER_AGAIN":
        next_action_message = "未走査の探索軸へ進み、次のDiscovery roundを実行します。"
    elif required_action == "REFRESH_AND_CONTINUE":
        next_action_message = "最新canonical stateを再取得し、返された次の独立作業へ進みます。"
    elif required_action == "FINALIZE":
        next_action_message = "正本所定の停止条件を満たしたため、安全な最終化処理へ進みます。"
    else:
        next_action_message = required_action

    return {
        "decision": decision,
        "required_action": required_action,
        "finalization_allowed": finalization_allowed,
        "hard_stop": bool(reasons),
        "stop_reasons": reasons,
        "candidate_inventory": candidate_inventory,
        "work_mode": work_mode,
        "mode_source": mode_source,
        "research_audit_completed_this_invocation": research_audit_completed_this_invocation,
        "research_minimum_completions": research_minimum_completions,
        "last_terminal_job_status": last_terminal_job_status,
        "status_only_terminal": status_only_terminal,
        "research_quota_remaining": max(
            research_minimum_completions - research_audit_completed_this_invocation, 0
        ),
        "discovery_rounds_completed": discovery_rounds_completed,
        "discovery_min_rounds": discovery_min_rounds,
        "minimum_rounds_remaining": minimum_rounds_remaining,
        "discovery_exhausted": discovery_exhausted,
        "next_axis_available": next_axis_available,
        "write_failure_scope": write_scope,
        "write_action": write_action,
        "claim_state_checked": claim_state_checked,
        "claim_result_pending_age_seconds": claim_result_pending_age_seconds,
        "claim_monitor_window_seconds": claim_monitor_window_seconds,
        "claim_result_pending": bool(args.claim_result_pending),
        "claim_wait_action": claim_wait_action,
        "claim_wait_seconds": claim_wait_seconds,
        "submission_state_checked": submission_state_checked,
        "submission_result_pending": bool(getattr(args, "submission_result_pending", False)),
        "pipeline_ahead_count": pipeline_ahead_count,
        "submission_wait_action": submission_wait_action,
        "submission_wait_seconds": submission_wait_seconds,
        "discovery_precheck_result_pending": discovery_precheck_result_pending,
        "discovery_submission_result_pending": discovery_submission_result_pending,
        "discovery_evaluation_pending": discovery_evaluation_pending,
        "discovery_recovery_required": discovery_recovery_required,
        "discovery_round_in_progress": discovery_round_in_progress,
        "discovery_wait_action": discovery_wait_action,
        "discovery_wait_seconds": discovery_wait_seconds,
        "next_action_message": next_action_message,
        "progress_notice": progress_notice,
        "fallback_writable": fallback_writable,
        "durable_transport_available": any_durable_transport,
        "independent_work_after_fallback": independent_work,
        "active_assignment": active_assignment,
        "handoff_window_active": handoff_window_active,
        "final_handoff_active": final_handoff_active,
        "seconds_to_run_deadline": seconds_to_deadline,
        "seconds_to_next_scheduled_task": seconds_to_next,
        "effective_seconds_to_handoff": effective_seconds_to_handoff,
        "handoff_time_source": handoff_time_source,
        "scheduled_handoff_guard_seconds": handoff_guard,
        "scheduled_handoff_active": handoff_window_active,
        "rule": (
            "A single transport failure, pending claim result, pending backlog, bank exhaustion, "
            "or discovery submission is never by itself a whole-run stop condition. Normal workers "
            "must explicitly confirm the latest claim and submission state before ordinary finalization. Required "
            "claim results are polled every 10 real seconds using the same target identity until terminal or a canonical hard stop. "
            "When claimable independent Research/Audit work is available, a pending submission permits exactly one following paper "
            "to be claimed, processed, and submitted; when no such work is available, wait on the pending result instead. "
            "After that one-paper lookahead, the previous submission result becomes the barrier before another claim. Hourly Scheduled Chat workers prefer an actual-"
            "invocation-start + 3600 second run deadline over the nominal schedule boundary. "
            "The :00 and :30 schedules are the same paper task. In automatic mode, the run-start "
            "candidate_inventory is mandatory: >=50 selects Research/Audit and <50 selects Discovery. "
            "The selected mode is frozen for the run. Schedule labels and legacy worker kinds never select a mode. "
            "Discovery's four-round floor counts successful canonical precheck rounds in this invocation; "
            "multiple submissions derived from one precheck count as one round only after every declared split submission is durably successful. "
            "Research/Audit exposes the combined three-completion quota state. After a terminal "
            "blocked/deferred/rejected result, or whenever the three-completion floor is still unmet, "
            "the required action is CLAIM_NEXT_RESEARCH_AUDIT rather than run finalization. A pending "
            "submission therefore becomes a barrier before the paper after next, not before the immediate next paper; hard "
            "handoff/platform/durability/read "
            "failures override ordinary continuation. The 600-second handoff window forbids new independent work but does not abort an already-started assignment; "
            "the final 180 seconds force safe handoff. The 600-second window never aborts an already-started Discovery precheck/evaluation/submission/recovery. Research/Audit with zero claimable jobs waits and refreshes instead of issuing empty claims or switching modes. "
            "Discovery has no exhaustion-based ordinary early stop."
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
    ap.add_argument("--active-assignment", type=yn, default=False)
    ap.add_argument("--spillover-work", type=yn, default=False)
    ap.add_argument("--can-discover", type=yn, default=True)
    ap.add_argument("--claim-state-checked", type=yn, default=False)
    ap.add_argument("--claim-result-pending", type=yn, default=False)
    ap.add_argument("--claim-result-pending-age-seconds", type=int, default=0)
    ap.add_argument("--claim-monitor-window-seconds", type=int, default=60)
    ap.add_argument("--submission-state-checked", type=yn, default=False)
    ap.add_argument("--submission-result-pending", type=yn, default=False)
    ap.add_argument("--pipeline-ahead-count", type=int, default=0)
    ap.add_argument("--discovery-precheck-result-pending", type=yn, default=False)
    ap.add_argument("--discovery-submission-result-pending", type=yn, default=False)
    ap.add_argument("--discovery-evaluation-pending", type=yn, default=False)
    ap.add_argument("--discovery-recovery-required", type=yn, default=False)
    ap.add_argument("--write-failed", type=yn, default=False)
    ap.add_argument("--probe", choices=("success", "failure", "not-run"), default="not-run")
    ap.add_argument("--seconds-to-run-deadline", type=int, default=None)
    ap.add_argument("--seconds-to-next-scheduled-task", type=int, default=None)
    ap.add_argument("--scheduled-handoff-guard-seconds", type=int, default=600)
    ap.add_argument("--candidate-inventory", type=int, default=None)
    ap.add_argument("--work-mode", choices=("auto", "research", "discovery"), default="auto")
    ap.add_argument("--research-audit-completed-this-invocation", type=int, default=0)
    ap.add_argument("--research-minimum-completions", type=int, default=3)
    ap.add_argument(
        "--last-terminal-job-status",
        choices=("none", "completed", "blocked", "deferred", "rejected"),
        default="none",
    )
    ap.add_argument("--discovery-rounds-completed", type=int, default=0)
    ap.add_argument("--discovery-min-rounds", type=int, default=4)
    ap.add_argument("--discovery-exhausted", type=yn, default=False)
    ap.add_argument("--next-axis-available", type=yn, default=False)
    args = ap.parse_args()
    print(json.dumps(decide(args), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    from worker_guidance import run_guided

    raise SystemExit(run_guided(main, script=__file__))
