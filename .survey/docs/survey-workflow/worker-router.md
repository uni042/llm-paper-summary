# Worker router — Library-first workflow v11

この文書は、LLM論文サーベイのScheduled Chat / Work系処理が読む**唯一の人間向け実行正本**である。2026-09-28以降の通常運用は、**Scheduled workerがGitHubをread-onlyで参照して成果をChatGPT Libraryへ保存し、GitHub反映はSurvey GitHub ImportのWorkタスクが行う**二段構成とする。

旧direct-GitHub worker運用は `worker-router-legacy-v10.22-direct-github.md` に退避した。履歴確認以外では参照せず、旧claim / reservation / submission / run-state / health-probe / worker-control経路をScheduled workerの新規runへ復活させない。

## 0. 正本順位と責務分離

正本順位は次の通り。

1. そのrunに対するユーザーの明示指示
2. 同一HEADの本書
3. Libraryの用途別正本
   - `/LLM-paper-summary-library-first/WORKER-LIBRARY-PROCEDURES.md`
   - `/LLM-paper-summary-library-first/PAPER-QUALITY-GUIDE.md`
   - Survey GitHub Import用 `github-import-procedure.md`
4. Scheduled Task / Work task本文のブートストラップ記述
5. 退役資料・履歴互換資料

通常のScheduled workerとGitHub反映者の責務を混ぜない。

| 実行主体 | GitHub | Library | 主責務 |
|---|---|---|---|
| `scheduled-chat-00` / `scheduled-chat-30` | **read-only** | read/write | 探索・読解・分類・完成成果の耐久保存 |
| Survey GitHub ImportのWorkタスク | read/write | read/write | Library成果の検証・正規化・GitHub反映・反映済み原本整理 |
| 通常チャット | 原則read-only | read/write | ユーザーが明示した回収・監査。GitHub反映はWorkタスクを優先 |

Scheduled workerはGitHubへの `write`、`claim`、`reservation`、`submission`、`result`、`handoff`、`health-probe`、`worker-control`、制御ファイル更新を試みない。GitHubは候補・既処理・最新テンプレート・系統・重複の確認に使う。

GitHub反映が必要な成果をScheduled workerが見つけても、自分でGitHubへ送らずLibraryへ保存する。GitHub側の旧transportが実装として残っていても、Scheduled workerの通常経路ではない。

## 1. run開始時に読むもの

各runの開始時に最新`main` HEADを取得し、同じHEADで次を読む。

- 本書
- 自分のworklist
  - `scheduled-chat-00`: `.survey/work-queue/worker-worklist-00.json` / `WORKLIST-00.md`
  - `scheduled-chat-30`: `.survey/work-queue/worker-worklist-30.json` / `WORKLIST-30.md`
- 必要な対象系統README
- Research本文を作るときだけ `.survey/templates/paper.md`
- Library `WORKER-LIBRARY-PROCEDURES.md`
- Research本文を作る直前に Library `PAPER-QUALITY-GUIDE.md`

固定identityは次を使う。

- :00 → `worker_id=scheduled-chat-00`, `scheduled_slot=00`
- :30 → `worker_id=scheduled-chat-30`, 通常 `scheduled_slot=30`
- :30の08:30 JST → maintenance専用run

ユーザーの明示指示なしにScheduled Taskを停止・無効化・削除せず、schedule・通知設定も変更しない。

## 2. worklistと処理順

Research / Audit候補は各worker最大200件を入口として扱う。Discovery側はLibrary手順書で指定された候補集合を使う。

候補は**専用リストの末尾から上方向**へ処理する。rank / # の大きいものから小さいものへ進み、skip・重複・既処理・取得不能があっても、その位置から上方向の次候補へ進む。

専用worklistが欠損・古い・空の場合だけ、最新mainの正規poolをread-onlyで参照して代替候補を選ぶ。GitHub側のqueueやjobをScheduled worker自身が更新して補充しない。

## 3. canonical identityと重複排除

候補ごとにcanonical identityを優先順で確定する。

1. arXiv ID
2. DOI
3. OpenReview ID
4. 正規化された一次資料URL

GitHubとLibraryの両方を確認し、同一canonical identityの重複を除外する。

