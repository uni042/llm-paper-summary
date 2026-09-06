# Conditional computation

収録論文: 8本。公開日が新しい順。

- 2025-07-27 — [DiffSkip: Differential Layer Skipping in Large Language Models](2025-diffskip-differential-layer-skipping-in-large-language-models.md)
  - 隣接層の表現差分を指標に冗長な層を選択的に飛ばし、品質劣化を抑えてLLM推論を高速化する方式。
- 2025-04-22 — [Dynamic Early Exit in Reasoning Models](2025-2504.15895-dynamic-early-exit-in-reasoning-models.md)
  - 推論途中の確信度から終了可否を動的に判定し、容易な問題ではreasoning modelの計算を早く打ち切る手法。
- 2025-03-31 — [Adaptive Layer-skipping in Pre-trained LLMs](2025-2503.23798-adaptive-layer-skipping-in-pre-trained-llms.md)
  - 入力と層の状態に応じたlayer skippingで、事前学習済みLLMの品質を保ちながら実行深度を削減する方式。
- 2025-03-11 — [Position-Aware Depth Decay Decoding: Boosting Large Language Model Inference Efficiency](2025-2503.08524-position-aware-depth-decay-decoding-boosting-large-language-model-inference-effi.md)
  - 生成位置が後ろになるほど実行深度を減衰させ、KV cacheを保ちながら自己回帰デコードを高速化する手法。
- 2024-12-15 — [D-LLM: A Token Adaptive Computing Resource Allocation Strategy for Large Language Models](2024-d-llm-a-token-adaptive-computing-resource-allocation-strategy-for-large-language.md)
  - トークンの難度に応じて使用するTransformer層を動的に割り当て、LLMの計算量を細粒度に制御する方式。
- 2024-08-12 — [LayerSkip: Enabling Early Exit Inference and Self-Speculative Decoding](2024-layerskip-enabling-early-exit-inference-and-self-speculative-decoding.md)
  - 学習時のlayer dropoutとearly-exit損失により、同一モデルで早期終了とself-speculative decodingを可能にする手法。
- 2024-07-19 — [LazyLLM: Dynamic Token Pruning for Efficient Long Context LLM Inference](2024-2407.14057-lazyllm-dynamic-token-pruning-for-efficient-long-context-llm-inference.md)
  - 長文入力で重要トークンだけを層ごとに選び、後段で再活性化も許す動的token pruningにより推論を高速化する手法。
- 2023-07-05 — [SkipDecode: Autoregressive Skip Decoding with Batching and Caching for Efficient LLM Inference](2023-2307.02628-skipdecode-autoregressive-skip-decoding-with-batching-and-caching-for-efficient-.md)
  - 生成位置とともに実行深度を単調減少させ、batchingとKV cacheを維持したまま自己回帰デコードを高速化する手法。
