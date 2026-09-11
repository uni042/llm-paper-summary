# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の本文・メタデータから arXiv ID / DOI の明示参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [Training-Free Halving of Activated Experts in Fine-Grained Mixture-of-Experts Models](2026-2609.04575-training-free-halving-activated-experts.md) | ✓ | 0 | 実行expert数k1とrouter正規化分母のreference set k2を分離し、fine-grained MoEでexpert computeを減らしつつ訓練時のexpert-branch gainを保つ。Qwen3.6-35B-A3Bの8→4 expertでMMLU低下を4.65ptから0.35ptへ縮小する。 |
| 2026-09 | [ACE: Adaptive Calibration-Free Expert Skipping for MoE-based LLMs](2026-2609.05228-ace.md) | ✓ | 0 | 固定top-kルーティングで選ばれたexpertのうち実際の寄与が小さいslotをtokenごとに省く、学習不要・checkpoint保持型のMoE推論手法。Global Spectral Proxy (GSP)がSwiGLU expertのgate/up/down投影とRMSNorm scalingから全体的な変換能力を推定し、Router-Conditioned Refinement (RCR)がcentered router weightからrouting-preferred方向を作って方向依存のexpert応答を補正する。実行時はrouter gateと2つのoffline tableを組み合わせ、両方で低寄与と判断されたslotだけをskipしtop-1 expertは必ず残す。 |
| 2026-06 | [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md) | ✓ | 0 | router上の寄与が小さい一方で転送・実行に時間がかかり、特に全体処理を遅らせているdevice上のexpertを省き、その寄与を実行済みexpertへ振り分けてmulti-device MoEを高速化する。 |
| 2026-05 | [ReMoE: Boosting Expert Reuse through Router Fine-Tuning in Memory-Constrained MoE LLM Inference](2026-2605.27081-remoe-router-finetuning-expert-reuse.md) | ✓ | 0 | 細粒度MoEを端末で動かすと、連続トークンが別々のエキスパートを選ぶたびに小さな高速キャッシュから重みが追い出され、CPU DRAMやNVMe SSDなど低速階層から再読込が必要になる。ReMoEは実行時キャッシュを複雑化する代わりに、既学習モデルのルータだけを追加学習し、直前に選んだエキスパートへ確率を寄せつつ元ルータからの逸脱をKL損失で抑える。DeepSeek-V2-Liteで隣接トークン間のエキスパート重複率を相対26.4%高め、Jetson Orin NXのSSD-backed llama.cppではトークン間遅延を43.6〜49.8%削減した。 |
| 2026-04 | [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md) | ✓ | 1 | モデル全体で許すexpert実行回数を先に決め、その予算を影響の大きいlayerとrouter判断が曖昧なtokenへ多く配ることで、固定Top-kより少ない計算で品質を保つ。 |
| 2025-11 | [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md) | ✓ | 1 | 必要なexpertがGPU cacheにない時、同じtokenで一緒に選ばれやすい常駐expertを代わりに使い、CPUからexpert weightを読むPCIe待ちを品質と引き換えに減らす。 |

### 直近12か月より前・リポジトリ内で被引用

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-02 | [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md) | [✓](https://github.com/Lucky-Lance/Expert_Sparsity) | 16 | 削除してもlayer出力があまり変わらないexpertをモデルから恒久的に除き、さらにtokenごとにrouter寄与が小さい第2expertを省いて、memoryとFFN計算を減らす学習不要の手法。 |
| 2024-10 | [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md) | ✓ | 7 | 数layer先で使うexpertを予測し、同じexpertを使いそうなtokenをまとめ、GPU cache容量も需要に応じてlayer間で動かすことで、CPUからexpertを読む待ち時間を減らすMoE推論system。 |
| 2023-10 | [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md) | [✓](https://github.com/UNITES-Lab/MC-SMoE) | 5 | routerの利用履歴から『似た入力を担当しているexpert』を見つけ、ニューロンの並びを揃えてから代表expertへ統合し、統合後weightをlow-rank成分と構造的に疎な残差へ分解することでMoEのmemory footprintを大幅に減らす。 |
| 2024-02 | [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md) | [✓](https://github.com/ysngki/XMoE) | 3 | router確率を高い順に足し、合計が設定値に達するまでexpertを選ぶことで、routerが確信しているtokenでは少数、判断が分散しているtokenでは多数のexpertを使う。 |
| 2025-09 | [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md) | ✓ | 2 | layerごとにTop-kを減らした時の出力変化を事前に測り、影響が小さいlayerではexpert数を減らし、影響が大きいlayerへexpert実行予算を回すことで、固定Top-kより少ない計算で品質維持を狙う。 |
| 2024-06 | [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md) | ✓ | 1 | 計算を行わないnull expertをrouting候補へ加え、簡単なtokenではnullを多く選ばせることで、実際にFFN計算するexpert数をtokenごとに変えるMoE。 |

### その他

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-10 | [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md) | [✓](https://github.com/SkyworkAI/MoE-plus-plus) | 0 | 通常のFFN expertに加えて、何も出力しない・入力をそのまま返す・学習済み定数を返す軽量expertをrouting候補へ入れ、tokenに応じて実際のFFN計算数を減らすMoE。 |
<!-- survey:auto:end -->
