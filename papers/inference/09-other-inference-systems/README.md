# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

## 収録論文

収録論文: 3本。公開日が新しい順。

- 2026-09-03 — [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md)
  - 軽量な追加moduleで複数token候補をまとめて提案し、元の自己回帰modelと同じ出力分布になるよう検証・補正して生成を高速化する。
- 2026-01-21 — [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)
  - 同じprefixを持つsequenceをprefix trieでまとめ、MLP・LayerNorm・線形射影など位置ごとに独立な演算をunique tokenだけに実行してbatch内の重複prefill計算を削減する。
- 2025-02-27 — [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)
  - multi-GPU MoEで、GPU間から届いたdataを全部待たず、届いた小単位からmatrix計算を始めることで通信待ちを計算の裏へ隠す。
