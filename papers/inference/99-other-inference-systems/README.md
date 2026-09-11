# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（9本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の本文・メタデータから arXiv ID / DOI の明示参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md) | [✓](https://github.com/ifm-ai/uno) | 0 | Unoは通常の自己回帰（AR）weightに、複数future tokenを並列提案する軽量な離散拡散（discrete diffusion）weightを追加し、Ψ-Spec samplerでそのproposalをAR target distributionへ補正する。別draft modelを常駐させず、同じmodel内の追加weightからmulti-token proposalを作るのが特徴。leading speculative decoding方式より全評価batch sizeで高いthroughputを報告し、base AR model比最大3×。 |
| 2026-09 | [Speculative Macro Commit for Faster Tool-Using Agents](2026-2609.03236-speculative-macro-commit-for-faster-tool-using-agents.md) | ✓ | 0 | ツール利用エージェントでは、モデルが次の操作を決め、外部ツールの結果を待ち、その観測を次の入力へ加える逐次ループが壁時計遅延を支配する。投機的マクロ確定（Speculative Macro Commit; SMC）は、高速なドラフトモデルが隔離した環境状態で複数操作を先行実行し、過去の成功軌跡から採掘した再現性の高い操作列と照合する。権威モデルが先頭操作だけを同じと確認した場合、十分な深さを持つマクロに限って後続のドラフト操作と観測を個別の権威モデル呼び出しなしでまとめて確定する。Qwen3.5-27B INT4を権威モデル、Qwen3.5-4Bをドラフトに用い、τ²-Bench Telecomでは逐次基準と同じ99.52%精度を維持して壁時計時間を18.59%短縮、AppWorldでは44.93%短縮したがTGCは41.67から40.48へ低下した。 |
| 2026-08 | [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md) | ✓ | 0 | Mixture-of-エキスパート（MoE）推論で一般的な高速化を局所性能だけで評価すると、実際のエンドツーエンド性能を誤って見積もる問題を実測した研究。OLMoE-1B-7B、DeepSeek-V2-Lite、Qwen3-30B-A3Bを用い、融合カーネル、4/8ビット量子化、PyTorchのグラフコンパイルを分解して検証する。融合RMSNormは単体で最大8.98倍高速でもモデル全体ではほぼ無効で、OLMoEが約1000回の小さな逐次カーネル起動に律速されることを示す。またINT4で専門家選択が変化しても、その変化自体が説明する品質低下は2.7%に留まり、ルーティング一致率を守ることが品質維持と同義ではないと因果介入で確認する。 |
| 2026-05 | [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md) | ✓ | 0 | 長context向けdynamic sparse attentionとspeculative decodingを単純に組み合わせると、verification queryごとに似たKV blockを別々に選んで何度もHBMから読む。SpecSAは近接queryをgroup化し、各queryの選択集合をon-chipでmergeして重複KVを1回だけ読むexact方式、代表queryのindexを共有する高速な近似方式、layer間index再利用、NSA 3 branchのkernel fusion、promptごとのstrategy再選択を組み合わせてsparse verificationを専用設計する。 |
| 2026-03 | [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md) | ✓ | 1 | LLMのBF16重みには指数部の偏りがあり無損失圧縮できるが、HuffmanやANSのような可変長符号はGPUのSIMT並列性を崩し、復号後の重みを一度グローバルメモリへ展開する方式は余計な読み書きを増やして推論を遅くする。ZipServは各重みの指数を固定長3ビットの三重ビットマップへ符号化するTCA-TBEを用い、デコード時には圧縮重みを読みながらレジスタ上でBF16へ復元してTensor Coreへ直接渡すZipGEMMで中間展開を消す。プリフィルでは復号を別カーネルへ分けてcuBLASを使う段階適応も行う。RTX4090・L40Sなどの実機でモデル重みを最大約30%削減し、ZipGEMMはcuBLAS比最大2.21倍、エンドツーエンドではvLLM比平均1.22倍のスループット向上を報告する。 |
| 2026-01 | [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md) | ✓ | 0 | 同じprefixを含む複数sequenceを1つのbatchで処理するとき、共有prefix部分のMLP・LayerNorm・線形射影をsequenceごとに繰り返さず、同じtoken位置の計算を1回だけ行って結果を各sequenceへ戻すことでprefill計算を削減する。 |

### 直近12か月より前・リポジトリ内で被引用

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-02 | [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md) | [✓](https://github.com/bytedance/flux) | 3 | multi-GPU MoEで、他GPUから必要dataが全部届くまで待たず、届いた小さな行列単位からexpert GEMMを開始してGPU間通信待ちを計算の裏へ隠すruntime。 |
| 2025-06 | [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md) | ✓ | 1 | 通常の投機的decodeではdraft生成→target検証が直列なので、両modelを同じGPU群へ載せるとdraftが終わるまでtarget GPUが待ち、modelごとに最適なtensor parallelismも選べない。SwiftSpecはdraft用GPU群とtarget用GPU群を分離し、draftが次の候補treeを伸ばしている間にtargetが前のtreeを検証する。検証結果に応じてtreeとKV cacheを再rootして有効な枝を再利用し、さらにsmall-batch向け融合kernelで同期・通信overheadを削ることでsingle-request decodeを高速化する。 |

### その他

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-04 | [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md) | ✓ | 0 | 大batch・長contextの投機的decodeでは、draft modelを極端に小さくするよりも、draft自身のKV cache読出し量を固定的に小さくしつつtargetに近い予測をさせる方がthroughput上有利になり得る。SPIReは、sliding-window型の疎KV、target modelからのpruned initialization、過去のtarget activationを使うfeedback memory、蒸留lossを組み合わせた浅いdraft modelを設計し、acceptance率とdraft 1回あたりのmemory/compute costの両方を最適化する。 |
<!-- survey:auto:end -->
