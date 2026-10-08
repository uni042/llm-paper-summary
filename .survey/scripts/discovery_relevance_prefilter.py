#!/usr/bin/env python3
"""Conservative, reversible offline Discovery worklist prefilter.

No papers, citation pools, relevance decisions, or research jobs are modified.
A quarantine verdict changes *worklist presentation* only. Turn the config off
and regenerate worklists to restore the exact original candidate ordering.
"""
from __future__ import annotations

import hashlib
import forward_lineage_citation
import json
import math
import re
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(".survey/config/discovery-relevance-prefilter.json")
POLICY_VERSION = "2026-10-08-v4-forward-lineage-percentile"

# Require an unambiguous *application topic in the title*. Never quarantine
# solely because a negative-domain keyword happens to appear in the abstract.
DOMAIN_TITLE_PATTERNS = (
    ("agriculture", r"\b(?:tomato|crop(?:s)?|phenotyp(?:e|ing)|agricultur\w*|wheat|orchard|rice blast|plant disease)\b"),
    ("biomedicine", r"\b(?:clinical diagnos\w*|medical imag\w*|patient care|cancer detect\w*|radiolog\w*|patholog\w*|drug discover\w*|protein fold\w*|genom\w*)\b"),
    ("chemistry", r"\b(?:chemical synthesis|organic synthesis|molecular docking|reaction prediction|catalyst discovery)\b"),
    ("political_content", r"\b(?:election disinformation|political disinformation|misinformation detect\w*|fake news detect\w*)\b"),
    ("earth_observation", r"\b(?:remote sensing|satellite imag\w*|land[- ]use classification|hyperspectral image)\b"),
    ("audio_application", r"\b(?:speech synthesis|text[- ]to[- ]speech|neural audio codec|music generation)\b"),
    ("human_behaviour", r"\b(?:social media sentiment|consumer sentiment|emotion recognition|crowd behaviour)\b"),
)
COMPILED_DOMAINS = tuple((name, re.compile(p, re.I)) for name, p in DOMAIN_TITLE_PATTERNS)

# Evidence for system-level innovations rescues cross-domain work. Bare
# words like "LLM", "Transformer", "efficient" and "performance" are not enough.
SYSTEM_EVIDENCE_PATTERNS = (
    r"\b(?:kv[- ]?cache|pagedattention|flashattention|flash[- ]attention)\b",
    r"\b(?:offload\w*|prefetch\w*|speculative decod\w*|model quantiz\w*|weight quantiz\w*)\b",
    r"\b(?:tensor parallel\w*|pipeline parallel\w*|expert parallel\w*|distributed train\w*)\b",
    r"\b(?:inference (?:latency|throughput|serving|engine|acceleration|optimization|speed|cost|efficiency))\b",
    r"\b(?:(?:llm|language model|transformer|moe) (?:serving|deployment|inference optimiz\w*|inference accelerat\w*))\b",
    r"\b(?:gpu (?:memory|kernel|offload\w*|throughput|acceleration|scheduling))\b",
    r"\b(?:memory[- ]efficient (?:attention|inference|training)|memory (?:offload\w*|bandwidth|optimization))\b",
    r"\b(?:low[- ]latency (?:inference|serving)|high[- ]throughput (?:inference|serving))\b",
    r"\b(?:optim(?:iz|is)\w* (?:llm|language model|transformer|moe) (?:inference|training|serving))\b",
)
COMPILED_SYSTEMS = tuple(re.compile(s, re.I) for s in SYSTEM_EVIDENCE_PATTERNS)


