# 朝の更新と集約

朝の更新はworkflow v8では**overlay**であり、cycleのmodeやrun_indexを変更しない。起動元が朝報告対象として指定した予定枠でだけ実行する。

## 担当範囲

1. 前回朝報告境界より後の論文追加・重要更新・分類変更を変更履歴から集約する。
2. `framework-updates/` と `llm-releases/` の重要更新を公式資料で確認する。
3. `.survey/survey-state/integrity/` の最新結果、open maintenance、blocker、cycle進捗を要約する。
4. 前回朝報告以降の `.survey/survey-state/runs/`、`blockers.json`、`maintenance-queue.json` を見て、繰返し手作業や取得・編集・検証制約を減らせる補助プログラム候補を最大3件抽出する。
5. 報告と必要な保存を確認してから朝報告境界を更新する。

## 補助プログラム提案

有効な案がある場合だけ `仮称 / 解決する問題 / 期待効果 / 優先度` を1〜2行で示す。同等機能が既に `.survey/scripts/` にあれば新規案ではなく既存ツール拡張として示す。一度きりの偶発障害より、反復する大きいファイル編集、状態同期、復旧、検証、差分生成を優先する。

## 通知

通知時刻・条件は起動元を維持する。朝overlayはその予定タスクのcycle runを1回だけ消費し、別runとして追加カウントしない。通知のためにcycle targetや完了数を変更しない。
