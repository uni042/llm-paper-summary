# Fallback Recovery Loop Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make one survey-helper run drain all currently replayable Research/Audit fallback envelopes through immutable publication, while preserving active claim banks and immutable slot history.

**Architecture:** Replay fallback records in bounded waves that never reuse the same record bank within one wave. After each wave, create a local Git commit that pins the exact slot blobs and descriptors into reachable history, process those descriptors synchronously into paper/job/results, then continue with the next wave. The final helper push publishes the whole commit chain; active claim banks remain excluded by existing bank selection.

**Tech Stack:** Python 3.12, Git, GitHub Actions, workflow-v10 immutable submission scripts.

**Spec:** `.survey/docs/survey-workflow/fallback-routing.md`, `.survey/docs/survey-workflow/library-checkpoint-registry.md`

## Global Constraints

- GitHub `main` remains the canonical repository state.
- Never overwrite a bank protected by an active claim.
- A descriptor must continue to reference exact Git blobs after its bank path is reused.
- Generic fallback remains at most one mutable singleton dispatch per helper invocation.
- A single invalid/deferred record must not starve independent replayable records.
- Publication failures must remain durable and isolated rather than silently dropped.

---

### Task 1: Prevent same-wave bank reuse

**Files:**
- Modify: `.survey/scripts/replay_record_fallback.py`
- Modify: `.survey/scripts/dispatch_fallback_inbox.py`
- Test: `.survey/tests/test_fallback_dispatch_batch.py`

**Interfaces:**
- `materialize(repo_root, envelope, *, excluded_banks=None)` excludes banks already consumed in the current wave.
- `dispatch(..., record_only=False)` tracks record banks used during one invocation and optionally skips generic envelopes.

- [ ] **Step 1: Write a failing test** asserting two replayed records cannot return the same bank in one dispatch wave and `record_only=True` leaves generic envelopes untouched.
- [ ] **Step 2: Run repository regression tests and confirm the new test fails.**
- [ ] **Step 3: Implement excluded-bank selection and record-only dispatch.**
- [ ] **Step 4: Run tests and confirm the new tests pass.**
- [ ] **Step 5: Commit the change.**

### Task 2: Add synchronous multi-wave fallback recovery

**Files:**
- Create: `.survey/scripts/drain_fallback_recovery.py`
- Create: `.survey/tests/test_drain_fallback_recovery.py`

**Interfaces:**
- `drain(repo_root, *, max_rounds=50, parallelism=4)` dispatches one distinct-bank wave, pins the wave in a local commit, processes its descriptors with `process_immutable_submission_batch`, commits settled outputs, and repeats until no replayable record descriptor is produced.
- Returns counts for rounds, envelopes, descriptors, failures, and remaining deferred records.

- [ ] **Step 1: Write a failing orchestration test** with mocked dispatch/processor/git helpers that requires multiple waves and verifies each wave is pinned before the next dispatch.
- [ ] **Step 2: Run tests and confirm failure.**
- [ ] **Step 3: Implement the minimal recovery driver.** It configures the bot identity, stages only durable recovery state for the pin commit, processes descriptors, stages publication state for the settlement commit, and stops safely on a no-progress round.
- [ ] **Step 4: Run tests and confirm success.**
- [ ] **Step 5: Commit the change.**

### Task 3: Wire recovery into survey-helper

**Files:**
- Modify: `.github/workflows/survey-helper.yml`

**Interfaces:**
- Helper runs `drain_fallback_recovery.py` before the ordinary generic fallback dispatch.
- The final publish step pushes local recovery commits even when the worktree is clean.

- [ ] **Step 1: Add workflow regression assertions** to ensure the recovery driver is compiled/invoked before generic dispatch and clean-worktree logic does not discard local commits ahead of `origin/main`.
- [ ] **Step 2: Update the workflow.**
- [ ] **Step 3: Run full repository regression tests, metadata validation, inventory, and structural checks.**
- [ ] **Step 4: Open a PR, inspect the patch, and merge only after all checks pass.**

### Task 4: Operational verification

**Files:**
- No persistent code beyond Tasks 1–3.

- [ ] **Step 1: Re-read latest `main` after merge.**
- [ ] **Step 2: Verify active claims still protect their assigned banks.**
- [ ] **Step 3: Verify reusable banks are recognized through immutable descriptors.**
- [ ] **Step 4: Verify fallback backlog decreases without requiring multiple scheduled helper invocations when all remaining records are independently replayable.**
