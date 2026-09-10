# Google Drive outbox fallback

GitHubへ完成済みの再送可能transport payloadを直接反映できない場合、そのlogical payloadをGoogle Driveへ耐久退避し、GitHub Actionsが後から回収する。Driveは配送待ちキューであり、研究正本・論文正本ではない。

GitHub write失敗時は `worker-router.md` のhealth probeで `target_or_payload_specific` と `run_wide_github_write_unavailable` を切り分ける。前者なら影響を受けたjobだけをDriveへ退避して他のGitHub writeは継続できる。後者ならそのrunでは以後GitHub writeを繰り返さず、完成した後続成果もDriveへ積みながら研究を続ける。

未送信論文やDrive pendingが増えたこと自体はrun停止理由にしない。詳細は [backlog-resilience.md](backlog-resilience.md) を正本とする。

## Drive folders

- root: `llm-paper-summary-outbox`
  - folder id: `1hd5ZDVgGbsecfOlmj68QczVu3xuQUG16`
- pending
  - folder id: `1zrP-RoQFa1-ElGsYKps5FwXkWXkkoe_k`
- processed
  - folder id: `1iH73yBkcdK8bm12eGUIa4g-tixs_s8B2`
- failed
  - folder id: `1L-BFienHytuHMj5jvV1utsZk2eThRmSf`

Chat workerが書くのは `pending` だけ。ActionsがGitHub transportへ正常投入できたものを `processed` へ移す。不正JSON、許可外path、破損payloadは `failed` へ移す。

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
      "path": ".survey/work-queue/records/chat-record/metadata.json",
      "content": "{\n  \"...\": \"...\"\n}\n"
    },
    {
      "path": ".survey/work-queue/submissions/chat-inbox.json",
      "content": "{\n  \"...\": \"...\"\n}\n"
    }
  ]
}
```

`content` はJSON文字列であり、その中身自体も有効なJSONでなければならない。research/auditでは5つのrecord slotと、全slotを参照する `chat-inbox.json` を**同一envelope**へまとめる。1論文を複数Drive envelopeへ分割しない。これにより、Drive上で一部slotだけ保存された状態を完成扱いしない。

## 許可されるGitHub path

Drive importerは任意ファイルを書けない。record bankは `.survey/work-queue/records/bank-registry.json` に定義されたA〜Hだけを許可し、その各bankでは次の5ファイルだけを許可する。

- `metadata.json`
- `problem_method.json`
- `evaluation.json`
- `results.json`
- `positioning.json`

これに加えて次の固定transport領域を許可する。

- `.survey/work-queue/submissions/*.json`
- `.survey/work-queue/transport/*.json`
- `.survey/update-worker/*.json`

`papers/**`、README、queue state、workflow、scriptなどをDrive payloadから直接更新してはならない。論文本文やstate変更は既存のActions workerへ委譲する。

research/auditのDrive envelopeでは通常のGitHub transportと同じ5 slot + inboxを使う。Driveだから別形式の研究recordを作ったり、完成Markdownを保存したりしない。

## Chat worker fallback procedure

1. GitHub write失敗時は `worker-router.md` のhealth probe手順でfailure scopeを判定する。
2. `target_or_payload_specific` の場合は、そのjobの完全logical payloadをDriveへ保存し、そのjobだけを未完了のまま残す。他の独立GitHub write/jobは継続してよい。
3. `run_wide_github_write_unavailable` の場合は、そのrunでは以後GitHub writeを試さない。既に完成した成果と、その後に完成する成果をDriveへ直接積む。
4. research/auditでは5 record slot + inboxを1 envelopeにまとめる。envelopeはUTF-8の `.json` としてDrive `pending` に保存する。
5. Driveへの保存成功をGitHub publication成功とは扱わない。GitHub上のjobは未完了のままにする。
6. **保存後は次の独立ready jobへ進む。** Drive pending数、未送信論文数、bank使用数だけを理由にStop Gateへ直行しない。
7. 次run開始時、GitHub readが可能なら通常queueを読む。Drive側の再投入はActionsに任せ、Chatが同じpayloadをGitHubへ手動二重投入しない。
8. A〜Hがすべてdirty/使用中に見えてもDriveが書けるなら、bank exhaustionを停止理由にせず、新しい完成payloadもDriveへ耐久保存して研究を続ける。

## GitHub Actions: backlog-safe drain

`.github/workflows/drive-outbox-import.yml` が10分おきに `pending` を確認する。

複数pendingを同時に固定bank/inboxへ展開すると上書き衝突が起こるため、Importerは次の規則で**1 runにつき最大1 logical envelope**だけをGitHubへ投入する。

1. 現在の `.survey/work-queue/submissions/chat-inbox.json` と `.survey/work-queue/results/chat-inbox.json` を確認する。
2. 現在inboxの `job_id` に対応するresultがまだ無ければ、research/audit envelopeは投入せずpendingのまま待つ。前payloadを上書きしない。
3. oldest-firstでpendingを検査する。不正payloadは `failed` へ隔離し、後続の正常payloadを飢餓させない。
4. busyなresearch envelopeはpendingに残すが、独立したframework/model-update envelopeが後ろにあればそれを処理してよい。
5. eligibleなenvelopeを1件だけ取得し、schema、サイズ、path allowlist、内部JSON、research bundleの5-slot完全性を検証する。
6. transport JSONをworking treeへ適用し、許可領域だけをstageしてmainへcommit/pushする。
7. push成功後にそのDriveファイルだけを `processed` へ移動する。
8. `chat-inbox.json` へのpushにより `survey-helper.yml` が起動し、record検証、renderer、queue処理、品質検査を行う。
9. 次回Importerは前inboxに対応するresultが確認できてから次のresearch envelopeへ進む。

この直列化により、Drive側では複数論文が同じ再利用bankを参照していても、複数payloadが同時上書きされない。

push前に失敗した場合は `processed` へ移動しないため、次回再試行できる。内容がすでにGitHubと同一なら変更なしとして扱い、そのenvelopeも安全にacknowledgeできる。

## GitHub secret setup

ActionsからDrive APIを読むため、repository secretとして次を1つ設定する。

- `GOOGLE_SERVICE_ACCOUNT_JSON`: Google service account key JSON全文

そのservice accountにDrive root `llm-paper-summary-outbox` の編集権限を付与する。既存のDrive/Sheets用service accountを再利用してよい。

このsecretが未設定の間、workflowは成功扱いでidleになり、Drive payloadを消費しない。secret設定後の次回scheduleまたは手動実行から回収を開始する。

## 運用上の正本

Google Driveは配送用outboxであり正本ではない。正本は引き続きGitHub mainと `.survey/work-queue/**`。`processed` は監査・障害解析用に当面残す。
