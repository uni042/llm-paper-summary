# Read-only legacy inventory

Date: 2026-09-24  
Repository snapshot: `main@b8d6e7ca41e99bd1aaef70cb9c36115544e7f7b2`

## Goal

Produce a machine-readable, read-only inventory that makes the next cleanup batch evidence-based. This step does not migrate or delete repository data and does not review paper content quality.

## Scope and contract

- Inventory repository worktree files by relative path, kind, size, path-based disposition class, reason, and write-freeze flag; exclude VCS and runtime directories.
- Count paper Markdown paths without opening their bodies.
- Do not open work-queue payloads; report only their paths and sizes.
- Scan scripts and workflow documentation for a targeted set of retired-format markers. Store path, line, and marker only; never copy source lines into the report.
- Classifications are triage labels, never deletion instructions. Archive, cache, and legacy-looking names still require producer/reader/reference checks.
- Generate JSON to an explicit output path or stdout. Never modify the repository by default.
- Add focused tests for live recovery preservation, archive triage, paper/payload non-disclosure, and deterministic report shape.

## Implementation sequence

1. Add `.survey/scripts/legacy_inventory.py` with path classification, read-only inventory, and JSON output.
2. Add unit tests under `.survey/tests/`.
3. Extend repository tests to create a temporary inventory report and upload it as a workflow artifact. No report is committed to the repository.
4. Run the focused tests and inspect the artifact. Use its sorted path inventory and legacy text hits to build the next producer/reader/reference contract table.
5. Only after that evidence table is reviewed, plan a separately scoped cleanup batch. Live-state mutation remains gated on a write freeze.

## Acceptance criteria

- The inventory runs on a checkout and produces valid JSON with source SHA, totals, classifications, and marker hits.
- Paper Markdown and queue payload contents do not appear in the report.
- Current fallback inbox paths are classified as live recovery.
- Nothing is automatically deleted, normalized, or rewritten.
- Focused tests and repository regression workflow pass.
