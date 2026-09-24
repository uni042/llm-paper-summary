# llm-paper-summary レガシー完全撤去手順書

## 1. 目的と適用範囲

`uni042/llm-paper-summary` の現行 `main` を起点に、保持する論文・状態データを現行契約へ移行し、現行producerが生成しない旧形式を読むコード・手順・試験を段階的に撤去する。Git履歴は書き換えない。ここでの「完全撤去」は最終作業ツリーからの撤去を指す。

**作業開始時に固定する基準点**（2026-09-24確認）:

- `main`: `5176d8bc6ed70a638bd817ef98353e7a2aa5e48a`
- 作業ブランチ: `legacy-purge/2026-09-24-current`（上記commitから作成）
- この文書の件数は上記commitの棚卸し値。移行実施時の件数を示すものではない。mainではDiscovery処理が進行中のため、ライブデータの移行・削除は書込凍結と再棚卸しが完了するまで開始しない。

|対象|基準点での件数|
|---|---:|
|Git tree entries（ディレクトリを含む）|11,024|
|ファイル|10,840|
|論文Markdown|1,024|
|papers/inference|986|
|papers/training|25|
|papers/survey|13|
|.survey/scripts/*.py|97|
|.survey/tests/*.py|136|
|work-queue/jobs|1,220|
|work-queue/claims|701|
|claim requests / results|各60|
|submissions / results|各382|
|research-preflight|556|
|run-state|169|
|discovery-preload|231|
|archive/transport|3,758|
|fallback-archive|100|
|fallback-failed|45|
|fallback-inbox|2|

件数はGit treeから算出したファイル数であり、実行中・完了済み等の状態判定ではない。分類は必ず実データを読み、同一の固定commitに対して作る。

## 2. 正本と移行原則

- 論文契約: `.survey/templates/paper.md`、`.survey/scripts/render_paper.py`、`check_repository.py`、`audit_paper_quality.py`、`audit_list_summary_quality.py`、`audit_overview_results.py`
- ワーカー手順の唯一の人間向け正本: `.survey/docs/survey-workflow/worker-router.md`
- 保守実装索引: `.survey/docs/survey-workflow/queue-v10.md`（現行文書は互換由来のファイル名を明記している）
- Research/Auditレコード: `metadata`、`problem_method`、`evaluation`、`results`、`positioning` の5スロット。レコードの `schema_version: 1` / `transport_version: 10` を、他のデータ種別へ流用しない。
- Discovery事前検査などは別契約を持つ。データ種別ごとに現行writerとreaderを調べ、正規形式を決める。

順序は「契約の確認 → 棚卸し → 意味のあるデータ移行または履歴要約 → 現行形式のみでの動作確認 → 旧reader削除」。科学的内容を推測で補完しない。現在も生成されるLibrary退避と不変提出への復旧経路は維持する。

## 3. 移行時点の再棚卸しと安全ゲート

1. 作業ブランチの親HEADと最新 `main` を記録する。mainが親HEADから進んでいたら、変更を始めず最新mainを取り込み、棚卸しをやり直す。基準HEAD、ブランチ、生成時刻、ツール版を台帳に記録する。
2. Git tree全体から対象パスと件数を再計算し、実データを読んで各項目を A.現行・ライブ、B.現行・履歴、C.旧形式・要移行、D.一時・削除可能、E.互換コード に分類する。パス名やファイル名だけで分類しない。
3. 台帳は機械可読JSONとし、各対象に `path`、blob SHA、種別、分類、状態判定根拠、参照元、移行/保持/削除理由、実施結果を記録する。移行中に再生成でき、同じHEAD・同じ入力で差分が再現できること。
4. 移行ツールはdry-run、冪等、対象件数・変更理由の出力を備える。2回目の適用で変更0件になることを専用検査で確認する。科学的本文を扱う変換は自動補完せず、要人手読解として出力する。
5. **ライブ移行前には短時間の書込凍結を実施する。** その直前にmainのHEADと全対象のblob SHAを再取得する。稼働中claimについて、完了、期限切れ、または耐久handoffのいずれかを個別に確認する。active claimが残る、処理結果待ちがある、またはHEADが動いた場合はそのレーンの移行・削除を開始しない。凍結解除後は再棚卸しを行い、台帳と実体の一致を確かめる。
6. **削除作業は作業ブランチで行い、mainへ直接書かない。** 各フェーズを独立commitにし、差分・台帳・テスト結果をレビューできる状態にする。旧データ削除前に、必要な終端状態、集計値、ID、必要なら元blob SHAを保持する。Git履歴を書き換えない。
7. 復旧不能項目は黙って破棄しない。理由、対象識別子、保持した要約、復旧を試した経路を台帳へ記録し、削除判断をレビュー可能にする。

## 4. フェーズ

### 0 — 基準点と保護
この文書冒頭のHEADを参照し、実施時点の最新mainへ追随する。作業ブランチの親commitを移行基準として固定し、旧形式削除は行わない。

### 1 — データ契約表と棚卸し
各データ種別について保存場所、現行producer/reader、必須フィールド、種別固有schema、過去形式、参照関係、一時/永続の別、移行方法、削除可能になる互換コードを表にする。全対象のA〜E台帳を生成する。`legacy_remaining` は旧形式の意味あるデータ、旧形式reader/producer、旧手順・旧専用試験を分けて集計する。全て0になるまで最終切替しない。

### 2 — 論文1,024件
まず全論文を実件数で再計数する。nullable項目、明示情報から確定できるメタデータ、正規化可能なfrontmatterは既存normalizerを確認して移行する。著者・出版情報は本文/一次資料に根拠がある場合だけ復元する。
`list_summary`、代表結果、手法、評価条件、限界、既存研究との差、一次資料に基づく実装状態は機械生成しない。内容が不足する論文は通常Research相当の読解・監査を経て更新する。
全論文に対して `check_repository.py`、`audit_paper_quality.py`、`audit_list_summary_quality.py`、`audit_overview_results.py` を実行し、FAIL 0件を確認する。その後に限り `list_summary.py` の旧fallbackを削除する。

### 3 — ライブ状態
jobs、claims、claim requests/results、records、research-preflight、submissions/results、run-state、Discovery preloadを種別別の現行writer契約へ揃える。旧claim alias、lease、route/transport field等を明示的に分類する。自動修復で旧値を隠さず、不正な旧ライブ入力は拒否する。各移行後に参照整合・重複ID・未完了状態を検査する。

### 4 — 完了履歴の縮約と旧bundle処理
`archive/transport`、fallback-archive、fallback-failed等について、現行コードが参照するかを静的検索とreader実行経路で確認する。参照されない終端履歴は必要な識別子・集計値・最終状態・必要なblob SHAだけを履歴台帳へ残し、個別輸送データを削除できる。
旧bundleは、(a)現行不変提出へ変換、(b)終端状態として確定、(c)復旧不能の根拠を記録して破棄、のいずれかに決着させる。「将来再生するかもしれない」は旧readerを残す理由にしない。現行Library退避経路は対象外として保護する。

### 5 — 旧形式生成能力の遮断
コード、workflow、文書、試験、生成物を調べ、旧形式のproducerが0件であることを確認する。対象語は固定 `chat-inbox.json`、旧record-bank alias、旧Scheduled Chat worker名、旧lease、旧fallback envelope、`## 一文要約`、旧schema値、廃止path等。ヒットは「現行機構」「移行記録として必要」「削除漏れ」に分類し、根拠を残す。

### 6 — 互換コード・旧手順の撤去
データが0件になった後、一覧旧fallback、固定chat inbox reader、record-bank alias、claim lease normalizer、旧Discovery envelope救済、その他旧reader、移行専用コード、旧互換試験の順に削除する。Library fallbackの現行部分は残す。
`worker-router.md` は現行正常系と現行障害復旧系だけを記述する。`queue-v10.md` は現行文書でも互換由来名を明記している。名前自体も撤去する場合は、参照を全更新したうえで `implementation-index.md` へ改名し、リンク切れ検査を通す。workflow v10が現行である間は番号自体を削除理由にしない。

### 7 — 拒否試験と最終検査
旧形式を受け入れる旧専用試験は、旧形式入力の明示拒否を検査する試験へ置換する。少なくとも旧chat inbox、旧record-bank alias、旧lease、list_summary欠落論文、現行schema外ライブ入力、移行専用field生成、既知legacy pathを検査する。
構造検査、4種の論文検査、全回帰試験、主要GitHub Actionsを実行する。repository-wide検索は許容リスト付きで評価し、単なる文字列ヒット数を0件条件にしない。Research / Discovery / Auditを各1サイクル以上、通常workerで実行し、新形式だけが生成されることを確認する。

## 5. 削除可否ゲート

次のすべてを満たすまで旧reader・移行コード・履歴を削除しない。

- 最新mainと対象台帳が同じHEAD/blob SHAを示す。ライブ書込凍結時にactive claim/result待ちがない。
- 意味のある旧データの移行・終端確定・記録付き破棄が完了し、台帳に未決事項がない。
- 現行producerが旧形式を生成しないことをコードとworkflowで確認した。
- 全公開論文の構造・品質検査がFAIL 0件。
- 現行形式だけの全回帰試験が成功し、旧形式拒否試験も成功。
- 現行Library退避機構が維持されている。
- Research / Discovery / Audit各1サイクルで旧形式が再生成されない。
- legacy残存台帳で削除漏れ・未分類・未決が0件。

いずれかが失敗したら該当フェーズだけ止め、失敗対象と安全な再開点を記録する。成功していない受入条件を完了扱いにしない。
