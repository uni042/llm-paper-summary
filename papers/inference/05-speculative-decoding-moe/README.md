# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

## 収録論文

収録論文: 13本。公開日が新しい順。

- 2026-08-04 — [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)
  - draft branchが受理される見込みとtarget側expertの重要度から、検証時に実行するexpert集合を必要最小限まで縮める。
- 2026-07-14 — [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)
  - 受理される見込みに対して新しく読み込むexpertが少ないdraft branchを優先し、すでにGPU上にあるexpertを再利用する。
- 2026-05-14 — [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md)
  - request rateから実効batch sizeを推定し、speculative decodingの固定costとload-dependent costを分けて、低負荷で速い設定が高負荷で失速する条件を説明する。
- 2026-05-04 — [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md)
  - 低稼働の小型model serviceを共有remote drafterとして再利用し、rollback率に応じて通常型と並列型のspeculative decodingを切り替える。
- 2026-05-01 — [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)
  - 各draft branchについて期待できる受理token数と実測検証コストを比較し、費用対効果の高い範囲だけを検証する。
- 2026-02-12 — [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)
  - speculative decodingの検証中に見えたexpert需要を次の先読みへ利用し、CPU / GPUのどちらで処理するかも同時に調整する。
- 2025-11-18 — [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)
  - 軽い量子化draft modelで先のtokenを作り、その間にtarget MoEで必要になりそうなexpertをCPUからGPUへ先読みする。
- 2025-10-11 — [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)
  - draft生成中にtarget modelの検証で使うexpertを予測して先に読み込み、検証開始時の重み待ちを減らす。
- 2024-02-03 — [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md)
  - 補助draft modelを使わず、Jacobi iterationで将来token候補のn-gramを並列収集し、target LLMで検証して複数tokenを一度に確定する。
- 2024-01-26 — [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md)
  - target LLMの上位hidden featureを軽量decoderで自己回帰予測し、1 step先tokenも入力してfeature uncertaintyを減らす。
- 2024-01-19 — [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md)
  - target LLMへ複数の軽量decoding headを追加して将来token候補を並列予測し、tree attentionでまとめて検証する。
- 2023-11-14 — [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md)
  - 別draft modelの代わりに既存corpusからcontinuationを検索し、retrievalしたtoken列をtarget LLMで並列検証する。
- 2023-05-16 — [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md)
  - 複数の小型draft modelが作る候補token列をtreeへ統合し、target LLMでtree全体を1回に並列検証する。
