# Discovery automatic search loop

この文書は、Discoveryで検索結果を1ページ/1バッチずつcandidate評価workerへ返さず、取得時filter/collector層で複数ページを先に消化してから評価対象をまとめて渡すための反復契約を定義する。

## 目的

検索ランキング上位が既収録論文や過去のcandidate評価落ち論文で埋まっていても、そのページだけをworkerへ渡して探索判断をさせず、`discovery_search_filter.collect_until_unseen(...)` が同一探索軸を深掘りし、それらを除外した未評価結果を既定10件まで蓄積してからcandidate評価へ渡す。

## filter/collector内部の自動反復

通常Discovery modeでは、1回の検索単位について次の処理をfilter/collector層の標準動作とする。

1. 最新default branchのidentity snapshotと `.survey/work-queue/discovery-rejections.json` を取得する。
2. provider adapterから現在cursorの1ページ/1バッチを取得する。
3. `discovery-search-filter.md` に従い、candidate評価より前に既収録・既投入・過去のcandidate評価落ち結果を除外する。
4. 残った未評価結果だけをcollector内部bufferへ追加し、同一identityはページをまたいでも1件へ畳み込む。
5. bufferが10件未満でproviderに次ページ/cursor/offsetがある場合は、candidate評価workerへ制御を返さずcollector自身が次ページを取得して2へ戻る。
6. 最後のページで10件を超えた場合は、そのページの未評価結果を切り捨てずbufferへ保持する。
7. bufferが10件以上になった、providerが尽きた、または明示的な安全上限に達した場合だけcollector結果をcandidate評価workerへ返す。
8. providerがpaginationを直接公開しない場合はprovider adapterが期間、arXiv月、引用方向、隣接キーワード、会議/カテゴリ等の検索窓をずらし、未走査集合を次cursor相当として供給する。同じqueryをそのまま繰り返さない。

つまりcandidate評価workerが通常見る単位は「検索1ページ」ではなく、**既収録・既投入・過去の評価落ちを除外済みの未評価検索結果buffer（標準10件前後）**である。

## workerへ返った後の処理

collectorが返したbufferに対してのみrelevance評価、priority付与、candidate選定を行う。品質基準を満たすdedupe済みcandidateがあればworkflow-v10契約に従い5件以下ずつimmutable Discovery submissionへ耐久保存する。5件はsubmission単位の上限であり、run全体の探索上限ではない。

candidate評価したが採用しなかった論文は、既収録・重複として事前除外したものを除き、同じimmutable submissionの `rejected_candidates` にidentity・title・source URL（取得できる場合）・具体的な `rejection_reason` を記録する。これらは `build_discovery_rejection_ledger.py` により次回以降のretrieval-stage exclusionへ反映される。同一run内ではledger更新待ちに依存せず、今回rejectしたidentityをrun-local exclusion setへ直ちに追加する。

submission後に最新HEAD、identity snapshot、rejection ledger、candidate inventoryを再取得する。`candidate_inventory <= 50` なら別の検索単位として再度collectorを起動する。`candidate_inventory > 50` かつactionable Research/Auditがある場合は既存契約どおりoverflow research modeへ切り替える。

## 停止・継続の扱い

以下はrun停止理由にしない。

- collectorが10件の未評価bufferを返した。
- 1 provider search unitを処理した。
- 1 roundを保存した。
- 上位結果の大半または全部が既収録または過去の評価落ちだった。
- candidateが5件に達した。
- 1 submissionを保存した。
- ある探索軸で新規評価対象が0件だった。

10件はcandidate採用ノルマではなく、candidate評価へ渡す検索結果bufferの既定サイズである。candidate inventoryの50はモード切替境界であり、弱い候補を件数合わせで採用するノルマではない。

runの終了は、continuation/finalization gateが明示的に停止を許可した場合、canonical read/durability/tool failureが実測された場合、または独立探索経路を実際に走査し切ったことを正本条件で確認できた場合に限る。探索枯渇を推測してはならない。

## telemetry

run内で最低限次を集計する。

- raw search results
- retrieval-stage represented-paper duplicates filtered
- rejection-ledger filtered
- cross-page duplicates filtered
- unseen/unrejected results returned by collector
- candidate evaluation rejected count
- provider pages/cursors traversed
- pagination unavailable時のshifted search windows数
- independent axes traversed
- candidates durably submitted
- end candidate inventory

これらは診断用telemetryであり、単独では停止条件にしない。
