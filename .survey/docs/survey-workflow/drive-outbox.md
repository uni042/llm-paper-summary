# Google Drive outbox fallback

GitHub writeがrun-wideで利用不能なときに、完成済みの再送可能transport payloadをGoogle Driveへ退避し、GitHub Actionsが後から回収する。

## Drive folders

- root: `llm-paper-summary-outbox`
  - folder id: `1hd5ZDVgGbsecfOlmj68QczVu3xuQUG16`
- pending
  - folder id: `1zrP-RoQFa1-ElGsYKps5FwXkWXkkoe_k`
- processed
  - folder id: `1iH73yBkcdK8bm12eGUIa4g-tixs_s8B2`
- failed
  - folder id: `1L-BFienHytuHMj5jvV1utsZk2eThRmSf`

Chat workerが書くのは `pending` だけ。ActionsがGitHubへ正常投入できたものを `processed` へ移す。不正JSON、許可外path、破損payloadは `failed` へ移す。

## ChatGPTからDriveへ書く経路

ChatGPTのLibraryにはGoogle Driveが `/Google Drive` としてマウントされている。workerはenvelopeをローカル一時ファイルとして生成した後、LibraryのGoogle Drive領域へuploadする。

保存先は必ず次とする。

`/Google Drive/llm-paper-summary-outbox/pending/<unique-id>.json`

Google Drive connectorで直接upload可能な実行環境では、pending folder id `1zrP-RoQFa1-ElGsYKps5FwXkWXkkoe_k` を親folderとして使ってもよい。どちらの経路でも保存されるDrive folderは同一である。

2026-09-10にChatGPTからこのpending folderへのJSON uploadを実動確認済み。テストファイルは確認後に削除した。

## envelope schema v1

Driveへは完成Markdownではなく、既存Actionsへ渡すtransport JSONを包んだenvelopeを1ファイルずつ保存する。

```json
{
  "schema_version": 1,
  "id": "20260910T090000JST-research-2609.12345",
  "writes": [
    {
      "path": ".survey/work-queue/submissions/record-a-1.json",
      "content": "{\n  \"...\": \"...\"\n}\n"
    }
  ]
}
```

`content` はJSON文字列であり、その中身自体も有効なJSONでなければならない。1つのlogical submissionが複数slotから成る場合は、同一envelopeの `writes` にまとめる。これにより部分的にDriveへ保存した状態を完成扱いしない。

## 許可されるGitHub path

Drive importerは任意ファイルを書けない。以下のJSON transport領域だけを許可する。

- `.survey/work-queue/submissions/*.json`
- `.survey/work-queue/transport/*.json`
- `.survey/update-worker/*.json`

`papers/**`、README、queue state、workflow、scriptなどをDrive payloadから直接更新してはならない。論文本文やstate変更は既存のActions workerへ委譲する。

## Chat worker fallback procedure

1. GitHub write失敗時は `worker-router.md` のhealth probe手順で `target_or_payload_specific` と `run_wide_github_write_unavailable` を切り分ける。
2. run-wide write不能の場合だけDrive outboxを使う。
3. GitHubへ本来送る予定だった固定transport JSONを、上記envelopeにそのまま格納する。
4. envelopeはUTF-8の `.json` としてDrive `pending` に保存する。
5. Driveへの保存成功をGitHub publication成功とは扱わない。GitHub上のjobは未完了のままにする。
6. 保存後は次の独立ready jobへ進む。
7. 次run開始時、GitHub readが可能なら通常queueを読み、Drive側の再投入はActionsに任せる。Chatが同じpayloadをGitHubへ手動二重投入しない。

## GitHub Actions

`.github/workflows/drive-outbox-import.yml` が10分おきに `pending` を確認する。

処理は次の順序。

1. Driveからenvelopeを取得。
2. schema、サイズ、path allowlist、内部JSONを検証。
3. transport JSONをworking treeへ適用。
4. mainへcommit/push。
5. push成功後にDriveファイルを `processed` へ移動。
6. transport pathへのpushにより既存 `survey-helper.yml` が起動し、その後のrenderer、queue処理、品質検査を担当する。

push前に失敗した場合は `processed` へ移動しないため、次回再試行できる。内容がすでにGitHubと同一なら変更なしとして扱い、そのenvelopeも安全にacknowledgeできる。

## GitHub secret setup

ActionsからDrive APIを読むため、repository secretとして次を1つ設定する。

- `GOOGLE_SERVICE_ACCOUNT_JSON`: Google service account key JSON全文

そのservice accountにDrive root `llm-paper-summary-outbox` の編集権限を付与する。既存のDrive/Sheets用service accountを再利用してよい。

このsecretが未設定の間、workflowは成功扱いでidleになり、Drive payloadを消費しない。secret設定後の次回scheduleまたは手動実行から回収を開始する。

## 運用上の正本

Google Driveは配送用outboxであり正本ではない。正本は引き続きGitHub mainと `.survey/work-queue/**`。`processed` は監査・障害解析用に当面残す。
