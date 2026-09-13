# Luna-first Operations Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make parallel Luna execution the default for independent repository work while reducing repeated context and keeping external effects under Sol control.

**Architecture:** Global Codex configuration retains four Luna slots and injects the DPAPI credential-store setting. Global and repository instructions define a compact task-packet protocol, a maximum-three-worker-plus-one-reserve policy, evidence-file handoffs, and exception-only Sol triage. Repository-specific rules serialize canonical writers and prevent overlapping edits.

**Tech Stack:** Codex TOML configuration, Markdown agent instructions, GitHub CLI, Git.

**Spec:** `C:\Users\YASUHIRO\.codex\attachments\b52192d9-8637-4460-8189-44249af22d07\pasted-text.txt`

## Global Constraints

- Preserve existing dirty worktrees and unrelated user changes.
- Use `gpt-5.6-luna` with high reasoning for Luna execution.
- Use `fork_turns="none"` and file-backed briefs/reports to reduce retained context.
- Never allow two Luna workers to edit the same file or an unfrozen shared interface concurrently.
- Keep commit, push, GitHub settings, credentials, and other external effects under Sol control.
- Do not enable unrestricted filesystem or network access.

---

### Task 1: Repository-specific Luna coordination contract

**Files:**
- Create: `AGENTS.md`

**Interfaces:**
- Consumes: the global Sol/Luna role definitions and the repository's existing single-writer workflow.
- Produces: repository-local ownership, token-budget, blocker, and verification rules.

- [ ] **Step 1: Add repository boundaries**

Document the three-plus-one concurrency default, non-overlapping write sets, canonical-writer serialization, and Sol-owned external effects.

- [ ] **Step 2: Add compact handoff rules**

Require a short file-backed brief, no full conversation history, concise status-only chat return, and a file-backed detailed report.

- [ ] **Step 3: Validate instructions**

Run: `rg -n "3\+1|fork_turns|write_set|BLOCKED_EVIDENCE|survey-helper-main|push" AGENTS.md`

Expected: every required coordination rule is present.

### Task 2: Global Codex and Luna defaults

**Files:**
- Modify: `C:\Users\YASUHIRO\.codex\config.toml`
- Modify: `C:\Users\YASUHIRO\.codex\AGENTS.md`
- Modify: `C:\Users\YASUHIRO\.codex\agents\luna.toml`

**Interfaces:**
- Consumes: existing trusted-project and four-subagent configuration.
- Produces: persistent DPAPI authentication and token-efficient Luna handoffs across projects.

- [ ] **Step 1: Preserve the existing TOML structure**

Add `GCM_CREDENTIAL_STORE = "dpapi"` to the existing `[shell_environment_policy.set]` table. Do not duplicate the table or replace existing entries.

- [ ] **Step 2: Update global coordination rules**

Define adaptive three-plus-one parallelism, exception-only Sol triage, file-backed briefs/reports, no repeated progress polling, and a two-attempt same-root-cause limit.

- [ ] **Step 3: Update Luna return behavior**

Limit chat output to status, changed files, test summary, and concerns; put detailed evidence in the assigned report file when one is supplied.

- [ ] **Step 4: Validate configuration**

Parse `config.toml` with Python `tomllib` and search the two instruction files for all required rules.

### Task 3: GitHub CLI availability

**Files:**
- External installation only; no repository files.

**Interfaces:**
- Consumes: Windows package manager and existing GitHub authentication.
- Produces: a working `gh` executable for Sol-owned GitHub checks and actions.

- [ ] **Step 1: Detect existing installation**

Run: `Get-Command gh -ErrorAction SilentlyContinue`.

- [ ] **Step 2: Install when absent**

Run the package manager non-interactively with the official GitHub CLI package identifier.

- [ ] **Step 3: Verify without exposing credentials**

Run: `gh --version` and `gh auth status`; do not print tokens. Installation is complete when the executable works. If `gh` has no independent login, record that user action separately and retain Git/GCM DPAPI for Git operations; never run `gh auth setup-git` automatically.

### Task 4: Integrated verification and review

**Files:**
- Review all files changed by Tasks 1 and 2.

**Interfaces:**
- Consumes: the completed repository and global changes.
- Produces: evidence that configuration parses, required constraints are present, and the repository remains healthy.

- [ ] **Step 1: Run focused checks**

Run TOML parsing, instruction searches, `git diff --check`, and repository status checks.

- [ ] **Step 2: Run repository regression tests**

Run: `python -B -m unittest discover -s .survey/tests -p 'test_*.py'`

- [ ] **Step 3: Obtain independent read-only review**

Review the repository diff and global-file patch for overlapping ownership, excessive context, unsafe permissions, or missing external-effect boundaries.

- [ ] **Step 4: Integrate safely**

Commit only the intended repository files, fast-forward `main`, rerun checks, then push without force.
