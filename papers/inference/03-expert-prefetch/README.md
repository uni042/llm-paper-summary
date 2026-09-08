# Expert Prefetch

MoEで次に使われるexpertを**routing結果が確定する前に予測して先にGPUへ読み込む**ことで、CPU / storageからの重み転送待ちを隠す研究をまとめる。予測器、過去のrouting履歴、前のlayerの状態などを使って将来のexpert需要を見積もり、現在の計算と次の転送を重ねるのが基本形となる。

一部の手法はexpertを小さく分けたり、予測したexpertをそのまま使うなどして、予測ミス時の追加I/Oまで減らす。将来需要の予測をcache保持判断に使い、必ずしも先読み転送しない方式も含む。最終目的が推論高速化であるため、予測器自体に学習が必要でもこの系統に分類する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

| 論文 | 一文要約 |
|---|---|
| [Cache-Aware Joint Router Adaptation for Memory-Efficient MoE Inference](2026-2609.04895-cache-aware-joint-router-adaptation.md) | MoEのnative routingを保ったまま、次tokenで再利用するexpertと次layerで必要になるexpertのcache優先度をpost-trainingで学習し、GPUに載らないexpert weightの転送回数を減らす。 |
| [SPICE: Speculative Prefetching with Low-Rank Expert Surrogates and Heterogeneous Orchestration for MoE Inference Acceleration](2026-2608.21240-spice-speculative-prefetching-low-rank-expert-surrogates-heterogeneous-orchestration.md) | 数layer先で使うMoE expertを予測してCPU DRAMからGPUへ先読みし、予測外れのうち重要度が低いexpertは常駐shared expert＋小型補正で近似し、正確な計算が必要な残りはPCIe混雑に応じてCPU実行かGPUへのweight転送へ振り分けることで、expert待ちを減らす。 |
| [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md) | 小型predictorで次layerのexpertを必要そうな順に並べ、対象layerへ到達するまでの残り時間と実測storage帯域から『間に合う数』だけを先読みして、実行時にexpertが準備済みである割合を高める。 |
| [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md) | 過去に似たpromptがあればその時のexpert利用履歴を再利用し、似た履歴がなければ学習済みpredictorで全layerのexpert候補を予測して、CPUからGPUへの先読みを早く始める。 |
| [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md) | 次layerで使うexpertを予測してGPUへ先読みし、予測が外れても正しいexpertを読み直さず、準備済みexpertをそのまま使うことでoffload待ちをなくす近似MoE方式。 |
| [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md) | expert weightを複数の小さな行列単位へ分け、複数の前layerが共通して必要と予測したexpert部分を優先して先読みし、VRAMとPCIe帯域に合わせて先読み量を変えるMoE推論方式。 |
| [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md) | 現在layerのhidden stateから次layerで使うexpertを予測し、weight転送だけでなくexpert FFN計算まで先に実行する。native routerと一致すれば先行結果を再利用し、外れれば正しいexpertを読み直して再計算するlossless方式。 |
| [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md) | 常設expert cacheを持たず、軽量化した別modelで数layer先のexpertを予測し、複数worker GPUへ必要expertだけを実行直前に読み込む。予測が外れた場合はnative routerの正しいexpertを追加ロードする分散edge MoE方式。 |
| [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md) | layerごとの小型予測器で将来使うexpertを見積もり、CPU→GPU先読み・必要時転送・CPUでのexpert実行を同じ計画で調整して、複数batchがPCIe帯域を奪い合う時の待ち時間を減らす。 |
| [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md) | 現在layerのrouter入力から次layerで使うexpertを予測し、浅いlayerには多めのexpertをGPUへ置き、深いlayerは先読みで補う。さらに利用頻度の低いexpertだけを強く量子化してedge環境の転送待ちとmemory使用量を減らす。 |
| [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md) | prefillでそのrequestがよく使うexpertを把握してGPU配置を調整し、decodeでは次layerでCPU側expertが必要かを1 block早く予測してCPU計算を先に始めることで、単一GPUのMoE推論を高速化する。 |
| [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md) | 数layer先で使うexpertを予測してCPUからGPUへ先読みし、誤予測転送を小単位で止められるようにし、GPU上にあるexpertから先に計算することで、expert weight待ちを減らすlossless MoE serving方式。 |
| [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md) | 小型LSTMで各tokenが使うexpertを先に予測し、予測したexpertだけをCPUからGPUへ読み込む。予測結果そのものをroutingに使うため、外れると元modelと異なるexpertを実行し得る近似方式。 |
| [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md) | 次layerのrouting判定を1 block前で行い、必要expertを早めに確定してCPU→GPU転送を現在blockの計算と重ねることで、expert weight待ちを減らすMoE offload方式。 |
<!-- survey:auto:end -->
