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
  小型予測器で次層のエキスパートを必要そうな順に並べ、対象層へ到達するまでの残り時間と実測ストレージ帯域から「間に合う数」だけを先読みして、実行時にエキスパートが準備済みである割合を高める。

- **2026-03 · [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/axonn-ai/yalis/tree/offload_prefetch) ・ リポジトリ内被引用：1  
  現在層のhidden stateから次層で使うエキスパートを予測し、重み転送だけでなくエキスパート FFN計算まで先に実行する。native ルータと一致すれば先行結果を再利用し、外れれば正しいエキスパートを読み直して再計算する無損失方式。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Cache-Aware Joint Router Adaptation for Memory-Efficient MoE Inference](2026-2609.04895-cache-aware-joint-router-adaptation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この研究の中心は「次に使うエキスパートを何でも先読みする」ことではない。MoE本来のTop-K実行規則は残したまま、GPUに今あるエキスパートのうち何を残すべきかをモデル側に学ばせ、必要な場合だけ次層のエキスパートを限定的に先読みする。

- **2026-08 · [SPICE: Speculative Prefetching with Low-Rank Expert Surrogates and Heterogeneous Orchestration for MoE Inference Acceleration](2026-2608.21240-spice-speculative-prefetching-low-rank-expert-surrogates-heterogeneous-orchestration.md)**  
  実装：[✓](https://anonymous.4open.science/r/SPICE) ・ リポジトリ内被引用：0  
  数層先で使う専門家を予測して先読みし、予測外れを「小型近似で済ませるもの」「CPU上で正確に計算するもの」「重みをGPUへ送って正確に計算するもの」に分けることで、MoE オフロードのPCIe待ちを減らす。

- **2026-03 · [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパート 重みを複数の小さな行列単位へ分け、複数の前層が共通して必要と予測したエキスパート部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。

- **2026-03 · [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  次層で使うエキスパートを予測してGPUへ先読みし、予測が外れても正しいエキスパートを読み直さず、準備済みエキスパートをそのまま使うことでオフロード待ちをなくす近似MoE方式。

- **2026-03 · [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  過去に似た入力文があればその時のエキスパート利用履歴を再利用し、似た履歴がなければ学習済み予測器で全層のエキスパート候補を予測して、CPUからGPUへの先読みを早く始める。

- **2025-12 · [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  常設エキスパート キャッシュを持たず、軽量化した別モデルで数層先のエキスパートを予測し、複数worker GPUへ必要エキスパートだけを実行直前に読み込む。予測が外れた場合は元の ルータの正しいエキスパートを追加ロードする分散edge MoE方式。

### 1年以上前

- **2023-08 · [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md)**  
  実装：[✓](https://github.com/ranggihwang/Pregated_MoE) ・ リポジトリ内被引用：38  
  次の層のルーティング判定を1ブロック前で行い、必要エキスパートを早めに確定してCPU→GPU転送を現在ブロックの計算と重ねることで、エキスパート重み待ちを減らすMoEオフロード方式。

- **2024-10 · [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md)**  
  実装：[✓](https://github.com/promoe-opensource/promoe) ・ リポジトリ内被引用：18  
  ProMoEは、GPUに入らないMoE 専門家をCPU DRAMへ置くとき、キャッシュ 未ヒットが起きてから専門家を読むのではなく、数層先で必要になりそうな専門家を先にGPUへ運び、誤予測だった転送は細粒度で止め、すでに到着した専門家から先に計算する方式である。

- **2024-12 · [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md)**  
  実装：[✓](https://github.com/ecolab-nus/DAOP) ・ リポジトリ内被引用：12  
  プリフィルでそのリクエストがよく使うエキスパートを把握してGPU配置を調整し、デコードでは次層でCPU側エキスパートが必要かを1 ブロック早く予測してCPU計算を先に始めることで、単一GPUのMoE推論を高速化する。

- **2025-02 · [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  現在層のルータ入力から次層で使うエキスパートを予測し、浅い層には多めのエキスパートをGPUへ置き、深い層は先読みで補う。さらに利用頻度の低いエキスパートだけを強く量子化してedge環境の転送待ちとメモリ使用量を減らす。

- **2025-09 · [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  層ごとの小型予測器で将来使うエキスパートを見積もり、CPU→GPU先読み・必要時転送・CPUでのエキスパート実行を同じ計画で調整して、複数バッチがPCIe帯域を奪い合う時の待ち時間を減らす。

- **2023-10 · [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md)**  
  実装：[✓](https://github.com/timlee0212/SiDA-MoE) ・ リポジトリ内被引用：4  
  小型LSTMで各トークンが使うエキスパートを先に予測し、予測したエキスパートだけをCPUからGPUへ読み込む。予測結果そのものをルーティングに使うため、外れると元モデルと異なるエキスパートを実行し得る近似方式。
<!-- survey:auto:end -->
