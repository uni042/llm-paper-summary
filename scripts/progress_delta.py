#!/usr/bin/env python3
"""Small per-paper progress records for connector-safe survey completion."""
from __future__ import annotations
import argparse, json, os, tempfile
from pathlib import Path
from urllib.parse import quote
import importlib.util

ROOT=Path(__file__).resolve().parents[1]

def load_cycle():
    spec=importlib.util.spec_from_file_location("cycle_state",ROOT/"scripts/cycle_state.py")
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def safe_id(cid:str)->str:
    return quote(cid,safe="._-")

def delta_path(cycle_id:str,side:str,cid:str)->Path:
    return ROOT/"survey-state/progress-deltas"/cycle_id/side/(safe_id(cid)+".json")

def write(path:Path,data:dict):
    path.parent.mkdir(parents=True,exist_ok=True)
    payload=json.dumps(data,ensure_ascii=False,indent=2)+"\n"
    fd,tmp=tempfile.mkstemp(prefix=path.name+".",suffix=".tmp",dir=path.parent)
    try:
        with os.fdopen(fd,"w",encoding="utf-8") as f:
            f.write(payload); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def prepare(side:str,cid:str,status:str,result:str|None,run_id:str,claim_token:str,
            artifact_paths:list[str],verified_commits:list[str],note:str|None,apply:bool):
    cs=load_cycle()
    st=cs.read_json(ROOT/"survey-state/cycle-state.json")
    claim=(st or {}).get("active_claim")
    if not claim or claim.get("run_id")!=run_id or claim.get("claim_token")!=claim_token:
        raise ValueError("progress delta requires current cycle claim")
    summary=cs.apply_progress(ROOT,st)
    items={i.get("canonical_id"):i for i in summary[side]["items"]}
    if cid not in items: raise ValueError("canonical_id is not selected in current plan")
    data={"schema_version":1,"workflow_version":8,"cycle_id":st["cycle_id"],"plan_id":st.get("current_plan_id"),
          "side":side,"canonical_id":cid,"status":status,"run_id":run_id,"run_index":claim["run_index"],
          "claim_token":claim_token}
    if result: data["result"]=result
    if artifact_paths: data["artifact_paths"]=artifact_paths
    if verified_commits: data["verified_commits"]=verified_commits
    if note: data["note"]=note
    path=delta_path(st["cycle_id"],side,cid)
    if path.exists():
        old=json.loads(path.read_text())
        if old.get("status") in {"completed","not_selected","deferred"}:
            raise ValueError("terminal progress delta already exists")
    if apply: write(path,data)
    return {"path":path.relative_to(ROOT).as_posix(),"delta":data}

def main():
    global ROOT
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=ROOT)
    sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("prepare"); a.add_argument("--side",choices=["research","audit"],required=True)
    a.add_argument("--canonical-id",required=True); a.add_argument("--status",choices=["completed","not_selected","deferred","blocked"],required=True)
    a.add_argument("--result"); a.add_argument("--run-id",required=True); a.add_argument("--claim-token",required=True)
    a.add_argument("--artifact",action="append",default=[]); a.add_argument("--verified-commit",action="append",default=[])
    a.add_argument("--note"); a.add_argument("--apply",action="store_true")
    args=p.parse_args(); ROOT=args.root.resolve()
    if args.cmd=="prepare":
        out=prepare(args.side,args.canonical_id,args.status,args.result,args.run_id,args.claim_token,args.artifact,args.verified_commit,args.note,args.apply)
        print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
