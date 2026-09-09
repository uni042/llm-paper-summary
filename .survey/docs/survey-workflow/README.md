# 研究サーベイ運用手順

現在の正本は **workflow v10（structured-record transport + queue）**。予定されたChat workerは毎回default branchの最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、`.survey/work-queue/next-jobs.json` を読む。

## 設計原則

- **Chat研究worker**: 一次資料の検索・取得、全文精読、科学的判断、正式監査、構造化research record作成。
- **GitHub Actions worker**: record検証、Markdownレンダリング、paper反映、job/state遷移、identity delta、派生view更新、次job生成。
- GitHub repositoryを唯一の正本とする。
- Notion / ChatGPT LibraryはGitHub反映保留時だけ使う一時配送キューであり、研究正本・paper正本・queue正本にはしない。
- 固定の日次件数、旧cycle/run、固定research/audit比率は使わない。
- 予約済みworkerは1つのまま維持し、08:30 JSTだけその他更新、それ以外の毎時:30は論文workerを選ぶ。
- 論文workerは探索だけで終了せず、探索した候補の全文精読・保存まで同一runで連続処理する。queueが空になって新しいdiscovery jobが補充された場合も処理を続け、実行上限または実処理上の阻害要因に当たるまで繰り返す。
- 論文本文の品質正本は [paper template](../../templates/paper.md) とする。論文を読んでいない読者でも背景、手法、処理の流れ、なぜ効くか、効かない条件まで追える文章を生成する。
- 説明密度のお手本は [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) とする。

## 論文ファイルの命名規則

既存の年始まり形式を正本とし、新規論文も同じ形式へ統一する。

- arXiv論文: `YYYY-YYMM.NNNNN-<slug>.md`
- arXiv IDを持たない論文: `YYYY-<stable-key>-<slug>.md` または既存互換の `YYYY-<slug>.md`
- `<slug>` は小文字英数字とハイフンを基本とし、論文・システムを識別できる短い名前にする。
- 年・識別子を欠く題名スラッグ単独の新規ファイルは作らない。
- `paper_path` は一次資料から `canonical_id`、`arxiv_id`、発表年を確認した後に確定する。
- auditでは既存pathを原則維持する。改名が必要な場合はカテゴリREADME、比較表、identity index等の派生viewも再生成する。

## v10 transport

v10では完成MarkdownをChatからGitHubへ送らない。research/auditを5つのJSON record slotへ分け、GitHub Actions内の `.survey/scripts/render_paper.py` が最終Markdownを生成する。

固定slotはA/Bの2 bankを事前作成している。

- bank A: `.survey/work-queue/records/chat-record/`
- bank B: `.survey/work-queue/records/chat-record-b/`
- slots: `metadata.json` / `problem_method.json` / `evaluation.json` / `results.json` / `positioning.json`

通常はAを使い、別jobの途中保存がAに残り、まだ完全payloadを他へ耐久保存していない場合だけBを使う。完全payloadが一時配送キューへ保存済みなら、partial slotは唯一の成果コピーではないためbankを後続jobへ再利用できる。

構造化recordは圧縮した研究メモではなく、Markdownへほぼそのまま変換される本文原稿である。特に `problem_method` は方式名・略語・数式の列挙で済ませず、各機構について入力、観測状態、処理、出力、次の処理との接続、改善するボトルネック、境界条件まで文章で書く。

選択したbankの5 slotすべての反映後だけ `.survey/work-queue/submissions/chat-inbox.json` を更新する。各slotは直前fetchしたblob SHAで既存ファイルをupdateし、manifestには保存後のblob SHAを入れる。Actionsはpath・順序・サイズ・SHA・attempt_id・job_idを検証してからMarkdownを生成する。

