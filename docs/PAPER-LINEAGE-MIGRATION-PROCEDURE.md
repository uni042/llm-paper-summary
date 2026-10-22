# 論文系統の分類とpath移行

この手順は、論文を新設または既存の系統へ再分類し、repository上のpaper pathを移す標準手順です。技術分類と物理移動は別の判断です。引用・共引用は候補発見に使えますが、採否と移動先は一次本文の主貢献、手法、評価、制約で決めます。

## 1. 最新状態と候補を固定する

1. 最新mainのSHAを固定し、対象のproject指示・paper workflow・identity、citation、path resolver、系統proposalの実装を読みます。
2. 99-other-inference-systemsと、候補が近い既存lineageの双方を監査します。候補ごとにcanonical ID、全alias、現在path、一次資料URLと確認節、主貢献、移動先と根拠、引用・内部path link、main SHAを記録します。
3. paper、identity、citation、STATUS、README等を書き得る全active/queued workflowを調べ、対象paperのResearch job、submission、retryも確認します。最新mainとSTATUSの一致、最低5分のwriter-free window、対象pathを書き得るjobがないことを満たさなければwriteを始めません。
4. source SHA、alias、path衝突、inbound citation、相対linkを照合します。identity不一致または一次根拠不足は移動manifestから外します。

## 2. 新しい系統の提案

既存系統が主貢献を十分表すならそこへ分類します。新系統は技術的に一貫したcluster、具体的な包含・除外境界、隣接系統との違いが必要です。10本程度は調査の目安であり、自動作成基準ではありません。

新系統は公式Discoveryの `lineage_proposal` 経路で提案します。現在のproposal gateは、high confidence、一次資料で確認したsupportが4本以上、repository収録済みsupportが2本以上、neighbor lineageが1〜3件です。各提出前に最新mainのgateとround上限を読み直します。registry・生成README・taxonomy indexを手編集しません。intake receiptだけで完了とせず、submission結果のproposal、registry、proposal ledger、生成READMEを照合します。新系統登録後もpaperのpath移行は別途行います。

## 3. manifestと移行CLI

mainに入った `.survey/scripts/paper_lineage_migration.py` を使います。manifestは `source_main_sha` と各entryのrepository相対 `old_path` / `new_path`、`canonical_id`、frontmatterと一致する `aliases`、元内容の `expected_sha256` を含めます。移行対象全件をひとつのbounded batchに含め、reviewします。CLIは最大25件・元本文合計64 MiBまでです。

```powershell
python .survey/scripts/paper_lineage_migration.py dry-run --manifest migration.json
python .survey/scripts/paper_lineage_migration.py apply --manifest migration.json
python .survey/scripts/paper_lineage_migration.py recover --transaction <32桁のtransaction-id> --action rollback
```

まず最新mainから隔離branchを作り、migration manifestをcurrent HEADへpinします。dry-runはread-onlyです。ID、hash、snapshot、aliases、identity delta、path/symlink/target、既存paper inventoryとMoved suffix衝突を検証し、失敗したらapplyしません。CLIが確認しないactive-job、workflow writer、citation、相対linkは担当者が別に確認して記録します。

applyは同じ本文bytesをnew pathへ置き、old pathをfrontmatterなし・先頭非空行 `# Moved` のstubにし、ignored-stub entryを加えてidentity snapshotを既存builderで再生成します。jobs、submissions、results、citation source records、paper本文は更新しません。scriptはjournalを使ってrollbackを試みます。復旧はcurrent HEADがjournalのsource SHAと一致する場合だけ実行できます。中断後はbranch/HEADを固定してdry-run結果、old/new path、snapshot、journal、temporary bytesを照合してからrollbackします。bytesやpathが曖昧なら手で削除・再試行せず停止します。

## 4. branch検証、commit、readback

applyと検証は非公開branchで行います。CLIは複数fileとsnapshotをOSレベルで原子的に置換せず、repository-wide writer lockも取得しません。そのためwriter-free gateを保ち、検証完了までHEADを変えません。検証が失敗したらHEADを固定したままCLIのrollbackを行い、復旧を検証してから調査をやり直します。

作業中にmainが進んだ場合は、branchのbaseから最新mainまでのcommitと変更pathを比較します。変更がSTATUSや独立したwork-queue等に限られ、候補paper、identity snapshot/delta、citation、taxonomy、生成indexの前提に触れなければ、そのPRを最新mainへそのまま出してCIとmergeabilityを確認します。無関係なcommitをmigration branchへ取り込む必要はありません。候補paper、alias、identity、citation evidence、taxonomyまたは移動先indexが変わった場合は、そのbatchを最新mainへrepinし、manifestとdry-runを作り直します。status/work-queue writerが終わった後にSTATUS整合性とwriter-free条件も再確認します。各PRのmerge後は、その時点のmainから次batchを作ります。

同一候補commitで次を確認します。

- 各canonical IDがnew path一件に解決し、aliasが同じIDを指す。
- new pathのbytesとsource SHAが一致し、old stubが条件どおりでpaper inventoryから除外される。
- citation node/edge、内部link、identity snapshot、lineage membership/countが意図どおりである。
- job/result履歴は不変。quality、metadata、consistency、STATUS、README/indexのcheckが通る。
- branchから固定commitをreadbackし、path・bytes・SHAを再照合する。

ひとつでも失敗すればcommit/公開せず、次batchへ進みません。全check合格後にだけ移行状態をひとつのcommitにまとめ、承認済みの通常review/write経路へ出します。commit SHA、readback、hash、check、未解決制約をreportへ記録します。
