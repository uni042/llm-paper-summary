# Expert Prefetch

MoEで次に使われるexpertを**routing結果が確定する前に予測して先にGPUへ読み込む**ことで、CPU / storageからの重み転送待ちを隠す研究をまとめる。予測器、過去のrouting履歴、前のlayerの状態などを使って将来のexpert需要を見積もり、現在の計算と次の転送を重ねるのが基本形となる。

一部の手法はexpertを小さく分けたり、予測したexpertをそのまま使うなどして、予測ミス時の追加I/Oまで減らす。最終目的が推論高速化であるため、予測器自体に学習が必要でもこの系統に分類する。

## 収録論文

収録論文: 12本。公開日が新しい順。

- 2026-06-24 — [SpecPrefetch: Parameter-Efficient Expert Prefetching for Sparse MoE Foundation Models](2026-2607.24787-specprefetch-parameter-efficient-expert-prefetching-for-sparse-moe-foundation-mo.md)
  - 軽量な予測器で次layerのexpertを必要そうな順に並べ、実際に転送できる時間から先読み数を決めてI/O待ちを減らす。
- 2026-03-14 — [FIRM-MoE: Fine-Grained Expert Decomposition for Resource-Adaptive MoE Inference](2026-firm-moe-fine-grained-expert-decomposition-for-resource-adaptive-moe-inference.md)
  - expertをより小さな行列単位へ分け、前の複数layerから必要部分を予測して、帯域に収まる範囲だけ先読みする。
- 2026-03-14 — [CommitMoE: Efficient Fallback-Free MoE Inference with Offloading Under GPU Memory Constraints](2026-commitmoe-efficient-fallback-free-moe-inference-with-offloading-under-gpu-memory.md)
  - 次のexpertを予測して先読みし、後のrouting結果と違っても追加ロードせず予測したexpertをそのまま使うことでI/O待ちをなくす。
- 2026-03-14 — [CasMoE: A Cascaded Framework for Efficient MoE Inference on Resource-constrained Devices](2026-casmoe-a-cascaded-framework-for-efficient-moe-inference-on-resource-constrained-.md)
  - 学習済み予測器と、過去に似たrouting履歴の検索を組み合わせ、promptの早い段階から将来使うexpertを予測する。
- 2026-03-09 — [Speculating Experts Accelerates Inference for Mixture-of-Experts](2026-2603.19289-speculating-experts-accelerates-inference-for-mixture-of-experts.md)
  - 現在のlayerから次layerのrouting入力を先に近似し、expert転送だけでなくexpert計算そのものも早く開始する。
- 2025-12-03 — [OD-MoE: On-Demand Expert Loading for Cacheless Edge-Distributed MoE Inference](2025-2512.03927-od-moe-on-demand-expert-loading-for-cacheless-edge-distributed-moe-inference.md)
  - 常設のexpert cacheを持たず、次に必要と予測したexpertだけをedge device間でその都度読み込んで転送量を抑える。
- 2025-09-28 — [LayerScope: Predictive Cross-Layer Scheduling for Efficient Multi-Batch MoE Inference on Legacy Servers](2025-2509.23638-layerscope-predictive-cross-layer-scheduling-for-efficient-multi-batch-moe-infer.md)
  - 複数batchについて先のlayerまでroutingを予測し、expert転送とGPU計算の順番をまとめて組むことで古いserverでも待ち時間を減らす。
- 2025-02-17 — [Fate: Fast Edge Inference of Mixture-of-Experts Models via Cross-Layer Gate](2025-2502.12224-fate-fast-edge-inference-of-mixture-of-experts-models-via-cross-layer-gate.md)
  - 次layerのrouting判定を前のlayerで先に行い、必要expertの転送を現在の計算と重ねる。
- 2024-12-16 — [DAOP: Data-Aware Offloading and Predictive Pre-Calculation for Efficient MoE Inference](2024-2501.10375-daop-data-aware-offloading-and-predictive-pre-calculation-for-efficient-moe-infe.md)
  - 入力ごとのexpert利用傾向に合わせて配置を変え、次のroutingを予測してCPU側の計算も先行させる。
- 2024-10-29 — [ProMoE: Fast MoE-based LLM Serving using Proactive Caching](2024-2410.22134-promoe-fast-moe-based-llm-serving-using-proactive-caching.md)
  - 軽量な予測器で将来使うexpertを見積もり、現在のGPU計算中にCPUから先読みしてcacheへ入れる。
- 2023-10-29 — [SiDA-MoE: Sparsity-Inspired Data-Aware Serving for Efficient and Scalable Large Mixture-of-Experts Models](2023-2310.18859-sida-moe-sparsity-inspired-data-aware-serving-for-efficient-and-scalable-large-m.md)
  - 過去のrouting列から次batchで使うexpertを予測し、必要な重みだけをCPUからGPUへ先に送る。
- 2023-08-23 — [Pre-gated MoE: An Algorithm-System Co-Design for Fast and Scalable Mixture-of-Expert Inference](2023-2308.12066-pre-gated-moe-an-algorithm-system-co-design-for-fast-and-scalable-mixture-of-exp.md)
  - 次layerのroutingを前段で確定できる構造に変え、expert通信を現在の計算と重ねて分散MoE推論を高速化する。
