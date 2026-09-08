# GitHub Actions 共通補助実行基盤

Scheduled Task側のPython・shell・checkout可否に依存しない補助処理は、GitHub Actionsの `Survey helper worker` を共通実行基盤として使う。

## 基本フロー

1. callerが `.survey/requests/<unique>.json` をcommitする。
2. `.github/workflows/survey-helper.yml` がpushを検知してcheckout＋Pythonを起動する。
3. `.survey/scripts/action_worker.py` が許可済みoperationだけを処理する。
4. workerは `.survey/results/<same-name>.json` と、operationが生成した状態差分をcommitする。
5. callerはresultを再取得し、`ok: true` を確認してから次へ進む。

request/resultは観測・受渡し用であり、論文本文の精読や科学的判断そのものをActionsへ委譲しない。

## 許可operation

- `status`: `next_work.py` を実行し、進捗、推奨対象、`after_action` を返す。
- `claim_run`: cycle stateの次runをclaimし、run記録を作る。
- `finish_run`: 現在claimを終了し、必要なら早期cycle締め/次cycle作成まで行う。
- `planning_seed`: 繰越・overflow・新規選定枠を返す。
- `prepare_result`: paper frontmatterとactive claimからidentity/progress deltaを生成する。
- `validate`: identity delta、workflow v8 validate、unit testsを実行する。

任意shell、任意Python、任意パス編集をrequest経由で許可しない。必要な機械処理は専用operationとして追加し、入力検証を持たせる。

## `after_action` は提案で止めない

`status` の `after_action` を取得したら、単に次作業を報告してrunを終了しない。安全に実行可能なら同じ予定実行内でそのactionを実行する。

- `continue_same_run`: `next` の論文/監査を実際に処理し、保存後に再度statusを取る。
- `close_cycle`: 現在runをfinishし、早期cycle締めを実行する。
- `claim_next_run`: `claim_run` を実行する。新runがplanningなら続けて `planning_seed` を取得し、選定作業へ入る。
- `integrity_only`: run 24の整合性処理を実行する。
- `finish_run`: runを終了する。

ただし、一次資料を最後まで読めない、保存権を失った、GitHub書込みができない、文脈容量上安全に成果保存まで完走できない等の場合は、無理に次作業へ着手せず正本へ残して終了する。

## result待ち

request commit直後にresultがまだ無いことは正常。Actions実行には数秒〜数十秒かかり得る。result不在だけで同じrequestを重複作成しない。workflow runまたは最新commitを確認し、同名resultが生成されるまで待つ。`ok: false` の場合はerrorをblocker/実行記録へ残し、手動で成功扱いしない。

## commitトリガ

workflowは `.survey/requests/*.json` のpushだけで起動する。worker自身がresults/stateをcommitしてもrequest pathを変更しないため、自己再帰起動しない。
