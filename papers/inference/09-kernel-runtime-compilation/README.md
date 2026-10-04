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
## 自動生成の論文一覧（48本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-12 · [MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs](2025-2512.22219-mirage-persistent-kernel-mega-kernel-runtime.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：9  
  演算子単位の多数カーネル起動をSM粒度の依存グラフへ分解し、単一常駐巨大カーネル内の分散スケジューラで演算・通信・タスク間パイプラインを重ね、vLLM/SGLang比で最大1.7倍の推論遅延改善を示す。

- **2026-01 · [FlashInfer-Bench: Building the Virtuous Cycle for AI-driven LLM Systems](2026-2601.00227-flashinfer-bench-ai-driven-kernel-deployment.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  実LLM serving由来のGPUカーネル課題を統一トレースで検証し、エージェント生成カーネルをSGLang/vLLMへ低オーバーヘッドで動的適用する閉ループ基盤。

- **2026-04 · [Event Tensor: A Unified Abstraction for Compiling Dynamic Megakernel](2026-2604.13327-event-tensor-dynamic-megakernel-generation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  タイル依存関係を記号形状のイベントテンソルとして表し、可変形状とMoEのデータ依存分岐を再コンパイルせず静的・動的メガカーネルへ変換するコンパイラ抽象。

- **2026-02 · [PackInfer: Compute- and I/O-Efficient Attention for Batched LLM Inference](2026-2602.06072-packinfer-batched-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  異種長要求を負荷均衡した群へ詰め、共有接頭辞を考慮した連続KV配置と一体化することで、注意計算の無駄と入出力断片化を同時に削減する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [Unfolding the Leech Lattice: Fused Multi-Shell Decoding and VRAM Layouts for 2-Bit LLM Weights](2026-2609.02652-unfolding-the-leech-lattice-fused-multi-shell-decoding-and-vram-layouts-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  2-bit級のLLM重み量子化では、ディスク上のbit数だけ小さくても、GPUが各重みを復号するための符号表や補助ストリームが大きければ、実際のデコードは速くならない。一方、融合カーネルによりFP16より小さい転送量を活かし、4B、8B、14Bモデルでエンドツーエンド 1.11倍、1.29倍、1.41倍を報告する。

- **2026-09 · [AttnFuse: A Composable DSL for Compiling Attentions to Fused GPU Kernels](2026-2609.13612-attnfuse-a-composable-dsl-for-compiling-attentions-to-fused-gpu-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  新しい注意方式を提案しても、実用速度を得るには専用GPUカーネルを書く必要がある。RTX 3090のRoPE付き因果注意では柔軟注意に対して2.10倍高速化し、H100ではLlama-3-8Bの訓練ステップをPyTorchの手調整済み後端との差5%以内で実行した。

- **2026-09 · [Accelerating the Mitigation of LLM Inference Nondeterminism Across GPU Architectures](2026-2609.25624-accelerating-the-mitigation-of-llm-inference-nondeterminism-across-gpu-a.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BF16重みをレジスタ内FP32化し固定順序のIEEE-754 FMAで積算するTriton GEMMにより、GPU世代を跨ぐbitwise再現性と既存対策比1.17〜3.1倍の推論高速化を両立する。

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

- **2026-06 · [Approaching Shannon Bound with Lossless LLM Weight Compression](2026-2606.15789-shannon-bound-lossless-weight-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GEMMタイルごとにANSで重みを損失なく圧縮し、共有メモリへ復号しながらテンソルコア計算と重ねることで、Mixtral-176Bの最大バッチを20から95へ増やし、SGLangスループットを最大1.6倍にする。

- **2026-06 · [AgentCompile: An LLM-Guided Compiler for Direct CUDA Inference](2026-2606.07665-agentcompile-llm-guided-direct-cuda-inference.md)**  
  実装：[✓](https://github.com/veneno1213822/AgentCompile) ・ リポジトリ内被引用：0  
  大規模言語モデルによるCUDA生成をコンパイラ契約・数値検証・実測性能選択で囲い込み、合格した復号カーネルだけを採用して既存実装へ安全にフォールバックできる推論コンパイラ。

- **2026-06 · [Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices](2026-2607.08786-moderately-unstructured-sparse-gpu-inference.md)**  
  実装：[✓](https://github.com/moui0/cudac) ・ リポジトリ内被引用：0  
  約50%の非構造疎重みを2:4疎テンソルコア層・差分距離で再配置する補助層・微小残差層へ分解し、疎テンソルコアとCUDAコアを重ねて実行してSpInfer比最大1.64倍を達成する。

- **2026-05 · [GPU Forecasters: Language Models as Selective Surrogates for Kernel Runtime Optimization](2026-2605.31464-gpu-forecasters-kernel-runtime-surrogates.md)**  
  実装：[✓](https://github.com/codezakh/gpu-forecasters) ・ リポジトリ内被引用：0  
  実GPU計測をLLMの相対速度予測で選択的に代替し、同じGPU計測予算で候補数を4倍へ広げて6課題中4課題で基準と同等以上の高速カーネルを発見する。

- **2026-05 · [Ada-MK: Adaptive MegaKernel Optimization via Automated DAG-based Search for LLM Inference](2026-2605.11581-ada-mk-adaptive-megakernel-compilation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Ada-MKはLLMデコードをPTX命令水準の依存グラフへ分解し、共有メモリ配置とワープ役割をオフライン探索して分岐のないメガカーネルを生成し、L20でTensorRT-LLM比最大23.6%高速化する。

- **2026-04 · [Hybrid JIT-CUDA Graph Optimization for Low-Latency Large Language Model Inference](2026-2604.23467-hybrid-jit-cuda-graph-low-latency-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  静的Transformer演算をCUDA Graph再生、動的制御を実行時コンパイルへ分け、短系列・バッチ1推論の起動オーバーヘッドと尾部遅延を削減する。

- **2026-03 · [Model2Kernel: Model-Aware Symbolic Execution For Safe CUDA Kernels](2026-2603.24595-model2kernel-safe-cuda-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モデル側からCUDA呼出し条件を抽出するHFProbeと、動的テンソル・全CUDAスレッドを記号化するcuKLEEを組み合わせ、LLM推論カーネルの未知メモリバグ353件を9誤検出で検出した。

- **2026-03 · [Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts](2026-2603.07169-cudamaster-multi-scenario-kernel-optimization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  50演算×FP32/BF16のMSKernelBenchと、律速別に選別したNsight Compute情報を計画・実装・コンパイル・デバッグの4担当へ渡すCUDAMasterで、多領域CUDA最適化を自動化し、o4-miniで正当性100%・基準超え94%を達成する。

- **2026-02 · [Deep Kernel Fusion for Transformers](2026-2602.11808-deep-kernel-fusion-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SwiGLU前半を単一CUDAカーネルへ深く融合して中間活性のHBM往復を削減し、事前プロファイルでGPU・バッチ別のタイル方式を選んでSGLangのデコードを最大13.2%高速化する。

### 2年前（2024-11〜2025-10）

- **2025-03 · [POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference](2025-pod-attention.md)**  
  実装：[✓](https://github.com/microsoft/vattention/tree/main/pod_attn) ・ リポジトリ内被引用：27  
  プリフィルとデコードの注意を同一SMで並行実行するSM認識型GPUカーネルにより、注意計算を平均28%、サービング処理量を最大22%改善する。

- **2024-12 · [Flex Attention: A Programming Model for Generating Optimized Attention Kernels](2024-2412.05496-flexattention-a-programming-model-for-generating-optimized-attention-kernels.md)**  
  実装：[✓](https://github.com/pytorch/pytorch) ・ リポジトリ内被引用：12  
  高速な融合注意カーネルを「注意変種ごとに手書きする」方式から、利用者が意味だけを書きコンパイラが高速カーネルへ落とす方式へ変える。

- **2025-04 · [Triton-distributed: Programming Overlapping Kernels on Distributed AI Systems with the Triton Compiler](2025-2504.19442-triton-distributed.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/Triton-distributed) ・ リポジトリ内被引用：8  
  OpenSHMEM通信をTritonへ統合し、計算・通信・メモリアクセスをPythonから細粒度に重ね合わせ、8〜64 GPUで分散カーネルを高速化するコンパイラ拡張。

- **2025-10 · [KTransformers: Unleashing the Full Potential of CPU/GPU Hybrid Inference for MoE Models](2025-b4e11ada8105-ktransformers-unleashing-the-full-potential-of-cpu-gpu-hybrid-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  この疎性は、注意や共有専門家をGPUに置き、多数のrouted 専門家を大容量CPUメモリへ置く混成推論と相性がよい。しかし単純なオフロードではCPU側の小さな行列演算が遅く、MoE層の結果を待つ間GPUが停止するため、PCIe転送だけでなくCPU計算と同期が律速になる。

- **2025-04 · [TileLang: A Composable Tiled Programming Model for AI Systems](2025-2504.17577-tilelang-a-composable-tiled-programming-model-for-ai-systems.md)**  
  実装：[✓](https://github.com/tile-ai/tilelang) ・ リポジトリ内被引用：7  
  GPUカーネルの「何を計算するか」をタイル単位のデータ流として書き、「どのスレッドがどの配置で、どの命令を使い、転送と計算をどう重ねるか」を別のスケジュール層へ分離する。高水準な記述を保ちながら、FlashAttention-3級の複雑なパイプラインまで表現・自動推論できることを狙う。

- **2025-03 · [Medusa: Accelerating Serverless LLM Inference with Materialization](2025-8c4404f09758-medusa-accelerating-serverless-llm-inference-with-materialization.md)**  
  実装：[✓](https://github.com/thustorage/Medusa) ・ リポジトリ内被引用：7  
  KV容量プロファイルとCUDAグラフをオフライン物化し、割当順序索引とカーネル再解決で別インスタンスへ復元してサーバーレスLLMのコールドスタートを短縮する。

- **2025-06 · [FlashMoE: Fast Distributed MoE in a Single Kernel](2025-2506.04667-flashmoe-fast-distributed-moe-in-a-single-kernel.md)**  
  実装：[✓](https://github.com/osayamenja/FlashMoE) ・ リポジトリ内被引用：5  
  分散MoE全体を単一の常駐GPUカーネルへ融合し、装置起点通信とタイル単位スケジューリングでCPU起動・同期待ちを除き、8基H100で最大6.4倍の遅延改善と5.7倍のスループットを示す。

- **2025-03 · [TileLink: Generating Efficient Compute-Communication Overlapping Kernels using Tile-Centric Primitives](2025-2503.20313-tilelink-generating-efficient-compute-communication-overlapping-kernels-using-tile-centric-primitives.md)**  
  実装：[✓](https://github.com/ByteDance-Seed/Triton-distributed) ・ リポジトリ内被引用：5  
  タイル中心プリミティブから計算・通信融合カーネルを生成し、8×H800で非重畳比1.17〜20.76倍、8モデルのエンドツーエンドでPyTorch比平均1.32倍を達成する。

- **2025-09 · [Towards Robust Agentic CUDA Kernel Benchmarking, Verification, and Optimization](2025-2509.14279-towards-robust-agentic-cuda-kernel-benchmarking-verification-and-optimization.md)**  
  実装：[✓](https://github.com/SakanaAI/robust-kbench) ・ リポジトリ内被引用：3  
  固定入力などを悪用した「高速だが一般化しないCUDA」を弾くrobust-kbenchと、翻訳・LLM検証・進化的最適化を統合したエージェントを提案し、KernelBenchの見かけの平均3.13倍高速化が堅牢化後1.49倍へ下がることを示す。

- **2025-09 · [Astra: A Multi-Agent System for GPU Kernel Performance Optimization](2025-2509.07506-astra-a-multi-agent-system-for-gpu-kernel-performance-optimization.md)**  
  実装：[✓](https://github.com/Anjiang-Wei/Astra) ・ リポジトリ内被引用：3  
  高水準PyTorchからCUDAを一から生成するのではなく、SGLangに既に存在する正しいCUDAカーネルを出発点にし、試験・プロファイル・計画・実装を別々の大規模言語モデル（Large Language モデル; LLM）エージェントへ分担する。

- **2025-04 · [70% Size, 100% Accuracy: Lossless LLM Compression for Efficient GPU Inference via Dynamic-Length Float (DFloat11)](2025-2504.11651-70-size-100-accuracy-lossless-llm-compression-for-efficient-gpu-inferenc.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  DFloat11は量子化ではなく、BFloat16重みの情報エントロピーを利用する可逆圧縮方式である。

- **2025-10 · [lm-Meter: Unveiling Runtime Inference Latency for On-Device Language Models](2025-2510.06126-lm-meter-unveiling-runtime-inference-latency-for-on-device-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末内LLMでは、GPUのピーク性能だけでなく動的周波数制御、熱、限られたメモリ、閉じたGPUドライバが実行時間を左右する。しかし通常のアプリケーション側計測は推論全体しか見えず、オフラインGPUプロファイラは外部ホストへのログ転送や後処理を必要とする。

### 3年前（2023-11〜2024-10）

- **2024-04 · [PyTorch 2: Faster Machine Learning Through Dynamic Python Bytecode Transformation and Graph Compilation](2024-d5ec11366816-pytorch-2-faster-machine-learning-through-dynamic-python-bytecode-transf.md)**  
  実装：[✓](https://github.com/pytorch/pytorch) ・ リポジトリ内被引用：20  
  Pythonの即時実行の柔軟性を残して演算グラフを実行時に取り出し、TritonやC++へコンパイルする仕組みを設計・評価した。

- **2024-06 · [S-LoRA: Serving Thousands of Concurrent LoRA Adapters](2024-2311.03285-s-lora-serving-thousands-of-concurrent-lora-adapters.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  しかしサービングでは、アダプタ数が増えるほど「小さいから全部GPUへ置く」という前提が崩れ、異なるrank・異なる要求長のアダプタとKVキャッシュがGPUメモリを断片化する。スケジューラが実行する要求に必要なアダプタだけをGPUへ取り込み、LoRA重みとKVキャッシュをUnified Pagingで統合管理する。

- **2024-05 · [Mirage: A Multi-Level Superoptimizer for Tensor Programs](2024-2405.05751-mirage-a-multi-level-superoptimizer-for-tensor-programs.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：6  
  Mirageは「既知のアルゴリズムに対して良いGPUスケジュールを探す」だけでも、「数式を書き換えて既存カーネルを組み合わせる」だけでもない。テンソル計算をGPUのカーネル・スレッドブロック・スレッド階層をまたぐμGraphで表し、数式の形、融合境界、並列化方法を同じ探索の中で変えることで、人手では実装量が大きい複合最適化を自動発見する。

- **2024-10 · [ThunderKittens: Simple, Fast, and Adorable AI Kernels](2024-2410.20399-thunderkittens-simple-fast-and-adorable-ai-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  AI演算をGPUへ効率良く写像するには、共有メモリ配置、テンソル Core命令、非同期コピー、ワープ間同期などを同時に調整する必要がある。ThunderKittens（TK）は、GPUの階層そのものに合わせた少数の抽象化へ設計を絞り、記述量を抑えながら高性能を得る枠組みである。

- **2024-05 · [LeanAttention: Hardware-Aware Scalable Attention Mechanism for the Decode-Phase of Transformers](2024-2405.10480-lean-attention-hardware-aware-scalable-attention-mechanism.md)**  
  実装：[✓](https://github.com/microsoft/onnxruntime) ・ リポジトリ内被引用：4  
  LeanAttentionが減らすのは注意の数学的な計算量ではない。まったく同じ厳密注意を、長いKV文脈方向へ細かく分割し、GPUの全SMへ端数なく近い形で仕事を割り振る。デコードでは問い合わせが1トークンしかないため従来のタイル並列性が不足する、というハードウェア利用率の問題を解く。

- **2024-02 · [Any-Precision LLM: Low-Cost Deployment of Multiple, Different-Sized LLMs](2024-2402.10517-any-precision-llm-low-cost-deployment-of-multiple-different-sized-llms.md)**  
  実装：[✓](https://github.com/SNU-ARC/any-precision-llm) ・ リポジトリ内被引用：3  
  実運用では、同じ能力系列でも低遅延用・高品質用の複数モデルを切り替えたり、投機的復号で小型ドラフトと大型対象モデルを同時常駐させたりする。

- **2024-09 · [CHESS: Optimizing LLM Inference via Channel-Wise Thresholding and Selective Sparsification](2024-2409.01366-chess-optimizing-llm-inference-via-channel-wise-thresholding-and-selecti.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  活性疎化は小さい中間値をゼロにし、後続行列積で対応する演算を省く。しかしLLMのFFNではチャネルごとに活性分布と後段重みへの影響が異なり、全チャネルへ同じ閾値を置くと「値は小さいが出力へ重要」な成分まで落とす。注意層もQ/K/V/O投影を同じように疎化すると品質感度が異なる。

- **2024-07 · [Inference Performance Optimization for Large Language Models on CPUs](2024-2407.07304-inference-performance-optimization-for-large-language-models-on-cpus.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  KVキャッシュ削減、oneCCL分散通信、CPU命令・モデル別カーネル最適化をxFasterTransformerへ統合し、GPUなしのLLM推論を実用化する。

### 4年前（2022-11〜2023-10）

- **2023-09 · [Flash-LLM: Enabling Cost-Effective and Highly-Efficient Large Generative Model Inference with Unstructured Sparsity](2023-2309.10285-flash-llm-enabling-cost-effective-and-highly-efficient-large-generative-.md)**  
  実装：[✓](https://github.com/AlibabaResearch/flash-llm) ・ リポジトリ内被引用：15  
  非構造疎重みをHBMから圧縮状態で読み、オンチップで密タイルへ復元してテンソル Coreの余剰演算力を使うことで、LLM生成の重み帯域律速を削る。

- **2022-11 · [Who Says Elephants Can't Run: Bringing Large Scale MoE Models into Cloud Scale Production](2022-2211.10017-who-says-elephants-can-t-run-bringing-large-scale-moe-models-into-cloud-.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  しかし推論では、巨大な専門家重みをGPUへ置く容量問題、ルータ出力に従ってトークンを専門家別に並べ替える費用、専門家ごとの小さく不均一な行列積によるGPU利用率低下が生じる。本論文はこれらを一つの推論エンジンで処理し、専門家の重みを4ビット整数へ量子化して容量・帯域を減らす。

- **2023-05 · [Blockwise Parallel Transformer for Large Context Models](2023-2305.19370-blockwise-parallel-transformer-for-large-context-models.md)**  
  実装：[✓](https://github.com/haoliuhl/ringattention) ・ リポジトリ内被引用：2  
  注意だけでなくFFNまで系列ブロック内で融合して学習時活性を保持しないBPT。A100/TPU v4でメモリ効率型注意より2〜4倍長い文脈を学習可能にし、1B・16Kでは通常Transformer比1.20倍の学習スループットを示す。

- **2023-10 · [Sparse Fine-tuning for Inference Acceleration of Large Language Models](2023-2310.06927-sparse-fine-tuning-for-inference-acceleration-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  この研究は、LLMの重みを疎にするだけでは実際の高速化にならないという問題を、精度回復と実行系の両側から扱う。T5翻訳、Whisper音声翻訳にも対象を広げ、疎性と量子化の併用も検証する点が、単なる枝刈り精度論文との差である。

### 5年前（2021-11〜2022-10）

- **2022-06 · [LUT-GEMM: Quantized Matrix Multiplication based on LUTs for Efficient Inference in Large-Scale Generative Language Models](2022-2206.09557-lut-gemm-quantized-matrix-multiplication-based-on-luts-for-efficient-inf.md)**  
  実装：[✓](https://github.com/naver-aics/lut-gemm) ・ リポジトリ内被引用：23  
  重みのみを3～4ビットへ量子化するとメモリ転送量は減るが、多くの既存GPU実装は行列積の直前に低ビット重みをFP16へ戻す逆量子化を行う。OPT-175Bの3ビット量子化では、逆量子化を行うOPTQ実装に対して生成遅延を約2.1倍高速化した。

### 7年前（2019-11〜2020-10）

- **2020-10 · [LightSeq: A High Performance Inference Library for Transformers](2020-2010.13887-lightseq-a-high-performance-inference-library-for-transformers.md)**  
  実装：[✓](https://github.com/bytedance/lightseq) ・ リポジトリ内被引用：8  
  モデルが大きくても、特に小バッチや自己回帰復号ではカーネル起動とGPUメモリ往復が相対的に大きくなり、理論FLOPsほどGPUを使い切れない。中心機構は三つある。標準機械翻訳ベンチマークではTensorFlow実装に対して最大14倍、同時期のCUDA専用FasterTransformerに対して最大1.4倍の高速化を報告する。

### 8年前（2018-11〜2019-10）

- **2019-06 · [Triton: an intermediate language and compiler for tiled neural network computations](2019-triton-an-intermediate-language-and-compiler-for-tiled-neural-network-computations.md)**  
  実装：[✓](https://github.com/triton-lang/triton) ・ リポジトリ内被引用：46  
  CUDAのスレッド単位ではなく、静的形状の多次元部分配列「タイル（tile）」をプログラムの基本単位にする。Triton-C→Triton-IR→Triton-JITのコンパイル経路で、メモリ合体アクセス、共有メモリ利用、タイル階層化などをコンパイラへ移し、GTX 1070上の行列積ではcuBLASと概ね同等、一部でデバイスピークの90%以上を達成する。
<!-- survey:auto:end -->