GitHub側では既収録paper、既存候補、unrelated / borderline ledger、active job等を確認する。Library側では完成Research、Discovery成果、worker別relevance ledger、保存失敗時のScheduled Chat完全退避を確認する。

同一identityが別pathにあるだけで新規論文を作らない。GitHub反映時の最終identity解決はWorkタスクが最新mainのresolverで行う。

## 4. モード判定

GitHubだけの候補在庫をそのまま使わない。Library取り込み待ちを補正して開始時候補在庫を求める。

- `G`: 最新main上の未処理候補在庫
- `D`: Libraryの未反映Discovery `accept` のうち、GitHubでまだ候補・既収録・既処理として表現されず、Libraryに完成Researchもないcanonical identity数
- `R`: Libraryに完成Researchがあり、GitHubの`G`ではまだ未処理Research候補として数えられているcanonical identity数
- `E = G + D - R`

ファイル数ではなくcanonical identityで重複排除して数える。GitHub取り込み済みidentityは次runで`D` / `R`補正から外す。

モードはrun開始時の`E`で固定する。

- `E > 500` → Research
- `E <= 500` → Discovery

run中に在庫が変化してもモードは切り替えない。次run開始時に再計算する。

Libraryを十分読めず`D` / `R`を確定できない場合、0件と仮定しない。別のLibrary読取経路を試し、それでも補正不能なら`G`による暫定判定であることを最終報告に明記する。

## 5. Discovery

### 5.1 ノルマ

Discovery runでは**新規canonical identity 40件を本文確認まで行い、最終分類を耐久保存する**。

分類は次の3つだけ。

- `accept`: サーベイ候補として残す
- `unrelated`: 現行対象外。恒久除外台帳へ送る
- `borderline`: 関連性・重要性・期待知見が弱い既定除外。明示的再検討時のみ復帰可能

タイトル・要旨だけで確定せず、可能な限り一次資料本文を確認する。本文取得不能で分類未完了の候補は40件に数えず、リスト末尾側から次候補で補充する。

### 5.2 保存先

`accept` はrun単位のDiscovery成果JSON / Markdownへ保存する。

`unrelated` / `borderline` はworker別Library ledgerだけへ保存する。

- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-00-unrelated-papers.json`
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-00-borderline-papers.json`
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-30-unrelated-papers.json`
- `/LLM-paper-summary-library-first/discovery-relevance/scheduled-chat-30-borderline-papers.json`

旧 `discovery-classification/{accept,unrelated,borderline}-candidates.json` は新規worker出力先にしない。残存recordはSurvey GitHub Import Workタスクが整理する。

Discovery recordは、少なくとも `classification`、`canonical_id`、`identity_tokens`、正式`title`、具体的`reason`、一次資料`source_url`、本文確認内容`body_check`、確認時刻、`linked_from`、`source_run_file` を保持する。GitHub取込側が再判定しやすい形式を優先する。

保存直前に最新Library状態を再取得し、同identityの既処理・別worker保存済み成果・完成Researchを再照合する。保存後は再取得し、JSON parse、record_count、identity、分類を確認する。

## 6. Research / Audit

Research runでは**新規canonical identityの完成論文を10件**Libraryへ耐久保存する。

Research本文は1論文1Markdownとし、最新templateと`PAPER-QUALITY-GUIDE.md`に従う。少なくとも次を含める。

- canonical identity
- `summary`
- `list_summary`
- `## 概要`
- 書誌情報
- 問題設定
- 手法
- 評価
- 主要結果
- 既存研究との差
- 限界
- 一次資料

Research読解ワーカーは**機械的な品質チェックを実行しない**。監査スクリプトを回したり、文字数・段落数・手法節数・主要機構数・日本語率などを厳密に計測してPASS/FAIL判定する必要はない。

ただし、GitHub公開ゲートから撤廃した旧v10条件も**読解ワーカー自身の執筆・セルフレビュー条件として維持する**。完成前に一次資料を読んだ文脈で、旧基準相当の十分な説明になっているかを確認する。

