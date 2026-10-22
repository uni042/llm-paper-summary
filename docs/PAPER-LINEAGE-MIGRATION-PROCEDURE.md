# 論文系統の分類とpath移行

この手順は、論文を新設または既存の系統へ再分類し、repository上のpaper pathを移す標準手順です。技術分類と物理移動は別の判断です。引用・共引用は候補発見に使えますが、採否と移動先は一次本文の主貢献、手法、評価、制約で決めます。

## 1. 最新状態と候補を固定する

1. 最新mainのSHAを固定し、対象のproject指示・paper workflow・identity、citation、path resolver、系統proposalの実装を読みます。
2. 99-other-inference-systemsと、候補が近い既存lineageの双方を監査します。候補ごとにcanonical ID、全alias、現在path、一次資料URLと確認節、主貢献、移動先と根拠、引用・内部path link、main SHAを記録します。
3. active/queued workflowと対象paperのResearch job、submission、retryを確認します。全repository共通のwriter-free windowは要求しません。候補source/destination、またはその分類根拠に関わるidentity/citation/taxonomyを更新中の処理だけを競合対象として扱います。別pathだけを更新する処理が動いていても、隔離worktreeでbatchを準備してPRを作れます。
4. source SHA、alias、path衝突、inbound citation、相対linkを照合します。identity不一致または一次根拠不足は移動manifestから外します。

## 2. 新しい系統の提案

既存系統が主貢献を十分表すならそこへ分類します。新系統は技術的に一貫したcluster、具体的な包含・除外境界、隣接系統との違いが必要です。10本程度は調査の目安であり、自動作成基準ではありません。

新系統は公式Discoveryの `lineage_proposal` 経路で提案します。現在のproposal gateは、high confidence、一次資料で確認したsupportが4本以上、repository収録済みsupportが2本以上、neighbor lineageが1〜3件です。各提出前に最新mainのgateとround上限を読み直します。registry・生成README・taxonomy indexを手編集しません。intake receiptだけで完了とせず、submission結果のproposal、registry、proposal ledger、生成READMEを照合します。新系統登録後もpaperのpath移行は別途行います。

## 3. manifestと移行CLI

mainに入った `.survey/scripts/paper_lineage_migration.py` を使います。manifestは `source_main_sha` と各entryのrepository相対 `old_path` / `new_path`、`canonical_id`、frontmatterと一致する `aliases`、元内容の `expected_sha256` を含めます。移行対象全件をひとつのbounded batchに含め、reviewします。CLIは最大25件・元本文合計64 MiBまでです。

```powershell
python .survey/scripts/paper_lineage_migration.py refresh-manifest --manifest reviewed.json --output refreshed.json --report refresh-report.json
python .survey/scripts/paper_lineage_migration.py dry-run --manifest refreshed.json
python .survey/scripts/paper_lineage_migration.py apply --manifest refreshed.json
python .survey/scripts/paper_lineage_migration.py recover --transaction <32桁のtransaction-id> --action rollback
```

manifestの元ファイルはレビュー済み計画として不変保存します。mainとPRのpath差分が独立していれば既存PRをそのまま進めます。共有identity indexなどが重なった場合は、最新 `origin/main` から新しい隔離branch/worktreeを作り、`refresh-manifest` で計画を再照合します。このコマンドはcleanな最新 `origin/main` checkoutだけで動き、元の各論文本文hash、canonical ID、frontmatter alias、identity snapshotのpath/hash/alias mappingを検証します。本文やidentityが変わった項目、sourceが消えた項目、移動先が埋まった項目は新manifestから外し、理由をreportへ出します。本文hashやaliasを自動更新して古い分類根拠を引き継ぐことはありません。出力manifestとreportは上書きせず、repository外に保存します。全項目が除外された場合はmanifestを作りません。

更新されていない項目は新しい `source_main_sha` のmanifestへ再pinされるので、旧branchのaggregate identity snapshotを手で合成せず、公式CLIが最新mainの全inventoryからindexを再生成します。refresh後に通常の `dry-run` を実行し、ID、hash、snapshot、aliases、identity delta、path/symlink/target、既存paper inventoryとMoved suffix衝突を確認してからapplyします。CLIが確認しないactive-job、同じpaper pathを書き得るworkflow、citation、相対linkは担当者が別に確認して記録します。

