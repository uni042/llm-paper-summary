# Queue-based survey workflow v10

workflow v10は、queue/state/identityをGitHub Actions側で管理し、Scheduled Chatは探索・全文精読・科学的判断・構造化research record作成を担当する。GitHub repositoryを唯一の正本とする。

## 1. Queue policy

1. ready jobがある場合はpriority順に処理する。
2. 1件処理するたび、Actions反映後の最新queueを読む。
3. readyが0件になればActionsがdiscovery jobを1件補充する。
4. discoveryは有望候補0〜5件。5件はノルマではない。
5. research後に明確な追加確認が必要な場合だけauditを生成する。
6. 同一runでは `discovery → research → 必要ならaudit → queue再取得 → 次discovery` を、実行環境が許す限り繰り返す。

固定の日次件数、固定research/audit比率、固定バッチ数、旧cycle/runは使わない。

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
- GitHub反映保留時のtemporary transport

### GitHub Actions

- structured slot / SHA / schema validation
- deterministic Markdown rendering
- paper publication/update
- job/state transition
- identity delta maintenance
- derived-view rebuild
- duplicate research suppression
- ready=0時のdiscovery補充

NotionとChatGPT Libraryは一時配送キューとしてのみ使い、研究・paper・queueの正本にはしない。

## 3. Duplicate prevention

Discovery候補提出前とresearch着手前に、次をidentity正本として照合する。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. `papers/inference/**` frontmatter

canonical ID / arXiv ID / DOI / OpenReview IDを優先する。GitHub code searchだけで未登録判定をしない。Actions側の `.survey/scripts/dedupe_queue.py` もdiscovery由来researchを再照合し、重複なら `superseded` にする。

## 4. Research quality

一次資料本文を最後まで読む。全文取得不能ならcompletedにせずblocked/deferredとする。抄録・検索断片から欠落情報を推測しない。

本文の品質基準は `.survey/templates/paper.md` を正本とする。新しい会話・実行環境では、テンプレートで例示する `papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md` も最初に確認する。

構造化recordは内部メモではなく、rendererが人間向け本文へ変換する原稿である。特に `problem_method` は次を文章で説明する。

1. 何がボトルネックで、既存方式ではなぜ残るか。
2. request / token / weight / KV cache / activation等がどう流れるか。
3. 各機構が何を観測・保持し、何を選択・移動・削除・予測するか。
4. その処理がどの計算・memory・I/O・待ち時間を減らすか。
5. 誤予測、通信増、resource不足、workload変化等で何が起きるか。
6. 評価値がなぜその条件で出て、どの条件で悪化するか。

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

### Paper path / filename

論文ファイル名は年始まりの既存形式へ統一する。

- arXiv論文: `papers/inference/<lineage>/YYYY-YYMM.NNNNN-<slug>.md`
- arXiv IDを持たない論文: `YYYY-<stable-key>-<slug>.md` または既存互換の `YYYY-<slug>.md`
- `<slug>` は小文字英数字とハイフンを基本とする。
- 年・識別子を欠く題名スラッグ単独の新規ファイルは作らない。
- `paper_path` は一次資料から識別子と発表年を確認してから確定する。
- auditでは既存pathを原則維持する。改名が必要な場合は派生viewもActionsで再生成する。

## 5. Structured record transport

research/auditの通常経路では完成MarkdownをChatからGitHubへ送らない。固定A/B bankの5 JSON slotを使用する。

- bank A: `.survey/work-queue/records/chat-record/`
- bank B: `.survey/work-queue/records/chat-record-b/`
- slots: `metadata.json`, `problem_method.json`, `evaluation.json`, `results.json`, `positioning.json`

通常はAを使う。Aに別jobの途中保存があり、その内容がまだ他に耐久保存されていない場合だけBを使う。一時配送キューへ完全payloadを保存済みなら、partial slotは唯一の成果コピーではないためbankを後続jobへ再利用してよい。

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

slot上限:

- `metadata`: 8192 bytes
- `problem_method`: 16384 bytes
- `evaluation`: 12288 bytes
- `results`: 12288 bytes
- `positioning`: 8192 bytes

### metadata.data

必須: `title`, `canonical_id`, `source`, `summary`。

主なfield:

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

### problem_method.data

`method_overview` と `components` は必須。複雑な論文では必要数のcomponentを使い、入力・状態・処理・出力・次段との接続・効果・境界条件が追える説明にする。

```json
{
  "problem": "...",
  "novelty": "...",
  "method_overview": "...",
  "components": [
    {"name": "...", "description": "..."}
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
  "settings": [{"name": "...", "description": "..."}],
  "correctness": "...",
  "methodology": "...",
  "scope": "..."
}
```

### results.data

主要値は比較条件と一緒に構造化し、`overview` / `interpretation` で意味も説明する。

