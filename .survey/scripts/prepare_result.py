#!/usr/bin/env python3
"""Prepare small publication-state files from a paper and the active workflow-v8 claim.

This helper does not publish to GitHub. It creates/validates identity and progress
deltas locally so the caller can commit them with the paper artifact.
"""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def prepare(root: Path, side: str, paper: str, status: str, result: str | None, note: str | None, apply: bool):
    cycle = load("cycle_state", root / "scripts/cycle_state.py")
    progress = load("progress_delta", root / "scripts/progress_delta.py")
    identity = load("identity_delta", root / "scripts/identity_delta.py")
    progress.ROOT = root
    identity.ROOT = root
    identity.survey.ROOT = root

    state = cycle.read_json(root / "survey-state/cycle-state.json") or {}
    claim = state.get("active_claim") or {}
    if not claim.get("run_id") or not claim.get("claim_token"):
        raise ValueError("active workflow-v8 claim required")

    record = identity.paper_record(paper)
    cid = record["canonical_id"]
    artifacts = [paper]
    identity_path = None
    if side == "research":
        identity.assert_no_conflicts(record)
        identity_path = identity.delta_path(cid)
        artifacts.append(identity_path)
        if apply:
            target = root / identity_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    prepared = progress.prepare(
        side=side,
        cid=cid,
        status=status,
        result=result,
        run_id=claim["run_id"],
        claim_token=claim["claim_token"],
        artifact_paths=artifacts,
        verified_commits=[],
        note=note,
        apply=apply,
    )
    return {
        "cycle_id": state.get("cycle_id"),
        "run_id": claim["run_id"],
        "run_index": claim["run_index"],
        "claim_token": claim["claim_token"],
        "side": side,
        "canonical_id": cid,
        "identity_delta": identity_path,
        "progress_delta": prepared["path"],
        "files_to_publish": artifacts + [prepared["path"]],
    }


def main():
    global ROOT
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--side", choices=["research", "audit"], required=True)
    p.add_argument("--paper", required=True)
    p.add_argument("--status", choices=["completed", "not_selected", "deferred", "blocked"], default="completed")
    p.add_argument("--result", default="added")
    p.add_argument("--note")
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    ROOT = args.root.resolve()
    print(json.dumps(prepare(ROOT, args.side, args.paper, args.status, args.result, args.note, args.apply), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
