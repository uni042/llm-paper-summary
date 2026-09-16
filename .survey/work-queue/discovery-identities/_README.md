# Discovery identity precheck

This directory is a derived lookup surface for Discovery workers. It is generated from
`queue_worker.existing_candidate_keys()`, so it contains the same identity tokens as the final duplicate gate.

Before accepting a candidate, check the appropriate shard using the candidate's strongest
available identity in this order: canonical/arXiv ID, DOI, OpenReview ID, normalized URL,
then normalized title. Refresh the latest default-branch HEAD and repeat this check
immediately before writing an immutable Discovery submission.

Do not use GitHub code search as duplicate authority. Code search may be used only for
navigation; a code-search miss does not mean a paper is new. A candidate whose normalized
identity token is present in a shard is already represented or pending and must be filtered
before submission.

Shard naming:
- `arxiv-YYMM.txt`: normalized arXiv identity tokens for one arXiv month prefix.
- `doi.txt`, `openreview.txt`, `id-other.txt`: other stable identifier tokens.
- `url-<host>.txt`: normalized URL tokens by host.
- `title-<bucket>.txt`: normalized title tokens by first ASCII letter/digit bucket.
- `_manifest.json`: source contract, source commit, token count, and per-shard counts.

Each `.txt` file contains one exact normalized identity token per line. Do not infer
novelty from a missing GitHub search result; check the appropriate shard before accepting a candidate.
