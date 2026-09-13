# Survey worker lane separation design

## Goal

Reduce Scheduled Chat survey-worker idle time and remove cross-worker head-of-line blocking by separating claim allocation, research/audit submission intake, and heavyweight maintenance/background processing.

The repository remains the canonical source of truth. Scheduled Chat remains responsible for literature discovery, primary-source retrieval, full-text reading, scientific judgment, audit judgment, and structured record authoring. GitHub Actions remains responsible for deterministic validation, rendering, queue/state mutation, duplicate suppression, derived views, and durable publication.

## Current bottlenecks

The current `survey-helper.yml` multiplexes several unrelated responsibilities under the same `survey-helper-main` concurrency group:

- claim allocation
- research/audit submission processing
- fallback dispatch
- offline job materialization
- dedupe/normalization
- queue rebuilds
- blocked retry
- citation refresh
- run-ledger updates
- final commit/push

Maintenance, citation backfill, and paper-index rebuild also share that writer lock. A short claim request can therefore wait behind work that is unrelated to claim allocation.

Research transport also converges on one reusable `chat-inbox.json`, so multiple Scheduled Chat workers cannot independently finish and submit records without contending for the same mutable inbox.

## Chosen architecture

Use three explicit lanes.

### 1. Claim fast lane

A dedicated workflow handles only immutable files under `.survey/work-queue/claim-requests/*.json`.

Responsibilities:

1. checkout latest `main`
2. validate claim-worker syntax
3. run `claim_worker.py`
4. commit only claim results/current-claim state and the minimum queue snapshot changes produced by claim allocation
5. push with bounded refetch/rebase retry
6. exit

It must not run fallback dispatch, research assembly, queue-wide dedupe, blocked retry, citation processing, index rebuilds, or maintenance.

Concurrency group: `survey-claim-main`.

The claim data model continues to enforce one assigned research/audit job per Scheduled Chat worker. A heartbeat for the same request/worker renews the current lease; it is not a request for another job.

### 2. Submission fast lane

Research/audit completion no longer uses a single mutable `chat-inbox.json` as the externally visible submission object. Scheduled Chat creates an immutable submission descriptor per completed attempt, for example:

`.survey/work-queue/submissions/research/<attempt-id>.json`

The descriptor contains:

- schema/transport version
- attempt ID
- job ID
- record bank ID
- five slot paths and exact blob SHAs
- paper path
- expected paper blob SHA when updating an existing page
- status/audit flags
- worker/run attribution metadata

The five record banks A-H remain reusable staging storage. A bank is unavailable while any unresolved immutable submission references its current attempt. Bank selection therefore checks immutable pending submissions/results rather than relying only on the single reusable inbox.

A dedicated submission workflow reacts to immutable research/audit descriptors.

Responsibilities for one immutable submission:

1. checkout latest `main`
2. locate exactly the triggering submission
3. validate that descriptor and its five slot blobs
4. assemble/render that one record
5. verify the job is still valid for the claiming worker/attempt
6. write/update the paper and identity delta
7. transition only that job
8. write an immutable result for that submission
9. refresh the lightweight queue snapshot needed by Scheduled Chat
10. commit/push with refetch/rebase/retry
11. exit

It must not scan/process unrelated submissions, run fallback dispatch, run global citation backfill, rebuild all derived views, or run maintenance.

Concurrency group: `survey-submission-main`.

The submission lane may still serialize GitHub-side publication initially. This is intentional: it removes unrelated heavyweight work from the critical path while retaining a single deterministic writer for paper/job/identity mutation. Scheduled Chat does not wait for terminal Actions status after durably sending a complete payload, so this serialization does not block full-text reading of the next claimed paper.

### 3. Background lane

The existing helper becomes a background/reconciliation workflow. It handles work that is important but not latency-sensitive:

- fallback inbox dispatch/replay
- offline discovery seed materialization
- checkpoint-aware transport requests
- dedupe and ready-job normalization
- blocked retry
- periodic queue reconciliation
- run-ledger reconciliation
- derived view/index rebuilds where appropriate
- citation refresh/backfill triggers

Concurrency group: `survey-background-main`.

Maintenance and citation graph workflows use background-specific groups rather than the claim group. Operations that mutate the same large derived state may still serialize with each other, but cannot block claim allocation.

## Data-flow after the change

