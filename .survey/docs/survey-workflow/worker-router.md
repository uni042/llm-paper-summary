# Worker router — workflow v10.12

この文書はScheduled Chat / Work系ワーカー（worker）の**唯一の実行手順正本**である。役割分岐（routing）、継続・停止、探索、研究、退避の判断を別文書から組み立て直してはならない。

ワーカーは実装リファレンス（implementation reference）や履歴互換資料（read-compatibility material）から手順を補完しない。必要な実装詳細は正規スクリプトが `[WORKER-GUIDE]`、`next_action`、`recovery_steps` として返す。実装リファレンスは保守・テスト用途に限定する。

**実行時の具体的な操作では、正規スクリプトが返す `[WORKER-GUIDE]` / `next_action` / `recovery_steps` を最優先する。** `[待機]` 中に依存する次操作へ進んだり、`[次]` を自己判断で飛ばしたり、`[手順エラー]` / `[正しい手順]` を無視して別経路へ迂回してはならない。機械案内とこの文書が矛盾した場合は、旧経路へ逃げず**そのrunでは機械案内に従って安全に処理し、矛盾の内容・採用した機械案内・影響を最終報告でユーザーへ相談事項として明記する。** ワーカーがその場で正本の意味を独自に上書きしない。

## 1. 開始時に読む状態

各実行（run）の開始時に最新 `main` HEADを取得し、同じHEADで次を読む。

- `.survey/work-queue/hot-dispatch.json`（存在する場合。ゼロ待ち開始用の再構築可能index）
- `.survey/work-queue/next-jobs.json`
- `.survey/work-queue/maintenance-cycle.json`
- `.survey/work-queue/discovery-state.json`
- 必要なら `.survey/work-queue/state.json`
- 出力品質が必要な場合は `.survey/templates/paper.md`

実際の起動時刻を1回取得し、`actual_invocation_start` として固定する。予定時刻や前回runの時刻を再利用しない。**タイムゾーン情報を必ず保持し、JSTの壁時計を `Z` / `+00:00` として偽装しない。** run-state正規化層は既知の「JST壁時計をUTCとして直列化した約9時間ずれ」だけを防御的に補正し、それ以外の実質的な未来時刻を拒否する。通常の時間枠は起動時刻から3600秒とする。通常のrun-state経路は必ずこの実起動時刻由来のdeadlineを使い、`seconds_to_next_scheduled_task` は過去の直接呼出しを読むための互換入力に限定する。新規runの時間判定を次回予定時刻から組み立てない。**残り600秒以下は新しい独立作業を開始しないための開始禁止窓**であり、すでに開始済みのResearch / Audit、既発行claim、既提出submissionのresult確認・正規repair、すでに開始済みDiscovery roundのprecheck/submission/result完了は継続してよい。残り600〜181秒で新しい論文claimや新しいDiscovery roundを開始してはならない。**残り180秒以下は最終handoff窓**とし、新規内容作業をせず耐久保存・既存非同期結果の確認・安全な引き継ぎだけを行う。開始禁止窓に入った時点で進行中作業が無ければ、そのrunは安全な引き継ぎ後に終了してよい。

### 1.1 run identity と scheduled slot

通常のScheduled Chat論文ワーカーは、実行ごとに名前を作り直さず**固定worker identity**を使う。

- 毎時 `:00`: `worker_id = scheduled-chat-00`, `scheduled_slot = 00`
- 毎時 `:30`: `worker_id = scheduled-chat-30`, `scheduled_slot = 30`
- 08:30専用run: `worker_id = scheduled-chat-30`, `scheduled_slot = 0830`

これに加えて、単発・臨時ワーカーは **`worker-N`（Nは0〜999999の数字）** を正式identityとして使用できる。単発ワーカーは `scheduled_slot = adhoc` とし、claim / 共有preload FIFO / Research-Audit品質preflight / immutable submission / run-stateの同じ正規経路へ参加する。`worker-N` を `:00` / `:30` / `0830` と偽装してはならず、08:30 maintenanceも担当しない。同時稼働する単発ワーカー同士では異なるNを使い、同一Nを再利用する場合はそのworkerの未完了claimを引き継ぐものとして扱う。

`worker_kind` は固定Scheduled Chatと `worker-N` の両方でtransport互換上 `scheduled_chat` とする。claim request、Library checkpoint marker、fallback envelope、run-state request、最終報告でこのidentityを一貫して使う。別名・時刻埋め込み名・共通名 `scheduled-chat-llm-survey` を新規runで生成しない。これにより各worker lineageを分離し、互いのactive claimを自分のclaimとして扱わない。

各runに一意な `run_key` を1つ作り、Discovery、run-state snapshot、最終報告まで同じ値を使う。`worker-N` も必ずrun-state requestを作り、固定2workerと同じ継続判定を使用する。

また、実際の起動時刻とは別に**予定実行枠（scheduled slot）**を開始時に確定してrun中固定する。`:00` workerは `HH:00`、`:30` workerは `HH:30` の予定枠を使う。08:30専用runの判定は実際の起動時計ではなく予定実行枠で行う。たとえば08:34に遅延起動しても予定枠が08:30なら第9節へ入り、09:30枠が08:59に早期起動した等の異常でも08:30専用runとは扱わない。

## 2. 共通ルーター

毎時 `:00` と毎時 `:30` の論文ワーカーは、**同じ論文処理規約・同じ手順**を使う。スケジュール時刻による役割差は設けない。run開始時に最新 `next-jobs.json` から **Research/Audit の ready 全件数**を `candidate_inventory` として取得する。`claimable` ではなく、原則 `claiming.ready_research_audit`、それが無ければ `counts.research.ready + counts.audit.ready` を使う。このrun開始時の値を固定し、次の1条件だけで今回の論文作業モードを決める。

- **`candidate_inventory >= RESEARCH_DISCOVERY_THRESHOLD` → 読解（Research / Audit）**
- **`candidate_inventory < RESEARCH_DISCOVERY_THRESHOLD` → 探索（Discovery）**

**この件数閾値は今回runでどちらを優先して処理するかを選ぶルーティング規則であり、Research / Discoveryどちらかのバンク・preload・direct-take機構を無効化する能力ゲートではない。** 二重用途バンクでは両レーンの在庫を同時に維持し、件数が閾値の上下どちらにあっても仕組み側はResearchとDiscoveryの両方を利用可能な状態に保つ。選ばれなかったレーンはそのrunで通常処理しないだけで、在庫生成・preload維持・次runからの利用を止めない。

閾値は `.survey/scripts/claim_window_policy.py` の正規policyから導出する。現在は、**各workerの論理在庫12件 × 容量設計上の同時worker基準6 × 4 = 288件**である。この6は在庫量・閾値を決める**容量サイジング基準であって参加worker数の上限ではない**。`worker-N` は6を超えても正規参加でき、共有poolを利用する。worker数・在庫幅の設計値を変更するときは閾値だけを別に手修正せず、同policyから連動させる。

**08:30 JSTの`:30`専用runだけ**は、この分岐より優先して第9節の日次更新・maintenance経路へ入る。通常runに「maintenance対象」という別条件は設けない。

モード決定後は、どちらのScheduled Chatから起動したかを一切条件分岐に使わない。探索なら第4節、読解なら第3節の共通手順をそのまま使う。`:00` 専用・`:30` 専用の探索手順、読解手順、overflow modeは作らない。

候補数は最新の耐久状態から毎run開始時に取得し、旧runや旧STATUSの推定値を再利用しない。候補数が現在の境界ちょうど288件なら読解を選ぶ。**一度選んだモードはそのrunの終了まで固定する。** run中に候補数が閾値を跨いでも再ルーティングしない。次回runの開始時にあらためて最新候補数で判定する。

runノルマの正規値は `.survey/scripts/worker_quota_policy.py` に一元化する。現在はResearch / Audit成功5件、Discovery成功8ラウンドである。Audit starvation防止の3件ブロックも同policyに置くが、これは**作業配分の公平性規則でありrun完了ノルマではない**。

- **読解モード**: 今回の起動中に **Research / Audit 合計で成功完了を最低5件**作る。Research job 1件とAudit job 1件は、同じ論文に対するものでも**別々に1件ずつ**数える。Researchは一次資料全文→5スロット→ワーカー自身のセルフレビュー→exact blob preflight合格→不変submission→submission result成功→最新mainへの反映確認まで、Auditも同じ提出前ゲート→不変submission→成功result→最新mainへの反映確認までを1件の完了とする。`blocked` / `deferred` / `rejected` や提出しただけのpending状態はノルマへ数えない。5件は停止上限ではない。最低5件を達成した後も、残り600秒の新規開始禁止窓に入るまでは、継続可能なResearch / Auditがある限り機械案内は `CLAIM_NEXT_RESEARCH_AUDIT` を返し、既確保standbyの昇格またはclaim windowの補充を行って同じ読解モードを継続する。曖昧な `CONTINUE_WORK` を最低件数達成後の停止・待機理由として扱わない。
- **探索モード**: 今回のrunで最低8つの**成功した正規schema v3 precheck**を完了させ、そのprecheckに対応するDiscovery submission/resultまで耐久反映する。**1つのprecheck `request_id` = 1ラウンド**と数える。同じprecheckから候補を複数submissionへ分割しても1ラウンドのままであり、逆に別の成功precheckなら同じprovider・同じ探索元でも別ラウンドとして数える。候補0件の成功precheckも、0件submission/resultまで正規経路を完了すれば1ラウンドに数える。8ラウンドは停止上限ではない。

handoff guard、platform/context limit、GitHub正本の読取不能、GitHub/Library双方への耐久保存不能などのhard stopはノルマより優先する。件数を満たすために弱い候補を採用したり、読解品質を下げたりしない。
### 2.0.1 ゼロ待ちhot dispatch（Research / Discovery共通）

通常runでは、`.survey/work-queue/hot-dispatch.json` が存在し、`direct_start_allowed=true` なら、**Actions resultを待ってから最初の内容作業を始めてはならない。** このindexは共有Research preload FIFOとDiscovery PRECHECKED preloadを1 readで公開する再構築可能な加速面である。`candidate_inventory` / `research_discovery_threshold` / `suggested_work_mode` を今回runの開始値として固定し、同時に通常のrun-state requestをmainへ保存するが、そのrequestには次の4項目も付けて**run-state Actionsは非同期の整合確認へ回す**。

- `candidate_inventory_at_start: <hot-dispatch candidate_inventory>`
- `work_mode_at_start: research | discovery`
- `research_discovery_threshold: <hot-dispatch research_discovery_threshold>`
- `hot_dispatch_generated_at: <hot-dispatch generated_at>`

run-state側はこの4項目の形式・policy整合性を検証し、最初の正規snapshotがまだ無いrunでは `route_source=hot_dispatch_direct_start` として同じrouteを固定する。`candidate_inventory` と閾値は選択モードを決めるための情報であり、direct-takeの技術的可否判定には使わない。hot-dispatchはResearch / Discoveryの両レーンを同時に公開し、`direct_start_allowed` は**今回選択済みレーンに準備済みpacketが存在するか**だけで決める。閾値からの距離・ガード帯を理由にdirect startを禁止しない。選択済みレーンに準備済みpacketが無い場合だけ従来どおりrun-state resultを待って開始する。08:30 maintenanceは常にhot dispatch対象外である。

**Research / Audit:** まず `research_resume.<worker_id>[]` を確認する。同一workerのactive未提出claimが載っている場合は、**新しいtake/claim/resultを待たず最古のforegroundを即時再開する。** `work_start_allowed=true` なら一次資料取得・全文読解を直ちに継続してよい。`record_write_allowed=false` の場合でも読解開始は止めず、同時に通常のrun-state requestを耐久保存してclaim fast pathの正規canonicalization/record-bank回復を走らせる。run-state resultの `auto_resume_recovery.foreground` または更新後の同じ `research_resume.<worker_id>[]` で `record_write_allowed=true` と正規routeが確定してから5スロットへ書く。resume packetは既存claimの再開専用であり、create-only takeを発行せず、別workerのpacketを取得しない。

同一workerのresume packetが無い場合だけ、`research[]` の最古packetから、`take_path=.survey/work-queue/direct-takes/research/<claim_id>.json` を**存在しない場合だけcreate**する。payloadは最低限 `schema_version:1`, `operation:direct_take_research`, packetの `claim_id/job_id/attempt_id`, 一意な `request_id`, `worker_id`, `scheduled_slot`, `run_key`, `actual_invocation_start`, UTC `requested_at`, `claim_window`, 上記4つのdirect-route値を持つ。create成功が排他的な担当確保であり、**その瞬間からpacket内 `job` の一次資料取得・全文読解を開始してよい。** createが既存ファイル競合なら同じindexの次packetへ進み、Actionsを待たない。claim laneは後段でpool claimを正規worker claimへ変換し、同じworkerのwindowを既定12件まで補充し、hot record bankを確保する。**Survey claim fast laneとrun-state derivationは別々のActions concurrency groupを使い、run-state処理待ちをdirect take canonicalizationの待ち行列へ混ぜない。両laneが同時にmainへ書く場合はforce pushせず、push race時に最新mainから正規再計算して収束させる。** 5スロットへ書き始める前には `direct-take-results/research/<claim_id>.json` が `status=ready_for_submission` / `record_write_allowed=true` になったこと、または対応canonical claim resultで同一 `job_id/claim_id/attempt_id` とrecord routeが確定したことを確認する。**読解開始はこれを待たない。**

**Discovery:** 正規selector方向に対応する `discovery.<direction>[]` の最古packetについて、packetの `take_path=.survey/work-queue/discovery-preload/claims/<preload_id>.json` を**存在しない場合だけcreate**する。payloadは `schema_version:1`, packetの `preload_id/discovery_bank/discovery_slot_path/preload_result_path`, `worker_id`, `run_key`, 一意な `request_id`, `claimed_at`, 90分後の `lease_expires_at`, `direct_take:true`, `scheduled_slot`, `actual_invocation_start`, 上記direct-route値を持つ。create成功が排他的なpreload担当確保であり、**直ちにpacketの `preload_result_path` にある20件を軽量評価し始めてよい。** さらに供給側はこの最初のdirect takeを検出した時点で、同じ `worker_id / run_key` のDiscovery in-flightが正規上限3本へ届くまで、候補を実際に持つPRECHECKED packetを最大2本追加で**自動予約**し、それぞれのrun固有schema v3 precheck requestも同じforeground laneでmaterializeする。追加予約は `auto_frontier=true` と元packetの `frontier_parent_preload_id` を持ち、別workerへ再配布しない。したがってworkerが最初のprecheckの `queued` / `in_progress` を観測してから「次を始めるか」を判断する必要はなく、**待機状態へ到達する前に最大3ラウンド分の作業フロンティアが供給済みになる**。hot-dispatchの `discovery_start_frontier` は開始時点で即読める追加cached候補を最大2packet公開し、direct-take resultの `reserved_frontier` は実際に同runへ予約された後続packetを示す。既に正式precheck済みのcached候補は軽量評価を進めてよいが、各roundのsubmissionは必ずそのround固有の正式precheck result / receiptを待ち、preloadで先に評価した候補のうち正式 `allowed_records` から外れたものは捨てる。直接開始・frontier先行評価は品質ゲートを省略せず、**候補を読む時間と正式precheck待ちを重ねるだけ**である。create競合なら同方向の次packetへ進む。frontier上限3は供給在庫の上限であり、3ラウンドを同時submissionする許可ではない。

