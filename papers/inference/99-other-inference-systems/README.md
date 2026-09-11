# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（9本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMのBF16重みには指数部の偏りがあり無損失圧縮できるが、HuffmanやANSのような可変長符号はGPUのSIMT並列性を崩し、復号後の重みを一度グローバルメモリへ展開する方式は余計な読み書きを増やして推論を遅くする。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md)**  
  実装：[✓](https://github.com/ifm-ai/uno) ・ リポジトリ内被引用：0  
  通常の大規模言語モデルは自己回帰（Autoregressive; AR）方式で生成する。1トークン目を出す。

- **2026-09 · [Speculative Macro Commit for Faster Tool-Using Agents](2026-2609.03236-speculative-macro-commit-for-faster-tool-using-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ツール利用エージェントでは、モデルが次の操作を決め、外部ツールの結果を待ち、その観測を次の入力へ加える逐次ループが壁時計遅延を支配する。

- **2026-08 · [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Mixture-of-エキスパート（MoE）推論で一般的な高速化を局所性能だけで評価すると、実際のエンドツーエンド性能を誤って見積もる問題を実測した研究。

- **2026-05 · [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己回帰復号（autoregressive デコード）では、1 トークンを生成するたびに過去のKVキャッシュ（KV キャッシュ）を読む必要がある。

- **2026-01 · [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じプレフィックスを含む複数系列を1つのバッチで処理するとき、共有プレフィックス部分のMLP・LayerNorm・線形射影を系列ごとに繰り返さず、同じトークン位置の計算を1回だけ行って結果を各系列へ戻すことでプリフィル計算を削減する。

### 1年以上前

- **2025-02 · [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/bytedance/flux) ・ リポジトリ内被引用：4  
  Cometは、分散MoEでエキスパート 分配/結合の全対全通信がGEMMを待たせる問題を、通信完了をテンソル全体で待たず、計算に必要な一部分が届いた時点からGEMMを始めることで隠すカーネル/ランタイムである。

- **2025-06 · [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  投機的デコードでは、小さな草稿 モデルが複数の候補トークンを先に生成し、大きな対象 モデルがそれらをまとめて検証する。

- **2025-04 · [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的デコードでは、小さな下書きモデル（下書きモデル）が数トークン先まで候補を生成し、大きな対象モデル（対象モデル）がそれらをまとめて検証する。
<!-- survey:auto:end -->
