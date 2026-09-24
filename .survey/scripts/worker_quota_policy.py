#!/usr/bin/env python3
"""Canonical per-run work quotas for survey workers.

These values are execution-policy constants, not scheduling-capacity limits.
Keep the Research/Audit completion floor and Discovery round floor separate from
the Audit starvation block size: the latter controls mix/fairness, not run
completion.
"""
from __future__ import annotations

RESEARCH_AUDIT_MINIMUM_COMPLETIONS = 5
DISCOVERY_MINIMUM_ROUNDS = 8

# Fairness policy only. This is intentionally independent of the five-completion
# Research/Audit run floor.
AUDIT_STARVATION_BLOCK_SIZE = 3