hot-dispatchが欠落・破損、create競合を全packetで失敗、またはdirect-take正規化がrecovery_requiredになった場合は従来経路へfallbackする。ただし**Discoveryを選択済みで初回の後方引用PRECHECKED packetが0件でも、hot-dispatchの `discovery_fallback` / `fallback_start_allowed=true` があればrun-state resultを待ってはならない。** 同じ `run_key / worker_id / scheduled_slot / actual_invocation_start` を持つrun固有schema v3 precheck requestを、その固定 `provider / source_url / axis` から即時作成し、通常のrun-state requestは並行して耐久保存する。さらに `discovery_start_frontier` が非空なら、後方引用fallback requestを耐久保存した直後にそのPRECHECKED packet群から利用可能なものを順にcreate-only claimし、cached候補の軽量評価を開始する（旧互換の `discovery_start_lookahead` はfrontier先頭を示す補助面として残す）。これにより初回formal precheckがまだpendingでも実内容作業を持てる。`zero_wait_start_allowed` は非同期経路を即開始できること、`zero_wait_content_start_allowed` はcached候補を直ちに評価できることを区別する。lookahead自身もrun固有formal precheckが `ok=true / evaluation_allowed=true` になるまでsubmission禁止であり、in-flight上限3・古いresultのrecovery/evaluation優先規則を維持する。precheck laneはこのidentityからrun-stateを自動回復・更新するため、初回run-state resultは内容作業開始の同期障壁ではない。hot-dispatchは正本状態を置き換えず、submission可否は従来どおりcanonical claim / formal precheck / quality preflight / immutable resultが決める。

## 2.1 正規スクリプトを直接実行できない環境のfast-lane transport

Scheduled Chat等でリポジトリ内Pythonを直接起動できないこと自体は、Research / Audit / Discoveryを停止する理由ではない。GitHubへのread/writeが可能なら、**requestファイルをmainへ耐久保存し、対応するGitHub Actions fast laneに正規スクリプトを実行させ、resultファイルを読む経路**を現行の正規transportとして使う。この経路はmanual state編集ではない。

**GitHubのファイル作成・更新API/connectorを利用できる場合、それ自体をGitHub write可能と判定する。** ローカルshell、Python実行、`git push`、Actionsのmanual dispatch専用toolが無いことを、claim / run-state / preflight / submissionのwrite不能理由にしてはならない。新規request・direct-take・immutable descriptor等は、正規pathへGitHubのcreate-file相当操作でJSONを作成することで耐久化でき、そのcommitに反応するActions fast laneへ後段処理を委譲する。既存ファイルの更新が必要な段階では、直前に最新HEADと対象blob SHAを再取得してupdate-file相当操作を使う。

`transport_unrecoverable` / `durable_transports_unavailable` を申告してhandoffする前に、**今回必要な正規pathへの実writeを少なくとも1回は実際に試す。** write操作を一度も試していない、または「直接スクリプトを実行できない」ことしか確認していない状態はtransport障害ではない。create-only pathで既存ファイル競合が返った場合もwrite不能ではなく排他取得競合なので、routerが定める次packet/同一identity確認へ進む。

### 2.2 main writeのcommit集約

Scheduled ChatからGitHubへ直接耐久保存する場合、**同一論文・同一論理段階で、途中にActions起動や別workerからの可視化を必要としない複数ファイル更新は1回のcommitへ集約する。** 特にResearch / Auditの5スロットは、内容が完成してセルフレビュー可能になった時点でまとめて保存し、metadata / method / evaluation / results / positioningを1ファイルずつ別commitにしてmainを進めない。利用可能なGitHub transportが複数ファイルを1commitで更新できる場合はGit dataのtree/commit等の原子的な複数ファイル更新を優先する。

ただし、次の**耐久境界はまとめて潰さない**。claim request、Research quality preflight request、immutable submission、run-state requestなど、commit自体がActions起動・正規結果生成・handoff identity確定のトリガーになる境界は、それぞれ必要な順序を守って独立に耐久化する。`completed-submission request` は合格済みpreflight resultからGitHub側のpublication pipelineが自動生成する監査用の耐久記録であり、Scheduled Chatが追加writeする独立境界にはしない。preflight resultはdescriptor生成より前にmainへ耐久反映し、別attempt、別論文、別workerのpayloadを無関係に1commitへ束ねない。

GitHub transportが1ファイル単位のwriteしか提供しない場合は、存在しない原子更新を捏造せず、その環境で可能な最小commit数に留める。commit集約のために品質チェック・preflight・submission順序を変更してはならない。

### 2.3 一次資料取得回数の節約と再利用

Web/PDF取得のplatform上限はrunを途中終了させる実害があるため、Research / Auditでは**一次資料の全文読解要件を維持したまま、外部取得回数を可能な限り減らす。** 取得回数を節約するために抄録・検索断片・二次資料だけでResearchを完成させてはならない。

- claim後、同じ論文について既に利用可能な**一次PDF全文**がChatGPT Library等の耐久ファイル領域に存在するかをcanonical ID / arXiv ID / DOI / titleで確認できる場合は、Webへ再取得しに行く前にそれを再利用する。論文identityが一致し、欠落ページのない一次資料であることを確認する。
- 一次PDFをWebから取得する必要がある場合は、抄録ページ→HTML各節→PDF各ページのような細切れ取得を常用せず、まず**完全な一次PDFを1回でダウンロードする経路**を試す。完全な一次PDFのダウンロードに成功し、Libraryへの保存が利用可能なら、**そのPDFをLibrary側の一時キャッシュへ保存してから読解を継続することを原則必須とする。** Web上のPDFをページ単位で何度も取り直しながら読む経路を、Library保存可能なのに選んではならない。全文取得後の5スロット作成、preflight修復、submission failure修復、次runでのactive claim再開でも同じLibraryコピーを再利用し、同一版のPDFをWebから再取得しない。
- Libraryへ保存する一次PDFには、少なくともcanonical IDまたはarXiv ID/DOI、一次資料URL、取得時刻、判別可能なら版番号を対応付け、別論文・別版を誤再利用しない。二次資料や検索断片を一次PDFキャッシュとして保存しない。
- **完全な一次PDFそのものをダウンロードできない場合だけ、従来の取得方法へフォールバックする。** 具体的には、公式/著者公開HTML、arXiv HTML、PDFの必要ページ範囲取得など、利用可能な一次資料経路を少数回の範囲取得で最後まで読む。このフォールバックでも既に取得済みの節・ページを不必要に取り直さず、同一内容を複数providerから重複取得しない。PDFダウンロード不能を理由に抄録や二次資料だけでResearchを完成させてはならない。
- **Library上の一次PDFは恒久保存しない。** active claim、preflight修復、submission/repair待ち、handoff後の再開などで同一PDFを再利用する必要がある間だけ一時キャッシュとして保持する。その論文について成功result＋main反映が確定した、または `blocked` / `deferred` / `rejected` 等の終端状態が耐久反映され、未完了repair・再提出・handoff再開で当該PDFを使う必要がなくなった時点で、そのrun中に保存したLibrary PDFを削除する。削除前に別workerや未完了attemptが同じPDF identityを再利用中でないことを確認する。
- PDF/HTMLの同じ内容を複数providerから重複取得しない。現在の一次経路が実際に不完全・取得不能・破損・版不一致の場合だけ代替経路へ切り替える。
- 修復ループでは、品質検査が要求する箇所だけを既取得の全文から再確認し、論文全体をWebから取り直さない。
- Discovery中は候補identityと採否判断に全文PDFが不要なら取得しない。Research/Auditとしてclaimされた時点で初めて全文取得する。
- 取得節約によって出典確認、全文読解、一次資料優先、品質基準を弱めてはならない。必要な一次情報がキャッシュにもWebにも無い場合は推測せず、正規のblocked/deferred経路を使う。
- **単一論文の一次資料全文を取得できないことはrun-level hard stopではない。** foregroundで正規取得経路と利用可能な代替一次資料経路を試しても全文を確保できない場合、そのattemptを同じ `attempt_id` のstatus-only immutable descriptorとして `.survey/work-queue/submissions/<kind>/<attempt_id>.json` へ `blocked`（一時的・再試行価値がある場合は `deferred`）で耐久化する。理由と実際に試した一次資料経路を `reason` / `retrieval_evidence` に残し、推測で5スロットを作らない。descriptorがmainへ耐久保存された時点でそのclaimは次foreground選択から外れるので、**同じrunの最古standbyを直ちに開始する。submission result待ちを同期障壁にせず、成功数にも数えない。** `research_resume.<worker_id>[]` が `status_only_submission_path` / `status_only_descriptor_base` / `source_unavailable_next_action` を返している場合はそれを正本テンプレートとして使う。

**ノルマを達成したrunの最終報告には、取得上限を避けるために実際に使った工夫を短く記載する。** 例: 「Library上の既取得PDFを再利用」「PDFを1回だけ取得して修復でも再利用」「同一論文の再ダウンロードを回避」「Discoveryで不要な全文取得を省略」。取得回数や再利用回数を正確に数えられる場合は併記し、計測できない場合は推測値を作らず、実施した工夫だけを報告する。ノルマ未達時も取得上限が原因または近因なら、どの取得が上限に寄与したかを障害診断へ残す。

Research / Auditのclaimは次の順で行う。

### 2.4 Research / Auditの可変claim window（foreground 1 + standby N）

#### 二重用途バンク（dual-purpose bank）上の共有paper preload FIFO

A〜AFの32個のcanonical bankは、**Research preload / Discovery preload / Research-Audit hot stagingの3面を同時に持つ二重用途バンク**として扱う。各bankには従来の5つのResearch/Audit record slotに加えて、再構築可能な `research-preload.json` と独立した `discovery-preload.json` を置く。3面は互いに上書きせず、同じbankが読解用在庫と探索用在庫を同時に保持できる。**Research在庫とDiscovery在庫の維持はcandidate件数や今回runの選択モードから独立させ、片方の件数条件を理由にもう片方のpreloadを停止・空化しない。**

Research / Auditの事前装填はworkerごとの固定本数ではなく、全Scheduled Chat / worker-Nで共有するFIFO poolを使う。claim stateを正本とし、`research-preload.json` はその派生インデックスである。共有pool目標は `claim_window_policy.py` から導出し、現在は **12件/worker × 6 worker × 2セット = 144件**（workerへadopt済みを含む）。各Research claimは `pool_order` をcanonical bank順へround-robinして `stock_bank` / `stock_lane=research` を持ち、通常144件なら32bankすべてへ4〜5件ずつ読解用在庫を分散する。cold Research stockは5 record slotを予約しないため、全bankへ読解用在庫を置いてもhot staging容量は先食いしない。

- 共有poolのclaimは特定workerに固定しない。Scheduled Chat requestが来た時点で、そのrequestのjob type / 明示job_id条件を満たす最古のpool claimから不足window分をadoptする。
- 通常はhot-dispatchのcreate-only `direct-takes/research/<claim_id>.json` を先に置き、そのmarkerを**Actions前の排他的予約**として扱う。共有poolの通常allocatorはmarker済みclaimをadopt対象から除外するため、同時・不規則なworkerでも同一claim / jobを2 workerへ渡さない。claim fast laneはmarkerを後段で正規claimへ変換し、既存のsurvey-claim-main concurrencyとpush-race再計算でcanonical stateを確定する。adopt後も `stock_bank` は維持する。record slotを使うのはhot sliceだけで、hot化時はまず同じ `stock_bank` の5スロットを使い、そこが他Research stagingで使用中の場合だけ別のfree/reusable bankへ退避する。
- pool内の順番はpool_orderで固定する。一度装填済みの論文を後から到着した高priority論文で追い越させない。新しい補充論文は常にpool末尾へ追加する。
- workerへadoptした後は、そのworker内のpipeline_orderの末尾へ接続する。したがって既存standbyを飛び越さず、foreground終端時は従来どおり最古standbyが昇格する。
- pool目標は待機poolだけの本数ではない。現在144件のうち6 workerが各12件をadopt済みなら72件がworker在庫、残り72件が共有待機となる。workerごとのwindowは共有poolの専有枠ではなく、pool不足時は取得可能な範囲だけadoptし、正規direct allocationへ進む。
- worker数や起動順に固定laneを割り当ててはならない。`stock_bank` はworker専用bankではなくResearch FIFOのシャードである。特定workerが長期間起動しなくても論文が滞留せず、どのworkerも任意bankのResearch/Discovery在庫を利用できる構造を維持する。
- pool claimのjobがreadyでなくなった、terminalになった、または耐久submissionで処理済みになった場合はpoolから解放する。pool leaseは保守runで必要時だけ更新し、lease更新を理由に順番を変更しない。
- Audit-only等でrequestのjob type条件に合わない先頭claimはそのrequestでは飛ばしてよいが、claim自体のpool_orderは変更しない。通常のResearch/Audit混合workerからは再びFIFO対象となる。
- 共有poolが一時的に空の場合は従来の直接allocationへ安全にフォールバックしてよい。pool不足やbank不足だけをrun停止理由にしない。

Scheduled Chat / worker-NのResearch / Auditは、**同時に精読する論文は常に1件**のまま、担当確保だけを可変長windowで先行させる。既定は `claim_window=12`、つまり **foreground 1件 + standby最大11件** とする。12は `claim_window_policy.py` の設定値であり、worker手順へ固定ロジックとして複製しない。`max_jobs=1` は精読並列度を表し、claim windowの大きさを表さない。

- claim resultの `pipeline_role=foreground` / `pipeline_position=1` の1件だけを本文読解・5スロット作成対象にする。`standby` は担当権だけを先に確保し、foregroundになるまで本文を先読みしない。**先頭4件だけをhot inventoryとしてrecord bank予約済みに保ち、5件目以降のcold standbyはbankを消費しない。**
- foregroundが `completed` / `blocked` / `deferred` / `rejected`、またはimmutable descriptor生成により現在claimから外れたら、**既確保standbyの先頭を即座に次foregroundとして開始する。ここで新しいclaim resultを待たない。**
- standby補充はhot 4件を使い切ってから始めない。正規policyは**hot sliceの半分を消費した時点**で補充を開始し、現在のwindow 12ではactive 10件以下が低水位となる。これにより通常はbank-readyな2件を残したまま非同期claim/bank昇格を走らせる。残り600秒より多くclaim可能jobがあるなら補充用claim requestを1件だけ発行し、可能な限りwindow 12へ戻す。windowを変更した場合も低水位は同policyから導出する。**補充result待ちはforeground読解の同期障壁にせず、既にhotなforeground/standbyの処理を続ける。**
- 既に補充claim requestがpendingなら重複requestを出さない。返ったresultでwindowを更新し、foregroundは変えない。
- 残り600秒以下では新しいstandby補充claimを発行しない。ただし600秒窓へ入る前に発行済みのclaimは既発行claimとして扱い、foreground終端時にstandbyへ昇格して処理を継続してよい。残り180秒以下の最終handoff規則は従来どおり優先する。
- claim allocatorは同一Scheduled Chat workerのactive claimを `pipeline_order` で並べ、最小をforeground、それ以降をstandbyとする。旧claimに `pipeline_order` が無い場合は正規allocatorが移行時に順序を付与する。
- 各claimには従来どおり独立したattemptを割り当てる。全Research claimは読解用 `stock_bank` を持つが、5つのrecord slotを予約するのは**hot sliceだけ**である。cold standbyがhot sliceへ昇格する際はclaim fast laneのbank reconciliationでまず `stock_bank` をrecord bankとして使い、使用中なら別bankへ割り当てる。bank不足時は既存Library fallbackを使い、bank不足だけをrun停止理由にしない。
- `claim_window` は1〜24の範囲で変更可能で、既定値は正規 `claim_window_policy.py` から導出する（現在は12）。通常hot bank幅は4件で、6 worker同時稼働なら通常bank使用は最大24件となり、32 bank中8件をrepair・例外用に残す。精読並列度 `max_jobs=1` は変えない。


