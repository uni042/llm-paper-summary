# Multi-outbox fallback routing

この文書は、GitHub write障害中でもScheduled Chatの論文研究を継続し、複数の一時配送先から安全に復旧するための正本である。研究・queue・paperの正本は常にGitHub mainであり、Google DriveとChatGPT Libraryは配送待ちoutboxとしてだけ使う。

## 1. 基本原則

GitHub直接transport、Google Drive outbox、ChatGPT Library outboxを独立した耐久経路として扱う。

- GitHub writeが正常なら通常transportを優先する。
- GitHub writeがrun-wideで利用不能なら、そのrunでは同じ失敗を各jobごとに繰り返さない。
- fallback保存はDriveを先に試し、Drive経路が利用不能ならLibraryへ切り替える。payload固有のDrive保存失敗でもLibraryへ切り替えてよい。
- 少なくとも1つの耐久保存先へ完全payloadまたは継続に必要なoffline job seedを保存できればrunを継続する。
- Drive pending件数、Library pending件数、未送信論文数、record bank使用数は研究容量ではなく、停止理由にしない。
- Notionは使用しない。

同じlogical payloadが操作結果不明などで複数outboxに存在する可能性は許容する。その場合も同じ `id` を維持し、GitHub側の不変fallback intakeで内容一致を確認して冪等に重複排除する。

## 2. Outbox

### Google Drive

`/Google Drive/llm-paper-summary-outbox/pending/<unique-id>.json`

Driveは `.github/workflows/drive-outbox-import.yml` が回収する。`GOOGLE_SERVICE_ACCOUNT_JSON` が未設定・一時失効していてもpending保存自体は有効な耐久checkpointであり、研究を止めない。

### ChatGPT Library

`/LLM-survey-outbox/pending/<unique-id>.json`

LibraryはScheduled Chat workerが回収する。GitHub writeが利用可能なrunでpendingをGitHubの不変fallback intakeへ送る。GitHub intake成功確認後だけ `/LLM-survey-outbox/processed/` へ移す。不正・再生不能payloadは `/LLM-survey-outbox/failed/` へ隔離する。

旧 `/LLM-survey-fallback/` はlegacy領域であり、新規保存先には使わない。残存pendingは一度だけ新envelopeへ変換・移行し、その後は新outboxだけを使う。

## 3. 共通envelope

DriveとLibraryは同じ `schema_version: 1` envelopeを使う。

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

`id` は `[A-Za-z0-9][A-Za-z0-9._-]{0,159}`。同一logical payloadを複数経路へ再保存するときは同じ`id`を使う。

research/auditでは1論文につき1 envelopeに5 record slot + `chat-inbox.json`を完全に含める。完成Markdownはfallbackへ保存しない。slot内容は通常のworkflow v10 transportと同じであり、fallback専用の短縮形式を作らない。

## 4. GitHub immutable fallback intake

DriveとLibraryは復旧時にrecord bankや`chat-inbox.json`へ直接再投入しない。まず次へ1 envelope = 1 immutable fileとして送る。

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

処理済みの同じenvelopeは:

`.survey/work-queue/fallback-archive/<envelope-id>.json`

不正payloadは:

`.survey/work-queue/fallback-failed/<envelope-id>.json`

に置く。

この層がDriveとLibraryの共通重複排除台帳になる。

- 同じ`id`がinbox/archiveにあり内容も同一なら、新しいsource copyは再投入せずacknowledgeしてよい。
- 同じ`id`で内容が異なる場合はID衝突としてfailed扱いにし、上書きしない。
- Drive importerは `.survey/scripts/import_drive_outbox_v4.py` でこのintakeだけを行う。
- Library replayも同じ規則で`fallback-inbox/<id>.json`を作る。固定bankへ直接writeしない。

## 5. serialized dispatch

`.github/workflows/survey-helper.yml` はDrive/Libraryのintakeを含め同じ `survey-helper-main` concurrency groupの中で処理する。

`.survey/scripts/dispatch_fallback_inbox.py` が1 runにつき最大1件のeligible envelopeだけを展開する。

