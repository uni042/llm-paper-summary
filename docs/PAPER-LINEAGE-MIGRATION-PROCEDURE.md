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

mainに入った `.survey/scripts/paper_lineage_migration.py` を使います。manifestは `source_main_sha` と各entryのrepository相対 `old_path` / `new_path`、`canonical_id`、frontmatterと一致する `aliases`、元内容の `expected_sha256` を含めます。移行対象をひとつのbounded batchにまとめてreviewします。従来どおり通常のbatchは25件以下で作成し、明示的に準備・reviewしたmanifestでは必要に応じて最大100件まで指定できます。CLIの上限は100件・元本文合計64 MiBです。100件は1つのtransactionの上限であり、複数transactionを独自に束ねません。各batchは1つのsource main SHAにpinし、次batchは前batchがmainへ受け入れられてから、その時点のmainで作ります。件数上限を広げてもhash・identity・alias・pathの全件preflight、journal、snapshot検証、recoveryは省略しません。

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
