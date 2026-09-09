# Chat worker router — workflow v10

予定されたChat workerは**1つだけ**。実行時刻で次のどちらか一方を選び、同じ枠で両方を処理しない。

- **08:30 JST** → その他更新worker
- **それ以外の毎時 :30** → 論文worker

毎回default branch最新HEADを取得し、このrouterと [queue-v10.md](queue-v10.md) を同じHEADから読む。

## 実行前の共通回復

GitHub writeが利用可能な場合、外部設定されたNotion退避キューの `pending` を確認する。現在のqueue/identity/対象blobと整合する成果だけを、新規作業より先にGitHubへ再投入する。再投入中は `replaying`、Actionsの成功確認後のみ `replayed` とする。すでにterminal/supersededで安全に適用できないものは盲目的に反映せず `dead_letter` とし理由を残す。

GitHub readができない場合は、repo状態に依存する新規処理を開始しない。

## A. 論文worker

正本: [README.md](README.md)、[queue-v10.md](queue-v10.md)、`.survey/work-queue/next-jobs.json`。

Chatは探索・全文精読・科学的判断・監査判断と**構造化research record**作成を担当する。完成Markdownは作成・送信しない。research/auditはqueue-v10で定義されたA/B固定record bankのうち安全に使える1 bankの5 JSON slotを使い、全slot成功後のみ固定 `chat-inbox.json` をtriggerする。通常はA、Aに別jobの途中保存が残る場合だけBを使う。paper/state/README/identity/queueをChatから直接編集しない。

Discovery / blocked / deferred / rejectedは長文artifact不要なので、固定inboxだけを小さくupdateしてよい。

## B. その他更新worker（08:30専用）

対象は以下だけ。

1. `framework-updates/**` — LLM推論・serving・runtime等の本質的更新
2. `llm-releases/**` — 新規LLMの正式公開・一般提供・主要更新

論文queueには触れない。Chatは対象ファイルを直接編集せず、既存の固定 `.survey/update-worker/update-payload.json` と `.survey/update-worker/update-inbox.json` だけを使い、Actionsへ反映を委譲する。既存ファイルは現在blob SHA付きcompact editを優先する。

## GitHub connector障害

書き込みが403/permission denied、write tool unavailable、安全検査、接続障害、またはSHA再取得後の再試行でも失敗した場合、成果を完了扱いにしない。論理payloadを外部設定されたNotion退避キューへ `pending` として保存し、次回以降のworkerが復旧後に再投入する。

NotionはGitHubの代替正本ではない。GitHub Actions内のpush失敗はGitHub入力済みなのでNotionへ重複退避しない。

単一失敗を理由に予定タスク自身を停止・無効化・再作成しない。
