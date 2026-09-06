# Speculative Decoding × MoE

Speculative decodingをMoEへ適用したときに増えやすい**expertの読み込み・分散実行・検証コスト**を減らす研究をまとめる。通常のdense modelではdraft tokenをまとめて検証すればよいが、MoEでは検証するtokenやbranchが増えるほど、呼び出すexpert数や重み転送量も増えやすい。

そのため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、すでにGPU上にあるexpertを優先して使うなどして、speculative decodingの並列性を維持しながらMoE特有の追加コストを抑える。

## 収録論文

収録論文: 6本。公開日が新しい順。

- 2026-08-04 — [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)
  - draft branchが受理される見込みとtarget側expertの重要度から、検証時に実行するexpert集合を必要最小限まで縮める。
- 2026-07-14 — [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)
  - 受理される見込みに対して新しく読み込むexpertが少ないdraft branchを優先し、すでにGPU上にあるexpertを再利用する。
- 2026-05-01 — [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)
  - 各draft branchについて期待できる受理token数と実測検証コストを比較し、費用対効果の高い範囲だけを検証する。
- 2026-02-12 — [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)
  - speculative decodingの検証中に見えたexpert需要を次の先読みへ利用し、CPU / GPUのどちらで処理するかも同時に調整する。
- 2025-11-18 — [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)
  - 軽い量子化draft modelで先のtokenを作り、その間にtarget MoEで必要になりそうなexpertをCPUからGPUへ先読みする。
- 2025-10-11 — [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)
  - draft生成中にtarget modelの検証で使うexpertを予測して先に読み込み、検証開始時の重み待ちを減らす。
