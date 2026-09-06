# Adaptive Expert Computation / Compression

MoEで毎回同じ数・同じ扱いのexpertを実行するのではなく、**token、layer、expertの重要度や実行コストに応じて、使うexpert数やexpertそのものを動的に変える**研究をまとめる。不要なexpertをskip・prune・mergeしたり、GPUにないexpertを似たexpertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を削減する。

Expert Prefetchが「必要なexpertを早く用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを、何個、実行するかを変える**ことが中心となる。

## 収録論文

収録論文: 10本。公開日が新しい順。

- 2026-06-29 — [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md)
  - 出力への寄与が小さい一方で転送・実行に時間がかかるexpertを省き、その寄与を他の実行済みexpertへ振り分けてmulti-device推論の遅延を減らす。
- 2026-04-09 — [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md)
  - モデル全体で使えるexpert実行回数を一つの予算として扱い、重要なlayerや判断が難しいtokenへ多く配分する。
- 2025-11-13 — [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md)
  - 必要なexpertがGPUにない場合、挙動が近い常駐expertで代替し、新しい重みを読み込む待ち時間を減らす。
- 2025-09-02 — [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md)
  - すべてのlayerで同じTop-kを使わず、layerごとの重要度に応じて実行するexpert数を変える。
- 2024-10-23 — [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md)
  - expertの利用予測とtokenの実行順をまとめて調整し、GPU上のexpertを有効利用しながら負荷の偏りと不要な待ち時間を減らす。
- 2024-10-09 — [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md)
  - 計算を行わないexpertをrouting先として追加し、簡単なtokenでは実際に計算するexpert数を減らす。
- 2024-06-19 — [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md)
  - 計算をしないnull expertを使い、tokenごとの難しさに応じて実expertの実行数を変える。
- 2024-02-27 — [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md)
  - router確率の合計が十分になるまでexpertを選ぶことで、tokenごとに必要なexpert数を変える。
- 2024-02-22 — [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md)
  - 重要度の低いexpertをモデルから恒久的に削り、さらにtokenごとに寄与の小さい追加expertをskipして計算量を減らす。
- 2023-10-02 — [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md)
  - routing傾向が似ているexpertをまとめてから低rank表現などで圧縮し、expert数とモデル容量を同時に減らす。
