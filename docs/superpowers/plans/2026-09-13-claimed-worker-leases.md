# Claimed Worker Leases Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (adapted to the repository rule that one Luna owns this entire vertical slice) to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add repository-backed claim leases and immutable claimed-worker completion intake so concurrent research/audit workers cannot duplicate or overwrite one another.

**Architecture:** A new standalone allocator consumes immutable claim requests inside the existing `survey-helper-main` single-writer workflow and maintains one current claim per job. Queue visibility and maintenance use shared claim semantics, while the existing fallback dispatcher validates claimed envelopes against the current claim before remapping their complete five-slot logical bundle to a safe record bank.

**Tech Stack:** Python 3.12 standard library, unittest temporary repositories, GitHub Actions YAML, workflow-v10 JSON transport.

**Spec:** `docs/superpowers/specs/2026-09-13-claimed-worker-leases-design.md`

## Global Constraints

- Do not add a claimed job status or otherwise change the existing job lifecycle.
- Only ready research/audit jobs are claimable; discovery behavior and specialist lane remain unchanged.
- A worker must have an assignment before full-text reading.
- Scheduled workers never directly update papers, queue/state, identity, README, fixed record banks, or reusable chat-inbox.
- Claimed completions are immutable envelopes; only serialized GitHub Actions expands them to the existing five-slot record bank and Chat inbox.
- Preserve `concurrency.group: survey-helper-main` with `cancel-in-progress: false` in survey-helper and maintenance.
- Preserve legacy fallback envelopes, single-writer queue/paper/index updates, existing dedupe/rebase retry, A-H banks, and Google Drive removal.
- Default lease is 28800 seconds; accepted lease range is 300 through 43200 seconds; max jobs defaults to 1 and accepts 1 through 4.
- Priority order is priority descending, created time ascending, job ID ascending.
- No external service, discovery claim, lease renewal, bank parallel writer, or unrelated refactor.

---

### Task 1: Repository-backed claim and immutable completion vertical slice

**Files:**
- Create: `.survey/scripts/claim_worker.py`
- Create: `.survey/scripts/claim_state.py`
- Create: `.survey/tests/test_claim_worker.py`
- Create: `.survey/tests/test_claimed_dispatch.py`
- Create: `.survey/tests/test_claim_gc.py`
- Modify: `.survey/scripts/queue_worker.py`
- Modify: `.survey/scripts/maintenance_health.py`
- Modify: `.survey/scripts/select_record_bank.py`
- Modify: `.survey/scripts/fallback_transport.py`
- Modify: `.survey/scripts/dispatch_fallback_inbox.py`
- Modify: `.survey/scripts/full_gc.py`
- Modify: `.survey/tests/test_queue_worker_metadata.py`
- Modify: `.survey/tests/test_maintenance_health.py`
- Modify: `.survey/tests/test_discovery_stats.py`
- Modify: `.github/workflows/survey-helper.yml`
- Modify: `.github/workflows/maintenance.yml`
- Modify: `.survey/docs/survey-workflow/README.md`
- Modify: `.survey/docs/survey-workflow/queue-v10.md`
- Modify: `.survey/docs/survey-workflow/always-on-worker.md`
- Modify: `.survey/docs/survey-workflow/fallback-routing.md`
- Modify: `.survey/docs/survey-workflow/worker-router.md`
- Modify: `.survey/docs/survey-workflow/backlog-resilience.md`
- Modify: `.survey/docs/survey-workflow/candidate-buffer-policy.md`
- Modify only if required by exact routing consistency: `.survey/docs/survey-workflow/continuation-policy.json`

**Interfaces:**
- `claim_state.parse_time(value) -> datetime | None`
- `claim_state.current_claims(repo_root, now) -> mapping` exposing current and active status without deleting expired claims.
- `claim_state.snapshot_claiming(jobs, repo_root, now) -> dict` returning `ready_research_audit`, `actively_claimed`, and `claimable`.
- `claim_worker.process_requests(repo_root, at=None) -> dict` validating every request, reusing existing results, allocating deterministically, and writing results/claims idempotently.
- `fallback_transport.claimed_envelope_state(repo_root, envelope) -> (accepted: bool, reason: str | None)` accepting an expired but current claim and rejecting missing/superseded claims.
- Existing `dispatch_fallback_inbox.dispatch(repo_root)` quarantines rejected claimed envelopes and otherwise preserves legacy behavior and bank remapping.
- Existing snapshot producers return the old fields plus `claiming`, with active claimed research/audit omitted from `next_jobs`.

- [ ] **Step 1: Write allocator RED tests**

Add real temporary-repository tests for one job/two requests, two jobs/two requests with literal priority order, idempotent repeated request, active lease exclusion, expired lease reallocation, terminal exclusion, discovery exclusion, validation errors, deterministic malformed-request results, and same-run reservation. Each test must assert result and current claim files, not mocks.

- [ ] **Step 2: Run allocator tests and verify RED**

Run: `python -m unittest .survey.tests.test_claim_worker -v`

Expected: import/function failures because claim modules do not yet exist.

- [ ] **Step 3: Implement minimal claim state and allocator**

Implement safe ID validation, request schema/defaults/bounds, UTC parsing, deterministic claim IDs, canonical job snapshots without private `_path`, stable ordering, result-authoritative reruns, sequential same-run exclusion, terminal/discovery filtering, and atomic-enough same-filesystem temp-write/replace JSON writes. Keep expired current claim files until reassignment.

