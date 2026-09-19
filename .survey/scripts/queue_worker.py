#!/usr/bin/env python3
"""Queue-oriented survey state worker (workflow v10).

GitHub Actions owns queue/state transitions. Chat owns research judgment and writes
small immutable submission JSON files. New research/audit jobs are created directly
with the workflow-v10 five-slot structured-record contract. Root-level direct
research/audit submissions remain readable only as historical compatibility input.
No daily paper quota is used.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_identity  # noqa: E402
import survey  # noqa: E402
import claim_state  # noqa: E402
import discovery_search_history  # noqa: E402
import represented_paper_index  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "work-queue"
JOBS = QUEUE / "jobs"
SUBMISSIONS = QUEUE / "submissions"
RESULTS = QUEUE / "results"
STATE = QUEUE / "state.json"
ARCHIVE = QUEUE / "archive"
DISCOVERY_STATE = QUEUE / "discovery-state.json"

TERMINAL = {"completed", "rejected", "superseded", "blocked_permanent"}
MAX_DISCOVERY_CANDIDATES = 5
DISCOVERY_PRECHECK_MARKER = PurePosixPath(".survey/work-queue/discovery-precheck/ENFORCED")
DISCOVERY_ITERATIVE_PRECHECK_MARKER = PurePosixPath(".survey/work-queue/discovery-precheck/ITERATIVE_ENFORCED")
DISCOVERY_FIXED_SOURCE_PRECHECK_MARKER = PurePosixPath(".survey/work-queue/discovery-precheck/FIXED_SOURCE_ENFORCED")


class DiscoveryPrecheckError(ValueError):
    """Future Discovery submissions must prove they passed the canonical retrieval gate."""

    def __init__(self, code: str, message: str, *, next_action: str, recovery_steps: list[str]):
        super().__init__(message)
        self.code = code
        self.next_action = next_action
        self.recovery_steps = list(recovery_steps)

DISCOVERY_INSTRUCTIONS = (
    "Search primary sources for strong LLM inference-system papers not already "
    "represented in the repository. Prefer recent work, but include an older "
    "important omission when clearly worthwhile. Return at most 5 candidates. "
    "Do not fill the list with weak papers."
)
DISCOVERY_COMPLETION = "Submit 0-5 strong candidates. Empty is valid."
RESEARCH_INSTRUCTIONS = (
    "Read the primary source in full. Produce a repository-quality structured research "
    "record covering problem, novelty, method, evaluation conditions, key quantitative "
    "results, limitations, implementation status, and relation to existing repository "
    "lineages. Preserve publication date/status, implementation and source URLs; for an "
    "arXiv paper, record its primary and cross-list categories from arXiv. Do not infer "
    "missing text from abstracts/search snippets. Follow workflow v10 fixed-slot "
    "transport; do not send completed Markdown from Scheduled Chat."
)
RESEARCH_COMPLETION = (
    "Submit the complete workflow-v10 five-slot structured research record and source "
    "evidence. If full text is unavailable, return blocked with retrieval evidence "
    "instead of guessing."
)
AUDIT_INSTRUCTIONS = (
    "Perform a formal audit using primary sources: identity/bibliography, authors/"
    "affiliations, publication state/final version, code, hardware/model/dataset/"
    "baselines, quantitative results, simulation vs real hardware, classification, "
    "arXiv primary/cross-list categories, differences and limitations. Return a complete "
    "workflow-v10 five-slot structured research record; do not send completed Markdown "
    "from Scheduled Chat."
)
AUDIT_COMPLETION = (
    "Submit the audited workflow-v10 five-slot structured research record. If the "
    "required primary evidence cannot be obtained, return blocked/deferred rather than "
    "guessing."
)


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


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("utf-8")
    return hashlib.sha1(header + data).hexdigest()


def valid_paper_path(value: object) -> str | None:
    if not isinstance(value, str) or not value.startswith("papers/"):
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or not value.endswith(".md"):
        return None
    return path.as_posix()


def current_paper_blob_sha(paper_path: object) -> str | None:
    paper = valid_paper_path(paper_path)
    if paper is None:
        return None
    target = ROOT.parent / paper
    if not target.is_file():
        return None
    return git_blob_sha(target.read_bytes())


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
        "workflow_version": 10,
        "mode": "queue",
        "created_at": now(),
        "updated_at": now(),
        "policy": {
            "fixed_daily_quota": False,
            "quality_over_quantity": True,
            "decision_rule": "maintain_discovery_lane_process_ready_by_priority",
            "max_discovery_candidates": MAX_DISCOVERY_CANDIDATES,
            "worker_poll_minutes": 10,
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
    job.setdefault("workflow_version", 10)
    job.setdefault("status", "ready")
    job.setdefault("created_at", now())
    job.setdefault("priority", 50)
    write_json(p, job)
    return True


def update_job(job: dict):
    p = job.pop("_path", JOBS / f"{job['job_id']}.json")
    write_json(Path(p), job)


def clear_repair_state(job: dict):
    """Clear stale validation-isolation metadata after successful completion."""
    job.pop("repair_required", None)
    job.pop("validation_error", None)
    job.pop("validation_errors", None)
    job.pop("last_validation_failed_at", None)


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


def ensure_discovery_job():
    """Keep exactly one worker-facing discovery job independently of ingest jobs."""
    if active_jobs(job_type="discovery", lane="discovery"):
        return False
    issued = now()
    jid = stable_id("job", "discovery", issued)
    return add_job({
        "job_id": jid,
        "type": "discovery",
        "lane": "discovery",
        "priority": 50,
        "instructions": DISCOVERY_INSTRUCTIONS,
        "completion": DISCOVERY_COMPLETION,
    })


def is_discovery_round_submission(sub: dict) -> bool:
    """Return whether *sub* is a self-describing immutable Discovery round.

    Workflow-v10 specialist rounds are safe to ingest without a pre-issued Discovery
    job because they contain only bounded candidate metadata plus durable round identity.
    Legacy specialist submissions used the same shape but attached a synthetic job_id;
    accepting both shapes lets old stranded rounds converge through the same path.
    """
    if not isinstance(sub, dict):
        return False
    operation = sub.get("operation")
    if operation not in {None, "submit_discovery_round"}:
        return False
    candidates = sub.get("candidates")
    meta = sub.get("discovery_stats")
    if not isinstance(candidates, list) or len(candidates) > MAX_DISCOVERY_CANDIDATES:
        return False
    if any(not isinstance(candidate, dict) for candidate in candidates):
        return False
    if not isinstance(meta, dict):
        return False
    for field in ("run_key", "round", "axis"):
        value = meta.get(field)
        if not isinstance(value, str) or not value.strip():
            return False
    return True


def _git_introducing_commit(relative_path: PurePosixPath) -> str | None:
    """Return the commit that first introduced one repository path."""
    import subprocess

    proc = subprocess.run(
        ["git", "log", "--diff-filter=A", "--format=%H", "--", relative_path.as_posix()],
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return None
    commits = [line.strip() for line in proc.stdout.splitlines() if line.strip()]
    return commits[-1] if commits else None


_POST_MARKER_SUBMISSION_CACHE: dict[str, set[str] | None] = {}


def _post_marker_submission_paths() -> set[str] | None:
    """Return current Discovery submission paths added after the enforcement marker."""
    import subprocess

    repo_key = str(ROOT.parent.resolve())
    if repo_key in _POST_MARKER_SUBMISSION_CACHE:
        return _POST_MARKER_SUBMISSION_CACHE[repo_key]

    marker_commit = _git_introducing_commit(DISCOVERY_PRECHECK_MARKER)
    if not marker_commit:
        _POST_MARKER_SUBMISSION_CACHE[repo_key] = None
        return None
    proc = subprocess.run(
        [
            "git", "diff", "--name-only", "--diff-filter=A",
            f"{marker_commit}..HEAD", "--", ".survey/work-queue/submissions",
        ],
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        _POST_MARKER_SUBMISSION_CACHE[repo_key] = None
        return None
    paths = {line.strip() for line in proc.stdout.splitlines() if line.strip()}
    _POST_MARKER_SUBMISSION_CACHE[repo_key] = paths
    return paths


def _submission_path_added_after_marker(
    sub: dict,
    marker: PurePosixPath,
    *,
    cache_key_suffix: str,
) -> bool:
    """Return whether this durable Discovery submission was added after one marker."""
    import subprocess

    source_submission = str(sub.get("_file") or "").strip()
    if not source_submission:
        return False
    source_path = PurePosixPath(source_submission)
    if source_path.is_absolute() or ".." in source_path.parts or source_path.suffix != ".json":
        return True
    if len(source_path.parts) == 3 and source_path.parts[:2] == ("work-queue", "submissions"):
        source_path = PurePosixPath(".survey") / source_path
    elif len(source_path.parts) == 4 and source_path.parts[:3] == (".survey", "work-queue", "submissions"):
        pass
    else:
        return True

    marker_path = ROOT.parent / Path(marker.as_posix())
    if not marker_path.exists():
        return False

    repo_key = str(ROOT.parent.resolve()) + "::" + cache_key_suffix
    if repo_key not in _POST_MARKER_SUBMISSION_CACHE:
        marker_commit = _git_introducing_commit(marker)
        if not marker_commit:
            _POST_MARKER_SUBMISSION_CACHE[repo_key] = None
        else:
            proc = subprocess.run(
                [
                    "git", "diff", "--name-only", "--diff-filter=A",
                    f"{marker_commit}..HEAD", "--", ".survey/work-queue/submissions",
                ],
                cwd=ROOT.parent,
                text=True,
                capture_output=True,
            )
            _POST_MARKER_SUBMISSION_CACHE[repo_key] = (
                {line.strip() for line in proc.stdout.splitlines() if line.strip()}
                if proc.returncode == 0
                else None
            )
    paths = _POST_MARKER_SUBMISSION_CACHE[repo_key]
    if paths is None:
        return True
    return source_path.as_posix() in paths


def _iterative_discovery_precheck_required(sub: dict) -> bool:
    """Require schema-v2+ terminal precheck for submissions added after ITERATIVE_ENFORCED."""
    return _submission_path_added_after_marker(
        sub,
        DISCOVERY_ITERATIVE_PRECHECK_MARKER,
        cache_key_suffix="iterative",
    )


def _fixed_source_discovery_precheck_required(sub: dict) -> bool:
    """Require schema-v3 fixed-source pagination after FIXED_SOURCE_ENFORCED."""
    return _submission_path_added_after_marker(
        sub,
        DISCOVERY_FIXED_SOURCE_PRECHECK_MARKER,
        cache_key_suffix="fixed-source",
    )


def _discovery_precheck_required(sub: dict) -> bool:
    """Require precheck for Discovery submissions introduced after the enforcement marker."""
    proof_present = isinstance(sub.get("discovery_precheck"), dict)
    source_submission = str(sub.get("_file") or "").strip()
    if not source_submission:
        # Direct/unit callers without a durable path remain explicit: if they present a
        # proof, validate it; durable queue processing always sets _file.
        return proof_present

    source_path = PurePosixPath(source_submission)
    if source_path.is_absolute() or ".." in source_path.parts or source_path.suffix != ".json":
        return True
    if len(source_path.parts) == 3 and source_path.parts[:2] == ("work-queue", "submissions"):
        source_path = PurePosixPath(".survey") / source_path
    elif len(source_path.parts) == 4 and source_path.parts[:3] == (".survey", "work-queue", "submissions"):
        pass
    else:
        # Unexpected durable Discovery transport is not a compatibility escape hatch.
        return True

    marker_path = ROOT.parent / Path(DISCOVERY_PRECHECK_MARKER.as_posix())
    if not marker_path.exists():
        return proof_present

    post_marker_paths = _post_marker_submission_paths()
    if post_marker_paths is None:
        # Once the marker exists, inability to prove the boundary fails closed.
        return True
    return proof_present or source_path.as_posix() in post_marker_paths


def _precheck_guidance(reason: str) -> DiscoveryPrecheckError:
    return DiscoveryPrecheckError(
        "discovery_precheck_required",
        reason,
        next_action=(
            "Create one schema-v3 Discovery precheck request for a fixed provider search result URL/API query. "
            "The precheck itself must fetch page 1, then page 2, and later pages of that SAME result set until "
            "the unseen buffer is ready or the provider is exhausted. Then create a NEW immutable Discovery "
            "submission referencing that final result."
        ),
        recovery_steps=[
            "Do not edit or overwrite the failed Discovery submission.",
            "Create .survey/work-queue/discovery-precheck/requests/<unique>.json with schema_version=3, "
            "operation 'precheck_discovery_candidates', request_id, collector_id, the same run_key/axis, "
            "provider, and one fixed source_url/API query.",
            "Do not put hand-picked records[] in a schema-v3 request and do not change query/date/topic to emulate pagination.",
            "Wait for .survey/work-queue/discovery-precheck/results/<same-name>.json with ok=true.",
            "The workflow result must have evaluation_allowed=true and decision=READY_FOR_EVALUATION.",
            "Evaluate only records in that result's results[] array; filtered records must not be re-added.",
            "Create a NEW submit_discovery_round submission and set discovery_precheck.request_id, "
            "discovery_precheck.result_path, and discovery_precheck.receipt from that result.",
        ],
    )


def _precheck_result_has_workflow_provenance(result_path: PurePosixPath) -> bool:
    """Accept only result files committed by the dedicated precheck workflow bot."""
    import subprocess

    proc = subprocess.run(
        ["git", "log", "-1", "--format=%ae", "--", result_path.as_posix()],
        cwd=ROOT.parent,
        text=True,
        capture_output=True,
    )
    return proc.returncode == 0 and proc.stdout.strip() == "survey-discovery-precheck[bot]@users.noreply.github.com"


def validate_discovery_precheck(sub: dict) -> dict[str, Any] | None:
    """Verify that a new Discovery payload can only contain records emitted by precheck."""
    if not _discovery_precheck_required(sub):
        return None

    proof = sub.get("discovery_precheck")
    if not isinstance(proof, dict):
        raise _precheck_guidance("Discovery precheck receipt is required for this run.")

    request_id = str(proof.get("request_id") or "").strip()
    result_path_value = str(proof.get("result_path") or "").strip()
    receipt = str(proof.get("receipt") or "").strip()
    if not request_id or not result_path_value or not receipt:
        raise _precheck_guidance(
            "discovery_precheck must include request_id, result_path, and receipt from a successful precheck result."
        )

    result_path = PurePosixPath(result_path_value)
    expected_prefix = (".survey", "work-queue", "discovery-precheck", "results")
    if (
        result_path.is_absolute()
        or ".." in result_path.parts
        or len(result_path.parts) != 5
        or result_path.parts[:4] != expected_prefix
        or result_path.suffix != ".json"
    ):
        raise _precheck_guidance(
            "discovery_precheck.result_path must point to .survey/work-queue/discovery-precheck/results/<name>.json."
        )

    result = read_json(ROOT.parent / Path(result_path.as_posix()), {}) or {}
    if not result:
        raise _precheck_guidance(
            "Referenced Discovery precheck result does not exist yet. Wait for the precheck workflow result before submitting candidates."
        )
    if not _precheck_result_has_workflow_provenance(result_path):
        raise _precheck_guidance(
            "Referenced Discovery precheck result was not committed by the dedicated precheck workflow. "
            "Do not hand-write or copy result files; create a request and use the workflow-produced result."
        )
    if result.get("ok") is not True:
        raise _precheck_guidance(
            "Referenced Discovery precheck result is not successful. Follow its recovery_steps and create a new request."
        )
    if result.get("operation") != "precheck_discovery_candidates":
        raise _precheck_guidance("Referenced result is not a Discovery precheck result.")
    if str(result.get("request_id") or "") != request_id:
        raise _precheck_guidance("Discovery precheck request_id does not match the referenced result.")
    if str(result.get("receipt") or "") != receipt:
        raise _precheck_guidance("Discovery precheck receipt does not match the referenced result.")

    schema_version = result.get("schema_version")
    fixed_source_required = _fixed_source_discovery_precheck_required(sub)
    iterative_required = _iterative_discovery_precheck_required(sub)
    if fixed_source_required and (
        isinstance(schema_version, bool)
        or not isinstance(schema_version, int)
        or schema_version < 3
    ):
        raise _precheck_guidance(
            "This Discovery submission is after FIXED_SOURCE_ENFORCED and must reference a schema-v3 "
            "fixed-source pagination result. Schema-v1/v2 results cannot authorize new submissions."
        )
    if iterative_required and (
        isinstance(schema_version, bool)
        or not isinstance(schema_version, int)
        or schema_version < 2
    ):
        raise _precheck_guidance(
            "This Discovery submission is after ITERATIVE_ENFORCED and must reference schema-v2 or newer precheck."
        )
    if fixed_source_required or iterative_required or (
        isinstance(schema_version, int) and not isinstance(schema_version, bool) and schema_version >= 2
    ):
        if result.get("evaluation_allowed") is not True or result.get("decision") != "READY_FOR_EVALUATION":
            raise _precheck_guidance(
                "Referenced Discovery precheck result is not final. Use the canonical precheck path and "
                "reference only READY_FOR_EVALUATION."
            )

    meta = sub.get("discovery_stats") if isinstance(sub.get("discovery_stats"), dict) else {}
    if str(result.get("run_key") or "") != str(meta.get("run_key") or ""):
        raise _precheck_guidance("Discovery precheck run_key does not match this Discovery round.")
    if str(result.get("axis") or "") != str(meta.get("axis") or ""):
        raise _precheck_guidance("Discovery precheck axis does not match this Discovery round.")

    allowed_rows = result.get("allowed_records")
    if not isinstance(allowed_rows, list):
        raise _precheck_guidance("Discovery precheck result is missing allowed_records.")
    allowed_token_sets: list[set[str]] = []
    for row in allowed_rows:
        if not isinstance(row, dict):
            continue
        values = row.get("identity_tokens")
        if isinstance(values, list):
            token_set = {value for value in values if isinstance(value, str) and value}
            if token_set:
                allowed_token_sets.append(token_set)

    bypassed: list[str] = []
    for candidate in sub.get("candidates") or []:
        tokens = paper_identity.identity_tokens(candidate)
        if not tokens or not any(tokens & allowed for allowed in allowed_token_sets):
            bypassed.append(
                str(candidate.get("canonical_id") or candidate.get("title") or candidate_key(candidate) or "<unknown>")
            )
    if bypassed:
        sample = ", ".join(bypassed[:5])
        raise _precheck_guidance(
            "Discovery submission contains candidate(s) not emitted by the referenced precheck result: " + sample
        )
    return result


def discovery_ingest_job(source_submission: str, submitted_job_id: str | None = None, template_job: dict | None = None) -> dict:
    """Return a deterministic internal Discovery job for one immutable round."""
    source_submission = Path(source_submission).as_posix()
    jid = stable_id("job", "discovery-ingest", source_submission)
    path = JOBS / f"{jid}.json"
    if path.exists():
        existing = read_json(path, {}) or {}
        if existing.get("type") != "discovery" or existing.get("ingest_for_submission") != source_submission:
            raise RuntimeError("discovery ingest job id collision")
        existing["_path"] = path
        return existing

    template_job = template_job if isinstance(template_job, dict) else {}
    add_job({
        "job_id": jid,
        "type": "discovery",
        "lane": "discovery-ingest",
        "priority": int(template_job.get("priority") or 50),
        "status": "processing",
        "ingest_only": True,
        "ingest_for_submission": source_submission,
        "submitted_job_id": submitted_job_id,
        "instructions": template_job.get("instructions") or (
            "Internal Discovery ingest job. Apply the already durable candidate payload; "
            "do not perform new research or discovery in this job."
        ),
        "completion": template_job.get("completion") or "Apply the durable Discovery round payload.",
    })
    created = read_json(path, {}) or {}
    created["_path"] = path
    return created


def candidate_key(c: dict) -> str:
    return paper_identity.primary_identity_key(c) or ""


def existing_candidate_keys():
    keys: set[str] = set()
    for job in iter_jobs():
        keys.update(paper_identity.identity_tokens(job))

    identity = read_json(ROOT / "survey-state" / "paper-identity-index.json", {}) or {}
    if isinstance(identity, dict):
        records = identity.get("papers") or {}
        if isinstance(records, dict):
            for canonical, rec in records.items():
                data = dict(rec) if isinstance(rec, dict) else {}
                data["canonical_id"] = canonical
                keys.update(paper_identity.identity_tokens(data))
        elif isinstance(records, list):
            for rec in records:
                if isinstance(rec, dict):
                    keys.update(paper_identity.identity_tokens(rec))
        aliases = identity.get("identifier_to_canonical") or {}
        if isinstance(aliases, dict):
            for ident, canonical in aliases.items():
                for value in (ident, canonical):
                    normalized = paper_identity.safe_norm_id(value)
                    if normalized:
                        keys.add("id:" + normalized)

    delta_root = ROOT / "survey-state" / "identity-deltas"
    if delta_root.exists():
        for path in delta_root.rglob("*.json"):
            rec = read_json(path, {}) or {}
            if isinstance(rec, dict):
                keys.update(paper_identity.identity_tokens(rec))

    survey.ROOT = ROOT
    for record in survey.papers():
        data = dict(record.get("meta") or {})
        data["canonical_id"] = record.get("canonical_id")
        data["identifiers"] = record.get("identifiers") or []
        data["title"] = record.get("title")
        keys.update(paper_identity.identity_tokens(data))
    return keys


def existing_represented_resolver() -> dict[str, Any]:
    """Build the same represented-paper view used by retrieval-stage prefiltering."""
    records = represented_paper_index.collect_represented_records(ROOT, JOBS)
    return paper_identity.build_represented_resolver(records)


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
        "workflow_version": 10,
        "artifact_transport": "structured_record_v10",
        "instructions": RESEARCH_INSTRUCTIONS,
        "completion": RESEARCH_COMPLETION,
    })


def make_audit_job(sub: dict, research_job: dict):
    nested = sub.get("submission") if isinstance(sub.get("submission"), dict) else {}
    audit_required = sub.get("audit_required", nested.get("audit_required"))
    audit_flags = sub.get("audit_flags", nested.get("audit_flags"))
    audit_reason = sub.get("audit_reason", nested.get("audit_reason"))
    need = bool(audit_required or audit_flags or audit_reason)
    if not need:
        return False
    key = str(research_job.get("canonical_id") or research_job.get("job_id"))
    jid = stable_id("job-audit", key)
    paper_path = sub.get("paper_path") or research_job.get("paper_path")
    job = {
        "job_id": jid,
        "type": "audit",
        "priority": max(40, min(74, int(research_job.get("priority") or 50) - 10)),
        "canonical_id": research_job.get("canonical_id"),
        "title": research_job.get("title"),
        "source_url": research_job.get("source_url"),
        "paper_path": paper_path,
        "reason": audit_reason or "research result left an explicit verification need",
        "workflow_version": 10,
        "artifact_transport": "structured_record_v10",
        "instructions": AUDIT_INSTRUCTIONS,
        "completion": AUDIT_COMPLETION,
    }
    expected_blob_sha = current_paper_blob_sha(paper_path)
    if expected_blob_sha:
        job["expected_blob_sha"] = expected_blob_sha
    return add_job(job)


def record_discovery_stats(
    sub: dict,
    accepted_count: int,
    final_duplicate_filtered_count: int = 0,
) -> bool:
    """Persist per-axis discovery yield once for a processed submission.

    The immutable submission carries what the Chat worker observed before transport;
    Actions supplies the authoritative accepted_count and final duplicate count after
    canonical identity normalization. Survey-helper runs are serialized by workflow
    concurrency, so this single writer prevents normal and specialist workers from
    racing on discovery-state.json.
    """
    meta = sub.get("discovery_stats")
    if not isinstance(meta, dict):
        return False
    axis = str(meta.get("axis") or "").strip()
    if not axis:
        return False

    state = read_json(DISCOVERY_STATE, {}) or {}
    history = state.get("history") if isinstance(state.get("history"), list) else []
    source_submission = str(sub.get("_file") or meta.get("source_submission") or "").strip()
    if source_submission:
        source_submission = Path(source_submission).as_posix()
    if source_submission and any(
        isinstance(row, dict) and row.get("source_submission") == source_submission
        for row in history
    ):
        return False

    submitted = sub.get("candidates") if isinstance(sub.get("candidates"), list) else []
    candidate_count = int(meta.get("candidate_count", len(submitted)) or 0)
    candidate_count = max(candidate_count, len(submitted), 0)
    duplicate_count = int(meta.get("duplicate_filtered_count", max(candidate_count - len(submitted), 0)) or 0)
    duplicate_count = min(max(duplicate_count, 0), candidate_count)
    novel_count = max(candidate_count - duplicate_count, 0)
    final_duplicate_filtered_count = min(
        max(int(final_duplicate_filtered_count or 0), 0),
        novel_count,
    )
    post_final_dedupe_count = max(novel_count - final_duplicate_filtered_count, 0)
    accepted_count = min(max(int(accepted_count or 0), 0), post_final_dedupe_count)
    duplicate_ratio = (duplicate_count / candidate_count) if candidate_count else 0.0
    final_duplicate_ratio = (
        final_duplicate_filtered_count / novel_count
        if novel_count else 0.0
    )

    row = {
        "run_key": meta.get("run_key"),
        "round": meta.get("round"),
        "axis": axis,
        "query_summary": meta.get("query_summary"),
        "candidate_count": candidate_count,
        "duplicate_filtered_count": duplicate_count,
        "novel_candidate_count": novel_count,
        "final_duplicate_filtered_count": final_duplicate_filtered_count,
        "post_final_dedupe_count": post_final_dedupe_count,
        "accepted_count": accepted_count,
        "duplicate_ratio": duplicate_ratio,
        "final_duplicate_ratio": final_duplicate_ratio,
        "accepted_canonical_ids": list(meta.get("accepted_canonical_ids") or []),
        "duplicate_canonical_ids": list(meta.get("duplicate_canonical_ids") or []),
        "next_axis_hint": meta.get("next_axis_hint"),
        "source_submission": source_submission or None,
    }
    history.append(row)
    limit = state.get("history_limit", 24)
    if not isinstance(limit, int) or limit < 1:
        limit = 24
    state["history_limit"] = limit
    state["history"] = history[-limit:]

    axes = state.get("axes") if isinstance(state.get("axes"), dict) else {}
    summary = axes.get(axis) if isinstance(axes.get(axis), dict) else {}
    summary["last_run_key"] = meta.get("run_key")
    summary["rounds"] = int(summary.get("rounds", 0) or 0) + 1
    for field, value in (
        ("candidate_count", candidate_count),
        ("duplicate_filtered_count", duplicate_count),
        ("novel_candidate_count", novel_count),
        ("final_duplicate_filtered_count", final_duplicate_filtered_count),
        ("post_final_dedupe_count", post_final_dedupe_count),
        ("accepted_count", accepted_count),
    ):
        summary[field] = int(summary.get(field, 0) or 0) + value
    total_candidates = int(summary.get("candidate_count", 0) or 0)
    total_duplicates = int(summary.get("duplicate_filtered_count", 0) or 0)
    total_novel = int(summary.get("novel_candidate_count", 0) or 0)
    total_final_duplicates = int(summary.get("final_duplicate_filtered_count", 0) or 0)
    summary["duplicate_ratio"] = (total_duplicates / total_candidates) if total_candidates else 0.0
    summary["final_duplicate_ratio"] = (
        total_final_duplicates / total_novel if total_novel else 0.0
    )
    summary["next_axis_hint"] = meta.get("next_axis_hint")
    axes[axis] = summary
    state["axes"] = axes

    search_windows = meta.get("search_windows")
    if search_windows is not None:
        if not isinstance(search_windows, list) or any(not isinstance(window, dict) for window in search_windows):
            raise ValueError("discovery_stats.search_windows must be a list of objects")
        discovery_search_history.record_search_windows(
            state,
            search_windows,
            run_key=meta.get("run_key"),
            round_name=meta.get("round"),
        )

    state["schema_version"] = max(int(state.get("schema_version", 2) or 2), 3)
    state["updated_at"] = now()
    state["last_run_key"] = meta.get("run_key")
    state["last_round"] = meta.get("round")
    if accepted_count == 0:
        state["consecutive_empty_rounds"] = int(state.get("consecutive_empty_rounds", 0) or 0) + 1
        state["last_empty_round_reason"] = meta.get("empty_round_reason") or (
            "探索候補は正本側で重複抑止されるか、新規強候補として採用されなかった。"
        )
    else:
        state["consecutive_empty_rounds"] = 0
        state["last_empty_round_reason"] = None
    state.setdefault("next_action_when_stock_zero", "discover_now")
    state.setdefault("next_action_when_round_empty", "change_axis_and_discover_again")
    state.setdefault(
        "notes",
        "Scheduled Chat discovery state. Record per-round candidate counts, worker-side duplicate filtering, final canonical duplicate filtering, novelty yield, and next-axis hints. High-duplicate axes should not be mechanically repeated in the immediately following run.",
    )
    write_json(DISCOVERY_STATE, state)
    return True


_PRECHECK_UNSET = object()


def process_discovery(sub: dict, job: dict, st: dict, *, precheck_result: Any = _PRECHECK_UNSET):
    candidates = sub.get("candidates") or []
    if not isinstance(candidates, list):
        raise ValueError("candidates must be a list")
    if len(candidates) > MAX_DISCOVERY_CANDIDATES:
        raise ValueError("discovery submission may contain at most 5 candidates")
    if precheck_result is _PRECHECK_UNSET:
        precheck_result = validate_discovery_precheck(sub)
    seen = existing_candidate_keys()
    represented_resolver = existing_represented_resolver()
    accepted_records: list[dict[str, Any]] = []
    added = 0
    final_duplicate_filtered_count = 0
    for candidate in sorted(candidates, key=lambda x: int(x.get("priority") or 0), reverse=True):
        key = candidate_key(candidate)
        tokens = paper_identity.identity_tokens(candidate)
        if not key:
            continue
        represented_match = paper_identity.match_represented_paper(candidate, represented_resolver)
        local_match = None
        if accepted_records:
            local_match = paper_identity.match_represented_paper(
                candidate,
                paper_identity.build_represented_resolver(accepted_records),
            )
        if tokens & seen or represented_match or local_match:
            final_duplicate_filtered_count += 1
            continue
        if int(candidate.get("priority") or 0) < 40:
            continue
        if make_research_job(candidate, job["job_id"]):
            added += 1
            seen.update(tokens)
            accepted_records.append(dict(candidate))
        else:
            final_duplicate_filtered_count += 1
    job["status"] = "completed"
    job["completed_at"] = now()
    job["result_summary"] = {
        "submitted_candidates": len(candidates),
        "final_duplicate_filtered_count": final_duplicate_filtered_count,
        "research_jobs_added": added,
    }
    if precheck_result is not None:
        job["result_summary"]["precheck_request_id"] = precheck_result.get("request_id")
        job["result_summary"]["precheck_snapshot_source_commit"] = precheck_result.get("snapshot_source_commit")
    st["stats"]["discovered"] += len(candidates)
    st["stats"]["selected"] += added
    record_discovery_stats(
        sub,
        accepted_count=added,
        final_duplicate_filtered_count=final_duplicate_filtered_count,
    )


def process_discovery_round_submission(sub: dict, st: dict, template_job: dict | None = None) -> dict:
    """Ingest one self-describing Discovery round without a pre-issued job dependency."""
    if not is_discovery_round_submission(sub):
        raise ValueError("invalid submit_discovery_round payload")
    source_submission = str(sub.get("_file") or "").strip()
    if not source_submission:
        raise ValueError("discovery round requires durable source submission path")
    precheck_result = validate_discovery_precheck(sub)
    submitted_job_id = sub.get("job_id") if isinstance(sub.get("job_id"), str) else None
    job = discovery_ingest_job(source_submission, submitted_job_id=submitted_job_id, template_job=template_job)
    if job.get("status") == "completed":
        return job
    if job.get("status") in TERMINAL:
        raise ValueError(f"discovery ingest job already terminal: {job.get('status')}")
    process_discovery(sub, job, st, precheck_result=precheck_result)
    update_job(job)
    job["_path"] = JOBS / f"{job['job_id']}.json"
    return job


def submission_content(sub: dict) -> str | None:
    """Load a historical root-level Markdown submission payload."""
    content = sub.get("content")
    payload = sub.get("payload_path")
    if content is not None and payload is not None:
        raise ValueError("use either content or payload_path, not both")
    if payload is None:
        return content
    if not isinstance(payload, str):
        raise ValueError("payload_path must be a string")
    pp = Path(payload)
    if not payload.startswith(".survey/work-queue/payloads/") or ".." in pp.parts or pp.suffix.lower() != ".md":
        raise ValueError("payload_path must stay within .survey/work-queue/payloads/ and use a .md file")
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
        if sub.get("paper_path"):
            job["paper_path"] = sub["paper_path"]
        clear_repair_state(job)
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
        if sub.get("paper_path"):
            job["paper_path"] = sub["paper_path"]
        clear_repair_state(job)
        st["stats"]["audit_completed"] += 1
        st.setdefault("maintenance", {})["views_dirty"] = True
    elif status in {"blocked", "deferred", "rejected"}:
        job["status"] = status
        job["completed_at"] = now()
        job["blocker"] = sub.get("reason")
    else:
        raise ValueError("invalid audit status")


def apply_artifact(sub: dict, job: dict):
    """Apply historical direct-Markdown research/audit submissions only."""
    if job.get("type") not in {"research", "audit"} or sub.get("status", "completed") != "completed":
        return None
    paper = sub.get("paper_path") or job.get("paper_path")
    if not paper or not str(paper).startswith("papers/") or ".." in Path(paper).parts:
        raise ValueError("paper_path must stay under papers/ without parent traversal")
    loaded = submission_content(sub)
    if not isinstance(loaded, str) or len(loaded.strip()) < 500:
        raise ValueError("completed artifact requires complete Markdown content or payload_path")
    content = loaded.rstrip() + "\n"
    target = ROOT.parent / paper
    expected_sha = sub.get("expected_blob_sha")
    if target.exists():
        if not expected_sha:
            raise ValueError("expected_blob_sha is required when updating an existing paper")
        import subprocess
        p = subprocess.run(["git", "rev-parse", f"HEAD:{paper}"], cwd=ROOT.parent, text=True, capture_output=True)
        current = p.stdout.strip() if p.returncode == 0 else None
        if current != expected_sha:
            if target.read_bytes() != content.encode("utf-8"):
                raise ValueError(f"paper blob changed: expected {expected_sha}, current {current}")
    existed = target.exists()
    previous_text = target.read_text(encoding="utf-8") if existed else None
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

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
    """Process root-level discovery/control submissions and historical direct results."""
    SUBMISSIONS.mkdir(parents=True, exist_ok=True)
    RESULTS.mkdir(parents=True, exist_ok=True)
    for p in sorted(SUBMISSIONS.glob("*.json")):
        rp = RESULTS / p.name
        if rp.exists():
            continue
        result = {"schema_version": 1, "workflow_version": 10, "submission": str(p.relative_to(ROOT)), "ok": False}
        try:
            sub = read_json(p, {})
            sub["_file"] = str(p.relative_to(ROOT))
            attempt_id = sub.get("attempt_id")
            if isinstance(attempt_id, str) and attempt_id:
                result["attempt_id"] = attempt_id
            if sub.get("operation") == "request_jobs":
                before = {j["job_id"] for j in iter_jobs() if j.get("status") == "ready"}
                ensure_discovery_job()
                after = [j["job_id"] for j in iter_jobs() if j.get("status") == "ready" and j["job_id"] not in before]
                result.update({
                    "ok": True,
                    "operation": "request_jobs",
                    "requested_at": now(),
                    "generated_ready_jobs": after,
                })
                write_json(rp, result)
                continue
            if sub.get("operation") == "record_discovery_stats":
                accepted_count = sub.get("accepted_count")
                if isinstance(accepted_count, bool) or not isinstance(accepted_count, int) or accepted_count < 0:
                    raise ValueError("record_discovery_stats requires non-negative integer accepted_count")
                final_duplicate_filtered_count = sub.get("final_duplicate_filtered_count", 0)
                if (
                    isinstance(final_duplicate_filtered_count, bool)
                    or not isinstance(final_duplicate_filtered_count, int)
                    or final_duplicate_filtered_count < 0
                ):
                    raise ValueError(
                        "record_discovery_stats requires non-negative integer final_duplicate_filtered_count"
                    )
                changed = record_discovery_stats(
                    sub,
                    accepted_count=accepted_count,
                    final_duplicate_filtered_count=final_duplicate_filtered_count,
                )
                result.update({
                    "ok": True,
                    "operation": "record_discovery_stats",
                    "stats_recorded": changed,
                })
                write_json(rp, result)
                continue

            jid = sub.get("job_id")
            jp = JOBS / f"{jid}.json" if isinstance(jid, str) and jid else None
            explicit_round = sub.get("operation") == "submit_discovery_round"
            self_describing_round = is_discovery_round_submission(sub)
            template_job = None
            should_ingest_round = explicit_round
            if self_describing_round and not should_ingest_round:
                if jp is None or not jp.exists():
                    should_ingest_round = True
                else:
                    candidate_job = read_json(jp, {}) or {}
                    if candidate_job.get("type") == "discovery" and candidate_job.get("status") in TERMINAL:
                        should_ingest_round = True
                        template_job = candidate_job
            if explicit_round and not self_describing_round:
                raise ValueError("invalid submit_discovery_round payload")
            if should_ingest_round:
                job = process_discovery_round_submission(sub, st, template_job=template_job)
                result.update({
                    "ok": True,
                    "operation": "submit_discovery_round",
                    "submitted_job_id": jid,
                    "job_id": job["job_id"],
                    "job_type": "discovery",
                    "artifact": None,
                    "job_status": job.get("status"),
                })
                write_json(rp, result)
                continue

            if not jid:
                raise ValueError("job_id required")
            if jp is None or not jp.exists():
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
            if isinstance(exc, DiscoveryPrecheckError):
                result["error_code"] = exc.code
                result["retryable"] = True
                result["next_action"] = exc.next_action
                result["recovery_steps"] = exc.recovery_steps
        write_json(rp, result)


def reconcile_legacy_identity_deltas():
    """Keep identity deltas complete for historical direct-Markdown completions."""
    import subprocess
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


def maybe_rebuild_views(st):
    import subprocess
    m = st.setdefault("maintenance", {})
    dirty = bool(m.get("views_dirty"))
    last = m.get("last_view_build_at")
    if not dirty and not last:
        dirty = any(j.get("type") in {"research", "audit"} and j.get("status") == "completed" for j in iter_jobs())
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
    """Keep only live policy normalization that is independent of transport version."""
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
    claiming = claim_state.snapshot_claiming(jobs, ROOT.parent)
    claims = claim_state.current_claims(ROOT.parent)
    ready = [
        j for j in jobs
        if j.get("status") == "ready"
        and not (j.get("type") in claim_state.CLAIMABLE_TYPES and claims.get(str(j.get("job_id")), {}).get("active"))
    ]
    ready.sort(key=lambda j: (-int(j.get("priority") or 0), j.get("created_at", ""), str(j.get("job_id") or "")))
    visible_ready = ready[:8]
    if not any(j.get("type") == "discovery" for j in visible_ready):
        discovery = next((j for j in ready if j.get("type") == "discovery"), None)
        if discovery is not None:
            visible_ready.append(discovery)
    return {
        "counts": counts,
        "claiming": claiming,
        "next_jobs": [{
            k: j.get(k) for k in (
                "job_id", "type", "lane", "priority", "canonical_id", "title", "source_url",
                "paper_path", "workflow_version", "artifact_transport", "instructions", "completion",
            )
        } for j in visible_ready],
    }


def main():
    global ROOT, QUEUE, JOBS, SUBMISSIONS, RESULTS, STATE, ARCHIVE, DISCOVERY_STATE
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args()
    ROOT = args.root.resolve()
    QUEUE = ROOT / "work-queue"
    JOBS, SUBMISSIONS, RESULTS = QUEUE / "jobs", QUEUE / "submissions", QUEUE / "results"
    STATE, ARCHIVE = QUEUE / "state.json", QUEUE / "archive"
    DISCOVERY_STATE = QUEUE / "discovery-state.json"
    st = load_state()
    st["workflow_version"] = 10
    st.setdefault("policy", {}).update({
        "fixed_daily_quota": False,
        "quality_over_quantity": True,
        "decision_rule": "maintain_discovery_lane_process_ready_by_priority",
        "max_discovery_candidates": MAX_DISCOVERY_CANDIDATES,
        "worker_poll_minutes": 10,
    })
    process_submissions(st)
    # Keep a discovery lane available even while research/audit work is ready so the
    # specialist worker can replenish the shared candidate buffer independently.
    ensure_discovery_job()
    reconcile_legacy_identity_deltas()
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
