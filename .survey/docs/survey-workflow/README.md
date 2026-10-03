# 研究サーベイ運用入口

Scheduled Chat / Workのワーカーが実行判断のために読む**唯一の人間向け正本**は [`worker-router.md`](worker-router.md) です。

## 現行運用

現行はLibrary-firstです。

- `LLM論文ワーカー :00` / `:30` / `:45` はGitHub `main` をread-onlyで参照し、探索・読解・分類の完成成果をChatGPT Libraryへ保存します。
- GitHubへの反映はSurvey GitHub ImportのWorkタスクが担当します。
- Scheduled workerはGitHubのclaim / reservation / submission / control-file等を書きません。
- Survey GitHub ImportはLibrary成果をGitHub受信箱へbyte-preservingで転送し、GitHub側が同一bytesまたは同一source SHAを耐久保持したことを確認できた後だけ対応Library原本を整理します。
- モード判定は同じ最新main HEADの `STATUS.md` にある `収録候補論文数` を使い、`収録候補論文数 > 600` ならResearch、`収録候補論文数 <= 600` ならDiscoveryです。Library未転送成果を足し引きして別の実効値を再計算しません。
- Researchは完成Markdown 5件、Discoveryは本文確認済みの新規canonical identity 10件を現在の標準ノルマとします。

Library側の詳細HOWは `/LLM-paper-summary-library-first/WORKER-LIBRARY-PROCEDURES.md` とSurvey GitHub Import用 `github-import-procedure.md` を読みます。本書とLibrary手順が矛盾する場合は最新mainの `worker-router.md` を優先し、Library側手順を後で整合させます。

## ワーカーが読むGitHub側入力

各runの開始時は最新`main`と同じHEADの`worker-router.md`を最初に読みます。ライブ状態や品質テンプレートは**手順書ではなく入力データ**です。

- `.survey/work-queue/worker-worklist-00.json` / `WORKLIST-00.md`
- `.survey/work-queue/worker-worklist-30.json` / `WORKLIST-30.md`
- `.survey/work-queue/worker-worklist-45.json` / `WORKLIST-45.md`
- 必要な対象系統README
- 論文レコード作成時だけ `.survey/templates/paper.md`

候補は各workerの専用worklistの**末尾から上方向**へ処理します。

## 保守資料の扱い

通常ワーカーが読むGitHub側の手順正本は`worker-router.md`だけです。`.survey/scripts/**`、`.github/workflows/**`、`.survey/tests/**` は実装・回帰検証用であり、Scheduled workerが旧direct-write経路を復活させる根拠にはしません。

旧direct-GitHub worker手順は [`worker-router-legacy-v10.22-direct-github.md`](worker-router-legacy-v10.22-direct-github.md) に退避済みです。履歴データや旧コードの意味確認にだけ使い、現行runの手順として参照しません。

`library-checkpoint-registry.md`、`library-publication-ack.md`、`library-superseded-cleanup.md` 等の旧outbox/checkpoint資料は、過去`/LLM-survey-outbox/`成果をWorkタスクが回収する際の互換・保守資料です。新規Scheduled workerの保存先・transport正本ではありません。
