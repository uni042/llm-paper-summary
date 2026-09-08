#!/usr/bin/env python3
"""Count-driven survey cycle state for workflow v8.

Control flow is based on GitHub-persisted cycle_id/run_index, never wall-clock time.
A cycle has at most 24 control runs:
  1 = planning
  2..23 = reading/audit
  24 = integrity check and cycle close
If both planned sides are exhausted before run 24, the cycle closes early and the
next cycle starts at run 1 immediately.
"""
from __future__ import annotations
import argparse, json, os, tempfile, uuid
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
TERMINAL = {"completed", "not_selected", "deferred"}

def read_json(path: Path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def atomic_write(path: Path, data: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload=(json.dumps(data, ensure_ascii=False, indent=2)+"\n").encode()
    fd,tmp=tempfile.mkstemp(prefix=path.name+".", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd,"wb") as f:
            f.write(payload); f.flush(); os.fsync(f.fileno())
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def cycle_id(number:int)->str:
    return f"cycle-{number:06d}"

def mode_for(index:int)->str:
    if index == 1: return "planning"
    if index == 24: return "integrity"
    if 2 <= index <= 23: return "reading"
    raise ValueError("run_index must be 1..24")

def progress_files(root:Path, cid:str):
    base=root/"survey-state"/"progress-deltas"/cid
    if not base.exists(): return []
    return sorted(base.rglob("*.json"))

def logical_progress(root:Path, cid:str, plan_path:str|None, targets:dict)->dict:
    if not plan_path:
        return {"research":{"target":int(targets["research"]),"done":0,"pending":0,"items":[]},
                "audit":{"target":int(targets["audit"]),"done":0,"pending":0,"items":[]}}
    plan=read_json(root/plan_path,{}) or {}
    overlays={}
    pfiles=progress_files(root,cid)
    for p in pfiles:
        d=read_json(p,{}) or {}
        overlays[(d.get("side"),d.get("canonical_id"))]=(d,p.relative_to(root).as_posix())
    sides={"research":("selected_papers","target"),"audit":("selected_audits","audit_target")}
    result={}
    for side,(key,target_key) in sides.items():
        items=[]
        for base in plan.get(key,[]):
            item=dict(base)
            entry=overlays.get((side,item.get("canonical_id")))
            if entry:
                d,dpath=entry
                for k,v in d.items():
                    if k not in {"schema_version","workflow_version","side","cycle_id","plan_id"}:
                        item[k]=v
                item["_progress_delta_path"]=dpath
            items.append(item)
        pending=sum(i.get("status") not in TERMINAL for i in items)
        done=sum(i.get("status") in TERMINAL for i in items)
        result[side]={"target":int(plan.get(target_key,targets[side])),"done":done,"pending":pending,"items":items}
    return result

def apply_progress(root:Path, state:dict)->dict:
    return logical_progress(root,state["cycle_id"],state.get("current_plan_path"),state["targets"])

def plan_exhausted(summary:dict)->bool:
    return summary["research"]["pending"]==0 and summary["audit"]["pending"]==0

def next_targets(state:dict, summary:dict, early:bool)->dict:
    if early:
        return {k:max(1,int(state["targets"][k])+1) for k in ("research","audit")}
    return {k:(int(state["targets"][k])+1 if summary[k]["pending"]==0
               else max(1,int(state["targets"][k])-1)) for k in ("research","audit")}

def claim(root:Path, run_id:str, workflow_commit:str, scheduled_at:str|None=None,
          morning_overlay:bool=False, apply:bool=False):
    path=root/"survey-state/cycle-state.json"
    st=read_json(path)
    if not st: raise ValueError("cycle-state.json missing")
    recovery_of=None
    if st.get("active_claim"):
        old=st["active_claim"]; index=int(old["run_index"]); recovery_of=old.get("run_id")
    else:
        index=int(st["next_run_index"])
    token=uuid.uuid4().hex
    rec={"cycle_id":st["cycle_id"],"run_index":index,"run_id":run_id,
         "claim_token":token,"workflow_commit":workflow_commit}
    if recovery_of: rec["recovery_of"]=recovery_of
    st["active_claim"]=rec
    mode=mode_for(index)
    run={"schema_version":1,"workflow_version":8,"run_id":run_id,"cycle_id":st["cycle_id"],
         "run_index":index,"mode":mode,"status":"running","stage":"claimed",
         "claim_token":token,"workflow_commit":workflow_commit}
    if scheduled_at: run["scheduled_at"]=scheduled_at
    if morning_overlay: run["overlays"]=["morning"]
    if recovery_of: run["recovery_of"]=recovery_of
    run_path=root/"survey-state/runs"/f"{run_id}.json"
    if run_path.exists(): raise ValueError("run_id already exists")
    if apply:
        atomic_write(path,st); atomic_write(run_path,run)
    return {"cycle_id":st["cycle_id"],"run_index":index,"mode":mode,"claim_token":token,
            "recovery_of":recovery_of,"morning_overlay":morning_overlay,
            "files_to_publish":["survey-state/cycle-state.json",f"survey-state/runs/{run_id}.json"]}

def _prune_claim_leases(root:Path, token:str, apply:bool)->bool:
    path=root/"survey-state/leases.json"
    data=read_json(path,{"schema_version":2,"workflow_version":8,"items":{}}) or {"schema_version":2,"workflow_version":8,"items":{}}
    items=data.setdefault("items",{})
    remove=[k for k,v in items.items() if v.get("claim_token")==token]
    for k in remove: items.pop(k,None)
    if remove and apply: atomic_write(path,data)
    return bool(remove)

def work_claim(root:Path, resource:str, run_id:str, claim_token:str, action:str, apply:bool=False):
    st=read_json(root/"survey-state/cycle-state.json") or {}
    active=st.get("active_claim") or {}
    if active.get("run_id")!=run_id or active.get("claim_token")!=claim_token:
        raise ValueError("run no longer owns active cycle claim")
    path=root/"survey-state/leases.json"
    data=read_json(path,{"schema_version":2,"workflow_version":8,"items":{}}) or {"schema_version":2,"workflow_version":8,"items":{}}
    data["schema_version"]=2; data["workflow_version"]=8
    items=data.setdefault("items",{})
    if action=="acquire":
        items[resource]={"cycle_id":st["cycle_id"],"run_index":active["run_index"],"run_id":run_id,"claim_token":claim_token}
    elif action=="release":
        cur=items.get(resource)
        if cur and cur.get("claim_token")==claim_token: items.pop(resource,None)
    else: raise ValueError(action)
    if apply: atomic_write(path,data)
    return {"resource":resource,"action":action,"owner":items.get(resource)}

def finish(root:Path, run_id:str, claim_token:str, status:str="completed", apply:bool=False):
    cpath=root/"survey-state/cycle-state.json"
    st=read_json(cpath)
    claimrec=(st or {}).get("active_claim")
    if not claimrec or claimrec.get("claim_token") != claim_token or claimrec.get("run_id") != run_id:
        raise ValueError("run no longer owns active cycle claim")
    idx=int(claimrec["run_index"])
    if idx==1 and status=="completed" and not st.get("current_plan_path"):
        raise ValueError("planning run cannot complete before current_plan_path is set")
    summary=apply_progress(root,st)
    early=idx<24 and idx>=2 and plan_exhausted(summary)
    close=(idx==24 or early)
    run_path=root/"survey-state/runs"/f"{run_id}.json"
    run=read_json(run_path,{}) or {}
    run.update({"status":status,"stage":"finished",
                "progress_summary":{k:{x:summary[k][x] for x in ("target","done","pending")} for k in summary}})
    history=None; files=["survey-state/cycle-state.json",f"survey-state/runs/{run_id}.json"]
    if close:
        targets=next_targets(st,summary,early)
        history={"schema_version":1,"workflow_version":8,"cycle_id":st["cycle_id"],
                 "closed_by_run_id":run_id,"closed_at_run_index":idx,
                 "close_reason":"early_exhausted" if early else "run_24_integrity",
                 "targets":st["targets"],"summary":run["progress_summary"],"next_targets":targets,
                 "plan_path":st.get("current_plan_path")}
        hpath=root/"survey-state/cycle-history"/f'{st["cycle_id"]}.json'
        prev_plan=st.get("current_plan_path"); prev_id=st["cycle_id"]
        number=int(st["cycle_number"])+1
        st={"schema_version":1,"workflow_version":8,"cycle_number":number,"cycle_id":cycle_id(number),
            "max_runs":24,"next_run_index":1,"active_claim":None,"targets":targets,
            "current_plan_id":None,"current_plan_path":None,"previous_plan_path":prev_plan,
            "previous_cycle_id":prev_id,"previous_cycle_summary":history["summary"]}
        run["cycle_closed"]=prev_id; run["next_cycle_id"]=st["cycle_id"]; run["next_run_index"]=1
        if early: run["immediate_next_action"]="claim new cycle run 1 and perform planning in this same scheduled invocation"
        files.append(f"survey-state/cycle-history/{prev_id}.json")
        if apply: atomic_write(hpath,history)
    else:
        st["active_claim"]=None; st["last_completed_run_index"]=idx; st["next_run_index"]=idx+1
        run["next_run_index"]=idx+1
    lease_changed=_prune_claim_leases(root,claim_token,apply)
    if lease_changed: files.append("survey-state/leases.json")
    if apply:
        atomic_write(cpath,st); atomic_write(run_path,run)
    return {"closed":close,"early_rollover":early,"next_cycle_id":st["cycle_id"],
            "next_run_index":st["next_run_index"],"summary":run["progress_summary"],
            "files_to_publish":files}

def planning_seed(root:Path):
    st=read_json(root/"survey-state/cycle-state.json")
    if not st: raise ValueError("cycle-state.json missing")
    if int(st["next_run_index"])!=1 and not ((st.get("active_claim") or {}).get("run_index")==1):
        raise ValueError("planning seed is only valid for run 1")
    result={"cycle_id":st["cycle_id"],"targets":st["targets"],"research":{"carryover":[]}, "audit":{"carryover":[]}}
    prev_id=st.get("previous_cycle_id"); prev_path=st.get("previous_plan_path")
    if prev_id and prev_path:
        hist=read_json(root/"survey-state/cycle-history"/f"{prev_id}.json",{}) or {}
        prev_targets=hist.get("targets",st["targets"])
        prev=logical_progress(root,prev_id,prev_path,prev_targets)
        for side in ("research","audit"):
            carry=[i for i in prev[side]["items"] if i.get("status") not in TERMINAL]
            n=int(st["targets"][side])
            result[side]["carryover"]=carry[:n]
            result[side]["overflow"]=carry[n:]
            result[side]["new_slots"]=max(0,n-len(result[side]["carryover"]))
    else:
        for side in ("research","audit"):
            result[side]["overflow"]=[]; result[side]["new_slots"]=int(st["targets"][side])
    return result

def main():
    p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=ROOT)
    sub=p.add_subparsers(dest="cmd",required=True)
    c=sub.add_parser("claim"); c.add_argument("--run-id",required=True); c.add_argument("--workflow-commit",required=True)
    c.add_argument("--scheduled-at"); c.add_argument("--morning-overlay",action="store_true"); c.add_argument("--apply",action="store_true")
    f=sub.add_parser("finish"); f.add_argument("--run-id",required=True); f.add_argument("--claim-token",required=True)
    f.add_argument("--status",default="completed"); f.add_argument("--apply",action="store_true")
    w=sub.add_parser("lease"); w.add_argument("action",choices=["acquire","release"]); w.add_argument("--resource",required=True)
    w.add_argument("--run-id",required=True); w.add_argument("--claim-token",required=True); w.add_argument("--apply",action="store_true")
    sub.add_parser("status"); sub.add_parser("planning-seed")
    args=p.parse_args(); root=args.root.resolve()
    if args.cmd=="claim": out=claim(root,args.run_id,args.workflow_commit,args.scheduled_at,args.morning_overlay,args.apply)
    elif args.cmd=="finish": out=finish(root,args.run_id,args.claim_token,args.status,args.apply)
    elif args.cmd=="lease": out=work_claim(root,args.resource,args.run_id,args.claim_token,args.action,args.apply)
    elif args.cmd=="planning-seed": out=planning_seed(root)
    else:
        st=read_json(root/"survey-state/cycle-state.json"); out={"cycle_state":st,"progress":apply_progress(root,st)}
    print(json.dumps(out,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
