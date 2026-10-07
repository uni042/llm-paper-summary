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


## Under-16KB semantic re-audit queue

`.survey/repair-queue/under-16kb-reaudit.json` is a generated queue for every
paper summary below 16,000 UTF-8 bytes that has not passed the current semantic
re-audit version.

The queue is rebuilt by
`.survey/scripts/refresh_under16kb_reaudit_queue.py` from the current paper
files. Membership is therefore derived state; do not edit entries by hand.

A paper leaves this queue only when all of the following are true:

- frontmatter has
  `under16kb_reaudit_version: "2026-10-07-v1"`
  and `under16kb_reaudit_passed: true`;
- the deterministic explanation checks pass;
- prose Japanese ratio is at least 80% after excluding frontmatter,
  references, URLs, code and other non-explanatory noise.

For inference/training papers the mechanical re-audit floor is body 2,200
characters, method 700 characters and evaluation 500 characters. Survey/review
papers are not forced to satisfy the experimental evaluation-length floor; their
taxonomy, coverage methodology, comparative synthesis and evidence must instead
be checked semantically by the worker.

Each queue entry is assigned stably from `sha256(path)` to one of the three
Scheduled workers and sorted by `file_bytes ASC, path ASC`.

Workers must re-read the primary source. If the current summary is already
semantically sufficient, they may preserve the prose and add the re-audit
attestation. If it is insufficient, they must rewrite the missing explanation
from the primary paper and re-run the same audit until it passes. Failed
intermediate drafts are not published.

The completed Markdown is saved through the normal Library Research lane with
these extra fields:

- `under16kb_reaudit_target_path`
- `under16kb_reaudit_source_sha256`
- `under16kb_reaudit_version`
- `under16kb_reaudit_passed: true`

The GitHub inbox processor only replaces the already represented paper when the
target path matches the resolved identity and the source SHA-256 still matches.
A concurrent edit therefore causes a safe block instead of a stale overwrite.
After a successful replacement the queue is regenerated immediately and the
paper disappears. A quality failure remains both in this queue and, through the
normal `blocked_quality` path, in `returned-research.json` until a corrected
revision passes.
