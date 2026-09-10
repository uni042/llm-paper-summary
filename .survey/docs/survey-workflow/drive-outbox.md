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

Scheduled Chatが書くのは`pending`だけ。Drive ImporterがGitHubへの投入に成功したものだけ`processed`へ移す。不正payloadは`failed`へ隔離する。

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
2. `target_or_payload_specific`なら影響payloadだけDriveへ保存して他のGitHub writeを続けてよい。
3. `run_wide_github_write_unavailable`ならそのrunでは以後GitHub writeを繰り返さず、完成payloadをDriveへ積み続ける。
4. Drive保存が失敗したらrun全体を止めず、`fallback-routing.md`に従ってChatGPT Libraryへ切り替える。
5. Drive pending件数はrun停止理由にしない。

## offline job seed

GitHub write不能中に実行可能readyが尽きても、Driveが書けるなら新規discoveryを継続する。候補0〜5件を `.survey/work-queue/transport/offline-job-seed.json` に格納し、そのファイルを書き込むenvelopeをpendingへ保存する。

seedを耐久保存した後は、`fallback-routing.md`の決定論的job IDを使って候補を同じrunで全文精読してよい。完成research payloadもDriveへ複数件積める。

## Drive Importer v3

`.github/workflows/drive-outbox-import.yml`は `.survey/scripts/import_drive_outbox_v3.py` を使い、1 runにつき最大1 logical envelopeをGitHubへ投入する。

1. oldest-firstでpendingを走査する。
2. 不正payloadは`failed`へ隔離し、後続を止めない。
3. Chat transportがbusyならresearch/auditをpendingに残す。
4. research/auditの対応jobがGitHubにまだ存在しない場合は`deferred_dependency`としてpendingに残し、failedへ送らない。
5. dependency待ちresearchの後ろにoffline seedや独立update payloadがあれば先に処理してよい。
6. eligible envelopeを1件だけ適用し、許可領域だけcommit/pushする。
7. push成功後だけそのDriveファイルを`processed`へ移す。
8. offline seedが反映されると`survey-helper.yml`が `.survey/scripts/apply_offline_job_seed.py` を実行し、決定論的research jobをGitHubへ実体化する。
9. 後続Importer runで対応research envelopeがeligibleになる。

この直列化と依存チェックにより、Driveに複数論文や複数seedが溜まっても固定bank/inboxを競合させず回復できる。

## Importer設定

Drive Importerが未設定の間はworkflowはidleになるが、Chatからpendingへ保存できるならその保存は有効な耐久checkpointである。Importer設定が有効になった後のscheduleまたは手動実行からbacklogを順次排出する。

Drive pendingはDrive ImporterだけがGitHubへ再投入する。Scheduled ChatはDrive payloadを手動で二重投入しない。Library pendingだけをScheduled Chatが再投入する。
