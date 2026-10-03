# Worker router — Library-first workflow v15

この文書は、LLM論文サーベイのScheduled Chat / Work系処理が読む唯一の人間向け実行正本である。v13ではLibrary-first責務分離を維持したまま、Discovery / Research候補の重要度優先と全収録論文の前方引用カバレッジ巡回をGitHub側自動化へ追加する。

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
| \`scheduled-chat-00\` / \`scheduled-chat-30\` / \`scheduled-chat-45\` | read-only | read/write | 探索・読解・分類・完成成果保存・自分のrun由来一時物掃除 |
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
- 08:30 JSTはLLM / framework日次更新専用run

### :45
- \`worker_id=scheduled-chat-45\`
- \`scheduled_slot=45\`
- worklist: \`.survey/work-queue/worker-worklist-45.json\`
- :00 と同じ通常Research / Discoveryフローを使う。08:30日次更新専用分岐は持たない

3 workerの専用worklistは同じ正規候補列から決定的な3-way round-robinで分割し、十分な候補在庫がある限り相互に重複させない。Library側は共通正本・共通保存先を使い、worker専用の可変台帳は追加しない。

各通常runは最新main HEADを取得し、同じHEADから本書、自分のworklist、必要な系統READMEを読む。Research本文作成時だけ最新templateとLibraryの品質ガイドを読む。

ユーザーの明示指示なしにScheduled Taskを停止・無効化・削除せず、schedule・通知設定も変更しない。

## 2. 候補順序

Research / Audit / Discovery候補はworker専用worklistを入口にし、**rank 1から上から下へ**処理する。rank 1がその生成時点で最も重要度スコアの高い候補である。skip、重複、既処理、取得不能があれば、その次のrankへ進む。旧「末尾から上方向」は使わない。

重要度スコアは `.survey/config/candidate-priority.json` を機械正本とし、`.survey/scripts/candidate_priority.py` がResearchとDiscoveryの双方へ同一式を適用する。初期設定は次の加点で、後から設定値だけを変更できる。

- 公開から設定期間内の最新論文: `+100`
- 設定allowlistにある主要査読venue: `+10`
- 外部被引用数: 1件につき `+1`、上限なし

スコアは**重要度・処理順だけ**を表し、accept / unrelated / borderline の関連性判定とは独立する。低得点を理由に候補を削除せず、Research投入下限も設けない。古い候補を一定割合で強制消化するaging枠も設けない。低得点候補でも後から被引用数が増えれば自動再取得後に上位へ浮上できる。

venue・被引用数はPDF本文を読むためだけに取得せず、Semantic Scholar等から得られる書誌メタデータをキャッシュする。取得不能時は未知項目を0点として候補を保持し、後続更新で再評価する。

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

通常runの開始時は、**同じ最新main HEADの \`STATUS.md\` を読み、サマリーの \`収録候補論文数\` を探索 / 読解の境界判定にそのまま使う。** この値は非終端Research jobのうち \`canonical_id\` で一意化できる論文数であり、構造化referencesの未処理件数、Discovery判定待ち件数、worklist表示件数で代用しない。

- \`収録候補論文数 > 600\` → Research
- \`収録候補論文数 <= 600\` → Discovery

Libraryの未転送成果を足し引きして別の実効値を再計算しない。\`STATUS.md\` にこの指標がない、同じHEADで生成された値として確認できない、または取得不能なら、推測で別指標を代用せずDiscoveryを選び、その旨をrun報告へ残す。

run中に在庫が変化してもモードは固定する。

### 4.1 通常runの反復ラウンド（必須）

通常のResearch / Discoveryでは、従来のノルマ1回分を**1ラウンド**とする。Researchは完成5件、Discoveryは最終分類10件で1ラウンド完了とする。Discoveryでは、タイトル・abstract・書誌情報だけで**明らかに対象外**と確定できた候補は本文確認を省略して `unrelated` として完了件数へ数えてよい。`accept` / `borderline` および対象外か判断不能な候補は本文確認を必須とする。08:30 JSTのmaintenance専用runにはこの反復規則を適用しない。

1. 第1ラウンドが所定ノルマを達成したら、まずそのラウンドの完成成果をLibraryへ保存し、再取得して内容・件数・identity一意性等の所定確認を完了する。
2. 保存・再取得確認まで成功した場合、**同じScheduled起動の中で次ラウンドを必ず開始する。** 「ノルマ達成済み」「残り時間が少ない」「追加ラウンドを完遂できる保証がない」ことだけを終了理由にしてはならない。
3. 第2ラウンド以降にも同じ規則を再帰的に適用する。追加ラウンドがノルマ達成・保存・再取得確認まで成功した場合、その直後にさらに次ラウンドを開始し、**続行可能な限り何ラウンドでも繰り返す。**
4. モードは起動開始時に選択したResearch / Discoveryを全ラウンドで固定する。追加ラウンドごとに在庫境界を再判定しない。worklistは前ラウンドの続きから進め、完了済み・重複・既処理候補を再処理しない。
5. 各ラウンドは独立して耐久保存する。次ラウンドを始めるために前ラウンドの保存を遅らせない。
6. 最後の追加ラウンドは、時間切れ、ツール制約、外部取得不能、候補枯渇、hard stop等で途中終了してよい。ただし、前ラウンドが正常完了したなら**次ラウンドの実作業を少なくとも開始すること自体は必須**とし、開始だけ記録して即終了せず可能な範囲で実処理を進める。
7. 途中ラウンドがノルマ未達でも、現行手順で完成扱いできる成果は破棄しない。Researchは品質基準を満たしたMarkdownを個別保存し、Discoveryはpre-screenまたは本文確認で最終分類まで完了したrecordだけをpartial round JSONとして保存し、未完候補は完成扱いしない。
8. 同一起動内で各ラウンドを識別できるようround番号を付ける。必要なら基底run keyへ `/r01`, `/r02`, ... のsuffixを付ける。最終報告では完了ラウンド数、partialラウンドの有無・処理件数、最終停止理由を示す。

## 5. Discovery

### 5.0 引用探索の二層構成

前方引用（forward citation）は二層で追跡する。

1. 既存のDiscovery preloadは、有望・高yieldな引用源を短い周期で追う高速レーンとして維持する。
2. `.github/workflows/forward-citation-sweep.yml` は `.survey/config/forward-citation-sweep.json` に従い、**収録済み全論文**を公平に低頻度巡回するカバレッジレーンとする。arXiv / DOI / Semantic Scholar IDを優先し、それらがなくてもSemantic Scholarが解決可能な安定した一次資料URLを持つ論文は `URL:` seedとして台帳へ載せる。未巡回・前回巡回が古いseedから順に処理し、長い引用一覧はprovider cursorを次回runへ持ち越す。1周を完了した後は所定期間後に先頭ページから新しい周回を開始するため、過去の収録論文を後日引用した新論文も再発見できる。
3. カバレッジ巡回で見つかった未収録候補は既存のDiscovery候補面へ合流させ、別のrelevance正本を作らない。

外部API失敗やrate limitで1seedを取得できなくても、そのseedを処理済みにせず状態を保持して後続runで再試行する。1 runで許容するprovider失敗数は `.survey/config/forward-citation-sweep.json` の `max_provider_errors_per_run` を正本とし、上限到達時はそのrunを早期終了して状態を保存する。失敗seedにも最終試行時刻を残して公平選択へ戻すため、同じ失敗seedだけが先頭を占有し続けない。安定ID・解決可能な一次資料URLのどちらもない等、provider照会不能な収録論文はunsupportedとして可視化し、全件巡回済みと偽装しない。

Discoveryの重複排除は、Library正本 `/LLM-paper-summary-library-first/WORKER-LIBRARY-PROCEDURES.md` の現行Discovery手順を必須とする。具体的には、候補本文確認前の**開始前重複ゲート**と、成果保存直前の**保存直前重複ゲート**の両方で、Libraryのimmutable Discovery成果群（必要な未転送Research成果を含む）を完全列挙してidentity集合を再構成し、GitHub mainのread-only canonical stateと統合する。意味検索だけを重複排除の正本にせず、共有可変台帳、claim、reservation、GitHub writeをScheduled workerへ追加しない。詳細な列挙・identity比較・並列worker時の再確認手順はLibrary正本へ委譲する。

### 5.1 ノルマ

Discoveryは**1ラウンドにつき**新規canonical identity 10件を1候補ずつ確認し、各件を次のどれかへ最終分類する。

- \`accept\`
- \`unrelated\`
- \`borderline\`

各候補はまずタイトル・abstract・書誌情報で軽量pre-screenする。そこで、このサーベイの対象外であることが**論文固有の根拠付きで明白**なら、その時点で \`unrelated\` を確定し、本文読解を省略してよい。このabstract-only除外も10件へ数える。\`reason\` にはabstract上の具体的な除外根拠を記録し、\`body_check\` には \`abstract_screen_only\` と本文未読であることを明記する。

一方、\`accept\` / \`borderline\`、または対象外か少しでも判断が残る候補は本文確認必須とする。曖昧な候補をabstractだけで捨てない。本文取得不能で判定未完了の候補は10件へ数えず補充する。acceptだけを10件集めるために基準を緩めない。複数候補をまとめて要旨だけで一括分類せず、1候補ずつpre-screenまたは本文確認による最終分類を完了してから次へ進む。

### 5.2 Library保存形式

v12以降のDiscovery通常runは、**1ラウンド = 1 immutable JSON**だけを正規成果として保存する。

推奨path:

\`/LLM-paper-summary-library-first/discovery/discovery-YYYYMMDD-HHMM-<worker_id>-rNN.json\`

各完了ラウンドは1ファイルに10件すべてを \`records[]\` として含める。最後のpartialラウンドはpre-screenまたは本文確認で最終分類まで完了したrecordだけを含め、\`record_count\` を実数に合わせる。accept / unrelated / borderlineを別Library台帳へ分割しない。

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

同ラウンド内重複とLibrary内の明白な重複だけを除く。GitHub最新mainに同一identityが存在するかの最終判定はここで必須にしない。GitHub側precheckへ委譲する。

保存後はLibraryから再取得し、JSON parse、\`record_count == len(records)\`、保存した全recordのidentity一意性を確認する。完了ラウンドは10件、partialラウンドはその時点の完了件数を正本とする。

## 6. Research / Audit

Researchは**1ラウンドにつき**新規完成Research Markdownを5件Libraryへ保存する。5件の保存・再取得確認まで成功した場合はrunを終了せず、§4.1に従って次ラウンドを必ず開始する。

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

一次資料取得は特定のfront-endや固定順へ縛らない。arXiv HTML / PDF / e-print、OpenReview、会議・出版社、著者・研究機関・公式project site等から同一論文の一次資料へ到達できる経路を柔軟に使う。1経路のHTTP失敗、PDF text extraction失敗、HTML未生成だけで取得不能と判定せず、論文タイトル、arXiv ID、DOI、OpenReview ID、著者名等から別の一次資料経路を確認する。**固定された4経路を各1回だけ試して打ち切る方式は使わない。** 検索断片や第三者解説は本文の代用にせず、合理的に利用可能な一次資料経路を尽くしても必要な一次証拠を得られない場合だけ取得不能として扱う。

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

Survey GitHub ImportはLibrary成果をGitHub受信箱へ転送するアップロードワーカーである。Researchについては、転送前に完成Markdown全文を読み、現行品質ガイドを**明らかに満たさない原稿をGitHubへ流さない**責務も持つ。一次論文本体を再読して補完・書き直す役割ではない。

### 9.1 Research品質確認と転送

Library `research/*.md` は**今回の転送対象候補を全件検査**し、必ず1件ずつ先頭から末尾まで全文を読む。サンプリング、抜き取り、代表例だけの確認、一括要約、タイトル・概要・検索snippet・機械ゲート結果だけによる代替は禁止する。1件の品質判定を `pass` / `reject` / `hold` のいずれかに確定するまで次のResearchへ進まず、未検査・判定未完了のResearchはGitHubへ転送しない。問題設定、主要機構、入力→処理→出力、評価条件、比較対象、主要結果、限界、既存研究との差が論文固有に記述されているかを確認する。

汎用テンプレート文が本文の中心、論文名や方式名だけを差し替えれば別論文にも成立する長文、主要機構の具体説明欠落、headline結果だけで評価条件なし、プレースホルダー・未完全文、極端に薄い本文など、現行品質ガイドを明らかに満たさない原稿はアップロードワーカー自身の判断でrejectし、GitHubへ転送せずLibraryから削除する。判断が微妙なものは削除せずLibraryに保留し、転送もしない。

Research MarkdownのYAML frontmatterは、**本文が完成していても書誌・実装メタデータが不足していれば未完成扱い**とする。Research workerは一次資料を読んだ同じrunで、少なくとも次を埋める。

- `canonical_id`, `title`, `summary`, `list_summary`
- `authors`: 1名以上の配列。文字列1本のまま保存しない
- `published`: `YYYY-MM` または `YYYY-MM-DD`
- `publication`, `publication_type`, `publication_status`
- `source`: 主一次URL
- `sources`: 1件以上の一次URL配列
- `implementation`: 論文での実装・評価形態と、公式実装公開状況を文章で記録
- `code`: 公式コードURL。確認できなければキー自体を省略せず `null`
- `last_checked`: 一次資料を確認した日
- arXiv論文では `arxiv_id` と `arxiv_categories.primary`、`arxiv_categories.cross_list`
- `worker_completed_at`: Research完成時刻（ISO 8601、タイムゾーン付き）
- `worker_run_key`: 元Scheduled worker runを一意に示すキー

`last_audited` / `audit_version` は後段監査が更新してよい。引用監査済みなら `references`, `references_checked_at`, `references_source`, `references_total` も保持するが、引用を未確認のまま値を捏造して埋めてはならない。引用メタデータはGitHub側の一次資料citation backfillで後から補完できる。

Research workerのセルフレビューでは本文だけでなく上記frontmatterを読み直す。Survey GitHub Importも転送前に同じ必須項目を確認し、不足原稿は完成Researchとして転送しない。GitHub import inbox processorは最終防衛線として同じcanonical metadata監査を実行し、不足が1項目でもあればpaperへ保存せず `blocked_metadata` として保全する。

`worker_completed_at` と `worker_run_key` は論文の出版日時ではなく、workerが実際にResearchを完了した時刻・runを表す。GitHub import inbox processorはpaperとimport resultへ同値を保持する。

品質確認を通ったResearchだけを内容変更せず:

`.survey/import-inbox/pending/research/<unique>.md`

へcreate-onlyでコピーする。GitHub側でも `paper_quality_gate.py` が長文散文段落の再利用を含む機械ゲートを実行し、FAILはblockedへ送る。

### 9.2 Discovery転送

v12 Discovery run JSONを内容変更せず:

\`.survey/import-inbox/pending/discovery/<unique>.json\`

へcreate-onlyでコピーする。

unique名は \`<library_file_id>--<original-basename>\` 等、衝突しない値を使う。

### 9.3 転送完了条件

GitHub create応答だけでLibrary原本を削除しない。まず同じpending pathをGitHubから再取得し、**byte/hash一致**を確認する。processorが先に進んでpendingが消えていた場合は、同名のwaiting/blocked/retained payloadを確認し、それも既に終端済みなら `results/<type>/<pending-stem>.json` の `source_sha256` とLibrary原本のSHA-256を照合する。

pending / waiting / blocked / retained の同一bytes、またはresult receiptの同一 `source_sha256` を確認できた後はGitHubが耐久原本を所有するため、そのLibrary成果を削除してよい。最終paper/candidate処理の完了をLibrary側で待たない。

Survey GitHub Importは1回の転送バッチを終えたら、`.survey/scheduler/library-import-kick.json` を**1回だけ**更新し、commit messageを `survey-orchestrator: kick ...` で始める。これにより中央schedulerをevent-drivenで起動する。個別pendingファイルごとにkickしない。

既存pathに別bytesがある場合は上書きせず別unique名で再送する。

## 10. GitHub import inbox processor

正本仕様は \`.survey/import-inbox/README.md\`。実行workflowは \`.github/workflows/library-import.yml\` の1本だけとする。

受信箱processor自身はcronを持たない。`.github/workflows/survey-orchestrator.yml` は `07,17,27,37,47,57` 分に10分周期で受信箱を確認し、pending/waitingがある場合だけ `library-import.yml` を `workflow_dispatch` する。空受信箱では通常runを省略し、約6 tickに1回だけ再試行可能な残存状態を拾う回復passを実行する。`.survey/scheduler/library-import-kick.json` のpushも同じ入口へ入るため、scheduled eventの遅延・drop時にも次のLibrary handoffで即時回復できる。processorは毎回最新mainから再計算する。アップロード1ファイルごとにActions runを増やさない。1 runの上限はResearch 5件、Discovery 20 records。Discovery JSONが20 recordsを超える場合は、GitHub側で原本bytesを \`retained/discovery-source/\` に保持したまま、20 records以下の決定論的chunkへ分割して処理する。Discoveryの負荷上限をファイル数で定義しない。

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
3. pendingが既に進んでいれば同名waiting/blocked/retainedのbytes一致、または `results/<type>/<pending-stem>.json` の `source_sha256` 一致を確認済み
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

## 13. 08:30 日次更新 — LLM / LLMフレームワーク

リポジトリのGC・品質監査・整合性確認を行うrepository maintenanceはScheduled Chatに依存させない。`.github/workflows/maintenance.yml` がGitHub Actionsのscheduleにより毎日08:30 JST（23:30 UTC）に自動実行する。08:30の`scheduled-chat-30`はrepository maintenanceの起動責任を持たず、以下のLLM / LLMフレームワーク日次更新だけを担当する。

08:30 JSTの\`scheduled-chat-30\`は通常Research / Discoveryへ置換せず、**LLMとLLM推論フレームワークの最新情報を調査し、GitHubへ反映できる完成差分をLibraryへ作る日次更新run**とする。候補在庫や通常モード判定でResearch / Discoveryへ置換しない。

この分岐は、旧direct-GitHub運用で行っていた \`framework-updates/**\` / \`llm-releases/**\` の08:30更新経路と、現行Library-first運用を統合したものである。旧運用のようにScheduled worker自身が \`.survey/update-worker/update-payload.json\`、\`update-inbox.json\`、control file、GitHub本文を書き換えてはならない。GitHubはread-onlyで参照し、反映用の完成差分をLibraryへ耐久保存する。

### 13.1 開始時の比較基準

1. 最新main HEADを取得し、同じHEADの \`framework-updates/README.md\` と \`llm-releases/README.md\` を読む。
2. 必要な対象別ページ、少なくとも更新候補に対応する \`framework-updates/**\` / \`llm-releases/**\` の既存ページを読む。
3. Libraryに前回08:30成果があれば、その \`checked_at\` / \`focus_window\` を確認し、その後を主な調査期間にする。前回成果が不明なら直近7日を重点確認し、主要releaseの取りこぼしも確認する。
4. リポジトリ内の \`.survey/scripts/update_worker.py\` は履歴上の更新対象境界の実装参照としてよく、同スクリプトが許可する \`framework-updates/\` と \`llm-releases/\` を08:30非論文更新の対象範囲とする。ただしScheduled workerから同スクリプトをGitHub write目的で実行しない。

### 13.2 LLM / 基盤モデル調査

主要model providerの公式発表、公式model card、公式technical report、公式配布repository / model hubを確認する。少なくとも、リポジトリ収録済みの主要系列と、Qwen、DeepSeek、Gemma、Llama、Mistral / Mixtral、NVIDIA Nemotron等の主要open-weight系列を優先する。

確認対象は次を含む。

- 新model、新系列、新checkpoint、正式release、一般提供開始
- parameter構成、MoE expert数・active parameter、context length、attention方式等の重要仕様
- 推論precision、量子化、推奨runtime、必要VRAM / memory、reasoning / tool use等の重要変更
- license、利用条件、公式配布先、rename / replacement / deprecation
- 既存リポジトリ記述を実質的に更新すべきmodel card / technical reportの変更

「近日公開」「予定」「ティザー」、未確認リーク、二次記事だけでは確定更新にしない。実際の公開・release・documentation反映を一次資料で確認する。

### 13.3 LLM推論フレームワーク調査

少なくとも vLLM、SGLang、TensorRT-LLM、llama.cpp、Ollama、LightLLM、ExLlama系、およびリポジトリに収録済みの主要推論基盤について、公式release、changelog、merged PR、公式documentationを確認する。

掲載候補はversion番号だけでなく、次のような**実質的な挙動・性能・対応範囲の変更**を対象とする。

- 新model / architecture対応、backend追加、量子化対応
- KV cache、prefix cache、offload、speculative decoding、MoE / expert parallelism
- scheduler、continuous batching、prefill/decode分離、distributed inference
- kernel、CUDA / ROCm / CPU backend、FlashAttention等の性能経路
- memory使用量、GPU間通信、CPU / SSD offload方式
- breaking change、deprecated option、必要環境・互換性変更
- 公式benchmarkまたは一次PRで確認できる重要な性能差

単なるallowlist追加、軽微なbugfix、UI変更等でリポジトリの技術サーベイ価値を実質的に変えないものは、各READMEの掲載方針に従って除外する。

### 13.4 GitHub反映用の完成差分を作る

重要更新を採用したら、単なる調査メモで終わらせず、**最新mainへ反映するときに再調査せず適用できる粒度**まで整える。

各変更候補について少なくとも次を確定する。

- 対象path。原則 \`framework-updates/**\` または \`llm-releases/**\`
- 対象が既存fileなら、調査時点のblob SHA
- 追加・置換すべき完成Markdown本文
- 挿入位置または置換対象が特定できる既存見出し・文
- version / model名、公開日、変更点、重要性
- 性能値を記載する場合の条件・比較対象
- 一次URL
- 既存リポジトリ記述との差分
- pre-release / RC等ならその状態

旧 \`update_worker.py\` の \`replace_once\` / \`insert_after_once\` / \`insert_before_once\` で表現できる変更なら、その考え方に合わせて一意に適用できる差分へする。実際のpayload JSONをGitHubへ書く必要はないが、後続の通常チャットまたは保守反映者が機械的にpayloadへ変換できる程度に具体化する。

同じreleaseを複数情報源で見つけても1件へ統合する。件数のために弱い更新を水増ししない。

### 13.5 Library保存

反映候補が1件以上ある場合は、1 run 1 Markdownとして次へ保存する。

\`/LLM-paper-summary-library-first/maintenance/llm-framework-update-YYYYMMDD-0830-scheduled-chat-30.md\`

frontmatterまたは冒頭metadataに少なくとも次を持たせる。

- \`artifact_type: maintenance_update\`
- \`worker_id: scheduled-chat-30\`
- \`run_key\`
- \`reference_main_sha\`
- \`checked_at\`
- \`focus_window\`

本文には最低限、\`## LLM / Model updates\`、\`## Framework updates\`、反映対象path、調査時点blob SHA、完成差分、一次URL、既存との差、主要監視対象の「確認したが重要更新なし」を含める。

重要更新が0件の場合は、主要監視対象を確認した事実と「更新なし」を最終報告へ残す。空の成果物を件数目的で作らない。

保存後はLibraryから再取得し、対象path、version/model名、公開日、完成差分、一次URL、\`reference_main_sha\` が保持されていることを確認する。保存失敗時は完成MarkdownをScheduled Chatへ完全添付し、GitHub writeで迂回しない。

### 13.6 終了時

自分のrunで作った一時HTML、release noteコピー、画像、中間メモ、下書きを安全条件の範囲で掃除する。未反映の完成maintenance成果は削除しない。

最終報告には少なくとも次を含める。

- 確認main SHA
- 調査期間
- LLM更新件数
- framework更新件数
- **今回見つかった新着情報の内容そのもの**。採用した各LLM / framework更新について、対象名、version/model名、公開日、何が変わったか、なぜリポジトリ更新対象なのかをチャット本文で簡潔に説明する
- 性能値やmemory削減量など重要な定量値がある場合は、主要条件と数値をチャット本文にも載せる
- 一次資料URLを各新着項目に対応付けてチャット本文にも示す
- Library成果だけを参照させて報告を省略しない。**新着が1件以上あるrunでは、ユーザーがLibraryファイルを開かなくても主要内容を把握できる報告を必須とする**
- 「確認したが重要更新なし」の主要対象。新着0件の場合も、何を確認して0件だったかをチャットで報告する
- Library保存・再取得確認結果
- GitHub反映待ちの対象path
- 未完了事項

08:30 runで作ったmaintenance成果はResearch / Discovery成果とは別用途だが、**Survey GitHub Importの同一runで一緒に回収・反映する。** Research / Discovery受信箱へは入れず、既存の `.survey/update-worker/update-payload.json` → `.survey/update-worker/update-inbox.json` → `.github/workflows/update-helper.yml` / `.survey/scripts/update_worker.py` の正規経路へ渡す。

そのため08:30成果には、後続アップローダーが再調査せずpayloadへ変換できる**機械適用可能な更新計画**を必須とする。最低限、各artifactについて `path`、調査時点の `expected_blob_sha`、および既存fileなら `content` または `edits` のどちらか一方、新規fileなら完成 `content` を持つ。`edits` は `replace_once` / `insert_after_once` / `insert_before_once` のいずれかで、anchor/old文字列が一意になるよう作る。人間向け説明だけで終わらせない。

Survey GitHub Importはmaintenanceを `checked_at` の古い順に直列処理し、反映直前に最新mainを再取得する。base SHAが古い場合は、現在内容に対して意図した差分が既に反映済みかを確認し、未反映なら無関係な変更を壊さないよう現在blob SHAへrebaseした一意なpayloadを作る。意味が衝突する、anchorが一意でない、再baseに再調査が必要な場合は推測適用せずLibrary原本を残して保留する。`result.json` の同一attempt_idで `ok=true`、かつ対象pathのmain再取得まで確認できた成果だけLibraryから削除する。

## 14. 報告

Scheduled worker:

- Library-first / GitHub read-only
- 確認main SHA
- モードと在庫判定根拠
- 完了ラウンド数と、Research完成件数またはDiscovery分類内訳
- partialラウンドの有無・処理件数・最終停止理由
- Library保存結果
- run終了時掃除内容
- 退避・未完了

Survey GitHub Import:

- Research検査対象件数・全文検査件数・pass/reject/hold/未検査件数
- Research/Discovery転送数
- GitHub pending再取得・hash一致数
- Library削除数
- 転送失敗・競合数
- legacy未移行件数
- 最終確認main SHA

GitHub Actionの最終状態は \`.survey/import-inbox/results/\` とblocked payloadを正本とする。

## 15. GitHub Actionsの現行自動レーンと退役レーン

通常のLibrary-first運用で自動起動する中核は `survey-orchestrator.yml`、`library-import.yml`、`discovery-precheck.yml`、`maintenance.yml`、`update-helper.yml`、`forward-citation-sweep.yml`、`candidate-priority-refresh.yml`、および状態・整合性維持用の現行ワークフローに限定する。旧direct-GitHub worker向けの claim/run-state/preload/submission/recovery/ack/helper レーンは履歴・明示回復用としてファイルを残しても、自動push/scheduleからは起動しない。

`survey-orchestrator.yml` は Library import、前方引用巡回、候補重要度更新だけを dispatch する。Library import自身がbounded intake、reference relevance、queue submission処理を行い、必要時だけ `discovery-precheck.yml` を明示dispatchするため、旧補助レーンを10分ごとに一括dispatchしない。

## 16. 退役資料

旧direct-GitHub worker、旧共有3分類台帳への新規追記、Library側でのprecheck receipt生成、Library側でのlatest-main create/update判定は新規通常runでは使わない。
