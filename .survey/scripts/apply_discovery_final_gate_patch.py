#!/usr/bin/env python3
"""Temporary bounded patch helper for the feature branch; remove after application."""
from pathlib import Path


path = Path(".survey/scripts/queue_worker.py")
text = path.read_text(encoding="utf-8")

import_old = (
    "import claim_state  # noqa: E402\n"
    "import discovery_search_history  # noqa: E402\n"
)
import_new = (
    "import claim_state  # noqa: E402\n"
    "import discovery_search_history  # noqa: E402\n"
    "import represented_paper_index  # noqa: E402\n"
)
if import_old not in text and import_new not in text:
    raise SystemExit("queue_worker import anchor changed")
text = text.replace(import_old, import_new, 1)

helper_anchor = """    return keys\n\n\ndef make_research_job(c: dict, parent: str):\n"""
helper_replacement = """    return keys\n\n\ndef existing_represented_resolver() -> dict[str, Any]:\n    \"\"\"Build the same represented-paper view used by retrieval-stage prefiltering.\"\"\"\n    records = represented_paper_index.collect_represented_records(ROOT, JOBS)\n    return paper_identity.build_represented_resolver(records)\n\n\ndef make_research_job(c: dict, parent: str):\n"""
if helper_anchor not in text and "def existing_represented_resolver()" not in text:
    raise SystemExit("queue_worker resolver helper anchor changed")
text = text.replace(helper_anchor, helper_replacement, 1)

process_old = """    seen = existing_candidate_keys()\n    added = 0\n    final_duplicate_filtered_count = 0\n    for candidate in sorted(candidates, key=lambda x: int(x.get(\"priority\") or 0), reverse=True):\n        key = candidate_key(candidate)\n        tokens = paper_identity.identity_tokens(candidate)\n        if not key:\n            continue\n        if tokens & seen:\n            final_duplicate_filtered_count += 1\n            continue\n        if int(candidate.get(\"priority\") or 0) < 40:\n            continue\n        if make_research_job(candidate, job[\"job_id\"]):\n            added += 1\n            seen.update(tokens)\n        else:\n            final_duplicate_filtered_count += 1\n"""
process_new = """    seen = existing_candidate_keys()\n    represented_resolver = existing_represented_resolver()\n    accepted_records: list[dict[str, Any]] = []\n    added = 0\n    final_duplicate_filtered_count = 0\n    for candidate in sorted(candidates, key=lambda x: int(x.get(\"priority\") or 0), reverse=True):\n        key = candidate_key(candidate)\n        tokens = paper_identity.identity_tokens(candidate)\n        if not key:\n            continue\n        represented_match = paper_identity.match_represented_paper(candidate, represented_resolver)\n        local_match = None\n        if accepted_records:\n            local_match = paper_identity.match_represented_paper(\n                candidate,\n                paper_identity.build_represented_resolver(accepted_records),\n            )\n        if tokens & seen or represented_match or local_match:\n            final_duplicate_filtered_count += 1\n            continue\n        if int(candidate.get(\"priority\") or 0) < 40:\n            continue\n        if make_research_job(candidate, job[\"job_id\"]):\n            added += 1\n            seen.update(tokens)\n            accepted_records.append(dict(candidate))\n        else:\n            final_duplicate_filtered_count += 1\n"""
if process_old not in text and process_new not in text:
    raise SystemExit("queue_worker process_discovery anchor changed")
text = text.replace(process_old, process_new, 1)

path.write_text(text, encoding="utf-8")
