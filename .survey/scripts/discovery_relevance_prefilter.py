#!/usr/bin/env python3
"""Conservative, reversible offline Discovery worklist prefilter.

No papers, citation pools, relevance decisions, or research jobs are modified.
A quarantine verdict changes *worklist presentation* only. Turn the config off
and regenerate worklists to restore the exact original candidate ordering.
"""
from __future__ import annotations

import hashlib
import discovery_relevance_classifier as classifier
import json
import re
from pathlib import Path
from typing import Any

CONFIG_PATH = Path(".survey/config/discovery-relevance-prefilter.json")
POLICY_VERSION = "2026-10-08-v2-shadow"

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
    ("robotics_applications", r"\b(?:autonomous (?:driving|navigation|vehicle)|robot(?:ic)? (?:grasping|manipulation|navigation)|visual slam|trajectory prediction)\b"),
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
    classifier_policy = policy.get("classifier") if isinstance(policy.get("classifier"), dict) else {}
    model = classifier.load_model(root) if root is not None and enabled and classifier_policy.get("enabled") else {}
    model_id = str(model.get("model_id") or "") if model.get("approved") else ""
    decisions = classifier.load_decisions(root, model_id) if root is not None and model_id else {}
    model_mode = str(classifier_policy.get("mode") or "shadow")
    extra_config = policy.get("expanded_rules")
    extra_mode = str(extra_config.get("mode") or "off") if isinstance(extra_config, dict) and extra_config.get("enabled") else "off"
    kept: list[dict[str, Any]] = []
    deferred: list[dict[str, Any]] = []
    rule_count = 0
    ml_count = 0
    expanded_count = 0
    expanded_applied_count = 0
    expanded_reasons: dict[str, int] = {}
    scanned = 0
    for row in rows:
        if not enabled:
            kept.append(row)
            continue
        rule_reject = classify(row, policy)["verdict"] == "quarantine"
        decision = decisions.get(classifier.identity_key(row)) if model_id else None
        if decision is not None:
            scanned += 1
        ml_reject = decision == "q" and model_mode == "quarantine"
        if rule_reject:
            rule_count += 1
        elif ml_reject:
            ml_count += 1
        expansion_reject = False
        if not rule_reject and not ml_reject and extra_mode in ("shadow", "quarantine"):
            extra = classify_expansion(row, policy)
            expansion_reject = extra["verdict"] == "quarantine"
            if expansion_reject:
                expanded_count += 1
                expanded_reasons[extra["reason"]] = expanded_reasons.get(extra["reason"], 0) + 1
        if expansion_reject and extra_mode == "quarantine":
            expanded_applied_count += 1
        if rule_reject or ml_reject or (expansion_reject and extra_mode == "quarantine"):
            deferred.append(row)
        else:
            kept.append(row)
    stats: dict[str, Any] = {
        "policy_version": POLICY_VERSION,
        "enabled": enabled,
        "mode": mode if enabled else "off",
        "unfiltered_count": len(rows),
        "quarantine_count": len(deferred),
        "rule_quarantine_count": rule_count,
        "classifier_quarantine_count": ml_count,
        "expanded_rule_mode": extra_mode if enabled else "off",
        "expanded_rule_shadow_count": expanded_count,
        "expanded_rule_applied_count": expanded_applied_count,
        "expanded_rule_reason_counts": dict(sorted(expanded_reasons.items())),
        "classifier_scanned_count": scanned,
        "classifier_pending_count": max(len(rows) - scanned, 0),
        "classifier_model_id": model_id,
        "classifier_mode": model_mode if model_id else "pending_model",
        "classifier_validation_positive_recall": model.get("validation_positive_recall"),
        "classifier_validation_negative_quarantine_rate": model.get("validation_negative_quarantine_rate"),
        "audit_count": 0,
        "reviewable_count": len(rows),
    }
    if not enabled or mode == "shadow":
        return rows, stats
    try:
        stride = max(int(policy.get("audit_stride", 50)), 2)
        max_audit = max(int(policy.get("max_audit_per_build", 30)), 0)
    except (TypeError, ValueError):
        stride, max_audit = 50, 30
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
