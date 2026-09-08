# 補助プログラムと共通形式

workflow 8では制御を時刻からGitHub上の回数へ移す。

## 主な補助プログラム

```bash
python scripts/run_bootstrap.py --run-id <id> --workflow-commit <commit> [--scheduled-at <metadata>] [--morning-overlay] --apply
python scripts/cycle_state.py status
python scripts/cycle_state.py claim --run-id <id> --workflow-commit <commit> --apply
python scripts/cycle_state.py finish --run-id <id> --claim-token <token> --apply
python scripts/cycle_state.py planning-seed
python scripts/cycle_state.py lease acquire --resource <resource> --run-id <id> --claim-token <token> --apply
python scripts/progress_delta.py prepare --side research --canonical-id <id> --status completed --run-id <id> --claim-token <token> --artifact <path> --verified-commit <sha> --apply
python scripts/identity_delta.py validate
python scripts/identity_delta.py compact
python scripts/repo_edit.py read --path <file> --start-line 1 --end-line 40 --number
python scripts/survey.py build
python scripts/survey.py validate
python scripts/check_repository.py --inventory /tmp/repository-inventory.json --report /tmp/integrity.json
python -m unittest discover -s tests
```

## run_bootstrap

`cycle-state.json` を読み、現在のrun indexをclaimして `cycle_id/run_index/mode/claim_token` を出力する。mode境界は固定:
- 1 planning
- 2〜23 reading
- 24 integrity

`--scheduled-at` は観測メタデータにしか使わない。`--morning-overlay` は起動元が朝報告対象と判定した時だけ渡し、cycle modeを変えない。

未終了claimが残る場合は同じrun indexのrecoveryとして新tokenでsupersedeする。古いtokenの後続成果は完了確定に使わない。

## cycle_state

`claim` は次runを取得、`finish` は通常runを次indexへ進める。両側のplanが23回目以前に尽きた場合はcycleを早期終了し、各目標を+1して次cycle run 1へ戻す。run 24は整合性チェック後にcycleを必ず閉じ、完了側を+1、未完了側を-1する。

`planning-seed` は前cycleのplanとprogress deltaを統合し、現在目標Nに対して古い繰越、overflow、新規探索可能枠を出力する。

作業権は期限時刻ではなく現在のclaim tokenに従属する。`lease acquire/release` は `cycle_id/run_index/run_id/claim_token` を保存し、最新cycle claimとtokenが一致する間だけ有効である。

## progress_delta

plan/queueの大きい書換えを毎論文で行わないための1研究1小ファイル。論理進捗はplan snapshotとdeltaを重ねて算出する。既存plan内の旧 `completed` も保持する。

## identity_delta

従来どおり形式3snapshot + 未compact差分。通常runは差分のみ、24回目に可能ならcompact。

## repo_edit

非生成テキストの局所修正用非常工具。root外禁止、dry-run、SHA前提、原子的保存を維持する。専用helperがある状態操作をrepo_editで迂回しない。

## 時刻を使うもの

通知条件、朝報告の境界、7日間隔の一次資料再確認、公式資料の公開/改訂日、観測メタデータには時刻を使える。run mode、run順序、目標増減、作業権有効性には時刻を使わない。
