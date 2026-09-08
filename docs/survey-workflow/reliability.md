# 安定実行・復旧の共通仕様（実行方式5）

## 補助プログラム

Python 3.10以上と `scripts/requirements.txt` の依存を使用する。実行前に、このファイルと使用するプログラムを同じ変更識別子で取得する。補助プログラムは読解・採否・監査の代行をせず、ローカルファイルの決定的な変換だけを行う。リモート保存は別工程である。

```bash
python -m pip install -r scripts/requirements.txt
python scripts/survey.py build
python scripts/survey.py validate
python scripts/survey.py closing-result
python -m unittest discover -s tests
```

`build` は冒頭属性から識別索引、系統別一覧、上位件数、横断比較、進捗ページを生成する。著者が書いた系統説明・技術の分岐・論文本文は保持する。自動生成範囲は手編集しない。`validate` は識別子重複、索引差分、必須属性、日次計画・未完了一覧の不整合、成果物欠落、日次履歴重複、再確認間隔、主要ページの内部リンクを検査する。一次資料の正確さや全文精読そのものを認定する検査ではない。

通常は保存前に変更論文と関連状態を検査する。全件生成・検査は朝の点検または形式移行時に実施する。実行環境にPythonがない場合、接続機能で同じ属性・不変条件・保存手順を実施してよい。全件再生成は保守へ送って当該論文だけ処理し、全検査を実行したと記録しない。再構築不能な索引の矛盾があるときは新規登録を止める。

## 識別・属性の仕様

`templates/paper.md` を共通形式とする。必須キーは `canonical_id`, `title`, `summary`, `source`, `last_audited`, `audit_version`。監査未実施は `last_audited: null`, `audit_version: 0` とし、形式移行だけでは監査日を更新しない。確認済みの `arxiv_id`, `doi`, `openreview_id` を同じページに保存する。改題・会議版追加でも既存の正規識別子は維持する。

識別索引の形式3は `papers[canonical_id].path` で保存先を直接解決し、`identifier_to_canonical` で別識別子を照合する。`source_hash` は論文ファイルの内容照合用で、一次資料確認の証拠ではない。移動案内は `ignored_moved_stubs` へ残し収録数から除く。本文と属性に矛盾があれば勝手に正しい方を決めず監査対象にする。

比較用の属性は `storage_targets`, `bottlenecks`, `hardware_details`, `quality_effect`, `evidence_locations`。既存の `topics`, `hardware_evaluation`, `code`, `summary` も表示する。未確認値は空配列またはnull。`evidence_locations` は一次資料URL・版・節/表/図・何を裏付けるかを含む。次回の通常監査で根拠が確認できた項目を補い、全論文を比較表のためだけに再精読しない。

## 作業権の確保と期限

`survey-state/leases.json` の `items[resource]` に実行識別子・更新時刻・有効期限を保持する。論文は `paper:<canonical_id>` とし精読と監査で共有する。日次選定・締めは `planning:<period_start>`、保守は `maintenance` を使う。有効期間45分、長い作業では20分以内を目安に更新する。

```bash
python scripts/survey.py lease acquire --resource paper:arXiv:2609.03949 --run-id RUN_ID
python scripts/survey.py lease renew --resource paper:arXiv:2609.03949 --run-id RUN_ID
python scripts/survey.py lease release --resource paper:arXiv:2609.03949 --run-id RUN_ID
```

このコマンドだけで排他を獲得したことにはならない。必ず次の順に行う。

1. 最新の先頭版と作業権ファイルを読む。他実行が有効期限内なら別の対象へ進む。
2. 読み取った先頭版を親として、作業権取得だけの変更を作り、強制なしで先頭参照を更新する。ファイル単独APIなら取得した内容SHAを条件に更新する。
3. 競合したら最新状態から再判断する。同じ古い変更を再送して奪わない。
4. リモートの作業権が自分の実行識別子で、未期限切れであることを再取得して確認した後に着手する。
5. 成果保存直前にも所有権と期限を確認し、その確認版を親として公開する。所有権を失った実行は成果を公開せず、保存済み成果を照合する。更新できなければ継続しない。
6. 成果と進捗を保存確認したら解放する。期限切れを他実行が取得した後、旧実行が解放・上書きしてはいけない。

実行ごとに独立したローカル作業場所を使用する。同じローカルファイルを複数実行で同時更新しない。競合時は最新版に自分の項目差分だけを適用する。

## 開始・途中・終了記録

`survey-state/runs/<run_id>.json` を実行ごとに作る。run_idは予定枠だけでなく一意な乱数等も含め、手動再実行で再利用しない。

```bash
python scripts/survey.py run start --run-id RUN_ID --scheduled-at ISO_TIME --mode reading --stage starting --next-action 照合
python scripts/survey.py run progress --run-id RUN_ID --stage reading --next-action 評価確認
python scripts/survey.py run finish --run-id RUN_ID --stage finished --next-action 次枠 --status completed --verified-commit COMMIT
```

