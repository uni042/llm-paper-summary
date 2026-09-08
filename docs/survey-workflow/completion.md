# 完了判定・日次件数調整・実行記録

## 10. 実行の終了
- 正常完了したcore成果だけ該当queueから除く。README等の派生不整合はmaintenanceへ送り、core完了を取り消さない。
- 今回割り当てたcore作業と保存確認が完了なら `completed`、一部成功かつ今回対象に残りがあれば `partial`、主要core作業を実行・保存できなければ `failed`。
- 精読と監査の完了率に偏りがある場合は低い側を優先する。
- 全文精読完了は一次資料本文を精読し、採否・core成果を保存確認した状態。取得不能見送りは当日項目として決着済みだが全文精読完了には数えない。
- 自力解消可能な残件は `maintenance-queue.json`、自力解消不能で外部条件や利用者対応が必要な残件だけ `blockers.json` に残す。

## 日次件数の調整
精読と監査に独立適用する。精読側でn本すべてが全文精読完了なら翌日は `n+1`。未完了が残れば `max(1,n-1)`。すべて決着済みだが `insufficient_primary_source` の取得不能見送りだけがある場合は据え置く。監査側はn本すべて正式監査完了なら `n+1`、未完了があれば `max(1,n-1)`。候補不足でn未満かつ選定済み全件完了なら据え置く。

締め結果は `daily-history.json` にplan_idごとに1件保存する。同一plan_idが存在すれば再加減算しない。

## maintenance queue
各項目は `id`, `kind`, `affected_paths`, `detected_at`, `source_commit`, `evidence`, `attempt_count`, `last_error`, `next_action`, `status: open|resolved` を基本とする。論文本文、識別索引、当日planから再生成できる派生物だけを入れる。解決時は `resolved_at` と修復commitを残す。古いresolved項目は朝の点検で整理してよい。

## blockers
`blockers.json` は自力で解消できない問題だけを保持する。実行ごとの一時失敗やREADME不整合を入れない。各実行で既存blockerの状態を悪化させず、解決確認時だけcloseする。朝の集約ではopen blockerを要約対象にする。

## 実行ログ
各実行の終了時に `survey-state/log/` へ1実行1ファイルで保存する。ファイル名は予定実行枠を先頭に `YYYY-MM-DDTHH-MM+0900_<run_id>.md` とする。
各ログに `started_at`, `finished_at`, 予定枠, `run_id`, `workflow_version`, mode, status, plan_id、精読・監査進捗、取得不能見送り、core保存結果、派生更新またはmaintenance登録、blocker追加／解消、確認commit、支障を記録する。

新しいログを保存・再取得して確認した後、`survey-state/log/` を列挙し、各ログの `finished_at` を基準に現在時刻から24時間を超えたログを古い順に削除する。README等の運用説明は削除対象外。ログは成果・queue・blocker・日次履歴の正本にしない。

通知は起動元の指示に従う。
