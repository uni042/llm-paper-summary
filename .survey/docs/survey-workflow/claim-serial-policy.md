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

Libraryに完全payloadを耐久checkpoint済みのjobがある場合、以後のclaim requestにはそのjobを次の形で `checkpointed_jobs` に含める。

```json
"checkpointed_jobs": [
  {
    "job_id": "job-research-...",
    "checkpoint_ref": "/LLM-survey-outbox/pending/<envelope>.json"
  }
]
```

- `checkpoint_ref`は実在をworkerが確認した完全payloadのLibrary pathだけを使う。
- `checkpointed_jobs`はworker-localなclaim除外情報であり、job本体を`completed`へ変更しない。
- 同workerがそのjobのactive claimをすでに持っている場合、claim-fastはそのclaimだけを解放し、jobは`ready`のまま残す。その後、同じrequest処理内で次のeligible jobを取得できる。
- 他workerのactive claimは解放しない。
- Library replayが完了してGitHub側のimmutable resultへ収束するまでは、checkpoint申告だけをrepository-wide completionの根拠にしない。
- Library pendingを確認できるrunでは、既知の完全checkpointをclaim requestから省略して同じjobを再精読しない。

通常ループ:

`1件claim → 全文精読 → 5-slot record作成 → preflight → immutable descriptor送信/Library checkpoint → 最新queue再取得 → 次の1件claim`

1件完了したこと自体はrun終了理由ではない。`always-on-worker.md` と `continuation-policy.json` がCONTINUEを示す限り、この直列ループを繰り返す。

## 3. Claim resultのrecord bank割当

Research / Auditのclaim resultに `record_bank` が入っている場合、その値を **そのattemptの予約済みbankとして正本扱いする**。

- `record_bank: "a"` など非null値が返ったら、そのbankだけへ5 slotを書く。別bankを`select_record_bank.py`で選び直してはならない。
- claim高速経路はclaim割当と同じ直列化区間でbankを予約し、claim/resultの両方に同じ`record_bank`を保存する。並列workerが同じbankを独立選択する旧方式は使わない。
- `record_bank: null` かつ `record_bank_fallback: "library"` の場合は、GitHub上の別bankを独自に探さず、完全logical payloadをChatGPT Libraryへcheckpointする。
- 移行前のactive claimなど、claim resultにbank情報が無い場合だけlegacy互換として`select_record_bank.py`を利用できる。その場合もoccupied/dirty bankは使わない。
- claimに記録されたbankとimmutable descriptorの`record_bank`は一致させる。
- attemptが未解決の間、その予約bankは他workerが再利用してはならない。

移行期間中にbank未記録の旧active claimが残っている場合、新規claimは安全のためLibrary fallbackへ回ることがある。これは旧workerが既にbankを選択済みである可能性との競合を避けるためであり、run停止理由ではない。

## 4. Actions待ちとclaim待ち

- immutable descriptor送信またはLibrary checkpoint後は、前jobのActions terminal反映を同期障壁にしない。
- 次job用claim requestは前jobの耐久保存直後に発行する。
- claim request発行後は、そのrequestのresultが確定する前にさらに別のclaim requestを重ねない。
- claim resultが0 assignmentの場合は、最新queue / claim state / Actions反映を再確認する。actionable researchが残っているなら、同じ空resultを仕事枯渇とみなさず、新しいrequest_idで次の1件取得を再試行する。
- ただし未完了assigned jobを残したまま再試行して別jobを積み増してはならない。
- Libraryへ完全checkpoint済みのjobが原因でactive claimが残っている場合は、次requestの`checkpointed_jobs`へそのjobと実在する`checkpoint_ref`を含めてclaimを解放する。lease expiry待ちをrun停止理由にしない。
- 未解決immutable descriptorが参照しているrecord bankは上書きしない。別bankが空いていなければLibrary checkpointへ切り替え、bank枯渇をrun停止理由にしない。

## 5. Lease

lease運用は`always-on-worker.md` / `queue-v10.md`を優先する。

- 通常は`lease_seconds`を省略し、既定90分（5400秒）を使う。
- 90分を超える可能性がある場合は、同じ`request_id` / `worker_id` / `worker_kind`で新しいUTC `requested_at`を使ったheartbeat更新だけを行う。
- heartbeatは新規job取得ではない。同じjobのlease延長として扱う。
- expired claimファイルは履歴として残るがactiveではなく、他workerの新規claimを阻害しない。
- lease期限切れ時点でまだ完全payloadを耐久保存していないworkerは、旧claimで新規送信せずfresh claimを取得し直す。

## 6. 禁止例

以下は行わない。

- `max_jobs: 3` などで複数jobを一括取得する。
- 1件目の精読途中に2件目、3件目のclaim requestを発行する。
- claim result待ち中に別requestを何本も作る。
- 「後で読むため」にpriority上位jobをまとめて確保する。
- 前jobの完全payloadが未保存なのに次jobへ移る。
- 実在する完全Library checkpointを確認せず`checkpointed_jobs`へjobを追加する。
- `checkpointed_jobs`をjobのrepository-wide completion代わりに使う。
- claim resultで予約されたbankとは別のbankへ書く。
- `record_bank_fallback: "library"` を無視して独自にbankを確保する。
- 新規通常Research/Auditで固定`chat-inbox.json`を上書きする。

狙いは **claimの抱え込み・Library checkpointによる直列停止・record bankの並列競合を防ぎつつ、1件終わるたびに次jobへ即時移行してworkerを遊ばせないこと** である。
