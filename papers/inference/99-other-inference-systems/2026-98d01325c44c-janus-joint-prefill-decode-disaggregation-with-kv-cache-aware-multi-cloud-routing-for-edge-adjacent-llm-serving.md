---
canonical_id: DOI:10.4108/eetiot.13349
doi: 10.4108/eetiot.13349
title: 'Janus: Joint Prefill/Decode Disaggregation with KV-Cache-Aware Multi-Cloud Routing for Edge-Adjacent LLM Serving'
summary: Janusは、マルチクラウドでプリフィルとデコードを分離するLLMサービングにおいて、KVキャッシュ転送を固定処理ではなくスケジューリング変数として扱うオンラインスケジューラである。prefix-aware配置、デコード先、migrate/recompute/hybrid/selectiveの4種KV輸送、長期コスト制御、プールサイズ調整を統合し、96 pod・512 GPU相当のトレース駆動シミュレーションで強いマルチクラウド基準に対し中央値TTFT 3.8倍、P99 TTFT 4.6倍、有効スループット 2.1倍、コスト38%削減を報告する。
list_summary: プリフィル/デコード配置とKV輸送方式を共同最適化し、異種マルチクラウドLLMサービングのTTFT・有効スループット・コストを同時改善する。
authors:
- K. B. Aruna
- V. Kaliraj
- L. Sudha
- V. Sureka
authors_affiliations: R.M.D. Engineering College, Tamil Nadu, India
published: '2026-08-12'
publication: EAI Endorsed Transactions on Internet of Things
publication_type: 査読済み論文
publication_status: Received 2026-06-05; accepted 2026-08-02; published 2026-08-12
lineage: disaggregated LLM serving / KV-cache routing / multi-cloud scheduling / prefix-cache locality
topics:
- プリフィル・デコード分離
- KVキャッシュ転送
- マルチクラウド推論
- prefix-aware ルーティング
- Lyapunov最適化
importance: 単一クラスタ内の高速RDMAを前提にした従来の分離サービングから、WAN帯域・スポット価格・異種GPU・データ所在地制約を含むマルチクラウドへ問題を拡張し、KV輸送方式そのものを第一級の意思決定にした点が重要である。
hardware_evaluation: 単一podの実測マイクロベンチマークでモデル係数を校正し、96 pod・512 GPU、AWS/GCP/Azure、6 regionの離散事象シミュレーションで評価。物理マルチクラウド実配備は未実施。
quality_effect: モデル出力品質を近似する手法ではなく、配置・転送・容量制御を変えるサービングシステム研究。主な品質軸はSLO、TTFT、有効スループット、コスト、再利用率。
references_checked_at: '2026-09-23'
references_source: primary manuscript
references_total: 62
source: https://doi.org/10.4108/eetiot.13349
sources:
- https://publications.eai.eu/index.php/IoT/article/view/13349
- https://publications.eai.eu/index.php/IoT/article/download/13349/4240/35587
code: https://github.com/arunakbofficial-tech/Janus
implementation: 17.1K行の制御プレーン試作、vLLMデータプレーン拡張、離散事象シミュレータを実装。公開コードあり。
last_checked: '2026-09-23'
references: []
last_audited: null
audit_version: 0
---

# Janus: Joint Prefill/Decode Disaggregation with KV-Cache-Aware Multi-Cloud Routing for Edge-Adjacent LLM Serving

