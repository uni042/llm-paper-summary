# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

<!-- survey:auto:start -->
## 自動生成の論文一覧（8本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の本文・メタデータから arXiv ID / DOI の明示参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

該当なし。

### 直近12か月より前・リポジトリ内で被引用

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-08 | [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md) | [✓](https://github.com/facebookresearch/LayerSkip) | 5 | 学習時に途中layerからでもnext-token予測できるようmodelを訓練し、推論時は前半layerだけで数tokenを仮生成して、残りlayerでまとめて検証することで、別draft modelなしのspeculative decodingを行う。 |
| 2023-07 | [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md) | ✓ | 4 | 生成が後ろへ進むほど実行するTransformer layer数を段階的に減らし、同じ生成位置ではbatch全体で同じ深度を使うことで、batchingとKV cacheを壊さずdecode計算を減らす。 |
| 2024-07 | [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md) | ✓ | 2 | 長文入力で現在の生成に重要なtokenだけを後続layerへ通し、外したtokenもhidden stateを別cacheへ保存して後で必要になれば途中layerから復帰できるようにすることで、主にprefill計算を減らす。 |

### その他

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-07 | [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md) | ✓ | 0 | tokenごとにFFN前後のhidden state差を見て、表現をほとんど変えないFFNを小さなadapterへ置き換え、固定layer削除より品質を保ちながら計算量を減らす。 |
| 2025-04 | [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md) | [✓](https://github.com/iie-ycx/DEER) | 0 | reasoning途中で一度final answerを試しに生成し、その答えのtoken確率が十分高ければCoTを終了、低ければ試行回答を捨てて元の地点からreasoningを続けるtraining-free手法。 |
| 2025-03 | [Position-Aware Depth Decay Decoding: Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md) | ✓ | 0 | 生成後半ほど実行するlayer数を減らすが、最初と最後のlayerは常に残し、中間layerだけを段階的にskipすることで、KV cacheを保ちながらdecode計算を減らすtraining-free手法。 |
| 2025-03 | [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md) | [✓](https://github.com/luoxuan-cs/Flexidepth) | 0 | tokenごと・layerごとに通常のattention+FFNを実行するか小型adapterだけで済ませるかを選び、skipしたtokenのKVは残すことで文脈を保ちながら計算量を減らす。 |
| 2024-12 | [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md) | [✓](https://github.com/Jyk-122/D-LLM) | 0 | 各token・各layerで『このlayerを実行するか』を小型moduleが判断し、skipしたtokenのKVも後続attentionから外すことで、計算量とKV使用量をtokenごとに変える。 |
<!-- survey:auto:end -->
