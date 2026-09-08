#!/usr/bin/env python3
"""Emit deterministic next work and an end-of-step continuation directive."""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TERMINAL = {"completed", "not_selected", "deferred"}


def load_cycle(root: Path):
    spec = importlib.util.spec_from_file_location("cycle_state", root / "scripts/cycle_state.py")
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def first_pending(items):
    for item in items:
        if item.get("status") not in TERMINAL:
            return item
    return None


def choose(summary):
    r, a = summary["research"], summary["audit"]
    if r["pending"] == 0 and a["pending"] == 0:
        return None
    if r["pending"] == 0:
        side = "audit"
    elif a["pending"] == 0:
        side = "research"
    else:
        rr = r["done"] / max(1, r["target"])
        ar = a["done"] / max(1, a["target"])
        side = "research" if rr <= ar else "audit"
    item = first_pending(summary[side]["items"])
    if not item:
        return None
    return {
        "side": side,
        "canonical_id": item.get("canonical_id"),
        "title": item.get("title"),
        "source_url": item.get("source_url"),
        "next_action": item.get("next_action") or ("perform formal audit" if side == "audit" else "read primary source in full"),
    }


def processed_in_active_run(root: Path, state: dict) -> int:
    claim = state.get("active_claim") or {}
    run_id = claim.get("run_id")
    if not run_id:
        return 0
    path = root / "survey-state/runs" / f"{run_id}.json"
    if not path.exists():
        return 0
    try:
        run = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    return len(run.get("processed") or [])


def continuation(state: dict, summary: dict, recommendation: dict | None, root: Path):
    claim = state.get("active_claim")
    exhausted = summary["research"]["pending"] == 0 and summary["audit"]["pending"] == 0
    if not claim:
        return {
            "action": "claim_next_run",
            "optional": False,
            "reason": "no active claim; normal work must start by claiming cycle-state.next_run_index",
        }
    run_index = int(claim.get("run_index", state.get("next_run_index") or 0))
    if run_index == 24:
        return {
            "action": "integrity_only",
            "optional": False,
            "reason": "run 24 is reserved for integrity/compaction/repair and cycle closing",
        }
    if exhausted:
        return {
            "action": "close_cycle",
            "optional": False,
            "reason": "research and audit plans are both terminal; close early instead of consuming more run indices",
        }
    if recommendation:
        return {
            "action": "continue_same_run",
            "optional": True,
            "reason": "another selected item is ready; continue immediately when execution capacity and safe access remain",
            "processed_in_this_run": processed_in_active_run(root, state),
            "next": recommendation,
            "fallback": "finish_run_without_advancing_extra_work; the next scheduled run will claim the following run index and resume from the same logical progress",
        }
    return {
        "action": "finish_run",
        "optional": False,
        "reason": "no deterministic next selected item is available",
    }


def status(root: Path):
    cs = load_cycle(root)
    st = cs.read_json(root / "survey-state/cycle-state.json")
    if not st:
        raise ValueError("cycle-state.json missing")
    summary = cs.apply_progress(root, st)
    rec = choose(summary)
    return {
        "cycle_id": st["cycle_id"],
        "next_run_index": st.get("next_run_index"),
        "active_claim": st.get("active_claim"),
        "progress": {k: {x: summary[k][x] for x in ("target", "done", "pending")} for k in ("research", "audit")},
        "plan_exhausted": summary["research"]["pending"] == 0 and summary["audit"]["pending"] == 0,
        "recommended": rec,
        "after_action": continuation(st, summary, rec, root),
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    print(json.dumps(status(args.root.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
