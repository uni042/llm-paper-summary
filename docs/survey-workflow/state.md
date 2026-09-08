# 開始処理と状態

### 3.1 毎回最初にすること
1. 開始時刻、対象リポジトリの最新先頭版（HEAD）、現在利用できる読み書き手段を確認する。
2. [第4章](state.md)の状態ファイル、識別索引、見送り記録を読む。過去の会話や実行ログから状態を推測しない。
3. 未完了キューと実ファイルを照合し、前回保存済みの成果を再作成せず、未完了部分だけ復旧する。復旧だけを今回の調査・監査件数に数えない。
4. 予定実行枠を基に、起動元の規則で日次選定・精読・朝の更新確認のいずれかを確定する。開始の遅れでモードを切り替えない。予定枠が不明なら起動元の明示指定を使い、それもなければ精読モードとする。日次切替は選定モードだけで行う。
5. 識別索引が欠落・形式不明・現行ファイルと不整合なら、新規論文作成前に `papers/inference/*/*.md`（README除外）から再構築する。再構築が終わるまで新規作成は禁止。必要なら調査件数を減らし、未完了を残す。

## 4. 状態・識別情報の正本
既存成果・未完了候補・監査キュー・実績は保全する。第3版移行は1回だけ行い、`workflow_version=3`、`daily_reading_target=10`、`daily_audit_target=10`、`daily_plan=null`、`daily_reading_history=[]` を設定する。日次本数を毎回10に戻さない。旧 `research_batch_size`, `audit_batch_size`, `full_batch_streak`, `recent_batch_history` は履歴として残すが、第3版の制御には使わない。

- `survey-state/exploration-state.json`：既存の再開位置と処理状態に以下を追加する。
  - `daily_reading_target` と `daily_audit_target`：精読・監査それぞれの当日目標（最小1、初期各10）。日次選定時に側ごとに独立して変更する。
  - `daily_plan`：未作成ならnull。作成後は `plan_id`, `period_start`, `period_end`, `target`（精読目標）, `audit_target`（監査目標）, `status: selecting|ready|closed`, `selected_papers`, `selected_audits`, `selection_shortfall`, `audit_selection_shortfall`, `selection_error`, `audit_selection_error` を持つ。期間は起動元指定の選定枠から次の選定枠直前まで。途中保存して選定を再開できるようにする。
  - 各 `selected_papers` と `selected_audits`：`canonical_id`, `title`, `source_url`, `source_version`（確認できる場合）, `discovery_source`, `carried_from`（繰越時）, `status: pending|reading|completed|blocked`, `next_action`。完了時は `result`, `completed_at`, `artifact_paths` を残し、保存確認後に `verified_commit` を補完する。
  - 精読候補の一次資料本文を [精読・監査手順](hourly.md) の取得確認後も取得できない場合は、`rejected-papers.json` への保存確認後に `status: completed`, `result: not_selected`, `reason_code: insufficient_primary_source` として決着させる。これは再試行待ちの `blocked` にしない。`blocked` はGitHub保存競合、認証・権限、実行基盤障害など、論文の採否ではなく後で再開すべき処理障害に使う。
  - `daily_reading_history`：日次確定結果。期間・精読と監査それぞれの目標・選定数・全文精読完了数・取得不能見送り数・その他の見送り数・未完了識別子・次目標・判定理由を `plan_id` ごとに1件保存し、同一日の増減を二重適用しない。日次履歴は24時間で削除しない。
  - `pending_research`：当日未完了・次回候補・枠外の繰越を保持。識別子で当日計画と照合し、別の独立した割当にはしない。精読結果または永続見送り結果の保存確認が済んだ項目だけ除く。
  - `pending_audit`：当日監査未完了と枠外繰越。`selected_audits` と識別子で照合し、監査完了だけ除く。精読本数に混ぜない。
  - `last_run`, `last_completed_paper`, `last_lineage`, `last_morning_report_cutoff`, `recently_checked` は既存意味を維持する。変更なし監査で `last_completed_paper` を置換しない。
- `survey-state/paper-identity-index.json`：1研究につき有効なパス1つを対応させる機械可読索引。本文の正本は論文ページ。
  各項目は `canonical_id`, `path`, `title`, `normalized_title`, 存在する `arxiv_id` / `doi` / `openreview_id`, 確認済み識別子 `aliases`, `status: active`。
- `survey-state/rejected-papers.json`：収録しなかった研究の永続記録。原則は一次資料まで調査して記録する。ただし、正式な一次資料本文が存在することを確認できる一方で、[精読・監査手順](hourly.md) に定める通常URL＋別の公式配布経路の確認後も本文を取得できない候補は例外として `insufficient_primary_source` で記録してよい。この場合は要旨や検索結果から本文内容を推測せず、取得を試みた公式経路と取得不能である事実だけを記録する。
  可能な範囲で `canonical_id`, `title`, `identifiers`, `checked_at`, `checked_source_version`, `reason_code`, 客観的な理由、`discovery_source`, `duplicate_of` を残す。`insufficient_primary_source` では `attempted_sources` と `retrieval_error` も残す。
  理由の例：`out_of_scope_training`, `out_of_scope_non_llm`, `duplicate_same_work`, `duplicate_newer_version_exists`, `insufficient_inference_systems_contribution`, `insufficient_primary_source`, `low_incremental_value`, `already_recorded`, `other_objective_reason`。
- `recently_checked` は一次資料確認済みの直近約100件。識別子、判定結果、探索経路、理由を保持する。永続の見送り記録の代用にしない。一次資料本文未取得で `insufficient_primary_source` にした候補は、本文確認済みと誤解しないようその旨を結果に明示する。
- `survey-state/execution-log.md`：利用者向けの観測記録。現在から直近24時間分だけ保持。成果・復旧・既読判定の正本にしない。未完了キュー、識別索引、見送り記録は24時間で削除しない。