> プリフィル/デコード配置とKV輸送方式を共同最適化し、異種マルチクラウドLLMサービングのTTFT・有効スループット・コストを同時改善する。
## 書誌情報
- **著者**: K. B. Aruna, V. Kaliraj, L. Sudha, V. Sureka
- **著者・所属**: R.M.D. Engineering College, Tamil Nadu, India
- **公開**: EAI Endorsed Transactions on Internet of Things
- **種別**: 査読済み論文
- **対象**: プリフィル・デコード分離、KVキャッシュ転送、マルチクラウド推論、prefix-aware ルーティング、Lyapunov最適化
- **実装**: 17.1K行の制御プレーン試作、vLLMデータプレーン拡張、離散事象シミュレータを実装。公開コードあり。
## 概要
Janusは、マルチクラウドでプリフィルとデコードを分離するLLMサービングにおいて、KVキャッシュ転送を固定処理ではなくスケジューリング変数として扱うオンラインスケジューラである。prefix-aware配置、デコード先、migrate/recompute/hybrid/selectiveの4種KV輸送、長期コスト制御、プールサイズ調整を統合し、96 pod・512 GPU相当のトレース駆動シミュレーションで強いマルチクラウド基準に対し中央値TTFT 3.8倍、P99 TTFT 4.6倍、有効スループット 2.1倍、コスト38%削減を報告する。

新規性はKV輸送をサービングの固定機構ではなく要求単位の最適化変数へ昇格させ、接頭辞再利用とマルチクラウド価格・帯域を一つのオンライン制御系に結合した点にある。オフライン問題のNP困難性を踏まえ、S1の接頭辞考慮プリフィル配置、S2のKV考慮デコード・輸送選択、S3のリアプノフ（Lyapunov）ドリフト加罰則による長期制御、S4の低頻度プール容量調整へ分解する。

KV輸送は全量移送M、再計算R、層単位ハイブリッドH-k、接頭辞転送と接尾辞再計算を組み合わせるΣを比較し、H-kには層分割の閉形式最適解を与える。これにより接頭辞の所在、ネットワーク帯域、再計算能力、GPU価格を同じ要求の中で比較できる。

代表結果として、TTFT改善はLlama-3-70B, 96-pod/512-GPU multi-cloud シミュレーションでMooncake-MCに対してmedian 3.8×, P99 4.6×。KV輸送とprefix配置を共同選択することでtail 遅延も大幅に改善する。
## 問題設定
プリフィル（prefill）とデコード（decode）を別GPUプールへ分離すると各段階の計算特性に合わせて最適化できるが、両段階を結ぶKVキャッシュは要求ごとに数百MiB〜数GiBとなる。単一クラスタでは高速な遠隔直接メモリアクセス（RDMA）で転送できる一方、マルチクラウドでは広域網（WAN）が2〜12 Gb/s程度まで落ち、GPU種類、地域、スポット価格、外向き転送料金も変動する。

そのため最安デコード先へ単純に移すとKV転送が最初のトークンまでの時間（TTFT）を支配し、接頭辞キャッシュ所有者だけを優先すると負荷集中、価格だけを見ると再利用率低下が起きる。Janusはプリフィル配置、デコード配置、KVの全量移送・再計算・部分転送、長期費用、容量調整を同時に扱う問題として定式化する。
## 新規性
新規性はKV輸送をサービングの固定機構ではなく要求単位の最適化変数へ昇格させ、接頭辞再利用とマルチクラウド価格・帯域を一つのオンライン制御系に結合した点にある。オフライン問題のNP困難性を踏まえ、S1の接頭辞考慮プリフィル配置、S2のKV考慮デコード・輸送選択、S3のリアプノフ（Lyapunov）ドリフト加罰則による長期制御、S4の低頻度プール容量調整へ分解する。

KV輸送は全量移送M、再計算R、層単位ハイブリッドH-k、接頭辞転送と接尾辞再計算を組み合わせるΣを比較し、H-kには層分割の閉形式最適解を与える。これにより接頭辞の所在、ネットワーク帯域、再計算能力、GPU価格を同じ要求の中で比較できる。
## 手法
### 手法のあらまし
処理は要求到着から容量調整まで四段階でつながる。まず制御プレーンが分散基数木索引から要求の最長再利用接頭辞とその所有プールを取得し、モデル互換性、KV精度、テンソル並列・パイプライン並列構成、データ所在地制約、GPU/KV容量を候補へ反映する。S1は再利用可能な接頭辞トークン量を単調劣モジュラ目的としてプリフィル先を選び、容量に余裕がある通常領域では実装貪欲法に1/2、異種KV容量制約が効く場合には1/3の保証を与える。

