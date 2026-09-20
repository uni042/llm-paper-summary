# 研究サーベイ運用入口

Scheduled Chat / Work のワーカー（worker）が実行判断のために読む**唯一の人間向け正本**は [`worker-router.md`](worker-router.md) です。

## ワーカーが読むもの

各runの開始時は、最新 `main` と同じHEADの `worker-router.md` を最初に読みます。以後の役割分岐（routing）、処理順、探索、保存、継続・停止判断は同書だけから決めます。

ライブ状態や品質テンプレートは**手順書ではなく入力データ**です。必要な場面で `worker-router.md` の指示どおり参照します。

- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`
- 必要な場合だけ `.survey/work-queue/state.json`
- 論文レコード作成時だけ `.survey/templates/paper.md`

正規スクリプトが `[WORKER-GUIDE]`、`next_action`、`recovery_steps` を返した場合は、それを現在の復帰手順として実行します。別の文書や旧経路を探して迂回しません。

## 実装資料の扱い

`queue-v10.md`、機械可読ポリシー、Library・監査・転送関連の文書は、GitHub Actionsや保守作業のための**実装リファレンス（implementation reference）**です。通常ワーカーは、これらを独立した実行手順として再解釈したり、複数文書を組み合わせて別ルートを作ったりしません。

履歴データの読取互換が内部実装に残っていても、それは新規処理で選択できる経路ではありません。新規書込み・復旧・終了判断は常に `worker-router.md` と正規スクリプトが示す現行経路だけを使います。
