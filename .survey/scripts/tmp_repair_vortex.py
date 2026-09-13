#!/usr/bin/env python3
from __future__ import annotations

import copy
import datetime as dt
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / ".survey" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import assemble_research_record as assemble
import claim_worker_with_banks as banks
import immutable_submission
import process_immutable_submission as processor
from japanese_style import japanese_ratio, record_prose_text
from record_bank_config import BANK_ROOTS

JOB_ID = "job-research-8df4b126a68a6be4"
ATTEMPT_ID = "attempt-manual-vortex-repair-20260914-001"
CLAIM_ID = "claim-manual-vortex-repair-20260914-001"
REQUEST_ID = "manual-vortex-repair-20260914-001"
WORKER_ID = "work-vortex-repair-20260914"
BANK = "h"

REPLACEMENTS = [
    ("query-independent", "クエリ非依存"),
    ("backward-compatible", "後方互換"),
    ("memory-bound", "メモリ律速"),
    ("compute-bound", "計算律速"),
    ("full-attention", "全注意"),
    ("full attention", "全注意"),
    ("sparse attention", "疎注意"),
    ("block table remapping", "ブロック表再マップ"),
    ("block top-k", "ブロック上位k"),
    ("top-k", "上位k"),
    ("end-to-end", "端から端まで"),
    ("programming model", "プログラミングモデル"),
    ("query", "クエリ"),
    ("attention", "注意機構"),
    ("backend", "バックエンド"),
    ("frontend", "フロントエンド"),
    ("operator", "演算子"),
    ("accuracy", "精度"),
    ("layout", "配置"),
    ("indexer", "索引器"),
    ("index", "索引"),
    ("metadata", "メタデータ"),
    ("paged", "ページ化"),
    ("page", "ページ"),
    ("radix", "基数"),
    ("sequence", "系列"),
    ("score", "スコア"),
    ("sparse", "疎"),
    ("dense", "密"),
    ("serving", "サービング"),
    ("server", "サーバー"),
    ("throughput", "スループット"),
    ("latency", "遅延"),
    ("prompt", "プロンプト"),
    ("output", "出力"),
    ("token", "トークン"),
    ("training", "学習"),
    ("backward", "逆方向"),
    ("decode", "デコード"),
    ("prefill", "プリフィル"),
    ("program", "プログラム"),
    ("algorithm", "アルゴリズム"),
    ("systems", "システム"),
    ("system", "システム"),
    ("runtime", "ランタイム"),
    ("deployment", "配備"),
    ("compiler", "コンパイラ"),
    ("cache", "キャッシュ"),
    ("kernel", "カーネル"),
    ("vendor", "ベンダー"),
    ("fallback", "フォールバック"),
    ("tensor", "テンソル"),
    ("recall", "再現率"),
    ("budget", "予算"),
    ("geometry", "形状"),
    ("shape", "形状"),
    ("size", "サイズ"),
    ("length", "長さ"),
    ("mean", "平均"),
    ("full", "全体"),
    ("ragged", "可変長"),
    ("prefix", "接頭辞"),
    ("iteration", "反復"),
    ("agent", "エージェント"),
    ("traffic", "転送量"),
    ("allocation", "割り当て"),
    ("stage", "段階"),
    ("load", "読み出し"),
    ("save", "保存"),
    ("parallelism", "並列度"),
    ("batching", "バッチ処理"),
    ("centroid", "重心"),
    ("thread", "スレッド"),
    ("template", "テンプレート"),
    ("selection", "選択"),
    ("approximate", "近似"),
    ("approx", "近似"),
    ("exact", "厳密"),
    ("reduction", "リダクション"),
    ("semantics", "意味規則"),
    ("named", "名前付き"),
    ("continuous", "連続"),
    ("pairwise", "対ごと"),
    ("workload", "ワークロード"),
    ("memory", "メモリ"),
    ("compute", "計算"),
    ("table", "表"),
    ("config", "設定"),
    ("step", "ステップ"),
    ("docs", "文書"),
    ("user", "利用者"),
    ("req", "要求"),
    ("pareto", "パレート"),
    ("block", "ブロック"),
]
TARGET_SLOTS = ("problem_method", "evaluation", "results", "positioning")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def translate_text(text: str) -> str:
    if text.startswith(("http://", "https://")):
        return text
    out = text
    for source, target in REPLACEMENTS:
        pattern = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(source) + r"(?![A-Za-z0-9_])", re.I)
        out = pattern.sub(target, out)
    return out


def translate_value(value: Any) -> Any:
    if isinstance(value, str):
        return translate_text(value)
    if isinstance(value, list):
        return [translate_value(item) for item in value]
    if isinstance(value, dict):
        return {key: translate_value(item) for key, item in value.items()}
    return value


def structure(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: structure(item) for key, item in value.items()}
    if isinstance(value, list):
        return [structure(item) for item in value]
    return type(value).__name__


def numbers(value: Any) -> list[str]:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return re.findall(r"\d+(?:\.\d+)?", text)


def urls(value: Any) -> list[str]:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return re.findall(r"https?://[^\s\"']+", text)


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()


