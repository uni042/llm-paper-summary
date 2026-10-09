# Expert Prefetch

MoEで次に使われるexpertを**routing結果が確定する前に予測して先にGPUへ読み込む**ことで、CPU / storageからの重み転送待ちを隠す研究をまとめる。予測器、過去のrouting履歴、前のlayerの状態などを使って将来のexpert需要を見積もり、現在の計算と次の転送を重ねるのが基本形となる。

一部の手法はexpertを小さく分けたり、予測したexpertをそのまま使うなどして、予測ミス時の追加I/Oまで減らす。将来需要の予測をcache保持判断に使い、必ずしも先読み転送しない方式も含む。最終目的が推論高速化であるため、予測器自体に学習が必要でもこの系統に分類する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（15本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-06 · [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md)**  
  実装：[✓](https://github.com/wei390/SpecPrefetch) ・ リポジトリ内被引用：1  
  SpecPrefetchは、混合専門家モデル（Mixture of エキスパート、MoE）の重みをGPUにすべて置けない環境で、必要な専門家をストレージから読み込む待ち時間を短縮する研究である。提案方式は、一つ前の層の状態から次層で使いそうな専門家を軽量な予測器で推定し、現在層の計算と専門家の非同期転送を重ねる。

- **2026-03 · [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/axonn-ai/yalis/tree/offload_prefetch) ・ リポジトリ内被引用：1  
  論文のA6000でのQwen3-30B-A3B評価では、要求時に専門家を読み込む方式のTPOTの約84〜88%を転送が占める。

- **2026-03 · [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FIRM-MoEは、専門家混合（Mixture-of-Experts、MoE）型の大規模言語モデルをGPUメモリの小さい端末で推論するとき、CPUからGPUへ専門家重みを運ぶ待ち時間を削減する仕組みである。従来の専門家先読みは、将来選択される専門家を予測して重み全体を先に転送する。

- **2026-03 · [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  不要な専門家をCPU側に退避し、必要時だけGPUへ読み込む方式は容量を節約するが、CPU・GPU間の転送が推論遅延を支配する。

- **2025-12 · [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  OD-MoEは常設キャッシュを持たず、軽量化モデルで数層先の専門家を予測して複数GPUへ実行直前に読み込む。予測が外れれば元ルータの専門家を追加ロードする分散エッジ方式である。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Cache-Aware Joint Router Adaptation for Memory-Efficient MoE Inference](2026-2609.04895-cache-aware-joint-router-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究はMoEルータを追加学習し、GPU内キャッシュの再利用を促す時間・時空間ルータを作る。必要時だけ限定的に先読みし、専門家重みの転送量と待ち時間を減らす。

- **2026-08 · [SPICE: Speculative Prefetching with Low-Rank Expert Surrogates and Heterogeneous Orchestration for MoE Inference Acceleration](2026-2608.21240-spice-speculative-prefetching-low-rank-expert-surrogates-heterogeneous-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/SPICE) ・ リポジトリ内被引用：0  
  SPICEは予測した専門家を低ランク近似・CPU正確計算・GPU正確計算へ振り分け、低ランク代替で予測外れの転送を避けつつ、MoEオフロードのPCIe待ちを減らす。

- **2026-03 · [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし専門家の総重量は大きく、GPUにすべて常駐させると容量不足になりやすい。CPU側へ非活性専門家を退避し、必要なものだけGPUへ移せば容量は節約できるが、専門家が決まってから転送するとPCIeの待機が推論時間へ直接加算される。

### 2年前（2024-11〜2025-10）

- **2024-12 · [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md)**  
  実装：[✓](https://github.com/ecolab-nus/DAOP) ・ リポジトリ内被引用：17  
  しかし、GPUメモリが限られると専門家の重みをすべて常駐させられない。従来のCPU専門家実行方式Fiddlerに対し、DAOPは二つの最適化を加える。RTX A6000 48GBと18コアCPUの実機評価では、Fiddler比で専門家キャッシュ比率を変えた場合の平均生成速度改善が35.4%、一部条件では40.4%である。

- **2025-02 · [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  11GBのGPUメモリしか持たないRTX 1080Tiでは全専門家を常駐させられず、CPUメモリから必要な専門家を都度転送すると待機時間が発生する。加えて、先読みの外れやすい浅い層へGPUキャッシュを重点配分し、最近使った専門家と繰り返し使う専門家を適応的に残す。

- **2025-09 · [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  将来必要になる専門家を予測しても、その先読みがPCIe帯域を占有すると、現在必要な専門家の緊急転送が遅れる。LayerScopeは、先読み、必要時転送、CPUでの直接計算を複数バッチ・複数層の時間軸で一体的に計画する。

- **2025-10 · [ExpertFlow: Adaptive Expert Scheduling and Memory Coordination for Efficient MoE Inference](2025-2510.26730-expertflow-adaptive-prefetch.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  固定先読み幅を帯域・入力・待機フィードバックで動的化し、予測器・二段LRU・キャッシュ認識ルーティングを協調させてMoEエキスパート転送待ちを隠蔽する実行時システム。

### 3年前（2023-11〜2024-10）

- **2024-10 · [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md)**  
  実装：[✓](https://github.com/promoe-opensource/promoe) ・ リポジトリ内被引用：35  
  ProMoEは数層先のルーティングから必要な専門家を予測し、CPUからGPUへ分割転送する。誤予測を止め、到着済みから実行して、重み転送待ちを計算の裏に隠す。

### 4年前（2022-11〜2023-10）

- **2023-08 · [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md)**  
  実装：[✓](https://github.com/ranggihwang/Pregated_MoE) ・ リポジトリ内被引用：86  
  Pre-gated MoEは次層のルーティング判定を1ブロック前へ移し、必要な専門家重みのCPUからGPUへの転送を現在ブロックの計算と重ねて、オフロード待ちを減らす。

- **2023-10 · [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md)**  
  実装：[✓](https://github.com/timlee0212/SiDA-MoE) ・ リポジトリ内被引用：7  
  SiDA-MoEは小型LSTMで各トークンの専門家を先に予測し、予測した重みだけをCPUからGPUへ読む。予測結果をルーティングにも使うため、外れれば品質が変わる近似方式である。
<!-- survey:auto:end -->