def load_policy(root: Path) -> dict[str, Any]:
    """Fail open when config is absent, invalid, or accidentally corrupted."""
    try:
        data = json.loads((Path(root) / CONFIG_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return {"enabled": False, "mode": "off"}
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        return {"enabled": False, "mode": "off"}
    if data.get("mode") not in ("shadow", "quarantine", "off"):
        return {"enabled": False, "mode": "off"}
    return data


def classify(row: dict[str, Any], policy: dict[str, Any]) -> dict[str, str]:
    """Worklist preference only: NEVER a durable unrelated/borderline verdict."""
    result = {"verdict": "review", "reason": "not_confident_off_topic", "version": POLICY_VERSION}
    if not policy.get("enabled") or policy.get("mode") == "off":
        result["reason"] = "disabled"
        return result
    canonical = str(row.get("canonical_id") or "")
    if canonical and canonical in policy.get("allow_canonical_ids", []):
        result["reason"] = "explicit_allowlist"
        return result
    title = str(row.get("title") or "").strip()
    if not title:
        result["reason"] = "missing_title"
        return result
    domain = next((name for name, pattern in COMPILED_DOMAINS if pattern.search(title)), None)
    if domain is None:
        return result
    description = title + " " + str(row.get("abstract") or "")
    if any(pattern.search(description) for pattern in COMPILED_SYSTEMS):
        result["reason"] = "system_mechanism_rescue"
        return result
    result["verdict"] = "quarantine"
    result["reason"] = "off_domain_title:" + domain
    return result



# Experimental v2 rules: require an application *phrase*, never a generic term
# such as image, finance, model, audio, transformer, or robotics alone.
# V2 starts in shadow mode; STATUS estimates incremental impact without hiding
# a single additional candidate until holdout and audit are reviewed.
EXPANSION_DOMAIN_PATTERNS = (
    ("vision_applications", r"\b(?:object detection|face recognition|facial emotion recognition|image (?:segmentation|classification|captioning|restoration|super[- ]resolution|retrieval)|visual question answering|video summarization)\b"),
    ("clinical_applications", r"\b(?:disease (?:detection|diagnosis|prediction)|clinical (?:decision support|prediction|notes)|healthcare (?:chatbot|application|question answering)|biomedical (?:entity recognition|text mining)|patient (?:outcome|monitoring|record\w*))\b"),
    ("financial_applications", r"\b(?:stock (?:price|market) prediction|credit (?:risk|scoring)|financial (?:sentiment|fraud|forecasting)|fraud detection|portfolio optimization|trading strategy)\b"),
    ("educational_legal_applications", r"\b(?:automated essay scoring|student performance prediction|educational (?:question answering|chatbot)|legal (?:case prediction|judgment prediction|document classification)|court judgment prediction)\b"),
    ("geoscience_applications", r"\b(?:weather forecasting|climate (?:projection|prediction)|seismic (?:event|prediction)|flood (?:prediction|mapping)|land cover (?:mapping|classification)|urban traffic (?:forecasting|prediction)|traffic flow prediction)\b"),
    ("content_moderation", r"\b(?:fake news (?:detection|classification)|hate speech detection|cyberbullying detection|phishing (?:email|website) detection|spam (?:message|email) detection)\b"),
    ("materials_applications", r"\b(?:material(?:s)? discovery|battery (?:capacity|life|degradation) prediction|protein (?:structure|function) prediction|drug (?:repositioning|repurposing|discovery)|molecule generation)\b"),
    ("environmental_applications", r"\b(?:bird species classification|animal behavior recognition|forest fire detection|wildfire risk prediction|pest detection)\b"),
)
COMPILED_EXPANSION = tuple((name, re.compile(expression, re.I)) for name, expression in EXPANSION_DOMAIN_PATTERNS)


def classify_expansion(row: dict[str, Any], policy: dict[str, Any]) -> dict[str, str]:
    """Conservative v2 assessment, independent of the active v1 verdict."""
    answer = {"verdict": "review", "reason": "not_explicitly_off_domain"}
    extra = policy.get("expanded_rules")
    if not isinstance(extra, dict) or not extra.get("enabled") or extra.get("mode") not in ("shadow", "quarantine"):
        answer["reason"] = "disabled"
        return answer
    identity = str(row.get("canonical_id") or "")
    if identity and identity in policy.get("allow_canonical_ids", []):
        answer["reason"] = "explicit_allowlist"
        return answer
    title = str(row.get("title") or "").strip()
    if not title:
        answer["reason"] = "missing_title"
        return answer
    match = next((name for name, pattern in COMPILED_EXPANSION if pattern.search(title)), None)
    if match is None:
        return answer
    description = title + " " + str(row.get("abstract") or "")
    if any(pattern.search(description) for pattern in COMPILED_SYSTEMS):
        answer["reason"] = "system_mechanism_rescue"
        return answer
    answer["verdict"] = "quarantine"
    answer["reason"] = "expanded_domain:" + match
    return answer



# Reversible shortlist quota: never write a permanent "unrelated" decision.
# Specialized technical evidence dominates application-domain citations/recency.
TARGET_MODEL = re.compile(
    r"\b(?:llms?|large language models?|foundation models?|language models?|"
    r"transformers?|mixture[- ]of[- ]experts?|moe|diffusion models?|"
    r"neural networks?|deep learning)\b", re.I
)
TARGET_SYSTEMS = re.compile(
    r"\b(?:inference|serving|decod(?:e|er|ing)|training|finetun(?:e|ing)|fine[- ]tun(?:e|ing)|"
    r"pre[- ]?training|parallel(?:ism)?|distributed|accelerat\w*|kernel|"
    r"gpu|cuda|tpu|memory|bandwidth|offload\w*|quantiz\w*|"
    r"compression|prun(?:e|ing)|sparsity|latency|throughput|"
    r"batching|scheduler?|checkpointing|attention)\b", re.I
)
TARGET_SPECIFIC = re.compile(
    r"\b(?:flashattention|pagedattention|vllm|sglang|tensor(rt)?[- ]llm|"
    r"llama[.]cpp|ollama|tensorrt|gptq|awq|"
    r"speculative decoding|kv[- ]?cache|mixture[- ]of[- ]experts|"
    r"expert (?:routing|parallelism|load balancing)|"
    r"training[- ]free acceleration|memory hierarchy|"
    r"cpu[- ]gpu offload\w*|parameter[- ]efficient finetun\w*)\b", re.I
)


def _fallback_topic_score(row: dict[str, Any]) -> float:
    """Tie-break zero/one-edge candidates without overpowering direct citations."""
    title = str(row.get("title") or "")
    abstract = str(row.get("abstract") or "")
    topical = bool(TARGET_MODEL.search(title))
    technical = bool(TARGET_SYSTEMS.search(title))
    score = (
        (130 if TARGET_SPECIFIC.search(title) else 0)
        + (100 if any(regex.search(title) for regex in COMPILED_SYSTEMS) else 0)
        + (65 if topical and technical else 0)
        + (23 if topical else 0)
        + (22 if technical else 0)
    )
    if topical or technical:
        if any(regex.search(abstract) for regex in COMPILED_SYSTEMS):
            score += 21
        elif TARGET_MODEL.search(abstract) and TARGET_SYSTEMS.search(abstract):
            score += 10
    return float(score)


def _relevance_rank(row: dict[str, Any]) -> tuple[Any, ...]:
    """Forward same-lineage citations rank FIRST; topic/importance only break ties.

    Citation count means the number of DISTINCT curated papers a candidate
    *itself cites*, counted inside the same fine-grained survey directory.
    The global citation_count is never substituted for this evidence.
    """
    try:
        same = max(int(row.get("forward_lineage_citation_max") or 0), 0)
        total = max(int(row.get("forward_lineage_citation_total") or 0), 0)
        priority = int(row.get("priority") or 0)
    except (TypeError, ValueError):
        same, total, priority = 0, 0, 0
    identity = str(row.get("canonical_id") or row.get("source_url") or row.get("title") or "")
    return (-same, -total, -_fallback_topic_score(row), -priority, identity)

def _quota_policy(policy: dict[str, Any]) -> tuple[str, int, int]:
    config = policy.get("relevance_quota")
    if not isinstance(config, dict) or not config.get("enabled"):
        return "off", 100, 0
    mode = str(config.get("mode") or "off")
    if mode not in ("off", "shadow", "quarantine"):
        return "off", 100, 0
    try:
        percent = int(config.get("retain_percent", 25))
        minimum = max(int(config.get("min_candidates", 100)), 0)
    except (TypeError, ValueError):
        return "off", 100, 0
    if not 1 <= percent <= 100:
        return "off", 100, 0
    return mode, percent, minimum


def _audit_key(row: dict[str, Any]) -> bytes:
    identity = str(row.get("canonical_id") or row.get("title") or row.get("source_url") or "")
    return hashlib.sha256(identity.encode("utf-8")).digest()


def triage_worklist(
    rows: list[dict[str, Any]], policy: dict[str, Any], *, root: Path | None = None
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    """Partition presentation only, keeping original pool and identity untouched.

    Shadow mode counts probable quarantines but returns *all* original rows in
    original order. Quarantine mode returns allowed + deterministic audit sample.
    """
    mode = str(policy.get("mode") or "off")
    enabled = bool(policy.get("enabled")) and mode in ("shadow", "quarantine")
    extra_config = policy.get("expanded_rules")
    extra_mode = str(extra_config.get("mode") or "off") if isinstance(extra_config, dict) and extra_config.get("enabled") else "off"
    kept: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    rule_count = 0
    expanded_count = 0
    expanded_applied_count = 0
    expanded_reasons: dict[str, int] = {}
    for row in rows:
        if not enabled:
            kept.append(row)
            continue
        rule_reject = classify(row, policy)["verdict"] == "quarantine"
        forced_allow = bool(row.get("canonical_id") and str(row.get("canonical_id")) in policy.get("allow_canonical_ids", []))
        if rule_reject:
            rule_count += 1
        expansion_reject = False
        if not rule_reject and extra_mode in ("shadow", "quarantine"):
            extra = classify_expansion(row, policy)
            expansion_reject = extra["verdict"] == "quarantine"
            if expansion_reject:
                expanded_count += 1
                expanded_reasons[extra["reason"]] = expanded_reasons.get(extra["reason"], 0) + 1
        if expansion_reject and extra_mode == "quarantine":
            expanded_applied_count += 1
        if rule_reject or (expansion_reject and extra_mode == "quarantine"):
            deferred.append(row)
        else:
            kept.append(row)
    quota_mode, quota_percent, quota_minimum = _quota_policy(policy)
    # Percentage is applied AFTER the mechanical domain rules, not before.
    quota_eligible_count = len(kept)
    quota_target = (quota_eligible_count * quota_percent + 99) // 100
    quota_removed_count = 0
    try:
        stride = max(int(policy.get("audit_stride", 50)), 2)
        max_audit = max(int(policy.get("max_audit_per_build", 30)), 0)
    except (TypeError, ValueError):
        stride, max_audit = 50, 30

    if enabled and mode == "quarantine" and quota_mode == "quarantine" and quota_eligible_count >= quota_minimum:
        # The audit sample is included in the requested percentage, not added beyond it.
        regular_budget = max(quota_target - max_audit, 0)
        if len(kept) > regular_budget:
            mandatory = {
                i for i, row in enumerate(kept)
                if str(row.get("canonical_id") or "") in policy.get("allow_canonical_ids", [])
            }
            ranked = sorted(
                (i for i in range(len(kept)) if i not in mandatory),
                key=lambda i: _relevance_rank(kept[i]),
            )
            selected = mandatory | set(ranked[:max(regular_budget - len(mandatory), 0)])
            deferred.extend(row for i, row in enumerate(kept) if i not in selected)
            quota_removed_count = len(kept) - len(selected)
            kept = [row for i, row in enumerate(kept) if i in selected]

    stats: dict[str, Any] = {
        "policy_version": POLICY_VERSION,
        "enabled": enabled,
        "mode": mode if enabled else "off",
        "unfiltered_count": len(rows),
        "quarantine_count": len(deferred),
        "quota_quarantine_count": quota_removed_count,
        "quota_target_count": quota_target,
        "quota_mode": quota_mode if enabled else "off",
        "quota_retain_percent": quota_percent,
        "quota_eligible_count": quota_eligible_count,
        "forward_lineage_2plus_count": sum(
            int(row.get("forward_lineage_citation_max") or 0) >= 2 for row in rows
        ),
        "forward_lineage_3plus_count": sum(
            int(row.get("forward_lineage_citation_max") or 0) >= 3 for row in rows
        ),
        "forward_lineage_2plus_kept": sum(
            int(row.get("forward_lineage_citation_max") or 0) >= 2 for row in kept
        ),
        "forward_lineage_nonzero_eligible": sum(
            int(row.get("forward_lineage_citation_max") or 0) > 0 for row in kept
        ),
        "rule_quarantine_count": rule_count,
        "expanded_rule_mode": extra_mode if enabled else "off",
        "expanded_rule_shadow_count": expanded_count,
        "expanded_rule_applied_count": expanded_applied_count,
        "expanded_rule_reason_counts": dict(sorted(expanded_reasons.items())),
        "audit_count": 0,
        "reviewable_count": len(rows),
    }
    if not enabled or mode == "shadow":
        return rows, stats
    kept.sort(key=_relevance_rank)
    audit_count = min(len(deferred), max_audit, len(kept) // stride + (1 if not kept else 0))
    audit_rows = [
        dict(row, prefilter_audit=True, prefilter_reason=classify(row, policy)["reason"])
        for row in sorted(deferred, key=_audit_key)[:audit_count]
    ]
    result: list[dict[str, Any]] = []
    audit_index = 0
    for row in kept:
        result.append(row)
        if audit_index < audit_count and len(result) % stride == stride - 1:
            result.append(audit_rows[audit_index])
            audit_index += 1
    result.extend(audit_rows[audit_index:])
    stats["audit_count"] = audit_count
    stats["reviewable_count"] = len(result)
    return result, stats
