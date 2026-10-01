# Library import inbox

This directory is the GitHub-owned handoff boundary for completed artifacts copied
from ChatGPT Library.

## Contract

The Library uploader does not decide whether an identity is already represented
in the latest main branch. It only copies bytes into one of these create-only
paths and verifies that the GitHub copy matches before deleting the Library
source.

- \`.survey/import-inbox/pending/research/<unique>.md\`
  - one completed Research Markdown
  - the Markdown itself is the payload; do not wrap or rewrite it
- \`.survey/import-inbox/pending/discovery/<unique>.json\`
  - one immutable Discovery-run JSON
  - \`records[]\` contains the run's final \`accept\`, \`unrelated\`, and
    \`borderline\` classifications

Use a collision-resistant filename, preferably
\`<library_file_id>--<original-basename>\`. Never overwrite a different inbox
payload.

## GitHub-owned processing

\`.github/workflows/library-import.yml\` is the single canonical processor workflow.
It runs every 10 minutes from the latest main branch and executes
\`.survey/scripts/process_library_import_inbox.py\` in bounded batches.

### Research

1. Parse and machine-audit the Markdown.
2. Run the repository-wide stable-identity resolver against the current main.
3. If already represented, record \`already_represented\` and do not overwrite
   the existing paper.
4. If not represented, canonicalize the inference lineage, write one paper,
   rerun identity resolution, rebuild derived survey views, and reconcile stale
   ready Research jobs.
5. Quality/import failures are moved to \`blocked/research/\`; successful or
   already-represented pending payloads are removed.

The default semantic operation is therefore **insert-if-absent**. Updating an
already represented paper is a separate explicit maintenance/editing task.

### Discovery

The Library classification is not treated as proof that an item is absent from
GitHub.

- \`accept\` records are converted to the existing schema-v3
  \`candidate_id_lookup\` precheck lane. The workflow-produced precheck result
  decides, from the current repository snapshot, which identifiers are already
  represented or otherwise filtered.
- Only workflow-produced \`allowed_records\` are turned into normal immutable
  \`submit_discovery_round\` submissions, in batches of at most five.
- \`unrelated\` and \`borderline\` records are converted to the existing
  reference-relevance request lane.
- Provider/validation/downstream failures move the original run JSON to
  \`blocked/discovery/\`. Successful runs are removed from \`waiting/discovery/\`
  after all canonical downstream results succeed.

## Ownership and cleanup

Once the uploader has created the exact pending file on GitHub and verified the
handoff, GitHub owns the durable copy. Prefer re-fetching the pending file and
checking byte/hash equality immediately. The processor may advance faster than
the uploader, so a missing pending path is not by itself a failed handoff:

1. check the same filename under \`waiting/\`, \`blocked/\`, or \`retained/discovery-source/\` and compare bytes;
2. otherwise read the predictable \`results/<type>/<pending-stem>.json\` receipt
   and compare its \`source_sha256\` with the Library source SHA-256.

Only one of those verified GitHub-owned representations is needed. After that
the uploader may delete the corresponding Library source without waiting for
final paper/candidate ingestion.

GitHub keeps blocked payloads because the Library copy may already be gone.
Oversized Discovery originals are retained byte-for-byte under
\`retained/discovery-source/\` while bounded chunks are processed. Successful
pending/waiting work payloads are deleted by the processor. Small terminal records
are kept under \`results/\` for auditability.

Do not put hand-written precheck results, queue results, Research jobs, claims,
or relevance ledgers into this inbox.

## Maintenance artifacts from the same Library uploader

The same `Survey GitHub Import` run also collects completed 08:30 LLM/framework
maintenance artifacts from ChatGPT Library, but they **do not enter this inbox**.
Research and Discovery keep using the paths documented above. Maintenance updates
use the existing bounded update lane:

1. read `/LLM-paper-summary-library-first/maintenance/llm-framework-update-*.md`
   oldest `checked_at` first;
2. re-read the current `framework-updates/**` / `llm-releases/**` target blobs;
3. construct one `kind: framework_llm_update` payload at
   `.survey/update-worker/update-payload.json` using only targets allowed by
   `.survey/scripts/update_worker.py`;
4. write/update `.survey/update-worker/update-inbox.json` **after** the payload
   with the same unique `attempt_id`; this push triggers `.github/workflows/update-helper.yml`;
5. confirm `.survey/update-worker/result.json` has the same `attempt_id` and
   `ok=true`, then re-fetch the updated target files from current main;
6. only after those checks may the uploader delete that maintenance Library source.

Maintenance artifacts are processed serially because the update lane has fixed reusable
`payload` / `inbox` / `result` paths. If an artifact was based on an older blob, the
uploader may rebase its intended edit onto current main only when the edit remains
unambiguous and does not overwrite unrelated changes. Already-represented changes are
treated as a verified no-op. Ambiguous or conflicting edits remain in Library for
manual repair; do not force them through by replacing whole files from a stale base.
