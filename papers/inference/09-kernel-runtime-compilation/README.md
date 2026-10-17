# Kernel / Runtime Compilation

GPUカーネル生成・融合・メガカーネル化・JIT/グラフ実行・実行時コンパイルなど、LLM推論の演算実装そのものを生成・統合・配置して起動やメモリ往復のオーバーヘッドを減らす研究をまとめる。

## 分類境界

主要貢献がGPUカーネル、コンパイラ、JIT、メガカーネル、演算融合またはそれらの実行時生成・配置である論文を含め、単なるserving policyや量子化手法だけを主貢献とする論文は含めない。

### 含める研究

- GPUカーネル生成・融合・メガカーネル化
- JIT・CUDA Graph・実行時コンパイル
- LLM演算向けコンパイラ／カーネル自動最適化

### 含めない研究

- 要求スケジューリングだけを主題とするserving研究
- 量子化形式そのものが主貢献でカーネル最適化が従属的な研究

## 近傍系統

- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)
- [06-moe-quantization-compression](../06-moe-quantization-compression/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（109本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-03 · [FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling](2026-2603.05451-flashattention-4-algorithm-and-kernel-pipelining-co-design-for-asymmetri.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention/tree/main/flash_attn/cute) ・ リポジトリ内被引用：14  
  FlashAttention-4は、NVIDIA Blackwell世代のB200でテンソルコアの行列積性能が大きく増加した一方、共有メモリの読出し帯域や指数関数演算器の性能が同じ比率では伸びないことに対応する注意カーネルである。FlashAttention-4は前向き・逆向きの処理を別々に設計し、行列積、softmax、メモリ転送、勾配集約を重ね合わせる。

- **2025-12 · [SonicMoE: Accelerating MoE with IO and Tile-aware Optimizations](2025-2512.14080-sonicmoe-accelerating-moe-with-io-and-tile-aware-optimizations.md)**  
  実装：[✓](https://github.com/Dao-AILab/sonic-moe) ・ リポジトリ内被引用：9  
  SonicMoEは混合専門家モデル（Mixture-of-Experts、MoE）の学習を対象に、専門家の細粒度化と高疎性化によって生じる三種類の非効率を同時に減らす。ICLR 2026正式版では、7B級の細粒度MoEでScatterMoEに対する活性値メモリ削減45%、Hopper世代GPUでの計算処理量1.86倍を報告する。

- **2025-12 · [MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs](2025-2512.22219-mirage-persistent-kernel-mega-kernel-runtime.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：9  
  演算子単位の多数カーネル起動をSM粒度の依存グラフへ分解し、単一常駐巨大カーネル内の分散スケジューラで演算・通信・タスク間パイプラインを重ね、vLLM/SGLang比で最大1.7倍の推論遅延改善を示す。

- **2026-01 · [FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems](2026-2601.00227-flashinfer-bench-ai-driven-kernel-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  実LLM serving由来のGPUカーネル課題を統一トレースで検証し、エージェント生成カーネルをSGLang/vLLMへ低オーバーヘッドで動的適用する閉ループ基盤。

- **2026-03 · [Mamba-3: Improved Sequence Modeling using State Space Principles](2026-2603.15569-mamba-3-improved-sequence-modeling-using-state-space-principles.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：3  
  Mamba-3は、状態空間モデル（State Space モデル、SSM）を使う系列モデルを学習時の並列性だけでなく推論時の実行効率から設計し直す研究である。

- **2026-04 · [Open-TQ-Metal: Fused Compressed-Domain Attention for Long-Context LLM Inference on Apple Silicon](2026-2604.16957-open-tq-metal-fused-compressed-domain-attention-for-long-context-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  70B級モデルを端末上で動かすとき、重みを4ビット化しても長文脈の鍵・値（KV）キャッシュが巨大になる。合計約79.1GBとなり、64GBの統合メモリを持つMacには収まらない。Llama 3.1 70Bの128K文脈では、注意カーネル単体が逆量子化後に注意を実行する方式の480.6msから9.9msへ短縮され、約48倍となる。

- **2026-04 · [FoE: Forest of Errors Makes the First Solution the Best in Large Reasoning Models](2026-2604.02967-foe-forest-of-errors-makes-the-first-solution-the-best-in-large-reasonin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案手法RED（Refine First and Discard Subs）は、最初の解法を生成している途中で不確実性が高い箇所へ介入し、別解を無制限に増やす代わりに、複数の中間回答が十分に一致した時点で停止する。6種類の推論モデル、数学・科学の5課題で、通常復号と比較して正答率を改善しつつ生成トークンを37.7～70.4%削減した。

- **2026-04 · [Event Tensor: A Unified Abstraction for Compiling Dynamic Megakernel](2026-2604.13327-event-tensor-dynamic-megakernel-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  タイル依存関係を記号形状のイベントテンソルとして表し、可変形状とMoEのデータ依存分岐を再コンパイルせず静的・動的メガカーネルへ変換するコンパイラ抽象。

- **2026-03 · [WaterSIC: Information-Theoretically (Near) Optimal Linear Layer Quantization](2026-2603.04956-watersic-information-theoretically-near-optimal-linear-layer-quantizatio.md)**  
  実装：[✓](https://github.com/egorlifar/watersic) ・ リポジトリ内被引用：1  
  WaterSICは、大規模言語モデルの線形層を学習後量子化（post-学習 量子化）するとき、入力チャネルごとに異なる格子幅を与えることで、同じ圧縮容量でも出力のずれを小さくする手法である。ただし論文が評価する主軸は品質対圧縮率であり、llama.cppなどの推論器に載せたトークン/秒、展開カーネルの速度、メモリ帯域削減の実測ではない。

- **2026-02 · [WildCat: Near-Linear Attention in Theory and Practice](2026-2602.10056-wildcat-near-linear-attention-in-theory-and-practice.md)**  
  実装：[✓](https://github.com/microsoft/wildcat) ・ リポジトリ内被引用：1  
  WildCatは、長い入力に対する注意機構の二乗計算量を減らすため、全ての鍵をそのまま参照する代わりに少数の代表鍵を選び、残りの鍵の寄与を最適な重みへ集約する近似注意方式である。

- **2026-02 · [PackInfer: Compute- and I/O-Efficient Attention for Batched LLM Inference](2026-2602.06072-packinfer-batched-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  異種長要求を負荷均衡した群へ詰め、共有接頭辞を考慮した連続KV配置と一体化することで、注意計算の無駄と入出力断片化を同時に削減する。

- **2026-02 · [Deep Kernel Fusion for Transformers](2026-2602.11808-deep-kernel-fusion-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SwiGLU前半を単一CUDAカーネルへ深く融合して中間活性のHBM往復を削減し、事前プロファイルでGPU・バッチ別のタイル方式を選んでSGLangのデコードを最大13.2%高速化する。

- **2025-12 · [MemEvolve: Meta-Evolution of Agent Memory Systems](2025-2512.18746-memevolve-meta-evolution-of-agent-memory-systems.md)**  
  実装：[✓](https://github.com/bingreeky/MemEvolve) ・ リポジトリ内被引用：1  
  しかし既存の自己改善型エージェントでは、記憶をどの形式で要約するか、どこへ保存するか、いつ検索するか、どの記憶を忘れるかといった記憶機構の設計自体は人手で固定されていることが多い。

- **2025-11 · [KernelBand: Steering LLM-based Kernel Optimization via Hardware-Aware Multi-Armed Bandits](2025-2511.18868-kernelband-steering-llm-based-kernel-optimization-via-hardware-aware-mul.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  高性能な実装では、演算量だけでなく、レジスタ圧迫、共有メモリ、キャッシュ利用、メモリ帯域、スレッド配置を同時に考える必要がある。KernelBandは、この探索判断を文脈付き多腕バンディット（contextual multi-armed bandit、MAB）へ置き換える方式である。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [VC-Attention: Value Smoothing and Softmax Casting for Low-bit Attention](2026-2609.15810-vc-attention-value-smoothing-and-softmax-casting-for-low-bit-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VC-注意機構は、動画拡散変換器（Diffusion Transformer、DiT）の長い時空間系列に対して、低ビット注意機構の値行列Vの量子化誤差と高精度ソフトマックス演算の律速を同時に減らす、追加学習不要のGPUカーネル方式である。

- **2026-09 · [Unfolding the Leech Lattice: Fused Multi-Shell Decoding and VRAM Layouts for 2-Bit LLM Weights](2026-2609.02652-unfolding-the-leech-lattice-fused-multi-shell-decoding-and-vram-layouts-.md)**  
  実装：[✓](https://github.com/pjmalandrino/llvq) ・ リポジトリ内被引用：0  
  本論文は、Leech格子ベクトル量子化（Leech-lattice vector 量子化; LLVQ）を「2 bit/重みで保存できる」という圧縮アルゴリズムの段階から、実際のGPUデコードへ載せる段階まで実装し、そのとき生じる保存bit数と実行時VRAM bit数の乖離を測るシステム研究である。

- **2026-09 · [Understanding LLM Quantization through Activation-Guided Compensation and Orthogonal Residuals](2026-2609.21450-understanding-llm-quantization-through-activation-guided-compensation-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みと活性値をともに4ビットへ縮小する学習後量子化では、特定の活性値チャネルに継続的に現れる大きな値が、量子化に使用する尺度を広げ、通常値に割り当てられる表現段階を粗くする。

- **2026-09 · [KV-Kaizen: Learning Context-Adaptive Cache Compression Choices](2026-2609.37988-kv-kaizen-learning-context-adaptive-cache-compression-choices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  例えばQwen2.5-14Bの非圧縮キャッシュは1トークン当たり192 KiBを占め、8,000トークンの系列32本を同時に保持すると約48 GiBに達する。Qwen2.5-14Bの16K文脈では、提案法による4倍圧縮とSnapKVによる8分の1トークン保持を組み合わせ、復号時KV容量を32分の1にして質問応答精度0.531を得た。

- **2026-09 · [AttnFuse: A Composable DSL for Compiling Attentions to Fused GPU Kernels](2026-2609.13612-attnfuse-a-composable-dsl-for-compiling-attentions-to-fused-gpu-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しい注意方式を論文で定義できても、そのまま高速に実行できるとは限らない。注意はクエリとキーの行列積、マスク、正規化、値との積などを繰り返し、処理を別々のGPUカーネルで行うと中間テンソルの書込みと再読込みが生じる。

- **2026-09 · [Accelerating the Mitigation of LLM Inference Nondeterminism Across GPU Architectures](2026-2609.25624-accelerating-the-mitigation-of-llm-inference-nondeterminism-across-gpu-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が扱うのは、乱数を固定し、温度を0にした貪欲復号でも、同じ大規模言語モデル（LLM）がGPUの世代や同時処理数によって異なるトークンを出す問題である。これは「丸め差が十分小さければ結果がたまたま一致する」という従来の確率的対策ではなく、対象線形層に限り演算順を構造的に一致させる設計である。

- **2026-08 · [UnionSparse: An Index-Efficient Sparsity Framework for Low-Bit Sparse LLM Inference on Edge](2026-2608.09291-unionsparse-index-efficient-low-bit-sparse-inference.md)**  
  実装：[✓](https://github.com/Victor-Alen/UnionSparse) ・ リポジトリ内被引用：0  
  低ビット化で相対的に増える疎行列の位置情報負担をPMRで定量化し、共有ビットマップ表現と並列復号カーネルを共同設計してJetson上の小バッチ疎推論を高速化する。

- **2026-08 · [MonoMoE: An Efficient Fused Mega-kernel for Quantized MoE Decoding](2026-2609.04244-monomoe-fused-megakernel-quantized-moe-decoding.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer/tree/main/csrc/fused_moe/monomoe) ・ リポジトリ内被引用：0  
  少トークンMoE復号を重み主導型の常駐巨大カーネルへ再構成し、ルーティングから二段の専門家射影と縮約までを融合してメモリ帯域利用を高める。

- **2026-08 · [Celty: SpMspV GPU Kernel and SIMT Co-Design for Efficient Dual-Sparse LLM Inference](2026-2608.01536-celty-dual-sparse-gpu-kernel.md)**  
  実装：[✓](https://github.com/RuokaiYin/Celty) ・ リポジトリ内被引用：0  
  重み疎性と実行時活性疎性の交差を疎行列×疎ベクトルとして扱い、走長圧縮形式、ワープ割当、レジスタ部分和、専用復号器を共同設計して低バッチLLMデコードを高速化する。

- **2026-08 · [A Thread-Register Decoupled GPU Execution Model for Efficient Tensor Computation](2026-2608.19628-fiber-thread-register-decoupled-gpu-execution.md)**  
  実装：[✓](https://github.com/SJTU-ReArch-Group/GTSim/) ・ リポジトリ内被引用：0  
  FIBERはGPUの実行単位から私有レジスタ所有を切り離し、SM内共有レジスタ、動的な並列度変更、レジスタ単位の依存追跡を組み合わせる。LLMのGEMMと非GEMMが交互に現れる処理を対象に、シミュレータ上でAmpere 2.25倍、Hopper 1.8倍、Blackwell 2.09倍のエンドツーエンド高速化を報告する。

- **2026-07 · [Harness Engineering for LLM-Driven GPU Kernel Generation](2026-2607.17979-harness-engineering-llm-gpu-kernels.md)**  
  実装：[✓](https://github.com/syhya/mlsys26-flashinfer-contest) ・ リポジトリ内被引用：0  
  LLM生成GPUカーネルを、公式準拠のコンパイル・正当性・計時・全形状評価とプロファイル駆動の保守的昇格ループで管理し、B200上の5演算子でFlashInfer比1.12〜29.68倍を得たハーネス設計。

- **2026-06 · [Prefilling-dLLM: Predictive Prefilling for Long-Context Inference in Diffusion Language Models](2026-2606.10537-prefilling-dllm-predictive-prefilling-for-long-context-inference-in-diff.md)**  
  実装：[✓](https://github.com/menik1126/Prefilling-dLLM) ・ リポジトリ内被引用：0  
  Prefilling-dLLMは、この入力接頭辞を長さ一定の小区間へ分け、各区間の鍵・値（Key–Value、KV）表現を事前に一度だけ計算し、問い合わせに関係する区間だけを残して反復的な雑音除去（denoising）に再利用する方式である。

- **2026-06 · [FOCUS: DLLMs Know How to Tame Their Compute Bound](2026-2601.23278-focus-dllms-know-how-to-tame-their-compute-bound.md)**  
  実装：[✓](https://github.com/sands-lab/FOCUS) ・ リポジトリ内被引用：0  
  拡散型言語モデル（diffusion language モデル、DLLM）は、マスクされた複数のトークンを一つのブロックとして反復的に復元する。自己回帰型言語モデルと違い、各反復でブロック内の複数位置を同時に処理できるが、実際に確定する位置が少ないと大部分の計算は次の反復でやり直される。直近の確定数と差分の分布から保持予算を決め、上位候補を残す。

- **2026-06 · [ERA: Entropy-Guided Visual Token Pruning with Rectified Attention for Efficient MLLMs](2026-2606.31982-era-entropy-guided-visual-token-pruning-with-rectified-attention-for-eff.md)**  
  実装：[✓](https://github.com/924973292/ERA) ・ リポジトリ内被引用：0  
  画像内の似た領域を一つの代表トークンへ統合すれば系列長は短くなるが、代表トークンの特徴ベクトルを平均しただけでは、注意機構がその領域に与える総重みを正しく保てない。LLaVA-1.5-7Bでは576個の視覚トークンを32個に減らしたとき、九評価の平均性能維持率93.4%を報告する。

- **2026-06 · [Approaching Shannon Bound with Lossless LLM Weight Compression](2026-2606.15789-shannon-bound-lossless-weight-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GEMMタイルごとにANSで重みを損失なく圧縮し、共有メモリへ復号しながらテンソルコア計算と重ねることで、Mixtral-176Bの最大バッチを20から95へ増やし、SGLangスループットを最大1.6倍にする。

- **2026-06 · [AgentCompile: An LLM-Guided Compiler for Direct CUDA Inference](2026-2606.07665-agentcompile-llm-guided-direct-cuda-inference.md)**  
  実装：[✓](https://github.com/veneno1213822/AgentCompile) ・ リポジトリ内被引用：0  
  大規模言語モデルによるCUDA生成をコンパイラ契約・数値検証・実測性能選択で囲い込み、合格した復号カーネルだけを採用して既存実装へ安全にフォールバックできる推論コンパイラ。

- **2026-06 · [Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices](2026-2607.08786-moderately-unstructured-sparse-gpu-inference.md)**  
  実装：[✓](https://github.com/moui0/cudac) ・ リポジトリ内被引用：0  
  約50%の非構造疎重みを2:4疎テンソルコア層・差分距離で再配置する補助層・微小残差層へ分解し、疎テンソルコアとCUDAコアを重ねて実行してSpInfer比最大1.64倍を達成する。

- **2026-05 · [ViBE: Co-Optimizing Workload Skew and Hardware Variability for MoE Serving](2026-2606.00735-vibe-co-optimizing-workload-skew-and-hardware-variability-for-moe-servin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート; MoE）の分散推論では、入力トークンに応じて選択される専門家（専門家）が偏る。専門家並列（専門家 parallelism; EP）では各GPUが担当する専門家を処理した後に同期するため、あるGPUの処理が遅いと層全体が待たされる。したがってトークン数が等しくても実行時間は等しくならない。

- **2026-05 · [ThriftAttention: Selective Mixed Precision for Long-Context FP4 Attention](2026-2605.23081-thriftattention-selective-mixed-precision-for-long-context-fp4-attention.md)**  
  実装：[✓](https://github.com/joesharratt1229/ThriftAttention) ・ リポジトリ内被引用：0  
  Blackwell世代のGPUは4ビット浮動小数点（FP4）の行列積を高速に処理できるため、注意計算を16ビット浮動小数点（FP16）からFP4へ落とせば演算とメモリ転送を軽くできる。ThriftAttentionは、全ての問い合わせ・鍵の組を捨てず、重要なブロックだけFP16へ戻す方式である。

- **2026-05 · [Self-Pruned Key-Value Attention: Learning When to Write by Predicting Future Utility](2026-2605.14037-self-pruned-key-value-attention-learning-when-to-write-by-predicting-fut.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長い会話、検索拡張生成、エージェントの反復処理ではKVキャッシュの容量とメモリ帯域がボトルネックとなる。読出し時だけ重要なKVを選ぶ疎注意方式は計算量を減らせるが、全KVを保存し続ける限り容量の増加は止まらない。

- **2026-05 · [Parallax: Parameterized Local Linear Attention for Language Modeling](2026-2605.29157-parallax-parameterized-local-linear-attention-for-language-modeling.md)**  
  実装：[✓](https://github.com/Yifei-Zuo/Parallax) ・ リポジトリ内被引用：0  
  Parallaxは、通常のSoftmax注意の「入力クエリに近いキーへ重みを置いて値を平均する」という計算に、キーと値の局所的な相互共分散を使った補正を加える注意機構である。H200でのBF16復号カーネルの測定では、比較対象のFlashAttention 2/3の速い方に対し、測定したバッチ・文脈長の範囲で同等以上と著者らは報告する。

- **2026-05 · [Memory-Bound but Not Bandwidth-Limited: The Physical AI Inference Gap in Batch-1 LLM Decode](2026-2605.30571-memory-bound-but-not-bandwidth-limited-the-physical-ai-inference-gap-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  研究の中心は新しい注意演算を発明することではなく、既存の復号経路で、メモリ転送、CPUからのGPUカーネル起動、量子化カーネルの適合性を切り分ける測定設計にある。

- **2026-05 · [KVBuffer: IO-aware Serving for Linear Attention](2026-2605.19049-kvbuffer-io-aware-serving-for-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVBufferは、線形注意（linear 注意機構）を使う大規模言語モデル（LLM）の推論サービングにおいて、毎トークン更新される大きな内部状態へのメモリアクセスを減らすための機構である。

- **2026-05 · [Improving the Efficiency of Language Agent Teams with Adaptive Task Graphs](2026-2605.06320-improving-the-efficiency-of-language-agent-teams-with-adaptive-task-grap.md)**  
  実装：[✓](https://github.com/emieczkowski/latte) ・ リポジトリ内被引用：0  
  複数の大規模言語モデル（LLM）を役割分担して実行するエージェントシステムでは、同じ作業の重複、ファイルの競合更新、長い通信、担当者の待機が発生しやすい。LATTEの成功試行集計は平均148,000トークン、3.5分、成功率約80%で、固定グラフ方式の297,000トークン、6.0分、58%より効率と成功率が高い。

- **2026-05 · [GPU Forecasters: Language Models as Selective Surrogates for Kernel Runtime Optimization](2026-2605.31464-gpu-forecasters-kernel-runtime-surrogates.md)**  
  実装：[✓](https://github.com/codezakh/gpu-forecasters) ・ リポジトリ内被引用：0  
  実GPU計測をLLMの相対速度予測で選択的に代替し、同じGPU計測予算で候補数を4倍へ広げて6課題中4課題で基準と同等以上の高速カーネルを発見する。

- **2026-05 · [Ada-MK: Adaptive MegaKernel Optimization via Automated DAG-based Search for LLM Inference](2026-2605.11581-ada-mk-adaptive-megakernel-compilation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Ada-MKはLLMデコードをPTX命令水準の依存グラフへ分解し、共有メモリ配置とワープ役割をオフライン探索して分岐のないメガカーネルを生成し、L20でTensorRT-LLM比最大23.6%高速化する。

- **2026-04 · [Nautilus: An Auto-Scheduling Tensor Compiler for Efficient Tiled GPU Kernels](2026-2604.14825-nautilus-an-auto-scheduling-tensor-compiler-for-efficient-tiled-gpu-kern.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の注意計算を高速化するには、数学的に同じ式でも、演算の融合、行列の分割幅、共有メモリの配置、並列実行単位、GPU世代ごとの命令特性を考慮しなければならない。FlashAttention系のカーネルはこれらを手作業で高度に調整してきた。

- **2026-04 · [Hybrid JIT-CUDA Graph Optimization for Low-Latency Large Language Model Inference](2026-2604.23467-hybrid-jit-cuda-graph-low-latency-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  静的Transformer演算をCUDA Graph再生、動的制御を実行時コンパイルへ分け、短系列・バッチ1推論の起動オーバーヘッドと尾部遅延を削減する。

- **2026-04 · [Evaluating CUDA Tile for AI Workloads on Hopper and Blackwell GPUs](2026-2604.23466-evaluating-cuda-tile-for-ai-workloads-on-hopper-and-blackwell-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、NVIDIAのタイル単位GPUプログラミング基盤CUDA Tile（CuTile）を採用すべき条件を、性能と開発工数の両面から実測した比較研究である。CuTileは行列積や注意計算をタイル演算として記述し、スレッド束、共有メモリ配置、レジスタ割当の一部をコンパイラへ任せる。主要結果は二面的である。

- **2026-04 · [Active Imitation Learning for Thermal- and Kernel-Aware LFM Inference on 3D S-NUCA Many-Cores](2026-2604.11948-active-imitation-learning-for-thermal-and-kernel-aware-lfm-inference-on-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案方式AILFM（Active Imitation Learning for LFMs）は、コアごとの命令実行率、最終段キャッシュのミス率、平均キャッシュ距離、電力予算、温度を観測し、どのカーネルをどのコアに割り当てると温度上限を守りながら実行時間を短縮できるかを判断する。

- **2026-03 · [Scaling Attention via Feature Sparsity](2026-2603.22300-scaling-attention-via-feature-sparsity.md)**  
  実装：[✓](https://github.com/YannX1e/Sparse-Feature-Attention) ・ リポジトリ内被引用：0  
  一方、クエリ・キーの次元そのものを小さくする方法は、各トークンの表現力を減らすため、特定の推論・検索課題で精度を落とし得る。本論文の疎特徴注意（Sparse Feature 注意機構、SFA）は別の軸を選ぶ。

- **2026-03 · [Model2Kernel: Model-Aware Symbolic Execution For Safe CUDA Kernels](2026-2603.24595-model2kernel-safe-cuda-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル側からCUDA呼出し条件を抽出するHFProbeと、動的テンソル・全CUDAスレッドを記号化するcuKLEEを組み合わせ、LLM推論カーネルの未知メモリバグ353件を9誤検出で検出した。

- **2026-03 · [Mixture-of-Depths Attention](2026-2603.15619-mixture-of-depths-attention.md)**  
  実装：[✓](https://github.com/hustvl/MoDA) ・ リポジトリ内被引用：0  
  Mixture-of-Depths 注意機構（MoDA）は、深い大規模言語モデル（Large Language モデル; LLM）で浅い層に形成された情報が、繰り返す残差更新により後段で薄まる問題を対象とする。

- **2026-03 · [Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts](2026-2603.07169-cudamaster-multi-scenario-kernel-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  50演算×FP32/BF16のMSKernelBenchと、律速別に選別したNsight Compute情報を計画・実装・コンパイル・デバッグの4担当へ渡すCUDAMasterで、多領域CUDA最適化を自動化し、o4-miniで正当性100%・基準超え94%を達成する。

- **2026-03 · [Kernel-Smith: A Unified Recipe for Evolutionary Kernel Optimization](2026-2603.28342-kernel-smith-a-unified-recipe-for-evolutionary-kernel-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM推論エンジンの実効性能は、モデル演算そのものだけでなく、GPU上で実行される個別カーネルの融合、メモリ移動、起動費用、並列化に左右される。しかし一度だけコードを生成する方式は、コンパイルできても数値が間違っていたり、正しくても実測速度が遅かったりする。

- **2026-03 · [FlashSampling: Fast and Memory-Efficient Exact Sampling](2026-2603.15854-flashsampling-fast-and-memory-efficient-exact-sampling.md)**  
  実装：[✓](https://github.com/FlashSampling/FlashSampling) ・ リポジトリ内被引用：0  
  一般的な実装では、この語彙投影を行列積として実行し、バッチ数×語彙数のロジット配列をGPUの高帯域メモリ（HBM）へ保存する。一次論文第3版は、H100、H200、B200、B300の4種類のGPUでのカーネル単体測定と、B200上でのvLLMへの統合測定を報告する。

- **2026-02 · [OptiML: An End-to-End Framework for Program Synthesis and CUDA Kernel Optimization](2026-2602.12305-optiml-an-end-to-end-framework-for-program-synthesis-and-cuda-kernel-opt.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OptiMLは、大規模言語モデルによるCUDAカーネルの初期生成と、その後の正しさを保つ性能改善を単一の開発経路へまとめる方式である。

- **2026-02 · [On State Reduction in Linear Attention](2026-2602.04852-on-state-reduction-in-linear-attention.md)**  
  実装：[✓](https://github.com/camail-official/LinearAttentionPruning) ・ リポジトリ内被引用：0  
  線形注意（linear 注意機構）は、通常のソフトマックス注意と異なり、過去のトークンを固定サイズの行列型状態へ逐次圧縮できる。Gated DeltaNet 1.3Bでは、状態次元を50%削減し回復用微調整を行った場合、WikiText-2困惑度は元モデル16.8に対しDRRQRで16.3、ゼロショット平均精度は59.4から58.0となった。

- **2026-01 · [Understanding Efficiency: Quantization, Batching, and Serving Strategies in LLM Energy Use](2026-2601.22362-understanding-efficiency-quantization-batching-and-serving-strategies-in.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の推論電力量は、モデルのパラメータ数や重みのビット幅だけでは決まらない。同じモデルを同じGPUで実行しても、事前充填（プリフィル）と逐次復号（デコード）では計算律速かメモリ律速かが異なり、要求を逐次処理するか連続バッチ化するかによってGPUの待機時間が大きく変わる。重要な結論は三つある。

- **2026-01 · [Syncopate: Efficient Multi-GPU AI Kernels via Automatic Chunk-Centric Compute-Communication Overlap](2026-2601.20595-syncopate-efficient-multi-gpu-ai-kernels-via-automatic-chunk-centric-com.md)**  
  実装：[✓](https://github.com/tie-pilot-qxw/syncopate) ・ リポジトリ内被引用：0  
  通信と計算を異なるCUDAストリームで同時実行する従来方式は、しばしばカーネル全体を単位として重ねるため、入力データの一部が先に到着しても、その部分を処理する計算を開始できない。全体平均1.3倍、最大4.7倍の高速化を報告し、特定の高度に最適化された手書き行列積と比較した性能は4GPU時で平均99.8%、8GPU時で104%だった。

- **2026-01 · [SD-E2: Semantic Exploration for Reasoning Under Token Budgets](2026-2601.17982-sd-e2-semantic-exploration-for-reasoning-under-token-budgets.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型言語モデルに複雑な問題を解かせる際、複数の解法を試すことは有効だが、生成トークン数には限りがある。結果・形式・長さを用いるGRPO-CFLの76.80%、意味を考慮しない探索・活用方式GRPO-CFEEの80.52%も上回る。

- **2026-01 · [LatencyPrism: Online Non-intrusive Latency Sculpting for SLO-Guaranteed LLM Inference](2026-2601.09258-latencyprism-online-non-intrusive-latency-sculpting-for-slo-guaranteed-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LatencyPrismは、本番の大規模言語モデル（LLM）推論で、ユーザーの体感品質に影響する遅延の一時的な増大を、サービスを止めずに検知し、原因の切り分けに必要な実行情報を取得するシステムである。

- **2025-12 · [KV Admission: Learning What to Write for Efficient Long-Context LLM Inference](2025-2512.17452-kv-admission-learning-what-to-write-for-efficient-long-context-llm-infer.md)**  
  実装：[✓](https://github.com/EMCLab-Sinica/WG-KV) ・ リポジトリ内被引用：0  
  KV破棄（追い出し）は容量を制限できる一方、一度書いたKVを後で捨てるため、不要な書込みや一時的なメモリ使用を防ぎにくい。本論文はこの二方式に先立つ第三の操作として、KV受入れ（admission）を明示的に定式化する。

- **2025-12 · [gpu_ext: Extensible OS Policies for GPUs via eBPF](2025-2512.12615-gpu-ext-extensible-os-policies-for-gpus-via-ebpf.md)**  
  実装：[✓](https://github.com/eunomia-bpf/gpu_ext) ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）の推論性能は、GPUの演算能力だけでなく、GPUメモリへ何を保持し、何をCPU側へ退避させ、いつ事前読み込みし、複数処理へどのように実行時間を割り当てるかに大きく左右される。

- **2025-12 · [Dynamic Large Concept Models: Latent Reasoning in an Adaptive Semantic Space](2025-2512.24617-dynamic-large-concept-models-latent-reasoning-in-an-adaptive-semantic-sp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  原著は平均4トークンを1概念へ圧縮するR=4の条件を中心に、通常の1.3B Transformerと、概念段に容量を再配分した2.3B DLCMを比較した。両者の推論浮動小数点演算量（FLOPs）を近づけた条件で、12種類のゼロショット課題の平均正解率は41.23%から43.92%へ2.69ポイント改善した。

- **2025-11 · [You Had One Job: Per-Task Quantization Using LLMs’ Hidden Representations](2025-2511.06516-you-had-one-job-per-task-quantization-using-llms-hidden-representations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  一般的な学習後量子化（Post-学習 量子化; PTQ）は、言語モデルの重みを一律に4ビットへ圧縮したり、重み再構成誤差に基づいて精度を選んだりする。原著第4版では、Qwen2.5-7B-InstructのMMLU-Proで、TAQ-KLが35.35点・重み5.95GB、均一4ビットのAWQが23.54点・5.19GBだった。

- **2025-11 · [HipKittens: Fast and Furious AMD Kernels](2025-2511.08083-hipkittens-fast-and-furious-amd-kernels.md)**  
  実装：[✓](https://github.com/HazyResearch/HipKittens) ・ リポジトリ内被引用：0  
  HipKittens（HK）は、AMDのCDNA3およびCDNA4世代のGPU上で、行列積と注意計算を効率よく記述するためのC++組込み型の領域特化言語である。従来の高性能AMDカーネルは、AITERなどの手書きアセンブリに強く依存していた。HKはタイルという小行列単位の操作を開発者へ公開し、性能に効く低水準制御を再利用可能な部品へまとめる。

- **2025-11 · [FlashEVA: Accelerating LLM inference via Efficient Attention](2025-2511.00576-flasheva-accelerating-llm-inference-via-efficient-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashEVAは、既存の全注意Transformerを再学習なしで置き換える方式ではなく、事前学習済み重みを出発点に、近似注意へ構造を変えたモデルを追加学習して高速化する研究である。2048トークンの入力に対して最大10240トークンを生成する条件では、通常Transformerに対して生成処理量が最大6.7倍、ピークGPUメモリが最大5分の1となった。

- **2025-11 · [EcoSpa: Efficient Transformer Training with Coupled Sparsity](2025-2511.11641-ecospa-efficient-transformer-training-with-coupled-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの注意機構では問い合わせ射影と鍵射影が内積を作り、値射影と出力射影も積として機能する。一次論文の表1では、LLaMA-1BのC4事前学習でメモリ7.80GBから3.88GB、学習時間51.1時間から40.3時間、トークン処理量21,786.49から35,211.27/s、検証パープレキシティ15.56から15.60という結果を報告する。

### 2年前（2024-11〜2025-10）

- **2025-03 · [POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference](2025-pod-attention.md)**  
  実装：[✓](https://github.com/microsoft/vattention/tree/main/pod_attn) ・ リポジトリ内被引用：32  
  プリフィルとデコードの注意を同一SMで並行実行するSM認識型GPUカーネルにより、注意計算を平均28%、サービング処理量を最大22%改善する。

- **2024-12 · [Flex Attention: A Programming Model for Generating Optimized Attention Kernels](2024-2412.05496-flexattention-a-programming-model-for-generating-optimized-attention-kernels.md)**  
  実装：[✓](https://github.com/pytorch/pytorch) ・ リポジトリ内被引用：25  
  高速な融合注意カーネルを「注意変種ごとに手書きする」方式から、利用者が意味だけを書きコンパイラが高速カーネルへ落とす方式へ変える。

- **2025-10 · [KTransformers: Unleashing the Full Potential of CPU/GPU Hybrid Inference for MoE Models](2025-b4e11ada8105-ktransformers-unleashing-the-full-potential-of-cpu-gpu-hybrid-inference-.md)**  
  実装：[✓](https://github.com/kvcache-ai/ktransformers) ・ リポジトリ内被引用：13  
  大規模な混合専門家モデルの多数の専門家重みをCPUメモリに常駐させ、注意機構などをGPUで処理する異種混成推論基盤。CPUの行列演算命令を算術強度に応じて使い分け、非同期の実行制御と専門家計算の遅延反映によってCPU・GPUの相互待ちを減らす。低同時実行の巨大モデルを主対象とし、評価した環境は二基の高性能XeonとA100またはRTX 4080である。

- **2025-04 · [TileLang: A Composable Tiled Programming Model for AI Systems](2025-2504.17577-tilelang-a-composable-tiled-programming-model-for-ai-systems.md)**  
  実装：[✓](https://github.com/tile-ai/tilelang) ・ リポジトリ内被引用：13  
  GPUカーネルの「何を計算するか」をタイル単位のデータ流として書き、「どのスレッドがどの配置で、どの命令を使い、転送と計算をどう重ねるか」を別のスケジュール層へ分離する。高水準な記述を保ちながら、FlashAttention-3級の複雑なパイプラインまで表現・自動推論できることを狙う。

- **2025-04 · [Triton-distributed: Programming Overlapping Kernels on Distributed AI Systems with the Triton Compiler](2025-2504.19442-triton-distributed.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/Triton-distributed) ・ リポジトリ内被引用：10  
  OpenSHMEM通信をTritonへ統合し、計算・通信・メモリアクセスをPythonから細粒度に重ね合わせ、8〜64 GPUで分散カーネルを高速化するコンパイラ拡張。

- **2025-03 · [Medusa: Accelerating Serverless LLM Inference with Materialization](2025-8c4404f09758-medusa-accelerating-serverless-llm-inference-with-materialization.md)**  
  実装：[✓](https://github.com/thustorage/Medusa) ・ リポジトリ内被引用：9  
  Medusaは、大規模言語モデル（large language モデル; LLM）を必要なときだけ起動するサーバーレス推論において、モデル重みの読み込み以外にも無視できない起動費用があることに着目したシステム論文である。

- **2025-09 · [Towards Robust Agentic CUDA Kernel Benchmarking, Verification, and Optimization](2025-2509.14279-towards-robust-agentic-cuda-kernel-benchmarking-verification-and-optimization.md)**  
  実装：[✓](https://github.com/SakanaAI/robust-kbench) ・ リポジトリ内被引用：6  
  固定入力などを悪用した「高速だが一般化しないCUDA」を弾くrobust-kbenchと、翻訳・LLM検証・進化的最適化を統合したエージェントを提案し、KernelBenchの見かけの平均3.13倍高速化が堅牢化後1.49倍へ下がることを示す。

- **2025-06 · [FlashMoE: Fast Distributed MoE in a Single Kernel](2025-2506.04667-flashmoe-fast-distributed-moe-in-a-single-kernel.md)**  
  実装：[✓](https://github.com/osayamenja/FlashMoE) ・ リポジトリ内被引用：6  
  分散MoE全体を単一の常駐GPUカーネルへ融合し、装置起点通信とタイル単位スケジューリングでCPU起動・同期待ちを除き、8基H100で最大6.4倍の遅延改善と5.7倍のスループットを示す。

- **2025-03 · [TileLink: Generating Efficient Compute-Communication Overlapping Kernels using Tile-Centric Primitives](2025-2503.20313-tilelink-generating-efficient-compute-communication-overlapping-kernels-using-tile-centric-primitives.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/Triton-distributed) ・ リポジトリ内被引用：6  
  タイル中心プリミティブから計算・通信融合カーネルを生成し、8×H800で非重畳比1.17〜20.76倍、8モデルのエンドツーエンドでPyTorch比平均1.32倍を達成する。

- **2025-09 · [Astra: A Multi-Agent System for GPU Kernel Performance Optimization](2025-2509.07506-astra-a-multi-agent-system-for-gpu-kernel-performance-optimization.md)**  
  実装：[✓](https://github.com/Anjiang-Wei/Astra) ・ リポジトリ内被引用：5  
  高水準PyTorchからCUDAを一から生成するのではなく、SGLangに既に存在する正しいCUDAカーネルを出発点にし、試験・プロファイル・計画・実装を別々の大規模言語モデル（Large Language モデル; LLM）エージェントへ分担する。

- **2025-08 · [Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning](2025-2508.19828-memory-r1-enhancing-large-language-model-agents-to-manage-and-utilize-me.md)**  
  実装：[✓](https://github.com/yansikuan/memory-r1) ・ リポジトリ内被引用：4  
  メモリ-R1は、記憶を管理するエージェント（メモリ Manager）と、検索した記憶から回答するエージェント（Answer Agent）を分離し、どちらも最終回答の正しさを報酬とする強化学習（reinforcement learning）で訓練する。

- **2025-04 · [70% Size, 100% Accuracy: Lossless LLM Compression for Efficient GPU Inference via Dynamic-Length Float (DFloat11)](2025-2504.11651-70-size-100-accuracy-lossless-llm-compression-for-efficient-gpu-inferenc.md)**  
  実装：[✓](https://github.com/LeanModels/DFloat11) ・ リポジトリ内被引用：4  
  DFloat11は、大規模言語モデルのBFloat16重みを数値を変えずに圧縮し、推論時にGPU上で必要な部分だけ復号する方式である。Llama 3.1 405Bの重み容量は約811.71GBから551.22GBへ減り、8台の80GB GPUを持つ単一ノードで可逆推論できる。

- **2025-10 · [lm-Meter: Unveiling Runtime Inference Latency for On-Device Language Models](2025-2510.06126-lm-meter-unveiling-runtime-inference-latency-for-on-device-language-mode.md)**  
  実装：[✓](https://github.com/amai-gsu/LM-Meter) ・ リポジトリ内被引用：2  
  さらにモバイルGPUではドライバが非公開で、カーネル単位の実行時間、キュー待機、ホスト側の発行遅延をアプリケーションから直接見ることが難しい。また量子化Gemma-2-2B-itの短い復号ではGPUの遊休時間が21%を超え、行列積カーネル群が実行時間の60%超を占める。

- **2024-11 · [Freeze-Omni: A Smart and Low Latency Speech-to-speech Dialogue Model with Frozen LLM](2024-2411.00774-freeze-omni-a-smart-and-low-latency-speech-to-speech-dialogue-model-with.md)**  
  実装：[✓](https://github.com/VITA-MLLM/Freeze-Omni) ・ リポジトリ内被引用：0  
  さらに、音声認識、文章生成、音声合成を独立したシステムとして直列に接続すると、応答開始までの待ち時間が積み重なる。主要結果として、音声入力によるWebQuestionsの正答率は44.73%で、同じ基盤LLMに文章を入力した45.13%と近い。

### 3年前（2023-11〜2024-10）

- **2024-04 · [PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation](2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transf.md)**  
  実装：[✓](https://github.com/pytorch/pytorch) ・ リポジトリ内被引用：28  
  Pythonの即時実行の柔軟性を残して演算グラフを実行時に取り出し、TritonやC++へコンパイルする仕組みを設計・評価した。

- **2024-06 · [S-LoRA: Serving Thousands of Concurrent LoRA Adapters](2024-2311.03285-s-lora-serving-thousands-of-concurrent-lora-adapters.md)**  
  実装：[✓](https://github.com/S-LoRA/S-LoRA) ・ リポジトリ内被引用：27  
  しかし、数千の個別化モデルを同時提供する場合、アダプタの保存先、要求ごとの重み切替、系列長に応じて伸びる鍵・値キャッシュ、異なる低ランク行列を使う要求のバッチ化が問題になる。アダプタを基盤モデルへ統合して個別のモデル重みを作る方式では、基盤部分を要求間で共有してまとめて計算する機会を失う。

- **2024-02 · [Simple linear attention language models balance the recall-throughput tradeoff](2024-2402.18668-simple-linear-attention-language-models-balance-the-recall-throughput-tr.md)**  
  実装：[✓](https://github.com/HazyResearch/based) ・ リポジトリ内被引用：22  
  通常のソフトマックス注意（softmax 注意機構）は、入力文脈に含まれる特定の情報を後から正確に参照する再取得（recall）に強い。モデル規模360M～1.3B、最大50Bトークンの学習、単一NVIDIA H100での実行測定を行い、1.3B・バッチ128・1024トークン生成でFlashAttention-2比最大24倍の処理量を報告する。

- **2024-04 · [CATS: Contextually-Aware Thresholding for Sparsity in Large Language Models](2024-2404.08763-cats-contextually-aware-thresholding-for-sparsity-in-large-language-mode.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/CATS) ・ リポジトリ内被引用：15  
  大規模言語モデルの多層パーセプトロン（MLP）では、活性値の小さい中間ニューロンも密行列積の対象となる。特にバッチが小さい自己回帰復号では、重みをGPUメモリから読む帯域が処理時間を制限しやすい。混合専門家（MoE）モデルは一部の専門家だけを選ぶが、通常のLlama2やMistralの密なGated-MLPにはそのような明示的な専門家選択器がない。

- **2024-05 · [Mirage: A Multi-Level Superoptimizer for Tensor Programs](2024-2405.05751-mirage-a-multi-level-superoptimizer-for-tensor-programs.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：12  
  Mirageは「既知のアルゴリズムに対して良いGPUスケジュールを探す」だけでも、「数式を書き換えて既存カーネルを組み合わせる」だけでもない。テンソル計算をGPUのカーネル・スレッドブロック・スレッド階層をまたぐμGraphで表し、数式の形、融合境界、並列化方法を同じ探索の中で変えることで、人手では実装量が大きい複合最適化を自動発見する。

- **2024-10 · [ThunderKittens: Simple, Fast, and Adorable AI Kernels](2024-2410.20399-thunderkittens-simple-fast-and-adorable-ai-kernels.md)**  
  実装：[✓](https://github.com/HazyResearch/ThunderKittens) ・ リポジトリ内被引用：10  
  各演算ごとに大量のCUDA制御コードを書く代わりに、タイル演算と「ロード・計算・保存・終了」の4段階を指定し、共有メモリの配置や同期の多くを共通部品に任せる。さらに、行列積の段数を1から4へ増やすと260→760 TFLOPS、L2再利用を意識したブロック順序では805対392 TFLOPSという差があり、性能改善の機構を個別に検証している。

- **2024-10 · [SageAttention: Accurate 8-Bit Attention for Plug-and-play Inference Acceleration](2024-2410.02367-sageattention-accurate-8-bit-attention-for-plug-and-play-inference-accel.md)**  
  実装：[✓](https://github.com/thu-ml/SageAttention) ・ リポジトリ内被引用：9  
  一般的なモデル量子化は全結合層の重み・活性へ集中するが、長い文脈では注意行列を計算するQKᵀと、注意重みを値へ適用するPVの行列積が大きな費用を占める。RTX 4090での注意カーネルの演算性能は、FlashAttention-2比で概ね2.1倍、xformers比で概ね2.7倍と報告される。

- **2024-02 · [Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs](2024-2402.10517-any-precision-llm-low-cost-deployment-of-multiple-different-sized-llms.md)**  
  実装：[✓](https://github.com/SNU-ARC/any-precision-llm) ・ リポジトリ内被引用：9  
  Any-Precision LLMは、同じ大規模言語モデルを複数の量子化精度で運用する場合のメモリと作成費用を削減する研究である。Llama-2-7Bの3～8ビット6種類を個別配置する場合29.9GBに対し、共通配置では8.4GBとなり、3.56倍の容量節約を報告する。

- **2023-12 · [An LLM Compiler for Parallel Function Calling](2023-2312.04511-an-llm-compiler-for-parallel-function-calling.md)**  
  実装：[✓](https://github.com/SqueezeAILab/LLMCompiler) ・ リポジトリ内被引用：9  
  言語モデルに検索、計算、データ取得などの外部関数を使わせる場合、素朴な方式では「一つの関数を呼ぶ、結果を読む、次の関数を決める」という往復を繰り返す。HotpotQAでは逐次方式ReAct比1.80倍、Movie Recommendationでは3.74倍、依存付きParallelQAでは最大2.27倍の遅延改善を報告する。

- **2024-08 · [STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs](2024-2408.01803-stbllm-breaking-the-1-bit-barrier-with-structured-binary-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  大規模言語モデルの推論では、特にバッチの小さい復号段階で重みを主記憶やGPUメモリから読み出す帯域が律速になりやすい。従来の二値化手法は、重要な重みを別扱いにしたり残差を追加したりして精度を回復するものの、重み当たり約1ビットの表現からさらに削る余地が残る。

- **2024-06 · [T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge](2024-2407.00088-t-mac-cpu-renaissance-via-table-lookup-for-low-bit-llm-deployment-on-edg.md)**  
  実装：[✓](https://github.com/microsoft/T-MAC) ・ リポジトリ内被引用：7  
  重みのみを低ビット量子化した大規模言語モデルでは、重みは1〜4ビットでも活性値は8〜16ビット以上の精度を保つことが多い。論文はカーネルの最大6.6倍、平均3.6倍の改善、モデル全体で条件により2〜4倍の生成速度改善を報告する。

- **2024-09 · [CHESS: Optimizing LLM Inference via Channel-Wise Thresholding and Selective Sparsification](2024-2409.01366-chess-optimizing-llm-inference-via-channel-wise-thresholding-and-selecti.md)**  
  実装：[✓](https://github.com/ZeonfaiHo/CHESS) ・ リポジトリ内被引用：5  
  注意機構には同じ閾値を機械的に適用せず、問い合わせ射影と出力射影に限定して活性疎化を行う。Intel Core i9-12900K、64GB DDR4、単一要求、FP32というCPU測定条件で、注意投影も選択的に疎化した構成の復号高速化は最大1.27倍である。

- **2024-05 · [LeanAttention: Hardware-Aware Scalable Attention Mechanism for the Decode-Phase of Transformers](2024-2405.10480-lean-attention-hardware-aware-scalable-attention-mechanism.md)**  
  実装：[✓](https://github.com/microsoft/onnxruntime) ・ リポジトリ内被引用：5  
  LeanAttentionが減らすのは注意の数学的な計算量ではない。まったく同じ厳密注意を、長いKV文脈方向へ細かく分割し、GPUの全SMへ端数なく近い形で仕事を割り振る。デコードでは問い合わせが1トークンしかないため従来のタイル並列性が不足する、というハードウェア利用率の問題を解く。

- **2024-04 · [DeFT: Decoding with Flash Tree-Attention for Efficient Tree-structured LLM Inference](2024-2404.00242-deft-decoding-with-flash-tree-attention-for-efficient-tree-structured-ll.md)**  
  実装：[✓](https://github.com/LINs-lab/DeFT) ・ リポジトリ内被引用：5  
  従来のGPU注意カーネルは通常の一本の系列を想定し、クエリごとに必要なKVを集めるため、同じ接頭辞のKVを何度もGPU広帯域メモリから共有メモリへ運ぶ。DeFT（デコード with Flash Tree-注意機構）は、木構造のKVと複数クエリを一緒に分割する際の基準を逆転させる。

- **2024-03 · [AIOS: LLM Agent Operating System](2024-2403.16971-aios-llm-agent-operating-system.md)**  
  実装：[✓](https://github.com/agiresearch/AIOS) ・ リポジトリ内被引用：4  
  従来のエージェント枠組みでは、各エージェントがLLMやツールを直接呼び出し、GPUメモリの不足、競合するAPI呼び出し、長時間要求の独占を個別に処理しがちだった。AIOSはエージェントアプリケーションと資源管理を分離し、専用のAIOSカーネルを通じてサービスを提供する。

- **2024-07 · [Inference Performance Optimization for Large Language Models on CPUs](2024-2407.07304-inference-performance-optimization-for-large-language-models-on-cpus.md)**  
  実装：[✓](https://github.com/intel/xFasterTransformer) ・ リポジトリ内被引用：3  
  IntelのxFasterTransformerに、CPU向けSlimAttention、トークン・ヘッド単位のINT8 KVキャッシュ、oneCCLによる分散推論とゼロコピー通信を組み込む。Xeon 8563C環境でLlama2-70Bの次トークン遅延を2ソケット249.7msから8ソケット87.7msへ短縮した。

- **2024-02 · [QUICK: Quantization-aware Interleaving and Conflict-free Kernel for efficient LLM inference](2024-2402.10076-quick-quantization-aware-interleaving-and-conflict-free-kernel-for-effic.md)**  
  実装：[✓](https://github.com/SqueezeBits/QUICK) ・ リポジトリ内被引用：2  
  4ビットに量子化した大規模言語モデルでは、重みの保存容量を減らせても、行列積の際には高精度の活性値と掛け合わせるために重みを半精度へ戻す処理が必要になる。原著の行列積単体の比較ではバッチ256でAutoAWQのカーネル比1.33〜1.91倍、モデル生成の比較では最大1.94倍の処理量を報告した。

- **2024-07 · [LeanQuant: Accurate and Scalable Large Language Model Quantization with Loss-error-aware Grid](2024-2407.10032-leanquant-accurate-and-scalable-large-language-model-quantization-with-l.md)**  
  実装：[✓](https://github.com/LeanModels/LeanQuant) ・ リポジトリ内被引用：0  
  LeanQuantは、大規模言語モデルの学習後量子化（Post-学習 量子化; PTQ）で、各重みをどの離散値へ丸めるかを決める量子化格子の位置を最適化する手法である。Llama-3.1-405Bの量子化を48GB GPU二枚と大容量CPUメモリで約20.7時間で完了した。

- **2024-06 · [ShiftAddLLM: Accelerating Pretrained LLMs via Post-Training Multiplication-Less Reparameterization](2024-2406.05981-shiftaddllm-accelerating-pretrained-llms-via-post-training-multiplicatio.md)**  
  実装：[✓](https://github.com/GATECH-EIC/ShiftAddLLM) ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを低ビット化すればGPUメモリの占有を減らせる。しかし、通常の重み量子化では、低ビット整数を推論時に浮動小数点へ復元して乗算する場合があり、保存容量の削減がそのまま計算演算の削減を意味しない。OPT-66Bの重みメモリはFP16の122 GBから３ビット時23 GB、２ビット時16 GBへ減少した。

### 4年前（2022-11〜2023-10）

- **2023-10 · [Deja Vu: Contextual Sparsity for Efficient LLMs at Inference Time](2023-2310.17157-deja-vu-contextual-sparsity-for-efficient-llms-at-inference-time.md)**  
  実装：[✓](https://github.com/FMInference/DejaVu) ・ リポジトリ内被引用：49  
  密なモデルから常に同じ重みを削除する静的枝刈りでは、入力に応じて必要な知識が変わるため、文章生成や文脈内学習の品質を損ない得る。

- **2023-09 · [Flash-LLM: Enabling Cost-Effective and Highly-Efficient Large Generative Model Inference with Unstructured Sparsity](2023-2309.10285-flash-llm-enabling-cost-effective-and-highly-efficient-large-generative-.md)**  
  実装：[✓](https://github.com/AlibabaResearch/flash-llm) ・ リポジトリ内被引用：21  
  Flash-LLMは、非構造枝刈りを施した大規模生成モデルの重みをGPUへ効率的に読み込むため、疎行列として転送し、GPU内部で密行列に戻してから行列演算器で計算する推論カーネルである。

- **2022-11 · [Who Says Elephants Can't Run: Bringing Large Scale MoE Models into Cloud Scale Production](2022-2211.10017-who-says-elephants-can-t-run-bringing-large-scale-moe-models-into-cloud-.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  提案はNVIDIAの推論エンジンFasterTransformerを拡張し、専門家番号でトークンを基数ソートする経路、CUTLASSの複数行列積統合、重みだけの4/8ビット量子化を行列積の中で復号する処理、翻訳完了文をバッチから除く処理を組み合わせる。

- **2023-10 · [QUIK: Towards End-to-end 4-Bit Inference on Generative Large Language Models](2023-2310.09259-quik-towards-end-to-end-4-bit-inference-on-generative-large-language-mod.md)**  
  実装：[✓](https://github.com/IST-DASLab/QUIK) ・ リポジトリ内被引用：11  
  QUIKは、生成大規模言語モデルの線形層を重み・活性値の双方が4ビット整数であるW4A4へ移すための量子化方式である。CUTLASSによる低ビット行列積と量子化・逆量子化の融合カーネルを実装し、RTX3090の2048トークン入力一括処理でFP16比最大3.4倍の処理量改善を報告する。

- **2023-05 · [Blockwise Parallel Transformer for Large Context Models](2023-2305.19370-blockwise-parallel-transformer-for-large-context-models.md)**  
  実装：[✓](https://github.com/haoliuhl/ringattention) ・ リポジトリ内被引用：3  
  注意だけでなくFFNまで系列ブロック内で融合して学習時活性を保持しないBPT。A100/TPU v4でメモリ効率型注意より2〜4倍長い文脈を学習可能にし、1B・16Kでは通常Transformer比1.20倍の学習スループットを示す。

- **2023-10 · [Sparse Fine-tuning for Inference Acceleration of Large Language Models](2023-2310.06927-sparse-fine-tuning-for-inference-acceleration-of-large-language-models.md)**  
  実装：[✓](https://github.com/IST-DASLab/SparseFinetuning) ・ リポジトリ内被引用：2  
  本研究は、大規模言語モデル（LLM）を高い重み疎性へ枝刈りしたうえで下流タスクへ微調整し、精度を回復する学習法と、その疎性をCPU/GPUの実際の推論高速化へ変換する実行系を一体で評価する。

### 5年前（2021-11〜2022-10）

- **2022-06 · [LUT-GEMM: Quantized Matrix Multiplication based on LUTs for Efficient Inference in Large-Scale Generative Language Models](2022-2206.09557-lut-gemm-quantized-matrix-multiplication-based-on-luts-for-efficient-inf.md)**  
  実装：[✓](https://github.com/naver-aics/lut-gemm) ・ リポジトリ内被引用：45  
  重みを3～4ビットへ圧縮すればGPUメモリへの転送量を減らせるが、既存の重みのみ量子化の多くは、積和を行う直前に重みを半精度へ展開する逆量子化処理を必要とする。

### 6年前（2020-11〜2021-10）

- **2021-02 · [TurboTransformers: An Efficient GPU Serving System For Transformer Models](2021-2010.05680-turbotransformers-an-efficient-gpu-serving-system-for-transformer-models.md)**  
  実装：[✓](https://github.com/Tencent/TurboTransformers) ・ リポジトリ内被引用：24  
  提案システムは、GEMM（行列積）間の演算融合とSoftmax・LayerNormの並列縮約、系列長を受け取ってから行う中間領域の再利用、実測コストを使う動的計画法による要求バッチ分割を組み合わせる。

- **2021-03 · [Random Feature Attention](2021-2103.02143-random-feature-attention.md)**  
  実装：[✓](https://github.com/haopeng-nlp/transformer-rfa) ・ リポジトリ内被引用：10  
  本論文が扱うのは、標準的な指数正規化注意（softmax 注意機構）において、各質問ベクトルが過去のすべての鍵ベクトルと内積を計算するため、自己回帰復号で生成長が増すほど注意処理が重くなる問題である。

### 7年前（2019-11〜2020-10）

- **2020-10 · [LightSeq: A High Performance Inference Library for Transformers](2020-2010.13887-lightseq-a-high-performance-inference-library-for-transformers.md)**  
  実装：[✓](https://github.com/bytedance/lightseq) ・ リポジトリ内被引用：19  
  LightSeqは、Transformerの推論を汎用学習フレームワークから直接実行するときに生じる多数の小規模GPU演算、自己回帰探索の不要な候補処理、可変長系列に伴うメモリ割当を、推論専用のCUDA実装で削減するライブラリである。2020年に公開された研究であり、後年の大規模言語モデル提供基盤を直接評価したものではない。中核は三つの独立した最適化である。

### 8年前（2018-11〜2019-10）

- **2019-06 · [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations](2019-triton-an-intermediate-language-and-compiler-for-tiled-neural-network-computations.md)**  
  実装：[✓](https://github.com/triton-lang/triton) ・ リポジトリ内被引用：97  
  深層学習の演算を高速なGPUカーネルにするには、数式を記述するだけでは足りない。入力配列のどの部分をまとめて読み出し、何回再利用し、どのスレッドに配り、いつ共有メモリへ移すかによって性能が大きく変わる。既存のcuBLASやcuDNNが対象とする標準演算なら高性能な実装を利用できるが、新しい行列演算や不規則な参照を伴う演算では、そのまま使えない。

- **2019-10 · [Structured Pruning of Large Language Models](2019-1910.04732-structured-pruning-of-large-language-models.md)**  
  実装：[✓](https://github.com/asappresearch/flop) ・ リポジトリ内被引用：19  
  FLOP（Factorized Low-rank Pruning、因子化低ランク枝刈り）は、重みを個別にゼロ化する非構造的な枝刈りでは、パラメータ数を減らしても一般的な計算装置で速度が上がりにくいという問題に取り組む。

### 9年前（2017-11〜2018-10）

- **2018-05 · [Online normalizer calculation for softmax](2018-1805.02867-online-normalizer-calculation-for-softmax.md)**  
  実装：[✓](https://github.com/NVIDIA/online-softmax) ・ リポジトリ内被引用：36  
  本論文は、数値的に安全なソフトマックスの出力を変えずに、入力配列を読み直す回数を減らす「オンライン正規化子（online normalizer）」を提案する。著者らのTesla V100での単精度実装では、ソフトマックス単体で最大約1.3倍の高速化が報告される。
<!-- survey:auto:end -->
