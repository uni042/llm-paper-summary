# Parallel Immutable Submission Batch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Process independent immutable research/audit descriptors concurrently inside the serialized submission lane while preserving exact-once shared queue statistics and deterministic snapshots.

**Architecture:** Keep the GitHub Actions `survey-submission-main` single-writer boundary for the final repository commit, but parallelize descriptor-local work inside one run. Each descriptor writes only its own paper/job/result/identity-delta plus a temporary state-effect JSON; after all descriptor workers finish, one reducer folds the temporary effects into `state.json` and rebuilds `next-jobs.json` once. The batch runner builds connected components over all shared mutation resources (`canonical_id`, `paper_path`, and `job_id`): descriptors sharing any resource run sequentially, while disconnected groups run concurrently. Identity-delta files are published with atomic replace so parallel readers never observe partial JSON.

**Tech Stack:** Python 3.12, GitHub Actions, Bash, `concurrent.futures`, subprocess workers, unittest.

**Spec:** `.github/workflows/survey-submission-fast.yml`, `.survey/scripts/process_immutable_submission.py`, `.survey/scripts/process_immutable_submission_batch.py`, `.survey/scripts/reduce_submission_effects.py`, `.survey/scripts/identity_delta.py`

## Global Constraints

- Do not remove the repository-wide submission workflow concurrency group in this phase.
- Preserve immutable descriptor/result identity checks and existing failure isolation behavior.
- Descriptors sharing canonical identity, paper path, or job ID must serialize; only disconnected mutation groups may overlap.
- Shared `state.json` and `next-jobs.json` are written exactly once per batch by the reducer.
- A failed descriptor must not prevent successful independent descriptors from becoming durable.
- Push-race retries must recompute the entire unsettled batch from latest `main`.

---

### Task 1: Deferred shared-state effects

**Files:**
- Modify: `.survey/scripts/process_immutable_submission.py`
- Create: `.survey/scripts/reduce_submission_effects.py`
- Test: `.survey/tests/test_parallel_submission_batch.py`

**Interfaces:**
- `process(..., defer_shared_state: bool = False, effect_path: Path | None = None)` keeps current behavior by default.
- Deferred mode writes one effect object containing `research_completed`, `audit_completed`, `rejected`, and `views_dirty` instead of saving shared state/snapshot.
- `reduce_submission_effects.py --repo-root . --effects-dir <dir>` folds effect files into current state and rebuilds `next-jobs.json` once.

- [x] **Step 1: Write failing tests** for deferred submission effects and reducer aggregation.
- [x] **Step 2: Run the new test module** and verify RED because deferred mode/reducer do not exist.
- [x] **Step 3: Implement deferred effect emission** without changing default single-descriptor semantics.
- [x] **Step 4: Implement reducer** with additive counters, `views_dirty` OR semantics, and one snapshot refresh.
- [x] **Step 5: Run repository regression tests** and verify GREEN.

### Task 2: Connected-resource exclusion and parallel batch runner

**Files:**
- Create: `.survey/scripts/process_immutable_submission_batch.py`
- Modify: `.survey/scripts/identity_delta.py`
- Test: `.survey/tests/test_parallel_submission_batch.py`
- Test: `.survey/tests/test_parallel_submission_identity_group.py`

**Interfaces:**
- Each descriptor exposes serialization resources for its canonical identity (from the immutable metadata slot), paper path, and job ID.
- Union-find builds connected components across those resources, so research/audit attempts that touch the same paper or identity cannot overlap even when job IDs differ.
- Malformed or unidentifiable descriptors fall back to their descriptor path as an isolated resource.
- Descriptors within one connected component run sequentially; disconnected components run concurrently with `ThreadPoolExecutor`.
- Production workers invoke `process_immutable_submission.py` as separate subprocesses, preserving module-global isolation.
- `process_immutable_submission_batch.py` accepts descriptor paths plus `--parallelism N` (default 4, bounded to 1..8), invokes existing isolation for failures, and runs the reducer after all groups finish.
- Identity-delta writers use temporary files plus `os.replace` to prevent partial JSON visibility.

- [x] **Step 1: Add failing tests** showing distinct jobs overlap while same job/paper/identity attempts serialize.
- [x] **Step 2: Implement connected-resource grouped batch runner** and bounded parallelism.
- [x] **Step 3: Make identity-delta publication atomic** for parallel readers.
- [x] **Step 4: Verify failure aggregation** keeps successful results/effects and records failed-result state.

### Task 3: Wire the workflow to batch parallelism

**Files:**
- Modify: `.github/workflows/survey-submission-fast.yml`
- Test: `.survey/tests/test_workflow_lane_separation.py`
- Test: `.survey/tests/test_submission_backlog_drain.py`

**Interfaces:**
- Push-triggered backlog drain passes all unsettled descriptors to the batch runner.
- `SUBMISSION_PARALLELISM` defaults to 4 and the runner clamps it to 1..8.
- The final Git commit/push remains one serialized transaction.

- [x] **Step 1: Add a workflow regression assertion** that the batch runner is used and `SUBMISSION_PARALLELISM` is bounded.
- [x] **Step 2: Replace the sequential descriptor loop** with the batch runner while retaining existing failure/push-retry messaging.
- [ ] **Step 3: Run the complete repository regression suite** and verify all tests pass at the final branch head.
- [ ] **Step 4: Review the PR diff** for accidental changes to claim/discovery routing or immutable transport semantics.
