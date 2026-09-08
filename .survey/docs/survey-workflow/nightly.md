# 24回目の全リポジトリ整合性チェック

この処理は時刻ではなく `run_index=24` でのみ実行する。24回目はそのcycleの最後であり、通常精読・新規選定を行わない。

## 順序

1. 最新HEADとcycle claimを固定し、`maintenance:<cycle_id>` の作業権をclaim tokenに結び付ける。
2. 可能なら完全checkoutで全ファイル一覧を取得する。
3. 未compact identity deltaを `.survey/scripts/identity_delta.py validate` → `compact` の順で処理する。
4. `.survey/scripts/survey_v8.py build` → `validate`、`.survey/scripts/check_repository_v8.py`、unit testsを実行可能な範囲で行う。
5. README、件数、comparison、STATUS、識別索引、progress delta、plan、cycle state、retry/reject、リンクを照合する。
6. 正本から決定的に直せるものだけ修復する。論文内容の判断が必要なら監査候補へ送る。
7. run 24を終了し、completion.mdに従って各次目標を決定してcycleを閉じる。

checkout/Pythonが無い場合はconnectorで可能な検査を行い `partial` を正確に残す。未実行検査を成功扱いしない。ただし24回目自体はcycleを閉じ、未解決保守は `.survey/survey-state/maintenance-queue.json` へ引き継ぐ。

詳細run記録は24時間超をこの整合性runで整理する。cycle history、progress delta、retry/reject、未解決blockerは削除対象外。
