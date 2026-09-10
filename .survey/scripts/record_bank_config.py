#!/usr/bin/env python3
"""Shared workflow-v10 structured-record bank configuration."""
from __future__ import annotations

BANK_IDS = tuple("abcdefgh")
SLOT_NAMES = ("metadata", "problem_method", "evaluation", "results", "positioning")


def bank_root(bank: str) -> str:
    bank = bank.lower()
    if bank not in BANK_IDS:
        raise ValueError(f"unknown record bank: {bank}")
    return ".survey/work-queue/records/chat-record" + ("" if bank == "a" else f"-{bank}")


BANK_ROOTS = {bank: bank_root(bank) for bank in BANK_IDS}
BANK_PATH_PREFIXES = tuple(root + "/" for root in BANK_ROOTS.values())


def slot_path(bank: str, slot: str) -> str:
    if slot not in SLOT_NAMES:
        raise ValueError(f"unknown record slot: {slot}")
    return f"{bank_root(bank)}/{slot}.json"
