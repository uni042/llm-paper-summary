# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

## 収録論文

収録論文: 10本。公開日が新しい順。

- 2026-06-29 — [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)
  - 出力への寄与が小さい一方で転送・実行に時間がかかるexpertを省き、そのexpertが担当するはずだった寄与を実行済みexpertへ振り分けてmulti-device推論の遅延を減らす。
- 2026-04-09 — [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)
  - モデル全体で使えるexpert実行回数を一つの予算として扱い、重要なlayerやrouterの判断が曖昧なtokenへ多く配分する。
- 2025-11-13 — [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)
  - 必要なexpertがGPUにない場合、出力傾向が近い常駐expertで代替し、新しいexpert weightを読み込む待ち時間を減らす。
- 2025-09-02 — [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)
  - すべてのlayerで同じTop-kを使わず、品質への影響が大きいlayerでは多く、小さいlayerでは少ないexpertを実行する。
- 2024-10-23 — [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)
  - 近い将来使うexpertを予測してGPUへ残す処理と、同じexpertを使うtokenをまとめて処理する順序調整を組み合わせ、expertの読み込み待ちとGPU内の負荷偏りを減らす。
- 2024-10-09 — [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)
  - 計算を行わず入力をそのまま通すexpertをrouting先として追加し、簡単なtokenでは実際にFFN計算するexpert数を減らす。
- 2024-06-19 — [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)
  - 計算をしないnull expertを候補に含め、tokenごとのrouter出力に応じて実際に計算するexpert数を変える。
- 2024-02-27 — [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)
  - router確率を高い順に足し、合計が設定値に達するまでexpertを選ぶことで、routerが確信しているtokenでは少数、判断が分散しているtokenでは多数のexpertを使う。
- 2024-02-22 — [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)
  - 削除してもlayer出力があまり変わらないexpertをモデルから恒久的に除き、さらにtokenごとに寄与が小さい第2expertを省いて計算量を減らす。
- 2023-10-02 — [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)
  - routerが似た入力を割り当てるexpertを一つにまとめ、そのweightを「少数の行列成分で表せる部分」と「そこから外れる少量の残差」に分けて圧縮し、expert数とモデル容量を同時に減らす。