次にS2が選択済みプリフィル先から互換デコード先を列挙し、全量移送M、再計算R、層単位ハイブリッドH-k、選択転送Σについて、転送遅延、GPU再計算遅延、外向き転送費、GPU費、仮想待ち行列の混雑価格を同じ目的関数へ換算して最小の組を選ぶ。H-kでは1層の転送時間aと再計算時間bを独立ストリームで重ね、k*=Nlayers*b/(a+b)の前後整数を実評価して分割を決める。

要求処理後、S3はSLO違反量を仮想待ち行列へ蓄積し、価格重みVを介して短期遅延と長期費用の均衡をオンライン更新する。さらにS4が30秒周期で需要予測、利用率、待ち行列、スポット停止リスクを読み、各地域のGPU上限内でレプリカ数を増減する。このため個別要求の接頭辞局所性とKV輸送判断が、長期の価格・容量制御へ連続して反映される。

### S1: 接頭辞考慮プリフィル配置
分散基数木索引で各要求の最長再利用接頭辞と所有プールを追跡し、再利用できるトークン価値を単調劣モジュラ集合関数として定義する。モデル互換性、プリフィル処理能力、GPUメモリ内のKV容量を満たす候補だけを残し、連続貪欲法では1-1/e、実装する組合せ貪欲法では容量余裕時1/2、異種KV容量が拘束する場合1/3の近似保証を持つ。

配置の価値には接頭辞を再計算せずに済む時間と現在のプール負荷が反映され、同じ接頭辞を持つ要求を所有プールへ寄せつつ過負荷を避ける。接頭辞所有者が無い、または全候補が不適格な要求も破棄せず、完全プリフィルを行う互換プールのうち費用関数が最小の先へフォールバックする。評価トレースでは高速貪欲法と連続貪欲参照の再利用目的値差は3.4%以内で、容量拘束は4%未満のマイクロバッチだった。

### S2: KV考慮デコードと輸送選択
S1が決めたプリフィル先ごとに、モデル、KV精度、テンソル配置、データ所在地制約を満たすデコード候補を列挙する。各候補で全量移送M、ネットワーク近傍での再計算R、層分割ハイブリッドH-k、接頭辞転送と接尾辞再計算を並行するΣの遅延と費用を同じ単位へ揃える。

全量移送ではKVサイズを実効帯域で割り外向き転送料金を加え、再計算ではデコード側近傍のプリフィル級GPUで不足KVを再生成する時間とGPU秒単価を加える。輸送遅延Λ、価格重み付き費用VΨ、仮想待ち行列Qと追加待ち時間δの和を最小化する。Llama-3-70Bの16K入力では12 Gb/s級WANで2.5GiB移送約1.8秒と再計算約1.9秒が拮抗する一方、2.5 Gb/sでは移送約8.6秒となるので再計算が優位になる。

### 層単位ハイブリッド・パイプライン
全層KVを送る代わりに先頭k層を転送し、残り層をデコード側近傍のプリフィル級GPUで再計算する。転送専用DMAストリームと再計算ストリームを重ねると理想遅延はmax(ka,(N-k)b)となるため、二直線の交点k=N*b/(a+b)が実数最適となる。

実装では床関数・天井関数で得る二つの整数候補を実評価し、パイプライン充填・排出の上界max(a,b)も加える。論文の8K冷キャッシュ例では25層転送・55層再計算で560msとなり、全量移送1792msと全再計算806msの双方を下回る。選択転送Σはすでにデコード側が接頭辞を保持する暖機状態で有利になり、6K/8Kを保持する例では残りを分割して224msまで短縮する。

### S3/S4 長期費用・容量制御
S3はSLOクラスごとの違反予算を仮想待ち行列へ変換し、リアプノフ・ドリフト加罰則法で混雑とドル費用を継続的に価格付けする。各時間枠で仮想待ち行列が大きいデコード先には追加の混雑価格が付き、S2がその先を避けるため、短期の要求割当が長期SLO制約を満たす方向へ戻される。理論上は価格重みVを大きくすると分解方策群内の最適費用との差がO(1/V)へ縮む一方、待ち行列はO(V)へ増える。