applyは同じ本文bytesをnew pathへ置き、old pathをfrontmatterなし・先頭非空行 `# Moved` のstubにし、ignored-stub entryを加えてidentity snapshotを既存builderで再生成します。jobs、submissions、results、citation source records、paper本文は更新しません。scriptはjournalを使ってrollbackを試みます。復旧はcurrent HEADがjournalのsource SHAと一致する場合だけ実行できます。中断後はbranch/HEADを固定してdry-run結果、old/new path、snapshot、journal、temporary bytesを照合してからrollbackします。bytesやpathが曖昧なら手で削除・再試行せず停止します。

## 4. branch検証、commit、readback

applyと検証は最新mainから作った非公開branch/worktreeで行います。CLIは複数fileとsnapshotをOSレベルで原子的に置換せず、repository-wide writer lockも取得しませんが、隔離worktree内では他workflowのcheckoutやfileを変更しません。HEADとindexを固定して検証し、失敗したらCLIのrollbackを行って復旧を検証します。別pathの更新が続いても、paper batchの調査、apply、PR作成を止めません。

作業中にmainが進んだ場合は、branchのbaseから最新mainまでのcommitと変更pathを比較します。変更pathがbatchと重ならず、分類前提にも触れない場合は古いbranchをrebaseせず、そのPRをそのまま提出できます。paper path、identity snapshot/delta、citation evidence、taxonomyまたは生成indexが重なった場合は、競合を手作業で解消せず、新しい最新main worktreeで `refresh-manifest` → `dry-run` → `apply` を行い、差し替えPRを作ります。元PRは差し替えPRのCI/readbackが確認できた後に閉じます。PR作成前後のmain更新はpath比較をやり直し、対象pathに変更がなければ無関係なcommit待ちはしません。merge直前には現在のmain、CI、active writerが同じ対象pathを変更していないことを再確認し、head/baseが変われば再比較します。各PRのmerge後は、その時点のmainから次batchを作ります。

同一候補commitで次を確認します。

- 各canonical IDがnew path一件に解決し、aliasが同じIDを指す。
- new pathのbytesとsource SHAが一致し、old stubが条件どおりでpaper inventoryから除外される。
- citation node/edge、内部link、identity snapshot、lineage membership/countが意図どおりである。
- job/result履歴は不変。quality、metadata、consistency、STATUS、README/indexのcheckが通る。
- branchから固定commitをreadbackし、path・bytes・SHAを再照合する。

ひとつでも失敗すればcommit/公開せず、次batchへ進みません。全check合格後にだけ移行状態をひとつのcommitにまとめ、承認済みの通常review/write経路へ出します。commit SHA、readback、hash、check、未解決制約をreportへ記録します。

### 待機中の候補台帳と再利用可能な分類

反映待ちと分類を混ぜないため、候補台帳はcanonical ID単位で管理し、各IDを次のどれか一つに置きます。

- `pending-reflection`: apply済みだが、反映中PRがまだmainに入っていない。
- `still-in-99`: 現在のidentity indexで99-other配下にあり、未apply。
- `already-placed`: 現在pathが提案先と一致し、追加移動が不要。
- `reviewed-retain`: 一次本文を確認し、99-otherまたは別系統に残す判断をした。
- `neighbor-pull-in`: 99-other外にあるが、近接系統から別系統へ移す候補。

古いmanifestのentry数を「残り件数」と見なしません。まず全候補をcanonical IDで重複排除し、最新のidentity indexで各IDの実pathを照合して上の状態へ分けます。`pending-reflection` と `already-placed` は次の99-other残数に含めず、`neighbor-pull-in` は99-other候補と別枠で数えます。source SHA、index SHA、照合日も台帳へ記録し、mainが変わったらpath判定だけを再実行します。過去manifestの重複や既移動paperを新しい候補と誤認しません。

