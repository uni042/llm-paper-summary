# Expert Prefetch

MoEで次に使われるexpertを**routing結果が確定する前に予測して先にGPUへ読み込む**ことで、CPU / storageからの重み転送待ちを隠す研究をまとめる。予測器、過去のrouting履歴、前のlayerの状態などを使って将来のexpert需要を見積もり、現在の計算と次の転送を重ねるのが基本形となる。

一部の手法はexpertを小さく分けたり、予測したexpertをそのまま使うなどして、予測ミス時の追加I/Oまで減らす。将来需要の予測をcache保持判断に使い、必ずしも先読み転送しない方式も含む。最終目的が推論高速化であるため、予測器自体に学習が必要でもこの系統に分類する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-06 · [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md)**  
  実装：[✓](https://github.com/wei390/SpecPrefetch) ・ リポジトリ内被引用：1  
  SpecPrefetchは次層専門家を必要度順に並べ、到達までの時間と実測ストレージ帯域から間に合う数だけ先読みして、準備不足による実機NVMe転送待ちを減らす。

- **2026-03 · [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/axonn-ai/yalis/tree/offload_prefetch) ・ リポジトリ内被引用：1  
  Speculating Expertsは次層の専門家を予測し、重み転送だけでなくFFN計算まで現在層と並行して先行実行する。元ルータと一致した結果だけ再利用し、外れれば正しく再計算する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Cache-Aware Joint Router Adaptation for Memory-Efficient MoE Inference](2026-2609.04895-cache-aware-joint-router-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究はMoEルータを追加学習し、GPU内キャッシュの再利用を促す時間・時空間ルータを作る。必要時だけ限定的に先読みし、専門家重みの転送量と待ち時間を減らす。

- **2026-08 · [SPICE: Speculative Prefetching with Low-Rank Expert Surrogates and Heterogeneous Orchestration for MoE Inference Acceleration](2026-2608.21240-spice-speculative-prefetching-low-rank-expert-surrogates-heterogeneous-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/SPICE) ・ リポジトリ内被引用：0  
  SPICEは予測した専門家を低ランク近似・CPU正確計算・GPU正確計算へ振り分け、低ランク代替で予測外れの転送を避けつつ、MoEオフロードのPCIe待ちを減らす。

- **2026-03 · [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FIRM-MoEは専門家FFNを射影行列単位へ分解し、複数前層の予測が一致した部分を優先して先読みする。VRAM容量とPCIe帯域に合わせて先読み距離・量を調整する。

- **2026-03 · [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CommitMoEは次層専門家を先読みして実行対象に確定し、予測が外れても正しい重みを待たず準備済み専門家へ出力重みを再配分し、オフロード待ちをなくす近似方式。

- **2026-03 · [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CasMoEは類似入力の過去ルーティング履歴を検索し、見つからない場合だけ学習予測器で全層の専門家を予測して、CPUからGPUへの先読みを早く始める。

- **2025-12 · [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OD-MoEは常設キャッシュを持たず、軽量化モデルで数層先の専門家を予測して複数GPUへ実行直前に読み込む。予測が外れれば元ルータの専門家を追加ロードする分散エッジ方式である。

### 2年前（2024-10〜2025-09）

- **2024-10 · [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md)**  
  実装：[✓](https://github.com/promoe-opensource/promoe) ・ リポジトリ内被引用：18  
  ProMoEは数層先のルーティングから必要な専門家を予測し、CPUからGPUへ分割転送する。誤予測を止め、到着済みから実行して、重み転送待ちを計算の裏に隠す。

- **2024-12 · [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md)**  
  実装：[✓](https://github.com/ecolab-nus/DAOP) ・ リポジトリ内被引用：12  
  DAOPはプリフィルでリクエスト固有の専門家をGPU配置へ反映し、デコードでは次層のCPU専門家を1ブロック前に予測・計算して、単一GPUの転送待ちを減らす。

- **2025-02 · [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  Fateは隣接層のルータ入力から次層専門家を予測し、層ごとのGPU常駐数と利用履歴を調整する。低頻度専門家の低ビット化も組み合わせ、エッジMoEの転送と容量を抑える。

- **2025-09 · [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LayerScopeは将来専門家の先読み、CPU直接計算、必要時転送を複数バッチで一体計画し、PCIe帯域を先読みで使い切って緊急転送を遅らせる問題を抑える。

### 3年前（2023-10〜2024-09）

- **2023-10 · [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md)**  
  実装：[✓](https://github.com/timlee0212/SiDA-MoE) ・ リポジトリ内被引用：4  
  SiDA-MoEは小型LSTMで各トークンの専門家を先に予測し、予測した重みだけをCPUからGPUへ読む。予測結果をルーティングにも使うため、外れれば品質が変わる近似方式である。

### 4年前（2022-10〜2023-09）

- **2023-08 · [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md)**  
  実装：[✓](https://github.com/ranggihwang/Pregated_MoE) ・ リポジトリ内被引用：41  
  Pre-gated MoEは次層のルーティング判定を1ブロック前へ移し、必要な専門家重みのCPUからGPUへの転送を現在ブロックの計算と重ねて、オフロード待ちを減らす。
<!-- survey:auto:end -->
