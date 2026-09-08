# 研究サーベイの運用手順

実行方式：8（`workflow_version: 8`）。管理用ファイルは `.survey/` 配下に集約する。実処理の順序は時刻ではなく、GitHub上の `.survey/survey-state/cycle-state.json` に保存された `cycle_id` と `run_index` を正本として決める。時刻は通知、朝報告、本文再確認期限、観測メタデータにだけ使い、モード判定・作業権・進捗加算には使わない。

## 1周の構成

1周は最大24回。

| run_index | 基本処理 |
|---:|---|
| 1 | 前周を必要に応じて締め、繰越を先に入れ、当周の精読・監査対象を選定する |
| 2〜23 | 選定済み論文の精読・正式監査を進める |
| 24 | 全リポジトリ整合性チェック、識別差分compact、生成物修復、未完了整理、周の締め |

精読・監査の当周予定が23回目以前に両方とも尽きた場合は、その時点で前周を成功として締め、次目標を各+1し、同じ予定タスク実行の残り時間で次の `cycle_id` の `run_index=1` を開始して新しい対象を選ぶ。24回目まで残件がある場合は、24回目の整合性チェック後に未完了側の次目標を1減らし、完了側は1増やす。次の1回目では前周の残りを最優先し、残りと新規候補を合わせて各目標N本にする。繰越がN本を超える場合は古い繰越からN本を選び、余剰はqueueに残す。

## 毎回の開始

1. 既定ブランチの最新変更識別子を取得し、その同じ版の `.survey/docs/survey-workflow/README.md` と必要な手順だけを読む。
2. `.survey/survey-state/cycle-state.json` を取得し、`.survey/scripts/run_bootstrap.py` が使えるなら同じ版で実行する。使えない場合も同じ規則を接続機能で再現する。
3. `cycle_state.active_claim` を最新HEADへ保存してから作業を始める。開始スクリプトは `cycle_id`, `run_index`, `mode`, `claim_token` を出力する。
4. 実行中の成果保存は現在のclaim tokenに結び付ける。別runがclaimを更新した後の古いtokenでは完了を確定しない。
5. 編集時は [保存と検証](publishing.md)、終了時は [完了判定](completion.md) を読む。

## モードとoverlay

`mode` はrun_indexだけで決める。予定時刻や実開始時刻では変更しない。

- `planning`: run 1
- `reading`: run 2〜23
- `integrity`: run 24

起動元が朝報告対象として指定した予定枠では `morning` をoverlayとして追加し、[朝の更新](morning.md)を実施して通知する。overlayはrun_indexを増やさず、基本modeを置き換えない。

## 共通仕様

- [開始・状態](state.md)：cycle state、claim、run記録、復旧
- [周選定](planning.md)：繰越＋新規でN本、一次資料preflight、優先度
- [精読・監査](hourly.md)：progress deltaによる小さい完了記録
- [保存と検証](publishing.md)：identity delta / progress delta / 生成物
- [本文再確認](retries.md)：7日間隔の本文再確認と根拠付き永久除外
- [24回目整合性](nightly.md)：全体検査と修復
- [補助プログラム](reliability.md)：bootstrap、cycle、delta、汎用編集
- [完了判定](completion.md)：早期繰上げ、24回目締め、次目標

## 保全

移行だけで精読・監査件数を増減しない。保存済み成果は再読せず、progress deltaが欠けた実成果だけを根拠付きでreconcileする。旧 `.survey/survey-state/daily-plans/`、`runtime.json`、`queues/` は互換情報として利用できるが、workflow 8の制御正本はcycle state、選定snapshot、progress delta、cycle historyである。通常実行で予定タスクや手順書を自己変更しない。