**初回claimのfallback高速経路:** hot-dispatch direct takeを利用できない場合に限り、通常run開始時のrun-state request resultが `work_mode=research`、`gate.required_action=CLAIM_NEXT_RESEARCH_AUDIT` を返し、同一runにまだclaim request/result・active assignment・submissionが存在せず、残り600秒より多い場合は、`.github/workflows/survey-run-state.yml` が**同じActions実行・同じcommit内で初回claimだけを自動生成・割当してよい。** このとき元のrun-state resultに `auto_initial_claim` が付与され、そこに `request_id` / `result_path` / statusが記録される。workerは `auto_initial_claim.status=allocated` ならそのclaim resultを正本として直ちに担当論文へ進み、同じrunの手動claim requestを重複発行しない。自動初回claimが対象外・失敗・未生成の場合だけ以下の通常claim手順へ戻る。この自動化は**各runの初回claim request 1回だけ**に限定するが、そのrequestが確保するassignment数は固定しない。run-state resultの `claim_window` を正本として foreground 1件 + standby N件を可変数で確保する。共有preload FIFOに必要数の整合したlogical claimがある通常ケースでは、それらを一括adoptし、**先頭4件だけをbank-ready化して**claim resultを生成する軽量経路を使う。12件すべてへbank予約を作らないため、深い在庫化後も初回allocationの速度を維持する。pool不足、repair、bank不整合、複数初回requestの同時回収などでは従来の `claim_fast_path.py` へ安全にフォールバックする。以後のclaim window補充requestもAudit starvation判定を含む通常のclaim前判断を維持する。

1. 最新main HEADとclaim stateを再取得する。**同一workerにactiveな未提出claimがある場合は新requestを出さない。直前claimのexact attemptに対する不変descriptorがmainへ耐久保存済みなら、そのclaimがまだactive表示でも次requestを出してよい。claim fast laneは新request処理の冒頭でdescriptor-backed claimを正規解放してから新jobを割り当てる。**
2. 一意な `request_id` を作り、`.survey/work-queue/claim-requests/<request_id>.json` をmainへcommitする。通常Scheduled Chatのrequestは `schema_version: 1`、`request_id`、`worker_id`、`worker_kind: scheduled_chat`、`requested_at`、`max_jobs: 1` に加え、今回runで固定した **`run_key`、`scheduled_slot`、`actual_invocation_start`** を持つ。これら3項目はclaim resultへ耐久伝播し、worker別増分run-state cacheをclaim結果だけで更新するために使う。旧requestで3項目が無いものは引き続き処理するが、その場合は該当workerのcacheを安全側に無効化し、次のrun-state導出をcanonical factsから再構築する。通常は `job_types: ["research", "audit"]` とし、第3節のAudit starvation防止条件に達したclaimだけ `job_types: ["audit"]` に限定する。 **`requested_at` は必ずUTCで、末尾を `Z` または `+00:00` とする。JST等の `+09:00` をそのまま入れてはならない。** `actual_invocation_start` はoffset-aware timestampなら受理され正規化されるが、claim requestの `requested_at` だけは実装契約としてUTC限定である。例: `2026-09-23T04:52:00+00:00`。
3. このpushで `.github/workflows/survey-claim-fast.yml` が起動し、最新main上で共通 `claim_fast_path.py` を実行する。通常allocationとbank予約は `claim_worker_with_banks.py` を使い、Library checkpoint barrierは割当前に維持する。repair用の重い回復走査は新規assignmentがrepair対象のときだけ実行し、canonical record routeはbank予約時にclaim/resultへ直接書く。ワーカー自身が `claims/*.json`、`jobs/*.json`、`state.json`、`next-jobs.json` を直接編集してclaimを再現してはならない。
4. 同じ `request_id` の `.survey/work-queue/claim-results/<request_id>.json` を確認する。未生成なら固定時間sleepや定周期pollingへ入らず、第7.0節の待機ミクロタスクを1件処理してから同じresultを再確認する。resultの `ok`、`assignments`、`attempt_id`、`claim_id`、`record_bank` / `record_bank_fallback`、`claim_window` / `claim_refill_threshold`、`pipeline_role` / `pipeline_position`、`foreground_job_id` / `standby_job_ids`、`next_action` / `instructions` を正本として以後の処理を行う。初回resultが複数件を返しても本文読解はforeground 1件だけ開始し、standbyは昇格まで読まない。
5. **通常claim request経路のclaim result待ちは受動待機にしない。** 第2.0.1節のResearch direct takeはcreate成功直後から全文読解を開始できるため、この待機規則の対象外である。通常request commitから60秒未満は `MONITOR_CLAIM_FAST_LANE` として、同じrequestを起動した `Survey claim fast lane` のActions runを確認し、`queued` / `in_progress` ならjob/step状態を確認する。並行して同一workerの未解決submission、`retryable` / repair待ち、active claim整合だけを軽く監査し、第7.0節の待機ミクロタスクを1件処理してから最新 `main` と同じ `request_id` のresultを再確認する。この作業サイクル中に別claimを発行したり、割当未確定の次論文本文を先読みしてはならない。
6. request ageが60秒以上でも別requestを発行しない。Actionsが `failed` / `cancelled` なら同じrequestの正規回復へ進み、`queued` / `in_progress` / success後の反映待ちなら同一identityの監視を継続する。claim fast laneはpush起動に加えて**10分周期で未result requestを定期回収**するため、一時的なActions失敗・cancel・push競合でrequestだけ残っても新requestを捏造しない。

**並列workerの扱い:** `max_jobs=1` は**同一worker内で同時に本文を精読するforegroundが1件**という制約である。各worker lineageは正規policyの `claim_window` 上限までactive claimを持てるが、2件目以降はstandbyであり本文処理しない。このforeground直列制約と可変claim windowは同一worker / 同一論理worker lineage内だけに適用する。`:00` worker、`:30` worker、その他の独立workerは、別 `worker_id` と別record bankで同時にResearch / Auditを進めてよい。他workerのactive claim、他workerのclaim request、またはclaim fast lane上で先行requestが処理中であることを理由に、このworkerのrunを停止・終了・handoffしてはならない。`.github/workflows/survey-claim-fast.yml` の `concurrency: survey-claim-main` は**claim割当commitの競合回避だけを直列化するもの**であり、論文精読そのものを全worker間で直列化するものではない。自分のrequestがfast lane待ちなら第7.0節の待機ミクロタスクを挟みながら同じ `request_id` のresultを再確認し、割当後は返された別job / record bankで処理を続ける。他workerのclaimを自分の未完了claimとして扱わない。

Research / Auditのcompleted submissionは、**ワーカー自身の意味品質セルフレビュー + 同期軽量セルフチェック + exact blob preflight** を通してからfast laneへ送る。

**非同期preflightへ送る前の同期軽量セルフチェックを必須とする。** 目的は品質基準を追加することではなく、固定済みの構造・段落・説明量不足をActions往復の前に見つけることにある。ローカル/Work等でrepository Pythonを直接実行できる場合は、5スロット保存後に次を実行する。

```bash
python .survey/scripts/research_quality_selfcheck.py \
  --kind <research|audit> \
  --attempt-id <attempt_id> \
  --job-id <job_id> \
  --record-bank <bank> \
  --paper-path <paper_path>
```

このスクリプトは `prepare_completed_submission.py`、正規renderer、`paper_quality_gate.py` をそのまま再利用し、request/result/submission/queue stateを作らない。**`selfcheck_passed=true` になるまで非同期research-preflight requestを作らない。** FAILなら一次資料に基づいて指摘されたslotだけを直し、同期セルフチェックを再実行する。

Scheduled Chat等でrepository Pythonを直接起動できない場合も、このセルフチェック自体を省略しない。5スロットをpreflightへ送る前に、少なくとも次を**手元のslot内容だけで同期確認**する。

- `metadata.summary` は180文字以上、`metadata.list_summary` は45〜180文字程度で「具体的に何をしたか」を含む。
- `problem_method.problem` は250文字以上、`novelty` は180文字以上、`method_overview` は500文字以上を構造化validationの最低条件として満たす。
- `components` は2個以上、各 `description` は240文字以上。さらに正規renderer後の手法H3が3個以上になる通常ケースでは、**「手法のあらまし」、各component、「全体のデータ／制御の流れ」を含む各手法構成要素を2説明段落以上**にする。1段落へ長文を詰め込んで文字数だけ満たさない。
- 評価条件、比較対象、実機/シミュレーションのscope、代表結果、負の結果・境界条件、品質影響、限界、既存研究との差を空欄にしない。`results.overview` は180文字以上、`key_results` は最低1件を持つ。
- 固定の公開品質基準であるUTF-8 4,500 bytes、説明文2,200文字、説明10段落、手法4段落、日本語比率70%以上、裸の英語専門語0件を十分な安全余裕付きで満たすよう確認する。厳密なrender後計測は後段のexact blob preflightが最終判定する。

同期セルフチェックは**最適化用の前段**であり、exact blob preflightを置き換えない。セルフチェック合格後も必ず新しいresearch-preflight requestを作り、Git blob SHAとdescriptor fingerprintを含む正規PASSを得てから提出へ進む。
**品質基準は固定する。** 提出前preflight、submission processor、repository-wide品質監査は `.survey/docs/survey-workflow/paper-quality-audit.md` に固定された同一基準を使う。ワーカーや監査タスクが品質閾値・要求項目・本文量・手法要件を独自に強化・緩和してはならない。変更は想定外挙動、解析バグ、移行/互換バグの修正に限る。`書誌情報` の著者名・所属等を品質計測から除外する扱いは、本文品質への英語メタデータ混入を防ぐ既知バグ修正として固定基準に含める。

**品質検査は隠しテストではない。** Research / Auditは5スロットの執筆前に同文書の公開済み固定基準を確認し、一次資料に十分な根拠がある限り、本文量・説明段落数・手法説明などを最低閾値ぎりぎりではなく**少し余裕を持って**作成する。これはレンダリング後の計測差、除外領域、表記揺れ等で不要なpreflight FAILが生じるのを避けるための安全余裕（safety margin）であり、品質閾値そのものを引き上げる指示ではない。文字数稼ぎの冗長化、同内容の重複、一次資料にない推測で余裕を作ってはならず、情報密度と従来の説明品質を維持する。

1. 5スロットの内容を作り終えた時点で、まだcompleted requestを出さず、ワーカー自身が一次資料と照合して意味品質を再確認する。少なくとも「一次資料を最後まで読んだ」「推測で穴埋めしていない」「概要と一覧文で固有の貢献と代表結果が分かる」「end-to-endの手法機構が説明されている」「評価条件・baseline・結果条件が明示されている」「限界と既存研究との差が具体的」の各項目を再点検する。
2. セルフレビュー後の5スロットだけをclaim result指定のrecord bankまたは現行fallbackへ完全保存する。次に一意な `request_id` を作り、`.survey/work-queue/research-preflight/requests/<request_id>.json` へ `schema_version: 1`、`operation: research_quality_preflight`、`request_id`、`kind`、`attempt_id`、`job_id`、`record_bank`、必要なら `paper_path` / `expected_blob_sha` と `self_review` を保存する。Scheduled Chatではさらに今回runで固定した **`worker_id`、`run_key`、`scheduled_slot`、`actual_invocation_start` を4項目そろえて保存する。** 加えて新規requestではoffset-awareな `requested_at` を保存し、同一attemptで複数回preflightした場合の順序判定に使う。旧requestで `requested_at` が無い場合はGit導入順とrequest identityから互換的に判定する。 これらはpreflight result→completed監査記録→immutable descriptor→submission resultへそのまま耐久伝播し、submission側から同一runのrun-stateを自動導出するidentityになる。旧requestで4項目が無いものはread compatibilityを維持し、自動導出できない場合だけrun-state request fast laneへ戻る。`self_review` は `primary_source_read_to_end`、`no_unverified_inference`、`summary_and_list_summary_specific`、`headline_result_grounded`、`method_end_to_end_explained`、`evaluation_conditions_and_baselines_explicit`、`results_conditions_and_interpretation_explicit`、`limitations_and_positioning_specific` の8項目をすべて `true` にする。事実として満たしていない項目を形式的にtrueにしてはならない。同じ内容を再検査するときも既存request/resultは書き換えず、新しい `request_id` を使う。
3. `.github/workflows/survey-research-quality-preflight.yml` が `research_quality_preflight.py` を実行し、実blob SHAから**submission processorと同じ構造化record validation・renderer・paper quality gate**を走らせる。同名resultを `.survey/work-queue/research-preflight/results/<request_id>.json` へ返す。**preflight requestをmainへ耐久保存した時点で、その論文の5スロットは結果が返るまで凍結し、`preflight-pending` として本文foregroundから一時退避してよい。** 同一workerでは新しくpreflightへ入れる先行窓を最大2件とし、`preflight_pipeline_capacity_remaining > 0` のときだけ次の完成済み論文を追加でpreflightへ送る。これは**入場制限**であり凍結解除条件ではない。競合・旧実装等でpending/PASS待ちが3件以上存在しても、既にpreflightへ入った全論文は凍結したまま `preflight_parked_*` に残し、3件目を本文foregroundへ戻して編集してはならない。`preflight_pipeline_overflow_count > 0` は異常の可視化であり、追加preflightを止めるだけである。既確保standbyがあれば最古standbyを唯一の本文foregroundへ昇格して精読を開始する。したがってpreflight pendingだけを理由に固定時間sleep・定周期polling・待機ミクロタスクへ落ちない。新着preflight resultは本文作業の区切りで回収し、最新resultがFAILなら凍結を解除してその古いattemptをpipeline順でforegroundへ戻し、指摘slotの修復を優先する。PASSならdescriptor自動生成まで凍結を維持する。preflight-pending論文は内容編集中ではないため、**同時に本文を精読・5スロット編集する論文は常に1件**という制約は維持される。2件のpreflight overlap上限に達し、他に実行可能な本文作業が無い場合だけ第7.0節の待機ミクロタスクへ戻る。
4. resultが `preflight_passed=false` ならcompleted requestを作らない。`validation_errors` / `quality.failures` を全部確認し、指摘されたslotだけを一次資料に基づいて修正してから、新しい `request_id` でセルフレビューとpreflightをやり直す。これはsubmission failureではなく**提出前の通常修正ループ**であり、run終了理由にしない。
5. resultが `preflight_passed=true` になったら、Scheduled Chatはcompleted requestを手動作成せず、同じ `survey-research-quality-preflight` pipelineにdescriptor生成を任せる。pipelineは合格resultの `kind` / `attempt_id` / `job_id` / `record_bank` / `paper_path` とexact `preflight_result` から `.survey/work-queue/completed-submission-requests/<attempt_id>.json` を監査用に自動生成し、続けて正規immutable descriptorを作る。
6. 自動pipelineと互換回収用 `.github/workflows/survey-completed-builder-fast.yml` はdescriptor生成前に `preflight_result` を検証し、preflight時のdescriptor fingerprintと現在の5スロットblob SHAが1つでも違えば拒否する。したがって**合格後にslotを変更した場合は必ず再preflight**する。壊れた・期限切れのcompleted requestは `.survey/work-queue/completed-submission-failures/` に内容ハッシュ付きで隔離し、他requestのdescriptor生成を止めない。Scheduled Chatがcompleted descriptorを直接作成・更新してはならない。
7. pipelineが1件以上のdescriptorを耐久反映したら `.github/workflows/survey-submission-fast.yml` を**バッチ全体で1回だけ**dispatchする。submission laneは個別descriptorごとのworkflow起動ではなく、最新main上の未確定immutable descriptorをまとめて列挙し、既存のbounded parallel batch processorでdrainする。processor側のquality gateは防御的な二重検査として残す。
8. 同名の `.survey/work-queue/results/research/<attempt_id>.json` または `audit/<attempt_id>.json` を確認し、`ok`、終端status、`next_action` / `recovery_steps` に従う。Scheduled Chatのrun identityがdescriptorまで耐久伝播しており、同一runのrouteが既にrun-state cacheへ確定済みなら、submission fast laneはsubmission result・paper・queue反映と**同じmain commit**に `.survey/work-queue/run-state/results/auto-*.json` の正規snapshotを生成する。`.survey/work-queue/run-state/latest/<worker_id>.json` は最新snapshotを引くためのindexにすぎず、継続判断の正本は従来どおりresult本体である。descriptorをmainへ耐久保存した時点でそのattemptは「提出済み」とする。**提出済みsubmissionのresult待ちはResearch / Auditの継続を止める同期障壁にしない。** 同一workerはclaim window内に複数の未提出active claimをstandbyとして保持してよいが、本文読解・5スロット作成を行うforegroundは常に1件だけとする。foregroundを耐久提出したら、既確保standbyがあれば最古standbyを直ちに次foregroundへ昇格し、低水位なら非同期でwindowを補充する。未確定submissionが何件残っていても、残り600秒より多く継続可能なResearch / Auditがある限り同じ直列処理を続ける。未確定resultは耐久identityを保持して並行監視し、終端resultが見えた時点で `next_action` / `recovery_steps` を回収する。
9. **1 attemptにつきcompleted descriptorは1本だけ**とする。preflight中の修正は同じattemptのrecord bankを直して新しいpreflight requestを作るが、completed descriptor生成後に同じ `job_id / attempt_id` の `repair1`、`repair2` 等を追加して修正しない。
10. 防御的なsubmission側検査でなお `content_validation` / `repair_required` になった場合だけ、そのfailure resultがmainへ耐久保存されたことを確認した後、同じjobを `job_ids: [<job_id>]` で指定した新しいclaim requestへ回す。新しいclaim_id / attempt_idで指摘slotを修正し、**再びセルフレビュー→preflightから**やり直す。全文読解済み成果は捨てない。
11. failure resultが `retryable=true` の場合は、同じattemptの別descriptorを作らない。既存の同一descriptorをsubmission laneのbounded recoveryに任せ、同じresultを再確認する。`retryable=false` かつ `repair_required` でもないstate/transport guardは、返された回復指示に従う。

