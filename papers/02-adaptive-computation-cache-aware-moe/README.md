# Adaptive Expert Computation / Compression

収録論文: 9本。公開日が新しい順。

- 2026-04-09 — [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)
  - モデル全体のexpert activation予算をlayer感度とtokenのrouter分布に基づいて再配分し、固定Top-kより品質を保って計算量を削減する。
- 2025-11-13 — [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)
  - expert間の冗長性を利用してcache missしたexpertをresidentなbuddy expertで近似し、重み転送を減らす方式。
- 2025-09-02 — [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)
  - 層ごとの重要度に合わせてactive expert数を変え、固定Top-kより少ない計算で品質維持を狙うMoE推論手法。
- 2024-10-23 — [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)
  - expert活性化とtoken割当てを共同最適化し、MoE推論の負荷不均衡と不要計算を抑えるフレームワーク。
- 2024-10-09 — [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)
  - zero-computation expertをMoEへ導入し、入力難度に応じて実計算を担うexpert数を動的に削減する手法。
- 2024-06-19 — [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)
  - 計算を行わないnull expertをルーティング先に加え、容易なトークンほど実expertの実行数を減らす適応型MoE。
- 2024-02-27 — [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)
  - ルータ確率の累積質量に応じてトークンごとの活性expert数を変え、品質とMoE計算量を適応的に両立する手法。
- 2024-02-22 — [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)
  - 層出力の再構成誤差で不要expertを恒久pruningし、低router weightの第二expertをtoken単位でskipする学習不要の圧縮手法。
- 2023-10-02 — [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)
  - router出力が似るexpertを整列・統合してから低rank＋sparse残差へ圧縮し、MoEのexpert数とモデル容量を削減する手法。
