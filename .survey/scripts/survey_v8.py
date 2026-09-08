#!/usr/bin/env python3
"""Workflow-v8 build/validate entrypoint.

Keeps legacy deterministic rendering logic, but treats .survey/survey-state as the
management state root and cycle-state + progress deltas as the control truth.
"""
from __future__ import annotations
import argparse
import copy
import json
import sys
from pathlib import Path

MANAGEMENT = Path(__file__).resolve().parents[1]
REPO = MANAGEMENT.parent
SCRIPTS = MANAGEMENT / "scripts"
sys.path.insert(0, str(SCRIPTS))
import survey  # noqa: E402
import cycle_state  # noqa: E402

STATE_REL = ".survey/survey-state/"
STATE_DIR = REPO / STATE_REL


def configure_legacy() -> None:
    survey.ROOT = REPO
    survey.STATE = STATE_REL


def read(path: Path, default=None):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else default


def write(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def logical_identity():
    snapshot = read(STATE_DIR / "paper-identity-index.json", {}) or {}
    papers = copy.deepcopy(snapshot.get("papers", {}))
    aliases = dict(snapshot.get("identifier_to_canonical", {}))
    delta_root = STATE_DIR / "identity-deltas"
    if delta_root.exists():
        for path in sorted(delta_root.rglob("*.json")):
            record = read(path, {}) or {}
            cid = record.get("canonical_id")
            if not cid:
                raise ValueError(f"identity delta missing canonical_id: {path}")
            existing = papers.get(cid)
            if existing and existing.get("path") not in (None, record.get("path")):
                raise ValueError(f"identity path conflict for {cid}")
            base = dict(existing or {})
            base["path"] = record.get("path")
            base["identifiers"] = sorted(set(record.get("identifiers", [])))
            papers[cid] = base
            for ident in base["identifiers"]:
                previous = aliases.get(ident)
                if previous and previous != cid:
                    raise ValueError(f"identifier conflict: {ident} -> {previous}/{cid}")
                aliases[ident] = cid
    return papers, aliases


def v8_dashboard():
    state = read(STATE_DIR / "cycle-state.json", {}) or {}
    progress = cycle_state.apply_progress(MANAGEMENT, state)
    lines = [
        "# サーベイの進捗",
        "",
        f"cycle: `{state.get('cycle_id', '未記録')}` / next run: **{state.get('next_run_index', '未記録')} / 24**",
        "",
        "| 作業 | 完了/決着 | 目標 | 未完了 |",
        "|---|---:|---:|---:|",
    ]
    for side, label in (("research", "精読"), ("audit", "監査")):
        row = progress[side]
        lines.append(f"| {label} | {row['done']} | {row['target']} | {row['pending']} |")
    lines += ["", "## 次の未完了", ""]
    for side, label in (("research", "精読"), ("audit", "監査")):
        for item in progress[side]["items"]:
            if item.get("status") not in cycle_state.TERMINAL:
                lines.append(f"- {label}: {item.get('title', item.get('canonical_id'))}")
    if len(lines) == 10:
        lines.append("未完了なし。")
    (STATE_DIR / "STATUS.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build():
    configure_legacy()
    survey.render()
    v8_dashboard()
    return {"status": "built", "workflow_version": 8}


def validate():
    configure_legacy()
    errors = []
    state = read(STATE_DIR / "cycle-state.json", {}) or {}
    if state.get("workflow_version") != 8:
        errors.append("cycle-state workflow_version is not 8")
    try:
        idx = int(state.get("next_run_index"))
        if not 1 <= idx <= 24:
            errors.append("next_run_index outside 1..24")
    except Exception:
        errors.append("next_run_index invalid")
    plan_path = state.get("current_plan_path")
    if plan_path and not (MANAGEMENT / plan_path).exists():
        errors.append(f"current plan missing: {plan_path}")
    try:
        progress = cycle_state.apply_progress(MANAGEMENT, state)
        for side in ("research", "audit"):
            ids = [x.get("canonical_id") for x in progress[side]["items"]]
            if len(ids) != len(set(ids)):
                errors.append(f"duplicate plan IDs: {side}")
    except Exception as exc:
        errors.append(f"progress invalid: {exc}")
    try:
        logical_papers, aliases = logical_identity()
        expected = {r["canonical_id"]: r for r in survey.papers()}
        for cid, record in expected.items():
            logical = logical_papers.get(cid)
            if not logical:
                errors.append(f"paper missing from logical identity index: {cid}")
            elif logical.get("path") != record.get("path"):
                errors.append(f"identity path mismatch: {cid}")
        for ident, cid in aliases.items():
            if cid not in logical_papers:
                errors.append(f"alias points to missing canonical ID: {ident} -> {cid}")
    except Exception as exc:
        errors.append(f"identity invalid: {exc}")
    delta_root = STATE_DIR / "progress-deltas"
    if delta_root.exists():
        for path in delta_root.rglob("*.json"):
            d = read(path, {}) or {}
            if d.get("workflow_version") != 8 or not d.get("cycle_id") or not d.get("canonical_id"):
                errors.append(f"invalid progress delta: {path.relative_to(REPO)}")
    if errors:
        raise ValueError("\n".join(errors))
    return {"status": "ok", "workflow_version": 8, "papers": len(survey.papers())}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["build", "validate"])
    args = parser.parse_args()
    result = build() if args.command == "build" else validate()
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