S4は30秒ごとに需要予測と仮想待ち行列を確認し、予測利用率85%超または高待ち行列なら増設、40%未満かつ低待ち行列なら縮小し、さらにスポット停止率に比例する余裕を足す。最後に地域ごとのGPU容量へ切り詰め、Raft合意で新しいプール構成を確定する。これにより数ミリ秒単位の要求ルーティングと数十秒単位の容量変更を分離しつつ、同じ混雑・価格信号で接続する。

### 全体のデータ／制御の流れ
Raft協調制御プレーンがAWS、GCP、Azureの異種プリフィル・デコードプール、分散基数木索引、価格・帯域テレメトリを管理する。データプレーンではKV転送と再計算をCUDA/DMAストリームで重畳し、テンソル並列構成が異なるプール間では転送中に再シャーディングする。

要求のデータ所在地制約もデコード候補選別へ入れ、接頭辞キャッシュはテナント間で隔離する。分散索引はgossipで更新されるため、制御プレーンはstale entryを考慮しながら配置する。
## 評価条件
- **ハードウェア**: 評価器は96 pod・512 GPUをAWS、GCP、Azureの6 regionへ配置し、H100、A100、L4、MI300Xを含む異種構成をモデル化する。物理マルチクラウド全体での実機評価ではなく、単一podの実測マイクロベンチマークでプリフィル/デコード係数を校正した離散事象シミュレーションが中心。
- **ソフトウェア**: 17.1K行のJanus制御プレーン、vLLMデータプレーン拡張、Raft制御、分散radix index、離散事象シミュレータ、multi-cloud 比較対象 shim、合成 トレース generatorを実装。公開リポジトリでコードと再現用合成トレースを提供する。
Llama-3-8B、Llama-3-70B、Mixtral-8x22Bを対象に、assistant ワークロードを再生したトレース-driven シミュレーションを実施する。比較対象にはMooncake-MC等を置き、TTFT中央値/P99、有効スループット、reuse-capture、GPU費用、WAN egress、SLO違反を測定する。WAN帯域、spot preemption、region failure、5倍load spike、長文脈32K〜128K、tenant 重み 5:2:1、pod数12〜192などを変化させ、ablationとfault injectionを行う。オフラインLP緩和oracleとも比較する。
強みはマルチクラウド分離サービングの制御問題を広く評価し、価格・帯域・障害・prefix localityを同時に扱う点。主要なエンドツーエンド数値はシミュレーション出力であり、実WAN・クラウドAPI・実spot preemptionを含む物理マルチクラウド展開での再現は今後の課題である。
## 主要結果
Janusは強いmulti-cloud 比較対象に対し、Llama-3-70Bで中央値TTFTを3.8倍、P99を4.6倍改善し、有効スループットを2.1倍、reuse-captureを71%へ高め、費用を38%削減したと報告する。prefix locality、WAN帯域、spot priceを共同最適化する効果は障害やburstでも維持され、12〜192 podへの拡張時もスケジューラ 遅延は0.6から1.4msへ緩やかに増える。

- TTFT改善 / median 3.8×, P99 4.6× (比較対象: Mooncake-MC; 条件: Llama-3-70B, 96-pod/512-GPU multi-cloud シミュレーション) — KV輸送とprefix配置を共同選択することでtail 遅延も大幅に改善する。

- 有効スループット / 2.1× (比較対象: strongest constructed multi-cloud 比較対象; 条件: トレース-driven シミュレーション) — SLOを満たす処理量が増える。

- reuse-capture / 71% (比較対象: Mooncake-MCの約1.5×、round-robinの約9×; 条件: multi-tenant assistant トレース) — 単なるprefix-hit機会ではなく、配置によって実際に再利用できたprefix トークン量が増える。

