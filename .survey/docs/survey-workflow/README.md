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

## 保守資料の扱い

通常ワーカーが読む手順書は `worker-router.md` だけです。実行契約の実体は正規スクリプトとワークフローにあり、保守者は必要に応じて次を確認します。

- `.survey/scripts/**`: 実行可能な正規経路と機械可読な復旧案内
- `.github/workflows/**`: GitHub Actions の実行順・権限・直列化条件
- `.survey/tests/**`: 現行契約と履歴読取互換の回帰条件
- このディレクトリの個別資料: Library、監査など特定機構の保守用リファレンス

閾値、ノルマ、停止条件、探索順序などのワーカー行動を別の保守資料へ重複記載して第二の正本にしません。履歴互換処理が内部実装に残っていても、新規処理で選択できる経路ではありません。
