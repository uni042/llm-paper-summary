# 研究サーベイ運用手順

現在の正本は **workflow v10（structured-record transport + queue）**。予定されたChat workerは、毎回default branchの最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、`.survey/work-queue/next-jobs.json` を読む。

## 設計原則

- **Chat研究worker**: 一次資料の検索・取得、全文精読、科学的判断、正式監査、構造化research record作成。
- **GitHub Actions worker**: record検証、Markdownレンダリング、paper反映、job/state遷移、identity delta、派生view更新、次job生成。
- GitHub repositoryを唯一の正本とする。
- NotionはGitHub書き込み不能時だけ使う**一時配送キュー**であり、研究正本・paper正本・queue正本にはしない。
- 固定の日次件数、旧cycle/run、10本/11本、固定research/audit比率は使わない。
- 予約済みworkerは1つのまま維持し、08:30 JSTだけその他更新、それ以外の毎時:30は論文workerを選ぶ。
- 論文workerは**探索だけで終了せず、探索した候補の全文精読・保存まで同一runで連続処理する**。queueが再び空になって新しいdiscovery jobが補充された場合も処理を続け、プラットフォーム上限または実処理上の阻害要因に当たるまで繰り返す。
- 論文本文の品質正本は [paper template](../../templates/paper.md) とする。**論文を読んでいない読者でも背景、手法、処理の流れ、なぜ効くか、効かない条件まで追える文章**を生成する。
- 説明密度のお手本は [MoE-Infinity のまとめ](../../../papers/inference/01-offload-hierarchical-memory/2024-2401.14361-moe-infinity-efficient-moe-inference-on-personal-machines-with-sparsity-aware-ex.md) とする。論文固有の略語や狭い分野の語を、それ自体を知っている前提で使わない。

## v10で変わった点

v9では完成Markdownを複数chunkへ分割してGitHubへ送っていた。v10では**完成MarkdownをChatからGitHubへ送らない**。research/auditの内容を5つの小さいJSON record slotへ分割し、GitHub Actions内の `.survey/scripts/render_paper.py` が最終Markdownを生成する。

固定slotはA/Bの2 bankを事前作成する。通常はbank A（`.survey/work-queue/records/chat-record/`）を使い、別jobの途中保存がAに残っていて上書きできない場合だけbank B（`.survey/work-queue/records/chat-record-b/`）を使う。各bankは `metadata.json` / `problem_method.json` / `evaluation.json` / `results.json` / `positioning.json` の5 slotを持つ。

**構造化recordは圧縮した研究メモではなく、Markdownへほぼそのまま変換される本文原稿である。** 特に `problem_method` は方式名・略語・数式の列挙で済ませず、各機構について入力、観測する状態、具体的な処理、出力、次の処理との接続、改善するボトルネック、失敗時や境界条件まで文章で書く。

選択したbankのすべてのslot保存に成功した後だけ `.survey/work-queue/submissions/chat-inbox.json` を更新する。各slotは直前fetchしたblob SHAで既存ファイルをupdateし、manifestには保存後のblob SHAを入れる。Actionsは5 slotのpath・順序・サイズ・SHA・attempt_id・job_idを検証してからMarkdownを生成する。

```text
Scheduled Chat worker
      │
      ├─ bank A または B
      │   ├─ metadata.json
      │   ├─ problem_method.json
      │   ├─ evaluation.json
      │   ├─ results.json
      │   └─ positioning.json
              │ 全5件成功後
              ▼
         chat-inbox.json
              │ push
              ▼
        Survey helper worker
              │
       record SHA/schema検証
              │
       render_paper.py
              │ runner内のみ
              ▼
       transient Markdown
              │
       stable queue worker
       ┌──────┼─────────┐
       ▼      ▼         ▼
     paper   state    next-jobs
```

旧 `part-01.md`〜`part-08.md` と `assemble_chat_chunks.py` は復旧互換用として残すが、予定タスクの通常経路では使わない。

## 1回の論文worker

1. 最新HEADのrouter、queue-v10、next-jobs、paper templateを読む。新しい会話・新しい実行環境ではMoE-Infinityのお手本も確認する。
2. GitHub writeが利用可能なら、まずNotion退避キューの `pending` を確認し、現在queueと整合する未反映成果があれば新規jobより先に再投入する。
3. ready research/auditがあればpriority順に処理する。research着手前とdiscovery候補提出前にidentity正本で重複確認する。
4. readyがdiscoveryなら探索を実行し、候補を固定inboxへ保存する。**discovery送信だけでrunを終了しない。** Actions反映後の最新queueを読み直し、生成されたresearch jobへ直ちに進む。
5. research/auditは一次資料全文を読み、選択したbankの5 slot用の構造化recordを作る。抄録や検索断片から欠落を推測しない。複雑な手法は、背景→全体像→主要機構→データ／制御の流れ→なぜ効くか→失敗・境界条件の順で説明し、数段落の研究メモに圧縮しない。
6. 評価は数値を並べるだけでなく、比較対象と条件を明示し、その数値が出る理由、別条件で利得が消える理由、実機かシミュレーションかを説明する。
7. 固定slotを順番に小さくupdateする。途中失敗なら成功済みslotを保持し、失敗slotだけ安全に1回再試行する。
8. 全slot成功後だけinboxをupdateする。
9. `chat-inbox.json` のpush時に旧resultがresetされ、その後生成された `.survey/work-queue/results/chat-inbox.json` が同一 `job_id` で `ok: true`、かつ最新queueでjob完了になるまで完了扱いにしない。
10. 1件完了ごとに最新queueを読み直す。researchからauditが生成されたら同じrunで処理する。
11. readyが0件になりActionsが次のdiscovery jobを補充したら、同じrunで再び探索へ進む。**discovery → research → 必要ならaudit → queue再取得 → 次discovery** を、実行環境が許す限り繰り返す。固定件数・固定バッチ数は設けない。
12. 次回へ残してよいのは、全文取得不能、GitHub/Notion/Libraryへの保存不能、未解決依存、または時間・実行回数・コンテキスト等のプラットフォーム上限で継続不能になった分だけとする。停止時点のqueueを次回runがそのまま引き継ぐ。

## GitHub write障害時

GitHub readはできるがconnector writeが403、write tool unavailable、安全検査、または再取得後もwriteに失敗する場合、完成済みの論理payloadをNotionの退避キューへ保存して `pending` とする。**Notionへ保存できたことをjob完了とは扱わない。** 次回以降のworkerがGitHub write復旧を確認したら、pending成果を現在queue/identityと再照合して固定slot/inboxへ再投入し、Actions結果確認後にNotion側を `replayed` にする。

GitHub Actions内の最終 `git push` だけが失敗した場合は、入力自体はすでにGitHubへ届いているためNotionへ二重退避しない。10分schedule/再実行でActions側の回復を優先する。

GitHub read自体ができず最新queue・identityを確認できない場合は、新しいrepo依存jobへ着手しない。

詳細は [queue-v10.md](queue-v10.md)。GitHub connector / scheduled taskの制約根拠は [references/github-connector-reliability.md](references/github-connector-reliability.md) に固定リンクで記録する。

## 08:30 JST

08:30だけは論文queueを処理せず、[worker-router.md](worker-router.md) のその他更新workerに従う。フレームワーク／新規LLM更新のGitHub transportは既存の固定 `update-payload.json` + `update-inbox.json` を維持する。GitHub connector writeが使えない場合のみ同じNotion退避キューへ論理payloadを保存し、復旧後に再投入する。