def main() -> int:
    job_path = ROOT / ".survey/work-queue/jobs" / f"{JOB_ID}.json"
    job = read_json(job_path)
    assert job.get("canonical_id") == "arXiv:2606.06453"
    assert job.get("status") == "ready"
    assert job.get("repair_required") is True
    assert not (ROOT / str(job["paper_path"])).exists()

    recovered = banks._repair_bank_candidate(ROOT, {"job_id": JOB_ID, "kind": "research"}, set())
    assert recovered is not None, "Vortex retained record was not recoverable"
    bank, payloads, attempts = recovered
    assert bank == BANK, f"expected bank {BANK}, got {bank}"
    assert attempts == {"attempt-2606.06453-20260913-0930-v10-vortex"}, attempts

    raw_record = {slot: copy.deepcopy(payloads[slot]["data"]) for slot in assemble.SLOT_NAMES}
    candidate = copy.deepcopy(raw_record)
    for slot in TARGET_SLOTS:
        candidate[slot] = translate_value(candidate[slot])
    candidate = assemble.normalize_preferred_terms(candidate)
    candidate["metadata"] = copy.deepcopy(raw_record["metadata"])
    assemble.ensure_explanatory_summary(candidate)

    assert candidate["metadata"] == raw_record["metadata"], "metadata changed"
    for slot in TARGET_SLOTS:
        assert structure(candidate[slot]) == structure(raw_record[slot]), f"structure changed in {slot}"
        assert numbers(candidate[slot]) == numbers(raw_record[slot]), f"numeric evidence changed in {slot}"
        assert urls(candidate[slot]) == urls(raw_record[slot]), f"URLs changed in {slot}"

    issues = assemble.collect_validation_issues(candidate)
    prose = record_prose_text(candidate)
    ratio, jp_chars, latin_chars = japanese_ratio(prose)
    assert not issues, issues
    assert ratio >= 0.70, ratio

    bank_root = ROOT / BANK_ROOTS[BANK]
    refs = []
    for slot in assemble.SLOT_NAMES:
        payload = copy.deepcopy(payloads[slot])
        payload["attempt_id"] = ATTEMPT_ID
        payload["job_id"] = JOB_ID
        payload["data"] = candidate[slot]
        slot_path = bank_root / f"{slot}.json"
        write_json(slot_path, payload)
        blob_sha = immutable_submission.git_blob_sha(slot_path.read_bytes())
        refs.append({
            "slot": slot,
            "path": slot_path.relative_to(ROOT).as_posix(),
            "blob_sha": blob_sha,
        })

    claim_path = ROOT / ".survey/work-queue/claims" / f"{JOB_ID}.json"
    previous_claim = read_json(claim_path) if claim_path.exists() else {}
    claimed_at = now_iso()
    expires_at = (
        dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=2)
    ).replace(microsecond=0).isoformat()
    claim = {
        "schema_version": 1,
        "workflow_version": 10,
        "claim_id": CLAIM_ID,
        "job_id": JOB_ID,
        "worker_id": WORKER_ID,
        "worker_kind": "work",
        "attempt_id": ATTEMPT_ID,
        "request_id": REQUEST_ID,
        "claimed_at": claimed_at,
        "expires_at": expires_at,
        "kind": "research",
        "depends_on_job_ids": [JOB_ID],
    }
    if previous_claim.get("claim_id"):
        claim["previous_claim_id"] = previous_claim["claim_id"]
    write_json(claim_path, claim)

    descriptor = {
        "schema_version": 1,
        "transport_version": 10,
        "kind": "research",
        "status": "completed",
        "attempt_id": ATTEMPT_ID,
        "job_id": JOB_ID,
        "claim_id": CLAIM_ID,
        "worker_id": WORKER_ID,
        "worker_kind": "work",
        "record_bank": BANK,
        "paper_path": job["paper_path"],
        "record_slots": refs,
    }
    submission_path = ROOT / ".survey/work-queue/submissions/research" / f"{ATTEMPT_ID}.json"
    assert not submission_path.exists(), "repair attempt already exists"
    write_json(submission_path, descriptor)

    result = processor.process(ROOT, submission_path)
    assert result.get("ok") is True, result
    assert result.get("attempt_id") == ATTEMPT_ID
    assert (result.get("artifact") or {}).get("paper") == job["paper_path"]

    final_job = read_json(job_path)
    assert final_job.get("status") == "completed", final_job
    assert final_job.get("paper_path") == job["paper_path"]
    for key in ("repair_required", "validation_error", "validation_errors", "last_validation_failed_at"):
        assert key not in final_job, f"stale repair state remains: {key}"
    paper_path = ROOT / str(job["paper_path"])
    assert paper_path.exists() and len(paper_path.read_text(encoding="utf-8")) > 1000

    released = read_json(claim_path)
    released_at = now_iso()
    released["released_at"] = released_at
    released["expires_at"] = released_at
    released["release_reason"] = "manual Vortex validation repair completed"
    write_json(claim_path, released)

    result_path = ROOT / ".survey/work-queue/results/research" / f"{ATTEMPT_ID}.json"
    durable_result = read_json(result_path)
    assert durable_result.get("ok") is True
    assert durable_result.get("attempt_id") == ATTEMPT_ID

    print(json.dumps({
        "job_id": JOB_ID,
        "attempt_id": ATTEMPT_ID,
        "record_bank": BANK,
        "source_attempts": sorted(attempts),
        "japanese_ratio": ratio,
        "japanese_chars": jp_chars,
        "latin_chars": latin_chars,
        "validation_issues": issues,
        "paper_path": job["paper_path"],
        "result_path": result_path.relative_to(ROOT).as_posix(),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
