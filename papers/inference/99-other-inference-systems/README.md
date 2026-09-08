# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（6本）

| 論文 | 一文要約 |
|---|---|
| [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md) | 投機的検証の複数queryが選ぶsparse KV blockの重なりをまとめて読み、layer間でselection indexを再利用し、draft構成まで含めて適応選択することで長context推論を高速化する。 |
| [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md) | multi-GPU MoEで、他GPUから必要dataが全部届くまで待たず、届いた小さな行列単位からexpert GEMMを開始してGPU間通信待ちを計算の裏へ隠すruntime。 |
| [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md) | 元の自己回帰modelとは別の軽量weightで複数の将来token候補を並列に作り、その候補を元modelと同じ確率分布になるよう補正して、出力分布を変えずに生成を高速化するUno方式。 |
| [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md) | 同じprefixを含む複数sequenceを1つのbatchで処理するとき、共有prefix部分のMLP・LayerNorm・線形射影をsequenceごとに繰り返さず、同じtoken位置の計算を1回だけ行って結果を各sequenceへ戻すことでprefill計算を削減する。 |
| [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md) | 小型draft modelの生成と大型target modelの検証を非同期・分離して独立にscaleし、**draft待ちをtargetのcritical pathから外しながら、tree状候補生成・KV管理・低latency kernelを組み合わせる**ことで単一requestのdecode latencyを下げるsystem。 |
| [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md) | 大batchでdraft model自身のKV cacheと計算が重くなる問題に対し、**静的sparse attention、pruned initialization、過去情報を保持するfeedback memoryを持つ軽量draft model**を使い、speculative decodingのthroughputを高める。 |
<!-- survey:auto:end -->
