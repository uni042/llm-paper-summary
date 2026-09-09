#!/usr/bin/env python3
"""Queue-oriented survey state worker (workflow v9).

GitHub Actions owns queue/state transitions. Chat owns research judgment and writes
small immutable submission JSON files. No daily paper quota is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "work-queue"
JOBS = QUEUE / "jobs"
SUBMISSIONS = QUEUE / "submissions"
RESULTS = QUEUE / "results"
STATE = QUEUE / "state.json"
ARCHIVE = QUEUE / "archive"

TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent"}
LANE_TARGETS = {
    "discovery_fresh": 1,
    "discovery_citation": 1,
    "discovery_gap": 1,
}
MAX_READY_RESEARCH = 12
MAX_READY_AUDIT = 6
DISCOVERY_REFRESH_HOURS = 6


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default: Any = None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stable_id(prefix: str, *parts: str) -> str:
    h = hashlib.sha256("\n".join(parts).encode()).hexdigest()[:16]
    return f"{prefix}-{h}"


def iter_jobs():
    JOBS.mkdir(parents=True, exist_ok=True)
    for p in sorted(JOBS.glob("*.json")):
        j = read_json(p, {})
        j["_path"] = p
        yield j


def load_state():
    st = read_json(STATE)
    if st:
        return st
    st = {
        "schema_version": 1,
        "workflow_version": 9,
        "mode": "queue",
        "created_at": now(),
        "updated_at": now(),
        "policy": {
            "fixed_daily_quota": False,
            "quality_over_quantity": True,
            "max_ready_research": MAX_READY_RESEARCH,
            "max_ready_audit": MAX_READY_AUDIT,
            "discovery_refresh_hours": DISCOVERY_REFRESH_HOURS,
        },
        "stats": {
            "discovered": 0,
            "selected": 0,
            "research_completed": 0,
            "audit_completed": 0,
            "rejected": 0,
        },
    }
    write_json(STATE, st)
    return st


def save_state(st):
    st["updated_at"] = now()
    write_json(STATE, st)


def add_job(job: dict):
    jid = job["job_id"]
    p = JOBS / f"{jid}.json"
    if p.exists():
        return False
    job.setdefault("schema_version", 1)
    job.setdefault("workflow_version", 9)
    job.setdefault("status", "ready")
    job.setdefault("created_at", now())
    job.setdefault("priority", 50)
    write_json(p, job)
    return True


def update_job(job: dict):
    p = job.pop("_path", JOBS / f"{job['job_id']}.json")
    write_json(Path(p), job)


def active_jobs(job_type=None, lane=None):
    out = []
    for j in iter_jobs():
        if j.get("status") in TERMINAL:
            continue
        if job_type and j.get("type") != job_type:
            continue
        if lane and j.get("lane") != lane:
            continue
        out.append(j)
    return out


def ensure_discovery_jobs(st):
    prompts = {
        "discovery_fresh": "Find genuinely new inference-system papers or important revisions from primary sources. Prefer papers not already represented in the repository.",
        "discovery_citation": "Follow citations, follow-up work, and descendant papers from important inference-system papers already in the repository. Return only candidates with meaningful system-level relevance.",
        "discovery_gap": "Search for missing lineages or adjacent-system techniques that plausibly matter to LLM inference systems. Prefer high-impact gaps over novelty for its own sake.",
    }
    history = st.setdefault("discovery_lanes", {})
    current_time = datetime.now(timezone.utc)
    for lane, target in LANE_TARGETS.items():
        current = active_jobs("discovery", lane)
        last = history.get(lane, {}).get("last_issued_at")
        due = True
        if last:
            try:
                last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
                due = (current_time - last_dt).total_seconds() >= DISCOVERY_REFRESH_HOURS * 3600
            except Exception:
                due = True
        if current or not due:
            continue
        while len(current) < target:
            issued = now()
            jid = stable_id("job", lane, issued, str(len(current)))
            add_job({
                "job_id": jid,
                "type": "discovery",
                "lane": lane,
                "priority": 80 if lane == "discovery_fresh" else 60,
                "instructions": prompts[lane],
                "completion": "Submit 0 or more candidates. Empty is valid when no strong candidates are found; never fill a quota with weak papers.",
                "output_schema": {
                    "operation": "discovery_result",
                    "job_id": jid,
                    "candidates": [{
                        "canonical_id": "preferred stable ID if known",
                        "title": "paper title",
                        "source_url": "primary source URL",
                        "paper_path": "planned papers/...md path if selected",
                        "priority": "0-100",
                        "reason": "why it deserves full reading",
                        "evidence": ["primary-source facts used for selection"]
                    }]
                },
            })
            history[lane] = {"last_issued_at": issued}
            current = active_jobs("discovery", lane)


def candidate_key(c: dict) -> str:
    return str(c.get("canonical_id") or c.get("source_url") or c.get("title") or "").strip().lower()


def existing_candidate_keys():
    keys = set()
    for j in iter_jobs():
        for k in ("canonical_id", "source_url", "title"):
            v = j.get(k)
            if v:
                keys.add(str(v).strip().lower())
    return keys


def make_research_job(c: dict, parent: str):
    key = candidate_key(c)
    if not key:
        return False
    jid = stable_id("job-research", key)
    return add_job({
        "job_id": jid,
        "type": "research",
        "parent_job_id": parent,
        "priority": int(c.get("priority") or 50),
        "canonical_id": c.get("canonical_id"),
        "title": c.get("title"),
        "source_url": c.get("source_url"),
        "paper_path": c.get("paper_path"),
        "selection_reason": c.get("reason"),
        "status": "ready",
        "instructions": "Read the primary source in full. Produce a repository-quality Japanese paper page covering problem, novelty, method, evaluation conditions, key quantitative results, limitations, and relation to existing repository lineages. Do not infer missing text from abstracts/search snippets.",
        "completion": "Return complete Markdown and source evidence. If full text is unavailable, return blocked with retrieval evidence instead of guessing.",
    })


def make_audit_job(sub: dict, research_job: dict):
    # Audits are conditional, not one-for-one. Trigger when uncertainty/important
    # publication-state checks are explicitly requested by the research result.
    need = sub.get("audit_required")
    if not need:
        return False
    key = str(research_job.get("canonical_id") or research_job.get("job_id"))
    jid = stable_id("job-audit", key)
    return add_job({
        "job_id": jid,
        "type": "audit",
        "priority": max(40, int(research_job.get("priority") or 50)),
        "canonical_id": research_job.get("canonical_id"),
        "title": research_job.get("title"),
        "source_url": research_job.get("source_url"),
        "paper_path": research_job.get("paper_path"),
        "reason": sub.get("audit_reason") or "research result requested formal audit",
        "instructions": "Perform a formal audit using primary sources: identity/bibliography, authors/affiliations, publication state/final version, code, hardware/model/dataset/baselines, quoted quantitative results, simulation vs real hardware, classification, differences and limitations. Update the full Markdown page.",
    })


def process_discovery(sub: dict, job: dict, st: dict):
    candidates = sub.get("candidates") or []
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    seen = existing_candidate_keys()
    added = 0
    for c in sorted(candidates, key=lambda x: int(x.get("priority") or 0), reverse=True):
        if len(active_jobs("research")) >= MAX_READY_RESEARCH:
            break
        key = candidate_key(c)
        if not key or key in seen:
            continue
        if int(c.get("priority") or 0) < 40:
            continue
        if make_research_job(c, job["job_id"]):
            added += 1
            seen.add(key)
    job["status"] = "completed"
    job["completed_at"] = now()
    job["result_summary"] = {"submitted_candidates": len(candidates), "research_jobs_added": added}
    st["stats"]["discovered"] += len(candidates)
    st["stats"]["selected"] += added


def process_research(sub: dict, job: dict, st: dict):
    status = sub.get("status", "completed")
    if status == "completed":
        content = sub.get("content")
        if not isinstance(content, str) or len(content.strip()) < 500:
            raise ValueError("completed research requires complete Markdown content")
        job["status"] = "completed"
        job["completed_at"] = now()
        job["artifact_submission"] = sub.get("_file")
        st["stats"]["research_completed"] += 1
        make_audit_job(sub, job)
    elif status in {"blocked", "deferred", "rejected"}:
        job["status"] = status
        job["completed_at"] = now()
        job["blocker"] = sub.get("reason")
        if status == "rejected":
            st["stats"]["rejected"] += 1
    else:
        raise ValueError("invalid research status")


def process_audit(sub: dict, job: dict, st: dict):
    status = sub.get("status", "completed")
    if status == "completed":
        content = sub.get("content")
        if not isinstance(content, str) or len(content.strip()) < 500:
            raise ValueError("completed audit requires complete Markdown content")
        job["status"] = "completed"
        job["completed_at"] = now()
        job["artifact_submission"] = sub.get("_file")
        st["stats"]["audit_completed"] += 1
    elif status in {"blocked", "deferred", "rejected"}:
        job["status"] = status
        job["completed_at"] = now()
        job["blocker"] = sub.get("reason")
    else:
        raise ValueError("invalid audit status")


def apply_artifact(sub: dict, job: dict):
    """Publish research/audit Markdown if supplied, with optimistic SHA check."""
    if job.get("type") not in {"research", "audit"} or sub.get("status", "completed") != "completed":
        return None
    paper = sub.get("paper_path") or job.get("paper_path")
    if not paper or not str(paper).startswith("papers/") or ".." in Path(paper).parts:
        raise ValueError("safe papers/... paper_path required")
    content = sub["content"].rstrip() + "\n"
    target = ROOT.parent / paper
    expected_sha = sub.get("expected_blob_sha")
    if target.exists() and expected_sha:
        import subprocess
        p = subprocess.run(["git", "rev-parse", f"HEAD:{paper}"], cwd=ROOT.parent, text=True, capture_output=True)
        current = p.stdout.strip() if p.returncode == 0 else None
        if current != expected_sha:
            raise ValueError(f"paper blob changed: expected {expected_sha}, current {current}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return paper


def process_submissions(st: dict):
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for p in sorted(SUBMISSIONS.glob("*.json")):
        rp = RESULTS / p.name
        if rp.exists():
            continue
        result = {"schema_version": 1, "workflow_version": 9, "submission": str(p.relative_to(ROOT)), "ok": False}
        try:
            sub = read_json(p, {})
            sub["_file"] = str(p.relative_to(ROOT))
            jid = sub.get("job_id")
            if not jid:
                raise ValueError("job_id required")
            jp = JOBS / f"{jid}.json"
            if not jp.exists():
                raise ValueError("unknown job_id")
            job = read_json(jp, {})
            job["_path"] = jp
            if job.get("status") in TERMINAL:
                raise ValueError(f"job already terminal: {job.get('status')}")
            if job["type"] == "discovery":
                process_discovery(sub, job, st)
                artifact = None
            elif job["type"] == "research":
                artifact = apply_artifact(sub, job)
                process_research(sub, job, st)
            elif job["type"] == "audit":
                artifact = apply_artifact(sub, job)
                process_audit(sub, job, st)
            else:
                raise ValueError(f"unsupported job type: {job.get('type')}")
            update_job(job)
            result.update({"ok": True, "job_id": jid, "job_type": job["type"], "artifact": artifact, "job_status": job.get("status")})
        except Exception as exc:
            result["error"] = f"{type(exc).__name__}: {exc}"
        write_json(rp, result)


def queue_snapshot():
    jobs = list(iter_jobs())
    counts = {}
    for j in jobs:
        counts.setdefault(j.get("type", "unknown"), {})
        s = j.get("status", "unknown")
        counts[j["type"]][s] = counts[j["type"]].get(s, 0) + 1
    ready = [j for j in jobs if j.get("status") == "ready"]
    ready.sort(key=lambda j: (-int(j.get("priority") or 0), j.get("created_at", "")))
    return {
        "generated_at": now(),
        "counts": counts,
        "next_jobs": [{
            k: j.get(k) for k in ("job_id", "type", "lane", "priority", "canonical_id", "title", "source_url", "paper_path", "instructions", "completion")
        } for j in ready[:8]],
    }


def main():
    global ROOT, QUEUE, JOBS, SUBMISSIONS, RESULTS, STATE, ARCHIVE
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    ROOT = args.root.resolve()
    QUEUE = ROOT / "work-queue"
    JOBS, SUBMISSIONS, RESULTS = QUEUE / "jobs", QUEUE / "submissions", QUEUE / "results"
    STATE, ARCHIVE = QUEUE / "state.json", QUEUE / "archive"
    st = load_state()
    process_submissions(st)
    ensure_discovery_jobs(st)
    save_state(st)
    write_json(QUEUE / "next-jobs.json", queue_snapshot())
    print(json.dumps(queue_snapshot(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
