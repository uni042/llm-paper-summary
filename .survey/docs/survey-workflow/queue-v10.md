# Queue-based survey workflow v10

workflow v10は、v9で安定しているqueue/state/identity処理を維持しつつ、Chat→GitHubのartifact transportを**完成Markdown chunk**から**構造化research record**へ置き換える。

## 1. Queue policy

1. ready jobがある → priority順に、安全にsubmission保存まで完了できる範囲で可能な限り処理する。
2. research / audit / discoveryの成果をActionsが反映した結果、ready jobが0件になる → 同じActions実行内でdiscovery jobを1件だけ生成する。
3. discoveryは有望候補0〜5件。5件はノルマではない。
4. research後、明確な確認事項が残った場合だけauditを要求する。
5. 1件終わるたびActions反映後の最新queueを読む。

固定の日次件数、旧cycle/run、固定research/audit比率、backlog数合わせは使わない。

## 2. Ownership

### Scheduled Chat worker

- literature discovery
- primary-source retrieval
- full-text reading
- scientific judgment
- formal audit judgment
- duplicate pre-check
- structured research record authoring
- fixed record slot transport
- GitHub connector write不能時のNotion temporary fallback

### GitHub Actions

- structured slot / SHA / schema validation
- deterministic Markdown rendering
- paper publication/update
- job/state transition
- identity delta maintenance
- derived-view rebuild
- duplicate research suppression
- ready=0時のdiscovery補充

GitHub repositoryが唯一の正本。Notionはtransport failure時の一時保管のみ。

## 3. Duplicate prevention

