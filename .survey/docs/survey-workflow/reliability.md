# 補助プログラムと共通形式

workflow 8では制御を時刻からGitHub上の回数へ移す。管理用の実ファイルは `.survey/` 配下に置く。checkout環境では `.survey` を管理root、リポジトリrootを公開コンテンツrootとして扱う。

## 主な補助プログラム

リポジトリrootから実行する。

```bash
python .survey/scripts/run_bootstrap.py --run-id <id> --workflow-commit <commit> [--scheduled-at <metadata>] [--morning-overlay] --apply
python .survey/scripts/cycle_state.py status
python .survey/scripts/cycle_state.py claim --run-id <id> --workflow-commit <commit> --apply
python .survey/scripts/cycle_state.py finish --run-id <id> --claim-token <token> --apply
python .survey/scripts/cycle_state.py planning-seed
python .survey/scripts/cycle_state.py lease acquire --resource <resource> --run-id <id> --claim-token <token> --apply
python .survey/scripts/progress_delta.py prepare --side research --canonical-id <id> --status completed --run-id <id> --claim-token <token> --artifact <path> --verified-commit <sha> --apply
python .survey/scripts/identity_delta.py validate
python .survey/scripts/identity_delta.py compact
python .survey/scripts/repo_edit.py read --root . --path <file> --start-line 1 --end-line 40 --number
python .survey/scripts/survey_v8.py build
python .survey/scripts/survey_v8.py validate
python .survey/scripts/check_repository_v8.py --inventory /tmp/repository-inventory.json --report /tmp/integrity.json
python -m unittest discover -s .survey/tests
```

## run_bootstrap / cycle_state

`.survey/survey-state/cycle-state.json` を読み、現在のrun indexをclaimして `cycle_id/run_index/mode/claim_token` を出力する。modeは1=planning、2〜23=reading、24=integrity。`--scheduled-at` は観測メタデータにしか使わない。`--morning-overlay` は起動元が朝報告対象と判定した時だけ渡し、cycle modeを変えない。

未終了claimが残る場合は同じrun indexのrecoveryとして新tokenでsupersedeする。古いtokenの後続成果は完了確定に使わない。作業権も現在のclaim tokenに従属する。

両側のplanが23回目以前に尽きた場合はcycleを早期終了し、各目標を+1して次cycle run 1へ戻す。run 24は整合性チェック後にcycleを必ず閉じ、完了側を+1、未完了側を-1する。

`planning-seed` は前cycleのplanとprogress deltaを統合し、現在目標Nに対して古い繰越、overflow、新規探索可能枠を出力する。

## progress delta / identity delta

plan/queueの大きい書換えを毎論文で行わず、`.survey/survey-state/progress-deltas/` に1研究1小ファイルを保存する。論理進捗はplan snapshotとdeltaを重ねて算出する。既存plan内の旧 `completed` も保持する。

識別索引は形式3snapshot + `.survey/survey-state/identity-deltas/`。通常runは差分のみ、24回目に可能ならcompactする。

## 汎用行編集

`.survey/scripts/repo_edit.py` は非生成UTF-8テキストの局所修正用非常工具。公開コンテンツを編集するときは `--root .` を明示する。root外禁止、dry-run、SHA前提、原子的保存を維持する。専用helperがある状態操作や自動生成範囲を迂回しない。

## build / validate

workflow 8では `survey_v8.py` を正規入口とする。旧 `survey.py` は生成ロジックの互換実装として内部利用できるが、旧plan/queueの完了状態だけでworkflow 8の進捗を判定しない。`check_repository_v8.py` はリポジトリroot全体を検査し、`.survey/` 内の管理状態と公開コンテンツを両方対象にする。

## 時刻を使うもの

通知条件、朝報告の境界、7日間隔の一次資料再確認、公式資料の公開/改訂日、観測メタデータには時刻を使える。run mode、run順序、目標増減、作業権有効性には時刻を使わない。
