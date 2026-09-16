# Discovery automatic search loop

この文書は、Discoveryで検索結果を1ページ/1バッチずつcandidate評価workerへ返さず、取得時filter/collector層で複数ページを先に消化してから評価対象をまとめて渡すための反復契約を定義する。

## 目的

検索ランキング上位が既収録論文や過去のcandidate評価落ち論文で埋まっていても、そのページだけをworkerへ渡して探索判断をさせず、`discovery_search_filter.collect_until_unseen(...)` が同一探索軸を深掘りし、それらを除外した未評価結果を既定10件まで蓄積してからcandidate評価へ渡す。

## filter/collector内部の自動反復

通常Discovery modeでは、1回の検索単位について次の処理をfilter/collector層の標準動作とする。

1. 最新default branchのidentity snapshot、同snapshotの `_represented_papers.json`、`.survey/work-queue/discovery-rejections.json` を取得する。
2. provider adapterから現在cursorの1ページ/1バッチを取得する。
3. `discovery-search-filter.md` に従い、candidate評価より前にexact identity、represented-paper alias、過去のcandidate評価落ち結果を除外する。
4. 残った未評価結果だけをcollector内部bufferへ追加し、同一primary identityだけでなく、arXiv / DOI / OpenReview / URL / exact normalized titleで同じpaperへ解決できるprovider結果もページ内・ページ間で1件へ畳み込む。
5. stable identifierを持たない検索結果については、first authorとpublication yearが一致し、normalized title similarityが高信頼thresholdを満たす場合だけrepresented-paper fuzzy matchを使う。stable identifierがある結果を似たtitleだけで除外しない。
6. bufferが10件未満でproviderに次ページ/cursor/offsetがある場合は、candidate評価workerへ制御を返さずcollector自身が次ページを取得して2へ戻る。
7. 最後のページで10件を超えた場合は、そのページの未評価結果を切り捨てずbufferへ保持する。
8. bufferが10件以上になった、providerが尽きた、または明示的な安全上限に達した場合だけcollector結果をcandidate評価workerへ返す。
9. providerがpaginationを直接公開しない場合はprovider adapterが期間、arXiv月、引用方向、隣接キーワード、会議/カテゴリ等の検索窓をずらし、未走査集合を次cursor相当として供給する。同じqueryをそのまま繰り返さない。

つまりcandidate評価workerが通常見る単位は「検索1ページ」ではなく、**既収録・既投入・過去の評価落ち・同一paper aliasを除外済みの未評価検索結果buffer（標準10件前後）**である。

## pagination非公開providerのsearch-window選択

paginationを公開しないproviderでは、検索窓をその場の記憶だけで選ばない。最新 `discovery-state.json` の `search_windows` / `recent_search_windows` を読み、`.survey/scripts/discovery_search_history.py` と同じ6次元keyで候補windowを比較する。

window keyは次を含む。

- `topic`
- `source`
- `date_range`
- `category`
- `citation_direction`
- `query_family`

候補windowが複数ある場合は、まず未走査windowを優先する。すべて走査済みならhistorical unseen rateとcandidate acceptance rateが高く、duplicate rateが低いwindowを優先する。累積duplicate rateが `0.80` 以上のwindowはcooldown扱いとして同一条件の再走査を後順位へ送り、検索上位が既知論文で埋まった窓を機械的に繰り返さない。走査履歴は永久blacklistではないため、新しい期間・カテゴリ・引用方向・query familyへ変化したwindowは別keyとして扱う。

実際に走査した各windowは、immutable Discovery submissionの `discovery_stats.search_windows` に6次元keyと少なくとも次を記録する。

- `raw_result_count`
- `unseen_result_count`
- `duplicate_filtered_count`
- `rejection_filtered_count`
- `candidate_evaluation_count`
- `candidate_accepted_count`
- `position`（providerが返すcursor / offset / page等の最後の走査位置。個別fieldで記録してもよい）

Actions側の `queue_worker.record_discovery_stats()` が単一writerとして `discovery-state.json` へ集約し、windowごとの `unseen_rate`、`duplicate_rate`、`candidate_acceptance_rate`、`last_position`、`scan_count`、`last_run_key`、`last_round` を耐久化する。次回workerは `last_position` をprovider adapterの再開・window shift判断に利用できる。件数がない場合に率を推測してはならず、0件は0として扱う。

## workerへ返った後の処理

collectorが返したbufferに対してのみrelevance評価、priority付与、candidate選定を行う。品質基準を満たすdedupe済みcandidateがあればworkflow-v10契約に従い5件以下ずつimmutable Discovery submissionへ耐久保存する。5件はsubmission単位の上限であり、run全体の探索上限ではない。

candidate評価したが採用しなかった論文は、既収録・重複として事前除外したものを除き、同じimmutable submissionの `rejected_candidates` にidentity・title・source URL（取得できる場合）・具体的な `rejection_reason` を記録する。これらは `build_discovery_rejection_ledger.py` により次回以降のretrieval-stage exclusionへ反映される。同一run内ではledger更新待ちに依存せず、今回rejectしたidentityをrun-local exclusion setへ直ちに追加する。

submission後に最新HEAD、identity snapshot、represented-paper resolver、rejection ledger、candidate inventoryを再取得する。`candidate_inventory <= 50` なら別の検索単位として再度collectorを起動する。`candidate_inventory > 50` かつactionable Research/Auditがある場合は既存契約どおりoverflow research modeへ切り替える。

## 停止・継続の扱い

以下はrun停止理由にしない。

- collectorが10件の未評価bufferを返した。
- 1 provider search unitを処理した。
- 1 roundを保存した。
- 上位結果の大半または全部が既収録または過去の評価落ちだった。
- candidateが5件に達した。
- 1 submissionを保存した。
- ある探索軸で新規評価対象が0件だった。
- 1つのsearch windowを走査済みにした。

10件はcandidate採用ノルマではなく、candidate評価へ渡す検索結果bufferの既定サイズである。candidate inventoryの50はモード切替境界であり、弱い候補を件数合わせで採用するノルマではない。

runの終了は、continuation/finalization gateが明示的に停止を許可した場合、canonical read/durability/tool failureが実測された場合、または独立探索経路を実際に走査し切ったことを正本条件で確認できた場合に限る。探索枯渇を推測してはならない。

## telemetry

run内で最低限次を集計する。

- raw search results
- exact identityでのrepresented-paper duplicates filtered
- represented-paper resolver filtered
- rejection-ledger filtered
- intra/cross-page duplicates filtered
- alias resolverで畳み込んだintra/cross-page duplicates
- unseen/unrejected results returned by collector
- candidate evaluation count / rejected count / accepted count
- provider pages/cursors traversedと最後のposition
- pagination unavailable時のshifted search windows数
- windowごとのunseen / duplicate / candidate acceptance rate
- independent axes traversed
- candidates durably submitted
- end candidate inventory

これらは診断用telemetryであり、単独では停止条件にしない。
