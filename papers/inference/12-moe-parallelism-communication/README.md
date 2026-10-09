# MoE Parallelism / Communication

MoEの専門家並列、テンソル並列との混成、all-to-all通信、専門家配置、負荷分散、ネットワークトポロジーを共同最適化し、複数GPU・複数ノード間の通信待ちと偏りを減らす研究をまとめる。

## 分類境界

主要貢献がMoEのexpert parallelism、all-to-all通信、分散expert配置、通信と計算の重畳、ネットワークトポロジーまたは分散負荷分散である論文を含め、単一GPU内のexpert offloadやexpert数削減だけの研究は含めない。

### 含める研究

- expert parallelismとall-to-all通信最適化
- 複数GPU／複数ノードのexpert配置と負荷分散
- MoE通信と計算の重畳・ネットワーク最適化

### 含めない研究

- 単一GPU向けexpert offload
- expert pruning・mergingだけを主題とする研究

## 近傍系統

- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)
- [01-offload-hierarchical-memory](../01-offload-hierarchical-memory/)
- [02-adaptive-expert-computation-compression](../02-adaptive-expert-computation-compression/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（41本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [GPU-Initiated Networking for NCCL](2025-2511.15076-gpu-initiated-networking-for-nccl.md)**  
  実装：[✓](https://github.com/NVIDIA/nccl) ・ リポジトリ内被引用：4  
  NCCL 2.28へGPUカーネルからRDMAを直接起動できるGINを追加し、直接GPU→NICとCPU代理を同一APIで切替。DeepEPのMoE通信をNVSHMEM相当の性能でNCCLへ統合する。

- **2026-07 · [Fine-grained Computation-Communication Overlap via Tile-level Signaling and Scheduling for Mixture-of-Experts](2026-2607.19539-tile-level-compute-communication-overlap-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  遠隔GPUへ返すMoE出力を先にタイル計算し、完成した行帯を専用通信カーネルが即時転送することで、第2の全対全通信の大半を専門家計算中へ隠し、4基A100でMoE層を最大2.74倍高速化する。

- **2026-03 · [NCCL EP: Towards a Unified Expert Parallel Communication API for NCCL](2026-2603.13606-nccl-ep-towards-a-unified-expert-parallel-communication-api-for-nccl.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの混合専門家（MoE）層では、ルータが各トークンを担当する専門家へ割り当て、専門家計算の後に結果を元の順序へ集約する。一方、実際にvLLMへ組み込んでQwen3-30B-A3Bを実行した場合は、DeepEPより出力トークン処理量が7〜10%低く、トークン間遅延も7〜9%長かった。

- **2026-01 · [Least-Loaded Expert Parallelism: Load Balancing An Imbalanced Mixture-of-Experts](2026-2601.17111-least-loaded-expert-parallelism-load-balancing-an-imbalanced-mixture-of-.md)**  
  実装：[✓](https://github.com/SalesforceAIResearch/LeastLoadedEP) ・ リポジトリ内被引用：2  
  標準的な専門家並列（専門家 Parallelism、EP）では専門家の重みを複数GPUへ固定配置し、選択された専門家を所有するGPUへトークンを送る。論文の層単体評価では、8台のH200上で極端な専門家偏りに対し最大6.11倍の速度改善とピークメモリの大幅削減を報告する。

- **2025-12 · [Efficient MoE Serving in the Memory-Bound Regime: Balance Activated Experts, Not Tokens](2025-2512.09277-efficient-moe-serving-in-the-memory-bound-regime-balance-activated-exper.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  混合専門家モデル（Mixture-of-Experts; MoE）を複数GPUへ載せる専門家並列（専門家 Parallelism; EP）では、人気専門家の複製を作り、各GPUへ配置し、同じ専門家を選んだトークンを複製間へ振り分ける。

- **2025-12 · [Efficient MoE Inference with Fine-Grained Scheduling of Disaggregated Expert Parallelism](2025-2512.21487-findep-fine-grained-disaggregated-expert-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  分離専門家並列で注意・共有専門家・専門家計算と双方向通信を細粒度タスクへ分割し、粒度と実行順を性能モデルから同時最適化して、最適化済みPPPipe比でスループットを最大1.61倍へ高める。

- **2026-07 · [OrderMoE: An expert similarity driven distributed edge MoE inference](2026-2607.17154-ordermoe-expert-similarity-distributed-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ルータ応答から専門家の機能類似性を推定し、類似専門家をエッジ間へ分散配置して、品質予算内なら遠隔の正確な専門家を局所類似専門家で代替し通信と遅延を削減する。

- **2026-05 · [Surviving Partial Rank Failures in Wide Expert-Parallel MoE Inference](2026-2605.10670-surviving-partial-rank-failures-wide-ep-moe.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：1  
  専門家並列の部分ランク障害を、通信相手・専門家被覆・CUDAグラフ可視経路の個別修復で全体再起動なしに復旧するEEPを提案する。

- **2026-04 · [Scaling Multi-Node Mixture-of-Experts Inference Using Expert Activation Patterns](2026-2604.23150-scaling-multinode-moe-expert-activation-patterns.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル時の専門家活性から似た要求を小バッチ化し、要求群で共発火する専門家を同じノードへ置くことで、マルチノードMoEの全対全通信を削減する。

- **2026-04 · [DWDP: Distributed Weight Data Parallelism for High-Performance LLM Inference on NVL72](2026-2604.01621-dwdp-distributed-weight-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DWDPは注意重みを各GPUへ複製し、MoE専門家重みだけをNVLinkドメイン内で分散する。必要重みを非同期先読みして全対全通信とGPU間同期を減らす。

- **2026-03 · [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エキスパートストリーミングは専門家重みをチップレット間の細粒度マイクロスライスへ分け、高負荷・低負荷専門家を組み合わせてDDR読込、チップレット転送、計算を重ね、オンチップ容量不足を緩和する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Scaling Inference Prefill with High-Radix Photonic Interconnects](2026-2609.01821-scaling-inference-prefill-high-radix-photonic-interconnects.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間通信が律速になるMoEプリフィルで、4倍帯域・最大1,152 GPUの光スケールアップ網をモデル化し、長文・高バッチ時のプリフィルを2〜5倍級に短縮する一方、デコード飽和へのボトルネック移動も示す。

- **2026-09 · [Epoch: Compiling Diffusion Blocks for Sparse MoE Serving](2026-2609.09748-epoch-diffusion-blocks-sparse-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散MoEの生成ブロックを再利用単位にし、候補エキスパート集合、確定トークンの期限付き出力、エキスパート並列の通信データをブロック内で疎化して、8基H100上で最良比較対象より最大2.7倍高速化するサービング方式。

- **2026-08 · [HetRoute: Heterogeneous and Cost-aware Collaborative Routing Framework for Distributed Edge MoE Inference](2026-2608.00577-hetroute-collaborative-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HetRouteは異種エッジ群で専門家配置・GPU常駐・複製精度を費用モデルで決め、Top-k専門家を集合としてサーバへ割り当てて、ネットワーク転送・計算待ち・量子化品質損失を抑える。

- **2026-08 · [FreeBalance: Pre-Routing Online Moe Load Balancing via Residual Workload Prediction](2026-2608.14205-freebalance-prerouting-online-load-balancing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FreeBalanceは前層出力を現層ルータへ先行入力して専門家負荷を予測し、注意計算中に予算内で専門家を交換する。正式ルーティングを維持し、負荷偏りと移動待ちを減らす。

- **2026-08 · [EasyBalance: Cross-Layer Load Balancing in Distributed MoE Inference](2026-2608.07964-easybalance-cross-layer-load-balancing-in-distributed-moe-inference.md)**  
  実装：[✓](https://github.com/yize-wu/EasyInfra) ・ リポジトリ内被引用：0  
  EasyBalanceが対象とするのは、混合専門家モデル（Mixture-of-Experts; MoE）の専門家並列（専門家 parallelism; EP）推論で、GPU間に配った専門家の処理量が入力ごとに偏る問題である。各バッチ内の層順序は保持するため、専門家選択やモデルの数値演算を近似する方式ではない。

- **2026-08 · [AirMoE: Realizing Over-the-Air Distributed Mixture-of-Experts Inference at the Wireless Edge](2026-2608.22932-airmoe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoE専門家の無線分散実行で、複数端末の専門家出力を空中計算で同時集約し、層感度を考慮した電力制御と専門家配置によって無線歪みによる推論精度低下を抑える。

- **2026-07 · [Mixture-of-Experts Serving](2026-2607.17880-mixture-of-experts-serving-online-algorithms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は時間変動する専門家需要へのGPU割当をサービス遅延と再構成費のオンライン最適化として定式化し、分数解の丸め・貪欲更新で再配置コストを抑える理論保証を示す。

- **2026-06 · [Director: Accelerating Distributed MoE Serving via Online Proactive Expert Placement](2026-2607.08782-director-online-proactive-expert-placement.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  待ち行列の入力からMoE専門家ルーティングを先読みし、通信が空く計算区間へ専門家移動を重ね、予測負荷と実測トポロジを使う配置最適化で静的・反応型配置の遅れを減らす方式。

- **2026-06 · [Coordinated Scheduling for MoE LLM Serving](2026-2606.15177-gimbal-coordinated-moe-serving-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Gimbalは要求の残りプリフィル量・待機量・KV使用量と専門家負荷を同時に見て要求振り分けと専門家配置を協調し、MoEサービングのキュー偏りとホットスポットを減らす。

- **2026-05 · [SiDP: Memory-Efficient Data Parallelism for Offline LLM Inference](2026-2605.28095-sidp-memory-efficient-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SiDPはデータ並列GPU間でFFN重みを一度だけ保持する共有プールを作り、バッチ規模に応じて重み先読み型と活性値集約型を切り替え、KV容量不足と重複重みを減らす。

- **2026-04 · [Rethinking Network Topologies for Cost-Effective Mixture-of-Experts LLM Serving](2026-2605.00254-network-topologies-cost-effective-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoE推論の通信・計算・重畳・総所有コストを横断モデル化し、高価なスケールアップ網より3Dフルメッシュ等のスイッチレス網と適度な帯域の方が単位費用当たり性能で優れる条件を体系化した研究。

- **2026-03 · [A Switch-Centric In-Network Architecture for Accelerating LLM Inference in Shared-Memory Network](2026-2603.28239-scin-switch-centric-in-network-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SCINはスイッチ内アクセラレータがGPUメモリを直接読みAll-Reduceを集約・書戻しし、GPU往復を減らす。INT8値と尺度も対応付け、テンソル並列の通信同期を短縮する。

- **2026-01 · [MixServe: An Automatic Distributed Serving System for MoE Models with Hybrid Parallelism Based on Fused Communication Algorithm](2026-2601.08800-mixserve-hybrid-tp-ep-fused-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル形状と階層ネットワーク帯域からTP・DP・EP・PP構成を自動選択し、ノード内の全削減通信とノード間の全対全通信を融合・重畳して、MoE配信のTTFTを最大3.80倍、スループットを最大50.3%改善する。

- **2026-01 · [A Scheduling Framework for Efficient MoE Inference on Edge GPU-NDP Systems](2026-2601.03992-edge-gpu-ndp-moe-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は専門家行列を複数NDPへ分割し、GPU/NDP実行時間を釣り合わせる動的割当と頻出専門家先読みを組み合わせ、エッジMoEの外部転送と装置間負荷偏りを減らす。

### 2年前（2024-11〜2025-10）

- **2025-02 · [MoETuner: Optimized Mixture of Expert Serving with Balanced Expert Placement and Token Routing](2025-2502.06643-moetuner-balanced-expert-placement-token-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  層間のトークン遷移統計を二段階ILPへ入力し、MoEのエキスパート配置を計算負荷とGPU間通信の両方が均衡するよう最適化する。

- **2025-09 · [Expert-as-a-Service: Towards Efficient, Scalable, and Robust Large-scale MoE Serving](2025-2509.17863-expert-as-a-service-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  MoEの専門家を状態のない独立GPUサービスへ分離し、CPU不要のIBGDA一対一通信、動的バッチ、専門家複製で、GPU単位の伸縮・負荷分散・障害迂回を可能にする大規模MoEサービング方式。

- **2025-03 · [Semantic Parallelism: Redefining Efficient MoE Inference via Model-Data Co-Scheduling](2025-2503.04398-semantic-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  トークンと専門家の活性化親和性を事前学習し、専門家配置と要求・トークン配置を協調させてMoEの全対全通信を削減する推論方式。

- **2025-09 · [GRACE-MoE: Grouping and Replication with Locality-Aware Routing for Efficient Distributed MoE Inference](2025-2509.25041-grace-moe-grouping-and-replication-with-locality-aware-routing-for-efficient-distributed-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  共活性に基づく階層専門家配置、動的複製、局所性・負荷認識ルーティング、階層疎通信を組み合わせ、分散MoE推論を最大4.66倍高速化するGRACE-MoE。

- **2025-03 · [Capacity-Aware Inference: Mitigating the Straggler Effect in Mixture of Experts](2025-2503.05066-capacity-aware-inference-mitigating-the-straggler-effect-in-mixture-of-experts.md)**  
  実装：[✓](https://github.com/CASE-Lab-UMD/Capacity-Aware-MoE) ・ リポジトリ内被引用：4  
  専門家並列（専門家 Parallelism; EP）では、平均トークン数が同じでも一部専門家に負荷が集中すると、その専門家を担当するGPUが同期点を支配する。Capacity-Aware Inferenceは各専門家へ容量上限を設け、低ゲートスコアの超過トークンを落とすか、同一GPU上の追加候補専門家へ逃がすことでこのストラグラー効果を抑える。

- **2024-11 · [Communication Compression for Tensor Parallel LLM Inference](2024-2411.09510-communication-compression-for-tensor-parallel-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  テンソル並列の部分活性値を集合通信直前に細粒度量子化し、低帯域8×L4ではLlama2-70BのTTFTを最大約2.08倍改善する一方、高帯域A100では逆効果になる条件も示す。

- **2025-10 · [ElasticMoE: An Efficient Auto Scaling Method for Mixture-of-Experts Models](2025-2510.02613-elasticmoe-an-efficient-auto-scaling-method-for-mixture-of-experts-model.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  垂直スケーリングで既存複製の並列度を変える方式は細粒度だが、プロセス再起動、重み再読込、KVキャッシュ再構築が発生し、短時間のバーストに間に合わない。Ascend NPU上で3種のMoE LLMを評価し、従来方式に対してスケールアップ遅延を最大9倍短縮し、スケール処理中の推論処理量を最大2倍にした。

- **2025-08 · [Accelerating Edge Inference for Distributed MoE Models with Latency-Optimized Expert Placement](2025-2508.12851-dancemoe-latency-optimized-edge-expert-placement.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  活性化頻度とエントロピーに基づく専門家配置と費用認識型移行により、異種エッジMoE推論の遠隔通信と遅延を削減する。

- **2025-05 · [Occult: Optimizing Collaborative Communication across Experts for Accelerated Parallel MoE Training and Inference](2025-2505.13345-occult-collaborative-expert-communication.md)**  
  実装：[✓](https://github.com/UNITES-Lab/Occult) ・ リポジトリ内被引用：1  
  共活性化する専門家を同一GPUへ集約し、再索引付き疎行列積と協調剪定でトークン複製を減らすことで、MoEの全対全通信を削減し学習・推論を1.5倍超高速化する。

### 3年前（2023-11〜2024-10）

- **2024-04 · [Shortcut-connected Expert Parallelism for Accelerating Mixture of Experts](2024-2404.05019-shortcut-connected-expert-parallelism-for-accelerating-mixture-of-expert.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  混合専門家モデル（Mixture of エキスパート; MoE）を複数GPUで実行する専門家並列では、各トークンを選択された専門家のGPUへ送る全対全通信（全対全）が不可欠となる。従来のtop-2 MoEでは、ルーティング、入力整列、全対全送信、専門家計算、全対全返送、出力整列が依存鎖上で続く。

- **2024-10 · [EPS-MoE: Expert Pipeline Scheduler for Cost-Efficient MoE Inference](2024-2410.12247-eps-moe-expert-pipeline-scheduler-for-cost-efficient-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  専門家単位にトークンを水平 分割し、負荷別GEMM選択とSM制限で全対全通信通信を計算へ重畳するMoE向け専門家 パイプライン スケジューラ。

- **2024-08 · [LongVILA: Scaling Long-Context Visual Language Models for Long Videos](2024-2408.10188-longvila-scaling-long-context-visual-language-models-for-long-videos.md)**  
  実装：[✓](https://github.com/NVlabs/VILA) ・ リポジトリ内被引用：5  
  LongVILAは、長時間動画を理解する視覚言語モデル（Vision-Language モデル、VLM）の学習手順と分散実行基盤を同時に設計した研究である。256基のGPUを使うと勾配チェックポイントを使わず約200万トークンの学習文脈を扱え、従来のリング型系列並列に対して2.1〜5.7倍の訓練処理量を得る。

### 4年前（2022-11〜2023-10）

- **2023-03 · [Towards MoE Deployment: Mitigating Inefficiencies in Mixture-of-Expert (MoE) Inference](2023-2303.06182-towards-moe-deployment-mitigating-inefficiencies-in-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  提案する三機構は動的ゲート（動的 Gating）、専門家バッファ（専門家 Buffering）、専門家負荷分散（専門家 読み込み Balancing）である。動的ゲートによる最大スループットは、静的方式比で言語モデル6.21～11.23倍、機械翻訳エンコーダ5.75～10.98倍、デコーダ2.58～5.71倍へ改善した。

### 5年前（2021-11〜2022-10）

- **2022-06 · [Tutel: Adaptive Mixture-of-Experts at Scale](2022-2206.03382-tutel-adaptive-mixture-of-experts-at-scale.md)**  
  実装：[✓](https://github.com/microsoft/tutel) ・ リポジトリ内被引用：21  
  Tutelは、混合専門家モデル（Mixture-of-Experts; MoE）で反復ごとに変わる専門家負荷へ実行系を追従させる分散実行基盤である。固定の並列化方式や固定の通信・計算パイプラインは、この変動に対して一つの実行形態しか使えず、通信時間または専門家計算時間のどちらかを無駄にしやすい。

- **2022-10 · [Accelerating Distributed MoE Training and Inference with Lina](2022-2210.17223-accelerating-distributed-moe-training-and-inference-with-lina.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  Linaは、分散した混合専門家モデル（Mixture of エキスパート、MoE）の通信を、学習と推論で異なる原因に分解して高速化するシステムである。論文の事前計測では、全対全通信が処理段階時間の平均34.1%、ある層の順伝播時間の74.9%を占め、通信中のGPU演算器利用率は平均3.7%にとどまった。

### 6年前（2020-11〜2021-10）

- **2021-01 · [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](2021-2101.03961-switch-transformers-scaling-to-trillion-parameter-models-with-simple-and.md)**  
  実装：[✓](https://github.com/tensorflow/mesh/blob/master/mesh_tensorflow/transformer/moe.py) ・ リポジトリ内被引用：89  
  論文は、専門家容量、容量超過トークンの扱い、負荷分散補助損失、ルータだけを高精度で計算する選択的精度、初期値スケールの縮小、専門家専用ドロップアウト、データ・モデル・専門家並列の組合せまで含め、巨大な疎モデルを実際に安定学習するための設計をまとめている。
<!-- survey:auto:end -->
