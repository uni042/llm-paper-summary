# Discovery continuation policy

This policy governs **discovery continuation** for both the hourly discovery-specialist worker and the discovery phase of the normal paper worker. It supplements `candidate-buffer-policy.md`; it does not remove discovery from the normal worker.

## Goal

Discovery should keep producing strong research candidates for as long as productive work remains possible. A weak or empty search round is a signal to change search strategy, not a run-level stop condition.

## Non-stop conditions

None of the following, by itself, ends discovery for the run:

- one search axis returns zero useful candidates;
- one axis returns only duplicates;
- one axis has low acceptance rate or high duplicate rate;
- `candidate_inventory` is already large;
- one search source/API/query fails;
- one candidate has inaccessible full text or insufficient evidence;
- one candidate is rejected as weak or out of scope;
- one GitHub write conflicts with concurrent work;
- one fallback replay/save operation fails while another durable route remains available;
- one discovery submission reaches its per-submission candidate limit.

When any of these happens, preserve useful state and continue by changing axis, query, source, citation direction, or adjacent field. There is no fixed number of discovery rounds, total candidates, or candidate-inventory target per Scheduled Chat run.

## Search-space rotation

Use multiple independent routes rather than retrying a depleted query mechanically:

1. new papers / recent revisions;
2. forward citations of collected or important papers;
3. backward references from important papers;
4. adjacent systems fields such as DBMS, OS, storage, distributed systems, HPC, GPU runtime, networking, and memory systems;
5. query expansion from titles, abstracts, keywords, and terminology of recently successful candidates;
6. priority themes: offload, hierarchical memory, SSD/NVMe, MoE expert placement/cache/prefetch, KV cache, scheduling, disaggregation, and inference frameworks.

Read `discovery-state.json` before choosing axes. Prefer axes with useful historical yield, but retain exploration of under-sampled axes. Do not overreact to a 0% or 100% rate based on only one or two candidates.

## Candidate quality

There is no inventory target, quota, or cap. Do not lower the quality bar to fill inventory. Candidate selection may consider relevance, novelty, difference from collected work, real measured evaluation, implementation availability, citation value, and usefulness to the project’s priority themes.

Discovery remains a lightweight stage: inspect title, abstract, bibliographic metadata, primary-source availability, duplicate status, and likely relevance. Full primary-source reading belongs to research. Do not infer research claims from snippets alone.

## Durability and concurrency

Before candidate submission, re-check the latest canonical identity/queue state. Concurrent discovery that finds the same paper must converge through canonical-ID / arXiv / DOI / OpenReview / normalized-title deduplication rather than producing intentional duplicate jobs.

Use GitHub direct persistence when available. If GitHub writes are unavailable but ChatGPT Library `/LLM-survey-outbox/pending/` can durably store a complete offline seed/envelope, continue discovery and persist there. Google Drive, Notion, and the old Library fallback are not active routes.

Every discovery round should submit `discovery_stats` so Actions can record evaluated candidates, pre-submit duplicates, final accepted count, axis/query, and the next-axis hint.

## Run-level stop conditions

Discovery may stop only when one of these is true:

1. the canonical repository/rules cannot be read well enough to search safely;
2. neither GitHub nor the approved Library fallback can durably preserve required candidate state;
3. the execution environment reaches a hard platform/runtime/tool limit that prevents further useful work;
4. the worker has reasonably exhausted the currently promising search space **after trying varied independent axes/sources**, and records what was attempted and why further rounds are unlikely to add value in this run.

A single empty round, all-duplicate round, large candidate inventory, or transient source failure never satisfies condition 4.

## Worker roles

- The discovery-specialist worker performs discovery only and does **not** increment the normal 24-run maintenance counter. Candidate inventory size does not throttle this worker.
- The normal paper worker retains its own discovery capability and follows this same continuation policy during any discovery phase, but `candidate-buffer-policy.md` controls when research should take priority over discovery.
- The specialist supplements the normal worker; it never assumes exclusive ownership of discovery.
