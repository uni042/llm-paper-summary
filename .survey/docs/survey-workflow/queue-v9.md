# Queue-based survey workflow v9

LLM inference-system research surveyの運用契約。判断基準は意図的に単純に保つ。

## 基本ルール

Chat research workerは毎回、default branch最新HEADの `.survey/work-queue/next-jobs.json` を読む。

1. ready jobがある → priority順に、成果を安全に保存できる範囲で可能な限り処理する。
2. research / audit / discoveryの成果をActionsが反映した結果、ready jobが0件になる → **その同じActions実行内でdiscovery jobを1件自動生成する**。
3. discoveryでは有望論文を最大5件まで返す。0件でも正常。件数合わせをしない。
4. research後、明確な確認事項が残った場合だけaudit jobを作る。
5. 1件終わったらActions反映後の最新queueを確認して次へ進む。次成果を安全に保存できない見込みなら終了する。

固定の日次件数、探索レーン別周期、research/audit比率、backlog維持目標は使わない。

## Ownership

### Chat research worker

- literature discovery
- primary-source retrieval
- full-text reading
- scientific judgment
- formal audit judgment
- complete Japanese Markdown authoring

### GitHub Actions worker

- submission validation
- paper publication/update
- job/state transitions
- identity delta maintenance
- derived-view rebuild
- ready-job generation
- **最後のready jobを消費した直後のdiscovery補充**

Actions workerは10分ごとにも起動するが、主目的は未処理submissionの回収・整合性維持。Chatがsubmissionをpushした場合はpushでも起動する。

## Queue replenishment

通常運用ではChatから `request_jobs` を投げない。

Actions workerはsubmission処理後、必ずready jobの有無を確認する。readyが1件以上なら何もしない。0件なら、その実行の中で単純なdiscovery jobを1件だけ生成してから `next-jobs.json` を確定する。

`最後のresearch/audit/discovery完了 → 同じActions runでqueue確認 → ready=0ならdiscovery生成 → next-jobsへ掲載`

## Discovery

一次情報を中心に、repo未登録のLLM推論システム関連研究を探す。新着を優先するが、重要な取りこぼしがあれば古い論文も可。1回のdiscovery submissionは**0〜5件**。弱い候補で5件を埋めない。

## Research

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

全文取得不能ならcompletedにせずblocked/deferredとする。抄録や検索断片から欠落部分を推測しない。

## Audit

全論文を機械的に監査しない。research時に、書誌・版、実装状態、評価条件、主要数値、実機/シミュレーション区別などについて**明確に確認すべき事項が残った場合だけ**auditを要求する。

## Artifact transport（通常経路）

予定されたChat workerは**新規ファイルを作成しない**。事前作成済みの固定2ファイルだけを使う。

- `.survey/work-queue/payloads/chat-payload.md`
- `.survey/work-queue/submissions/chat-inbox.json`

### research / audit

1. 最新HEADから固定payloadをfetchし、現在blob SHAを取得する。
2. 完成Markdownを固定payloadへupdateする。
3. 最新HEADから固定inboxをfetchし、現在blob SHAを取得する。
4. 小さいsubmission JSONを固定inboxへupdateする。`payload_path` は `.survey/work-queue/payloads/chat-payload.md` を指定する。
5. inbox pushでActionsが起動する。Actionsはhead commitで `chat-inbox.json` が変更された場合だけ古い `.survey/work-queue/results/chat-inbox.json` を削除して再処理する。
6. resultとqueueを確認するまで、次の固定payload/inbox上書きを開始しない。

submission例:

```json
{
  "submission_id": "chat-<job-id>-<unique>",
  "job_id": "job-...",
  "status": "completed",
  "paper_path": "papers/...md",
  "expected_blob_sha": "existing paper update時のみ必須",
  "payload_path": ".survey/work-queue/payloads/chat-payload.md",
  "audit_required": false,
  "audit_reason": null,
  "audit_flags": []
}
```

### discovery / blocked / deferred / rejected

長いMarkdownが不要なため、固定inboxだけを上書きしてよい。新規submissionファイルは作らない。

### なぜ固定2ファイルか

- 新規ファイル作成の安全検査を通常経路から除外する。
- 長いMarkdownをJSONに直接埋め込まず、長文updateと小さい制御updateを分離する。
- payload更新後にinbox更新が失敗しても、jobは未完了のままで完成Markdownは固定payloadに残る。
- 次回はpayloadの内容と対象jobを確認し、まだ有効ならinbox更新だけ再試行できる。

### update競合

updateは必ず直前にfetchしたblob SHAで行う。SHA競合時は最新HEADと対象ファイルSHAを再取得し、対象jobがまだreadyで内容が有効な場合だけ1回再試行する。競合が続く場合は保存失敗として終了し、jobを完了扱いにしない。

### 互換経路

従来の一意な `.survey/work-queue/payloads/<unique>.md` + `.survey/work-queue/submissions/<unique>.json` 新規作成方式は復旧互換用として残すが、予定Chat workerでは使用しない。

## Idempotency

- 固定inboxは更新pushのときだけ対応resultをリセットして再処理する。
- schedule起動では処理済み固定inboxを再処理しない。
- 固定payload/inboxは、前回result確認前に次jobで上書きしない。
- terminal jobを再完了しない。
- discovery補充はready jobが0件のときだけ行い、同時に複数作らない。
- paper更新はblob SHAで競合検査する。
- Actionsは単一concurrency groupで動く。

## Derived data

paper反映後のidentity delta、README、比較表等の派生データはActions側で処理する。Chatは大きい共有ファイルを通常処理で直接更新しない。

## Legacy boundary

workflow v8以前のcycle/run/daily target、10本/11本等の固定件数、旧request/result群は履歴・復旧互換であり、v9の仕事量や優先順位には使わない。
