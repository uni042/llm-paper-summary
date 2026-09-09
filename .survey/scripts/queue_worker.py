#!/usr/bin/env python3
"""Queue-oriented survey state worker (workflow v9).

GitHub Actions owns queue/state transitions. Chat owns research judgment and writes
small immutable submission JSON files. No daily paper quota is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import survey  # noqa: E402

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
DISCOVERY_REFRESH_HOURS = {
    "discovery_fresh": 2,
    "discovery_citation": 6,
    "discovery_gap": 24,
}


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path, default: Any = None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return False
    path.write_text(text, encoding="utf-8")
    return True


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
    old = read_json(STATE, {}) or {}
    old_cmp = dict(old)
    new_cmp = dict(st)
    old_cmp.pop("updated_at", None)
    new_cmp.pop("updated_at", None)
    if old_cmp == new_cmp:
        st["updated_at"] = old.get("updated_at", st.get("updated_at", now()))
        return
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
        "discovery_fresh": "Find genuinely new inference-system papers or important revisions from primary sources. As a rule, require the paper or meaningful revision to be within the last 30 days. Older missing work belongs in the gap lane. Prefer papers not already represented in the repository.",
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
                due = (current_time - last_dt).total_seconds() >= DISCOVERY_REFRESH_HOURS[lane] * 3600
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
    # Queue history.
    for j in iter_jobs():
        for k in ("canonical_id", "source_url", "title"):
            v = j.get(k)
            if v:
                keys.add(str(v).strip().lower())

    # Identity snapshot and deltas.
    identity = read_json(ROOT / "survey-state" / "paper-identity-index.json", {})
    if isinstance(identity, dict):
        records = identity.get("papers") or {}
        if isinstance(records, dict):
            records = list(records.values())
        if isinstance(records, list):
            for rec in records:
                if not isinstance(rec, dict):
                    continue
                for k in ("canonical_id", "arxiv_id", "doi", "openreview_id", "source_url", "title"):
                    v = rec.get(k)
                    if v:
                        keys.add(str(v).strip().lower())
    delta_root = ROOT / "survey-state" / "identity-deltas"
    if delta_root.exists():
        for p in delta_root.rglob("*.json"):
            rec = read_json(p, {})
            for v in [rec.get("canonical_id"), *(rec.get("identifiers") or [])]:
                if v:
                    keys.add(str(v).strip().lower())

    # Final guard: scan current paper frontmatter so stale/absent snapshots cannot
    # allow a paper already present in the repository back into the queue.
    survey.ROOT = ROOT
    for rel in survey.papers():
        try:
            meta, _ = survey.front(ROOT / rel)
        except Exception:
            continue
        for k in ("canonical_id", "arxiv_id", "doi", "openreview_id", "source", "title"):
            v = meta.get(k)
            if not v:
                continue
            keys.add(str(v).strip().lower())
            if k == "arxiv_id":
                keys.add(("arxiv:" + str(v)).strip().lower())
            elif k == "doi":
                keys.add(("doi:" + str(v)).strip().lower())
            elif k == "openreview_id":
                keys.add(("openreview:" + str(v)).strip().lower())
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
    # Formal audits are targeted rather than one-for-one: important papers,
    # explicit uncertainty, or a deterministic quality-control sample.
    priority = int(research_job.get("priority") or 50)
    explicit = bool(sub.get("audit_required"))
    uncertainty = bool(sub.get("audit_flags") or sub.get("audit_reason"))
    sample_key = str(research_job.get("canonical_id") or research_job.get("job_id"))
    sampled = int(hashlib.sha256(sample_key.encode()).hexdigest()[:8], 16) % 5 == 0
    need = explicit or uncertainty or priority >= 75 or sampled
    if not need or len(active_jobs("audit")) >= MAX_READY_AUDIT:
        return False
    key = str(research_job.get("canonical_id") or research_job.get("job_id"))
    jid = stable_id("job-audit", key)
    return add_job({
        "job_id": jid,
        "type": "audit",
        "priority": max(
            40,
            min(
                74,
                int(research_job.get("priority") or 50) - 15
                + (10 if sub.get("audit_flags") else 0),
            ),
        ),
        "canonical_id": research_job.get("canonical_id"),
        "title": research_job.get("title"),
        "source_url": research_job.get("source_url"),
        "paper_path": research_job.get("paper_path"),
        "reason": sub.get("audit_reason") or ("high-priority paper" if priority >= 75 else "deterministic quality-control sample"),
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


def submission_content(sub: dict) -> str | None:
    """Return inline Markdown or load an immutable payload Markdown file."""
    content = sub.get("content")
    payload = sub.get("payload_path")
    if content is not None and payload is not None:
        raise ValueError("use either content or payload_path, not both")
    if payload is None:
        return content
    if not isinstance(payload, str):
        raise ValueError("payload_path must be a string")
    pp = Path(payload)
    if (
        not payload.startswith(".survey/work-queue/payloads/")
        or ".." in pp.parts
        or pp.suffix.lower() != ".md"
    ):
        raise ValueError("unsafe payload_path")
    target = ROOT.parent / pp
    if not target.is_file():
        raise ValueError("payload_path does not exist")
    return target.read_text(encoding="utf-8")


def process_research(sub: dict, job: dict, st: dict):
    status = sub.get("status", "completed")
    if status == "completed":
        content = submission_content(sub)
        if not isinstance(content, str) or len(content.strip()) < 500:
            raise ValueError("completed research requires complete Markdown content or payload_path")
        job["status"] = "completed"
        job["completed_at"] = now()
        job["artifact_submission"] = sub.get("_file")
        st["stats"]["research_completed"] += 1
        st.setdefault("maintenance", {})["views_dirty"] = True
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
        content = submission_content(sub)
        if not isinstance(content, str) or len(content.strip()) < 500:
            raise ValueError("completed audit requires complete Markdown content or payload_path")
        job["status"] = "completed"
        job["completed_at"] = now()
        job["artifact_submission"] = sub.get("_file")
        st["stats"]["audit_completed"] += 1
        st.setdefault("maintenance", {})["views_dirty"] = True
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
    loaded = submission_content(sub)\n    if not isinstance(loaded, str):\n        raise ValueError("completed artifact requires content or payload_path")\n    content = loaded.rstrip() + "\\n"
    target = ROOT.parent / paper
    expected_sha = sub.get("expected_blob_sha")
    if target.exists():
        if not expected_sha:
            raise ValueError("expected_blob_sha is required when updating an existing paper")
        import subprocess
        p = subprocess.run(["git", "rev-parse", f"HEAD:{paper}"], cwd=ROOT.parent, text=True, capture_output=True)
        current = p.stdout.strip() if p.returncode == 0 else None
        if current != expected_sha:
            raise ValueError(f"paper blob changed: expected {expected_sha}, current {current}")
    existed = target.exists()
    previous_text = target.read_text(encoding="utf-8") if existed else None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    # Keep connector-safe identity state current without rewriting the compact
    # index. Roll back the paper if identity validation fails.
    import subprocess
    p = subprocess.run(
        [sys.executable, ".survey/scripts/identity_delta.py", "prepare", "--paper", paper],
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
    )
    if p.returncode != 0:
        if existed:
            target.write_text(previous_text, encoding="utf-8")
        else:
            target.unlink(missing_ok=True)
        raise RuntimeError("identity delta failed: " + (p.stderr or p.stdout))
    return {"paper": paper, "identity_delta": p.stdout.strip()}


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


def reconcile_v9_identity_deltas():
    """Repair missing identity deltas for v9-published completed jobs."""
    import subprocess
    repaired = 0
    seen = set()
    for j in iter_jobs():
        if j.get("status") != "completed" or j.get("type") not in {"research", "audit"}:
            continue
        paper = j.get("paper_path")
        if not paper or paper in seen or not (ROOT.parent / paper).exists():
            continue
        seen.add(paper)
        p = subprocess.run(
            [sys.executable, ".survey/scripts/identity_delta.py", "prepare", "--paper", paper],
            cwd=ROOT.parent,
            text=True,
            capture_output=True,
        )
        if p.returncode != 0:
            raise RuntimeError("identity reconciliation failed for " + paper + ": " + (p.stderr or p.stdout))
        repaired += 1
    return repaired


def maybe_rebuild_views(st):
    """Batch large derived-view rewrites; never do them on every 10-minute poll."""
    import subprocess
    m = st.setdefault("maintenance", {})
    dirty = bool(m.get("views_dirty"))
    last = m.get("last_view_build_at")
    # On migration, a completed v9 research artifact with no recorded build means dirty.
    if not dirty and not last:
        dirty = any(
            j.get("type") in {"research", "audit"} and j.get("status") == "completed"
            for j in iter_jobs()
        )
    if not dirty:
        return False
    current = datetime.now(timezone.utc)
    if last:
        try:
            last_dt = datetime.fromisoformat(last.replace("Z", "+00:00"))
            if (current - last_dt).total_seconds() < 3600:
                return False
        except Exception:
            pass
    p = subprocess.run(
        [sys.executable, ".survey/scripts/survey.py", "--root", ".survey", "build"],
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
    )
    if p.returncode != 0:
        raise RuntimeError("derived view build failed: " + (p.stderr or p.stdout))
    m["views_dirty"] = False
    m["last_view_build_at"] = now()
    return True


def normalize_ready_jobs():
    changed = False
    for j in iter_jobs():
        if j.get("status") != "ready":
            continue
        if j.get("type") == "audit" and int(j.get("priority") or 0) > 74:
            j["priority"] = 74
            update_job(j)
            changed = True
    return changed


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
    previous_state = json.loads(json.dumps(st))
    st.setdefault("policy", {}).update({
        "fixed_daily_quota": False,
        "quality_over_quantity": True,
        "max_ready_research": MAX_READY_RESEARCH,
        "max_ready_audit": MAX_READY_AUDIT,
        "discovery_refresh_hours": DISCOVERY_REFRESH_HOURS,
        "worker_poll_minutes": 10,
    })
    process_submissions(st)
    ensure_discovery_jobs(st)
    reconcile_v9_identity_deltas()
    normalize_ready_jobs()
    maybe_rebuild_views(st)
    save_state(st)
    snap = queue_snapshot()
    snap_path = QUEUE / "next-jobs.json"
    old_snap = read_json(snap_path, {}) or {}
    old_cmp = dict(old_snap)
    old_cmp.pop("generated_at", None)
    if old_cmp == snap:
        snap["generated_at"] = old_snap.get("generated_at", now())
    else:
        snap["generated_at"] = now()
        write_json(snap_path, snap)
    print(json.dumps(snap, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
