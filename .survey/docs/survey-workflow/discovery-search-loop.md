# Discovery automatic search loop

この文書は、Discoveryで検索結果を1ページずつcandidate評価workerへ返さず、**1つの固定された検索結果URL/API query** をprecheckへ渡し、その同一結果集合のpage/cursor/offsetをcollectorが自動で進めてから評価対象をまとめて返す契約を定義する。Scheduled Chatの強制経路ではprovider取得・pagination・buffer累積・重複除外・継続判定をworkflow precheckが一括して実行する。

## 目的

検索ランキング上位が既収録論文や過去のcandidate評価落ち論文で埋まっていても、そのページだけをworkerへ渡して探索判断をさせない。`discovery_search_filter.collect_until_unseen(...)` が定義する「未評価結果を既定20件まで蓄積する」意味論を、実運用ではschema-v2 precheckの `CONTINUE_FETCH` / `READY_FOR_EVALUATION` 反復として強制する。

## filter/collector内部の自動反復

通常Discovery modeでは、1回の検索単位について次を標準動作とする。

1. workerは検索provider上で**1つの結果集合を表すURL/API query**を決める。通常検索なら検索結果URL、被引用探索なら対象論文のcitations endpoint、参考文献探索ならreferences endpointを使う。
2. workerはschema-v3 precheck requestへ `provider`, `source_url`, `collector_id`, `run_key`, `axis` を保存する。**検索結果record自体はworkerがrequestへ手書きしない。**
3. workflow precheckがproviderのpage 1を取得し、canonical identity snapshot / represented-paper resolver / rejection ledgerで既収録・既投入・過去不採用・alias重複を除外する。
4. 未収録bufferが `target_unseen`（既定20）未満でproviderに次page/cursor/offsetがある場合、`collect_until_unseen()` が**同じsource_urlの次ページ**を取得して3へ戻る。
5. ページ間でもprimary identity / arXiv / DOI / URL / title aliasを畳み込み、重複候補をbufferへ二重投入しない。
6. bufferが20件以上、provider exhaustion、または安全上限到達のいずれかでcollectorを終了する。
7. workflow resultは最終bufferのみを `results[]` として返し、`evaluation_allowed=true` / `decision=READY_FOR_EVALUATION` とする。
8. candidate評価workerはこの最終 `results[]` だけを見る。

**別キーワード、別期間、別カテゴリ、別citation directionへの変更はpaginationではない。** 1つの結果集合が尽きたあとに必要なら、別のDiscovery round / collectorとして新しい `source_url` を作る。同一collector内で「次ページ相当」と称してqueryを変更してはならない。

つまりcandidate評価workerが通常見る単位は「検索1ページ」ではなく、**1つの固定検索結果を必要なだけpage 1→2→3…と走査した後の、重複除外済み未評価buffer（標準20件前後）**である。

## pagination非公開providerと次の探索軸

paginationを公開しないproviderでは、そのproviderを同一collectorの自動ページ送りには使わない。結果集合を安定してページングできるAPI/provider adapterを優先する。別の期間・カテゴリ・引用方向・query familyへ移る場合は新しいDiscovery roundとして扱う。次roundの検索窓は、その場の記憶だけで選ばない。最新 `discovery-state.json` の `search_windows` / `recent_search_windows` を読み、`.survey/scripts/discovery_search_history.py` と同じ6次元keyで候補windowを比較する。

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

## 外部アクセス効率を最大化する実務指針

探索では、外部検索・abstract取得・全文取得を同じコストの呼び出しとして扱わない。限られた外部アクセス枠から最大の未評価候補を得るため、次を標準的な運用指針とする。

1. **canonical identityを外部検索より先に使う。** 検索候補のarXiv ID / DOI / OpenReview ID / canonical IDが得られた時点で、最新identity snapshot、`_represented_papers.json`、rejection ledger、既存jobをまとめて照合する。既知候補ごとに外部abstractや全文を取り直さない。GitHub code searchは補助に限り、canonical identity shard / represented-paper resolverを主判定にする。
2. **1回の外部検索を複数候補へ再利用する。** 1 query / 1 result pageを1論文確認に消費せず、得られた結果集合から複数のstable identifier、title、abstract相当情報、評価値をまとめて回収し、collector bufferへ入れる。同じ取得結果をcandidate評価・重複照合・次検索軸の語彙抽出に再利用する。
3. **軽量取得を先に使い、全文取得をDiscoveryでは原則避ける。** 検索結果、公式abstract、HTMLの冒頭・書誌情報で、対象範囲への直接性、システム寄与、実測評価の有無を判定できる場合はそこでcandidate評価を行う。Discovery段階でPDF全文取得や高コストな一次資料精読へ進まず、Researchへ送る価値がある候補だけを耐久投入する。
4. **検索軸は高重複を確認したら早く切り替える。** 同一queryの再送や同じ上位結果の反復より、topic、date range、category、citation direction、query familyを変える。特に、新着→memory/offload→MoE→KV/network→scheduling→speculative decoding→GPU runtime→隣接分野、のように独立軸を明示的に切り替える。同じ軸を深掘りする場合もcursor/offset/date windowを進め、未走査集合を対象にする。
5. **検索語は一般語から機構語へ絞る。** `LLM inference` や `GPU runtime` のような一般語で既知率が高い場合、`NVMe`、`CXL`、`expert cache`、`expert prefetch`、`KV transport`、`output-length scheduling`、`persistent kernel`、`prefix routing` など具体的な機構へ寄せる。新規候補率が低いquery familyはcooldownへ送る。
6. **厳密な日付指定が低収益なら、月・ID範囲・テーマ軸へ戻す。** providerによっては「特定提出日」検索が空振りしやすい。結果0件を探索枯渇とせず、arXiv月、ID帯、カテゴリ、隣接キーワードへ検索窓を変える。結果が出ない厳密日付queryを繰り返さない。
7. **非同期処理を探索の同期障壁にしない。** Discovery submission保存後、GitHub Actionsによるdedupe / materialization待ちだけを理由に停止しない。submission自体の耐久保存を確認したら、同じrunの次の独立探索軸へ進み、後で最新identity/stateを再取得して取り込み結果を確認する。
8. **run-local exclusionを即時更新する。** 今回runで重複・不採用と確認したidentityは、Actionsやledger反映を待たずrun-local exclusionへ入れる。同じrunで同じ候補に外部アクセスを再消費しない。
9. **空ラウンドも情報として使う。** ある軸が全既知・全不採用だった場合、それを失敗として同じqueryを繰り返さず、そのwindowのduplicate率・unseen率低下の証拠として次軸選択へ利用する。連続空ラウンドが出ても、独立未走査軸が残る限り探索は継続する。
10. **7 round以上回せたrunでは再現可能性を残す。** 最終通知では、どの検索軸順序が高収益だったか、どのquery/windowが低収益だったか、1回の外部取得をどう複数候補へ再利用したか、canonical identity照合でどの無駄アクセスを避けたか、非同期待ちをどう回避したかを短く報告する。外部アクセス回数や残量が実測できない場合は推測値を作らない。

