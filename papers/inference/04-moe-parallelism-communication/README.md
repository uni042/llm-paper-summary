# MoE並列化・通信

この系統では、混合専門家モデル（Mixture of Experts; MoE）の専門家配置、並列化、チップ間・ノード間通信、負荷分散を扱う推論システム研究を整理する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（9本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [HetRoute: Heterogeneous and Cost-aware Collaborative Routing Framework for Distributed Edge MoE Inference](2026-2608.00577-hetroute-collaborative-routing.md) | ✓ | 0 | 地理的に分散した異種エッジサーバで混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、各トークンが選んだ複数の専門家をどのサーバへ送るかで、ネットワーク転送、GPUとCPU間の専門家読み込み、GPU計算待ち、量子化による品質損失が同時に絡む。HetRouteは、これらを一つの費用モデルで評価し、事前段階では専門家の配置・GPU常駐・複製精度を決め、実行時には上位k個の専門家を個別ではなく集合として割り当てる。10台の異種エッジサーバによるトレース駆動評価では、Mixtral-8x7Bの代表条件で平均遅延156ms、P99遅延286ms、通信量1.24GB/1000トークン、スループット1490トークン/秒を報告し、品質低下を設定予算内に抑えた。 |
| 2026-08 | [FreeBalance: Pre-Routing Online Moe Load Balancing via Residual Workload Prediction](2026-2608.14205-freebalance-prerouting-online-load-balancing.md) | ✓ | 0 | 混合専門家モデル（Mixture of エキスパート; MoE）のオンライン負荷分散では、通常は現在層のルータが専門家選択を終えてから専門家交換を決めるため、重み移動が推論クリティカルパスに残る。FreeBalanceは残差接続により隣接層の隠れ表現が近いことを利用し、現在層のルータを前層出力へ先行適用して専門家負荷を予測する。予測は配置計画だけに使い、実際のMoE計算は本来のルーティング結果を使うため出力を変えない。注意計算時間から移動予算を計算し、その時間内に隠せる専門家交換だけを決定論的に選ぶ。8台のNVIDIA A800、Qwen3-30B-A3BとMoonlight-16B-A3B、LongBench等で評価し、最大/平均rank負荷比を最大32.8%下げ、プリフィル遅延を平均13.1%削減し、1層あたり平均5.1専門家分の移動費を隠す。 |
| 2026-07 | [Mixture-of-Experts Serving](2026-2607.17880-mixture-of-experts-serving-online-algorithms.md) | ✓ | 0 | 混合専門家モデル（Mixture of エキスパート; MoE）で専門家需要が時間変動する状況を、各専門家へ何台の追加GPUを割り当てるかというオンライン資源配置問題として定式化した理論研究。各専門家には最低1台を置き、余剰k台を動的に配る。各時刻の費用を、最も遅い専門家の負荷÷GPU数で表すサービス遅延と、前時刻からGPU割当を動かしたL1距離で表す再構成費の和とする。分数解に対する正則化付き貪欲法と遅延しきい値丸めを組み合わせ、多項式時間でO(√log k)競合比を与える。さらにオンライン双対問題にΩ(√log k)障壁、静的版に2近似、整数性ギャップ2-1/m、NP困難性、指数時間仮説（ETH）下で完全多項式時間近似方式（FPTAS）が存在しないことを示す。 |
| 2026-06 | [Coordinated Scheduling for MoE LLM Serving](2026-2606.15177-gimbal-coordinated-moe-serving-scheduling.md) | ✓ | 0 | 混合専門家モデル（Mixture of エキスパート; MoE）のサービングでは、フロントエンドのデータ並列エンジンへの要求振り分けと、バックエンドの専門家配置を別々に最適化すると、入力長やKVキャッシュ使用量の偏りと専門家ホットスポットが互いに増幅される。Gimbalは各エンジンの残りプリフィル量、待機トークン量、KVキャッシュ使用量、MoE圧力を使う細粒度要求スケジューラと、送信元データ並列群から各専門家への実測ルーティング行列を使う専門家配置器を協調させる。vLLM上約1.7K行で実装し、4台のH100、Qwen3-30B-A3B、BurstGPT負荷でvLLM比の平均TTFTを42.9%、平均TPOTを33.3%削減し、高負荷スループットを3.0%改善する。 |
| 2026-05 | [SiDP: Memory-Efficient Data Parallelism for Offline LLM Inference](2026-2605.28095-sidp-memory-efficient-data-parallelism.md) | ✓ | 0 | オフラインLLM推論では大きなバッチを維持するとGPU演算効率が上がるが、通常のデータ並列は各GPUにモデル重みを完全複製するため、KVキャッシュに使えるHBMが減ってバッチを増やせない。SiDPはフィードフォワードネットワーク重みをデータ並列グループ内で一度だけ保持する分散重みプールへ変え、非所有GPUが必要時に共有する。大バッチ中は遠隔重みを非同期先読みして各GPUで計算する重みサービス方式、小バッチの末尾では活性値を重み所有GPUへ送りまとめて計算する計算サービス方式へ切り替える。H20/H200/B200上のQwen3-32B、Llama-3.1-70B、Qwen2.5-72BでKV容量を最大1.8倍、エンドツーエンドスループットを最大1.5倍にする。 |
| 2026-04 | [DWDP: Distributed Weight Data Parallelism for High-Performance LLM Inference on NVL72](2026-2604.01621-dwdp-distributed-weight-data-parallelism.md) | ✓ | 0 | 大規模な混合専門家モデル（Mixture of エキスパート; MoE）を複数GPUで推論すると、従来の専門家並列では各層の全対全通信と同期のため、入力長や専門家選択が偏ったとき速いGPUまで遅いGPUを待つ。DWDPは注意機構の重みを各GPUへ複製し、MoEの専門家重みだけを同一NVLinkドメイン内のGPUへ分散配置する。各GPUは次層で不足する専門家重みを非同期に先読みし、集団通信を使わず自分に必要な転送が終わり次第独立に進む。GB200 NVL72上のDeepSeek-R1で、20〜100 TPS/userのサービス範囲において同等の利用者当たり生成速度でGPU当たり出力スループットを平均8.8%改善する。 |
| 2026-03 | [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md) | ✓ | 0 | 低バッチのオンデバイスMoEでは、専門家ごとの活性化トークン数が長い裾を持ち、オンチップ容量不足からDDRへ重みを逃がすため、重み読込・チップレット間負荷不均衡・重複保持が同時にボトルネックになる。本論文のFully Sharded エキスパート Data Parallelism（FSE-DP）は、専門家重みをチップレット間で細かいマイクロスライスに分け、一つの物理コピーを動的な軌跡に沿って流す。高負荷専門家と低負荷専門家を組み合わせ、DDR読込・D2D転送・演算を重ね、軽量ハードウェアスケジューラで実行する。EP/Hydra比で1.22〜2.00倍高速化し、オンチップメモリを最大78.8%削減する。 |
| 2026-03 | [A Switch-Centric In-Network Architecture for Accelerating LLM Inference in Shared-Memory Network](2026-2603.28239-scin-switch-centric-in-network-llm-inference.md) | ✓ | 0 | テンソル並列推論では各層の注意機構と全結合ネットワーク後に全GPUの部分結果を集約するAll-Reduceが入り、低遅延・低同時実行数では計算で通信を隠しにくい。既存のNVLink SHARP（NVLS）はスイッチ内集約を使うが、GPUが要素単位のロード／ストアとして集団通信を駆動するため、集約結果がいったん要求GPUへ戻ってから再びスイッチへ送られる余分な往復と、量子化値と尺度係数を対応付けられない制約が残る。SCINはスイッチ内アクセラレータ（In-Switch Accelerator; ISA）がAll-Reduce全体を主導し、参加GPUのメモリを直接読み、スイッチ内で集約して全GPUへ直接書き戻す。さらにINT8量子化値を尺度係数と対応付けて復元・集約・再量子化するパイプラインを備える。4端点＋1スイッチのFPGA試作で実現可能性を示し、H200相当の8GPUシミュレーションではNVLS比でAll-Reduce最大2.76倍、最初のトークンまでの時間（Time To First トークン; TTFT）最大1.42倍、トークン間時間（Time Per Output トークン; TPOT）最大1.12倍の改善を報告する。 |
| 2026-01 | [A Scheduling Framework for Efficient MoE Inference on Edge GPU-NDP Systems](2026-2601.03992-edge-gpu-ndp-moe-scheduling.md) | ✓ | 0 | エッジ端末で混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、全専門家の重みが民生GPUのメモリへ収まらず、外部メモリからの転送が推論を支配しやすい。近データ処理（Near-Data Processing; NDP）付きメモリへ専門家計算を移す既存方式でも、トークンごとの専門家選択が偏るとNDP装置間の負荷が不均衡になり、GPUが待たされる。本論文は、各専門家の行列計算を複数NDP装置へ分割するテンソル並列、GPUとNDPの実行時間を釣り合わせる動的割当、プリフィル中に得た活性頻度だけで頻出専門家をGPUへ先読みする方式を統合する。RTX 5080相当GPUと最大6基のNDP-DIMMを模擬した評価では、MoNDEに対してエンドツーエンドで平均2.41倍、最大2.56倍の高速化を報告する。 |

### 1年以上前

該当なし。
<!-- survey:auto:end -->
