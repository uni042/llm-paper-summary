# Continuous Discovery Specialist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the hourly discovery specialist continue rotating through useful search axes until genuine execution/durability limits are reached, without removing discovery from the normal paper worker.

**Architecture:** Repository policy documents define soft vs hard stop conditions and axis-rotation rules. Discovery submissions continue to flow through workflow-v10 transport, with Actions as the single writer of discovery statistics. The Scheduled Chat prompt is kept thin enough to defer to repository policy while explicitly requiring continuation behavior.

**Tech Stack:** Markdown policy, Scheduled Chat automation prompt, existing workflow-v10 JSON transport and Python queue worker.

**Spec:** `docs/superpowers/specs/2026-09-12-status-dashboard-continuous-discovery-design.md`

## Global Constraints

- Existing `:30` normal worker retains discovery capability.
- Specialist candidate inventory target/watermarks are prioritization signals, not stop conditions.
- No fixed discovery-round count or candidate quota.
- Empty/all-duplicate/low-yield rounds rotate axes and continue.
- One inaccessible source/tool/write does not end the run when alternate search or durable fallback exists.
- Hard stop only on unsafe canonical-state access, total durability failure, execution ceiling, or reasonable exhaustion of independent promising axes.

---

### Task 1: Repository policy hardening

**Files:**
- Modify: `.survey/docs/survey-workflow/discovery-specialist-worker.md`
- Modify: `.survey/docs/survey-workflow/candidate-buffer-policy.md`

**Interfaces:**
- Produces explicit `soft stop / hard stop / continuation loop` contract used by Scheduled Chat.

- [ ] Add a regression/document-policy test that asserts key continuation phrases/requirements are present.
- [ ] Confirm it fails against current policy.
- [ ] Add the continuation loop, alternate-source behavior, inventory-not-stop rule, and narrow hard-stop conditions.
- [ ] Re-run the policy test and confirm pass.

### Task 2: Discovery metadata and Scheduled Chat prompt

**Files:**
- Modify: `.survey/scripts/queue_worker.py` only as needed for backward-compatible `source_worker` metadata and expanded discovery history retention.
- Modify active automation `LLM論文探索専用` prompt.

**Interfaces:**
- `discovery_stats.source_worker` is optional and defaults compatibly for historical/normal submissions.
- Specialist prompt reads repo policy first and continues until policy hard-stop.

- [ ] Extend discovery-stat tests for `source_worker` persistence and 256-round minimum retention.
- [ ] Confirm new assertions fail before implementation.
- [ ] Implement metadata/retention changes without changing dedupe semantics.
- [ ] Update active specialist Scheduled Chat prompt to make the repository continuation contract authoritative.
- [ ] Run complete repository regression tests.
