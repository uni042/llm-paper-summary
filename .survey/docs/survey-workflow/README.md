# 研究サーベイ運用入口

Scheduled Chat / Work のワーカー（worker）が実行判断のために読む**唯一の人間向け正本**は [`worker-router.md`](worker-router.md) です。

## ワーカーが読むもの

各runの開始時は最新 `main` と同じHEADの `worker-router.md` を最初に読み、モード分岐（routing）、読解・探索、保存、継続・停止、最終化を同書だけから決めます。

ライブ状態や品質テンプレートは**手順書ではなく入力データ**です。`worker-router.md` が必要とする場面でだけ参照します。

- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`
- 必要な場合だけ `.survey/work-queue/state.json`
- 論文レコード作成時だけ `.survey/templates/paper.md`

正規スクリプトが `[WORKER-GUIDE]`、`next_action`、`recovery_steps` を返した場合は、その復帰手順に従います。別文書や旧経路を探して迂回しません。

## 実装資料の扱い

`continuation-policy.json`、`queue-v10.md`、Library・監査・転送関連文書は、スクリプト、GitHub Actions、保守作業のための**実装リファレンス（implementation reference）**です。通常ワーカーは、それらを独立した手順として再解釈したり、複数文書を合成して別ルートを作ったりしません。

履歴互換処理が内部実装に残っていても、新規処理で選択できる経路ではありません。新規書込み・復旧・終了判断は `worker-router.md` と正規スクリプトが示す現行経路だけを使います。
