# MoE並列化・通信

この系統では、混合専門家モデル（Mixture of Experts; MoE）の専門家配置、並列化、チップ間・ノード間通信、負荷分散を扱う推論システム研究を整理する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（11本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

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

- **2026-06 · [Coordinated Scheduling for MoE LLM Serving](2026-2606.15177-gimbal-coordinated-moe-serving-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Gimbalは要求の残りプリフィル量・待機量・KV使用量と専門家負荷を同時に見て要求振り分けと専門家配置を協調し、MoEサービングのキュー偏りとホットスポットを減らす。

- **2026-05 · [SiDP: Memory-Efficient Data Parallelism for Offline LLM Inference](2026-2605.28095-sidp-memory-efficient-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SiDPはデータ並列GPU間でFFN重みを一度だけ保持する共有プールを作り、バッチ規模に応じて重み先読み型と活性値集約型を切り替え、KV容量不足と重複重みを減らす。

- **2026-04 · [DWDP: Distributed Weight Data Parallelism for High-Performance LLM Inference on NVL72](2026-2604.01621-dwdp-distributed-weight-data-parallelism.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DWDPは注意重みを各GPUへ複製し、MoE専門家重みだけをNVLinkドメイン内で分散する。必要重みを非同期先読みして全対全通信とGPU間同期を減らす。

- **2026-03 · [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパートストリーミングは専門家重みをチップレット間の細粒度マイクロスライスへ分け、高負荷・低負荷専門家を組み合わせてDDR読込、チップレット転送、計算を重ね、オンチップ容量不足を緩和する。

- **2026-03 · [A Switch-Centric In-Network Architecture for Accelerating LLM Inference in Shared-Memory Network](2026-2603.28239-scin-switch-centric-in-network-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SCINはスイッチ内アクセラレータがGPUメモリを直接読みAll-Reduceを集約・書戻しし、GPU往復を減らす。INT8値と尺度も対応付け、テンソル並列の通信同期を短縮する。

- **2026-01 · [A Scheduling Framework for Efficient MoE Inference on Edge GPU-NDP Systems](2026-2601.03992-edge-gpu-ndp-moe-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は専門家行列を複数NDPへ分割し、GPU/NDP実行時間を釣り合わせる動的割当と頻出専門家先読みを組み合わせ、エッジMoEの外部転送と装置間負荷偏りを減らす。
<!-- survey:auto:end -->
