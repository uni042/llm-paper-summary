# 研究サーベイ運用手順

現在の正本は **workflow v9（queue-based）**。通常運用はこのファイルと [queue-v9.md](queue-v9.md) だけを読む。

## 役割分担

- **Chat研究worker**: 一次資料の検索・取得、全文精読、科学的判断、正式監査、完成Markdown作成。
- **GitHub Actions worker**: submission検証、論文本体への反映、job/state遷移、identity delta、集約view更新、次job生成。
- Notionは使わない。正本はこのGitHub repository。
- 固定の日次件数、cycle、run、10本/11本、日次targetは使わない。

## 1回のChat worker

1. default branchの最新HEADを取得する。
2. **同じHEAD** のこのREADME、[queue-v9.md](queue-v9.md)、`.survey/work-queue/next-jobs.json` を読む。
3. ready jobがあればpriority順に処理する。安全にsubmission保存まで完走できる範囲なら複数件処理してよい。
4. research/auditの完成Markdownは、原則として新規の `.survey/work-queue/payloads/<unique>.md` に保存する。
5. 続けて小さい `.survey/work-queue/submissions/<unique>.json` を新規作成し、`payload_path` からpayloadを参照する。
6. submissionのpushで `Survey helper worker` が自動起動する。ChatからActionsを直接起動しない。
7. Actionsはsubmission処理後にready queueを確認し、**0件なら同じActions実行内でdiscovery jobを1件補充する**。
8. ChatはActions反映後の最新HEADとqueueを読み直し、生成済みの次jobをそのまま処理する。通常は `request_jobs` を作らない。
9. 1件終わるたび最新queueを確認して次へ進む。次成果を安全に保存できない見込みなら着手せず終了する。
10. 次回も必ず最新HEADからqueueを読み直す。同じsubmissionを再送しない。

## transport

通常経路は **payload → submission → push-triggered Actions**。

```
Chat
  ├─ research/audit → payloads/<unique>.md
  └─ submissions/<unique>.json
                         │ push
                         ▼
                 Survey helper worker
                         │
       ┌─────────────────┼─────────────────┐
       ▼                 ▼                 ▼
   paper反映          job/state更新      next-jobs生成
                            │
                    ready=0なら即discovery補充
```

GitHubの10分scheduleは未処理submission回収とqueue保守の**保険**。通常処理の成立条件ではない。

## queue policy

判断基準は以下だけにする。

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

詳細なsubmission schema、冪等性、状態遷移は [queue-v9.md](queue-v9.md) を正本とする。

## legacy

workflow v8以前の文書、state、request/result、cycle/run helperは履歴・復旧資料。過去の `request_jobs` submissionも互換用途だけで、新しい通常フローでは使わない。
