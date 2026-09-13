# GitHub + ChatGPT Library fallback routing

この文書は、GitHub write障害中でもScheduled Chatの研究を継続し、安全に復旧するための正本である。研究・queue・paperの正本は常にGitHub main。外部fallbackはChatGPT Libraryだけを使う。

Google Drive fallback経路は2026-09-10に現行mainから廃止した。旧Drive実装は `archive/drive-fallback-before-removal-20260910` ブランチに保存している。Notionと旧 `/LLM-survey-fallback/` も新規保存には使わない。

## 1. 基本原則

耐久経路は2つだけ。

1. GitHub direct transport
2. ChatGPT Library outbox `/LLM-survey-outbox/pending/`

GitHub writeが正常なら必ずGitHubを優先する。GitHub writeがrun-wideで利用不能なら、完成logical payloadまたは継続に必要なoffline job seedをLibraryへ保存する。Libraryへの耐久保存が成功すれば、そのjobをGitHub上で完了扱いにせずcheckpoint済みとして後続研究へ進んでよい。

Library pending件数、GitHub fallback-inbox件数、未送信論文数、record bank使用数は研究容量ではなく、run停止理由にしない。

## 2. ChatGPT Library outbox

新規fallback保存先:

`/LLM-survey-outbox/pending/<unique-id>.json`

復旧時、Scheduled Chat workerがGitHub write可能なrunでpending envelopeをGitHub immutable intakeへ送る。GitHub intake成功確認後だけLibrary側を `/LLM-survey-outbox/processed/` へ移す。不正・再生不能payloadは `/LLM-survey-outbox/failed/` へ隔離する。

旧 `/LLM-survey-fallback/` はlegacy領域であり、新規保存には使わない。

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

`id` は `[A-Za-z0-9][A-Za-z0-9._-]{0,159}`。research/auditでは1論文につき1 envelopeに5 record slot + `chat-inbox.json`を完全に含める。完成Markdownはfallbackへ保存しない。fallback専用の短縮形式を作らない。

## 4. GitHub immutable fallback intake

Library pendingは固定record bankや`chat-inbox.json`へ直接replayしない。まず1 envelope = 1 immutable fileとして次へ送る。

- intake: `.survey/work-queue/fallback-inbox/<envelope-id>.json`
- processed ledger: `.survey/work-queue/fallback-archive/<envelope-id>.json`
- invalid/conflict: `.survey/work-queue/fallback-failed/<envelope-id>.json`

同じ`id`がinbox/archiveにあり内容も同一なら再投入せずLibrary copyをprocessedへ移してよい。同じ`id`で内容が異なる場合はID衝突としてfailed扱いにし、上書きしない。

## 5. serialized dispatch

`.github/workflows/survey-helper.yml` と `.survey/scripts/dispatch_fallback_inbox.py` がGitHub fallback-inboxから固定transportへ直列展開する。

1. invalid envelopeはfallback-failedへ隔離し後続を止めない。
2. research/auditの対応GitHub jobが未実体化ならdependency待ちとしてinboxに残す。
3. reusable `chat-inbox.json` がbusyなら待機する。
4. eligible envelopeだけを固定transportへ展開する。
5. GitHub jobがすでにterminalなら再展開せずarchiveへ移す。
6. 成功後に元fallback envelopeをarchiveへ移す。

## 6. GitHub write不能中のoffline job seed

GitHub queueを直接更新できなくてもLibraryへ保存可能なら探索を止めない。候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` として書くenvelopeをLibraryへ保存する。

seed保存後はjob実体化を待たず同じrunで候補を全文精読してよい。完成research envelopeはqueueと同じ決定論的job IDを使う。

candidate keyは `canonical_id`、なければ `source_url`、なければ `title` をtrimして小文字化し、`sha256(candidate_key)`先頭16桁から `job-research-<16hex>` とする。

復旧時、seed envelopeが先にdispatchされると `.survey/scripts/apply_offline_job_seed.py` がjobを実体化する。research envelopeが先にGitHub intakeへ入った場合はjobが存在するまでinboxに残す。

## 7. Backlog indexと実行可能job

Scheduled Chatは可能な範囲で次を読む。

- GitHub queue
- ChatGPT Library `/LLM-survey-outbox/pending/`
- GitHub fallback-inbox
- GitHub fallback-archive

一時的に次を作る。

- `checkpointed_job_ids`: 完全research/audit payloadがLibraryまたはGitHub fallback-inboxへ保存済みのjob
- `spillover_candidates`: offline seedに存在し、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でもcheckpoint済みjobは再精読しない。Actions反映までstatusは未完了のまま維持する。

実行順:

1. actionable GitHub ready
2. Library seed由来spillover candidate
3. 新規discovery

GitHub writeが復旧しているがcheckpoint済みreadyだけがqueueを塞ぐ場合は `.survey/work-queue/transport/request-jobs.json` でcheckpoint済みjobをstatus変更せず一時除外し、新しいdiscovery jobを追加発行してよい。

## 8. Recovery ownership

- Library pending → Scheduled ChatがGitHub immutable intakeへ送る。
- GitHub fallback-inbox → survey-helper dispatcherだけが固定transportへ展開する。
- GitHub fallback-archive → global dedupe ledger。再writeしない。

Library `processed`は「GitHub immutable intakeへの受領確認済み」を意味し、paper publication完了を意味しない。publication完了はActions result + latest queueで判定する。

## 9. 停止条件

停止条件は `continuation-policy.json` が唯一の正本。

少なくとも次の場合だけrun停止を検討する。

- GitHub read不能でrepo/identity/queueを安全に確認できない。
- 完成成果または継続に必要なoffline seedをGitHubにもLibraryにも耐久保存できない。
- プラットフォーム上限に達した。
- GitHub ready、fallback spillover、新規offline discoveryを考慮しても独立して安全に進められる作業が残らない。

Library pending数、GitHub fallback-inbox件数、未送信論文数、bank exhaustion、単一payload障害はSTOP_RUN条件ではない。

Claimed-worker envelopes carry job, claim, worker, and attempt identity. The
dispatcher compares these values with the current repository claim before any
record-bank or reusable Chat write. A missing or superseded claim is quarantined
with an error sidecar; an expired but still-current claim is accepted. Legacy
envelopes without `origin: claimed_worker` retain the existing routing behavior.
There is no terminal wait barrier: a completion for an already-terminal job is
acknowledged into the archive without changing its paper or transport.
