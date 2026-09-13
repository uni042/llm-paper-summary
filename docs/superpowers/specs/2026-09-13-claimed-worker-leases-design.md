# Claimed Worker Leases Design

## Goal

Allow multiple research and audit workers to run concurrently without assigning the same ready job twice, while preserving GitHub Actions as the only canonical writer and preserving workflow-v10 five-slot transport.

## Approved architecture

- Claims are separate from job lifecycle state. No new `job.status` is introduced.
- Workers submit immutable, uniquely named claim requests. A serialized GitHub Actions allocator writes an idempotent result and one current claim file per assigned job.
- Only ready `research` and `audit` jobs are claimable. Discovery remains outside this allocator and keeps its existing specialist/normal-worker policy.
- A claim is active before `expires_at`. Expiry makes a ready job eligible for reassignment but does not delete the old claim file. The current claim file changes only when a newer assignment replaces it.
- A claimed worker must wait for its claim result before full-text reading. It then emits one immutable fallback-inbox envelope containing the complete five-slot record plus reusable Chat inbox write. It never writes a fixed record bank, paper, queue, identity index, README, or derived state directly.
- Dispatcher acceptance is fenced by the current claim ID. An expired but not superseded claim remains acceptable. A superseded or missing claim is quarantined with a reason. Legacy envelopes without `origin: claimed_worker` retain current behavior.
- The existing dispatcher remaps an accepted immutable record bundle onto a safe A-H record bank and GitHub Actions serially applies canonical changes.
- `next-jobs.json` hides actively claimed research/audit jobs and reports ready total, active claims, and claimable count. Discovery remains visible under the existing priority-window policy.
- Maintenance reconstructs the same claim-aware snapshot. GC preserves the latest claim for every ready job, whether active or expired, and preserves unprocessed requests/results; it may collect retained claim history only after the associated job is terminal and old enough.
- No external database, Redis, message queue, lease renewal, discovery claim, Google Drive fallback, parallel bank writer, or UI redesign is added.

## Data contracts

Claim request files live at `.survey/work-queue/claim-requests/<request_id>.json`, result files at `.survey/work-queue/claim-results/<request_id>.json`, and current job claims at `.survey/work-queue/claims/<job_id>.json`.

Requests use schema version 1, a safe unique request ID, safe worker/session ID, worker kind `scheduled_chat` or `work`, job types limited to `research` and `audit`, `max_jobs` from 1 through 4 with default 1, UTC request time, and lease seconds with default 28800 and an accepted range of 300 through 43200 seconds.

Allocator ordering is priority descending, created time ascending, then job ID ascending. A result that already exists is authoritative and is never expanded or changed on rerun. Claim IDs are deterministic from request ID and job ID.

Claimed envelopes use schema version 1 and carry `origin: claimed_worker`, `job_id`, `claim_id`, `worker_id`, `attempt_id`, dependencies, and complete writes. All IDs use the repository's existing safe ID character policy.

## Failure semantics

- Malformed requests are represented by deterministic result files with no assignments and an explicit error, allowing Actions reruns to converge without blocking later requests.
- A filename/request-ID mismatch, unsafe IDs, unsupported job types or worker kinds, invalid bounds, or invalid timestamps is rejected.
- Multiple requests in one allocator run observe claims written by earlier requests in that run.
- Terminal jobs are never assigned. If a job becomes terminal before envelope dispatch, the envelope is archived as terminal without changing the paper.
- A claimed envelope with a missing current claim or a different current claim ID is quarantined and preserved with an error sidecar; it is never expanded into a record bank.
- Actions reruns reuse existing results and existing deterministic claims. Existing fetch/rebase/push retry remains the GitHub race recovery boundary.
- Dispatcher reruns remain idempotent through immutable inbox/archive IDs and current reusable transport checks.

## Acceptance

The fourteen concurrency, lease, compatibility, record-bank, snapshot, and GC scenarios in the approved request are automated using synthetic temporary repositories. CI compile, YAML parse, the full unittest suite, repository consistency checking, diff checks, and a 2-4 worker simulation must pass without modifying paper content or reintroducing Google Drive.
