#!/usr/bin/env python3
"""Frozen, validated, stdlib-only supervised Discovery relevance classifier."""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json
import math
from pathlib import Path
import re
from typing import Any

import citation_graph

MODEL_PATH = Path(".survey/work-queue/discovery-prefilter/model.json")
SHARD_DIR = Path(".survey/work-queue/discovery-prefilter")
SHARDS = 16
SCHEMA = 1
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOP = {"the", "a", "an", "of", "to", "with", "and", "for", "on", "in", "by", "from", "via", "using", "based", "toward", "towards", "through", "its", "at", "is", "are", "as"}


def normalize_title(value: Any) -> str:
    return " ".join(TOKEN_RE.findall(str(value or "").lower()))


def features(title: str) -> set[str]:
    tokens = [t for t in TOKEN_RE.findall(title.lower()) if t not in STOP and len(t) > 1]
    return {"u:" + token for token in tokens} | {
        "b:" + x + "_" + y for x, y in zip(tokens, tokens[1:])
    }


def identity_key(row: dict[str, Any]) -> str:
    # Title edits invalidate the previous verdict automatically.
    identity = str(row.get("canonical_id") or row.get("source_url") or row.get("title") or "")
    return sha256((identity + "\x00" + normalize_title(row.get("title"))).encode("utf-8")).hexdigest()[:20]


def shard_for(key: str) -> int:
    return int(key[:2], 16) % SHARDS


def _paper_labels(root: Path) -> tuple[list[str], list[str]]:
    positives = {normalize_title(p.meta.get("title")) for p in citation_graph.load_records(root)}
    positives.discard("")
    path = root / ".survey/work-queue/reference-curation/unrelated-papers.json"
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        payload = {}
    records = payload.get("records") if isinstance(payload, dict) else {}
    negatives = {
        normalize_title(row.get("title"))
        for row in (records.values() if isinstance(records, dict) else [])
        if isinstance(row, dict) and row.get("title")
    }
    negatives.difference_update(positives)
    negatives.discard("")
    return sorted(positives), sorted(negatives)


def _partition(titles: list[str]) -> tuple[list[str], list[str]]:
    train, valid = [], []
    for title in titles:
        test = int.from_bytes(sha256(title.encode("utf-8")).digest()[:2], "big") % 5 == 0
        (valid if test else train).append(title)
    return train, valid


def _train_weights(pos: list[str], neg: list[str], max_features: int = 24000) -> dict[str, float]:
    p, n = Counter(), Counter()
    for title in pos:
        p.update(features(title))
    for title in neg:
        n.update(features(title))
    vocabulary = set(p) | set(n)
    v = max(len(vocabulary), 1)
    ps = sum(p.values()) + v
    ns = sum(n.values()) + v
    weights = {
        key: math.log((p[key] + 1) / ps) - math.log((n[key] + 1) / ns)
        for key in vocabulary
    }
    top = sorted(weights, key=lambda key: (-abs(weights[key]), key))[:max_features]
    return {key: round(weights[key], 5) for key in sorted(top)}


def _score(title: str, weights: dict[str, float]) -> float:
    tokens = features(title)
    return sum(weights.get(token, 0.0) for token in tokens) / math.sqrt(len(tokens)) if tokens else 0.0


def train(root: Path) -> dict[str, Any]:
    pos, neg = _paper_labels(root)
    p_train, p_valid = _partition(pos)
    n_train, n_valid = _partition(neg)
    model: dict[str, Any] = {
        "schema_version": SCHEMA,
        "classifier": "balanced-title-unigram-bigram-multinomial-naive-bayes",
        "training": {
            "positive": len(p_train), "negative": len(n_train),
            "validation_positive": len(p_valid), "validation_negative": len(n_valid),
        },
        "approved": False, "threshold": None, "weights": {},
    }
    if min(len(p_train), len(n_train)) < 60 or len(p_valid) < 20 or len(n_valid) < 30:
        model["diagnostic"] = "insufficient_labeled_examples_fail_open"
    else:
        weights = _train_weights(p_train, n_train)
        positive_scores = [_score(title, weights) for title in p_valid]
        threshold = min(positive_scores) - 0.25  # zero misses on held-out positives
        rejected_negatives = sum(_score(title, weights) < threshold for title in n_valid)
        model.update({
            "weights": weights, "threshold": round(threshold, 6),
            "validation_positive_recall": 1.0,
            "validation_negative_quarantine_rate": round(rejected_negatives / len(n_valid), 5),
            "approved": True,
            "diagnostic": "zero_positive_holdout_quarantines",
        })
    blob = json.dumps(model, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    model["model_id"] = sha256(blob.encode("utf-8")).hexdigest()[:20]
    return model


def load_model(root: Path | None) -> dict[str, Any]:
    if root is None:
        return {}
    try:
        model = json.loads((root / MODEL_PATH).read_text(encoding="utf-8"))
    except (OSError, ValueError, UnicodeError):
        return {}
    if not isinstance(model, dict) or model.get("schema_version") != SCHEMA:
        return {}
    return model


def predict(title: str, model: dict[str, Any]) -> bool:
    if not model.get("approved") or not title or not model.get("weights"):
        return False
    return _score(title, model["weights"]) < float(model["threshold"])


def load_decisions(root: Path | None, model_id: str) -> dict[str, str]:
    results: dict[str, str] = {}
    if root is None or not model_id:
        return results
    for shard in range(SHARDS):
        path = root / SHARD_DIR / f"shard-{shard:02d}.json"
        try:
            record = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError, UnicodeError):
            continue
        if isinstance(record, dict) and record.get("schema_version") == SCHEMA and record.get("model_id") == model_id:
            values = record.get("decisions")
            if isinstance(values, dict):
                results.update({key: val for key, val in values.items() if isinstance(key, str) and val in ("q", "r")})
    return results


def save_shard(root: Path, shard: int, model_id: str, decisions: dict[str, str]) -> None:
    path = root / SHARD_DIR / f"shard-{shard:02d}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {"schema_version": SCHEMA, "model_id": model_id, "decisions": dict(sorted(decisions.items()))}
    content = json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    if not path.is_file() or path.read_text(encoding="utf-8") != content:
        path.write_text(content, encoding="utf-8")
