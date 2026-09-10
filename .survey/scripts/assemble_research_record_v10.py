#!/usr/bin/env python3
"""Workflow-v10 assembler entrypoint with expanded reusable record banks."""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import assemble_research_record as base  # noqa: E402
from record_bank_config import BANK_ROOTS  # noqa: E402

# Keep validation/rendering logic in the canonical assembler while extending the
# pre-created fixed-bank set. This avoids duplicating the quality contract.
base.BANK_ROOTS.clear()
base.BANK_ROOTS.update(BANK_ROOTS)

if __name__ == "__main__":
    raise SystemExit(base.main())