- [ ] **Step 4: Run allocator tests and verify GREEN**

Run: `python -m unittest .survey.tests.test_claim_worker -v`

Expected: all allocator tests pass.

- [ ] **Step 5: Write dispatch fencing and bank-remap RED tests**

Use complete synthetic five-slot envelopes. Assert: late result before reassignment dispatches; stale claim after reassignment is quarantined without touching Chat inbox or paper; current replacement claim dispatches; missing claim quarantines; terminal claimed job archives without applying; legacy envelope still dispatches; two claimed envelopes serialize through safe bank selection and do not overwrite an unsettled attempt.

- [ ] **Step 6: Run dispatch tests and verify RED**

Run: `python -m unittest .survey.tests.test_claimed_dispatch -v`

Expected: claimed envelopes are not yet fenced and one or more assertions fail for the named behavior.

- [ ] **Step 7: Implement claimed-envelope validation before any transport expansion**

Extend envelope metadata validation only for `origin == "claimed_worker"`; require safe `job_id`, `claim_id`, `worker_id`, and `attempt_id`, check top-level IDs against Chat payload identity, and compare with `.survey/work-queue/claims/<job_id>.json`. In dispatcher order, acknowledge terminal jobs first, then quarantine missing/superseded claims with the existing error sidecar, then dependency/busy/bank checks. Call `remap_research_bank` before `apply_envelope`; preserve the immutable source envelope in archive and all legacy behavior.

- [ ] **Step 8: Run dispatch tests and verify GREEN**

Run: `python -m unittest .survey.tests.test_claimed_dispatch -v`

Expected: all dispatch fencing, legacy, and remapping tests pass.

- [ ] **Step 9: Write snapshot, maintenance, selector, and GC RED tests**

Assert active claimed research/audit is absent from normal `next_jobs`; expired-current research becomes visible/claimable; discovery remains visible and unchanged; claiming totals are literal; maintenance rebuild matches queue worker output; selector protects every ready job by reading job files rather than the truncated snapshot; ready-job claims survive active and expired GC; old terminal-job claims and linked processed request/result become eligible only after retention; unprocessed requests/results remain protected.

- [ ] **Step 10: Run state/GC tests and verify RED**

Run: `python -m unittest .survey.tests.test_queue_worker_metadata .survey.tests.test_maintenance_health .survey.tests.test_claim_gc -v`

Expected: failures show old snapshot, selector, and GC behavior.

- [ ] **Step 11: Implement shared claim-aware state and GC**

Use the shared claim-state helpers from both snapshot producers. Preserve counts as lifecycle counts, omit only active claimed research/audit from the visible candidate list, retain discovery injection, and add the three-field `claiming` summary. Make selector read canonical ready job files. Extend GC with explicit claim/request/result candidates that never remove a current claim for a ready job, never remove active claims, and never remove an unprocessed request/result pair. Include new protected/live-reference paths and report kinds. Fix the existing Windows submission path serialization with `.as_posix()` so the baseline suite is platform-stable.

- [ ] **Step 12: Run focused state/GC tests and verify GREEN**

Run: `python -m unittest .survey.tests.test_queue_worker_metadata .survey.tests.test_maintenance_health .survey.tests.test_claim_gc .survey.tests.test_discovery_stats -v`

Expected: all pass on Windows and the claim-aware snapshots are identical apart from timestamps.

- [ ] **Step 13: Integrate workflow and protocol documentation**

Add only `.survey/work-queue/claim-requests/*.json` to the push paths so claim result/claim commits do not self-trigger. Compile `claim_state.py` and `claim_worker.py`, process claims before dispatch, and keep allocator/dispatcher/queue steps inside the existing concurrency group and commit/rebase retry. Document latest-main → unique request → wait for result before reading → assigned job only → five slots → claimed immutable envelope → no terminal wait barrier → new request. State that Work helpers currently process research/audit backlog without discovery, while the scheduled normal-worker and discovery specialist policies remain unchanged. Add claim directories to maintenance protection/GC reporting without changing its concurrency group.

- [ ] **Step 14: Run focused integration and simulation**

Run the complete claim test set and a synthetic 2-4 worker script/test that processes several requests in one run, expires/reassigns one claim, submits old/new envelopes, and proves only the current claim reaches reusable transport after reassignment.

- [ ] **Step 15: Run repository verification**

Run:

```text
python -m compileall -q .survey/scripts
python -c "from pathlib import Path; import yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in sorted(Path('.github/workflows').glob('*.yml'))]"
python -m unittest discover -s .survey/tests -p 'test_*.py'
python .survey/scripts/build_repository_inventory.py --root . --output .survey/reports/claim-worktree-inventory.json --source-commit claim-worktree
python .survey/scripts/check_repository.py --root . --inventory .survey/reports/claim-worktree-inventory.json --report .survey/reports/claim-worktree-consistency.json
git diff --check
```

Delete only the two generated worktree verification reports if they are untracked/transient. Inspect `git diff --name-only origin/main...HEAD` and `git diff origin/main...HEAD -- papers .survey/survey-state` to prove no paper or identity data changed. Search the diff for Google Drive and workflow trigger/concurrency regressions.

- [ ] **Step 16: Commit meaningful units**

Commit allocator/tests, dispatcher fencing/tests, snapshot/GC/workflow/tests, and protocol documentation as separate meaningful commits. Do not commit generated reports, caches, or live queue mutations.
