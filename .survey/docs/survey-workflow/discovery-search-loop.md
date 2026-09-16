# Discovery automatic search loop

この文書は、Discoveryで検索結果を1ページ/1バッチだけ処理してworkerへ制御を戻すことを禁止し、同一run内で未収録候補を継続的に蓄積するための反復契約を定義する。

## 目的

検索ランキング上位が既収録論文で埋まっていても、そのページだけで探索を終了せず、未収録候補へ到達するまで検索を深掘りする。候補在庫が十分でない間は、run-level continuation/finalization gateが継続を許す限り、同一run内で検索を続ける。

## 自動反復ループ

通常Discovery modeでは、次のループをworker自身の任意判断ではなく標準動作として実行する。

1. 最新default branchのidentity snapshotとcandidate inventoryを取得する。
2. 現在の探索軸で検索providerから1ページ/1バッチを取得する。
3. `discovery-search-filter.md` に従い、candidate評価より前に既収録結果を除外する。
4. 未収録結果だけをrun-local candidate bufferへ追加する。同一identityは1件へ畳み込む。
5. 現在の探索軸で未収録結果がまだ十分に蓄積しておらず、providerに次ページ/cursor/offsetがある場合は、**workerへ終了判断を戻さず、そのまま次ページを取得して2へ戻る**。
6. providerがページングを公開しない場合は、同じ探索意図を保ったまま検索窓をずらす。具体的には期間、語句、引用方向、隣接キーワード、会議/カテゴリ、arXiv月、著者/研究グループ等を変えて未走査領域を取得し、2へ戻る。単に同じqueryを再送して同じ上位結果を繰り返さない。
7. 現在軸のprovider結果を使い切った、または独立な検索窓を十分に走査した場合は、別の独立探索軸へ切り替えて2へ戻る。
8. candidate bufferに品質基準を満たす候補があれば、workflow-v10契約に従い5件以下ずつimmutable Discovery submissionへ耐久保存する。5件はsubmission単位の上限であり、run全体の探索上限ではない。
9. submission後に最新HEAD、identity snapshot、candidate inventoryを再取得する。`candidate_inventory <= 50` ならDiscovery loopを再開する。`candidate_inventory > 50` かつactionable Research/Auditがある場合は既存契約どおりoverflow research modeへ切り替える。
10. 各独立検索単位の前、耐久保存後、final response候補地点ではcontinuation/finalization gateを評価し、その出力が停止を許可した場合だけloopを抜ける。

## 停止・継続の扱い

以下はloopを止める理由にしない。

- 1ページを処理した。
- 1 queryを処理した。
- 1 roundを保存した。
- 上位結果の大半または全部が既収録だった。
- candidate bufferが5件に達した。
- 1 submissionを保存した。
- ある探索軸で未収録候補が0件だった。

candidate inventoryの50はモード切替境界であり、弱い候補を件数合わせで採用するノルマではない。品質基準を満たす候補だけを蓄積する。

loopの終了は、continuation/finalization gateが明示的に停止を許可した場合、canonical read/durability/tool failureが実測された場合、または独立探索経路を実際に走査し切ったことを正本条件で確認できた場合に限る。探索枯渇を推測してはならない。

## provider paginationがない場合

Scheduled Chatの検索tool等がpage/cursorを直接公開しない場合でも、本契約を無効にしない。その場合は同じqueryの再実行ではなく、検索結果集合が変わるように検索窓を明示的にシフトし、擬似ページングとして扱う。各windowはrun-localで記録し、同じwindowを無意味に繰り返さない。

## telemetry

run内で最低限次を集計する。

- raw search results
- retrieval-stage duplicates filtered
- unseen results passed to candidate evaluation
- provider pages/cursors traversed
- pagination unavailable時のshifted search windows数
- independent axes traversed
- candidates durably submitted
- end candidate inventory

これらは診断用telemetryであり、単独では停止条件にしない。
