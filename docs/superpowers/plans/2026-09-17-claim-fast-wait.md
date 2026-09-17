# Claim Fast-Lane and Wait-Loop Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reduce claim-result latency and make pending claim waits use an actual 30-second runtime delay before re-reading the same request.

**Architecture:** Keep claim allocation safety logic in the serialized `survey-claim-main` workflow, but remove dashboard/status generation from the claim critical path. Strengthen the canonical liveness contract and active Scheduled Chat prompts so pending claims must invoke an actual timer/sleep mechanism for 30 seconds before each same-request recheck.

**Tech Stack:** GitHub Actions YAML, Python/unittest policy tests, Scheduled Chat automation prompts.

**Spec:** User-selected remediation items 1 and 3 from the claim-pending incident analysis in the current `論文サーベイ` project.

## Global Constraints

- Preserve claim allocation, checkpoint barriers, repair recovery, record-bank routing, and immutable queue state.
- Do not modify immutable submission/result payloads.
- Pending claim rechecks must keep the same `request_id` and must not issue duplicate claims.
- A single pending/in-progress observation must never permit normal finalization.

---

### Task 1: Slim the claim fast lane

**Files:**
- Modify: `.github/workflows/survey-claim-fast.yml`
- Create: `.survey/tests/test_claim_fast_lane_scope.py`

**Interfaces:**
- Consumes: claim request files under `.survey/work-queue/claim-requests/`.
- Produces: claim/job/result/record-bank state required for workers to start the assigned job.

- [ ] **Step 1: Write the failing workflow-scope test**

Add assertions that the fast lane still executes `normalize_research_paper_paths.py`, `apply_library_checkpoint_barriers.py`, `claim_worker_with_banks.py`, `repair_claim_bank_recovery.py`, and `enrich_claim_record_routes.py`, while forbidding queue snapshot/dashboard/status scripts and `STATUS.md` staging from the workflow.

- [ ] **Step 2: Run the test and confirm RED**

Run repository regression tests on the branch; the new test must fail against the current workflow because dashboard/status work is still present.

- [ ] **Step 3: Remove non-claim critical-path work**

Delete `refresh_queue_snapshot.py`, `ensure_dashboard_history.py`, `render_status_dashboard.py`, `append_research_throughput_status.py`, and `refine_status_observability.py` from the fast-lane execution and syntax-validation lists. Restrict `git add` to jobs/claims/claim-results/records and any request/barrier state actually changed by claim safety logic; do not stage `STATUS.md` or dashboard-only snapshots.

- [ ] **Step 4: Run targeted and full regression tests**

Confirm the new test passes and repository tests remain green.

### Task 2: Require real-time 30-second pending waits

**Files:**
- Modify: `.survey/docs/survey-workflow/run-liveness-policy.md`
- Modify: `.survey/tests/test_run_liveness_policy.py`
- Modify active Scheduled Chat prompts `LLM論文探索専用` and `LLM研究サーベイ`.

**Interfaces:**
- Consumes: a pending claim result identified by one durable `request_id`.
- Produces: a re-read of the same claim result only after at least 30 seconds of actual elapsed wait, repeated until result/terminal hard stop.

- [ ] **Step 1: Write the failing policy test**

Require the canonical policy to state that an actual runtime timer/sleep must elapse for 30 seconds and that immediate repeated refreshes/tool calls are not a substitute.

- [ ] **Step 2: Run the test and confirm RED**

The current policy says `30秒待機` but does not require an actual runtime wait mechanism, so the new assertion must fail.

- [ ] **Step 3: Strengthen the canonical policy**

Specify that each pending-claim loop iteration must invoke an available runtime wait/timer mechanism for 30 real seconds before refreshing the same request; immediate re-fetch loops and merely stating that 30 seconds passed are invalid.

- [ ] **Step 4: Update both active Scheduled Chat prompts**

Add the same operational rule: when claim result is pending, invoke an available runtime/Python wait mechanism equivalent to `time.sleep(30)`, then re-fetch the same `request_id`; repeat until result or explicit hard stop, and do not emit the final response from the pending branch.

- [ ] **Step 5: Verify tests and prompt state**

Run repository regression tests, verify the active tasks remain enabled on their existing schedules, and confirm their prompts contain the real-wait rule.
