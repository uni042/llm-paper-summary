#!/usr/bin/env python3
"""Worker-facing execution guidance for repository CLI scripts.

Messages are written to stderr so machine-readable stdout (especially JSON)
remains unchanged.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable

DEFAULT_PROFILE = {
    "task": "リポジトリ処理",
    "next": [
        "標準出力または生成された結果ファイルを確認し、そこに示された next_action / instructions に従う。",
        "次の操作を開始する前に、今回の処理が正常終了したことを確認する。",
    ],
    "recovery": [
        "エラーになった操作を飛ばして別経路へ進まない。",
        "エラー文・入力ファイル・現在の状態を確認して入力を修正し、同じ正規スクリプトを再実行する。",
        "状態ファイルや結果ファイルを手作業で成功扱いに書き換えない。",
    ],
}

PROFILES = {
    "process_discovery_precheck.py": {
        "task": "探索候補の取得・重複除外・ページ送り",
        "next": [
            "result JSON の decision と evaluation_allowed を確認する。",
            "READY_FOR_EVALUATION の場合だけ results[] を評価し、result_path と receipt を submit_discovery_round 側へ渡す。",
            "同一 source_url のページ送りはこのスクリプトに任せ、ワーカー側で検索結果ページを手選別しない。",
        ],
        "recovery": [
            "失敗した request は変更せず証跡として残す。",
            "新しい schema_version=3 request を作り、provider / source_url / collector_id / run_key / axis を指定する。",
            "records を直接渡さず、1つの固定した検索結果 source_url を指定する。",
            "不足時のページ送りは precheck に任せ、別クエリへ切り替えるのは同一結果集合を使い切った後にする。",
        ],
    },
    "queue_worker.py": {
        "task": "キュー整合・次ジョブ一覧の更新",
        "next": [
            "next-jobs.json または標準出力の next_jobs を確認する。",
            "claimable なジョブは claim 経路で割り当てを取得してから処理する。",
            "discovery ジョブは探索 precheck の正規経路へ進み、直接候補をキューへ書き込まない。",
        ],
        "recovery": [
            "work-queue の jobs / submissions / state を手作業で成功扱いに変更しない。",
            "指定 root が .survey 配下を指しているか確認する。",
            "入力・状態を修正後に queue_worker を再実行し、next-jobs.json が更新されてから次へ進む。",
        ],
    },
    "claim_worker.py": {
        "task": "ジョブ割り当て（claim）の処理",
        "next": [
            "出力の assignments と request ごとの result を確認する。",
            "割り当てがある場合だけ、その assignment の job / instructions に従って処理する。",
            "処理完了後は正規の submission 経路へ渡し、claim/state を直接完了扱いにしない。",
        ],
        "recovery": [
            "claim request と worker_id / worker_kind / attempt_id の整合を確認する。",
            "期限切れ・競合時は既存 claim を手修正せず、claim worker に再評価させる。",
            "キュー状態が不明な場合は queue_worker で整合してから claim を再実行する。",
        ],
    },
    "claim_worker_with_banks.py": {
        "task": "ジョブ割り当てと作業バンク予約",
        "next": [
            "assignments と banks_* の結果を確認する。",
            "割り当てに紐づく予約済みバンクだけを使って処理する。",
            "完了物は正規の submission 経路へ渡し、別バンクへ自己判断で移さない。",
        ],
        "recovery": [
            "claim と bank descriptor の対応を手作業で差し替えない。",
            "競合・期限切れ・dirty bank はこのスクリプトの回収処理に任せる。",
            "キュー整合後に同じ claim 経路を再実行する。",
        ],
    },
    "process_immutable_submission_batch.py": {
        "task": "不変 submission の一括処理",
        "next": [
            "summary の failures を確認する。",
            "failures=0 なら後続の正規化・描画・検査へ進む。",
            "失敗が残る場合は保存済み descriptor / result を使って再試行し、成功分を作り直さない。",
        ],
        "recovery": [
            "descriptors-file が正規の immutable submission descriptor 一覧を指すことを確認する。",
            "effects-dir と repo-root を確認し、途中生成物を手作業で成功扱いにしない。",
            "失敗 descriptor を修正または回復経路へ渡してから同じ batch processor を再実行する。",
        ],
    },
    "continuation_gate.py": {
        "task": "継続可否判定",
        "next": [
            "出力 decision / finalization_allowed / next_action をそのまま実行する。",
            "CONTINUE の場合は指示された作業を続ける。",
            "STOP_RUN でも finalization_allowed を確認し、最終応答前に finalization gate を通す。",
        ],
        "recovery": [
            "最新の claim 状態と submission 状態を確認してから判定をやり直す。",
            "pending を STOP_RUN 扱いにせず、同じ対象を指定された間隔で再確認する。",
            "判定結果を飛ばして直接 finalization へ進まない。",
        ],
    },
    "run_finalization_gate.py": {
        "task": "最終化許可判定",
        "next": [
            "permit / next_action / wait_targets を確認する。",
            "待機指示がある間は同じ claim / submission / ACK 対象を再確認する。",
            "明示的な最終化許可が出た場合だけ最終応答へ進む。",
        ],
        "recovery": [
            "continuation decision と finalization_allowed を再確認する。",
            "claim-state-checked / submission-state-checked を実際の最新状態確認なしに true にしない。",
            "pending 対象がある場合は指定された待機・再確認を行い、gate を再実行する。",
        ],
    },
    "update_worker.py": {
        "task": "更新 payload の検証・適用",
        "next": [
            ".survey/update-worker/result.json を確認する。",
            "ok=true の場合だけ updated_paths を後続の検査対象として扱う。",
            "適用後はリポジトリ検査を実行し、生成物と状態の整合を確認する。",
        ],
        "recovery": [
            "update-inbox.json と固定 update-payload.json の attempt_id を一致させる。",
            "既存ファイル更新では現在の blob SHA を expected_blob_sha に使う。",
            "payload_path・kind・対象パス制約を守り、検証を迂回して直接書き換えない。",
        ],
    },
    "survey.py": {
        "task": "論文索引・比較表・識別子状態の再生成",
        "next": [
            "生成差分を確認する。",
            "check_repository.py を実行して構造・メタデータ・索引の整合を検査する。",
            "検査成功後にのみ後続の公開・完了処理へ進む。",
        ],
        "recovery": [
            "エラー対象の論文メタデータや重複識別子を修正する。",
            "生成済み README / comparison / identity index を手作業で辻褄合わせしない。",
            "元データを直して survey.py build を再実行する。",
        ],
    },
    "check_repository.py": {
        "task": "リポジトリ整合性検査",
        "next": [
            "検査成功なら、その処理系の publish / submission / finalization の次段へ進む。",
            "検査結果に警告・失敗がある場合は先に原因を修正する。",
        ],
        "recovery": [
            "失敗項目を無視して publish / finalization へ進まない。",
            "エラーが示す元ファイルまたは状態を修正する。",
            "生成ファイルの問題なら生成元を直して再生成し、check_repository.py を再実行する。",
        ],
    },
}


def _profile(script: str) -> dict[str, Any]:
    base = Path(script).name
    merged = dict(DEFAULT_PROFILE)
    merged.update(PROFILES.get(base, {}))
    return merged


def _emit(line: str) -> None:
    print(line, file=sys.stderr, flush=True)


def _emit_steps(tag: str, steps: list[str]) -> None:
    for idx, step in enumerate(steps, 1):
        _emit(f"[WORKER-GUIDE][{tag}] {idx}. {step}")


def _exit_code(value: Any) -> int:
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    return 0


def _arg_value(name: str, default: str | None = None) -> str | None:
    prefix = name + "="
    for idx, arg in enumerate(sys.argv[1:]):
        if arg == name:
            pos = idx + 2
            return sys.argv[pos] if pos < len(sys.argv) else default
        if arg.startswith(prefix):
            return arg[len(prefix):]
    return default


def _postcheck(script: str) -> tuple[bool, str | None]:
    if Path(script).name != "update_worker.py":
        return True, None
    root = Path(_arg_value("--root", ".survey") or ".survey")
    result_path = root / "update-worker" / "result.json"
    try:
        payload = json.loads(result_path.read_text(encoding="utf-8"))
    except Exception:
        return True, None
    if payload.get("ok") is False:
        return False, str(payload.get("error") or "result.json reported ok=false")
    return True, None


def emit_wait(script: str) -> None:
    prof = _profile(script)
    _emit(
        f"[WORKER-GUIDE][待機] {Path(script).name}: {prof['task']}を実行中です。"
        "完了またはエラー案内が出るまで次の操作をせず待機してください。"
    )


def emit_done(script: str) -> None:
    prof = _profile(script)
    _emit(f"[WORKER-GUIDE][完了] {Path(script).name}: 処理が正常終了しました。")
    _emit_steps("次", list(prof["next"]))


def emit_error(script: str, reason: str) -> None:
    prof = _profile(script)
    _emit(f"[WORKER-GUIDE][手順エラー] {Path(script).name}: {reason}")
    _emit("[WORKER-GUIDE][正しい手順] エラーを無視して別経路へ進まないでください。")
    _emit_steps("正しい手順", list(prof["recovery"]))


def run_guided(main_func: Callable[[], Any], *, script: str | None = None) -> Any:
    script = script or sys.argv[0] or getattr(main_func, "__module__", "script")
    emit_wait(script)
    try:
        value = main_func()
    except SystemExit as exc:
        code = _exit_code(exc.code)
        if code == 0:
            emit_done(script)
        else:
            emit_error(script, f"終了コード {code} で停止しました。引数または前提手順を確認してください。")
        raise
    except BaseException as exc:
        emit_error(script, f"{type(exc).__name__}: {exc}")
        raise

    code = _exit_code(value)
    post_ok, post_reason = _postcheck(script)
    if code != 0:
        emit_error(script, f"終了コード {code} で停止しました。")
    elif not post_ok:
        emit_error(script, post_reason or "結果ファイルが失敗を報告しました。")
    else:
        emit_done(script)
    return value
