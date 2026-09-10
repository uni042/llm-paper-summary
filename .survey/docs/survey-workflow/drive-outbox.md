# Google Drive outbox

Google DriveはGitHubへ直接反映できないtransport payloadを一時的に耐久保存するoutboxである。研究・paper・queueの正本ではない。fallback全体の選択・切替・ChatGPT Libraryとの役割分担は [fallback-routing.md](fallback-routing.md) を正本とする。

## Drive folders

- root: `llm-paper-summary-outbox`
  - folder id: `1hd5ZDVgGbsecfOlmj68QczVu3xuQUG16`
- pending
  - folder id: `1zrP-RoQFa1-ElGsYKps5FwXkWXkkoe_k`
- processed
  - folder id: `1iH73yBkcdK8bm12eGUIa4g-tixs_s8B2`
- failed
  - folder id: `1L-BFienHytuHMj5jvV1utsZk2eThRmSf`

Scheduled Chatが書くのは`pending`だけ。Drive importerがGitHub immutable fallback intakeへの受領を確認したものだけ`processed`へ移す。不正payloadは`failed`へ隔離する。

保存先:

`/Google Drive/llm-paper-summary-outbox/pending/<unique-id>.json`

## envelope schema v1

DriveとChatGPT Libraryは同じ`schema_version: 1` envelopeを使う。`writes`には後でGitHubへ再投入する完全な固定transport JSONを含める。

```json
{
  "schema_version": 1,
  "id": "20260910T130000JST-research-2609.12345-attempt-x",
  "kind": "research",
  "job_id": "job-research-...",
  "attempt_id": "attempt-x",
  "depends_on_job_ids": ["job-research-..."],
  "writes": [
    {"path": ".survey/work-queue/records/chat-record/metadata.json", "content": "{...}\n"},
    {"path": ".survey/work-queue/submissions/chat-inbox.json", "content": "{...}\n"}
  ]
}
```

research/auditは5 record slot + `chat-inbox.json`を1論文1 envelopeへまとめる。完成MarkdownはDriveへ置かない。

## 許可されるGitHub path

record bankは `.survey/work-queue/records/bank-registry.json` に定義されたA〜Hだけを許可し、各bankでは5 slot JSONだけを許可する。加えて次の固定transport領域を許可する。

- `.survey/work-queue/submissions/*.json`
- `.survey/work-queue/transport/*.json`
- `.survey/update-worker/*.json`

`papers/**`、README、queue state、workflow、scriptなどをDrive payloadから直接更新しない。

## fallback procedure

1. GitHub write失敗時は`worker-router.md`と`continuation-policy.json`でfailure scopeを判定する。
2. `target_or_payload_specific`なら影響payloadだけfallbackへ保存して他のGitHub writeを続けてよい。
3. `run_wide_github_write_unavailable`ならそのrunでは以後GitHub writeを繰り返さず、完成payloadをDriveへ積み続ける。
4. Drive保存が失敗したらrun全体を止めず、`fallback-routing.md`に従ってChatGPT Libraryへ切り替える。
5. Drive pending件数はrun停止理由にしない。

## offline job seed

GitHub write不能中にactionable readyが尽きてもDriveが書けるなら新規discoveryを継続する。候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` に格納し、そのファイルを書き込むenvelopeをpendingへ保存する。

seedを耐久保存した後は、`fallback-routing.md`の決定論的job IDを使って候補を同じrunで全文精読してよい。完成research payloadもDriveへ複数件積める。

## Drive Importer v4

`.github/workflows/drive-outbox-import.yml` は `.survey/scripts/import_drive_outbox_v4.py` を使う。

Importerは固定record bankや`chat-inbox.json`へ直接展開しない。1 runにつき最大1 logical envelopeを次へ受け入れる。

`.survey/work-queue/fallback-inbox/<envelope-id>.json`

手順:

1. oldest-firstでDrive pendingを走査する。
2. schema、size、path allowlist、内部JSON、research bundle完全性を検証する。
3. 不正payloadはDrive `failed`へ隔離し、後続を止めない。
4. 同じ`id`がGitHub fallback-inbox/archiveにあり内容も同一なら、GitHubへ再writeせず重複copyとしてacknowledgeする。
5. 同じ`id`で内容が異なる場合はID衝突としてfailedにする。
6. 新規payloadならimmutable fallback-inbox fileを1件作ってcommit/pushする。
7. GitHub intake成功後だけDriveファイルを`processed`へ移す。
8. survey-helperが共通concurrency group内で `.survey/scripts/dispatch_fallback_inbox.py` を実行し、eligible envelopeを1件ずつ通常transportへ展開する。

この二段階化により、DriveとChatGPT Libraryが同時に復旧しても両者は固定bank/inboxを直接競合しない。

## GitHub secret setup

ActionsからDrive APIを読むため、repository secretとして次を設定する。

- `GOOGLE_SERVICE_ACCOUNT_JSON`: Google service account key JSON全文

そのservice accountにDrive root `llm-paper-summary-outbox` の編集権限を付与する。既存のDrive/Sheets用service accountを再利用してよい。

secretが未設定の間、workflowは成功扱いでidleになり、Drive payloadを消費しない。secret設定後の次回scheduleまたは手動実行から回収を開始する。

## 完了状態の意味

Drive `processed` は**GitHub immutable intakeへの受領済み**を意味する。paper publication完了ではない。publication完了はActions resultと最新queueで判定する。
