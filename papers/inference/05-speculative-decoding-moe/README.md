# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（16本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の本文・メタデータから arXiv ID / DOI の明示参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md) | [✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) | 0 | GLANCEはfrozen VLM targetの融合済みvision-language stateからfuture token blockを1 passでdraftし、wide treeを1 target passで検証するlossless speculative decoder。grounded taskでautoregressive比最大2.93x。free-running textではchain drafterが優位となる境界も示す。 |
| 2026-08 | [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md) | ✓ | 0 | draft枝がtargetに受理される見込みとrouter上のexpert寄与を合わせて、verificationで実行するexpert数をlayerごとに減らし、offload時のHost→GPU転送を削る近似手法。 |
| 2026-07 | [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md) | ✓ | 0 | draft nodeごとに受理される見込みと新しく必要になるexpert数を比較し、すでに使う予定のexpertを再利用しやすい枝を優先してMoE検証のHBM readを減らす手法。 |
| 2026-07 | [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md) | ✓ | 0 | 端末上のMixture-of-エキスパート（MoE）推論で、専門家重みをCPUメモリやフラッシュストレージからGPU/NPUへ都度搬送する場合、通常の投機デコードは候補トークンを増やすほどドラフト側・検証側で必要専門家の集合が膨らみ、搬送費が増えて高速化条件を失う。DraftExpertは各MoE層に小さな常駐ドラフト専門家を1個だけ追加し、共有経路＋上位1専門家＋ドラフト専門家という固定フットプリントで候補を作る。自己蒸留で受理率とルーター一致を回復し、予測した検証専門家集合を使う展開量考慮打ち切りと非同期プリフェッチを組み合わせることで、完全な対象モデル検証を保ったまま平均1.45倍のデコード処理量を得る。 |
| 2026-05 | [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md) | [✓](https://github.com/sgl-project/sglang/pull/22272) | 0 | 複数LLMを同時提供するクラウドでは、人気の大型モデルが混雑する一方、小型モデル用GPUが余ることがある。SPECTREはその空き小型モデルを遠隔下書きモデルとして使って大型モデルの投機的デコードを支援し、下書き生成と大型モデル検証を直列に行う通常型と、両方を重ねる並列型を失敗率に応じて切り替える。余剰GPUを新規専用draf­terなしで再利用するserving手法。 |
| 2026-05 | [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md) | ✓ | 0 | draft treeの各候補について受理される見込みと実際の検証時間を比較し、費用対効果の高い枝だけをtarget MoEで検証する手法。 |
| 2026-05 | [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md) | ✓ | 0 | speculative decodingの低負荷時の速さだけでなく、request rateが上がるとdraft・verificationの負荷依存costがbatchとともに増えてspeedupが縮む現象を、Little's Lawから推定した実効batch sizeと少数のcost係数で説明するserving latency model。 |
| 2026-02 | [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md) | ✓ | 0 | Mixture-of-エキスパート（MoE）モデルで木構造の投機デコードを行うと、候補トークンが増えるほど各層で必要になる専門家の和集合が膨らみ、疎な専門家活性化の利点が検証段階で失われる。MoE-Specは、ドラフト木全体のルーター確率を合算して各層で重要な専門家だけを固定予算B個へ絞り、その専門家集合の中で各候補トークンの上位k専門家を再選択して検証する学習不要方式。専門家予算により木の大きさと読み出す専門家数を切り離し、A100実機上のOLMoE、Qwen3-30B-A3B、MixtralでEAGLE系に対し27/30条件で速度を改善し、平均受理長をほぼ維持した。 |
| 2026-02 | [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md) | [✓](https://github.com/lshAlgorithm/MoE-SpAc) | 0 | speculative decodingで少し先に見えるexpert需要を利用し、どのexpertをGPUへ残す・先読みする・CPUで実行するかをまとめて決めるedge向けMoE推論方式。 |
| 2025-11 | [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md) | ✓ | 0 | target MoEの4-bit版をdraftとして使い、token候補と将来使うexpertの両方を先に予測して、target検証前に必要なexpert重みをCPUからGPUへ読み込む方式。 |
| 2025-10 | [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md) | ✓ | 0 | speculative decodingでdraft tokenを作っている間に、target MoEが検証時に使いそうなexpert重みをCPUからGPUへ先読みし、verification開始後のweight待ちを減らす手法。 |

### 直近12か月より前・リポジトリ内で被引用

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-02 | [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md) | [✓](https://github.com/hao-ai-lab/LookaheadDecoding) | 1 | target LLM自身をJacobi型に複数future positionへ並列適用し、その反復軌跡から将来使えそうなn-gramを大量に収集する。現在prefixに接続できるn-gramだけを同じtarget LLMで並列検証し、複数tokenを一度に確定する。追加draft model・追加training・外部corpusを必要とせず、余っているGPU FLOPsを使って逐次decode step数を減らすexact decoding方式。 |
| 2024-01 | [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md) | [✓](https://github.com/SafeAILab/EAGLE) | 1 | target LLMの上から2番目の層が作る高水準な特徴量を軽量decoderで自己回帰予測し、さらに1 step先へずらした実tokenを条件として与えることでfeature予測の分岐不確実性を解消する。予測featureから元LM headでdraft tokenを作り、target LLMがtree状候補を一括検証するlossless speculative sampling方式。 |
| 2023-11 | [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md) | [✓](https://github.com/FasterDecoding/REST) | 1 | 小型draft modelを別途学習・実行する代わりに、既存text corpusから現在contextの末尾と一致する過去断片を検索し、その続き候補をTrieへまとめてtarget LLMで一括検証することで、1回のtarget-model passで複数tokenをlosslessに確定する。 |
| 2023-05 | [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md) | [✓](https://github.com/flexflow/FlexFlow) | 1 | 複数の小型draft modelやretrievalが作る候補token列を共通prefixでtreeへまとめ、target LLMにtree全体を1回で並列検証させることで、target modelの巨大weightを読む回数や分散通信回数を減らし、1 verification stepで複数tokenを確定するspeculative inference system。 |

### その他

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-01 | [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md) | [✓](https://github.com/FasterDecoding/Medusa) | 0 | 別のdraft LLMを常駐させず、target LLMの最後のhidden stateへ複数の軽量decoding headを追加して1〜数token先の候補を同時予測し、候補をsparse token treeへまとめてbackbone自身で一括検証することで、1回の巨大model forwardから複数tokenを確定する。 |
<!-- survey:auto:end -->
