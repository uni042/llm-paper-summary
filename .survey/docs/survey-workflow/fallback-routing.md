# GitHub + ChatGPT Library fallback routing

この文書は、GitHub write障害中でもScheduled Chatの研究を継続し、安全に復旧するためのfallback / replay正本である。研究・queue・paperの正本は常にGitHub main。外部fallbackはChatGPT Libraryだけを使う。

Google Drive fallbackは2026-09-10に廃止した。Notionと旧 `/LLM-survey-fallback/` も新規保存・replay・backlog判定に使わない。旧Drive実装は `archive/drive-fallback-before-removal-20260910` ブランチにだけ保存する。

## 1. 基本原則

耐久経路は2つだけ。

1. GitHub direct transport
2. ChatGPT Library outbox `/LLM-survey-outbox/pending/`

GitHub writeが正常ならGitHubを優先する。GitHub writeがrun-wideで利用不能なら、完成logical payloadまたは継続に必要なoffline job seedをLibraryへ保存する。Libraryへの耐久保存が成功すれば、そのjobをGitHub上で完了扱いにせずcheckpoint済みとして後続研究へ進んでよい。

Library pending件数、GitHub fallback-inbox件数、未送信論文数、record bank使用数は研究容量ではなく、run停止理由にしない。

## 2. ChatGPT Library outbox

新規fallback保存先:

`/LLM-survey-outbox/pending/<unique-id>.json`

復旧時、Scheduled Chat workerがGitHub write可能なrunでpending envelopeをGitHub immutable intakeへ送る。GitHub intake成功確認後だけLibrary側を `/LLM-survey-outbox/processed/` へ移す。不正・再生不能payloadは `/LLM-survey-outbox/failed/` へ隔離する。

## 3. 共通envelope

Library fallbackは `schema_version: 1` の完全envelopeを使う。

```json
{
  "schema_version": 1,
  "id": "20260910T130000JST-research-2609.12345-attempt-x",
  "kind": "research",
  "job_id": "job-research-...",
  "attempt_id": "attempt-x",
  "depends_on_job_ids": ["job-research-..."],
  "writes": [
    {"path": ".survey/work-queue/records/chat-record/metadata.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/submissions/chat-inbox.json", "content": "{...}\n"}
  ]
}
```

上の `chat-record` は **bank Aの例** にすぎない。research/auditでは1論文につき1 envelopeに同一bankの5 record slot + `chat-inbox.json`を完全に含める。完成Markdownはfallbackへ保存せず、fallback専用の短縮形式も作らない。

重要: immutable envelopeに含まれるbank pathは **作成時のstaging参照** であり、将来のreplay時にそのbankを予約するものではない。replay時はdispatcherが現在のbank状態を再評価し、安全なbankへ一時remapしてから固定transportへ展開する。GitHub immutable ledgerの原envelope自体は書き換えない。

`id` は `[A-Za-z0-9][A-Za-z0-9._-]{0,159}` に従う。

## 4. GitHub immutable fallback intake

Library pendingは固定record bankや`chat-inbox.json`へ直接replayしない。まず1 envelope = 1 immutable fileとして次へ送る。

- intake: `.survey/work-queue/fallback-inbox/<envelope-id>.json`
- processed ledger: `.survey/work-queue/fallback-archive/<envelope-id>.json`
- invalid/conflict: `.survey/work-queue/fallback-failed/<envelope-id>.json`

同じ`id`がinbox/archiveにあり内容も同一なら再投入せずLibrary copyをprocessedへ移してよい。同じ`id`で内容が異なる場合はID衝突としてfailed扱いにし、上書きしない。

## 5. Serialized dispatchとrecord bank安全性

`.github/workflows/survey-helper.yml` と `.survey/scripts/dispatch_fallback_inbox.py` がGitHub fallback-inboxから固定transportへ直列展開する。

1. invalid envelopeはfallback-failedへ隔離し、後続を止めない。
2. research/auditの対応GitHub jobが未実体化ならdependency待ちとしてinboxに残す。
3. reusable `chat-inbox.json` がbusyなら待機する。
4. research/audit envelopeは `.survey/scripts/fallback_transport.py` で安全なrecord bankを選ぶ。
5. envelope作成時のbankが現在別の未完了jobに使用中なら、そのbankを上書きせずfree/reusableな別bankへ一時remapする。
6. 安全なbankがまだない場合はinvalid扱いにせずdependency/deferredとしてinboxに残す。
7. eligible envelopeだけを固定transportへ展開する。
8. GitHub jobがすでにterminalなら再展開せずarchiveへ移す。
9. 成功後に元fallback envelopeをarchiveへ移す。

bank選択は `.survey/work-queue/next-jobs.json` の表示枠だけで判断しない。`.survey/scripts/select_record_bank.py` はcanonical `.survey/work-queue/jobs/*.json` の全ready jobを確認し、表示外readyが保持するbankもoccupiedとして扱う。

## 6. GitHub write不能中のoffline job seed

GitHub queueを直接更新できなくてもLibraryへ保存可能なら探索を止めない。1 discovery submissionあたり候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` として書くenvelopeをLibraryへ保存する。5件はbatch上限だけで、run全体の探索上限ではない。

seed保存後、通常論文workerはjob実体化を待たず同じrunで候補を全文精読してよい。完成research envelopeはqueueと同じ決定論的job IDを使う。探索専用workerはresearchへ進まない。

candidate keyは `canonical_id`、なければ `source_url`、なければ `title` をtrimして小文字化し、`sha256(candidate_key)`先頭16桁から `job-research-<16hex>` とする。

復旧時、seed envelopeが先にdispatchされると `.survey/scripts/apply_offline_job_seed.py` がjobを実体化する。research envelopeが先にGitHub intakeへ入った場合はjobが存在するまでinboxに残す。

## 7. Backlog indexと実行可能job

Scheduled Chatは可能な範囲で次を読む。

- GitHub queue / canonical job files
- ChatGPT Library `/LLM-survey-outbox/pending/`
- GitHub fallback-inbox
- GitHub fallback-archive

一時的に次を作る。

- `checkpointed_job_ids`: 完全research/audit payloadがLibraryまたはGitHub fallback ledgerへ保存済みのjob
- `spillover_candidates`: offline seedに存在し、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でもcheckpoint済みjobは再精読しない。Actions反映までstatusは未完了のまま維持する。

実行順はcandidate水位と通常run正本を優先しつつ、基本的にはactionable GitHub ready、spillover candidate、新規discoveryを組み合わせる。checkpoint済みreadyだけがqueueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` でstatusを変えずdiscovery補充を要求してよい。

## 8. Recovery ownership

- Library pending → Scheduled ChatがGitHub immutable intakeへ送る。
- GitHub fallback-inbox → survey-helper dispatcherだけが固定transportへ展開する。
- GitHub fallback-archive → global dedupe ledger。再writeしない。

Library `processed`は「GitHub immutable intakeへの受領確認済み」を意味し、paper publication完了を意味しない。publication完了はActions result + latest queueで判定する。

## 9. 停止条件

停止条件は `continuation-policy.json` が唯一の正本。

少なくとも次の単独事象はSTOP_RUN条件ではない。

- Library pending増加
- GitHub fallback-inbox増加
- 未送信論文増加
- record bank exhaustion
- 単一payload障害
- dependency待ち1件
- replay時に安全なbankがまだ空いていないこと

GitHub read不能、完成成果または必要なoffline seedをGitHub/Libraryどちらにも耐久保存不能、hard platform limit、または正本どおり独立作業を合理的に生成できない場合だけrun停止を検討する。