- cost reduction / 38% (比較対象: strongest multi-cloud 比較対象; 条件: volatile spot prices and heterogeneous clouds) — 価格裁定をKV状態移動コストと同時に評価することで、遅延悪化を避けながら費用を下げる。

- hybrid transport / 560 ms vs migrate 1792 ms / recompute 806 ms (比較対象: pure transport policies; 条件: cold デコード pool, 8K prompt, calibrated model) — 25層転送・55層再計算の分割で、全量移送より3.2倍、全再計算より1.4倍短いモデル推定遅延となる。

- oracle proximity / 89.4% of oracle cost, 92.1% of oracle TTFT (比較対象: offline LP-relaxation oracle with future knowledge; 条件: シミュレーション トレース) — オンライン分解の損失が評価トレースでは約11%範囲に収まる。

### 負の結果・境界条件
- 主要結果は実クラウド横断配備ではなく、単一pod実測で校正したシミュレータによる。HybridのCUDA/DMA重畳も実行timeline上は可能とするが、nsys/ncuでの実測重畳効率は未検証。長文脈ではWAN全量migrateが不可能になる領域があり、最適方策は帯域とキャッシュ warmnessに強く依存する。region failure時もJanusのP99 spikeは47秒まで上がるため障害影響自体は消えない。

### 結果の読み方
Janusの結果は『最適なKV輸送方式は一つではない』ことを定量化している。12 Gb/s級WANと16K promptでは移送と再計算が拮抗し、2.5 Gb/sでは再計算、100 Gb/s intra-regionでは移送が優位になるため、prefix localityとqueueを含め要求ごとに方策を切り替える価値がある。
## 品質への影響
生成品質を変更する圧縮・近似法ではないため、主な影響は応答遅延、SLO達成率、費用、再利用率。recomputeも同一モデルプリフィルを再実行する設計で、論文はモデル精度劣化を主要論点としていない。
## 既存研究との差
DistServe、Splitwise、Mooncake、MemServeなどはプリフィル/デコード分離やKV共有を主に単一クラスタ・高速fabric内で扱うのに対し、Janusはcross-cloud WANの帯域・egress料金・spot価格を明示的に目的へ入れる。プリフィル-as-a-Serviceのようなcross-datacenter研究よりも、KVを送るか再計算するか、どの層/部分だけ送るかをデコード配置と同時に選ぶ点が広い。Llumnix等の動的スケジューラと比べても、prefix所有位置と4種KV輸送を長期Lyapunov制御へ統合する点が特徴である。
## 限界
エンドツーエンド評価は96 pod/512 GPU相当の離散事象シミュレーションであり、実際のAWS/GCP/Azureをまたぐ物理展開でのネットワークjitter、API制御遅延、障害相関、spot 追い出し挙動は未検証である。モデル係数は単一pod実測で校正しているが、Hybridのtransfer/recompute overlap効率はhardware トレースで未確認。分散radix indexはgossipによりstaleになり得る。理論保証は分解されたpolicy classと明示仮定の範囲で、offline全体最適とのdecomposition gapが残る。proprietary raw assistant トレースは公開されず、統計一致合成 トレースで再現する。
## 実装状態
査読済みEAI論文として2026-08-12公開。17.1K行の制御プレーン、vLLM拡張、simulator、比較対象 shim、合成 トレース、calibration harness、plot scriptsをGitHubで公開している。物理マルチクラウド実証はfuture work。
## 研究上の位置づけ
LLM推論基盤の中では、プリフィル・デコード分離、KVキャッシュ階層/転送、prefix-aware ルーティング、異種GPU スケジューラ、multi-cloud cost optimizationの交点に位置する。特にKV キャッシュを『移送される状態』から『移送・再計算・部分移送を選択できる制御対象』へ変えたことで、Mooncake/KVDirect/LMCache系のKV-centric servingとSkyPilot/Helix系の異種・multi-cloud配置を接続する研究として整理できる。
## 一次資料
- https://publications.eai.eu/index.php/IoT/article/view/13349
- https://publications.eai.eu/index.php/IoT/article/download/13349/4240/35587
