<!-- survey:auto:start -->
## 自動生成の論文一覧（18本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-12 · [MPK: A Compiler and Runtime for Mega-Kernelizing Tensor Programs](2025-2512.22219-mirage-persistent-kernel-mega-kernel-runtime.md)**  
  実装：[✓](https://github.com/mirage-project/mirage) ・ リポジトリ内被引用：7  
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

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-08 · [UnionSparse: An Index-Efficient Sparsity Framework for Low-Bit Sparse LLM Inference on Edge](2026-2608.09291-unionsparse-index-efficient-low-bit-sparse-inference.md)**  
  実装：[✓](https://github.com/Victor-Alen/UnionSparse) ・ リポジトリ内被引用：0  
  低ビット化で相対的に増える疎行列の位置情報負担をPMRで定量化し、共有ビットマップ表現と並列復号カーネルを共同設計してJetson上の小バッチ疎推論を高速化する。

- **2026-08 · [MonoMoE: An Efficient Fused Mega-kernel for Quantized MoE Decoding](2026-2609.04244-monomoe-fused-megakernel-quantized-moe-decoding.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer/tree/main/csrc/fused_moe/monomoe) ・ リポジトリ内被引用：0  
  少トークンMoE復号を重み主導型の常駐巨大カーネルへ再構成し、ルーティングから二段の専門家射影と縮約までを融合してメモリ帯域利用を高める。

- **2026-08 · [Celty: SpMspV GPU Kernel and SIMT Co-Design for Efficient Dual-Sparse LLM Inference](2026-2608.01536-celty-dual-sparse-gpu-kernel.md)**  
  実装：[✓](https://github.com/RuokaiYin/Celty) ・ リポジトリ内被引用：0  
  重み疎性と実行時活性疎性の交差を疎行列×疎ベクトルとして扱い、走長圧縮形式、ワープ割当、レジスタ部分和、専用復号器を共同設計して低バッチLLMデコードを高速化する。

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

### 2年前（2024-10〜2025-09）

- **2025-03 · [POD-Attention: Unlocking Full Prefill-Decode Overlap for Faster LLM Inference](2025-pod-attention.md)**  
  実装：[✓](https://github.com/microsoft/vattention/tree/main/pod_attn) ・ リポジトリ内被引用：14  
  プリフィルとデコードの注意を同一SMで並行実行するSM認識型GPUカーネルにより、注意計算を平均28%、サービング処理量を最大22%改善する。
<!-- survey:auto:end -->
