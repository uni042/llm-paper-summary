# 成果の保存と検証

## 小さい正本を優先する

通常runでは巨大な派生ファイルやplan全体を書き換えず、以下の小さい正本を優先する。

- 論文本体または監査済み論文ページ
- `.survey/survey-state/identity-deltas/`（必要な場合）
- `.survey/survey-state/progress-deltas/<cycle_id>/<side>/...`
- `.survey/survey-state/runs/` のrun記録
- `.survey/survey-state/cycle-state.json` のclaim/state

`.survey/survey-state/paper-identity-index.json`、各系統README、比較表、STATUSは再生成可能な派生物として24回目の整合性チェックへ回せる。

## progress delta

必須: `schema_version`, `workflow_version`, `cycle_id`, `plan_id`, `side`, `canonical_id`, `status`, `run_id`, `run_index`。

成果保存時は現在の `claim_token` も記録し、最新cycle claimと一致することを保存前に確認する。古いtokenのdeltaは完了確定に使わない。

既に旧runで論文本体が保存済みの場合は、既存成果とrun記録を検証して `recovery_only` / `recovered_from_run` を付けたdeltaを作成できる。再読や二重加算をしない。

## identity delta

形式3のidentity indexはcompact済みsnapshotとして維持する。通常runは小さいidentity deltaを使い、巨大snapshot全体を書き換えない。別canonical IDとの識別子衝突だけは保存前に止める。

## connector-only

完全checkoutがなくても、論文本体・identity delta・progress deltaの小さい変更を順に保存できる。可能ならGit data APIで一つのcommitへまとめる。途中まで保存された場合は、次runが成果をreconcileする。plan/queueの巨大更新ができないことだけで論文成果を未完了に戻さない。

## 生成物

各系統READMEが大きくなっても、生成範囲は `.survey/scripts/survey_v8.py build` を優先する。非生成の局所修正には `.survey/scripts/repo_edit.py` を `--root .` 付きで使える。24回目にidentity delta compact、生成README/件数/比較表/STATUSの再生成と検証を行う。
