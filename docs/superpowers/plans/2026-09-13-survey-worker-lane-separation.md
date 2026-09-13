# Survey Worker Lane Separation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate claim allocation, research/audit submission publication, and heavyweight background maintenance so Scheduled Chat workers can claim one paper at a time without unrelated GitHub Actions work blocking them, while also making claim-age status and lease documentation accurately reflect the 90-minute default lease.

**Architecture:** Add a claim-only fast workflow and a single-submission publication fast workflow, and reduce the existing helper to background reconciliation. Research/audit completions use immutable per-attempt descriptors that reference the existing A-H fixed-slot banks. Claim and submission critical paths use dedicated concurrency groups; maintenance/citation/index/background use a separate writer group and bounded rebase/retry. Legacy `chat-inbox.json` remains accepted during migration.

**Tech Stack:** GitHub Actions YAML, Python 3.12, `unittest`, existing workflow-v10 queue/claim scripts.

**Spec:** `docs/superpowers/specs/2026-09-13-survey-worker-lane-separation-design.md`

## Global Constraints

- GitHub `main` remains the canonical source of truth.
- One Scheduled Chat/Work research worker may hold only one unfinished research/audit claim at a time.
- Default claim lease is exactly 5400 seconds (90 minutes); heartbeat may renew it.
- Expired claim files remain durable history but must not count as active claim age.
- New claim requests must never execute fallback, citation, maintenance, global dedupe, blocked retry, or full queue reconciliation.
- New research/audit submissions are immutable per attempt and may not overwrite another worker's submission.
- A record bank remains occupied while an unresolved immutable submission references its current attempt.
- Background failures must not prevent new claim allocation or durable immutable submission intake.
- Legacy `chat-inbox.json` remains replay-compatible during migration.
- All workflow YAML must parse and the full `.survey/tests/test_*.py` suite must pass.

---

### Task 1: Claim lease/status consistency

**Files:**
- Modify: `.survey/scripts/append_research_throughput_status.py`
- Modify: `.survey/tests/test_research_throughput_status.py`
- Modify: `.survey/docs/survey-workflow/queue-v10.md`
- Verify: `.survey/docs/survey-workflow/claim-serial-policy.md`

**Interfaces:**
- Consumes: `.survey/work-queue/jobs/*.json`, `.survey/work-queue/claims/*.json`
- Produces: `_oldest_active_claim_age(repo_root, now)` that considers only unexpired claims whose jobs are still ready research/audit jobs; STATUS label `最古の有効claimの経過時間`; queue-v10 default lease wording of 90 minutes.

- [ ] **Step 1: Add failing regression tests**

Add a test where an old unexpired claim points to a completed job while a newer unexpired claim points to a ready research job. Assert the displayed age uses only the ready job. Add assertions that the rendered label is `最古の有効claimの経過時間`.

```python
_write(repo / ".survey/work-queue/jobs/job-old.json", {"job_id": "job-old", "type": "research", "status": "completed"})
_write(repo / ".survey/work-queue/jobs/job-live.json", {"job_id": "job-live", "type": "research", "status": "ready"})
_write(repo / ".survey/work-queue/claims/job-old.json", {
    "job_id": "job-old", "claimed_at": "2026-09-13T02:00:00+00:00", "expires_at": "2026-09-13T05:20:00+00:00"
})
_write(repo / ".survey/work-queue/claims/job-live.json", {
    "job_id": "job-live", "claimed_at": "2026-09-13T03:30:00+00:00", "expires_at": "2026-09-13T05:00:00+00:00"
})
self.assertIn("最古の有効claimの経過時間 | **30 min**", text)
```

- [ ] **Step 2: Run the focused test and verify RED**

Run: `python -m unittest .survey.tests.test_research_throughput_status -v`

Expected: the new test fails because `_oldest_active_claim_age` currently does not require the job to remain ready, and the old label differs.

- [ ] **Step 3: Implement ready-only active age and wording**

Reuse `_ready_claimable_job_ids(repo_root)` inside `_oldest_active_claim_age`; skip every claim whose job ID is not in that set. Rename only the rendered table label, not durable claim files.