未登録判定をGitHub code searchだけに依存しない。次をidentity正本として、Discovery候補提出前とresearch着手前に照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**` frontmatter

canonical ID / arXiv ID / DOI / OpenReview IDを優先する。Actions側の `.survey/scripts/dedupe_queue.py` もdiscovery由来ready researchを再照合し、重複なら `superseded` にする。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedにせずblocked/deferredとする。抄録・検索断片から欠落情報を推測しない。

最低限確認する情報:

- 書誌・版・著者/所属
- 問題設定と新規性
- system設計と主要構成要素
- hardware / software / model / dataset / trace
- baselinesと比較条件
- 主要定量結果とcondition
- negative result / boundary condition
- correctness / quality trade-off
- limitation
- implementation/public artifact status
- 既存研究との差
- 一次資料URL

## 5. Structured record transport

research/auditの通常経路では完成MarkdownをGitHub APIへ送らない。Chatは同じ5 slotを持つ固定A/B bankを使用する。

- bank A: `.survey/work-queue/records/chat-record/`
- bank B: `.survey/work-queue/records/chat-record-b/`
- 各bankのslot: `metadata.json`, `problem_method.json`, `evaluation.json`, `results.json`, `positioning.json`

通常はAを使う。Aに別jobの途中保存が残り、そのjobを今すぐ完了できずAを上書きすると成果を失う場合だけBを使う。単に負荷分散するため交互利用しない。

各slot envelope:

```json
{
  "schema_version": 1,
  "transport_version": 10,
  "slot": "metadata",
  "attempt_id": "attempt-unique",
  "job_id": "job-...",
  "data": {}
}
```

各slot最大8192 bytes。通常は数百〜数千byteを目安とし、冗長な重複を避ける。ただし事実・条件・重要な説明を削ってサイズ合わせをしない。

### metadata.data

```json
{
  "canonical_id": "arXiv:2606.26666",
  "arxiv_id": "2606.26666",
  "title": "...",
  "summary": "...",
  "source": "https://...",
  "authors": ["..."],
  "publication": "...",
  "publication_type": "...",
  "topics": ["..."],
  "implementation": "...",
  "sources": ["https://..."]
}
```

`title`, `canonical_id`, `source`, `summary` は必須。

### problem_method.data

```json
{
  "problem": "...",
  "novelty": "...",
  "method_overview": "...",
  "components": [
    {"name": "component", "description": "..."}
  ],
  "system_design": "..."
}
```

### evaluation.data

```json
{
  "hardware": ["..."],
  "software": ["..."],
  "model": ["..."],
  "datasets": ["..."],
  "baselines": ["..."],
  "settings": [
    {"name": "page size", "description": "16"}
  ],
  "correctness": "...",
  "methodology": "...",
  "scope": "..."
}
```

### results.data

主要値は可能な限り自由文へ埋めず、比較条件と一緒にレコード化する。

```json
{
  "overview": "...",
  "key_results": [
    {
      "metric": "B1 decode speedup",
      "value": "1.403±0.065×",
      "baseline": "FlashInfer",
      "condition": "5 held-out seeds, synchronized wall throughput",
      "interpretation": "..."
    }
  ],
  "negative_results": [
    {"name": "B4", "description": "..."}
  ],
  "interpretation": "...",
  "quality_impact": "..."
}
```

### positioning.data

```json
{
  "differences": ["..."],
  "limitations": ["..."],
  "implementation_status": "...",
  "research_positioning": "...",
  "audit_notes": "..."
}
```

## 6. Save protocol

1. 同一job用の一意な `attempt_id` を決め、使用bank `a` / `b` を選ぶ。
2. `metadata` → `problem_method` → `evaluation` → `results` → `positioning` の順に処理する。
3. 各固定slotを直前fetchし、現在blob SHA付きでupdateする。
4. update成功後に返った新blob SHAを記録する。
5. 途中失敗ならinboxを送らない。成功済みslotは保持し、job/attemptがまだ有効なら失敗slotだけ1回安全に再試行する。
6. 選択bankの5 slotすべて保存成功後だけ固定 `.survey/work-queue/submissions/chat-inbox.json` をupdateする。
7. inboxの `record_slots` は5件固定・上記順序で、各 `slot`, `path`, `blob_sha` を入れる。
8. Actionsの `.survey/scripts/assemble_research_record.py` が全slotを検証し、`.survey/scripts/render_paper.py` でrunner内だけにMarkdownを生成する。
9. 既存 `queue_worker.py` へ一時 `payload_path` として渡す。
10. transient Markdown/inbox変換はcommit前にrestoreする。
11. inbox push時に旧resultがresetされた後、新しく生成されたresultが同一 `job_id` で `ok: true`、かつ最新queueでjob terminalになるまでslotを次jobで上書きしない。

Inbox例:

```json
{
  "submission_id": "chat-job-...",
  "attempt_id": "attempt-...",
  "job_id": "job-...",
  "status": "completed",
  "record_bank": "a",
  "paper_path": "papers/inference/...md",
  "expected_blob_sha": "existing paper update時のみ",
  "record_slots": [
    {"slot": "metadata", "path": ".survey/work-queue/records/chat-record/metadata.json", "blob_sha": "..."},
    {"slot": "problem_method", "path": ".survey/work-queue/records/chat-record/problem_method.json", "blob_sha": "..."},
    {"slot": "evaluation", "path": ".survey/work-queue/records/chat-record/evaluation.json", "blob_sha": "..."},
    {"slot": "results", "path": ".survey/work-queue/records/chat-record/results.json", "blob_sha": "..."},
    {"slot": "positioning", "path": ".survey/work-queue/records/chat-record/positioning.json", "blob_sha": "..."}
  ],
  "audit_required": false,
  "audit_reason": null,
  "audit_flags": []
}
```

`record_bank` と各 `record_slots[].path` は一致させる。bank Bではpath rootを `.survey/work-queue/records/chat-record-b/` に置き換える。

## 7. Discovery / blocked / deferred / rejected

長いartifactが不要なので固定inboxだけをupdateする。新規submissionファイルを通常経路で作らない。

## 8. Notion transport fallback

Notion接続先は公開repoへIDを書かず、予定タスクのprivate設定に保持する。

### 退避する条件

研究成果/更新payloadが完成しているが、次の理由でChat→GitHub transportを完了できない場合:

- connector writeが403 / permission denied
- GitHub write toolが実行中に利用不能になった
- GitHub connector接続障害
- write操作が安全検査で停止
- SHA競合後、最新状態を取り直して1回再試行しても保存不能

GitHub Actions内部の最終push失敗はNotion退避対象外。入力はGitHubに届いているため、Actions側の再実行/10分scheduleで回復する。

### Notionに保存する論理payload

1ページ=1 attempt。propertiesには少なくとも `Status=pending`, `Kind`, `Job ID`, `Attempt ID`, `Paper Path`, `Failure Class` を持たせる。本文には再投入に必要な論理データをJSONとして保存する。

research/audit:

```json
{
  "transport_version": 10,
  "kind": "research",
  "job_id": "job-...",
  "attempt_id": "attempt-...",
  "paper_path": "papers/...md",
  "expected_blob_sha": null,
  "slots": {
    "metadata": {},
    "problem_method": {},
    "evaluation": {},
    "results": {},
    "positioning": {}
  },
  "submission": {
    "status": "completed",
    "audit_required": false,
    "audit_reason": null,
    "audit_flags": []
  }
}
```

GitHub blob SHAはNotionへ固定しない。replay時に各固定slotを改めてfetch/updateし、その時に返った新SHAからinbox manifestを作る。

### Replay protocol

各scheduled runの開始時、GitHub writeが使えるなら `pending` を確認する。

1. pending pageを読む。
2. 最新queue/identity/対象paperを再確認する。
3. 同じ成果が未反映でjobがまだ適用可能なら `replaying` にする。
4. 空いているv10 record bankを選び、固定slot/inboxへ通常protocolで再投入する。
5. Actions resultとqueueを確認する。
6. 成功時だけNotionを `replayed` にする。
7. jobがすでにterminal/superseded、identity衝突、成果がstaleで安全に適用不能なら `dead_letter` とし、盲目的に反映しない。
8. 再度connector障害なら `pending` のまま残す。

Notion保存成功はGitHub publication成功ではない。queue上のjobをcompletedにしない。

## 9. Safety / connector rules

- Scheduled Chatから `create_file` を通常運用で使わない。
- paper/state/README/identity/queueを直接updateしない。
- 予定タスクから書けるGitHub pathをA/B固定record slots、固定inbox、08:30用固定payload/inboxに限定する。
- Base64、圧縮、難読化などを安全検査回避のために使わない。
- 構造化JSONは操作サイズ・再試行粒度・検証性を改善するための形式であり、安全境界を迂回するためのものではない。
- 単一write失敗で予定タスクを停止/無効化/自己変更しない。
- completionはresult + latest queueで検証する。

## 10. Compatibility

v9のMarkdown chunk経路は復旧互換として残す。

- `.survey/work-queue/payloads/chat-chunks/part-01.md`〜`part-08.md`
- `.survey/scripts/assemble_chat_chunks.py`

v10予定workerの通常経路では使わない。Actionsはv10 structured recordを先に処理し、legacy `payload_chunks` がある場合だけv9 assemblerを使う。

## 11. Rationale / external evidence

Scheduled Tasks / GitHub connectorの実効能力は、接続権限・実行環境・承認境界・API endpointごとに非対称になり得る。設計判断の根拠と固定URLは [references/github-connector-reliability.md](references/github-connector-reliability.md) を参照する。
