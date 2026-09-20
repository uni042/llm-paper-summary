# 研究サーベイ運用入口

Scheduled Chat / Work のワーカー（worker）が実行判断のために読む**唯一の人間向け正本**は [`worker-router.md`](worker-router.md) です。

同じ `main` の最新HEADで、ワーカーが通常参照するものは次だけです。

1. `worker-router.md` — 役割分岐（routing）、処理ループ、探索、保存、停止条件。
2. `continuation-policy.json` — 実行時間やしきい値の機械可読設定。
3. `.survey/templates/paper.md` — 論文レコードの品質・必須項目。
4. ライブ状態: `.survey/work-queue/next-jobs.json`、`maintenance-cycle.json`、`discovery-state.json`。

`queue-v10.md`、Library関連文書、監査文書はGitHub Actionsや保守担当向けの**実装リファレンス（implementation reference）**です。ワーカーはそれらを独立した役割分岐の指示として扱いません。

## 現行経路

- 研究・監査（Research / Audit）: 1件だけ担当確保（claim）→一次資料全文→5スロット構造化レコード→事前検査（preflight）→不変提出（immutable submission）またはChatGPT Libraryへ耐久保存。
- 探索（Discovery）: 固定ソース方式の schema v3 だけを新規利用。引用グラフ優先で、通常runは `repository_references` による後方引用を先に1バッファ処理し、同じrunで前方引用も実行する。後方引用候補が残っていても前方引用を止めない。通常検索は同じrunで後方引用・前方引用の両方を試した後の補完にだけ使う。候補は既定20件ずつ事前検査し、無関係・微妙判定を台帳へ残して再判定を避ける。
- 外部退避（fallback）: GitHub直接保存またはChatGPT Libraryのみ。
- ワーカーが誤った経路を選んだ場合は、検証エラーの `next_action` / `recovery_steps` に従って現行経路へ戻す。旧経路で回避しない。

## 廃止済み経路

新規処理では次を使いません。

- Google Drive / Notion / 旧 `/LLM-survey-fallback/`
- 固定 `.survey/work-queue/submissions/chat-inbox.json`
- Discovery schema v1 / v2 の手書き候補投入
- 手動Library復旧ワークフロー
- ServerlessLoRA専用復旧ワークフロー
- 旧Library replay bundleワークフロー

履歴データを読み取るための互換コードが内部に残る場合がありますが、それは**新規ワーカーが選べる経路ではありません**。