Discovery precheckも、ローカルCLIがない場合は `.survey/work-queue/discovery-precheck/requests/<request-id>.json` をmainへcommitし、`.github/workflows/discovery-precheck.yml` に `process_discovery_precheck.py` を実行させ、同名resultを読む。Discovery precheck laneも**5分周期で未result requestを定期回収**する。Discovery submissionは既存のqueue処理経路へ流し、Research jobやstateを手で生成しない。Discovery submissionは既存の10分周期recoveryで未完了を回収する。

**Discovery precheckが `ok=true` / `evaluation_allowed=true` / `decision=READY_FOR_EVALUATION` になった時点では、そのroundはまだ完了していない。** 対応する候補評価を行い、0件を含む正規Discovery submissionを耐久保存し、対応resultまたは明示的hard stopまで進める。`READY_FOR_EVALUATION` のresultだけを残して最終応答・通常handoffへ進んではならない。precheck workflowは成功resultの公開時に同じ `run_key` のrun-state再導出requestを自動生成し、`discovery_evaluation_pending=true` を最新snapshotへ反映する。したがって最終化ゲートが `CONTINUE_DISCOVERY_ROUND` を返す間は、候補枯渇・Actions待ち・古いrun-state snapshotを終了理由にしない。

**重要:** 「ローカルPython/任意コマンド実行機能がない」は、GitHub read/writeと上記fast laneが利用可能な限り `platform_limit` / hard stopではない。fast lane自体がGitHub/API/認証/Actions障害で利用不能になった場合だけ、第6節の保存障害・退避と第7節の停止判定へ進む。

claim requestでは `request_id` をrequestファイル名のstemと完全一致させ、`requested_at` はUTCの `Z` または `+00:00` で保存する。`:00` は常に `worker_id: scheduled-chat-00`、`:30` は常に `worker_id: scheduled-chat-30` を使う。

## 3. 読解（Research / Audit）の共通処理ループ

1. 最新queueと現在の担当確保状態（claim state）を取得する。
2. 担当確保は第2.4節の可変claim windowに従い、同一workerが**foreground 1件 + standby N件**を先行確保してよい。`max_jobs=1` は担当確保数ではなく、**同時に本文を精読するforeground並列度が1**という意味である。通常priority順を維持しつつ、**Audit starvation防止をpriorityより優先**する。`.survey/scripts/worker_quota_policy.py` の `AUDIT_STARVATION_BLOCK_SIZE=3` に従い、foreground開始順を3件ずつのブロックとして扱い、claim windowの初回確保・pool adopt・補充の各段階で、利用可能なAuditがあるなら各3件ブロックに少なくとも1件Auditが入るようallocatorが順序を調整する。Auditがその時点で他workerに取得済み等で利用不能なら待たず、残りは通常priority順で埋める。この「3」は配分規則であり、runの成功完了ノルマ5件とは別である。
3. 通常claim request経路でclaim result待ちなら同じ `request_id` を保持する。別requestを発行して回避しない。**第2.0.1節のdirect takeで担当確保済みならcanonical claim resultを待たず本文読解を続け、5スロット書込開始前にだけrecord route確定を確認する。** 通常requestでageが60秒未満ならActions run/job/stepと同一worker transport状態を確認し、第7.0節の待機ミクロタスクを1件処理してから同じ対象を再確認する。 60秒以降も受動的に終了せず、Actions状態と正規回復可否を確認しながら同一requestを追跡する。
4. claim resultの `record_bank` / `record_bank_fallback` をそのまま使う。ワーカーが別bankを選び直さない。
5. 一次資料本文を最後まで読み、抄録や検索断片から欠落情報を推測しない。
6. `metadata`、`problem_method`、`evaluation`、`results`、`positioning` の5スロットを完成させる。
7. **GitHub上の公開paperへ出す前にワーカー自身で意味品質をセルフレビューする。** 一次資料との整合、概要・一覧文の固有性、代表結果、end-to-end手法、評価条件/baseline、結果の条件と解釈、限界・関連差を読み返し、不十分ならこの段階で5スロットを修正する。単にチェック項目をtrueにするだけで済ませない。
8. セルフレビュー済み5スロットをrecord bankへ耐久保存した直後、**非同期requestを作る前に上記の同期軽量セルフチェックを必ず通す。** repository Pythonを直接実行できる場合は `research_quality_selfcheck.py` を使い、使えないScheduled Chatでは同じ固定基準をslot上で同期確認する。`selfcheck_passed=false` または手元チェックで不足があれば指摘slotだけを修正して再セルフチェックし、合格してから第2.1節の `research-preflight` laneでexact blob validation + renderer + paper quality gateを実行する。`preflight_passed=false` なら返された全指摘を修正して新しいpreflight requestで再検査する。合格後にslotを変更した場合も再検査する。
9. `preflight_passed=true` のexact resultを得たら、Scheduled Chatは手動のcompleted request writeを挟まず、GitHub側のpublication pipelineがexact blob fingerprintを再照合して監査用completed requestとimmutable descriptorを自動生成するのを追跡する。**その間にpreflight overlapで次foregroundへ進んでいる場合は、その本文作業を不必要に止めず、PASS側は自動descriptor生成へ任せる。** descriptorがmainへ耐久保存された時点で提出済みとみなし、submission result待ちは次claimの同期障壁にしない。pipelineが終了したのにdescriptorが無い場合は `.survey/work-queue/completed-submission-failures/` とworkflow結果を確認し、該当sourceだけを正規修復する。status-only `blocked` / `deferred` / `rejected` は第3.1節4項の最小descriptorを従来どおりsubmission laneへ直接保存する。
10. GitHub書込みがrun全体で利用不能なら、完全な5スロットpayloadをChatGPT Library `/LLM-survey-outbox/pending/` へ1論文1envelopeで保存する。
11. 完全payloadまたはstatus-only descriptorを耐久保存して不変submissionを送ったら、**submission resultを待たず次のforegroundへ進む。** 論文Nを提出→既確保standbyのN+1をforegroundへ昇格・読解・提出→N+2……と、論文本体は常に1件ずつ直列に進める。standbyが不足して低水位なら同時にclaim windowを非同期補充するが、補充result待ちをforegroundの同期障壁にしない。提出済みattemptの未確定result数には先行上限を設けない。各提出後・各claim前には最新run-stateと新着resultを確認し、既に返ったfailure / `repair_required` / `retryable` は `next_action` / `recovery_steps` に従って耐久回復へ流す。ただし**未確定resultそのものを理由に新規claimを止めない。** 残り600秒以下の開始禁止窓、未提出active claim、claimable job 0件、hard stopだけが新規claimを止められる。status-only終端は成功件数へ数えない。

禁止事項:

- 固定 `submissions/chat-inbox.json` を生成・更新しない。
- 完成MarkdownをScheduled Chatから直接送らない。
- claim resultが返したbankを無視して別bankへ書かない。
- 1本処理したことだけをrun終了理由にしない。
- `blocked` / `deferred` / `rejected` が `ok=true` で終端したことをrun終了理由にしない。これは**次の論文へ進めるようになった状態**であり、hard stop / handoff guardでない限り次claimへ進む。

**論文本体の作業は1件ずつ直列、担当確保はwindowで先行、preflight / submission result確認は非同期に並行する。** 同時に全文読解・5スロット作成・修復を行う論文は常にforegroundの1本だけとする。通常はN+1以降をstandbyとして保持するが、論文Nのセルフレビュー済み5スロットとpreflight requestを耐久保存した後は、**新規preflightへの入場を同一worker最大2件まで**先行させ、その各論文を `preflight-pending` として内容凍結し、次の非凍結standbyを本文foregroundへ昇格してよい。既にpendingになった論文数が競合等で2件を超えても全件を凍結したままにする。NのFAILが返ればNを古いpipeline順で修復foregroundへ戻し、PASSなら自動descriptor生成へ進める。descriptor後のsubmission resultも従来どおり同期障壁にしない。これにより本文編集の並列度1を維持したまま、Actionsのpreflight待ちを次論文の精読時間で隠蔽する。

### 3.1 実運用で確立した高スループット原則

以下は品質基準を緩める高速化ではなく、全文精読・検証・耐久保存を維持したまま重複作業を減らすための標準手順である。

1. **全文読解済み成果を捨てない。** 初回全文精読後はrecord bankと既存5スロットを再利用し、validation失敗時は指摘されたslotだけを一次資料に基づいて修復する。一次証拠が不足・変更していない限り、全文を最初から読み直さない。
2. **初回5スロットをvalidator下限ぎりぎりにしない。** 問題設定は「問題＋既存法で解けない理由」、method overviewは入力から出力までのend-to-end流れ、各componentは「入力・内部処理・出力・他componentとの接続」を十分に記述する。短すぎる説明によるrepair往復を減らす。
3. **一次資料は取得できた時に一度で必要範囲を読む。** 以前の運用どおり、特定のfront-endや固定順に縛られず、同一論文の一次資料へ到達できる経路を柔軟に使う。arXiv HTML / PDF / e-print、OpenReview、会議・出版社、著者・研究機関・公式project site等のうち利用可能なものから本文を取得し、手法・評価・結果・ablation・限界・関連研究までまとめて確認する。検索結果や書誌ページは一次資料への到達経路を探すために使ってよいが、検索断片そのものを本文の代用にしない。HTTP取得やページ表示が1経路で失敗しても、それだけで全文取得不能とは判定しない。
4. **1経路の取得失敗をwhole-run failureにしない。** 以前の運用へ戻し、固定された4経路を各1回だけ試して打ち切る方式は使わない。まず既知の一次資料URLを試し、失敗・欠落があれば論文タイトル、arXiv ID、DOI、OpenReview ID、著者名等から別の一次資料経路を探す。少なくとも materially distinct な一次資料経路を複数確認し、同一front-endの一時障害・PDF text extraction失敗・HTML未生成・1回のtool/HTTP失敗だけでは `blocked` にしない。別形式・別公式ホスト・著者/研究機関配布版等で必要な一次証拠を補完できる限り読解を継続する。一次資料として同一版であることを確認できない第三者解説・検索断片・非公式要約は5スロットの根拠にしない。合理的に利用可能な一次資料経路を尽くしても必要な一次証拠を十分取得できない場合だけstatus-only `blocked` を不変submissionとして耐久保存する。**取得不能は一時状態であり、取得失敗だけを永久除外理由にしない。blocked Researchは原則7日後に再確認し、同じ取得不能が5回以上かつ最初のblockから28日以上続いた場合は通常の定期再試行を休止するだけで、`blocked_permanent` / `rejected` へ自動昇格しない。** duplicate / out-of-scope / non-paper / official retraction等、一次証拠で再試行不要と確認できた場合だけ別の終端除外状態を使う。**status-onlyでもcompleted submissionと同じ非同期result規則を使い、descriptor耐久保存後はresult確定を待たず次論文をclaimしてよい。** status-only resultは並行監視し、終端状態になった時点で最新main反映を確認するが、それまでのpendingを新規claimの同期障壁にしない。status-only `blocked` / `deferred` / `rejected` は、Scheduled Chatが最小の不変JSON descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ直接保存し、既存のsubmission laneに処理させる。**descriptorを書き込む直前に最新 `main` を再取得し、`.survey/work-queue/jobs/<job_id>.json` がまだ存在し、同じ `job_id` / `kind` の非終端jobであることを再確認する。jobが既に消失・終端・別identity化している場合はstatus-only descriptorを新規作成せず、そのclaimをstaleとして最新run-state/claim経路へ戻す。** ローカルPythonや保存前canonicalizerの実行を前提にしない。descriptorは `schema_version` / `transport_version` / `kind` / `attempt_id` / `job_id` / `claim_id` / `worker_id` / `status` / `reason` を基本とし、取得済みなら `retrieval_evidence` / `blocked_at` を加えてよい。`record_bank` / `paper_path` / `record_slots` / `expected_blob_sha` その他のrecord transport fieldはstatus-only descriptorへ混在させない。一時障害の `blocked` と、一次証拠で再試行不要と確定した `rejected` を混同しない。
5. **submission待ちは非同期化して読解を止めない。** 論文Nのdescriptorを耐久保存したら、Nのresultがpendingでも最古standbyをN+1のforegroundへ昇格して全文処理・提出し、以後も同様に1件ずつ継続する。各foreground切替・提出後に新着resultを軽く回収し、failureが返っていれば正規repairを耐久化するが、未確定result数に上限を設けて読解を止めない。claim window内のstandby active claimは複数保持してよいが、同一jobの重複claimや同一requestの重複発行はしない。
6. **canonical stateを再利用する。** foreground切替・claim window補充・submission後・repair時に最新queue、identity、rejection ledger、result、record bankを使い、重複claim・重複探索・重複取得を避ける。Research / Auditではactive claimをclaim window上限まで保持してよいが、**本文処理中foregroundは常に1件だけ**とする。既確保standbyがある間は新規claim待ちを挟まず順番に昇格し、補充は正規低水位条件でのみ行う。過去submissionのresult未確定は補充・foreground進行の禁止条件にしない。
7. **Research / Audit のrun完了ノルマは合計5件である。** `research_audit_completed_this_invocation < 5` の間は、hard stopまたはhandoff guardでない限り読解を継続する。成功resultと最新main反映を確認したResearchまたはAuditだけを1件として数え、同一論文のResearchとAuditも別jobとしてそれぞれ1件に数える。これとは独立して、Audit starvation防止は3件のforegroundブロックごとに適用する。利用可能なAuditがあるブロックでは少なくとも1件Auditが入るようclaim allocatorが順序を調整する。5件到達は停止上限ではなく、600秒開始禁止窓に入るまで同じモードで継続する。Research / Auditの作業枯渇を理由に終了できるのは、run-state resultでclaimableな次jobが0、pending claim/submission/recoveryが0、Library checkpointから回復可能な作業も0であることが導出された場合だけとし、ワーカーが「もう無さそう」と判断して終了しない。取得枠を節約するため、再取得より既存成果の局所修復を優先する。

