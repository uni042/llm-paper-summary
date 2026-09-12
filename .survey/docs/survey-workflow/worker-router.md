# Chat worker router — workflow v10

この文書は **通常Scheduled Chat worker（毎時`:30`）の時刻routing・maintenance routing・正本の優先関係** を定義する。通常論文runの継続・待ち時間削減・可視queueの扱いは [always-on-worker.md](always-on-worker.md)、discoveryの継続・停止は [discovery-continuation-policy.md](discovery-continuation-policy.md) と [discovery-exhaustive-run-policy.md](discovery-exhaustive-run-policy.md)、transportは [queue-v10.md](queue-v10.md) と [fallback-routing.md](fallback-routing.md)、全runのSTOP判定は [continuation-policy.json](continuation-policy.json) を正本とする。

通常workerとは別に毎時`:00` JSTで探索専用Scheduled Chat workerを動かしてよい。探索専用workerの正本は [discovery-specialist-worker.md](discovery-specialist-worker.md)。探索専用workerの追加を理由に通常workerのdiscovery機能を削除・停止・縮小しない。

## 1. 毎runのブートストラップ

毎回default branch最新HEADを取得し、同じHEADから少なくとも次を読む。

- 本router
- [always-on-worker.md](always-on-worker.md)
- [queue-v10.md](queue-v10.md)
- [candidate-buffer-policy.md](candidate-buffer-policy.md)
- [discovery-continuation-policy.md](discovery-continuation-policy.md)
- [discovery-exhaustive-run-policy.md](discovery-exhaustive-run-policy.md)
- [continuation-policy.json](continuation-policy.json)
- [fallback-routing.md](fallback-routing.md)
- [backlog-resilience.md](backlog-resilience.md)
- [suggestion-box.md](suggestion-box.md)
- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`

必要に応じて `.survey/work-queue/jobs/`、`.survey/survey-state/paper-identity-index.json`、identity delta、`.survey/work-queue/records/bank-registry.json`、[paper template](../../templates/paper.md) を読む。

### 正本の優先範囲

同じ事項を複数文書へ重複定義しない。矛盾を見つけた場合は、事項ごとに次を優先する。

- **時刻routing / maintenance gate**: 本router
- **通常論文runの継続、Actions待ち、`next-jobs.json`の可視範囲**: `always-on-worker.md`
- **candidate水位**: `candidate-buffer-policy.md`
- **discoveryの継続・探索空間枯渇判定**: `discovery-continuation-policy.md` / `discovery-exhaustive-run-policy.md`
- **queue / structured transport**: `queue-v10.md`
- **fallback / replay**: `fallback-routing.md`
- **run全体のSTOP判定**: `continuation-policy.json`
- **本文品質**: `.survey/templates/paper.md`

Google Drive fallback、Notion、旧 `/LLM-survey-fallback/` は新規保存・replay・backlog判定に使わない。Drive実装の保存版は `archive/drive-fallback-before-removal-20260910` ブランチにのみ残す。

## 2. 24-run maintenance gate

時刻routingより先に `.survey/work-queue/maintenance-cycle.json` を処理する。カウント対象は通常Scheduled Chat workerだけで、探索専用workerの毎時`:00` runは加算しない。

1. 現在のScheduled Chat実行枠をJSTで一意な `run_key` とする。
2. `last_counted_run_key` が同じなら二重加算しない。
3. 新しいrunなら `total_runs_counted += 1`、`runs_since_maintenance += 1`、`last_counted_run_key = run_key` を保存する。
4. `runs_since_maintenance < cadence_runs` なら通常routingへ進む。cadence値はstateを正本とする。
5. `runs_since_maintenance >= cadence_runs` のrunでは、同じ更新で `runs_since_maintenance = 0`、`maintenance_sequence += 1`、`maintenance_pending = true`、`last_maintenance_requested_at` を設定する。
6. maintenance runは論文worker、その他更新worker、fallback replay、discovery、research、auditを行わない。`.github/workflows/maintenance.yml` にfull GC + repository-wide consistency checkを委ね、そのrunは終了する。
7. maintenance失敗・遅延でpendingが残っても後続run全体は止めず、問題として扱う。

maintenanceは論文Markdown、docs、scripts、workflow、現在参照中job、queue/state、record banks、fallback ledgerを無条件削除しない。GC対象と保持期間の詳細はmaintenance実装を正本とする。

## 3. 時刻routing

maintenance runでない場合だけ次を適用する。

- **08:30 JST**: その他更新workerだけを実行する。
- **それ以外の毎時`:30`**: 通常論文workerを実行する。
- **別タスクの毎時`:00`**: 探索専用worker。通常workerのmaintenance counterへ加算しない。

同じ`:30`枠で通常論文workerとその他更新workerを両方実行しない。

## 4. 通常論文worker

通常論文runは [always-on-worker.md](always-on-worker.md) のwork-conservingループに従う。固定research件数、固定audit件数、固定discovery round数、固定総candidate数、固定batch数をrun終了条件にしない。

research / audit / discoveryの完全logical payloadをGitHubへ送信済み、またはChatGPT Libraryへ耐久checkpoint済みなら、Actionsのterminal反映を次の独立作業開始の同期障壁にしない。`next-jobs.json`は優先スナップショットであり全ready一覧ではないため、countsやjob実体にreadyが残る場合は表示枠だけで「仕事なし」と判断しない。

research / auditの品質、5-slot structured record、preflight、paper family routingは `queue-v10.md` とpaper templateを正本とする。

## 5. discovery共有stateの所有権

`.survey/work-queue/discovery-state.json` は **GitHub Actionsを単一writer** とする。通常Scheduled Chat workerも探索専用Scheduled Chat workerもこの共有stateを直接編集しない。

各discovery submissionは観測値をトップレベル `discovery_stats` として渡し、GitHub Actions側が重複抑止後の採用結果と合わせて共有stateへ反映する。Scheduled Chatは探索開始時とcandidate投入直前に最新HEAD / identity / queue / discovery-stateを再取得する。

1探索軸・1 submissionのcandidate上限5本はtransport batch上限であり、run全体の上限ではない。0件、全重複、5件送信、soft target到達だけを終了理由にしない。詳細はdiscovery各正本に従う。

## 6. fallbackとreplay

耐久経路は次の2つだけ。

1. GitHub direct transport
2. ChatGPT Library `/LLM-survey-outbox/pending/`

Library pendingの回復はScheduled ChatがGitHub immutable intake `.survey/work-queue/fallback-inbox/<id>.json` へ送る。固定record bankや`chat-inbox.json`へ直接replayしない。GitHub fallback-inboxから固定transportへの展開は `.survey/scripts/dispatch_fallback_inbox.py` を呼ぶsurvey-helperだけが行う。

同一envelope ID・同一内容は冪等に受領し、同一ID・異内容は衝突として隔離する。research/audit fallbackのimmutable envelopeが作成時のrecord bankを参照していても、dispatcherはreplay時点で安全なbankへ一時再配置してから固定transportへ展開する。immutable ledger自体は書き換えない。

単一write失敗、単一replay失敗、Library pending増加、GitHub fallback-inbox増加、record bank枯渇だけではrun全体を止めない。停止判定は `continuation-policy.json` を正本とする。

## 7. その他更新worker（08:30専用）

対象は次だけ。

1. `framework-updates/**`
2. `llm-releases/**`

論文queueには触れない。固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` を使う。GitHub write不能でも更新payloadをLibraryへ耐久保存できるならScheduled task自体を停止・無効化・再作成しない。復旧はGitHub immutable intakeを経由する。

08:30 runでは [suggestion-box.md](suggestion-box.md) に従い、ChatGPT Library `/LLM-survey-suggestion-box/pending/` を確認する。pendingが0件なら目安箱について通知しない。pendingがある場合は実質重複をまとめ、`improvement` と `continuation_obstacle` を区別して重要度順に報告する。ユーザーの明示採用なしに提案を自動実装しない。報告生成後だけ `reported/` へ移し、移動失敗時はpendingに残す。

## 8. 作業中の改善知見

maintenance runを除くworkerは、実作業中に具体的な摩擦、失敗、重複作業、無駄、復旧コスト、品質低下リスクを観測し、具体的で実行可能な改善案を得た場合だけsuggestion boxへ保存する。提案を作るための追加探索や件数ノルマは設けない。

run終了時、実行可能だったはずの独立作業を何かが妨げた場合は `continuation_obstacle` を検討する。ただしsuggestion-box保存はbest-effortであり、research、queue、fallback checkpoint、GitHub publicationを止めない。

## 9. 通知

予定タスク本文に通知条件が指定されている場合は、その通知条件を優先する。問題報告はrun終了命令ではない。STOP判定が`CONTINUE`なら、必要な通知後も処理可能な独立作業を続ける。

08:30 JSTの通知にはその他更新workerの結果に加え、直近24時間について次を含める。

1. **発見した論文数**: 通常workerと探索専用worker双方のdiscoveryで、重複除外後に新規候補として発見した論文数。
2. **追加した論文数**: 直近24時間に正本repoへ新規収録された論文数。
3. **残っている論文候補数**: 通知時点の未処理research候補数。GitHub readyとfallback由来spilloverを重複排除する。
4. 可能なら **candidate inventory / target inventory(50)**。

run ledger、discovery-state、queue、fallback状態など耐久記録から集計し、集計不能な値を推測しない。