- 成果Markdownは旧4,500 bytes以上相当の十分な情報量を目安にし、極端に短い原稿を完成扱いしない。
- 説明本文は旧2,200文字以上相当の十分な説明量を目安にする。
- 全体は旧10段落以上、手法説明は旧4段落以上相当の厚みを目安にする。
- 主要機構が3個以上ある場合、各主要機構を旧2段落以上相当の密度で、役割・入力・処理・出力・効く理由・制約まで説明する。
- `list_summary` は旧45〜180文字程度を目安にし、一文だけで他論文と主な貢献を区別できる内容にする。
- 日本語・カタカナへ自然に置換できる裸の英語専門語は残さない方向でセルフレビューする。
- `## 概要` には代表的な定量結果、または定量化が自然でない研究なら主要な定性的発見を含める。
- 問題設定、新規性、手法、評価、主要結果、限界、既存研究との差を、それぞれ内容上不足しないよう確認する。
- 定量結果を書く場合は、比較対象・条件・指標・意味を取り違えない。
- 負の結果、品質影響、失敗条件、トレードオフが一次資料にある場合は落とさない。

これらは**セルフレビュー用の目安・内容条件**であり、Researchワーカーが文字数カウンタ等で厳密に検査する義務はない。数値だけを満たすための水増し・同義反復は禁止する。最終判断は、一次資料を読んだワーカーが「未読者が仕組み・結果・限界を追えるか」で行い、不十分ならLibrary保存前に修正する。

本文取得で単一経路が失敗しても、別の一次資料経路を探す。arXiv HTML / PDF、OpenReview、出版社・会議、著者・研究機関の正式配布版など、materially distinctな一次資料経路を使う。検索断片や第三者要約を本文根拠にしない。

`blocked` は一時状態であり、duplicate / unrelated / permanent rejectionへ読み替えない。現行GitHubのblocked retry規則をread-onlyで参照し、通常は7日後に再試行、異なるblocked eventが5回以上かつ最初のblockから28日以上続いた場合は定期再試行を休止するだけとする。`blocked_permanent`へ自動昇格しない。

最終的な適用先が学習工程の高速化・省メモリ化で、現在凍結中の範囲に該当する論文はResearch新規収録へ回さず、除外理由を保持してWork側の整理対象に渡す。

## 7. Library保存と失敗時の保全

通常runの耐久保存先はChatGPT Libraryである。

重要作業を単一実行経路へ固定しない。Library読取・保存・固定ファイル更新・一次資料取得について、現在の環境で利用できる複数経路を使い分ける。ただし正本、identity、read-only制約、version競合保護を崩す経路は使わない。

Library保存不能時も完成成果を破棄しない。

- Research: 完成MarkdownをScheduled Chatへ完全添付する。
- Discovery: 40件全件のclassificationとprovenanceを含むJSON / Markdownを完全添付する。
- 後続runでconversation file IDからLibraryへ回収できる場合は回収し、Libraryから再取得して検証する。

一部だけ保存できた場合、成功分を巻き戻さず失敗分だけ再試行・退避する。同じ失敗経路を連打しない。

GitHub writeを試してLibrary失敗を回避することは禁止する。

## 8. Survey GitHub Import Workタスク

GitHub反映はSurvey GitHub ImportのWorkタスクが担当する。Workタスクは毎回Libraryの`github-import-procedure.md`を読み、最新mainと本書に照らして処理する。

### 8.1 取り込み対象

少なくとも次を確認する。

- `/LLM-paper-summary-library-first/research/` の完成Research
- `/LLM-paper-summary-library-first/discovery/` のDiscovery成果
- worker別`discovery-relevance/`
- 旧共有`discovery-classification/`に残るrecord
- `/LLM-survey-outbox/pending/` 等の過去attempt成果
- 08:30 maintenance成果
- Library保存失敗から回収された完全添付

運用手順書、品質ガイド、制御用固定ファイルは成果として削除しない。

### 8.2 Research取り込み