## 4. 探索（Discovery）の共通入口

新規Discoveryは**固定ソース precheck schema v3** だけを使う。ワーカーが検索結果を数件だけ手でJSONへ詰め、schema v1/v2として投入してはならない。

requestは `.survey/work-queue/discovery-precheck/requests/<request-id>.json` に保存し、少なくとも次を含める。

```yaml
schema_version: 3
operation: precheck_discovery_candidates
request_id: <request filename stemと一致する一意ID>
provider: openalex | semantic_scholar | openalex_references | repository_references
source_url: <固定した検索/API URL>
collector_id: <同一探索軸の識別子>
run_key: <今回runの識別子>
axis: <探索軸>
target_unseen: 20
```

### 4.0 探索の事前装填待ち行列（Discovery preload queue）

**Discovery hot take:** 初回・2回目以降を問わず、selector方向にPRECHECKED preloadがある場合は第2.0.1節のcreate-only direct takeを優先する。claim create成功直後からpreloadの20件を評価し、run固有の正式schema v3再フィルタは同時に後段Actionsで走らせる。従来のrun-state内 `auto_initial_discovery` はhot-dispatchを使えない場合だけのfallbackであり、`route_source=hot_dispatch_direct_start` のrunでは二重precheckを避けるため自動発行しない。

Discoveryは、run開始後に外部APIの取得を始める待ち時間を減らすため、Research paper preloadとは独立した**探索事前装填待ち行列（Discovery preload queue）**を持つ。ただし物理バンク自体は分離しない。workflow-v10の32 record bankはすべて二重用途バンクで、各bankは **`research-preload.json` + `discovery-preload.json` + Research/Audit用5スロット**を同時に持つ。読解面と探索面は同じbank IDを共有するが、それぞれ独立したsidecar/slotなので互いを上書きしない。

- `.github/workflows/discovery-precheck.yml` は**実workerのrun固有schema v3 precheck専用のforeground lane**とし、preload取得を同じrunで処理しない。事前装填は `.github/workflows/discovery-preload-warm.yml` が独立して担当する。foreground laneが完了すると `workflow_run` でwarm laneを即時起動し、取りこぼし対策として5分周期でも再実行する。warm laneは `.survey/scripts/discovery_preload_queue.py` で32バンクの探索面を**利用可能32窓**まで先行予約し、1回で最大32窓をdrainして `READY → PRECHECKED` を進める。1窓は `target_unseen=20` / `page_size=20` とする。32窓は32個の `discovery-preload.json` と1対1で対応し、Research/Audit用5スロットがoccupiedでも同じバンクの探索面は利用できる。逆に探索面がoccupiedでもResearch/Auditのbank予約を妨げない。Semantic Scholarは背景lane内で直列化し、ローカル参照・その他providerはbounded parallelismで処理するため、外部API待ちやrate limitを実worker resultの公開障壁にしない。foreground pushでは重い回帰test suiteやpreload top-upを実行しない。
- 探索元は耐久済み `discovery-state.json` の実績から選び、後方引用・前方引用を優先する。構造化referencesの後方引用は常に補充候補とし、実績のある前方引用seedを複数保持する。利用可能在庫が片方向へ偏らないよう、可変targetの約1/3ずつを後方引用・前方引用の最低在庫、約1/8を通常検索の小さな予備在庫として扱い、残りを実績順の余剰枠にする。通常検索のpreloadは、引用2方向を実run内で完了した後のgap-fill用在庫としてのみ扱う。**ローカルの `repository_references` はevergreen sourceとして扱い、あるsnapshotで末尾まで到達しても後方引用在庫を空のまま次の6時間bucketまで放置しない。** そのPRECHECKED窓が消費された後はfresh immutable preload identityでcursor 0から再検査し、候補0件でも「正式に空であることを事前計算済み」の窓を維持する。これによりselectorがbackwardを要求した瞬間にlive precheckから始める経路を極力避ける。
- preloadの論理状態は **READY → PRECHECKED → CLAIMED → INGESTED** とする。READYは先行precheck requestが耐久化済み、PRECHECKEDはworkflow生成resultが利用可能、CLAIMEDは実runが担当確保（claim）済み、INGESTEDはそのrun固有roundのDiscovery submission/resultが正規に耐久反映済みであることを表す。状態は共有JSONを上書きせず、entry / claim / ingestedの独立耐久ファイルから導出する。
- 担当確保（claim）は通常、`.survey/work-queue/discovery-preload/claims/<preload_id>.json` のcreate-only direct writeで**Actions起動前に排他的に成立**させる。同じpreloadへの2 worker目のcreateは失敗するため二重取得しない。Discovery precheck laneはそのclaimを同一identityで再利用して正式precheckを生成する。claim leaseは90分。claim成立時点でcached result / entry / claimが耐久化済みなので、そのpreloadは物理 `discovery-preload.json` から即座に切り離し、同じバンクの探索面を次窓のpreloadへ再利用してよい。Research/Audit用5スロットには触れない。未完了claimが期限切れになった場合は、そのPRECHECKED窓を空いている探索面へ再バインドして再利用できる。未取得preloadの鮮度上限は6時間とし、それを超えた窓はSTALEとして在庫から外す。preload専用entry/request/result/claim/ingestedは24時間後にGCし、実run固有precheck resultとDiscovery submission/resultは削除しない。
- run-state resultの `discovery_selector.next_direction` が今回の正規探索方向を決め、同方向のPRECHECKED在庫があれば `discovery_preload` に最古の1窓を返す。返却値には `discovery_bank` と `discovery_slot_path` も含め、どの二重用途バンクの探索面から取得したかを明示する。**preloadはselectorを上書きしない。** 同runで後方→前方の必須順序や通常検索解禁条件は従来どおりである。
- `discovery_preload` が非nullなら、新しいrun固有schema v3 requestを作り、そこから返された `provider` / `source_url` / `axis` / `initial_cursor` / `page_size` / `max_pages` / `target_unseen` / `discovery_bank` / `discovery_slot_path` をそのまま使い、追加で今回の `worker_id` と `preload_id` を保存する。`run_key` は**必ず今回runの値**にする。preload側の `run_key=preload:...` をコピーしない。precheck側はrun-stateで見えたバンクと実claim時のバンクが一致することを検証する。
- 実run用 `process_discovery_precheck.py` は、先行取得済み20件を現在のidentity snapshot / rejection ledgerで**再フィルタ**する。20件残れば外部providerへ追加アクセスせず、その場で今回run固有の正式precheck result / receiptを生成する。既収録化などで20件未満になった場合だけ、同じ固定 `source_url` の保存済み `next_cursor` から不足分を補充する。
- バックグラウンドpreload result自体をDiscovery submissionの証明として参照してはならない。submissionが参照できるのは、今回runの `run_key` / `axis` で再検査されたworkflow生成resultだけである。queue workerも `preload_seed=true` のresultからの直接submissionを拒否する。
- 同方向の利用可能preloadが無い、claim競合で先行窓を取れなかった、preloadが破損している等の場合は停止しない。**最新run-stateの再取得を先に待たず**、既に得ているselectorまたはhot-dispatchの `discovery_fallback` が示す固定ソースをrun固有schema v3 precheckとして即時開始する。run-state再導出は並行して行う。preload不足をrun終了理由・受動待機理由にしない。background preloadのprovider失敗は同一ソース・同一6時間bucketで最大2回までとし、preload request追加pushによる自己起動が障害時に無限再試行ループにならないようにする。

`target_unseen` の既定値は20。precheck側の `discovery_provider_adapter.py` と `collect_until_unseen()` が**同じ検索結果をページ送り**し、各ページで既収録・既候補・既却下・ページ間重複を除外する。ワーカーが2ページ目以降を個別に手作業で継ぎ足す必要はない。

正式な採否確定・Candidate submissionに使ってよい候補は、schema v3 resultが `evaluation_allowed=true` として返した `allowed_records` だけである。第2.0.1節のDiscovery direct takeではpreload resultのrecordsを**暫定的に先行評価**してよいが、正式precheck完了後に `allowed_records` との積集合へ必ず絞り、除外された候補をsubmissionへ送らない。direct take以外でprecheck resultが未完了なら、旧schemaへ逃げずに同じ現行経路を完了させる。

**2ラウンド目以降のprepared-bank即時継続:** Discovery submission/resultが成功して `discovery-state.json` へroundが反映されると、`survey-discovery-recovery` は同じcommit内で今回runのcontinuation gateを再導出する。残り600秒より多く、`required_action=DISCOVER_AGAIN` で、selector方向にPRECHECKED preloadがあれば、最古の1窓をcreate-only相当で排他的にclaimし、`auto-next-discovery-*` のrun固有schema v3 precheck requestまで自動materializeする。同時に `.survey/work-queue/run-state/results/auto-discovery-advance-*.json` と `run-state/latest/<worker_id>.json` を更新し、`auto_next_discovery.work_start_allowed=true` を付ける。workerは同一 `run_key / scheduled_slot / actual_invocation_start` のこのsnapshotが見えたら、追加run-state requestや別preload takeを作らず、指定された `discovery_bank / discovery_slot_path` のpreload resultを使って次roundの軽量評価へ直行する。正式precheckがpendingでも先行評価はよいが、submissionは `formal_precheck_result_path` が `ok=true / evaluation_allowed=true` になるまで禁止し、最終候補を正式 `allowed_records` との積集合へ絞る。該当方向のPRECHECKED bankが無い場合も同じfast laneが最新run-state snapshotを残すので、その `DISCOVER_AGAIN` に従って固定ソースprecheckへ即時フォールバックする。push競合時は最新mainからround反映とbank選択を再計算し、他workerが先に取ったbankを二重claimしない。

**非同期結果待ち中のbounded lookahead:** 既に開始したDiscovery precheckまたはsubmissionのresultがpendingでも、残り600秒より多く、未評価成功round・recovery対象がなく、in-flight roundが3未満なら、run-stateは `discovery_pipeline_preload` と `discovery_pipeline_work_available=true` を返してよい。この場合continuation gateの正規actionは `CONTINUE_DISCOVERY_PIPELINE` であり、**待機ミクロタスクより先に**そのpacketをcreate-only claimしてcached候補の軽量評価へ進む。既存pending identityは保持し、新しいlookaheadは別roundとして最大3本までに制限する。候補評価は開始してよいが、そのlookahead自身のrun固有formal precheckが `ok=true / evaluation_allowed=true` になるまでsubmissionしてはならない。先行評価の途中でも古いresultが返れば回収し、`recovery_required` または評価可能roundが出た場合はそれをlookaheadより優先する。これによりActions待ちを作業停止理由にせず、事前装填済み引用windowを実作業で隠蔽する。

### 4.1 探索方法

探索は**引用グラフ優先（citation-first）**とし、既存の収録論文に直接つながる2方向を主経路にする。どちらも同じschema v3 precheck、identity/rejection重複排除、固定ソースページ送りを使う。

1. **後方引用（backward reference）**: 収録済み論文が引用している論文を掘る。最初はリポジトリ全体の構造化 `references` を横断する `provider: repository_references`、`source_url: repository://structured-references`、原則 `target_unseen: 20` を使う。構造化メタデータが不足する系統では、種論文ごとの `openalex_references` または Semantic Scholar `/references` を補助的に使う。
2. **前方引用（forward citation）**: 収録済み論文を引用している後続研究を、系統ごとの種論文から最新順に掘る。OpenAlexの `cites:W...` または Semantic Scholar `/citations` を固定ソースにする。
3. **通常検索・新着検索**: 引用関係だけでは拾えない新系統・新用語を補完するフォールバック。OpenAlex / Semantic Scholar等の固定検索URLを使う。

**通常・定期Discoveryでは、同じrun_keyの中で後方引用と前方引用を少なくとも1回ずつ試すまで通常検索へ進まない。** 一方、後方引用側の候補山が残っていても前方引用を止めない。原則として後方引用1バッファを分類・投入したら前方引用refreshへ進み、その後は `discovery_stats.search_windows` の未収録率・採用率・重複率を見て、実績の良い種論文／方向を優先する。これにより古い参考文献の巨大な山を掘りつつ、新しく既存研究を引用し始めた論文も取りこぼしにくくする。

前方引用・後方引用のどちらも、同じ固定結果集合のページ送りは `collect_until_unseen()` に任せる。ワーカーが上位数件だけを手作業で抜き、重複が多いから別クエリに変えることは禁止する。原則 `target_unseen: 20` まで既収録・既候補・既却下・ページ間重複を飛ばしてから軽量評価する。

**明示ユーザー指定探索（explicit user-directed discovery）の例外**: ユーザーが現在の会話で探索軸・対象系統・引用方向などを明示して個別探索を依頼した場合、その依頼に限って上記の自動実行順を上書きしてよい。これは通常・定期Discoveryの方針変更ではなく、ユーザー指定軸を即時に調べるための限定例外である。候補投入は必ずschema v3固定ソース事前検査（fixed-source precheck）→identity/rejection重複排除→通常Discovery submission→queue workerの一本道を通し、precheck自体を省略してはならない。submissionには `discovery_stats.trigger: explicit_user_request` と、非空の `user_directed_request.request_id` / `user_directed_request.summary` を付ける。自律・Scheduled workerはこの印を自己生成して通常優先順位を回避してはならない。

#### 4.1.1 structured-reference curation の進め方

この経路は、収録済み論文の `references` を横断して候補集合を作り、同じ候補を指す収録論文数 `relation_count` が多い順に少しずつ評価する。1回に全候補を掃除しようとせず、通常の `target_unseen: 20` の1バッファを処理する。**候補集合は空になるまで継続して掘るが、前方引用refreshをブロックしない。各runで後方引用を処理したら前方引用も実行し、その後は探索実績に応じて配分する。**

- 候補生成は `.survey/scripts/reference_pool.py` を正本とする。既収録論文に加え、`.survey/work-queue/reference-curation/unrelated-papers.json` と `.survey/work-queue/reference-curation/borderline-papers.json` の登録済み候補を通常時は除外する。
- **明確にサーベイ対象外**と判断した候補は、`.survey/scripts/reference_relevance_ledger.py mark-unrelated` を正規実装として無関係台帳へ永続保存する。同じ論文を後続runで再判定しない。
- **関連性・重要性・得られそうな知見が微妙で、現時点ではResearchへ送る価値が弱い候補**は、同スクリプトの `mark-borderline` を正規実装として微妙台帳へ保存する。微妙台帳も通常の `repository_references` 探索ではデフォルト除外し、同じ候補を毎回評価し直さない。

**Scheduled Chat / connector用 relevance fast lane:** ローカルPythonを直接実行できないworkerは、上記スクリプトを実行できないことを停止理由にしてはならない。一意な `request_id` を作り、`.survey/work-queue/reference-curation/requests/<request_id>.json` をcreate-onlyでmainへ耐久保存する。requestは `schema_version: 1`、filename stemと一致する `request_id`、`operation: mark_unrelated | mark_borderline`、`canonical_id`、非空の `reason` を必須とし、分かる場合は `title`、`identity_tokens[]`、`linked_from[]`、今回runの `worker_id` / `run_key` / `scheduled_slot` / `actual_invocation_start`、元の `source_precheck_request_id` を付ける。**有効なrequestのcreate成功を、このworkerによる分類判断の耐久保存完了とみなし、その候補を今回roundのローカル除外集合へ直ちに入れて次の候補評価へ進む。Actions resultや台帳本体への反映を待ってはならない。** 当該候補は同じroundのcandidate / rejected candidate submissionへ重複投入しない。