1. invalid envelopeは`fallback-failed`へ隔離し、後続を止めない。
2. research/auditの対応GitHub jobがまだ存在しなければdependency待ちとしてinboxに残す。
3. reusable `chat-inbox.json` がbusyならresearch/auditは待たせる。
4. 待機中researchの後ろにoffline seed、transport request、framework/model updateなど独立payloadがあれば先に処理してよい。
5. eligible envelopeだけを固定transportへ展開し、同じActions runで通常のvalidator/renderer/queue workerへ渡す。
6. GitHub jobがすでにterminalなら再展開せずarchiveへ移す。
7. 成功後に元fallback envelopeをarchiveへ移す。

DriveとLibraryが同時に復旧しても、両者は不変intake fileを追加するだけで固定bankを直接競合しない。実際のbank/inbox展開は1本の直列dispatcherだけが行う。

## 6. GitHub write不能中のoffline job seed

GitHub queueを直接更新できないときでも、DriveまたはLibraryへ保存可能なら探索を止めない。候補0〜5件を固定transport `.survey/work-queue/transport/offline-job-seed.json` として書くenvelopeをfallbackへ保存する。

seed本体:

```json
{
  "schema_version": 1,
  "transport_version": 10,
  "seed_id": "seed-unique",
  "candidates": [
    {
      "canonical_id": "arXiv:2609.12345",
      "title": "...",
      "source_url": "https://...",
      "priority": 80,
      "reason": "..."
    }
  ]
}
```

候補の将来research `job_id` はqueueと同じ決定論的規則で計算する。candidate keyは `canonical_id`、なければ `source_url`、なければ `title` をtrimして小文字化し、`sha256(candidate_key)`先頭16桁から `job-research-<16hex>` とする。

seedを耐久保存した後はjob実体化を待たず同じrunで候補を全文精読してよい。完成research envelopeは決定論的job IDを使う。

復旧時はseed envelopeがGitHub intakeから先にdispatchされると `.survey/scripts/apply_offline_job_seed.py` が同じjob IDを実体化する。research envelopeはjobが存在するまでintakeに残るため、seedとresearchが別outboxに分散しても失われない。

## 7. Backlog indexと実行可能job

Scheduled Chatは可能な範囲でGitHub queue、Drive pending、Library pending、新しいGitHub fallback-inboxを読み、一時的なbacklog indexを作る。

- `checkpointed_job_ids`: 完全research/audit payloadがいずれかのoutboxまたはGitHub fallback-inboxへ保存済みのjob
- `spillover_candidates`: offline seedに存在し、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でも`checkpointed_job_ids`にあるjobは再精読しない。statusは最終Actions反映まで未完了のまま維持する。

実行順:

1. GitHub readyからcheckpoint済みを除いたactionable readyをpriority順に処理する。
2. fallback seed由来の未処理spillover candidateをpriority順に処理する。
3. どちらも無ければ新規discoveryを行う。
4. GitHub write可能なら通常job発行、write不能ならoffline seedを生きているfallbackへ保存する。
5. 完成・blocked・checkpoint後は状態を再取得して繰り返す。

GitHub writeが復旧しているがcheckpoint済みreadyだけがqueueを塞いでいる場合は `.survey/work-queue/transport/request-jobs.json` でcheckpoint済みjobをstatus変更せず一時除外し、新しいdiscovery jobを追加発行してよい。

## 8. Recovery ownership

- Drive pending → Drive importerがGitHub immutable intakeへ送る。
- Library pending → Scheduled ChatがGitHub immutable intakeへ送る。
- GitHub fallback-inbox → survey-helper dispatcherだけが固定transportへ展開する。
- GitHub fallback-archive → global dedupe ledger。再writeしない。

各source outboxの`processed`は「GitHub immutable intakeへの受領が確認済み」を意味し、必ずしもpaper publication完了を意味しない。publication完了はActions result + latest queueで判定する。

## 9. 停止条件

fallback障害は経路単位で扱う。Driveが壊れていてもLibraryへ保存できれば継続し、Libraryが壊れていてもDriveへ保存できれば継続する。

run停止条件は `continuation-policy.json` が唯一の正本である。少なくとも以下を守る。

- GitHub read不能でrepo/identity/queueを安全に確認できない。
- 完成成果または継続に必要なoffline seedをGitHub・Drive・Libraryのいずれにも耐久保存できない。
- プラットフォーム上限に達した。
- fallback spilloverを含めても独立して安全に進められる研究作業が残っていない。

Drive pending数、Library pending数、GitHub fallback-inbox件数、未送信論文数、bank exhaustion、単一経路の障害はSTOP_RUN条件ではない。
