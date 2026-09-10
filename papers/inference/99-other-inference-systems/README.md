# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（6本）

| 論文 | 一文要約 |
|---|---|
| [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md) | Unoは通常の自己回帰（AR）weightに、複数future tokenを並列提案する軽量な離散拡散（discrete diffusion）weightを追加し、Ψ-Spec samplerでそのproposalをAR target distributionへ補正する。別draft modelを常駐させず、同じmodel内の追加weightからmulti-token proposalを作るのが特徴。leading speculative decoding方式より全評価batch sizeで高いthroughputを報告し、base AR model比最大3×。 |
| [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md) | 長context向けdynamic sparse attentionとspeculative decodingを単純に組み合わせると、verification queryごとに似たKV blockを別々に選んで何度もHBMから読む。SpecSAは近接queryをgroup化し、各queryの選択集合をon-chipでmergeして重複KVを1回だけ読むexact方式、代表queryのindexを共有する高速な近似方式、layer間index再利用、NSA 3 branchのkernel fusion、promptごとのstrategy再選択を組み合わせてsparse verificationを専用設計する。 |
| [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md) | 通常の投機的decodeではdraft生成→target検証が直列なので、両modelを同じGPU群へ載せるとdraftが終わるまでtarget GPUが待ち、modelごとに最適なtensor parallelismも選べない。SwiftSpecはdraft用GPU群とtarget用GPU群を分離し、draftが次の候補treeを伸ばしている間にtargetが前のtreeを検証する。検証結果に応じてtreeとKV cacheを再rootして有効な枝を再利用し、さらにsmall-batch向け融合kernelで同期・通信overheadを削ることでsingle-request decodeを高速化する。 |
| [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md) | 大batch・長contextの投機的decodeでは、draft modelを極端に小さくするよりも、draft自身のKV cache読出し量を固定的に小さくしつつtargetに近い予測をさせる方がthroughput上有利になり得る。SPIReは、sliding-window型の疎KV、target modelからのpruned initialization、過去のtarget activationを使うfeedback memory、蒸留lossを組み合わせた浅いdraft modelを設計し、acceptance率とdraft 1回あたりのmemory/compute costの両方を最適化する。 |
| [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md) | multi-GPU MoEで、他GPUから必要dataが全部届くまで待たず、届いた小さな行列単位からexpert GEMMを開始してGPU間通信待ちを計算の裏へ隠すruntime。 |
| [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md) | 同じprefixを含む複数sequenceを1つのbatchで処理するとき、共有prefix部分のMLP・LayerNorm・線形射影をsequenceごとに繰り返さず、同じtoken位置の計算を1回だけ行って結果を各sequenceへ戻すことでprefill計算を削減する。 |
<!-- survey:auto:end -->