`.github/workflows/survey-reference-relevance-fast.yml` はrequestを受けると `.survey/scripts/process_reference_relevance_requests.py` を実行し、既存の `reference_relevance_ledger.py` を通して正規台帳へ反映し、`.survey/work-queue/reference-curation/results/<request_id>.json` を返す。push起動に加えて周期回収も行い、未result requestを再処理する。valid requestのresult未生成・Actions queued/in_progressは**待機理由でもrun終了理由でもない**。他候補評価、正式precheck回収、submission準備など今回runの実作業を継続し、作業の区切りでresultを回収する。resultが `ok=false` / `FIX_REFERENCE_RELEVANCE_REQUEST` の場合も、その失敗request/resultは不変証跡として残し、修正版を新しい `request_id` で作る一方、他候補の評価は止めない。processor内部の一時的I/O/競合失敗はresultを確定させず周期回収へ残し、1件のpoison requestで他の分類を停止させない。
- 微妙台帳は永久除外ではない。後で明示的に再検討する場合だけ `reference_pool.py --include-borderline` を使って再び候補へ含めてよい。通常runでは使わない。
- 関連ありの候補は一次資料でtitle/abstract/書誌を補完してから、当該schema v3 precheck result / receiptを参照する通常のDiscovery submissionへ送る。canonical IDだけをtitle代わりにして提出しない。
- この経路からResearch jobを直接生成しない。Candidate投入以降は4.3〜4.4の一本道へ合流する。

### 4.1.2 系統限定の最新被引用探索（lineage-scoped forward-citation refresh）

特定の系統ページにある収録済み論文を**種論文（seed papers）**として、その論文を引用する後続研究から最新の有力候補を拾う方法。既存論文の引用先を掘るstructured-reference curationとは逆方向なので、直近数か月の新手法を拾うのに向く。通常runでも後方引用と並ぶ主経路として使い、`repository_references` の枯渇を待たない。ユーザーが「この系統を引用する最新論文を探して」のように明示した場合は、上記の明示ユーザー指定探索として対象系統を即時実行してよい。

効率化の標準手順:

1. **系統全体を種集合にする。** READMEだけでなく、その系統ディレクトリ内の収録論文の正規識別子（canonical ID）を列挙する。最初は、引用が十分蓄積している代表論文・基礎論文から始める。1本で十分な新規候補が出る場合、全種論文を同時に走査しない。
2. **最新順を保証できる固定ソースを優先する。** OpenAlexでWork IDを解決できる場合は `/works?filter=cites:W...&sort=publication_date:desc` を固定 `source_url` とし、必要なら公開日範囲も付ける。Semantic Scholarを使う場合は対象論文の `/citations` エンドポイントを固定ソースにする。検索語だけの類似検索に置き換えない。
3. **schema v3事前検査（precheck）へ渡す。** 原則 `target_unseen: 20`。同一固定ソースのページ送りは `collect_until_unseen()` に任せ、既収録・既候補・既却下・ページ間重複を自動除外する。引用件数が大きい種論文でも、ワーカーが先頭数件だけ手で抜かない。
4. **新しいものから軽量評価する。** `allowed_records` を公開日降順で見て、対象系統への直接性を確認する。「種論文を引用している」だけでは採用理由にせず、既存系統をどの軸で更新するか（例: expert数の適応配分、expert pruning/merging、圧縮後回復、実測serving改善）をreasonに書く。
5. **1 submissionは強い候補だけ0〜5件。** 5件を埋めるための弱い候補は入れない。候補化後は4.3〜4.4の通常経路へ合流し、Research jobを直接生成しない。
6. **次の種論文へ進む条件を明確にする。** 1本の種論文から十分な強候補が得られたら、そのsubmissionを先に耐久保存する。続行時は同じ種論文を再度precheckしてidentity snapshotにより既候補を飛ばすか、別の種論文へ移る。複数種で同じ後続論文が出てもshared identityで重複除外させる。
7. **探索効率を記録する。** 前方引用roundでは `discovery_stats.seed_canonical_id` に実際に使った種論文のcanonical IDを必ず残し、`discovery_stats.search_windows` に種論文、引用方向 `forward`、取得件数、未収録件数、評価件数、採用件数を残す。後続runでは `select_discovery_direction.py` がこの耐久履歴を使って採用率の高かった種論文を優先し、0件が続く種論文を毎回先頭から調べ直さない。repository-wide後方引用のように単一seedを持たないroundでは `seed_canonical_id` を省略してよい。

この方法が特に有効なのは、既存系統が2024〜2025年の代表論文を含み、2026年の新手法がその代表論文を関連研究として引用し始めている場合である。単純なキーワード検索より、対象系統との接続根拠を保ったまま最新研究へ追従しやすい。

### 4.2 探索ノルマ

探索モードでは、hard stopまたはhandoff guardがない限り、**今回のrunで成功した正規schema v3 precheckを合計8回**完了させ、それぞれをDiscovery submission/resultまで耐久反映する。ラウンドIDはprecheckの `request_id` とし、カウントはrun開始時に0から始める。1 precheckから強候補が6件以上出て `5 + 残り` の複数submissionに分割しても**1ラウンド**である。別precheckが成功すれば、同じprovider・同じ固定ソースでも別ラウンドとして数える。候補0件でも成功precheckと0件submission/resultまで完了すれば1ラウンドである。失敗・pendingのprecheckは数えない。8ラウンドは停止上限ではない。**残り600秒の開始禁止窓に入るまでは、selectorが返す次方向・次windowで探索を続ける。探索枯渇という通常終了条件は設けない。** 単一provider・単一seed・単一検索軸、あるいは前方/後方引用の一時的0件は終了理由にせず、selectorの次手へ進む。残り600秒以下では新しいDiscovery roundを開始せず、開始済みroundだけを完了・耐久保存してhandoffする。

### 4.3 Candidate投入

Discoveryは軽量評価だけを行う。title、abstract、書誌、一次資料の存在、テーマ適合性、新規性の見込みを確認し、全文精読はResearchへ送る。

**Candidate priorityは0〜100点とし、基礎評価はワーカー判断を残しつつ、既存系統との関連・新しさ・venueが実際に読む順を動かす重みを持つようにする。** 推奨計算は `priority = min(100, base + lineage + recency + venue)` とする。

- **base: 0〜55点** — テーマ適合性、技術的重要性、得られる知見、実装・評価の有用性をまとめてワーカーが判断する。ここは固定チェックリストで機械化しない。
- **既存系統への関連度（lineage）: 0〜20点** — 既収録論文の直接引用・被引用、明確な後継/改良/比較対象で既存系統を直接更新する候補は `+20`、同一サブテーマに明確な差分を加える候補は `+10`、広いテーマ一致だけなら `+0` を目安とする。
- **新しさ（recency）: 0〜15点** — 直近6か月 `+15`、6〜12か月 `+10`、12〜24か月 `+5`、それ以前 `+0`。基礎的重要論文は古さだけで除外しない。
- **査読venue: 0〜10点** — NeurIPS / ICML / ICLR / MLSys / OSDI / SOSP / NSDI / USENIX ATC / EuroSys / ASPLOS / ISCA / MICRO / HPCA 等、対象分野の主要査読venueへの採択が既知なら `+10`、その他の信頼できる査読付きvenueは `+4`、不明またはarXivのみなら `+0`。推測しない。
- **Research投入下限**: 現行queueの正規実装に合わせ `priority >= 40` をCandidate→Research投入の下限とする。ただし40点を満たすためにbaseを水増ししない。弱い候補はborderline/unrelatedへ送る。
- **追加ネットアクセス禁止**: priority採点だけを目的として追加のWeb/APIアクセスを発生させない。precheckや既取得metadata、一次資料中に既にある情報だけを使い、不明項目は0点とする。
- candidateの `reason` には、lineage / recency / venueのうちpriorityを大きく押し上げた要因を短く残す。可能なら `priority_breakdown` に `base` / `lineage` / `recency` / `venue` / `total` を残す。

1回のDiscovery submissionへ送るcandidateは0〜5件。**5件はrun上限でもround上限でもなく、1 submissionの上限**である。1回のprecheckで評価後に強候補が6件以上残った場合は、同じprecheck result / receiptを参照した複数submissionへ `5 + 残り` で分割し、強候補をすべてCandidate化する。複数submissionに分けても探索ラウンド数は1のままとする。**ただし分割した全submissionについて対応resultが `ok=true` で耐久反映されるまで、そのprecheck roundを成功ラウンドとして数えない。** 一部だけ成功・残りpending/失敗の状態はラウンド未完了である。分割時は全submissionの `discovery_stats` に同じ `run_key` / `round` / `axis` を持たせ、`round_submission_index` を1始まり、`round_submission_count` を総分割数として記録する。単一submissionなら両方1としてよい。

Discoveryのmulti-round submissionは、どちらのwork mixから探索を選んだ場合でも自己記述型（self-describing）を使い、存在しないDiscovery `job_id` を合成しない。candidate投入前に最新HEAD / identity / queueを再確認する。

### 4.3.1 新しい研究系統の昇格ルート

既存の正規系統へ無理に押し込むと研究上の差分が失われる**明確な近傍クラスタ**をDiscoveryで確認した場合、candidateに `lineage_proposal` を付けて正規の系統昇格ゲートへ送ってよい。未知のディレクトリをワーカーが直接作ってはならない。

新設は次をすべて満たす場合だけ提案する。

- `confidence: high`。
- `neighbor_lineages` に既存の正規系統を1〜3個指定し、`distinctness_reason` で近傍系統では表現できない理由を具体化する。
- `boundary_rule`、`scope_includes`、`scope_excludes` を明記し、別workerでも同じ境界で分類できるようにする。
- `supporting_papers` を4本以上指定し、正規IDで検証できること。そのうち少なくとも2本は既収録論文とする。
- 単一論文、1〜2本の派生研究、単なる実装差では新設しない。
- 1 Discovery roundで新設できる系統は最大1個とする。

提案は `slug_tail`、`title`、`description`、`distinctness_reason`、`boundary_rule`、`scope_includes`、`scope_excludes`、`neighbor_lineages`、`confidence`、`supporting_papers` を持つ。`queue_worker.py` は `.survey/scripts/lineage_proposal.py` で検査し、PASSなら空いている2桁番号を自動採番して `.survey/config/promoted-inference-lineages.json` へ正規登録し、`papers/inference/<new-lineage>/README.md` を作成してcandidateを新系統へ送る。

条件未達は探索失敗ではない。`.survey/work-queue/lineage-proposals/` に `deferred` と理由を保存し、candidate自体は既存系統または `99-other-inference-systems` へ通常どおり流す。**既存系統の説明を少し広げれば十分な場合は新設せず、複数論文が同じ主要機構を共有し、近傍系統との境界を再現可能に書ける場合は `99-other` に溜め続けず昇格ルートを使う。**

### 4.4 Discovery submissionからResearchへの一本道

Discovery後半は次の順序を正規経路とする。途中を手作業で代替してはならない。

1. `process_discovery_precheck.py` のschema v3 resultが `READY_FOR_EVALUATION` / `evaluation_allowed=true` になったことを確認する。
2. `allowed_records` だけを軽量評価し、候補0〜5件を `operation: submit_discovery_round` の不変submissionとして `.survey/work-queue/submissions/<unique>.json` に保存する。submissionは対応するprecheck result path / receiptを参照する。
3. `queue_worker.py` にsubmission処理を任せる。workerはResearch job IDを合成したり、`jobs/*.json` / `state.json` を直接書き換えたりしない。
4. 同名の `.survey/work-queue/results/<unique>.json` を確認し、`ok=true`、`research_jobs_added`、`final_duplicate_filtered_count`、`next_action` を読む。
5. `refresh_queue_snapshot.py` または `queue_worker.py` が更新した `.survey/work-queue/next-jobs.json` を確認する。
6. ready Research/Audit が現れても、**今回runがDiscoveryならclaimしない。** `next-jobs.json` への反映だけ確認し、run開始時に固定したDiscoveryを続ける。Research / Auditのclaimは、次回run開始時の `candidate_inventory >= RESEARCH_DISCOVERY_THRESHOLD` 判定で読解モードになった場合に `claim_worker_with_banks.py` から1件だけ取得する。
7. `research_jobs_added=0` でもrun終了理由にしない。最終重複排除や低優先度除外を確認し、必要なら別探索軸をschema v3 precheckから開始する。

失敗submissionの回収には `recover_discovery_submissions.py` を使う。回収後は `refresh_queue_snapshot.py` → `next-jobs.json` でcanonical stateを確認する。ただし**このrunが探索モードならResearchへ切り替えず、run開始時に固定した探索モードを維持する。** Research jobのclaimは次回以降、読解モードで行う。失敗済みsubmissionを上書きしたり、synthetic `job_id` を作って回避してはならない。

引用優先runでは、後方引用の候補山が残っていても前方引用へ進む。逆に前方引用が0件でも後方引用の山は継続する。**通常検索へ進めるのは、同じrun_keyで後方引用と前方引用の両方を試した後だけ**とし、通常検索は引用グラフで空く領域を埋める用途に限定する。単一provider障害は「0件」とみなさず、同じ引用方向の別providerまたは別種論文を試す。1 Discovery roundが耐久保存まで完了したら、**今回runの探索モードを維持したまま**次の探索軸を選ぶ。次方向の決定は原則 `.survey/scripts/select_discovery_direction.py` の出力を使い、ワーカーが「なんとなく次を選ぶ」ことは禁止する。selectorは同一runで未実施の後方引用→前方引用をまず埋め、その後は過去の `accepted_count`、`novel_candidate_count`、重複率、連続0件を使ってproductiveな引用方向を優先し、同点なら直前と反対方向を選ぶ。通常検索は同一runで後方・前方の両方が耐久記録済みの場合だけ候補になる。種論文についても過去search windowにseed identityがあれば同じyield規則を使い、履歴がないseed間ではcanonical ID昇順を決定的fallbackとする。候補在庫を再取得してもrun中のモード変更には使わず、次回runの開始判定用状態としてのみ扱う。

## 5. 重複排除

candidate提出前とResearch着手前に、正規識別子（canonical ID）、arXiv ID、DOI、OpenReview ID、正規化題名（normalized title）の順で照合する。

Discovery precheckではidentity snapshotとrejection ledgerを使う。GitHub code searchだけで「未収録」と判断しない。

## 6. 保存障害と退避

耐久経路は次の2つだけ。

1. GitHub direct write
2. ChatGPT Library `/LLM-survey-outbox/pending/`

Google Drive、Notion、旧 `/LLM-survey-fallback/` は使わない。

**record bankだけが枯渇し、GitHub read/write自体は利用可能な場合はrun-wide write障害ではない。** claim resultが `record_bank_fallback: library` を返したら、その論文の完全5-slot Research/Audit envelopeをLibrary `/LLM-survey-outbox/pending/` とcheckpoint markerへ保存する。GitHub writeが使えるなら同一run中にexact envelopeを `.survey/work-queue/fallback-inbox/` へimmutableに搬送し、`dispatch_fallback_inbox.py` / `drain_fallback_recovery.py` → immutable submission → result →最新main反映の正規publication経路へ流す。bank枯渇を理由に再精読やrun停止を行わない。成功件数へ数えるのはLibrary保存時点ではなく、canonical publication result `ok=true` と最新main反映を確認した時点だけである。

GitHub write失敗時:

1. 対象の最新blob SHA / repo状態を取り直し、その対象だけ1回再試行。
2. まだ失敗する場合、そのrun最初のwrite失敗に限り `.survey/work-queue/transport/health-probe.json` を1回更新。
3. probe成功 → 対象固有障害。影響payloadだけLibraryへcheckpointし、他のGitHub writeは継続。
4. probe失敗 → run-wide障害。そのrunではGitHub writeを繰り返さない。Research / Audit中なら現在の1論文だけをLibraryへcheckpointし、GitHub上の成功resultと最新main反映を確認できないため**次の論文へ進まない**。Discovery中も正規precheck/result要件を飛ばして新ラウンドを捏造せず、既に得た成果だけをLibraryへ耐久保存する。
5. GitHub direct writeとLibrary保存の両方が不能な場合だけ、未保存成果を増やす前に停止。

**Scheduled Task自体を一時停止・無効化してはならない。** GitHub/API/Actions/Library障害、今回runのhard stop、ノルマ未達、その他の一時障害があっても、Scheduled Chat / automationのenabled状態は維持する。停止とは今回runの安全終了だけを意味し、将来runのスケジュール停止を意味しない。

Research/AuditのLibrary fallbackは1論文1envelopeで、root-level identityと完全5スロットを持たせる。復旧は `.survey/work-queue/fallback-inbox/<id>.json` から現行immutable submissionへ収束させる。

過去形式を読み込む互換コードが内部に存在しても、ワーカーが旧形式を新規生成してはならない。

## 7. 待機・継続・終了

### 7.0 非同期結果待ちの待機ミクロタスク

claim result、Research quality preflight、submission result、Discovery precheck/submission result、またはclaim可能jobの再出現待ちなど、**依存結果が未確定で本処理を直ちに進められない場合も、固定時間のsleepや定周期pollingだけを行ってはならない。** Scheduled Chatが「やることなし」と判断してrunを早期終了することを避けるため、依存結果がpendingの間は次の**待機ミクロタスクを1件だけ実行し、その完了直後に同じ耐久target/resultまたは最新queueを再確認する。** resultがまだpendingなら次のミクロタスクを1件実行して再確認する。このサイクル自体をrun終了理由にしない。

待機ミクロタスクは、現在のclaim/result identityを壊さず、途中で即座に本処理へ戻れる小さい作業に限定し、原則として次の優先順を使う。

1. **同一workerの非同期transport監査**: 未解決submission、retryable / repair待ち、active claim整合、対象Actions run/job/step、descriptor/result対応を確認する。
2. **直近完成論文の軽量生成物チェック**: Markdownの明白な自動置換破壊、source/code URL欠落、canonical ID/arXiv ID、必須見出し、正式英語名の破壊など、生成・変換バグだけをread中心に確認する。品質閾値・説明量・採否基準を変更してはならない。
3. **一時PDFキャッシュ掃除**: 成功result＋main反映済み、またはblocked/deferred/rejectedの終端が耐久反映済みで、別worker/未完了attemptが再利用していないLibrary一次PDFだけを削除する。
4. **キューの軽量健全性確認**: result済みclaim残留、descriptor済みactive表示、孤児request、同一canonical IDの明白な二重claim等をread-onlyで確認する。異常を見つけた場合だけ既存の正規repairへ渡し、待ち時間を理由に新しいrepair scriptやmanual state編集を作らない。
5. **現在論文の証拠整理**: すでに取得済み一次資料から代表結果、評価条件、限界、実装情報の根拠位置を整理する。依存preflight/resultが返る前に5スロットや公開paperを勝手に変更しない。

待機ミクロタスクの制約は次のとおり。

- **新しい論文claim、未claim論文の先読み、新しいDiscovery round、新規外部PDF取得、大規模refactorは行わない。**
- 新しい外部取得を増やさず、原則としてGitHub/Libraryの既取得状態だけで完結させる。
- 1件ごとに中断可能な粒度にする。長引く場合は途中状態を増やさず、そのタスクを打ち切って依存resultを再確認する。
- 残り600秒以下の開始禁止窓でもread-only監査・安全なcache cleanup等の小作業は行ってよいが、新しい独立内容作業には拡大しない。残り180秒以下ではミクロタスクも新規開始せず、耐久保存・result確認・handoffだけを行う。
- 実行可能なミクロタスクを一通り確認済みでも、それ自体をrun終了理由にしない。同一targetの状態を再確認し、pendingなら安全なread-only確認を繰り返すか、既存の正規回復へ従う。
- resultが生成された時点でミクロタスクよりresult処理を優先し、`next_action` / `recovery_steps` にただちに戻る。

### 7.0.1 ゼロアイドル不変条件

通常の作業時間帯では、**非同期request/result待ちだけが残ってworkerに実行可能作業が0件になる状態を許容しない。** hot-dispatchのPRECHECKED packet、同一runの次Discovery固定ソースprecheck、Research/Audit standby、または第7.0節の有限ミクロタスクの少なくとも1つを常に次作業として持つ。特にDiscoveryは、PRECHECKED在庫が0でも固定ソースfallbackを即時開始し、前ラウンド成功時の自動advanceも同方向bankが無ければ同じrecovery transaction内で固定ソースprecheckまで実行する。

`idle_gap_forbidden=true` / hot-dispatchの `idle_gap_guard.passive_wait_forbidden=true` は、`Actionsが処理中なので何もせず終了`、`resultがまだ無いので最終応答`、`次の定期回収を待つ` を禁止する機械指示である。待ち対象が存在する場合も、そのtargetを保持したまま独立に進められる準備済み作業を先に実行する。**準備済み作業も固定ソースfallbackもミクロタスクも本当に生成できない状態は運用上の在庫欠損として最終報告へ記録するが、それ自体を通常終了許可にはしない。**

### 7.1 hard stopの機械判定

hard stopは曖昧な「安全そうでない」「難しい」「時間がかかる」では立てない。通常runでhard stopとして許可するのは次の機械的事実だけである。

- 予定run deadlineまで**180秒以下**になった最終handoff guard。または残り600秒以下の開始禁止窓に入り、進行中の独立作業・必要な非同期結果確認が無く、安全にhandoffできる状態。
- GitHubのcanonical stateをreadできず、同じrunで復旧確認もできない。
- 保存対象についてGitHub direct writeとLibrary耐久保存の両方が利用不能。
- platform/context上限が実際に発生し、継続するtool callまたは出力がプラットフォームから拒否された。
- 正規transportが要求するGitHub Actions/API/認証が利用不能で、Libraryを含む代替耐久経路でも現在成果を安全に引き継げない。

単一provider失敗、**単一論文の一次資料全文取得失敗**、validation failure、record bank枯渇、claim/submission result pending、候補0件、Library backlog、単に次手が分かりにくいことはhard stopではない。これらは正規回復・別provider・status-only・Library route・同一target待機・次の独立作業へ進む。特に一次資料取得失敗を `platform_context_limit` / `global_dependency` へ読み替えてrun全体を終了してはならない。

`continuation_gate.py` / `run_finalization_gate.py` へ停止系入力を渡す場合も、この列挙に対応する観測事実がある時だけtrueにする。ワーカー独自の解釈で `platform_limit` / `global_dependency` / `discovery_exhausted` を立てない。

### 7.2 run-state fast lane

run-stateは **request駆動snapshotとsubmission駆動の自動snapshotを同じ正規result schemaで扱う。** run開始時・runtime_condition申告時・自動導出不能時は従来どおりrequest fast laneを使う。一方、Research / Auditのsubmission処理で同一run identityと固定routeを安全に特定できる場合は、submission処理直後にGitHub側で正規snapshotを生成し、workerによる追加run-state request writeを省略してよい。自動snapshotもcontinuation gate / finalization gateを必ず通り、resultが存在すること自体でgateを迂回してはならない。

**run開始時の初回claim連結:** request駆動snapshotがResearch / Auditを選び、`CLAIM_NEXT_RESEARCH_AUDIT` かつ同一runにclaim transport・active assignment・submissionがまだ無い場合、run-state laneは同じserialized claim domain内で `auto_claim_from_run_state.py` → `claim_fast_path.py` を続けて実行し、初回claim request・bank予約・claim result・claim後の自動run-state snapshotを**同じmain commit**に耐久反映してよい。これによりworkerがrun-state resultを読んでから別のclaim Actionsを起動する往復を省く。run-state laneとstandalone claim laneはともに `concurrency: survey-claim-main` を使い、claim ownershipの競合回避を維持する。対象はrun開始時の**初回claim request自動生成だけ**であり、既存claim transportが1件でもあるrun、carry-over active claim、08:30 maintenance、Discovery、残り600秒以下では自動生成しない。以後のclaim window補充requestは通常のclaim経路を使う。

通常のScheduled Chatは、継続判断用の多数のbooleanを手作業で組み立てない。`.survey/work-queue/run-state/requests/<request-id>.json` に次の最小requestを耐久保存し、`.github/workflows/survey-run-state.yml` に `.survey/scripts/derive_worker_run_state.py` を実行させる。 **各再判定snapshotでは新しい一意な `request_id` を使う。** 同じrun内では `run_key` / `worker_id` / `scheduled_slot` / `actual_invocation_start` を維持するが、resultが既に存在するrequest IDを再利用して最新状態を得ようとしてはならない。既存resultは不変snapshotである。requestが存在してresultだけ未生成の場合は新requestを作らず、同じrequest IDのresultを待って定期回収に任せる。

```yaml
schema_version: 1
request_id: <filename stemと一致>
run_key: <今回runで固定した値>
worker_id: scheduled-chat-00 | scheduled-chat-30
scheduled_slot: "00" | "30" | "0830"
actual_invocation_start: <offset-aware timestamp>
runtime_condition: none
# hot-dispatch direct startを使った場合だけ追加:
# candidate_inventory_at_start: <hot-dispatch candidate_inventory>
# work_mode_at_start: research | discovery
# research_discovery_threshold: <hot-dispatch threshold>
# hot_dispatch_generated_at: <hot-dispatch generated_at>
# runtime障害を申告する場合だけ追加:
# runtime_condition_confirmed: true
# runtime_condition_attempts: 2
# runtime_condition_detail: <観測した障害と回復試行>
# platform_context_limit の場合だけ必須:
# runtime_condition_event: platform_tool_call_rejected
```

hot-dispatch direct startではrun-state requestを**内容作業開始前に耐久保存するがresultは待たない**。上記4項目がpolicyと整合する場合、run-stateはその開始時routeを正規snapshotへ固定する。従来経路ではresultを待ってから開始する。`runtime_condition` は通常 `none`。repoから導出できない実際のplatform/transport事象が起きた場合だけ、`github_read_unavailable` / `durable_transports_unavailable` / `platform_context_limit` / `transport_unrecoverable` のいずれかを使う。**単発のAPI/認証/ネットワーク失敗をruntime hard stopへ昇格させない。** retriableなread/transport事象は待機ミクロタスク等の別作業を1件以上挟んだ正規回復を最低2回試し、それでも同じ条件が継続した場合だけ `runtime_condition_confirmed=true`、`runtime_condition_attempts>=2`、短い `runtime_condition_detail` をrequestへ付ける。`platform_context_limit` は実際にplatformから**必要なtool callまたはoutputを拒否された事実**がある場合に限り、`runtime_condition_confirmed=true`、`runtime_condition_attempts>=1`、非空の `runtime_condition_detail` に加えて **`runtime_condition_event=platform_tool_call_rejected`** を持つ場合だけ有効とする。この構造化証拠が無い `platform_context_limit` はrun-state側で `none` に降格する。単一論文のPDF/HTML/DOI/provider取得失敗はこのeventではなくstatus-only終端対象である。`handoff_guard` はworkerが申告せず、run-stateが残り180秒から自動導出する。証拠不足のruntime_conditionはrun-state側で `none` に降格する。

同名の `.survey/work-queue/run-state/results/<request-id>.json` が返す `candidate_inventory`、run開始時に固定された `work_mode`、claim/submission pending、成功完了数、Discovery round数、**Discovery precheck pending / evaluation pending / submission pending / recovery required**、`gate.decision` / `gate.required_action` を継続判断の正本とする。 **foreground Discovery precheckに有効な `worker_id` / `run_key` / `scheduled_slot` / `actual_invocation_start` が存在するのに同runのrun-state requestが無い場合、Discovery precheck laneはそのidentityから決定的な回復requestを自動生成し、precheck resultと同じpublish transactionでrun-stateを導出する。** この回復は既に開始済みのDiscovery modeを保持し、後から増減したcandidate inventoryでResearchへ再ルーティングしない。回復時の `candidate_inventory` は回復時観測値であり、`candidate_inventory_at_start_exact=false` として明示する。さらにDiscovery submission recovery側もlinked precheck identityから同じ回復を試してからauto-advanceするため、worker側のrun-state write漏れだけを理由に継続制御を失わない。`pipeline_ahead_count` が出力される場合は観測用テレメトリであり、Research / Auditの新規claim上限には使わない。run-state lane自体も**10分周期で未result requestを定期回収**し、push競合は最新mainから最大12回再導出し、各再試行は上限付きバックオフ＋ジッタで衝突位相をずらす。同一 `run_key` の最初の成功snapshotが `candidate_inventory` / `work_mode` を固定し、後続snapshotはそれを再利用する。ワーカーは結果と矛盾するbooleanを別途推測して `continuation_gate.py` を呼ばない。

**増分状態とsnapshot世代:** `.survey/work-queue/run-state/cache/<worker_id>.json` と `fact-clock.json` は高速化用の再構築可能index/cacheであり、immutable descriptor/result、claim state、queue state等のcanonical durable factsを置き換えない。cache欠落・破損・fact世代不一致ではcanonical factsから再構築し、maintenanceでも全履歴とのreconcileを行う。cache更新はmonotonic generationで管理し、古いgenerationを新しい状態として採用しない。`:00` と `:30` はworker_id別cacheで分離する。current invocation成功件数は従来どおり**resultの `processed_at >= actual_invocation_start`**だけを数え、claim時刻では数えない。carry-over unresolved attempt、前run由来pending result、retryable repairはcurrent run cacheにも残す。

**自動snapshotの鮮度:** 同一 `run_key` のsnapshotが複数ある場合、routeの固定値は最初の成功snapshotを維持し、現在状態の読取には同一run identityで最大の `snapshot_generation`、同世代なら新しい `processed_at` を優先する。`.survey/work-queue/run-state/latest/<worker_id>.json` はこの検索を短縮するpointerであり、それ自体を継続判断の正本にしない。pointerの `actual_invocation_start` / generationが対象runより古い場合は使わない。

**hot queue退避:** settled transportは `.survey/work-queue/archive/transport/**` へ段階的に退避する。対象はidentity確認済みcompleted-submission request、十分に古くdescriptor化済みのpassing preflight request/result、十分に古いsettled run-state request/result、全assignment終端確認済みの古いclaim request/resultに限定する。unresolved、pending、retryable、repair_required、active claim、handoff再開に必要なidentityは退避しない。immutable Research/Audit descriptor/resultはこのcompactorでは移動しない。archive失敗は論文処理を停止させずmaintenanceで再試行する。canonical再構築はarchive済み旧履歴もread compatibilityとして読める。

`gate.hard_stop` が返る場合はその値も正本とし、ワーカーが停止理由を再分類しない。主な `required_action` は次のように解釈する。

