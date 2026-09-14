# GitHub + ChatGPT Library fallback routing

この文書は、GitHub write障害中でもScheduled Chat / Work workerの研究を継続し、安全に復旧するための正本である。研究・queue・paperの正本は常にGitHub `main`。外部fallbackはChatGPT Libraryだけを使う。

Google Drive fallbackは2026-09-10に廃止済み。旧Drive実装は `archive/drive-fallback-before-removal-20260910` ブランチに保存している。Notionと旧 `/LLM-survey-fallback/` も新規保存には使わない。

Library上のcheckpoint lifecycle、再精読barrier、`processed/` の意味は `library-checkpoint-registry.md` を正本とする。本書と表現が衝突する場合は同文書を優先する。

## 1. 基本原則

耐久経路は2つだけ。

1. GitHub direct transport
2. ChatGPT Library outbox `/LLM-survey-outbox/pending/`

GitHub writeが正常ならGitHubを優先する。GitHub writeがrun-wideで利用不能なら、完成logical payloadまたは継続に必要なoffline job seedをLibraryへ保存する。Research/Auditでは完全payload保存後に `/LLM-survey-outbox/checkpoints/<job-id>.json` markerを作成し、Library markerまたはGitHub claimの`checkpoint_ref`のどちらかが精読済みを示すjobを再精読しない。Libraryへの耐久保存が成功すれば、そのjobをGitHub上で完了扱いにはせず、checkpoint済みとして後続の独立作業へ進んでよい。

Library pending件数、GitHub fallback-inbox件数、未送信論文数、record bank使用数は研究容量ではなく、run停止理由にしない。

## 2. ChatGPT Library outbox

新規fallback payload保存先:

`/LLM-survey-outbox/pending/<unique-id>.json`

Research/Auditの精読済みregistry:

`/LLM-survey-outbox/checkpoints/<job-id>.json`

GitHub writeが復旧したrunで、workerはcheckpoint registryを先に読み、pending envelopeをGitHubの不変intakeへ送る。同一payloadがGitHub intake/archiveに耐久保存されたことを確認したらmarkerを`transported`へ更新するが、**この時点ではLibrary payloadを`processed/`へ移さない。** canonical jobのterminal化、対応immutable result成功、Researchならpaper artifact整合まで確認してmarkerを`reflected`へ更新した後だけ `/LLM-survey-outbox/processed/` へ移す。不正・再生不能payloadは `/LLM-survey-outbox/failed/` へ隔離する。

旧 `/LLM-survey-fallback/` はlegacy領域であり、新規保存には使わない。

## 3. Current Research/Audit fallback envelope

新規Research/Audit fallbackは `schema_version: 1` の1論文1envelopeとし、**固定 `chat-inbox.json` を含めない。** 完成Markdownも保存しない。

例:

```json
{
  "schema_version": 1,
  "id": "20260914T010000JST-research-2609.12345-attempt-x",
  "origin": "claimed_worker",
  "kind": "research",
  "job_id": "job-research-...",
  "claim_id": "claim-...",
  "worker_id": "scheduled-chat-...",
  "worker_kind": "scheduled_chat",
  "attempt_id": "attempt-x",
  "depends_on_job_ids": ["job-research-..."],
  "paper_path": "papers/inference/.../paper.md",
  "writes": [
    {"path": ".survey/work-queue/records/chat-record-a/metadata.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/records/chat-record-a/problem_method.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/records/chat-record-a/evaluation.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/records/chat-record-a/results.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/records/chat-record-a/positioning.json", "content": "{...}\n"}
  ]
}
```

`id`、job/claim/worker/attempt identityは安全な識別子を使う。5 slotは同じ`job_id` / `attempt_id`を持ち、`transport_version: 10`であること。1論文を複数fragmentへ分割しない。

GitHub direct書込み時にclaim resultがbankを予約していたとしても、Library fallback envelope内のbank pathは永続的な所有権を意味しない。復旧時には最新のbank状態を再評価し、安全なbankへ再配置してよい。