- [ ] **Step 4: Fix lease documentation**

Replace queue-v10's stale default `8-hour lease` statement with `90-minute (5400-second) lease`, and state explicitly that expired claim files remain on disk/history but stop blocking assignment. Ensure `claim-serial-policy.md` still says 90 minutes.

- [ ] **Step 5: Run focused tests**

Run: `python -m unittest .survey.tests.test_research_throughput_status .survey.tests.test_claim_worker .survey.tests.test_claim_heartbeat -v`

Expected: PASS.

---

### Task 2: Immutable research/audit submission primitives

**Files:**
- Create: `.survey/scripts/immutable_submission.py`
- Modify: `.survey/scripts/assemble_research_record.py`
- Modify: `.survey/scripts/select_record_bank.py`
- Create: `.survey/tests/test_immutable_submission.py`
- Modify: `.survey/tests/test_record_bank_selection.py` if present; otherwise extend `test_immutable_submission.py`.

**Interfaces:**
- Produces: `load_descriptor(path) -> dict`, `validate_descriptor(repo_root, descriptor) -> dict`, `pending_descriptors(repo_root) -> list[dict]`, `result_path_for(descriptor_path) -> Path`.
- Descriptor path: `.survey/work-queue/submissions/research/<attempt-id>.json` or `.survey/work-queue/submissions/audit/<attempt-id>.json`.
- Result path: `.survey/work-queue/results/research/<attempt-id>.json` or `.survey/work-queue/results/audit/<attempt-id>.json`.

- [ ] **Step 1: Add failing tests for two coexisting descriptors and bank occupancy**

Create two descriptors referencing different banks/attempts. Assert both validate independently, processing metadata for one never mutates the other, and `select_record_bank.inspect()` excludes any bank referenced by an unresolved descriptor.

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m unittest .survey.tests.test_immutable_submission -v`

Expected: FAIL because immutable submission helpers do not exist and bank selection only understands the reusable inbox.

- [ ] **Step 3: Implement immutable descriptor validation**

Require schema version, transport version 10, kind research/audit, unique safe attempt/job IDs, registered bank, exactly five slot references in canonical order, repository-relative fixed paths, exact blob SHAs, optional `expected_blob_sha`, paper path under `papers/`, and worker/claim attribution fields when present.

- [ ] **Step 4: Make record assembly descriptor-aware**

Refactor record-slot assembly into a pure helper that accepts a descriptor object/path and returns validated record + rendered Markdown without rewriting the global reusable `chat-inbox.json`. Preserve the existing legacy `assemble(repo_root)` entry point for `chat-inbox.json` replay compatibility.

- [ ] **Step 5: Extend bank selection**

Treat a bank as occupied when an unresolved immutable descriptor references its coherent current attempt. Treat it reusable only after the matching immutable result exists or legacy rules release it.

- [ ] **Step 6: Run focused tests**

Run: `python -m unittest .survey.tests.test_immutable_submission -v`

Expected: PASS.

---

### Task 3: Single-submission publication fast path

**Files:**
- Create: `.survey/scripts/process_immutable_submission.py`
- Modify: `.survey/scripts/queue_worker.py` only to expose reusable narrow helpers if needed; do not make the fast path scan all submissions.
- Create: `.survey/tests/test_process_immutable_submission.py`

**Interfaces:**
- CLI: `python .survey/scripts/process_immutable_submission.py --repo-root . --submission <repo-relative-path>`
- Processes exactly one immutable descriptor and writes exactly one immutable result plus that job/paper/identity delta and a lightweight queue snapshot.

- [ ] **Step 1: Add failing tests**

Cover: one descriptor processed while a second stays untouched; duplicate rerun is idempotent; stale expected paper SHA fails; terminal matching job reconciles to success; terminal conflicting attempt fails stale.

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m unittest .survey.tests.test_process_immutable_submission -v`

Expected: FAIL because processor is absent.

- [ ] **Step 3: Implement one-descriptor processor**

