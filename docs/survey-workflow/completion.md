# 完了判定と周の引継ぎ

## run 1

選定snapshotを保存確認できたらrun 1完了。`next_run_index=2`。

## run 2〜23

progress deltaで当runの成果を確認する。planに未完了が残れば次indexへ進む。

精読・監査の両方が予定分すべてterminalなら早期終了:
- current cycleを `early_exhausted` で閉じる
- 精読目標・監査目標を各+1
- 次cycleを作り `next_run_index=1`
- 同じ予定タスク実行に余裕があれば、そのまま新cycle run 1をclaimして選定する

## run 24

run 24は必ず整合性チェックを実施して当cycleの最後とする。その後、精読・監査を別々に判定する。

- その側の未完了が0: 次目標 = n+1
- 未完了あり: 次目標 = max(1, n-1)

次cycleは `next_run_index=1`。24回目の中では次cycleの通常精読を始めない。次の予定タスクがrun 1を行う。

## 次cycleのN本

run 1は前cycleの未完了を最優先し、繰越＋新規を合わせて新目標N本にする。繰越がN本を超える場合は古い順にN本だけ当cycleへ割り当て、余剰はqueue/backlogに残す。

## 不可用本文

取得不能をretryへ移した項目はそのcycleでterminalとして扱えるが、全文精読成果とは区別して記録する。永久除外はretries.mdの根拠要件を満たす場合だけ。

## cycle history

閉じたcycleは `cycle-history/<cycle_id>.json` に一度だけ記録し、close reason、run index、各目標、done/pending、次目標、plan pathを保存する。移行・reconcileだけで同じ成果を再加算しない。
