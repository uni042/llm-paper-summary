# Expert Prefetch

MoEで次に使われるexpertを**routing結果が確定する前に予測して先にGPUへ読み込む**ことで、CPU / storageからの重み転送待ちを隠す研究をまとめる。予測器、過去のrouting履歴、前のlayerの状態などを使って将来のexpert需要を見積もり、現在の計算と次の転送を重ねるのが基本形となる。

一部の手法はexpertを小さく分けたり、予測したexpertをそのまま使うなどして、予測ミス時の追加I/Oまで減らす。将来需要の予測をcache保持判断に使い、必ずしも先読み転送しない方式も含む。最終目的が推論高速化であるため、予測器自体に学習が必要でもこの系統に分類する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-06 · [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md)**  
  実装：[✓](https://github.com/wei390/SpecPrefetch) ・ リポジトリ内被引用：1  
  SpecPrefetchは、エキスパート IDを高精度に当てるだけでなく、対象層へ到達するまでに実際に何個のエキスパート 転送を完了できるかを先読み 方針へ入れる方式である。

- **2026-03 · [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/axonn-ai/yalis/tree/offload_prefetch) ・ リポジトリ内被引用：1  
  この論文はエキスパート 先読みを一段進め、次層のエキスパート 重みを先に送るだけでなく、そのエキスパート計算自体も先に実行する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Cache-Aware Joint Router Adaptation for Memory-Efficient MoE Inference](2026-2609.04895-cache-aware-joint-router-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家混合（Mixture-of-エキスパート; MoE）モデルは、1 トークンを処理するとき全エキスパートを計算するのではなく、ルータが選んだ少数エキスパートだけを実行する。

- **2026-08 · [SPICE: Speculative Prefetching with Low-Rank Expert Surrogates and Heterogeneous Orchestration for MoE Inference Acceleration](2026-2608.21240-spice-speculative-prefetching-low-rank-expert-surrogates-heterogeneous-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/SPICE) ・ リポジトリ内被引用：0  
  数層先で使う専門家を予測して先読みし、予測外れを「小型近似で済ませるもの」「CPU上で正確に計算するもの」「重みをGPUへ送って正確に計算するもの」に分けることで、MoE オフロードのPCIe待ちを減らす。

- **2026-03 · [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FIRM-MoEは、通常のエキスパート オフロードがエキスパート全体を一つの転送単位として扱うため、必要のない重みまでまとめて運びやすい点を問題にする。

- **2026-03 · [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CommitMoEは、エキスパート 先読みで大きな待ち時間になるprediction ミス時の追加読み込みそのものを行わない。

- **2026-03 · [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CasMoEは、エキスパート 先読みの予測方法を1つに固定せず、過去ルーティング パターンの検索と学習型予測器を段階的に使い分ける。

- **2025-12 · [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OD-MoEは、GPUへhot エキスパートを固定常駐する通常のキャッシュ方式をやめ、必要エキスパートを実行直前だけworker GPUへ載せ、計算後すぐ解放する設計である。

### 1年以上前

- **2023-08 · [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md)**  
  実装：[✓](https://github.com/ranggihwang/Pregated_MoE) ・ リポジトリ内被引用：38  
  Pre-gated MoEは、GPUへ全エキスパートを常駐できないMoEで、ルータ結果が出るまで次エキスパートの重み転送を始められないという逐次依存を壊す手法である。

- **2024-10 · [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md)**  
  実装：[✓](https://github.com/promoe-opensource/promoe) ・ リポジトリ内被引用：18  
  MoE（Mixture-of-専門家）では各トークンが全専門家を使うわけではなく、層ごとに一部だけを選ぶ。

- **2024-12 · [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md)**  
  実装：[✓](https://github.com/ecolab-nus/DAOP) ・ リポジトリ内被引用：12  
  DAOPは、GPUにないエキスパートを毎回GPUへ転送する代わりに、CPUをエキスパート実行器として使い、次層のCPU エキスパート計算を1 ブロック早く始める方式である。

- **2025-02 · [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  Fateは、別のpredictor networkを追加せず、隣接層のルータ入力が似ているという性質を使って次層 エキスパートを予測するedge向けMoE オフロード方式である。

- **2025-09 · [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  LayerScopeは、multi-バッチ MoEでは先読み転送を増やし過ぎるとPCIe帯域を使い切り、本当に必要になったエキスパートの緊急転送まで遅くなるという問題を扱う。

- **2023-10 · [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md)**  
  実装：[✓](https://github.com/timlee0212/SiDA-MoE) ・ リポジトリ内被引用：4  
  SiDA-MoEは、Switch Transformerの大部分を占めるエキスパート重みをCPU DRAMへ置き、次のバッチが使うエキスパートを小型LSTMで先に予測してGPUへ載せる推論システムである。
<!-- survey:auto:end -->