開始記録をリモート保存確認してから外部調査に着手する。対象決定時・論文ごとの保存確認時・長い処理の工程境界で途中記録を更新する。少なくとも `started_at`, `scheduled_at`, `last_progress_at`, `mode`, `stage`, `status`, `next_action` を残し、対象の `canonical_id` と `plan_id` も判明後に追加する。記録は観測用で成果の正本ではない。

強制終了した実行は終了記録を偽造しない。期限切れの作業権と古い途中記録から「停止の疑い」と表示し、実際の成果を照合して別実行で復旧する。終了済み詳細記録は24時間で整理するが、未解決の開始・途中記録は復旧確認まで保持する。整理は朝の点検でまとめて実施し、論文保存ごとに全記録を列挙しない。既存の `log/` 形式も24時間対象として読めるが、新規記録は `runs/` に統一する。

## 日次選定が未実行のとき

起動元が渡す予定実行枠・タイムゾーン・日次選定時刻から、その枠が属する読書期間を決める。現在時刻の遅れだけで別期間へ移さない。

```bash
python scripts/survey.py route --scheduled-at ISO_SLOT --period-start ISO_BOUNDARY
```

当日計画が存在しない、前期間の計画のまま、または選定途中なら `recover_planning`。精読実行も当日選定の代行を行える。日次選定用の作業権を確保し、前計画の締め・履歴追加・次目標・新計画・未完了一覧・runtime参照を整合した一括変更として保存する。同じplan_idの締めは再適用しない。計画がreadyになった後で通常の精読へ戻る。選定だけで余裕がなくなれば保存して次枠へ渡す。

複数日空いても、未実行の仮想日を作って目標を繰り返し減らさない。実在する前計画を一度だけ締め、当該期間を選定する。計画終了直前に始めた論文は、締め側が有効な作業権の解放/期限切れを待って成果を照合する。旧期間の遅延実行は現在計画を巻き戻さない。朝モードは選定を代行しない。

## 本文取得失敗の再確認

当日の進行を止めず項目を決着させ、`survey-state/retry-papers.json` へ移す。全文精読には数えず、当日枠を毎時補充しない。

- 初回失敗から **7日後** に再確認する。以後も最後の確認から7日以上空ける。期限到来分を日次選定で確認し、取得可能なら元の優先基準で候補に戻す。取得できただけで精読完了にしない。
- 1回の確認は優先経路と別の公式経路を各1回まで。試行日・URL・失敗種別・確認した版を記録する。過去の試行日が不明なら回数を推測しない。
- 初回を含む **5回以上** の確認が失敗し、初回から **28日以上** 経過した場合は `dormant` として定期取得を停止する。これは永久除外ではない。公式の新しい本文経路・新版公開を通常探索で発見した場合、または利用者の再調査指示で再開できる。
- 通信障害、認証障害、有料公開、未取得、採択未確認、候補順位が低いことだけでは永久除外しない。

永久除外は次の根拠がある場合に限定し、`rejected-papers.json` に `reason_code`, `evidence_url`, `checked_at`, `checked_source_version`, `reopen_condition` を残す。

| 理由 | 基準 | 後日の扱い |
|---|---|---|
| `duplicate` | 既存研究との同一性を一次資料で確認 | `duplicate_of` に統合先を指定。別ページ作成はしない |
| `out_of_scope` | 一次資料から最終目的が推論効率化の収録範囲外と確認 | 対象範囲変更・研究目的の実質変更時だけ再評価 |
| `not_research` | 公式原文から研究論文ではなく予告・広告等と確認 | 正式論文が公開されたらその論文を新候補として評価 |
| `withdrawn_or_retracted` | 公式の撤回・取り下げを確認し、訂正版への置換もない | 訂正版・公式復活を確認したら再評価 |

既に掲載済みの研究が撤回された場合はページを削除せず状態と公式根拠を追記し、通常の新規候補から除く。「永久」は通常探索で繰り返し候補化しない意味で、公式状況変更の追跡を禁止する意味ではない。

## 進捗と比較の入口

- [進捗ページ](../../survey-state/STATUS.md)：精読・監査の進捗、直近実行、次の処理、取得再確認、保守待ち。
- [横断比較](../../papers/inference/comparison.md)：明示属性の比較。未記録は次の監査で補完。
- 朝の集約では新着・修復・未解決問題とともに、開始記録なし／停止疑い／正常終了の観測範囲を区別する。通知時刻は起動元の既存設定を維持する。

`closing-result` は前計画の翌日目標と繰越識別子を計算する読取り専用コマンド。結果を履歴へ保存する際は新計画・未完了一覧と同時に公開する。`cleanup` は朝の記録整理用で、削除差分もリモート保存確認する。旧log形式の整理は本文のfinished_atを確認して行う。