```text
Scheduled Chat worker
      │
      ├─ bank A または B
      │   ├─ metadata.json
      │   ├─ problem_method.json
      │   ├─ evaluation.json
      │   ├─ results.json
      │   └─ positioning.json
              │ 全5件反映後
              ▼
         chat-inbox.json
              │
              ▼
        Survey helper worker
              │
       record SHA/schema検証
              │
       render_paper.py
              │
       stable queue worker
       ┌──────┼─────────┐
       ▼      ▼         ▼
     paper   state    next-jobs
```

旧 `part-01.md`〜`part-08.md` と `assemble_chat_chunks.py` は復旧互換用として残すが、予定タスクの通常経路では使わない。

## 1回の論文worker

1. 最新HEADのrouter、queue-v10、next-jobs、paper templateを読む。新しい会話・実行環境ではMoE-Infinityのお手本も確認する。
2. GitHubへの反映が利用可能なら、まずNotion / Libraryの `pending` を確認し、現在queueと整合する未反映成果があれば新規jobより先に再投入する。
3. ready research/auditがあればpriority順に処理する。research着手前とdiscovery候補提出前にidentity正本で重複確認する。
4. readyがdiscoveryなら探索を実行し候補を固定inboxへ保存する。Actions反映後の最新queueを読み直し、生成されたresearch jobへ直ちに進む。
5. research/auditは一次資料全文を読み、選択bankの5 slot用の構造化recordを作る。抄録や検索断片から欠落を推測しない。
6. 評価は比較対象と条件を明示し、数値が出る理由、別条件で利得が消える理由、実機かsimulationかを説明する。
7. 固定slotを順番にupdateする。途中で反映が保留になった場合は最新状態を取得し、対象slotだけ1回再試行する。
8. 全slot反映後だけinboxをupdateする。
9. `.survey/work-queue/results/chat-inbox.json` が同一 `job_id` で `ok: true`、かつ最新queueでjob完了になるまで完了扱いにしない。
10. 1件完了ごとに最新queueを読み直す。researchからauditが生成されたら同じrunで処理する。
11. readyが0件になりActionsが次のdiscovery jobを補充したら、同じrunで再び探索へ進む。固定件数・固定バッチ数は設けない。
12. GitHubへの反映を完了できなくても、完全payloadをNotionまたはLibraryへ耐久保存できた時点で同じrunの後続jobへ進む。元jobはGitHub上では未完了のまま残し、後のrunで再投入する。
13. 次回へ残してよいのは、全文取得不能、GitHub read不能、未解決依存、3つの保存先のいずれにも成果を保持できない場合、または実行上限で継続不能になった分だけとする。

## GitHub反映保留時

GitHub側でwriteを完了できない場合は、最新状態を取り直して対象単位を1回再試行する。それでも反映できなければ、再投入に必要な完全logical payloadをNotion一時配送キューへ `pending` 保存する。Notionへ保存できない場合はprivate設定のChatGPT Library一時配送キューへ保存する。

一時配送キューへの保存はjob完了ではない。次回以降、最新queue/identityと再照合して適用可能なものを固定slot/inboxへ再投入し、Actions結果とqueueで成功確認後だけ `replayed` とする。適用対象外になったものは理由を残して `dead_letter` とする。

GitHub Actions内の最終反映が保留になった場合は入力自体がGitHubへ届いているため外部キューへ重複保存せず、Actions側の再処理を優先する。

GitHub read自体ができず最新queue・identityを確認できない場合は、新しいrepo依存jobへ着手しない。

詳細は [queue-v10.md](queue-v10.md)。GitHub connector / scheduled taskの制約根拠は [references/github-connector-reliability.md](references/github-connector-reliability.md) に固定リンクで記録する。

## 08:30 JST

08:30だけは論文queueを処理せず、[worker-router.md](worker-router.md) のその他更新workerに従う。フレームワーク／新規LLM更新は既存の固定 `update-payload.json` + `update-inbox.json` を使う。GitHubへの反映を完了できない場合だけ同じ一時配送キューへlogical payloadを保存し、後続runで再投入する。
