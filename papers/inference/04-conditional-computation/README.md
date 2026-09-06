# Conditional Computation

入力やtokenの難しさに応じて、**実行するlayer数、処理するtoken数、終了位置などを変え、不要な計算を最初から行わない**研究をまとめる。全tokenが全layerを必ず通る通常の実行を崩し、layer skipping、early exit、token pruningなどで計算量を減らす。

MoEのexpert数を変えるAdaptive Expert Computationとは対象が異なり、この系統では主にTransformer本体の実行深度や処理対象tokenを動的に変える。

## 収録論文

収録論文: 8本。公開日が新しい順。

- 2025-07-27 — [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)
  - 前後のlayerで表現がほとんど変わらない箇所を冗長とみなし、そのlayerを選択的に飛ばして計算量を減らす。
- 2025-04-22 — [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)
  - reasoning途中の内部状態から答えが十分固まったかを判定し、容易な問題では追加の思考token生成を早く終了する。
- 2025-03-31 — [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)
  - 入力内容と現在のhidden stateに応じて通過するlayerを変え、必要な計算だけを実行する。
- 2025-03-11 — [Position-Aware Depth Decay Decoding: Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)
  - 生成が進むほど使用するlayer数を段階的に減らし、KV cacheの利用を維持したまま後半tokenの計算を軽くする。
- 2024-12-15 — [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)
  - tokenごとの難しさを見積もり、難しいtokenには多く、容易なtokenには少ないlayerを割り当てる。
- 2024-08-12 — [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)
  - 学習時に途中layerからでもtoken予測できるようにしておき、推論では途中終了や同一モデル内のspeculative decodingに利用する。
- 2024-07-19 — [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)
  - 長いpromptの中からlayerごとに重要なtokenだけを残して処理し、必要になったtokenは後のlayerで再び使えるようにする。
- 2023-07-05 — [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)
  - 生成位置が後ろになるほど通過layerを減らす固定ルールを使い、batchingやKV cacheを崩さずdecode計算を削減する。
