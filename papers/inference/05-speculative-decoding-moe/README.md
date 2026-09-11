# Speculative Decoding / MoE

Speculative decodingで1回のtarget LLM実行から複数tokenを確定し、逐次decodeのweight読出し・latencyを減らす研究をまとめる。draft model、追加head、feature予測、retrieval、Jacobi iterationなどの候補生成方式と、tree verificationを含む。

MoEではさらに、検証するtokenやbranchが増えるほど呼び出すexpert数や重み転送量も増えやすいため、受理されそうなdraftだけを選ぶ、必要expertを先読みする、GPU常駐expertを優先する等の研究も含める。

<!-- survey:auto:start -->
## 自動生成の論文一覧（17本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [MoE-SpeQ: Speculative Quantized Decoding with Proactive Expert Prefetching and Offloading for Mixture-of-Experts](2025-2511.14102-moe-speq-speculative-quantized-decoding-with-proactive-expert-prefetching-and-of.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  target MoEの4-bit版を下書きとして使い、トークン候補と将来使うエキスパートの両方を先に予測して、target検証前に必要なエキスパート重みをCPUからGPUへ読み込む方式。

- **2025-10 · [SP-MoE: Speculative Decoding and Prefetching for Accelerating MoE-based Model Inference](2025-2510.10302-sp-moe-speculative-decoding-and-prefetching-for-accelerating-moe-based-model-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  投機的 デコードで下書き トークンを作っている間に、target MoEが検証時に使いそうなエキスパート重みをCPUからGPUへ先読みし、検証開始後の重み待ちを減らす手法。

- **2026-02 · [MoE-Spec: Expert Budgeting for Efficient Speculative Decoding](2026-2602.16052-moe-spec-expert-budgeting-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  Mixture-of-エキスパート（MoE）モデルで木構造の投機デコードを行うと、候補トークンが増えるほど各層で必要になる専門家の和集合が膨らみ、疎な専門家活性化の利点が検証段階で失われる。

- **2026-02 · [MoE-SpAc: Efficient MoE Inference Based on Speculative Activation Utility in Heterogeneous Edge Scenarios](2026-2603.09983-moe-spac-efficient-moe-inference-based-on-speculative-activation-utility-in-hete.md)**  
  実装：[✓](https://github.com/lshAlgorithm/MoE-SpAc) ・ リポジトリ内被引用：2  
  投機的 デコードで少し先に見えるエキスパート需要を利用し、どのエキスパートをGPUへ残す・先読みする・CPUで実行するかをまとめて決めるedge向けMoE推論方式。

- **2026-07 · [Less Experts, Faster Decoding: Cost-Aware Speculative Decoding for Mixture-of-Experts](2026-2607.12696-less-experts-faster-decoding-cost-aware-speculative-decoding-for-mixture-of-expe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  下書き nodeごとに受理される見込みと新しく必要になるエキスパート数を比較し、すでに使う予定のエキスパートを再利用しやすい枝を優先してMoE検証のHBM readを減らす手法。

- **2026-05 · [Making Every Verified Token Count: Adaptive Verification for MoE Speculative Decoding](2026-2605.00342-making-every-verified-token-count-adaptive-verification-for-moe-speculative-deco.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  下書き treeの各候補について受理される見込みと実際の検証時間を比較し、費用対効果の高い枝だけを対象モデル MoEで検証する手法。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Osprey: Target-agnostic Pre-training Makes Stronger Drafters in Speculative Decoding](2026-2609.09338-osprey-target-agnostic-pretraining-speculative-decoding.md)**  
  実装：[✓](https://github.com/LeanModels/Osprey) ・ リポジトリ内被引用：0  
  Ospreyは、投機的デコードのドラフトモデルが特定ターゲットと狭い学習分布へ過度に結び付くことで、分野や言語が変わると受理長が低下する問題を、再利用可能な事前学習済み小型言語モデルの知識で緩和する手法である。Qwen3-4Bなどを数層だけ残して枝刈りし、汎用ウェブ文書で次トークン予測を継続学習した浅い骨格を一度作る。

- **2026-08 · [Vision Is Not Overhead: One-Pass Block Drafting for Lossless Speculative Decoding in Vision-Language Models](2026-2609.00355-glance-vlm-speculative-decoding.md)**  
  実装：[✓](https://github.com/js-lee-AI/GLANCE。実運用比較はSGLang) ・ リポジトリ内被引用：0  
  GLANCEは、凍結したVLM対象モデルが入力処理で作った視覚・言語融合状態から、将来のトークン塊を1回で下書きし、幅のある候補木を対象モデルの1回の処理で検証する無損失の投機的デコーダである。画像に根差した課題では自己回帰方式に対して最大2.93倍となる一方、自由生成の文章では連鎖型下書きが有利になる境界も示す。

- **2026-08 · [AcceptMoE: Commitment-Weighted Self-Sizing Verifier Expert Sets for Efficient MoE Speculative Decoding](2026-2608.02989-acceptmoe-commitment-weighted-self-sizing-verifier-expert-sets-for-efficient-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  下書き枝が対象モデルに受理される見込みとルータ上のエキスパート寄与を合わせて、検証で実行するエキスパート数を層ごとに減らし、オフロード時のホスト→GPU転送を削る近似手法。

- **2026-07 · [DraftExpert: Expansion-Aware Self-Speculative Decoding for End-Device MoE Inference](2026-2607.24434-draftexpert-expansion-aware-self-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末上のMixture-of-エキスパート（MoE）推論で、専門家重みをCPUメモリやフラッシュストレージからGPU/NPUへ都度搬送する場合、通常の投機デコードは候補トークンを増やすほどドラフト側・検証側で必要専門家の集合が膨らみ、搬送費が増えて高速化条件を失う。

- **2026-05 · [SPECTRE: Hybrid Ordinary-Parallel Speculative Serving for Resource-Efficient LLM Inference](2026-2605.08151-spectre-hybrid-ordinary-parallel-speculative-serving.md)**  
  実装：[✓](https://github.com/sgl-project/sglang/pull/22272) ・ リポジトリ内被引用：0  
  複数LLMを同時提供するクラウドでは、人気の大型モデルが混雑する一方、小型モデル用GPUが余ることがある。SPECTREはその空き小型モデルを遠隔下書きモデルとして使って大型モデルの投機的デコードを支援し、下書き生成と大型モデル検証を直列に行う通常型と、両方を重ねる並列型を失敗率に応じて切り替える。

- **2026-05 · [An Interpretable Latency Model for Speculative Decoding in LLM Serving](2026-2605.15051-interpretable-latency-model-speculative-decoding-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的 デコードの低負荷時の速さだけでなく、リクエスト 率が上がると下書き・検証の負荷依存コストがバッチとともに増えて高速化倍率が縮む現象を、Little's Lawから推定した実効バッチ サイズと少数のコスト係数で説明する提供 遅延 モデル。

### 1年以上前

- **2024-01 · [Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](2024-2401.10774-medusa-multiple-decoding-heads.md)**  
  実装：[✓](https://github.com/FasterDecoding/Medusa) ・ リポジトリ内被引用：24  
  Medusaは、投機的復号（投機的 デコード）用に別の小型ドラフト モデルを用意せず、対象 LLM自身の隠れ 状態から複数の未来トークンを予測する小さなヘッドを足す方式である。候補を木構造へまとめて対象 基盤で一括検証し、1回の大きなモデル 順伝播で複数トークンを確定する。

- **2024-01 · [EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](2024-2401.15077-eagle-feature-speculative-sampling.md)**  
  実装：[✓](https://github.com/SafeAILab/EAGLE) ・ リポジトリ内被引用：23  
  EAGLEは、別の小型LLMに未来トークンを予測させる代わりに、対象 LLM内部の高水準な特徴量（特徴量）を小さな1-層 decoderで先読みする投機的復号（投機的 デコード）方式である。

- **2023-05 · [SpecInfer: Accelerating Generative Large Language Model Serving with Tree-based Speculative Inference and Verification](2023-2305.09781-specinfer-tree-speculative-inference.md)**  
  実装：[✓](https://github.com/flexflow/FlexFlow) ・ リポジトリ内被引用：17  
  SpecInferは、通常なら対象 LLMを1 トークンごとに呼ぶところを、小さいモデルが先に複数の未来候補を作り、それらを木構造として対象 LLMにまとめて検査させることで、1回の対象-モデル 処理回から複数トークンを確定しようとするシステムである。

- **2024-02 · [Break the Sequential Dependency of LLM Inference Using Lookahead Decoding](2024-2402.02057-lookahead-decoding.md)**  
  実装：[✓](https://github.com/hao-ai-lab/LookaheadDecoding) ・ リポジトリ内被引用：7  
  先読み デコードは、別の下書きモデルに未来を予測させるのではなく、目標 LLM自身を複数の未来位置へ並列に走らせ、その途中で偶然できた正しそうなn-gramを再利用する方式である。計算量は大きく増やすが、バッチ=1 デコードで余りがちなGPU演算能力を使って逐次ステップ数を減らし、追加モデル・学習・外部コーパスなしで元LLMの出力分布を保つ。

- **2023-11 · [REST: Retrieval-Based Speculative Decoding](2023-2311.08252-rest-retrieval-speculative-decoding.md)**  
  実装：[✓](https://github.com/FasterDecoding/REST) ・ リポジトリ内被引用：3  
  RESTは、投機的復号（投機的 デコード）で必要になる「次に来そうなトークン列」を小型ニューラル ドラフト モデルに作らせる代わりに、大量の既存文章から似た続き方を検索して候補として使う方式である。候補は対象 LLM自身が検証するため、検索が外れても生成品質を犠牲にしない。
<!-- survey:auto:end -->
