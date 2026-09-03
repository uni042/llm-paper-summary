# Speculative decoding × MoE

収録論文: 6本。公開日が新しい順。

- 2026-08-04 — [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)
  - draft nodeの受理確率とtarget router scoreから検証expert集合を層ごとに縮小し、offload時はresident expertを優先して転送量を削減する。
- 2026-07-14 — [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)
  - 受理確率／新規expertコスト比でdraft nodeを選び、buffer内expertを再利用することでlossless verificationのexpert scatteringとHBM trafficを抑える。
- 2026-05-01 — [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)
  - 各draft nodeの受理確率と実測verification costから、期待受理token／コストが最大となるtree prefixだけを動的検証する。
- 2026-02-12 — [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)
  - speculative decodingの検証で観測したexpert需要を先読み信号にし、utility推定・整数最適化・非同期実行でedgeのprefetchとCPU/GPU分担を制御する。
- 2025-11-18 — [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)
  - 量子化draftによる投機生成とproactive expert prefetch／offloadを協調させ、MoE検証時の重みI/Oを削減する方式。
- 2025-10-11 — [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)
  - speculative decodingとexpert prefetchを統合し、ドラフト生成中に検証で必要なMoE重みを先読みして待ち時間を減らす手法。
