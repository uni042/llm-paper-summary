#!/usr/bin/env python3
"""Advance one bounded, durable Discovery classifier batch per GitHub run."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

import build_worker_worklist as worklist
import discovery_relevance_classifier as ml
import discovery_relevance_prefilter as rule


def run(root: Path, *, batch_size: int = 2000) -> dict[str, object]:
    if batch_size < 1 or batch_size > 5000:
        raise ValueError("batch_size must be 1..5000")
    policy = rule.load_policy(root)
    classifier_policy = policy.get("classifier") if isinstance(policy.get("classifier"), dict) else {}
    if not policy.get("enabled") or not classifier_policy.get("enabled"):
        return {"status": "disabled"}
    model = ml.load_model(root)
    new_model = not model
    if new_model:
        model = ml.train(root)
        path = root / ml.MODEL_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(model, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    if not model.get("approved"):
        return {"status": "model_failed_open", "training": model.get("training"), "diagnostic": model.get("diagnostic")}
    rows, _ = worklist._discovery_candidates(root)
    rows = worklist._exclude_reserved_identities(
        rows, reserved_rows=worklist._current_research_reservations(root)
    )
    decisions = ml.load_decisions(root, str(model["model_id"]))
    buckets: list[list[tuple[str, dict]]] = [[] for _ in range(ml.SHARDS)]
    for row in rows:
        key = ml.identity_key(row)
        if key not in decisions:
            buckets[ml.shard_for(key)].append((key, row))
    pending_before = sum(map(len, buckets))
    if not pending_before:
        return {
            "status": "complete", "unfiltered_count": len(rows),
            "scanned_count": len(rows), "pending_count": 0, "model_id": model["model_id"],
        }
    shard = next(i for i, entries in enumerate(buckets) if entries)
    selected = sorted(buckets[shard], key=lambda item: item[0])[:batch_size]
    values = {key: value for key, value in decisions.items() if ml.shard_for(key) == shard}
    for key, row in selected:
        # System-mechanism evidence always rescues a borderline/novel technology.
        description = str(row.get("title") or "") + " " + str(row.get("abstract") or "")
        rescue = any(regex.search(description) for regex in rule.COMPILED_SYSTEMS)
        negative = not rescue and ml.predict(str(row.get("title") or ""), model)
        values[key] = "q" if negative else "r"
    ml.save_shard(root, shard, str(model["model_id"]), values)
    return {
        "status": "advanced", "new_model": new_model, "processed_this_batch": len(selected),
        "remaining_estimate": pending_before - len(selected), "total_current": len(rows),
        "shard": shard, "model_id": model["model_id"],
        "classifier_quarantined_this_batch": sum(values[key] == "q" for key, _ in selected),
        "validation": {
            "positive_recall": model.get("validation_positive_recall"),
            "negative_quarantine_rate": model.get("validation_negative_quarantine_rate"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--batch-size", type=int, default=2000)
    args = parser.parse_args()
    print(json.dumps(run(args.repo_root.resolve(), batch_size=args.batch_size), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
