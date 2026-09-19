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
            "指定した --result の JSON を開き、decision / evaluation_allowed / receipt / results[] を確認する。",
            "decision=READY_FOR_EVALUATION かつ evaluation_allowed=true の場合だけ results[] を軽量評価する。",
            "採用候補0〜5件を operation=submit_discovery_round の不変 submission として .survey/work-queue/submissions/ に保存し、precheck の result_path と receipt を参照させる。",
            "submission 保存後は最新 queue / identity を再取得する。同一 source_url の追加ページをワーカー側で手取得しない。",
        ],
        "recovery": [
            "失敗した request は変更せず証跡として残す。",
            "新しい schema_version=3 request を作り、provider / source_url / collector_id / run_key / axis を指定する。",
            "records を直接渡さず、1つの固定した検索結果 source_url を指定する。",
            "不足時のページ送りは precheck に任せ、別クエリへ切り替えるのは同一結果集合を使い切った後にする。",
        ],
    },
    "recover_discovery_submissions.py": {
        "task": "失敗・旧形式Discovery submissionの正規経路への回収",
        "next": [
            "標準出力の recovered_count / recovered[] を確認する。",
            "recovered_count>0 の場合は各 recovered[].job_id と research_jobs_added を確認し、refresh_queue_snapshot.py で next-jobs.json を更新する。",
            "next-jobs.json に ready Research/Audit が出たら claim_worker_with_banks.py の正規claim経路で1件だけ取得する。",
            "回収できなかったsubmissionは手編集せず、対応する result の error / next_action / recovery_steps を確認する。",
        ],
        "recovery": [
            "失敗済みDiscovery submissionを上書き・削除しない。",
            "schema v3 precheck proofが不足している場合は process_discovery_precheck.py から新しい正規submissionを作る。",
            "synthetic job_idを新規作成せず、self-describing submit_discovery_round または実在するready Discovery jobだけを使う。",
            "修正後に recover_discovery_submissions.py → refresh_queue_snapshot.py の順で再確認する。",
        ],
    },
    "refresh_queue_snapshot.py": {
        "task": "Discovery反映後を含む次ジョブ一覧の再生成",
        "next": [
            ".survey/work-queue/next-jobs.json の counts / next_jobs を確認する。",
            "ready Research/Audit がある場合は claim_worker_with_banks.py の正規claim経路で max_jobs=1 の割り当てを取得する。",
            "Research/Audit がなく candidate在庫補充が必要なら、新しい探索軸を schema v3 process_discovery_precheck.py から開始する。",
            "next-jobs.json を直接編集してResearch jobを追加・選択しない。",
        ],
        "recovery": [
            "repo-root がリポジトリrootを指しているか確認する。",
            "jobs/state/resultを直接修正せず、queue_worker.py でsubmission処理と整合を先に行う。",
            "queue_worker.py 正常終了後に refresh_queue_snapshot.py を再実行する。",
        ],
    },
    "queue_worker.py": {
        "task": "キュー整合・次ジョブ一覧の更新",
        "next": [
            ".survey/work-queue/results/ に今回の未処理submissionと同名のresultが生成されたか確認する。",
            "submit_discovery_round result では ok=true / research_jobs_added / final_duplicate_filtered_count / next_action を確認する。",
            ".survey/work-queue/next-jobs.json の next_jobs と counts を確認する。",
            "ready Research/Audit がある場合は claim_worker_with_banks.py の正規経路で max_jobs=1 の割り当てを取得する。",
            "Research/Audit がなくDiscovery補充が必要なら process_discovery_precheck.py の schema v3 経路へ進む。next-jobs.json や state.json を直接編集しない。",
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
            ".survey/work-queue/claim-results/ の該当 request result と出力 assignments を確認する。",
            "assignment が1件ある場合だけ、その job / instructions / attempt_id / claim_id に従って処理する。",
            "Research/Audit 完了後は5スロットを保存し、attempt固有の immutable descriptor を .survey/work-queue/submissions/research/ または audit/ に作る。",
            "assignment が0件なら queue_worker.py で最新 queue を再取得し、別jobを手動選択しない。",
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
            ".survey/work-queue/claim-results/ の assignment と record_bank / record_bank_fallback を確認する。",
            "record_bank がある場合は、その予約済みbankの metadata / problem_method / evaluation / results / positioning の5スロットだけを使う。",
            "record_bank_fallback=library の場合はGitHub上で別bankを選ばず、完全5スロットpayloadを ChatGPT Library /LLM-survey-outbox/pending/ へ保存する。",
            "耐久保存後は attempt固有 immutable descriptor またはLibrary checkpointを正本として、queue_worker.py で次の状態を取り直す。",
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
            "標準出力 summary の failures と effects-dir に生成されたeffect/resultを確認する。",
            "failures=0 なら normalize_required_metadata.py → normalize_research_paper_paths.py → survey.py build → build_repository_inventory.py → check_repository.py の検査系へ進む。",
            "failures>0 なら失敗descriptorだけを回復対象にし、成功済みattemptを再生成しない。",
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
            "出力の decision / finalization_allowed / next_action / wait_seconds / wait_targets を確認する。",
            "decision=CONTINUE なら next_action の対象を実行し、pending target があれば同一targetを指定された間隔で再確認する。",
            "decision=STOP_RUN の場合も直接終了せず、その出力値を run_finalization_gate.py に渡す。",
            "最終応答は run_finalization_gate.py が明示的に許可するまで出さない。",
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
            "出力の permit / blocking_reasons / next_action / wait_targets / wait_seconds を確認する。",
            "permit が出ていなければ wait_targets の同一 claim / submission / ACK を再確認し、状態を更新して run_finalization_gate.py を再実行する。",
            "permit が明示的に出た場合だけ最終応答へ進む。",
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
            ".survey/update-worker/result.json を開き、ok / updated_paths / created_paths を確認する。",
            "ok=true の場合だけ、必要なら survey.py build で派生物を再生成する。",
            "その後 build_repository_inventory.py で新しいinventoryを作り、check_repository.py に渡して整合性を確認する。",
            "check_repository.py が passed になるまで更新完了扱いにしない。",
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
            "生成された README / comparison.md / .survey/survey-state/paper-identity-index.json の差分を確認する。",
            "build_repository_inventory.py --root . --output <new-inventory> で現在HEADのinventoryを作る。",
            "check_repository.py --root . --inventory <new-inventory> --report <report> を実行する。",
            "report の status=passed を確認してから publish / submission / finalization の次段へ進む。",
        ],
        "recovery": [
            "エラー対象の論文メタデータや重複識別子を修正する。",
            "生成済み README / comparison / identity index を手作業で辻褄合わせしない。",
            "元データを直して survey.py build を再実行する。",
        ],
    },
    "build_repository_inventory.py": {
        "task": "検査用リポジトリ inventory の生成",
        "next": [
            "この実行で指定した --output の inventory ファイルをそのまま check_repository.py --inventory に渡す。",
            "例: python .survey/scripts/check_repository.py --root . --inventory <output> --report <report>。",
            "inventory 生成後にリポジトリ対象ファイルを変更した場合は、そのinventoryを破棄して build_repository_inventory.py からやり直す。",
        ],
        "recovery": [
            "root と output が意図したリポジトリ・出力先を指しているか確認する。",
            "inventory を手編集せず、元ファイルを修正して再生成する。",
        ],
    },
    "maintenance_health.py": {
        "task": "保守状態・品質レポートの健全性検査",
        "next": [
            "生成reportの status / findings / errors / warnings を確認する。",
            "status=issues_found なら findings が指す元データ・queue・派生indexを修正し、maintenance_health.py を再実行する。",
            "status=passed なら build_repository_inventory.py → check_repository.py で最終整合性を確認する。",
            "check_repository.py も passed の場合だけ maintenance 完了扱いにする。",
        ],
        "recovery": [
            "missing quality report や index drift の原因を先に修正する。",
            "fail_on_error を無効化して問題を無視するのではなく、findings を解消して再実行する。",
        ],
    },
    "full_gc.py": {
        "task": "不要な一時状態・回復済みデータの GC",
        "next": [
            "GC report の deleted / skipped / protected を確認し、未完了対象が deleted に入っていないことを確認する。",
            "GC後に queue_worker.py で queue snapshot を再構築する。",
            "続けて survey.py build → build_repository_inventory.py → check_repository.py を実行し、派生物とリポジトリ整合性を確認する。",
        ],
        "recovery": [
            "protected path を手作業で削除しない。",
            "参照中・未完了の項目は削除せず、先に対応する処理を terminal 状態へ進める。",
            "状態整合後に GC を再実行する。",
        ],
    },
    "check_repository.py": {
        "task": "リポジトリ整合性検査",
        "next": [
            "--report で指定したJSONを開き、status / findings / missing_files / working_changes を確認する。",
            "status=passed なら、元の処理がResearch/Auditなら最新 queue/claim state取得、Discoveryならsubmission確認、maintenance/updateなら完了判定へ戻る。",
            "status=issues_found なら findings の元ファイル・生成元・stateを修正し、必要な生成スクリプトを再実行してから新しいinventoryで check_repository.py を再実行する。",
            "passed になるまで publish / finalization を行わない。",
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
