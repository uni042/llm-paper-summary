# Fallback Recovery Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make one survey-helper run drain all currently replayable Research/Audit fallback envelopes through immutable publication while preserving active claim banks and exact slot history.

**Architecture:** Process replayable record fallbacks sequentially. For each record, materialize it into a bank selected by the existing safety logic, commit the exact slot blobs and immutable descriptor before the mutable bank path can be reused, synchronously publish that descriptor, then proceed to the next record. Generic fallback remains on its existing serialized route.

**Tech Stack:** Python 3.12, Git, GitHub Actions, workflow-v10 immutable submissions.

**Spec:** `.survey/docs/survey-workflow/fallback-routing.md`, `.survey/docs/survey-workflow/library-checkpoint-registry.md`

## Global Constraints

- GitHub `main` remains canonical.
- Never overwrite a bank protected by an active claim.
- A descriptor must retain access to its exact Git blobs after bank-path reuse.
- Invalid/deferred records must not starve independent replayable records.
- Generic mutable fallback remains serialized.
- Publication failures remain durable and isolated.

---

### Task 1: Add synchronous record recovery driver

**Files:**
- Create: `.survey/scripts/drain_fallback_recovery.py`
- Create: `.survey/tests/test_drain_fallback_recovery.py`

**Interfaces:**
- `dispatch_one_record(repo_root)` selects at most one replayable record fallback.
- `pin_materialized_record(repo_root, row)` commits exact transport blobs before bank reuse.
- `settle_descriptor(repo_root, descriptor, parallelism=4)` publishes the pinned immutable descriptor.
- `drain(repo_root, max_records=200, parallelism=4)` repeats until no more replayable records can progress.

- [x] **Step 1: Write a failing orchestration test** requiring dispatch → pin → settle before the next dispatch.
- [x] **Step 2: Verify the test fails before implementation.**
- [x] **Step 3: Implement the recovery driver.**
- [x] **Step 4: Run the full regression suite.**

### Task 2: Wire recovery into survey-helper

**Files:**
- Modify: `.github/workflows/survey-helper.yml`

**Interfaces:**
- Run synchronous record recovery before ordinary fallback dispatch.
- Preserve local pin commits during final publication even if the worktree is otherwise clean.

- [x] **Step 1: Compile the recovery driver in workflow syntax validation.**
- [x] **Step 2: Invoke the recovery driver before generic dispatch.**
- [x] **Step 3: Make final publication recognize local commits ahead of `origin/main`.**
- [x] **Step 4: Run regression, metadata, inventory, and structural verification.**

### Task 3: Operational verification

- [ ] **Step 1: Merge to latest `main`.**
- [ ] **Step 2: Verify active claims still protect assigned banks.**
- [ ] **Step 3: Verify fallback backlog drains within one helper invocation when records are replayable.**
