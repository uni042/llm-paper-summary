# 補助プログラムと共通形式

workflow 8では制御を時刻からGitHub上の回数へ移す。管理用の実ファイルは `.survey/` 配下に置く。checkout環境では `.survey` を管理root、リポジトリrootを公開コンテンツrootとして扱う。

## 共通実行基盤

Scheduled Task側のPython・shell・checkout可否はrunごとに保証されないため、deterministicな補助処理は [GitHub Actions共通補助実行基盤](actions-worker.md) を優先する。`.survey/requests/*.json` をcommitするとActionsがcheckout＋Pythonで処理し、`.survey/results/*.json` を返す。request/resultが使えない場合に限り、下記スクリプトをローカルで直接実行するか、同じ規則をconnectorで再現する。

## 主な補助プログラム

リポジトリrootから実行する。

```bash
python .survey/scripts/run_bootstrap.py --run-id <id> --workflow-commit <commit> [--scheduled-at <metadata>] [--morning-overlay] --apply
python .survey/scripts/cycle_state.py status
python .survey/scripts/next_work.py
python .survey/scripts/cycle_state.py claim --run-id <id> --workflow-commit <commit> --apply
python .survey/scripts/cycle_state.py finish --run-id <id> --claim-token <token> --apply
python .survey/scripts/cycle_state.py planning-seed
python .survey/scripts/cycle_state.py lease acquire --resource <resource> --run-id <id> --claim-token <token> --apply
python .survey/scripts/prepare_result.py --side research --paper papers/inference/<lineage>/<paper>.md --apply
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

## next_work

`.survey/scripts/next_work.py` はplan snapshotと当cycleのprogress deltaを統合し、研究側/監査側の `target/done/pending` と次に処理すべき1件をJSONで返す。優先規則は決定的で、片側だけ未完了ならその側、両側未完了なら完了率 `done/target` が低い側、同率ならresearchを選び、side内はplan順を維持する。

同時に `after_action` を返す。callerはこれを単なる提案として表示して終了せず、安全に実行可能なら同じrun内で実行する。`continue_same_run` なら次論文/監査、`close_cycle` ならcycle締め、`claim_next_run` なら次run claim、`integrity_only` ならrun24処理、`finish_run` なら終了する。成果保存後に再評価し、余裕がある限りループできる。

このhelperで代替するのは進捗集計と次対象の機械的選択だけであり、論文の関連性・採否、本文解釈、監査品質の判断は自動化しない。

## prepare_result / progress delta / identity delta

`.survey/scripts/prepare_result.py` は保存済みpaper frontmatterと現在のactive claimを読み、canonical ID、必要なidentity delta、progress delta、同時に公開すべきファイル一覧を生成する。run_id / run_index / claim_tokenを手入力しないため、古いclaimを誤ってprogressへ埋め込む作業を減らす。GitHubへのpublish自体は行わないので、callerは生成物を論文本体と同じcommitへまとめ、リモート再取得で確認する。

Actions workerの `prepare_result` operationを使う場合はworkerがcheckout上でこのhelperを実行し、生成差分とresultをcommitする。callerは同名resultの `ok: true` とpayloadを確認する。

plan/queueの大きい書換えを毎論文で行わず、`.survey/survey-state/progress-deltas/` に1研究1小ファイルを保存する。論理進捗はplan snapshotとdeltaを重ねて算出する。既存plan内の旧 `completed` も保持する。

識別索引は形式3snapshot + `.survey/survey-state/identity-deltas/`。通常runは差分のみ、24回目に可能ならcompactする。

## 汎用行編集

`.survey/scripts/repo_edit.py` は非生成UTF-8テキストの局所修正用非常工具。公開コンテンツを編集するときは `--root .` を明示する。root外禁止、dry-run、SHA前提、原子的保存を維持する。専用helperがある状態操作や自動生成範囲を迂回しない。Actions requestから任意編集を許可せず、必要なら入力検証付き専用operationを追加する。

## build / validate

workflow 8では `survey_v8.py` を正規入口とする。旧 `survey.py` は生成ロジックの互換実装として内部利用できるが、旧plan/queueの完了状態だけでworkflow 8の進捗を判定しない。`check_repository_v8.py` はリポジトリroot全体を検査し、`.survey/` 内の管理状態と公開コンテンツを両方対象にする。

## 時刻を使うもの

通知条件、朝報告の境界、7日間隔の一次資料再確認、公式資料の公開/改訂日、観測メタデータには時刻を使える。run mode、run順序、目標増減、作業権有効性には時刻を使わない。
