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
## 自動生成の論文一覧（362本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/09-kernel-runtime-compilation/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-03 · [FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling](2026-2603.05451-flashattention-4-algorithm-and-kernel-pipelining-co-design-for-asymmetri.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention/tree/main/flash_attn/cute) ・ リポジトリ内被引用：43  
  FlashAttention-4は、NVIDIA Blackwell世代のB200でテンソルコアの行列積性能が大きく増加した一方、共有メモリの読出し帯域や指数関数演算器の性能が同じ比率では伸びないことに対応する注意カーネルである。FlashAttention-4は前向き・逆向きの処理を別々に設計し、行列積、softmax、メモリ転送、勾配集約を重ね合わせる。

- **2025-12 · [MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs](2025-2512.22219-mirage-persistent-kernel-mega-kernel-runtime.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：27  
  演算子単位の多数カーネル起動をSM粒度の依存グラフへ分解し、単一常駐巨大カーネル内の分散スケジューラで演算・通信・タスク間パイプラインを重ね、vLLM/SGLang比で最大1.7倍の推論遅延改善を示す。

- **2026-03 · [Mamba-3: Improved Sequence Modeling using State Space Principles](2026-2603.15569-mamba-3-improved-sequence-modeling-using-state-space-principles.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：18  
  Mamba-3は、状態空間モデル（State Space モデル、SSM）を使う系列モデルを学習時の並列性だけでなく推論時の実行効率から設計し直す研究である。

- **2025-12 · [SonicMoE: Accelerating MoE with IO and Tile-aware Optimizations](2025-2512.14080-sonicmoe-accelerating-moe-with-io-and-tile-aware-optimizations.md)**  
  実装：[✓](https://github.com/Dao-AILab/sonic-moe) ・ リポジトリ内被引用：12  
  SonicMoEは混合専門家モデル（Mixture-of-Experts、MoE）の学習を対象に、専門家の細粒度化と高疎性化によって生じる三種類の非効率を同時に減らす。ICLR 2026正式版では、7B級の細粒度MoEでScatterMoEに対する活性値メモリ削減45%、Hopper世代GPUでの計算処理量1.86倍を報告する。

- **2026-04 · [Event Tensor: A Unified Abstraction for Compiling Dynamic Megakernel](2026-2604.13327-event-tensor-dynamic-megakernel-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  タイル依存関係を記号形状のイベントテンソルとして表し、可変形状とMoEのデータ依存分岐を再コンパイルせず静的・動的メガカーネルへ変換するコンパイラ抽象。

- **2026-01 · [FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems](2026-2601.00227-flashinfer-bench-ai-driven-kernel-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  実LLM serving由来のGPUカーネル課題を統一トレースで検証し、エージェント生成カーネルをSGLang/vLLMへ低オーバーヘッドで動的適用する閉ループ基盤。

- **2026-05 · [KVBuffer: IO-aware Serving for Linear Attention](2026-2605.19049-kvbuffer-io-aware-serving-for-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  KVBufferは、線形注意（linear 注意機構）を使う大規模言語モデル（LLM）の推論サービングにおいて、毎トークン更新される大きな内部状態へのメモリアクセスを減らすための機構である。

- **2026-02 · [On State Reduction in Linear Attention](2026-2602.04852-on-state-reduction-in-linear-attention.md)**  
  実装：[✓](https://github.com/camail-official/LinearAttentionPruning) ・ リポジトリ内被引用：5  
  線形注意（linear 注意機構）は、通常のソフトマックス注意と異なり、過去のトークンを固定サイズの行列型状態へ逐次圧縮できる。Gated DeltaNet 1.3Bでは、状態次元を50%削減し回復用微調整を行った場合、WikiText-2困惑度は元モデル16.8に対しDRRQRで16.3、ゼロショット平均精度は59.4から58.0となった。

- **2026-06 · [FOCUS: DLLMs Know How to Tame Their Compute Bound](2026-2601.23278-focus-dllms-know-how-to-tame-their-compute-bound.md)**  
  実装：[✓](https://github.com/sands-lab/FOCUS) ・ リポジトリ内被引用：4  
  拡散型言語モデル（diffusion language モデル、DLLM）は、マスクされた複数のトークンを一つのブロックとして反復的に復元する。自己回帰型言語モデルと違い、各反復でブロック内の複数位置を同時に処理できるが、実際に確定する位置が少ないと大部分の計算は次の反復でやり直される。直近の確定数と差分の分布から保持予算を決め、上位候補を残す。

- **2026-02 · [MetaAttention: A Unified and Performant Attention Framework across Hardware Backends](2026-2502.15349-metaattention-a-unified-and-performant-attention-framework-across-hardwa.md)**  
  実装：[✓](https://github.com/SJTU-IPADS/MetaAttention) ・ リポジトリ内被引用：4  
  MetaAttentionは、異なる注意機構をハードウェアごとに手作業で実装する費用を削減しながら、専用実装に近い実行性能を得るためのカーネル生成基盤である。両者は著者・基本設計・最大10.4倍という結果が対応する一方、本稿で詳細な数値・実験条件を確認したのは公開プレプリント版である。

- **2025-12 · [Dynamic Large Concept Models: Latent Reasoning in an Adaptive Semantic Space](2025-2512.24617-dynamic-large-concept-models-latent-reasoning-in-an-adaptive-semantic-sp.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  原著は平均4トークンを1概念へ圧縮するR=4の条件を中心に、通常の1.3B Transformerと、概念段に容量を再配分した2.3B DLCMを比較した。両者の推論浮動小数点演算量（FLOPs）を近づけた条件で、12種類のゼロショット課題の平均正解率は41.23%から43.92%へ2.69ポイント改善した。

- **2026-08 · [DeltaLog: Deferred Materialization of Recurrent States for Linear Attention Decoding](2026-2608.15533-deltalog-deferred-materialization-of-recurrent-states-for-linear-attention-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  線形注意の密な再帰状態を基底状態と有界な差分ログへ分解し、毎トークンの全状態書き戻しを周期的なマージへ遅延する。

- **2026-05 · [ThriftAttention: Selective Mixed Precision for Long-Context FP4 Attention](2026-2605.23081-thriftattention-selective-mixed-precision-for-long-context-fp4-attention.md)**  
  実装：[✓](https://github.com/joesharratt1229/ThriftAttention) ・ リポジトリ内被引用：3  
  Blackwell世代のGPUは4ビット浮動小数点（FP4）の行列積を高速に処理できるため、注意計算を16ビット浮動小数点（FP16）からFP4へ落とせば演算とメモリ転送を軽くできる。ThriftAttentionは、全ての問い合わせ・鍵の組を捨てず、重要なブロックだけFP16へ戻す方式である。

- **2026-03 · [WaterSIC: Information-Theoretically (Near) Optimal Linear Layer Quantization](2026-2603.04956-watersic-information-theoretically-near-optimal-linear-layer-quantizatio.md)**  
  実装：[✓](https://github.com/egorlifar/watersic) ・ リポジトリ内被引用：3  
  WaterSICは、大規模言語モデルの線形層を学習後量子化（post-学習 量子化）するとき、入力チャネルごとに異なる格子幅を与えることで、同じ圧縮容量でも出力のずれを小さくする手法である。ただし論文が評価する主軸は品質対圧縮率であり、llama.cppなどの推論器に載せたトークン/秒、展開カーネルの速度、メモリ帯域削減の実測ではない。

- **2026-02 · [WildCat: Near-Linear Attention in Theory and Practice](2026-2602.10056-wildcat-near-linear-attention-in-theory-and-practice.md)**  
  実装：[✓](https://github.com/microsoft/wildcat) ・ リポジトリ内被引用：3  
  WildCatは、長い入力に対する注意機構の二乗計算量を減らすため、全ての鍵をそのまま参照する代わりに少数の代表鍵を選び、残りの鍵の寄与を最適な重みへ集約する近似注意方式である。

- **2026-01 · [Understanding Efficiency: Quantization, Batching, and Serving Strategies in LLM Energy Use](2026-2601.22362-understanding-efficiency-quantization-batching-and-serving-strategies-in.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大規模言語モデル（Large Language モデル; LLM）の推論電力量は、モデルのパラメータ数や重みのビット幅だけでは決まらない。同じモデルを同じGPUで実行しても、事前充填（プリフィル）と逐次復号（デコード）では計算律速かメモリ律速かが異なり、要求を逐次処理するか連続バッチ化するかによってGPUの待機時間が大きく変わる。重要な結論は三つある。

- **2026-09 · [Taming Bitwise Behavior in GPU Kernels with Tensor Core: Black-Box Reconstruction, Compiler Enforcement, and Static Verification](2026-2609.11356-taming-bitwise-behavior-gpu-tensor-core-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPU縮約順序を記述子化し、非公開行列積のビット挙動復元、コンパイラでの平衡木強制、命令列の静的同値判定を接続して再現性と自動調整を両立する。

- **2026-09 · [mKernel: Fast Multi-GPU, Multi-Node Fused Kernels](2026-2609.13585-mkernel-fast-multi-gpu-multi-node-fused-kernels.md)**  
  実装：[✓](https://github.com/uccl-project/mKernel) ・ リポジトリ内被引用：2  
  しかし計算がまとまった出力を完成するまで通信を始められない場合、演算の途中で生じる細かな待ち時間を隠せない。計算と通信を一つの融合カーネルへまとめても、従来方式の多くは単一NVLink領域に限られる。

- **2026-09 · [LeapQuant: Efficient Linear Attention with Accurate Recurrent State Quantization](2026-2609.38166-leapquant-efficient-linear-attention-with-accurate-recurrent-state-quant.md)**  
  実装：[✓](https://github.com/leapquant/LeapQuant) ・ リポジトリ内被引用：2  
  線形注意の再帰状態を窓ごとに1回だけ量子化し、外れ値を高精度の補償トークンへ逃がす学習不要の方式で、8ビットでも精度をほぼ保ちながら状態転送を3.4倍減らしデコードを高速化した。

- **2026-06 · [Prefilling-dLLM: Predictive Prefilling for Long-Context Inference in Diffusion Language Models](2026-2606.10537-prefilling-dllm-predictive-prefilling-for-long-context-inference-in-diff.md)**  
  実装：[✓](https://github.com/menik1126/Prefilling-dLLM) ・ リポジトリ内被引用：2  
  Prefilling-dLLMは、この入力接頭辞を長さ一定の小区間へ分け、各区間の鍵・値（Key–Value、KV）表現を事前に一度だけ計算し、問い合わせに関係する区間だけを残して反復的な雑音除去（denoising）に再利用する方式である。

- **2026-06 · [Approaching Shannon Bound with Lossless LLM Weight Compression](2026-2606.15789-shannon-bound-lossless-weight-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GEMMタイルごとにANSで重みを損失なく圧縮し、共有メモリへ復号しながらテンソルコア計算と重ねることで、Mixtral-176Bの最大バッチを20から95へ増やし、SGLangスループットを最大1.6倍にする。

- **2026-05 · [Ada-MK: Adaptive MegaKernel Optimization via Automated DAG-based Search for LLM Inference](2026-2605.11581-ada-mk-adaptive-megakernel-compilation.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Ada-MKはLLMデコードをPTX命令水準の依存グラフへ分解し、共有メモリ配置とワープ役割をオフライン探索して分岐のないメガカーネルを生成し、L20でTensorRT-LLM比最大23.6%高速化する。

- **2026-04 · [VFA: Relieving Vector Operations in Flash Attention with Global Maximum Pre-computation](2026-2604.12798-vfa-relieving-vector-operations-in-flash-attention-with-global-maximum-p.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  FlashAttentionは、巨大な注意行列をGPUの高帯域メモリへ書き出さず、クエリ・キー・値を小さなブロックに分割してオンチップメモリで処理する。VFA（Vector Relieved Flash 注意機構）はこの残った部分に焦点を当てる。要旨ではC16V32という計算器構成を基準にC8V32、C4V32、C4V16で約2倍の高速化を報告する。

- **2026-04 · [Open-TQ-Metal: Fused Compressed-Domain Attention for Long-Context LLM Inference on Apple Silicon](2026-2604.16957-open-tq-metal-fused-compressed-domain-attention-for-long-context-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  70B級モデルを端末上で動かすとき、重みを4ビット化しても長文脈の鍵・値（KV）キャッシュが巨大になる。合計約79.1GBとなり、64GBの統合メモリを持つMacには収まらない。Llama 3.1 70Bの128K文脈では、注意カーネル単体が逆量子化後に注意を実行する方式の480.6msから9.9msへ短縮され、約48倍となる。

- **2026-04 · [Nautilus: An Auto-Scheduling Tensor Compiler for Efficient Tiled GPU Kernels](2026-2604.14825-nautilus-an-auto-scheduling-tensor-compiler-for-efficient-tiled-gpu-kern.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデル（Large Language モデル; LLM）の注意計算を高速化するには、数学的に同じ式でも、演算の融合、行列の分割幅、共有メモリの配置、並列実行単位、GPU世代ごとの命令特性を考慮しなければならない。FlashAttention系のカーネルはこれらを手作業で高度に調整してきた。

- **2026-03 · [Trinity: Three-Dimensional Tensor Program Optimization via Tile-level Equality Saturation](2026-f777f1110d4d-trinity-three-dimensional-tensor-program-optimization-via-tile-level-equ.md)**  
  実装：[✓](https://github.com/kaist-ina/Trinity-AE) ・ リポジトリ内被引用：2  
  Transformerの推論カーネル最適化では、計算グラフ上の演算融合・代数変形と、GPU上のタイル分割・共有メモリ配置・並列化を別々のコンパイラ段階で決めることが多い。この分離によって、FlashAttentionのように代数変形とデータ移動・実行順序を同時に変える最適化を一般的なコンパイラが自動発見しにくい。

- **2026-03 · [Scaling Attention via Feature Sparsity](2026-2603.22300-scaling-attention-via-feature-sparsity.md)**  
  実装：[✓](https://github.com/YannX1e/Sparse-Feature-Attention) ・ リポジトリ内被引用：2  
  一方、クエリ・キーの次元そのものを小さくする方法は、各トークンの表現力を減らすため、特定の推論・検索課題で精度を落とし得る。本論文の疎特徴注意（Sparse Feature 注意機構、SFA）は別の軸を選ぶ。

- **2026-03 · [FlashSampling: Fast and Memory-Efficient Exact Sampling](2026-2603.15854-flashsampling-fast-and-memory-efficient-exact-sampling.md)**  
  実装：[✓](https://github.com/FlashSampling/FlashSampling) ・ リポジトリ内被引用：2  
  一般的な実装では、この語彙投影を行列積として実行し、バッチ数×語彙数のロジット配列をGPUの高帯域メモリ（HBM）へ保存する。一次論文第3版は、H100、H200、B200、B300の4種類のGPUでのカーネル単体測定と、B200上でのvLLMへの統合測定を報告する。

- **2026-01 · [TIRx: A Unified Tile Primitive ML Compiler Across Heterogeneous Backends](2026-2601.19092-tirx-a-unified-tile-primitive-ml-compiler-across-heterogeneous-backends.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  テンソルの物理配置、演算に参加するハードウェアチーム、プリミティブの実装選択を3つの明示的な接口で分離した機械学習コンパイラで、最新GPUと専用加速器の双方でベンダ水準のカーネル性能を保ちながら低水準コードを大幅に減らした。

- **2025-12 · [MemEvolve: Meta-Evolution of Agent Memory Systems](2025-2512.18746-memevolve-meta-evolution-of-agent-memory-systems.md)**  
  実装：[✓](https://github.com/bingreeky/MemEvolve) ・ リポジトリ内被引用：2  
  しかし既存の自己改善型エージェントでは、記憶をどの形式で要約するか、どこへ保存するか、いつ検索するか、どの記憶を忘れるかといった記憶機構の設計自体は人手で固定されていることが多い。

- **2025-12 · [Kitsune: Enabling Dataflow Execution on GPUs with Spatial Pipelines](2025-2502.18403-kitsune-enabling-dataflow-execution-on-gpus-with-spatial-pipelines.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  カーネル境界で中間テンソルが高帯域メモリへ書き戻され、次のカーネルが再び読む。さらに、一般命令主体のCTAとテンソル演算主体のCTAを同じストリーミングマルチプロセッサ（SM）へ配置できるようグリッドスケジューラを拡張する。

- **2026-10 · [SparseDecoding: Decoding-Aware Pruning for Accurate and Efficient LLM Inference](2026-2610.12327-sparsedecoding-decoding-aware-pruning-for-accurate-and-efficient-llm-inf.md)**  
  実装：[✓](https://wang-qitong.github.io/SparseDecoding) ・ リポジトリ内被引用：1  
  枝刈りの較正を固定文からモデル自身の生成トークン（生成段階のみ）へ替えることで長文生成の品質劣化を抑え、ビットマスク走査の生成向け疎カーネルで最大1.48倍の復号高速化を得た。

- **2026-10 · [LinQuant: Functional Invariances for Low-Precision Linear Recurrences](2026-2610.39418-linquant-functional-invariances-for-low-precision-linear-recurrences.md)**  
  実装：[✓](https://github.com/ntumm120/LinQuant) ・ リポジトリ内被引用：1  
  全精度計算を変えない7つの基底変換と因子配置で量子化される被演算子を整える枠組みにより、線形再帰のINT8プリフィルの困惑度悪化を最大86パーセント回復し、最大2.0倍の高速化を得た。

- **2026-09 · [VC-Attention: Value Smoothing and Softmax Casting for Low-bit Attention](2026-2609.15810-vc-attention-value-smoothing-and-softmax-casting-for-low-bit-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  VC-注意機構は、動画拡散変換器（Diffusion Transformer、DiT）の長い時空間系列に対して、低ビット注意機構の値行列Vの量子化誤差と高精度ソフトマックス演算の律速を同時に減らす、追加学習不要のGPUカーネル方式である。

- **2026-09 · [Unfolding the Leech Lattice: Fused Multi-Shell Decoding and VRAM Layouts for 2-Bit LLM Weights](2026-2609.02652-unfolding-the-leech-lattice-fused-multi-shell-decoding-and-vram-layouts-.md)**  
  実装：[✓](https://github.com/pjmalandrino/llvq) ・ リポジトリ内被引用：1  
  本論文は、Leech格子ベクトル量子化（Leech-lattice vector 量子化; LLVQ）を「2 bit/重みで保存できる」という圧縮アルゴリズムの段階から、実際のGPUデコードへ載せる段階まで実装し、そのとき生じる保存bit数と実行時VRAM bit数の乖離を測るシステム研究である。

- **2026-09 · [Routing Should Pay for Itself: Sparse Supervision for Economical LLM Routing](2026-2609.37402-routing-should-pay-for-itself-sparse-supervision-for-economical-llm-rout.md)**  
  実装：[✓](https://github.com/LAMDA-Model-Reuse/SaveRouter) ・ リポジトリ内被引用：1  
  LLMの品質と推論単価はモデルごとに異なるため、容易な問い合わせを小型・安価なモデルへ送り、難しい問い合わせを高性能モデルへ送れば総費用を下げられる。しかし、どの問い合わせにどのモデルが適するかを学習するには、通常は大量の過去問い合わせに複数モデルを実行し、品質の教師信号を取得する必要がある。従来方式で最も早い損益分岐は11,500件である。

- **2026-09 · [Empowering Hybrid Attention Models on NPUs](2026-2609.32114-empowering-hybrid-attention-models-on-npus.md)**  
  実装：[✓](https://github.com/yinyuanzhang/HA-NPU) ・ リポジトリ内被引用：1  
  線形注意の仕事をヘッド単位に割り当てて依存演算子を同一コアへ融合し、中間テンソルの寿命に合わせた実行順の並べ替えと、得な場合だけ変換するレイアウト計画で、エッジNPU上のハイブリッド注意モデルのプリフィルを支配するグローバルメモリ往復を消す実行方式。

- **2026-09 · [Beyond Accuracy: Prefix-Invariant Realizations of Low-Precision Fast Matrix Multiplication](2026-2609.39816-beyond-accuracy-prefix-invariant-realizations-of-low-precision-fast-matr.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究が問題にするのは、低精度の高速行列乗算で通常の正答率が保たれていても、言語モデルの出力が本来参照してはならない未来のトークンに依存することである。

- **2026-09 · [Accelerating the Mitigation of LLM Inference Nondeterminism Across GPU Architectures](2026-2609.25624-accelerating-the-mitigation-of-llm-inference-nondeterminism-across-gpu-a.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この論文が扱うのは、乱数を固定し、温度を0にした貪欲復号でも、同じ大規模言語モデル（LLM）がGPUの世代や同時処理数によって異なるトークンを出す問題である。これは「丸め差が十分小さければ結果がたまたま一致する」という従来の確率的対策ではなく、対象線形層に限り演算順を構造的に一致させる設計である。

- **2026-08 · [Dispatch Overhead, Not Kernel Quality: The Performance Bottleneck in Single-Stream WebGPU LLM Inference](2026-2608.08730-dispatch-overhead-not-kernel-quality-the-performance-bottleneck-in-singl.md)**  
  実装：[✓](https://github.com/jmaczan/torch-webgpu) ・ リポジトリ内被引用：1  
  単一演算測定が同期を混ぜて発行費用を約20倍に膨らませることを暴き、連続発行測定で真の費用を測った上で、同じシェーダで発行だけを減らして53パーセント速くなる統制実験により、律速がカーネルではなく発行回数だと示した測定研究。

- **2026-08 · [Determinism-Preserving GPU Spatial Sharing with Vitamin-E](2026-2603.15042-determinism-preserving-gpu-spatial-sharing-with-vitamin-e.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Vitamin-Eは、カーネル起動時のバイナリ・グリッド・ブロック・依存順序を固定したまま、各起動を利用可能な物理SM集合へ遅延結合する。2026年8月5日のarXiv v4で題名・方式が更新された同一論文である。v4はH20/H200で実機評価し、固定構造で決定的な処理のビット単位一致を確認した。

- **2026-08 · [CoRun: Padding is Simple and Efficient for Deterministic LLM Inference](2026-2608.14376-corun-padding-is-simple-and-efficient-for-deterministic-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  再現性が重要なモデル比較や強化学習のロールアウトでは、単なる見かけのゆらぎではなく運用上の問題となる。しかしこれではGPUが入力形状に応じて分割を最適化できず、行列積や注意機構の並列分割を制限する。

- **2026-08 · [A Thread-Register Decoupled GPU Execution Model for Efficient Tensor Computation](2026-2608.19628-fiber-thread-register-decoupled-gpu-execution.md)**  
  実装：[✓](https://github.com/SJTU-ReArch-Group/GTSim/) ・ リポジトリ内被引用：1  
  FIBERはGPUの実行単位から私有レジスタ所有を切り離し、SM内共有レジスタ、動的な並列度変更、レジスタ単位の依存追跡を組み合わせる。LLMのGEMMと非GEMMが交互に現れる処理を対象に、シミュレータ上でAmpere 2.25倍、Hopper 1.8倍、Blackwell 2.09倍のエンドツーエンド高速化を報告する。

- **2026-07 · [Harness Engineering for LLM-Driven GPU Kernel Generation](2026-2607.17979-harness-engineering-llm-gpu-kernels.md)**  
  実装：[✓](https://github.com/syhya/mlsys26-flashinfer-contest) ・ リポジトリ内被引用：1  
  LLM生成GPUカーネルを、公式準拠のコンパイル・正当性・計時・全形状評価とプロファイル駆動の保守的昇格ループで管理し、B200上の5演算子でFlashInfer比1.12〜29.68倍を得たハーネス設計。

- **2026-07 · [Every Microsecond Matters: Achieving Near Speed-of-Light Latency in GPU Collectives](2026-2607.16100-every-microsecond-matters-achieving-near-speed-of-light-latency-in-gpu-c.md)**  
  実装：[✓](https://github.com/ss16118/low-latency-nccl) ・ リポジトリ内被引用：1  
  本研究は、GPU間の集合通信（collective 通信）を大きなメッセージの帯域幅ではなく、短いメッセージの待ち時間を中心に最適化する。そこで、データ転送と到着通知を一体化するLL方式、受信領域の特殊値で到着を判定するsentinel方式、双方向通信と二重バッファによる暗黙の順序制御、NVLinkの原子的加算を使うLL128方式を設計した。

- **2026-06 · [When Good Enough Is Optimal: Multiplication-Only Matrix Inversion Approximation for Quantized Gated DeltaNet](2026-2606.06034-when-good-enough-is-optimal-multiplication-only-matrix-inversion-approxi.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  三角行列の逆行列を低次のノイマン級数と対角マスクと乗算のみの残差補正で近似し、逐次依存を消して神経処理装置の行列演算へ載せ、カーネルで最大5.2倍、層全体で最大24.6パーセントの削減を得た。

- **2026-06 · [TwinQuant: Learnable Subspace Decomposition for 4-Bit LLM Quantization](2026-2606.01556-twinquant-learnable-subspace-decomposition-for-4-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ランク成分と残差成分の両方を量子化しやすい分布へ学習で作り替える4ビット量子化により、FP16に近い精度を保ちながら最大1.8倍の高速化を得た。

- **2026-06 · [ReSET: Accurate Latency-Critical NVFP4 Reasoning via Step-Aware Temperature Scaling](2026-2606.13233-reset-accurate-latency-critical-nvfp4-reasoning-via-step-aware-temperatu.md)**  
  実装：[✓](https://github.com/aiha-lab/ReSET) ・ リポジトリ内被引用：1  
  ステップ相対のエントロピー閾値でサンプリング温度を切り替えてNVFP4推論の正解率を最大2.6ポイント回復し、小バッチ向けCUDAコアカーネルでBF16比最大1.97倍のデコード高速化を実現する方式。

- **2026-06 · [Qift: Shift-Friendly No-Zero W2 Post-Training Quantization for Rotated W2A4/KV4 LLM Inference](2026-2606.02823-qift-shift-friendly-no-zero-w2-post-training-quantization-for-rotated-w2.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Qiftは、大規模言語モデル（Large Language モデル; LLM）の推論を省メモリ化する際、2ビットの符号で表現できる四つの実数値をどこへ置くかを主題とする。通常の符号付き2ビット量子化は$\{-2,-1,0,+1\}$を復元値に使う。

- **2026-06 · [ERA: Entropy-Guided Visual Token Pruning with Rectified Attention for Efficient MLLMs](2026-2606.31982-era-entropy-guided-visual-token-pruning-with-rectified-attention-for-eff.md)**  
  実装：[✓](https://github.com/924973292/ERA) ・ リポジトリ内被引用：1  
  画像内の似た領域を一つの代表トークンへ統合すれば系列長は短くなるが、代表トークンの特徴ベクトルを平均しただけでは、注意機構がその領域に与える総重みを正しく保てない。LLaVA-1.5-7Bでは576個の視覚トークンを32個に減らしたとき、九評価の平均性能維持率93.4%を報告する。

- **2026-06 · [Ekka: Automated Diagnosis of Silent Errors in LLM Inference](2026-2606.04594-ekka-automated-diagnosis-of-silent-errors-in-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  異常信号なしに品質だけが劣化する提供基盤の誤りを、参照実装との中間状態の突き合わせで自動診断する仕組みを提案し、実在不具合17件で5回試行88パーセントの特定率と新規4件の確認済み診断を示した。

- **2026-05 · [ViBE: Co-Optimizing Workload Skew and Hardware Variability for MoE Serving](2026-2606.00735-vibe-co-optimizing-workload-skew-and-hardware-variability-for-moe-servin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  混合専門家モデル（Mixture of エキスパート; MoE）の分散推論では、入力トークンに応じて選択される専門家（専門家）が偏る。専門家並列（専門家 parallelism; EP）では各GPUが担当する専門家を処理した後に同期するため、あるGPUの処理が遅いと層全体が待たされる。したがってトークン数が等しくても実行時間は等しくならない。

- **2026-05 · [TLX: Hardware-Native, Evolvable MIMW GPU Compiler for Large-scale Production Environments](2026-2605.10905-tlx-hardware-native-evolvable-mimw-gpu-compiler-for-large-scale-producti.md)**  
  実装：[✓](https://github.com/facebookexperimental/triton) ・ リポジトリ内被引用：1  
  ワープグループ単位で役割と依存を明示する実行モデルをTritonの拡張として実装し、行列積で約200行の記述のまま最先端実装と同等の性能と、異なるベンダーへの移植を両立した。

- **2026-05 · [Self-Pruned Key-Value Attention: Learning When to Write by Predicting Future Utility](2026-2605.14037-self-pruned-key-value-attention-learning-when-to-write-by-predicting-fut.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長い会話、検索拡張生成、エージェントの反復処理ではKVキャッシュの容量とメモリ帯域がボトルネックとなる。読出し時だけ重要なKVを選ぶ疎注意方式は計算量を減らせるが、全KVを保存し続ける限り容量の増加は止まらない。

- **2026-04 · [InfiniLoRA: Disaggregated Multi-LoRA Serving for Large Language Models](2026-2604.07173-infinilora-disaggregated-multi-lora-serving-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ランク適応の保持と計算を基盤モデルから切り離して専用サーバーで共有し、遠隔実行の通信を専門家計算と二重に重ねて隠すことで、基盤モデルを複製せずに適応の保持容量だけを増やせるようにした分離型の多数適応提供方式。

- **2026-04 · [FoE: Forest of Errors Makes the First Solution the Best in Large Reasoning Models](2026-2604.02967-foe-forest-of-errors-makes-the-first-solution-the-best-in-large-reasonin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  提案手法RED（Refine First and Discard Subs）は、最初の解法を生成している途中で不確実性が高い箇所へ介入し、別解を無制限に増やす代わりに、複数の中間回答が十分に一致した時点で停止する。6種類の推論モデル、数学・科学の5課題で、通常復号と比較して正答率を改善しつつ生成トークンを37.7～70.4%削減した。

- **2026-04 · [Fleet: Hierarchical Task-based Abstraction for Megakernels on Multi-Die GPUs](2026-2604.15379-fleet-multi-die-gpu-megakernel.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Fleetは複数ダイGPUにチップレット単位の作業階層を追加し、永続カーネル内で同一L2を共有するCUを協調スケジュールしてLLMデコードの重み再利用と同期局所性を高める。

- **2026-04 · [EncFormer: Secure and Efficient Transformer Inference Over Encrypted Data](2026-2604.09975-encformer-secure-and-efficient-transformer-inference-over-encrypted-data.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  暗号文の詰め方を段階間で互換に保ち、境界の費用を最小変換基準で判定し、複素変換で転送を半分にする混合方式で、暗号化したままの推論の通信を最大30.4倍分、遅延を最大9.8倍分減らした。

- **2026-04 · [Diagonal-Tiled Mixed-Precision Attention for Efficient Low-Bit MXFP Inference](2026-2604.03950-diagonal-tiled-mixed-precision-attention-for-efficient-low-bit-mxfp-infe.md)**  
  実装：[✓](https://github.com/yifu-ding/MP-Sparse-Attn) ・ リポジトリ内被引用：1  
  注意の対角付近だけを高精度に残す混合精度と、量子化前処理の全面融合により、低ビット注意の誤差と前処理費用を同時に抑えた。

- **2026-04 · [DeInfer: Efficient Parallel Inferencing for Decomposed Large Language Models](2026-2604.17709-deinfer-efficient-parallel-inferencing-for-decomposed-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  分解済みLLMの並列推論を、低ランク空間での通信と固定バッファによるKV再構成で高速化し、NVLinkなし構成で最初のトークンまでの時間を約83パーセント削減する専用推論基盤。

- **2026-04 · [Bit-by-Bit: Progressive QAT Strategy with Outlier Channel Splitting for Stable Low-Bit LLMs](2026-2604.07888-bit-by-bit-progressive-qat-strategy-with-outlier-channel-splitting-for-s.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Bit-by-Bitは、事前学習済みLLMを重み2ビット、活性化2ビットまで量子化したときの精度低下と学習不安定性を抑える量子化対応学習（QAT）の方式である。RTX 4090の行列ベクトル積単体では形状によって11倍を超える高速化がある一方、小さい形状ではBF16より遅い。

- **2026-03 · [Mixture-of-Depths Attention](2026-2603.15619-mixture-of-depths-attention.md)**  
  実装：[✓](https://github.com/hustvl/MoDA) ・ リポジトリ内被引用：1  
  Mixture-of-Depths 注意機構（MoDA）は、深い大規模言語モデル（Large Language モデル; LLM）で浅い層に形成された情報が、繰り返す残差更新により後段で薄まる問題を対象とする。

- **2026-03 · [Kernel-Smith: A Unified Recipe for Evolutionary Kernel Optimization](2026-2603.28342-kernel-smith-a-unified-recipe-for-evolutionary-kernel-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLM推論エンジンの実効性能は、モデル演算そのものだけでなく、GPU上で実行される個別カーネルの融合、メモリ移動、起動費用、並列化に左右される。しかし一度だけコードを生成する方式は、コンパイルできても数値が間違っていたり、正しくても実測速度が遅かったりする。

- **2026-02 · [PackInfer: Compute- and I/O-Efficient Attention for Batched LLM Inference](2026-2602.06072-packinfer-batched-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  異種長要求を負荷均衡した群へ詰め、共有接頭辞を考慮した連続KV配置と一体化することで、注意計算の無駄と入出力断片化を同時に削減する。

- **2026-02 · [NanoQuant: Efficient Sub-1-Bit Quantization of Large Language Models](2026-2602.06694-nanoquant-efficient-sub-1-bit-quantization-of-large-language-models.md)**  
  実装：[✓](https://github.com/SamsungLabs/NanoQuant) ・ リポジトリ内被引用：1  
  NanoQuantは、事前学習済みLLMを追加の大規模訓練なしで1bitおよび実効1bit未満に圧縮する重み専用の事後量子化（PTQ）方式である。著者らは単一H100 80GBでLlama-2-70Bを約13時間かけて137.95GBから5.75GBへ圧縮し、RTX3050 8GB上で実行できると報告する。

- **2026-02 · [Deep Kernel Fusion for Transformers](2026-2602.11808-deep-kernel-fusion-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SwiGLU前半を単一CUDAカーネルへ深く融合して中間活性のHBM往復を削減し、事前プロファイルでGPU・バッチ別のタイル方式を選んでSGLangのデコードを最大13.2%高速化する。

- **2026-01 · [Mosaic: Unlocking Long-Context Inference for Diffusion LLMs via Global Memory Planning and Dynamic Peak Taming](2026-2601.06562-mosaic-unlocking-long-context-inference-for-diffusion-llms-via-global-me.md)**  
  実装：[✓](https://github.com/flashserve/Mosaic) ・ リポジトリ内被引用：1  
  Mosaicは、拡散型大規模言語モデル（diffusion-based Large Language モデル; dLLM）の長文脈生成で生じる、鍵・値キャッシュではなく一時活性化が容量の限界になるという問題を解く推論基盤である。過去KVを長期保持する手法だけでは、この大きな一時メモリを削れない。

- **2026-01 · [LLMs can Compress LLMs: Adaptive Pruning by Agents](2026-2601.09694-llms-can-compress-llms-adaptive-pruning-by-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、大規模言語モデル（LLM）の重みを間引く際、全層へ同じ間引き率を割り当てるのではなく、別のLLMを方針決定器として使う。

- **2025-12 · [KV Admission: Learning What to Write for Efficient Long-Context LLM Inference](2025-2512.17452-kv-admission-learning-what-to-write-for-efficient-long-context-llm-infer.md)**  
  実装：[✓](https://github.com/EMCLab-Sinica/WG-KV) ・ リポジトリ内被引用：1  
  KV破棄（追い出し）は容量を制限できる一方、一度書いたKVを後で捨てるため、不要な書込みや一時的なメモリ使用を防ぎにくい。本論文はこの二方式に先立つ第三の操作として、KV受入れ（admission）を明示的に定式化する。

- **2025-12 · [gpu_ext: Extensible OS Policies for GPUs via eBPF](2025-2512.12615-gpu-ext-extensible-os-policies-for-gpus-via-ebpf.md)**  
  実装：[✓](https://github.com/eunomia-bpf/gpu_ext) ・ リポジトリ内被引用：1  
  大規模言語モデル（Large Language モデル; LLM）の推論性能は、GPUの演算能力だけでなく、GPUメモリへ何を保持し、何をCPU側へ退避させ、いつ事前読み込みし、複数処理へどのように実行時間を割り当てるかに大きく左右される。

- **2025-12 · [Exact Flow Linear Attention: Exact Solution from Continuous-Time Dynamics](2025-2512.12602-exact-flow-linear-attention-exact-solution-from-continuous-time-dynamics.md)**  
  実装：[✓](https://github.com/declare-lab/EFLA) ・ リポジトリ内被引用：1  
  厳密流線形注意（Exact Flow Linear 注意機構、EFLA）は、デルタ則更新が、入力を一つのトークン区間で固定した連続時間の微分方程式を前進オイラー法（explicit Euler）で一歩近似したものと解釈できることを示す。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-11 · [Storing the Gemma 4 K=V Cache Once: Exact Global-KV Memory Savings in a Paged Serving Engine with Unchanged Attention Kernels](2026-2611.23035-storing-the-gemma-4-k-v-cache-once-exact-global-kv-memory-savings-in-a-p.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Gemma 4の全体注意層でキーと値が同じ射影から決まる冗長性を使い、640値の行を二つの重なるビューで既存カーネルに読ませてKVキャッシュを一度だけ保存することで、注意カーネル無改変のまま定常デコードのKVメモリを1.34倍から1.40倍小さくするvLLM試作。

- **2026-11 · [LiquidCP: Decoupling Attention Tasks from Communication and Kernel Boundaries in Context Parallelism](2026-2611.04401-liquidcp-decoupling-attention-tasks-from-communication-and-kernel-bounda.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の作業を通信とカーネルの境界から切り離し、学習側では注意量とトークン量を両方均す配置と届いた範囲での随時実行、デコード側では注意と集約の完了を一緒に予測する分割計画で、中核注意を幾何平均で一点一八倍から一点三五倍速くしたと報告した。

- **2026-11 · [IsoMoE: Placement-Invariant Hybrid CPU-GPU MoE Inference with Lossless 12-bit Experts](2026-2611.27604-isomoe-placement-invariant-hybrid-cpu-gpu-moe-inference-with-lossless-12.md)**  
  実装：[✓](https://anonymous.4open.science/r/isomoe-artifact-9C21/) ・ リポジトリ内被引用：0  
  CPUとGPUでエキスパートを分担するハイブリッドMoE推論で、配置が変わると出力まで変わる問題に対し、GPUがCPUの演算をビット単位で再現し、無損失12ビット形式をCPU向けの並びで保持することで、配置不変のビット同一出力を保ちながら平均1.26倍のデコード高速化を得る方式。

- **2026-11 · [Fused-Softmax for efficient quantized attention](2026-2611.09225-fused-softmax-for-efficient-quantized-attention.md)**  
  実装：[✓](https://github.com/ROCm/aiter) ・ リポジトリ内被引用：0  
  行最大値の凍結と巻き戻し、指数のアフィン近似の行列積への畳み込み、確率の2段階変換と行和の行列積化で、ソフトマックスのベクトル仕事をほぼ消した量子化注意カーネルを MI355X で実装し、BF16比で最大3.2倍のカーネル高速化と動画生成で最大2.05倍の高速化を示した研究。

- **2026-11 · [EpiLoRA: Fusing Many LoRA Adapters into Low-Precision GEMMs for Serving and RL](2026-2611.03899-epilora-fusing-many-lora-adapters-into-low-precision-gemms-for-serving-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  アダプタの下向き射影を先に走らせ低精度の行列積の本体と重ね、上向き射影を行列積の書き出し段で加える方式で、単一アダプタのトークン当たり時間を最大二十四パーセント短縮し、同じ八ビット重みでの訓練により二百七十億級が四十八ギガバイト一台で訓練可能になったと報告した。

- **2026-11 · [CipherFlow: Compiling AI Programs for Efficient Cryptographically Secure Inference](2026-2611.01450-cipherflow-compiling-ai-programs-for-efficient-cryptographically-secure-.md)**  
  実装：[✓](https://github.com/loopleap-lab/CipherFlow) ・ リポジトリ内被引用：0  
  暗号プリミティブの実測コストと暗号文の状態まで含めた計画探索で、準同型暗号とマルチパーティ計算の配置・変換・維持を自動決定し、静的配置より最大22倍速いセキュア推論プログラムを生成するコンパイラ。

- **2026-11 · [CacheWeave: Learning to Recompute for Efficient Position-Independent KV Caching](2026-2611.01735-cacheweave-learning-to-recompute-for-efficient-position-independent-kv-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  位置を問わない区画キャッシュの再利用へ適応したモデル自身で学習した選択器が、注意得点を使わずに再計算すべき区画を選ぶことで、予算百分の五で規則型二方式を全組で上回り完全な入力処理への相対低下を最大百分の八・三に抑え、初回トークン時間を最大十六・一倍、有効スループットを最大七・八倍にしたと報告した。

- **2026-11 · [Berth: SLO-Preserving GPU Sharing Without New Preemption](2026-2611.25091-berth-slo-preserving-gpu-sharing-without-new-preemption.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  市販GPUの時間分割が持つ横取り能力を外側から活かし、ベストエフォート作業への供給をリクエスト不在時だけに絞り、短い時間スライスで実行中カーネルの費用を抑えることで、カーネルやドライバを変えずにサービス品質目標とGPU利用率を両立させた共有方式。

- **2026-11 · [Ask, Don't Equip: Question-Driven Coding Agents for Deep Kernel Optimization](2026-2611.03517-ask-don-t-equip-question-driven-coding-agents-for-deep-kernel-optimizati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  カーネル最適化エージェントへ装備を足す代わりに、検証可能な目標を強制する最小の基盤と、判断の節目で残りの差の所在を問う短い問いを与え、直接対決で装備型の〇・五〇倍に対し一点一三倍、依存なし注意カーネルで上流比最大一点四六倍を報告した。

- **2026-11 · [AscMLA: Unlocking FP4 Efficiency for Long-Context MLA Decoding through Asymmetric Scaling](2026-2611.26106-ascmla-unlocking-fp4-efficiency-for-long-context-mla-decoding-through-as.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MLAの共有潜在をFP4化するとキー側と値側でブロック・スケールの軸が食い違う問題に対し、符号は1つに共有したまま値側はトークン単位スケールを確率へ畳み込み、キー側は16チャネル単位スケールを後から合わせる非対称スケーリングと、寿命の違う2種のスケールの配送最適化で…

- **2026-10 · [When Shards Fly: Cross-Tensor In-Flight Conversion for Low-Latency, Low-Memory Weight Updates in Disaggregated RL](2026-2611.00646-when-shards-fly-cross-tensor-in-flight-conversion-for-low-latency-low-me.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  訓練側からロールアウト側への重み同期で、シャード対応付けとレプリカ経路を再利用可能な計画へまとめ、変換と量子化と通信と書き込みを持続カーネルへ融合することで、完全更新を最大27.92倍速くし通信メモリも最小水準にした研究。

- **2026-10 · [Understanding GPU Megakernels: Why Residency Can Mislead](2026-2611.00495-understanding-gpu-megakernels-why-residency-can-mislead.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  巨大核を元の演算子符号のまま別々の核へ再構成して比べ、依存起動で起動と先読みを重ねれば常駐実行に並ぶか百分の五・七上回ること、常駐側は順序付け費用が先読みで膨らむこと、早期準備の障害は処理ブロック単位の資源の受付制約であることを実測で示した分析である。

- **2026-10 · [TranSAGE: Automating Spatial Accelerator Generation for Large-Scale Transformer Models](2026-2610.32279-transage-automating-spatial-accelerator-generation-for-large-scale-trans.md)**  
  実装：[✓](https://github.com/sjtu-zhao-lab/TranSAGE) ・ リポジトリ内被引用：0  
  複数演算のパイプライン化を前提に、グラフ分割とデータフロー探索で演算クラスタとアーキテクチャを共同で決め、回路記述まで自動生成する、トランスフォーマ向け空間アクセラレータのコンパイラ型生成器。

- **2026-10 · [TenonAgent: Virtualizing Execution Residency for Memory-Oversubscribed LLM Agents](2026-2611.00051-tenonagent-virtualizing-execution-residency-for-memory-oversubscribed-ll.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMエージェントのサンドボックス常駐を仮想化し、アクション境界の予測受付と再起動安全な解体、実行中のカーネル側ペーシングでホストメモリの過剰割当てを安全に行うランタイムを提案した研究。

- **2026-10 · [SyclKittens: A Tile Programming Model for Programmers and Coding Agents on Intel GPUs](2026-2610.04277-syclkittens-a-tile-programming-model-for-programmers-and-coding-agents-o.md)**  
  実装：[✓](https://github.com/intel/SyclKittens) ・ リポジトリ内被引用：0  
  インテルGPUで速くなる書き方そのものを操作として内蔵したタイル型プログラミングモデルを提示し、生の言語よりコーディングエージェントが速いカーネルへ早く届くことと、推論の高速化を実測で示した研究。

- **2026-10 · [SparseGDN: Chunk Sparse in Linear Attention](2026-2610.41420-sparsegdn-chunk-sparse-in-linear-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈のゲート付きデルタネットワークの入力処理を、ブロック隣接のデルタ解法と頭の組ごとの再帰イベント選択の二段で疎化し、平均で約二十九パーセントのイベントだけを残して核の入力処理を一点五倍から一点九四倍速くし、集計精度をほぼ維持したと報告した。

- **2026-10 · [Scaling LLM Inference via Parallelism: Throughput-Latency Trade-off](2026-2610.19405-scaling-llm-inference-via-parallelism-throughput-latency-trade-off.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しい注意カーネル、重み圧縮器、GPU間通信プリミティブを提案する論文ではない。実験はQwen2.5-14B-Instruct、BF16、NVIDIA H200 141GBを8基、vLLM v0.15.0という条件で行われた。

- **2026-10 · [SARATHI: Decoupled Data-Free Probing and Adaptive Reconstruction for Structured LLM Pruning](2026-2610.15514-sarathi-decoupled-data-free-probing-and-adaptive-reconstruction-for-stru.md)**  
  実装：[✓](https://github.com/snkrbhr/SARATHI) ・ リポジトリ内被引用：0  
  ニューロン選択を校正データなしの非負行列分解の残差探査に分離し、補償を層ごとの局所再構成に限定することで、除去率40パーセントで他法がメモリ不足や崩壊に陥る条件でも完走し、OPT-2.7Bの困惑度を補正なし2082から18.98へ戻した。

- **2026-10 · [Reorienting the Vector Axis: Restructuring FlashAttention for Long-Vector Processors](2026-2610.29489-reorienting-the-vector-axis-restructuring-flashattention-for-long-vector.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長ベクトルプロセッサ向けにFlashAttentionのスコアタイルと累積出力を転置してクエリ軸をベクトル長にし、行ごとの縮約を消し、指数関数の多項式係数をスカラーレジスタへ逃がすことで、実チップでカーネルを1.84倍から2.08倍高速化するカーネル再構成の研究。

- **2026-10 · [PhOSv1: Efficient Scaling of Model Sleeping on a Single Server for Autoscaling with GPU-Context Deduplication](2026-2610.39999-phosv1-efficient-scaling-of-model-sleeping-on-a-single-server-for-autosc.md)**  
  実装：[✓](https://github.com/blitz-serving/PhoenixOSv1) ・ リポジトリ内被引用：0  
  休眠モデルの図形処理装置文脈の重複を中央の常駐プログラムで取り除き、二十三モデル分の文脈容量を九十八・一パーセント減らしながら休眠と同等の起動時間を保ち、複数モデル提供で最初のトークンまでの平均時間を八十七パーセント短くしたと報告した。

- **2026-10 · [Mosaic: GPU Sharing with Latency Guarantees through Kernel-Level Interference Prediction](2026-2610.07504-mosaic-gpu-sharing-with-latency-guarantees-through-kernel-level-interfer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  干渉源をスレッドブロック配置、メモリ階層競合、SM内競合へ分解してカーネル単位で減速を予測し、受付制御と同居方式選択で高優先処理のP99遅延のSLOを守るGPU共有方式。

- **2026-10 · [MOLT: A Fine-Grained GPU Memory Sharing System for LLM Serving with Opportunistic Fine-Tuning](2026-2610.05748-molt-a-fine-grained-gpu-memory-sharing-system-for-llm-serving-with-oppor.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  推論レプリカの遊休メモリを、実行中PEFTステップの保存済み活性値1個単位で推論へ引き渡し、ステップを捨てずに逆伝播の再計算で取り戻す細粒度GPUメモリ共有方式。

- **2026-10 · [Learning Structured Sparsity for Large Models: Bridging Model Compressibility and Efficient Inference](2026-2610.31897-learning-structured-sparsity-for-large-models-bridging-model-compressibi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの低ランク成分と構造化スパース成分を学習時に一体で学び、単一チェックポイントから複数メモリ予算へゼロショットで圧縮し、ブロック専用カーネルでメモリ削減を実際の推論高速化へ変換する、エッジ推論向けの弾性圧縮の枠組み。

- **2026-10 · [Is 2:4 Sparsity Still Worth It? Semi-Structured Sparsity versus Quantization in LLM Inference](2026-2610.28947-is-2-4-sparsity-still-worth-it-semi-structured-sparsity-versus-quantizat.md)**  
  実装：[✓](https://github.com/PuppyQ08/24_quant_compare) ・ リポジトリ内被引用：0  
  2対4スパース性と量子化を等ビットと等階層で全オペランド実測比較し、床より上では一段の量子化が常に勝ち、床でのみ再学習を条件に2対4が1.3倍から1.7倍の高速化と27パーセントのプリフィル改善をもたらすことを、エネルギー損失の解析とともに示した研究。

- **2026-10 · [Inference First, Training Underneath: Layer-Granular LoRA Co-Serving with LayerLoom](2026-2611.00652-inference-first-training-underneath-layer-granular-lora-co-serving-with-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク適応の逆伝播を層単位へ分解し、推論の順伝播へ同層の逆伝播だけを遅延余裕の範囲で差し込むことで、需要急増時でも推論の目標達成率を守りながら空き容量を学習へ使う同時提供ランタイム。

- **2026-10 · [HiNa-MoE: High-Performance, Non-Intrusive MoE Inference on CPUs with Matrix Engines](2026-2610.05123-hina-moe-high-performance-non-intrusive-moe-inference-on-cpus-with-matri.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパート重みを標準レイアウトのまま残し、変換は小さい中間行列側へ融合し、ページのインターリーブ配置に合わせたタスク分割で遠隔参照を消すことで、フレームワーク無改変でCPU側の混合専門家計算を高速化する演算子ライブラリ。

- **2026-10 · [GPU Goldmines: Tunable WebGPU Kernels for Edge LLM Inference](2026-2610.17321-gpu-goldmines-tunable-webgpu-kernels-for-edge-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  WebGPU向けLLMカーネルを行列積・行列ベクトル積・フラッシュアテンションについて調整可能化し、実測を中央データベースへ蓄積することで、装置やブラウザをまたいだ性能移植性の測定、移植可能設定の選択、未知装置への調整高速化を実現する枠組み。

- **2026-10 · [gKSM: GPU Memory Deduplication at Driver Layer for Serverless LLM Inference](2026-2610.25219-gksm-gpu-memory-deduplication-at-driver-layer-for-serverless-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ドライバ層で重複した重みページを検出して物理ページを共有し、転送前の重複除去と書き込み時コピーで分離を保つことで、フレームワークを改変せずに同居インスタンスのメモリ重複を最大59.8パーセント削減する方式。

- **2026-10 · [From Overloaded to Guaranteed: High-Throughput Multi-SLO Enforcement for LoRA-Assisted On-Premise LLM Deployment](2026-2610.04956-from-overloaded-to-guaranteed-high-throughput-multi-slo-enforcement-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オンプレミスの複数LoRAサービングで、ベース層とLoRA層へのSM分割による同時実行と、リクエスト単位スラックに基づくプリフィル・デコード統合スケジューリングにより、異種SLO違反を減らしながらスループットを上げる方式。

- **2026-10 · [Fast and Exact Relative-Position Attention via Structure-Aware Kernels](2026-2611.01182-fast-and-exact-relative-position-attention-via-structure-aware-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  相対位置アテンションの加算項を稠密なバイアス行列にせず、届く範囲だけへの射影、同じ関係行になるタイルでの読み出し再利用、オフセット単位の原子操作なし勾配集約によってFlashAttention式タイル計算へ正確に組み込むカーネル研究。

- **2026-10 · [CompileMask: Bridging the Gap Between Expressiveness and Efficiency in Attention Masking](2026-2610.13474-compilemask-bridging-the-gap-between-expressiveness-and-efficiency-in-at.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意マスクの利用者向け仕様をオフラインコンパイラで区間表現へ変換し、端点の事前計算によりカーネル内の可視判定を軽くすることで、表現力と実行効率を両立させる注意実行基盤。

- **2026-10 · [Cleave: Scaling Tensor Program Optimization via Decoupled Algebraic Search and Operator Scheduling](2026-2610.07742-cleave-scaling-tensor-program-optimization-via-decoupled-algebraic-searc.md)**  
  実装：[✓](https://github.com/nyu-systems/cleave) ・ リポジトリ内被引用：0  
  形状を記号化して代数変換の探索をスケジューリングから分離し、反復タイリングと水平融合で複数リダクションを含むグラフを自動で融合カーネル化するコンパイラ。手書き注意カーネル級の最適化を自動生成する。

- **2026-10 · [Causal Attention on CPU: A Cache-Aware and Load-Balanced Scheduling Kernel for Prefill](2026-2610.38809-causal-attention-on-cpu-a-cache-aware-and-load-balanced-scheduling-kerne.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUのL3とL2キャッシュへ注意のループ構造を合わせ、因果マスクで生じるスレッド間の負荷不均衡を費用優先の共有キューで均すことで、長文脈プリフィルのCPU注意カーネルを最大2.01倍速くしTTFTを最大1.74倍改善する方式。

- **2026-10 · [BiLoCo: Binary Low-Rank Corrections for Post-Training Quantization](2026-2610.32243-biloco-binary-low-rank-corrections-for-post-training-quantization.md)**  
  実装：[✓](https://github.com/jindavid/BiLoCo) ・ リポジトリ内被引用：0  
  4ビット量子化への低ランク補正を、16ビット因子から符号だけの二値因子へ置き換えて同じ保存量で16倍のランクを使い、補正の計算を遊んでいる汎用コアへ逃がして本体の行列積と並行実行する量子化方式と融合カーネル。

- **2026-10 · [AlignQuant: Tile-Aligned Mixed-Precision Quantization for Efficient LLM Generation](2026-2610.07457-alignquant-tile-aligned-mixed-precision-quantization-for-efficient-llm-g.md)**  
  実装：[✓](https://github.com/HanzhiZhang-Ulrica/AlignQuant) ・ リポジトリ内被引用：0  
  重みの二次元タイルを精度配分・詰め込み保存・GPU実行の共通単位とし、プリフィルとデコード両方の損失感度で各タイルの4ビット／8ビットを決めて、1つの詰め込みモデルを段階専用カーネルで直接実行する混合精度量子化。

- **2026-10 · [AdaSpark: Adaptive DSpark with Online Learning for Tree Verification and N-gram Fill](2026-2610.05774-adaspark-adaptive-dspark-with-online-learning-for-tree-verification-and-.md)**  
  実装：[✓](https://github.com/zeraix/imparo) ・ リポジトリ内被引用：0  
  AdaSparkは、投機的復号の草案器が一度に提案した複数候補を、大きな教師モデルが何行まとめて検証するかを実行時に決めるスケジューラである。4モデル・6公開データセットの会話で、llama.cppのDSparkより復号速度が約1.5〜3.1倍となった。

- **2026-09 · [Weave: Fine-Grained Dynamic SM Scheduling in an MoE Megakernel for Compute-Communication Overlap](2026-2609.21483-weave-fine-grained-dynamic-sm-scheduling-in-an-moe-megakernel-for-comput.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ルーティング結果が判明した直後に、永続メガカーネル内のコストモデルで層ごとGPUごとに通信用と計算用のSM分割と実行順を動的に決め、MoE層を幾何平均2.89倍高速化する重ね合わせ方式。

- **2026-09 · [WavePP: High-Throughput Pipeline Parallel LLM Prefill under Prefix Reuse](2026-2609.35263-wavepp-high-throughput-pipeline-parallel-llm-prefill-under-prefix-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再利用できる範囲の合意、キャッシュを削除されないように保護する処理、未計算部分のメモリ確保を同期的に行うと、GPUに次の入力を供給する頻度が下がり、段の間に空き時間が発生する。準備が整った要求は処理波（wave）に分割し、パイプラインを埋めるように波の大きさを動的に選ぶ。

- **2026-09 · [Unleashing the Power of Equality Saturation for Tensor Program Superoptimization](2026-2609.12330-unleashing-the-power-of-equality-saturation-for-tensor-program-superopti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特定の注意機構パターンを手書きで登録するのではなく、softmaxの依存関係を修復しながらreductionを融合する規則から、online softmaxを含む融合カーネルを導くことができる。

- **2026-09 · [Understanding LLM Quantization through Activation-Guided Compensation and Orthogonal Residuals](2026-2609.21450-understanding-llm-quantization-through-activation-guided-compensation-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みと活性値をともに4ビットへ縮小する学習後量子化では、特定の活性値チャネルに継続的に現れる大きな値が、量子化に使用する尺度を広げ、通常値に割り当てられる表現段階を粗くする。

- **2026-09 · [SketchSSM: Write to the Full State, Read from a Compact Sketch](2026-2609.33051-sketchssm-write-to-the-full-state-read-from-a-compact-sketch.md)**  
  実装：[✓](https://github.com/SNU-ARC/SketchSSM) ・ リポジトリ内被引用：0  
  回帰状態の更新は全状態で正確に行い、読み出しは固定クエリ基底への事前計算出力を集めた小さなスケッチの線形結合で近似する学習不要の方式で、状態転送を約10倍減らしながら精度を保ちデコードを最大2.77倍高速化した。

- **2026-09 · [Shift-Accumulate Attention: Multiplier-Free Query--Key Products for Transformer Decoding](2026-2609.09208-shift-accumulate-attention-multiplier-free-query-key-products-for-transf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の2の冪乗（power-of-two、PoT）量子化は、主として後者の重みをシフト演算に変える用途で使われてきた。RTX 4090のTinyLlama-1.1B-Chatでは、バッチ8、文脈32,768の条件で4ビット鍵を使う注意カーネルがFP16 SDPA比4.60倍高速だった。

- **2026-09 · [REVISE: Validity-Guided Recovery for Online Revisions in Agent Workflows](2026-2609.00643-revise-validity-guided-recovery-for-online-revisions-in-agent-workflows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行中のエージェントへの指示差し替えに対し、依存関係から影響範囲だけを特定して無効な作業を止め有効な進捗を再検証して流用するランタイムにより、古い出力を出さずにモデル呼び出しを全面再開より最大56.0%削減する回復方式。

- **2026-09 · [Programming AMD XDNA NPUs with Open-source Compiler Tools: A FlashAttention Case Study](2026-2609.21264-programming-amd-xdna-npus-with-open-source-compiler-tools-a-flashattenti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  XDNAは複数の計算タイルと小さな局所メモリ、共有メモリタイル（MemTile）、外部メモリとの入出力を担うshimタイルから構成され、DMAとストリームの経路をソフトウェアが明示的に設計する。

- **2026-09 · [Model Casting and Low-Parameter Gating: Towards More Sparsely Activated FFNs](2026-2609.31975-model-casting-and-low-parameter-gating-towards-more-sparsely-activated-f.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中間訓練で活性化を替えて全結合層の中間活性を目標どおり疎にし、低ランク化したゲートで理論上限3倍を超え、同一品質で学習不要方式の2倍の計算削減を得る方式。

- **2026-09 · [KV-Kaizen: Learning Context-Adaptive Cache Compression Choices](2026-2609.37988-kv-kaizen-learning-context-adaptive-cache-compression-choices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  例えばQwen2.5-14Bの非圧縮キャッシュは1トークン当たり192 KiBを占め、8,000トークンの系列32本を同時に保持すると約48 GiBに達する。Qwen2.5-14Bの16K文脈では、提案法による4倍圧縮とSnapKVによる8分の1トークン保持を組み合わせ、復号時KV容量を32分の1にして質問応答精度0.531を得た。

- **2026-09 · [Herschel: Continuous Optimization of Production LLM Inference through On-Demand Profiling](2026-2609.40247-herschel-continuous-optimization-of-production-llm-inference-through-on-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本番LLM推論へ再起動なしに取り付けるオンデマンドプロファイリングと、非効率パターンの照合、AIエージェントによる統制実験を組み合わせた継続的最適化システムを提案した研究。

- **2026-09 · [Hardware-Native Joint Sparse-Quantization for Trillion-Scale Mixture-of-Experts](2026-2610.02241-hardware-native-joint-sparse-quantization-for-trillion-scale-mixture-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エキスパート重みの疎性パターン選択を連続緩和で量子化と同時に学習し、対になった4対8のNVFP4表現へ圧縮して、スパーステンソルコア向けのグループ化した疎行列積で実行する、兆級MoE向けの共設計圧縮枠組み。

- **2026-09 · [Hardware Characterization of Diffusion vs. Autoregressive Language Model Inference: Compute vs. Memory Bottlenecks](2026-8d428e79f81e-hardware-characterization-of-diffusion-vs-autoregressive-language-model-.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21839997) ・ リポジトリ内被引用：0  
  拡散言語モデルの推論をGPUカーネルとメモリ階層で実測し、自己回帰デコードと違って計算律速で活性値支配的であり、ブロック長がハードウェア調整パラメータになることを示した特性分析。

- **2026-09 · [ForgeMegakernel: A General Framework for Efficient Auto-Regressive Model Decode Megakernels](2026-2609.12379-forgemegakernel-a-general-framework-for-efficient-auto-regressive-model-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの自己回帰デコードは、次の1トークンを計算するたびにモデルの重みとKVキャッシュを読み込む。対話的な小バッチでは、GPUの演算器が飽和する前にHBMからの転送が律速になりやすい。通常の推論エンジンは線形層、正規化、RoPE、注意、KV書込み、語彙射影を別々のGPUカーネルで実行する。

- **2026-09 · [FoldAttention: Declared-Reference Softmax for Fast Decode and Deterministic Backward](2026-2609.33410-foldattention-declared-reference-softmax-for-fast-decode-and-determinist.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈の自己回帰デコードでは、次の一トークンを作るたびに伸び続けるKVキャッシュを参照する。後方計算では、CTAごとの部分勾配を共通整数格子へ丸めて加算することで、加算順序に依存しない決定的な勾配を得る。

- **2026-09 · [Exploring the Efficiency of 3D-Stacked AI Chip Architecture for LLM Inference with VOXEL](2026-2604.26821-exploring-the-efficiency-of-3d-stacked-ai-chip-architecture-for-llm-infe.md)**  
  実装：[✓](https://github.com/yiqiliu2/voxelsim) ・ リポジトリ内被引用：0  
  VOXELは、演算コアの上に多数のDRAMバンクを三次元積層したAIチップを対象に、コンパイラが生成する演算配置・データ配置と、分散メモリ・オンチップ通信・熱制約を一体として評価するシミュレータである。性能差の大部分は設計空間を模擬した結果であり、量産シリコンの確定性能として扱わない。

- **2026-09 · [EFQ-Softmax: Exp-Free Quantization for Softmax](2026-2609.09721-efq-softmax-exp-free-quantization-for-softmax.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の確率生成から高精度な指数関数と事後量子化を外し、ずらしたスコアをブロック単位スケール付きのE2M1コードへアフィン規則で直接変換して、分子と分母で共有する低ビット確率生成法。

- **2026-09 · [Does Execution Require Target KV Fidelity? A Mixed-Fidelity KV Runtime for LLM Serving](2026-2609.33536-does-execution-require-target-kv-fidelity-a-mixed-fidelity-kv-runtime-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は精度が完全でないKVでも、処理を進める方が総遅延を小さくできるという観察から、KVの精度を実行時に変更するElasticKVを提案する。

- **2026-09 · [Dissecting How Die Scaling Breaks GPU Fine-grained Scheduling](2026-2609.24270-dissecting-how-die-scaling-breaks-gpu-fine-grained-scheduling.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ダイスケーリングが作る個体ごとの計算トポロジーとメモリの非一様性を軽量な実測で暴き、割当てる資源の個数ではなく物理的な割当て先まで考えることで、主流カーネルを最大1.22倍、多重化した言語モデル推論を最大14.3パーセント速くした分析と改善の研究。

- **2026-09 · [DeepSeek-V4-Flash on AMD gfx90a: Correctness Recovery and Inference Performance Engineering](2026-2609.15627-deepseek-v4-flash-on-amd-gfx90a-correctness-recovery-and-inference-performance-engineering.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MI250上のDeepSeek-V4-Flashで数値不具合を修復し、CDNA2向けカーネル・通信・事前充填最適化によりTP8復号をC64で1327.10トークン/秒まで実測した。

- **2026-09 · [ConvMem: Convolutional Memory for Long-Context Reasoning](2026-2609.10441-convmem-convolutional-memory-for-long-context-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  質問付きの凍結モデルをカーネルとして文書を重なり窓で並列走査し、要約を対数深さの木で集約する学習不要の長文推論で、分布外課題でも強化学習型メモリの過適合を避けて精度を保つ。

- **2026-09 · [AttnFuse: A Composable DSL for Compiling Attentions to Fused GPU Kernels](2026-2609.13612-attnfuse-a-composable-dsl-for-compiling-attentions-to-fused-gpu-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しい注意方式を論文で定義できても、そのまま高速に実行できるとは限らない。注意はクエリとキーの行列積、マスク、正規化、値との積などを繰り返し、処理を別々のGPUカーネルで行うと中間テンソルの書込みと再読込みが生じる。

- **2026-09 · [A Multi-Engine Dataflow for MoE Decoding on AWS Tranium](2026-2609.21137-a-multi-engine-dataflow-for-moe-decoding-on-aws-tranium.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各トークンについて一部の専門家だけを選択するため演算回数は節約できるが、専門家の選択がルータの計算後に確定するため、選ばれた専門家の重みを高帯域幅メモリ（HBM）から片上の明示管理メモリへ転送する時間が残る。従来の単純な専門家重み圧縮だけでは、索引検索や形式変換の計算が増えて総遅延が悪化し得る。

- **2026-08 · [UnionSparse: An Index-Efficient Sparsity Framework for Low-Bit Sparse LLM Inference on Edge](2026-2608.09291-unionsparse-index-efficient-low-bit-sparse-inference.md)**  
  実装：[✓](https://github.com/Victor-Alen/UnionSparse) ・ リポジトリ内被引用：0  
  低ビット化で相対的に増える疎行列の位置情報負担をPMRで定量化し、共有ビットマップ表現と並列復号カーネルを共同設計してJetson上の小バッチ疎推論を高速化する。

- **2026-08 · [Symbiotic MLLM Serving: Dynamically Balancing Parallelism Across GPUs and Resources Within GPUs](2026-a953baa22bb6-symbiotic-mllm-serving-dynamically-balancing-parallelism-across-gpus-and.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の文字列専用LLMサービングを拡張する場合、画像符号化器を生成器と同居させるか、固定されたGPU群へ分離することが多い。実装はSGLang 0.4.7を基礎とし、8基のNVIDIA A100 SXM 80GBとNVLinkを備える単一サーバで評価された。

- **2026-08 · [Serving Masked Diffusion LLMs: Characterization and Design Principles from Real Hardware](2026-2608.23807-serving-masked-diffusion-llms-characterization-and-design-principles-fro.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、マスク拡散言語モデル（masked diffusion language モデル、以下dLLM）を多数の利用者へ提供するとき、どの処理が遅延を生み、要求ごとの計算量がどのように変動し、バッチ処理で何を共有すべきかを実機で調べた特性分析である。新しい復号アルゴリズムや完成した推論サーバーの提案ではない。

- **2026-08 · [Reduced Matrix Multiplication: Input-Adaptive Matrix-Product Reduction for LLM Inference](2026-2608.13426-reduced-matrix-multiplication-input-adaptive-matrix-product-reduction-fo.md)**  
  実装：[✓](https://github.com/Zesearch/rmm-llm) ・ リポジトリ内被引用：0  
  行列積の乗算軸を入力の活性値で決定的に間引く学習不要の削減法で、保持率一つで費用と品質を調整し、注意側が全結合側より削減しやすい非対称性を示しつつ、長系列で実測1.40倍の高速化を得る研究。

- **2026-08 · [Opt.Gear Technical Report](2026-2608.01034-opt-gear-technical-report.md)**  
  実装：[✓](https://huggingface.co/OptGear) ・ リポジトリ内被引用：0  
  局所層のKVキャッシュを固定長の畳み込み状態へ置き換えるConvKV-Gated Mixerと、ヘッシアン初期化つき量子化対応学習で、端末NPUでの高速推論とマイコン上での生成までを狙うオンデバイス基盤モデルOpt.Gearの技術報告。

- **2026-08 · [OCGQuant: Outlier-Companion Grouping for NVFP4 Quantization](2026-2609.00066-ocgquant-outlier-companion-grouping-for-nvfp4-quantization.md)**  
  実装：[✓](https://github.com/Eshamont/OCGQuant) ・ リポジトリ内被引用：0  
  NVFP4のブロック内で外れ値が通常値を巻き込む誤差に着目し、外れ値チャネルへ低振幅チャネルだけを同伴させる並べ替えで、Qwen3-1.7Bの困惑度をRTNの19.25から16.71へ下げ、入力処理で最大2.29倍の高速化を保った量子化手法。

- **2026-08 · [MonoMoE: An Efficient Fused Mega-kernel for Quantized MoE Decoding](2026-2609.04244-monomoe-fused-megakernel-quantized-moe-decoding.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer/tree/main/csrc/fused_moe/monomoe) ・ リポジトリ内被引用：0  
  少トークンMoE復号を重み主導型の常駐巨大カーネルへ再構成し、ルーティングから二段の専門家射影と縮約までを融合してメモリ帯域利用を高める。

- **2026-08 · [LLM4LLM: Bridging Kernel Benchmarks and Real Deployment via Closed-Loop Agentic Optimization](2026-2608.21836-llm4llm-bridging-kernel-benchmarks-and-real-deployment-via-closed-loop-agentic-optimization.md)**  
  実装：[✓](https://github.com/hzeng2000/LLM4LLM) ・ リポジトリ内被引用：0  
  実モデルを計測して段階別カーネルを探索し、モデル内検証まで閉ループ化してA100/H100で幾何平均3.91倍/6.98倍の端から端までの高速化を達成する。

- **2026-08 · [Intern-S2-Mobius: Foundation Model with Decoupled Knowledge and Reasoning](2026-2608.14290-intern-s2-mobius-foundation-model-with-decoupled-knowledge-and-reasoning.md)**  
  実装：[✓](https://github.com/InternLM/Intern-S2-Mobius) ・ リポジトリ内被引用：0  
  通常のTransformerは各層でSelf-注意機構とFFNが対になり、前の層の隠れ状態を次の層へ送る。スクラッチ学習では7B-A1BのMobiusがTransformerと同程度のMMLUを達成するのに0.626倍の訓練トークンしか必要としない。

- **2026-08 · [FSGen: Agile Fused and Sparse Accelerator Generator with Accurate Power Model for LLM Applications](2026-2608.09252-fsgen-agile-fused-and-sparse-accelerator-generator-with-accurate-power-m.md)**  
  実装：[✓](https://github.com/hkust-zhiyao/FSGen) ・ リポジトリ内被引用：0  
  融合演算データフローと多層の疎性を統一表現で扱い、ChiselによるRTL生成とプリミティブ単位の機械学習電力モデルで広い設計空間を高速に探索するLLMアクセラレータ生成器FSGenを提案し、先行生成器比で最大58倍の性能指標を達成した。

- **2026-08 · [Daedalus-150M: A Convolution-Attention Hybrid Designed for CPU Inference](2026-2608.20210-daedalus-150m-a-convolution-attention-hybrid-designed-for-cpu-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUでのバッチ1デコードを先に固定し、18層中12層を状態が2ステップで一定の短い畳み込みへ置き換えてKVキャッシュの読み直しを消すことで、文脈2048で全注意の同規模対照より1.76倍速く、品質は同等以上を保つ小型ハイブリッドモデル。

- **2026-08 · [Celty: SpMspV GPU Kernel and SIMT Co-Design for Efficient Dual-Sparse LLM Inference](2026-2608.01536-celty-dual-sparse-gpu-kernel.md)**  
  実装：[✓](https://github.com/RuokaiYin/Celty) ・ リポジトリ内被引用：0  
  重み疎性と実行時活性疎性の交差を疎行列×疎ベクトルとして扱い、走長圧縮形式、ワープ割当、レジスタ部分和、専用復号器を共同設計して低バッチLLMデコードを高速化する。

- **2026-07 · [X-Stage: Modeling Post-Issue Backpressure in GPU Communication–Computation Fusion](2026-2607.23264-x-stage-modeling-post-issue-backpressure-in-gpu-communication-computatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  遠隔書き込みの発行後区間を排出率と有限容量でモデル化し、バースト間隔から背圧の蓄積と回復を予測してスケジュールを直すことで、専門並列で最大1.62倍、テンソル並列で最大1.75倍、系列並列で最大1.43倍の高速化を実測した。

- **2026-07 · [WIDE: Boosting Adaptive LLM Inference via Token-level Dynamic Width Pruning](2026-2607.28418-wide-boosting-adaptive-llm-inference-via-token-level-dynamic-width-pruni.md)**  
  実装：[✓](https://github.com/EIT-NLP/LLM-Pruning/tree/main/WIDE) ・ リポジトリ内被引用：0  
  トークンごとに注意ヘッド群とFFNチャネル群の実行可否をルータが決め、マスク並べ替えで不規則な選択をタイル単位の規則性へ変換してブロックごと飛ばす動的幅枝刈りで、削減率50パーセントでも品質を保ちながらプリフィル1.68倍の高速化を得た。

- **2026-07 · [VTC: DNN Compilation with Virtual Tensors for Data Movement Elimination](2026-2604.09558-vtc-dnn-compilation-with-virtual-tensors-for-data-movement-elimination.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中間テンソルを実データでなく添字の対応関係として保持する仮想テンソルで全種類のデータ移動を消すコンパイラにより、既存系の最良比で最大一・九三倍、平均一・二八倍の高速化と最大六十パーセントのメモリ削減を得たと報告した。

- **2026-07 · [Unified Static-Dynamic Pruning for Efficient LLM Inference](2026-2607.21985-unified-static-dynamic-pruning-for-efficient-llm-inference.md)**  
  実装：[✓](https://github.com/AIDASLab/SPDP) ・ リポジトリ内被引用：0  
  静的枝刈りと動的枝刈りを一つのタイル化ビットマップ形式と段階別カーネルで統合し、同じパープレキシティで最大25パーセント高い疎率と静的専用基盤比で最大2.51倍の高速化を実現する疎推論基盤。

- **2026-07 · [TileSight: A First-Principles Tile-Centric Analytical GPU Performance Model from Cores to Clusters](2026-2607.22432-tilesight-a-first-principles-tile-centric-analytical-gpu-performance-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  タイルを解析単位にして資源ベクトル、依存スケジューリング、再利用距離によるキャッシュ推定、通信段階費用を一つの第一原理モデルでつなぎ、単一カーネルから32GPUのvLLMサービングまで二桁前半の誤差で遅延を予測するGPU性能モデル。

- **2026-07 · [SCVQ: Sparse-Compensated Vector Quantization for Large Language Models](2026-47d0d3b8c049-scvq-sparse-compensated-vector-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  顕著さ重み付きK平均と対称性制約でコードブックを縮め、外れ値と顕著な重みと残差を一つのスパース行列で補償するベクトル量子化SCVQを提案し、LLaMA-2-7Bの2ビットでパープレキシティ5.87とA100上でFP16比2.3倍のデコード処理量を達成した。

- **2026-07 · [Rethinking Small VLM Quantization: From Component-Wise Analysis to Hardware-Aware Edge Deployment](2026-2607.08029-rethinking-small-vlm-quantization-from-component-wise-analysis-to-hardwa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型視覚言語モデルの量子化を視覚エンコーダ・プロジェクタ・言語基盤へ分けてJetson 2機で測り、感度は規模でなくMoEか密かで決まること、SigLIPのINT8遅延異常、INT4のVRAM減と速度悪化の交換を実証した配置指針の研究。

- **2026-07 · [PolyQ: Codesigning End-to-End Quantization Framework for Scalable Edge CPU LLM Inference](2026-2607.14618-polyq-codesigning-end-to-end-quantization-framework-for-scalable-edge-cp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  平均ビット予算に合わせてチャネルごとにビット幅を配り、並べ替えをコンパイル時に統合して実行時の配置費用を消すことで、小数ビット単位の量子化をCPU上で実用的に動かす量子化とコンパイラの共同設計の研究。

- **2026-07 · [Kernelized Linear Attention: Breaking the Capacity Wall with Symmetric Cones](2026-2607.17419-kernelized-linear-attention-breaking-the-capacity-wall-with-symmetric-co.md)**  
  実装：[✓](https://github.com/ayghri/KATA) ・ リポジトリ内被引用：0  
  論文はこの「容量の壁」を単なる実装問題ではなく、特徴空間内で互いに区別可能なキー方向を何個置けるかという球面充填問題として扱う。KATA（Kernelized Linear 注意機構 活性値）は、注意重みの非負性を保証する対称錐の特徴写像を設計軸に置く。

- **2026-07 · [Elastic Gang: Per-Token Membership Change for a Hard-Barriered LLM Inference Gang Co-Scheduled with OS Processes](2026-2607.04668-elastic-gang-per-token-membership-change-for-a-hard-barriered-llm-infere.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  バリア同期する推論ギャングの参加コアをトークンごとに確認応答で入れ替えられるようにし、推論出力をビット単位で保ったまま、遊んでいるコアを一般処理へ自動で貸し借りするカーネル内スケジューリングの研究。

- **2026-07 · [Decomposing Runtime, Kernel, and Quantization Speedups via a Matched FP16 Intermediate: A Hardware-Conditioned Case Study on Four NVIDIA RTX A5000 GPUs](2026-2607.11368-decomposing-runtime-kernel-and-quantization-speedups-via-a-matched-fp16-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FP16中間構成を挟んで高速化を実行系1.90倍と核・量子化1.36倍へ分け、広いバッチでは実行系が対数で約3分の2を占めること、4枚分割は約1.5倍に留まり不足の約8割が調整作業であることをA5000の4枚構成で示した。

- **2026-07 · [CTA-Pipelining: A Latency-Oriented Spatial Scaling Method for Multi-GPU Systems](2026-2607.07862-cta-pipelining-a-latency-oriented-spatial-scaling-method-for-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  協調スレッド配列（Cooperative Thread Array、以下CTA）ごとの依存関係を追跡し、GPU間の共有メモリ空間に配置した待ち行列で後段CTAを起動する方式がCTA-Pipeliningである。

- **2026-07 · [Cross-Layer Error Compensation and Finite-Sample Feature-Statistics Matching for Extreme Low-Bit Quantization of Large Language Models](2026-2607.14630-cross-layer-error-compensation-and-finite-sample-feature-statistics-matc.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全層の符号を同時に動かして累積誤差を後の層で打ち消す補償と、特徴統計を相対正規化で合わせる正則化を組み合わせ、1.5Bモデルの1.125ビット2値化で困惑度比を層局所再構成の約1400倍から9.56倍まで下げた。

- **2026-07 · [BrownoutMoE: Structure-Aware Expert Grouping for Efficient and Accurate LLM Web-based Services](2026-2607.04164-brownoutmoe-structure-aware-expert-grouping-for-efficient-and-accurate-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BrownoutMoEは、混合専門家モデル（Mixture of エキスパート、MoE）の推論配信において、低頻度の専門家をまとめて計算量とメモリ転送を減らす際の精度低下を抑える方式である。

- **2026-06 · [TileMaxSim: Roofline Regimes and Compression Limits for Fused GPU MaxSim Scoring](2026-2606.26439-tilemaxsim-roofline-regimes-and-compression-limits-for-fused-gpu-maxsim-.md)**  
  実装：[✓](https://github.com/ashutoshuiuc/tilemaxsim) ・ リポジトリ内被引用：0  
  融合した最大類似度スコア計算が帯域律速から計算律速へ切り替わる境界を閉形式と実測で示し、転送量を15.9倍減らす積量子化の融合が従属的な表引き65億回のために3.0倍遅くなることを明らかにした分析研究。

- **2026-06 · [TileFuse: A Fused Mixed-Precision Kernel Library for Efficient Quantized LLM Inference on AMD NPUs](2026-2606.11357-tilefuse-a-fused-mixed-precision-kernel-library-for-efficient-quantized-.md)**  
  実装：[✓](https://github.com/glassescrab/mlir-aie/tree/feature/update-mix-mm-int4-verification) ・ リポジトリ内被引用：0  
  AMD XDNA2 NPU向けに、逆量子化を融合した混合精度カーネルとメタデータ同梱の事前タイリングと全アレイGEMVを共設計し、AWQ形式をそのまま動かせるようにしたTileFuseの研究。

- **2026-06 · [Spectral-LSH: Sub-Quadratic Prompt Compression via Krylov-Projected Locality-Sensitive Hashing](2026-2607.19368-spectral-lsh-sub-quadratic-prompt-compression-via-krylov-projected-local.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意カーネルの固有空間で似たトークンをハッシュによりまとめ、プロンプトをモデル投入前に圧縮する訓練不要の方式。高圧縮で連続平均より品質を保つが、遅延では常に見劣りするため、圧縮率で経路を切り替える適応型が実用形になる。

- **2026-06 · [P-Cast Precision in FP8 Attention: Sink-Induced Collapse and the Optimality of S=2^8](2026-2606.06521-p-cast-precision-in-fp8-attention-sink-induced-collapse-and-the-optimali.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  アテンションシンク下でFP8変換により確率値がゼロへ落ちる崩壊を閉形式で定量化し、逆方向走査とスケール256のどちらでも解消でき、256が三条件を満たす最適な静的スケールであることを示す分析。

- **2026-06 · [Joint Structural Pruning and Mixed-Precision Quantization for LLM Compression](2026-2606.07819-joint-structural-pruning-and-mixed-precision-quantization-for-llm-compre.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合精度量子化と構造的枝刈りの二値マスクを、エンドツーエンド損失で学習するハイパーネットワークで同時最適化する圧縮手法。超低ビットで先行手法を上回り、実測でもプリフィル高速化とメモリ削減を示す。

- **2026-06 · [FuseFSS: Efficient Secure LLM Inference with Function Secret Sharing](2026-2606.09551-fusefss-efficient-secure-llm-inference-with-function-secret-sharing.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  2サーバ秘匿推論の非線形演算を演算子ごとの手作りプロトコルから、区間と多項式片と述語の仕様を2回の関数秘密分散評価へ落とす単一コンパイラへ置き換え、精度を保って1.24から1.50倍高速化する研究。

- **2026-06 · [Demystifying Numerical Instability in LLM Inference: Achieving Reproducible Inference for Mission-Critical Tasks with HEAL](2026-2606.21023-demystifying-numerical-instability-in-llm-inference-achieving-reproducib.md)**  
  実装：[✓](https://github.com/ucla-systems/HEAL) ・ リポジトリ内被引用：0  
  異なる装置で答えが変わる原因をカーネル境界の切り捨てと特定し、クエリ・キー・バリューの整数16ビット保持と行列積の残差補償で誤差を反転閾値の下へ抑え、32ビット並みの再現性を16ビットのメモリ量で得た方式。

- **2026-06 · [APEX4: Efficient Pure W4A4 LLM Inference via Intra-SM Compute Rebalancing](2026-2606.08761-apex4-efficient-pure-w4a4-llm-inference-via-intra-sm-compute-rebalancing.md)**  
  実装：[✓](https://github.com/APEX4-W4A4/APEX4-W4A4) ・ リポジトリ内被引用：0  
  ところが、量子化精度を守るため重み・活性化を細かいグループへ分けると、各グループのINT32行列積結果に対してFP32スケールを適用しなければならない。

- **2026-06 · [AgentCompile: An LLM-Guided Compiler for Direct CUDA Inference](2026-2606.07665-agentcompile-llm-guided-direct-cuda-inference.md)**  
  実装：[✓](https://github.com/veneno1213822/AgentCompile) ・ リポジトリ内被引用：0  
  大規模言語モデルによるCUDA生成をコンパイラ契約・数値検証・実測性能選択で囲い込み、合格した復号カーネルだけを採用して既存実装へ安全にフォールバックできる推論コンパイラ。

- **2026-06 · [Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices](2026-2607.08786-moderately-unstructured-sparse-gpu-inference.md)**  
  実装：[✓](https://github.com/moui0/cudac) ・ リポジトリ内被引用：0  
  約50%の非構造疎重みを2:4疎テンソルコア層・差分距離で再配置する補助層・微小残差層へ分解し、疎テンソルコアとCUDAコアを重ねて実行してSpInfer比最大1.64倍を達成する。

- **2026-06 · [A 35B Hybrid-Attention Mixture-of-Experts Model on a 6GB 2011 GPU: Hand-Written 4-bit CUDA Inference for Fermi](2026-2606.24031-a-35b-hybrid-attention-mixture-of-experts-model-on-a-6gb-2011-gpu-hand-w.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  2011年の6GB GPUと旧式ホストで35B級MoEを動かすため、GPUプリフィルとCPU整数デコードへ分割し、再帰状態の位置スナップショットでプリフィックス再利用まで復活させ、プリフィル34パーセント短縮とデコード約3倍を実測する実装研究。

- **2026-05 · [XFP: Quality-Targeted Adaptive Codebook Quantization with Sparse Outlier Separation for LLM Inference](2026-2605.14844-xfp-quality-targeted-adaptive-codebook-quantization-with-sparse-outlier-.md)**  
  実装：[✓](https://github.com/flash7777/vllm/tree/multiquant) ・ リポジトリ内被引用：0  
  XFPは、大規模言語モデルの重みを低ビット化する際に、最初からINT4やINT3などのビット幅を固定するのではなく、各層の重み再構成品質を満たす最小のビット幅を自動で選ぶ推論向け量子化方式である。後者を2ビットへ落としやすくすることで、モデルの全専門家を削除せず、2枚の96GBワークステーションGPUへ397B規模の重みを収める構成を探索する。

- **2026-05 · [Tile-Level Activation Overlap for Efficient LLM Inference](2026-2607.02521-tile-level-activation-overlap-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SwiGLUの中間テンソルのメモリ往復をタイル単位の融合で消し、計算と読み込みや保存を重ねる二つのカーネルで、H100上でPyTorch比最大2.47倍と高い数値精度を得る研究。

- **2026-05 · [SonicSampler: Unified Tile-Aware Kernels for LLM Sampling and Speculative Verification](2026-2607.20475-sonicsampler-unified-tile-aware-kernels-for-llm-sampling-and-speculative.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SonicSamplerは語彙を固定長タイルへ分割し、第1段階で要求別のロジット変換とタイル内top-k抽出を融合し、第2段階でタイル候補を統合して確率切り詰め・乱数抽出・投機的検証を行う。

- **2026-05 · [PopPy: Opportunistically Exploiting Parallelism in Python Compound AI Applications](2026-2605.18697-poppy-opportunistically-exploiting-parallelism-in-python-compound-ai-app.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  逐次Pythonで書かれた複合AIアプリケーションを機会的実行の核計算へコンパイルし、独立なモデル呼び出しを自動で並行化して逐次意味論を保ったまま最大6.4倍高速化するコンパイラと実行系。

- **2026-05 · [Parallax: Parameterized Local Linear Attention for Language Modeling](2026-2605.29157-parallax-parameterized-local-linear-attention-for-language-modeling.md)**  
  実装：[✓](https://github.com/Yifei-Zuo/Parallax) ・ リポジトリ内被引用：0  
  Parallaxは、通常のSoftmax注意の「入力クエリに近いキーへ重みを置いて値を平均する」という計算に、キーと値の局所的な相互共分散を使った補正を加える注意機構である。H200でのBF16復号カーネルの測定では、比較対象のFlashAttention 2/3の速い方に対し、測定したバッチ・文脈長の範囲で同等以上と著者らは報告する。

- **2026-05 · [Memory-Bound but Not Bandwidth-Limited: The Physical AI Inference Gap in Batch-1 LLM Decode](2026-2605.30571-memory-bound-but-not-bandwidth-limited-the-physical-ai-inference-gap-in-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  研究の中心は新しい注意演算を発明することではなく、既存の復号経路で、メモリ転送、CPUからのGPUカーネル起動、量子化カーネルの適合性を切り分ける測定設計にある。

- **2026-05 · [Litespark Inference For CPUs: Ultra-Fast SIMD Framework for Ternary (1.58-bit) Language Models](2026-2605.06485-litespark-inference-for-cpus-ultra-fast-simd-framework-for-ternary-1-58-.md)**  
  実装：[✓](https://github.com/Mindbeam-AI/Litespark-Inference) ・ リポジトリ内被引用：0  
  三値重みを8ビット整数のままSIMDドット積命令へ流し、乗算なしで線形層を計算するCPU推論フレームワーク。プラットフォーム別カーネルの自動振り分けで、PyTorch比18倍から97倍のスループットと約6倍のメモリ削減を実測した。

- **2026-05 · [KLineage: Recovering the Missing When of Kernel Optimization by Deoptimizing Experts](2026-2605.28213-klineage-recovering-the-missing-when-of-kernel-optimization-by-deoptimiz.md)**  
  実装：[✓](https://github.com/ict-agent/klineage) ・ リポジトリ内被引用：0  
  専門家カーネルを検証付きで脱最適化し、受理ステップの逆操作を前提条件付きスキルとして蓄えることで、言語モデルへ最適化の適用条件を教え、供給元比1.12倍のカーネルを全組で正しく生成する枠組み。

- **2026-05 · [Kaczmarz Linear Attention](2026-2605.08587-kaczmarz-linear-attention.md)**  
  実装：[✓](https://github.com/anonymous-kla-review/kla-anonymous) ・ リポジトリ内被引用：0  
  Kaczmarz Linear 注意機構（KLA）は、線形時間の再帰型注意で、過去の情報を有限サイズの状態行列に書き込む際の更新量を、オンライン回帰の最小化から導く研究である。32K文脈の単一バッチ復号の原著実測では3.54トークン/秒で、GDNの1.65トークン/秒に対し2.1倍だった。

- **2026-05 · [Improving the Efficiency of Language Agent Teams with Adaptive Task Graphs](2026-2605.06320-improving-the-efficiency-of-language-agent-teams-with-adaptive-task-grap.md)**  
  実装：[✓](https://github.com/emieczkowski/latte) ・ リポジトリ内被引用：0  
  複数の大規模言語モデル（LLM）を役割分担して実行するエージェントシステムでは、同じ作業の重複、ファイルの競合更新、長い通信、担当者の待機が発生しやすい。LATTEの成功試行集計は平均148,000トークン、3.5分、成功率約80%で、固定グラフ方式の297,000トークン、6.0分、58%より効率と成功率が高い。

- **2026-05 · [GPU Forecasters: Language Models as Selective Surrogates for Kernel Runtime Optimization](2026-2605.31464-gpu-forecasters-kernel-runtime-surrogates.md)**  
  実装：[✓](https://github.com/codezakh/gpu-forecasters) ・ リポジトリ内被引用：0  
  実GPU計測をLLMの相対速度予測で選択的に代替し、同じGPU計測予算で候補数を4倍へ広げて6課題中4課題で基準と同等以上の高速カーネルを発見する。

- **2026-05 · [Exact Linear Attention](2026-2605.18848-exact-linear-attention.md)**  
  実装：[✓](https://github.com/yauntyour/Exact-Linear-Attention) ・ リポジトリ内被引用：0  
  Exact Linear 注意機構（ELA）は、注意カーネルが有限次元の二つの特徴写像の内積として厳密に分解できるとき、注意行列全体を作らずに系列方向の累積統計だけで注意出力を計算する方式である。

- **2026-05 · [EntmaxKV: Support-Aware Decoding for Entmax Attention](2026-2605.21649-entmaxkv-support-aware-decoding-for-entmax-attention.md)**  
  実装：[✓](https://github.com/deep-spin/entmaxkv) ・ リポジトリ内被引用：0  
  疎なデコードは必要そうなトークンやページだけを読むが、softmaxは有限スコアを持つ全トークンに正の確率を割り当てるため、どれほど小さくても捨てた確率質量が残る。

- **2026-05 · [Eliminating Hidden Serialization in Multi-Node Megakernel Communication](2026-2605.00686-eliminating-hidden-serialization-in-multi-node-megakernel-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案システムPerseusは、(1)GPU側でデータ転送と通知を分離し、宛先群ごとに順序保証をまとめる分離通知（decoupled signaling）、(2)CPUプロキシが転送完了を待つ代わりに、NICのハードウェアfenceフラグで通知の順序を保証するNIC側順序制御（NIC-side ordering）を組み合わせる。

- **2026-05 · [DynaFlow: Transparent and Flexible Intra-Device Parallelism via Programmable Operator Scheduling](2026-2605.21603-dynaflow-transparent-and-flexible-intra-device-parallelism-via-programma.md)**  
  実装：[✓](https://github.com/uw-syfi/DynaFlow) ・ リポジトリ内被引用：0  
  複数の演算子を重畳する最適化自体は既知だが、実際のvLLMやSGLangへ組み込むにはモデル実行順序の大規模な変更が必要であり、入力長・バッチ量・GPU世代で最適な重畳方式も変わる。従来の配信・学習システム6種類へ代表的な装置内並列方式を導入し、元のシステム比で最大1.29倍の端から端までの処理量を実測した。

- **2026-05 · [Demystifying the Mixture of Experts Serving Tax](2026-b71f37ac28fc-demystifying-the-mixture-of-experts-serving-tax.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Mixture-of-Experts（MoE）が「1トークン当たりに実行する演算量を減らせる」という設計上の利点と、実際のGPUサービングで低遅延・高スループットを得られることの間にある差を調べるシステム特性分析研究である。

- **2026-05 · [Behavioral Consistency in Machine Learning](2026-2606.07581-behavioral-consistency-in-machine-learning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同一重みを実行カーネルで添字付けし、ロジット差から分布・報酬・勾配バイアスへの bound と、スライス別に許容ドリフトと対処を宣言するカーネル契約を提案し、vLLMとHugging Faceの9構成で検証した研究。

- **2026-04 · [Towards a Solution to the Management Scaling Paradox in Distributed LLM Inference](2026-f2a77ecc52ae-towards-a-solution-to-the-management-scaling-paradox-in-distributed-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型推論でKVキャッシュ管理のユーザ空間オーバーヘッドがヒット率とともに膨らむ逆説を定量化し、カーネル内のコンテンツアドレス型PGASで無調整にチャンクを引けるRMCによりTTFTを1.1〜1.3倍短縮する提案。

- **2026-04 · [SinkRouter: Sink-Aware Routing for Efficient Long-Context Decoding in Large Language and Multimodal Models](2026-2604.16883-sinkrouter-sink-aware-routing-for-efficient-long-context-decoding-in-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  先頭トークンに注意重みが集中する注意の沈み込み（注意機構 sink）を、重要な履歴情報を保持するための目印としてだけでなく、「現在の注意出力がほぼゼロとなり、残差流への更新が小さい」状態を示す手掛かりとして解釈する。原著はNVIDIA RTX PRO 6000で512Kトークン文脈の復号を最大2.03倍高速化したと報告する。

- **2026-04 · [Screening Is Enough](2026-2604.01178-screening-is-enough.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、通常のソフトマックス注意（softmax 注意機構）が各問い合わせについて全鍵の重みを合計1に正規化するため、「どの鍵も十分に関連しない」という状態を直接表現しにくい点に着目する。パラメータ規模に関する近似的な学習曲線からは、同等の検証損失に必要なパラメータが約30%少ないと推定する。

- **2026-04 · [Reducing Language Model Inference Latency using CPU-Assisted Serving](2026-0ed1914daa9a-reducing-language-model-inference-latency-using-cpu-assisted-serving.md)**  
  実装：[✓](https://github.com/tgasla/cpu-assisted-lm-serving/) ・ リポジトリ内被引用：0  
  GPU仮想化のAPIリモーティングで遊休CPUノードを推論サーバ化し、実測遅延に基づく動的振り分けと組み合わせて、CPU律速な小規模言語モデルの推論遅延を最大98パーセント削減するクラスタ側サービング方式。

- **2026-04 · [Ragged Paged Attention: A High-Performance and Flexible LLM Inference Kernel for TPU](2026-2604.15464-ragged-paged-attention-a-high-performance-and-flexible-llm-inference-ker.md)**  
  実装：[✓](https://github.com/vllm-project/tpu-inference/blob/main/tpu_inference/kernels/ragged_paged_attention/v3/kernel.py) ・ リポジトリ内被引用：0  
  細粒度タイル化、KV更新と注意計算の融合パイプライン、負荷分布ごとの専用コンパイルでTPUの不揃い実行を扱う注意カーネルで、帯域利用率86パーセントと演算利用率73パーセントを実測した。

- **2026-04 · [LP-GEMM: Integrating Layout Propagation into GEMM Operations](2026-2604.04599-lp-gemm-integrating-layout-propagation-into-gemm-operations.md)**  
  実装：[✓](https://github.com/czariv/simple_attention) ・ リポジトリ内被引用：0  
  連続する行列積が毎回入出力を詰め替える無駄を除くため、GEMMを初期・中間・終端の3種類に分割し、内部の詰め込み配置を次の行列積へ伝播するLP-GEMMを提案。

- **2026-04 · [Layer-wise MoE Routing Locality under Shared-Prefix Code Generation: Token-Identity Decomposition and Compile-Equivalent Fork Redundancy](2026-2604.17182-layer-wise-moe-routing-locality-under-shared-prefix-code-generation-toke.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有プリフィックスから分岐した851本のコード生成でMoEルーティングの重なりを層とトークン同一性に分解して測り、中間層で文脈依存が盛り上がる交差と、コンパイル等価な冗長候補が生成の大半を占めることを示す分析研究。

- **2026-04 · [Hybrid JIT-CUDA Graph Optimization for Low-Latency Large Language Model Inference](2026-2604.23467-hybrid-jit-cuda-graph-low-latency-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  静的Transformer演算をCUDA Graph再生、動的制御を実行時コンパイルへ分け、短系列・バッチ1推論の起動オーバーヘッドと尾部遅延を削減する。

- **2026-04 · [From LLM to Silicon: RL-Driven ASIC Architecture Exploration for On-Device AI Inference](2026-2604.07526-from-llm-to-silicon-rl-driven-asic-architecture-exploration-for-on-devic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ASICの設計空間全体を強化学習で探索するコンパイラ。メッシュ形状、コア別パラメータ、メモリ配分、演算子分割を単一の決定過程でSACが最適化し、ノードごとに人手調整なしでPPAの良い構成を導く。数値は解析モデルによる推定。

- **2026-04 · [FluidGPU: Fine-Grained Kernel Disaggregation for Large Model Inference on Heterogeneous GPUs](2026-2604.10180-fluidgpu-fine-grained-kernel-disaggregation-for-large-model-inference-on.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、性能と価格の異なるGPUが混在するクラスタで、モデルのフェーズやTransformerブロックより細かいCUDAカーネル単位に処理を配置する推論実行基盤を提案する。

- **2026-04 · [Fast Cross-Operator Optimization of Attention Dataflow](2026-2604.03446-fast-cross-operator-optimization-of-attention-dataflow.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中間の注意得点行列を外部DRAMへ書き戻すと大量のメモリ転送が生じるため、複数演算を融合し、オンチップの小さなバッファで部分結果を保持することが重要になる。MMEE（Matrix Multiplication Encoded Enumeration、行列積符号化列挙）は、この探索空間を解析式と行列演算で高速に評価する手法である。

- **2026-04 · [FASQ: Flexible Accelerated Subspace Quantization for Calibration-Free LLM Compression](2026-2605.04084-fasq-flexible-accelerated-subspace-quantization-for-calibration-free-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み自身へのクラスタリングによる積量子化で較正なしの連続圧縮を実現し、参照表なし直接計算のデコードカーネルで圧縮法として唯一FP16超えのデコード速度を達成した研究。

- **2026-04 · [FairyFuse: Multiplication-Free LLM Inference on CPUs via Fused Ternary Kernels](2026-2604.20913-fairyfuse-multiplication-free-llm-inference-on-cpus-via-fused-ternary-ke.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存の量子化ランタイムでは、低ビット重みを格納しても実行時に浮動小数点へ復元して積和演算を行う場合がある。原著のIntel Xeon 8558P・48スレッド・単一NUMAソケットでの7B級復号では32.43 トークン/sを報告し、同じCPUのllama.cpp Q4KMの26.15 トークン/sより1.24倍高速だった。

- **2026-04 · [Evaluating CUDA Tile for AI Workloads on Hopper and Blackwell GPUs](2026-2604.23466-evaluating-cuda-tile-for-ai-workloads-on-hopper-and-blackwell-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、NVIDIAのタイル単位GPUプログラミング基盤CUDA Tile（CuTile）を採用すべき条件を、性能と開発工数の両面から実測した比較研究である。CuTileは行列積や注意計算をタイル演算として記述し、スレッド束、共有メモリ配置、レジスタ割当の一部をコンパイラへ任せる。主要結果は二面的である。

- **2026-04 · [Efficient Matrix Implementation for Rotary Position Embedding](2026-2604.09742-efficient-matrix-implementation-for-rotary-position-embedding.md)**  
  実装：[✓](https://gitcode.com/cann/ops-transformer) ・ リポジトリ内被引用：0  
  回転位置埋め込みの分割と結合を一つの構造化行列変換へ書き換える数学的に等価な再定式化で、多次元版まで統一し演算子単体で最大約3.7倍、モデル全体でも数パーセントの高速化と大幅な実装簡素化を得る方式。

- **2026-04 · [Continuous Semantic Caching for Low-Cost LLM Serving](2026-2604.20021-continuous-semantic-caching-for-low-cost-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キャッシュの容量は有限であり、どの応答を保存すれば推論費用と不一致費用の合計を小さくできるかが問題になる。提案の中心は、近い問い合わせを代表点へまとめるε-netによる離散化と、観測された一部の推論費用から周辺の費用を推定するカーネルリッジ回帰（カーネル ridge regression; KRR）である。

- **2026-04 · [An Empirical Study of LLM Serving in Confidential GPUs](2026-6489368bb8a1-an-empirical-study-of-llm-serving-in-confidential-gpus.md)**  
  実装：[✓](https://github.com/bearhw/Confidential-GPU-LLM-Serving-Performance-Profiling) ・ リポジトリ内被引用：0  
  機密GPU上でvLLMとSGLangを2種の機密仮想マシンで実測し、暗号化の上乗せがフレームワークのメモリ管理とスケジューリングで大きく変わり、オンラインでは最大で約4倍へ膨らみ、通常向け最適化が逆効果になり得ることを示した実証研究。

- **2026-04 · [Active Imitation Learning for Thermal- and Kernel-Aware LFM Inference on 3D S-NUCA Many-Cores](2026-2604.11948-active-imitation-learning-for-thermal-and-kernel-aware-lfm-inference-on-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案方式AILFM（Active Imitation Learning for LFMs）は、コアごとの命令実行率、最終段キャッシュのミス率、平均キャッシュ距離、電力予算、温度を観測し、どのカーネルをどのコアに割り当てると温度上限を守りながら実行時間を短縮できるかを判断する。

- **2026-03 · [Sparser, Faster, Lighter Transformer Language Models](2026-2603.23198-sparser-faster-lighter-transformer-language-models.md)**  
  実装：[✓](https://github.com/SakanaAI/sparser-faster-llms) ・ リポジトリ内被引用：0  
  フィードフォワード層の活性スパース性を、タイル単位の疎形式と融合カーネルで実際の速度・省メモリ・省エネルギーへ変える研究。正則化だけで99パーセント超のスパース性をほぼ無劣化で得られることも示す。

- **2026-03 · [RSR-core: A High-Performance Engine for Low-Bit Matrix-Vector Multiplication](2026-2603.27462-rsr-core-a-high-performance-engine-for-low-bit-matrix-vector-multiplicat.md)**  
  実装：[✓](https://github.com/UIC-InDeXLab/RSR-core) ・ リポジトリ内被引用：0  
  RSR-coreは、二値または三値の重み行列に繰り返し現れる列パターンをまとめる冗長セグメント削減（Redundant Segment Reduction; RSR）アルゴリズムを、CPUおよびGPUで直接実行できる形に実装した推論エンジンである。

- **2026-03 · [Model2Kernel: Model-Aware Symbolic Execution For Safe CUDA Kernels](2026-2603.24595-model2kernel-safe-cuda-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル側からCUDA呼出し条件を抽出するHFProbeと、動的テンソル・全CUDAスレッドを記号化するcuKLEEを組み合わせ、LLM推論カーネルの未知メモリバグ353件を9誤検出で検出した。

- **2026-03 · [Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts](2026-2603.07169-cudamaster-multi-scenario-kernel-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  50演算×FP32/BF16のMSKernelBenchと、律速別に選別したNsight Compute情報を計画・実装・コンパイル・デバッグの4担当へ渡すCUDAMasterで、多領域CUDA最適化を自動化し、o4-miniで正当性100%・基準超え94%を達成する。

- **2026-03 · [From Skew to Symmetry: Node-Interconnect Multi-Path Balancing with Execution-time Planning for Modern GPU Clusters](2026-2604.00317-from-skew-to-symmetry-node-interconnect-multi-path-balancing-with-execut.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  偏った通信で一部のリンクだけが飽和する問題に対し、リンク負荷を見て最大混雑を最小化するようメッセージを複数パスへ実行時に再配分するランタイムNIMBLEを提案し、偏ったオールツーオールでNCCL比最大5.2倍、MoEのエンドツーエンドで最大1.35倍を示す。

- **2026-03 · [Compiling Code LLMs into Lightweight Executables](2026-2603.29813-compiling-code-llms-into-lightweight-executables.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック単位のコードブック量子化と、行列ベクトル積をBLASへ置き換えるLLVMパスを組み合わせ、7B級コードモデルを一般的なノートPCで最大10.5倍速く、6.4倍小さいメモリで動かす枠組み。

- **2026-02 · [Xami: Expert-Aware Adaptive Compression for Mixture-of-Experts on Sparse Tensor Cores](2026-ed5f0e8fb57d-xami-expert-aware-adaptive-compression-for-mixture-of-experts-on-sparse-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  専門家の活性化頻度の偏りを使い、よく使う専門家は軽く、あまり使わない専門家は強く圧縮する。冷たい専門家は詰めて保存し実行時にハードウェア形式へ展開することで、疎テンソルコアの実行モデルを変えずにメモリを最大2.4倍圧縮する仕組み。

- **2026-02 · [The Quantization Trap: Breaking Linear Scaling Laws in Multi-Hop Reasoning](2026-2602.13595-the-quantization-trap-breaking-linear-scaling-laws-in-multi-hop-reasonin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  多段推論では逆量子化のキャスティング費用が段数だけ積み上がり、8ビット化がかえってエネルギーを4倍に増やす量子化の罠を、理論分解と0.6Bから72B・6種GPUの実測で示した分析。

- **2026-02 · [RedFuser: An Automatic Operator Fusion Framework for Cascaded Reductions on AI Accelerators](2026-2603.10026-redfuser-an-automatic-operator-fusion-framework-for-cascaded-reductions-.md)**  
  実装：[✓](https://github.com/alibaba/redfuser) ・ リポジトリ内被引用：0  
  連鎖した集約演算を集約木の連鎖として形式化し、融合条件と増分計算を自動で導いて単一カーネルを生成することで、注意や量子化付き行列積で既存コンパイラの2倍から5倍、手書きカーネル同等の性能を得る自動融合の枠組み。

- **2026-02 · [RaBiT: Residual-Aware Binarization Training for Accurate and Efficient LLMs](2026-2602.05367-rabit-residual-aware-binarization-training-for-accurate-and-efficient-ll.md)**  
  実装：[✓](https://github.com/SamsungLabs/RaBiT) ・ リポジトリ内被引用：0  
  RaBiT（Residual-Aware Binarization 学習）は、複数の二値行列の和によって全精度の重みを近似する残差二値化（residual binarization）を、量子化認識学習（量子化-aware 学習; QAT）で安定させる方式である。

- **2026-02 · [OptiML: An End-to-End Framework for Program Synthesis and CUDA Kernel Optimization](2026-2602.12305-optiml-an-end-to-end-framework-for-program-synthesis-and-cuda-kernel-opt.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OptiMLは、大規模言語モデルによるCUDAカーネルの初期生成と、その後の正しさを保つ性能改善を単一の開発経路へまとめる方式である。

- **2026-02 · [FlashMem: Supporting Modern DNN Workloads on Mobile with GPU Memory Hierarchy Optimizations](2026-2602.15379-flashmem-supporting-modern-dnn-workloads-on-mobile-with-gpu-memory-hiera.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モバイルGPUで全重み事前読み込みをやめ、負荷容量を考慮したオフライン計画で重みの断片を計算と重ねてテクスチャメモリへ流すことで、11モデルでメモリ2.0〜8.4倍削減と初期化込み1.7〜75.0倍高速化を実現する実行枠組み。

- **2026-01 · [Syncopate: Efficient Multi-GPU AI Kernels via Automatic Chunk-Centric Compute-Communication Overlap](2026-2601.20595-syncopate-efficient-multi-gpu-ai-kernels-via-automatic-chunk-centric-com.md)**  
  実装：[✓](https://github.com/tie-pilot-qxw/syncopate) ・ リポジトリ内被引用：0  
  通信と計算を異なるCUDAストリームで同時実行する従来方式は、しばしばカーネル全体を単位として重ねるため、入力データの一部が先に到着しても、その部分を処理する計算を開始できない。全体平均1.3倍、最大4.7倍の高速化を報告し、特定の高度に最適化された手書き行列積と比較した性能は4GPU時で平均99.8%、8GPU時で104%だった。

- **2026-01 · [SD-E2: Semantic Exploration for Reasoning Under Token Budgets](2026-2601.17982-sd-e2-semantic-exploration-for-reasoning-under-token-budgets.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型言語モデルに複雑な問題を解かせる際、複数の解法を試すことは有効だが、生成トークン数には限りがある。結果・形式・長さを用いるGRPO-CFLの76.80%、意味を考慮しない探索・活用方式GRPO-CFEEの80.52%も上回る。

- **2026-01 · [RadixMLP -- Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)**  
  実装：[✓](https://github.com/michaelfeil/radix-mlp) ・ リポジトリ内被引用：0  
  RadixMLPは、同一バッチに入った複数の系列が長い接頭辞を共有している場合、共有部分の多層パーセプトロン（MLP）、層正規化（LayerNorm）、線形射影、埋め込みなどを何度も実行する無駄を削減する方式である。

- **2026-01 · [Magellan: Autonomous Discovery of Novel Compiler Optimization Heuristics with AlphaEvolve](2026-2601.21096-magellan-autonomous-discovery-of-novel-compiler-optimization-heuristics-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MagellanはLLMのコード生成エージェント、進化的探索、外部のハイパーパラメータ調整器を閉ループで結び、LLVMやXLAのコンパイラ最適化パスに組み込めるC++の判断規則を自動発見する。生成したポリシーを実際のコンパイラへ挿入して再ビルドし、アプリケーションの最終バイナリサイズや実行時間を報酬にして改善する。

- **2026-01 · [LatencyPrism: Online Non-intrusive Latency Sculpting for SLO-Guaranteed LLM Inference](2026-2601.09258-latencyprism-online-non-intrusive-latency-sculpting-for-slo-guaranteed-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LatencyPrismは、本番の大規模言語モデル（LLM）推論で、ユーザーの体感品質に影響する遅延の一時的な増大を、サービスを止めずに検知し、原因の切り分けに必要な実行情報を取得するシステムである。

- **2026-01 · [A Survey of Quantization in LLM: Unlocking Potential Hardware Efficiency](2026-740889701e27-a-survey-of-quantization-in-llm-unlocking-potential-hardware-efficiency.md)**  
  実装：[✓](https://github.com/Qcompiler/llm_bench) ・ リポジトリ内被引用：0  
  LLM量子化を事前学習・微調整・推論の三段階と対象部位で体系化し、数学的基礎、外れ値対策、KVキャッシュ量子化、カーネル生成までを整理したサーベイで、混合精度が低ビットでも精度を保つ鍵だと示す。

- **2025-12 · [Memory-Efficient Acceleration of Block Low-Rank Foundation Models on Resource Constrained GPUs](2025-2512.20861-memory-efficient-acceleration-of-block-low-rank-foundation-models-on-res.md)**  
  実装：[✓](https://github.com/pabillam/mem-efficient-blr) ・ リポジトリ内被引用：0  
  ブロック低ランク圧縮は多トークン推論では中間テンソルの往復でメモリ律速になることをルーフライン分析で示し、部分融合とメモリ配置の最適化を行ったTritonカーネルで中間の書き戻しを消すことで、圧縮の理論上の節約を実測の高速化へ戻す研究。

- **2025-12 · [Magneton: Optimizing Energy Efficiency of ML Systems via Differential Energy Debugging](2025-2512.08365-magneton-optimizing-energy-efficiency-of-ml-systems-via-differential-ene.md)**  
  実装：[✓](https://github.com/uw-syfi/Magneton) ・ リポジトリ内被引用：0  
  同等機能の別実装と演算子単位でエネルギーを比べ、無駄な実装とその原因である設定や呼出し経路まで自動で特定する差分エネルギーデバッグ。9システムで既知15件を診断し未知8件を発見。

- **2025-12 · [GatedFWA: Linear Flash Windowed Attention with Gated Associative Memory](2025-2512.07782-gatedfwa-linear-flash-windowed-attention-with-gated-associative-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GatedFWAは、自己回帰型言語モデルのスライディング窓注意（sliding-window 注意機構; SWA）に、トークン位置と注意ヘッドに依存する記憶ゲートを組み込む方式である。

- **2025-12 · [Flash Multi-Head Feed-Forward Network](2025-2512.06989-flash-multi-head-feed-forward-network.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FFNの複数ヘッド化を、比率を保つ並列サブネットワークとSRAM上でオンライン計算する融合カーネルで実用化し、SwiGLUよりメモリを3から5倍削減し推論を最大1.08倍速くしながら品質も改善した研究。

### 2年前（2024-12〜2025-11）

- **2025-01 · [FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving](2025-2501.01005-flashinfer-attention-engine-serving.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer) ・ リポジトリ内被引用：238  
  多様なKV配置と注意派生形をブロック疎形式と実行時コンパイルで統一し、可変系列長を固定CTAへ動的に負荷均衡しながらCUDAグラフ互換性も保つ、LLMサービング向け高性能注意エンジン。

- **2025-03 · [POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference](2025-pod-attention.md)**  
  実装：[✓](https://github.com/microsoft/vattention/tree/main/pod_attn) ・ リポジトリ内被引用：61  
  プリフィルとデコードの注意を同一SMで並行実行するSM認識型GPUカーネルにより、注意計算を平均28%、サービング処理量を最大22%改善する。

- **2024-12 · [Flex Attention: A Programming Model for Generating Optimized Attention Kernels](2024-2412.05496-flexattention-a-programming-model-for-generating-optimized-attention-kernels.md)**  
  実装：[✓](https://github.com/pytorch/pytorch) ・ リポジトリ内被引用：53  
  高速な融合注意カーネルを「注意変種ごとに手書きする」方式から、利用者が意味だけを書きコンパイラが高速カーネルへ落とす方式へ変える。

- **2025-10 · [KTransformers: Unleashing the Full Potential of CPU/GPU Hybrid Inference for MoE Models](2025-b4e11ada8105-ktransformers-unleashing-the-full-potential-of-cpu-gpu-hybrid-inference-.md)**  
  実装：[✓](https://github.com/kvcache-ai/ktransformers) ・ リポジトリ内被引用：29  
  大規模な混合専門家モデルの多数の専門家重みをCPUメモリに常駐させ、注意機構などをGPUで処理する異種混成推論基盤。CPUの行列演算命令を算術強度に応じて使い分け、非同期の実行制御と専門家計算の遅延反映によってCPU・GPUの相互待ちを減らす。低同時実行の巨大モデルを主対象とし、評価した環境は二基の高性能XeonとA100またはRTX 4080である。

- **2025-04 · [TileLang: A Composable Tiled Programming Model for AI Systems](2025-2504.17577-tilelang-a-composable-tiled-programming-model-for-ai-systems.md)**  
  実装：[✓](https://github.com/tile-ai/tilelang) ・ リポジトリ内被引用：27  
  GPUカーネルの「何を計算するか」をタイル単位のデータ流として書き、「どのスレッドがどの配置で、どの命令を使い、転送と計算をどう重ねるか」を別のスケジュール層へ分離する。高水準な記述を保ちながら、FlashAttention-3級の複雑なパイプラインまで表現・自動推論できることを狙う。

- **2025-04 · [Triton-distributed: Programming Overlapping Kernels on Distributed AI Systems with the Triton Compiler](2025-2504.19442-triton-distributed.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/Triton-distributed) ・ リポジトリ内被引用：20  
  OpenSHMEM通信をTritonへ統合し、計算・通信・メモリアクセスをPythonから細粒度に重ね合わせ、8〜64 GPUで分散カーネルを高速化するコンパイラ拡張。

- **2025-03 · [Medusa: Accelerating Serverless LLM Inference with Materialization](2025-8c4404f09758-medusa-accelerating-serverless-llm-inference-with-materialization.md)**  
  実装：[✓](https://github.com/thustorage/Medusa) ・ リポジトリ内被引用：20  
  Medusaは、大規模言語モデル（large language モデル; LLM）を必要なときだけ起動するサーバーレス推論において、モデル重みの読み込み以外にも無視できない起動費用があることに着目したシステム論文である。

- **2025-03 · [TileLink: Generating Efficient Compute-Communication Overlapping Kernels using Tile-Centric Primitives](2025-2503.20313-tilelink-generating-efficient-compute-communication-overlapping-kernels-using-tile-centric-primitives.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/Triton-distributed) ・ リポジトリ内被引用：19  
  タイル中心プリミティブから計算・通信融合カーネルを生成し、8×H800で非重畳比1.17〜20.76倍、8モデルのエンドツーエンドでPyTorch比平均1.32倍を達成する。

- **2025-06 · [FlashMoE: Fast Distributed MoE in a Single Kernel](2025-2506.04667-flashmoe-fast-distributed-moe-in-a-single-kernel.md)**  
  実装：[✓](https://github.com/osayamenja/FlashMoE) ・ リポジトリ内被引用：17  
  分散MoE全体を単一の常駐GPUカーネルへ融合し、装置起点通信とタイル単位スケジューリングでCPU起動・同期待ちを除き、8基H100で最大6.4倍の遅延改善と5.7倍のスループットを示す。

- **2025-09 · [Towards Robust Agentic CUDA Kernel Benchmarking, Verification, and Optimization](2025-2509.14279-towards-robust-agentic-cuda-kernel-benchmarking-verification-and-optimization.md)**  
  実装：[✓](https://github.com/SakanaAI/robust-kbench) ・ リポジトリ内被引用：13  
  固定入力などを悪用した「高速だが一般化しないCUDA」を弾くrobust-kbenchと、翻訳・LLM検証・進化的最適化を統合したエージェントを提案し、KernelBenchの見かけの平均3.13倍高速化が堅牢化後1.49倍へ下がることを示す。

- **2025-05 · [TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference](2025-2505.11329-tokenweave-efficient-compute-communication-overlap-for-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/tokenweave) ・ リポジトリ内被引用：13  
  GPU実行波を考慮した2分割とAllReduce–RMSNorm融合により、小さなテンソル並列バッチでも通信と計算を重ね、遅延とスループットを改善する。

- **2025-04 · [70% Size, 100% Accuracy: Lossless LLM Compression for Efficient GPU Inference via Dynamic-Length Float (DFloat11)](2025-2504.11651-70-size-100-accuracy-lossless-llm-compression-for-efficient-gpu-inferenc.md)**  
  実装：[✓](https://github.com/LeanModels/DFloat11) ・ リポジトリ内被引用：12  
  DFloat11は、大規模言語モデルのBFloat16重みを数値を変えずに圧縮し、推論時にGPU上で必要な部分だけ復号する方式である。Llama 3.1 405Bの重み容量は約811.71GBから551.22GBへ減り、8台の80GB GPUを持つ単一ノードで可逆推論できる。

- **2025-09 · [Astra: A Multi-Agent System for GPU Kernel Performance Optimization](2025-2509.07506-astra-a-multi-agent-system-for-gpu-kernel-performance-optimization.md)**  
  実装：[✓](https://github.com/Anjiang-Wei/Astra) ・ リポジトリ内被引用：11  
  高水準PyTorchからCUDAを一から生成するのではなく、SGLangに既に存在する正しいCUDAカーネルを出発点にし、試験・プロファイル・計画・実装を別々の大規模言語モデル（Large Language モデル; LLM）エージェントへ分担する。

- **2025-04 · [Efficient and Adaptable Overlapping for Computation and Communication via Signaling and Reordering](2025-2504.19519-efficient-and-adaptable-overlapping-for-computation-and-communication-vi.md)**  
  実装：[✓](https://github.com/infinigence/FlashOverlap) ・ リポジトリ内被引用：10  
  FlashOverlapは、複数GPUで大規模言語モデルを推論・学習するとき、行列積（general matrix multiplication、GEMM）と、それに依存するGPU間集団通信を重ねて実行する仕組みである。テンソル並列では、各GPUが計算した部分結果を全GPUで合計するAllReduceや、部分ごとに配布するReduceScatterを行う。

- **2025-06 · [LittleBit: Ultra Low-Bit Quantization via Latent Factorization](2025-2506.13771-littlebit-ultra-low-bit-quantization-via-latent-factorization.md)**  
  実装：[✓](https://github.com/SamsungLabs/LittleBit) ・ リポジトリ内被引用：8  
  大規模言語モデルの重みを4ビットへ量子化すると、FP16と比べて保存量を大きく減らせる。Llama2-13Bの0.1 BPWでは重み保存量をFP16の26.06GBから0.84GBへ縮小し、31.02倍の圧縮を報告する。

- **2025-08 · [Memory-R1: Enhancing Large Language Model Agents to Manage and Utilize Memories via Reinforcement Learning](2025-2508.19828-memory-r1-enhancing-large-language-model-agents-to-manage-and-utilize-me.md)**  
  実装：[✓](https://github.com/yansikuan/memory-r1) ・ リポジトリ内被引用：7  
  メモリ-R1は、記憶を管理するエージェント（メモリ Manager）と、検索した記憶から回答するエージェント（Answer Agent）を分離し、どちらも最終回答の正しさを報酬とする強化学習（reinforcement learning）で訓練する。

- **2025-04 · [Characterizing and Optimizing LLM Inference Workloads on CPU-GPU Coupled Architectures](2025-2504.11750-characterizing-and-optimizing-llm-inference-workloads-on-cpu-gpu-coupled.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  著者らはシステム対応カーネル推論プロファイラ（システム-Aware Kernel Inference Profiler; SKIP）を作り、PyTorch演算子からCUDA起動呼出し、GPUカーネルへ至る依存関係を時刻と対応付ける。

- **2025-10 · [PT2-LLM: Post-Training Ternarization for Large Language Models](2025-2510.03267-pt2-llm-post-training-ternarization-for-large-language-models.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/PT2-LLM) ・ リポジトリ内被引用：5  
  大規模言語モデルの重みを三値 {-1,0,+1} に制限すると、通常の2-bit量子化より少ない情報量で保存できる。LLaMA-7Bを三値化した場合、モデルサイズはFP16の13.48GBから1.88GBへ減り、圧縮倍率は7.17倍、変換時間は32分と報告される。

- **2025-10 · [lm-Meter: Unveiling Runtime Inference Latency for On-Device Language Models](2025-2510.06126-lm-meter-unveiling-runtime-inference-latency-for-on-device-language-mode.md)**  
  実装：[✓](https://github.com/amai-gsu/LM-Meter) ・ リポジトリ内被引用：4  
  さらにモバイルGPUではドライバが非公開で、カーネル単位の実行時間、キュー待機、ホスト側の発行遅延をアプリケーションから直接見ることが難しい。また量子化Gemma-2-2B-itの短い復号ではGPUの遊休時間が21%を超え、行列積カーネル群が実行時間の60%超を占める。

- **2025-09 · [LiquidGEMM: Hardware-Efficient W4A8 GEMM Kernel for High-Performance LLM Serving](2025-2509.01229-liquidgemm-hardware-efficient-w4a8-gemm-kernel-for-high-performance-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  LiquidGEMM は、重みを4ビット、活性を8ビットに量子化するW4A8構成の一般行列積（General Matrix Multiplication; GEMM）を高速化するGPUカーネルである。

- **2025-05 · [FlashFormer: Whole-Model Kernels for Efficient Low-Batch Inference](2025-2505.22758-flashformer-whole-model-kernels-for-efficient-low-batch-inference.md)**  
  実装：[✓](https://github.com/cheetah-lang) ・ リポジトリ内被引用：4  
  FlashFormerは、LLMをバッチ1で1トークンずつ復号する際、層ごとのカーネル起動と重み・KVキャッシュのメモリ転送が実行時間を支配するという状況に特化したGPUカーネル設計である。

- **2025-04 · [SD2: Self-Distilled Sparse Drafters](2025-2504.08838-sd2-self-distilled-sparse-drafters.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  投機的復号では、小さなドラフトモデルが数トークンを先に生成し、大きなターゲットモデルが候補をまとめて検証する。ドラフトが軽くてもターゲットと予測が合わなければ、受理されるトークン数が減り、高速化の利得が消える。逆に高精度なドラフトが重すぎれば、候補生成の逐次時間が支配的になる。受理長、理論MAC削減、実機の遅延改善は異なる評価軸として区別する。

- **2025-11 · [HipKittens: Fast and Furious AMD Kernels](2025-2511.08083-hipkittens-fast-and-furious-amd-kernels.md)**  
  実装：[✓](https://github.com/HazyResearch/HipKittens) ・ リポジトリ内被引用：3  
  HipKittens（HK）は、AMDのCDNA3およびCDNA4世代のGPU上で、行列積と注意計算を効率よく記述するためのC++組込み型の領域特化言語である。従来の高性能AMDカーネルは、AITERなどの手書きアセンブリに強く依存していた。HKはタイルという小行列単位の操作を開発者へ公開し、性能に効く低水準制御を再利用可能な部品へまとめる。

- **2025-09 · [Optimal Brain Restoration for Joint Quantization and Sparsification of LLMs](2025-2509.11177-optimal-brain-restoration-for-joint-quantization-and-sparsification-of-l.md)**  
  実装：[✓](https://github.com/cshguo/OBR) ・ リポジトリ内被引用：3  
  本論文は2025年9月公開のarXivプレプリントで、低ビット量子化と枝刈りを同時に適用する大規模言語モデルの圧縮を扱う。対象はLlama2、Llama3、Qwen2.5系列であり、重み4ビット・活性4ビット・KVキャッシュ4ビット（W4A4KV4）と50%の疎性を組み合わせることを主な目標とする。

- **2025-09 · [CoSpaDi: Compressing LLMs via Calibration-Guided Sparse Dictionary Learning](2025-2509.22075-cospadi-compressing-llms-via-calibration-guided-sparse-dictionary-learni.md)**  
  実装：[✓](https://github.com/mts-ai/CoSpaDi) ・ リポジトリ内被引用：3  
  異なる出力チャネルが異なる特徴を必要とする場合、この共通部分空間の制約が圧縮品質を損なう。LLaMA-3.2-1Bの20%圧縮率では、SVD-LLMの平均ゼロショット精度37.6%に対してCoSpaDiは42.7%で、WikiText PPLは約170から64へ低下した。

- **2025-07 · [BlockBPE: Parallel BPE Tokenization](2025-2507.11941-blockbpe-parallel-bpe-tokenization.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BlockBPEは正規表現による事前分割を廃止し、Rustで入力をバイト列と特殊トークンへ分けた後、各文字列を一つのGPUスレッドブロックへ割り当てる。高バッチではtiktokenに対して最大2倍、HuggingFace Tokenizersに対して最大2.5倍の字句分割処理量を報告した。

- **2025-05 · [FlashBias: Fast Computation of Attention with Bias](2025-2505.12044-flashbias-fast-computation-of-attention-with-bias.md)**  
  実装：[✓](https://github.com/thuml/FlashBias) ・ リポジトリ内被引用：3  
  注意バイアスを低ランク分解してクエリとキーへ埋め込み、二乗のメモリ読み込みを消すことでバイアス付き注意を無損失から近似まで含めて高速化した方式。

- **2025-11 · [Flashlight: PyTorch Compiler Extensions to Accelerate Attention Variants](2025-2511.02043-flashlight-pytorch-compiler-extensions-to-accelerate-attention-variants.md)**  
  実装：[✓](https://github.com/bozhiyou/pytorch-flashlight) ・ リポジトリ内被引用：2  
  通常のPyTorchコードから、統一リダクション表現と次元降格・代数変換・次元消去の融合でFlashAttention型カーネルを自動生成するコンパイラ拡張。テンプレートに合わない注意バリアントでもtorch.compile比5倍以上の高速化。

- **2025-10 · [Insum: Sparse GPU Kernels Simplified and Optimized with Indirect Einsums](2025-2510.17505-insum-sparse-gpu-kernels-simplified-and-optimized-with-indirect-einsums.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Insumは、疎演算を間接インデックス付きEinsum（indirect Einsum）へ変換することで、疎テンソルの値と座標情報を、通常のdense テンソル演算へ写像する。

- **2025-10 · [Compressed Convolutional Attention: Efficient Attention in a Compressed Latent Space](2025-2510.04476-compressed-convolutional-attention-efficient-attention-in-a-compressed-l.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CCGQAはさらにGQA型の鍵・値ヘッド共有を潜在空間で行い、クエリの圧縮率 $C1$ とKVの圧縮率 $C2$ を分離する。H100上の融合カーネル評価では、隠れ次元2048、BF16、系列長16Kの事前処理で、CCAの4倍圧縮設定がMHA比約1.6〜1.7倍低遅延、逆伝播で約1.2〜1.3倍高速となる。

- **2025-08 · [ExpertWeave: Efficiently Serving Expert-Specialized Fine-Tuned Adapters at Scale](2025-2508.17624-expertweave-efficiently-serving-expert-specialized-fine-tuned-adapters-a.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  従来のLoRA配信は基盤重みに低ランク差分を加算する設計であり、ESFTで必要な「ルーティングが選んだ元専門家を、タスク固有の別重みに差し替える」動作には直接対応しない。単一64GB NPUで二つのアダプタを扱う際、個別mergedモデル方式のKVキャッシュ容量約6K トークンに対し、ExpertWeaveは572K トークン超を確保した。

- **2025-08 · [APT-LLM: Exploiting Arbitrary-Precision Tensor Core Computing for LLM Acceleration](2025-2508.19087-apt-llm-exploiting-arbitrary-precision-tensor-core-computing-for-llm-acc.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  APT-LLMが解くのは、モデルをINT2やINT3まで量子化しても、GPUの行列積命令がその精度を直接サポートしないため、低ビット化した理論上の利点を実際の推論速度へ移しにくい問題である。

- **2025-06 · [MCFuser: High-Performance and Rapid Fusion of Memory-Bound Compute-Intensive Operators](2025-2506.22169-mcfuser-high-performance-and-rapid-fusion-of-memory-bound-compute-intens.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  削減次元が小さく帯域律速へ転じた計算集約演算子の連鎖を、タイル式の完全な探索空間とグラフ解析による冗長転送の除去、解析的性能模型による高速な探索で融合し、カーネルを最大五・九倍速くし調整時間を七十倍以上短縮した。

- **2025-06 · [EQuARX: Efficient Quantized AllReduce in XLA for Distributed Machine Learning Acceleration](2025-2506.17615-equarx-quantized-allreduce-xla.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  AllReduce内でブロック量子化と逆量子化を通信へ重ね、TPU/XLAの集団通信量を削減する方式。int8でBF16 AllReduce比最大1.8倍、Gemma 3 27Bプリフィル最大1.28倍を示す。

- **2025-02 · [PASER: Post-Training Data Selection for Efficient Pruned Large Language Model Recovery](2025-2502.12594-paser-post-training-data-selection-for-efficient-pruned-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  常識推論、知識、翻訳、文章生成などの一部だけが大きく損なわれる場合、汎用instructionデータを均等に使って回復学習しても、限られた学習予算を劣化していない能力へ使ったり、互いに矛盾する指示へ過適合したりする。PASERは、剪定済みLLMのどの能力がどれだけ変化したかを元モデルとの出力分布の差で推定し、その劣化に応じて回復学習データを選ぶ方式である。

- **2025-11 · [You Had One Job: Per-Task Quantization Using LLMs’ Hidden Representations](2025-2511.06516-you-had-one-job-per-task-quantization-using-llms-hidden-representations.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  一般的な学習後量子化（Post-学習 量子化; PTQ）は、言語モデルの重みを一律に4ビットへ圧縮したり、重み再構成誤差に基づいて精度を選んだりする。原著第4版では、Qwen2.5-7B-InstructのMMLU-Proで、TAQ-KLが35.35点・重み5.95GB、均一4ビットのAWQが23.54点・5.19GBだった。

- **2025-11 · [Optimizing Attention on GPUs by Exploiting GPU Architectural NUMA Effects](2025-2511.02132-optimizing-attention-on-gpus-by-exploiting-gpu-architectural-numa-effect.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  チップレット型GPUで、同じキーと値を共有するワークグループを同じダイへ寄せてL2再利用を回復するフラッシュアテンション2の配置最適化。最大50パーセント高速化し無損失。

- **2025-11 · [KernelBand: Steering LLM-based Kernel Optimization via Hardware-Aware Multi-Armed Bandits](2025-2511.18868-kernelband-steering-llm-based-kernel-optimization-via-hardware-aware-mul.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  高性能な実装では、演算量だけでなく、レジスタ圧迫、共有メモリ、キャッシュ利用、メモリ帯域、スレッド配置を同時に考える必要がある。KernelBandは、この探索判断を文脈付き多腕バンディット（contextual multi-armed bandit、MAB）へ置き換える方式である。

- **2025-08 · [FlexQ: Efficient Post-training INT6 Quantization for LLM Serving via Algorithm-System Co-Design](2025-2508.04405-flexq-efficient-post-training-int6-quantization-for-llm-serving-via-algo.md)**  
  実装：[✓](https://github.com/FlyFoxPlayer/FlexQ) ・ リポジトリ内被引用：1  
  FlexQは、LLMの重みと活性値を6bitへ量子化して品質を維持しつつ、GPU上で本当に高速に実行するための方式である。

- **2025-07 · [Cloud Native System for LLM Inference Serving](2025-2507.18007-cloud-native-system-for-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、LLM推論を一体のモデルプロセスとして固定配置する方式では、あるTransformer層だけが過負荷になってもモデル全体を複製するしかなく、必要な資源へ局所的に対処しにくいと指摘する。実験はLLaMA-2-13B、A100 80GBを備えた3ノードのKubernetesクラスタで行う。

- **2025-07 · [BlindSight: Harnessing Sparsity for Efficient Vision-Language Models](2025-2507.09071-blindsight-harnessing-sparsity-for-efficient-vision-language-models.md)**  
  実装：[✓](https://anonymous.4open.science/r/BlindSight-AFDC) ・ リポジトリ内被引用：1  
  各ヘッドをDense（密）、Sink（境界シンク）、Intra-Image（同じ画像内）、Intra-Image+Sink（画像内と境界シンク）の4種類へ割り当て、実行時には画像境界位置だけから固定的な疎注意マスクを作る。

- **2025-05 · [Low-Cost FlashAttention with Fused Exponential and Multiplication Hardware Operators](2025-2505.14314-low-cost-flashattention-with-fused-exponential-and-multiplication-hardwa.md)**  
  実装：[✓](https://github.com/ic-lab-duth/Fused-ExpMul) ・ リポジトリ内被引用：1  
  本論文は、FlashAttention-2の計算アルゴリズムを変えるのではなく、オンラインsoftmaxに必要な指数関数とValueベクトル乗算をASIC上の一つの演算器へまとめるハードウェア最適化を提案する。

- **2025-05 · [Highly Efficient and Effective LLMs with Multi-Boolean Architectures](2025-2505.22811-highly-efficient-and-effective-llms-with-multi-boolean-architectures.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MBOK（Multiple Boolean Kernels）の基本表現は、通常の実数重み行列を複数の符号行列とチャネル別スケールの和で近似するものである。各カーネルの重みは1-bitで、入力側・出力側の実数スケールを別途持つ。元のFP重みから順に近似成分を抽出し、残差へ同じ分解を繰り返すため、単一の符号行列より表現力が高い。

- **2025-04 · [Tilus: A Tile-Level GPGPU Programming Language for Low-Precision Computation](2025-2504.12984-tilus-a-tile-level-gpgpu-programming-language-for-low-precision-computat.md)**  
  実装：[✓](https://github.com/NVIDIA/tilus) ・ リポジトリ内被引用：1  
  一から八ビットの任意幅の低精度型を原生的に扱い、配置の代数と再解釈で配置変換を消しパイプライン化を保つタイル単位の言語で、低精度カーネルが既存コンパイラより一・七五倍と二・六一倍、手書きカーネルより一・二九倍と一・〇三倍速くなった。

- **2025-04 · [GPU Performance Portability needs Autotuning](2025-2505.03780-gpu-performance-portability-needs-autotuning.md)**  
  実装：[✓](https://github.com/foundation-model-stack/vllm-triton-backend) ・ リポジトリ内被引用：1  
  行列のタイル寸法、warp数、パイプライン段数、共有メモリ、レジスタ割当てをあるGPUへ手作業で合わせると、別のGPUでは速度が落ち、カーネルを移植するたびにCUDA/HIPの実装と検証を繰り返す必要がある。モデル全体の学習やサービングスケジューラを新しくする研究ではない。

- **2025-03 · [Samoyeds: Accelerating MoE Models with Structured Sparsity Leveraging Sparse Tensor Cores](2025-2503.10725-samoyeds-accelerating-moe-models-with-structured-sparsity-leveraging-spa.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  全専門家を毎回動かさないことで計算量を抑えられるが、実装上はトークンを専門家ごとに並べ替える入力転置、専門家の行列積、出力の再結合、GPUメモリの読み書きが必要になる。従来の高速化では、重みの構造化枝刈りによる疎性と、トークンが選択された専門家にだけ存在するという活性側の疎性を別々に扱うことが多かった。

- **2025-03 · [Maximum Redundancy Pruning: A Principle-Driven Layerwise Sparsity Allocation for LLMs](2025-2503.18377-maximum-redundancy-pruning-a-principle-driven-layerwise-sparsity-allocat.md)**  
  実装：[✓](https://github.com/Gaochang-bjtu/MRP) ・ リポジトリ内被引用：1  
  本論文は、大規模言語モデルの重み枝刈りで「全層に同じ疎度を設定すること」が精度を損ねる理由を実験的に調べ、その結果から層別疎度を決めるMaximum Redundancy Pruning（MRP）を提案する。特に全体の70%を削る高疎度では、ある層を削ると出力が急激に悪化する一方、別の層はさらに削っても影響が小さい。

- **2024-12 · [GQSA: Group Quantization and Sparsity for Accelerating Large Language Model Inference](2024-2412.17560-gqsa-group-quantization-and-sparsity-for-accelerating-large-language-mod.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMの推論を軽くする方法として、重みを低ビット化する量子化と、重要度の低い重みを削除する疎化がある。特に2:4の半構造化疎化はハードウェアに合う一方、疎化率が50%に固定され、低ビット量子化と自由に組み合わせにくい。

- **2025-11 · [Kunlun Anomaly Troubleshooter: Enabling Kernel-Level Anomaly Detection and Causal Reasoning for Large Model Distributed Inference](2025-2511.05978-kunlun-anomaly-troubleshooter-enabling-kernel-level-anomaly-detection-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模モデルの分散推論では、複数のGPUワーカーがモデル並列化の演算、集合通信、メモリ操作、要求処理を協調して実行する。本論文のKunlun Anomaly Troubleshooter（KAT）は、検出と説明を分離する。Outpostの異常イベント検出では適合率88.4%、再現率93.6%、F1値90.1%、偽陽性率0.27%を報告する。

- **2025-11 · [FlashEVA: Accelerating LLM inference via Efficient Attention](2025-2511.00576-flasheva-accelerating-llm-inference-via-efficient-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashEVAは、既存の全注意Transformerを再学習なしで置き換える方式ではなく、事前学習済み重みを出発点に、近似注意へ構造を変えたモデルを追加学習して高速化する研究である。2048トークンの入力に対して最大10240トークンを生成する条件では、通常Transformerに対して生成処理量が最大6.7倍、ピークGPUメモリが最大5分の1となった。

- **2025-11 · [Efficient Kernel Mapping and Comprehensive System Evaluation of LLM Acceleration on a CGLA](2025-2512.00335-efficient-kernel-mapping-and-comprehensive-system-evaluation-of-llm-acce.md)**  
  実装：[✓](https://github.com/Takuto-Ando/IMAX3-LLM) ・ リポジトリ内被引用：0  
  汎用の粗粒度線形アレイIMAXへllama.cppの量子化カーネルを写像してQwen3を動かし、FPGA実測とASIC投影で、遅延はGPUに劣るが電力遅延積は最大44.4倍良いことを示した包括評価。

- **2025-11 · [EcoSpa: Efficient Transformer Training with Coupled Sparsity](2025-2511.11641-ecospa-efficient-transformer-training-with-coupled-sparsity.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerの注意機構では問い合わせ射影と鍵射影が内積を作り、値射影と出力射影も積として機能する。一次論文の表1では、LLaMA-1BのC4事前学習でメモリ7.80GBから3.88GB、学習時間51.1時間から40.3時間、トークン処理量21,786.49から35,211.27/s、検証パープレキシティ15.56から15.60という結果を報告する。

- **2025-10 · [Transformer Based Linear Attention with Optimized GPU Kernel Implementation](2025-2510.21956-transformer-based-linear-attention-with-optimized-gpu-kernel-implementat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、線形注意機構（Linear 注意機構、LA）の漸近的な計算量が小さいのに、実際のGPUでは必ずしも高速でない問題を扱う。A6000上の単層注意機構実験では、Gated LAに対して最大3.3倍の速度と3.6分の1のメモリ使用量を報告する。

- **2025-10 · [RACE Attention: A Strictly Linear-Time Attention Layer for Training on Outrageously Large Contexts](2025-2510.04008-race-attention-a-strictly-linear-time-attention-layer-for-training-on-ou.md)**  
  実装：[✓](https://github.com/sahiljoshi515/RACE_Attention) ・ リポジトリ内被引用：0  
  RACE 注意機構は、Transformerのsoftmax注意が系列長Nに対してO(N²d)のQuery-Key相互作用を要求する問題を、別の注意カーネルと確率的スケッチで解決する研究である。

- **2025-10 · [PermLLM: Learnable Channel Permutation for N:M Sparse Large Language Models](2025-2510.10136-permllm-learnable-channel-permutation-for-n-m-sparse-large-language-mode.md)**  
  実装：[✓](https://github.com/lanchengzou/PermLLM) ・ リポジトリ内被引用：0  
  チャネル順序を入れ替えてからマスクを決めれば保持する重みの組合せを変えられるが、従来の手法は残存重みの重要度スコアを最大化するヒューリスティックに依存していた。

- **2025-10 · [Opt4GPTQ: Co-Optimizing Memory and Computation for 4-bit GPTQ Quantized LLM Inference on Heterogeneous Platforms](2025-2511.19438-opt4gptq-co-optimizing-memory-and-computation-for-4-bit-gptq-quantized-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ハイゴンDCU上でvLLMのGPTQ 4ビットカーネルへ、共有メモリ集約・ベクトル化ロード・インラインアセンブリの3最適化を統合し、スループットを最大84.42%改善するプラットフォーム適応の実践研究。

- **2025-10 · [NeuronMM: High-Performance Matrix Multiplication for LLM Inference on AWS Trainium](2025-2510.25977-neuronmm-high-performance-matrix-multiplication-for-llm-inference-on-aws.md)**  
  実装：[✓](https://github.com/dinghongsong/NeuronMM) ・ リポジトリ内被引用：0  
  Trainium向けに、重みの特異値分解のランクをタイル境界へ揃え、二つの行列積を中間結果のSRAMキャッシュと暗黙の転置で融合することで、AWS公式カーネル比でエンドツーエンド推論を平均1.66倍高速化する行列積カーネル。

- **2025-10 · [Exact Causal Attention with 10% Fewer Operations](2025-2510.05175-exact-causal-attention-with-10-fewer-operations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、自己回帰型Transformerの因果注意（causal 注意機構）を、近似やトークン削除を行わずに、計算に必要な加減算・乗算を減らす問題を扱う。構造を利用することで、通常の三角領域だけを計算する行列積に対して約9.4%の主要な乗算を削減し、再帰的な適用では理論上約11.1%の削減が可能とする。

- **2025-10 · [Automatically Generating ML Compiler Backends from Tensor Accelerator ISA Descriptions](2025-2510.09932-automatically-generating-ml-compiler-backends-from-tensor-accelerator-is.md)**  
  実装：[✓](https://github.com/act-compiler/act) ・ リポジトリ内被引用：0  
  命令セット記述だけから機械学習コンパイラのバックエンドを自動生成し、Trainiumで本家コンパイラの2.3倍の生成カバレッジ、Gemminiで手調整ライブラリ比最大6.88倍を達成したバックエンド生成器。

- **2025-10 · [Accelerating Attention with Basis Decomposition](2025-2510.01718-accelerating-attention-with-basis-decomposition.md)**  
  実装：[✓](https://github.com/abcbdf/basis-decomposition-official) ・ リポジトリ内被引用：0  
  TransformerのMulti-Head 注意機構では、入力からQuery、Key、Valueを線形投影し、QK内積とSoftmax、Valueの重み付き和、出力投影を計算する。FP16のWikiText2 PPLは6.307075から6.308252へごくわずかに悪化する一方、投影演算のGPU速度は平均1.34倍、対象重みは25%減る。

- **2025-09 · [TyphoonMLA: A Mixed Naive-Absorb MLA Kernel For Shared Prefix](2025-2509.21081-typhoonmla-a-mixed-naive-absorb-mla-kernel-for-shared-prefix.md)**  
  実装：[✓](https://github.com/huawei-csl/TyphoonMLA-community) ・ リポジトリ内被引用：0  
  TyphoonMLAは、DeepSeek-v3やKimi K2に採用される多頭潜在注意（Multi-Head Latent 注意機構、MLA）で、複数要求が同じ入力prefixを共有する場合のデコードを高速化する。原著のカーネル実測は、Ascend NPUで最大3.0倍、GPUで最大3.24倍の注意処理量改善を報告する。

- **2025-07 · [Toward Efficient SpMV in Sparse LLMs via Block Extraction and Compressed Storage](2025-2507.12205-toward-efficient-spmv-in-sparse-llms-via-block-extraction-and-compressed.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非構造化剪定は、大規模言語モデルの重みを疎にしてメモリ容量を減らす。しかしゼロ要素を単に削除しただけでは、GPUでの生成が速くなるとは限らない。特にローカルLLMのようにバッチサイズが1の自己回帰デコードでは、線形層の重み行列と入力ベクトルの積が繰り返される。まず非ゼロ要素の共通列を持つ行を組み合わせ、複数の粒度でブロックを抽出する。

- **2025-07 · [PoTPTQ: A Two-step Power-of-Two Post-training for LLMs](2025-2507.11959-potptq-a-two-step-power-of-two-post-training-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを2の冪で表す量子化のスケールを、重みだけのグリッド探索と少量較正での残差学習の2段で決め、ビット操作の逆量子化で推論も速くする学習後量子化。3.25ビットで一様量子化の最先端を上回り、逆量子化は最大3.67倍高速。

- **2025-07 · [Degrees of Freedom for Linear Attention: Distilling Softmax Attention with Optimal Feature Efficiency](2025-2507.03340-degrees-of-freedom-for-linear-attention-distilling-softmax-attention-wit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意カーネルの統計的自由度から層ごとの実効次元を推定し、同じ計算予算のまま線形注意の特徴次元を層別に配分し直すことで、ソフトマックス注意から線形注意への蒸留精度を上げる次元選択法。

- **2025-06 · [Spectra 1.1: Scaling Laws and Efficient Inference for Ternary Language Models](2025-2506.23025-spectra-1-1-scaling-laws-and-efficient-inference-for-ternary-language-mo.md)**  
  実装：[✓](https://github.com/NolanoOrg/TriRun) ・ リポジトリ内被引用：0  
  三値言語モデルのスケーリング則と推論高速化を一体で示す研究。パラメータより学習トークンの拡大が効くことを示し、重みを1.6ビットと2ビットへ詰める方式とGPUカーネルTriRunで70Bモデルを4.9倍高速化した。

- **2025-05 · [Turning LLM Activations Quantization-Friendly](2025-2506.01967-turning-llm-activations-quantization-friendly.md)**  
  実装：[✓](https://github.com/czakop/smooth-rot-exper) ・ リポジトリ内被引用：0  
  LLMの重み-only量子化は重み転送量を削減する一方、活性がFP16/BF16のままなら、行列演算を低bit整数だけで完結させることはできない。

- **2025-05 · [QuantX: A Framework for Hardware-Aware Quantization of Generative AI Workloads](2025-2505.07531-quantx-a-framework-for-hardware-aware-quantization-of-generative-ai-work.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み分布・外れ値・注意マップの歪みを層ごとに観測して均一／非一様量子化とビット幅を選び、ハードウェア制約も入れるレシピ集で、LLaVA-v1.6を3ビット化してFP16比6パーセント以内の精度低下に収める研究。

- **2025-05 · [M-Wanda: Improving One-Shot Pruning for Multilingual LLMs](2025-2505.21171-m-wanda-improving-one-shot-pruning-for-multilingual-llms.md)**  
  実装：[✓](https://github.com/RochelleChoenni/M-Wanda) ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の重みを一部ゼロにする枝刈り（枝刈り）は、保存する非ゼロ重みを減らすための圧縮方法である。50%の非構造化疎化率で、Llama3-8BのFlores平均パープレキシティ（perplexity、低いほど次トークン予測が良好）はWandaの19.59からM-Wandaの18.57へ下がった。

- **2025-05 · [HybridServe: Efficient Serving of Large AI Models with Confidence-Based Cascade Routing](2025-2505.12566-hybridserve-efficient-serving-of-large-ai-models-with-confidence-based-c.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小型モデルへ置き換える蒸留・量子化は電力を削減できるが、難しい要求で品質を落としやすい。論文は最大19.8倍の省電力と記載するが、丸め済み表の値から計算すると115/6=19.17倍である。

- **2025-05 · [FireQ: Fast INT4-FP8 Kernel and RoPE-aware Quantization for LLM Inference Acceleration](2025-2505.20839-fireq-fast-int4-fp8-kernel-and-rope-aware-quantization-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みINT4・活性FP8の混合精度カーネルとRoPE配慮の外れ値平滑化、3段パイプラインの注意カーネルを共同設計した量子化推論手法。FFNでQServe比1.68倍、プリフィルで1.26倍を精度を保って達成。

- **2025-05 · [COUNTDOWN: Contextually Sparse Activation Filtering Out Unnecessary Weights in Down Projection](2025-2505.17701-countdown-contextually-sparse-activation-filtering-out-unnecessary-weigh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  下方射影の重み付き和という見方から、直接係数と間接係数で残す中間次元を選ぶ二つの疎な活性化を導き、理想条件で90パーセントの計算省略と最良5.5パーセントの低下、予測器なし方式ではCATS比で最大29.4パーセント良い性能保持を示す。

- **2025-04 · [Pruning Laws for Large Language Models](2025-2504.04342-pruning-laws-for-large-language-models.md)**  
  実装：[✓](https://github.com/parmanu-lcs2/pruning_laws) ・ リポジトリ内被引用：0  
  LLMの構造化・非構造化枝刈りは、重み容量や推論演算量を減らすが、何%を削ると下流課題の正答率がどの程度低下するかを事前に知るのは難しい。モデル未剪定時の性能をL0、削除した割合をrとすると、枝刈り後の性能Lを L = L0 × P0 × (1−r)^α と近似する。

- **2025-04 · [ParallelFlow: Parallelizing Linear Transformers via Flow Discretization](2025-2504.00492-parallelflow-parallelizing-linear-transformers-via-flow-discretization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ParallelFlowは、線形注意機構や行列値状態空間モデル（SSM）の逐次更新を、制御微分方程式（CDE）の区間フローとして表現する理論・アルゴリズム研究である。

- **2025-04 · [Minimizing transformer inference overhead using controlling element on Shenwei AI accelerator](2025-9d0005ab2d5d-minimizing-transformer-inference-overhead-using-controlling-element-on-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Whisper推論の実測分解で読み込みと起動が全体の最大96パーセントを占めることを示し、アクセラレータ上の制御要素へ制御を寄せる三層スケジューリング、ゼロコピー、高速読み込みで起動費用と読み込み時間を桁違いに削る研究。

- **2025-03 · [NM-SpMM: Accelerating Matrix Multiplication Using N:M Sparsity with GPGPU](2025-2503.01253-nm-spmm-accelerating-matrix-multiplication-using-n-m-sparsity-with-gpgpu.md)**  
  実装：[✓](https://github.com/M-H482/NM-SpMM) ・ リポジトリ内被引用：0  
  N:Mスパース行列積について疎性で計算律速からメモリ律速へ移ることを分析し、階層的ブロッキングと疎性に応じたパッキングおよびパイプラインで、汎用実装nmSPARSEより2.1倍速くするGPUカーネル。

- **2025-02 · [AdaSplash: Adaptive Sparse Flash Attention](2025-2502.12082-adasplash-adaptive-sparse-flash-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常のsoftmax注意では、注意スコアが有限であれば全トークンへ正の確率が割り当てられる。合成8192要素の閾値計算ではTorch二分法36.67msに対しHalley-bisection2.38ms、約15倍の改善を報告する。

- **2025-01 · [Longer Attention Span: Increasing Transformer Context Length with Sparse Graph Processing Techniques](2025-2502.01659-longer-attention-span-increasing-transformer-context-length-with-sparse-.md)**  
  実装：[✓](https://github.com/KLab-AI3/Graph-Processing-Attention-IPDPS-2025) ・ リポジトリ内被引用：0  
  本論文の主張は、疎な注意機構 maskを使うだけではGPUの計算は必ずしも疎にならない、という実装上の問題を解決することである。

- **2024-12 · [Adaptive Layer Sparsity for Large Language Models via Activation Correlation Assessment](2024-8203b84bd016-adaptive-layer-sparsity-for-large-language-models-via-activation-correla.md)**  
  実装：[✓](https://github.com/lliai/ALS) ・ リポジトリ内被引用：0  
  層間活性値の相互情報量から作る冗長性指標を目的関数にした線形計画で層別スパース率を大域的に配分し、一様配分の枝刈りよりパープレキシティとゼロショット精度の劣化を抑える配分方式。

### 3年前（2023-12〜2024-11）

- **2024-07 · [FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](2024-2407.08608-flashattention-3-fast-and-accurate-attention-with-asynchrony-and-low-pre.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：233  
  従来のFlashAttention系列は、注意重みの巨大な中間行列を高帯域メモリ（HBM）に書き戻さず、共有メモリとレジスタ内でタイルごとに処理することでメモリ転送を削減した。

- **2024-04 · [PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation](2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transf.md)**  
  実装：[✓](https://github.com/pytorch/pytorch) ・ リポジトリ内被引用：70  
  Pythonの即時実行の柔軟性を残して演算グラフを実行時に取り出し、TritonやC++へコンパイルする仕組みを設計・評価した。

- **2024-06 · [S-LoRA: Serving Thousands of Concurrent LoRA Adapters](2024-2311.03285-s-lora-serving-thousands-of-concurrent-lora-adapters.md)**  
  実装：[✓](https://github.com/S-LoRA/S-LoRA) ・ リポジトリ内被引用：56  
  しかし、数千の個別化モデルを同時提供する場合、アダプタの保存先、要求ごとの重み切替、系列長に応じて伸びる鍵・値キャッシュ、異なる低ランク行列を使う要求のバッチ化が問題になる。アダプタを基盤モデルへ統合して個別のモデル重みを作る方式では、基盤部分を要求間で共有してまとめて計算する機会を失う。

- **2024-10 · [SageAttention: Accurate 8-Bit Attention for Plug-and-play Inference Acceleration](2024-2410.02367-sageattention-accurate-8-bit-attention-for-plug-and-play-inference-accel.md)**  
  実装：[✓](https://github.com/thu-ml/SageAttention) ・ リポジトリ内被引用：35  
  一般的なモデル量子化は全結合層の重み・活性へ集中するが、長い文脈では注意行列を計算するQKᵀと、注意重みを値へ適用するPVの行列積が大きな費用を占める。RTX 4090での注意カーネルの演算性能は、FlashAttention-2比で概ね2.1倍、xformers比で概ね2.7倍と報告される。

- **2024-06 · [T-MAC: CPU Renaissance via Table Lookup for Low-Bit LLM Deployment on Edge](2024-2407.00088-t-mac-cpu-renaissance-via-table-lookup-for-low-bit-llm-deployment-on-edg.md)**  
  実装：[✓](https://github.com/microsoft/T-MAC) ・ リポジトリ内被引用：35  
  重みのみを低ビット量子化した大規模言語モデルでは、重みは1〜4ビットでも活性値は8〜16ビット以上の精度を保つことが多い。論文はカーネルの最大6.6倍、平均3.6倍の改善、モデル全体で条件により2〜4倍の生成速度改善を報告する。

- **2024-02 · [Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs](2024-2402.10517-any-precision-llm-low-cost-deployment-of-multiple-different-sized-llms.md)**  
  実装：[✓](https://github.com/SNU-ARC/any-precision-llm) ・ リポジトリ内被引用：33  
  Any-Precision LLMは、同じ大規模言語モデルを複数の量子化精度で運用する場合のメモリと作成費用を削減する研究である。Llama-2-7Bの3～8ビット6種類を個別配置する場合29.9GBに対し、共通配置では8.4GBとなり、3.56倍の容量節約を報告する。

- **2024-06 · [FLUX: Fast Software-based Communication Overlap On GPUs Through Kernel Fusion](2024-2406.06858-flux-fast-software-based-communication-overlap-on-gpus-through-kernel-fu.md)**  
  実装：[✓](https://github.com/bytedance/flux) ・ リポジトリ内被引用：32  
  テンソル並列では、行列の列や行をGPUごとに分割して計算する。各GPUが自分の部分を処理しても、次の行列積が必要とする入力を集める全収集（AllGather）、あるいは計算結果を加算して分散する縮約散布（ReduceScatter）が必要になる。通信の完了を待ってから次の行列積を始めると、GPUが計算できない待機時間が生じる。

- **2024-04 · [CATS: Contextually-Aware Thresholding for Sparsity in Large Language Models](2024-2404.08763-cats-contextually-aware-thresholding-for-sparsity-in-large-language-mode.md)**  
  実装：[✓](https://github.com/ScalingIntelligence/CATS) ・ リポジトリ内被引用：30  
  大規模言語モデルの多層パーセプトロン（MLP）では、活性値の小さい中間ニューロンも密行列積の対象となる。特にバッチが小さい自己回帰復号では、重みをGPUメモリから読む帯域が処理時間を制限しやすい。混合専門家（MoE）モデルは一部の専門家だけを選ぶが、通常のLlama2やMistralの密なGated-MLPにはそのような明示的な専門家選択器がない。

- **2024-05 · [Mirage: A Multi-Level Superoptimizer for Tensor Programs](2024-2405.05751-mirage-a-multi-level-superoptimizer-for-tensor-programs.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：27  
  Mirageは「既知のアルゴリズムに対して良いGPUスケジュールを探す」だけでも、「数式を書き換えて既存カーネルを組み合わせる」だけでもない。テンソル計算をGPUのカーネル・スレッドブロック・スレッド階層をまたぐμGraphで表し、数式の形、融合境界、並列化方法を同じ探索の中で変えることで、人手では実装量が大きい複合最適化を自動発見する。

- **2024-10 · [ThunderKittens: Simple, Fast, and Adorable AI Kernels](2024-2410.20399-thunderkittens-simple-fast-and-adorable-ai-kernels.md)**  
  実装：[✓](https://github.com/HazyResearch/ThunderKittens) ・ リポジトリ内被引用：22  
  各演算ごとに大量のCUDA制御コードを書く代わりに、タイル演算と「ロード・計算・保存・終了」の4段階を指定し、共有メモリの配置や同期の多くを共通部品に任せる。さらに、行列積の段数を1から4へ増やすと260→760 TFLOPS、L2再利用を意識したブロック順序では805対392 TFLOPSという差があり、性能改善の機構を個別に検証している。

- **2023-12 · [An LLM Compiler for Parallel Function Calling](2023-2312.04511-an-llm-compiler-for-parallel-function-calling.md)**  
  実装：[✓](https://github.com/SqueezeAILab/LLMCompiler) ・ リポジトリ内被引用：21  
  言語モデルに検索、計算、データ取得などの外部関数を使わせる場合、素朴な方式では「一つの関数を呼ぶ、結果を読む、次の関数を決める」という往復を繰り返す。HotpotQAでは逐次方式ReAct比1.80倍、Movie Recommendationでは3.74倍、依存付きParallelQAでは最大2.27倍の遅延改善を報告する。

- **2024-08 · [STBLLM: Breaking the 1-Bit Barrier with Structured Binary LLMs](2024-2408.01803-stbllm-breaking-the-1-bit-barrier-with-structured-binary-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  大規模言語モデルの推論では、特にバッチの小さい復号段階で重みを主記憶やGPUメモリから読み出す帯域が律速になりやすい。従来の二値化手法は、重要な重みを別扱いにしたり残差を追加したりして精度を回復するものの、重み当たり約1ビットの表現からさらに削る余地が残る。

- **2024-03 · [AIOS: LLM Agent Operating System](2024-2403.16971-aios-llm-agent-operating-system.md)**  
  実装：[✓](https://github.com/agiresearch/AIOS) ・ リポジトリ内被引用：19  
  従来のエージェント枠組みでは、各エージェントがLLMやツールを直接呼び出し、GPUメモリの不足、競合するAPI呼び出し、長時間要求の独占を個別に処理しがちだった。AIOSはエージェントアプリケーションと資源管理を分離し、専用のAIOSカーネルを通じてサービスを提供する。

- **2024-07 · [LeanQuant: Accurate and Scalable Large Language Model Quantization with Loss-error-aware Grid](2024-2407.10032-leanquant-accurate-and-scalable-large-language-model-quantization-with-l.md)**  
  実装：[✓](https://github.com/LeanModels/LeanQuant) ・ リポジトリ内被引用：17  
  LeanQuantは、大規模言語モデルの学習後量子化（Post-学習 量子化; PTQ）で、各重みをどの離散値へ丸めるかを決める量子化格子の位置を最適化する手法である。Llama-3.1-405Bの量子化を48GB GPU二枚と大容量CPUメモリで約20.7時間で完了した。

- **2024-05 · [Large Language Model Pruning](2024-2406.00030-large-language-model-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：17  
  ニューロン同士の相互情報量で冗長性を測り、カーネル幅の新しい推定で精度を高めた、教師なし・再学習不要の全結合層の構造的枝刈り手法。

- **2024-05 · [LeanAttention: Hardware-Aware Scalable Attention Mechanism for the Decode-Phase of Transformers](2024-2405.10480-lean-attention-hardware-aware-scalable-attention-mechanism.md)**  
  実装：[✓](https://github.com/microsoft/onnxruntime) ・ リポジトリ内被引用：16  
  LeanAttentionが減らすのは注意の数学的な計算量ではない。まったく同じ厳密注意を、長いKV文脈方向へ細かく分割し、GPUの全SMへ端数なく近い形で仕事を割り振る。デコードでは問い合わせが1トークンしかないため従来のタイル並列性が不足する、というハードウェア利用率の問題を解く。

- **2024-04 · [DeFT: Decoding with Flash Tree-Attention for Efficient Tree-structured LLM Inference](2024-2404.00242-deft-decoding-with-flash-tree-attention-for-efficient-tree-structured-ll.md)**  
  実装：[✓](https://github.com/LINs-lab/DeFT) ・ リポジトリ内被引用：15  
  従来のGPU注意カーネルは通常の一本の系列を想定し、クエリごとに必要なKVを集めるため、同じ接頭辞のKVを何度もGPU広帯域メモリから共有メモリへ運ぶ。DeFT（デコード with Flash Tree-注意機構）は、木構造のKVと複数クエリを一緒に分割する際の基準を逆転させる。

- **2024-06 · [ShiftAddLLM: Accelerating Pretrained LLMs via Post-Training Multiplication-Less Reparameterization](2024-2406.05981-shiftaddllm-accelerating-pretrained-llms-via-post-training-multiplicatio.md)**  
  実装：[✓](https://github.com/GATECH-EIC/ShiftAddLLM) ・ リポジトリ内被引用：10  
  大規模言語モデルの重みを低ビット化すればGPUメモリの占有を減らせる。しかし、通常の重み量子化では、低ビット整数を推論時に浮動小数点へ復元して乗算する場合があり、保存容量の削減がそのまま計算演算の削減を意味しない。OPT-66Bの重みメモリはFP16の122 GBから３ビット時23 GB、２ビット時16 GBへ減少した。

- **2024-09 · [CHESS: Optimizing LLM Inference via Channel-Wise Thresholding and Selective Sparsification](2024-2409.01366-chess-optimizing-llm-inference-via-channel-wise-thresholding-and-selecti.md)**  
  実装：[✓](https://github.com/ZeonfaiHo/CHESS) ・ リポジトリ内被引用：8  
  注意機構には同じ閾値を機械的に適用せず、問い合わせ射影と出力射影に限定して活性疎化を行う。Intel Core i9-12900K、64GB DDR4、単一要求、FP32というCPU測定条件で、注意投影も選択的に疎化した構成の復号高速化は最大1.27倍である。

- **2024-03 · [Scattered Mixture-of-Experts Implementation](2024-2403.08245-scattered-mixture-of-experts-implementation.md)**  
  実装：[✓](https://github.com/shawntan/scattermoe) ・ リポジトリ内被引用：8  
  特にバッチが大きい学習や複数要求の推論では、中間のトークン表現を何度も高帯域メモリへ書き戻すことが問題になる。ScatterMoEは専門家へ割り当てたトークンを実体の配列として並べ替える代わりに、専門家順の索引を並べ替え、カーネルが入力の必要な位置を直接読み込む。

- **2024-02 · [L4Q: Parameter Efficient Quantization-Aware Fine-Tuning on Large Language Models](2024-2402.04902-l4q-parameter-efficient-quantization-aware-fine-tuning-on-large-language.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  巨大言語モデル（LLM）の低ビット量子化は推論時の重み容量とメモリ帯域を減らすが、精度低下を起こす。LLaMA-1 7Bの学習ピークメモリはLoRAの25.1GBに対してL4Qが25.4GB、通常QATは79.5GBである。

- **2024-07 · [Inference Performance Optimization for Large Language Models on CPUs](2024-2407.07304-inference-performance-optimization-for-large-language-models-on-cpus.md)**  
  実装：[✓](https://github.com/intel/xFasterTransformer) ・ リポジトリ内被引用：5  
  IntelのxFasterTransformerに、CPU向けSlimAttention、トークン・ヘッド単位のINT8 KVキャッシュ、oneCCLによる分散推論とゼロコピー通信を組み込む。Xeon 8563C環境でLlama2-70Bの次トークン遅延を2ソケット249.7msから8ソケット87.7msへ短縮した。

- **2024-11 · [TATAA: Programmable Mixed-Precision Transformer Acceleration with a Transformable Arithmetic Architecture](2024-2411.03697-tataa-programmable-mixed-precision-transformer-acceleration-with-a-trans.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  前者は8ビット整数（int8）へ量子化すると、整数積和演算器を高密度に並べたシストリック配列（systolic array）で効率よく実行できる。比較する既存FPGA研究に対してエンドツーエンド処理量最大1.45倍、DSP当たりの効率最大2.29倍、GPUとの比較ではRTX 4090に対し特定BERT条件で電力効率2.19倍を示す。

- **2024-09 · [Rotated Runtime Smooth: Training-Free Activation Smoother for accurate INT4 inference](2024-2409.20361-rotated-runtime-smooth-training-free-activation-smoother-for-accurate-in.md)**  
  実装：[✓](https://github.com/Coco58323/Rotated_Runtime_Smooth) ・ リポジトリ内被引用：3  
  大規模言語モデルの重みと活性値をともに四ビットへ量子化すれば、行列積を低精度演算器で実行でき、重みだけを圧縮する方式よりも演算費用を減らせる可能性がある。一方、論文の速度評価は主に単一の融合行列積カーネルであり、モデル全体の生成速度や電力削減を実証したものではない。

- **2024-02 · [QUICK: Quantization-aware Interleaving and Conflict-free Kernel for efficient LLM inference](2024-2402.10076-quick-quantization-aware-interleaving-and-conflict-free-kernel-for-effic.md)**  
  実装：[✓](https://github.com/SqueezeBits/QUICK) ・ リポジトリ内被引用：3  
  4ビットに量子化した大規模言語モデルでは、重みの保存容量を減らせても、行列積の際には高精度の活性値と掛け合わせるために重みを半精度へ戻す処理が必要になる。原著の行列積単体の比較ではバッチ256でAutoAWQのカーネル比1.33〜1.91倍、モデル生成の比較では最大1.94倍の処理量を報告した。

- **2024-11 · [Freeze-Omni: A Smart and Low Latency Speech-to-speech Dialogue Model with Frozen LLM](2024-2411.00774-freeze-omni-a-smart-and-low-latency-speech-to-speech-dialogue-model-with.md)**  
  実装：[✓](https://github.com/VITA-MLLM/Freeze-Omni) ・ リポジトリ内被引用：2  
  さらに、音声認識、文章生成、音声合成を独立したシステムとして直列に接続すると、応答開始までの待ち時間が積み重なる。主要結果として、音声入力によるWebQuestionsの正答率は44.73%で、同じ基盤LLMに文章を入力した45.13%と近い。

- **2024-06 · [Optimized Speculative Sampling for GPU Hardware Accelerators](2024-2406.11016-optimized-speculative-sampling-for-gpu-hardware-accelerators.md)**  
  実装：[✓](https://github.com/dwgnr/optimized-speculative-sampling) ・ リポジトリ内被引用：2  
  投機的復号では、小型のドラフトモデルが生成した複数の候補トークンを大型のターゲットモデルが並列に検証する。確率的な投機的標本化（投機的 sampling）では、ドラフト分布とターゲット分布から候補の受理確率を計算し、拒否した位置では補正分布から再標本化する。本論文は、モデルを変更せず、投機的標本化の検証・補正部分をGPU向けに再実装する。

- **2024-10 · [MatMamba: A Matryoshka State Space Model](2024-2410.06718-matmamba-a-matryoshka-state-space-model.md)**  
  実装：[✓](https://github.com/ScaledFoundations/MatMamba) ・ リポジトリ内被引用：1  
  MatMambaは最大サイズのモデルの先頭部分に小さなモデルのパラメータを含める構造を採り、複数の粒度を共同学習することで、モデルの再学習なしにサイズを選べるようにする。原著§4.1.2は計算量を55%減らしつつ、検索精度の低下を0.5%未満に抑えた例を報告する。

- **2024-10 · [FastAttention: Extend FlashAttention2 to NPUs and Low-resource GPUs](2024-2410.16663-fastattention-extend-flashattention2-to-npus-and-low-resource-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  FlashAttentionは注意重み行列をGPUの外部メモリに全量書き出さず、タイル単位の行列積とオンラインsoftmaxによって中間データの移動を抑える。

- **2024-09 · [Efficiently Dispatching Flash Attention For Partially Filled Attention Masks](2024-2409.15097-efficiently-dispatching-flash-attention-for-partially-filled-attention-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  SharmaとGeipingのBinary Block Masking（BinBlkMsk）は、FlashAttentionのブロック分割を活用し、マスクに許可要素が一つもないブロックを実行せず、許可要素を含むブロックだけを処理する方式である。

- **2024-05 · [Integer Scale: A Free Lunch for Faster Fine-grained Quantization of LLMs](2024-2405.14597-integer-scale-a-free-lunch-for-faster-fine-grained-quantization-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMの重みを小さなグループに分けて量子化すると、グループごとに異なる量子化スケールを選べるため、粗い量子化より精度を維持しやすい。原著は最大1.85倍のFP16比エンドツーエンド速度改善、浮動小数点スケールの同等カーネル比最大1.83倍などを報告する。

- **2024-04 · [The Feasibility of Implementing Large-Scale Transformers on Multi-FPGA Platforms](2024-2404.16158-the-feasibility-of-implementing-large-scale-transformers-on-multi-fpga-p.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数FPGAへ大規模モデルを展開する基盤と自動ツールを整え、I-BERTの符号器を6台のFPGAで実働させ、最新FPGAでの推定では高性能GPUに近い遅延へ届くことを示した、大規模トランスフォーマーのFPGA実装の実現可能性の検証。

- **2024-07 · [FlashNorm: Fast Normalization for Transformers](2024-2407.09577-flashnorm-fast-normalization-for-transformers.md)**  
  実装：[✓](https://github.com/OpenMachine-ai/transformer-tricks) ・ リポジトリ内被引用：0  
  RMSNormは多くのLLMで注意機構やFFNの直前に置かれ、活性ベクトルの二乗平均平方根で各要素を割り、学習済みスケールを掛ける。T4 GPUのnorm-then-project単体実験では、SmolLM2-135M相当の4096トークンで0.704msから0.468msへ、8192トークンで0.929msから0.599msへ短縮した。

- **2024-05 · [CLAQ: Pushing the Limits of Low-Bit Post-Training Quantization for LLMs](2024-2405.17233-claq-pushing-the-limits-of-low-bit-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/fayuge/CLAQ) ・ リポジトリ内被引用：0  
  CLAQ（Column-Level 適応的 重み 量子化）は、LLMの重みを2〜4bitに圧縮するとき、全ての列へ同じ量子化方式・精度を割り当てると重要な外れ値情報が失われるという問題を扱う。6課題ゼロショット平均も純2bitの43.65%から64.29%へ改善する。

- **2024-03 · [TaylorShift: Shifting the Complexity of Self-Attention from Squared to Linear (and Back) using Taylor-Softmax](2024-2403.02920-taylorshift-shifting-the-complexity-of-self-attention-from-squared-to-li.md)**  
  実装：[✓](https://github.com/tobna/TaylorShift) ・ リポジトリ内被引用：0  
  ソフトマックスの2次テイラー近似とテンソル積による再順序付けで、全トークン相互作用を保ちながら注意を線形時間化する方式を提案し、移行点の理論と実測の一致と精度低下なしを示した研究。

- **2024-02 · [Compass: A Decentralized Scheduler for Latency-Sensitive ML Workflows](2024-2402.17652-compass-a-decentralized-scheduler-for-latency-sensitive-ml-workflows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル配置を織り込むタスク配置とGPUキャッシュ管理を統合した完全分散型スケジューラで、混在する機械学習ワークフローの平均遅延をHEFTの18.0秒から2.5秒へ下げ、キャッシュヒット率99パーセントを出す。

- **2024-01 · [AutoChunk: Automated Activation Chunk for Memory-Efficient Long Sequence Inference](2024-2401.10652-autochunk-automated-activation-chunk-for-memory-efficient-long-sequence-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長系列推論で急増する活性値メモリに対し、計算グラフ上の合法なチャンク領域をチャンクフローの規則で全探索し、速度損失のコスト関数と動的計画法で最適な分割計画を選んで自動適用するコンパイラAutoChunkを提案した研究。

### 4年前（2022-12〜2023-11）

- **2023-07 · [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](2023-2307.08691-flashattention-2.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：683  
  初代FlashAttentionのオンライン・ソフトマックスとタイル分割を保ちつつ、行列積以外の演算とブロック・ワープ間の仕事分割を再設計し、A100で理論演算性能の最大73%と初代比約2倍の高速化を達成する。

- **2023-10 · [Deja Vu: Contextual Sparsity for Efficient LLMs at Inference Time](2023-2310.17157-deja-vu-contextual-sparsity-for-efficient-llms-at-inference-time.md)**  
  実装：[✓](https://github.com/FMInference/DejaVu) ・ リポジトリ内被引用：140  
  密なモデルから常に同じ重みを削除する静的枝刈りでは、入力に応じて必要な知識が変わるため、文章生成や文脈内学習の品質を損ない得る。

- **2023-11 · [FlashDecoding++: Faster Large Language Model Inference on GPUs](2023-2311.01282-flashdecoding-faster-large-language-model-inference-on-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：56  
  FlashDecoding++は、自己回帰型の大規模言語モデルで一語ずつ出力する復号段階を、GPUの演算資源とメモリ階層に合わせて高速化する推論エンジンである。論文が分離した三つの障害は、長い注意系列を分割したときの部分ソフトマックス結合同期、少数トークンを入力する細長い行列積のゼロ埋め、行列形状とGPUの種類を無視する固定実行方式である。

- **2023-09 · [Flash-LLM: Enabling Cost-Effective and Highly-Efficient Large Generative Model Inference with Unstructured Sparsity](2023-2309.10285-flash-llm-enabling-cost-effective-and-highly-efficient-large-generative-.md)**  
  実装：[✓](https://github.com/AlibabaResearch/flash-llm) ・ リポジトリ内被引用：38  
  Flash-LLMは、非構造枝刈りを施した大規模生成モデルの重みをGPUへ効率的に読み込むため、疎行列として転送し、GPU内部で密行列に戻してから行列演算器で計算する推論カーネルである。

- **2023-10 · [QUIK: Towards End-to-end 4-Bit Inference on Generative Large Language Models](2023-2310.09259-quik-towards-end-to-end-4-bit-inference-on-generative-large-language-mod.md)**  
  実装：[✓](https://github.com/IST-DASLab/QUIK) ・ リポジトリ内被引用：26  
  QUIKは、生成大規模言語モデルの線形層を重み・活性値の双方が4ビット整数であるW4A4へ移すための量子化方式である。CUTLASSによる低ビット行列積と量子化・逆量子化の融合カーネルを実装し、RTX3090の2048トークン入力一括処理でFP16比最大3.4倍の処理量改善を報告する。

- **2023-10 · [Sparse Fine-tuning for Inference Acceleration of Large Language Models](2023-2310.06927-sparse-fine-tuning-for-inference-acceleration-of-large-language-models.md)**  
  実装：[✓](https://github.com/IST-DASLab/SparseFinetuning) ・ リポジトリ内被引用：9  
  本研究は、大規模言語モデル（LLM）を高い重み疎性へ枝刈りしたうえで下流タスクへ微調整し、精度を回復する学習法と、その疎性をCPU/GPUの実際の推論高速化へ変換する実行系を一体で評価する。

- **2023-05 · [Blockwise Parallel Transformer for Large Context Models](2023-2305.19370-blockwise-parallel-transformer-for-large-context-models.md)**  
  実装：[✓](https://github.com/haoliuhl/ringattention) ・ リポジトリ内被引用：5  
  注意だけでなくFFNまで系列ブロック内で融合して学習時活性を保持しないBPT。A100/TPU v4でメモリ効率型注意より2〜4倍長い文脈を学習可能にし、1B・16Kでは通常Transformer比1.20倍の学習スループットを示す。

- **2023-10 · [Improving Computation and Memory Efficiency for Real-world Transformer Inference on GPUs](2023-dfdf93e19be2-improving-computation-and-memory-efficiency-for-real-world-transformer-i.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  系列長の裾の重い分布が生むゼロ埋めの冗長を、自己注意の有効ミニブロックだけを実行する細粒度処理とブロック配置、チャンク単位のメモリ管理で削り、モデル全体の遅延と中間結果のメモリを大きく減らす統合解法。

- **2023-07 · [QIGen: Generating Efficient Kernels for Quantized Inference on Large Language Models](2023-2307.03738-qigen-generating-efficient-kernels-for-quantized-inference-on-large-lang.md)**  
  実装：[✓](https://github.com/IST-DASLab/QIGen) ・ リポジトリ内被引用：0  
  QIGenは、量子化済みの大規模言語モデルをCPUで逐次生成するときの行列ベクトル積（GEMV）カーネルを自動生成する研究である。比率は約2.68倍だが、原著は最大約2.6倍と表現する。

- **2023-06 · [An Efficient Sparse Inference Software Accelerator for Transformer-based Language Models on CPUs](2023-2306.16601-an-efficient-sparse-inference-software-accelerator-for-transformer-based.md)**  
  実装：[✓](https://github.com/intel/intel-extension-for-transformers) ・ リポジトリ内被引用：0  
  4x1ブロック疎性とINT8を前提に、VNNI向けJIT生成SpMMカーネルでCPUの疎なトランスフォーマー推論を高速化するスタック。既存疎ライブラリを1桁上回り、密GEMM比でも最大5倍。

- **2023-02 · [The Framework Tax: Disparities Between Inference Efficiency in NLP Research and Deployment](2023-2302.06117-the-framework-tax-disparities-between-inference-efficiency-in-nlp-resear.md)**  
  実装：[✓](https://github.com/JaredFern/Framework-Tax) ・ リポジトリ内被引用：0  
  小さなバッチでは基盤のカーネル起動などの固定費が推論遅延を支配し演算量が予測指標にならないことを実測で示し、静的コンパイル型の実行環境がバッチ一で即時実行型より平均七一・三八パーセント速いことと、幅は無償で増やせる一方で深さは遅延を増やすことを明らかにした。

### 5年前（2021-12〜2022-11）

- **2022-05 · [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](2022-2205.14135-flashattention.md)**  
  実装：[✓](https://github.com/HazyResearch/flash-attention) ・ リポジトリ内被引用：943  
  タイル化、オンラインsoftmax、逆伝播時再計算により二次元注意行列の高帯域メモリ往復を避ける厳密注意カーネル。

- **2022-06 · [LUT-GEMM: Quantized Matrix Multiplication based on LUTs for Efficient Inference in Large-Scale Generative Language Models](2022-2206.09557-lut-gemm-quantized-matrix-multiplication-based-on-luts-for-efficient-inf.md)**  
  実装：[✓](https://github.com/naver-aics/lut-gemm) ・ リポジトリ内被引用：85  
  重みを3～4ビットへ圧縮すればGPUメモリへの転送量を減らせるが、既存の重みのみ量子化の多くは、積和を行う直前に重みを半精度へ展開する逆量子化処理を必要とする。

- **2022-11 · [Who Says Elephants Can't Run: Bringing Large Scale MoE Models into Cloud Scale Production](2022-2211.10017-who-says-elephants-can-t-run-bringing-large-scale-moe-models-into-cloud-.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  提案はNVIDIAの推論エンジンFasterTransformerを拡張し、専門家番号でトークンを基数ソートする経路、CUTLASSの複数行列積統合、重みだけの4/8ビット量子化を行列積の中で復号する処理、翻訳完了文をバッチから除く処理を組み合わせる。

- **2022-10 · [ByteTransformer: A High-Performance Transformer Boosted for Variable-Length Inputs](2022-2210.03052-bytetransformer-a-high-performance-transformer-boosted-for-variable-leng.md)**  
  実装：[✓](https://github.com/bytedance/ByteTransformer) ・ リポジトリ内被引用：8  
  ByteTransformerは、バッチに混在する長さの異なる文章をBERT系のTransformerへ入力する際、最長文章に合わせたゼロ埋め（padding）で発生する計算とGPUメモリ転送の無駄を削減する推論実装である。論文の重要性は、入力の有効トークンだけを扱う表現と、注意計算の実行形態を一体で設計した点にある。

### 6年前（2020-12〜2021-11）

- **2021-02 · [TurboTransformers: An Efficient GPU Serving System For Transformer Models](2021-2010.05680-turbotransformers-an-efficient-gpu-serving-system-for-transformer-models.md)**  
  実装：[✓](https://github.com/Tencent/TurboTransformers) ・ リポジトリ内被引用：38  
  提案システムは、GEMM（行列積）間の演算融合とSoftmax・LayerNormの並列縮約、系列長を受け取ってから行う中間領域の再利用、実測コストを使う動的計画法による要求バッチ分割を組み合わせる。

- **2021-03 · [Random Feature Attention](2021-2103.02143-random-feature-attention.md)**  
  実装：[✓](https://github.com/haopeng-nlp/transformer-rfa) ・ リポジトリ内被引用：22  
  本論文が扱うのは、標準的な指数正規化注意（softmax 注意機構）において、各質問ベクトルが過去のすべての鍵ベクトルと内積を計算するため、自己回帰復号で生成長が増すほど注意処理が重くなる問題である。

- **2021-06 · [LightSeq: A High Performance Inference Library for Transformers](2021-439132b7c6e4-lightseq-a-high-performance-inference-library-for-transformers.md)**  
  実装：[✓](https://github.com/bytedance/lightseq) ・ リポジトリ内被引用：4  
  一方、推論の律速が行列積そのものではなく周辺処理へ移るというシステム上の問題を、具体的なカーネル構成と実測で説明した基礎的な実装研究である。

### 7年前（2019-12〜2020-11）

- **2020-10 · [LightSeq: A High Performance Inference Library for Transformers](2020-2010.13887-lightseq-a-high-performance-inference-library-for-transformers.md)**  
  実装：[✓](https://github.com/bytedance/lightseq) ・ リポジトリ内被引用：23  
  LightSeqは、Transformerの推論を汎用学習フレームワークから直接実行するときに生じる多数の小規模GPU演算、自己回帰探索の不要な候補処理、可変長系列に伴うメモリ割当を、推論専用のCUDA実装で削減するライブラリである。2020年に公開された研究であり、後年の大規模言語モデル提供基盤を直接評価したものではない。中核は三つの独立した最適化である。

- **2020-09 · [Real-Time Execution of Large-scale Language Models on Mobile](2020-2009.06823-real-time-execution-of-large-scale-language-models-on-mobile.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本論文は、モデル構造の探索とモバイル実行コンパイラの最適化を同一ループに入れることを提案する。Galaxy S20の系列長128の分類推論では、元のBERT-baseがCPU 257ms／GPU 186msであるのに対し、著者らの蒸留・NAS済みBERTはCPU 49ms／GPU 45msとなる。

### 8年前（2018-12〜2019-11）

- **2019-06 · [Triton: An Intermediate Language and Compiler for Tiled Neural Network Computations](2019-triton-an-intermediate-language-and-compiler-for-tiled-neural-network-computations.md)**  
  実装：[✓](https://github.com/triton-lang/triton) ・ リポジトリ内被引用：227  
  深層学習の演算を高速なGPUカーネルにするには、数式を記述するだけでは足りない。入力配列のどの部分をまとめて読み出し、何回再利用し、どのスレッドに配り、いつ共有メモリへ移すかによって性能が大きく変わる。既存のcuBLASやcuDNNが対象とする標準演算なら高性能な実装を利用できるが、新しい行列演算や不規則な参照を伴う演算では、そのまま使えない。

- **2019-10 · [Structured Pruning of Large Language Models](2019-1910.04732-structured-pruning-of-large-language-models.md)**  
  実装：[✓](https://github.com/asappresearch/flop) ・ リポジトリ内被引用：60  
  FLOP（Factorized Low-rank Pruning、因子化低ランク枝刈り）は、重みを個別にゼロ化する非構造的な枝刈りでは、パラメータ数を減らしても一般的な計算装置で速度が上がりにくいという問題に取り組む。

### 9年前（2017-12〜2018-11）

- **2018-05 · [Online normalizer calculation for softmax](2018-1805.02867-online-normalizer-calculation-for-softmax.md)**  
  実装：[✓](https://github.com/NVIDIA/online-softmax) ・ リポジトリ内被引用：81  
  本論文は、数値的に安全なソフトマックスの出力を変えずに、入力配列を読み直す回数を減らす「オンライン正規化子（online normalizer）」を提案する。著者らのTesla V100での単精度実装では、ソフトマックス単体で最大約1.3倍の高速化が報告される。
<!-- survey:auto:end -->
