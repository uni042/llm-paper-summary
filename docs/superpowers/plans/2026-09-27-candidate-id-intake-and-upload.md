# Feature Implementation Plan: Library Candidate ID Intake and Upload

## Goal

Implement the approved exact-ID intake route, then process every candidate currently in Library accept-candidates.json through the normal Discovery and Research path. Finish each candidate only after one of these outcomes is verified from GitHub main: a normal submission has entered the standard queue, a same-ID canonical paper meets the repository quality bar, or the primary source cannot be verified and that one candidate entry is removed under the user's standing instruction. Preserve unresolved and in-flight candidates.

## Architecture

- Add a bounded schema-v3 request mode for stable identifiers only. Each request has at most 100 IDs and no worker-authored paper records or caller-controlled URLs.
- Resolve arXiv and DOI IDs through the official Semantic Scholar batch endpoint, with an isolated single-ID fallback. Resolve OpenReview IDs through OpenReview's official API/forum path. Normalize provider records and require exact normalized identity equality before a record can proceed.
- Emit one outcome per input ID. Only allowed records enter the existing snapshot/rejection filtering and standard allowed_records/receipt shape. Existing queue-worker provenance and receipt validation remain the submission gate.
- Keep ordinary fixed-source discovery and Scheduled Chat behavior unchanged. Retain the existing push-triggered precheck workflow; use workflow_dispatch with the request path only when a pushed request did not start a run.
- Process the restored 390-ID inventory in bounded requests, submit allowed candidates in normal groups of at most five, and reconcile each terminal outcome against the latest GitHub state before editing the latest Library accept-candidates.json version.

## Tech Stack

Python 3 standard library, existing schema-v3 Discovery scripts and GitHub Actions workflow, unittest, GitHub repository connector, and the Library file connector.

## Spec and Baseline

- Approved design: docs/superpowers/specs/2026-09-27-library-candidate-precheck-design.md
- Repository: uni042/llm-paper-summary, main at 34d2be54bef1f449495d5092349a1207a27fbde1 when this plan was written.
- Existing focused test runner: python -m unittest discover -s .survey/tests -p 'test_*.py'

## Global Constraints

- Follow test-first development for each implementation task: add a failing test, run it to confirm RED, implement the smallest change, then run the focused test to GREEN.
- Never accept records, titles, abstracts, or source URLs supplied by the worker as lookup evidence. Request routing must use fixed, allowlisted public API hosts.
- Exact ID matching is mandatory. A provider miss, mismatch, API outage, active job, or ambiguous existing record must not be treated as a duplicate or as permission to delete a candidate.
- Keep receipt/provenance validation on the normal queue path. Only workflow-produced results and their allowed_records may authorize submissions.
- Before removing an accept-list entry, verify a terminal outcome using current GitHub main and re-read the latest Library version. Modify only completed IDs; preserve unrelated edits and the other two candidate files.
- Record only routes and fallbacks that actually succeed in the Library github-import-procedure.md.
- Use an isolated feature branch/worktree for implementation. Keep each task commit scoped to its listed files.

## Review Focus: Five Failure Modes and Their Tests

1. **False identity match from normalization or provider response.** Adapter tests cover arXiv, DOI and OpenReview identities, canonicalization, exact match, mismatch rejection, and unknown IDs.
2. **Unsafe or oversized request input.** Request tests reject records, arbitrary URLs, malformed IDs, duplicates where unsupported, and more than 100 IDs.
3. **One lookup failure corrupts a batch.** Mixed-result tests verify per-ID success, provider_unresolved, provider_error, and fallback behavior without losing successful IDs.
4. **Snapshot filtering hides why an ID did not proceed.** Filter/processor tests verify per-ID filtered_by_snapshot and intra_batch_duplicate outcomes and preserve those IDs for separate paper/job/rejection reconciliation.
5. **Forged or mismatched results authorize a submission.** Queue-gate tests verify result provenance, request ID, path, receipt, and exact allowed identity membership; normal fixed-source provider tests run as regression coverage.

## Task 1: Add Exact-ID Provider Lookups

Files:
- .survey/scripts/discovery_provider_adapter.py
- .survey/tests/test_discovery_provider_adapter.py

Steps:
1. Add mocked HTTP tests first for Semantic Scholar batch lookup, a single-ID fallback, OpenReview official lookup, unsupported host rejection, and returned-ID mismatch. Confirm the new tests fail before implementation.
2. Add a lookup function that accepts normalized stable IDs and returns provider records associated with their requested IDs. Select fixed endpoints internally; do not accept a URL from the request to determine the host. Retry transient 429/network failures using the adapter's existing bounded retry conventions, and isolate failures by ID.
3. Run: python -m unittest discover -s .survey/tests -p 'test_discovery_provider_adapter.py'
4. Commit: feat: add exact-id discovery lookups

## Task 2: Preserve Per-ID Filter Outcomes

Files:
- .survey/scripts/discovery_search_filter.py
- .survey/tests/test_discovery_precheck_snapshot.py
- .survey/tests/test_discovery_candidate_id_filter.py (new)

Steps:
1. Add tests first for an already represented canonical identity, an alias match, a rejection-ledger match, an unseen ID, and two requested IDs resolving to the same paper. Confirm RED.
2. Add an explicit-ID classification helper that reuses the current snapshot, represented-paper resolver, and rejection ledger, while retaining an outcome row for every input ID. Keep the existing fixed-source filter return behavior unchanged.
3. Run: python -m unittest discover -s .survey/tests -p 'test_discovery_candidate_id_filter.py'
4. Run regression: python -m unittest discover -s .survey/tests -p 'test_discovery_precheck_snapshot.py'
5. Commit: feat: classify exact-id precheck outcomes

