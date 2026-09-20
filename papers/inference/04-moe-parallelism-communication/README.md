# MoE並列化・通信

この系統では、混合専門家モデル（Mixture of Experts; MoE）の専門家配置、並列化、チップ間・ノード間通信、負荷分散を扱う推論システム研究を整理する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（23本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-07 · [Fine-grained Computation-Communication Overlap via Tile-level Signaling and Scheduling for Mixture-of-Experts](2026-2607.19539-tile-level-compute-communication-overlap-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  遠隔GPUへ返すMoE出力を先にタイル計算し、完成した行帯を専用通信カーネルが即時転送することで、第2の全対全通信の大半を専門家計算中へ隠し、4基A100でMoE層を最大2.74倍高速化する。

- **2026-07 · [OrderMoE: An expert similarity driven distributed edge MoE inference](2026-2607.17154-ordermoe-expert-similarity-distributed-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ルータ応答から専門家の機能類似性を推定し、類似専門家をエッジ間へ分散配置して、品質予算内なら遠隔の正確な専門家を局所類似専門家で代替し通信と遅延を削減する。

- **2026-05 · [Surviving Partial Rank Failures in Wide Expert-Parallel MoE Inference](2026-2605.10670-surviving-partial-rank-failures-wide-ep-moe.md)**  
  実装：[✓](https://github.com/kvcache-ai/Mooncake) ・ リポジトリ内被引用：1  
  専門家並列の部分ランク障害を、通信相手・専門家被覆・CUDAグラフ可視経路の個別修復で全体再起動なしに復旧するEEPを提案する。

- **2026-04 · [Scaling Multi-Node Mixture-of-Experts Inference Using Expert Activation Patterns](2026-2604.23150-scaling-multinode-moe-expert-activation-patterns.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  プリフィル時の専門家活性から似た要求を小バッチ化し、要求群で共発火する専門家を同じノードへ置くことで、マルチノードMoEの全対全通信を削減する。

### 直近12か月・未被引用（2025-10〜2026-09）

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

- **2026-04 · [DWDP: Distributed Weight Data Parallelism for High-Performance LLM Inference on NVL72](2026-2604.01621-dwdp-distributed-weight-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DWDPは注意重みを各GPUへ複製し、MoE専門家重みだけをNVLinkドメイン内で分散する。必要重みを非同期先読みして全対全通信とGPU間同期を減らす。

- **2026-03 · [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパートストリーミングは専門家重みをチップレット間の細粒度マイクロスライスへ分け、高負荷・低負荷専門家を組み合わせてDDR読込、チップレット転送、計算を重ね、オンチップ容量不足を緩和する。

- **2026-03 · [A Switch-Centric In-Network Architecture for Accelerating LLM Inference in Shared-Memory Network](2026-2603.28239-scin-switch-centric-in-network-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SCINはスイッチ内アクセラレータがGPUメモリを直接読みAll-Reduceを集約・書戻しし、GPU往復を減らす。INT8値と尺度も対応付け、テンソル並列の通信同期を短縮する。

- **2026-01 · [MixServe: An Automatic Distributed Serving System for MoE Models with Hybrid Parallelism Based on Fused Communication Algorithm](2026-2601.08800-mixserve-hybrid-tp-ep-fused-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル形状と階層ネットワーク帯域からTP・DP・EP・PP構成を自動選択し、ノード内の全削減通信とノード間の全対全通信を融合・重畳して、MoE配信のTTFTを最大3.80倍、スループットを最大50.3%改善する。

- **2026-01 · [A Scheduling Framework for Efficient MoE Inference on Edge GPU-NDP Systems](2026-2601.03992-edge-gpu-ndp-moe-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は専門家行列を複数NDPへ分割し、GPU/NDP実行時間を釣り合わせる動的割当と頻出専門家先読みを組み合わせ、エッジMoEの外部転送と装置間負荷偏りを減らす。

### 2年前（2024-10〜2025-09）

- **2025-02 · [MoETuner: Optimized Mixture of Expert Serving with Balanced Expert Placement and Token Routing](2025-2502.06643-moetuner-balanced-expert-placement-token-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  層間のトークン遷移統計を二段階ILPへ入力し、MoEのエキスパート配置を計算負荷とGPU間通信の両方が均衡するよう最適化する。

- **2025-09 · [Expert-as-a-Service: Towards Efficient, Scalable, and Robust Large-scale MoE Serving](2025-2509.17863-expert-as-a-service-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  MoEの専門家を状態のない独立GPUサービスへ分離し、CPU不要のIBGDA一対一通信、動的バッチ、専門家複製で、GPU単位の伸縮・負荷分散・障害迂回を可能にする大規模MoEサービング方式。

- **2025-03 · [Semantic Parallelism: Redefining Efficient MoE Inference via Model-Data Co-Scheduling](2025-2503.04398-semantic-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  トークンと専門家の活性化親和性を事前学習し、専門家配置と要求・トークン配置を協調させてMoEの全対全通信を削減する推論方式。

- **2025-08 · [Accelerating Edge Inference for Distributed MoE Models with Latency-Optimized Expert Placement](2025-2508.12851-dancemoe-latency-optimized-edge-expert-placement.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  活性化頻度とエントロピーに基づく専門家配置と費用認識型移行により、異種エッジMoE推論の遠隔通信と遅延を削減する。
<!-- survey:auto:end -->
