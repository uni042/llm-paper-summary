# Submission Recovery Implementation Plan

**Goal:** Make durable Discovery/Research/Audit payloads self-healing after Actions/transport interruptions without re-reading papers or rebinding Research/Audit records to a different job.

## Safety contract

- Discovery root-level submissions may be rebound only from a terminal/missing discovery job to the current eligible discovery job; if none exists, create one first.
- Research/Audit immutable descriptors are permanently bound to their original `job_id` + `attempt_id`; never rebind them to another job.
- Research/Audit content/record-validation failures remain repair work and require a new attempt.
- Only explicitly retryable processing/transport failures may replay the same Research/Audit immutable descriptor.
- Legacy failed results without retryability metadata stay settled for backward compatibility.

## Tasks

1. Add RED regression tests for Discovery stale-job recovery and Research/Audit retryable-failure backlog selection.
2. Add explicit failure classification after immutable-submission isolation and persist `retryable` metadata in exact failure results.
3. Change backlog listing so matching `retryable: true` failures remain unsettled, while success, validation failures, stale-state conflicts, malformed descriptor tombstones, and legacy failures remain settled.
4. Add bounded periodic/self-draining execution to `survey-submission-fast.yml` so retryable descriptors are retried without requiring an unrelated new submission.
5. Make Discovery compatibility submission handling recover stale terminal discovery job references by binding to the single active discovery job or creating one, while preserving the original submitted job id in the result for traceability.
6. Add partial-publication reconciliation where safe: if a Research/Audit descriptor's target paper already equals its exact rendered content, treat the paper write as already applied rather than failing only because the original expected blob changed.
7. Update workflow policy documentation.
8. Run the full repository test workflow, inspect diff, open a PR, verify PR CI, merge to `main`, then verify post-merge CI and current pending backlog state.
