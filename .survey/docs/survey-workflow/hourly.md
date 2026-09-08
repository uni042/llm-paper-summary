# 選定済み論文の精読・監査

run 2〜23だけが通常の精読・監査を担当する。

## 対象選択

plan snapshotと当cycleの `.survey/survey-state/progress-deltas/` を統合して未完了を算出する。checkout/Pythonが使える場合は、まず `.survey/scripts/next_work.py` を実行し、正規化済み進捗・優先side・次のcanonical IDを機械的に決める。helperが使えない場合だけ同じ規則を接続機能で再現する。

優先規則は、片側だけ未完了ならその側、両側未完了なら `done/target` が低い側、同率なら精読を先にする。各side内ではplan順の最初の未完了を選ぶ。保存済み論文本体があるのにprogress deltaだけ欠ける場合は、一次資料を再読せず成果・識別子・既存run記録を照合してreconcileする。

## 精読

一次資料本文を読み、問題、新規性、手法、評価条件、主要結果、限界を確認する。取得不能ならretries手順に従い、次候補へ進む。

## 監査

同一研究、書誌、著者/所属、公開・採択・出版状態、最終版、一次資料/実装、主要値の出典、機器/モデル/データ/比較条件、実機/模擬、分類、差分、限界を確認する。すべて確認できた場合だけ `last_audited` と `audit_version` を更新する。

## 保存

1論文ごとに論文本体/監査変更、必要なidentity delta、progress deltaを保存する。checkout/Pythonが使える場合は `.survey/scripts/prepare_result.py` を優先し、paper frontmatterと現在claimからidentity/progress deltaを機械生成する。大きいplan/queue全体の更新は通常runの完了条件にしない。progress deltaをリモート再取得できた時点で論理完了に数える。

## 成果保存後の続行判定

**1件保存するたびに** `.survey/scripts/next_work.py` をもう一度実行する。helperの `after_action` を同一run内の次導線として使う。

- `continue_same_run`: 実行環境・接続・文脈容量に余裕があり、安全に次の1件へ進めるならrunを終了せず、そのまま `after_action.next` を処理する。1run=1本とはしない。
- `close_cycle`: 精読・監査の両方がterminal。runを通常終了させず早期cycle締めへ進む。
- `integrity_only`: run 24。通常の精読・監査を追加せず整合性処理だけ続ける。
- `finish_run`: 続行可能な決定的対象がないため終了する。
- `claim_next_run`: active claimがない。新しい通常作業を始める前に次runをclaimする。

`continue_same_run` は追加作業の**提案**であり、無理に開始して途中で壊すことを要求しない。一次資料の取得、GitHub書込み、現在claimの有効性が保たれ、少なくとも次の成果を安全に保存できる見込みがある場合だけ続行する。続行しない場合も未完了対象はprogress正本に残るため、次の予定実行が同じ論理進捗から再開する。

同一runで追加処理した場合は、run記録の `processed` に成果ごとに追記する。各成果保存後に再度 `next_work.py` を実行し、余裕がある限りこのループを繰り返せる。

## 早期繰上げ

精読・監査の当周planが両方ともterminalになったら、run 23を待たずcycleを成功終了する。各次目標を+1し、次cycleを作成してrun indexを1に戻す。同じ予定実行に余裕があれば、その場でrun 1をclaimして次の論文選定を始める。