引用ネットワークは仕分け対象を絞るための優先順位付けに使います。citation graphのsnapshot SHAと集計条件を保存し、引用先lineageへの偏りが強いpaperから一次本文を確認します。引用先件数だけで移動を確定せず、主貢献・中核手法・評価対象がそのlineageの包含境界に合うかを確認します。citation graphが更新されたら候補順位を再計算できますが、一次資料確認済みの判断は根拠URL/version・確認節・判断理由とともに引き継ぎ、同じ本文を読み直しません。根拠versionや内容が変わったpaper、判断境界に近いpaperのみ再確認します。

候補レビューの成果は、反映中manifestとは別のimmutable planへ保存します。1行あたりcanonical ID、全alias、現在path、一次資料URLとversion/節、短い主貢献、決定（移動先/保持/要追加調査）、隣接系統との境界、source/index snapshotを必須にします。引用ランキング、要旨だけの判断、未確認のID/pathは「分類済み」に数えません。新系統の候補は、既存系統への移動候補と混ぜず、共通の技術的中核・除外境界・隣接lineageを示せるclusterとして束ね、概ね10件を調査の目安に一次本文を比較します。

反映待ち中はこのimmutable planの作成と読み取り専用レビューを進めます。前batchがmainに入った時点で、ledgerの重複IDと現在pathを再照合し、未反映・未移動の候補だけを次batchの `refresh-manifest` に渡します。refreshが返す全rejectを理由別に確認し、分類根拠が古いものは一次資料から再審査します。`dry-run` が有効な候補だけapplyし、反映後は実pathを台帳へ反映して次の待機区間へ進みます。

### 反映待ち中の並行運用（実績に基づく標準 cadence）

反映待ちを主作業にしません。反映処理は「出す・必要時に一度確認する・イベントまたは次の作業区切りで再確認する」に限定し、空いた時間を候補の読解と分類へ使います。

1. batchのPRを出したら、PR URL、head SHA、CI状態、対象path集合、現在main SHAを台帳へ記録し、PRの完了を待つ間に次の10〜20件を独立したimmutable review planへまとめます。planは候補IDの重複を除き、99-otherからの候補と近接lineageからの引き抜き候補を両方含めます。batchサイズは一次本文の確認に使える時間で調整し、未読候補を「分類済み」に数えません。
2. 次候補の優先順位はcitation graphとrepository内引用先lineageから作ります。引用は読む順序を決める信号に限り、各論文は一次本文の主貢献・手法・評価・制約を確認して分類します。既読本文のURL/version/確認節・根拠はplanから再利用し、同じ本文を読み直す代わりに未読候補へ進みます。
3. PRのCIが実行中なら、短い間隔のpollingやPR画面の連続確認をしません。独立した分類単位（目安10件）を終えた時、CI完了通知を受けた時、または次にbatchを作る必要が生じた時に状態を確認します。失敗・競合・レビュー依頼が出た場合だけ、その原因に必要な確認へ切り替えます。mainに無関係なpath更新があっても分類を止めず、path overlapを確認してから次の判断をします。
4. 次候補の読解中はGitHubへのpaper変更を行わず、分類planと証拠だけをローカルに保存します。反映PRがmainに入る前に次batchをapplyしません。main反映後、最新identity indexとlineage pathで候補を再照合し、既移動・重複・レビュー済み保持を除いて残った候補だけを新しいmain worktreeで `refresh-manifest` に渡します。これにより待機中に分類を進めながら、古いpath/hashを使った移動を防ぎます。
5. `refresh-manifest` のrejectは全件を理由別に確認し、候補planのstateを `already-placed`、`reviewed-retain`、再審査または次batch対象へ更新します。rejectされた項目を機械的に再投入しません。`dry-run` 後にapplyできるものだけを反映し、PR作成まで進んだら次の分類blockへ戻ります。

2026-10-23のbatch 2では、最新mainへのrefreshが25件保持・0件rejectとなり、dry-runとapply/readbackがすべて通りました。一方で、全体buildは月次表示を含むsurvey・training系READMEまで広く更新しました。以後、build後は移行対象のinference README、inference index/comparison、identity index、必要な上位件数READMEに変更を絞り、他カテゴリの差分は内容上必要と説明できない限り当該branchから除外します。変更理由が日付の経過だけの差分は分類移行のPRへ混ぜず、生成物の再生成時期を別途扱います。広い生成差分が出ても、それを理由に候補読解を止めず、生成差分の切り分けはPR準備の短い工程として行います。
