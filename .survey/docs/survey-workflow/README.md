# 研究サーベイ運用手順

現在の正本は **workflow v9（queue-based）**。詳細は [queue-v9.md](queue-v9.md) を読む。

## 実行原則

- 固定の日次件数、cycle目標、精読/監査同数ノルマは使わない。
- GitHub Actionsを状態管理worker、Chat側Scheduled Taskを研究作業workerとして分離する。
- GitHub Actionsは10分ごとに起動し、未処理submissionを反映して次jobを生成する。
- Chatは `.survey/work-queue/next-jobs.json` と各jobだけを読み、検索・本文精読・科学的判断・正式監査を行う。
- Chatが書くのは `.survey/work-queue/submissions/<unique>.json` の新規小ファイルだけとし、大きな共有状態・集約index・READMEを通常処理で直接更新しない。
- workerは冪等で、同じsubmission/jobを二重反映しない。
- 一次資料本文を取得できない場合は推測せずblocked/deferredとして返す。

## 探索

workerの10分pollと探索頻度は分離する。

- 新着探索: 2時間ごと
- 引用・follow-up探索: 6時間ごと
- 系統gap/隣接分野探索: 24時間ごと

弱い候補で数を埋めない。研究backlogは最大12、監査backlogは最大6。

## 監査

全論文を1対1で監査しない。高重要度、明示的不確実性、版・書誌確認が必要なもの、決定的20%サンプルを正式監査する。

## 旧workflow

workflow v8の `cycle-state.json`、run、plan、progress delta、10/10・11/11等のtargetは履歴・復旧用であり、v9の仕事生成には使わない。移行だけを理由に旧成果を再読・再加算しない。
