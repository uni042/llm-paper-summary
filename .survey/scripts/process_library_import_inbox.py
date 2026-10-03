#!/usr/bin/env python3
"""Process ChatGPT Library artifacts copied into the GitHub import inbox.

The uploader is intentionally dumb: it copies completed Research Markdown or one
immutable Discovery-run JSON into .survey/import-inbox/pending/. This processor,
running on GitHub, owns the current-main decisions:

* resolve represented Research identities against the current checkout;
* audit/route new Research papers and update derived views;
* turn Discovery accept records into candidate_id_lookup schema-v3 prechecks;
* turn unrelated/borderline records into the canonical relevance-request lane;
* create Discovery submissions only from workflow-produced precheck results;
* retain blocked payloads in GitHub so the Library copy can be removed once the
  pending inbox copy itself has been verified.

The script is idempotent. Request/submission names are content-derived and
create-only in spirit; an existing file with different content is a hard error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import audit_metadata_coverage  # noqa: E402
import audit_paper_quality  # noqa: E402
import paper_quality_gate  # noqa: E402
import paper_identity  # noqa: E402
import paper_taxonomy  # noqa: E402
import research_job_reconciliation  # noqa: E402
import resolve_paper_identity  # noqa: E402
import survey  # noqa: E402


INBOX = Path(".survey/import-inbox")
PENDING_RESEARCH = INBOX / "pending/research"
PENDING_DISCOVERY = INBOX / "pending/discovery"
WAITING_DISCOVERY = INBOX / "waiting/discovery"
RETAINED_DISCOVERY_SOURCE = INBOX / "retained/discovery-source"
DISCOVERY_CHUNK_RECORDS = 20
BLOCKED_RESEARCH = INBOX / "blocked/research"
BLOCKED_DISCOVERY = INBOX / "blocked/discovery"
RESULT_RESEARCH = INBOX / "results/research"
RESULT_DISCOVERY = INBOX / "results/discovery"

PRECHECK_REQUESTS = Path(".survey/work-queue/discovery-precheck/requests")
PRECHECK_RESULTS = Path(".survey/work-queue/discovery-precheck/results")
RELEVANCE_REQUESTS = Path(".survey/work-queue/reference-curation/requests")
RELEVANCE_RESULTS = Path(".survey/work-queue/reference-curation/results")
DISCOVERY_SUBMISSIONS = Path(".survey/work-queue/submissions")
DISCOVERY_RESULTS = Path(".survey/work-queue/results")

SAFE_ID_RE = re.compile(r"[^A-Za-z0-9._-]+")
SAFE_SLUG_RE = re.compile(r"[^a-z0-9]+")
CLASSIFICATIONS = {"accept", "unrelated", "borderline"}

# Library Research frontmatter may contain a human-readable lineage name rather
# than the repository slug. Path selection is a GitHub-side responsibility, so
# map strong topic signals to the current canonical taxonomy here.
LINEAGE_KEYWORDS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("13-sparse-attention", ("sparse attention", "疎注意", "疎attention", "block sparse attention")),
    ("10-kv-cache-offload-recomputation", ("kv cache offload", "kv offload", "kv cache退避", "kv退避", "kv recomputation")),
    ("07-kv-cache-optimization-compression", ("kv cache", "kv-cache", "kv圧縮", "kv cache compression", "kv cache optimization")),
    ("03-expert-prefetch", ("expert prefetch", "expert-prefetch", "エキスパート先読み", "専門家先読み")),
    ("05-speculative-decoding-moe", ("speculative decoding", "speculative decode", "投機的デコード", "投機デコード")),
    ("12-moe-parallelism-communication", ("expert parallel", "all-to-all", "moe communication", "moe並列", "専門家並列")),
    ("06-moe-quantization-compression", ("moe quantization", "expert quantization", "expert compression", "moe量子化", "エキスパート量子化")),
    ("16-weight-quantization-compression", ("weight quantization", "weight compression", "weight-only", "重み量子化", "重み圧縮")),
    ("17-pim-near-data-acceleration", ("pim", "near-data", "near memory", "near-memory", "in-storage", "メモリ内処理", "メモリ近傍")),
    ("15-inference-simulation-emulation", ("simulation", "simulator", "emulation", "emulator", "シミュレーション", "エミュレーション")),
    ("19-inference-evaluation-benchmarking", ("benchmark", "workload diagnosis", "trace replay", "ベンチマーク", "性能診断")),
    ("14-agentic-inference-serving-runtime", ("agentic", "multi-agent", "agent serving", "エージェント推論", "エージェントサービング")),
    ("09-kernel-runtime-compilation", ("kernel", "compiler", "compilation", "jit", "カーネル", "コンパイラ")),
    ("11-llm-serving-scheduling-disaggregation", ("serving", "scheduler", "scheduling", "disaggregation", "サービング", "スケジューリング", "分離型")),
    ("08-edge-on-device-llm-systems", ("on-device", "edge device", "mobile", "オンデバイス", "エッジ")),
    ("02-adaptive-expert-computation-compression", ("expert pruning", "expert merging", "adaptive expert", "専門家枝刈り", "エキスパート枝刈り")),
    ("04-conditional-computation", ("conditional computation", "dynamic computation", "条件付き計算")),
    ("01-offload-hierarchical-memory", ("offload", "hierarchical memory", "tiered memory", "expert cache", "オフロード", "階層メモリ")),
)


def infer_inference_lineage(meta: dict[str, Any], repo_root: Path) -> str:
    """Resolve a Library paper's human or slug lineage to current GitHub taxonomy."""
    requested = str(meta.get("lineage") or "").strip()
    valid = set(paper_taxonomy.canonical_inference_lineages(repo_root))
    if requested in valid:
        return requested

    # Historical slug aliases are handled by the taxonomy helper.
    direct = paper_taxonomy.canonical_lineage(
        "inference",
        requested or paper_taxonomy.DEFAULT_INFERENCE_LINEAGE,
        repo_root=repo_root,
    )
    if requested and direct != paper_taxonomy.DEFAULT_INFERENCE_LINEAGE and direct in valid:
        return direct

    topics = meta.get("topics")
    if isinstance(topics, list):
        topic_text = " ".join(str(item) for item in topics)
    else:
        topic_text = str(topics or "")
    haystack = " ".join(
        [
            requested,
            str(meta.get("title") or ""),
            str(meta.get("summary") or ""),
            topic_text,
        ]
    ).casefold()
    for lineage, needles in LINEAGE_KEYWORDS:
        if lineage in valid and any(needle.casefold() in haystack for needle in needles):
            return lineage
    return paper_taxonomy.DEFAULT_INFERENCE_LINEAGE


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def write_text_if_absent(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = path.read_text(encoding="utf-8")
        if existing != content:
            raise RuntimeError(f"immutable path collision: {path}")
        return
    path.write_text(content, encoding="utf-8")


def write_json_if_absent(path: Path, payload: dict[str, Any]) -> None:
    write_text_if_absent(
        path,
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
    )


def replace_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    tmp.replace(path)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def repo_relative(path: Path, repo_root: Path) -> str:
    """Return a stable repository-relative POSIX path for relative or absolute Paths."""
    path = Path(path)
    if path.is_absolute():
        return path.relative_to(repo_root).as_posix()
    return path.as_posix()


def source_token(path: Path) -> str:
    digest = sha256_bytes(path.read_bytes())
    stem = SAFE_ID_RE.sub("-", path.stem).strip("-.")[:48] or "artifact"
    return f"{stem}-{digest[:12]}"


def result_filename(path: Path) -> str:
    """Stable result name derived from the uploader's unique inbox filename."""
    stem = SAFE_ID_RE.sub("-", path.stem).strip("-.")[:160] or "artifact"
    return stem + ".json"


def parse_frontmatter(text: str) -> dict[str, Any]:
    if not text.startswith("---\n"):
        raise ValueError("Research Markdown requires YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError("Research Markdown frontmatter is not closed")
    meta = yaml.safe_load(parts[1])
    if not isinstance(meta, dict):
        raise ValueError("Research Markdown frontmatter must be a mapping")
    return meta


def research_metadata_failures(source: Path, meta: dict[str, Any], repo_root: Path) -> list[str]:
    failures = list(audit_metadata_coverage.findings(source, repo_root))
    for key in ("list_summary", "worker_completed_at", "worker_run_key"):
        value = meta.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            failures.append(key)

    published = str(meta.get("published") or "").strip()
    if published and not re.fullmatch(r"\d{4}-\d{2}(?:-\d{2})?", published):
        failures.append("published:format")

    canonical = str(meta.get("canonical_id") or "").strip().casefold()
    source_url = str(meta.get("source") or "").strip().casefold()
    is_arxiv = canonical.startswith("arxiv:") or "arxiv.org/" in source_url
    if is_arxiv:
        if not str(meta.get("arxiv_id") or "").strip():
            failures.append("arxiv_id")
        categories = meta.get("arxiv_categories")
        if not isinstance(categories, dict):
            failures.extend(("arxiv_categories.primary", "arxiv_categories.cross_list"))
        else:
            if not str(categories.get("primary") or "").strip():
                failures.append("arxiv_categories.primary")
            if "cross_list" not in categories or not isinstance(categories.get("cross_list"), list):
                failures.append("arxiv_categories.cross_list")

    return sorted(set(str(item) for item in failures))


def publication_year(meta: dict[str, Any]) -> str:
    published = str(meta.get("published") or "")
    match = re.search(r"\b(19\d{2}|20\d{2})\b", published)
    if match:
        return match.group(1)
    for value in (meta.get("arxiv_id"), meta.get("canonical_id"), meta.get("source")):
        match = re.search(r"(?:arXiv:|arxiv\.org/(?:abs|html|pdf)/)?(\d{2})(\d{2})\.\d{4,5}", str(value or ""), re.I)
        if match:
            return str(2000 + int(match.group(1)))
    return "unknown"


def paper_filename(meta: dict[str, Any]) -> str:
    canonical_id = str(meta.get("canonical_id") or "").strip()
    arxiv_id = str(meta.get("arxiv_id") or "").strip()
    if not arxiv_id:
        match = re.search(r"arXiv:(\d{4}\.\d{4,5})", canonical_id, re.I)
        if match:
            arxiv_id = match.group(1)
    ident = arxiv_id if arxiv_id else hashlib.sha256(canonical_id.encode("utf-8")).hexdigest()[:12]
    title = str(meta.get("title") or "paper").casefold()
    slug = SAFE_SLUG_RE.sub("-", title).strip("-")[:72] or "paper"
    return f"{publication_year(meta)}-{ident}-{slug}.md"


def block_payload(source: Path, target_dir: Path) -> Path:
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / source.name
    if target.exists():
        if target.read_bytes() == source.read_bytes():
            source.unlink(missing_ok=True)
            return target
        target = target_dir / f"{source.stem}-{sha256_bytes(source.read_bytes())[:12]}{source.suffix}"
    source.replace(target)
    return target


def _retryable_precheck_provenance_failure(repo_root: Path, failure_id: str) -> bool:
    result_path = repo_root / DISCOVERY_RESULTS / f"{failure_id}.json"
    if not result_path.is_file():
        return False
    try:
        payload = read_json(result_path)
    except Exception:
        return False
    return (
        payload.get("ok") is False
        and payload.get("retryable") is True
        and str(payload.get("error_code") or "") == "discovery_precheck_required"
    )


def recover_retryable_precheck_provenance_blocks(repo_root: Path) -> int:
    """Requeue Library Discovery payloads blocked only by invalid precheck provenance.

    Historical failed submissions/results stay immutable. The retained original
    Library payload is copied to a deterministic retry inbox name, which creates
    a fresh content-derived precheck/submission lineage. A terminal retry result
    suppresses future requeue attempts.
    """
    recovered = 0
    results_root = repo_root / RESULT_DISCOVERY
    blocked_root = repo_root / BLOCKED_DISCOVERY
    pending_root = repo_root / PENDING_DISCOVERY
    waiting_root = repo_root / WAITING_DISCOVERY
    pending_root.mkdir(parents=True, exist_ok=True)

    if not results_root.is_dir():
        return 0

    for result_path in sorted(results_root.glob("*.json")):
        try:
            result = read_json(result_path)
        except Exception:
            continue
        if str(result.get("status") or "") != "blocked_downstream":
            continue
        failures = result.get("failures")
        if not isinstance(failures, list) or not failures:
            continue
        failure_ids = [str(item) for item in failures if isinstance(item, str) and item.strip()]
        if not failure_ids or not all(
            _retryable_precheck_provenance_failure(repo_root, failure_id)
            for failure_id in failure_ids
        ):
            continue

        retained = result.get("retained_payload")
        if not isinstance(retained, str) or not retained.strip():
            continue
        source = repo_root / retained
        if not source.is_file() or blocked_root not in source.parents:
            continue

        retry_tag = hashlib.sha256(
            result_path.relative_to(repo_root).as_posix().encode("utf-8")
        ).hexdigest()[:12]
        retry_name = f"retry-precheck-{retry_tag}--{source.name}"
        retry_pending = pending_root / retry_name
        retry_waiting = waiting_root / retry_name
        retry_result = results_root / result_filename(Path(retry_name))

        if retry_result.is_file():
            continue
        if retry_pending.is_file():
            if retry_pending.read_bytes() != source.read_bytes():
                raise RuntimeError(f"retry payload collision: {retry_pending}")
            continue
        if retry_waiting.is_file():
            if retry_waiting.read_bytes() != source.read_bytes():
                raise RuntimeError(f"retry payload collision: {retry_waiting}")
            continue

        retry_pending.write_bytes(source.read_bytes())
        recovered += 1

    return recovered


def process_research(repo_root: Path, max_items: int | None = None) -> tuple[int, int]:
    imported = 0
    terminal = 0
    PENDING_RESEARCH.mkdir(parents=True, exist_ok=True)

    sources = sorted(PENDING_RESEARCH.glob("*.md"))
    if max_items is not None:
        sources = sources[:max(0, max_items)]
    for source in sources:
        token = source_token(source)
        result_path = RESULT_RESEARCH / result_filename(source)
        raw = source.read_text(encoding="utf-8")
        payload_hash = sha256_bytes(raw.encode("utf-8"))

        try:
            meta = parse_frontmatter(raw)
            metadata_failures = research_metadata_failures(source, meta, repo_root)
            if metadata_failures:
                blocked_path = block_payload(source, BLOCKED_RESEARCH)
                replace_json(
                    result_path,
                    {
                        "schema_version": 1,
                        "artifact_type": "research",
                        "status": "blocked_metadata",
                        "source_sha256": payload_hash,
                        "blocked_path": repo_relative(blocked_path, repo_root),
                        "canonical_id": meta.get("canonical_id"),
                        "worker_completed_at": meta.get("worker_completed_at"),
                        "worker_run_key": meta.get("worker_run_key"),
                        "failures": metadata_failures,
                        "processed_at": now(),
                    },
                )
                terminal += 1
                continue

            audit = paper_quality_gate.inspect_rendered_paper(
                repo_root,
                repo_relative(source, repo_root),
                raw,
            )
            if audit.status == "FAIL":
                blocked_path = block_payload(source, BLOCKED_RESEARCH)
                replace_json(
                    result_path,
                    {
                        "schema_version": 1,
                        "artifact_type": "research",
                        "status": "blocked_quality",
                        "source_sha256": payload_hash,
                        "blocked_path": repo_relative(blocked_path, repo_root),
                        "canonical_id": meta.get("canonical_id"),
                        "worker_completed_at": meta.get("worker_completed_at"),
                        "worker_run_key": meta.get("worker_run_key"),
                        "failures": audit.failures,
                        "processed_at": now(),
                    },
                )
                terminal += 1
                continue

            record = dict(meta)
            record.setdefault("source_url", meta.get("source"))
            resolution = resolve_paper_identity.resolve(repo_root, record)
            if resolution["status"] == "represented":
                source.unlink()
                replace_json(
                    result_path,
                    {
                        "schema_version": 1,
                        "artifact_type": "research",
                        "status": "already_represented",
                        "source_sha256": payload_hash,
                        "canonical_id": meta.get("canonical_id"),
                        "paper_path": resolution.get("paper_path"),
                        "worker_completed_at": meta.get("worker_completed_at"),
                        "worker_run_key": meta.get("worker_run_key"),
                        "processed_at": now(),
                    },
                )
                terminal += 1
                continue

            lineage = infer_inference_lineage(meta, repo_root)

            target_dir = repo_root / "papers" / "inference" / lineage
            target_dir.mkdir(parents=True, exist_ok=True)
            target = target_dir / paper_filename(meta)
            if target.exists():
                alternate = target.with_name(
                    f"{target.stem}-{hashlib.sha256(str(meta.get('canonical_id')).encode('utf-8')).hexdigest()[:8]}.md"
                )
                if alternate.exists():
                    raise RuntimeError(f"paper target collision: {target} / {alternate}")
                target = alternate

            target.write_text(raw, encoding="utf-8")
            post = resolve_paper_identity.resolve(repo_root, record)
            if post["status"] != "represented" or post.get("paper_path") != repo_relative(target, repo_root):
                target.unlink(missing_ok=True)
                raise RuntimeError("post-write identity resolution did not resolve to the imported paper")

            source.unlink()
            replace_json(
                result_path,
                {
                    "schema_version": 1,
                    "artifact_type": "research",
                    "status": "imported",
                    "source_sha256": payload_hash,
                    "canonical_id": meta.get("canonical_id"),
                    "paper_path": target.relative_to(repo_root).as_posix(),
                    "lineage": lineage,
                    "audit_status": audit.status,
                    "worker_completed_at": meta.get("worker_completed_at"),
                    "worker_run_key": meta.get("worker_run_key"),
                    "processed_at": now(),
                },
            )
            imported += 1
            terminal += 1
        except Exception as exc:
            blocked_path = block_payload(source, BLOCKED_RESEARCH)
            replace_json(
                result_path,
                {
                    "schema_version": 1,
                    "artifact_type": "research",
                    "status": "blocked_import",
                    "source_sha256": payload_hash,
                    "blocked_path": blocked_path.relative_to(repo_root).as_posix(),
                    "error": f"{type(exc).__name__}: {exc}",
                    "processed_at": now(),
                },
            )
            terminal += 1

    if imported:
        # These are derived-view refreshes. A stale README/worklist is repairable,
        # while losing an already validated Library import is not. Keep failures
        # visible on stderr but do not roll back durable inbox progress.
        survey.ROOT = repo_root / ".survey"
        try:
            survey.render()
        except Exception as exc:
            print(f"warning: survey.render failed after durable Research import: {type(exc).__name__}: {exc}", file=sys.stderr)
        try:
            research_job_reconciliation.reconcile(repo_root)
        except Exception as exc:
            print(f"warning: research reconciliation failed after durable Research import: {type(exc).__name__}: {exc}", file=sys.stderr)

    return imported, terminal


def discovery_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    records = payload.get("records")
    if not isinstance(records, list):
        raise ValueError("Discovery artifact requires records[]")
    out: list[dict[str, Any]] = []
    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"records[{index}] must be an object")
        classification = str(record.get("classification") or "").strip()
        if classification not in CLASSIFICATIONS:
            raise ValueError(f"records[{index}].classification must be accept/unrelated/borderline")
        canonical_id = str(record.get("canonical_id") or "").strip()
        if not canonical_id:
            raise ValueError(f"records[{index}].canonical_id is required")
        reason = str(record.get("reason") or "").strip()
        if not reason:
            raise ValueError(f"records[{index}].reason is required")
        out.append(record)
    return out


def split_oversized_discovery_sources(max_records: int | None) -> int:
    """Split large immutable Discovery runs into bounded GitHub-side work chunks.

    The original run payload is retained byte-for-byte under retained/discovery-source.
    Chunk files are deterministic derived work artifacts; they preserve provenance and
    allow downstream precheck/relevance work to stay within a records-per-invocation cap.
    """
    if max_records is None or max_records <= 0:
        return 0
    WAITING_DISCOVERY.mkdir(parents=True, exist_ok=True)
    RETAINED_DISCOVERY_SOURCE.mkdir(parents=True, exist_ok=True)
    split_count = 0

    for source in sorted(WAITING_DISCOVERY.glob("*.json")):
        if "--chunk-" in source.stem:
            continue
        try:
            payload = read_json(source)
            records = discovery_records(payload)
        except Exception:
            continue
        if len(records) <= max_records:
            continue

        parent_run_key = str(payload.get("parent_run_key") or payload.get("run_key") or source.stem)
        chunk_count = (len(records) + max_records - 1) // max_records
        for index in range(chunk_count):
            lo = index * max_records
            hi = min(len(records), lo + max_records)
            chunk_payload = dict(payload)
            chunk_payload["records"] = records[lo:hi]
            chunk_payload["record_count"] = hi - lo
            chunk_payload["parent_run_key"] = parent_run_key
            chunk_payload["run_key"] = (
                f"{parent_run_key}::chunk-{index + 1:04d}-of-{chunk_count:04d}"
            )
            chunk_payload["chunk_index"] = index + 1
            chunk_payload["chunk_count"] = chunk_count
            chunk_payload["source_record_count"] = len(records)
            chunk_path = WAITING_DISCOVERY / (
                f"{source.stem}--chunk-{index + 1:04d}-of-{chunk_count:04d}.json"
            )
            write_json_if_absent(chunk_path, chunk_payload)

        retained = RETAINED_DISCOVERY_SOURCE / source.name
        if retained.exists():
            if retained.read_bytes() != source.read_bytes():
                retained = RETAINED_DISCOVERY_SOURCE / (
                    f"{source.stem}-{sha256_bytes(source.read_bytes())[:12]}{source.suffix}"
                )
        retained.parent.mkdir(parents=True, exist_ok=True)
        if retained.exists():
            if retained.read_bytes() != source.read_bytes():
                raise RuntimeError(f"retained Discovery source collision: {retained}")
            source.unlink(missing_ok=True)
        else:
            source.replace(retained)
        split_count += 1

    return split_count


def select_discovery_sources(max_records: int | None) -> list[Path]:
    selected: list[Path] = []
    used_records = 0
    for source in sorted(WAITING_DISCOVERY.glob("*.json")):
        try:
            count = len(discovery_records(read_json(source)))
        except Exception:
            count = 0
        if max_records is not None and max_records > 0:
            if selected and used_records + count > max_records:
                break
            if not selected and count > max_records:
                # Oversized valid payloads should already have been split. Select
                # an invalid/unexpected survivor alone so it can be blocked instead
                # of permanently starving the FIFO.
                selected.append(source)
                break
        selected.append(source)
        used_records += count
        if max_records is not None and max_records > 0 and used_records >= max_records:
            break
    return selected


def preferred_candidate_id(record: dict[str, Any]) -> str | None:
    identifiers = sorted(paper_identity.record_identifiers(record))
    for prefix in ("arXiv:", "DOI:", "OpenReview:"):
        for value in identifiers:
            if value.startswith(prefix):
                return value
    return None


def candidate_request_id(token: str, batch_index: int) -> str:
    return f"libimp-{hashlib.sha256(token.encode('utf-8')).hexdigest()[:16]}-pre{batch_index:02d}"


def relevance_request_id(token: str, index: int, classification: str) -> str:
    suffix = "unrel" if classification == "unrelated" else "border"
    return f"libimp-{hashlib.sha256(token.encode('utf-8')).hexdigest()[:16]}-{suffix}-{index:03d}"


def merge_library_reason(provider_record: dict[str, Any], library_records: list[dict[str, Any]]) -> dict[str, Any]:
    candidate = dict(provider_record)
    candidate_tokens = paper_identity.identity_tokens(candidate)
    for record in library_records:
        if candidate_tokens & paper_identity.identity_tokens(record):
            candidate["reason"] = record.get("reason")
            if record.get("lineage"):
                candidate["lineage"] = record.get("lineage")
            candidate["library_body_check"] = record.get("body_check")
            candidate["library_source_run_file"] = record.get("source_run_file")
            break
    return candidate


def create_relevance_requests(repo_root: Path, token: str, records: list[dict[str, Any]]) -> tuple[list[str], list[str]]:
    waiting: list[str] = []
    failures: list[str] = []
    for index, record in enumerate(records, 1):
        classification = str(record["classification"])
        request_id = relevance_request_id(token, index, classification)
        request_path = repo_root / RELEVANCE_REQUESTS / f"{request_id}.json"
        result_path = repo_root / RELEVANCE_RESULTS / f"{request_id}.json"
        request = {
            "schema_version": 1,
            "request_id": request_id,
            "operation": "mark_unrelated" if classification == "unrelated" else "mark_borderline",
            "canonical_id": record["canonical_id"],
            "reason": record["reason"],
            "title": record.get("title"),
            "identity_tokens": list(record.get("identity_tokens") or []),
            "linked_from": [
                item
                for item in list(record.get("linked_from") or [])
                if isinstance(item, str) and item.strip()
            ],
            "worker_id": "library-import-inbox",
            "run_key": f"library-import-{hashlib.sha256(token.encode('utf-8')).hexdigest()[:12]}",
            "source_precheck_request_id": record.get("source_precheck_request_id"),
        }
        write_json_if_absent(request_path, request)
        if not result_path.exists():
            waiting.append(request_id)
            continue
        result = read_json(result_path)
        if result.get("ok") is not True:
            failures.append(request_id)
    return waiting, failures


def create_accept_pipeline(repo_root: Path, token: str, records: list[dict[str, Any]]) -> tuple[list[str], list[str], list[str], dict[str, int]]:
    id_to_records: dict[str, list[dict[str, Any]]] = {}
    missing_ids: list[str] = []
    for record in records:
        identifier = preferred_candidate_id(record)
        if identifier is None:
            missing_ids.append(str(record.get("canonical_id")))
            continue
        id_to_records.setdefault(identifier, []).append(record)

    identifiers = sorted(id_to_records)
    batches = [identifiers[i : i + 100] for i in range(0, len(identifiers), 100)]
    waiting: list[str] = []
    failures: list[str] = []
    submission_waiting: list[str] = []
    counts = {"allowed": 0, "filtered": 0, "submitted": 0}

    for batch_index, batch in enumerate(batches, 1):
        request_id = candidate_request_id(token, batch_index)
        request_path = repo_root / PRECHECK_REQUESTS / f"{request_id}.json"
        result_path = repo_root / PRECHECK_RESULTS / f"{request_id}.json"
        request = {
            "schema_version": 3,
            "operation": "precheck_discovery_candidates",
            "request_id": request_id,
            "collector_id": "library-candidate-intake",
            "run_key": f"library-import-{hashlib.sha256(token.encode('utf-8')).hexdigest()[:12]}",
            "axis": "library-candidate-intake",
            "target_unseen": len(batch),
            "provider": "candidate_id_lookup",
            "source_url": "identifier://approved-public-apis",
            "identifiers": batch,
        }
        write_json_if_absent(request_path, request)

        if not result_path.exists():
            waiting.append(request_id)
            continue
        result = read_json(result_path)
        if result.get("ok") is not True or result.get("evaluation_allowed") is not True:
            failures.append(request_id)
            continue

        statuses = result.get("candidate_statuses")
        if isinstance(statuses, list):
            counts["filtered"] += sum(
                1
                for row in statuses
                if isinstance(row, dict) and row.get("status") == "filtered_by_snapshot"
            )
            unresolved = [
                row
                for row in statuses
                if isinstance(row, dict) and row.get("status") in {"provider_unresolved", "provider_error"}
            ]
            failures.extend(str(row.get("requested_id") or request_id) for row in unresolved)

        allowed_rows = result.get("allowed_records")
        if not isinstance(allowed_rows, list):
            failures.append(request_id + ":missing_allowed_records")
            continue
        allowed_candidates: list[dict[str, Any]] = []
        library_batch_records = [
            record for ident in batch for record in id_to_records.get(ident, [])
        ]
        for row in allowed_rows:
            if not isinstance(row, dict) or not isinstance(row.get("record"), dict):
                continue
            allowed_candidates.append(merge_library_reason(row["record"], library_batch_records))
        counts["allowed"] += len(allowed_candidates)

        submission_count = max((len(allowed_candidates) + 4) // 5, 0)
        for submission_index in range(submission_count):
            candidates = allowed_candidates[submission_index * 5 : (submission_index + 1) * 5]
            submission_id = f"{request_id}-sub{submission_index + 1:02d}"
            submission_path = repo_root / DISCOVERY_SUBMISSIONS / f"{submission_id}.json"
            queue_result_path = repo_root / DISCOVERY_RESULTS / f"{submission_id}.json"
            submission = {
                "schema_version": 1,
                "operation": "submit_discovery_round",
                "candidates": candidates,
                "discovery_stats": {
                    "run_key": request["run_key"],
                    "round": request_id,
                    "axis": request["axis"],
                    "trigger": "explicit_user_request",
                    "candidate_count": len(allowed_candidates),
                    "round_submission_count": submission_count,
                    "round_submission_index": submission_index + 1,
                    "query_summary": "ChatGPT Libraryで本文確認・分類済みのaccept候補をID照合して取り込む。",
                },
                "discovery_precheck": {
                    "request_id": request_id,
                    "result_path": PRECHECK_RESULTS.joinpath(f"{request_id}.json").as_posix(),
                    "receipt": result.get("receipt"),
                },
                "user_directed_request": {
                    "request_id": f"library-import-{hashlib.sha256(token.encode('utf-8')).hexdigest()[:12]}",
                    "summary": "ChatGPT Libraryに保存済みのDiscovery判定をGitHub正規候補へ取り込む。",
                },
            }
            write_json_if_absent(submission_path, submission)
            counts["submitted"] += len(candidates)
            if not queue_result_path.exists():
                submission_waiting.append(submission_id)
                continue
            queue_result = read_json(queue_result_path)
            if queue_result.get("ok") is not True:
                failures.append(submission_id)

    failures.extend(missing_ids)
    return waiting, submission_waiting, failures, counts


def terminalize_discovery(
    repo_root: Path,
    source: Path,
    token: str,
    payload_hash: str,
    status: str,
    detail: dict[str, Any],
    *,
    blocked: bool,
) -> None:
    result_path = repo_root / RESULT_DISCOVERY / result_filename(source)
    source_ref: str | None = None
    if blocked:
        blocked_path = block_payload(source, repo_root / BLOCKED_DISCOVERY)
        source_ref = blocked_path.relative_to(repo_root).as_posix()
    else:
        source.unlink(missing_ok=True)
    replace_json(
        result_path,
        {
            "schema_version": 1,
            "artifact_type": "discovery",
            "status": status,
            "source_sha256": payload_hash,
            "retained_payload": source_ref,
            "processed_at": now(),
            **detail,
        },
    )


def process_discovery(
    repo_root: Path,
    max_records: int | None = None,
) -> tuple[int, int]:
    recover_retryable_precheck_provenance_blocks(repo_root)
    PENDING_DISCOVERY.mkdir(parents=True, exist_ok=True)
    WAITING_DISCOVERY.mkdir(parents=True, exist_ok=True)
    advanced = 0
    terminal = 0

    for source in sorted(PENDING_DISCOVERY.glob("*.json")):
        target = WAITING_DISCOVERY / source.name
        if target.exists():
            if target.read_bytes() != source.read_bytes():
                target = WAITING_DISCOVERY / f"{source.stem}-{sha256_bytes(source.read_bytes())[:12]}.json"
            else:
                source.unlink()
                continue
        source.replace(target)
        advanced += 1

    split_oversized_discovery_sources(DISCOVERY_CHUNK_RECORDS)
    waiting_sources = select_discovery_sources(max_records)
    for source in waiting_sources:
        token = source_token(source)
        raw_bytes = source.read_bytes()
        payload_hash = sha256_bytes(raw_bytes)
        try:
            payload = read_json(source)
            records = discovery_records(payload)
        except Exception as exc:
            terminalize_discovery(
                repo_root,
                source,
                token,
                payload_hash,
                "blocked_invalid",
                {"error": f"{type(exc).__name__}: {exc}"},
                blocked=True,
            )
            terminal += 1
            continue

        accepts = [r for r in records if r["classification"] == "accept"]
        relevance = [r for r in records if r["classification"] in {"unrelated", "borderline"}]

        try:
            rel_waiting, rel_failures = create_relevance_requests(repo_root, token, relevance)
            pre_waiting, sub_waiting, accept_failures, counts = create_accept_pipeline(
                repo_root, token, accepts
            )
        except Exception as exc:
            terminalize_discovery(
                repo_root,
                source,
                token,
                payload_hash,
                "blocked_pipeline",
                {"error": f"{type(exc).__name__}: {exc}"},
                blocked=True,
            )
            terminal += 1
            continue

        failures = rel_failures + accept_failures
        if failures:
            terminalize_discovery(
                repo_root,
                source,
                token,
                payload_hash,
                "blocked_downstream",
                {
                    "record_count": len(records),
                    "accept_count": len(accepts),
                    "relevance_count": len(relevance),
                    "failures": sorted(set(failures)),
                    "counts": counts,
                },
                blocked=True,
            )
            terminal += 1
            continue

        if rel_waiting or pre_waiting or sub_waiting:
            advanced += 1
            continue

        terminalize_discovery(
            repo_root,
            source,
            token,
            payload_hash,
            "imported",
            {
                "record_count": len(records),
                "run_key": payload.get("run_key"),
                "parent_run_key": payload.get("parent_run_key"),
                "chunk_index": payload.get("chunk_index"),
                "chunk_count": payload.get("chunk_count"),
                "worker_id": payload.get("worker_id"),
                "accept_count": len(accepts),
                "relevance_count": len(relevance),
                "counts": counts,
            },
            blocked=False,
        )
        terminal += 1

    return advanced, terminal


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--max-research", type=int, default=None)
    parser.add_argument("--max-discovery-records", type=int, default=None)
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()

    research_imported, research_terminal = process_research(repo_root, args.max_research)
    discovery_advanced, discovery_terminal = process_discovery(
        repo_root, args.max_discovery_records
    )

    summary = {
        "ok": True,
        "processed_at": now(),
        "research_imported": research_imported,
        "research_terminal": research_terminal,
        "discovery_advanced": discovery_advanced,
        "discovery_terminal": discovery_terminal,
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
