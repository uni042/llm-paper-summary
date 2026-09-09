# 研究サーベイ運用手順

現在の正本は **workflow v10（structured-record transport + queue）**。予定されたChat workerは、毎回default branchの最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、`.survey/work-queue/next-jobs.json` を読む。

## 設計原則

- **Chat研究worker**: 一次資料の検索・取得、全文精読、科学的判断、正式監査、構造化research record作成。
- **GitHub Actions worker**: record検証、Markdownレンダリング、paper反映、job/state遷移、identity delta、派生view更新、次job生成。
- GitHub repositoryを唯一の正本とする。
- NotionはGitHub書き込み不能時だけ使う**一時配送キュー**であり、研究正本・paper正本・queue正本にはしない。
- 固定の日次件数、旧cycle/run、10本/11本、固定research/audit比率は使わない。
- 予約済みworkerは1つのまま維持し、08:30 JSTだけその他更新、それ以外の毎時:30は論文workerを選ぶ。

## v10で変わった点

v9では完成Markdownを複数chunkへ分割してGitHubへ送っていた。v10では**完成MarkdownをChatからGitHubへ送らない**。research/auditの内容を5つの小さいJSON record slotへ分割し、GitHub Actions内の `.survey/scripts/render_paper.py` が最終Markdownを生成する。

固定slot:

1. `.survey/work-queue/records/chat-record/metadata.json`
2. `.survey/work-queue/records/chat-record/problem_method.json`
3. `.survey/work-queue/records/chat-record/evaluation.json`
4. `.survey/work-queue/records/chat-record/results.json`
5. `.survey/work-queue/records/chat-record/positioning.json`

すべてのslot保存に成功した後だけ `.survey/work-queue/submissions/chat-inbox.json` を更新する。各slotは直前fetchしたblob SHAで既存ファイルをupdateし、manifestには保存後のblob SHAを入れる。Actionsは5 slotのpath・順序・サイズ・SHA・attempt_id・job_idを検証してからMarkdownを生成する。

```text
Scheduled Chat worker
      │
      ├─ metadata.json
      ├─ problem_method.json
      ├─ evaluation.json
      ├─ results.json
      └─ positioning.json
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

1. 最新HEADのrouter、queue-v10、next-jobsを読む。
2. GitHub writeが利用可能なら、まずNotion退避キューの `pending` を確認し、現在queueと整合する未反映成果があれば新規jobより先に再投入する。
3. ready jobをpriority順に処理する。research着手前とdiscovery候補提出前にidentity正本で重複確認する。
4. research/auditは一次資料全文を読み、5 slot用の構造化recordを作る。抄録や検索断片から欠落を推測しない。
5. 固定slotを順番に小さくupdateする。途中失敗なら成功済みslotを保持し、失敗slotだけ安全に1回再試行する。
6. 全slot成功後だけinboxをupdateする。
7. `chat-inbox.json` のpush時に旧resultがresetされ、その後生成された `.survey/work-queue/results/chat-inbox.json` が同一 `job_id` で `ok: true`、かつ最新queueでjob完了になるまで完了扱いにしない。
8. 1件完了ごとに最新queueを読み直し、安全に保存完了できる範囲で次jobへ進む。

## GitHub write障害時

GitHub readはできるがconnector writeが403、write tool unavailable、安全検査、または再取得後もwriteに失敗する場合、完成済みの論理payloadをNotionの退避キューへ保存して `pending` とする。**Notionへ保存できたことをjob完了とは扱わない。** 次回以降のworkerがGitHub write復旧を確認したら、pending成果を現在queue/identityと再照合して固定slot/inboxへ再投入し、Actions結果確認後にNotion側を `replayed` にする。

GitHub Actions内の最終 `git push` だけが失敗した場合は、入力自体はすでにGitHubへ届いているためNotionへ二重退避しない。10分schedule/再実行でActions側の回復を優先する。

GitHub read自体ができず最新queue・identityを確認できない場合は、新しいrepo依存jobへ着手しない。

詳細は [queue-v10.md](queue-v10.md)。GitHub connector / scheduled taskの制約根拠は [references/github-connector-reliability.md](references/github-connector-reliability.md) に固定リンクで記録する。

## 08:30 JST

08:30だけは論文queueを処理せず、[worker-router.md](worker-router.md) のその他更新workerに従う。フレームワーク／新規LLM更新のGitHub transportは既存の固定 `update-payload.json` + `update-inbox.json` を維持する。GitHub connector writeが使えない場合のみ同じNotion退避キューへ論理payloadを保存し、復旧後に再投入する。
