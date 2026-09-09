# Queue-based survey workflow v9

This is the authoritative workflow for continuous LLM inference-system paper collection.

## Design goals

- No fixed daily paper quota.
- Quality and relevance dominate volume.
- GitHub Actions owns queue/state transitions and repository publication.
- Chat/Scheduled Task owns literature search, full-text reading, scientific judgment, and audit judgment.
- Chat writes only small immutable submission files. Large completed Markdown may be stored separately as an immutable payload file.
- GitHub Actions runs every 10 minutes and is idempotent.
- Re-running the worker must never double-count or duplicate completed work.

## Pipeline

1. GitHub Actions runs `.survey/scripts/queue_worker.py`.
2. The worker consumes unprocessed files in `.survey/work-queue/submissions/`.
3. It validates and publishes accepted research/audit Markdown.
4. It updates the matching job to a terminal state.
5. It creates follow-up jobs when needed.
6. It writes `.survey/work-queue/next-jobs.json`.
7. Chat reads ready jobs and processes as many as can be safely completed.
8. Chat writes one new submission file per completed job. For large research/audit Markdown, Chat first writes an immutable `.survey/work-queue/payloads/<unique>.md` and the submission references it.
9. The next 10-minute worker run consumes those submissions.

## Discovery lanes

Discovery is decoupled from the 10-minute polling interval.

- `discovery_fresh`: every 2 hours when no outstanding job exists. Search genuinely new inference-system papers and important revisions from primary sources.
- `discovery_citation`: every 6 hours. Follow citations, descendants, follow-up work, and implementations around important papers already in the repository.
- `discovery_gap`: every 24 hours. Search missing lineages and adjacent-system ideas that materially matter to inference systems.

An empty discovery result is valid. Never add a weak paper to satisfy volume.

## Backpressure

The queue is intentionally bounded.

- At most 12 ready research jobs.
- At most 6 ready audit jobs.
- If the research backlog is full, discovery results remain recorded but do not create unlimited reading work.
- Frequent worker polling must not increase discovery frequency.

## Research job

A research job requires reading the primary source in full. The output is a complete Japanese repository page covering at least:

- problem and motivation
- novelty
- system/algorithm design
- hardware/model/dataset conditions
- baselines
- key quantitative results
- quality trade-offs
- memory/I/O effects where relevant
- limitations
- relationship to existing repository lineages
- primary-source evidence

If full text cannot be obtained, return a blocked/deferred result with retrieval evidence. Never infer missing content from abstracts or search snippets.

## Audit job

Formal audit is targeted rather than one-to-one with research.

Generate an audit when any of the following holds:

- priority >= 75
- the research result explicitly requests an audit
- there are uncertainty flags or publication/version questions
- deterministic 20% quality-control sampling selects the paper

Audit checks identity, bibliography, authors/affiliations, publication/final version, code, hardware/model/dataset/baseline details, quoted quantitative results, simulation versus real hardware, classification, differences, and limitations.

## Submission contract

Chat writes one immutable JSON file under:

`.survey/work-queue/submissions/<unique>.json`

Every submission must include `job_id`.

Discovery submission:

```json
{
  "job_id": "job-...",
  "candidates": [
    {
      "canonical_id": "stable id if known",
      "title": "...",
      "source_url": "primary source",
      "paper_path": "papers/...md",
      "priority": 0,
      "reason": "...",
      "evidence": ["..."]
    }
  ]
}
```

Research/audit submission:

```json
{
  "job_id": "job-...",
  "status": "completed",
  "paper_path": "papers/...md",
  "expected_blob_sha": "required when updating an existing paper",
  "payload_path": ".survey/work-queue/payloads/<unique>.md",
  "audit_required": false,
  "audit_reason": null,
  "audit_flags": []
}
```

For research/audit, exactly one of inline `content` or `payload_path` may supply the complete Markdown. Prefer `payload_path` for normal completed paper pages so the JSON stays small. Payload paths must be new immutable `.md` files under `.survey/work-queue/payloads/`. For blocked/deferred/rejected work, omit both and provide `reason`.

## Idempotency and concurrency

- A submission is processed only when the same filename does not already exist in `.survey/work-queue/results/`.
- A terminal job cannot be completed twice.
- GitHub Actions uses a single concurrency group with `cancel-in-progress: false`.
- The worker always checks out the latest `main`.
- Existing paper updates can use `expected_blob_sha` to reject stale writes.
- Worker commits use pull-rebase before push.

## Legacy workflow

Workflow v8 cycle/run/target files are historical compatibility data. They are not the control plane for v9 and fixed targets such as 10/10 or 11/11 must not influence new job generation.

The old helpers remain available for recovery of historical state, but new survey execution follows `.survey/work-queue/`.
