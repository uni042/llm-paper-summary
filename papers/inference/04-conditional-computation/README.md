# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（8本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

該当なし。

### 直近12か月・未被引用（2025-10〜2026-09）

該当なし。

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-08 | [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md) | [✓](https://github.com/facebookresearch/LayerSkip) | 7 | 層kipは、同じLLMの浅い層を下書きモデルの代わりに使い、残り層でその下書き トークンを検証する自己投機的 デコードを成立させる学習レシピである。 |
| 2024-07 | [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md) | ✓ | 4 | LazyLLMは、長文入力のすべてのトークンを全層で処理する代わりに、その時点の生成に重要そうな入力トークンだけを後段へ通す学習不要なトークン 枝刈り手法である。 |
| 2023-07 | [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md) | ✓ | 4 | Skipデコードは、各生成トークンに常に全Transformer層を使う代わりに、出力が後ろへ進むほど使う層数を減らす方式である。 |
| 2025-07 | [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md) | ✓ | 0 | DiffSkipは、元LLMのFFNをモデルから削除せずに残し、トークンごとに各FFNを実行するか、小さい代替変換だけで済ませるかをルータで選ぶ動的 skipping手法である。 |
| 2025-04 | [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md) | [✓](https://github.com/iie-ycx/DEER) | 0 | DEERはTransformer 層をスキップする早期終了ではなく、推論モデルが生成する思考連鎖のトークン列を途中で終わらせる手法である。 |
| 2025-03 | [Position-Aware Depth Decay Decoding: Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md) | ✓ | 0 | D3は、生成が後ろへ進むほど使うTransformer 層を減らす学習不要な深度減衰手法である。 |
| 2025-03 | [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md) | [✓](https://github.com/luoxuan-cs/Flexidepth) | 0 | FlexiDepthは、元LLMの重みを固定したまま、トークンごと・層ごとにfull処理か軽いskip経路かを選ぶ追加module型の動的 depth手法である。 |
| 2024-12 | [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md) | [✓](https://github.com/Jyk-122/D-LLM) | 0 | D-LLMは、各トークン・各層ごとに「この層を実行するかskipするか」を学習する動的 depth方式である。 |
<!-- survey:auto:end -->
