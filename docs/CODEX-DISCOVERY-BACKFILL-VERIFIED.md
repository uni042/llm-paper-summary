# Verified Discovery backfill upload route

Validated against the B113 p01 import on 2026-10-11. This file records the create-only route and the evidence required before calling a Discovery artifact accepted. A successful Contents write alone is never acceptance proof.

## Before an upload

1. Read the local `PAPER-ADDITION-WORKFLOW.md`; do not use old GitHub workflow documents as the source of procedure. Pin the latest main SHA and matching `STATUS.md`. Wait for relevant Actions writers to finish, then require a five-minute stable main window before current-main eligibility checks.
2. Use a completely classified, rooted and validated Discovery artifact of at most 20 records. Preserve confirmed-identity primary-source retrieval failures as `borderline` with the title, primary URL, and concrete failure. Keep `identity_unresolved` separate and outside formal classifications. Root-review the final packet, ordered IDs, title/reason evidence, classification counts, and staged manifests. Superseded local parts must never be mixed into the upload set.
3. Run the canonical Discovery validator and `stage_upload.py emit`. Strictly decode the emitted base64 and verify UTF-8 roundtrip. Confirm source, staged, and emitted bytes and SHA-256 match exactly. Do not reserialize or normalize JSON.
4. Derive the destination path from the staged manifest and source SHA. On the pinned current main, fetch that exact path and require it to be absent. Only then use GitHub Contents API create-file semantics; never update or overwrite an existing payload.

## Create and verify the write

5. Create one artifact through the official Contents API. Record the returned commit SHA and exact path. At that immutable commit, fetch the same path as base64. Remove only connector-added ASCII space, tab, CR, or LF, then compare the entire base64 payload with `stage_upload.py emit`. Decode both to bytes and compare exact bytes and SHA-256. Any mismatch stops processing.
6. On subsequent current main, locate the durable Discovery receipt by exact `source_sha256` and run key. Require `status=imported`, exact record count, accept/relevance counts, and provider-gap status. Do not infer receipt identity from a filename or aggregate counts alone.
7. Trace the formal precheck to the exact uploaded source. For processor-generated or generic-looking request IDs, apply the pinned processor's deterministic source-token mapping to the exact filename/source SHA; require the derived request ID and run key to equal the durable request. Then require a successful formal precheck (`READY_FOR_EVALUATION`, expected allowed IDs, unresolved/duplicate filters zero), successful submission, and each expected canonical ID in its matching ready Research job.
8. Wait for all relevant receipt, precheck, submission, Research, and STATUS/dashboard writers to terminalize. Read the newly regenerated `STATUS.md` from that fixed main and verify the imported receipt, expected job presence/count, and zero consistency anomalies. Record each durable path, exact source SHA, commit, workflow run/job state, and timestamp. Do not send the next part until this artifact's full gate is complete.

## If a gate fails or appears stalled

- Preserve the payload and evidence. Distinguish a moving `in_progress` step from a stopped gate by comparing repeated UTC observations, active-step progression, run start, declared timeout, and normal duration. Matching IDs or a generic route label alone do not establish lineage.
- If a confirmed ID's primary source cannot be retrieved, keep it `borderline` with title, primary URL, and concrete failure. Do not mark it `unrelated` or `identity_unresolved` merely because the source failed to load.
- Only when acceptance is clearly stalled, request a read-only `gpt-6.1-sol` diagnosis with the exact run/job/step and minimal durable evidence. Root retains implementation, repair, dispatch, upload, and final acceptance decisions. Re-run the relevant focused checks after any repair.

## Verified instance

B113 p01 source SHA-256 `0352f2655c912ecbf121d6569feca9cad0898aef6a86917ce40c0974930e0bc7` was created only at Contents path `.survey/import-inbox/pending/discovery/b113-a68c009-p01--0352f2655c912ecbf121d6569feca9cad0898aef6a86917ce40c0974930e0bc7--b113-part-01.json`, commit `43f2b5f7955a911ee496571c67029dd5ad4b7316`; the fixed-commit full byte readback matched. The exact source-SHA receipt was `imported` with 20 records (2 accept, 18 relevance, provider gap 0). The code-derived precheck was `READY_FOR_EVALUATION` with both accepted IDs allowed and no unresolved/duplicates; its submission succeeded with 2 jobs, both matching Research jobs became ready, and regenerated STATUS had zero consistency anomalies. The complete lineage and fixed-main observations are recorded in local `reports/20261010-main-57470d7-worklist-5000/upload-record.md`.
