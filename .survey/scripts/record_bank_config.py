#!/usr/bin/env python3
"""Shared workflow-v10 structured-record bank configuration."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY_PATH = HERE.parent / "work-queue" / "records" / "bank-registry.json"


def _load_registry() -> dict:
    value = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("bank-registry.json must contain an object")
    if int(value.get("transport_version") or 0) != 10:
        raise ValueError("bank-registry.json transport_version must be 10")
    banks = value.get("banks")
    slots = value.get("slots")
    if not isinstance(banks, dict) or not banks:
        raise ValueError("bank-registry.json banks must be a non-empty object")
    if not isinstance(slots, list) or not slots:
        raise ValueError("bank-registry.json slots must be a non-empty array")
    return value


REGISTRY = _load_registry()
BANK_ROOTS = {str(k).lower(): str(v) for k, v in REGISTRY["banks"].items()}
BANK_IDS = tuple(BANK_ROOTS)
SLOT_NAMES = tuple(str(slot) for slot in REGISTRY["slots"])

BANK_PATH_PREFIXES = tuple(root.rstrip("/") + "/" for root in BANK_ROOTS.values())


def bank_root(bank: str) -> str:
    bank = bank.lower()
    if bank not in BANK_ROOTS:
        raise ValueError(f"unknown record bank: {bank}")
    return BANK_ROOTS[bank]


def slot_path(bank: str, slot: str) -> str:
    if slot not in SLOT_NAMES:
        raise ValueError(f"unknown record slot: {slot}")
    return f"{bank_root(bank)}/{slot}.json"


def canonical_slot_paths(bank: str) -> dict[str, str]:
    """Return exact paths a worker must use for every slot in a new write."""
    bank = bank.lower()
    bank_root(bank)
    return {slot: slot_path(bank, slot) for slot in SLOT_NAMES}


!/usr/bin/env python3
"""Shared workflow-v10 structured-record bank configuration."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REGISTRY_PATH = HERE.parent / "work-queue" / "records" / "bank-registry.json"


def _load_registry() -> dict:
    value = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("bank-registry.json must contain an object")
    if int(value.get("transport_version") or 0) != 10:
        raise ValueError("bank-registry.json transport_version must be 10")
    banks = value.get("banks")
    slots = value.get("slots")
    if not isinstance(banks, dict) or not banks:
        raise ValueError("bank-registry.json banks must be a non-empty object")
    if not isinstance(slots, list) or not slots:
        raise ValueError("bank-registry.json slots must be a non-empty array")
    return value


REGISTRY = _load_registry()
BANK_ROOTS = {str(k).lower(): str(v) for k, v in REGISTRY["banks"].items()}
BANK_IDS = tuple(BANK_ROOTS)
SLOT_NAMES = tuple(str(slot) for slot in REGISTRY["slots"])

BANK_PATH_PREFIXES = tuple(root.rstrip("/") + "/" for root in BANK_ROOTS.values())


def bank_root(bank: str) -> str:
    bank = bank.lower()
    if bank not in BANK_ROOTS:
        raise ValueError(f"unknown record bank: {bank}")
    return BANK_ROOTS[bank]


def slot_path(bank: str, slot: str) -> str:
    if slot not in SLOT_NAMES:
        raise ValueError(f"unknown record slot: {slot}")
    return f"{bank_root(bank)}/{slot}.json"


def canonical_slot_paths(bank: str) -> dict[str, str]:
    """Return exact paths a worker must use for every slot in a new write."""
    bank = bank.lower()
    bank_root(bank)
    return {slot: slot_path(bank, slot) for slot in SLOT_NAMES}


def accepted_slot_paths(bank: str, slot: str) -> tuple[str, ...]:
    """Return canonical path plus narrowly-scoped historical read aliases."""
    canonical = slot_path(bank, slot)
    legacy_root = LEGACY_BANK_ROOTS.get(bank.lower())
    if legacy_root is None:
        return (canonical,)
    return (canonical, f"{legacy_root}/{slot}.json")
