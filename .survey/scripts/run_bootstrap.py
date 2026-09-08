#!/usr/bin/env python3
"""Survey startup aggregator for workflow v8.

The control mode comes only from survey-state/cycle-state.json:
run 1 planning, runs 2-23 reading/audit, run 24 integrity.
Time is metadata only. --morning-overlay preserves the external 08:30 reporting/update
condition without changing cycle control.
"""
from __future__ import annotations
import argparse, importlib.util, json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load_cycle(root:Path):
    spec=importlib.util.spec_from_file_location("cycle_state",root/"scripts/cycle_state.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--root",type=Path,default=ROOT)
    p.add_argument("--run-id",required=True)
    p.add_argument("--workflow-commit",required=True)
    p.add_argument("--scheduled-at")
    p.add_argument("--morning-overlay",action="store_true")
    p.add_argument("--apply",action="store_true")
    a=p.parse_args(); root=a.root.resolve()
    mod=load_cycle(root)
    out=mod.claim(root,a.run_id,a.workflow_commit,a.scheduled_at,a.morning_overlay,a.apply)
    out["control_source"]="survey-state/cycle-state.json"
    out["time_controls_mode"]=False
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
