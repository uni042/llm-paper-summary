# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

| 論文 | 一文要約 |
|---|---|
| [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md) | draft枝がtargetに受理される見込みとrouter上のexpert寄与を合わせて、verificationで実行するexpert数をlayerごとに減らし、offload時のHost→GPU転送を削る近似手法。 |
| [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md) | draft nodeごとに受理される見込みと新しく必要になるexpert数を比較し、すでに使う予定のexpertを再利用しやすい枝を優先してMoE検証のHBM readを減らす手法。 |
| [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md) | speculative decodingの低負荷時の速さだけでなく、request rateが上がるとdraft・verificationの負荷依存costがbatchとともに増えてspeedupが縮む現象を、Little's Lawから推定した実効batch sizeと少数のcost係数で説明するserving latency model。 |
| [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md) | 複数LLMを同時提供するクラウドでは、人気の大型モデルが混雑する一方、小型モデル用GPUが余ることがある。SPECTREはその空き小型モデルを遠隔下書きモデルとして使って大型モデルの投機的デコードを支援し、下書き生成と大型モデル検証を直列に行う通常型と、両方を重ねる並列型を失敗率に応じて切り替える。余剰GPUを新規専用draf­terなしで再利用するserving手法。 |
| [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md) | draft treeの各候補について受理される見込みと実際の検証時間を比較し、費用対効果の高い枝だけをtarget MoEで検証する手法。 |
| [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md) | speculative decodingで少し先に見えるexpert需要を利用し、どのexpertをGPUへ残す・先読みする・CPUで実行するかをまとめて決めるedge向けMoE推論方式。 |
| [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md) | target MoEの4-bit版をdraftとして使い、token候補と将来使うexpertの両方を先に予測して、target検証前に必要なexpert重みをCPUからGPUへ読み込む方式。 |
| [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md) | speculative decodingでdraft tokenを作っている間に、target MoEが検証時に使いそうなexpert重みをCPUからGPUへ先読みし、verification開始後のweight待ちを減らす手法。 |
| [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md) | target LLM自身をJacobi型に複数future positionへ並列適用し、その反復軌跡から将来使えそうなn-gramを大量に収集する。現在prefixに接続できるn-gramだけを同じtarget LLMで並列検証し、複数tokenを一度に確定する。追加draft model・追加training・外部corpusを必要とせず、余っているGPU FLOPsを使って逐次decode step数を減らすexact decoding方式。 |
| [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md) | target LLMの上から2番目の層が作る高水準な特徴量を軽量decoderで自己回帰予測し、さらに1 step先へずらした実tokenを条件として与えることでfeature予測の分岐不確実性を解消する。予測featureから元LM headでdraft tokenを作り、target LLMがtree状候補を一括検証するlossless speculative sampling方式。 |
| [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md) | 別のdraft LLMを常駐させず、target LLMの最後のhidden stateへ複数の軽量decoding headを追加して1〜数token先の候補を同時予測し、候補をsparse token treeへまとめてbackbone自身で一括検証することで、1回の巨大model forwardから複数tokenを確定する。 |
| [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md) | 小型draft modelを別途学習・実行する代わりに、既存text corpusから現在contextの末尾と一致する過去断片を検索し、その続き候補をTrieへまとめてtarget LLMで一括検証することで、1回のtarget-model passで複数tokenをlosslessに確定する。 |
| [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md) | 複数の小型draft modelやretrievalが作る候補token列を共通prefixでtreeへまとめ、target LLMにtree全体を1回で並列検証させることで、target modelの巨大weightを読む回数や分散通信回数を減らし、1 verification stepで複数tokenを確定するspeculative inference system。 |
<!-- survey:auto:end -->
