# Survey Status Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate and automatically maintain a deterministic `STATUS.md` summarizing the latest survey run, rolling 24-hour throughput, discovery efficiency, queue health, and operational warnings.

**Architecture:** A focused Python generator reads existing canonical JSON state and renders Markdown. Survey helper invokes it after queue processing and run-ledger recording, before the final commit. The generator never queries external services and never guesses unavailable Library-only state.

**Tech Stack:** Python 3.12 standard library, Markdown, GitHub Actions, unittest/pytest-compatible tests.

**Spec:** `docs/superpowers/specs/2026-09-12-status-dashboard-continuous-discovery-design.md`

## Global Constraints

- Output is `STATUS.md` at repository root.
- All displayed dates/times are JST.
- No timestamp-only churn: identical source state must render identical output.
- Rolling 24-hour counts deduplicate papers/candidates by stable IDs where possible.
- Seven-day comparison is emitted only with sufficient retained coverage; otherwise show `履歴不足`.
- Library pending count must be reported as unavailable rather than inferred.

---

### Task 1: Dashboard aggregation and rendering

**Files:**
- Create: `.survey/scripts/build_status_dashboard.py`
- Create: `.survey/tests/test_status_dashboard.py`

**Interfaces:**
- Consumes repository root `Path` and canonical JSON files.
- Produces `build_dashboard(repo_root: Path) -> str` and CLI `--repo-root`, `--output`.

- [ ] Write failing tests for latest-run selection, 24-hour aggregation, discovery funnel aggregation, queue/repair warnings, deterministic timestamp selection, and insufficient 7-day history.
- [ ] Run the new test file and confirm failure because the generator does not yet exist.
- [ ] Implement minimal JSON loading, ISO timestamp parsing, 24-hour/7-day window helpers, queue inventory/repair inspection, warning generation, discovery-axis summaries, and Markdown rendering.
- [ ] Run the new tests and confirm pass.
- [ ] Generate `STATUS.md` against branch state and inspect required sections.

### Task 2: Retention and workflow integration

**Files:**
- Modify: `.survey/scripts/record_run_ledger.py`
- Modify: `.survey/scripts/queue_worker.py`
- Modify: `.github/workflows/survey-helper.yml`
- Modify: `README.md`
- Create/update: `STATUS.md`

**Interfaces:**
- Run ledger retains at least 192 run entries.
- Discovery state retains at least 256 round entries.
- Survey helper runs `python .survey/scripts/build_status_dashboard.py --repo-root . --output STATUS.md` after ledger recording.

- [ ] Add failing assertions to existing/new tests for expanded retention.
- [ ] Confirm the retention assertions fail before code changes.
- [ ] Update retention migration logic so existing smaller stored limits are raised rather than preserved forever.
- [ ] Add dashboard script to workflow syntax validation and generation step.
- [ ] Add `運用ダッシュボード` link to README navigation.
- [ ] Run all repository regression tests and confirm pass.
