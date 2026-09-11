# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（17本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-11 | [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md) | ✓ | 6 | MoE-SpeQは、targetとほぼ同じ構造を持つ4-bit量子化版を下書きモデルとして使い、そのルーティング結果をエキスパート予測にも利用する方式である。 |
| 2025-10 | [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md) | ✓ | 6 | SP-MoEは、投機的 デコードの下書き処理を単にトークンを先に生成するためだけでなく、対象モデルが将来使うエキスパートを早く知るための時間として利用する。 |
| 2026-02 | [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md) | ✓ | 5 | Mixture-of-エキスパート（MoE）モデルで木構造の投機デコードを行うと、候補トークンが増えるほど各層で必要になる専門家の和集合が膨らみ、疎な専門家活性化の利点が検証段階で失われる。MoE-Specは、ドラフト木全体のルーター確率を合算して各層で重要な専門家だけを固定予算B個へ絞り。 |
| 2026-02 | [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md) | [✓](https://github.com/lshAlgorithm/MoE-SpAc) | 2 | MoE-SpAcは、投機的 デコードで先に見えるfuture トークンのルーティング情報を、エキスパート キャッシュ / 先読み / CPU-GPU配置を決めるための予測信号として再利用するedge向けシステムである。 |
| 2026-07 | [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md) | ✓ | 1 | EcoSpecは、投機的 デコードの下書き treeを作る段階で、トークンが対象モデルに受理されそうかだけでなく、そのnodeを追加すると新しいエキスパート 重みを何種類読む必要があるかまで考える方式である。 |
| 2026-05 | [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md) | ✓ | 1 | 追い出しは、MoE 投機的 デコードで下書き treeを何nodeまで対象モデル モデルで検証するかを動的に決める手法である。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding](2026-2609.09338-osprey-target-agnostic-pretraining-speculative-decoding.md) | [✓](https://github.com/LeanModels/Osprey) | 0 | Ospreyは、投機的デコードのドラフトモデルが特定ターゲットと狭い学習分布へ過度に結び付くことで、分野や言語が変わると受理長が低下する問題を、再利用可能な事前学習済み小型言語モデルの知識で緩和する手法である。Qwen3-4Bなどを数層だけ残して枝刈りし、汎用ウェブ文書で次トークン予測を継続学習した浅い骨格を一度作る。その後、ターゲットごとに語彙を整合し。 |
| 2026-08 | [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md) | [✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) | 0 | GLANCEは、凍結したVLM対象モデルが入力処理で作った視覚・言語融合状態から、将来のトークン塊を1回で下書きし、幅のある候補木を対象モデルの1回の処理で検証する無損失の投機的デコーダである。画像に根差した課題では自己回帰方式に対して最大2.93倍となる一方、自由生成の文章では連鎖型下書きが有利になる境界も示す。 |
| 2026-08 | [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md) | ✓ | 0 | AcceptMoEは、投機的 デコードの検証で対象モデル ルータが本来選ぶエキスパートを全部実行せず、結果へ効きやすいエキスパートだけを残す近似手法である。 |
| 2026-07 | [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md) | ✓ | 0 | 端末上のMixture-of-エキスパート（MoE）推論で、専門家重みをCPUメモリやフラッシュストレージからGPU/NPUへ都度搬送する場合、通常の投機デコードは候補トークンを増やすほどドラフト側・検証側で必要専門家の集合が膨らみ、搬送費が増えて高速化条件を失う。DraftExpertは各MoE層に小さな常駐ドラフト専門家を1個だけ追加し。 |
| 2026-05 | [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md) | [✓](https://github.com/sgl-project/sglang/pull/22272) | 0 | SPECTREが対象にするのは、複数種類のLLMを同じクラウドで提供しているときのGPU利用率の偏りである。 |
| 2026-05 | [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md) | ✓ | 0 | 投機的 デコードの低負荷時の速さだけでなく、リクエスト 率が上がると下書き・検証の負荷依存コストがバッチとともに増えて高速化倍率が縮む現象を、Little's Lawから推定した実効バッチ サイズと少数のコスト係数で説明する提供 遅延 モデル。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-01 | [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md) | [✓](https://github.com/FasterDecoding/Medusa) | 24 | 通常の自己回帰復号（自己回帰 デコード）は、1 トークンを出すたびに大規模LLM全体を1回順伝播する。 |
| 2024-01 | [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md) | [✓](https://github.com/SafeAILab/EAGLE) | 23 | 通常の自己回帰復号（自己回帰 デコード）では、巨大なLLMを1回順伝播しても原則1 トークンしか確定しない。 |
| 2023-05 | [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md) | [✓](https://github.com/flexflow/FlexFlow) | 17 | 通常の自己回帰復号（自己回帰 デコード）では、次トークンを1つ生成してからでないと、その次のトークンを確定できない。この依存関係そのものは言語モデルの意味上必要だが、実装上は大きな問題になる。 |
| 2024-02 | [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md) | [✓](https://github.com/hao-ai-lab/LookaheadDecoding) | 7 | LLMの自己回帰復号（自己回帰 デコード）では、トークン t+1 が確定するまで t+2 を正しく計算できない。 |
| 2023-11 | [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md) | [✓](https://github.com/FasterDecoding/REST) | 3 | 通常の自己回帰復号（自己回帰 デコード）では、対象 LLMを1回順伝播して1 トークンを確定し、そのトークンを入力へ追加して次の順伝播へ進む。 |
<!-- survey:auto:end -->
