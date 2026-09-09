# 研究サーベイ運用手順

現在の正本は **workflow v9（queue-based）**。通常運用はこのファイルと [queue-v9.md](queue-v9.md) だけを読む。

## 役割分担

- **Chat研究worker**: 一次資料の検索・取得、全文精読、科学的判断、正式監査、完成Markdown作成。
- **GitHub Actions worker**: submission検証、分割payloadの連結、論文本体への反映、job/state遷移、identity delta、集約view更新、次job生成。
- Notionは使わない。正本はこのGitHub repository。
- 固定の日次件数、cycle、run、10本/11本、日次targetは使わない。

## 1回のChat worker

1. default branchの最新HEADを取得する。
2. **同じHEAD** のこのREADME、[queue-v9.md](queue-v9.md)、`.survey/work-queue/next-jobs.json` を読む。
3. ready jobがあればpriority順に処理する。安全にsubmission保存まで完走できる範囲なら複数件処理してよい。
4. research/auditの完成Markdownは、章・節の自然な境界で小分けし、事前作成済み `.survey/work-queue/payloads/chat-chunks/part-01.md` 〜 `part-08.md` を必要数だけ現在blob SHA付きで順番に上書きする。**完成Markdown全文を1ファイルへ丸ごと送らない。**
5. 各chunkのupdate後に返った最新blob SHAを記録する。1chunkは最大8 KiB、通常は2〜5 KiB程度を目安とする。
6. 全chunk保存成功後、小さい `.survey/work-queue/submissions/chat-inbox.json` を現在blob SHA付きで上書きし、`payload_chunks` に使用したchunk pathとblob SHAを順番に指定する。予定Chat workerは通常運用で新規ファイルを作成しない。
7. `chat-inbox.json` のpushで `Survey helper worker` が自動起動する。Actionsは各chunkのblob SHAを検証し、runner内だけで連結してqueue workerへ渡す。連結済み長文はGitHubへcommitしない。
8. Actionsはsubmission処理後にready queueを確認し、**0件なら同じActions実行内でdiscovery jobを1件補充する**。
9. ChatはActions反映後のresultと最新queueを読み直し、生成済みの次jobへ進む。通常は `request_jobs` を作らない。
10. 1件終わるたび最新queueを確認する。次成果を安全に保存できない見込みなら着手せず終了する。terminal jobを再完了しない。

## transport

通常経路は **reusable chunk slots → reusable inbox manifest → push-triggered Actions**。新規payload/submissionファイルの作成は通常運用では行わない。

```text
Chat
  ├─ update part-01.md
  ├─ update part-02.md
  ├─ ... 必要数だけ
  └─ update submissions/chat-inbox.json
                 │ push
                 ▼
          Survey helper worker
                 │
        chunk SHAを全件検証
                 │
        runner内で一時連結
                 │
       ┌─────────┼─────────┐
       ▼         ▼         ▼
   paper反映  job/state  next-jobs
                          │
                  ready=0ならdiscovery補充
```

分割は安全検査対策だけではなく、途中失敗からの回復単位でもある。例えばpart-01〜03が保存済みでpart-04だけ失敗した場合、成功済み3chunkを上書きし直さず、最新状態を確認してpart-04から再開できる。inboxを送るのは**全使用chunkが保存成功した後だけ**。

GitHubの10分scheduleは未処理submission回収とqueue保守の**保険**。通常処理の成立条件ではない。

旧 `.survey/work-queue/payloads/chat-payload.md` はActionsがrunner内で一時的に連結結果を渡す互換scratchとして残す。予定Chat workerはこのファイルを直接更新しない。旧来の一意な `.survey/work-queue/payloads/<unique>.md` + `.survey/work-queue/submissions/<unique>.json` 新規作成経路も復旧互換用であり、予定タスクでは使用しない。

## queue policy

- ready jobがある → priority順に可能な限り処理する。
- 最後のready jobをActionsが完了させて0件になる → 同じActions実行内でdiscovery jobを1件補充する。
- discoveryは有望論文を0〜5件返す。5件はノルマではない。
- research後、明確な確認事項が残った場合だけaudit jobを作る。
- 固定の探索周期、research/audit比率、backlog維持目標、固定割合監査は使わない。

## 品質原則

- 候補0件は正常。数合わせで弱い論文を追加しない。
- researchは一次資料本文を最後まで読む。全文取得不能なら抄録・検索断片から推測せずblocked/deferred。
- auditは一次資料・正式公開情報・公式実装を使って書誌、版、code、評価条件、主要値、実機/模擬、分類、差分、限界まで確認する。
- 既存paper更新では現在blob SHAを取得し、submissionに `expected_blob_sha` を付ける。
- Chatは通常処理で既存paper、`.survey/survey-state/`、queue state、identity index、README、集約viewを直接更新しない。

詳細なsubmission schema、分割payload、重複防止、冪等性、状態遷移は [queue-v9.md](queue-v9.md) を正本とする。

## legacy

workflow v8以前の文書、state、request/result、cycle/run helperは履歴・復旧資料。過去の `request_jobs` submissionも互換用途だけで、新しい通常フローでは使わない。
