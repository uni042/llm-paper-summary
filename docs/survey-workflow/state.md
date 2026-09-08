# 開始処理と状態

### 3.1 毎回最初にすること
1. 開始時刻、対象リポジトリの最新先頭版（HEAD）、現在利用できる読み書き手段を確認する。[安定実行・復旧仕様](reliability.md)に従い、開始記録を保存確認する。
2. `survey-state/state-layout.json` を読み、今回必要な分割状態だけを読む。精読・監査なら `runtime.json`、当日plan、該当queue、`rejected-papers.json`、`paper-identity-index.json`、`leases.json` を基本とする。日次選定ならさらに `daily-history.json`、朝は `maintenance-queue.json` と `blockers.json` も読む。
3. 未完了queueと実ファイルを照合し、前回保存済みの成果を再作成せず、未完了部分だけ復旧する。復旧だけを今回の調査・監査件数に数えない。
4. 予定実行枠を基に、起動元の規則で日次選定・精読・朝の更新確認のいずれかを確定する。開始の遅れでモードを切り替えない。通常は日次切替を選定モードで行う。当日計画が欠落・期限切れ・選定途中なら、精読モードが作業権を取って選定処理を代行できる。旧期間の遅延実行で現行計画を巻き戻さない。
5. 識別索引が欠落・形式不明・現行ファイルと不整合なら、新規論文作成前に `papers/inference/*/*.md`（README除外）から再構築する。再構築が終わるまで新規作成は禁止。

## 4. 状態・識別情報の正本
workflow v5では、巨大な単一JSONを通常更新しない。状態は用途別に分ける。

- `survey-state/state-layout.json`：状態ファイルの配置と方式版。最初に読む。
- `survey-state/runtime.json`：`workflow_version`, `last_run`, `last_completed_paper`, `last_lineage`, `last_morning_report_cutoff`, 当日目標、現在planへの参照など、頻繁に変わる小さい実行状態。
- `survey-state/daily-plans/YYYY-MM-DD.json`：1読書日につき1ファイル。当日plan本体。`selected_papers`, `selected_audits`, 期間、目標、shortfall、statusを保持する。項目ごとの完了はこのファイルだけを書き換え、全履歴を巻き込まない。
- `survey-state/queues/research.json`：精読の未完了・翌日以降の候補。
- `survey-state/queues/audit.json`：監査の未完了・翌日以降の候補。
- `survey-state/daily-history.json`：締め済みplanの増減判定だけを永続保持する。実行中の細かな進捗は入れない。
- `survey-state/recently-checked.json`：直近の調査結果。永続見送りの代用にしない。
- `survey-state/maintenance-queue.json`：README件数、一覧、一言説明、派生索引、リンク、表示上の整合性など、研究成果そのものと切り離して後で自力修復できる保守項目。論文の精読queueへ混ぜない。
- `survey-state/blockers.json`：通常の再試行や保守処理だけでは解消できず、外部条件・権限・利用者判断などが必要な未解決問題。解決するまで24時間ログとは独立して保持する。
- `survey-state/paper-identity-index.json`：1研究につき有効なパス1つを対応させる機械可読索引。論文本文と合わせて同一性の正本。
- `survey-state/rejected-papers.json`：根拠付きの永久除外記録。取得不能は含めない。
- `survey-state/runs/`：開始・途中・終了の観測記録。状態の正本ではない。旧 `log/` は移行前形式。
- `survey-state/leases.json`：期限付きの作業権。
- `survey-state/retry-papers.json`：本文取得の再確認日と履歴。
- `survey-state/STATUS.md`：上記から生成する進捗表示。
- `survey-state/exploration-state.json`：workflow v3までの移行スナップショット。v5以降は読み取り専用。新しい進捗を書き込まない。

### 4.1 当日plan項目
`selected_papers` / `selected_audits` は `canonical_id`, `title`, `source_url`, `source_version`, `discovery_source`, `carried_from`, `status`, `next_action` を基本とする。新規選定する精読候補はさらに `publication_date`, `last_revision_date`, `venue`, `venue_status`, `venue_verified_url`, `priority_tier`, `priority_reason`, `primary_source_preflight` を確認できる範囲で持つ。

`primary_source_preflight` は `checked_at`, `status: available|unavailable`, `preferred_url`, `fallback_url`, `retrieval_kind` を持つ。選定時点で通常の一次資料経路と別の公式経路の双方から本文を取得できない候補は当日planへ入れず、`retry-papers.json` に `insufficient_primary_source` として保存し、7日後に再確認する。当日選定では別候補を探す。

精読完了時は `result`, `completed_at`, `artifact_paths`, `verified_commit` を残す。一次資料本文を精読した採用・更新・見送りと、本文取得不能の見送りを混同しない。`blocked` はGitHub保存競合、認証・権限、実行基盤障害など後で再開すべき処理障害に使う。

### 4.2 maintenance と blocker の境界
- 自力で再生成・再照合・再保存できる問題は `maintenance-queue.json`。
- 利用者判断、権限付与、外部サービス復旧など自力解消できない問題だけ `blockers.json`。
- 研究成果の保存成功後に派生README更新だけ失敗した場合、論文成果を巻き戻さずmaintenanceへ送る。
- blockerは `id`, `first_seen`, `last_seen`, `severity`, `problem`, `impact`, `attempted_fixes`, `user_action_required`, `requested_action`, `status` を持ち、解決時に `resolved_at` を追加する。

### 4.3 見送りと最近確認
`rejected-papers.json` には可能な範囲で `canonical_id`, `title`, `identifiers`, `checked_at`, `checked_source_version`, `reason_code`, 客観的な理由、`discovery_source`, `duplicate_of` を残す。取得不能は永久見送りへ入れず `retry-papers.json` に試行経路・エラー・7日後の再確認日を残す。永久除外の基準は[安定実行・復旧仕様](reliability.md)に従う。
`recently-checked.json` は直近約100件を目安とし、永続見送り・日次履歴・queueの代用にしない。

識別索引は形式3を用い、`papers[canonical_id].path` と `identifier_to_canonical` で直接照合する。論文の必須属性と比較属性は[共通仕様](reliability.md)に従う。
