# Adaptive Expert Computation / Compression

MoEで毎回同じ数のexpertを実行するのではなく、**token・layer・expertの重要度や実行コストに応じて、実際に使うexpert数やexpert構成を変える**研究をまとめる。簡単なtokenではexpert計算を減らし、重要なtokenやlayerには多くの計算を割り当てるほか、役割が似たexpertを統合したり、GPUにないexpertを似た常駐expertで代替したりして、品質低下を抑えながら計算量・転送量・モデル容量を減らす。

`Expert Prefetch` が「この先必要になるexpertを予測して早めにGPUへ用意する」ことを主眼とするのに対し、この系統は**そもそもどのexpertを何個実行するか、あるいはexpert構成そのものをどう小さくするか**が中心となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-04 | [Alloc-MoE: Budget-Aware Expert Activation Allocation for Efficient Mixture-of-Experts Inference](2026-2604.08133-alloc-moe-budget-aware-expert-activation-allocation-for-efficient-mixture-of-exp.md) | ✓ | 1 | Alloc-MoEは、全層・全トークンで使えるエキスパート実行回数の合計を一つのglobal budgetとして扱い、そのbudgetを「どの層へ何個」「その層内のどのトークンへ何個」配るかを二段階で決める。 |
| 2025-11 | [BuddyMoE: Exploiting Expert Redundancy to Accelerate Memory-Constrained Mixture-of-Experts Inference](2025-2511.10054-buddymoe-exploiting-expert-redundancy-to-accelerate-memory-constrained-mixture-o.md) | ✓ | 1 | BuddyMoEは、CPUへオフロードしたMoEでGPU キャッシュに必要エキスパートがない時、そのエキスパートをPCIe経由で読み込む代わりに、GPUにすでにある機能的に近そうなエキスパートで代用する近似手法である。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [Training-Free Halving of Activated Experts in Fine-Grained Mixture-of-Experts Models](2026-2609.04575-training-free-halving-activated-experts.md) | ✓ | 0 | 実行エキスパート数k1とルータ正規化分母の基準 集合 k2を分離し、細粒度 MoEでエキスパート 計算を減らしつつ訓練時のエキスパート-分岐 利得を保つ。 |
| 2026-09 | [ACE: Adaptive Calibration-Free Expert Skipping for MoE-based LLMs](2026-2609.05228-ace.md) | ✓ | 0 | 固定上位kルーティングで選ばれたエキスパートのうち実際の寄与が小さいスロットをトークンごとに省く、学習不要・チェックポイント保持型のMoE推論手法。 |
| 2026-06 | [Beyond Uniform Experts: Cost-Aware Expert Execution for Efficient Multi-Device MoE Inference](2026-2606.29982-beyond-uniform-experts-cost-aware-expert-execution-for-efficient-multi-device-mo.md) | ✓ | 0 | コスト-Aware エキスパート実行（CAEE）は、元Top-k内のエキスパートをすべて同じ価値として扱わず、ルータ上の寄与と実際のハードウェア費用を同時に見て、一部エキスパートを実行しない近似手法である。 |
| 2026-05 | [ReMoE: Boosting Expert Reuse through Router Fine-Tuning in Memory-Constrained MoE LLM Inference](2026-2605.27081-remoe-router-finetuning-expert-reuse.md) | ✓ | 0 | 細粒度MoEを端末で動かすと、連続トークンが別々のエキスパートを選ぶたびに小さな高速キャッシュから重みが追い出され、CPU DRAMやNVMe SSDなど低速階層から再読込が必要になる。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-02 | [Not All Experts are Equal: Efficient Expert Pruning and Skipping for Mixture-of-Experts Large Language Models](2024-2402.14800-not-all-experts-are-equal-efficient-expert-pruning-and-skipping-for-mixture-of-e.md) | [✓](https://github.com/Lucky-Lance/Expert_Sparsity) | 18 | この論文はMixtral-8x7Bのエキスパート冗長性を、配備前にエキスパートそのものを削除する処理と、実行時に一部トークンの第2エキスパートだけを省く処理の二段階で削る。 |
| 2024-10 | [ExpertFlow: Efficient Mixture-of-Experts Inference via Predictive Expert Caching and Token Scheduling](2024-2410.17954-expertflow-efficient-mixture-of-experts-inference-via-predictive-expert-caching-.md) | ✓ | 8 | エキスパートFlowは、CPUへオフロードしたエキスパートを単に先読みするだけでなく、同じエキスパート経路を通りそうなトークンを同じバッチへ集め、GPU上のエキスパート キャッシュ容量も層ごとの将来需要に合わせて動かすシステムである。 |
| 2023-10 | [Merge, Then Compress: Demystify Efficient SMoE with Hints from Its Routing Policy](2023-2310.01334-merge-then-compress-demystify-efficient-smoe-with-hints-from-its-routing-policy.md) | [✓](https://github.com/UNITES-Lab/MC-SMoE) | 6 | 疎活性化Mixture-of-専門家（Sparse Mixture-of-専門家: SMoE）は、1 トークンあたり実際に使う専門家を少数に限定するため、全パラメータ数を増やしてもFLOPsの増加を抑えられる。 |
| 2024-02 | [XMoE: Sparse Models with Fine-grained and Adaptive Expert Selection](2024-2403.18926-xmoe-sparse-models-with-fine-grained-and-adaptive-expert-selection.md) | [✓](https://github.com/ysngki/XMoE) | 3 | XMoEは、固定Top-kでは全トークンへ同じエキスパート数を割り当てるため、簡単なトークンにも難しいトークンにも同じ計算量を使うことを問題にする。 |
| 2025-09 | [LExI: Layer-Adaptive Active Experts for Efficient MoE Model Inference](2025-2509.02753-lexi-layer-adaptive-active-experts-for-efficient-moe-model-inference.md) | ✓ | 2 | LExIは、全MoE 層で同じTop-kを使うのではなく、Top-kを下げても出力があまり変わらない層ではKを減らし、変化が大きい層にはKを多く残すdata-freeな推論最適化である。 |
| 2024-06 | [AdaMoE: Token-Adaptive Routing with Null Experts for Mixture-of-Experts Language Models](2024-2406.13233-adamoe-token-adaptive-routing-with-null-experts-for-mixture-of-experts-language-.md) | ✓ | 1 | AdaMoEは固定Top-kを直接可変長ルータへ作り直す代わりに、計算をしないnull エキスパートを通常エキスパートと同じルーティング候補へ混ぜることで、トークンごとの実FFN数を変える。 |
| 2024-10 | [MoE++: Accelerating Mixture-of-Experts Methods with Zero-Computation Experts](2024-2410.07348-moe-accelerating-mixture-of-experts-methods-with-zero-computation-experts.md) | [✓](https://github.com/SkyworkAI/MoE-plus-plus) | 0 | MoE++は、通常のFFN エキスパートだけでなく、大きな行列計算をほとんど必要としない3種類のエキスパートをルータ候補へ最初から組み込む異種MoEである。 |
<!-- survey:auto:end -->
