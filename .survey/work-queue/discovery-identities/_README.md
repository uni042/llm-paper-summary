# Discovery identity precheck

This directory is a derived lookup surface for Discovery workers. Exact identity shards are generated from `queue_worker.existing_candidate_keys()` and contain the same identity tokens as the final duplicate gate. `_represented_papers.json` folds the same canonical sources into paper-level alias groups so arXiv/DOI/OpenReview/URL/title representations can be treated as one paper before candidate evaluation.

Workers must check the appropriate shard before accepting a candidate, using the candidate's
strongest available identity in this order: canonical/arXiv ID, DOI, OpenReview ID,
normalized URL, then normalized title. Then use the represented-paper resolver. Exact title
hash matches are deterministic aliases. Fuzzy title matching is allowed only when a provider
result has no stable identifier and first-author plus publication year also agree at a high
confidence threshold. A fuzzy title alone must never discard a paper.

Refresh the latest default-branch HEAD and repeat this check immediately before writing an
immutable Discovery submission.

Do not use GitHub code search as duplicate authority. Code search may be used only for
navigation; a code-search miss does not mean a paper is new.

Shard naming:
- `arxiv-YYMM.txt`: normalized arXiv identity tokens for one arXiv month prefix.
- `doi.txt`, `openreview.txt`, `id-other.txt`: other stable identifier tokens.
- `url-<host>.txt`: normalized URL tokens by host.
- `title-<bucket>.txt`: normalized title tokens by first ASCII letter/digit bucket.
- `_represented_papers.json`: paper-level alias resolver plus conservative title metadata.
- `_manifest.json`: source contract, source commit, token count, resolver metadata, and per-shard counts.

Each `.txt` file contains one exact normalized identity token per line. Do not infer novelty
from a missing GitHub search result; use the exact shards and represented-paper resolver.
