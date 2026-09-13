# Serial claim policy

本書はScheduled Chat / Work系のresearch・audit workerがjobをclaimする際の **同時保有数と次job取得タイミング** の正本とする。

## 1. 1 worker = 未完了claim 1件

research / audit workerは、**未完了のassigned jobを同時に1件だけ保持する**。

- claim requestは常に1 jobだけ要求する。`max_jobs`は省略して既定値1を使うか、明示する場合も`1`だけとする。
- 1回のrequestで複数jobを要求しない。
- 現在のassigned jobがまだ精読中・record作成中・preflight中・耐久保存前である間は、次jobを先取りclaimしない。
- claim result待ちのrequestが1件ある間に、別requestを追加発行してclaimを積み増さない。
- throughput確保のために複数jobを先にclaimして在庫化することは禁止する。

この制約はworker単位で適用する。別worker同士がそれぞれ1件ずつ並列処理することは許可する。

## 2. 完了後は直ちに次の1件を取得する

現在jobについて、完全logical payloadが次のいずれかを満たした時点で、そのjobはworker内では処理済みとみなす。

1. GitHubへ5 slotを書き終え、attempt固有immutable descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ耐久保存済み。
2. GitHub write不能時にChatGPT Library `/LLM-survey-outbox/pending/` へ完全payloadを耐久checkpoint済み。

この時点で **submission-fast / background Actionsのterminal反映を待たず**、run内処理済みjobとして記録し、直ちに最新HEAD / queue / claim stateを再取得して、priority最上位の次jobを1件だけ新しいclaim requestで取得する。

通常ループ:

`1件claim → 全文精読 → 5-slot record作成 → preflight → immutable descriptor送信/Library checkpoint → 最新queue再取得 → 次の1件claim`

1件完了したこと自体はrun終了理由ではない。`always-on-worker.md` と `continuation-policy.json` がCONTINUEを示す限り、この直列ループを繰り返す。

## 3. Actions待ちとclaim待ち

- immutable descriptor送信またはLibrary checkpoint後は、前jobのActions terminal反映を同期障壁にしない。
- 次job用claim requestは前jobの耐久保存直後に発行する。
- claim request発行後は、そのrequestのresultが確定する前にさらに別のclaim requestを重ねない。
- claim resultが0 assignmentの場合は、最新queue / claim state / Actions反映を再確認する。actionable researchが残っているなら、同じ空resultを仕事枯渇とみなさず、新しいrequest_idで次の1件取得を再試行する。
- ただし未完了assigned jobを残したまま再試行して別jobを積み増してはならない。
- 未解決immutable descriptorが参照しているrecord bankは上書きしない。別bankが空いていなければLibrary checkpointへ切り替え、bank枯渇をrun停止理由にしない。

## 4. Lease

lease運用は`always-on-worker.md` / `queue-v10.md`を優先する。

- 通常は`lease_seconds`を省略し、既定90分（5400秒）を使う。
- Scheduled Chatのclaim fast laneでは5400秒を上限として強制する。5400秒を超える新規requestはassignmentせずerror resultにする。Work系workerの明示的な長いleaseはこのScheduled Chat上限の対象外とする。
- 90分を超える可能性がある場合は、同じ`request_id` / `worker_id` / `worker_kind`で新しいUTC `requested_at`を使ったheartbeat更新だけを行う。
- heartbeatは新規job取得ではない。同じjobのlease延長として扱う。Scheduled Chatのheartbeatも1回ごとの新しい期限は最新activityから最大90分とする。
- 旧実装で作成済みのScheduled Chat長時間leaseは、claim fast laneが次に動いた時点で`heartbeat_at`、なければ`claimed_at`を基準に90分へ正規化する。正規化後の期限を既に超えているclaimはinvalidatedとして直ちにactive集合から外す。
- invalidatedまたは通常の期限切れclaimに紐づく古いattemptからの新規immutable submissionは拒否する。一方、期限内にimmutable descriptorを耐久保存した結果としてclaim fast laneがその同一attemptをreleaseした場合は、submission-fastがそのdescriptorを引き続き処理してよい。
- expired claimファイルは履歴として残るがactiveではなく、他workerの新規claimを阻害しない。
- lease期限切れ時点でまだ完全payloadを耐久保存していないworkerは、旧claimで新規送信せずfresh claimを取得し直す。

## 5. 禁止例

以下は行わない。

- `max_jobs: 3` などで複数jobを一括取得する。
- 1件目の精読途中に2件目、3件目のclaim requestを発行する。
- claim result待ち中に別requestを何本も作る。
- 「後で読むため」にpriority上位jobをまとめて確保する。
- 前jobの完全payloadが未保存なのに次jobへ移る。
- 新規通常Research/Auditで固定`chat-inbox.json`を上書きする。

狙いは **claimの抱え込みを防ぎつつ、1件終わるたびに次jobへ即時移行してworkerを遊ばせないこと** である。