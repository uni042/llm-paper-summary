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
## 自動生成の論文一覧（177本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/16-weight-quantization-compression/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-06 · [CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs](2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：5  
  CAT-Qは、高精度で事前学習された大規模言語モデル（LLM）を、重みが負一・零・正一の三値しか取らない形式へ変換する学習後量子化（Post-学習 量子化; PTQ）方式である。235Bモデルの三値化にはA100 80GBを8枚使って最大60時間を要する。

- **2026-06 · [TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization](2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post.md)**  
  実装：[✓](https://github.com/Kishon-zzx/TWLA) ・ リポジトリ内被引用：4  
  TWLA（Ternarized Weights and Low-bit Activations）は、学習済み大規模言語モデル（LLM）の重みを三値へ圧縮し、さらに活性値を平均4ビット級へ下げる事後学習量子化（Post-学習 量子化; PTQ）の研究である。ここではFP16の23.70トークン/秒に対しTWLAが86.35トークン/秒を示した。

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  BF16重みの指数を固定長ビットマップへ無損失符号化し、圧縮データをレジスタ上で復元してテンソル Coreへ直送することで、重み帯域と中間展開の読み書きを減らす。

- **2026-08 · [Attend to Your Own Thoughts: Breaking the Barrier for Post-Training Quantization of Reasoning LLMs through the Lens of 1.58-Bit Quantization](2026-2608.01078-attend-to-your-own-thoughts-breaking-the-barrier-for-post-training-quant.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：2  
  大規模言語モデルの推論では重みの転送量と記憶容量が実行費用を決める重要な要因である。16ビットの重みを4ビットへ圧縮すれば容量を減らせるが、さらに1.58ビット相当の三値表現へ落とすと、数学の途中計算やコード生成など、複数段階の推論を必要とする課題の精度が大きく失われる。

- **2026-05 · [OSAQ: Outlier Self-Absorption for Accurate Low-bit LLM Quantization](2026-2605.04738-osaq-outlier-self-absorption-for-accurate-low-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、大規模言語モデル（Large Language モデル, LLM）の学習後量子化（Post-学習 量子化, PTQ）で、重みの少数の外れ値が量子化刻みを粗くする問題を扱う。これは約42.4%のPPL低下だが、元のFP16モデルのPPL5.47には遠い。

- **2026-05 · [ADMM-Q: An Improved Hessian-based Weight Quantizer for Post-Training Quantization of Large Language Models](2026-2605.11222-admm-q-an-improved-hessian-based-weight-quantizer-for-post-training-quan.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  しかし学習後量子化（Post-学習 量子化; PTQ）では、元の重みを単純に最も近い離散値へ丸めると、層の出力誤差が蓄積して言語モデルの品質が低下する。

- **2026-04 · [Rethinking Residual Errors in Compensation-based LLM Quantization](2026-2604.07955-rethinking-residual-errors-in-compensation-based-llm-quantization.md)**  
  実装：[✓](https://github.com/list0830/ResComp) ・ リポジトリ内被引用：2  
  GPTQなどの学習後量子化（Post-学習 量子化; PTQ）は、線形層の重みを一列ずつ低ビット化し、量子化によって失われる出力を残りの未量子化重みの更新で補償する。Llama3.1-8B-InstructのGPTAQではゼロショット6課題平均70.3%→72.3%となった。

- **2026-01 · [What Makes Low-Bit Quantization-Aware Training Work for Reasoning LLMs? A Systematic Study](2026-2601.14888-what-makes-low-bit-quantization-aware-training-work-for-reasoning-llms-a.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  数学やコード生成を得意とする推論特化型の大規模言語モデルでは、低ビット量子化が通常の自然言語課題より大きな品質低下を引き起こすことがある。Qwen3-0.6Bの重み3ビット・群サイズ128の設定では、MATH-500正答率がGPTQの13.27%からReasoning-QATの57.80%へ改善した。

- **2026-09 · [OBC-Prune: Outcome-Based Calibration for Large Reasoning Model Pruning](2026-2609.17890-obc-prune-outcome-based-calibration-for-large-reasoning-model-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  正答・誤答の思考過程を同一問題で対にし、文ごとの因果的寄与で較正活性値を再重み付けすることで、一発枝刈り後の推論精度と停止挙動を改善する。

- **2026-09 · [Beyond Scalar Sensitivity: Activation-Aware Mixed-Precision LLM Quantization with Cross-Layer Refinement](2026-2609.25916-beyond-scalar-sensitivity-activation-aware-mixed-precision-llm-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルを低メモリで推論するために重みを量子化する際、全ての行列へ同じビット幅を適用する必要はない。Llama-3-8Bで平均2.25ビット／重みの場合、既存のQ-PaletteのWikiText-2パープレキシティ47.20に対してCASAは22.41、6課題平均正解率34.0%に対して39.2%だった。

- **2026-08 · [SSDi8: Accurate and Efficient 8-bit Quantization for State Space Duality](2026-2608.21952-ssdi8-accurate-and-efficient-8-bit-quantization-for-state-space-duality.md)**  
  実装：[✓](https://github.com/cau-hai-lab/SSDi8) ・ リポジトリ内被引用：1  
  Mamba-2の構造化状態空間双対の内部状態をINT8のまま受け渡すため、再帰計算の式を並べ替え、異なる軸の分布に合わせて量子化する方式を示す。

- **2026-07 · [KronQ: LLM Quantization via Kronecker-Factored Hessian](2026-2607.07964-kronq-llm-quantization-via-kronecker-factored-hessian.md)**  
  実装：[✓](https://github.com/Intelligent-Computing-Lab-Panda/KronQ) ・ リポジトリ内被引用：1  
  大規模言語モデル（large language モデル; LLM）の重みを16ビットから4ビット、3ビット、2ビットへ縮小すると、メモリ占有と重み読出し帯域を削減できる。一方、単純な丸めでは、重要なチャネルの誤差が後段へ蓄積し、特に2ビット量子化で生成品質が崩れる。

- **2026-06 · [MosaicQuant: Inlier–Outlier Disaggregation for Unified 4-Bit LLM Quantization](2026-2606.15652-mosaicquant-inlier-outlier-disaggregation-for-unified-4-bit-llm-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの行列演算を高速化するため、重みと活性値を低ビット化するとメモリ転送量と演算費用を減らせる。従来の混合精度方式は外れ値のあるチャネルや低ランク成分を8～16ビットで保持するが、別精度の行列演算や変換・転送が発生し、低ビットの演算器を一貫して使う利点が減る。

- **2026-06 · [LiftQuant: Continuous Bit-Width LLM via Dimensional Lifting and Projection](2026-2606.04050-liftquant-continuous-bit-width-llm-via-dimensional-lifting-and-projectio.md)**  
  実装：[✓](https://github.com/Heliulu/LiftQuant) ・ リポジトリ内被引用：1  
  LLMの重み量子化はGPUメモリ消費を減らす有力な方法だが、多くの方式は2ビット、3ビット、4ビットといった整数の量子化幅を単位にする。たとえば70Bモデルの3ビット版が24GBのGPUへ収まらず、2ビット版なら大きな余裕が残る場合、空いた容量を精度向上へ使いにくい。

- **2026-05 · [HARP: Hadamard-Preconditioned Adaptive Rotation Processor for Extreme LLM Quantization](2026-2605.29843-harp-hadamard-preconditioned-adaptive-rotation-processor-for-extreme-llm.md)**  
  実装：[✓](https://github.com/brain-lab-research/HARP) ・ リポジトリ内被引用：1  
  重みを2～4ビットへ圧縮する事後量子化（Post-学習 量子化; PTQ）では、少数の大きな外れ値や入力方向ごとに異なる誤差感度のため、単純な丸めが深刻な品質劣化を招く。

- **2026-05 · [Fitting Is Not Enough: Smoothness in Extremely Quantized LLMs](2026-2605.08894-fitting-is-not-enough-smoothness-in-extremely-quantized-llms.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/FINE) ・ リポジトリ内被引用：1  
  極低ビットの大規模言語モデル（LLM）量子化では、元の浮動小数点モデルと量子化モデルの中間出力を近付ける「順方向の再構成誤差」が一般的な最適化対象である。

- **2026-05 · [EdgeRazor: A Lightweight Framework for Large Language Models via Mixed-Precision Quantization-Aware Distillation](2026-2605.04062-edgerazor-a-lightweight-framework-for-large-language-models-via-mixed-pr.md)**  
  実装：[✓](https://github.com/zhangsq-nju/EdgeRazor) ・ リポジトリ内被引用：1  
  対象は単なる事後量子化ではなく、量子化した生徒モデルを教師モデルで監督して再学習する混合精度量子化対応蒸留（Mixed-Precision Quantization-Aware Distillation; MPQAD）である。

- **2026-01 · [HESTIA: A Hessian-Guided Differentiable Quantization-Aware Training Framework for Extremely Low-Bit LLMs](2026-2601.20745-hestia-a-hessian-guided-differentiable-quantization-aware-training-frame.md)**  
  実装：[✓](https://github.com/hestia2026/Hestia) ・ リポジトリ内被引用：1  
  重みを{-1,0,+1}の三値に制限する1.58ビット級の量子化は、重み保存量や乗算器への要求を減らせる可能性がある。

### 直近12か月・未被引用（2025-12〜2026-11）

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

- **2026-09 · [Security-Enhanced Seed-Based Weight Quantization for Large Language Models](2026-2609.38477-security-enhanced-seed-based-weight-quantization-for-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの自己回帰デコードは重み転送に律速される場合があり、低ビット重みの保持だけでなく、圧縮した記号から演算時に重みを生成する方法が検討されている。

- **2026-09 · [Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution](2026-2609.09240-scaling-post-training-ternarisation-to-qwen3-8b-capability-retention-reproduction-lossless-packing-and-packed-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-8Bを適応的約1.64 bit/重みへ後量子化し、78.5%の補正済み能力保持、8.24 GiBの無損失packed artifact、RTX 5070上15.52 トークン/s・7.35 GiBの直接実行まで検証する。

- **2026-09 · [RGSQ: Riemannian Geometry-Sensitive Quantization for Large Vision-Language Models](2026-2609.25492-rgsq-riemannian-geometry-sensitive-quantization-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/RL-MIND/RGSQ) ・ リポジトリ内被引用：0  
  重みの学習後量子化（Post-学習 量子化; PTQ）は配備時のメモリ占有と転送帯域を減らせるが、視覚トークンと言語トークンの分布が異なるため、単一言語モデル向けの量子化手順をそのまま適用すると品質が崩れやすい。LLaVA-OneVision-7BのW4A8で、A800一枚における校正時間は2.1時間、ピークメモリは38GBである。

- **2026-09 · [QATFactory: A Versatile, Deployment-Aligned Framework for Quantization-aware Training and Distillation of LLMs](2026-2609.39223-qatfactory-a-versatile-deployment-aligned-framework-for-quantization-awa.md)**  
  実装：[✓](https://github.com/QATFactory/QATFactory) ・ リポジトリ内被引用：0  
  QATFactoryは、実際の推論エンジンが用いる量子化グリッド、ブロック構成、スケール階層、丸め規則を前向き計算に反映する。Qwen3.5-9Bの複数ベンチマーク平均正答率は、NVFP4では最良PTQの65.4%から68.9%へ、MXFP4では56.4%から66.0%へ改善した。

- **2026-09 · [Predicting Quantization Price for Selecting PTQ Configurations Before Deployment](2026-2609.28270-predicting-quantization-price-for-selecting-ptq-configurations-before-de.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習後量子化（Post-学習 量子化; PTQ）では、学習済みの大規模言語モデル（Large Language モデル; LLM）の重みを、少ないビット数で保存・計算できる表現に置き換える。

- **2026-09 · [Predict Before You Deploy: Offline Prediction of Quantization-Induced Task Degradation for World Action Models](2026-2609.19441-prede-quantization-task-degradation-prediction.md)**  
  実装：[✓](https://github.com/jiuyixu25/PreDE) ・ リポジトリ内被引用：0  
  PreDE（Predict Before You Deploy）は、世界行動モデル（World Action モデル、WAM）を学習後量子化したとき、候補ごとに高価な閉ループ試験を行う前に、タスク成功率の劣化を「受理・棄却・保留」の三値で予測する方式である。

- **2026-09 · [MiX: Micro-Inverted-Scaling for End-to-End Low-Bit Vision-Language Model Acceleration](2026-2609.19683-mix-micro-inverted-scaling-for-end-to-end-low-bit-vision-language-model-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VLMのマルチモーダル外れ値に対し、要素別指数＋共有仮数へマイクロスケーリングを反転し、4bit級の端から端までの量子化と乗算器不要のシフト加算PEを同時に実現する。

- **2026-09 · [KBBQ: A Predictive Noise Law and the Limits of Spectrum Flattening in FP4 Quantization](2026-2609.08135-kbbq-a-predictive-noise-law-and-the-limits-of-spectrum-flattening-in-fp4.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みと活性化をともに4ビットに落とす量子化（W4A4）では、表現範囲を共有するブロック内の外れ値と丸め誤差がモデル精度を損なう。4つの基盤モデルと2種類の4ビット浮動小数点形式を用いた8組の実験で、単純丸めにKBBQを組み合わせる方式は、同じ設定の完全平坦化方式WUSHを7組で上回った。

- **2026-09 · [G²PTQ: Improving LLM Post-Training Quantization with Generalized Gradient Compensation](2026-2609.31009-g-ptq-improving-llm-post-training-quantization-with-generalized-gradient.md)**  
  実装：[✓](https://github.com/G2PTQ/G2PTQ) ・ リポジトリ内被引用：0  
  G²PTQは、学習済み大規模言語モデル（LLM）の重みを低ビットへ変換する学習後量子化（post-学習 量子化、PTQ）を、量子化途中のモデル状態に応じて誤差補償を更新する処理として再設計した研究である。

- **2026-09 · [FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators](2026-2609.04724-flexposit-tunable-fractional-precision-for-llm-inference-accelerators.md)**  
  実装：[✓](https://github.com/hplp/FlexPosit) ・ リポジトリ内被引用：0  
  LLMの重み量子化には、精度を保つために細かいグループごとに倍率を持つ方式と、ハードウェア実装しやすいチャネル単位の方式がある。

- **2026-09 · [Faster Block-Diffusion Serving with Distribution-Free Risk Guarantees](2026-2609.33887-faster-block-diffusion-serving-with-distribution-free-risk-guarantees.md)**  
  実装：[✓](https://github.com/js-lee-AI/Redline) ・ リポジトリ内被引用：0  
  高速設定ほど未確定なトークンを早く確定する傾向があり、正答率の低下が問題になる。提案方式Redlineは、候補となる複数の推論設定を較正用の質問集合で実行し、基準設定が正解し候補設定が不正解となる件数を数える。

- **2026-09 · [Breaking the 1.58-bit Barrier for Ternary LLMs](2026-2609.16338-breaking-the-1-58-bit-barrier-for-ternary-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値重みのゼロ偏りを利用するBITCOSで格納量を最小1.485ビット/重みまで下げ、専用CPU・Xe2復号で一要求デコードを最大1.27倍高速化する。

- **2026-09 · [All for 1-Bit: Towards Genuine 1-Bit Post-Training Quantization for LLMs](2026-2609.06161-all-for-1-bit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  All for 1-Bit（AF1）は、既存の「1ビット」学習後量子化が尺度、外れ値、グループ情報などの補助データを含めると実効2〜4ビット/重みへ膨らむ問題に対し、対象線形重みを実効1.0ビット/重みに収める学習後量子化方式である。

- **2026-08 · [SchurQuant: Groupwise Discrete Optimization for Layer-Wise LLM Quantization](2026-2608.15567-schurquant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを4ビットから2〜3ビットへ縮めると、量子化格子の段数が少なくなり、各層の誤差が累積して言語モデルの予測を壊す。Llama2、Llama3、Qwen3の計8モデルを比較した2ビットの六課題平均ゼロショット精度は、SchurQuantが50.83%、GPTQが39.25%、QEPが41.18%である。

- **2026-08 · [SandwichQuant: Which Parameters Matter Before and After Quantization?](2026-2608.24173-sandwichquant-which-parameters-matter-before-and-after-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事後量子化（Post-学習 量子化; PTQ）の品質を回復する研究では、重み、量子化尺度、丸め、局所再構成などを調整する。Llama2-7B、Llama3-8B、Qwen3-8Bなどの強い量子化条件で一貫して改善し、Llama2-7BのW2A4KV4条件では比較構成の平均6タスク精度48.9を55.1へ改善する一方、推論時の追加演算子は増やさない。

- **2026-08 · [ReRound: Reconstructive Rounding to Resolve Midpoint Ambiguity in Calibration-Free LLM Quantization](2026-2608.11045-reround-reconstructive-rounding-to-resolve-midpoint-ambiguity-in-calibra.md)**  
  実装：[✓](https://github.com/louisYen/ReRound) ・ リポジトリ内被引用：0  
  この研究が変更するのは量子化スケールそのものではなく、既に決められた量子化区間の下側整数・上側整数のどちらを選ぶかという最終段階である。例えばGemma 2 2Bの4ビット条件で、四つのゼロショット課題の平均正答率はグループ別RTNの66.4%から67.4%へ上昇した。

- **2026-08 · [Recurrent Residual Quantization: A Progressive Multi-Precision Representation for LLMs](2026-2608.04048-recurrent-residual-quantization-a-progressive-multi-precision-representa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  回帰残差量子化（Recurrent Residual Quantization、RRQ）は、大規模言語モデルの重みを、低ビットの基底表現と複数の量子化残差へ分解することで、単一の保存パッケージから複数の実効精度を選べる後学習量子化（Post-学習 量子化、PTQ）の方式である。

- **2026-08 · [PRQuant: Permutation Residual Quantization for Low-Overhead Inference](2026-2609.22106-prquant-permutation-residual-quantization-for-low-overhead-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PRQuantは、言語モデルの線形層を重み・活性値とも4ビット相当で実行する際、少数の外れ値経路が精度を左右する問題を扱う。特に微小尺度浮動小数点4ビット形式（MXFP4）では小ブロックが共通尺度を持ち、ブロック内の一部の大きな値に尺度を合わせると、それ以外の値の量子化刻みが粗くなる。

- **2026-08 · [HBQ: Hierarchical Scaling Block Quantization with Hardware-Efficiency-Aware Design for Accurate LLM Inference](2026-2609.00450-hbq-hierarchical-scaling-block-quantization-with-hardware-efficiency-awa.md)**  
  実装：[✓](https://github.com/SeoLabCornell/HBQ) ・ リポジトリ内被引用：0  
  LLMの重みだけを4ビット化する重み-only 量子化（WoQ）は、モデル重みのメモリ帯域を節約できるが、活性値と注意計算のKVキャッシュには高精度のデータパスが残る。

- **2026-08 · [FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy](2026-2608.15602-fluxbin-lut-ultra-low-bit-inference.md)**  
  実装：[✓](https://github.com/nicyyyy/FluxBin) ・ リポジトリ内被引用：0  
  重要列だけをヘッセ行列で選んで追加二値基底を与え、逆量子化を避けるLUT融合CUDAカーネルで約2〜3ビットLLMを実行し、A100で最大5.92倍高速化・10.19倍省エネルギーを報告する。

- **2026-08 · [FlashQuant: Sparse-Dense Fusion for Memory-Efficient Outlier-Aware LLM Inference](2026-2608.15531-flashquant-sparse-dense-fusion-for-memory-efficient-outlier-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashQuantは、大規模言語モデルの重み4ビット・活性値16ビット量子化（W4A16）で生じる「低精度の密行列積と、高精度で残した少数の外れ値による疎行列積を別々に実行する」という問題を、GPUカーネルの内部構造から解決する研究である。BF16のcuBLASに対するカーネル高速化は2.74〜4.18倍だが、これは4ビット量子化の効果も含む。

- **2026-08 · [FAMPWQ: Fisher Information-based Adaptive Mixed Precision Weight Quantization for Effective LLM Inference](2026-2608.24945-fampwq-fisher-information-based-adaptive-mixed-precision-weight-quantization-for-effective-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実量子化ノイズでFisher情報の層別感度を測り、PPOで全体ビット予算を層へ配分して、3〜4bit域の品質劣化を一様量子化より抑える。

- **2026-08 · [ARCHead: Activation-Metric Residual Correction for Large Language Model Output Heads](2026-2608.02703-archead-activation-metric-residual-correction-for-large-language-model-output-heads.md)**  
  実装：[✓](https://github.com/suayptalha/archead) ・ リポジトリ内被引用：0  
  ARCHeadは、大規模言語モデル（LLM）の最終出力射影（language-modeling head; LM-head）に特化した学習後圧縮方式である。語彙数が大きいモデルでは、この例外だけで数百MBから1GB以上の重みを保持する。

- **2026-08 · [AdaMX：異質性を考慮した低ビット・マイクロスケーリング](2026-2608.03867-heterogeneity-aware-microscaling-for-efficient-low-bit-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  4ビットのMXFP4はブロック単位の共有尺度で低ビット推論を実現するが、すべてのブロックへ同じ要素形式と精度回復方式を適用するため、量子化しやすさの違いを十分に利用できない。3B〜70BモデルでMXFP4が失う精度のうち常識推論で83%、MMLUで82%を回復し、NVFP4に対してもそれぞれ43%、27%の損失を回復する。

- **2026-07 · [BiSCo-LLM: Lookup-Free Binary Spherical Coding for Extreme Low-Bit Large Language Model Compression](2026-2607.08643-bisco-llm-lookup-free-binary-spherical-coding-for-extreme-low-bit-large-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BiSCo-LLMは、大規模言語モデル（LLM）の重みを2ビット級へ圧縮する際、単純なスカラー量子化では表現力が不足し、ベクトル量子化では明示的なコードブックの記憶容量と検索費用が増える問題に対処する研究である。BiSCo-LLMは較正データと元の重みから重要チャネルを選び、約1%を8ビットで保護する。

- **2026-06 · [SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving](2026-2606.11244-spear-error-adaptive-low-bit-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン適応型量子化誤差補償とカーネル・通信・SLOスケジューリングを共同設計し、W4–FP16のperplexity差を56–75%回復。

- **2026-06 · [QuBLAST: A Framework for Quantizing Large Language Models with Block-Level Compression Approach and Activation Scaling Strategy](2026-2606.04620-qublast-a-framework-for-quantizing-large-language-models-with-block-leve.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  QuBLASTは、既に学習済みの大規模言語モデルを再学習せずに圧縮する学習後量子化（post-学習 量子化; PTQ）の方法である。Qwen3-8B、Llama3-8B、Mistral v0.1-7B、Falcon H1R-7Bを対象に、重みの混合精度構成でモデル容量を40.0〜45.2%削減し、WikiText-2/103のPPL増加を5%以内に抑えた。

- **2026-06 · [Multi-Bitwidth Quantization for LLMs Using Additive Codebooks](2026-2606.12876-multi-bitwidth-quantization-for-llms-using-additive-codebooks.md)**  
  実装：[✓](https://anonymous.4open.science/r/DropbyDrop2026/) ・ リポジトリ内被引用：0  
  大規模言語モデルを異なる記憶容量の機器へ展開するとき、通常の学習後量子化（post-学習 量子化、PTQ）は3ビット、4ビット、5ビットといった精度ごとに別の圧縮モデルを作る必要がある。

- **2026-06 · [Minimizing the Hidden Cost of Scales: Graph-Guided Ultra-Low-Bit Quantization for Large Language Models](2026-2606.05429-minimizing-the-hidden-cost-of-scales-graph-guided-ultra-low-bit-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAGE-PTQ（Saliency-Aware Graph-guided Efficient Post-学習 量子化）は、LLM重みを1bit前後まで圧縮する際に見落とされがちな量子化スケールと重みグループの位置情報の費用を抑える方式である。

- **2026-06 · [GRINQH: Graded Input-based Quantization Hierarchy for Efficient LLM Generation](2026-2606.23419-grinqh-graded-input-based-quantization-hierarchy-for-efficient-llm-gener.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  後者、とりわけバッチ1では、大きな線形層の重みを毎トークン読み出すため帯域律速になりやすい。重みを一律に3ビットや4ビットへ量子化すると帯域は減るが、重要なチャネルの精度も同時に失われる。Qwen3-8BのRTX 4090上では、4ビットMARLINの最適化カーネルより約25%高速な、GSM8K品質とのパレート前線上の動作点を示す。

- **2026-05 · [The Quantization Benefits of Residual-Free Transformers](2026-2605.25880-the-quantization-benefits-of-residual-free-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Transformerの量子化を難しくする活性値の外れ値が、量子化器の選択だけでなくモデルの残差接続（Residual Connection）という構造に起因し得ることを示す。

- **2026-05 · [QAM-W: Joint 2D Codebook Quantization for LLM Weights via Hadamard Rotation and Activation-Aware Scaling](2026-2605.26339-qam-w-joint-2d-codebook-quantization-for-llm-weights-via-hadamard-rotati.md)**  
  実装：[✓](https://github.com/white07S/qam-w) ・ リポジトリ内被引用：0  
  通常のスカラー学習後量子化（scalar post-学習 量子化）は各重みをほぼ独立に離散値へ丸める。TinyLlama-1.1B、Qwen2.5-3B、Mistral-7Bの主比較では5.5ビット相当のQAM-WでWikiText-2のパープレキシティー（PPL）がBF16比+0.4%、+0.3%、+0.1%に留まる。

- **2026-05 · [MixFP4: Enhancing NVFP4 with Adaptive FP4/INT4 Block Representations](2026-2605.31035-mixfp4-enhancing-nvfp4-with-adaptive-fp4-int4-block-representations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixFP4は、4ビット浮動小数点（FP4）量子化で生じる精度低下を、同じ4ビットの中で表現方式を切り替えて緩和する研究である。テンソル Core相当の合成回路では面積3.1%、電力1.5%増に収まる。

- **2026-05 · [LAQuant: A Simple Overhead-free Large Reasoning Model Quantization by Layer-wise Lookahead Loss](2026-2605.08755-laquant-a-simple-overhead-free-large-reasoning-model-quantization-by-lay.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LAQuantは、数学やコード生成のように長い思考列を生成する大規模推論モデル（LRM）の重みのみの量子化を対象とする。Qwen3-4Bの3ビット重み・128要素グループ（W3G128）でAIME2025 Pass@1は54.69%。

- **2026-05 · [Influence-Inspired Spectral Rotations for Extreme Low-Bit LLM Quantization](2026-2605.25203-influence-inspired-spectral-rotations-for-extreme-low-bit-llm-quantizati.md)**  
  実装：[✓](https://github.com/gogipav14/spectral-llm) ・ リポジトリ内被引用：0  
  この論文は、LLMの重みを極端に少ないビット数へ丸めるとき、同じ量子化グループ内でも出力に強く影響する方向を優先して精度を残す方法を検討する。ただし4ビットではQwen2.5-1.5BのPPLが9.65から9.71となり、評価ノイズの範囲で改善が見られない。

- **2026-05 · [GPTQ-intrinsic LoRA: A Near-optimal Algorithm for Low-precision Quantization with Low-rank Adaptation](2026-2606.01412-gptq-intrinsic-lora-a-near-optimal-algorithm-for-low-precision-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを3〜4ビットへ圧縮すると、各重みを丸める量子化誤差が積み重なり、困惑度や下流課題の品質が悪化する。

- **2026-05 · [GoQuant: Geometric Orthogonal Residual Projection for Multiplier-Reduced Power-of-Two Transformer Quantization](2026-2605.26092-goquant-geometric-orthogonal-residual-projection-for-multiplier-reduced-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerを低ビットで実行する際、重みを2の冪乗（Power-of-Two、PoT）に量子化すると、一般的な重み乗算をシフトと加算へ置き換えやすい。

- **2026-05 · [BCJR-QAT: A Differentiable Relaxation of Trellis-Coded Weight Quantization](2026-2605.10655-bcjr-qat-a-differentiable-relaxation-of-trellis-coded-weight-quantizatio.md)**  
  実装：[✓](https://github.com/Venugopalan2610/quant-2bit) ・ リポジトリ内被引用：0  
  BCJR-QATは、トレリス符号化量子化（Trellis-Coded Quantization; TCQ）を使うLLMの2ビット重み表現に対し、量子化認識学習（Quantization-Aware 学習; QAT）を適用する方法である。

- **2026-04 · [Supernodes and Halos: Loss-Critical Hubs in LLM Feed-Forward Layers](2026-2604.23475-supernodes-and-halos-loss-critical-hubs-in-llm-feed-forward-layers.md)**  
  実装：[✓](https://github.com/KempnerInstitute/nodelens) ・ リポジトリ内被引用：0  
  この研究は、LLMのフィードフォワード層（feed-順伝播 network、FFN）の中間チャネルを丸ごと削除する構造化枝刈り（structured 枝刈り）で、ある削除はほとんど害がないのに、別の削除はモデル品質を急激に崩壊させる理由を調べる。

- **2026-04 · [Robust Ultra Low-Bit Post-Training Quantization via Stable Diagonal Curvature Estimate](2026-2604.13806-robust-ultra-low-bit-post-training-quantization-via-stable-diagonal-curv.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  DASH-Qは、学習済み大規模言語モデル（LLM）の重みを2〜4ビットへ圧縮する際、少量の較正入力から推定した相関情報を過信すると量子化後の回答品質が壊れるという問題を扱う。

- **2026-04 · [Initialisation Determines the Basin: Efficient Codebook Optimisation for Extreme LLM Quantization](2026-2604.08118-initialisation-determines-the-basin-efficient-codebook-optimisation-for-.md)**  
  実装：[✓](https://github.com/kenno94-IK/aqlm-oaem) ・ リポジトリ内被引用：0  
  LLMを2ビット/重み（2 bpp）程度へ圧縮する際、各重みを独立に少数の整数へ丸めるスカラー量子化では品質低下が大きくなる。

- **2026-03 · [HALO: Hardware-Aware Quantization with Low Critical-Path-Delay Weights for LLM Acceleration](2026-2502.19662-halo-hardware-aware-quantization-with-low-critical-path-delay-weights-fo.md)**  
  実装：[✓](https://github.com/ecolab-nus/HALO) ・ リポジトリ内被引用：0  
  重みの数値精度を下げれば計算器やメモリの費用は小さくなる。HALOはこの差を量子化設計へ直接持ち込み、重要な重みを保護しつつ、残りの重みを回路遅延の短い離散値へ写像する。

- **2026-02 · [SFMP: Fine-Grained, Hardware-Friendly and Search-Free Mixed-Precision Quantization for Large Language Models](2026-2602.01027-sfmp-fine-grained-hardware-friendly-and-search-free-mixed-precision-quan.md)**  
  実装：[✓](https://github.com/Nkniexin/SFMP) ・ リポジトリ内被引用：0  
  重み量子化は、大規模言語モデル（LLM）の重みを16ビットなどの高精度形式から2～4ビット程度の表現へ圧縮し、GPUメモリ使用量を削減する。

- **2026-02 · [LittleBit-2: Maximizing the Spectral Energy Gain in Sub-1-Bit LLMs via Latent Geometry Alignment](2026-2603.00042-littlebit-2-maximizing-the-spectral-energy-gain-in-sub-1-bit-llms-via-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LittleBit-2は、学習済み大規模言語モデル（LLM）の重み行列を低ランクの二値因子に分解するLittleBit方式を改良し、二値化の直前に潜在空間を回転して量子化誤差を小さくする研究である。

- **2026-02 · [A Case Study of Selected PTQ Baselines for Reasoning LLMs on Ascend NPU](2026-2602.17693-a-case-study-of-selected-ptq-baselines-for-reasoning-llms-on-ascend-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は新規量子化法の提案ではなく、既存の事後量子化（PTQ）をHuawei Ascend 910Bへ移した場合の再現性と実装費用を測定する事例研究である。

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

- **2025-12 · [Efficient LLM Deployment in Consumer Electronics Applications via Resource-Aware and Salience-Guided Quantization](2025-38c6f5463687-efficient-llm-deployment-in-consumer-electronics-applications-via-resour.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全層を一律2ビットへ下げるとモデルは小さくなるが、重要な重みの量子化誤差によって生成品質が悪化し得る。

### 2年前（2024-12〜2025-11）

- **2025-04 · [SpinQuant: LLM quantization with learned rotations](2025-2405.16406-spinquant-llm-quantization-with-learned-rotations.md)**  
  実装：[✓](https://github.com/facebookresearch/SpinQuant) ・ リポジトリ内被引用：185  
  外れ値が低ビット量子化の誤差を大きくする問題に対して、全精度の機能を保つ旋回行列を学習し、重み・活性値・KVキャッシュの量子化に合わせる。

- **2025-04 · [HIGGS: Pushing the Limits of Large Language Model Quantization via the Linearity Theorem](2025-2411.17525-higgs-pushing-the-limits-of-large-language-model-quantization-via-the-li.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  HIGGSは、LLMの各重み行列を別々に量子化するとき、どの誤差指標を最小化すればモデル全体の予測品質を守れるのかを理論と実験の両面から扱う。GPU実装面では、RTX 4090でLlama-3.1-8Bの4ビットHIGGSをFLUTEカーネルで実行すると、バッチ1で139トークン/秒、FP16は57トークン/秒だった。

- **2025-11 · [DartQuant: Efficient Rotational Distribution Calibration for LLM Quantization](2025-2511.04063-dartquant-efficient-rotational-distribution-calibration-for-llm-quantiza.md)**  
  実装：[✓](https://github.com/CAS-CLab/DartQuant) ・ リポジトリ内被引用：10  
  DartQuantは、大規模言語モデル（LLM）の低ビット量子化で問題になる活性値の外れ値を、直交回転行列の校正によって緩和する方法である。時間比は約47倍、メモリ比は約10倍である。

- **2025-08 · [LMDeploy Accelerates Mixed-Precision LLM Inference with TurboMind](2025-2508.15601-efficient-mixed-precision-large-language-model-inference.md)**  
  実装：[✓](https://github.com/InternLM/lmdeploy) ・ リポジトリ内被引用：9  
  量子化された重みを行列積の直前に浮動小数点へ復号すると、復号命令と共有メモリへの転送が計算の待ち時間になる。既存の混合精度推論基盤に対して配信遅延を最大61%（平均30%）削減し、処理率を最大156%（平均58%）向上したと報告する。

- **2025-02 · [M-ANT: Efficient Low-bit Group Quantization for LLMs via Mathematically Adaptive Numerical Type](2025-2502.18755-m-ant-efficient-low-bit-group-quantization-for-llms-via-mathematically-a.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  一般的なINT4量子化は整数演算に向くが、各値の分布が一様でないと量子化誤差が大きくなる。専用アクセラレータのシミュレーションでは、先行するLLMアクセラレータに対して平均2.99倍、最大4.46倍の高速化と、平均2.81倍、最大4.10倍のエネルギー削減を報告する。

- **2025-04 · [MiLo: Efficient Quantized MoE Inference with Mixture of Low-Rank Compensators](2025-2504.02658-milo-efficient-quantized-moe-inference-with-mixture-of-low-rank-compensa.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/MiLo) ・ リポジトリ内被引用：8  
  Mixtral-8×7Bの半精度重みは約90GBに達し、単一の40GBや80GBのGPUに収まりにくい。4ビット量子化は比較的品質を保てる一方、3ビットに下げると重みを表現できる値が減り、WikiText-2の予測性能が顕著に悪化する。論文はMixtral-8×7BとDeepSeek-MoEで精度を測り、A100 40GBで推論遅延も測定した。

- **2025-10 · [QSVD: Efficient Low-rank Approximation for Unified Query-Key-Value Weight Compression in Low-Precision Vision-Language Models](2025-2510.16292-qsvd-efficient-low-rank-approximation-for-unified-query-key-value-weight.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/QSVD) ・ リポジトリ内被引用：7  
  QSVDは、画像と文章を同時に処理する視覚言語モデル（Vision-Language モデル; VLM）の注意層で、問い合わせ（Query; Q）・鍵（Key; K）・値（Value; V）の射影重みを別々に圧縮するのではなく結合して低ランク分解する手法である。

- **2025-10 · [INT v.s. FP: A Comprehensive Study of Fine-Grained Low-bit Quantization Formats](2025-2510.25602-int-v-s-fp-a-comprehensive-study-of-fine-grained-low-bit-quantization-fo.md)**  
  実装：[✓](https://github.com/ChenMnZ/INT_vs_FP) ・ リポジトリ内被引用：7  
  しかし、32要素や16要素ごとに独立した尺度を持つ細粒度量子化では、外れ値と典型値を同じ広い範囲へ押し込める必要が小さくなる。ハードウェアの評価は論理回路モデルによる推定であり、MXINT8のエネルギーがMXFP8の0.63倍という数値を、既存GPUの実測消費電力や推論速度と混同してはならない。

- **2025-02 · [Huff-LLM: End-to-End Lossless Compression for Efficient LLM Inference](2025-2502.00922-huff-llm-end-to-end-lossless-compression-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Huff-LLMは、言語モデルの重みを数値を一切変えずに圧縮し、保存先から推論演算器の直前まで圧縮状態を維持する方式である。Llama、Qwen、OPT、Vicunaの重みで容量削減を測定し、専用推論回路のモデル化で最大約32%の重み容量削減、最大約31%の推論遅延短縮、最大約26%のエネルギー削減を報告する。

- **2025-09 · [PTQTP: Post-Training Quantization to Trit-Planes for Large Language Models](2025-2509.16989-ptqtp-post-training-quantization-to-trit-planes-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  PTQTPは、学習済み重みを2枚の三値平面（trit-plane）と連続尺度へ分解し、約1.58ビット級の超低ビット表現を事後量子化（Post-学習 量子化; PTQ）だけで作る。二値PTQより表現力を増やしつつ、混合精度の例外経路を使わず一様な三値演算へ落とすのが狙いである。

- **2025-05 · [DLP: Dynamic Layerwise Pruning in Large Language Models](2025-2505.23807-dlp-dynamic-layerwise-pruning-in-large-language-models.md)**  
  実装：[✓](https://github.com/ironartisan/DLP) ・ リポジトリ内被引用：5  
  DLP（動的 Layerwise 枝刈り、動的層別刈り込み）は、重みのどれを削るかだけでなく、各層に何割の重みを残すかを決めるためのモデル圧縮方式である。ただし同じ70%の疎化率でも、重要な層を一律に70%削ると、あまり重要でない層を多く削る場合より予測品質が大きく損なわれる。

- **2025-02 · [LO-BCQ: Locally Optimal Block Clustered Quantization for 4-bit (W4A4) LLM Inference](2025-2502.05376-lo-bcq-locally-optimal-block-clustered-quantization-for-4-bit-w4a4-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  主題は、大規模言語モデルの重みと活性値の両方を4ビット程度へ量子化し、再学習を行わずに推論品質を保つ事後量子化（Post-学習 量子化; PTQ）である。代表例としてLlama2-7Bの5つの言語理解課題平均では、BF16の65.65%に対し、実効4.5ビットのLO-BCQは64.68%となり、0.97ポイント低下した。

- **2025-05 · [ICQuant: Index Coding enables Low-bit LLM Quantization](2025-2505.00850-icquant-index-coding-enables-low-bit-llm-quantization.md)**  
  実装：[✓](https://github.com/Avery-xl/ICQuant) ・ リポジトリ内被引用：4  
  ICQuant（Index Coding enables Low-bit LLM Quantization）は、大規模言語モデル（LLM）の重みを2〜3ビット程度へ圧縮する際、少数の極端な値が量子化範囲を不必要に広げる問題を、外れ値の分離と位置索引の効率的な符号化で解く学習後量子化（Post-学習 量子化; PTQ）方式である。

- **2025-05 · [Addition is almost all you need: Compressing large language models with double binary factorization](2025-2505.11076-addition-is-almost-all-you-need-compressing-large-language-models-with-d.md)**  
  実装：[✓](https://github.com/usamec/double_binary) ・ リポジトリ内被引用：4  
  大規模言語モデルの重みを低ビット化すると、モデルの保存容量とメモリ帯域要求を減らせる。ただし一般的な量子化は、実行時に低ビットの重みを展開して高精度の積和演算を行うことが多い。RTX4090でのバッチ1復号では、Llama3-8BのFP16 60 トークン/sに対して2bit DBFが133 トークン/s、約2.22倍となる。

- **2025-04 · [OAC: Output-adaptive Calibration for Accurate Post-training Quantization](2025-2405.15025-oac-output-adaptive-calibration-for-accurate-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重みを2ビットあるいは1ビットに圧縮すると、元の浮動小数点重みを丸める際の誤差が大きくなり、通常の層単位の校正だけではモデルの最終予測が著しく悪化する。

- **2025-09 · [Bi-VLM: Pushing Ultra-Low Precision Post-Training Quantization Boundaries in Vision-Language Models](2025-2509.18763-bi-vlm-pushing-ultra-low-precision-post-training-quantization-boundaries.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大きな重み容量と画像トークンの計算費用があるため、小型端末への配置が難しい。Bi-VLMは、事前学習済みの視覚言語モデルを再学習せずに極低ビット化するため、重みの分布を統計的な分位点で複数群へ分け、重要な外れ値重みには2bit、その他の多数の重みには1bitを割り当てる後学習量子化方式である。

- **2025-06 · [Unifying Uniform and Binary-coding Quantization for Accurate Compression of Large Language Models](2025-2506.03781-unifying-uniform-and-binary-coding-quantization-for-accurate-compression.md)**  
  実装：[✓](https://github.com/snudm-starlab/UniQuanF) ・ リポジトリ内被引用：3  
  UQは一定間隔に並んだ量子化レベルを使う。Llama-3 8B InstructのGSM8Kでは3ビットでUniQuanFが58.73%、FlexRoundが54.13%で、差は4.60パーセントポイント。

- **2025-01 · [BlockDialect: Block-wise Fine-grained Mixed Format Quantization for Energy-Efficient LLM Inference](2025-2501.01144-blockdialect-block-wise-fine-grained-mixed-format-quantization-for-energ.md)**  
  実装：[✓](https://code.stanford.edu/tambe-lab/blockdialect) ・ リポジトリ内被引用：3  
  著者らは、符号1ビットと値索引3ビットという4ビット格納形式を保ちつつ、16種類の表現可能値集合を用意するDialectFP4を提案する。LLaMA3-8Bで注意行列積まで含めて量子化した場合、最良のブロック混合設定では7課題平均正答率69.00%、比較対象のMXFP4-16は58.22%、全精度FP16は74.45%である（原著Table 1）。

- **2025-11 · [SpecQuant: Spectral Decomposition and Adaptive Truncation for Ultra-Low-Bit LLMs Quantization](2025-2511.11663-specquant-spectral-decomposition-and-adaptive-truncation-for-ultra-low-b.md)**  
  実装：[✓](https://github.com/Kishon-zzx/SpecQuant) ・ リポジトリ内被引用：2  
  本研究は、大規模言語モデル（LLM）の重みと活性を同時に4ビット程度へ圧縮するときに生じる、外れ値による量子化誤差を低減する手法を扱う。

- **2025-09 · [Quant-dLLM: Post-Training Extreme Low-Bit Quantization for Diffusion Large Language Models](2025-2510.03274-quant-dllm-post-training-extreme-low-bit-quantization-for-diffusion-larg.md)**  
  実装：[✓](https://github.com/ZTA2785/Quant-dLLM) ・ リポジトリ内被引用：2  
  本研究は、拡散型大規模言語モデル（diffusion large language モデル、以下dLLM）の重みを、追加の勾配学習なしに平均2ビットへ圧縮しながら、生成・推論課題の正答率を維持する手法を提案する。

- **2025-01 · [Pivoting Factorization: A Compact Meta Low-Rank Representation of Sparsity for Efficient Inference in Large Language Models](2025-2501.19090-pivoting-factorization-a-compact-meta-low-rank-representation-of-sparsit.md)**  
  実装：[✓](https://github.com/biomedical-cybernetics/pivoting-factorization) ・ リポジトリ内被引用：2  
  ランクが行列次元の半分の単層比較では、既存低ランク層から追加でメモリ24.2%・推論時間24.6%削減を報告。PIFAの無損失は元の低ランク近似に対する再表現の性質であり、密な原モデルを無損失圧縮するという意味ではない。

- **2024-12 · [RILQ: Rank-Insensitive LoRA-based Quantization Error Compensation for Boosting 2-bit Large Language Model Accuracy](2024-2412.01129-rilq-rank-insensitive-lora-based-quantization-error-compensation-for-boo.md)**  
  実装：[✓](https://github.com/aiha-lab/RILQ) ・ リポジトリ内被引用：2  
  重み量子化（重み 量子化）は、FP16などで保持していた行列を低ビット表現へ写像してモデルの重み記憶量を削減する。LLaMA-3-8BのQuIP#量子化では常識推論5課題平均が52.48%→60.61%、WikiText-2の困惑度（perplexity; PPL）が12.74→9.39となった。

- **2024-12 · [DecDEC: A Systems Approach to Advancing Low-Bit LLM Quantization](2024-2412.20185-decdec-a-systems-approach-to-advancing-low-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低ビット量子化（low-bit 量子化）は、LLMの重みを3ビット・4ビット程度へ圧縮し、GPUメモリと復号時の重み読出しを削減する。原著はRTX 4070 Super 12GBを含む5種類の一般消費者向けGPUで評価した。

- **2025-09 · [RSAVQ: Riemannian Sensitivity-Aware Vector Quantization for Large Language Models](2025-2510.01240-rsavq-riemannian-sensitivity-aware-vector-quantization-for-large-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  RSAVQ（Riemannian Sensitivity-Aware Vector Quantization）は、大規模言語モデル（LLM）の重みを2〜4ビット程度に圧縮するとき、量子化誤差がどの方向へ生じるかと、どの重みチャネルへ多くのビットを割くかを同時に最適化する学習後量子化（Post-学習 量子化; PTQ）方式である。

- **2025-05 · [RWKVQuant: Quantizing the RWKV Family with Proxy Guided Hybrid of Scalar and Vector Quantization](2025-2505.03803-rwkvquant-quantizing-the-rwkv-family-with-proxy-guided-hybrid-of-scalar-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Transformer向けに有効な学習後量子化（PTQ）をそのままRWKVへ移すと、重み分布と非線形演算の違いから精度が大きく落ちたり、量子化前後の変換演算が追加されたりする。

- **2025-05 · [DenoiseRotator: Enhance Pruning Robustness for LLMs via Importance Concentration](2025-2505.23049-denoiserotator-enhance-pruning-robustness-for-llms-via-importance-concen.md)**  
  実装：[✓](https://github.com/Axel-gu/DenoiseRotator) ・ リポジトリ内被引用：1  
  DenoiseRotatorは、大規模言語モデル（LLM）の枝刈り（枝刈り）を行う前に、どの重みが重要かという分布自体を変える方式である。推論時の速度も重要で、A100上のLLaMA3-8B単層では、密行列5.80ms、回転なし2:4疎行列4.37ms、回転を含む2:4疎行列4.69msだった。

- **2025-03 · [EfficientLLaVA:Generalizable Auto-Pruning for Large Vision-language Models](2025-2503.15369-efficientllava-generalizable-auto-pruning-for-large-vision-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  EfficientLLaVAは、画像と文章を扱う大規模視覚言語モデル（Large Vision-Language モデル; LVLM）の重みを、元の巨大な学習データを持たずに削減するための自動枝刈り方式である。

- **2025-11 · [Adaptive Layer-Wise Transformations for Post-Training Quantization of Large Language Models](2025-2511.17809-adaptive-layer-wise-transformations-for-post-training-quantization-of-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの事後量子化（post-学習 量子化、PTQ）では、重みと活性値を低ビット整数へ丸める際、少数の外れ値に量子化範囲が引きずられて通常値の分解能が不足する。

- **2025-10 · [Neural Weight Compression for Language Models](2025-2510.11234-neural-weight-compression-for-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Neural 重み Compression（NWC）は、LLMの重みを手作業で設計した一様量子化やHadamard回転だけで圧縮するのではなく、重み分布からencoderとdecoderを学習して圧縮する方式である。

- **2025-09 · [Fair-GPTQ: Bias-Aware Quantization for Large Language Models](2025-2509.15206-fair-gptq-bias-aware-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/upunaprosk/fair-gptq) ・ リポジトリ内被引用：0  
  LLMの重みを16bitから4bitへ量子化すると、パラメータ格納容量とデータ転送量を大幅に減らせる。著者らの主評価では、Mistral-v0.3-7B-InstructのUnQover（曖昧な属性質問での回答評価）が通常GPTQの33.30%からFair-GPTQの58.89%へ改善した。

- **2025-06 · [ROSAQ: Rotation-based Saliency-Aware Weight Quantization for Efficiently Compressing Large Language Models](2025-2506.13472-rosaq-rotation-based-saliency-aware-weight-quantization-for-efficiently-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ROSAQ（Rotation-based Saliency-Aware 重み 量子化）は、言語モデルの重みを3〜4bitへ圧縮するときに、すべての重みを一律に低精度化するのではなく、校正活性の主成分方向に沿った重要チャネルだけをFP16で保持する事後量子化方式である。

- **2025-06 · [Boost Post-Training Quantization via Null Space Optimization for Large Language Models](2025-2506.11044-boost-post-training-quantization-via-null-space-optimization-for-large-l.md)**  
  実装：[✓](https://github.com/zjq0455/q2n) ・ リポジトリ内被引用：0  
  重みだけを量子化すると、浮動小数点重みWと量子化後重みWqの間に数値差が生じる。しかしLLMの実際の出力誤差は、重みの差そのものではなく、入力活性Xに作用した (W−Wq)X によって決まる。

- **2025-05 · [Optimal Formats for Weight Quantisation](2025-2505.12988-optimal-formats-for-weight-quantisation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット重み量子化では、整数、浮動小数点、非一様コードブック、ブロック単位のスケーリング、外れ値の高精度保持など、数値表現の選択肢が多数ある。

- **2025-01 · [FBQuant: FeedBack Quantization for Large Language Models](2025-2501.16385-fbquant-feedback-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FBQuantは、LLMの重みのみを3/4ビットへ量子化するときに生じる誤差を、LoRA型の低ランク副枝で補償する方式である。FBQuantは主枝の復元・行列積と副枝のup投影を一つのCUDAカーネルに融合し、追加レイテンシの約60%を削減する。

### 3年前（2023-12〜2024-11）

- **2024-03 · [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](2024-2404.00456-quarot-outlier-free-4-bit-inference-in-rotated-llms.md)**  
  実装：[✓](https://github.com/spcl/QuaRot) ・ リポジトリ内被引用：238  
  QuaRotは、大規模言語モデル（LLM）の4ビット推論を難しくする活性値の外れ値を、高精度の例外チャネルへ逃がすのではなく、モデルの関数を変えない直交回転（orthogonal rotation）で多数の次元へ分散する量子化手法である。

- **2024-02 · [QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks](2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/quip-sharp) ・ リポジトリ内被引用：173  
  QuIP#は、学習済みの大規模言語モデルを再学習せずに2〜4ビット/重みへ圧縮する事後学習量子化（Post-学習 量子化、PTQ）である。試作推論実装はRTX 4090上で70Bの2ビット重みを32.74トークン/秒で生成し、実効メモリ帯域利用率56.84%を記録した（表5）。

- **2024-05 · [QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving](2024-2405.04532-qserve.md)**  
  実装：[✓](https://github.com/mit-han-lab/omniserve) ・ リポジトリ内被引用：120  
  QServeは、クラウド型の大規模言語モデル（LLM）サービングにおいて、重みを4ビットへ量子化してもGPU上の実行速度が期待ほど上がらない問題を、量子化アルゴリズムと推論カーネルの協調設計によって解く研究である。論文はこの量子化解除の費用が20〜90%に達する条件を示し、ビット数を減らすだけではサービング処理率を改善できないことを説明する。

- **2024-01 · [Extreme Compression of Large Language Models via Additive Quantization](2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md)**  
  実装：[✓](https://github.com/Vahe1994/AQLM) ・ リポジトリ内被引用：109  
  加算量子化による言語モデル圧縮（AQLM）は、重みの極低ビット量子化における「小さいモデルを高精度で保持した方が、巨大モデルを2ビットにするより良い」という従来の精度対容量の関係を改善する研究である。Llama 2 7B・13B・70B、Mixtral 8×7B、Mistral 7Bを評価する。

- **2024-01 · [SliceGPT: Compress Large Language Models by Deleting Rows and Columns](2024-2401.15024-slicegpt-compress-large-language-models-by-deleting-rows-and-columns.md)**  
  実装：[✓](https://github.com/microsoft/TransformerCompression) ・ リポジトリ内被引用：101  
  SliceGPTは、学習済みTransformerの埋め込み次元を減らす学習後圧縮である。代表的なLLaMA-2 70Bの25%削減では、A100 40GBで1トークン生成時間が125ミリ秒から110ミリ秒へ、必要GPUが4台から3台へ減った。

- **2024-06 · [DuQuant: Distributing Outliers via Dual Transformation Makes Stronger Quantized LLMs](2024-2406.01721-duquant-distributing-outliers-via-dual-transformation-makes-stronger-quantized-llms.md)**  
  実装：[✓](https://github.com/Hsu1023/DuQuant) ・ リポジトリ内被引用：75  
  巨大外れ値を外れ値誘導のブロック回転とジグザグ置換で分散し、4ビット重み・活性量子化の精度を改善しつつ、LLaMA2-7Bでプリフィル最大2.08倍・復号時メモリ3.50倍削減を示す。

- **2024-02 · [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](2024-2402.17764-the-era-of-1-bit-llms-all-large-language-models-are-in-1-58-bits.md)**  
  実装：✓ ・ リポジトリ内被引用：68  
  狙いは、学習済みFP16/BF16モデルを後から近似する事後学習量子化ではなく、モデル自体を極低bit表現へ適応させ、品質を維持したまま重み転送・行列積・メモリ容量の支配項を小さくすることにある。

- **2024-02 · [BiLLM: Pushing the Limit of Post-Training Quantization for LLMs](2024-2402.04291-billm-pushing-the-limit-of-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/BiLLM) ・ リポジトリ内被引用：62  
  ヘッセ感度で重要列を選び二値残差近似し、残りのベル形重み分布を最適分割して別々に二値化することで、再学習なしにLLM重みを約1.1ビットまで圧縮する。

- **2023-12 · [ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models](2023-2312.05821-asvd-activation-aware-singular-value-decomposition-for-compressing-large.md)**  
  実装：[✓](https://github.com/hahnyuan/ASVD4LLM) ・ リポジトリ内被引用：61  
  活性値認識型特異値分解（活性値-aware Singular Value Decomposition、ASVD）は、大規模言語モデル（LLM）の線形重みを追加学習なしで低ランク行列へ置き換える圧縮方式である。LLaMA-7BとLLaMA-2-7B/13Bで重み容量を10～30%削減する実験を行い、活性値を考慮しないSVDより大幅に良い困惑度を報告する。

- **2024-10 · [FlatQuant: Flatness Matters for LLM Quantization](2024-2410.09426-flatquant-flatness-matters-for-llm-quantization.md)**  
  実装：[✓](https://github.com/ruikangliu/FlatQuant) ・ リポジトリ内被引用：59  
  層ごとの学習可能アフィン変換を小さなクロネッカー積へ分解し量子化と融合して、LLaMA-3-70BのW4A4で精度低下1%未満とプリフィル最大2.3倍高速化を両立する。

- **2024-06 · [QTIP: Quantization with Trellises and Incoherence Processing](2024-2406.11235-qtip-quantization-with-trellises-and-incoherence-processing.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/qtip) ・ リポジトリ内被引用：51  
  ベクトル量子化（Vector Quantization, VQ）は複数重みをまとめて符号化するほど量子化効率が上がる一方、通常の符号帳は次元に対して指数的に巨大化する。QTIPは、符号帳を列挙せず有限状態の「トレリス」を使うことで、この次元の壁を外し、2bit級でも256次元の高次元量子化を実用的な復号コストで実現する。

- **2024-02 · [OneBit: Towards Extremely Low-bit Large Language Models](2024-2402.11295-onebit-towards-extremely-low-bit-large-language-models.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/OneBit) ・ リポジトリ内被引用：48  
  OneBitは、学習済み大規模言語モデル（LLM）の重みを極端に低いビット数で保存する際に生じる精度劣化を、線形層の表現形式そのものを変更することで緩和する研究である。査読版の表3では、LLaMA-7Bの重み保存量が13.5 GBから1.3 GBへ、LLaMA-13Bでは26.0 GBから2.2 GBへ減る。

- **2024-02 · [GPTVQ: The Blessing of Dimensionality for LLM Quantization](2024-2402.15319-gptvq-the-blessing-of-dimensionality-for-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：46  
  複数の重みを1ベクトルとして量子化し、代理ヘッセ行列（proxy Hessian）で量子化誤差を後続列へ補償する。Llama 3 8Bの約3.125 bit/value構成では、Snapdragon X Elite上で独自INT4実装よりモデル占有量を約19%減らし、23.81から26.15 トークン/sへ高速化する。

- **2024-01 · [SliM-LLM: Salience-Driven Mixed-Precision Quantization for Large Language Models](2024-2405.14917-slim-llm-salience-driven-mixed-precision-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：44  
  要素単位で重要重みだけ高精度に残すのではなく、重要度が空間的にまとまる性質を使ってグループ単位で1/2/3ビットを割り当てる。さらに各グループ内部の少数の重要要素を量子化器校正で重く扱い、LLaMA-7Bの2ビット級でWikiText2パープレキシティ14.58を達成する。

- **2024-02 · [BitDistiller: Unleashing the Potential of Sub-4-Bit LLMs via Self-Distillation](2024-2402.10631-bitdistiller-unleashing-the-potential-of-sub-4-bit-llms-via-self-distill.md)**  
  実装：[✓](https://github.com/DD-DuDa/BitDistiller) ・ リポジトリ内被引用：39  
  学習後量子化（post-学習 量子化、PTQ）は比較的低費用だが、低ビットでは誤差を修正しにくい。

- **2024-03 · [AffineQuant: Affine Transformation Quantization for Large Language Models](2024-2403.12544-affinequant-affine-transformation-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  スカラーの拡大縮小や平行移動に限られていた等価変換を、可逆な行列によるアフィン変換へ拡張する。変換を量子化前の重みへ掛け、逆変換を活性値側へ入れることで元の線形演算を保ったまま量子化しやすい座標系を学習し、LLaMA2-7BのW4A4でC4パープレキシティをOmniQuantの18.02から15.76へ改善する。

- **2024-05 · [PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM Compression](2024-2405.14852-pv-tuning-beyond-straight-through-estimation-for-extreme-llm-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  大規模言語モデルを1～2ビット/重みへ圧縮すると、モデルを小さなメモリへ収められる一方、量子化誤差によって予測品質が大きく低下する。Llama-2 7Bの約2.02ビット/重みではWikiText-2のパープレキシティ5.84、5課題平均正答率61.35%を報告し、同程度のQuIP#の6.19・57.51%を上回る。

- **2024-07 · [Compact Language Models via Pruning and Knowledge Distillation](2024-2407.14679-compact-language-models-via-pruning-and-knowledge-distillation.md)**  
  実装：[✓](https://github.com/NVlabs/Minitron) ・ リポジトリ内被引用：28  
  15Bを学習した後に8B・4Bを別々にゼロから学習する代わりに、Nemotron-4 15Bから注意ヘッド、MLP中間次元、埋め込み幅、必要に応じて層を構造枝刈りし、元15Bのロジットを教師にして短期間だけ知識蒸留（Knowledge Distillation; KD）する。

- **2024-03 · [IntactKV: Improving Large Language Model Quantization by Keeping Pivot Tokens Intact](2024-2403.01241-intactkv-improving-large-language-model-quantization-by-keeping-pivot-to.md)**  
  実装：[✓](https://github.com/ruikangliu/IntactKV) ・ リポジトリ内被引用：22  
  IntactKVは、低ビット量子化した大規模言語モデル（LLM）において、入力の最初に置かれる少数の支点トークン（pivot トークン）の鍵・値キャッシュ（KV キャッシュ）だけを高精度モデルから生成して保存する方式である。

- **2024-01 · [LLM-FP4: 4-Bit Floating-Point Quantized Transformers](2023-2310.16836-llm-fp4-4-bit-floating-point-quantized-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  4ビット浮動小数点（floating point; FP）の指数部構成とクリップ範囲を層ごとに探索し、活性値の大きなチャネル間分散はチャネル別指数バイアスを重みへ事前吸収して処理する。LLaMA-13Bの埋め込み・重み・活性値を4/4/4ビットにして、6つの常識推論タスク平均63.1を維持する。

- **2024-02 · [DB-LLM: Accurate Dual-Binarization for Efficient LLMs](2024-2402.11960-db-llm-accurate-dual-binarization-for-efficient-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：18  
  大規模言語モデルの重み量子化は、16ビット浮動小数点の重みを数ビットの離散値へ置き換え、モデル保存量と重み読み出し量を減らす。LLaMA-1-7Bでは平均重み疎性が62.8%となり、著者らの計算量モデルでは32トークン入力のFLOPsが通常2ビット量子化の37.3Gから29.8Gへ減る。

- **2023-12 · [CBQ: Cross-Block Quantization for Large Language Models](2023-2312.07950-cbq-cross-block-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  学習後量子化（Post-学習 量子化、PTQ）は、学習済み大規模言語モデルの重みや活性を少ないビット数で表現し、メモリ使用量や演算費用を下げる技術である。65Bの4ビット重み量子化を単一GPUで4.3時間で行ったという処理費用の報告はあるが、量子化後の推論速度を4.3倍にしたという意味ではない。

- **2024-02 · [LQER: Low-Rank Quantization Error Reconstruction for LLMs](2024-2402.02446-lqer-low-rank-quantization-error-reconstruction-for-llms.md)**  
  実装：[✓](https://github.com/ChengZhang-98/lqer) ・ リポジトリ内被引用：13  
  大規模言語モデルの重みを4ビットへ圧縮しても、実行時に半精度へ逆量子化してから行列積を計算するなら、重みの保存容量削減がそのまま演算器の省資源化につながるとは限らない。

- **2024-04 · [Mitigating the Impact of Outlier Channels for Language Model Quantization with Activation Regularization](2024-2404.03605-mitigating-the-impact-of-outlier-channels-for-language-model-quantizatio.md)**  
  実装：[✓](https://github.com/aninrusimha/qat-pretrain) ・ リポジトリ内被引用：8  
  本研究は、言語モデルの重みと活性値の両方を4ビット整数にするW4A4量子化を、事前学習の段階から成立させる方法を調べる。300Mモデルを後からQAT微調整した試験では、基準に対しパープレキシティが16%悪化したという負の結果が重要である。

- **2024-02 · [Accurate LoRA-Finetuning Quantization of LLMs via Information Retention](2024-2402.05445-accurate-lora-finetuning-quantization-of-llms-via-information-retention.md)**  
  実装：[✓](https://github.com/AI-Efficiency/IR-QLoRA) ・ リポジトリ内被引用：8  
  大規模言語モデルの重みを16ビットから4ビット以下へ縮めると、重みの保存量と推論時に必要な重み転送量を減らせる。量子化後の基盤重みを固定し、小さな低ランク適応行列だけを微調整するQLoRA系の方法でも、失われた情報を十分に取り戻せない場合がある。

- **2024-05 · [I-LLM: Efficient Integer-Only Inference for Fully-Quantized Low-Bit Large Language Models](2024-2405.17849-i-llm-efficient-integer-only-inference-for-fully-quantized-low-bit-large.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  I-LLMは、LLMの重みと活性値を低ビットへ量子化するだけでなく、注意機構のSoftmax、ゲート付き活性化のSwiGLU、RMSNormなどの非線形演算も整数演算へ置き換える学習後量子化（PTQ）方式である。

- **2024-11 · [ZipNN: Lossless Compression for AI Models](2024-2411.05239-zipnn-lossless-compression-for-ai-models.md)**  
  実装：[✓](https://github.com/zipnn/zipnn) ・ リポジトリ内被引用：6  
  ZipNNは、モデルの重みを変更せずに保存・転送時のバイト数を減らし、展開すると元の重みビット列を完全に復元する可逆圧縮（無損失 compression）である。論文表IIIのLlama 3.1（BF16）では、Zstd単体の圧縮後サイズが原寸の77.7%なのに対してZipNNは66.4%。

- **2024-05 · [Post Training Quantization of Large Language Models with Microscaling Formats](2024-2405.07135-post-training-quantization-of-large-language-models-with-microscaling-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  本論文は、大規模言語モデル（LLM）の事後量子化（post-学習 量子化, PTQ）で広く使われるSmoothQuant、活性認識重み量子化（AWQ）、勾配不要の重み誤差補償（GPTQ）を、ブロックごとに尺度を共有する微小尺度（microscaling, MX）形式へ拡張し、三方式の組合せと適用順序を体系的に評価した研究である。

- **2024-04 · [Cherry on Top: Parameter Heterogeneity and Quantization in Large Language Models](2024-2404.02837-cherry-on-top-parameter-heterogeneity-and-quantization-in-large-language.md)**  
  実装：[✓](https://github.com/wangitu/CherryQ) ・ リポジトリ内被引用：6  
  大規模言語モデル（LLM）の重みを一律に低ビットへ量子化すると、保存容量を減らせる反面、ごく少数の重要な重みに発生した誤差が出力品質を大きく損なう。

- **2024-06 · [LLMEasyQuant: Scalable Quantization for Parallel and Distributed LLM Inference](2024-2406.19657-llmeasyquant-scalable-quantization-for-parallel-and-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/NoakLiu/LLMEasyQuant) ・ リポジトリ内被引用：5  
  LLMEasyQuantは、大規模言語モデル（LLM）の学習後量子化を研究・実行するための統合基盤である。論文は、量子化方式の品質だけを比較しても、実行時のメモリ転送や通信、逆量子化が遅ければ推論の速度向上につながらないと考える。

- **2023-12 · [ZeroQuant(4+2): Redefining LLMs Quantization with a New FP6-Centric Strategy for Diverse Generative Tasks](2023-2312.08583-zeroquant-4-2-redefining-llms-quantization-with-a-new-fp6-centric-strate.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  4ビット整数量子化（INT4）が自由生成課題で不安定になる条件を測り、6ビット浮動小数点（FP6）の品質を、4+2ビットの格納・復号方式と指数バイアスの事前変換によって既存GPU上で利用する研究。

- **2024-06 · [BoA: Attention-aware Post-training Quantization without Backpropagation](2024-2406.13474-boa-attention-aware-post-training-quantization-without-backpropagation.md)**  
  実装：[✓](https://github.com/SamsungLabs/BoA) ・ リポジトリ内被引用：4  
  BoA（Backpropagation-free optimization for 注意機構-aware PTQ）は、大規模言語モデルの学習後量子化（post-学習 量子化、PTQ）で、重みの整数化に伴う性能低下を抑える手法である。

- **2024-10 · [SeedLM: Compressing LLM Weights into Seeds of Pseudo-Random Generators](2024-2410.10714-seedlm-compressing-llm-weights-into-seeds-of-pseudo-random-generators.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの自己回帰生成では、1トークンを生成するたびに大量の重みを読み出す必要があり、演算器の理論性能よりもDRAM帯域が制約になる場合がある。通常の低ビット量子化は、FP16などの重みを整数値へ写像して読み出し量を減らす。速度については、専用FPGA上の行列ベクトル積でFP16基準比3.67〜3.98倍のサイクル数削減を報告する。

- **2024-05 · [ReALLM: A general framework for LLM compression and fine-tuning](2024-2405.13155-reallm-a-general-framework-for-llm-compression-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  元の行列を16ビットで保存する代わりに、学習済みの小型デコーダ、量子化した埋め込み、コードブック、必要な逆置換、低ランク行列とスケールを保存する。

- **2024-02 · [FlattenQuant: Breaking Through the Inference Compute-bound for Large Language Models with Per-tensor Quantization](2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  FlattenQuantは、大規模言語モデル（LLM）の推論で、重みだけを低ビット化しても行列演算が半精度のまま残るという問題を解く後学習量子化（post-学習 量子化; PTQ）方式である。難点は、LLMの活性値に他のチャネルより20〜100倍程度大きい外れ値チャネルが存在することだ。

- **2024-02 · [SparseLLM: Towards Global Pruning for Pre-trained Language Models](2024-2402.17946-sparsellm-towards-global-pruning-for-pre-trained-language-models.md)**  
  実装：[✓](https://github.com/BaiTheBest/SparseLLM) ・ リポジトリ内被引用：1  
  大規模言語モデルの重みを間引く非構造化枝刈りは、モデルの保存容量と演算の理論上の非ゼロ要素数を減らせる。原著のOPT-1.3B、WikiText2、重みの80%を疎化した条件では、SparseGPTの困惑度69.67に対しSparseLLMは58.92である。

- **2024-09 · [Accumulator-Aware Post-Training Quantization for Large Language Models](2024-2409.17092-accumulator-aware-post-training-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が対象とするのは、量子化後の重み・活性化値を掛け合わせる演算ではなく、その積を多数足し込む累積器（accumulator）のビット幅である。

### 4年前（2022-12〜2023-11）

- **2023-06 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](2023-2306.00978-awq.md)**  
  実装：[✓](https://github.com/mit-han-lab/llm-awq) ・ リポジトリ内被引用：279  
  活性の大きい入力チャネルに対応する重みを等価スケーリングで保護し、全重みを均一な低ビット形式のまま高精度化する重み専用量子化とTinyChat実装。

- **2023-01 · [SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot](2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md)**  
  実装：[✓](https://github.com/IST-DASLab/sparsegpt) ・ リポジトリ内被引用：269  
  重みの絶対値が小さい順に削除する単純な枝刈りでは、巨大モデルであっても削除による層出力誤差が累積し、50%の疎化で性能が崩壊し得る。

- **2023-08 · [OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models](2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-m.md)**  
  実装：[✓](https://github.com/OpenGVLab/OmniQuant) ・ リポジトリ内被引用：229  
  大規模言語モデルの重みを16ビットから4ビット、3ビット、2ビットへ縮めると、保存容量と重み転送量を大きく削減できる。一方、極低ビットでは重みや活性値の少数の外れ値が量子化範囲を広げ、重要な値の量子化刻みが粗くなって出力品質が崩れる。LLaMA-2 7B～70Bは128個の校正系列とA100 40GB 1基で1～16時間の処理が可能と報告される。

- **2023-07 · [QuIP: 2-Bit Quantization of Large Language Models With Guarantees](2023-2307.13304-quip-2-bit-quantization-of-large-language-models-with-guarantees.md)**  
  実装：✓ ・ リポジトリ内被引用：197  
  重みと代理ヘッセ行列（proxy Hessian）の座標依存の偏りをランダム直交変換で崩してから、LDL分解に基づく適応丸めを行う。Llama 2 70Bでは2ビット重みでもWikiText2パープレキシティ6.326を保ち、同条件のOPTQの123.908から大幅に改善する。

- **2023-06 · [SqueezeLLM: Dense-and-Sparse Quantization](2023-2306.07629-squeezellm-dense-and-sparse-quantization.md)**  
  実装：[✓](https://github.com/SqueezeAILab/SqueezeLLM) ・ リポジトリ内被引用：177  
  二次感度に基づく非一様量子化と、外れ値・高感度重みだけをFP16疎行列へ逃がすDense-and-Sparse分解により、3-bit級でも品質を保ちながら重み転送量と生成遅延を削減する。

- **2023-06 · [SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression](2023-2306.03078-spqr-a-sparse-quantized-representation-for-near-lossless-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Vahe1994/SpQR) ・ リポジトリ内被引用：177  
  高感度な少数重みだけを十六ビット疎表現に逃がし、残りと量子化尺度を三〜四ビット化してほぼ無損失圧縮する混合重み表現。

- **2023-05 · [LLM-QAT: Data-Free Quantization Aware Training for Large Language Models](2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/LLM-QAT) ・ リポジトリ内被引用：164  
  LLM-QATは、学習後量子化（Post-学習 量子化: PTQ）では精度が大きく低下する低ビット領域に対し、量子化誤差を学習中に経験させる量子化対応学習（Quantization-Aware 学習: QAT）を大規模言語モデルへ適用する研究である。

- **2023-10 · [Atom: Low-bit Quantization for Efficient and Accurate LLM Serving](2023-2310.19102-atom-low-bit-quantization-for-efficient-and-accurate-llm-serving.md)**  
  実装：[✓](https://github.com/efeslab/Atom) ・ リポジトリ内被引用：122  
  外れ値チャネルだけ高精度に残して重み・活性・KVキャッシュを低ビット化し、再配置と融合カーネルで4ビットGPU演算器を直接使ってLLM配信を高速化する。

- **2023-06 · [OWQ: Outlier-Aware Weight Quantization for Efficient Fine-Tuning and Inference of Large Language Models](2023-2306.02272-owq-outlier-aware-weight-quantization-for-efficient-fine-tuning-and-infe.md)**  
  実装：[✓](https://github.com/xvyaward/owq) ・ リポジトリ内被引用：81  
  大規模言語モデルの重みを3ビット級へ圧縮すると、モデル容量と重み読出し量は減るが、わずかな量子化誤差が特定の特徴次元で増幅され、出力品質が大きく悪化することがある。

- **2022-12 · [The case for 4-bit precision: k-bit Inference Scaling Laws](2022-2212.09720-the-case-for-4-bit-precision-k-bit-inference-scaling-laws.md)**  
  実装：✓ ・ リポジトリ内被引用：74  
  量子化では、1パラメータ当たりのビット数を下げるほど同じ重みメモリへ大きなモデルを置ける。

- **2023-09 · [PB-LLM: Partially Binarized Large Language Models](2023-2310.00034-pb-llm-partially-binarized-large-language-models.md)**  
  実装：[✓](https://github.com/hahnyuan/BinaryLLM) ・ リポジトリ内被引用：55  
  重みを一律1ビット化するのではなく、ヘッセ行列で選んだ少数の顕著重みを高精度で残し、それ以外だけを±1へ二値化する。LLaMA-7Bでは顕著重み30%を残す量子化対応学習版が7つのゼロショット常識推論で平均66.9を達成し、10%まで減らしても60.6を保つ。

- **2023-04 · [Outlier Suppression+: Accurate quantization of large language models by equivalent and optimal shifting and scaling](2023-2304.09145-outlier-suppression-accurate-quantization-of-large-language-models-by-eq.md)**  
  実装：[✓](https://github.com/ModelTC/Outlier_Suppression_Plus) ・ リポジトリ内被引用：44  
  Outlier Suppression+（OS+）は、大規模言語モデルの活性値に現れる極端な外れ値が、事後量子化（Post-学習 量子化: PTQ）の精度を悪化させる問題に対する方法である。

- **2023-06 · [OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization](2023-olive-accelerating-large-language-models-via-hardware-friendly-outlier-victim-pair-quantization.md)**  
  実装：[✓](https://github.com/clevercool/ANT-Quantization) ・ リポジトリ内被引用：43  
  外れ値を別の疎データ構造へ逃がすのではなく、隣接する低重要度の通常値を「犠牲値（victim）」として使い、外れ値を同じ固定幅ペアの中へ埋め込む。これにより外れ値対応量子化で問題になる座標リストと別演算経路をなくし、4ビットの整列アクセスをテンソルコアやシストリック配列へ直接載せる。

- **2023-03 · [ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehen.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  ZeroQuant-V2は、大規模言語モデルの学習後量子化（Post-学習 量子化、PTQ）を、特定の一手法の成功例だけで評価するのではなく、量子化対象、数値精度、粒度、モデル系列、最適化方式を組み合わせて調べた研究である。元の16ビットモデルは10.33なので、この設定では測定上ほぼ同等となる。

- **2023-06 · [LoSparse: Structured Compression of Large Language Models based on Low-Rank and Sparse Approximation](2023-2306.11222-losparse-structured-compression-of-large-language-models-based-on-low-rank-and-sparse-approximation.md)**  
  実装：[✓](https://github.com/yxli2123/LoSparse) ・ リポジトリ内被引用：25  
  各重み行列を「全ニューロンに共有される低ランク成分」と「ニューロン固有の残差成分」に分け、残差側だけを構造枝刈りする。低ランク近似が表現力のある共通基底を守るため、高い枝刈り率でも通常の反復構造枝刈りより品質を落としにくい。

- **2023-05 · [Memory-Efficient Fine-Tuning of Compressed Large Language Models via sub-4-bit Integer Quantization](2023-2305.14152-memory-efficient-fine-tuning-of-compressed-large-language-models-via-sub.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  提案するPEQA（パラメータ-Efficient and 量子化-aware Adaptation）は、事前学習済みの重みを3～4ビットなどの整数表現へ量子化した後、整数値を凍結し、量子化尺度だけを学習する。

- **2023-02 · [With Shared Microexponents, A Little Shifting Goes a Long Way](2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  Rouhaniらは、ブロックデータ表現（Block Data Representation; BDR）という共通の設計枠を用意し、ブロックサイズ、尺度の階層、尺度を保存するビット数、各要素の仮数幅を変えて比較した。

- **2023-10 · [Dynamic Sparse No Training: Training-Free Fine-tuning for Sparse LLMs](2023-2310.08915-dynamic-sparse-no-training-training-free-fine-tuning-for-sparse-llms.md)**  
  実装：[✓](https://github.com/zyxxmu/DSnoT) ・ リポジトリ内被引用：13  
  DSnoT（動的 Sparse No 学習）は、既存の枝刈り手法で疎化した大規模言語モデル（Large Language モデル、LLM）を、勾配逆伝播も重み値の更新も行わずに改善する方法である。

- **2023-08 · [FineQuant: Unlocking Efficiency with Fine-Grained Weight-Only Quantization for LLMs](2023-2308.09723-finequant-unlocking-efficiency-with-fine-grained-weight-only-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  FineQuantは、大規模言語モデル（Large Language モデル; LLM）の重みだけを低ビット化し、活性値と積和演算は浮動小数点で実行する重み専用量子化（重み-only 量子化）の研究である。最大3.65倍の総処理量改善は、この三番目の複製数増加を含むノード全体の処理量であり、単一要求のトークン生成速度が3.65倍という意味ではない。

- **2023-10 · [E-Sparse: Boosting the Large Language Model Inference through Entropy-based N:M Sparsity](2023-2310.15929-e-sparse-boosting-the-large-language-model-inference-through-entropy-bas.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  こうした制約では重要な重みが同じ4要素のグループに集中すると、どれかを必ず削除しなければならず、言語モデルの品質が下がりやすい。残した重みの値を再学習・再最適化せずに疎性を作り、FasterTransformerへ統合した疎行列積（Sparse-GEMM）で実際の推論を高速化する。

- **2023-10 · [Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM](2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md)**  
  実装：[✓](https://github.com/ilur98/DGQ) ・ リポジトリ内被引用：2  
  しかし、重みを小さなグループ単位で4ビット量子化すると、グループごとに尺度が異なるため、整数の行列積を区切って浮動小数点で部分和を結合する必要が生じる。原著はLLaMA、LLaMA 2、OPTなどで困惑度とゼロショット推論精度を評価し、単一A100 80GBでの実行時間・メモリ使用量を測定した。

### 5年前（2021-12〜2022-11）

- **2022-10 · [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](2022-2210.17323-gptq.md)**  
  実装：[✓](https://github.com/IST-DASLab/gptq) ・ リポジトリ内被引用：585  
  二次情報に基づく誤差補償をGPU向けに再設計し、175B級LLMを数時間で3〜4bit化して単一A100実行と約3.24倍の生成高速化を実現した基礎的GPTQ研究。

- **2022-11 · [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/mit-han-lab/smoothquant) ・ リポジトリ内被引用：531  
  活性値全体を単純に8ビットへ写すと、その少数の外れ値が量子化範囲を広げ、通常値へ割り当てられる段階数が減って精度が崩れる。OPT、BLOOM、GLM、MT-NLGなどで8ビット重み・8ビット活性値（W8A8）を実現し、精度低下をほぼ抑えながら最大1.56倍の推論高速化と2倍のメモリ削減を報告し、530Bモデルを単一ノードで提供可能にした。

- **2022-11 · [LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](2022-2208.07339-llm-int8-8-bit-matrix-multiplication-for-transformers-at-scale.md)**  
  実装：[✓](https://github.com/TimDettmers/bitsandbytes) ・ リポジトリ内被引用：257  
  特徴次元の外れ値を16-bitへ分離し、残る99.9%以上をベクトル単位INT8で計算する。175B級モデルの品質とほぼ半減の重み容量を両立する一方、小さい行列では量子化費用が速度改善を打ち消す。

- **2022-06 · [ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers](2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：183  
  大規模言語モデルの量子化では、重みを16ビットから8ビットへ減らすだけでメモリ転送量は小さくなる。INT8では追加の学習や校正なしでBERT・GPT系の品質をほぼ保ち、NVIDIA A100上のBERT-baseで最大5.19倍、GPT-3 350Mで4.16倍の速度向上を示した。

### 6年前（2020-12〜2021-11）

- **2021-01 · [I-BERT: Integer-only BERT Quantization](2021-2101.01321-i-bert-integer-only-bert-quantization.md)**  
  実装：[✓](https://github.com/kssteven418/i-bert) ・ リポジトリ内被引用：42  
  Transformerの重みと行列積を8ビット整数へ量子化しても、推論全体が整数だけで実行できるとは限らない。Tesla T4上の予備的な整数カーネル実装では、FP32比で2.4～4.0倍の推論高速化を報告する。

- **2021-09 · [Block Pruning For Faster Transformers](2021-2109.04838-block-pruning-for-faster-transformers.md)**  
  実装：[✓](https://github.com/huggingface/nn_pruning) ・ リポジトリ内被引用：26  
  Block Pruningは移動量に基づく枝刈り（movement 枝刈り）を重みブロック単位へ拡張し、フィードフォワード層の次元や注意ヘッドを構造的に除去できる形へ誘導する。

- **2021-02 · [Accelerated Sparse Neural Training: A Provable and Efficient Method to Find N:M Transposable Masks](2021-2102.08124-accelerated-sparse-neural-training-a-provable-and-efficient-method-to-fi.md)**  
  実装：[✓](https://github.com/papers-submission/structured_transposable_masks) ・ リポジトリ内被引用：12  
  本研究は、この非対称性を解消する転置可能細粒度疎マスク（transposable fine-grained sparsity mask）を提案する。論文が示す「2倍」は主として疎テンソルコアの適用可能な行列積の範囲の比較であり、全学習時間の2倍高速化を実測したものと読み替えない。

### 7年前（2019-12〜2020-11）

- **2020-05 · [GOBO: Quantizing Attention-Based NLP Models for Low Latency and Energy Efficient Inference](2020-2005.03842-gobo-quantizing-attention-based-nlp-models-for-low-latency-and-energy-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：42  
  GOBOは、BERTなどの注意機構を使う自然言語処理モデルの重みを、学習後に大幅に圧縮する手法である。重みの約99.9%を少数の代表値への索引で表し、残る約0.1%の外れ値だけを元の32ビット浮動小数点のまま保持する。

- **2020-09 · [TernaryBERT: Distillation-aware Ultra-low Bit BERT](2020-2009.12812-ternarybert-distillation-aware-ultra-low-bit-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：27  
  TernaryBERTは、自然言語理解向けのBERTを極低ビットで実行可能な重み表現へ圧縮し、精度低下を知識蒸留（Knowledge Distillation）で抑える手法である。これにより重み2ビット・埋め込み2ビット・活性値8ビットの代表構成で、BERTの保存サイズを418MBから28MBへ減らす。

- **2020-04 · [Training with Quantization Noise for Extreme Model Compression](2020-2004.07320-training-with-quantization-noise-for-extreme-model-compression.md)**  
  実装：[✓](https://github.com/pytorch/fairseq/tree/master/examples/quant_noise) ・ リポジトリ内被引用：23  
  学習済みモデルの重みを低ビットや積量子化で保存すると、推論時の重み容量を減らせるが、各層で生じた量子化誤差が次層の入力へ蓄積し、精度が急激に落ちることがある。ICLR 2021の原著では、16層Transformerの942MBを反復積量子化で38MBへ圧縮した場合、量子化雑音なしのテスト困惑度25.2に対して20.7へ改善した。

- **2020-02 · [Compressing BERT: Studying the Effects of Weight Pruning on Transfer Learning](2020-2002.08307-compressing-bert-studying-the-effects-of-weight-pruning-on-transfer-lear.md)**  
  実装：[✓](https://github.com/mitchellgordon95/bert-prune) ・ リポジトリ内被引用：22  
  対象はBERT-Baseの非構造化重み枝刈りである。主結果は、30～40%程度の重みを削除しても下流性能がほぼ変わらない一方、40～60%では事前学習で獲得した情報の消失が、70%以上ではそれに加えて残存ネットワークの表現容量制約が効くという三つの領域である。
<!-- survey:auto:end -->
