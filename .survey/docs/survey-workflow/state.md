# 開始処理と実行状態

## 制御の正本

`.survey/survey-state/cycle-state.json` が実行順序の唯一の正本である。

必須属性: `cycle_number`, `cycle_id`, `max_runs: 24`, `next_run_index`, `active_claim`, `targets.research`, `targets.audit`, `current_plan_id`, `current_plan_path`, `previous_cycle_id`, `previous_plan_path`。

時刻は制御に使わない。`scheduled_at`、`started_at`、`finished_at` は観測用で、取得できない場合は省略してよい。モデルが推測した時刻を正本にしない。

## run claim

開始時に最新HEADのcycle stateを読み、次のrunをclaimする。

- claimが無い場合: `next_run_index` を取得
- 未終了claimが残る場合: 同じ `run_index` をrecovery対象とし、新しい `claim_token` でsupersedeする
- `mode` はrun 1=`planning`、2〜23=`reading`、24=`integrity`
- claim保存と `.survey/survey-state/runs/<run_id>.json` の開始記録を同一変更に入れる
- 保存後にリモート再取得し、`cycle_id/run_index/run_id/claim_token` が一致してから着手する

古いrunはsupersede後のtokenで成果を完了確定できない。古いrunが論文本体だけ保存していた場合は、次runが成果を照合してreconcileし、再読や二重加算をしない。

## 作業権

45分などの時刻期限は制御に使わない。`.survey/survey-state/leases.json` はworkflow 8ではrun claimに従属する作業権として扱い、各resourceに `cycle_id`, `run_index`, `run_id`, `claim_token` を記録する。有効性は最新 `cycle-state.active_claim.claim_token` との一致で判定する。

resource: `paper:<canonical_id>`、`planning:<cycle_id>`、`maintenance:<cycle_id>`。別tokenが現在のclaimなら古い作業権は失効する。保存前に最新HEADのclaim tokenを再確認する。

## 進捗の正本

選定planはsnapshotであり、毎論文の完了で巨大plan/queueを書き換えない。動的進捗は `.survey/survey-state/progress-deltas/<cycle_id>/<side>/<canonical_id>.json` を正本とする。

論理状態は「plan snapshot + progress delta」。旧planに既に `status: completed` がある場合はその完了を保持する。progress deltaは同じ項目を二度完了にしない。

## 互換状態

`.survey/survey-state/runtime.json`, `daily-plans/`, `queues/`, `daily-history.json` はworkflow 7以前の履歴・表示・移行用。workflow 8ではcycle stateとcycle plan/historyを優先する。queueは繰越backlogの保持と選定時の補助に使えるが、毎論文の完了更新は要求しない。

## run記録

必須属性は `run_id`, `cycle_id`, `run_index`, `mode`, `claim_token`, `status`, `stage`, `workflow_commit`, `workflow_version`。朝報告対象なら `overlays: ["morning"]` を持てる。時刻は観測できたものだけ追加する。

実行終了時は `.survey/scripts/cycle_state.py finish` と同じ規則でclaimを解放し、通常runなら次indexへ進める。早期完了ならcycleを閉じて次cycle run 1へ、run 24なら必ずcycleを閉じて次cycle run 1へ進める。