```text
Scheduled Chat A -> immutable claim request -> claim-fast -> claim result
                 -> full-text reading
                 -> five slot bank + immutable submission -> submission-fast -> paper/job/result

Scheduled Chat B -> immutable claim request -> claim-fast -> claim result
                 -> full-text reading
                 -> five slot bank + immutable submission -> submission-fast -> paper/job/result

fallback / dedupe / blocked retry / indexes / citation / maintenance
                 -> background lanes
```

## Submission idempotency

Each immutable submission is keyed by a unique attempt ID and job ID. Re-running the same workflow must converge to the same result.

Rules:

- if an immutable result already exists and matches the same attempt/job, the workflow is a no-op
- a terminal job with an existing matching artifact is reconciled to success instead of rendered twice
- a terminal job with a conflicting attempt is rejected as stale
- an existing paper update requires the expected blob SHA
- identity delta generation must succeed before the publication commit is accepted
- if `main` advances during processing, refetch and recompute/revalidate before retrying the push

## Record-bank ownership

The record-bank registry remains A-H.

A bank is `occupied` when any of the following is true:

- its five slots do not form one coherent attempt/job
- an unresolved immutable submission references that attempt and bank
- the associated job is still ready/assigned and the attempt has not been durably submitted

A bank becomes reusable when the immutable result settles the referencing submission or when the complete payload was durably checkpointed to ChatGPT Library and the GitHub staging attempt is no longer authoritative.

Bank exhaustion is not a run-stop condition while Library fallback is writable.

## Queue consistency

Critical queue mutations are split into two categories.

Claim-fast may update only claim ownership/result state and the lightweight `next-jobs.json` snapshot required to make subsequent claims accurate.

Submission-fast may update only the completed job, paper/identity delta, immutable result, state counters needed for completion, and the lightweight queue snapshot.

Global dedupe, blocked retry, discovery-state aggregation, large view rebuilds, citation graph generation, and maintenance stay in the background lane.

## Migration

Migration is staged so current workers keep operating during rollout.

1. Add immutable-submission parsing and single-submission processing helpers with tests.
2. Add bank inspection support for unresolved immutable submissions.
3. Add claim-fast workflow and stop claim-request pushes from triggering the full helper.
4. Add submission-fast workflow and teach Scheduled Chat workflow docs to use immutable submission descriptors.
5. Keep legacy `chat-inbox.json` processing temporarily for already-staged/fallback payloads.
6. Remove research/audit submission and claim triggers from the full helper after fast lanes are verified.
7. Move helper concurrency to `survey-background-main` and update maintenance/citation/index workflow locks so they cannot block claim-fast.
8. After the compatibility window, mark direct new writes to reusable `chat-inbox.json` legacy-only.

No queued job or fallback envelope is discarded during migration.

## Failure handling

- Claim-fast failure affects only claim allocation; existing assigned workers may continue their current paper.
- Submission-fast failure leaves the immutable descriptor and record slots intact for retry.
- Background failure must not block claims or new durable submissions.
- GitHub write failure still uses the canonical ChatGPT Library fallback path.
- Repeated push races trigger refetch/revalidation; they must not silently overwrite newer queue/job/paper state.

## Tests

Add regression coverage for:

1. claim workflow contains no heavyweight helper/background steps
2. one claim request assigns at most one research/audit job
3. a worker with an unresolved assigned job cannot accumulate additional jobs
4. two immutable submission descriptors coexist without overwriting each other
5. processing one immutable submission never processes a second one
6. unresolved immutable submission keeps its record bank occupied
7. settled result releases its bank for reuse
8. legacy `chat-inbox.json` remains replay-compatible during migration
9. submission retry is idempotent after partial/duplicate workflow execution
10. stale expected paper SHA prevents lost updates
11. claim-fast is in a different concurrency group from maintenance/citation/background
12. background reconciliation can rebuild canonical `next-jobs.json` after fast-path updates
13. full repository regression suite passes

## Success criteria

- A claim-only push no longer waits for fallback, citation, maintenance, or queue-wide reconciliation work.
- Claim workflow runtime is dominated by checkout/setup/claim allocation/commit rather than repeated queue rebuilds.
- Research/audit results from different Scheduled Chat workers have distinct immutable descriptors and cannot overwrite one another.
- Heavy background work cannot block new claims.
- Existing fallback and legacy pending work remains recoverable.
- Queue/job/identity/paper state remains deterministic under retry and concurrent `main` advancement.