Validate descriptor and slots, render Markdown, validate current job and claim/attempt ownership, apply paper update with expected SHA protection, prepare identity delta, transition only that job, update minimal state counters, write immutable result, and refresh `next-jobs.json` without scanning/processing unrelated submissions.

- [ ] **Step 4: Make retry idempotent**

If matching result exists, return success/no-op. If job is already terminal with the same artifact/attempt, reconstruct matching success result. Never overwrite a conflicting result.

- [ ] **Step 5: Run focused tests**

Run: `python -m unittest .survey.tests.test_process_immutable_submission -v`

Expected: PASS.

---

### Task 4: Claim-only GitHub Actions fast lane

**Files:**
- Create: `.github/workflows/survey-claim-fast.yml`
- Modify: `.github/workflows/survey-helper.yml`
- Create: `.survey/tests/test_workflow_lane_separation.py`

**Interfaces:**
- Trigger: push to `.survey/work-queue/claim-requests/*.json` plus manual dispatch.
- Concurrency: `survey-claim-main`.

- [ ] **Step 1: Add workflow structure tests**

Parse YAML and assert claim-fast uses `survey-claim-main`, runs `claim_worker.py`, and contains none of: `dispatch_fallback_inbox.py`, `queue_worker.py`, `dedupe_queue.py`, `blocked_retry.py`, citation scripts, `survey.py --root .survey build`, or maintenance scripts. Assert `survey-helper.yml` no longer triggers on claim-request paths.

- [ ] **Step 2: Run focused tests and verify RED**

Run: `python -m unittest .survey.tests.test_workflow_lane_separation -v`

Expected: FAIL because workflow does not yet exist and helper still owns claims.

- [ ] **Step 3: Implement claim-fast workflow**

Checkout latest main, setup Python, syntax-check claim scripts, run `claim_worker.py`, refresh only the lightweight queue snapshot if required, stage only claim/result/snapshot files, commit, refetch/rebase, and retry push a bounded number of times.

- [ ] **Step 4: Remove claim trigger/work from background helper**

Remove `.survey/work-queue/claim-requests/*.json` from `survey-helper.yml` push triggers and remove the claim allocation step from that workflow.

- [ ] **Step 5: Run workflow tests**

Run: `python -m unittest .survey.tests.test_workflow_lane_separation -v`

Expected: claim-related assertions PASS.

---

### Task 5: Immutable submission GitHub Actions fast lane

**Files:**
- Create: `.github/workflows/survey-submission-fast.yml`
- Modify: `.github/workflows/survey-helper.yml`
- Modify: `.survey/tests/test_workflow_lane_separation.py`

**Interfaces:**
- Trigger: push to `.survey/work-queue/submissions/research/*.json` and `.survey/work-queue/submissions/audit/*.json`.
- Concurrency: `survey-submission-main`.

- [ ] **Step 1: Extend failing workflow tests**

Assert submission-fast has its own group and invokes only the single-submission processor for immutable submission pushes. Assert background helper does not trigger on the immutable research/audit descriptor directories.

- [ ] **Step 2: Run test and verify RED**

Run: `python -m unittest .survey.tests.test_workflow_lane_separation -v`

- [ ] **Step 3: Implement submission-fast workflow**

Determine the one descriptor changed by the triggering commit; if more than one immutable descriptor changed in one commit, iterate those explicit changed paths one by one without scanning historical submissions. For each, invoke `process_immutable_submission.py`. Commit/push with refetch/revalidation retry.

- [ ] **Step 4: Preserve legacy helper intake**

Keep legacy `.survey/work-queue/submissions/chat-inbox.json` and old immutable discovery submissions on the background helper during migration so existing staged/fallback work remains recoverable.

- [ ] **Step 5: Run workflow tests**

Run: `python -m unittest .survey.tests.test_workflow_lane_separation -v`

Expected: PASS.

---

### Task 6: Background lane and writer-lock separation

**Files:**
- Modify: `.github/workflows/survey-helper.yml`
- Modify: `.github/workflows/maintenance.yml`
- Modify: `.github/workflows/citation-graph-backfill.yml`
- Modify: `.github/workflows/rebuild-paper-indexes.yml`
- Modify: `.survey/tests/test_workflow_lane_separation.py`

