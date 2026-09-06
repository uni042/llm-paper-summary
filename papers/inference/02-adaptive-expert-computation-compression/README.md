# Adaptive Expert Computation / Compression

収録論文: 10本。公開日が新しい順。

- 2026-06-29 — [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)
  - router寄与が小さく転送・実行コストが高いexpertをstraggler-awareに省き、既存active expertへ寄与を再配分する。
- 2026-04-09 — [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)
  - モデル全体のexpert activation予算をlayer感度とtokenのrouter分布に基づいて再配分する。
- 2025-11-13 — [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)
  - cache missしたexpertをresidentなbuddy expertで近似して転送を減らす。
- 2025-09-02 — [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)
  - 層ごとにactive expert数を変える。
- 2024-10-23 — [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)
  - expert活性化とtoken schedulingを共同最適化する。
- 2024-10-09 — [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)
  - zero-computation expertで実計算expert数を動的に減らす。
- 2024-06-19 — [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)
  - null expertによりtoken単位で計算量を調整する。
- 2024-02-27 — [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)
  - router確率に応じて活性expert数を変える。
- 2024-02-22 — [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)
  - expert pruningとtoken単位skipを組み合わせる。
- 2023-10-02 — [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)
  - routingの類似性に基づきexpertを統合・圧縮する。
