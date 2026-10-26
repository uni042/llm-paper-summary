# Weight Quantization / Compression

一般LLMの重み表現を低ビット量子化、ベクトル量子化、疎量子化、無損失符号化などで小さくし、モデル品質を保ちながら重み容量・帯域・演算費用を削減する研究をまとめる。

## 分類境界

主要貢献が一般LLMのweight quantization、weight compression、mixed/sparse quantized representation、lossless weight codingである研究を含め、KV cache圧縮、MoE expert固有圧縮、単なる量子化カーネル実装だけが主貢献の研究は含めない。

### 含める研究

- post-training weight quantization
- 低ビット／ベクトル／疎量子化表現
- 重みの無損失圧縮と復元

### 含めない研究

- KV cache量子化・圧縮
- MoE expert固有の量子化・pruning
- 量子化方式を変えないカーネル最適化

## 近傍系統

- [06-moe-quantization-compression](../06-moe-quantization-compression/)
- [09-kernel-runtime-compilation](../09-kernel-runtime-compilation/)
- [08-edge-on-device-llm-systems](../08-edge-on-device-llm-systems/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（110本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/16-weight-quantization-compression/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  BF16重みの指数を固定長ビットマップへ無損失符号化し、圧縮データをレジスタ上で復元してテンソル Coreへ直送することで、重み帯域と中間展開の読み書きを減らす。

- **2026-06 · [MosaicQuant: Inlier–Outlier Disaggregation for Unified 4-Bit LLM Quantization](2026-2606.15652-mosaicquant-inlier-outlier-disaggregation-for-unified-4-bit-llm-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの行列演算を高速化するため、重みと活性値を低ビット化するとメモリ転送量と演算費用を減らせる。従来の混合精度方式は外れ値のあるチャネルや低ランク成分を8～16ビットで保持するが、別精度の行列演算や変換・転送が発生し、低ビットの演算器を一貫して使う利点が減る。

- **2026-06 · [LiftQuant: Continuous Bit-Width LLM via Dimensional Lifting and Projection](2026-2606.04050-liftquant-continuous-bit-width-llm-via-dimensional-lifting-and-projectio.md)**  
  実装：[✓](https://github.com/Heliulu/LiftQuant) ・ リポジトリ内被引用：1  
  LLMの重み量子化はGPUメモリ消費を減らす有力な方法だが、多くの方式は2ビット、3ビット、4ビットといった整数の量子化幅を単位にする。たとえば70Bモデルの3ビット版が24GBのGPUへ収まらず、2ビット版なら大きな余裕が残る場合、空いた容量を精度向上へ使いにくい。

- **2026-05 · [HARP: Hadamard-Preconditioned Adaptive Rotation Processor for Extreme LLM Quantization](2026-2605.29843-harp-hadamard-preconditioned-adaptive-rotation-processor-for-extreme-llm.md)**  
  実装：[✓](https://github.com/brain-lab-research/HARP) ・ リポジトリ内被引用：1  
  重みを2～4ビットへ圧縮する事後量子化（Post-学習 量子化; PTQ）では、少数の大きな外れ値や入力方向ごとに異なる誤差感度のため、単純な丸めが深刻な品質劣化を招く。

- **2026-01 · [What Makes Low-Bit Quantization-Aware Training Work for Reasoning LLMs? A Systematic Study](2026-2601.14888-what-makes-low-bit-quantization-aware-training-work-for-reasoning-llms-a.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  数学やコード生成を得意とする推論特化型の大規模言語モデルでは、低ビット量子化が通常の自然言語課題より大きな品質低下を引き起こすことがある。Qwen3-0.6Bの重み3ビット・群サイズ128の設定では、MATH-500正答率がGPTQの13.27%からReasoning-QATの57.80%へ改善した。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [RapidMoE: Exploiting Cross-Asymmetry via Adaptive Residual Offloading for Large-Scale MoE Inference](2026-2610.01265-rapidmoe-exploiting-cross-asymmetry-via-adaptive-residual-offloading-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  たとえばDeepSeek-R1は671Bパラメータのうち約37Bを活性化するが、FP16重みをGPU VRAMへ格納するには700GB超を要する。単一ノードのCPU–GPU混在機では、GPUに置けない専門家をPCIe経由で都度転送する方式は転送遅延が律速になり、専門家計算自体をCPUへ寄せる方式はCPU側へ仕事が集中してGPUを十分使えない。

- **2026-09 · [Why Does Post-Training Quantization Work?](2026-2609.11716-why-does-post-training-quantization-work.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の重みを学習後に4ビットへ量子化すると、各線形層の重みが元の値からずれる。Qwen3-32Bの第1〜48層では、この相互作用がブロック更新誤差の二乗ノルムの累積寄与の50.2%を相殺した。

- **2026-09 · [Vortex: Bridging Extreme Compression and Efficient LLM Inference](2026-2609.12208-vortex-bridging-extreme-compression-and-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  超低ビットベクトル量子化と入力依存疎性を二種類の実行流へ合わせ、圧縮率を実際の推論高速化へ変換する加速器。

- **2026-09 · [VLAQuantBench: Closed-Loop Evaluation of Post-Training Quantization for Vision-Language-Action Models](2026-2609.25376-vlaquantbench.md)**  
  実装：[✓](https://github.com/jiuyixu25/VLAQuantBench) ・ リポジトリ内被引用：0  
  VLAQuantBenchは、視覚・言語・行動モデル（Vision-Language-Action モデル、VLA）の学習後量子化（Post-学習 量子化、PTQ）を、重みの再構成誤差だけでなく、ロボットが環境を動かし続けた結果のタスク成功率で検証する評価基盤である。

- **2026-09 · [Structured Transforms for Low-Overhead Quantization of Language Models](2026-2609.11687-structured-transforms-for-low-overhead-quantization-of-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Kashin分解を利用した大規模言語モデルの学習後量子化（post-学習 量子化）について、量子化前処理が遅いこと、因子分布が不安定なこと、数値的に収束しない層があることを同時に解決しようとする。

- **2026-09 · [Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution](2026-2609.09240-scaling-post-training-ternarisation-to-qwen3-8b-capability-retention-reproduction-lossless-packing-and-packed-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-8Bを適応的約1.64 bit/重みへ後量子化し、78.5%の補正済み能力保持、8.24 GiBの無損失packed artifact、RTX 5070上15.52 トークン/s・7.35 GiBの直接実行まで検証する。

- **2026-09 · [Predict Before You Deploy: Offline Prediction of Quantization-Induced Task Degradation for World Action Models](2026-2609.19441-prede-quantization-task-degradation-prediction.md)**  
  実装：[✓](https://github.com/jiuyixu25/PreDE) ・ リポジトリ内被引用：0  
  PreDE（Predict Before You Deploy）は、世界行動モデル（World Action モデル、WAM）を学習後量子化したとき、候補ごとに高価な閉ループ試験を行う前に、タスク成功率の劣化を「受理・棄却・保留」の三値で予測する方式である。

- **2026-09 · [FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators](2026-2609.04724-flexposit-tunable-fractional-precision-for-llm-inference-accelerators.md)**  
  実装：[✓](https://github.com/hplp/FlexPosit) ・ リポジトリ内被引用：0  
  LLMの重み量子化には、精度を保つために細かいグループごとに倍率を持つ方式と、ハードウェア実装しやすいチャネル単位の方式がある。

- **2026-09 · [Faster Block-Diffusion Serving with Distribution-Free Risk Guarantees](2026-2609.33887-faster-block-diffusion-serving-with-distribution-free-risk-guarantees.md)**  
  実装：[✓](https://github.com/js-lee-AI/Redline) ・ リポジトリ内被引用：0  
  高速設定ほど未確定なトークンを早く確定する傾向があり、正答率の低下が問題になる。提案方式Redlineは、候補となる複数の推論設定を較正用の質問集合で実行し、基準設定が正解し候補設定が不正解となる件数を数える。

- **2026-09 · [All for 1-Bit: Towards Genuine 1-Bit Post-Training Quantization for LLMs](2026-2609.06161-all-for-1-bit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  All for 1-Bit（AF1）は、既存の「1ビット」学習後量子化が尺度、外れ値、グループ情報などの補助データを含めると実効2〜4ビット/重みへ膨らむ問題に対し、対象線形重みを実効1.0ビット/重みに収める学習後量子化方式である。

- **2026-08 · [SchurQuant: Groupwise Discrete Optimization for Layer-Wise LLM Quantization](2026-2608.15567-schurquant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを4ビットから2〜3ビットへ縮めると、量子化格子の段数が少なくなり、各層の誤差が累積して言語モデルの予測を壊す。Llama2、Llama3、Qwen3の計8モデルを比較した2ビットの六課題平均ゼロショット精度は、SchurQuantが50.83%、GPTQが39.25%、QEPが41.18%である。

- **2026-08 · [SandwichQuant: Which Parameters Matter Before and After Quantization?](2026-2608.24173-sandwichquant-which-parameters-matter-before-and-after-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事後量子化（Post-学習 量子化; PTQ）の品質を回復する研究では、重み、量子化尺度、丸め、局所再構成などを調整する。Llama2-7B、Llama3-8B、Qwen3-8Bなどの強い量子化条件で一貫して改善し、Llama2-7BのW2A4KV4条件では比較構成の平均6タスク精度48.9を55.1へ改善する一方、推論時の追加演算子は増やさない。

- **2026-08 · [Recurrent Residual Quantization: A Progressive Multi-Precision Representation for LLMs](2026-2608.04048-recurrent-residual-quantization-a-progressive-multi-precision-representa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  回帰残差量子化（Recurrent Residual Quantization、RRQ）は、大規模言語モデルの重みを、低ビットの基底表現と複数の量子化残差へ分解することで、単一の保存パッケージから複数の実効精度を選べる後学習量子化（Post-学習 量子化、PTQ）の方式である。

- **2026-08 · [FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy](2026-2608.15602-fluxbin-lut-ultra-low-bit-inference.md)**  
  実装：[✓](https://github.com/nicyyyy/FluxBin) ・ リポジトリ内被引用：0  
  重要列だけをヘッセ行列で選んで追加二値基底を与え、逆量子化を避けるLUT融合CUDAカーネルで約2〜3ビットLLMを実行し、A100で最大5.92倍高速化・10.19倍省エネルギーを報告する。

- **2026-07 · [BiSCo-LLM: Lookup-Free Binary Spherical Coding for Extreme Low-Bit Large Language Model Compression](2026-2607.08643-bisco-llm-lookup-free-binary-spherical-coding-for-extreme-low-bit-large-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BiSCo-LLMは、大規模言語モデル（LLM）の重みを2ビット級へ圧縮する際、単純なスカラー量子化では表現力が不足し、ベクトル量子化では明示的なコードブックの記憶容量と検索費用が増える問題に対処する研究である。BiSCo-LLMは較正データと元の重みから重要チャネルを選び、約1%を8ビットで保護する。

- **2026-06 · [SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving](2026-2606.11244-spear-error-adaptive-low-bit-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン適応型量子化誤差補償とカーネル・通信・SLOスケジューリングを共同設計し、W4–FP16のperplexity差を56–75%回復。

- **2026-06 · [GRINQH: Graded Input-based Quantization Hierarchy for Efficient LLM Generation](2026-2606.23419-grinqh-graded-input-based-quantization-hierarchy-for-efficient-llm-gener.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  後者、とりわけバッチ1では、大きな線形層の重みを毎トークン読み出すため帯域律速になりやすい。重みを一律に3ビットや4ビットへ量子化すると帯域は減るが、重要なチャネルの精度も同時に失われる。Qwen3-8BのRTX 4090上では、4ビットMARLINの最適化カーネルより約25%高速な、GSM8K品質とのパレート前線上の動作点を示す。

- **2026-05 · [Fitting Is Not Enough: Smoothness in Extremely Quantized LLMs](2026-2605.08894-fitting-is-not-enough-smoothness-in-extremely-quantized-llms.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/FINE) ・ リポジトリ内被引用：0  
  極低ビットの大規模言語モデル（LLM）量子化では、元の浮動小数点モデルと量子化モデルの中間出力を近付ける「順方向の再構成誤差」が一般的な最適化対象である。

- **2026-05 · [BCJR-QAT: A Differentiable Relaxation of Trellis-Coded Weight Quantization](2026-2605.10655-bcjr-qat-a-differentiable-relaxation-of-trellis-coded-weight-quantizatio.md)**  
  実装：[✓](https://github.com/Venugopalan2610/quant-2bit) ・ リポジトリ内被引用：0  
  BCJR-QATは、トレリス符号化量子化（Trellis-Coded Quantization; TCQ）を使うLLMの2ビット重み表現に対し、量子化認識学習（Quantization-Aware 学習; QAT）を適用する方法である。

- **2026-05 · [ADMM-Q: An Improved Hessian-based Weight Quantizer for Post-Training Quantization of Large Language Models](2026-2605.11222-admm-q-an-improved-hessian-based-weight-quantizer-for-post-training-quan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  しかし学習後量子化（Post-学習 量子化; PTQ）では、元の重みを単純に最も近い離散値へ丸めると、層の出力誤差が蓄積して言語モデルの品質が低下する。

- **2026-03 · [HALO: Hardware-Aware Quantization with Low Critical-Path-Delay Weights for LLM Acceleration](2026-2502.19662-halo-hardware-aware-quantization-with-low-critical-path-delay-weights-fo.md)**  
  実装：[✓](https://github.com/ecolab-nus/HALO) ・ リポジトリ内被引用：0  
  重みの数値精度を下げれば計算器やメモリの費用は小さくなる。HALOはこの差を量子化設計へ直接持ち込み、重要な重みを保護しつつ、残りの重みを回路遅延の短い離散値へ写像する。

- **2026-02 · [SFMP: Fine-Grained, Hardware-Friendly and Search-Free Mixed-Precision Quantization for Large Language Models](2026-2602.01027-sfmp-fine-grained-hardware-friendly-and-search-free-mixed-precision-quan.md)**  
  実装：[✓](https://github.com/Nkniexin/SFMP) ・ リポジトリ内被引用：0  
  重み量子化は、大規模言語モデル（LLM）の重みを16ビットなどの高精度形式から2～4ビット程度の表現へ圧縮し、GPUメモリ使用量を削減する。

- **2026-02 · [LittleBit-2: Maximizing the Spectral Energy Gain in Sub-1-Bit LLMs via Latent Geometry Alignment](2026-2603.00042-littlebit-2-maximizing-the-spectral-energy-gain-in-sub-1-bit-llms-via-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LittleBit-2は、学習済み大規模言語モデル（LLM）の重み行列を低ランクの二値因子に分解するLittleBit方式を改良し、二値化の直前に潜在空間を回転して量子化誤差を小さくする研究である。

- **2026-01 · [StableQAT: Stable Quantization-Aware Training at Ultra-Low Bitwidths](2026-2601.19320-stableqat-stable-quantization-aware-training-at-ultra-low-bitwidths.md)**  
  実装：[✓](https://github.com/microsoft/StableQAT) ・ リポジトリ内被引用：0  
  量子化考慮学習（Quantization-Aware 学習、QAT）は、学習時に重みを低ビットへ丸めることによる誤差をモデルに経験させ、推論時の低ビット実装に適応させる手法である。

- **2026-01 · [Sliced-Wasserstein Distribution Alignment Loss Improves the Ultra-Low-Bit Quantization of Large Language Models](2026-2601.07878-sliced-wasserstein-distribution-alignment-loss-improves-the-ultra-low-bi.md)**  
  実装：[✓](https://github.com/TokuyuSou/SWLoss_LightCompress) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（LLM）を4ビット未満へ量子化するとき、従来の要素ごとの再構成誤差だけでは失われる情報があることに着目する。LLaMA-2-7Bの重み4ビット・活性値4ビット（W4A4）では、六つのゼロショット課題の平均正答率がOmniQuantの46.24%から48.92%へ改善した。

- **2026-01 · [Post-Training Probability Manifold Correction via Structured SVD Pruning and Self-Referential Distillation](2026-2602.00372-post-training-probability-manifold-correction-via-structured-svd-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Sparse Knowledge Distillation（SparseKD）は、すでに学習を終えた自己回帰言語モデルのMLP重みを構造的に低ランク化し、その変換によって崩れた出力確率分布を、元モデル自身を教師とする蒸留で修復する手法である。

- **2026-01 · [D2Quant: Accurate Low-bit Post-Training Weight Quantization for LLMs](2026-2602.02546-d2quant-accurate-low-bit-post-training-weight-quantization-for-llms.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/D2Quant) ・ リポジトリ内被引用：0  
  D²Quantは、大規模言語モデルの重みのみを4ビット未満へ圧縮するときの精度劣化を対象とする、学習後量子化（post-学習 量子化; PTQ）の研究である。実験においてQwen3-8Bの2ビット重み量子化はWikiText2でパープレキシティ14.10、C4で25.96、MMLUで49.94%、7課題の平均正答率57.22%となった。

- **2026-01 · [Breaking the Blocks: Continuous Low-Rank Decomposed Scaling for Unified LLM Quantization and Adaptation](2026-2601.22716-breaking-the-blocks-continuous-low-rank-decomposed-scaling-for-unified-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LoRDS（Low-Rank Decomposed Scaling）は、重みを低ビット整数に変換するときのスケール因子の表現を変える方式である。

### 2年前（2024-11〜2025-10）

- **2025-04 · [SpinQuant: LLM quantization with learned rotations](2025-2405.16406-spinquant-llm-quantization-with-learned-rotations.md)**  
  実装：[✓](https://github.com/facebookresearch/SpinQuant) ・ リポジトリ内被引用：130  
  外れ値が低ビット量子化の誤差を大きくする問題に対して、全精度の機能を保つ旋回行列を学習し、重み・活性値・KVキャッシュの量子化に合わせる。

- **2025-08 · [LMDeploy Accelerates Mixed-Precision LLM Inference with TurboMind](2025-2508.15601-efficient-mixed-precision-large-language-model-inference.md)**  
  実装：[✓](https://github.com/InternLM/lmdeploy) ・ リポジトリ内被引用：9  
  量子化された重みを行列積の直前に浮動小数点へ復号すると、復号命令と共有メモリへの転送が計算の待ち時間になる。既存の混合精度推論基盤に対して配信遅延を最大61%（平均30%）削減し、処理率を最大156%（平均58%）向上したと報告する。

- **2025-04 · [MiLo: Efficient Quantized MoE Inference with Mixture of Low-Rank Compensators](2025-2504.02658-milo-efficient-quantized-moe-inference-with-mixture-of-low-rank-compensa.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/MiLo) ・ リポジトリ内被引用：8  
  Mixtral-8×7Bの半精度重みは約90GBに達し、単一の40GBや80GBのGPUに収まりにくい。4ビット量子化は比較的品質を保てる一方、3ビットに下げると重みを表現できる値が減り、WikiText-2の予測性能が顕著に悪化する。論文はMixtral-8×7BとDeepSeek-MoEで精度を測り、A100 40GBで推論遅延も測定した。

- **2025-04 · [HIGGS: Pushing the Limits of Large Language Model Quantization via the Linearity Theorem](2025-2411.17525-higgs-pushing-the-limits-of-large-language-model-quantization-via-the-li.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  HIGGSは、LLMの各重み行列を別々に量子化するとき、どの誤差指標を最小化すればモデル全体の予測品質を守れるのかを理論と実験の両面から扱う。GPU実装面では、RTX 4090でLlama-3.1-8Bの4ビットHIGGSをFLUTEカーネルで実行すると、バッチ1で139トークン/秒、FP16は57トークン/秒だった。

- **2025-02 · [Huff-LLM: End-to-End Lossless Compression for Efficient LLM Inference](2025-2502.00922-huff-llm-end-to-end-lossless-compression-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Huff-LLMは、言語モデルの重みを数値を一切変えずに圧縮し、保存先から推論演算器の直前まで圧縮状態を維持する方式である。Llama、Qwen、OPT、Vicunaの重みで容量削減を測定し、専用推論回路のモデル化で最大約32%の重み容量削減、最大約31%の推論遅延短縮、最大約26%のエネルギー削減を報告する。

- **2024-11 · [ZipNN: Lossless Compression for AI Models](2024-2411.05239-zipnn-lossless-compression-for-ai-models.md)**  
  実装：[✓](https://github.com/zipnn/zipnn) ・ リポジトリ内被引用：6  
  ZipNNは、モデルの重みを変更せずに保存・転送時のバイト数を減らし、展開すると元の重みビット列を完全に復元する可逆圧縮（無損失 compression）である。論文表IIIのLlama 3.1（BF16）では、Zstd単体の圧縮後サイズが原寸の77.7%なのに対してZipNNは66.4%。

- **2025-10 · [QSVD: Efficient Low-rank Approximation for Unified Query-Key-Value Weight Compression in Low-Precision Vision-Language Models](2025-2510.16292-qsvd-efficient-low-rank-approximation-for-unified-query-key-value-weight.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/QSVD) ・ リポジトリ内被引用：5  
  QSVDは、画像と文章を同時に処理する視覚言語モデル（Vision-Language モデル; VLM）の注意層で、問い合わせ（Query; Q）・鍵（Key; K）・値（Value; V）の射影重みを別々に圧縮するのではなく結合して低ランク分解する手法である。

- **2025-09 · [PTQTP: Post-Training Quantization to Trit-Planes for Large Language Models](2025-2509.16989-ptqtp-post-training-quantization-to-trit-planes-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  PTQTPは、学習済み重みを2枚の三値平面（trit-plane）と連続尺度へ分解し、約1.58ビット級の超低ビット表現を事後量子化（Post-学習 量子化; PTQ）だけで作る。二値PTQより表現力を増やしつつ、混合精度の例外経路を使わず一様な三値演算へ落とすのが狙いである。

- **2025-04 · [OAC: Output-adaptive Calibration for Accurate Post-training Quantization](2025-2405.15025-oac-output-adaptive-calibration-for-accurate-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重みを2ビットあるいは1ビットに圧縮すると、元の浮動小数点重みを丸める際の誤差が大きくなり、通常の層単位の校正だけではモデルの最終予測が著しく悪化する。

- **2025-05 · [Addition is almost all you need: Compressing large language models with double binary factorization](2025-2505.11076-addition-is-almost-all-you-need-compressing-large-language-models-with-d.md)**  
  実装：[✓](https://github.com/usamec/double_binary) ・ リポジトリ内被引用：3  
  大規模言語モデルの重みを低ビット化すると、モデルの保存容量とメモリ帯域要求を減らせる。ただし一般的な量子化は、実行時に低ビットの重みを展開して高精度の積和演算を行うことが多い。RTX4090でのバッチ1復号では、Llama3-8BのFP16 60 トークン/sに対して2bit DBFが133 トークン/s、約2.22倍となる。

- **2025-02 · [LO-BCQ: Locally Optimal Block Clustered Quantization for 4-bit (W4A4) LLM Inference](2025-2502.05376-lo-bcq-locally-optimal-block-clustered-quantization-for-4-bit-w4a4-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  主題は、大規模言語モデルの重みと活性値の両方を4ビット程度へ量子化し、再学習を行わずに推論品質を保つ事後量子化（Post-学習 量子化; PTQ）である。代表例としてLlama2-7Bの5つの言語理解課題平均では、BF16の65.65%に対し、実効4.5ビットのLO-BCQは64.68%となり、0.97ポイント低下した。

- **2025-09 · [Quant-dLLM: Post-Training Extreme Low-Bit Quantization for Diffusion Large Language Models](2025-2510.03274-quant-dllm-post-training-extreme-low-bit-quantization-for-diffusion-larg.md)**  
  実装：[✓](https://github.com/ZTA2785/Quant-dLLM) ・ リポジトリ内被引用：2  
  本研究は、拡散型大規模言語モデル（diffusion large language モデル、以下dLLM）の重みを、追加の勾配学習なしに平均2ビットへ圧縮しながら、生成・推論課題の正答率を維持する手法を提案する。

- **2025-06 · [Unifying Uniform and Binary-coding Quantization for Accurate Compression of Large Language Models](2025-2506.03781-unifying-uniform-and-binary-coding-quantization-for-accurate-compression.md)**  
  実装：[✓](https://github.com/snudm-starlab/UniQuanF) ・ リポジトリ内被引用：2  
  UQは一定間隔に並んだ量子化レベルを使う。Llama-3 8B InstructのGSM8Kでは3ビットでUniQuanFが58.73%、FlexRoundが54.13%で、差は4.60パーセントポイント。

- **2025-05 · [ICQuant: Index Coding enables Low-bit LLM Quantization](2025-2505.00850-icquant-index-coding-enables-low-bit-llm-quantization.md)**  
  実装：[✓](https://github.com/Avery-xl/ICQuant) ・ リポジトリ内被引用：2  
  ICQuant（Index Coding enables Low-bit LLM Quantization）は、大規模言語モデル（LLM）の重みを2〜3ビット程度へ圧縮する際、少数の極端な値が量子化範囲を不必要に広げる問題を、外れ値の分離と位置索引の効率的な符号化で解く学習後量子化（Post-学習 量子化; PTQ）方式である。

- **2024-12 · [DecDEC: A Systems Approach to Advancing Low-Bit LLM Quantization](2024-2412.20185-decdec-a-systems-approach-to-advancing-low-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低ビット量子化（low-bit 量子化）は、LLMの重みを3ビット・4ビット程度へ圧縮し、GPUメモリと復号時の重み読出しを削減する。原著はRTX 4070 Super 12GBを含む5種類の一般消費者向けGPUで評価した。

- **2025-09 · [Bi-VLM: Pushing Ultra-Low Precision Post-Training Quantization Boundaries in Vision-Language Models](2025-2509.18763-bi-vlm-pushing-ultra-low-precision-post-training-quantization-boundaries.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大きな重み容量と画像トークンの計算費用があるため、小型端末への配置が難しい。Bi-VLMは、事前学習済みの視覚言語モデルを再学習せずに極低ビット化するため、重みの分布を統計的な分位点で複数群へ分け、重要な外れ値重みには2bit、その他の多数の重みには1bitを割り当てる後学習量子化方式である。

- **2024-12 · [RILQ: Rank-Insensitive LoRA-based Quantization Error Compensation for Boosting 2-bit Large Language Model Accuracy](2024-2412.01129-rilq-rank-insensitive-lora-based-quantization-error-compensation-for-boo.md)**  
  実装：[✓](https://github.com/aiha-lab/RILQ) ・ リポジトリ内被引用：1  
  重み量子化（重み 量子化）は、FP16などで保持していた行列を低ビット表現へ写像してモデルの重み記憶量を削減する。LLaMA-3-8BのQuIP#量子化では常識推論5課題平均が52.48%→60.61%、WikiText-2の困惑度（perplexity; PPL）が12.74→9.39となった。

### 3年前（2023-11〜2024-10）

- **2024-02 · [QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks](2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/quip-sharp) ・ リポジトリ内被引用：121  
  QuIP#は、学習済みの大規模言語モデルを再学習せずに2〜4ビット/重みへ圧縮する事後学習量子化（Post-学習 量子化、PTQ）である。試作推論実装はRTX 4090上で70Bの2ビット重みを32.74トークン/秒で生成し、実効メモリ帯域利用率56.84%を記録した（表5）。

- **2024-05 · [QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving](2024-2405.04532-qserve.md)**  
  実装：[✓](https://github.com/mit-han-lab/omniserve) ・ リポジトリ内被引用：91  
  QServeは、クラウド型の大規模言語モデル（LLM）サービングにおいて、重みを4ビットへ量子化してもGPU上の実行速度が期待ほど上がらない問題を、量子化アルゴリズムと推論カーネルの協調設計によって解く研究である。論文はこの量子化解除の費用が20〜90%に達する条件を示し、ビット数を減らすだけではサービング処理率を改善できないことを説明する。

- **2024-01 · [Extreme Compression of Large Language Models via Additive Quantization](2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md)**  
  実装：[✓](https://github.com/Vahe1994/AQLM) ・ リポジトリ内被引用：74  
  加算量子化による言語モデル圧縮（AQLM）は、重みの極低ビット量子化における「小さいモデルを高精度で保持した方が、巨大モデルを2ビットにするより良い」という従来の精度対容量の関係を改善する研究である。Llama 2 7B・13B・70B、Mixtral 8×7B、Mistral 7Bを評価する。

- **2024-01 · [SliceGPT: Compress Large Language Models by Deleting Rows and Columns](2024-2401.15024-slicegpt-compress-large-language-models-by-deleting-rows-and-columns.md)**  
  実装：[✓](https://github.com/microsoft/TransformerCompression) ・ リポジトリ内被引用：61  
  SliceGPTは、学習済みTransformerの埋め込み次元を減らす学習後圧縮である。代表的なLLaMA-2 70Bの25%削減では、A100 40GBで1トークン生成時間が125ミリ秒から110ミリ秒へ、必要GPUが4台から3台へ減った。

- **2024-06 · [DuQuant: Distributing Outliers via Dual Transformation Makes Stronger Quantized LLMs](2024-2406.01721-duquant-distributing-outliers-via-dual-transformation-makes-stronger-quantized-llms.md)**  
  実装：[✓](https://github.com/Hsu1023/DuQuant) ・ リポジトリ内被引用：50  
  巨大外れ値を外れ値誘導のブロック回転とジグザグ置換で分散し、4ビット重み・活性量子化の精度を改善しつつ、LLaMA2-7Bでプリフィル最大2.08倍・復号時メモリ3.50倍削減を示す。

- **2024-10 · [FlatQuant: Flatness Matters for LLM Quantization](2024-2410.09426-flatquant-flatness-matters-for-llm-quantization.md)**  
  実装：[✓](https://github.com/ruikangliu/FlatQuant) ・ リポジトリ内被引用：43  
  層ごとの学習可能アフィン変換を小さなクロネッカー積へ分解し量子化と融合して、LLaMA-3-70BのW4A4で精度低下1%未満とプリフィル最大2.3倍高速化を両立する。

- **2023-12 · [ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models](2023-2312.05821-asvd-activation-aware-singular-value-decomposition-for-compressing-large.md)**  
  実装：[✓](https://github.com/hahnyuan/ASVD4LLM) ・ リポジトリ内被引用：42  
  活性値認識型特異値分解（活性値-aware Singular Value Decomposition、ASVD）は、大規模言語モデル（LLM）の線形重みを追加学習なしで低ランク行列へ置き換える圧縮方式である。LLaMA-7BとLLaMA-2-7B/13Bで重み容量を10～30%削減する実験を行い、活性値を考慮しないSVDより大幅に良い困惑度を報告する。

- **2024-06 · [QTIP: Quantization with Trellises and Incoherence Processing](2024-2406.11235-qtip-quantization-with-trellises-and-incoherence-processing.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/qtip) ・ リポジトリ内被引用：37  
  ベクトル量子化（Vector Quantization, VQ）は複数重みをまとめて符号化するほど量子化効率が上がる一方、通常の符号帳は次元に対して指数的に巨大化する。QTIPは、符号帳を列挙せず有限状態の「トレリス」を使うことで、この次元の壁を外し、2bit級でも256次元の高次元量子化を実用的な復号コストで実現する。

- **2024-02 · [GPTVQ: The Blessing of Dimensionality for LLM Quantization](2024-2402.15319-gptvq-the-blessing-of-dimensionality-for-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：37  
  複数の重みを1ベクトルとして量子化し、代理ヘッセ行列（proxy Hessian）で量子化誤差を後続列へ補償する。Llama 3 8Bの約3.125 bit/value構成では、Snapdragon X Elite上で独自INT4実装よりモデル占有量を約19%減らし、23.81から26.15 トークン/sへ高速化する。

- **2024-02 · [BiLLM: Pushing the Limit of Post-Training Quantization for LLMs](2024-2402.04291-billm-pushing-the-limit-of-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/BiLLM) ・ リポジトリ内被引用：36  
  ヘッセ感度で重要列を選び二値残差近似し、残りのベル形重み分布を最適分割して別々に二値化することで、再学習なしにLLM重みを約1.1ビットまで圧縮する。

- **2024-01 · [SliM-LLM: Salience-Driven Mixed-Precision Quantization for Large Language Models](2024-2405.14917-slim-llm-salience-driven-mixed-precision-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：29  
  要素単位で重要重みだけ高精度に残すのではなく、重要度が空間的にまとまる性質を使ってグループ単位で1/2/3ビットを割り当てる。さらに各グループ内部の少数の重要要素を量子化器校正で重く扱い、LLaMA-7Bの2ビット級でWikiText2パープレキシティ14.58を達成する。

- **2024-03 · [AffineQuant: Affine Transformation Quantization for Large Language Models](2024-2403.12544-affinequant-affine-transformation-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  スカラーの拡大縮小や平行移動に限られていた等価変換を、可逆な行列によるアフィン変換へ拡張する。変換を量子化前の重みへ掛け、逆変換を活性値側へ入れることで元の線形演算を保ったまま量子化しやすい座標系を学習し、LLaMA2-7BのW4A4でC4パープレキシティをOmniQuantの18.02から15.76へ改善する。

- **2024-02 · [OneBit: Towards Extremely Low-bit Large Language Models](2024-2402.11295-onebit-towards-extremely-low-bit-large-language-models.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/OneBit) ・ リポジトリ内被引用：26  
  OneBitは、学習済み大規模言語モデル（LLM）の重みを極端に低いビット数で保存する際に生じる精度劣化を、線形層の表現形式そのものを変更することで緩和する研究である。査読版の表3では、LLaMA-7Bの重み保存量が13.5 GBから1.3 GBへ、LLaMA-13Bでは26.0 GBから2.2 GBへ減る。

- **2024-02 · [BitDistiller: Unleashing the Potential of Sub-4-Bit LLMs via Self-Distillation](2024-2402.10631-bitdistiller-unleashing-the-potential-of-sub-4-bit-llms-via-self-distill.md)**  
  実装：[✓](https://github.com/DD-DuDa/BitDistiller) ・ リポジトリ内被引用：26  
  学習後量子化（post-学習 量子化、PTQ）は比較的低費用だが、低ビットでは誤差を修正しにくい。

- **2024-05 · [PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM Compression](2024-2405.14852-pv-tuning-beyond-straight-through-estimation-for-extreme-llm-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  大規模言語モデルを1～2ビット/重みへ圧縮すると、モデルを小さなメモリへ収められる一方、量子化誤差によって予測品質が大きく低下する。Llama-2 7Bの約2.02ビット/重みではWikiText-2のパープレキシティ5.84、5課題平均正答率61.35%を報告し、同程度のQuIP#の6.19・57.51%を上回る。

- **2024-07 · [Compact Language Models via Pruning and Knowledge Distillation](2024-2407.14679-compact-language-models-via-pruning-and-knowledge-distillation.md)**  
  実装：[✓](https://github.com/NVlabs/Minitron) ・ リポジトリ内被引用：18  
  15Bを学習した後に8B・4Bを別々にゼロから学習する代わりに、Nemotron-4 15Bから注意ヘッド、MLP中間次元、埋め込み幅、必要に応じて層を構造枝刈りし、元15Bのロジットを教師にして短期間だけ知識蒸留（Knowledge Distillation; KD）する。

- **2024-03 · [IntactKV: Improving Large Language Model Quantization by Keeping Pivot Tokens Intact](2024-2403.01241-intactkv-improving-large-language-model-quantization-by-keeping-pivot-to.md)**  
  実装：[✓](https://github.com/ruikangliu/IntactKV) ・ リポジトリ内被引用：16  
  IntactKVは、低ビット量子化した大規模言語モデル（LLM）において、入力の最初に置かれる少数の支点トークン（pivot トークン）の鍵・値キャッシュ（KV キャッシュ）だけを高精度モデルから生成して保存する方式である。

- **2024-01 · [LLM-FP4: 4-Bit Floating-Point Quantized Transformers](2023-2310.16836-llm-fp4-4-bit-floating-point-quantized-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  4ビット浮動小数点（floating point; FP）の指数部構成とクリップ範囲を層ごとに探索し、活性値の大きなチャネル間分散はチャネル別指数バイアスを重みへ事前吸収して処理する。LLaMA-13Bの埋め込み・重み・活性値を4/4/4ビットにして、6つの常識推論タスク平均63.1を維持する。

- **2024-02 · [DB-LLM: Accurate Dual-Binarization for Efficient LLMs](2024-2402.11960-db-llm-accurate-dual-binarization-for-efficient-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  大規模言語モデルの重み量子化は、16ビット浮動小数点の重みを数ビットの離散値へ置き換え、モデル保存量と重み読み出し量を減らす。LLaMA-1-7Bでは平均重み疎性が62.8%となり、著者らの計算量モデルでは32トークン入力のFLOPsが通常2ビット量子化の37.3Gから29.8Gへ減る。

- **2024-02 · [LQER: Low-Rank Quantization Error Reconstruction for LLMs](2024-2402.02446-lqer-low-rank-quantization-error-reconstruction-for-llms.md)**  
  実装：[✓](https://github.com/ChengZhang-98/lqer) ・ リポジトリ内被引用：8  
  大規模言語モデルの重みを4ビットへ圧縮しても、実行時に半精度へ逆量子化してから行列積を計算するなら、重みの保存容量削減がそのまま演算器の省資源化につながるとは限らない。

- **2023-12 · [CBQ: Cross-Block Quantization for Large Language Models](2023-2312.07950-cbq-cross-block-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  学習後量子化（Post-学習 量子化、PTQ）は、学習済み大規模言語モデルの重みや活性を少ないビット数で表現し、メモリ使用量や演算費用を下げる技術である。65Bの4ビット重み量子化を単一GPUで4.3時間で行ったという処理費用の報告はあるが、量子化後の推論速度を4.3倍にしたという意味ではない。

- **2024-06 · [LLMEasyQuant: Scalable Quantization for Parallel and Distributed LLM Inference](2024-2406.19657-llmeasyquant-scalable-quantization-for-parallel-and-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/NoakLiu/LLMEasyQuant) ・ リポジトリ内被引用：4  
  LLMEasyQuantは、大規模言語モデル（LLM）の学習後量子化を研究・実行するための統合基盤である。論文は、量子化方式の品質だけを比較しても、実行時のメモリ転送や通信、逆量子化が遅ければ推論の速度向上につながらないと考える。

- **2024-05 · [Post Training Quantization of Large Language Models with Microscaling Formats](2024-2405.07135-post-training-quantization-of-large-language-models-with-microscaling-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  本論文は、大規模言語モデル（LLM）の事後量子化（post-学習 量子化, PTQ）で広く使われるSmoothQuant、活性認識重み量子化（AWQ）、勾配不要の重み誤差補償（GPTQ）を、ブロックごとに尺度を共有する微小尺度（microscaling, MX）形式へ拡張し、三方式の組合せと適用順序を体系的に評価した研究である。

- **2024-06 · [BoA: Attention-aware Post-training Quantization without Backpropagation](2024-2406.13474-boa-attention-aware-post-training-quantization-without-backpropagation.md)**  
  実装：[✓](https://github.com/SamsungLabs/BoA) ・ リポジトリ内被引用：3  
  BoA（Backpropagation-free optimization for 注意機構-aware PTQ）は、大規模言語モデルの学習後量子化（post-学習 量子化、PTQ）で、重みの整数化に伴う性能低下を抑える手法である。

- **2024-02 · [FlattenQuant: Breaking Through the Inference Compute-bound for Large Language Models with Per-tensor Quantization](2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  FlattenQuantは、大規模言語モデル（LLM）の推論で、重みだけを低ビット化しても行列演算が半精度のまま残るという問題を解く後学習量子化（post-学習 量子化; PTQ）方式である。難点は、LLMの活性値に他のチャネルより20〜100倍程度大きい外れ値チャネルが存在することだ。

- **2023-12 · [ZeroQuant(4+2): Redefining LLMs Quantization with a New FP6-Centric Strategy for Diverse Generative Tasks](2023-2312.08583-zeroquant-4-2-redefining-llms-quantization-with-a-new-fp6-centric-strate.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  4ビット整数量子化（INT4）が自由生成課題で不安定になる条件を測り、6ビット浮動小数点（FP6）の品質を、4+2ビットの格納・復号方式と指数バイアスの事前変換によって既存GPU上で利用する研究。

- **2024-05 · [ReALLM: A general framework for LLM compression and fine-tuning](2024-2405.13155-reallm-a-general-framework-for-llm-compression-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  元の行列を16ビットで保存する代わりに、学習済みの小型デコーダ、量子化した埋め込み、コードブック、必要な逆置換、低ランク行列とスケールを保存する。

- **2024-10 · [SeedLM: Compressing LLM Weights into Seeds of Pseudo-Random Generators](2024-2410.10714-seedlm-compressing-llm-weights-into-seeds-of-pseudo-random-generators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの自己回帰生成では、1トークンを生成するたびに大量の重みを読み出す必要があり、演算器の理論性能よりもDRAM帯域が制約になる場合がある。通常の低ビット量子化は、FP16などの重みを整数値へ写像して読み出し量を減らす。速度については、専用FPGA上の行列ベクトル積でFP16基準比3.67〜3.98倍のサイクル数削減を報告する。

- **2024-09 · [Accumulator-Aware Post-Training Quantization for Large Language Models](2024-2409.17092-accumulator-aware-post-training-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が対象とするのは、量子化後の重み・活性化値を掛け合わせる演算ではなく、その積を多数足し込む累積器（accumulator）のビット幅である。

### 4年前（2022-11〜2023-10）

- **2022-11 · [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/mit-han-lab/smoothquant) ・ リポジトリ内被引用：395  
  活性値全体を単純に8ビットへ写すと、その少数の外れ値が量子化範囲を広げ、通常値へ割り当てられる段階数が減って精度が崩れる。OPT、BLOOM、GLM、MT-NLGなどで8ビット重み・8ビット活性値（W8A8）を実現し、精度低下をほぼ抑えながら最大1.56倍の推論高速化と2倍のメモリ削減を報告し、530Bモデルを単一ノードで提供可能にした。

- **2023-06 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](2023-2306.00978-awq.md)**  
  実装：[✓](https://github.com/mit-han-lab/llm-awq) ・ リポジトリ内被引用：235  
  活性の大きい入力チャネルに対応する重みを等価スケーリングで保護し、全重みを均一な低ビット形式のまま高精度化する重み専用量子化とTinyChat実装。

- **2022-11 · [LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](2022-2208.07339-llm-int8-8-bit-matrix-multiplication-for-transformers-at-scale.md)**  
  実装：[✓](https://github.com/TimDettmers/bitsandbytes) ・ リポジトリ内被引用：199  
  特徴次元の外れ値を16-bitへ分離し、残る99.9%以上をベクトル単位INT8で計算する。175B級モデルの品質とほぼ半減の重み容量を両立する一方、小さい行列では量子化費用が速度改善を打ち消す。

- **2023-08 · [OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models](2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-m.md)**  
  実装：[✓](https://github.com/OpenGVLab/OmniQuant) ・ リポジトリ内被引用：152  
  大規模言語モデルの重みを16ビットから4ビット、3ビット、2ビットへ縮めると、保存容量と重み転送量を大きく削減できる。一方、極低ビットでは重みや活性値の少数の外れ値が量子化範囲を広げ、重要な値の量子化刻みが粗くなって出力品質が崩れる。LLaMA-2 7B～70Bは128個の校正系列とA100 40GB 1基で1～16時間の処理が可能と報告される。

- **2023-07 · [QuIP: 2-Bit Quantization of Large Language Models With Guarantees](2023-2307.13304-quip-2-bit-quantization-of-large-language-models-with-guarantees.md)**  
  実装：✓ ・ リポジトリ内被引用：135  
  重みと代理ヘッセ行列（proxy Hessian）の座標依存の偏りをランダム直交変換で崩してから、LDL分解に基づく適応丸めを行う。Llama 2 70Bでは2ビット重みでもWikiText2パープレキシティ6.326を保ち、同条件のOPTQの123.908から大幅に改善する。

- **2023-06 · [SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression](2023-2306.03078-spqr-a-sparse-quantized-representation-for-near-lossless-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Vahe1994/SpQR) ・ リポジトリ内被引用：125  
  高感度な少数重みだけを十六ビット疎表現に逃がし、残りと量子化尺度を三〜四ビット化してほぼ無損失圧縮する混合重み表現。

- **2023-06 · [SqueezeLLM: Dense-and-Sparse Quantization](2023-2306.07629-squeezellm-dense-and-sparse-quantization.md)**  
  実装：[✓](https://github.com/SqueezeAILab/SqueezeLLM) ・ リポジトリ内被引用：121  
  二次感度に基づく非一様量子化と、外れ値・高感度重みだけをFP16疎行列へ逃がすDense-and-Sparse分解により、3-bit級でも品質を保ちながら重み転送量と生成遅延を削減する。

- **2023-05 · [LLM-QAT: Data-Free Quantization Aware Training for Large Language Models](2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/LLM-QAT) ・ リポジトリ内被引用：114  
  LLM-QATは、学習後量子化（Post-学習 量子化: PTQ）では精度が大きく低下する低ビット領域に対し、量子化誤差を学習中に経験させる量子化対応学習（Quantization-Aware 学習: QAT）を大規模言語モデルへ適用する研究である。

- **2023-10 · [Atom: Low-bit Quantization for Efficient and Accurate LLM Serving](2023-2310.19102-atom-low-bit-quantization-for-efficient-and-accurate-llm-serving.md)**  
  実装：[✓](https://github.com/efeslab/Atom) ・ リポジトリ内被引用：89  
  外れ値チャネルだけ高精度に残して重み・活性・KVキャッシュを低ビット化し、再配置と融合カーネルで4ビットGPU演算器を直接使ってLLM配信を高速化する。

- **2023-06 · [OWQ: Outlier-Aware Weight Quantization for Efficient Fine-Tuning and Inference of Large Language Models](2023-2306.02272-owq-outlier-aware-weight-quantization-for-efficient-fine-tuning-and-infe.md)**  
  実装：[✓](https://github.com/xvyaward/owq) ・ リポジトリ内被引用：53  
  大規模言語モデルの重みを3ビット級へ圧縮すると、モデル容量と重み読出し量は減るが、わずかな量子化誤差が特定の特徴次元で増幅され、出力品質が大きく悪化することがある。

- **2022-12 · [The case for 4-bit precision: k-bit Inference Scaling Laws](2022-2212.09720-the-case-for-4-bit-precision-k-bit-inference-scaling-laws.md)**  
  実装：✓ ・ リポジトリ内被引用：50  
  量子化では、1パラメータ当たりのビット数を下げるほど同じ重みメモリへ大きなモデルを置ける。

- **2023-09 · [PB-LLM: Partially Binarized Large Language Models](2023-2310.00034-pb-llm-partially-binarized-large-language-models.md)**  
  実装：[✓](https://github.com/hahnyuan/BinaryLLM) ・ リポジトリ内被引用：36  
  重みを一律1ビット化するのではなく、ヘッセ行列で選んだ少数の顕著重みを高精度で残し、それ以外だけを±1へ二値化する。LLaMA-7Bでは顕著重み30%を残す量子化対応学習版が7つのゼロショット常識推論で平均66.9を達成し、10%まで減らしても60.6を保つ。

- **2023-06 · [OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization](2023-olive-accelerating-large-language-models-via-hardware-friendly-outlier-victim-pair-quantization.md)**  
  実装：[✓](https://github.com/clevercool/ANT-Quantization) ・ リポジトリ内被引用：34  
  外れ値を別の疎データ構造へ逃がすのではなく、隣接する低重要度の通常値を「犠牲値（victim）」として使い、外れ値を同じ固定幅ペアの中へ埋め込む。これにより外れ値対応量子化で問題になる座標リストと別演算経路をなくし、4ビットの整列アクセスをテンソルコアやシストリック配列へ直接載せる。

- **2023-04 · [Outlier Suppression+: Accurate quantization of large language models by equivalent and optimal shifting and scaling](2023-2304.09145-outlier-suppression-accurate-quantization-of-large-language-models-by-eq.md)**  
  実装：[✓](https://github.com/ModelTC/Outlier_Suppression_Plus) ・ リポジトリ内被引用：34  
  Outlier Suppression+（OS+）は、大規模言語モデルの活性値に現れる極端な外れ値が、事後量子化（Post-学習 量子化: PTQ）の精度を悪化させる問題に対する方法である。

- **2023-03 · [ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehen.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  ZeroQuant-V2は、大規模言語モデルの学習後量子化（Post-学習 量子化、PTQ）を、特定の一手法の成功例だけで評価するのではなく、量子化対象、数値精度、粒度、モデル系列、最適化方式を組み合わせて調べた研究である。元の16ビットモデルは10.33なので、この設定では測定上ほぼ同等となる。

- **2023-06 · [LoSparse: Structured Compression of Large Language Models based on Low-Rank and Sparse Approximation](2023-2306.11222-losparse-structured-compression-of-large-language-models-based-on-low-rank-and-sparse-approximation.md)**  
  実装：[✓](https://github.com/yxli2123/LoSparse) ・ リポジトリ内被引用：18  
  各重み行列を「全ニューロンに共有される低ランク成分」と「ニューロン固有の残差成分」に分け、残差側だけを構造枝刈りする。低ランク近似が表現力のある共通基底を守るため、高い枝刈り率でも通常の反復構造枝刈りより品質を落としにくい。

- **2023-05 · [Memory-Efficient Fine-Tuning of Compressed Large Language Models via sub-4-bit Integer Quantization](2023-2305.14152-memory-efficient-fine-tuning-of-compressed-large-language-models-via-sub.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  提案するPEQA（パラメータ-Efficient and 量子化-aware Adaptation）は、事前学習済みの重みを3～4ビットなどの整数表現へ量子化した後、整数値を凍結し、量子化尺度だけを学習する。

- **2023-02 · [With Shared Microexponents, A Little Shifting Goes a Long Way](2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  Rouhaniらは、ブロックデータ表現（Block Data Representation; BDR）という共通の設計枠を用意し、ブロックサイズ、尺度の階層、尺度を保存するビット数、各要素の仮数幅を変えて比較した。

- **2023-08 · [FineQuant: Unlocking Efficiency with Fine-Grained Weight-Only Quantization for LLMs](2023-2308.09723-finequant-unlocking-efficiency-with-fine-grained-weight-only-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  FineQuantは、大規模言語モデル（Large Language モデル; LLM）の重みだけを低ビット化し、活性値と積和演算は浮動小数点で実行する重み専用量子化（重み-only 量子化）の研究である。最大3.65倍の総処理量改善は、この三番目の複製数増加を含むノード全体の処理量であり、単一要求のトークン生成速度が3.65倍という意味ではない。

- **2023-10 · [Dynamic Sparse No Training: Training-Free Fine-tuning for Sparse LLMs](2023-2310.08915-dynamic-sparse-no-training-training-free-fine-tuning-for-sparse-llms.md)**  
  実装：[✓](https://github.com/zyxxmu/DSnoT) ・ リポジトリ内被引用：6  
  DSnoT（動的 Sparse No 学習）は、既存の枝刈り手法で疎化した大規模言語モデル（Large Language モデル、LLM）を、勾配逆伝播も重み値の更新も行わずに改善する方法である。

- **2023-10 · [E-Sparse: Boosting the Large Language Model Inference through Entropy-based N:M Sparsity](2023-2310.15929-e-sparse-boosting-the-large-language-model-inference-through-entropy-bas.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  こうした制約では重要な重みが同じ4要素のグループに集中すると、どれかを必ず削除しなければならず、言語モデルの品質が下がりやすい。残した重みの値を再学習・再最適化せずに疎性を作り、FasterTransformerへ統合した疎行列積（Sparse-GEMM）で実際の推論を高速化する。

- **2023-10 · [Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM](2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md)**  
  実装：[✓](https://github.com/ilur98/DGQ) ・ リポジトリ内被引用：1  
  しかし、重みを小さなグループ単位で4ビット量子化すると、グループごとに尺度が異なるため、整数の行列積を区切って浮動小数点で部分和を結合する必要が生じる。原著はLLaMA、LLaMA 2、OPTなどで困惑度とゼロショット推論精度を評価し、単一A100 80GBでの実行時間・メモリ使用量を測定した。

### 5年前（2021-11〜2022-10）

- **2022-10 · [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](2022-2210.17323-gptq.md)**  
  実装：[✓](https://github.com/IST-DASLab/gptq) ・ リポジトリ内被引用：456  
  二次情報に基づく誤差補償をGPU向けに再設計し、175B級LLMを数時間で3〜4bit化して単一A100実行と約3.24倍の生成高速化を実現した基礎的GPTQ研究。

- **2022-06 · [ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers](2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：132  
  大規模言語モデルの量子化では、重みを16ビットから8ビットへ減らすだけでメモリ転送量は小さくなる。INT8では追加の学習や校正なしでBERT・GPT系の品質をほぼ保ち、NVIDIA A100上のBERT-baseで最大5.19倍、GPT-3 350Mで4.16倍の速度向上を示した。

### 6年前（2020-11〜2021-10）

- **2021-01 · [I-BERT: Integer-only BERT Quantization](2021-2101.01321-i-bert-integer-only-bert-quantization.md)**  
  実装：[✓](https://github.com/kssteven418/i-bert) ・ リポジトリ内被引用：34  
  Transformerの重みと行列積を8ビット整数へ量子化しても、推論全体が整数だけで実行できるとは限らない。Tesla T4上の予備的な整数カーネル実装では、FP32比で2.4～4.0倍の推論高速化を報告する。

- **2021-09 · [Block Pruning For Faster Transformers](2021-2109.04838-block-pruning-for-faster-transformers.md)**  
  実装：[✓](https://github.com/huggingface/nn_pruning) ・ リポジトリ内被引用：21  
  Block Pruningは移動量に基づく枝刈り（movement 枝刈り）を重みブロック単位へ拡張し、フィードフォワード層の次元や注意ヘッドを構造的に除去できる形へ誘導する。

- **2021-02 · [Accelerated Sparse Neural Training: A Provable and Efficient Method to Find N:M Transposable Masks](2021-2102.08124-accelerated-sparse-neural-training-a-provable-and-efficient-method-to-fi.md)**  
  実装：[✓](https://github.com/papers-submission/structured_transposable_masks) ・ リポジトリ内被引用：6  
  本研究は、この非対称性を解消する転置可能細粒度疎マスク（transposable fine-grained sparsity mask）を提案する。論文が示す「2倍」は主として疎テンソルコアの適用可能な行列積の範囲の比較であり、全学習時間の2倍高速化を実測したものと読み替えない。

### 7年前（2019-11〜2020-10）

- **2020-05 · [GOBO: Quantizing Attention-Based NLP Models for Low Latency and Energy Efficient Inference](2020-2005.03842-gobo-quantizing-attention-based-nlp-models-for-low-latency-and-energy-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：32  
  GOBOは、BERTなどの注意機構を使う自然言語処理モデルの重みを、学習後に大幅に圧縮する手法である。重みの約99.9%を少数の代表値への索引で表し、残る約0.1%の外れ値だけを元の32ビット浮動小数点のまま保持する。

- **2020-09 · [TernaryBERT: Distillation-aware Ultra-low Bit BERT](2020-2009.12812-ternarybert-distillation-aware-ultra-low-bit-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：23  
  TernaryBERTは、自然言語理解向けのBERTを極低ビットで実行可能な重み表現へ圧縮し、精度低下を知識蒸留（Knowledge Distillation）で抑える手法である。これにより重み2ビット・埋め込み2ビット・活性値8ビットの代表構成で、BERTの保存サイズを418MBから28MBへ減らす。

- **2020-04 · [Training with Quantization Noise for Extreme Model Compression](2020-2004.07320-training-with-quantization-noise-for-extreme-model-compression.md)**  
  実装：[✓](https://github.com/pytorch/fairseq/tree/master/examples/quant_noise) ・ リポジトリ内被引用：21  
  学習済みモデルの重みを低ビットや積量子化で保存すると、推論時の重み容量を減らせるが、各層で生じた量子化誤差が次層の入力へ蓄積し、精度が急激に落ちることがある。ICLR 2021の原著では、16層Transformerの942MBを反復積量子化で38MBへ圧縮した場合、量子化雑音なしのテスト困惑度25.2に対して20.7へ改善した。

- **2020-02 · [Compressing BERT: Studying the Effects of Weight Pruning on Transfer Learning](2020-2002.08307-compressing-bert-studying-the-effects-of-weight-pruning-on-transfer-lear.md)**  
  実装：[✓](https://github.com/mitchellgordon95/bert-prune) ・ リポジトリ内被引用：17  
  対象はBERT-Baseの非構造化重み枝刈りである。主結果は、30～40%程度の重みを削除しても下流性能がほぼ変わらない一方、40～60%では事前学習で獲得した情報の消失が、70%以上ではそれに加えて残存ネットワークの表現容量制約が効くという三つの領域である。
<!-- survey:auto:end -->
