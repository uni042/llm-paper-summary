# Expert prefetch

収録論文: 12本。公開日が新しい順。

- 2026-06-24 — [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md)
  - 低ランク予測器で次層expertの優先順位を推定し、転送可能時間から先読み数を動的制限して、native routingを変えずにedge MoEのI/O待ちを減らす。
- 2026-03-14 — [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md)
  - expertを行列単位のsub-expertへ分解し、複数前層の合意予測と資源適応型prefetchでCPU–GPU転送量を抑えるMoE推論方式。
- 2026-03-14 — [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md)
  - 次層expertを先読みし、予測が外れても追加ロードへ戻らず予測expertを確定実行することで、MoE重みオフロードの待ち時間を除く手法。
- 2026-03-14 — [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md)
  - 学習済み予測器と過去routing patternの検索器をcascadeし、promptから全層のexpertを先読みして資源制約下のMoE推論を高速化する。
- 2026-03-09 — [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md)
  - 現在層の隠れ状態から次層router入力を近似し、expert転送だけでなく投機実行まで前倒ししてCPUオフロードMoEのTPOTを下げる。
- 2025-12-03 — [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md)
  - 常設cacheを持たないedge分散環境で、予測した必要expertだけをオンデマンドにロードして転送量を抑える手法。
- 2025-09-28 — [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md)
  - 複数batchのroutingを層横断で予測し、legacy server上のexpert転送と計算を共同スケジューリングする方式。
- 2025-02-17 — [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md)
  - 前層で次層のgateを先行評価するcross-layer gatingにより、edge MoEのexpert先読みと転送隠蔽を行う手法。
- 2024-12-16 — [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md)
  - sequence固有のexpert配置と次層routing予測によるCPU先行計算を組み合わせ、単一GPUのMoE推論を高速化するシステム。
- 2024-10-29 — [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md)
  - 軽量予測器で将来のexpert選択を先読みし、proactive cachingでCPU–GPU転送を計算に重ねるMoE serving方式。
- 2023-10-29 — [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md)
  - LSTM予測器で次batchの活性expertを推定し、必要重みだけをCPUからGPUへ先読みするdata-aware MoE serving方式。
- 2023-08-23 — [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md)
  - 次層のroutingを前段で確定するpre-gatingにより、expert通信を計算と重ねて分散MoE推論を高速化する手法。
