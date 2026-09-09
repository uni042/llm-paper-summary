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

したがって通常は次のようになる。

`最後のresearch/audit/discovery完了 → 同じActions runでqueue確認 → ready=0ならdiscovery生成 → next-jobsへ掲載`

Chatは成果submissionを保存した後、Actions反映済みの最新HEADと `next-jobs.json` を読み直せばよい。別の `request_jobs` 往復を挟まない。

過去に作成済みの `request_jobs` submissionは互換のため処理可能でもよいが、新規通常運用では使用しない。

## Discovery

一次情報を中心に、repo未登録のLLM推論システム関連研究を探す。新着を優先するが、重要な取りこぼしがあれば古い論文も可。

1回のdiscovery submissionは**0〜5件**。弱い候補で5件を埋めない。

候補0件だった場合、そのdiscovery jobが完了してreadyが0になるため、同じActions実行で次のdiscovery jobが1件補充される。これによりqueueは原則として空のまま確定しない。

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

重要度だけを理由に自動監査しない。固定割合の抜取監査もしない。

## Artifact transport

完成research/auditは原則として:

1. `.survey/work-queue/payloads/<unique>.md`
2. `.survey/work-queue/submissions/<unique>.json`

の2ファイルに分ける。

submission例:

```json
{
  "job_id": "job-...",
  "status": "completed",
  "paper_path": "papers/...md",
  "expected_blob_sha": "existing paper update時のみ必須",
  "payload_path": ".survey/work-queue/payloads/<unique>.md",
  "audit_required": false,
  "audit_reason": null,
  "audit_flags": []
}
```

既存paper更新では最新blob SHAを必須とする。

## Idempotency

- submission/result filenameは一意で再利用しない。
- 同名resultがあれば再処理しない。
- terminal jobを再完了しない。
- discovery補充はready jobが0件のときだけ行い、同時に複数作らない。
- paper更新はblob SHAで競合検査する。
- Chatはsubmission保存後に同じ成果を再送しない。
- Actionsは単一concurrency groupで動く。

## Derived data

paper反映後のidentity delta、README、比較表等の派生データはActions側で処理する。Chatは大きい共有ファイルを通常処理で直接更新しない。

## Legacy boundary

workflow v8以前のcycle/run/daily target、10本/11本等の固定件数、旧request/result群は履歴・復旧互換であり、v9の仕事量や優先順位には使わない。