### 過去運用から得た再発防止知見

過去の多ラウンド探索では、探索そのものよりも **重複判定・継続判定・submission transport・非同期反映確認** の不整合が実効スループットを大きく落とした。以下を再発防止の標準則とする。

1. **GitHub code searchをnovelty判定の正本にしない。** 過去にはcode searchで見つからない既収録論文を新規扱いし、最終dedupeで大量除外され、連続空ラウンド化した。探索前とwrite直前は、Actionsの最終ゲートと同系統のcanonical identity snapshot / represented-paper resolver / rejection ledgerを使う。
2. **retrieval-stageで既知を落としてからpaginationを進める。** 既収録論文が上位を埋めるproviderでは、1ページ目をそのまま評価へ渡すと評価workerが既知論文ばかり処理する。各ページで既知・過去不採用・alias重複を即除外し、未評価bufferが標準20件前後になるまでcursor / offset / 次windowをcollector側で進める。
3. **1 submission / accepted 0 / 全重複を停止条件にしない。** 過去には次探索軸が残っているのに1 roundで終了するrunがあり、探索量が不安定になった。continuation gateを毎round後に実際に評価し、未走査の有望軸がある限り次roundへ進む。Actions待ちも停止理由にしない。
4. **multi-round submissionでjob IDを自作しない。** 過去にはActions待ちを避けるためsynthetic / terminal Discovery job IDを付けたsubmissionが大量に未処理となり、見かけ上の候補数だけ増えてResearch jobへmaterializeされなかった。探索主体workerのmulti-round経路ではself-describing `submit_discovery_round` を使い、`job_id` を付けない。
5. **同一Scheduled Chat runでは `run_key` を固定する。** round時刻・submission時刻・Actions待ち後の再開時刻ごとにrun_keyを変えると、1時間の探索量・連続round・停止理由の可観測性が壊れる。予定実行枠またはrun開始時刻から決めた1つのrun_keyを全roundで共有する。
6. **「提出済み」と「Research job化済み」を区別する。** submissionのGitHub保存が成功しても、Actionsのdedupe / materializationが未完了なら最終採用数として数えない。最終通知ではdurably submitted、validated、materialized、Research readyを区別し、未反映分を成功として水増ししない。
7. **Actions / state表示だけでround数を断定しない。** 過去には実際は7round以上保存されているのに`discovery-state.json`が第1roundのみを表示する可観測性不整合があった。必要ならimmutable submission群とrun_keyを正として実round数を確認し、集約stateは補助証拠として扱う。
8. **recoveryは原本を壊さず冪等にする。** transport不整合で失敗した過去submissionを救済する場合、原本を上書きせずdeterministic ingest / recovered artifactへ収束させ、同じsubmissionの二重replayを防ぐ。Actions完走前は復旧完了とみなさない。
9. **高重複windowは履歴でcooldownする。** 同じ軸の上位結果が既知で埋まる場合、語句を少し変えて機械的に再検索するのではなく、`discovery-state.json`のduplicate率・unseen率・acceptance率を使って後順位へ送り、引用方向・年月・隣接分野・具体的機構へ移る。
10. **検索結果の“候補数”より最終materialization率を見る。** 過去には多数の候補を送ってもtransport不整合や最終dedupeで実採用0件になったrunがあった。探索効率の評価ではraw hit数やsubmission candidate数ではなく、重複除外後のnovel candidate、validated submission、Research job materializationまでを分けて追跡する。

これらは探索量を減らすための保守策ではない。**無効な候補・無効なsubmission・既知論文への再アクセスを早期に落とし、節約した外部アクセスとrun時間を次の独立探索軸へ再配分するための規則**として適用する。

### search-window選択への反映

次windowを選ぶ際は、単純な「未走査か」だけでなく、**期待情報利得 / 外部アクセスコスト**も考慮する。具体的には、過去の `unseen_rate` と `candidate_acceptance_rate` が高く `duplicate_rate` が低いwindow、または未走査で重点テーマに直結する具体的機構queryを優先する。一方、直近runで高重複・空振り・低受理が続いた一般queryや厳密日付queryはcooldownへ送る。

ただし、この効率化は品質基準を緩める理由にしてはならない。候補の採否基準、一次資料精読のResearch契約、最終dedupe契約は従来どおり維持する。

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
