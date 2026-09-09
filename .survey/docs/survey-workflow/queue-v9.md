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
- discovery候補を出す前のidentity事前確認
- 完成Markdownを小さい固定chunkへ分割して保存

### GitHub Actions worker

- submission validation
- chunk SHA validation / transient assembly
- paper publication/update
- job/state transitions
- identity delta maintenance
- derived-view rebuild
- ready-job generation
- duplicate research job suppression
- **最後のready jobを消費した直後のdiscovery補充**

Actions workerは10分ごとにも起動するが、主目的は未処理submissionの回収・整合性維持。Chatがsubmissionをpushした場合はpushでも起動する。

## Queue replenishment

通常運用ではChatから `request_jobs` を投げない。

Actions workerはsubmission処理後、必ずready jobの有無を確認する。readyが1件以上なら何もしない。0件なら、その実行の中で単純なdiscovery jobを1件だけ生成してから `next-jobs.json` を確定する。

`最後のresearch/audit/discovery完了 → 同じActions runでqueue確認 → ready=0ならdiscovery生成 → next-jobsへ掲載`

## Duplicate prevention

重複判定の正本はGitHub code searchではなく、次のidentity情報とする。

1. `.survey/survey-state/paper-identity-index.json`
2. `.survey/survey-state/identity-deltas/**/*.json`
3. 現在の `papers/inference/**` frontmatter

### Chat側の事前チェック

Discovery候補をsubmissionへ入れる前に、候補ごとに可能な限り canonical ID / arXiv ID / DOI / OpenReview ID を確定し、上記identity情報と照合する。特にarXiv URLからはIDを抽出して比較する。**GitHub code searchで論文名が見つからないことを「未登録」の根拠にしない。**

identity上ですでに登録済みなら候補から除外する。research着手前にもcanonical IDを再照合する。

### Actions側の強制ガード

`.survey/scripts/dedupe_queue.py` をqueue処理の前後に実行する。

- queue処理前: 過去runから残った重複ready research jobを `superseded` にする。
- queue処理後: discoveryが新しく生成したresearch jobを再度identity照合し、重複なら同じActions run内で `superseded` にする。
- その後queue workerを再実行して `next-jobs.json` を再生成する。

自動supersede対象はdiscovery由来のready research jobだけ。auditや意図的な既存paper更新は自動除外しない。

## Discovery

一次情報を中心に、repo未登録のLLM推論システム関連研究を探す。新着を優先するが、重要な取りこぼしがあれば古い論文も可。1回のdiscovery submissionは**0〜5件**。弱い候補で5件を埋めない。候補作成時はDuplicate preventionを必ず適用する。

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

# Artifact transport（通常経路）

## 原則

予定されたChat workerは**完成Markdown全文を1回のGitHub updateへ渡さない**。また、通常運用では新規payload/submissionファイルを作らない。

事前作成済みの固定slotを使う。

- `.survey/work-queue/payloads/chat-chunks/part-01.md`
- `.survey/work-queue/payloads/chat-chunks/part-02.md`
- ...
- `.survey/work-queue/payloads/chat-chunks/part-08.md`
- trigger: `.survey/work-queue/submissions/chat-inbox.json`

旧 `.survey/work-queue/payloads/chat-payload.md` はActions runner内の一時連結先としてのみ使う。予定Chat workerは直接更新しない。

## research / audit 保存手順

1. 完成Markdownを章・節・表などの自然な境界で分割する。
2. 使用するslotは必ず `part-01` から連番にする。飛び番を使わない。
3. 各chunkは最大 **8192 bytes**。安全検査の実績を考慮し、通常は **2〜5 KiB程度**を目安にする。必要以上に長いchunkを作らない。
4. `part-01.md` を最新HEADからfetchし、現在blob SHAで既存ファイルupdateする。成功後に返った**新しいblob SHA**を保持する。
5. `part-02.md` 以降も同様に、必要数だけ順番にupdateする。
6. 途中のchunk updateが失敗したら、**まだinboxを送らない**。成功済みchunkは保持し、最新HEAD/SHAと内容を確認したうえで失敗chunkから再開する。成功済みchunkを無意味に再送しない。
7. すべての使用chunkが保存できたら、固定inboxを小さいmanifestでupdateする。各chunkについてpathと**保存後blob SHA**を指定する。
8. inbox pushでActionsが起動する。`.survey/scripts/assemble_chat_chunks.py` が使用chunkを順番・path・size・blob SHAまで検証する。
9. 検証成功時だけrunner内で旧 `chat-payload.md` へ一時連結し、local inboxをqueue worker互換の `payload_path` 形式へ変換する。
10. queue workerがpaperへ反映した後、Actionsは一時連結した `chat-payload.md` とlocal変換したinboxをcheckout状態へ戻してからcommitする。**連結済み長文そのものはGitHubへcommitしない。**
11. `.survey/work-queue/results/chat-inbox.json` が同じjobに対して `ok: true` となり、最新queueからjob完了を確認するまで、同じslot群を次jobで上書きしない。

