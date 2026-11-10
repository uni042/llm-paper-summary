#!/usr/bin/env python3
"""Shared worker identity rules for survey Scheduled Chat and ad-hoc workers."""
from __future__ import annotations
import datetime as dt
import re
from typing import Any

FIXED_SCHEDULED_WORKER_SLOTS = {
    "scheduled-chat-00": {"00"},
    "scheduled-chat-30": {"30", "0830"},
}
ADHOC_SLOT = "adhoc"
ADHOC_WORKER_RE = re.compile(r"^worker-[0-9]{1,6}$")
JST = dt.timezone(dt.timedelta(hours=9))
PAPER_SCHEDULE_MINUTES = (0, 30)


def is_adhoc_worker_id(worker_id: Any) -> bool:
    return isinstance(worker_id, str) and ADHOC_WORKER_RE.fullmatch(worker_id) is not None


def is_supported_worker_id(worker_id: Any) -> bool:
    return isinstance(worker_id, str) and (
        worker_id in FIXED_SCHEDULED_WORKER_SLOTS or is_adhoc_worker_id(worker_id)
    )


def allowed_slots(worker_id: Any) -> set[str]:
    if not isinstance(worker_id, str):
        return set()
    if worker_id in FIXED_SCHEDULED_WORKER_SLOTS:
        return set(FIXED_SCHEDULED_WORKER_SLOTS[worker_id])
    if is_adhoc_worker_id(worker_id):
        return {ADHOC_SLOT}
    return set()


def identity_slot_valid(worker_id: Any, scheduled_slot: Any) -> bool:
    return isinstance(scheduled_slot, str) and scheduled_slot in allowed_slots(worker_id)


def next_paper_scheduled_start(actual_invocation_start: dt.datetime, worker_id: str) -> dt.datetime | None:
    """Return the next shared :00/:30 paper-task boundary after this invocation starts.

    Fixed Scheduled Chat workers share the same paper-task cadence, so a late or manual
    invocation must yield to whichever :00/:30 task comes next. Ad-hoc workers have no
    scheduled successor and therefore return None.
    """
    if worker_id not in FIXED_SCHEDULED_WORKER_SLOTS:
        return None
    if actual_invocation_start.tzinfo is None:
        raise ValueError("actual_invocation_start must be timezone-aware")
    local = actual_invocation_start.astimezone(JST)
    if local.minute < 30:
        candidate = local.replace(minute=30, second=0, microsecond=0)
    else:
        candidate = (local.replace(minute=0, second=0, microsecond=0) + dt.timedelta(hours=1))
    return candidate.astimezone(dt.timezone.utc)


def validate_identity_slot(worker_id: str, scheduled_slot: str) -> str:
    if not is_supported_worker_id(worker_id):
        raise ValueError("worker_id must be scheduled-chat-00, scheduled-chat-30, or worker-N")
    if not identity_slot_valid(worker_id, scheduled_slot):
        expected = ", ".join(sorted(allowed_slots(worker_id))) or "none"
        raise ValueError(f"{worker_id} must use scheduled_slot={expected}")
    return scheduled_slot