Library fallbackを確定する順序は、完全payload保存 → payload再読によるidentity確認 → job単位checkpoint marker作成/更新 → claim解放、とする。marker作成前にclaimを解放しない。

## 4. GitHub immutable fallback intake

Library pendingをrecord bankへ直接replayしない。まず1 envelope = 1 immutable fileとして次へ送る。

- intake: `.survey/work-queue/fallback-inbox/<envelope-id>.json`
- processed ledger: `.survey/work-queue/fallback-archive/<envelope-id>.json`
- invalid/conflict: `.survey/work-queue/fallback-failed/<envelope-id>.json`

同じ`id`がinbox/archiveにあり内容も同一なら再投入しない。同じ`id`で内容が異なる場合は衝突としてfailed扱いにし、上書きしない。

GitHub intake/archiveへの同一payload保存確認はLibrary markerを`transported`に進める条件であり、Library payload自体を`processed/`へ移す条件ではない。

## 5. Research/Audit replay

`.survey/scripts/dispatch_fallback_inbox.py` はrecord bundleを検出すると `.survey/scripts/replay_record_fallback.py` へ渡す。

Research/Audit replayは次の順で行う。

1. envelopeと5 slotのschema / identity / dependencies / paper pathを検証する。
2. `origin: claimed_worker` なら現在のcanonical claimとidentityを照合する。通常は`claim_id`、`worker_id`、`attempt_id`の完全一致を要求する。ただし旧不具合により後続の重複claimが作られ、その**解放済みcurrent claim自身が `checkpoint_ref=/LLM-survey-outbox/pending/<このenvelope-id>.json` を正確に保持している場合に限り**、current claimが元Library checkpointを明示的にadoptしたものとして元attemptのreplayを許可する。単なるsuperseded attemptは引き続き拒否する。
3. jobがterminalならpaperやbankへ再適用せずacknowledgeしてarchiveする。
4. 同attemptの既存bank、またはfree/reusable bankから安全なbankを選ぶ。安全なbankがなければinboxに残してdeferredとする。
5. 5 slotを選択bankへmaterializeする。
6. 各slot内容からGit blob SHAを計算し、attempt固有descriptorを生成する。
   - Research: `.survey/work-queue/submissions/research/<attempt-id>.json`
   - Audit: `.survey/work-queue/submissions/audit/<attempt-id>.json`
7. 元envelopeをfallback-archiveへ移す。
8. `survey-submission-fast` が通常の不変提出（immutable submission）として処理する。

**replay中に `.survey/work-queue/submissions/chat-inbox.json` を生成・更新してはならない。**

## 6. Legacy read compatibility

2026-09-14以前にLibraryへ保存済みのResearch/Audit envelopeには、5 slotに加えて固定 `.survey/work-queue/submissions/chat-inbox.json` を含むものがある。これらは既存pending成果を失わないための**読込互換**として受理する。

- legacy `chat-inbox.json` は不足する`paper_path`、claim identity等を復元する入力としてだけ読む。
- envelope rootとlegacy chat payloadの値が両方存在して食い違う場合は隔離する。
- legacy chat payload自体をGitHubの固定transportへ書き戻さない。
- 最終的には現行の5 slot + attempt固有immutable descriptorへ変換して収束させる。

新しいworkerはlegacy `chat-inbox.json` 形式を生成してはならない。

## 7. Non-record fallback

Research/Audit record bundle以外のfallbackはserialized background dispatcherで処理する。対象には次が含まれる。

- offline discovery seed
- checkpoint-aware job request
- framework / LLM update worker input
- その他allowlistされた軽量JSON transport

これらはResearch/Auditのimmutable descriptor変換とは別系統であり、固定Chat research transportを復活させる理由にはならない。

## 8. Offline discovery

