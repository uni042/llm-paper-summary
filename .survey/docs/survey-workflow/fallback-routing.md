# Multi-outbox fallback routing

この文書は、GitHub write障害中でも論文研究を継続するための一時配送経路の正本である。研究・queue・paperの正本は常にGitHub mainであり、Google DriveとChatGPT Libraryは配送待ちoutboxとしてだけ使う。

## 1. 基本原則

GitHubへの直接反映、Google Drive outbox、ChatGPT Library outboxを独立した配送経路として扱う。完成済み成果または新規研究を継続するためのjob seedを、少なくとも1つの耐久保存先へ保存できればrunを継続する。

- GitHub writeが正常なら通常transportを優先する。
- GitHub writeがrun-wideで利用不能なら、そのrunでは同じGitHub writeを各jobごとに再試行しない。
- fallback保存はDriveを先に試し、同runでDrive経路が利用不能と判定済みならLibraryを使う。Drive保存が個別payloadだけで失敗した場合もLibraryへ切り替えてよい。
- DriveとLibraryの両方へ同じ完全payloadを通常時に複製しない。最初に耐久保存へ成功した1経路を所有者とする。
- 保存結果が不明瞭で重複の可能性がある場合は同一 `id` / `job_id` / `attempt_id` を維持し、再投入側で冪等に扱う。
- Notionは使用しない。

pending件数、未送信論文数、record bank使用数は研究容量ではない。これらをrun停止理由にしない。

## 2. Outbox

### Google Drive

`/Google Drive/llm-paper-summary-outbox/pending/<unique-id>.json`

Driveは `.github/workflows/drive-outbox-import.yml` が回収する。GitHub Actions用の認証が未設定でもpendingへの保存自体は有効な耐久チェックポイントであり、研究を止めない。認証が復旧・設定された後にImporterが順次排出する。

### ChatGPT Library

`/LLM-survey-outbox/pending/<unique-id>.json`

LibraryはScheduled Chat worker自身が回収する。GitHub read/writeが利用可能なrunの開始時とjob間でpendingを確認し、依存関係を満たす最古のenvelopeから再投入する。反映完了をGitHub側で確認した後だけ `/LLM-survey-outbox/processed/` へ移す。不正・再生不能payloadは `/LLM-survey-outbox/failed/` へ隔離し、後続正常payloadを止めない。

Library replayはDrive pendingを手動で二重投入しない。各envelopeは保存に成功したoutboxが排出責任を持つ。

## 3. 共通envelope

DriveとLibraryは同じ `schema_version: 1` のtransport envelopeを使う。追加metadataは任意だが、`writes` がGitHubへ再投入する完全な固定transportでなければならない。

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

research/auditでは5 slot + `chat-inbox.json` を1 envelopeにまとめる。完成Markdownはfallbackへ保存しない。

## 4. GitHub write不能中の新規job発行

GitHub queueを直接更新できないときでも、fallbackが1つ以上書き込み可能なら探索を止めない。Scheduled Chatは候補0〜5件を選び、固定transport `.survey/work-queue/transport/offline-job-seed.json` を書くenvelopeをoutboxへ保存する。

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

各候補の将来のresearch `job_id` はqueueと同じ決定論的規則で計算する。candidate keyは `canonical_id`、なければ `source_url`、なければ `title` をtrimして小文字化した値。`sha256(candidate_key)` の先頭16桁を使い `job-research-<16hex>` とする。

seedを耐久保存した後は、その候補をGitHub jobの実体化待ちにせず同じrunで精読してよい。完成したresearch recordは上記の決定論的 `job_id` を使う通常の5-slot envelopeとしてoutboxへ保存する。

GitHub復旧後、seedが先にGitHubへ入り `.survey/scripts/apply_offline_job_seed.py` が同じ `job_id` のready jobを実体化する。research envelopeは対応jobがGitHubに存在するまでpendingのまま待つ。この依存チェックにより、別outboxへseedとresearch結果が分散しても安全に回復できる。

## 5. Backlog indexと実行可能job

Scheduled Chatはrun開始時、可能な範囲でDrive pendingとLibrary pendingを読み、次を一時的なbacklog indexとして構築する。

- `checkpointed_job_ids`: research/auditの完全payloadがどちらかのoutboxへ保存済みのjob
- `spillover_candidates`: offline seedに存在し、まだ完成payloadがcheckpointされていない候補

GitHub上で `ready` でも `checkpointed_job_ids` にあるjobは、そのrunでは再精読対象にしない。GitHub上のstatusは未完了のまま維持する。

処理順は次とする。

1. GitHubのready jobからcheckpoint済みを除いた実行可能jobをpriority順に処理する。
2. outbox seed由来の未処理spillover candidateをpriority順に処理する。
3. どちらも無ければ新しいdiscoveryを行い、GitHub write可能なら通常job発行、write不能ならoffline seedをfallbackへ保存する。
4. 完成・blocked・checkpoint後は状態を再取得して繰り返す。

GitHub writeが復旧しているがcheckpoint済みreadyだけがqueueを塞いでいる場合、`.survey/work-queue/transport/request-jobs.json` を使い、checkpoint済みjob IDを一時的に実行不能として除外した上でdiscovery jobを追加発行してよい。checkpoint済みjob自体のstatusは変更しない。

## 6. Recovery ownership

- Drive pending: Drive ImporterだけがGitHubへ再投入する。Scheduled Chatは二重投入しない。
- Library pending: Scheduled Chatだけが再投入する。
- GitHubに同一jobのterminal resultが既にあれば、対応fallback envelopeは再writeせずprocessedとしてacknowledgeしてよい。
- offline seedは同じ決定論的job IDを生成するため再適用可能。既存job/identityと重複する候補はskipする。
- research/audit envelopeは対応jobがGitHubに存在しない間はfailedへ送らずdependency待ちとしてpendingに残す。

## 7. 停止条件

fallback障害は経路単位で扱う。Driveが壊れていてもLibraryへ保存できれば継続し、Libraryが壊れていてもDriveへ保存できれば継続する。

runを停止してよい条件は `continuation-policy.json` が正本であり、少なくとも次の考え方を守る。

- GitHub read不能でrepo/identity/queueを安全に確認できない。
- 完成成果または継続に必要なoffline seedをGitHub・Drive・Libraryのいずれにも耐久保存できない。
- プラットフォーム上限に達した。
- fallbackを含めても独立して安全に進められる研究作業が残っていない。

Drive pending数、Library pending数、未送信論文数、bank exhaustion、単一経路の障害はSTOP_RUN条件ではない。
