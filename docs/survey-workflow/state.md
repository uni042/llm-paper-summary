# 開始処理と状態

### 3.1 毎回最初にすること
1. 開始時刻、対象リポジトリの最新先頭版（HEAD）、現在利用できる読み書き手段を確認する。
2. [第4章](state.md)の状態ファイル、識別索引、見送り記録を読む。過去の会話や実行ログから状態を推測しない。
3. 未完了キューと実ファイルを照合し、前回保存済みの成果を再作成せず、未完了部分だけ復旧する。復旧だけを今回の調査・監査件数に数えない。
4. 今回の実行枠とモードを、起動元が指定する予定実行枠・モード規則から確定する。予定実行時刻が取得できるならその日本時間を使い、起動元が朝モードとして指定した枠は朝モード、それ以外は毎時モードとする。予定実行枠が取得できない場合は起動元の明示的なモード指定を使い、それもなければ通常の毎時モードとして扱う。公開手順書側で特定の時計時刻を朝モードに固定しない。開始後に時刻が変わってもモードを変更しない。
5. 識別索引が欠落・形式不明・現行ファイルと不整合なら、新規論文作成前に `papers/inference/*/*.md`（README除外）から再構築する。再構築が終わるまで新規作成は禁止。必要なら調査件数を減らし、未完了を残す。

## 4. 状態・識別情報の正本
既存の形式と値を尊重し、存在しない項目だけ初期化する。ただし運用方式の第2版への移行は次の1回だけ行う。
状態の `workflow_version` が2未満または未設定なら、未完了候補・論文実体・過去実績を保全したまま `research_batch_size=1`, `audit_batch_size=1`, `full_batch_streak=0`, `workflow_version=2` にする。これは負荷安定化のための計画的な設定移行であり、キューや既存成果の初期化ではない。第2版以降は[第10章](completion.md)の規則だけで増減する。移行と通常の中間保存はまとめてよい。
- `survey-state/exploration-state.json`：再開位置と処理状態。
  `last_run`, `last_completed_paper`, `last_lineage`, `last_morning_report_cutoff`, `recently_checked`, `pending_research`, `pending_audit`, `research_batch_size`, `audit_batch_size`, `full_batch_streak`, `recent_batch_history`。
  新規状態の初期値は調査1、監査1、連続成功0、履歴空。直近6回の割当・完了・繰越・件数設定・実行方式版・実行識別子を履歴に残す。同じ実行の複数巡回を複数回の成功に数えない。
  `last_completed_paper` は最後に正常追加または実質更新した推論論文。変更なし監査では置換しない。
- `survey-state/paper-identity-index.json`：1研究につき有効なパス1つを対応させる機械可読索引。本文の正本は論文ページ。
  各項目は `canonical_id`, `path`, `title`, `normalized_title`, 存在する `arxiv_id` / `doi` / `openreview_id`, 確認済み識別子 `aliases`, `status: active`。
- `survey-state/rejected-papers.json`：一次資料まで調査したが収録しなかった研究の永続記録。要旨だけの簡易選別は記録しない。
  可能な範囲で `canonical_id`, `title`, `identifiers`, `checked_at`, `checked_source_version`, `reason_code`, 客観的な理由、`discovery_source`, `duplicate_of` を残す。
  理由の例：`out_of_scope_training`, `out_of_scope_non_llm`, `duplicate_same_work`, `duplicate_newer_version_exists`, `insufficient_inference_systems_contribution`, `insufficient_primary_source`, `low_incremental_value`, `already_recorded`, `other_objective_reason`。
- `recently_checked` は一次資料確認済みの直近約100件。識別子、判定結果、探索経路、理由を保持する。永続の見送り記録の代用にしない。
- `survey-state/execution-log.md`：利用者向けの観測記録。現在から直近24時間分だけ保持。成果・復旧・既読判定の正本にしない。未完了キュー、識別索引、見送り記録は24時間で削除しない。