1. Libraryの完成原稿を取得する。
2. 最新mainの本書、対象系統README、template、resolver、公開完全性監査、日本語率規則を確認する。
3. Library成果のcanonical identityを最新mainと照合する。内容品質のために一次資料を読み直さない。
4. repository全体でidentityを解決する。
5. `represented`なら既存paperを正規update先にし、`not_found`のときだけ新規pathを作る。
6. 軽微なformat崩れと日本語率不足はWork側で修正してよい。日本語率修正は意味・数値・比較条件を変えず、裸の英語表現を自然な日本語・カタカナへ置換する範囲に限る。論文を読み直さないと判断できない内容不足はWork側のFAIL条件にせず、読解ワーカーのセルフレビュー責任とする。
7. GitHubへ1件ずつ反映する。同一pathへのwriteを並列化しない。
8. write後は最新mainから同じpathを再取得し、identity・本文・commitを確認する。
9. 再取得確認できた後だけ対応Library原本を削除する。

同一identityの完全な正規本文がすでに存在する場合は、重複として再取得確認した後にLibrary原本を削除する。既存本文が不完全なら重複扱いにせず正規paperを補完する。

### 8.3 Discovery取り込み

`accept` はLibrary recordだけでResearch候補登録済みとみなさない。最新mainのDiscovery正規経路に沿って、必要な固定ソース事前検査（precheck）とidentity照合を行い、正規候補へ反映する。

`unrelated` / `borderline` は最新mainのrelevance ledger経路へ反映する。`borderline`を`unrelated`と混同しない。

旧共有3分類ファイルは残存recordの回収用にだけ読み、新規worker出力先にしない。

GitHub反映または既存正規状態との重複を再取得確認できたcanonical identityだけLibrary側から除く。複数recordのファイルは処理済みrecordだけ除き、未処理recordを保持する。

### 8.4 Libraryを空に近づける原則

GitHub反映対象のLibrary成果は、**致命的なGitHub書込み不能・identity不明・一次資料不足などで安全に終端できないものを除き、Workタスクが「GitHubへ反映」または「既存正規成果との重複確認後に原本整理」のどちらかまで進める。**

1件の失敗で他の独立成果を止めない。処理可能な残件を続け、Libraryの反映待ち成果を可能な限り空にする。

`unrelated` / `borderline` / `blocked` の扱いは本書の定義とGitHub正規状態に従う。単に取り込みにくいことを理由に分類を変更しない。

## 9. GitHub write経路

Workタスクは環境ごとに利用可能な経路が異なるため、複数の正規経路を保持する。

第一候補はGitHub connectorによるfile create/update。別経路を使う場合も、最新mainの同一HEADから始め、dirtyな作業領域や別変更を混ぜず、反映後にGitHubから再取得して検証する。

結果不明のwriteは二重送信しない。まず最新mainと対象pathを読み、反映済みか確認する。

安全検査や権限制約を回避するための低レベル迂回を作らない。利用可能な正規write経路がすべて失敗した場合はLibrary原本を保持し、失敗段階を報告する。

## 10. 08:30 maintenance

`scheduled-chat-30` の08:30 JST runは通常Research / Discoveryへ置換せず、フレームワーク更新、主要LLM / モデル更新、maintenance状態、未完了事項を確認する。

結果はLibraryの`0830-updates/`へMarkdownで保存し、GitHub反映が必要な変更成果はSurvey GitHub Import Workタスクが取り込む。

## 11. 終了条件と報告

Scheduled workerはGitHub write待ちを終了条件にしない。Libraryへ成果を保存し、ノルマ到達または実際の取得・保存上限まで独立作業を続ける。

通常runの報告には少なくとも次を含める。

- 実行経路: Library-first（GitHub read-only）
- GitHub読取成否と確認main SHA
- `G / D / R / E`
- 選択モード
- Research完成件数、またはDiscovery 40件の達成状況
- accept / unrelated / borderline内訳
- 重複・既処理skip数
- Library保存結果
- Scheduled Chat完全退避の有無
- 未完了事項と終了理由
- GitHub writeを試みていないこと

Survey GitHub Import Workタスクの報告には、GitHub新規作成・更新・重複確認・relevance記録・Library原本整理・保留件数、最終main SHAを分けて示す。

## 12. 退役資料

旧direct-GitHub worker手順は `worker-router-legacy-v10.22-direct-github.md` に保存する。旧手順にあるclaim、record bank、preflight fast lane、submission result、run-state、worker-control、health-probe、fallback-inbox等は、既存コードや履歴データの解釈に必要な場合だけ参照する。

**新規Scheduled worker runの実行手順として旧資料を補完利用しない。**