GitHub queueを直接更新できなくてもLibraryが書けるなら探索を止めない。候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` として書くenvelopeをLibraryへ保存する。

candidate keyは `canonical_id`、なければ `source_url`、なければ `title` をtrimして小文字化し、`sha256(candidate_key)`先頭16桁から `job-research-<16hex>` とする。

seed保存後はjob実体化を同期的に待たず同じrunで候補を全文精読し、完成Research fallbackもLibraryへ保存してよい。復旧時にcanonical jobがまだ存在しないResearch envelopeはdependency待ちとしてinboxに残す。

## 9. Backlog indexと実行可能job

Scheduled Chat / Work workerは可能な範囲で次を読む。

- GitHub queue
- ChatGPT Library `/LLM-survey-outbox/checkpoints/`
- ChatGPT Library `/LLM-survey-outbox/pending/`
- GitHub fallback-inbox
- GitHub fallback-archive

一時的に次を構築する。

- `checkpointed_job_ids`: Library markerが`checkpointed`/`transported`、GitHub claimが有効な`checkpoint_ref`を持つ、またはGitHub fallbackへ完全Research/Audit payloadが耐久保存済みのjob
- `spillover_candidates`: offline seedに存在し、まだ完成payloadがcheckpointされていない候補

GitHub上で`ready`でもcheckpoint済みjobは再精読しない。Actions反映までcanonical statusは未完了のまま維持する。claim requestへはLibrary registry由来の`checkpointed_jobs`を渡し、GitHub側の`.survey/scripts/apply_library_checkpoint_barriers.py`もpersisted claimの`checkpoint_ref`を未処理requestへマージして二重に保護する。

実行順は `always-on-worker.md` と `continuation-policy.json` を優先する。

## 10. Recovery ownership

- Library checkpoint registry / pending → Scheduled Chat / Work workerが新規claimより先に確認し、GitHub fallback-inboxへ送る。
- GitHub fallback-inbox内のResearch/Audit → `dispatch_fallback_inbox.py` + `replay_record_fallback.py` がimmutable descriptorへ変換する。
- GitHub fallback-inbox内の非record envelope → background dispatcherがallowlistされたtransportへ展開する。
- GitHub fallback-archive → global dedupe ledger。再writeしない。

Library `processed/` は **GitHub publicationまで確認済みのpayload** を意味する。GitHub intake受領だけでは`processed/`へ移さない。Research/Auditのpublication完了はcanonical terminal job + immutable result成功 + Research paper artifact整合で判定する。

旧運用で`processed/`へ移動済みなのにcanonical jobがnonterminalのpayloadは反映済みとみなさない。対応payloadとjob/claim/attemptを照合してcheckpoint markerを再構築し、必要ならpendingへ戻してreplayする。再精読はしない。

## 11. Claim fencing

Claimed-worker envelopeはjob、claim、worker、attempt identityを持つ。replay前に現在のrepository claimと照合する。

- missing/superseded claimは原則隔離する。
- 例外は、解放済みcurrent claim自身が元envelopeへの完全一致`checkpoint_ref`を保持し、そのLibrary payloadを明示的にadoptしている場合だけ。
- terminal jobは再適用せずarchiveする。
- replay可能なcurrent/adopted attemptだけをslot + descriptorへ変換する。
- stale payloadが別workerのbankやpaperを上書きしてはならない。

claim詳細は `claim-serial-policy.md`、Library checkpoint詳細は `library-checkpoint-registry.md` を正本とする。

## 12. 停止条件

停止条件は `continuation-policy.json` が唯一の正本。

少なくとも次の場合だけrun停止を検討する。

- GitHub read不能でrepo / identity / queueを安全に確認できない。
- 完成成果または継続に必要なoffline seedをGitHubにもLibraryにも耐久保存できない。
- プラットフォーム上限に達した。
- GitHub ready、fallback spillover、新規offline discoveryを考慮しても独立して安全に進められる作業が残らない。

Library pending数、GitHub fallback-inbox件数、未送信論文数、bank枯渇、単一payload障害はSTOP_RUN条件ではない。
