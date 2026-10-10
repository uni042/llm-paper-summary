# Codex Discovery Backfill: Verified Import Procedure

This runbook documents the official, create-only Discovery intake path for locally screened batches. Keep primary-source screening evidence and the local project contract as the source of truth; do not use obsolete repository-side routing prose to override them.

## Screen and assemble locally

- Pin the ranked-pool source and current main separately. Recheck current-main paper and Research identities, prior local batches, and active candidates before assigning work.
- Screen 50 candidates per batch. Keep candidates with a plausible inference-system efficiency connection for primary-source screening; use title-only unrelated only for clear exclusions.
- Store confirmed identity, exact title, primary URL, paper-specific rationale, and actual UTC retrieval timestamps. If a primary abstract cannot be retrieved, retain the confirmed ID/title/primary URL and exact failure as borderline with source_unavailable; abstract_not_read; body_not_read. Keep unresolved identity separate from formal classifications.
- Complete exact 50-row rank/ID/title parity and independent root validation before assembling upload files. Keep each official Discovery artifact at 20 records or fewer.

## Create-only upload and verification

1. Stage the final JSON from its immutable local source. Verify stage manifest SHA-256, byte count, UTF-8 round trip, schema, and record count. Do not serialize or normalize the JSON after hashing.
2. Confirm the unique destination path is absent on the latest main. Create it once through the Contents API. On an ambiguous response, do not retry the same content.
3. Read the file back at the exact creation commit as base64. Remove only connector-added ASCII whitespace and line wrapping, then compare decoded bytes with the staged source. A successful API response alone is not readback proof.
4. Let the normal importer create waiting state, precheck requests/results, submissions, receipts, Research jobs, and regenerated STATUS.md. Never synthesize these queue or result files.
5. Before the next artifact, verify the source-matched receipt and SHA-256; terminal importer status; precheck decision and filter counts; every submission result; expected per-ID Research jobs and states; and the post-import STATUS.md run pointer and waiting/blocked counts. An imported receipt or ready Research jobs are handoff states, not proof of final paper inclusion.
6. While these official gates run, continue the next local candidate batch in order. Do not send later artifacts until the current part passes all gates, so the waiting queue stays controlled.
7. Diagnose a stall only when the active processor exceeds its declared timeout and no successor or state progress exists. Capture run/job IDs, latest state and time, and recent commits. Then use the authorized read-only gpt-6.1-sol diagnosis; apply only a scoped repair, root-review it, run focused checks, and resume through the same official route.

## Verified end-to-end example: B50/B51 p03, 2026-10-10

- Source SHA-256: 08ebded08f4fb5ea53b822778a3c3beaa306909ff52cfe4bde869d3a878a82fa; create-only commit: 8e4f29f3a978054a7ef03e9e78837597e9ba38de.
- The official precheck became ready at 08:39:11Z: 9 allowed, with zero duplicate filters and zero unresolved identities.
- The exact-source receipt reached imported at 08:51:54Z: 20 records (9 accept, 11 relevance), provider gap 0.
- Two normal submission results covered 5 and 4 candidates, both ok, with zero final duplicate filters and 9 Research jobs added. All nine IDs had matching ready Research jobs.
- Receipt-to-STATUS refresh completed at 08:54:24Z in commit 37bb99bbb77a7f8498b26eaefd51900c1ca5462f. STATUS referenced this p03 receipt and reported zero blocked Codex results.
- Observed elapsed time from create commit (08:28:35Z): 10m36s to precheck, 23m19s to receipt, and 25m49s to STATUS refresh. These are one-run observations, not a latency guarantee or measured improvement.
