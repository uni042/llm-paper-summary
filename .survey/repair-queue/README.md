# Returned Research repair queue

`.survey/repair-queue/returned-research.json` is a generated, durable queue for
Research artifacts rejected by the GitHub Library import quality gate.

## Source of truth

The queue is rebuilt by `.survey/scripts/process_library_import_inbox.py` from
Research import receipts under `.survey/import-inbox/results/research/`.

For each `canonical_id`, only the newest relevant terminal receipt is used.

- newest status `blocked_quality` -> the paper is present in the queue
- newer status `imported` or `already_represented` -> the paper is removed
- repeated `blocked_quality` receipts increase `return_count`

Do not edit queue entries by hand.

## Deterministic worker ownership

Each entry has exactly one `assigned_worker` selected by:

`sha256(canonical_id)[0] mod 3`

The slots are, in order:

1. `scheduled-chat-00`
2. `scheduled-chat-30`
3. `scheduled-chat-45`

This assignment is stable even when queue membership changes, so independent
workers do not need a shared claim ledger.

## Worker priority

A Scheduled worker reads this queue before normal Research/Discovery mode
selection.  It processes only entries assigned to itself, oldest
`returned_at` first.

Before repairing an entry, the worker checks ChatGPT Library `research/*.md`
for the same canonical identity.  If a repaired artifact is already waiting for
upload, the worker leaves the GitHub queue entry alone and does not repair the
paper again.

A repair must reread the primary paper and fix the actual missing explanation;
padding only to pass the mechanical character floor is not acceptable.  The
repaired Markdown goes through the normal Research quality preflight and is
saved to Library under a new unique filename.  The next Library import attempt
will either clear the queue entry on success or update it with another return.