- `CLAIM_NEXT_RESEARCH_AUDIT`: Research / Auditの実行在庫を前へ進める。既確保standbyがあれば最古standbyをforegroundへ昇格し、windowが低水位なら正規claim requestでstandbyを補充する。1回のclaim requestが複数assignmentを返しても、本文処理するforegroundは1件だけである。
- `CONTINUE_ASSIGNED_WORK`: すでにactiveな同一workerの担当を継続し、新規claimを作らない。
- `WAIT_FOR_READY_RESEARCH_AUDIT`: claim可能jobが0件なので空claimを発行せず、第7.0節の待機ミクロタスクを1件処理してから最新queue/run-stateを再確認する。Discoveryへ切り替えない。
- `MONITOR_CLAIM_FAST_LANE`: claim requestから60秒未満の監視フェーズ。同じrequestを起動したSurvey claim fast laneのActions run/job/step、同一workerの未解決submission・retryable repair・active claim整合を確認し、待機ミクロタスクを1件処理してから最新main/resultを再確認する。新claim・次論文先読みは禁止。
- `WAIT_FOR_CLAIM_RESULT`: 60秒以上pendingのclaimを同一identityのまま追跡する。Actions失敗/cancelなら正規回復、処理中なら待機ミクロタスクを1件処理して再確認する。pendingだけを理由にrunを終了しない。
- `MONITOR_SUBMISSION_RESULTS`: 残り600秒以下の開始禁止窓で新規claimを始めず、待機ミクロタスクを1件処理するたびに既存の未確定submission resultを回収し `next_action` / `recovery_steps` に従う。通常の読解時間帯ではsubmission pendingだけを理由にこのactionへ入らない。
- `WAIT_FOR_DISCOVERY_PRECHECK_RESULT` / `WAIT_FOR_DISCOVERY_SUBMISSION_RESULT`: 開始済みDiscovery roundとして、第7.0節の待機ミクロタスクを1件処理するたびに同一identityを再確認する。600秒開始禁止窓に入っても最終180秒まではこの作業サイクルを継続する。
- `CONTINUE_DISCOVERY_ROUND`: 成功済みprecheckの評価・submissionなど、すでに開始済みのroundを完了する。
- `RECOVER_DISCOVERY_SUBMISSION`: precheck/submissionの失敗を正規recovery_stepsで回収し、同じroundを終端まで進める。
- `DISCOVER_AGAIN`: 残り600秒より多い場合だけ新しいDiscovery roundへ進む。run-stateの `discovery_selector.next_direction` を正本とする。**今回runの初回roundでは、run-state fast laneが同方向PRECHECKED preloadを自動adoptしてrun固有precheckまで同一commitで完了していれば、返された `auto_initial_discovery` / 正式precheck resultを使って直ちに評価へ進み、同じprecheck requestを作り直さない。第2round以降も、直前roundのsubmission recovery fast laneが次のPRECHECKED preloadを確保した場合は、同じrecovery transaction内でrun固有schema v3 precheckまで完了させ、周期precheck回収を待たず正式resultから評価へ進む。** 自動高速化されていない場合だけ、同方向の `discovery_preload` が返っていれば従来どおりその事前装填窓をrun固有schema v3 requestとしてadoptする。利用可能preloadが無ければ固定ソースprecheckへ即時フォールバックし、preload待ちで停止しない。**通常検索（normal）のforeground schema-v3 precheckでSemantic Scholarのrate limit、provider fetch failure、または非対応search endpointにより `FIX_REQUEST` となった場合は、その失敗request/resultを不変証跡として残したまま、同じrun・同じ検索queryをOpenAlexの固定 `/works?search=...` result setへ写した新しいschema-v3 requestを正規provider failoverとして自動生成し、同じprecheck workflow内で処理する。citation request、preload seed、手選別recordsはこのfailover対象にしない。failover成功resultのみ評価へ進め、元のfailed precheckを成功roundとして数えない。**
- `RUN_0830_MAINTENANCE`: 08:30専用runの非論文更新→maintenanceを続行する。通常論文処理へ入らない。
- `FINALIZE`: `run_finalization_gate.py` で最終化許可を確認してから終了する。


継続判断の内部実装は `.survey/scripts/continuation_gate.py`、最終化判断は `.survey/scripts/run_finalization_gate.py` を使う。Scheduled Chatからは原則run-state fast laneの導出結果を経由する。 run-state導出は同じcanonical factsを使って `run_finalization_gate.py` も評価し、`finalization_gate` と `finalization_permit_issued` をsnapshotへ耐久保存する。これらは**作業継続・停止の判断専用**であり、ユーザーへの報告可否を制御しない。run-stateは最終応答を禁止するfieldやdirectiveを持たない。Research / Auditでは**各提出直後と各claim前**にcontinuation gateを再実行し、新着submission resultも同時に回収する。提出直後はまず同一submission commitで生成された `.survey/work-queue/run-state/latest/<worker_id>.json` を確認し、`run_key` / `scheduled_slot` / `actual_invocation_start` が今回runと一致し、そのpointerが示す正規resultのidentityとgenerationも一致するなら、そのresultを使って追加run-state request writeを省略する。自動resultが無い、identity不一致、cache再構築要求、またはruntime_conditionを申告する必要がある場合だけ従来の一意なrun-state request fast laneへfallbackする。`submission_result_pending=true` でも、残り600秒より多く継続可能なResearch / Auditがあれば `required_action=CLAIM_NEXT_RESEARCH_AUDIT` を返し、standby昇格またはclaim window補充へ進む。`pipeline_ahead_count` は未確定submission後に積まれた提出数の観測値として保持してよいが、claim可否の閾値には使わない。残り600秒以下では `MONITOR_SUBMISSION_RESULTS`、claim可能jobが0件なら `WAIT_FOR_READY_RESEARCH_AUDIT` を使う。終端確認時はそのjobの終端statusを `--last-terminal-job-status`、今回runの成功完了数を `--research-audit-completed-this-invocation` として渡す。

`run_finalization_gate.py` にも今回runの `--work-mode` と最低条件カウンタを必ず渡す。run-state resultの `gate.hard_stop` をそのまま `--hard-stop` の正本とし、ワーカーが独自に再分類しない。Research / Auditで成功完了5件未達、またはDiscoveryで8 round未達の通常runは、仮に誤って `STOP_RUN` が渡されてもfinalization gateが拒否する。hard stop + safe handoffだけはこの最低条件より優先する。pending resultを含むsafe handoffでは、request/submission identity、期待result path、現在のpending状態、次の正規操作が耐久保存済みの場合だけ `handoff_safe=true` とする。

- claim/resultやsubmission/resultが次の安全な判断に必要なら、固定時間sleepや定周期pollingは行わず、同一targetを保持したまま**第7.0節の待機ミクロタスクを1件処理し、その直後に再確認する。** claim result待ちではActions run/job/step確認と同一worker transport監査を優先する。Research / Auditモードで最新queue上のclaim可能jobが0件なら、空のclaim requestを連打せず待機ミクロタスクを1件処理して最新queueを再確認する。run中にDiscoveryへ切り替えない。
- Research / Audit のsubmission result待ちは**foreground進行やclaim window補充の同期障壁にしない**。N提出後は既確保standbyのN+1、N+2、N+3…を順番にforegroundへ昇格し、各論文を1件ずつ直列に処理・耐久提出し続ける。standbyが低水位なら正規policyで非同期補充する。未確定resultは並行監視し、failureが見えた時点で `recovery_steps` に従って耐久回復へ流す。残り600秒以下、foreground処理中、claimable job 0件、hard stop以外の理由でsubmission pendingを読解停止条件にしない。
- candidate在庫、Library pending、fallback backlog、record bank枯渇、単一job失敗、status-only終端、1本完了、単一探索軸0件だけをrun終了理由にしない。
- **通常runは、次の3系統以外を理由に終了してはならない。** (1) 正規回復を試しても継続不能または安全に継続できない具体的な問題が発生した場合、(2) PDF・一次資料・Web/provider・Library等の**取得上限が実際に観測され**、必要な取得をそれ以上継続できない場合、(3) runの終了時刻が近づき、600秒開始禁止窓または180秒最終handoff窓の規則に従って安全にhandoffすべき場合。ノルマ達成、1本/1round完了、候補0件、submission/precheck/result pending、Actions進行中、単一provider失敗、単一論文の取得失敗、待機が発生したこと、次手が分かりにくいこと、通常処理が一区切り付いたことは、それ単独では終了理由にしない。取得上限は推測で立てず、実際の上限・拒否・quota/cap到達を観測した場合だけ使う。
- `finalization_gate` / `finalization_permit_issued` は停止判断には使用してよいが、**報告許可として扱わない。終了すると決めたrunは、終了理由が問題・取得上限・終了時刻接近のどれであっても、Scheduled Chatへ必ず最終報告を残してから終了する。** hard stop、safe handoff、取得上限、時間切れ接近を含め、報告を省略して終了してはならない。最終報告には少なくとも選択モード、今回の処理件数/round数、耐久反映、未完了事項、終了理由、確認できた最終main SHAを含める。最終mainを再取得できない問題で終了する場合は、最後に確認できたSHAと再取得不能であることを明記する。
- 残り600秒以下の開始禁止窓に入ったら新規独立作業を開始しない。**ただし開始済みDiscovery round（precheck result待ち、成功precheckの評価中、Discovery submission result待ち、正規recovery中）もResearch/Auditの開始済み作業と同じく継続対象**であり、600秒到達だけで終了してはならない。進行中作業・必要な非同期結果確認が本当に0件のときだけ安全handoff後に終了してよい。残り180秒以下では新規内容作業を止め、耐久保存と安全な引き継ぎだけを行う。処理中resultが残る場合、180秒より前は待機ミクロタスクを挟みながら追跡し、180秒以下になってもpendingならsubmission/request identity・result path・現在状態・次に行うべき正規操作が耐久保存済みであることを確認してhandoffする。

### 7.3 実行環境・transport障害の診断記録

Scheduled Chatで操作不能・platform limit・transport障害を理由に継続不能またはhandoffする場合、単に「操作できない」「GitHub操作を継続できない」と記録してはならない。**失敗した具体的な操作を、再現可能な粒度で必ず記録する。** 通常チャットとScheduled Chatでは利用可能なtool/transportが異なり得るため、リポジトリ回帰と実行環境差を切り分けられる情報を残す。

最低限、次をrun-stateの `runtime_condition_detail`、耐久handoff、最終報告のうち保存可能な箇所へ記録する。

- 失敗した段階（例: HEAD読取、worker-router読取、claim request write、Actions確認、result読取、record bank write、completed-submission request write、submission result確認）。
- **実際に試した操作/transport**（GitHub read、GitHub write、Actions read、Library write等）。利用可能なtool名を推測で列挙せず、実際に呼び出した操作だけを記録する。
- 対象repository/path/request_id/attempt_id等のidentity。秘密情報・認証情報は記録しない。
- 観測したエラー種別と、可能なら短いerror message / status。エラーが返る前にplatform側でtool call自体を拒否した場合はその事実を明記する。
- 正規回復として何を何回試したか、その結果。
- **直前まで成功していた操作**。たとえばHEADとworker-routerのreadは成功したがwriteだけ失敗した場合、それを明示する。
- 「未試行」「利用不能」「試行して失敗」を区別する。利用可能な正規transportを試していない状態で `transport_unrecoverable` と結論しない。
- **GitHub readが成功しており、ファイル作成・更新API/connectorが利用可能なら、GitHub writeは未試行扱いにしない。** 必要なrequest/direct-take等の正規pathへ実際のcreate/updateを試し、その具体的な失敗を観測して初めてwrite障害候補とする。shell/Python/CLIが無いことはwrite失敗の証拠ではない。

GitHub read/writeの一部だけが失敗した場合は、第6節のprobeと正規回復を行い、read成功をwrite成功と同一視しない。逆にwrite失敗をGitHub全体のread不能とも扱わない。Scheduled Chat固有の能力差が疑われる場合も、観測事実だけを記録し、リポジトリ変更が原因だと推測してhard stopにしない。

hard stop / safe handoffに入る場合の最終報告には、少なくとも **`failed_operation`、`last_successful_operation`、`recovery_attempts`、`observed_error`** に相当する4情報を人間が読める形で含める。これらを特定できない場合は「不明」と明記し、曖昧な一般文へ置き換えない。

## 8. 誤経路に入った場合

実行可能スクリプトが標準エラー出力（stderr）へ出す `[WORKER-GUIDE]` は、そのコマンド実行中の**必須行動指示**である。ワーカーは表示された順番に従い、ガイドが明示した完了条件を満たす前に次段へ進まない。

- `[待機]`: 完了またはエラー案内が出るまで、その処理に依存する次操作を開始しない。処理中に別の同目的スクリプトへ切り替えない。
- `[完了]` と `[次]`: 正常終了後の後続手順。記載されたスクリプト、結果ファイル、進行条件を順番どおり確認する。結果ファイルの `next_action` / `instructions` がある場合は併せて従う。
- `[手順エラー]` と `[正しい手順]`: その場で別経路へ迂回せず、示された復旧手順で同じ現行入口へ戻る。旧schema・manual手順・直接state編集で回避しない。
- JSON等の機械可読出力はstdout、ワーカー向け案内はstderrで分離される。案内をJSON本文として扱わない。

検証処理が `next_action` または `recovery_steps` を返した場合、それがその実行時点の復帰手順の最優先指示である。この文書と矛盾して見える場合も機械案内に従い、矛盾を隠さず最終報告の相談事項へ残す。**ただし保守・監査による実装変更は、稼働中のactive claim / immutable submission / result readerが使う現行schema・入口・読取契約を壊してはならない。破壊的変更が必要ならactive処理が収束するまで延期し、移行期間は後方互換読取を維持する。**

ワーカーは次を行う。

1. 最新HEADと対象stateを再取得する。
2. エラーが示した現行入口へ戻る。
3. 同一payloadの二重投入を避ける。
4. 旧schema、旧manual workflow、固定 `chat-inbox.json`、旧fallbackへ迂回しない。

「エラーになったので別の古い経路を試す」は禁止する。

## 9. 08:30更新とmaintenance

毎時 `:30` のScheduled Chatから起動したworkerのうち、**08:30 JSTのrunだけ**を日次更新・maintenance専用runとする。このrunではResearch / Audit / Discoveryを行わない。

実行順序は固定する。

1. 先に `framework-updates/**`、`llm-releases/**` の前回確認日時を読み、前回以降の一次資料（公式release / PR / documentation / model provider公式発表）を確認する。単なるmodel allowlist、軽微bugfix等は各READMEの掲載方針に従い除外する。
2. 更新があれば、最新blob SHAを基準に一意な `attempt_id` を持つ `.survey/update-worker/update-payload.json` と `update-inbox.json` を作る。`.github/workflows/update-helper.yml` / `.survey/scripts/update_worker.py` の正規入口で反映し、`.survey/update-worker/result.json` の同じ `attempt_id` で `ok=true` を確認する。更新が0件でも「確認済み」を最終報告へ残す。固定update inbox/payloadを過去attemptのまま再実行しない。
3. update result確認後に最新mainを再取得し、対象READMEの最終確認日と反映内容が一致することを確認する。ここまでを「非論文更新完了」とする。
4. 非論文更新の保存が完了した後、**runの最後の独立作業としてmaintenanceを実行する。**
5. maintenanceは `.survey/work-queue/maintenance-cycle.json` の `maintenance_pending=true` を耐久反映して `.github/workflows/maintenance.yml` を起動し、GC、index再構築、品質・メタデータ監査、整合性確認を直列実行させる。
6. maintenance workflowの結果を確認し、完了後の最新 `main` と `maintenance-cycle.json` を再取得して、`maintenance_pending=false`、かつ `last_maintenance_completed_at >= actual_invocation_start` が耐久反映されたことまでを今回08:30 runの完了条件とする。run-state fast laneはこの条件を満たす前は `RUN_0830_MAINTENANCE` を返し、完了後だけ最終化を許可する。workflowがhard stopで確認不能なら、その事実と未完了状態をhandoffしScheduled Task自体は止めない。未完了08:30 maintenanceの回収責任は次の`:45` STATUS異常修復に置き、通常の`:00`/`:30`論文runはmaintenanceを再発火しない。
7. 最終報告には非論文更新点（0件なら0件と明記）に加え、update result、maintenanceの起動・完了状態、GC/監査/整合性確認の結果、最終main SHAを含める。

maintenance実行の責任は08:30 JSTの `:30` workerに集約する。通常runでは定期maintenanceを発火させず、旧run-countカウンタも実行条件に使わない。
