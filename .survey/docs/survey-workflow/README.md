# 研究サーベイ運用入口

Scheduled Chat / Workのワーカーが実行判断のために読む**唯一の人間向け正本**は [`worker-router.md`](worker-router.md) です。

## 現行運用

現行はLibrary-firstです。

- `LLM論文ワーカー :00` / `:30` はGitHub `main` をread-onlyで参照し、探索・読解・分類の完成成果をChatGPT Libraryへ保存します。
- GitHubへの反映はSurvey GitHub ImportのWorkタスクが担当します。
- Scheduled workerはGitHubのclaim / reservation / submission / control-file等を書きません。
- WorkタスクはLibrary成果を最新mainへ正規化して反映し、GitHubから再取得して確認できた後だけ対応Library原本を整理します。
- モード判定はLibrary未反映分を補正した `E = G + D - R` を使い、`E > 500` ならResearch、`E <= 500` ならDiscoveryです。
- Researchは10件、Discoveryは新規canonical identity 40件を現在の標準ノルマとします。

Library側の詳細HOWは `/LLM-paper-summary-library-first/WORKER-LIBRARY-PROCEDURES.md` とSurvey GitHub Import用 `github-import-procedure.md` を読みます。本書とLibrary手順が矛盾する場合は最新mainの `worker-router.md` を優先し、Library側手順を後で整合させます。

## ワーカーが読むGitHub側入力

各runの開始時は最新`main`と同じHEADの`worker-router.md`を最初に読みます。ライブ状態や品質テンプレートは**手順書ではなく入力データ**です。

- `.survey/work-queue/worker-worklist-00.json` / `WORKLIST-00.md`
- `.survey/work-queue/worker-worklist-30.json` / `WORKLIST-30.md`
- 必要な対象系統README
- 論文レコード作成時だけ `.survey/templates/paper.md`

候補は各workerの専用worklistの**末尾から上方向**へ処理します。

## 保守資料の扱い

通常ワーカーが読むGitHub側の手順正本は`worker-router.md`だけです。`.survey/scripts/**`、`.github/workflows/**`、`.survey/tests/**` は実装・回帰検証用であり、Scheduled workerが旧direct-write経路を復活させる根拠にはしません。

旧direct-GitHub worker手順は [`worker-router-legacy-v10.22-direct-github.md`](worker-router-legacy-v10.22-direct-github.md) に退避済みです。履歴データや旧コードの意味確認にだけ使い、現行runの手順として参照しません。

`library-checkpoint-registry.md`、`library-publication-ack.md`、`library-superseded-cleanup.md` 等の旧outbox/checkpoint資料は、過去`/LLM-survey-outbox/`成果をWorkタスクが回収する際の互換・保守資料です。新規Scheduled workerの保存先・transport正本ではありません。