```json
{
  "overview": "...",
  "key_results": [
    {
      "metric": "...",
      "value": "...",
      "baseline": "...",
      "condition": "...",
      "interpretation": "..."
    }
  ],
  "negative_results": [{"name": "...", "description": "..."}],
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

1. 同一job用の一意な `attempt_id` と使用bankを決める。
2. `metadata` → `problem_method` → `evaluation` → `results` → `positioning` の順に処理する。
3. 各slotは直前fetchした現在blob SHA付きでupdateする。
4. update後のblob SHAを記録する。
5. 途中で反映が保留になった場合はinboxを送らず、最新状態を取得して対象slotだけ1回再試行する。
6. 5 slotすべて反映後だけ固定 `.survey/work-queue/submissions/chat-inbox.json` をupdateする。
7. inboxの `record_slots` は5件固定・上記順序で、各 `slot`, `path`, `blob_sha` を入れる。
8. `.survey/scripts/assemble_research_record.py` がrecordを検証し、`.survey/scripts/render_paper.py` がrunner内でMarkdownを生成する。
9. 既存 `queue_worker.py` へ一時 `payload_path` として渡す。
10. transient Markdown/inbox変換はcommit前にrestoreする。
11. 新しいresultが同一 `job_id` で `ok: true`、かつ最新queueでjob terminalになるまで次jobでslotを上書きしない。ただし、そのattemptの完全payloadを一時配送キューへ耐久保存済みならbankは再利用できる。

Inbox例:

```json
{
  "submission_id": "chat-job-...",
  "attempt_id": "attempt-...",
  "job_id": "job-...",
  "status": "completed",
  "record_bank": "a",
  "paper_path": "papers/inference/...md",
  "expected_blob_sha": null,
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

bank Bではpath rootを `.survey/work-queue/records/chat-record-b/` に置き換える。

## 7. Discovery / blocked / deferred / rejected

長いartifactは不要なので固定inboxだけをupdateする。新規submissionファイルを通常経路で作らない。

## 8. Temporary transport

接続先IDは公開repoへ書かず、予定タスクのprivate設定に保持する。

研究成果/更新payloadが完成しているがGitHubへの反映を完了できない場合（権限状態、接続状態、操作検証、SHA競合等）は、最新状態を取得して対象単位を1回再試行する。それでも反映できなければ、再投入に必要な完全logical payloadをNotion一時配送キューへ `pending` 保存する。Notionへ保存できなければChatGPT Libraryのprivate一時配送キューへ保存する。

Notion/Libraryへの一時保管はGitHub publication成功ではない。queue上のjobは未完了のままにする。ただし完全payloadの一時保管が成功した時点を後続jobへ進む耐久チェックポイントとし、同じrunを継続する。3つの保存先のいずれにも成果を保持できない場合のみ後続処理を停止する。

GitHub Actions内で最終反映が保留になった場合は入力済みなので外部キューへ重複保存せず、Actions側の再処理を優先する。

### Temporary payload

1 attempt = 1 payload。少なくとも `Status=pending`, `Kind`, `Job ID`, `Attempt ID`, `Paper Path`, `Failure Class` と再投入に必要なlogical dataを保持する。

research/audit例:

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

GitHub blob SHAは一時配送キューへ固定しない。再投入時に各slotを改めてfetch/updateし、その時のblob SHAからinbox manifestを作る。

### Replay protocol

各scheduled runの開始時に `pending` を確認する。

1. pending payloadを読む。
2. 最新queue/identity/対象paperを確認する。
3. 成果が未反映でjobがまだ適用可能なら `replaying` とする。
4. 利用可能なv10 record bankへ通常protocolで再投入する。
5. Actions resultとqueueを確認する。
6. 成功時だけ `replayed` とする。
7. jobがterminal/superseded、identity衝突、成果がstale等で適用対象外なら理由を残して `dead_letter` とする。
8. 再投入を完了できなければ `pending` のまま残す。

## 9. Transport integrity / connector rules

- Scheduled Chatから新規GitHub transport fileを通常運用で作らない。
- paper/state/README/identity/queueをChatから直接updateしない。
- 予定タスクから書けるpathはA/B固定record slots、固定inbox、08:30用固定payload/inboxに限定する。
- 転送データは通常のUTF-8 JSON/Markdownとして扱い、既定の検証・承認条件を維持する。
- 構造化JSONはpayload size、validation、partial retry、idempotencyを改善するために使用する。
- 単一の反映保留で予定タスクを停止/無効化/自己変更しない。
- completionはActions result + latest queueで検証する。

## 10. Compatibility

v9のMarkdown chunk経路は復旧互換として残す。

- `.survey/work-queue/payloads/chat-chunks/part-01.md`〜`part-08.md`
- `.survey/scripts/assemble_chat_chunks.py`

v10予定workerの通常経路では使わない。Actionsはv10 structured recordを先に処理し、legacy `payload_chunks` がある場合だけv9 assemblerを使う。

## 11. Rationale / external evidence

Scheduled Tasks / GitHub connectorの実効能力は、接続権限・実行環境・承認条件・API endpointごとに非対称になり得る。設計判断の根拠と固定URLは [references/github-connector-reliability.md](references/github-connector-reliability.md) を参照する。
