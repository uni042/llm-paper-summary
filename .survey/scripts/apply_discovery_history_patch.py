#!/usr/bin/env python3
"""Temporary bounded patch helper for the feature branch; removed after application."""
from pathlib import Path


path = Path(".survey/scripts/queue_worker.py")
text = path.read_text(encoding="utf-8")

import_old = "import paper_identity  # noqa: E402\nimport survey  # noqa: E402\nimport claim_state  # noqa: E402\n"
import_new = (
    "import paper_identity  # noqa: E402\n"
    "import survey  # noqa: E402\n"
    "import claim_state  # noqa: E402\n"
    "import discovery_search_history  # noqa: E402\n"
)
if import_old not in text and import_new not in text:
    raise SystemExit("queue_worker import anchor changed")
text = text.replace(import_old, import_new, 1)

state_old = "    axes[axis] = summary\n    state[\"axes\"] = axes\n\n    state[\"schema_version\"] = max(int(state.get(\"schema_version\", 2) or 2), 2)\n"
state_new = """    axes[axis] = summary
    state[\"axes\"] = axes

    search_windows = meta.get(\"search_windows\")
    if search_windows is not None:
        if not isinstance(search_windows, list) or any(not isinstance(window, dict) for window in search_windows):
            raise ValueError(\"discovery_stats.search_windows must be a list of objects\")
        discovery_search_history.record_search_windows(
            state,
            search_windows,
            run_key=meta.get(\"run_key\"),
            round_name=meta.get(\"round\"),
        )

    state[\"schema_version\"] = max(int(state.get(\"schema_version\", 2) or 2), 3)
"""
if state_old not in text and state_new not in text:
    raise SystemExit("queue_worker discovery-state anchor changed")
text = text.replace(state_old, state_new, 1)

path.write_text(text, encoding="utf-8")
