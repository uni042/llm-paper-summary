# Worker router — Library-first workflow v12

この文書は、LLM論文サーベイのScheduled Chat / Work系処理が読む唯一の人間向け実行正本である。v12では責務を次の3段に分離する。

1. Scheduled workerは探索・読解・分類を行い、完成成果をChatGPT Libraryへ保存する。
2. Survey GitHub ImportはLibrary成果をGitHub受信箱へ**そのまま転送**する。
3. GitHub側の受信箱プロセッサが、最新mainでidentity解決、重複排除、正規配置、precheck、relevance反映を行う。

旧direct-GitHub worker運用は履歴資料であり、新規通常runへ復活させない。

## 0. 正本順位と責務

正本順位:

1. そのrunに対するユーザーの明示指示
2. 同一HEADの本書
3. Library用途別正本
   - \`/LLM-paper-summary-library-first/WORKER-LIBRARY-PROCEDURES.md\`
   - \`/LLM-paper-summary-library-first/PAPER-QUALITY-GUIDE.md\`
   - Survey GitHub Import用 \`github-import-procedure.md\`
4. Scheduled Task / Work task本文のブートストラップ
5. 退役資料

| 実行主体 | GitHub | Library | 主責務 |
|---|---|---|---|
| \`scheduled-chat-00\` / \`scheduled-chat-30\` | read-only | read/write | 探索・読解・分類・完成成果保存・自分のrun由来一時物掃除 |
| Survey GitHub Import | create/read | read/delete | Library成果をGitHub受信箱へbyte-preserving転送し、転送確認後にLibrary原本を整理 |
| GitHub import inbox processor | Actions内read/write | なし | 最新mainでidentity解決、Research配置、Discovery precheck/relevance/submission、GitHub側掃除 |
| 通常チャット | 原則read-only | read/write | 明示された監査・回収・保守 |

Scheduled workerはGitHubへのclaim、reservation、submission、result、handoff、health-probe、worker-control、制御ファイル更新を行わない。Survey GitHub Importも論文内容や候補の意味判定を行わず、受信箱への転送だけを担当する。

## 1. 固定identityと開始時読取

### :00
- \`worker_id=scheduled-chat-00\`
- \`scheduled_slot=00\`
- worklist: \`.survey/work-queue/worker-worklist-00.json\`

### :30
- \`worker_id=scheduled-chat-30\`
- 通常 \`scheduled_slot=30\`
- worklist: \`.survey/work-queue/worker-worklist-30.json\`
- 08:30 JSTはmaintenance専用run

各通常runは最新main HEADを取得し、同じHEADから本書、自分のworklist、必要な系統READMEを読む。Research本文作成時だけ最新templateとLibraryの品質ガイドを読む。

ユーザーの明示指示なしにScheduled Taskを停止・無効化・削除せず、schedule・通知設定も変更しない。

## 2. 候補順序

Research / Audit候補はworker専用worklistを入口にする。候補はリスト末尾から上方向、すなわちrankの大きいものから処理する。skip、重複、既処理、取得不能があってもその位置から上方向の次候補へ進む。

専用worklistが欠損・古い・空の場合だけ最新mainの正規poolをread-onlyで参照する。

## 3. identityの責務

候補を読む際のcanonical identityは次の優先順で使う。

1. arXiv ID
2. DOI
3. OpenReview ID
4. 正規化一次資料URL

Scheduled workerは、無駄な再読解を避けるためGitHub/Libraryの既知状態をread-onlyで参照してよい。ただし、**「最新mainに同一identityがあるためGitHubへ新規createしてよい／いけない」という最終判断はScheduled workerもSurvey GitHub Importも行わない。**

最終identity判断はGitHub受信箱プロセッサが、処理直前の最新mainに対して \`.survey/scripts/resolve_paper_identity.py\` と既存Discovery precheckを用いて行う。

したがって、Library保存済み成果は「保存時点では未収録だった」ことを証明する必要はない。転送後にmainで既収録と判定された場合はGitHub側で安全にno-op/filteredとして終端する。

## 4. モード判定

開始時の実効候補在庫を次で扱う。

- \`G\`: 最新main上の未処理候補在庫
- \`D\`: Libraryに未転送のDiscovery acceptで、明らかにまだResearch化していない件数
- \`R\`: Libraryに完成Researchがあり、G側にまだ未処理候補として残る件数
- \`E = G + D - R\`

500件の閾値から明らかに離れている場合は厳密全件照合をしない。

- \`E > 500\` → Research
- \`E <= 500\` → Discovery
- 概算でも境界が曖昧ならDiscovery

run中に在庫が変化してもモードは固定する。

## 5. Discovery

### 5.1 ノルマ

新規canonical identity 10件を本文確認まで行い、各件を次のどれかへ最終分類する。

- \`accept\`
- \`unrelated\`
- \`borderline\`

タイトル・要旨だけで確定しない。本文取得不能で判定未完了の候補は10件へ数えず補充する。acceptだけを10件集めるために基準を緩めない。

### 5.2 Library保存形式

v12以降のDiscovery通常runは、**1 run = 1 immutable JSON**だけを正規成果として保存する。

推奨path:

\`/LLM-paper-summary-library-first/discovery/discovery-YYYYMMDD-HHMM-<worker_id>.json\`

1ファイルにそのrunの10件すべてを \`records[]\` として含める。accept / unrelated / borderlineを別Library台帳へ分割しない。

必須top-level:

- \`schema_version\`
- \`artifact_type: "discovery_run"\`
- \`worker_id\`
- \`run_key\`
- \`reference_main_sha\`
- \`record_count\`
- \`records[]\`

各recordの必須項目:

- \`classification\`
- \`canonical_id\`
- \`identity_tokens\`
- \`title\`
- \`reason\`
- \`source_url\`
- \`body_check\`
- \`first_checked_at\`
- \`last_checked_at\`
- \`linked_from\`

取得できる場合は \`worklist_rank\` 等を追加してよい。

**共有3分類JSONやworker別relevance台帳へ新規追記しない。** 既存の旧形式ファイルは移行対象として残し、別途ユーザーが依頼した移行作業でv12形式へ変換する。

### 5.3 保存直前

同run内重複とLibrary内の明白な重複だけを除く。GitHub最新mainに同一identityが存在するかの最終判定はここで必須にしない。GitHub側precheckへ委譲する。

保存後はLibraryから再取得し、JSON parse、\`record_count == len(records)\`、10件のidentity一意性を確認する。

## 6. Research / Audit

Research runでは新規完成Research Markdownを3件Libraryへ保存する。

保存先:

\`/LLM-paper-summary-library-first/research/<paper>.md\`

1論文1Markdownとし、最新templateと \`PAPER-QUALITY-GUIDE.md\` に従う。

必須内容:

- canonical identity
- \`summary\`
- \`list_summary\`
- 書誌
- \`## 概要\`
- 問題設定
- 手法
- 評価条件・主要結果
- 既存研究との差
- 限界
- 一次資料

一次資料読解 → 固有事実抽出 → 執筆 → 固有性セルフレビュー → Library保存の順を守る。

Research worker自身は厳密な機械監査をノルマにしない。ただし、極端に短い原稿、汎用テンプレート文、比較条件のない数値、主要機構の説明不足を完成扱いにしない。

GitHub側受信箱プロセッサが保存済みMarkdownに対して公開完全性・日本語率の機械監査を行う。FAILした原稿はGitHub側blockedへ保全される。

最終適用先が学習工程そのものの高速化・省メモリ化で凍結対象なら新規Researchへ回さない。

## 7. Library保存失敗時

Library保存不能でも完成成果を破棄しない。

- Research: 完成MarkdownをScheduled Chatへ完全添付
- Discovery: 10件全件を含む完成JSONをScheduled Chatへ完全添付

後続runでLibraryへ回収できたら正規pathへ保存し、再取得確認後に退避コピーを重複扱いにする。

GitHub writeをLibrary失敗回避手段として使わない。

## 8. 毎時Scheduled workerのLibrary掃除

各通常runの最後に、自分が扱った範囲だけを掃除する。目的は「未転送完成成果だけが残る」状態へ近づけることであり、他workerの未確認成果を消すことではない。

### 常時保持

- \`WORKER-LIBRARY-PROCEDURES.md\`
- \`PAPER-QUALITY-GUIDE.md\`
- \`github-import-procedure.md\`
- 未転送の完成Research Markdown
- 未転送のv12 Discovery run JSON
- GitHub反映とは無関係なユーザー資料

### run終了時に消してよいもの

自分のrunについて以下の条件が確認できたものだけ。

- 正規Library成果へ統合済みの一時コピー
- 同一bytes / 同一canonical identityの重複退避
- 本文抽出用に作った一時PDF・HTML・画像キャッシュ
- 中間JSON、下書き、品質確認用一時ファイル
- 正規Library保存後に残ったScheduled Chat回収用コピーをLibraryへ二重保存したもの
- 空になった自分専用の一時folder

### 消してはいけないもの

- GitHubへまだ転送されていない完成Research / Discovery
- 保存成否が不明な成果
- 他workerが作った未確認成果
- 手順書・品質ガイド
- 既存legacy成果。v12移行が明示されるまで自動変換・自動削除しない

掃除前後で対象folderを再listし、完成成果件数と削除対象を確認する。

## 9. Survey GitHub Import

Survey GitHub Importは内容取込者ではなく**転送者**である。

### 9.1 Research転送

Library \`research/*.md\` を1件ずつ読み、内容を変更せず:

\`.survey/import-inbox/pending/research/<unique>.md\`

へcreate-onlyでコピーする。

### 9.2 Discovery転送

v12 Discovery run JSONを内容変更せず:

\`.survey/import-inbox/pending/discovery/<unique>.json\`

へcreate-onlyでコピーする。

unique名は \`<library_file_id>--<original-basename>\` 等、衝突しない値を使う。

### 9.3 転送完了条件

GitHub create応答だけでLibrary原本を削除しない。まず同じpending pathをGitHubから再取得し、**byte/hash一致**を確認する。processorが先に進んでpendingが消えていた場合は、同名のwaiting/blocked payloadを確認し、それも既に終端済みなら `results/<type>/<pending-stem>.json` の `source_sha256` とLibrary原本のSHA-256を照合する。

pending / waiting / blocked の同一bytes、またはresult receiptの同一 `source_sha256` を確認できた後はGitHubが耐久原本を所有するため、そのLibrary成果を削除してよい。最終paper/candidate処理の完了をLibrary側で待たない。

既存pathに別bytesがある場合は上書きせず別unique名で再送する。

## 10. GitHub import inbox processor

正本仕様は \`.survey/import-inbox/README.md\`。

### Research

GitHub Actionは毎回最新mainから処理を再計算する。

1. Markdown機械監査
2. repository-wide identity resolver
3. represented → \`already_represented\`、既存本文を上書きしない
4. not_found → canonical inference lineageへ新規配置
5. post-write identity再確認
6. survey view再生成
7. ready Research job reconciliation
8. 成功pending削除、失敗は \`blocked/research/\` 保全

Researchの既定操作は **insert-if-absent**。既収録本文の更新は通常importとは別の明示保守タスクで行う。

### Discovery accept

1. Library recordから安定IDを取り出す
2. schema-v3 \`candidate_id_lookup\` precheck requestを作成
3. 専用precheck workflowが最新snapshotで既収録・既候補・既却下を判定
4. workflowの \`allowed_records\` だけを0〜5件の通常Discovery submissionへ送る
5. queue側の最終重複排除を通す

これにより「最新mainに同一識別子があるか」はGitHub側へ完全委譲される。

### Discovery unrelated / borderline

既存 \`reference-curation/requests/\` 経路へ送り、正規relevance ledger processorに処理させる。

## 11. Survey GitHub ImportのLibrary掃除

アップロードワーカーは毎回Library転送後に掃除を行う。

### 削除条件

次をすべて満たす成果だけLibraryから削除する。

1. GitHub pending inboxへcreate済み
2. pendingが残っていれば同pathのbytes/hash一致を確認済み
3. pendingが既に進んでいれば同名waiting/blockedのbytes一致、または `results/<type>/<pending-stem>.json` の `source_sha256` 一致を確認済み
4. 転送対象のLibrary成果identityを取り違えていない

最終paper/candidateへの反映完了は削除条件ではない。

### 掃除対象

- 転送確認済みResearch原本
- 転送確認済みv12 Discovery JSON
- 転送済み成果の不要な二重コピー
- 移行作業で完全変換・転送確認済みとなったlegacy成果
- 空になった旧成果folder

### 常時保持

- 3本の運用正本
- 転送未確認成果
- 転送失敗成果
- 変換未実施のlegacy成果
- 別用途のLibrary資料

一つの成果の転送失敗で他の独立成果を止めない。

## 12. legacy移行

現時点でLibraryに存在する共有3分類ファイル、worker別relevance台帳、旧run成果等は自動削除しない。

別途移行を依頼されたとき、canonical identityで重複排除し、v12のimmutable Discovery JSONへ変換してから受信箱へ転送する。変換元は、GitHub pending copyのhash一致確認後にだけ削除する。

## 13. 08:30 maintenance

08:30 JSTの\`scheduled-chat-30\`は通常Research / Discoveryへ置換せず、maintenance専用runとする。GitHub反映が必要な完成変更はLibraryへ耐久保存し、Survey GitHub Importへ渡す。

## 14. 報告

Scheduled worker:

- Library-first / GitHub read-only
- 確認main SHA
- モードと在庫判定根拠
- Research完成件数、またはDiscovery 10件内訳
- Library保存結果
- run終了時掃除内容
- 退避・未完了

Survey GitHub Import:

- Research/Discovery転送数
- GitHub pending再取得・hash一致数
- Library削除数
- 転送失敗・競合数
- legacy未移行件数
- 最終確認main SHA

GitHub Actionの最終状態は \`.survey/import-inbox/results/\` とblocked payloadを正本とする。

## 15. 退役資料

旧direct-GitHub worker、旧共有3分類台帳への新規追記、Library側でのprecheck receipt生成、Library側でのlatest-main create/update判定は新規通常runでは使わない。
