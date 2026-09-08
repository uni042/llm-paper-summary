#!/usr/bin/env python3
"""Emit the next deterministic survey work item for workflow v8."""
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
        # Prefer the side with lower normalized completion. Ties prefer research.
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
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    print(json.dumps(status(args.root.resolve()), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
