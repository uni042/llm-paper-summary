# Backlog resilience policy

This document is the canonical policy for preventing unsent research results from starving new survey work.

## Core rule

Unsent completed research is a **delivery backlog**, not a reason to stop research. Record banks are temporary staging areas for direct GitHub transport; they are not the durable queue for unsent papers.

When a complete logical research payload cannot be published to GitHub but can be durably saved to the Google Drive outbox, that Drive checkpoint releases the Chat worker from the affected bank/job for purposes of continuing the current run. The GitHub job remains incomplete until Actions later imports and processes the payload.

## Record banks

The pre-created reusable banks are defined by `.survey/work-queue/records/bank-registry.json`. There are eight banks, A through H, each with the same five slots:

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

For direct GitHub transport, use the first bank that is not known to contain the only durable copy of an unfinished attempt. If a complete payload has already been durably checkpointed to Drive, its former bank is no longer considered reserved by that payload.

If all GitHub banks appear dirty or reserved but Drive is writable, **do not stop the run**. Build a complete Drive envelope for the new result and continue to the next independent ready job. Bank exhaustion is therefore a transport-path condition, not a research-capacity limit.

## Drive backlog behavior

Multiple unsent papers may accumulate in `/Google Drive/llm-paper-summary-outbox/pending/`. The count of pending Drive envelopes does not reduce the number of papers the Chat worker may read in the current run.

Research envelopes must contain one complete logical submission: all five record-slot JSON files for exactly one bank plus `chat-inbox.json`. Do not split one paper across multiple Drive envelopes. Completed Markdown must not be stored in the outbox.

The Drive importer drains the backlog separately from the Chat research worker. It imports at most one eligible logical envelope per run. It will not overwrite a reusable Chat inbox whose previous submission has not yet produced a matching result. Invalid envelopes are moved aside and do not block later valid envelopes. A busy research envelope may remain pending while an independent framework/model-update envelope is imported.

This serialization is intentional: several queued envelopes may reference the same reusable bank and the same fixed `chat-inbox.json`; importing more than one at once would collapse them into the final write. One-at-a-time import plus the inbox/result handshake prevents that loss mode.

## Failure handling

A paper-specific GitHub transport failure affects only that paper. After the configured retry and health-probe classification, preserve the complete logical payload in Drive when the canonical workflow permits fallback, then continue independent work.

A growing Drive backlog should be reported for observability but must not by itself trigger `STOP_RUN`. Stop only according to `continuation-policy.json`, especially when completed work cannot be durably preserved anywhere or all remaining work shares a genuine unresolved global dependency.

## Throughput and recovery

The importer is scheduled independently of the hourly Chat worker. Once GitHub transport recovers, it drains old pending envelopes oldest-first subject to the inbox/result gate. Because the research worker can continue producing Drive checkpoints while the importer drains them, temporary GitHub write outages do not turn the reusable record banks into a finite-capacity queue.