## Task 3: Add the Schema-v3 Explicit-ID Processor Path

Files:
- .survey/scripts/process_discovery_precheck.py
- .survey/tests/test_discovery_precheck_schema_contract.py
- .survey/tests/test_discovery_precheck_candidate_ids.py (new)

Steps:
1. Add request-contract tests first. Require the fixed candidate-ID provider/source marker, 1–100 stable IDs, no records or user metadata, and reject arbitrary URL/source overrides, malformed IDs, and wrong schema versions. Confirm RED.
2. Route explicit-ID requests to the adapter and per-ID filter. Emit standard schema-v3 provenance fields plus candidate_statuses for allowed, filtered_by_snapshot, provider_unresolved, provider_error, and intra_batch_duplicate. Generate allowed_records only from exact-ID-matched records that pass filtering. Bind input IDs, statuses, allowed records, and snapshot commit into the receipt. A finite ID request is complete when all requested lookups have a final per-ID outcome; transient errors remain explicit and are not silently retried as misses.
3. Add mixed-batch tests for partial provider outage, fallback success, no matching records, and receipt changes after status or ID changes. Confirm RED before implementation.
4. Run: python -m unittest discover -s .survey/tests -p 'test_discovery_precheck_schema_contract.py'
5. Run: python -m unittest discover -s .survey/tests -p 'test_discovery_precheck_candidate_ids.py'
6. Run fixed-source regression: python -m unittest discover -s .survey/tests -p 'test_discovery_precheck_*.py'
7. Commit: feat: add explicit candidate id precheck

## Task 4: Verify the Existing Submission Gate and Document the Route

Files:
- .survey/tests/test_discovery_precheck_gate.py
- .survey/docs/survey-workflow/worker-router.md
- .github/workflows/discovery-precheck.yml only if an integration check proves the existing triggers cannot process this request mode

Steps:
1. Add queue-gate tests first for a valid workflow-produced explicit-ID result, an ID absent from allowed_records, a changed receipt, a wrong request ID/path, and a hand-authored result. Confirm RED.
2. Keep queue_worker unchanged if the standard result format already passes the existing provenance, receipt and exact-token gate. Change it only to close a demonstrated gap, with the failing gate test first.
3. Document the assistant-only request shape, allowed source routes, per-ID status meanings, primary-source verification, push trigger, workflow_dispatch fallback, and the boundary from Scheduled Chat's ordinary discovery process.
4. Check the workflow's existing push and workflow_dispatch behavior. Do not change workflow configuration if both paths already work.
5. Run: python -m unittest discover -s .survey/tests -p 'test_discovery_precheck_gate.py'
6. Run full suite: python -m unittest discover -s .survey/tests -p 'test_*.py'
7. Commit: docs: document exact-id candidate intake

## Task 5: Process the 390 Library Candidates to Terminal Outcomes

Files:
- Current Library file: /LLM-paper-summary-library-first/discovery-classification/accept-candidates.json
- Procedure to update after verified success: /LLM-paper-summary-library-first/discovery-classification/github-import-procedure.md
- GitHub artifacts: standard discovery-precheck requests/results and discovery submissions/results under .survey/work-queue/

Steps:
1. Re-read the latest accept-candidates.json and confirm its IDs and count before intake. Group IDs into requests of at most 100, preserving each candidate's stable ID and grouping provider-specific lookups through the approved adapter.
2. For each request, verify whether push started the existing workflow. If not, dispatch the existing workflow with that exact request path. Fetch the workflow-produced result from main and verify request ID, receipt, all per-ID outcomes, and allowed_records before evaluation.
3. For every filtered_by_snapshot ID, inspect the canonical paper, active Research jobs, and rejection history separately. A confirmed active job stays in the candidate file until its result is resolved. A complete duplicate is removed only after the same-ID canonical paper passes the quality bar. Repair deficient content at its existing canonical path and re-fetch main to verify the repaired paper.
4. For every allowed ID, verify the primary source itself, then use the standard Research quality path and Discovery submissions of at most five candidates each. Re-fetch main and confirm the canonical paper/job/result status before considering the candidate complete.
5. For provider_unresolved, verify official primary-source routes and distinguish a lasting inability to verify from transient network/API failure. Remove only the individually confirmed unverifiable ID, as already authorized; retain provider_error and all unresolved investigations.
6. After each batch reaches terminal outcomes, re-read the latest Library version and delete only entries whose terminal GitHub state has been verified. Preserve concurrent edits, all pending IDs, and the unrelated/borderline candidate files.
7. Reconcile the final GitHub and Library inventories by stable ID. Report counts for submitted, quality-confirmed existing, removed after primary-source verification failure, active, transiently blocked, and otherwise unresolved. Update github-import-procedure.md with the routes/fallbacks that succeeded and the final verified operating steps.

## Self-Review

- Coverage: every spec change target and every candidate terminal outcome is represented above.
- Ordering: provider lookup precedes snapshot classification; processor and receipt tests precede gate tests; candidate processing and Library edits happen only after the code path passes.
- Interfaces: provider results retain the requested ID; the processor emits standard allowed_records plus explicit statuses; the queue worker remains the authority for result provenance and allowed identity membership.
- Failure coverage: five concrete failure modes have focused tests and the full unittest suite catches regressions.
- Scope: workflow.yml and queue_worker.py change only if a test demonstrates a real integration gap. Candidate processing remains bounded and resumable; errors never trigger candidate deletion.