### inbox例

```json
{
  "submission_id": "chat-<job-id>-<unique>",
  "attempt_id": "attempt-<unique>",
  "job_id": "job-...",
  "status": "completed",
  "paper_path": "papers/...md",
  "expected_blob_sha": "existing paper update時のみ必須",
  "payload_chunks": [
    {
      "path": ".survey/work-queue/payloads/chat-chunks/part-01.md",
      "blob_sha": "<saved blob sha 01>"
    },
    {
      "path": ".survey/work-queue/payloads/chat-chunks/part-02.md",
      "blob_sha": "<saved blob sha 02>"
    }
  ],
  "audit_required": false,
  "audit_reason": null,
  "audit_flags": []
}
```

`payload_chunks` と `payload_path` は同時に指定しない。通常の予定Chat workerは `payload_chunks` を使う。

## 分割境界

文字数均等分割より意味境界を優先する。推奨例:

- chunk 1: frontmatter + 概要 + 問題設定
- chunk 2: 新規性 + 設計概要
- chunk 3: 詳細手法
- chunk 4: 評価条件 + baseline
- chunk 5: 主要結果
- chunk 6: 限界 + 関連研究との差 + 一次資料

短い論文ページなら2〜3chunkでよい。8chunkを埋めることは目的ではない。

## Partial-save recovery

分割slotは**回復単位**でもある。

- part-01〜03成功、part-04失敗 → 01〜03を保持し、04から再試行。
- chunk保存は全部成功、inboxだけ失敗 → chunkのblob SHAと内容が現在HEADでも同じことを確認してinboxだけ再試行。
- inbox成功後にActions error → slotを上書きせずresult原因を確認し、内容が有効なら修正対象だけ更新して新しいattempt_idで再送。

前回途中保存済みのjobがまだreadyで内容も有効なら、**新しいpriority jobより先に途中保存jobを完了させる**。固定slotを別jobで上書きして完成済み部分を失わないため。

## discovery / blocked / deferred / rejected

長いMarkdownが不要なため、固定inboxだけを上書きしてよい。新規submissionファイルは作らない。

既登録重複の整理をChat submissionで行う必要は通常ない。Actionsのduplicate guardがdiscovery由来ready research jobを自動supersedeする。

## Connector-safe write rules

予定タスク環境では次を正式ルールとする。

- `create_file` を通常経路で使わない。
- **完成Markdown全文を1ファイルupdateしない。**
- 長文は固定chunkへ分ける。1chunk最大8 KiB、通常2〜5 KiB程度。
- 制御JSONは最小限にする。
- 大きい共有READMEやstateをChatから直接書き換えない。
- 既存ファイルupdateは直前fetchしたblob SHAを使う。
- 各chunkの保存後blob SHAをinboxに固定し、Actions側で再検証する。
- 同一内容の再送を避けるため一意な `attempt_id` を使う。
- 安全検査・接続・SHA競合で失敗してもjobを完了扱いにしない。
- 失敗時は最新HEAD/SHAを取り直し、内容がまだ有効ならその失敗単位だけ1回再試行する。
- 単一失敗を理由に予定タスクを停止・無効化しない。

## update競合

chunk updateは必ず直前にfetchしたblob SHAで行う。SHA競合時は最新HEADと対象slot SHAを再取得し、対象jobがまだreadyでchunk内容が有効な場合だけそのchunkを1回再試行する。競合が続く場合は保存失敗として終了し、jobを完了扱いにしない。

## 互換経路

以下は復旧互換用で、予定Chat workerの通常経路では使わない。

- `.survey/work-queue/payloads/chat-payload.md` の直接更新
- 一意な `.survey/work-queue/payloads/<unique>.md` + `.survey/work-queue/submissions/<unique>.json` 新規作成
- inline `content` に完成Markdown全文を埋め込む方式

## Idempotency

- 固定inboxは更新pushのときだけ対応resultをリセットして再処理する。
- schedule起動では処理済み固定inboxを再処理しない。
- 使用chunk/inboxは、前回result確認前に次jobで上書きしない。
- inboxは各chunkのblob SHAを固定するため、別内容へのすり替わりや古いslot混在をActionsが拒否できる。
- terminal jobを再完了しない。
- discovery補充はready jobが0件のときだけ行い、同時に複数作らない。
- paper更新はblob SHAで競合検査する。
- discovery由来research jobはActionsでidentity再照合する。
- Actionsは単一concurrency groupで動く。

## Derived data

paper反映後のidentity delta、README、比較表等の派生データはActions側で処理する。Chatは大きい共有ファイルを通常処理で直接更新しない。

## Legacy boundary

workflow v8以前のcycle/run/daily target、10本/11本等の固定件数、旧request/result群は履歴・復旧互換であり、v9の仕事量や優先順位には使わない。