**Interfaces:**
- Background lock: `survey-background-main` for helper/maintenance/citation/index operations that mutate shared derived state.
- Claim lock remains `survey-claim-main`; submission lock remains `survey-submission-main`.

- [ ] **Step 1: Add assertions for lock separation**

Test that no maintenance/citation/index/background workflow uses `survey-claim-main` or `survey-submission-main`, and that the background writers share `survey-background-main` where serialization is required.

- [ ] **Step 2: Run focused test and verify RED**

- [ ] **Step 3: Move helper to background responsibilities**

Keep fallback dispatch, offline job materialization, checkpoint transport requests, dedupe/normalization, blocked retry, periodic queue reconciliation, ledger reconciliation, and legacy chat-inbox compatibility. Remove normal research/audit immutable publication and claim allocation from it.

- [ ] **Step 4: Move maintenance/citation/index locks**

Use `survey-background-main` for workflows that must serialize large derived-state writes. Their work may queue behind one another but can no longer block claim-fast.

- [ ] **Step 5: Run focused tests**

Run: `python -m unittest .survey.tests.test_workflow_lane_separation -v`

Expected: PASS.

---

### Task 7: Canonical workflow documentation migration

**Files:**
- Modify: `.survey/docs/survey-workflow/queue-v10.md`
- Modify: `.survey/docs/survey-workflow/always-on-worker.md`
- Modify: `.survey/docs/survey-workflow/claim-serial-policy.md`
- Modify: `.survey/docs/survey-workflow/fallback-routing.md` if it references direct reusable inbox replay as the normal path.

**Interfaces:**
- Scheduled Chat normal transport becomes immutable descriptor after five slot writes.
- Legacy reusable inbox is migration/replay-only.

- [ ] **Step 1: Document immutable descriptor send protocol**

After writing five slot files and obtaining their exact Git blob SHAs, write a unique immutable descriptor under `submissions/research/` or `submissions/audit/`; do not update `chat-inbox.json` for new normal research/audit work.

- [ ] **Step 2: Document bank ownership and release**

An unresolved descriptor pins its bank/attempt. Matching result releases it. Library fallback remains the escape route when direct GitHub staging cannot proceed.

- [ ] **Step 3: Document critical-path behavior**

A worker may issue the next one-job claim immediately after the complete immutable descriptor or Library envelope is durably saved; it does not wait for submission-fast terminal completion.

- [ ] **Step 4: Verify 90-minute lease wording everywhere**

Search canonical survey workflow docs for `8-hour`, `8 hour`, `8時間`, `28800`, and stale default lease descriptions; update only default-lease statements, preserving configurable max lease documentation where relevant.

---

### Task 8: Full regression and live Actions verification

**Files:**
- No new production files unless failures require focused fixes.

**Interfaces:**
- Repository regression workflow is authoritative CI verifier.

- [ ] **Step 1: Run full local-style regression in CI-equivalent command**

Run: `python -m compileall -q .survey/scripts`

Run: YAML parse over every `.github/workflows/*.yml` using PyYAML.

Run: `python -m unittest discover -s .survey/tests -p 'test_*.py'`

Expected: all PASS.

- [ ] **Step 2: Push/commit final changes to main**

Use fresh blob SHAs/current main; reconcile any concurrent survey-helper/status commits rather than overwriting them.

- [ ] **Step 3: Verify repository regression Actions**

Confirm the `Repository regression tests` workflow for the final implementation commit succeeds.

- [ ] **Step 4: Verify lane behavior from workflow runs**

Confirm a claim-only commit triggers `survey-claim-fast` and does not trigger full background work; confirm maintenance/citation activity does not share its concurrency group. If a safe immutable submission fixture is available, confirm the submission-fast workflow processes it independently without consuming unrelated pending submissions.

- [ ] **Step 5: Inspect generated STATUS**

Confirm the dashboard shows `最古の有効claimの経過時間`, expired/terminal claims do not inflate it, and current active-claim totals still reconcile with `next-jobs.json`.
