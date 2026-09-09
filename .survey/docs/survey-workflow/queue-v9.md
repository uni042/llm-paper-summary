# Queue-based survey workflow v9

LLM inference-system research surveyの**機械可読な運用契約**。READMEと矛盾する場合は本書を優先する。

## Ownership

### Chat research worker

Chatだけが行う:

- literature discovery
- primary-source retrieval
- full-text reading
- scientific judgment
- formal audit judgment
- complete Japanese Markdown authoring

### GitHub Actions worker

Actionsだけが行う:

- submission validation
- paper publication/update
- job/state transitions
- identity delta maintenance
- derived-view rebuild
- ready-job generation

Chatは通常処理で共有stateや既存paperを直接更新しない。

## Trigger model

通常の制御経路は**push-driven**。

1. Chatが成果をimmutable payload/submissionとしてcommitする。
2. `.survey/work-queue/submissions/*.json` のpushで `Survey helper worker` が起動する。
3. `queue_worker.py` が未処理submissionを検証・反映する。
4. workerがresult、job/state、next-jobsを更新してcommitする。

10分scheduleはfallback/reconciliation用。Chatから `workflow_dispatch` やjob rerunを通常経路として呼ばない。

## Queue

Chatは毎回、default branch最新HEADの `.survey/work-queue/next-jobs.json` を読む。同じ実行内で参照するREADME、job、queue-v9も同一HEADに固定する。

ready jobはpriority降順。1回1件に固定しないが、次jobの成果を安全に保存できない見込みなら着手しない。

### Discovery lanes

- `discovery_fresh`: 2h。原則30日以内の新規論文・重要改訂。
- `discovery_citation`: 6h。既存重要論文の引用、後継、実装。
- `discovery_gap`: 24h。欠落系統・隣接system技術。

research backlogは最大12、audit backlogは最大6。候補0件は正常。

## Job contracts

### discovery

一次情報中心に探索し、既存repoとの重複を可能な範囲で確認する。

```json
{
  "job_id": "job-...",
  "candidates": [
    {
      "canonical_id": "stable id if known",
      "title": "...",
      "source_url": "primary source URL",
      "paper_path": "papers/...md",
      "priority": 80,
      "reason": "...",
      "evidence": ["primary-source fact"]
    }
  ]
}
```

### research

一次資料本文を最後まで読み、完成済み日本語Markdownを作る。最低限:

- 問題設定・動機
- 新規性
- 手法・system設計
- hardware/model/dataset
- baseline・比較条件
- 主要定量結果
- 品質trade-off
- memory/I/O効果
- 限界
- 既存系統との差
- 一次資料

全文取得不能ならcompletedにしない。

### audit

一次資料・正式公開情報・公式実装を用い、少なくとも以下を正式監査する:

- identity / bibliography
- authors / affiliations
- publication / final version
- code / implementation status
- hardware / model / dataset / baseline
- quoted quantitative results
- real hardware vs simulation
- classification / lineage
- differences / limitations

priority >= 75、明示audit要求、不確実性、または決定的20% quality-control sampleで生成する。

## Artifact transport

### Completed research/audit

完成Markdownは**原則payload分離**する。

1. 新規 `.survey/work-queue/payloads/<unique>.md` を作る。
2. 新規 `.survey/work-queue/submissions/<unique>.json` を作る。
3. submissionはpayloadを `payload_path` で参照する。

```json
{
  "job_id": "job-...",
  "status": "completed",
  "paper_path": "papers/...md",
  "expected_blob_sha": "required for existing paper",
  "payload_path": ".survey/work-queue/payloads/<unique>.md",
  "audit_required": false,
  "audit_reason": null,
  "audit_flags": []
}
```

inline `content` は後方互換・小規模診断用に受理するが、通常のresearch/auditでは使わない。`content` と `payload_path` の同時指定は禁止。

payloadは:

- `.survey/work-queue/payloads/` 配下
- `.md`
- immutable
- submissionごとに一意
- 完成paper全体

とする。既存paperを更新する場合は、そのsubmission作成直前のblob SHAを `expected_blob_sha` に入れる。競合した場合はworkerが拒否し、Chatが最新HEADから再判断する。

### blocked / deferred / rejected

Markdownを捏造しない。

```json
{
  "job_id": "job-...",
  "status": "blocked",
  "paper_path": "papers/...md",
  "reason": "primary full text could not be obtained; ..."
}
```

## Idempotency

- submission/result filenameは一意で再利用しない。
- 同名resultが存在するsubmissionは再処理しない。
- terminal jobは再完了させない。
- workerは単一concurrency group、`cancel-in-progress: false`。
- worker commit前にpull --rebaseする。
- Chatはsubmission保存後に同じ成果を再送しない。
- paper更新はoptimistic blob SHA checkを使う。

## Derived data

paper反映後、Actionsがidentity deltaを生成する。大きい集約viewはdirty flagを立て、最大でも概ね1時間単位でbatch rebuildする。Chatはこれらを直接書かない。

## Legacy boundary

以下はworkflow v8以前の履歴・復旧互換であり、v9 control planeではない:

- cycle/run/daily target
- 10本/11本等の固定件数
- `.survey/requests/` / `.survey/results/`
- `.survey/submissions/` / `.survey/submission-results/`
- v8 state/helper scripts

旧成果は削除せず保持してよいが、新規job生成・優先順位・通常transportに使わない。
