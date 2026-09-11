# MoE並列化・通信

この系統では、混合専門家モデル（Mixture of Experts; MoE）の専門家配置、並列化、チップ間・ノード間通信、負荷分散を扱う推論システム研究を整理する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（11本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Epoch: Compiling Diffusion Blocks for Sparse MoE Serving](2026-2609.09748-epoch-diffusion-blocks-sparse-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散MoEの生成ブロックを再利用単位にし、候補エキスパート集合、確定トークンの期限付き出力、エキスパート並列の通信データをブロック内で疎化して、8基H100上で最良比較対象より最大2.7倍高速化するサービング方式。

- **2026-08 · [HetRoute: Heterogeneous and Cost-aware Collaborative Routing Framework for Distributed Edge MoE Inference](2026-2608.00577-hetroute-collaborative-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  地理的に分散した異種エッジサーバで混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、各トークンが選んだ複数の専門家をどのサーバへ送るかで、ネットワーク転送、GPUとCPU間の専門家読み込み、GPU計算待ち、量子化による品質損失が同時に絡む。

- **2026-08 · [FreeBalance: Pre-Routing Online Moe Load Balancing via Residual Workload Prediction](2026-2608.14205-freebalance-prerouting-online-load-balancing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート; MoE）のオンライン負荷分散では、通常は現在層のルータが専門家選択を終えてから専門家交換を決めるため、重み移動が推論クリティカルパスに残る。FreeBalanceは残差接続により隣接層の隠れ表現が近いことを利用し、現在層のルータを前層出力へ先行適用して専門家負荷を予測する。

- **2026-08 · [AirMoE: Realizing Over-the-Air Distributed Mixture-of-Experts Inference at the Wireless Edge](2026-2608.22932-airmoe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoE専門家の無線分散実行で、複数端末の専門家出力を空中計算で同時集約し、層感度を考慮した電力制御と専門家配置によって無線歪みによる推論精度低下を抑える。

- **2026-07 · [Mixture-of-Experts Serving](2026-2607.17880-mixture-of-experts-serving-online-algorithms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート; MoE）で専門家需要が時間変動する状況を、各専門家へ何台の追加GPUを割り当てるかというオンライン資源配置問題として定式化した理論研究。各専門家には最低1台を置き、余剰k台を動的に配る。

- **2026-06 · [Coordinated Scheduling for MoE LLM Serving](2026-2606.15177-gimbal-coordinated-moe-serving-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート; MoE）のサービングでは、フロントエンドのデータ並列エンジンへの要求振り分けと、バックエンドの専門家配置を別々に最適化すると、入力長やKVキャッシュ使用量の偏りと専門家ホットスポットが互いに増幅される。

- **2026-05 · [SiDP: Memory-Efficient Data Parallelism for Offline LLM Inference](2026-2605.28095-sidp-memory-efficient-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインLLM推論では大きなバッチを維持するとGPU演算効率が上がるが、通常のデータ並列は各GPUにモデル重みを完全複製するため、KVキャッシュに使えるHBMが減ってバッチを増やせない。SiDPはフィードフォワードネットワーク重みをデータ並列グループ内で一度だけ保持する分散重みプールへ変え、非所有GPUが必要時に共有する。

- **2026-04 · [DWDP: Distributed Weight Data Parallelism for High-Performance LLM Inference on NVL72](2026-2604.01621-dwdp-distributed-weight-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模な混合専門家モデル（Mixture of エキスパート; MoE）を複数GPUで推論すると、従来の専門家並列では各層の全対全通信と同期のため、入力長や専門家選択が偏ったとき速いGPUまで遅いGPUを待つ。DWDPは注意機構の重みを各GPUへ複製し、MoEの専門家重みだけを同一NVLinkドメイン内のGPUへ分散配置する。

- **2026-03 · [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低バッチのオンデバイスMoEでは、専門家ごとの活性化トークン数が長い裾を持ち、オンチップ容量不足からDDRへ重みを逃がすため、重み読込・チップレット間負荷不均衡・重複保持が同時にボトルネックになる。

- **2026-03 · [A Switch-Centric In-Network Architecture for Accelerating LLM Inference in Shared-Memory Network](2026-2603.28239-scin-switch-centric-in-network-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テンソル並列推論では各層の注意機構と全結合ネットワーク後に全GPUの部分結果を集約するAll-Reduceが入り、低遅延・低同時実行数では計算で通信を隠しにくい。

- **2026-01 · [A Scheduling Framework for Efficient MoE Inference on Edge GPU-NDP Systems](2026-2601.03992-edge-gpu-ndp-moe-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エッジ端末で混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、全専門家の重みが民生GPUのメモリへ収まらず、外部メモリからの転送が推論を支配しやすい。

### 1年以上前

該当なし。
<!-- survey:auto:end -->
