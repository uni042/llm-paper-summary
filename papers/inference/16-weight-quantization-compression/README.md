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
## 自動生成の論文一覧（404本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/16-weight-quantization-compression/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-06 · [TWLA: Achieving Ternary Weights and Low-Bit Activations for LLMs via Post-Training Quantization](2026-2606.13054-twla-achieving-ternary-weights-and-low-bit-activations-for-llms-via-post.md)**  
  実装：[✓](https://github.com/Kishon-zzx/TWLA) ・ リポジトリ内被引用：8  
  TWLA（Ternarized Weights and Low-bit Activations）は、学習済み大規模言語モデル（LLM）の重みを三値へ圧縮し、さらに活性値を平均4ビット級へ下げる事後学習量子化（Post-学習 量子化; PTQ）の研究である。ここではFP16の23.70トークン/秒に対しTWLAが86.35トークン/秒を示した。

- **2026-06 · [CAT-Q: Cost-efficient and Accurate Ternary Quantization for LLMs](2026-2606.26650-cat-q-cost-efficient-and-accurate-ternary-quantization-for-llms.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：7  
  CAT-Qは、高精度で事前学習された大規模言語モデル（LLM）を、重みが負一・零・正一の三値しか取らない形式へ変換する学習後量子化（Post-学習 量子化; PTQ）方式である。235Bモデルの三値化にはA100 80GBを8枚使って最大60時間を要する。

- **2026-02 · [HiFloat4 Format for Language Model Inference](2026-2602.11287-hifloat4-format-for-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  4ビット浮動小数点を使うとモデル容量とメモリ転送を削減できるが、4ビットの中で符号・指数・仮数をすべて表すと、精度と数値範囲の両立が難しい。そこで複数要素で尺度を共有するブロック浮動小数点（Block Floating-Point; BFP）を利用する。尺度が階層化されるため、外れ値が一部の要素だけにある場合も群全体の量子化刻みを粗くしすぎずに済む。

- **2026-08 · [Attend to Your Own Thoughts: Breaking the Barrier for Post-Training Quantization of Reasoning LLMs through the Lens of 1.58-Bit Quantization](2026-2608.01078-attend-to-your-own-thoughts-breaking-the-barrier-for-post-training-quant.md)**  
  実装：[✓](https://github.com/IntelChina-AI/BitTern) ・ リポジトリ内被引用：6  
  大規模言語モデルの推論では重みの転送量と記憶容量が実行費用を決める重要な要因である。16ビットの重みを4ビットへ圧縮すれば容量を減らせるが、さらに1.58ビット相当の三値表現へ落とすと、数学の途中計算やコード生成など、複数段階の推論を必要とする課題の精度が大きく失われる。

- **2026-07 · [KronQ: LLM Quantization via Kronecker-Factored Hessian](2026-2607.07964-kronq-llm-quantization-via-kronecker-factored-hessian.md)**  
  実装：[✓](https://github.com/Intelligent-Computing-Lab-Panda/KronQ) ・ リポジトリ内被引用：6  
  大規模言語モデル（large language モデル; LLM）の重みを16ビットから4ビット、3ビット、2ビットへ縮小すると、メモリ占有と重み読出し帯域を削減できる。一方、単純な丸めでは、重要なチャネルの誤差が後段へ蓄積し、特に2ビット量子化で生成品質が崩れる。

- **2026-05 · [LoopQ: Quantization for Looped Language Models](2026-2605.16343-loopq-quantization-for-looped-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  従来の事後量子化（PTQ）は同一重みに同じ変換行列と尺度を適用し続けるため、周回ごとに活性化の大きさ・方向が変わると丸め誤差やクリッピングが生じる。W4A4条件で4バックボーンの5課題平均正答率は静的PTQ最良比較方式に対して相対平均67.8%改善し、8つのバックボーン×データセット条件のPPL相対減少は下限代入による保守的平均75.2%と報告した。

- **2026-04 · [GSQ: Highly-Accurate Low-Precision Scalar Quantization for LLMs via Gumbel-Softmax Sampling](2026-2604.18556-gsq-highly-accurate-low-precision-scalar-quantization-for-llms-via-gumbe.md)**  
  実装：[✓](https://github.com/IST-DASLab/GSQ) ・ リポジトリ内被引用：6  
  大規模言語モデルを2～3ビット程度に圧縮すると、重みの転送量と常駐メモリを大幅に減らせる。Llama-3.1-8B/70Bの2ビット評価で従来スカラー量子化より高い精度を示し、Qwen3-8Bの既存GGUF K-Quantチェックポイントを同じ保存形式のまま改善する点が実用上重要である。

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  BF16重みの指数を固定長ビットマップへ無損失符号化し、圧縮データをレジスタ上で復元してテンソル Coreへ直送することで、重み帯域と中間展開の読み書きを減らす。

- **2026-03 · [LatentLLM: Activation-Aware Transform to Multi-Head Latent Attention](2026-2505.18413-latentllm-activation-aware-transform-to-multi-head-latent-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  学習済みの多頭注意を、活性値共分散の平方根による最適な前処理、単位ブロック化する接続行列、クエリ・キーの共同分解で多頭潜在注意型へ学習なしに変換し、KVキャッシュと計算を減らす圧縮方式LatentLLM。

- **2026-08 · [SSDi8: Accurate and Efficient 8-bit Quantization for State Space Duality](2026-2608.21952-ssdi8-accurate-and-efficient-8-bit-quantization-for-state-space-duality.md)**  
  実装：[✓](https://github.com/cau-hai-lab/SSDi8) ・ リポジトリ内被引用：4  
  Mamba-2の構造化状態空間双対の内部状態をINT8のまま受け渡すため、再帰計算の式を並べ替え、異なる軸の分布に合わせて量子化する方式を示す。

- **2026-04 · [Rethinking Residual Errors in Compensation-based LLM Quantization](2026-2604.07955-rethinking-residual-errors-in-compensation-based-llm-quantization.md)**  
  実装：[✓](https://github.com/list0830/ResComp) ・ リポジトリ内被引用：4  
  GPTQなどの学習後量子化（Post-学習 量子化; PTQ）は、線形層の重みを一列ずつ低ビット化し、量子化によって失われる出力を残りの未量子化重みの更新で補償する。Llama3.1-8B-InstructのGPTAQではゼロショット6課題平均70.3%→72.3%となった。

- **2026-03 · [Fine-Grained Post-Training Quantization for Large Vision Language Models with Quantization-Aware Integrated Gradients](2026-2603.17809-fine-grained-post-training-quantization-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/ucas-xiang/QIG) ・ リポジトリ内被引用：4  
  重みと活性値を低ビット化すればメモリ使用量を抑えられるが、量子化誤差の影響は画像と文章という二つのモダリティの間だけでなく、同じモダリティ内の各トークンや層によっても異なる。著者はこれを1.60%の改善と説明するが、表の数値としては1.60ポイントの上昇である。

- **2026-01 · [What Makes Low-Bit Quantization-Aware Training Work for Reasoning LLMs? A Systematic Study](2026-2601.14888-what-makes-low-bit-quantization-aware-training-work-for-reasoning-llms-a.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  数学やコード生成を得意とする推論特化型の大規模言語モデルでは、低ビット量子化が通常の自然言語課題より大きな品質低下を引き起こすことがある。Qwen3-0.6Bの重み3ビット・群サイズ128の設定では、MATH-500正答率がGPTQの13.27%からReasoning-QATの57.80%へ改善した。

- **2026-01 · [Is Finer Better? The Limits of Microscaling Formats in Large Language Models](2026-2601.19026-is-finer-better-the-limits-of-microscaling-formats-in-large-language-mod.md)**  
  実装：[✓](https://github.com/iclr2016codeshare/microscaling) ・ リポジトリ内被引用：4  
  本論文は、大規模言語モデルの重みと活性を4ビット浮動小数点（FP4）へ圧縮する際、「量子化のブロックを小さくするほど精度が良くなる」という一般的な期待が破れる条件を明らかにした研究である。

- **2025-12 · [UniQL: Unified Quantization and Low-rank Compression for Adaptive Edge LLMs](2025-2512.03383-uniql-unified-quantization-and-low-rank-compression-for-adaptive-edge-ll.md)**  
  実装：[✓](https://github.com/enyac-group/UniQL) ・ リポジトリ内被引用：4  
  端末上で大規模言語モデル（LLM）を実行する際には、モデルの重みだけでなく、実行時の一時領域やほかのアプリケーションが共有するメモリも考慮する必要がある。4ビット量子化だけで端末に収まるモデルを作れても、別のアプリケーションが起動して空きメモリが減れば、固定サイズの量子化モデルは実行不能になる。

- **2026-08 · [H-Scale: Hessian-Guided Scale Refinement for NVFP4 Sub-Byte LLM Inference](2026-2608.28113-h-scale-hessian-guided-scale-refinement-for-nvfp4-sub-byte-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  H-Scaleは、NVIDIA Blackwell世代のGPUが直接扱える4ビット浮動小数点量子化形式（NVFP4）に対して、重みをどの4ビット値へ丸めるかではなく、16個の重みに共通して掛ける尺度をどう選ぶかに着目した学習後量子化（Post-学習 量子化; PTQ）の後処理である。

- **2026-05 · [Search Your Block Floating Point Scales!](2026-2605.12464-search-your-block-floating-point-scales.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ScaleSearchは、ブロック浮動小数点（Block Floating Point、BFP）形式で低ビット量子化するとき、各ブロックに共通する尺度（Scale）を最適化する方法である。これらは異なる評価対象の数値であり、尺度探索だけで全ての改善が生じたと見なしてはならない。

- **2026-05 · [HARP: Hadamard-Preconditioned Adaptive Rotation Processor for Extreme LLM Quantization](2026-2605.29843-harp-hadamard-preconditioned-adaptive-rotation-processor-for-extreme-llm.md)**  
  実装：[✓](https://github.com/brain-lab-research/HARP) ・ リポジトリ内被引用：3  
  重みを2～4ビットへ圧縮する事後量子化（Post-学習 量子化; PTQ）では、少数の大きな外れ値や入力方向ごとに異なる誤差感度のため、単純な丸めが深刻な品質劣化を招く。

- **2026-03 · [BATQuant: Outlier-resilient MXFP4 Quantization via Learnable Block-wise Optimization](2026-2603.16590-batquant-outlier-resilient-mxfp4-quantization-via-learnable-block-wise-o.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大規模言語モデル（LLM）や画像言語モデル（MLLM）の重み・活性化を4ビットへ量子化すれば、メモリ帯域と計算資源の負担を軽くできる可能性がある。マルチモーダル5課題の総合回復率はBF16比96.43%で、同条件のFlatQuant94.79%、GPTQ94.64%を上回る。

- **2026-02 · [ScaleBITS: Scalable Bitwidth Search for Hardware-Aligned Mixed-Precision LLMs](2026-2602.17698-scalebits-scalable-bitwidth-search-for-hardware-aligned-mixed-precision-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大規模言語モデル（LLM）の重みを4ビット未満に量子化すると、同じ平均ビット数でも、どの重みを低精度にするかによって予測品質が大きく変わる。第三に、行列積のタイルと整合する64×128重みブロックへ整数ビット幅を割り当て、勾配に基づく一括更新と受理判定で全モデルの平均容量予算へ近づける。

- **2026-09 · [Faster Block-Diffusion Serving with Distribution-Free Risk Guarantees](2026-2609.33887-faster-block-diffusion-serving-with-distribution-free-risk-guarantees.md)**  
  実装：[✓](https://github.com/js-lee-AI/Redline) ・ リポジトリ内被引用：2  
  高速設定ほど未確定なトークンを早く確定する傾向があり、正答率の低下が問題になる。提案方式Redlineは、候補となる複数の推論設定を較正用の質問集合で実行し、基準設定が正解し候補設定が不正解となる件数を数える。

- **2026-09 · [All for 1-Bit: Towards Genuine 1-Bit Post-Training Quantization for LLMs](2026-2609.06161-all-for-1-bit.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  All for 1-Bit（AF1）は、既存の「1ビット」学習後量子化が尺度、外れ値、グループ情報などの補助データを含めると実効2〜4ビット/重みへ膨らむ問題に対し、対象線形重みを実効1.0ビット/重みに収める学習後量子化方式である。

- **2026-08 · [SoftWater: Class-Aware Rate Allocation for Softmax Quantization](2026-2608.12026-softwater-class-aware-rate-allocation-for-softmax-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  通常の事後量子化では中間の線形層を2〜4ビットにしても、この最終出力層だけを16ビットで残すことが多い。例えばLlama-3.2-1Bの出力層は約2.63億パラメータ、モデル全体の21.3%であり、本体を低ビット化すると出力層の相対的な容量負担がさらに増える。

- **2026-08 · [Recurrent Residual Quantization: A Progressive Multi-Precision Representation for LLMs](2026-2608.04048-recurrent-residual-quantization-a-progressive-multi-precision-representa.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  回帰残差量子化（Recurrent Residual Quantization、RRQ）は、大規模言語モデルの重みを、低ビットの基底表現と複数の量子化残差へ分解することで、単一の保存パッケージから複数の実効精度を選べる後学習量子化（Post-学習 量子化、PTQ）の方式である。

- **2026-08 · [QTEA: Ternary LLMs with Sparse Residual Salient Weight and By-Column Optimization](2026-2609.00224-qtea-ternary-llms-with-sparse-residual-salient-weight-and-by-column-opti.md)**  
  実装：[✓](https://github.com/Intelligent-Microsystems-Lab/QTEA) ・ リポジトリ内被引用：2  
  全重み三値化に列単位の疎残差補償と再スケール改良、誤差減衰を組み合わせた2ビット未満の学習後量子化で、実効1.7ビットでも精度を大きく保ちFP16比7.2倍に高速化した。

- **2026-08 · [AdaMX：異質性を考慮した低ビット・マイクロスケーリング](2026-2608.03867-heterogeneity-aware-microscaling-for-efficient-low-bit-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  4ビットのMXFP4はブロック単位の共有尺度で低ビット推論を実現するが、すべてのブロックへ同じ要素形式と精度回復方式を適用するため、量子化しやすさの違いを十分に利用できない。3B〜70BモデルでMXFP4が失う精度のうち常識推論で83%、MMLUで82%を回復し、NVFP4に対してもそれぞれ43%、27%の損失を回復する。

- **2026-06 · [LiftQuant: Continuous Bit-Width LLM via Dimensional Lifting and Projection](2026-2606.04050-liftquant-continuous-bit-width-llm-via-dimensional-lifting-and-projectio.md)**  
  実装：[✓](https://github.com/Heliulu/LiftQuant) ・ リポジトリ内被引用：2  
  LLMの重み量子化はGPUメモリ消費を減らす有力な方法だが、多くの方式は2ビット、3ビット、4ビットといった整数の量子化幅を単位にする。たとえば70Bモデルの3ビット版が24GBのGPUへ収まらず、2ビット版なら大きな余裕が残る場合、空いた容量を精度向上へ使いにくい。

- **2026-05 · [ScaleSweep: Accurate NVFP4 Post-Training Quantization of LLMs via Block Scale Initialization](2026-2606.07618-scalesweep-accurate-nvfp4-post-training-quantization-of-llms-via-block-s.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ScaleSweepは、NVIDIA Blackwell世代でハードウェア対応するNVFP4の重み・活性値・KVキャッシュ・query状態の量子化について、16要素ブロックのFP8スケールの選び方を改善する後学習量子化（PTQ）手法である。これはBF16比約93.9%の平均性能回復である。

- **2026-05 · [OSAQ: Outlier Self-Absorption for Accurate Low-bit LLM Quantization](2026-2605.04738-osaq-outlier-self-absorption-for-accurate-low-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  本論文は、大規模言語モデル（Large Language モデル, LLM）の学習後量子化（Post-学習 量子化, PTQ）で、重みの少数の外れ値が量子化刻みを粗くする問題を扱う。これは約42.4%のPPL低下だが、元のFP16モデルのPPL5.47には遠い。

- **2026-05 · [MixFP4: Enhancing NVFP4 with Adaptive FP4/INT4 Block Representations](2026-2605.31035-mixfp4-enhancing-nvfp4-with-adaptive-fp4-int4-block-representations.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  MixFP4は、4ビット浮動小数点（FP4）量子化で生じる精度低下を、同じ4ビットの中で表現方式を切り替えて緩和する研究である。テンソル Core相当の合成回路では面積3.1%、電力1.5%増に収まる。

- **2026-05 · [IO-SVD: Input-Output Whitened SVD for Adaptive-Rank LLM Compression](2026-2605.15626-io-svd-input-output-whitened-svd-for-adaptive-rank-llm-compression.md)**  
  実装：[✓](https://github.com/mint-vu/IO-SVD) ・ リポジトリ内被引用：2  
  特異値分解（Singular Value Decomposition; SVD）による学習後圧縮は、密な線形層の重み行列を低階数の二つの因子に分け、保存量と乗算量を減らす手法である。

- **2026-05 · [ADMM-Q: An Improved Hessian-based Weight Quantizer for Post-Training Quantization of Large Language Models](2026-2605.11222-admm-q-an-improved-hessian-based-weight-quantizer-for-post-training-quan.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  しかし学習後量子化（Post-学習 量子化; PTQ）では、元の重みを単純に最も近い離散値へ丸めると、層の出力誤差が蓄積して言語モデルの品質が低下する。

- **2026-03 · [SliderQuant: Accurate Post-Training Quantization for LLMs](2026-2603.25284-sliderquant-accurate-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/deep-optimization/SliderQuant) ・ リポジトリ内被引用：2  
  SliderQuantは、事前学習済みLLMを追加の大規模学習なしで低ビット化する事後量子化（PTQ）方式である。Llama2-7BのW4A4でWikiText2困惑度（PPL）はCBQの12.73に対し8.34、Qwen3-30B-A3BのW4A4ではOmniQuantのゼロショット平均50.11%に対し66.86%だった。

- **2026-02 · [MoBiQuant: Mixture-of-Bits Quantization for Token-Adaptive Any-Precision LLM](2026-2602.20191-mobiquant-mixture-of-bits-quantization-for-token-adaptive-any-precision-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデル（Large Language モデル; LLM）の推論における重み量子化は、GPUメモリ容量と重み読み出し帯域を節約する一方、ビット幅を下げるほど丸め誤差を増やす。

- **2026-02 · [FlexRank: Nested Low-Rank Knowledge Decomposition for Adaptive Model Deployment](2026-2602.02680-flexrank-nested-low-rank-knowledge-decomposition-for-adaptive-model-depl.md)**  
  実装：[✓](https://github.com/RickZack/FlexRank) ・ リポジトリ内被引用：2  
  FlexRankは、一つの事前学習済みモデルから、計算・メモリ予算に応じて大きさの異なる複数の部分モデルを切り出すための低ランク分解・学習方式である。

- **2025-12 · [SkipCat: Rank-Maximized Low-Rank Compression of Large Language Models via Shared Projection and Block Skipping](2025-2512.13494-skipcat-rank-maximized-low-rank-compression-of-large-language-models-via.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  同一入力の行列で低ランク射影を共有し、射影の先頭ブロックを再構成側へ吸収して省略することで、同じ圧縮率で保持できる有効ランクを増やし、学習なし低ランク圧縮の精度低下を既存法の半分以下に抑えた。

- **2025-12 · [OptRot: Mitigating Weight Outliers via Data-Free Rotations for Post-Training Quantization](2025-2512.24124-optrot-mitigating-weight-outliers-via-data-free-rotations-for-post-train.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  GPTQによる低ビット重み量子化では、極端に大きい重みが量子化スケールを押し広げ、通常の重みの再現精度を損なう。

- **2025-12 · [More Than Bits: Multi-Envelope Double Binary Factorization for Extreme Quantization](2025-2512.24545-more-than-bits-multi-envelope-double-binary-factorization-for-extreme-qu.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルの重みを1～1.5ビットまで圧縮すると、各重みを独立に丸める方式では振幅の情報が著しく失われ、生成品質が低下する。

- **2025-12 · [Fairy2i: Training Complex LLMs from Real LLMs with All Parameters in {±1, ±i}](2025-2512.02901-fairy2i-training-complex-llms-from-real-llms-with-all-parameters-in-1-i.md)**  
  実装：[✓](https://github.com/PKULab1806/Fairy2i-W2) ・ リポジトリ内被引用：2  
  Fairy2iは、通常の実数値で学習済みのTransformerを、量子化前の出力を変えずに複素数の広義線形（widely-linear）表現へ変換する。実効2ビットのFairy2i-W2はC4検証集合の困惑度（Perplexity; PPL）7.85、ARC-Easyなど五つのゼロショット課題平均62.00%を示した。

- **2026-09 · [SPHQuant: Efficient extreme low bit weight quantization for Vision-Language Models](2026-2609.24875-sphquant-efficient-extreme-low-bit-weight-quantization-for-vision-langua.md)**  
  実装：[✓](https://github.com/Pushazf/SPHQuant) ・ リポジトリ内被引用：1  
  重みを符号と半径と単位方向へ分解する球面量子化で外れ値を半径へ隔離し、半径への追加精度と小さな方向符号帳で極低ビットの精度を保ちながら、生成をQTIPより30.3パーセント速くした。

- **2026-09 · [Quantizing Looped Transformers: Feedback Exposure and Calibration Blindness](2026-2609.30820-quantizing-looped-transformers-feedback-exposure-and-calibration-blindne.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ループ型変換器の量子化が、恒等経路のない入口層での誤差の再帰と、ステップ0だけを見る較正の盲目性で壊れることを制御実験で切り分け、全ステップの統計を累積する較正で9件全ての主指標を改善した分析と手法の論文。

- **2026-09 · [OBC-Prune: Outcome-Based Calibration for Large Reasoning Model Pruning](2026-2609.17890-obc-prune-outcome-based-calibration-for-large-reasoning-model-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  正答・誤答の思考過程を同一問題で対にし、文ごとの因果的寄与で較正活性値を再重み付けすることで、一発枝刈り後の推論精度と停止挙動を改善する。

- **2026-09 · [Beyond Scalar Sensitivity: Activation-Aware Mixed-Precision LLM Quantization with Cross-Layer Refinement](2026-2609.25916-beyond-scalar-sensitivity-activation-aware-mixed-precision-llm-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルを低メモリで推論するために重みを量子化する際、全ての行列へ同じビット幅を適用する必要はない。Llama-3-8Bで平均2.25ビット／重みの場合、既存のQ-PaletteのWikiText-2パープレキシティ47.20に対してCASAは22.41、6課題平均正解率34.0%に対して39.2%だった。

- **2026-08 · [Understanding Calibration and Truncation Error Propagation in Training-Free Low-Rank Compression for LLMs](2026-2608.08506-understanding-calibration-and-truncation-error-propagation-in-training-f.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  圧縮済み層を通した活性値で後段を較正し直し、圧縮後に測り直した層重要度で保持率を反復的に直す二つの補正により、学習なし低ランク圧縮のゼロショット正解率を最大で約1から2.5ポイント改善した分析と手法の論文である。

- **2026-08 · [ARCHead: Activation-Metric Residual Correction for Large Language Model Output Heads](2026-2608.02703-archead-activation-metric-residual-correction-for-large-language-model-output-heads.md)**  
  実装：[✓](https://github.com/suayptalha/archead) ・ リポジトリ内被引用：1  
  ARCHeadは、大規模言語モデル（LLM）の最終出力射影（language-modeling head; LM-head）に特化した学習後圧縮方式である。語彙数が大きいモデルでは、この例外だけで数百MBから1GB以上の重みを保持する。

- **2026-07 · [Beyond Activation Alignment: The Alignment-Diversity Tradeoff in Task-Aware LLM Quantization](2026-2607.00908-beyond-activation-alignment-the-alignment-diversity-tradeoff-in-task-awa.md)**  
  実装：[✓](https://github.com/WangFei-2019/TASA) ・ リポジトリ内被引用：1  
  TASA（Task-Aware Sensitivity Analysis）は、LLMの重みを低ビットへ圧縮するとき、どの層へ何ビット割り当てるかを単一の言語モデル損失だけで決めない方式である。LLaMA-3-8Bでは平均3.5ビットで7タスク平均68.9%、HQQ W4の68.1%とRTN W4の67.9%を上回るが、AWQ W4の69.4%は下回る。

- **2026-06 · [STaR-Quant: State-Time Consistent Post-Training Quantization for Diffusion Large Language Models](2026-2606.04945-star-quant-state-time-consistent-post-training-quantization-for-diffusio.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  拡散型言語モデルの量子化で、マスク状態ごとに活性変換を分け、注意出力へブロック単位の補償を入れて誤差の蓄積を抑える学習後量子化。4ビット条件で比較対象を上回り、最大1.69倍の高速化と3.14倍のメモリ削減を示した。

- **2026-06 · [PhaseQuant: Mitigating Activation Quantization Collapse via Residual-Stream Dynamics](2026-2606.12487-phasequant-mitigating-activation-quantization-collapse-via-residual-stre.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  残差ストリームの動態から量子化に弱い層を見つけ、その層だけ活性値を8ビットへ上げる混合精度方針。回転系の学習後量子化へそのまま重ねられ、4ビット設定のパープレキシティと下流精度を一貫して改善する。

- **2026-06 · [Multi-Bitwidth Quantization for LLMs Using Additive Codebooks](2026-2606.12876-multi-bitwidth-quantization-for-llms-using-additive-codebooks.md)**  
  実装：[✓](https://anonymous.4open.science/r/DropbyDrop2026/) ・ リポジトリ内被引用：1  
  大規模言語モデルを異なる記憶容量の機器へ展開するとき、通常の学習後量子化（post-学習 量子化、PTQ）は3ビット、4ビット、5ビットといった精度ごとに別の圧縮モデルを作る必要がある。

- **2026-06 · [MosaicQuant: Inlier–Outlier Disaggregation for Unified 4-Bit LLM Quantization](2026-2606.15652-mosaicquant-inlier-outlier-disaggregation-for-unified-4-bit-llm-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデルの行列演算を高速化するため、重みと活性値を低ビット化するとメモリ転送量と演算費用を減らせる。従来の混合精度方式は外れ値のあるチャネルや低ランク成分を8～16ビットで保持するが、別精度の行列演算や変換・転送が発生し、低ビットの演算器を一貫して使う利点が減る。

- **2026-06 · [GRINQH: Graded Input-based Quantization Hierarchy for Efficient LLM Generation](2026-2606.23419-grinqh-graded-input-based-quantization-hierarchy-for-efficient-llm-gener.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  後者、とりわけバッチ1では、大きな線形層の重みを毎トークン読み出すため帯域律速になりやすい。重みを一律に3ビットや4ビットへ量子化すると帯域は減るが、重要なチャネルの精度も同時に失われる。Qwen3-8BのRTX 4090上では、4ビットMARLINの最適化カーネルより約25%高速な、GSM8K品質とのパレート前線上の動作点を示す。

- **2026-05 · [MGVQ: Synergizing Multi-dimensional Sensitivity-Aware and Gradient-Hessian Fusion for Vector Quantization](2026-2605.24019-mgvq-synergizing-multi-dimensional-sensitivity-aware-and-gradient-hessia.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  感度の融合で重み行列の塊ごとにビットを配り、一次の勾配のずれまで補償する視覚言語モデル向けベクトル量子化を提案し、2ビットで最良の既存方式を1.3から4.9点上回った。

- **2026-05 · [Fitting Is Not Enough: Smoothness in Extremely Quantized LLMs](2026-2605.08894-fitting-is-not-enough-smoothness-in-extremely-quantized-llms.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/FINE) ・ リポジトリ内被引用：1  
  極低ビットの大規模言語モデル（LLM）量子化では、元の浮動小数点モデルと量子化モデルの中間出力を近付ける「順方向の再構成誤差」が一般的な最適化対象である。

- **2026-05 · [EdgeRazor: A Lightweight Framework for Large Language Models via Mixed-Precision Quantization-Aware Distillation](2026-2605.04062-edgerazor-a-lightweight-framework-for-large-language-models-via-mixed-pr.md)**  
  実装：[✓](https://github.com/zhangsq-nju/EdgeRazor) ・ リポジトリ内被引用：1  
  対象は単なる事後量子化ではなく、量子化した生徒モデルを教師モデルで監督して再学習する混合精度量子化対応蒸留（Mixed-Precision Quantization-Aware Distillation; MPQAD）である。

- **2026-04 · [Supernodes and Halos: Loss-Critical Hubs in LLM Feed-Forward Layers](2026-2604.23475-supernodes-and-halos-loss-critical-hubs-in-llm-feed-forward-layers.md)**  
  実装：[✓](https://github.com/KempnerInstitute/nodelens) ・ リポジトリ内被引用：1  
  この研究は、LLMのフィードフォワード層（feed-順伝播 network、FFN）の中間チャネルを丸ごと削除する構造化枝刈り（structured 枝刈り）で、ある削除はほとんど害がないのに、別の削除はモデル品質を急激に崩壊させる理由を調べる。

- **2026-04 · [Robust Ultra Low-Bit Post-Training Quantization via Stable Diagonal Curvature Estimate](2026-2604.13806-robust-ultra-low-bit-post-training-quantization-via-stable-diagonal-curv.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DASH-Qは、学習済み大規模言語モデル（LLM）の重みを2〜4ビットへ圧縮する際、少量の較正入力から推定した相関情報を過信すると量子化後の回答品質が壊れるという問題を扱う。

- **2026-04 · [A KL Lens on Quantization: Fast, Forward-Only Sensitivity for Mixed-Precision SSM-Transformer Models](2026-2604.13440-a-kl-lens-on-quantization-fast-forward-only-sensitivity-for-mixed-precis.md)**  
  実装：[✓](https://github.com/jasonkongie/kl-ssm-quant) ・ リポジトリ内被引用：1  
  層を一つずつ量子化して順伝播だけで出力分布のずれを測り、学生から教師へのカルバック・ライブラー距離の順位が困惑度悪化の順位と六モデル平均で相関〇・七九と最もよく一致することを示し、その順位で高精度に残す層を選ぶ混合精度が実機で困惑度を保ったまま大きさと遅延を大きく減らした。

- **2026-03 · [SERQ: Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization](2026-2603.08185-serq-saliency-aware-low-rank-error-reconstruction-for-llm-quantization.md)**  
  実装：[✓](https://github.com/acalabys/SERQ) ・ リポジトリ内被引用：1  
  SERQ（Saliency-Aware Low-Rank Error Reconstruction for LLM Quantization）は、LLMの線形層で重みと活性値をともに低ビット化した際の誤差を、小さな追加行列で補う後学習量子化（PTQ）手法である。

- **2026-03 · [OneComp: One-Line Revolution for Generative AI Model Compression](2026-2603.28845-onecomp-one-line-revolution-for-generative-ai-model-compression.md)**  
  実装：[✓](https://github.com/FujitsuResearch/OneCompression) ・ リポジトリ内被引用：1  
  大規模言語モデル（Large Language モデル; LLM）の重み量子化では、同じ平均ビット幅でも層ごとの感度、較正用入力の分布、丸め誤差の伝播、量子化後の品質回復方法によって性能が大きく変わる。Llama-3-8BとQwen3系の実験では、感度に応じた混合ビット幅割当や誤差伝播補正が量子化後の困惑度を改善した。

- **2026-03 · [MASQuant: Modality-Aware Smoothing Quantization for Multimodal Large Language Models](2026-2603.04800-masquant-modality-aware-smoothing-quantization-for-multimodal-large-lang.md)**  
  実装：[✓](https://github.com/alibaba/EfficientAI) ・ リポジトリ内被引用：1  
  通常の文章向け平滑化量子化は、チャネルごとに一つのスケールを決め、活性の外れ値を重み側へ移して低ビット表現の誤差を減らす。

- **2026-02 · [SFMP: Fine-Grained, Hardware-Friendly and Search-Free Mixed-Precision Quantization for Large Language Models](2026-2602.01027-sfmp-fine-grained-hardware-friendly-and-search-free-mixed-precision-quan.md)**  
  実装：[✓](https://github.com/Nkniexin/SFMP) ・ リポジトリ内被引用：1  
  重み量子化は、大規模言語モデル（LLM）の重みを16ビットなどの高精度形式から2～4ビット程度の表現へ圧縮し、GPUメモリ使用量を削減する。

- **2026-02 · [Quant Experts: Token-aware Adaptive Error Reconstruction with Mixture of Experts for Large Vision-Language Models Quantization](2026-2602.24059-quant-experts-token-aware-adaptive-error-reconstruction-with-mixture-of-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  画像・テキストを統合処理するVision-Language モデル（VLM）を低ビットで推論する際、量子化された重み行列と活性値の積には誤差が生じる。

- **2026-01 · [HESTIA: A Hessian-Guided Differentiable Quantization-Aware Training Framework for Extremely Low-Bit LLMs](2026-2601.20745-hestia-a-hessian-guided-differentiable-quantization-aware-training-frame.md)**  
  実装：[✓](https://github.com/hestia2026/Hestia) ・ リポジトリ内被引用：1  
  重みを{-1,0,+1}の三値に制限する1.58ビット級の量子化は、重み保存量や乗算器への要求を減らせる可能性がある。

- **2026-01 · [HeRo-Q: A General Framework for Stable Low-Bit Quantization via Hessian Conditioning](2026-2601.21626-hero-q-a-general-framework-for-stable-low-bit-quantization-via-hessian-c.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  大規模言語モデル（LLM）の重みを2〜4ビットへ量子化すると、モデルをGPUメモリへ収めやすくなる。Llama-3.1-8BのW4A16条件では、NVIDIA A800上の生成処理量が113.1トークン/秒で、SpinQuantの112.8トークン/秒とほぼ同じである。

- **2026-01 · [D2Quant: Accurate Low-bit Post-Training Weight Quantization for LLMs](2026-2602.02546-d2quant-accurate-low-bit-post-training-weight-quantization-for-llms.md)**  
  実装：[✓](https://github.com/XIANGLONGYAN/D2Quant) ・ リポジトリ内被引用：1  
  D²Quantは、大規模言語モデルの重みのみを4ビット未満へ圧縮するときの精度劣化を対象とする、学習後量子化（post-学習 量子化; PTQ）の研究である。実験においてQwen3-8Bの2ビット重み量子化はWikiText2でパープレキシティ14.10、C4で25.96、MMLUで49.94%、7課題の平均正答率57.22%となった。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-11 · [Computed Permutation Trellis Coding: Near-Optimal Quantization from Two Multiplications and a 64-Byte Table](2026-2611.22019-computed-permutation-trellis-coding-near-optimal-quantization-from-two-m.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  状態への2回の乗算と64バイトのテーブル参照だけでトレリス符号の置換を計算し、4ビットで理想まで0.07ビットに迫る実効ビット数3.93を達成する低ビット量子化形式。1つのデコーダが1から6ビットと標準スカラー形式を兼ね、Llama 3.1の重み量子化でQTIPより最大27%低いKLを示し、Trainium 4ではネイティブ形式と同等の速度で復号できる。

- **2026-11 · [Calibration of Large Model Quantization based on HiFloat4 Format](2026-2610.41112-calibration-of-large-model-quantization-based-on-hifloat4-format.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三階層スケールの4ビット形式ハイフロート4へ、誤差補償、指数と仮数の学習補正、外れ値をならす等価変換という三つの較正を作り替えて適用し、五つのモデルと七つの課題の平均精度を直接変換の72.804パーセントから最大73.708パーセントへ上げ、16ビットとの差を0.262ポイントまで縮めたと報告した。

- **2026-11 · [BitPrefill: W1.58A4 Tensor-Core Acceleration for Compute-Bound LLM Prefill](2026-2611.26657-bitprefill-w1-58a4-tensor-core-acceleration-for-compute-bound-llm-prefil.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値重みと4ビット活性値をネイティブINT4テンソルコア行列積へ載せ、形状適応型のカーネル選択と融合した逆量子化で計算律速のプリフィルを速くする演算子で、BitNet-b1.58 3BのプリフィルをBF16比1.42倍にしエネルギーも42パーセント減らす。

- **2026-10 · [Trainable Vector Quantization for Large Language Models](2026-2610.41822-trainable-vector-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  離散的な割当て行列を潜在重みとコードブックから決まる関数へ書き直し、直通推定で勾配を流す訓練可能なベクトル量子化で、2ビット量子化の品質を回復させ、Llama2-70B の質問応答では元のモデルとの差を 0.7% まで縮めた。

- **2026-10 · [ThinkBit: Search Codewords, Recalibrate Scales, Select by Reasoning](2026-2610.34886-thinkbit-search-codewords-recalibrate-scales-select-by-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ベクトルコードブックも回転も使わない厳密なスカラー2ビット量子化で、感度配分・コードワード探索・スケール再調整・量子化認識学習を積み重ね、最後は訓練問題の推論テストで選ぶことで、Qwen3-1.7Bを0.52GBまで小さくしながらMATH-500で73.0を保つ枠組み。

- **2026-10 · [The Devil Is in the Reconstruction Loss Scale: Rethinking Optimization in LLM Quantization](2026-2610.00983-the-devil-is-in-the-reconstruction-loss-scale-rethinking-optimization-in.md)**  
  実装：[✓](https://github.com/IntelChina-AI/RMSE) ・ リポジトリ内被引用：0  
  この論文は、学習済み大規模言語モデルを小さな校正データだけで低ビット化する学習後量子化（post-学習 量子化; PTQ）の最適化損失に焦点を当てる。

- **2026-10 · [SAGE: Pushing 2-Bit Vector-Quantized LLMs toward Real-World Usability](2026-2610.14745-sage-pushing-2-bit-vector-quantized-llms-toward-real-world-usability.md)**  
  実装：[✓](https://github.com/Zincwolf/sage) ・ リポジトリ内被引用：0  
  球面ベクトル量子化のチャネル grouping と方向・半径のビット配分を活性統計で決め直し、2ビット級でも生成ベンチマークの実用精度を保つ重み量子化手法。

- **2026-10 · [SACQ: Structure-Aware Codebook Quantization for Ultra-Low-Bit Vision-Language-Action Models](2026-2610.41408-sacq-structure-aware-codebook-quantization-for-ultra-low-bit-vision-lang.md)**  
  実装：[✓](https://github.com/haesunglee116/SACQ) ・ リポジトリ内被引用：0  
  射影の役割別の尺度で符号帳を合わせ最終行動の誤差で精度を配分し二段の仕上げを行う重みのみの符号帳量子化で、一点五ビットでも成功率の低下を零点二五ポイントに抑えメモリを四点八三倍削減し活性八ビット併用で一点五一倍高速化したと報告した。

- **2026-10 · [RoleQ: Role-Aligned Scales for Converting Language Models to Ternary](2026-2610.21808-roleq-role-aligned-scales-for-converting-language-models-to-ternary.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化スケールを残差ストリームへの読み取り・書き込みという機能的役割で割り当てる規則と、数GPU時間の三値変換パイプラインにより、学習後三値変換でパープレキシティとMMLUを従来手法から大きく改善し、感度の高いユニットへの疎な第2プレーンで知識の損失を追加ビットで回復した。

- **2026-10 · [ResCom: Activation Residual Compensation for Large Language Model Quantization](2026-2610.35955-rescom-activation-residual-compensation-for-large-language-model-quantiz.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化で捨てられる丸め残差そのものを補正の入力にし、校正済みモデルを凍結したまま閉形式で低ランク枝を後付けして、4ビット量子化の精度を回復する修復法。

- **2026-10 · [RECAP: Calibrating Low-Bit Reasoning Models on the History They Read](2026-2610.15259-recap-calibrating-low-bit-reasoning-models-on-the-history-they-read.md)**  
  実装：[✓](https://github.com/AI-Efficiency/RECAP) ・ リポジトリ内被引用：0  
  長い推論履歴を現在の量子化器で再生成した接頭辞を読みながら短いブロックを回転させて再構成し、キャッシュ誤差を後続の注意への影響で重み付けて較正することで、低ビット推論モデルの精度低下を抑える学習後量子化。

- **2026-10 · [RapidMoE: Exploiting Cross-Asymmetry via Adaptive Residual Offloading for Large-Scale MoE Inference](2026-2610.01265-rapidmoe-exploiting-cross-asymmetry-via-adaptive-residual-offloading-for.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  たとえばDeepSeek-R1は671Bパラメータのうち約37Bを活性化するが、FP16重みをGPU VRAMへ格納するには700GB超を要する。単一ノードのCPU–GPU混在機では、GPUに置けない専門家をPCIe経由で都度転送する方式は転送遅延が律速になり、専門家計算自体をCPUへ寄せる方式はCPU側へ仕事が集中してGPUを十分使えない。

- **2026-10 · [OSFP4: Joint Optimization of Diagonal Smoothing and Block Scales for NVFP4 Quantization](2026-2610.08231-osfp4-joint-optimization-of-diagonal-smoothing-and-block-scales-for-nvfp.md)**  
  実装：[✓](https://github.com/neriahbd/OSFP4) ・ リポジトリ内被引用：0  
  NVFP4量子化で、射影ごとの対角平滑化とブロック尺度を、ディザ付き量子化の損失で共同最適化し、最後に決定的尺度を探し直す学習後量子化。同条件の比較手法中で最高の平均精度を保ちながらネイティブ実行の効率をほぼ維持する。

- **2026-10 · [Loopy: Low-Bit Quantization Framework for Looped Language Models](2026-2610.05265-loopy-low-bit-quantization-framework-for-looped-language-models.md)**  
  実装：[✓](https://github.com/Shameless0817/Loopy-review.git) ・ リポジトリ内被引用：0  
  ループ型モデルの共有コア量子化で、構成の優劣が再帰深さで入れ替わる問題に対し、目標深さで完走させた最終損失で構成を選び、校正窓の段階配分で探索費用を抑えた量子化基盤。

- **2026-10 · [LoopQuant: Accurate and Efficient Post-Training Quantization for Looped Transformers](2026-2610.16368-loopquant-accurate-and-efficient-post-training-quantization-for-looped-t.md)**  
  実装：[✓](https://github.com/Kishon-zzx/LoopQuant) ・ リポジトリ内被引用：0  
  ループ型言語モデル専用の学習後量子化として、共有変換による分布の正準化、感度と相互作用に基づくループ別ビット配分、再帰軌跡に沿った較正を組み合わせ、4ビット量子化でも8ビット従来法を上回る精度と1.5から1.7倍の復号高速化を得た。

- **2026-10 · [Integer-Exact Microscaling: Running MXFP4 Language Models on INT8 Matrix Units](2026-2611.00486-integer-exact-microscaling-running-mxfp4-language-models-on-int8-matrix-.md)**  
  実装：[✓](https://github.com/shinyoungkang1/mxfp4-int8-m5) ・ リポジトリ内被引用：0  
  行内の区画指数の広がりが三以内なら標準の四ビット重み行を一つの整数ベクトルへ厳密に畳めることを示し、実在の重みのほぼ全行が既に満たすこの条件で整数行列装置の入力処理を一・一倍から一・七四倍速くし、整数倍率へ緩めた新形式では千二百五十億モデルで数学課題の正解率百分の九十四・八を得たと報告した。

- **2026-10 · [Fractional Power-of-Two Quantization for Efficient and Effective Multiplier-Free LLM Inference](2026-2610.21257-fractional-power-of-two-quantization-for-efficient-and-effective-multipl.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの格子を半オクターブの分数冪へ細かくし、活性値は一様整数のまま、ルート2倍を加算器1個で近似して誤差を較正で吸収することで、乗算器なしのシフト加算実行を保ったまま4ビットで一様整数に近い精度を得る量子化。

- **2026-10 · [Extreme Compression of Per-Layer Embeddings via Cross-Layer Latent Vector Quantization](2026-2610.31309-extreme-compression-of-per-layer-embeddings-via-cross-layer-latent-vecto.md)**  
  実装：[✓](https://github.com/VILA-Lab/optic) ・ リポジトリ内被引用：0  
  Gemma 4の層別埋め込みを、トークン共有のコードと層別アフィンデコーダで表し、ゲートと出力射影の先で誤差を測るfittingにより約100倍圧縮で7タスク保持率97.8パーセントを達成し、圧縮したままの推論でGPUメモリを29.7パーセント減らす手法。

- **2026-10 · [E8-QAT: Efficient 2-Bit Quantization-Aware Training with Implicit Lattice Codebooks](2026-2610.27699-e8-qat-efficient-2-bit-quantization-aware-training-with-implicit-lattice.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  E8格子への算術的な射影で重み8個を探索なしに共同量子化し、有限コアと疎な拡張で正確に書き出す2ビット量子化対応学習で、35B級モデルをBF16同等の平均スコアまで回復させた。

- **2026-10 · [DualQuant: Dual-scale Calibration-free Weight-and-Activation Quantization for LLMs](2026-2610.13767-dualquant-dual-scale-calibration-free-weight-and-activation-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み再構成誤差の最小化で得た行と列の二重スケールを、そのまま活性値のチャネル再スケーリングに流用することで、調整データなしに重みと活性値の4ビット量子化をINT4からMX形式・NVFP4まで一つの手続きで実現する方式。

- **2026-10 · [Differentiable Bit-Widths: Co-optimizing Pruning and Quantization via SVD for Ultra-Efficient LLM Compression](2026-2610.06026-differentiable-bit-widths-co-optimizing-pruning-and-quantization-via-svd.md)**  
  実装：[✓](https://github.com/MMAI-Laboratory/DBW) ・ リポジトリ内被引用：0  
  特異値分解の成分ごとのビット幅を0ビット込みで微分可能に学習し、枝刈りと量子化を同時に最適化する圧縮法で、平均1.61ビットでも二段階方式や極低ビット量子化の比較対象を上回り、重みメモリを最大約9倍削減した研究。

- **2026-10 · [CoS-VQ: Coordinated Shared-Scale Vector Quantization for Large Language Models](2026-2610.37336-cos-vq-coordinated-shared-scale-vector-quantization-for-large-language-m.md)**  
  実装：[✓](https://github.com/xzktx003/Cos_VQ) ・ リポジトリ内被引用：0  
  低次元コードワードを保ち、共有スケールとハードインデックスを下側包絡の探索で協調最適化するベクトル量子化で、スケール単独調整では届かない量子化誤差の削減を約2ビット毎重みで実現し、Qwen3.8-27BでQTIPやLLVQを上回る。

- **2026-10 · [Advancing SVD-based LLM Compression via Layer-Wise Error Model Search](2026-2610.32878-advancing-svd-based-llm-compression-via-layer-wise-error-model-search.md)**  
  実装：[✓](https://lems-svd.github.io) ・ リポジトリ内被引用：0  
  層ごとの誤差を形・較正・伝播バイアスでモデル化して整数線形計画で最適なランク配分を解き、フィッシャー因子はトークン単位の統計で推定してランク崩壊を防ぐSVD圧縮で、同じ予算でも精度を大きく保てるようにした。

- **2026-10 · [Activation Denoising: A Robustness View on Parallel vs Sequential LLM Quantization](2026-2610.07522-activation-denoising-a-robustness-view-on-parallel-vs-sequential-llm-qua.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  上流の量子化誤差をランダムノイズとして扱い、全層へ並列にデノイジングフィルタを吸収させることで、逐次量子化の精度利得の一部を並列量子化のまま回収する頑健性正則化の手法。

- **2026-10 · [A Unified Hessian-Guided Framework for Post-Training Quantization](2026-2610.40345-a-unified-hessian-guided-framework-for-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層出力のFisher情報をクロネッカー分解で近似し、変換・スケール・丸め・クリッピングを単一の下流感度目的で統一的に決める学習後量子化で、4ビット条件の全対象モデルで最良のパープレキシティを達成した研究。

- **2026-09 · [XOR-Trellis: Ultra-Low-Complexity Dequantization and Curvature-Aware Hadamard-Free LLM Quantization](2026-2610.00432-xor-trellis-ultra-low-complexity-dequantization-and-curvature-aware-hada.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  2ビット前後まで重みを圧縮すると、重み転送量は小さくなる一方で、単純なスカラー量子化では量子化誤差が大きくなる。復元は約14個の2入力XORゲートと固定された4×4の小さな候補表で表現できる。

- **2026-09 · [Why Does Post-Training Quantization Work?](2026-2609.11716-why-does-post-training-quantization-work.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（LLM）の重みを学習後に4ビットへ量子化すると、各線形層の重みが元の値からずれる。Qwen3-32Bの第1〜48層では、この相互作用がブロック更新誤差の二乗ノルムの累積寄与の50.2%を相殺した。

- **2026-09 · [WaterKron and FlipFlop Hessian: Information-Theoretically Grounded Quantization with Kronecker-factored Hessians](2026-2609.14706-waterkron-and-flipflop-hessian-information-theoretically-grounded-quanti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  両側GPTQの格子スケールを行列両側のウォーターフィリングで配分し、クロネッカー近似の歪み倍率を最小化するフリップフロップ反復でヘッセ近似を選ぶことで、2ビット量子化の品質を従来の近似選択より一貫して改善した。

- **2026-09 · [Vortex: Bridging Extreme Compression and Efficient LLM Inference](2026-2609.12208-vortex-bridging-extreme-compression-and-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  超低ビットベクトル量子化と入力依存疎性を二種類の実行流へ合わせ、圧縮率を実際の推論高速化へ変換する加速器。

- **2026-09 · [VLAQuantBench: Closed-Loop Evaluation of Post-Training Quantization for Vision-Language-Action Models](2026-2609.25376-vlaquantbench.md)**  
  実装：[✓](https://github.com/jiuyixu25/VLAQuantBench) ・ リポジトリ内被引用：0  
  VLAQuantBenchは、視覚・言語・行動モデル（Vision-Language-Action モデル、VLA）の学習後量子化（Post-学習 量子化、PTQ）を、重みの再構成誤差だけでなく、ロボットが環境を動かし続けた結果のタスク成功率で検証する評価基盤である。

- **2026-09 · [ThinQuant: Scalable Rotation Learning for Weight and Activation Quantization of LLMs](2026-2609.36120-thinquant-scalable-rotation-learning-for-weight-and-activation-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット量子化では、重みと活性の外れ値が量子化範囲を広げ、通常の小さい値に割り当てられる表現精度を低下させる。Llama-3-70BのW4A4KV4ではDartQuantのWikiText-2困惑度7.55に対して5.63へ改善し、校正時間は111分から11分57秒へ、保存データは960GiBから0.51GiBへ削減する。

- **2026-09 · [Tetra: Serving Leech-Lattice Quantized LLMs at 2.7 Bits per Parameter](2026-2609.35465-tetra-serving-leech-lattice-quantized-llms-at-2-7-bits-per-parameter.md)**  
  実装：[✓](https://github.com/pjmalandrino/llvq) ・ リポジトリ内被引用：0  
  Leech格子の符号帳を3区間のトレリスと共有16KiB表で再構成し、展開なしに積の中で復号して重みあたり2.150ビットだけを読む2ビット級量子化カーネルと、約2.7ビット毎パラメータの完全モデル化レシピ。

- **2026-09 · [Structured Transforms for Low-Overhead Quantization of Language Models](2026-2609.11687-structured-transforms-for-low-overhead-quantization-of-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Kashin分解を利用した大規模言語モデルの学習後量子化（post-学習 量子化）について、量子化前処理が遅いこと、因子分布が不安定なこと、数値的に収束しない層があることを同時に解決しようとする。

- **2026-09 · [Softmax Reparameterization for Output-Head Quantization](2026-2609.31291-softmax-reparameterization-for-output-head-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全精度では予測が変わらない出力ヘッドの同値な表し方の中から、量子化後の分布のずれが最小になるものを検証KLで選ぶ再パラメータ化で、歪みの大きいヘッドのKLを最大93パーセント減らした。

- **2026-09 · [Security-Enhanced Seed-Based Weight Quantization for Large Language Models](2026-2609.38477-security-enhanced-seed-based-weight-quantization-for-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの自己回帰デコードは重み転送に律速される場合があり、低ビット重みの保持だけでなく、圧縮した記号から演算時に重みを生成する方法が検討されている。

- **2026-09 · [Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution](2026-2609.09240-scaling-post-training-ternarisation-to-qwen3-8b-capability-retention-reproduction-lossless-packing-and-packed-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-8Bを適応的約1.64 bit/重みへ後量子化し、78.5%の補正済み能力保持、8.24 GiBの無損失packed artifact、RTX 5070上15.52 トークン/s・7.35 GiBの直接実行まで検証する。

- **2026-09 · [RGSQ: Riemannian Geometry-Sensitive Quantization for Large Vision-Language Models](2026-2609.25492-rgsq-riemannian-geometry-sensitive-quantization-for-large-vision-language-models.md)**  
  実装：[✓](https://github.com/RL-MIND/RGSQ) ・ リポジトリ内被引用：0  
  重みの学習後量子化（Post-学習 量子化; PTQ）は配備時のメモリ占有と転送帯域を減らせるが、視覚トークンと言語トークンの分布が異なるため、単一言語モデル向けの量子化手順をそのまま適用すると品質が崩れやすい。LLaVA-OneVision-7BのW4A8で、A800一枚における校正時間は2.1時間、ピークメモリは38GBである。

- **2026-09 · [Replay the Curvature: Accurate and Scalable NVFP4 Quantization for Large Language Model Inference](2026-2609.36654-replay-the-curvature-accurate-and-scalable-nvfp4-quantization-for-large-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有スケールを適切に選べばメモリ転送と保存容量を削減できるが、外れ値と通常値を同じスケールで表すため量子化誤差が生じる。Qwen3.5-397B-A17BのW4A4量子化では、七つの評価課題15,461問の正答数を集計し、BF16比99.35%の正答回復率を得た。

- **2026-09 · [QuLoC: Photonic Quantum-Assisted Low-Rank LLM Compression](2026-2609.40146-quloc-photonic-quantum-assisted-low-rank-llm-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの線形射影行列を特異値分解（singular value decomposition; SVD）して小さな二つの行列へ置き換える低ランク圧縮は、重み数と行列演算量を削減できる。Qwen3.5-4Bの言語モデル部分のパラメータを20.05%減らした条件で、六つの下流課題の平均精度はSwift-SVDの49.24%から54.03%へ上昇した。

- **2026-09 · [Quantization Error Is Spectrally Flat: A Single Random Probe Is a Calibrated, Data-Free Sensitivity Estimator, with Application to Budget-Targeted Mixed-Precision Quantization at 400B Scale](2026-2609.33923-quantization-error-is-spectrally-flat-a-single-random-probe-is-a-calibra.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模LLMを低ビット量子化する際、すべての重みを同じビット幅にするより、精度劣化に敏感なテンソルを高ビット、耐性のあるテンソルを低ビットにした方が、同じ容量予算で品質を維持できる可能性がある。

- **2026-09 · [QuantaSpike: Short-Window Spike-Driven Quantization for Large Language Models](2026-2609.34259-quantaspike-short-window-spike-driven-quantization-for-large-language-mo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値イベントと2のべき乗の量子で1ステップあたりの情報量を増やし、外れ値だけに開始スパイクを1回追加することで、発火窓4ステップのままシフトと累積だけで計算できるスパイク駆動の学習後量子化。

- **2026-09 · [QATFactory: A Versatile, Deployment-Aligned Framework for Quantization-aware Training and Distillation of LLMs](2026-2609.39223-qatfactory-a-versatile-deployment-aligned-framework-for-quantization-awa.md)**  
  実装：[✓](https://github.com/QATFactory/QATFactory) ・ リポジトリ内被引用：0  
  QATFactoryは、実際の推論エンジンが用いる量子化グリッド、ブロック構成、スケール階層、丸め規則を前向き計算に反映する。Qwen3.5-9Bの複数ベンチマーク平均正答率は、NVFP4では最良PTQの65.4%から68.9%へ、MXFP4では56.4%から66.0%へ改善した。

- **2026-09 · [Predicting Quantization Price for Selecting PTQ Configurations Before Deployment](2026-2609.28270-predicting-quantization-price-for-selecting-ptq-configurations-before-de.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習後量子化（Post-学習 量子化; PTQ）では、学習済みの大規模言語モデル（Large Language モデル; LLM）の重みを、少ないビット数で保存・計算できる表現に置き換える。

- **2026-09 · [Predict Before You Deploy: Offline Prediction of Quantization-Induced Task Degradation for World Action Models](2026-2609.19441-prede-quantization-task-degradation-prediction.md)**  
  実装：[✓](https://github.com/jiuyixu25/PreDE) ・ リポジトリ内被引用：0  
  PreDE（Predict Before You Deploy）は、世界行動モデル（World Action モデル、WAM）を学習後量子化したとき、候補ごとに高価な閉ループ試験を行う前に、タスク成功率の劣化を「受理・棄却・保留」の三値で予測する方式である。

- **2026-09 · [Per-Matrix Optimality Is Not Enough: Three-Level Optimization for Low-Rank LLM Compression](2026-2609.15838-per-matrix-optimality-is-not-enough-three-level-optimization-for-low-ran.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  行列単位のSVD、ブロック単位の共同最適化、モデル全体の言語モデリング損失による磨き上げを256系列の較正だけでつなぎ、LLaMA-7Bの60パーセント圧縮でパープレキシティを42.1から11.4へ下げる三段階の低ランク圧縮。

- **2026-09 · [MiX: Micro-Inverted-Scaling for End-to-End Low-Bit Vision-Language Model Acceleration](2026-2609.19683-mix-micro-inverted-scaling-for-end-to-end-low-bit-vision-language-model-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VLMのマルチモーダル外れ値に対し、要素別指数＋共有仮数へマイクロスケーリングを反転し、4bit級の端から端までの量子化と乗算器不要のシフト加算PEを同時に実現する。

- **2026-09 · [KBBQ: A Predictive Noise Law and the Limits of Spectrum Flattening in FP4 Quantization](2026-2609.08135-kbbq-a-predictive-noise-law-and-the-limits-of-spectrum-flattening-in-fp4.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みと活性化をともに4ビットに落とす量子化（W4A4）では、表現範囲を共有するブロック内の外れ値と丸め誤差がモデル精度を損なう。4つの基盤モデルと2種類の4ビット浮動小数点形式を用いた8組の実験で、単純丸めにKBBQを組み合わせる方式は、同じ設定の完全平坦化方式WUSHを7組で上回った。

- **2026-09 · [G²PTQ: Improving LLM Post-Training Quantization with Generalized Gradient Compensation](2026-2609.31009-g-ptq-improving-llm-post-training-quantization-with-generalized-gradient.md)**  
  実装：[✓](https://github.com/G2PTQ/G2PTQ) ・ リポジトリ内被引用：0  
  G²PTQは、学習済み大規模言語モデル（LLM）の重みを低ビットへ変換する学習後量子化（post-学習 量子化、PTQ）を、量子化途中のモデル状態に応じて誤差補償を更新する処理として再設計した研究である。

- **2026-09 · [From Attention Sensitivity to Layer Role: Revisiting Mixed-Precision Quantization of Transformers](2026-2609.34866-from-attention-sensitivity-to-layer-role-revisiting-mixed-precision-quan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  注意の共同目的で再構成とビット配分を統一するJABを検証し、注意だけでは感度配分が効く一方、全モデルでは行列の役割に基づく単純なオフセット規則が曲率基準を上回ることを示した混合精度量子化の分析研究。

- **2026-09 · [FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators](2026-2609.04724-flexposit-tunable-fractional-precision-for-llm-inference-accelerators.md)**  
  実装：[✓](https://github.com/hplp/FlexPosit) ・ リポジトリ内被引用：0  
  LLMの重み量子化には、精度を保つために細かいグループごとに倍率を持つ方式と、ハードウェア実装しやすいチャネル単位の方式がある。

- **2026-09 · [Breaking the 1.58-bit Barrier for Ternary LLMs](2026-2609.16338-breaking-the-1-58-bit-barrier-for-ternary-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値重みのゼロ偏りを利用するBITCOSで格納量を最小1.485ビット/重みまで下げ、専用CPU・Xe2復号で一要求デコードを最大1.27倍高速化する。

- **2026-08 · [SchurQuant: Groupwise Discrete Optimization for Layer-Wise LLM Quantization](2026-2608.15567-schurquant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを4ビットから2〜3ビットへ縮めると、量子化格子の段数が少なくなり、各層の誤差が累積して言語モデルの予測を壊す。Llama2、Llama3、Qwen3の計8モデルを比較した2ビットの六課題平均ゼロショット精度は、SchurQuantが50.83%、GPTQが39.25%、QEPが41.18%である。

- **2026-08 · [SandwichQuant: Which Parameters Matter Before and After Quantization?](2026-2608.24173-sandwichquant-which-parameters-matter-before-and-after-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事後量子化（Post-学習 量子化; PTQ）の品質を回復する研究では、重み、量子化尺度、丸め、局所再構成などを調整する。Llama2-7B、Llama3-8B、Qwen3-8Bなどの強い量子化条件で一貫して改善し、Llama2-7BのW2A4KV4条件では比較構成の平均6タスク精度48.9を55.1へ改善する一方、推論時の追加演算子は増やさない。

- **2026-08 · [ReRound: Reconstructive Rounding to Resolve Midpoint Ambiguity in Calibration-Free LLM Quantization](2026-2608.11045-reround-reconstructive-rounding-to-resolve-midpoint-ambiguity-in-calibra.md)**  
  実装：[✓](https://github.com/louisYen/ReRound) ・ リポジトリ内被引用：0  
  この研究が変更するのは量子化スケールそのものではなく、既に決められた量子化区間の下側整数・上側整数のどちらを選ぶかという最終段階である。例えばGemma 2 2Bの4ビット条件で、四つのゼロショット課題の平均正答率はグループ別RTNの66.4%から67.4%へ上昇した。

- **2026-08 · [PRQuant: Permutation Residual Quantization for Low-Overhead Inference](2026-2609.22106-prquant-permutation-residual-quantization-for-low-overhead-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PRQuantは、言語モデルの線形層を重み・活性値とも4ビット相当で実行する際、少数の外れ値経路が精度を左右する問題を扱う。特に微小尺度浮動小数点4ビット形式（MXFP4）では小ブロックが共通尺度を持ち、ブロック内の一部の大きな値に尺度を合わせると、それ以外の値の量子化刻みが粗くなる。

- **2026-08 · [LegoLM: Structured Weight Sharing for Large Language Models](2026-2608.08652-legolm-structured-weight-sharing-for-large-language-models.md)**  
  実装：[✓](https://anonymous.4open.science/r/legolm) ・ リポジトリ内被引用：0  
  重み共有圧縮の失敗原因を尺度不一致と外れ値支配に分解し、スカラー化と外れ値の原文保持と境界層保護を組み合わせて、校正データなしで7Bモデルを4倍以上圧縮しても品質劣化をほぼゼロに抑える研究。

- **2026-08 · [HBQ: Hierarchical Scaling Block Quantization with Hardware-Efficiency-Aware Design for Accurate LLM Inference](2026-2609.00450-hbq-hierarchical-scaling-block-quantization-with-hardware-efficiency-awa.md)**  
  実装：[✓](https://github.com/SeoLabCornell/HBQ) ・ リポジトリ内被引用：0  
  LLMの重みだけを4ビット化する重み-only 量子化（WoQ）は、モデル重みのメモリ帯域を節約できるが、活性値と注意計算のKVキャッシュには高精度のデータパスが残る。

- **2026-08 · [From Sweep to Seam: Interleaved Cross-Block Post-Training Quantization](2026-2608.09595-from-sweep-to-seam-interleaved-cross-block-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Interleaved Cross-Block Quantization（ICBQ）は、学習済みLLMの重みを極低ビットへ圧縮する際、隣接Transformerブロックを再構成する最適化窓をどの順序で訪れるかを変更する方式である。

- **2026-08 · [FOCUS: FP4 Optimization via Coupled-Relaxation and Dual-Granularity Scaling](2026-2608.01847-focus-fp4-optimization-via-coupled-relaxation-and-dual-granularity-scali.md)**  
  実装：[✓](https://github.com/tencent/AngelSlim) ・ リポジトリ内被引用：0  
  保存されない量子化スケールを、保存される逆量子化スケールへ全精度の係数を掛けた形へ緩め、さらに部分ブロック単位へ細分化して学習することで、標準のFP4形式のまま精度をFP16近傍まで回復させた学習後量子化である。

- **2026-08 · [FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy](2026-2608.15602-fluxbin-lut-ultra-low-bit-inference.md)**  
  実装：[✓](https://github.com/nicyyyy/FluxBin) ・ リポジトリ内被引用：0  
  重要列だけをヘッセ行列で選んで追加二値基底を与え、逆量子化を避けるLUT融合CUDAカーネルで約2〜3ビットLLMを実行し、A100で最大5.92倍高速化・10.19倍省エネルギーを報告する。

- **2026-08 · [FlashQuant: Sparse-Dense Fusion for Memory-Efficient Outlier-Aware LLM Inference](2026-2608.15531-flashquant-sparse-dense-fusion-for-memory-efficient-outlier-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashQuantは、大規模言語モデルの重み4ビット・活性値16ビット量子化（W4A16）で生じる「低精度の密行列積と、高精度で残した少数の外れ値による疎行列積を別々に実行する」という問題を、GPUカーネルの内部構造から解決する研究である。BF16のcuBLASに対するカーネル高速化は2.74〜4.18倍だが、これは4ビット量子化の効果も含む。

- **2026-08 · [FAMPWQ: Fisher Information-based Adaptive Mixed Precision Weight Quantization for Effective LLM Inference](2026-2608.24945-fampwq-fisher-information-based-adaptive-mixed-precision-weight-quantization-for-effective-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実量子化ノイズでFisher情報の層別感度を測り、PPOで全体ビット予算を層へ配分して、3〜4bit域の品質劣化を一様量子化より抑える。

- **2026-08 · [CubicQuant: Parametric Non-Uniform Codebooks for High-Throughput LLM Inference with 1-8-Bit Weights](2026-2608.06763-cubicquant-parametric-non-uniform-codebooks-for-high-throughput-llm-infe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究が扱うのは、大規模言語モデル（LLM）の重みをGPUメモリに置き、自己回帰復号の各段階で行列演算に供給する際の表現形式である。提案形式は、1〜8ビットの重み符号を連続したビット列へ保存し、重み群ごとに尺度 s と二つの形状係数 a,b を付加する。

- **2026-08 · [Budget-Aware LLM Quantization and Low-Rank Correction via Information-Guided Subspace Matrices](2026-b373673622df-budget-aware-llm-quantization-and-low-rank-correction-via-information-gu.md)**  
  実装：[✓](https://github.com/sinuofan/IJCAI2026-BALANCER) ・ リポジトリ内被引用：0  
  BALANCERは、限られた記憶容量で大規模言語モデル（LLM）を実行するため、各重み行列の量子化精度と低ランク補正の階数を全モデル共通のビット予算で割り当てる学習不要の圧縮方式である。

- **2026-08 · [A Method for Layer Bit-Width Allocation in LLM Quantization via Performance Maximization Under a Quality-Degradation Constraint](2026-2608.28003-a-method-for-layer-bit-width-allocation-in-llm-quantization-via-performa.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  品質劣化の予算の下で速度を最大化する層ビット配分として、感度プロファイルに基づきGemma-3-1Bの全結合・注意・語彙射影をブロック単位でW8A8化し、RTX 5090実測で全結合と語彙射影は速くなり短文脈の注意は遅くなることと、品質保持下で11.0%の遅延削減を示す研究。

- **2026-07 · [Variable Bit-width Quantization: Learning Per-Group Precision for 'Bigger-but-Smaller' Language Models](2026-2607.02893-variable-bit-width-quantization-learning-per-group-precision-for-bigger-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化は重みの容量を減らすが、通常の方法では全重みに同じ4bitや2bitを割り当てる。Gumbel-Softmaxの連続緩和と交互最適化で精度選択を学習すると、グループの69%が1bitへ落ちる一方、最初のMLPブロックや頻出語彙の出力行は高い精度を要求する。

- **2026-07 · [SharVeT: Similarity-aware Parameter Sharing with Vector-based Tuning for Efficient LLM Compression](2026-f8a8760eeca9-sharvet-similarity-aware-parameter-sharing-with-vector-based-tuning-for-.md)**  
  実装：[✓](https://github.com/snudatalab/SharVeT) ・ リポジトリ内被引用：0  
  重みと活性値の両面から似たモジュールだけを集めて特異値分解の基底を共有し、グループのばらつきに応じてランクを配分し、二つの軽量ベクトルと知識蒸留で共有のずれを直すことで、同じ圧縮率で既存のパラメータ共有法より精度を保つ圧縮方式。

- **2026-07 · [Saturation Makes Quantization Error Additive: A Coverage Model with a Certificate](2026-2607.12266-saturation-makes-quantization-error-additive-a-coverage-model-with-a-cer.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化損傷は損失の飽和のためほぼ加法的に振る舞うことを実測と理論で示し、孤立感度が構成損失を71から376パーセント過大評価する一方、層数+1パラメータの予測器が同一メモリ配分でModelOptよりKLを17から21パーセント下げた。

- **2026-07 · [SAB-LVLM: Significance-Aware Binarization for Large Vision-Language Models](2026-2607.01876-sab-lvlm-significance-aware-binarization-for-large-vision-language-model.md)**  
  実装：[✓](https://github.com/LyuQi127/SAB_LVLM) ・ リポジトリ内被引用：0  
  SAB-LVLMは、画像と文章を扱う大規模視覚言語モデル（LVLM）を、重み約1bitの二値化へ圧縮する事後量子化（PTQ）方式である。Qwen2.5-VL-32B-InstructのMMStarは約1bitのARB-LLM48.48点からSAB-LVLM54.77点へ改善し、モデルメモリは10.28GBと報告される。

- **2026-07 · [RDQ: Residual Distribution Quantization for Large Language Models](2026-2607.10137-rdq-residual-distribution-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化劣化の主因を残差ストリームのドリフトと特定し、量子化済み上流から捕捉した実際の入力で層ごとに較正し直す逐次補償で、3ビットでも最良水準のパープレキシティを達成する学習後量子化。

- **2026-07 · [PE-QAT: Parameter-Efficient Quantization-Aware Training for Large Language Models](2026-b388700aa349-pe-qat-parameter-efficient-quantization-aware-training-for-large-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  凍結した基底モデルへ低ランクアダプタを統合した重みに疑似量子化をかけ、平滑化係数とクリッピング閾値も一緒に学習することで、学習可能パラメータ約1%で重み・活性値4ビット量子化の精度低下を補う量子化認識学習。

- **2026-07 · [LogbQuant: Quantizing Language Models in Logarithmic Space](2026-2607.01127-logbquant-quantizing-language-models-in-logarithmic-space.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み行列ごとに対数コードブックを作りエネルギー基準の枝刈りで範囲を絞る重み量子化で、4ビットで崩壊する線形量子化に対し正解率とパープレキシティを大きく保ちメモリを最大65パーセント減らす方式。

- **2026-07 · [JW-SVD: Bridging the Cross-Modal Mismatch in Post-Training MLLM Compression](2026-89ae46e494cf-jw-svd-bridging-the-cross-modal-mismatch-in-post-training-mllm-compressi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  テキスト専用に最適化した特異値分解が視覚情報を潰す問題を、テキストと画像の共同共分散による白化と視覚塔からバックボーンへの予算移転で解き、保持率40%でも知覚性能の大幅な回復とテキスト性能の維持を両立するマルチモーダル圧縮方式。

- **2026-07 · [HiSVD: Principled Low-Rank Approximation of LLMs via Hierarchical Modeling of Information Capacity and Spectral Structure](2026-a4fadb2637c2-hisvd-principled-low-rank-approximation-of-llms-via-hierarchical-modelin.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  有効ランクで決めた基準ランク配分を、特異値の裾の冗長さで削り直す二段のランク配分により、容量は高いが構造的に膨らんだ層を見つけてSVD圧縮の無駄を減らす。

- **2026-07 · [GyRot: Leveraging Hidden Synergy between Rotation and Fine-grained Group Quantization for Low-bit LLM Inference](2026-2607.27694-gyrot-leveraging-hidden-synergy-between-rotation-and-fine-grained-group-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GyRotは、重み・活性化を4ビットに圧縮したLLMを精度よく、しかも整数演算中心の専用回路で実行するためのアルゴリズムとハードウェアの共同設計である。回路性能は28nm・1GHz条件の合成・推定に基づき、Tender比の幾何平均で速度3.40倍、エネルギー効率3.64倍と報告する。

- **2026-07 · [Fast and Accurate Fisher-Guided Quantization via Efficient Kronecker Factorization](2026-10cd8299130f-fast-and-accurate-fisher-guided-quantization-via-efficient-kronecker-fac.md)**  
  実装：[✓](https://github.com/sayankotor/FastKron_QTIP) ・ リポジトリ内被引用：0  
  ヘッセ行列のクロネッカー因子をランチョス法で速く求めることで、二次の曲率情報を使う量子化の因子計算を最大で約10倍速くし、キャリブレーションのトークンを約96パーセント減らしながら4ビットでほぼ基準並み、2ビットでも小さい劣化に抑える。

- **2026-07 · [BiSCo-LLM: Lookup-Free Binary Spherical Coding for Extreme Low-Bit Large Language Model Compression](2026-2607.08643-bisco-llm-lookup-free-binary-spherical-coding-for-extreme-low-bit-large-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  BiSCo-LLMは、大規模言語モデル（LLM）の重みを2ビット級へ圧縮する際、単純なスカラー量子化では表現力が不足し、ベクトル量子化では明示的なコードブックの記憶容量と検索費用が増える問題に対処する研究である。BiSCo-LLMは較正データと元の重みから重要チャネルを選び、約1%を8ビットで保護する。

- **2026-07 · [ACBQ: Adaptive Cross-Block Quantization of Large Language Models](2026-e72658ea1043-acbq-adaptive-cross-block-quantization-of-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  自己注意と全結合ネットワークを別単位で最適化し、エントロピーで測った依存の強いブロックをグループ化して一緒に量子化することで誤差の蓄積を抑え、重み2ビットや重み・活性値4ビットでも精度を保つ学習後量子化ACBQ。

- **2026-06 · [UniRank: Unified Rank Allocation for Low-Rank LLM Compression](2026-2606.21847-unirank-unified-rank-allocation-for-low-rank-llm-compression.md)**  
  実装：[✓](https://github.com/EIT-NLP/LLM-Pruning) ・ リポジトリ内被引用：0  
  全行列の特異成分を層の機能的重要度と特異エネルギーで統一採点して予算まで貪欲に残し、再分解なしの微調整を組み合わせることで、微調整なし圧縮のパープレキシティを分解法横断で最大約6割下げる低ランク圧縮のランク配分法。

- **2026-06 · [Tailoring LLM Weight Compression For PIM Architectures](2026-12d4703b0ce4-tailoring-llm-weight-compression-for-pim-architectures.md)**  
  実装：[✓](https://github.com/Tajdari-S/PIM-LLM-Compression) ・ リポジトリ内被引用：0  
  BF16の指数部の冗長性を使い、固定長でバンク内復号できる辞書方式と差分方式の二つの重み圧縮をPIM向けに設計し、容量を約24から25パーセント減らして復号回路の面積増を1割前後に抑える研究。

- **2026-06 · [SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving](2026-2606.11244-spear-error-adaptive-low-bit-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン適応型量子化誤差補償とカーネル・通信・SLOスケジューリングを共同設計し、W4–FP16のperplexity差を56–75%回復。

- **2026-06 · [Signed Symmetric Quantization for Few-Bit Integers](2026-2607.08779-signed-symmetric-quantization-for-few-bit-integers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対称量子化のスケールの符号をグループごとに選び、余分な整数水準を支配的な外れ値側へ回すことで、ゼロ点なしのまま切り捨て誤差を減らし、2ビットでパープレキシティを103.1から17.8へ改善する。

- **2026-06 · [Recover-LoRA for Aggressive Quantization: Reclaiming Accuracy in 2-Bit Language Models via Low-Rank Adaptation with Knowledge Distillation on Synthetic Data](2026-2606.04238-recover-lora-for-aggressive-quantization-reclaiming-accuracy-in-2-bit-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの重みを4ビットから2ビットへ圧縮すると、デコード時に重みをGPUメモリから読み出す帯域費用を減らせる。12ベンチマーク中9件で、量子化による教師との差の80〜95%を回復した。

- **2026-06 · [QuBLAST: A Framework for Quantizing Large Language Models with Block-Level Compression Approach and Activation Scaling Strategy](2026-2606.04620-qublast-a-framework-for-quantizing-large-language-models-with-block-leve.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  QuBLASTは、既に学習済みの大規模言語モデルを再学習せずに圧縮する学習後量子化（post-学習 量子化; PTQ）の方法である。Qwen3-8B、Llama3-8B、Mistral v0.1-7B、Falcon H1R-7Bを対象に、重みの混合精度構成でモデル容量を40.0〜45.2%削減し、WikiText-2/103のPPL増加を5%以内に抑えた。

- **2026-06 · [OffQ: Taming Structured Outliers in LLM Quantization by Offsetting](2026-2606.07116-offq-taming-structured-outliers-in-llm-quantization-by-offsetting.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット量子化は、大規模言語モデル（LLM）の重み転送量と行列積の費用を削減する。一次論文の表1では、Llama 3-8BのWikiText困惑度が16ビットの6.1、比較方式ResQの7.1に対してOffQは6.98、8課題平均ゼロショット正解率はResQの63.91%に対して65.49%だった。

- **2026-06 · [Minimizing the Hidden Cost of Scales: Graph-Guided Ultra-Low-Bit Quantization for Large Language Models](2026-2606.05429-minimizing-the-hidden-cost-of-scales-graph-guided-ultra-low-bit-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SAGE-PTQ（Saliency-Aware Graph-guided Efficient Post-学習 量子化）は、LLM重みを1bit前後まで圧縮する際に見落とされがちな量子化スケールと重みグループの位置情報の費用を抑える方式である。

- **2026-06 · [HyperQuant: A Rate-Distortion-Optimal Quantization Pipeline for Large Language and Diffusion Models](2026-2606.23406-hyperquant-a-rate-distortion-optimal-quantization-pipeline-for-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みの低ビット化とKVの低ビット化は別々の手法が発展してきたが、ビット幅を固定した符号化では、量子化後の符号分布が偏っていても同じ長さの符号を全要素へ割り当てるため、統計的な冗長性が残る。

- **2026-06 · [Activation- and Influence-Aware Ranks (AIR): Function-Preserving SVD Compression for LLMs](2026-2606.19993-activation-and-influence-aware-ranks-air-function-preserving-svd-compres.md)**  
  実装：[✓](https://github.com/NicodeHarder/air) ・ リポジトリ内被引用：0  
  活性プロファイルと逆伝播の影響度行列を組み合わせ、閉形式の交代最小二乗走査で近似誤差を影響度の高い重みから遠ざける特異値分解圧縮。活性のみの方式より高圧縮で品質を保ち、較正データも大幅に減らせる。

- **2026-05 · [Theory-optimal Quantization Based on Flatness](2026-2605.18800-theory-optimal-quantization-based-on-flatness.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低bitの重み・活性化量子化でoutlierが量子化誤差を拡大する問題を、行列の二方向の分布平坦化として捉える。LLaMA3-70BのW2A4KV16でFlatQuant比C4 PPLを19.64から16.39に改善し、A100のプリフィルで最大3.44倍の高速化を報告。

- **2026-05 · [The Quantization Benefits of Residual-Free Transformers](2026-2605.25880-the-quantization-benefits-of-residual-free-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、Transformerの量子化を難しくする活性値の外れ値が、量子化器の選択だけでなくモデルの残差接続（Residual Connection）という構造に起因し得ることを示す。

- **2026-05 · [SPARQLe: Sub-Precision Activation Representation for Quantized LLM Inference](2026-2606.00365-sparqle-sub-precision-activation-representation-for-quantized-llm-infere.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  8ビット活性の上位4ビットが多くゼロになる冗長性を利用し、密な下位ビットと疎な上位ビットへ分解して専用加速器で直接計算する協調設計。量子化方式は変えずに遅延を最大で約24パーセント短縮した。

- **2026-05 · [Scaled Outer Product: A Hardware-Aware, Per-Layer Methodology for Post-Training Quantization of Large Language Models](2026-2605.14929-scaled-outer-product-a-hardware-aware-per-layer-methodology-for-post-tra.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロックごとの拡大率、層ごとの符号帳の組の探索、活性で重み付けた類似度による昇格配分を組み合わせた学習後量子化の方法論で、推奨動作点では六・五ビットで八・〇ビットの八ビット基準より重み再構成誤差が低く、一・五ビット節約できた。完全な評価は別論文に委ねられる。

- **2026-05 · [QAM-W: Joint 2D Codebook Quantization for LLM Weights via Hadamard Rotation and Activation-Aware Scaling](2026-2605.26339-qam-w-joint-2d-codebook-quantization-for-llm-weights-via-hadamard-rotati.md)**  
  実装：[✓](https://github.com/white07S/qam-w) ・ リポジトリ内被引用：0  
  通常のスカラー学習後量子化（scalar post-学習 量子化）は各重みをほぼ独立に離散値へ丸める。TinyLlama-1.1B、Qwen2.5-3B、Mistral-7Bの主比較では5.5ビット相当のQAM-WでWikiText-2のパープレキシティー（PPL）がBF16比+0.4%、+0.3%、+0.1%に留まる。

- **2026-05 · [ProjQ: Project-and-Quantize for Adapter-Aware LLM Compression](2026-2606.00494-projq-project-and-quantize-for-adapter-aware-llm-compression.md)**  
  実装：[✓](https://github.com/yy9301/ProjQ) ・ リポジトリ内被引用：0  
  量子化ノイズを直交射影でLoRAが直せる低ランク部分空間へ閉じ込め、補正不能な残差を最小化してから共分散-awareな閉形式でアダプタを初期化することで、3ビットで4ビット級の性能を出す量子化枠組み。

- **2026-05 · [MARR: Module-Adaptive Residual Reconstruction for Low-Bit Post-Training Quantization](2026-2605.17997-marr-module-adaptive-residual-reconstruction-for-low-bit-post-training-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MARR（Module-適応的 Residual Reconstruction）は、学習済みモデルを追加学習せず低ビットへ変換する学習後量子化（post-学習 量子化; PTQ）で、層をまたぐ量子化誤差の補正を強めすぎないための方法である。

- **2026-05 · [LASER: Loss-Aware Singular-value Decomposition and Rank Allocation for Efficient Low-Precision Vision-Language Models](2026-2606.00573-laser-loss-aware-singular-value-decomposition-and-rank-allocation-for-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LASERは、視覚言語モデル（VLM）の自己注意のQ/K/V射影を低ランク化し、同時に低精度化を行う圧縮・推論実装である。

- **2026-05 · [LAQuant: A Simple Overhead-free Large Reasoning Model Quantization by Layer-wise Lookahead Loss](2026-2605.08755-laquant-a-simple-overhead-free-large-reasoning-model-quantization-by-lay.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LAQuantは、数学やコード生成のように長い思考列を生成する大規模推論モデル（LRM）の重みのみの量子化を対象とする。Qwen3-4Bの3ビット重み・128要素グループ（W3G128）でAIME2025 Pass@1は54.69%。

- **2026-05 · [Influence-Inspired Spectral Rotations for Extreme Low-Bit LLM Quantization](2026-2605.25203-influence-inspired-spectral-rotations-for-extreme-low-bit-llm-quantizati.md)**  
  実装：[✓](https://github.com/gogipav14/spectral-llm) ・ リポジトリ内被引用：0  
  この論文は、LLMの重みを極端に少ないビット数へ丸めるとき、同じ量子化グループ内でも出力に強く影響する方向を優先して精度を残す方法を検討する。ただし4ビットではQwen2.5-1.5BのPPLが9.65から9.71となり、評価ノイズの範囲で改善が見られない。

- **2026-05 · [Importance-Guided Basis Selection for Low-Rank Decomposition of Large Language Models](2026-2605.01627-importance-guided-basis-selection-for-low-rank-decomposition-of-large-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ランク圧縮の基底選択を特異値の大きさから、勾配とヘッセ対角で推定する損失増加の重要度へ置き換え、深い圧縮でも正解率の崩れを緩やかにする基底選択方式BSI。

- **2026-05 · [GPTQ-intrinsic LoRA: A Near-optimal Algorithm for Low-precision Quantization with Low-rank Adaptation](2026-2606.01412-gptq-intrinsic-lora-a-near-optimal-algorithm-for-low-precision-quantizat.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを3〜4ビットへ圧縮すると、各重みを丸める量子化誤差が積み重なり、困惑度や下流課題の品質が悪化する。

- **2026-05 · [GoQuant: Geometric Orthogonal Residual Projection for Multiplier-Reduced Power-of-Two Transformer Quantization](2026-2605.26092-goquant-geometric-orthogonal-residual-projection-for-multiplier-reduced-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Transformerを低ビットで実行する際、重みを2の冪乗（Power-of-Two、PoT）に量子化すると、一般的な重み乗算をシフトと加算へ置き換えやすい。

- **2026-05 · [Distribution-aware Low-bitwidth Quantization for Large Language Models](2026-5e4ab017b5df-distribution-aware-low-bitwidth-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLM重みの2〜3ビット学習後量子化を、重み分布を保つKLDキャリブレーション、ノイズ置換による学習可能なコードブック最適化、分布類似度による層グループ化の3機構で実現し、量子化後ファインチューニングなしで先行手法と競合する精度を示した研究。

- **2026-05 · [BCJR-QAT: A Differentiable Relaxation of Trellis-Coded Weight Quantization](2026-2605.10655-bcjr-qat-a-differentiable-relaxation-of-trellis-coded-weight-quantizatio.md)**  
  実装：[✓](https://github.com/Venugopalan2610/quant-2bit) ・ リポジトリ内被引用：0  
  BCJR-QATは、トレリス符号化量子化（Trellis-Coded Quantization; TCQ）を使うLLMの2ビット重み表現に対し、量子化認識学習（Quantization-Aware 学習; QAT）を適用する方法である。

- **2026-05 · [A general tensor-structured compression scheme for efficient large language models](2026-2605.25344-a-general-tensor-structured-compression-scheme-for-efficient-large-langu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MixT（Mixture of Tensors）は、Transformer内の密な線形変換を、局所的なテンソル演算子を複数重ねた構造に置き換える方式である。

- **2026-04 · [SA-ANT: Efficient Low-Bit Group-Wise Quantization for Large Language Models via Sign-Asymmetric Adaptive Numeric Type](2026-4afc6233177a-sa-ant-efficient-low-bit-group-wise-quantization-for-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  3ビットなどの低ビット重み量子化では、各グループの重み分布に量子化点をどれだけ合わせられるかが品質を大きく左右する。Qwen2.5-0.5Bの5つのゼロショットタスク平均正答率は、BitModの46.44%に対しSA-ANT-L47.52%、SA-ANT-P50.36%となった。

- **2026-04 · [ReSpinQuant: Efficient Layer-Wise LLM Quantization via Subspace Residual Rotation Approximation](2026-2604.11080-respinquant-efficient-layer-wise-llm-quantization-via-subspace-residual-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層別の密な回転を重みへ融合し、残差の基底のずれを低次元部分空間で近似することで、層別適応の品質をほぼ追加計算なしに得る量子化方式を提案した。

- **2026-04 · [LBLLM: Lightweight Binarization of Large Language Models via Three-Stage Distillation](2026-2604.19167-lbllm-lightweight-binarization-of-large-language-models-via-three-stage-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LBLLMは、既存の大規模言語モデルを極端な低ビット表現へ変換する際、重みと活性化を一度に量子化して学習すると誤差が増幅し、蒸留が不安定になる問題を扱う。LLaMA-2-7Bの同等ビット幅で、LBLLMのWikiText-2困惑度は9.18、C4困惑度は10.91、六つの常識推論課題の平均正答率は54.91%となった。

- **2026-04 · [Initialisation Determines the Basin: Efficient Codebook Optimisation for Extreme LLM Quantization](2026-2604.08118-initialisation-determines-the-basin-efficient-codebook-optimisation-for-.md)**  
  実装：[✓](https://github.com/kenno94-IK/aqlm-oaem) ・ リポジトリ内被引用：0  
  LLMを2ビット/重み（2 bpp）程度へ圧縮する際、各重みを独立に少数の整数へ丸めるスカラー量子化では品質低下が大きくなる。

- **2026-04 · [D-QReLO: Training- and Data-Free Delta Compression for Large Language Models via Quantization and Residual Low-Rank Approximation](2026-2604.16940-d-qrelo-training-and-data-free-delta-compression-for-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模微調整で大きくなったデルタ重みを、1ビット量子化で大枠を捉えてから残差を低ランク近似で回収する二段圧縮で、圧縮率8分の1でも性能低下を平均6.17パーセントに抑える学習不要のデルタ圧縮。

- **2026-04 · [Coverage-Based Calibration for Post-Training Quantization via Weighted Set Cover over Outlier Channels](2026-2604.24008-coverage-based-calibration-for-post-training-quantization-via-weighted-s.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CoverCal（Coverage-Based Calibration）は、LLMをAWQやGPTQでINT4事後量子化（PTQ）する際、どのサンプルを較正データとして選ぶかを改善する方式である。LLaMA-3-8BのAWQ INT4・128較正サンプルでは、MMLU 5-shot正答率がrandom 63.1%からCoverCal 64.6%へ改善した。

- **2026-04 · [CoQuant: Joint Weight-Activation Subspace Projection for Mixed-Precision LLMs](2026-2604.26378-coquant-joint-weight-activation-subspace-projection-for-mixed-precision-.md)**  
  実装：[✓](https://github.com/Zachary5895/CoQuant) ・ リポジトリ内被引用：0  
  高精度に残す部分空間を活性と重みの両方の共分散を足した混合共分散の上位の固有方向で決めることで、平均四・五ビットで常識推論の平均正解率五七・五九パーセントと従来の最良を一・九三点上回り、三ビット級でも困惑度の破綻を抑えたと報告した。

- **2026-03 · [TTQ: Activation-Aware Test-Time Quantization to Accelerate LLM Inference On The Fly](2026-2603.19296-ttq-activation-aware-test-time-quantization-to-accelerate-llm-inference-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化の較正を配置前に済ませる前提をやめ、プロンプト自身の活性値からその場で尺度を決めることで、ドメインシフトに弱い静的量子化を、較正データなしで適応できる量子化へ変えた方式。

- **2026-03 · [Structural Sensitivity in Compressed Transformers: Relative Error Propagation and Layer Removal](2026-2603.20991-structural-sensitivity-in-compressed-transformers-relative-error-propaga.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層ごとの誤差の収縮率を測って圧縮誤差の伝播を説明し、その1からの距離で層削除を順位付ける訓練不要の物差しで、LLaMA-2-7Bの8層削除でパープレキシティをShortGPT比1.6倍低くし物理削除で1.22倍高速化する分析と手法。

- **2026-03 · [RAMP: Reinforcement Adaptive Mixed Precision Quantization for Efficient On Device LLM Inference](2026-2603.17891-ramp-reinforcement-adaptive-mixed-precision-quantization-for-efficient-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層の十一項目の特徴だけを見てビット幅を逐次決める強化学習の方策により、七十億級モデルで困惑度五・五四を三・六八ギガバイトで達成して一様四ビットの代表方式を大きさと品質の両方で上回り、一つのモデルで学んだ方策が別系統・別規模のモデルへ再学習なしで移って直接学習と同等以上になることを示した。

- **2026-03 · [Mitigating the impact of activation smoothing on weights: A channel permutation and smoothing-based LLMs quantization method](2026-d621875e47b5-mitigating-the-impact-of-activation-smoothing-on-weights-a-channel-permu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  4ビット重み・8ビット活性（W4A8）の推論では、活性の少数の極端な値が量子化範囲を支配する。結果として小さな重みの丸め誤差が増え、活性側の改善を重み側の劣化が相殺する。

- **2026-03 · [HALO: Hardware-Aware Quantization with Low Critical-Path-Delay Weights for LLM Acceleration](2026-2502.19662-halo-hardware-aware-quantization-with-low-critical-path-delay-weights-fo.md)**  
  実装：[✓](https://github.com/ecolab-nus/HALO) ・ リポジトリ内被引用：0  
  重みの数値精度を下げれば計算器やメモリの費用は小さくなる。HALOはこの差を量子化設計へ直接持ち込み、重要な重みを保護しつつ、残りの重みを回路遅延の短い離散値へ写像する。

- **2026-03 · [GlowQ: Group-Shared LOw-Rank Approximation for Quantized LLMs](2026-2603.25385-glowq-group-shared-low-rank-approximation-for-quantized-llms.md)**  
  実装：[✓](https://github.com/ahnselim/GlowQ) ・ リポジトリ内被引用：0  
  量子化誤差の低ランク補正の右因子を入力共有グループで共有し、射影を1回だけ計算して使い回す方式。共分散整合でランク配分を適正化し、選択的復元で遅延を大きく下げる。

- **2026-03 · [DAQ: Delta-Aware Quantization for Post-Training LLM Weight Compression](2026-2603.22324-daq-delta-aware-quantization-for-post-training-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Tencent/AngelSlim) ・ リポジトリ内被引用：0  
  量子化の目的を重み再構成から、学習後微調整の更新の方向の保存へ変える方式。データなしでスケールを探索し、微調整で得た振る舞いを保ったままFP8へ圧縮する。

- **2026-02 · [Two-Stage Grid Optimization for Group-wise Quantization of LLMs](2026-2602.02126-two-stage-grid-optimization-for-group-wise-quantization-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPTQのグループ別スケールを、入力統計による初期化と層再構成損失の座標降下による洗練の二段で決め直す量子化。2ビットでの精度崩壊を大きく緩和する。

- **2026-02 · [The AetherFloat Family: Block-Scale-Free Quad-Radix Floating-Point Architectures for AI Accelerators](2026-2603.08741-the-aetherfloat-family-block-scale-free-quad-radix-floating-point-archit.md)**  
  実装：[✓](https://github.com/k1832/aetherfloat-validation) ・ リポジトリ内被引用：0  
  基数4の指数と明示的な仮数でブロック・スケーリング回路を不要にし、積和演算器の面積を33.17パーセント減らす浮動小数点形式群。16ビット版はほぼ無損失、8ビット版は微調整前提。

- **2026-02 · [ROCKET: Rapid Optimization via Calibration-guided Knapsack Enhanced Truncation for Efficient Model Compression](2026-2602.11008-rocket-rapid-optimization-via-calibration-guided-knapsack-enhanced-trunc.md)**  
  実装：[✓](https://github.com/mts-ai/ROCKET/tree/main) ・ リポジトリ内被引用：0  
  辞書学習を閉形式の1パスで置き換えた疎な行列因数分解と、層別圧縮配分の多選択ナップサック最適化を組み合わせ、学習なしで高圧縮でも性能を保つモデル圧縮方式。

- **2026-02 · [Revisiting Adaptive Rounding with Vectorized Reparameterization for LLM Quantization](2026-2602.02151-revisiting-adaptive-rounding-with-vectorized-reparameterization-for-llm-.md)**  
  実装：[✓](https://github.com/zhoustan/VQRound) ・ リポジトリ内被引用：0  
  適応型丸めの丸め行列をコードブックで表し直し、学習量を最大で元の0.2パーセント程度まで削る量子化。初期化の工夫と合わせて、2ビットでも崩壊を避ける。

- **2026-02 · [QuEPT: Quantized Elastic Precision Transformers with One-Shot Calibration for Multi-Bit Switching](2026-2602.12609-quept-quantized-elastic-precision-transformers-with-one-shot-calibration.md)**  
  実装：[✓](https://github.com/xuke225/QuEPT) ・ リポジトリ内被引用：0  
  一回の較正で複数ビット幅へ対応する弾性量子化QuEPTを提案し、ビット幅間の特徴融合と段階的低ランク補償で競合を抑え、再最適化なしのビット幅切り替えと混合精度化を可能にする。

- **2026-02 · [On the Importance of a Multi-Scale Calibration for Quantization](2026-2602.07465-on-the-importance-of-a-multi-scale-calibration-for-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定長キャリブレーションが落とす入力長依存の活性値分布を、複数長の系列を長さ正規化して系列単位で等しく混ぜるMaCaでヘッセ行列へ取り込み、低ビット量子化の精度を同一トークン予算で改善する。

- **2026-02 · [LittleBit-2: Maximizing the Spectral Energy Gain in Sub-1-Bit LLMs via Latent Geometry Alignment](2026-2603.00042-littlebit-2-maximizing-the-spectral-energy-gain-in-sub-1-bit-llms-via-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LittleBit-2は、学習済み大規模言語モデル（LLM）の重み行列を低ランクの二値因子に分解するLittleBit方式を改良し、二値化の直前に潜在空間を回転して量子化誤差を小さくする研究である。

- **2026-02 · [LATMiX: Learnable Affine Transformations for Microscaling Quantization of LLMs](2026-2602.17681-latmix-learnable-affine-transformations-for-microscaling-quantization-of.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LATMiXは、低ビット量子化で問題になる活性値の外れ値を、量子化する前の可逆な座標変換によって緩和する事後量子化手法である。Qwen3-4BのMXFP4では単純GPTQの7課題平均62.11%に対しLATMiX-LUは64.74%、MXINT4では55.09%に対し63.63%である。

- **2026-02 · [COMPOT: Calibration-Optimized Matrix Procrustes Orthogonalization for Transformers Compression](2026-2602.15200-compot-calibration-optimized-matrix-procrustes-orthogonalization-for-tra.md)**  
  実装：[✓](https://github.com/mts-ai/COMPOT) ・ リポジトリ内被引用：0  
  較正で白色化した重みを直交辞書と疎な係数の積へ分解し、辞書更新を閉形式のプロクルステス解、係数更新をハード閾値処理で解くことで、単一共有部分空間の低ランク圧縮より高い精度を訓練なしで保つ圧縮方式の研究。

- **2026-02 · [Astro: Activation-guided Structured Regularization for Outlier-Robust LLM Post-Training Quantization](2026-2602.07596-astro-activation-guided-structured-regularization-for-outlier-robust-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Astroは、LLMの重みのみの事後量子化（重み-only PTQ）において、外れ値に由来する精度低下を抑えるための量子化前処理である。

- **2026-02 · [A Case Study of Selected PTQ Baselines for Reasoning LLMs on Ascend NPU](2026-2602.17693-a-case-study-of-selected-ptq-baselines-for-reasoning-llms-on-ascend-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は新規量子化法の提案ではなく、既存の事後量子化（PTQ）をHuawei Ascend 910Bへ移した場合の再現性と実装費用を測定する事例研究である。

- **2026-01 · [StableQAT: Stable Quantization-Aware Training at Ultra-Low Bitwidths](2026-2601.19320-stableqat-stable-quantization-aware-training-at-ultra-low-bitwidths.md)**  
  実装：[✓](https://github.com/microsoft/StableQAT) ・ リポジトリ内被引用：0  
  量子化考慮学習（Quantization-Aware 学習、QAT）は、学習時に重みを低ビットへ丸めることによる誤差をモデルに経験させ、推論時の低ビット実装に適応させる手法である。

- **2026-01 · [Sliced-Wasserstein Distribution Alignment Loss Improves the Ultra-Low-Bit Quantization of Large Language Models](2026-2601.07878-sliced-wasserstein-distribution-alignment-loss-improves-the-ultra-low-bi.md)**  
  実装：[✓](https://github.com/TokuyuSou/SWLoss_LightCompress) ・ リポジトリ内被引用：0  
  本論文は、大規模言語モデル（LLM）を4ビット未満へ量子化するとき、従来の要素ごとの再構成誤差だけでは失われる情報があることに着目する。LLaMA-2-7Bの重み4ビット・活性値4ビット（W4A4）では、六つのゼロショット課題の平均正答率がOmniQuantの46.24%から48.92%へ改善した。

- **2026-01 · [RPIQ: Residual-Projected Multi-Collaboration Closed-Loop and Single Instance Quantization for Visually Impaired Assistance](2026-2601.02888-rpiq-residual-projected-multi-collaboration-closed-loop-and-single-insta.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RPIQ（Residual-Projected Multi-Collaboration Closed-Loop and Single Instance Quantization）は、視覚障害者向け支援を動機として、大規模言語モデルと視覚言語モデルを少ないメモリで利用するために提案された重みの事後量子化（post-学習 量子化、PTQ）手法である。

- **2026-01 · [Post-Training Probability Manifold Correction via Structured SVD Pruning and Self-Referential Distillation](2026-2602.00372-post-training-probability-manifold-correction-via-structured-svd-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Sparse Knowledge Distillation（SparseKD）は、すでに学習を終えた自己回帰言語モデルのMLP重みを構造的に低ランク化し、その変換によって崩れた出力確率分布を、元モデル自身を教師とする蒸留で修復する手法である。

- **2026-01 · [Float8@2bits: Entropy Coding Enables Data-Free Model Compression](2026-2601.22787-float8-2bits-entropy-coding-enables-data-free-model-compression.md)**  
  実装：[✓](https://github.com/merantix-momentum/entquant) ・ リポジトリ内被引用：0  
  8ビット形式の表現力を保ったまま重みのエントロピーを下げて無損失圧縮し、実効2ビット台の保存量をデータなしで実現する圧縮方式で、較正手法並みの品質を保ちながら70Bを10分未満で圧縮した。

- **2026-01 · [Enhancing Post-Training Quantization via Future Activation Awareness](2026-2602.02538-enhancing-post-training-quantization-via-future-activation-awareness.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  後続三層の活性を平均した予告信号を現在の活性へ重み〇・八五で融合して量子化の倍率を作ることで、三ビット量子化で八十億級モデルの困惑度を一一・六九から一一・五一へ下げ、五億級モデルでは二九・一三から二五・九六へ大きく改善し、校正データ量を変えてもばらつきが約三分の一になった。

- **2026-01 · [Breaking the Blocks: Continuous Low-Rank Decomposed Scaling for Unified LLM Quantization and Adaptation](2026-2601.22716-breaking-the-blocks-continuous-low-rank-decomposed-scaling-for-unified-l.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LoRDS（Low-Rank Decomposed Scaling）は、重みを低ビット整数に変換するときのスケール因子の表現を変える方式である。

- **2026-01 · [Benford's Law as a Distributional Prior for Post-Training Quantization of Large Language Models](2026-2602.00165-benford-s-law-as-a-distributional-prior-for-post-training-quantization-o.md)**  
  実装：[✓](https://github.com/ufopcsilab/benford-quant) ・ リポジトリ内被引用：0  
  変換層の重みがベンフォード則に近いという診断から対数間隔コードブックBenQを作り、データなし量子化で一様RTNを上回りNF4と互角に渡り合う一方、正規化層は高精度に残す選択的量子化。

- **2025-12 · [Rethinking Output Alignment For 1-bit Post-Training Quantization of Large Language Models](2025-2512.21651-rethinking-output-alignment-for-1-bit-post-training-quantization-of-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデル（Large Language モデル; LLM）を事後量子化（Post-学習 量子化; PTQ）で1ビットへ圧縮すると、重みをほぼ±1に制限するため、4ビットなどの量子化より精度劣化が大きい。

- **2025-12 · [Efficient LLM Deployment in Consumer Electronics Applications via Resource-Aware and Salience-Guided Quantization](2025-38c6f5463687-efficient-llm-deployment-in-consumer-electronics-applications-via-resour.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  全層を一律2ビットへ下げるとモデルは小さくなるが、重要な重みの量子化誤差によって生成品質が悪化し得る。

### 2年前（2024-12〜2025-11）

- **2025-04 · [SpinQuant: LLM quantization with learned rotations](2025-2405.16406-spinquant-llm-quantization-with-learned-rotations.md)**  
  実装：[✓](https://github.com/facebookresearch/SpinQuant) ・ リポジトリ内被引用：274  
  外れ値が低ビット量子化の誤差を大きくする問題に対して、全精度の機能を保つ旋回行列を学習し、重み・活性値・KVキャッシュの量子化に合わせる。

- **2025-04 · [HIGGS: Pushing the Limits of Large Language Model Quantization via the Linearity Theorem](2025-2411.17525-higgs-pushing-the-limits-of-large-language-model-quantization-via-the-li.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  HIGGSは、LLMの各重み行列を別々に量子化するとき、どの誤差指標を最小化すればモデル全体の予測品質を守れるのかを理論と実験の両面から扱う。GPU実装面では、RTX 4090でLlama-3.1-8Bの4ビットHIGGSをFLUTEカーネルで実行すると、バッチ1で139トークン/秒、FP16は57トークン/秒だった。

- **2025-11 · [DartQuant: Efficient Rotational Distribution Calibration for LLM Quantization](2025-2511.04063-dartquant-efficient-rotational-distribution-calibration-for-llm-quantiza.md)**  
  実装：[✓](https://github.com/CAS-CLab/DartQuant) ・ リポジトリ内被引用：14  
  DartQuantは、大規模言語モデル（LLM）の低ビット量子化で問題になる活性値の外れ値を、直交回転行列の校正によって緩和する方法である。時間比は約47倍、メモリ比は約10倍である。

- **2025-02 · [M-ANT: Efficient Low-bit Group Quantization for LLMs via Mathematically Adaptive Numerical Type](2025-2502.18755-m-ant-efficient-low-bit-group-quantization-for-llms-via-mathematically-a.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  一般的なINT4量子化は整数演算に向くが、各値の分布が一様でないと量子化誤差が大きくなる。専用アクセラレータのシミュレーションでは、先行するLLMアクセラレータに対して平均2.99倍、最大4.46倍の高速化と、平均2.81倍、最大4.10倍のエネルギー削減を報告する。

- **2025-10 · [QSVD: Efficient Low-rank Approximation for Unified Query-Key-Value Weight Compression in Low-Precision Vision-Language Models](2025-2510.16292-qsvd-efficient-low-rank-approximation-for-unified-query-key-value-weight.md)**  
  実装：[✓](https://github.com/SAI-Lab-NYU/QSVD) ・ リポジトリ内被引用：12  
  QSVDは、画像と文章を同時に処理する視覚言語モデル（Vision-Language モデル; VLM）の注意層で、問い合わせ（Query; Q）・鍵（Key; K）・値（Value; V）の射影重みを別々に圧縮するのではなく結合して低ランク分解する手法である。

- **2025-04 · [MiLo: Efficient Quantized MoE Inference with Mixture of Low-Rank Compensators](2025-2504.02658-milo-efficient-quantized-moe-inference-with-mixture-of-low-rank-compensa.md)**  
  実装：[✓](https://github.com/Supercomputing-System-AI-Lab/MiLo) ・ リポジトリ内被引用：12  
  Mixtral-8×7Bの半精度重みは約90GBに達し、単一の40GBや80GBのGPUに収まりにくい。4ビット量子化は比較的品質を保てる一方、3ビットに下げると重みを表現できる値が減り、WikiText-2の予測性能が顕著に悪化する。論文はMixtral-8×7BとDeepSeek-MoEで精度を測り、A100 40GBで推論遅延も測定した。

- **2025-08 · [LMDeploy Accelerates Mixed-Precision LLM Inference with TurboMind](2025-2508.15601-efficient-mixed-precision-large-language-model-inference.md)**  
  実装：[✓](https://github.com/InternLM/lmdeploy) ・ リポジトリ内被引用：11  
  量子化された重みを行列積の直前に浮動小数点へ復号すると、復号命令と共有メモリへの転送が計算の待ち時間になる。既存の混合精度推論基盤に対して配信遅延を最大61%（平均30%）削減し、処理率を最大156%（平均58%）向上したと報告する。

- **2025-10 · [INT v.s. FP: A Comprehensive Study of Fine-Grained Low-bit Quantization Formats](2025-2510.25602-int-v-s-fp-a-comprehensive-study-of-fine-grained-low-bit-quantization-fo.md)**  
  実装：[✓](https://github.com/ChenMnZ/INT_vs_FP) ・ リポジトリ内被引用：10  
  しかし、32要素や16要素ごとに独立した尺度を持つ細粒度量子化では、外れ値と典型値を同じ広い範囲へ押し込める必要が小さくなる。ハードウェアの評価は論理回路モデルによる推定であり、MXINT8のエネルギーがMXFP8の0.63倍という数値を、既存GPUの実測消費電力や推論速度と混同してはならない。

- **2025-02 · [Huff-LLM: End-to-End Lossless Compression for Efficient LLM Inference](2025-2502.00922-huff-llm-end-to-end-lossless-compression-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  Huff-LLMは、言語モデルの重みを数値を一切変えずに圧縮し、保存先から推論演算器の直前まで圧縮状態を維持する方式である。Llama、Qwen、OPT、Vicunaの重みで容量削減を測定し、専用推論回路のモデル化で最大約32%の重み容量削減、最大約31%の推論遅延短縮、最大約26%のエネルギー削減を報告する。

- **2025-05 · [DLP: Dynamic Layerwise Pruning in Large Language Models](2025-2505.23807-dlp-dynamic-layerwise-pruning-in-large-language-models.md)**  
  実装：[✓](https://github.com/ironartisan/DLP) ・ リポジトリ内被引用：8  
  DLP（動的 Layerwise 枝刈り、動的層別刈り込み）は、重みのどれを削るかだけでなく、各層に何割の重みを残すかを決めるためのモデル圧縮方式である。ただし同じ70%の疎化率でも、重要な層を一律に70%削ると、あまり重要でない層を多く削る場合より予測品質が大きく損なわれる。

- **2025-04 · [Mitigating Quantization Errors Due to Activation Spikes in Gated Linear Unit-Based Large Language Models](2025-2405.14428-mitigating-quantization-errors-due-to-activation-spikes-in-gated-linear-.md)**  
  実装：[✓](https://github.com/onnoo/activation-spikes) ・ リポジトリ内被引用：7  
  Yangらは、SwiGLUなどのゲート付き線形ユニット（GLU）を用いる大規模言語モデルで、少数のトークン位置に非常に大きい活性化値が現れ、活性化の量子化スケールを過大にする現象を調べた。著者はLLaMA-2を中心にW8A8量子化の精度低下を軽減し、代表的なzero-shot指標で量子化ベースラインより約7〜16%の改善を報告する。

- **2025-01 · [BlockDialect: Block-wise Fine-grained Mixed Format Quantization for Energy-Efficient LLM Inference](2025-2501.01144-blockdialect-block-wise-fine-grained-mixed-format-quantization-for-energ.md)**  
  実装：[✓](https://code.stanford.edu/tambe-lab/blockdialect) ・ リポジトリ内被引用：7  
  著者らは、符号1ビットと値索引3ビットという4ビット格納形式を保ちつつ、16種類の表現可能値集合を用意するDialectFP4を提案する。LLaMA3-8Bで注意行列積まで含めて量子化した場合、最良のブロック混合設定では7課題平均正答率69.00%、比較対象のMXFP4-16は58.22%、全精度FP16は74.45%である（原著Table 1）。

- **2025-09 · [SINQ: Sinkhorn-Normalized Quantization for Calibration-Free Low-Precision LLM Weights](2025-2509.22944-sinq-sinkhorn-normalized-quantization-for-calibration-free-low-precision.md)**  
  実装：[✓](https://github.com/huawei-csl/SINQ) ・ リポジトリ内被引用：6  
  通常の4ビットあるいは3ビット重み量子化では、同じ量子化群に非常に大きな重みが混ざると、その外れ値に合わせて量子化刻みを広げる必要がある。これを「モデル全体が3.5倍高速になった」と解釈してはいけない。

- **2025-09 · [PTQTP: Post-Training Quantization to Trit-Planes for Large Language Models](2025-2509.16989-ptqtp-post-training-quantization-to-trit-planes-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  PTQTPは、学習済み重みを2枚の三値平面（trit-plane）と連続尺度へ分解し、約1.58ビット級の超低ビット表現を事後量子化（Post-学習 量子化; PTQ）だけで作る。二値PTQより表現力を増やしつつ、混合精度の例外経路を使わず一様な三値演算へ落とすのが狙いである。

- **2025-09 · [Quant-dLLM: Post-Training Extreme Low-Bit Quantization for Diffusion Large Language Models](2025-2510.03274-quant-dllm-post-training-extreme-low-bit-quantization-for-diffusion-larg.md)**  
  実装：[✓](https://github.com/ZTA2785/Quant-dLLM) ・ リポジトリ内被引用：5  
  本研究は、拡散型大規模言語モデル（diffusion large language モデル、以下dLLM）の重みを、追加の勾配学習なしに平均2ビットへ圧縮しながら、生成・推論課題の正答率を維持する手法を提案する。

- **2025-06 · [Unifying Uniform and Binary-coding Quantization for Accurate Compression of Large Language Models](2025-2506.03781-unifying-uniform-and-binary-coding-quantization-for-accurate-compression.md)**  
  実装：[✓](https://github.com/snudm-starlab/UniQuanF) ・ リポジトリ内被引用：5  
  UQは一定間隔に並んだ量子化レベルを使う。Llama-3 8B InstructのGSM8Kでは3ビットでUniQuanFが58.73%、FlexRoundが54.13%で、差は4.60パーセントポイント。

- **2025-05 · [ICQuant: Index Coding enables Low-bit LLM Quantization](2025-2505.00850-icquant-index-coding-enables-low-bit-llm-quantization.md)**  
  実装：[✓](https://github.com/Avery-xl/ICQuant) ・ リポジトリ内被引用：5  
  ICQuant（Index Coding enables Low-bit LLM Quantization）は、大規模言語モデル（LLM）の重みを2〜3ビット程度へ圧縮する際、少数の極端な値が量子化範囲を不必要に広げる問題を、外れ値の分離と位置索引の効率的な符号化で解く学習後量子化（Post-学習 量子化; PTQ）方式である。

- **2025-05 · [ERC-SVD: Error-Controlled SVD for Large Language Model Compression](2025-2505.20112-erc-svd-error-controlled-svd-for-large-language-model-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  切り捨て残差を2段目の特異値分解で回収する残差補償と、最後の数層だけへの部分層圧縮で誤差伝播を抑える、学習不要の特異値分解圧縮手法。同じ圧縮率で既存の特異値分解系手法より品質を保つ。

- **2025-05 · [Addition is almost all you need: Compressing large language models with double binary factorization](2025-2505.11076-addition-is-almost-all-you-need-compressing-large-language-models-with-d.md)**  
  実装：[✓](https://github.com/usamec/double_binary) ・ リポジトリ内被引用：5  
  大規模言語モデルの重みを低ビット化すると、モデルの保存容量とメモリ帯域要求を減らせる。ただし一般的な量子化は、実行時に低ビットの重みを展開して高精度の積和演算を行うことが多い。RTX4090でのバッチ1復号では、Llama3-8BのFP16 60 トークン/sに対して2bit DBFが133 トークン/s、約2.22倍となる。

- **2025-04 · [OAC: Output-adaptive Calibration for Accurate Post-training Quantization](2025-2405.15025-oac-output-adaptive-calibration-for-accurate-post-training-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  重みを2ビットあるいは1ビットに圧縮すると、元の浮動小数点重みを丸める際の誤差が大きくなり、通常の層単位の校正だけではモデルの最終予測が著しく悪化する。

- **2025-02 · [LO-BCQ: Locally Optimal Block Clustered Quantization for 4-bit (W4A4) LLM Inference](2025-2502.05376-lo-bcq-locally-optimal-block-clustered-quantization-for-4-bit-w4a4-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  主題は、大規模言語モデルの重みと活性値の両方を4ビット程度へ量子化し、再学習を行わずに推論品質を保つ事後量子化（Post-学習 量子化; PTQ）である。代表例としてLlama2-7Bの5つの言語理解課題平均では、BF16の65.65%に対し、実効4.5ビットのLO-BCQは64.68%となり、0.97ポイント低下した。

- **2025-01 · [Pivoting Factorization: A Compact Meta Low-Rank Representation of Sparsity for Efficient Inference in Large Language Models](2025-2501.19090-pivoting-factorization-a-compact-meta-low-rank-representation-of-sparsit.md)**  
  実装：[✓](https://github.com/biomedical-cybernetics/pivoting-factorization) ・ リポジトリ内被引用：5  
  ランクが行列次元の半分の単層比較では、既存低ランク層から追加でメモリ24.2%・推論時間24.6%削減を報告。PIFAの無損失は元の低ランク近似に対する再表現の性質であり、密な原モデルを無損失圧縮するという意味ではない。

- **2025-11 · [SpecQuant: Spectral Decomposition and Adaptive Truncation for Ultra-Low-Bit LLMs Quantization](2025-2511.11663-specquant-spectral-decomposition-and-adaptive-truncation-for-ultra-low-b.md)**  
  実装：[✓](https://github.com/Kishon-zzx/SpecQuant) ・ リポジトリ内被引用：4  
  本研究は、大規模言語モデル（LLM）の重みと活性を同時に4ビット程度へ圧縮するときに生じる、外れ値による量子化誤差を低減する手法を扱う。

- **2025-05 · [DenoiseRotator: Enhance Pruning Robustness for LLMs via Importance Concentration](2025-2505.23049-denoiserotator-enhance-pruning-robustness-for-llms-via-importance-concen.md)**  
  実装：[✓](https://github.com/Axel-gu/DenoiseRotator) ・ リポジトリ内被引用：4  
  DenoiseRotatorは、大規模言語モデル（LLM）の枝刈り（枝刈り）を行う前に、どの重みが重要かという分布自体を変える方式である。推論時の速度も重要で、A100上のLLaMA3-8B単層では、密行列5.80ms、回転なし2:4疎行列4.37ms、回転を含む2:4疎行列4.69msだった。

- **2025-04 · [Task-Circuit Quantization: Leveraging Knowledge Localization and Interpretability for Compression](2025-2504.07389-task-circuit-quantization-leveraging-knowledge-localization-and-interpre.md)**  
  実装：[✓](https://github.com/The-Inscrutable-X/TACQ) ・ リポジトリ内被引用：4  
  Task-Circuit Quantization（TACQ）は、学習済みLLMを2〜3ビットへ圧縮した際の性能崩壊を抑えるため、全ての重みを同じ精度で丸めるのではなく、タスクにとって重要で、かつ実際の量子化で大きな損失を引き起こしそうな重みだけを16ビットのまま残す学習後量子化方式である。

- **2025-11 · [Rotate, Clip, and Partition: Towards W2A4KV4 Quantization by Integrating Rotation and Learnable Non-uniform Quantizer](2025-2502.15779-rotate-clip-and-partition-towards-w2a4kv4-quantization-by-integrating-ro.md)**  
  実装：[✓](https://github.com/songsm921/RCP) ・ リポジトリ内被引用：3  
  重みを二ビット、活性値とキャッシュを四ビットにする極端な量子化では、単純な事後量子化や従来の量子化認識学習だけでは予測が崩れる場合がある。ピークメモリは13.48GBから2.55GBへ減り、約5.29倍の削減となる。

- **2025-10 · [ARA: Adaptive Rank Allocation for Efficient Large Language Model SVD Compression](2025-2510.19389-ara-adaptive-rank-allocation-for-efficient-large-language-model-svd-comp.md)**  
  実装：[✓](https://github.com/compressionOrg/ARA) ・ リポジトリ内被引用：3  
  ARA（適応的 Rank Allocation）は、圧縮予算を複数の線形モジュールに配る学習可能なランク選択器である。特に「80% 残存比率」はパラメータの80%を残すという意味で、80%を削る意味ではない。

- **2025-09 · [Bi-VLM: Pushing Ultra-Low Precision Post-Training Quantization Boundaries in Vision-Language Models](2025-2509.18763-bi-vlm-pushing-ultra-low-precision-post-training-quantization-boundaries.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大きな重み容量と画像トークンの計算費用があるため、小型端末への配置が難しい。Bi-VLMは、事前学習済みの視覚言語モデルを再学習せずに極低ビット化するため、重みの分布を統計的な分位点で複数群へ分け、重要な外れ値重みには2bit、その他の多数の重みには1bitを割り当てる後学習量子化方式である。

- **2025-05 · [Radio: Rate–Distortion Optimization for Large Language Model Compression](2025-2505.03031-radio-rate-distortion-optimization-for-large-language-model-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  RadioはLLM重みの事後量子化を、平均ビット数の制約下で元モデルとの出力歪みを最小化するレート・歪み最適化として定式化する。

- **2024-12 · [DecDEC: A Systems Approach to Advancing Low-Bit LLM Quantization](2024-2412.20185-decdec-a-systems-approach-to-advancing-low-bit-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  低ビット量子化（low-bit 量子化）は、LLMの重みを3ビット・4ビット程度へ圧縮し、GPUメモリと復号時の重み読出しを削減する。原著はRTX 4070 Super 12GBを含む5種類の一般消費者向けGPUで評価した。

- **2025-11 · [MLWQ: Efficient Small Language Model Deployment via Multi-Level Weight Quantization](2025-3399d40c799e-mlwq-efficient-small-language-model-deployment-via-multi-level-weight-qu.md)**  
  実装：[✓](https://github.com/hudevictor/mlwq) ・ リポジトリ内被引用：2  
  層ごとの量子化損失でビット予算を全局的に配り、層内では重要度を三段階に分けて精度を割り当て、群ごとに量子化パラメータを微調整することで、平均約3ビットでも小規模モデルの品質を守る学習後量子化。

- **2025-10 · [CARVQ: Corrective Adaptor with Group Residual Vector Quantization for LLM Embedding Compression](2025-2510.12721-carvq-corrective-adaptor-with-group-residual-vector-quantization-for-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  埋め込み行列を群ごとの残差ベクトル量子化で段階的に圧縮し、その誤差を細い多層回路の補正アダプタで直す学習後方式で、専用の低ビットハードウェアなしに平均約一・六ビットまで圧縮し、二ビットの均一量子化が崩壊する条件でも困惑度と正解率を保ったと報告した。

- **2025-09 · [RSAVQ: Riemannian Sensitivity-Aware Vector Quantization for Large Language Models](2025-2510.01240-rsavq-riemannian-sensitivity-aware-vector-quantization-for-large-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  RSAVQ（Riemannian Sensitivity-Aware Vector Quantization）は、大規模言語モデル（LLM）の重みを2〜4ビット程度に圧縮するとき、量子化誤差がどの方向へ生じるかと、どの重みチャネルへ多くのビットを割くかを同時に最適化する学習後量子化（Post-学習 量子化; PTQ）方式である。

- **2025-07 · [CCQ: Convolutional Code for Extreme Low-bit Quantization in LLMs](2025-2507.07145-ccq-convolutional-code-for-extreme-low-bit-quantization-in-llms.md)**  
  実装：[✓](https://github.com/PaddlePaddle/FastDeploy/tree/develop) ・ リポジトリ内被引用：2  
  2bit級の重み量子化では、単純な整数丸めでは表現可能な値が少なすぎて精度が大きく落ちる。原著Table 2ではDeepSeek-V3-0324の8bit版642GBに対し、CCQ 2.06bpw版は184GBで、GSM8K/C-Eval/MMLU平均が90.01から87.76へ低下する。

- **2025-06 · [AWP: Activation-Aware Weight Pruning and Quantization with Projected Gradient Descent](2025-2506.10205-awp-activation-aware-weight-pruning-and-quantization-with-projected-grad.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  層ごとの学習後圧縮を活性値つきスパース近似として定式化し、射影勾配降下法で枝刈りと量子化とその同時適用を統一的に解き、枝刈りには収束保証も与えた圧縮方式の研究。

- **2025-05 · [RWKVQuant: Quantizing the RWKV Family with Proxy Guided Hybrid of Scalar and Vector Quantization](2025-2505.03803-rwkvquant-quantizing-the-rwkv-family-with-proxy-guided-hybrid-of-scalar-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  Transformer向けに有効な学習後量子化（PTQ）をそのままRWKVへ移すと、重み分布と非線形演算の違いから精度が大きく落ちたり、量子化前後の変換演算が追加されたりする。

- **2025-05 · [NeUQI: Near-Optimal Uniform Quantization Parameter Initialization for Low-Bit LLMs](2025-2505.17595-neuqi-near-optimal-uniform-quantization-parameter-initialization-for-low.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低ビットの言語モデルを作る際、重みを整数格子へ写す一様量子化は既存GPUの整数演算・メモリ削減と相性がよい。

- **2025-04 · [Achieving Binary Weight and Activation for LLMs Using Post-Training Quantization](2025-2504.05352-achieving-binary-weight-and-activation-for-llms-using-post-training-quan.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  重みに所属ビットを足して四つの自由な代表値を持たせ期待値最大化法で決め、活性値の四ビットを四つの一ビットへ分解して内積を論理演算で計算する学習後量子化で、実質二ビット・四ビット設定の困惑度を七十億モデルで八・五八まで抑え、行列積カーネルで従来カーネルの約三倍の高速化を報告した。

- **2025-03 · [RSQ: Learning from Important Tokens Leads to Better Quantized LLMs](2025-2503.01820-rsq-learning-from-important-tokens-leads-to-better-quantized-llms.md)**  
  実装：[✓](https://github.com/ylsung/rsq) ・ リポジトリ内被引用：2  
  GPTQなどの事後量子化（Post-学習 量子化; PTQ）は、元の重みを低ビットへ丸めるとき、少数の校正データで量子化前後の層出力を比較して誤差を補償する。2bit条件ではQuaRotの平均35.3%に対しRSQは40.6%となる。

- **2025-03 · [EfficientLLaVA:Generalizable Auto-Pruning for Large Vision-language Models](2025-2503.15369-efficientllava-generalizable-auto-pruning-for-large-vision-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  EfficientLLaVAは、画像と文章を扱う大規模視覚言語モデル（Large Vision-Language モデル; LVLM）の重みを、元の巨大な学習データを持たずに削減するための自動枝刈り方式である。

- **2025-02 · [MEADOW: Memory-efficient Dataflow and Data Packing for Low Power Edge LLMs](2025-2503.11663-meadow-memory-efficient-dataflow-and-data-packing-for-low-power-edge-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  低消費電力エッジ向けに、アテンションの中間結果をオンチップへ保つトークン並列・ヘッド逐次のデータフローと、重みを一意な要素へロスレス分解するパッキングを組み合わせ、オフチップメモリへのアクセスを減らす実装フレームワーク。10W未満のFPGAでプリフィルが2.5倍、デコードが1.5倍速くなった。

- **2024-12 · [RILQ: Rank-Insensitive LoRA-based Quantization Error Compensation for Boosting 2-bit Large Language Model Accuracy](2024-2412.01129-rilq-rank-insensitive-lora-based-quantization-error-compensation-for-boo.md)**  
  実装：[✓](https://github.com/aiha-lab/RILQ) ・ リポジトリ内被引用：2  
  重み量子化（重み 量子化）は、FP16などで保持していた行列を低ビット表現へ写像してモデルの重み記憶量を削減する。LLaMA-3-8BのQuIP#量子化では常識推論5課題平均が52.48%→60.61%、WikiText-2の困惑度（perplexity; PPL）が12.74→9.39となった。

- **2025-11 · [Layer-Wise High-Impact Parameter Ratio Optimization in Post-Training Quantization for Large Language Models](2025-2511.17801-layer-wise-high-impact-parameter-ratio-optimization-in-post-training-qua.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  本研究は、大規模言語モデルを2〜3ビット程度の重み精度に縮小するとき、少数の高感度な重みが量子化誤差を増幅する問題を扱う。

- **2025-09 · [LUQ: Layerwise Ultra-Low Bit Quantization for Multimodal Large Language Models](2025-2509.23729-luq-layerwise-ultra-low-bit-quantization-for-multimodal-large-language-m.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LUQ（Layerwise Ultra-Low Bit Quantization）は、視覚言語モデル（VLM/MLLM）の各Transformer層が低ビット量子化に耐える度合いは一様でないことに着目し、層の出力活性entropyが低い順に1bit系量子化へ切り替える方式である。

- **2025-07 · [Squeeze10-LLM: Squeezing LLMs’ Weights by 10 Times via a Staged Mixed-Precision Quantization Method](2025-2507.18073-squeeze10-llm-squeezing-llms-weights-by-10-times-via-a-staged-mixed-prec.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  しかし均一に1～2bitへ量子化すると、外れ値や重要なチャネルの情報が失われ、出力活性が層を通るたびにずれていく。Squeeze10-LLMは、すべての重みをいきなり1bitにせず、まず4bitへ変換してから重要度を測定し、80%を1bit、残り20%を4bitで保存する段階的な重み専用post-学習 量子化（PTQ）を提案する。

- **2025-06 · [ROSAQ: Rotation-based Saliency-Aware Weight Quantization for Efficiently Compressing Large Language Models](2025-2506.13472-rosaq-rotation-based-saliency-aware-weight-quantization-for-efficiently-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ROSAQ（Rotation-based Saliency-Aware 重み 量子化）は、言語モデルの重みを3〜4bitへ圧縮するときに、すべての重みを一律に低精度化するのではなく、校正活性の主成分方向に沿った重要チャネルだけをFP16で保持する事後量子化方式である。

- **2025-06 · [BAQ: Efficient Bit Allocation Quantization for Large Language Models](2025-2506.05664-baq-efficient-bit-allocation-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/CSU-ModelCompression/BAQ) ・ リポジトリ内被引用：1  
  BAQ（Bit Allocation Quantization）は、大規模言語モデルの事後量子化で各列に同じビット数を割り当てることの非効率を、逆ヘッセ行列に基づく感度係数から計算した列別ビット幅で改善する手法である。

- **2025-05 · [QStore: Quantization-Aware Compressed Model Storage](2025-2505.04081-qstore-quantization-aware-compressed-model-storage.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低精度モデルと復元用の条件付き情報だけを保持する無損失の統合保管形式で、量子化関数と量子化後の値による二重のグループ化で条件付き情報を圧縮し、六つのモデルで保管量を最大で無圧縮の二・二分の一、読み込みを最大で一・八倍速くしたと報告した。

- **2025-05 · [Optimal Formats for Weight Quantisation](2025-2505.12988-optimal-formats-for-weight-quantisation.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  低ビット重み量子化では、整数、浮動小数点、非一様コードブック、ブロック単位のスケーリング、外れ値の高精度保持など、数値表現の選択肢が多数ある。

- **2025-05 · [LCD: Advancing Extreme Low-Bit Clustering for Large Language Models via Knowledge Distillation](2025-2506.12038-lcd-advancing-extreme-low-bit-clustering-for-large-language-models-via-k.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LCDは密度に基づく重み代表値の初期化、ヘッセ対角近似による代表値更新、段階的・投機的な代表値数削減、層別活性平滑化を組み合わせる極低ビット量子化方式。A100上の報告速度改善はBERT-large最大6.2倍、LLaMA-2-7Bは4.7倍。

- **2025-04 · [Enhancing Ultra-Low-Bit Quantization of Large Language Models Through Saliency-Aware Partial Retraining](2025-2504.13932-enhancing-ultra-low-bit-quantization-of-large-language-models-through-sa.md)**  
  実装：[✓](https://github.com/TokuyuSou/ULB-SAPR) ・ リポジトリ内被引用：1  
  CaoとArefは、事前学習済み大規模言語モデルの重みを2ビットへ圧縮するとき、既存のApiQが残す精度劣化を、小規模な部分再学習だけで軽減する手法を提案した。LLaMA-2-7Bのゼロショット常識推論5課題平均は、全精度64.85%、ApiQ 55.91%に対して、提案法の最良設定で56.88%となる。

- **2025-03 · [Universality of Layer-Level Entropy-Weighted Quantization Beyond Model Architecture and Size](2025-2503.04704-universality-of-layer-level-entropy-weighted-quantization-beyond-model-a.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LLMを一律4bitに量子化すると、容量は大幅に減るが、精度に敏感な層も同じビット幅へ押し込まれる。原著は1.6B〜70B級の複数モデルを対象に、MMLUで元モデルから概ね0.5%以内の精度差を目標とし、最大18%のメモリ削減を報告する。

- **2025-03 · [QUAD: Quantization and Parameter-Efficient Tuning of LLM with Activation Decomposition](2025-2503.19353-quad-quantization-and-parameter-efficient-tuning-of-llm-with-activation-.md)**  
  実装：[✓](https://github.com/hyx1999/Quad) ・ リポジトリ内被引用：1  
  重みと活性をともに4bitへ量子化する方式は、GPUの低精度行列積を利用できる可能性がある。

- **2025-03 · [ClusComp: A Simple Paradigm for Model Compression and Efficient Finetuning](2025-2503.13089-cluscomp-a-simple-paradigm-for-model-compression-and-efficient-finetunin.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ClusCompは、言語モデルの重みを一様な低ビット数値へ丸める代わりに、似た値の短いベクトルをまとめて代表ベクトルへ置き換える圧縮法である。

- **2025-01 · [DiscQuant: A Quantization Method for Neural Networks Inspired by Discrepancy Theory](2025-2501.06417-discquant-a-quantization-method-for-neural-networks-inspired-by-discrepa.md)**  
  実装：[✓](https://github.com/jerry-chee/DiscQuant) ・ リポジトリ内被引用：1  
  DiscQuantは、事前学習済みLLMの重みを低ビット化する際、量子化格子を設計した後の「各重みを上側と下側のどちらへ丸めるか」という問題を解く。原著の代表例では、Phi-3-mini-4k-instructを平均3.25ビットで量子化したGSM8kの正答率が、DiscQuant64%、GPTQ54%、RTN31%、無量子化84%である。

- **2025-11 · [R2Q: Towards Robust 2-Bit Large Language Models via Residual Refinement Quantization](2025-2511.21736-r2q-towards-robust-2-bit-large-language-models-via-residual-refinement-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  R2Q（Residual Refinement Quantization）は、2ビットの重み量子化を1回の4値への丸めではなく、元重みを二値近似した後、その残差をさらに二値近似する2段階へ分解する方式である。2ビットで品質を完全に保てる方式ではなく、比較対象の崩壊が極端な条件で改善幅が大きく見える点を区別する必要がある。

- **2025-11 · [FermiGrad-SVD: An LLM Compression Pipeline with Global Rank Selection and Gauge Fixing](2025-2512.03062-fermigrad-svd-an-llm-compression-pipeline-with-global-rank-selection-and.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  特異値切断をフェルミゲートで連続化し全層ランクを一括最適化するFermiGradと、因子の超過を無損失に消すゲージ固定PivGaによるSVD圧縮。感度方式より良い配分を70B規模まで示す。

- **2025-11 · [Beyond Dynamic Quantization: An Efficient Static Hierarchical Mix-precision Framework for Near-Lossless LLM Compression](2025-84553b047243-beyond-dynamic-quantization-an-efficient-static-hierarchical-mix-precisi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの推論で重みと活性を低ビット化すると、転送するデータ量と行列積の計算負荷を減らせる。ただし少数の極端に大きな値（外れ値）に量子化範囲を合わせると、多数の通常値に割り当てられる表現段階が粗くなり、生成品質が損なわれる。主要な評価条件は、重みの80%を4ビット、20%を8ビット、活性を8ビットとするW4.8A8である。

- **2025-11 · [Adaptive Layer-Wise Transformations for Post-Training Quantization of Large Language Models](2025-2511.17809-adaptive-layer-wise-transformations-for-post-training-quantization-of-la.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの事後量子化（post-学習 量子化、PTQ）では、重みと活性値を低ビット整数へ丸める際、少数の外れ値に量子化範囲が引きずられて通常値の分解能が不足する。

- **2025-10 · [To Compress or Not? Pushing the Frontier of Lossless GenAI Model Weights Compression with Exponent Concentration](2025-2510.02676-to-compress-or-not-pushing-the-frontier-of-lossless-genai-model-weights-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FP8形式は、行列積を低精度で直接計算できるため、LLM推論時の重みメモリと演算費用を抑えられる。ECF8（Exponent-Concentrated FP8）は、この偏りを利用してFP8重みの値そのものは一切変えずに、保存時のビット数を減らす方式である。報告されたメモリ削減率は9.8〜26.9%、固定メモリ予算での処理率改善は11.3〜177.1%である。

- **2025-10 · [SQS: Bayesian DNN Compression through Sparse Quantized Sub-distributions](2025-2510.08999-sqs-bayesian-dnn-compression-through-sparse-quantized-sub-distributions.md)**  
  実装：[✓](https://nan-jiang-group.github.io/SQS/) ・ リポジトリ内被引用：0  
  スパイク・アンド・スラブ型の変分分布で枝刈りと量子化を同時に学習し、別々に圧縮するより高い圧縮率を同程度の性能低下で得るベイズ型の統合圧縮方式。

- **2025-10 · [Neural Weight Compression for Language Models](2025-2510.11234-neural-weight-compression-for-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Neural 重み Compression（NWC）は、LLMの重みを手作業で設計した一様量子化やHadamard回転だけで圧縮するのではなく、重み分布からencoderとdecoderを学習して圧縮する方式である。

- **2025-10 · [Energy-Efficient and Dequantization-Free Q-LLMs: A Spiking Neural Network Approach to Salient Value Mitigation](2025-2510.19498-energy-efficient-and-dequantization-free-q-llms-a-spiking-neural-network.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  顕著な活性値をTTFSスパイクで混合精度のまま扱い、スケールを発火しきい値へ埋め込んで逆量子化を消す量子化手法SpikeQuant。W4A4でほぼFP16の精度と最大78.5パーセントのエネルギー削減。

- **2025-10 · [ELUTQ: Optimizing Quantization Accuracy under LUT-Based Computation for Edge LLMs](2025-2510.19482-elutq-optimizing-quantization-accuracy-under-lut-based-computation-for-e.md)**  
  実装：[✓](https://github.com/Nkniexin/ELUTQ) ・ リポジトリ内被引用：0  
  ELUTQは、LLMの重みを2〜3bitへ圧縮するときの量子化誤差と、量子化後の重みをCPU/GPUで実行するときの復号・乗算費用を一緒に扱うシステムである。

- **2025-10 · [Beyond Uniform SVD: Dual-Level Optimization across Columns and Modules for LLM Compression](2025-2510.19385-beyond-uniform-svd-dual-level-optimization-across-columns-and-modules-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SVD圧縮で誤差の大きい列はそのまま保持し小さい列だけ低ランク化する列保持と、モジュール単位の圧縮率配分により、同じ圧縮率でパープレキシティと正解率を同時に改善する再学習不要の圧縮法。

- **2025-10 · [AMS-Quant: Adaptive Mantissa Sharing for Floating-Point Quantization](2025-2510.16045-ams-quant-adaptive-mantissa-sharing-for-floating-point-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  k個の重みで仮数の最下位ビットを共有して非整数ビット幅を実現する浮動小数点量子化。適応探索で共有ビットを決め、FP5.33でFP16同等の精度と最大2.77倍の高速化を得る。

- **2025-10 · [1+1>2: A Synergistic Sparse and Low-Rank Compression Method for Large Language Models](2025-2510.26446-1-1-2-a-synergistic-sparse-and-low-rank-compression-method-for-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを低ランク成分と疎成分へ分け、再構成誤差の単一目的で交互最適化する共同圧縮手法。単独手法の弱点を相殺し、50パーセント圧縮でも品質を保ち、低ランク部だけの微調整で回復もできる。

- **2025-09 · [SDQ-LLM: Sigma-Delta Quantization for 1-bit LLMs of any size](2025-2510.03275-sdq-llm-sigma-delta-quantization-for-1-bit-llms-of-any-size.md)**  
  実装：[✓](https://github.com/Dreamlittlecat/LLM-Quant-Factory) ・ リポジトリ内被引用：0  
  SDQ-LLMは、アナログ信号のA/D変換で用いられるSigma-Delta（ΣΔ）量子化をLLMの重みへ適用し、低ビットの離散値をオーバーサンプリングした長い表現として保持する事後量子化（PTQ）方式である。

- **2025-09 · [SBVR: Summation of BitVector Representation for Efficient LLM Quantization](2025-2509.18172-sbvr-summation-of-bitvector-representation-for-efficient-llm-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMの重みを4ビット程度へ圧縮する事後量子化では、表現可能な値を減らすことで重みの転送量を節約できる。ただしRTX 3090・バッチ1のTPOTはSBVR 10.24msに対しAWQ 8.61msで、速度の絶対首位ではない。

- **2025-09 · [MPPQ: Enhancing Post-Training Quantization for LLMs via Mixed Supervision, Proxy Rounding, and Pre-Searching](2025-39681c9463ae-mppq-enhancing-post-training-quantization-for-llms-via-mixed-supervision.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  混合指標の監督、低ランク代理行列による要素ごとの適応丸め、クリッピング係数の事前格子探索を組み合わせ、2〜4ビット級の学習後量子化でも分布のずれと丸め誤差を抑える枠組みMPPQ。

- **2025-09 · [Fair-GPTQ: Bias-Aware Quantization for Large Language Models](2025-2509.15206-fair-gptq-bias-aware-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/upunaprosk/fair-gptq) ・ リポジトリ内被引用：0  
  LLMの重みを16bitから4bitへ量子化すると、パラメータ格納容量とデータ転送量を大幅に減らせる。著者らの主評価では、Mistral-v0.3-7B-InstructのUnQover（曖昧な属性質問での回答評価）が通常GPTQの33.30%からFair-GPTQの58.89%へ改善した。

- **2025-09 · [Calibration and Transformation-Free Weight-Only LLMs Quantization via Dynamic Grouping](2025-2509.03054-calibration-and-transformation-free-weight-only-llms-quantization-via-dy.md)**  
  実装：[✓](https://github.com/johnnyzheng0636/MSBPTQ) ・ リポジトリ内被引用：0  
  二値量子化を多ビット化し、グループ内分散を最小化する分割で重み表現を決める、較正も変換も不要な重みのみ量子化。CPUだけで量子化でき、4ビットと6ビットで比較対象と競合する。

- **2025-08 · [SEPTQ: A Simple and Effective Post-Training Quantization Paradigm for Large Language Models](2025-2604.10091-septq-a-simple-and-effective-post-training-quantization-paradigm-for-lar.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SEPTQは、LLMの重み-only事後量子化（Post-学習 量子化; PTQ）を、(1) 重要重みの保存位置を静的・行列globalに決める、(2) 残りの重みを列ごとに量子化してHessian情報で誤差補償する、という2段階に整理した方式である。

- **2025-08 · [Rethinking 1-bit Optimization Leveraging Pre-trained Large Language Models](2025-2508.06974-rethinking-1-bit-optimization-leveraging-pre-trained-large-language-mode.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、事前学習済みの言語モデルをそのまま極端な低ビット形式へ変換すると知識が破壊される問題に対し、BinaryLLMという段階的な一ビット化方式を提案する。原著はSmolLM、LLaMA3、LLaMA2などで評価し、三十億パラメータ規模ではゼロショット七課題平均57.0%を得た。

- **2025-08 · [CALR: Corrective Adaptive Low-Rank Decomposition for Efficient Large Language Model Layer Compression](2025-2508.16680-calr-corrective-adaptive-low-rank-decomposition-for-efficient-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SVD圧縮で失われる機能残差を、並列の学習可能な低ランク補正モジュールに学習させるLLM圧縮手法CALRを提案し、安定したFFNだけを選ぶ対象選択とあわせて圧縮率と性能保持の釣り合いを改善した研究。

- **2025-07 · [Variable Layerwise Quantization: A Simple and Effective Approach to Quantize LLMs](2025-19bdead741ff-variable-layerwise-quantization-a-simple-and-effective-approach-to-quant.md)**  
  実装：[✓](https://github.com/RazvanDu/LayerwiseQuant) ・ リポジトリ内被引用：0  
  層の重要度を二つの単純な指標で測り、重要な層を高ビット、重要でない層を低ビットへ割り当てるメタ量子化で、基盤の量子化方式を問わず平均ビット数を下げながら精度を保つ方式。

- **2025-07 · [MGAA: Multi-Granular Adaptive Allocation fof Low-Rank Compression of LLMs](2025-2507.03294-mgaa-multi-granular-adaptive-allocation-fof-low-rank-compression-of-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MGAA（Multi-Granular 適応的 Allocation）は、LLMの重み行列を低ランク分解するときに、各行列へ同じ削減率を割り当てるのではなく、Transformerサブレイヤ間の重要度と同じサブレイヤ内の各行列が保持する情報量を別々に見積もる手法である。

- **2025-07 · [Assigning Distinct Roles to Quantized and Low-Rank Matrices Toward Optimal Weight Decomposition](2025-2506.02077-assigning-distinct-roles-to-quantized-and-low-rank-matrices-toward-optim.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CALDERAなどの方式はWを量子化行列Qと低ランク行列積LRの和、すなわちW ≈ Q + LRで近似し、Qの量子化とLRの更新を交互に行う。一方、同じ条件のARC-Easy正答率は66.35%から65.49%へ下がり、すべての下流タスクを改善するわけではない。

- **2025-06 · [UltraSketchLLM: Sub-1-Bit LLM Compression via Sketch and Hardware-Friendly Operators](2025-2506.17255-ultrasketchllm-sub-1-bit-llm-compression-via-sketch-and-hardware-friendl.md)**  
  実装：[✓](https://github.com/suenar/UltraSketchLLM) ・ リポジトリ内被引用：0  
  索引なしのスケッチで重み表現を共有し、1重み当たり0.5ビットまで圧縮する手法。過小評価型のスケッチ設計と行列演算への写像で、品質劣化と推論オーバーヘッドを同時に抑える。

- **2025-06 · [Principled SVD-based Delta Compression via Quantization Error Minimization](2025-2506.11087-principled-svd-based-delta-compression-via-quantization-error-minimizati.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PRINMIXは、同じ基盤LLMから多数の微調整済みモデルを提供する場面を想定し、各モデルに固有の差分重みΔWだけを圧縮する方式である。

- **2025-06 · [Boost Post-Training Quantization via Null Space Optimization for Large Language Models](2025-2506.11044-boost-post-training-quantization-via-null-space-optimization-for-large-l.md)**  
  実装：[✓](https://github.com/zjq0455/q2n) ・ リポジトリ内被引用：0  
  重みだけを量子化すると、浮動小数点重みWと量子化後重みWqの間に数値差が生じる。しかしLLMの実際の出力誤差は、重みの差そのものではなく、入力活性Xに作用した (W−Wq)X によって決まる。

- **2025-05 · [Grouped Sequency-arranged Rotation: Optimizing Rotation Transformation for Quantization for Free](2025-2505.03810-grouped-sequency-arranged-rotation-optimizing-rotation-transformation-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  アダマール行列の行を符号反転回数の順に並べ替えたウォルシュ行列を、量子化グループ単位のブロック対角回転として使う学習なしの方式で、二ビット重み量子化の困惑度を通常回転の二十点二九から十一・五九へ下げ、学習型方式に迫る水準とゼロショット平均精度四十二・四四パーセントを報告した。

- **2025-05 · [EntroLLM: Entropy Encoded Weight Compression for Efficient Large Language Model Inference on Edge Devices](2025-2505.02380-entrollm-entropy-encoded-weight-compression-for-efficient-large-language.md)**  
  実装：[✓](https://github.com/arnabsanyal/EntroLLM) ・ リポジトリ内被引用：0  
  テンソル単位の混合量子化で重み分布のエントロピーを下げ、ハフマン符号化で無損失に追加圧縮し、並列復号で遅延を抑えるエッジ向け圧縮手法。保存量とトークン生成遅延の両方を実機で改善した。

- **2025-04 · [Gradual Binary Search and Dimension Expansion: A general method for activation quantization in LLMs](2025-2504.13989-gradual-binary-search-and-dimension-expansion-a-general-method-for-activ.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの低ビット事後量子化では、活性値の外れ値が量子化範囲を占有し、3〜4ビットの小さい整数レンジに通常の値を十分に割り当てられない。Mistral 7B v0.1を重み・活性・KVとも3ビット化した実験では、QuaRot単独の6課題平均18.43%がGBS併用58.31%へ改善した。

- **2025-03 · [SplitQuantV2: Enhancing Low-Bit Quantization of LLMs Without GPUs](2025-2503.07657-splitquantv2-enhancing-low-bit-quantization-of-llms-without-gpus.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みをk平均法で三つの層へ等価分割して値域を狭め、基本的な線形量子化の分解能を上げるGPU不要の前処理で、Llama 3.2 1BのINT4正解率を11.76ポイント改善し浮動小数点モデルにほぼ並ばせる研究。

- **2025-03 · [RaanA: A Fast, Flexible, and Data-Efficient Post-Training Quantization Algorithm](2025-2504.03717-raana-a-fast-flexible-and-data-efficient-post-training-quantization-algo.md)**  
  実装：[✓](https://github.com/FFTYYY/RaanA) ・ リポジトリ内被引用：0  
  層の最終出力への感度からビット配分を整数計画で最適化し、アダマール変換で高速化したベクトル量子化で重みを圧縮する学習後量子化。較正は5件か合成文1件で足り、70Bでも約55分で量子化できる。

- **2025-03 · [Large Language Model Compression via the Nested Activation-Aware Decomposition](2025-2503.17101-large-language-model-compression-via-the-nested-activation-aware-decompo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活性考慮型の特異値分解に元の重みへの近似を担う第2段を入れ子に重ね、較正分布と異なる言語やタスクでも劣化しにくい低ランク圧縮。圧縮率30から50パーセントで平均13から18パーセントのパープレキシティ削減。

- **2025-02 · [PacQ: A SIMT Microarchitecture for Efficient Dataflow in Hyper-asymmetric GEMMs](2025-2502.18627-pacq-a-simt-microarchitecture-for-efficient-dataflow-in-hyper-asymmetric.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みを詰めたまま行列積まで処理する超非対称行列積のために、詰め方向とデータフローと専用乗算器を一体設計したハードウェア研究。レジスタアクセスとエネルギー遅延積を大きく減らした。

- **2025-01 · [SWSC: Shared Weight for Similar Channel in LLM](2025-2501.08631-swsc-shared-weight-for-similar-channel-in-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  似たチャネル同士で代表ベクトルを共有し、圧縮誤差を特異値分解の低ランク近似で補う圧縮手法。低ビット域でRTN量子化が崩壊する条件でもパープレキシティを保つ。

- **2025-01 · [RQT: Hierarchical Residual Quantization for Multi-Model Compression](2025-28f8da2934ce-rqt-hierarchical-residual-quantization-for-multi-model-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  似た微調整モデル同士で低ビット整数重みを木構造で共有し、根から葉への経路の和で重みを再構成する残差量子化木RQTにより、デルタの大きさに弱い従来のデルタ圧縮を避けながら16モデルを実効約2ビットへ圧縮する方式。

- **2025-01 · [Rethinking Post-Training Quantization: Introducing a Statistical Pre-Calibration Approach](2025-2501.09107-rethinking-post-training-quantization-introducing-a-statistical-pre-cali.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、LLMの学習後量子化（PTQ）において、校正用の入力文を使わずに重要な重みを識別し、低ビット量子化での品質低下を抑える事前校正（pre-calibration）を提案する。LLaMA-7B、4ビット系の実験では、量子化時間が57秒でAWQの838秒、SpQRの10,901秒より短い。

- **2025-01 · [FBQuant: FeedBack Quantization for Large Language Models](2025-2501.16385-fbquant-feedback-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FBQuantは、LLMの重みのみを3/4ビットへ量子化するときに生じる誤差を、LoRA型の低ランク副枝で補償する方式である。FBQuantは主枝の復元・行列積と副枝のup投影を一つのCUDAカーネルに融合し、追加レイテンシの約60%を削減する。

- **2025-01 · [CURing Large Models: Compression via CUR Decomposition](2025-2501.04211-curing-large-models-compression-via-cur-decomposition.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの重みを圧縮する場合、ニューロンや層を削除する構造化剪定はパラメータ数を減らせるが、ネットワーク構造と残差経路の整合性を変更する必要がある。原著はLlama3.1-8Bで10層をrank 256で分解し、8.03Bパラメータを7.32Bに削減する処理を129.45秒で実行した。

- **2024-12 · [Taming Sensitive Weights: Noise Perturbation Fine-tuning for Robust LLM Quantization](2024-2412.06858-taming-sensitive-weights-noise-perturbation-fine-tuning-for-robust-llm-q.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大規模言語モデルの低ビット重み量子化では、全重みを一律に丸めると少数の敏感な重みが出力品質を大きく悪化させる。RTX 4090でOPT-1.3Bの128トークン生成を測ると、FP16外れ値0.5%を保持したsqLLMの2.62秒に対し、外れ値を保持しないNPFT併用版は2.40秒であった。

- **2024-12 · [LSAQ: Layer-Specific Adaptive Quantization for Large Language Model Deployment](2024-2412.18135-lsaq-layer-specific-adaptive-quantization-for-large-language-model-deplo.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LSAQ（層-Specific 適応的 量子化）は、GPUの利用可能メモリが異なるエッジ端末へLLMを配備するため、層ごとに重みの量子化ビット幅を変える方式である。Llama-3-8Bの平均5bit条件では、既存の層別量子化LWQに対して6課題zero-shot平均67.59→69.10%、WikiText-2のPPL7.386→7.331と小幅に改善した。

- **2024-12 · [CPTQuant - A Novel Mixed Precision Post-Training Quantization Techniques for Large Language Models](2024-2412.03599-cptquant-a-novel-mixed-precision-post-training-quantization-techniques-f.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層の感度を相関・枝刈り・摂動の3方法で測り、16・8・4ビットを層ごとに割り当てる混合精度の学習後量子化。最大4倍圧縮でも精度低下をFP16より小さく抑える。

### 3年前（2023-12〜2024-11）

- **2024-03 · [QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs](2024-2404.00456-quarot-outlier-free-4-bit-inference-in-rotated-llms.md)**  
  実装：[✓](https://github.com/spcl/QuaRot) ・ リポジトリ内被引用：345  
  QuaRotは、大規模言語モデル（LLM）の4ビット推論を難しくする活性値の外れ値を、高精度の例外チャネルへ逃がすのではなく、モデルの関数を変えない直交回転（orthogonal rotation）で多数の次元へ分散する量子化手法である。

- **2024-02 · [QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks](2024-2402.04396-quip-even-better-llm-quantization-with-hadamard-incoherence-and-lattice-.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/quip-sharp) ・ リポジトリ内被引用：233  
  QuIP#は、学習済みの大規模言語モデルを再学習せずに2〜4ビット/重みへ圧縮する事後学習量子化（Post-学習 量子化、PTQ）である。試作推論実装はRTX 4090上で70Bの2ビット重みを32.74トークン/秒で生成し、実効メモリ帯域利用率56.84%を記録した（表5）。

- **2024-01 · [SliceGPT: Compress Large Language Models by Deleting Rows and Columns](2024-2401.15024-slicegpt-compress-large-language-models-by-deleting-rows-and-columns.md)**  
  実装：[✓](https://github.com/microsoft/TransformerCompression) ・ リポジトリ内被引用：169  
  SliceGPTは、学習済みTransformerの埋め込み次元を減らす学習後圧縮である。代表的なLLaMA-2 70Bの25%削減では、A100 40GBで1トークン生成時間が125ミリ秒から110ミリ秒へ、必要GPUが4台から3台へ減った。

- **2024-05 · [QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving](2024-2405.04532-qserve.md)**  
  実装：[✓](https://github.com/mit-han-lab/omniserve) ・ リポジトリ内被引用：154  
  QServeは、クラウド型の大規模言語モデル（LLM）サービングにおいて、重みを4ビットへ量子化してもGPU上の実行速度が期待ほど上がらない問題を、量子化アルゴリズムと推論カーネルの協調設計によって解く研究である。論文はこの量子化解除の費用が20〜90%に達する条件を示し、ビット数を減らすだけではサービング処理率を改善できないことを説明する。

- **2024-01 · [Extreme Compression of Large Language Models via Additive Quantization](2024-2401.06118-extreme-compression-of-large-language-models-via-additive-quantization.md)**  
  実装：[✓](https://github.com/Vahe1994/AQLM) ・ リポジトリ内被引用：140  
  加算量子化による言語モデル圧縮（AQLM）は、重みの極低ビット量子化における「小さいモデルを高精度で保持した方が、巨大モデルを2ビットにするより良い」という従来の精度対容量の関係を改善する研究である。Llama 2 7B・13B・70B、Mixtral 8×7B、Mistral 7Bを評価する。

- **2023-12 · [ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models](2023-2312.05821-asvd-activation-aware-singular-value-decomposition-for-compressing-large.md)**  
  実装：[✓](https://github.com/hahnyuan/ASVD4LLM) ・ リポジトリ内被引用：106  
  活性値認識型特異値分解（活性値-aware Singular Value Decomposition、ASVD）は、大規模言語モデル（LLM）の線形重みを追加学習なしで低ランク行列へ置き換える圧縮方式である。LLaMA-7BとLLaMA-2-7B/13Bで重み容量を10～30%削減する実験を行い、活性値を考慮しないSVDより大幅に良い困惑度を報告する。

- **2024-06 · [DuQuant: Distributing Outliers via Dual Transformation Makes Stronger Quantized LLMs](2024-2406.01721-duquant-distributing-outliers-via-dual-transformation-makes-stronger-quantized-llms.md)**  
  実装：[✓](https://github.com/Hsu1023/DuQuant) ・ リポジトリ内被引用：97  
  巨大外れ値を外れ値誘導のブロック回転とジグザグ置換で分散し、4ビット重み・活性量子化の精度を改善しつつ、LLaMA2-7Bでプリフィル最大2.08倍・復号時メモリ3.50倍削減を示す。

- **2024-02 · [The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](2024-2402.17764-the-era-of-1-bit-llms-all-large-language-models-are-in-1-58-bits.md)**  
  実装：✓ ・ リポジトリ内被引用：97  
  狙いは、学習済みFP16/BF16モデルを後から近似する事後学習量子化ではなく、モデル自体を極低bit表現へ適応させ、品質を維持したまま重み転送・行列積・メモリ容量の支配項を小さくすることにある。

- **2024-10 · [FlatQuant: Flatness Matters for LLM Quantization](2024-2410.09426-flatquant-flatness-matters-for-llm-quantization.md)**  
  実装：[✓](https://github.com/ruikangliu/FlatQuant) ・ リポジトリ内被引用：91  
  層ごとの学習可能アフィン変換を小さなクロネッカー積へ分解し量子化と融合して、LLaMA-3-70BのW4A4で精度低下1%未満とプリフィル最大2.3倍高速化を両立する。

- **2024-02 · [BiLLM: Pushing the Limit of Post-Training Quantization for LLMs](2024-2402.04291-billm-pushing-the-limit-of-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/BiLLM) ・ リポジトリ内被引用：78  
  ヘッセ感度で重要列を選び二値残差近似し、残りのベル形重み分布を最適分割して別々に二値化することで、再学習なしにLLM重みを約1.1ビットまで圧縮する。

- **2024-06 · [QTIP: Quantization with Trellises and Incoherence Processing](2024-2406.11235-qtip-quantization-with-trellises-and-incoherence-processing.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/qtip) ・ リポジトリ内被引用：70  
  ベクトル量子化（Vector Quantization, VQ）は複数重みをまとめて符号化するほど量子化効率が上がる一方、通常の符号帳は次元に対して指数的に巨大化する。QTIPは、符号帳を列挙せず有限状態の「トレリス」を使うことで、この次元の壁を外し、2bit級でも256次元の高次元量子化を実用的な復号コストで実現する。

- **2024-01 · [SliM-LLM: Salience-Driven Mixed-Precision Quantization for Large Language Models](2024-2405.14917-slim-llm-salience-driven-mixed-precision-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：61  
  要素単位で重要重みだけ高精度に残すのではなく、重要度が空間的にまとまる性質を使ってグループ単位で1/2/3ビットを割り当てる。さらに各グループ内部の少数の重要要素を量子化器校正で重く扱い、LLaMA-7Bの2ビット級でWikiText2パープレキシティ14.58を達成する。

- **2024-02 · [OneBit: Towards Extremely Low-bit Large Language Models](2024-2402.11295-onebit-towards-extremely-low-bit-large-language-models.md)**  
  実装：[✓](https://github.com/xuyuzhuang11/OneBit) ・ リポジトリ内被引用：59  
  OneBitは、学習済み大規模言語モデル（LLM）の重みを極端に低いビット数で保存する際に生じる精度劣化を、線形層の表現形式そのものを変更することで緩和する研究である。査読版の表3では、LLaMA-7Bの重み保存量が13.5 GBから1.3 GBへ、LLaMA-13Bでは26.0 GBから2.2 GBへ減る。

- **2024-02 · [GPTVQ: The Blessing of Dimensionality for LLM Quantization](2024-2402.15319-gptvq-the-blessing-of-dimensionality-for-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：58  
  複数の重みを1ベクトルとして量子化し、代理ヘッセ行列（proxy Hessian）で量子化誤差を後続列へ補償する。Llama 3 8Bの約3.125 bit/value構成では、Snapdragon X Elite上で独自INT4実装よりモデル占有量を約19%減らし、23.81から26.15 トークン/sへ高速化する。

- **2024-02 · [BitDistiller: Unleashing the Potential of Sub-4-Bit LLMs via Self-Distillation](2024-2402.10631-bitdistiller-unleashing-the-potential-of-sub-4-bit-llms-via-self-distill.md)**  
  実装：[✓](https://github.com/DD-DuDa/BitDistiller) ・ リポジトリ内被引用：44  
  学習後量子化（post-学習 量子化、PTQ）は比較的低費用だが、低ビットでは誤差を修正しにくい。

- **2024-07 · [Compact Language Models via Pruning and Knowledge Distillation](2024-2407.14679-compact-language-models-via-pruning-and-knowledge-distillation.md)**  
  実装：[✓](https://github.com/NVlabs/Minitron) ・ リポジトリ内被引用：43  
  15Bを学習した後に8B・4Bを別々にゼロから学習する代わりに、Nemotron-4 15Bから注意ヘッド、MLP中間次元、埋め込み幅、必要に応じて層を構造枝刈りし、元15Bのロジットを教師にして短期間だけ知識蒸留（Knowledge Distillation; KD）する。

- **2024-03 · [AffineQuant: Affine Transformation Quantization for Large Language Models](2024-2403.12544-affinequant-affine-transformation-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：43  
  スカラーの拡大縮小や平行移動に限られていた等価変換を、可逆な行列によるアフィン変換へ拡張する。変換を量子化前の重みへ掛け、逆変換を活性値側へ入れることで元の線形演算を保ったまま量子化しやすい座標系を学習し、LLaMA2-7BのW4A4でC4パープレキシティをOmniQuantの18.02から15.76へ改善する。

- **2024-05 · [PV-Tuning: Beyond Straight-Through Estimation for Extreme LLM Compression](2024-2405.14852-pv-tuning-beyond-straight-through-estimation-for-extreme-llm-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  大規模言語モデルを1～2ビット/重みへ圧縮すると、モデルを小さなメモリへ収められる一方、量子化誤差によって予測品質が大きく低下する。Llama-2 7Bの約2.02ビット/重みではWikiText-2のパープレキシティ5.84、5課題平均正答率61.35%を報告し、同程度のQuIP#の6.19・57.51%を上回る。

- **2024-01 · [LLM-FP4: 4-Bit Floating-Point Quantized Transformers](2023-2310.16836-llm-fp4-4-bit-floating-point-quantized-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  4ビット浮動小数点（floating point; FP）の指数部構成とクリップ範囲を層ごとに探索し、活性値の大きなチャネル間分散はチャネル別指数バイアスを重みへ事前吸収して処理する。LLaMA-13Bの埋め込み・重み・活性値を4/4/4ビットにして、6つの常識推論タスク平均63.1を維持する。

- **2024-03 · [IntactKV: Improving Large Language Model Quantization by Keeping Pivot Tokens Intact](2024-2403.01241-intactkv-improving-large-language-model-quantization-by-keeping-pivot-to.md)**  
  実装：[✓](https://github.com/ruikangliu/IntactKV) ・ リポジトリ内被引用：24  
  IntactKVは、低ビット量子化した大規模言語モデル（LLM）において、入力の最初に置かれる少数の支点トークン（pivot トークン）の鍵・値キャッシュ（KV キャッシュ）だけを高精度モデルから生成して保存する方式である。

- **2023-12 · [CBQ: Cross-Block Quantization for Large Language Models](2023-2312.07950-cbq-cross-block-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  学習後量子化（Post-学習 量子化、PTQ）は、学習済み大規模言語モデルの重みや活性を少ないビット数で表現し、メモリ使用量や演算費用を下げる技術である。65Bの4ビット重み量子化を単一GPUで4.3時間で行ったという処理費用の報告はあるが、量子化後の推論速度を4.3倍にしたという意味ではない。

- **2024-02 · [DB-LLM: Accurate Dual-Binarization for Efficient LLMs](2024-2402.11960-db-llm-accurate-dual-binarization-for-efficient-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  大規模言語モデルの重み量子化は、16ビット浮動小数点の重みを数ビットの離散値へ置き換え、モデル保存量と重み読み出し量を減らす。LLaMA-1-7Bでは平均重み疎性が62.8%となり、著者らの計算量モデルでは32トークン入力のFLOPsが通常2ビット量子化の37.3Gから29.8Gへ減る。

- **2024-02 · [LQER: Low-Rank Quantization Error Reconstruction for LLMs](2024-2402.02446-lqer-low-rank-quantization-error-reconstruction-for-llms.md)**  
  実装：[✓](https://github.com/ChengZhang-98/lqer) ・ リポジトリ内被引用：18  
  大規模言語モデルの重みを4ビットへ圧縮しても、実行時に半精度へ逆量子化してから行列積を計算するなら、重みの保存容量削減がそのまま演算器の省資源化につながるとは限らない。

- **2024-10 · [AlphaPruning: Using Heavy-Tailed Self Regularization Theory for Improved Layer-wise Pruning of Large Language Models](2024-2410.10912-alphapruning-using-heavy-tailed-self-regularization-theory-for-improved-.md)**  
  実装：[✓](https://github.com/haiquanlu/AlphaPruning) ・ リポジトリ内被引用：17  
  重み行列の固有値分布の裾の重さで層の学習度を測り、よく学んだ層ほど少なく刈る層別疎率の配分法で、疎率80%のLLaMA-7Bで従来の層別配分より困惑度を304.31下げ、CPU推論3.06倍を実測した。

- **2024-03 · [Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2024-8166d1af62df-exploring-post-training-quantization-in-llms-from-comprehensive-study-to.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  この論文は、大規模言語モデル（Large Language モデル; LLM）の学習後量子化（Post-学習 量子化; PTQ）について、「何ビットにするか」だけでなく、重みと活性化のどちらを量子化するか、どの範囲で尺度を共有するか、誤差をどの方法で補正するか、モデル系列と規模によって結果がどう変わるかを分離して調べる。

- **2024-02 · [Accurate LoRA-Finetuning Quantization of LLMs via Information Retention](2024-2402.05445-accurate-lora-finetuning-quantization-of-llms-via-information-retention.md)**  
  実装：[✓](https://github.com/AI-Efficiency/IR-QLoRA) ・ リポジトリ内被引用：11  
  大規模言語モデルの重みを16ビットから4ビット以下へ縮めると、重みの保存量と推論時に必要な重み転送量を減らせる。量子化後の基盤重みを固定し、小さな低ランク適応行列だけを微調整するQLoRA系の方法でも、失われた情報を十分に取り戻せない場合がある。

- **2024-11 · [ZipNN: Lossless Compression for AI Models](2024-2411.05239-zipnn-lossless-compression-for-ai-models.md)**  
  実装：[✓](https://github.com/zipnn/zipnn) ・ リポジトリ内被引用：10  
  ZipNNは、モデルの重みを変更せずに保存・転送時のバイト数を減らし、展開すると元の重みビット列を完全に復元する可逆圧縮（無損失 compression）である。論文表IIIのLlama 3.1（BF16）では、Zstd単体の圧縮後サイズが原寸の77.7%なのに対してZipNNは66.4%。

- **2024-10 · [Quamba: A Post-Training Quantization Recipe for Selective State Space Models](2024-2410.13229-quamba-a-post-training-quantization-recipe-for-selective-state-space-mod.md)**  
  実装：[✓](https://github.com/enyac-group/Quamba) ・ リポジトリ内被引用：10  
  Mambaのような選択的状態空間モデル（SSM）は、注意機構のKVキャッシュを保持せず、固定サイズの再帰状態で長い系列を処理できる。2.8BのMambaではOrin Nano 8GBで生成1トークン当たりの遅延が103.56msから60.17msに減り、6種zero-shot平均精度は63.1%から62.2%へ低下した。

- **2024-05 · [I-LLM: Efficient Integer-Only Inference for Fully-Quantized Low-Bit Large Language Models](2024-2405.17849-i-llm-efficient-integer-only-inference-for-fully-quantized-low-bit-large.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  I-LLMは、LLMの重みと活性値を低ビットへ量子化するだけでなく、注意機構のSoftmax、ゲート付き活性化のSwiGLU、RMSNormなどの非線形演算も整数演算へ置き換える学習後量子化（PTQ）方式である。

- **2024-04 · [Mitigating the Impact of Outlier Channels for Language Model Quantization with Activation Regularization](2024-2404.03605-mitigating-the-impact-of-outlier-channels-for-language-model-quantizatio.md)**  
  実装：[✓](https://github.com/aninrusimha/qat-pretrain) ・ リポジトリ内被引用：9  
  本研究は、言語モデルの重みと活性値の両方を4ビット整数にするW4A4量子化を、事前学習の段階から成立させる方法を調べる。300Mモデルを後からQAT微調整した試験では、基準に対しパープレキシティが16%悪化したという負の結果が重要である。

- **2024-06 · [BoA: Attention-aware Post-training Quantization without Backpropagation](2024-2406.13474-boa-attention-aware-post-training-quantization-without-backpropagation.md)**  
  実装：[✓](https://github.com/SamsungLabs/BoA) ・ リポジトリ内被引用：8  
  BoA（Backpropagation-free optimization for 注意機構-aware PTQ）は、大規模言語モデルの学習後量子化（post-学習 量子化、PTQ）で、重みの整数化に伴う性能低下を抑える手法である。

- **2024-05 · [Post Training Quantization of Large Language Models with Microscaling Formats](2024-2405.07135-post-training-quantization-of-large-language-models-with-microscaling-fo.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  本論文は、大規模言語モデル（LLM）の事後量子化（post-学習 量子化, PTQ）で広く使われるSmoothQuant、活性認識重み量子化（AWQ）、勾配不要の重み誤差補償（GPTQ）を、ブロックごとに尺度を共有する微小尺度（microscaling, MX）形式へ拡張し、三方式の組合せと適用順序を体系的に評価した研究である。

- **2024-02 · [SparseLLM: Towards Global Pruning for Pre-trained Language Models](2024-2402.17946-sparsellm-towards-global-pruning-for-pre-trained-language-models.md)**  
  実装：[✓](https://github.com/BaiTheBest/SparseLLM) ・ リポジトリ内被引用：7  
  大規模言語モデルの重みを間引く非構造化枝刈りは、モデルの保存容量と演算の理論上の非ゼロ要素数を減らせる。原著のOPT-1.3B、WikiText2、重みの80%を疎化した条件では、SparseGPTの困惑度69.67に対しSparseLLMは58.92である。

- **2023-12 · [ZeroQuant(4+2): Redefining LLMs Quantization with a New FP6-Centric Strategy for Diverse Generative Tasks](2023-2312.08583-zeroquant-4-2-redefining-llms-quantization-with-a-new-fp6-centric-strate.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  4ビット整数量子化（INT4）が自由生成課題で不安定になる条件を測り、6ビット浮動小数点（FP6）の品質を、4+2ビットの格納・復号方式と指数バイアスの事前変換によって既存GPU上で利用する研究。

- **2024-10 · [BitStack: Any-Size Compression of Large Language Models in Variable Memory Environments](2024-2410.23918-bitstack-any-size-compression-of-large-language-models-in-variable-memor.md)**  
  実装：[✓](https://github.com/xinghaow99/BitStack) ・ リポジトリ内被引用：6  
  BitStackは、LLMの重みを固定の2bit、3bit、4bitなどへ一度だけ量子化する代わりに、複数の小さな残差ブロックへ分解して優先順位を付け、使えるメモリ量に応じて必要なブロックだけを読み込む学習不要の圧縮方式である。

- **2024-04 · [Cherry on Top: Parameter Heterogeneity and Quantization in Large Language Models](2024-2404.02837-cherry-on-top-parameter-heterogeneity-and-quantization-in-large-language.md)**  
  実装：[✓](https://github.com/wangitu/CherryQ) ・ リポジトリ内被引用：6  
  大規模言語モデル（LLM）の重みを一律に低ビットへ量子化すると、保存容量を減らせる反面、ごく少数の重要な重みに発生した誤差が出力品質を大きく損なう。

- **2024-01 · [Fast and Effective Weight Update for Pruned Large Language Models](2024-2401.02938-fast-and-effective-weight-update-for-pruned-large-language-models.md)**  
  実装：[✓](https://github.com/fmfi-compbio/admm-pruning) ・ リポジトリ内被引用：6  
  大規模言語モデルの重みを事後的に枝刈りする際には、重要度の低い重みをゼロにするだけでは、各層の出力が元モデルからずれてしまう。LLaMA-7Bの60%疎性ではWikiText2困惑度がSparseGPTの10.51に対して提案方式の9.22へ改善する。

- **2024-10 · [TesseraQ: Ultra Low-Bit LLM Post-Training Quantization with Block Reconstruction](2024-2410.19103-tesseraq-ultra-low-bit-llm-post-training-quantization-with-block-reconst.md)**  
  実装：[✓](https://github.com/Intelligent-Computing-Lab-Yale/TesseraQ) ・ リポジトリ内被引用：5  
  大規模言語モデルを2〜4bitに事後量子化すると、重みの容量を大幅に減らせるが、2bit付近では量子化誤差が大きくなり、困惑度や下流タスク精度が崩れやすい。Table 2では5つの常識推論タスクの平均正答率が50.52%から59.27%へ上がる。

- **2024-06 · [LLMEasyQuant: Scalable Quantization for Parallel and Distributed LLM Inference](2024-2406.19657-llmeasyquant-scalable-quantization-for-parallel-and-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/NoakLiu/LLMEasyQuant) ・ リポジトリ内被引用：5  
  LLMEasyQuantは、大規模言語モデル（LLM）の学習後量子化を研究・実行するための統合基盤である。論文は、量子化方式の品質だけを比較しても、実行時のメモリ転送や通信、逆量子化が遅ければ推論の速度向上につながらないと考える。

- **2024-06 · [Layer-Wise Quantization: A Pragmatic and Effective Method for Quantizing LLMs Beyond Integer Bit-Levels](2024-2406.17415-layer-wise-quantization-a-pragmatic-and-effective-method-for-quantizing-.md)**  
  実装：[✓](https://github.com/RazvanDu/LayerwiseQuant/) ・ リポジトリ内被引用：4  
  層の重要度を二つの物差しで順位付けし、重要な層を高ビット、重要でない層を低ビットに割り当てることで、平均三ビット前後まで性能の九割前後を保ちながらメモリ予算へ細かく合わせられるようにした。

- **2024-10 · [SeedLM: Compressing LLM Weights into Seeds of Pseudo-Random Generators](2024-2410.10714-seedlm-compressing-llm-weights-into-seeds-of-pseudo-random-generators.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  大規模言語モデルの自己回帰生成では、1トークンを生成するたびに大量の重みを読み出す必要があり、演算器の理論性能よりもDRAM帯域が制約になる場合がある。通常の低ビット量子化は、FP16などの重みを整数値へ写像して読み出し量を減らす。速度については、専用FPGA上の行列ベクトル積でFP16基準比3.67〜3.98倍のサイクル数削減を報告する。

- **2024-05 · [ReALLM: A general framework for LLM compression and fine-tuning](2024-2405.13155-reallm-a-general-framework-for-llm-compression-and-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  元の行列を16ビットで保存する代わりに、学習済みの小型デコーダ、量子化した埋め込み、コードブック、必要な逆置換、低ランク行列とスケールを保存する。

- **2024-02 · [Towards Next-Level Post-Training Quantization of Hyper-Scale Transformers](2024-2402.08958-towards-next-level-post-training-quantization-of-hyper-scale-transformer.md)**  
  実装：[✓](https://github.com/SamsungLabs/aespa) ・ リポジトリ内被引用：3  
  量子化は層ごとに実行しながら誤差の物差しを注意全体の再構成に置き、目的関数を事前計算可能な形へ変形することで、二ビットでも崩壊せず、ブロック型より桁違いに速い学習後量子化を実現した。

- **2024-02 · [FlattenQuant: Breaking Through the Inference Compute-bound for Large Language Models with Per-tensor Quantization](2024-2402.17985-flattenquant-breaking-through-the-inference-compute-bound-for-large-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  FlattenQuantは、大規模言語モデル（LLM）の推論で、重みだけを低ビット化しても行列演算が半精度のまま残るという問題を解く後学習量子化（post-学習 量子化; PTQ）方式である。難点は、LLMの活性値に他のチャネルより20〜100倍程度大きい外れ値チャネルが存在することだ。

- **2023-12 · [DSFormer: Effective Compression of Text-Transformers by Dense-Sparse Weight Factorization](2023-2312.13211-dsformer-effective-compression-of-text-transformers-by-dense-sparse-weig.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  DSFormerは、事前学習済みTransformerの大きな線形変換行列を、密な基底行列と半構造化された疎な係数行列の積に置き換える圧縮手法である。原著Table 1のGLUE開発セットでは、BERT-baseの8タスク単純平均82.05に対して、DSFormerの2倍圧縮が83.13、2.8倍圧縮が81.85、3.57倍圧縮が79.80である。

- **2024-11 · [Zeroth-Order Adaptive Neuron Alignment Based Pruning without Re-Training](2024-2411.07066-zeroth-order-adaptive-neuron-alignment-based-pruning-without-re-training.md)**  
  実装：[✓](https://github.com/eliacunegatti/NeuroAL) ・ リポジトリ内被引用：1  
  既存の枝刈り手法の上に乗り、ブロック単位と行単位の疎率の配分をニューロンの整列度で自動的に決め直すことで、再学習なしに高疎率でも性能と実行時間の釣り合いを改善するNeuroAl。

- **2024-11 · [ATQ: Activation Transformation for Weight-Activation Quantization of Large Language Models](2024-ebb210d8b588-atq-activation-transformation-for-weight-activation-quantization-of-larg.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  三角不等式で誤差を重み側と活性値側へ分け、チャネルごとの移動と拡大で外れ値を通常範囲へ寄せた活性値と、GPTQ型補償で量子化した変換後重みを組み合わせ、W8A8でほぼ無損失の精度を狙う学習後量子化。

- **2024-10 · [ESPACE: Dimensionality Reduction of Activations for Model Compression](2024-2410.05437-espace-dimensionality-reduction-of-activations-for-model-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ESPACEはこの順序を逆転させ、入力活性化を較正済みの低次元空間へ射影してから元の重みで学習し、推論時だけ結合則で圧縮重みへ置き換える。GPT3、Llama2、Nemotron4の複数モデルで、20〜55%程度の圧縮に対するPPL、下流精度、GEMMレイテンシ、プリフィル TTFTを評価する。

- **2024-07 · [Compensate Quantization Errors+: Quantized Models Are Inquisitive Learners](2024-2407.15508-compensate-quantization-errors-quantized-models-are-inquisitive-learners.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Compensate Quantization Errors+（CQE+）は、学習済み大規模言語モデルの重みを2〜4ビットへ量子化する際、量子化の整数格子に適した重み分布へ調整する方法を提案する。

- **2024-06 · [Rethinking Pruning Large Language Models: Benefits and Pitfalls of Reconstruction Error Minimization](2024-2406.15524-rethinking-pruning-large-language-models-benefits-and-pitfalls-of-recons.md)**  
  実装：[✓](https://github.com/LOG-postech/rethinking-LLM-pruning) ・ リポジトリ内被引用：1  
  枝刈りの再構成誤差をブロック単位化と大域伝播とブロック間再構成で9割前後削減できる一方、誤差最小化の推し進めは小さい校正データへの過適合を招いて汎化を損なうことを示し、自己生成校正データによる緩和を提示した分析研究。

- **2024-06 · [Compensate Quantization Errors: Make Weights Hierarchical to Compensate Each Other](2024-2406.16299-compensate-quantization-errors-make-weights-hierarchical-to-compensate-e.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  事後量子化は、既存の言語モデルの重みや活性を低ビット整数で近似し、メモリ占有量とデータ転送量を削減する。著者は実際のGPUサービング速度を新たに測定していないため、精度改善と高速化を混同しない。

- **2024-05 · [Dependency-Aware Semi-Structured Sparsity of GLU Variants in Large Language Models](2024-2405.01943-dependency-aware-semi-structured-sparsity-of-glu-variants-in-large-langu.md)**  
  実装：[✓](https://github.com/guozhiyu/glu_dass) ・ リポジトリ内被引用：1  
  LLaMA2やMistralのMLPでは、入力をGate投影とUp投影に通し、活性化関数と要素積によって中間表現を作り、Down投影で元の隠れ次元へ戻す。通常の重み単位剪定は各線形層の入力活性と重みの大きさを見て独立にゼロ化するため、ある中間ニューロンのDown側の寄与を重視しても、その中間値を作るGate/Up側の重みが多く削られる可能性がある。

- **2024-05 · [AdpQ: A Zero-shot Calibration Free Adaptive Post Training Quantization Method for LLMs](2024-2405.13358-adpq-a-zero-shot-calibration-free-adaptive-post-training-quantization-me.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  適応型LASSOのソフトしきい値化で重みだけから外れ値を分離し、較正データなしで完全な低ビット量子化を行う学習後量子化手法。量子化時間は既存手法の10倍以上速い。

- **2024-02 · [RepQuant: Towards Accurate Post-Training Quantization of Large Transformer Models via Scale Reparameterization](2024-2402.05628-repquant-towards-accurate-post-training-quantization-of-large-transforme.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  これらへ単一の量子化尺度や単純な2進対数量子化を直接適用すると、4ビット付近では重要な情報が失われやすい。

- **2024-10 · [Error Diffusion: Post Training Quantization with Block-Scaled Number Formats for Neural Networks](2024-2410.11203-error-diffusion-post-training-quantization-with-block-scaled-number-form.md)**  
  実装：[✓](https://github.com/ROCm/tensorcast) ・ リポジトリ内被引用：0  
  ブロックスケール数値形式に対応する学習後量子化手法EDを提案し、活性値の変化を伝播させながら量子化誤差を全層へ拡散させる較正と、形式エミュレーション用ライブラリTensorCastを与えた研究。

- **2024-10 · [DeltaDQ: Ultra-High Delta Compression for Fine-Tuned LLMs via Group-wise Dropout and Separate Quantization](2024-2410.08666-deltadq-ultra-high-delta-compression-for-fine-tuned-llms-via-group-wise-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  デルタ重みの中間積が均衡する性質を使い、グループ単位ドロップアウトで疎化し値域別に分離量子化することで、微調整モデルの差分を最大512倍まで圧縮する方式。

- **2024-09 · [Hyper-Compression: Model Compression via Hyperfunction](2024-2409.00592-hyper-compression-model-compression-via-hyperfunction.md)**  
  実装：[✓](https://github.com/Juntongkuki/Hyper-Compression) ・ リポジトリ内被引用：0  
  学習済み大規模言語モデルの重み容量を小さくする一般的な方法は、低ビット量子化、枝刈り、低ランク分解である。LLaMA2-7Bでは原著Table 5で保存容量12.50GB→4.80GB（2.60倍圧縮）、8課題の平均正答率65.88%→64.89%（0.99ポイント低下）を報告する。

- **2024-09 · [Foundations of Large Language Model Compression - Part 1: Weight Quantization](2024-2409.02026-foundations-of-large-language-model-compression-part-1-weight-quantizati.md)**  
  実装：[✓](https://github.com/seannz/cvxq) ・ リポジトリ内被引用：0  
  重み量子化を凸最適化として定式化し、勾配と重みの分散から最適なビット配分を導く理論と手法CVXQを提示した研究。低ビット域、とくに2ビット台で既存の学習後量子化を上回る。

- **2024-09 · [Accumulator-Aware Post-Training Quantization for Large Language Models](2024-2409.17092-accumulator-aware-post-training-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  この論文が対象とするのは、量子化後の重み・活性化値を掛け合わせる演算ではなく、その積を多数足し込む累積器（accumulator）のビット幅である。

- **2024-08 · [LLM-Barber: Block-Aware Rebuilder for Sparsity Mask in One-Shot for Large Language Models](2024-2408.10631-llm-barber-block-aware-rebuilder-for-sparsity-mask-in-one-shot-for-large.md)**  
  実装：[✓](https://github.com/YupengSu/LLM-Barber) ・ リポジトリ内被引用：0  
  枝刈り後のモデルで重みの重要度が変わることに着目し、ブロック単位の再構成誤差の勾配と重みの積でマスクを作り直して、重要になった重みを復活させ不要になった重みを落とす、再学習なしの一括マスク再構築。

- **2024-05 · [On the Way to Lossless Compression of Language Transformers: Exploring Cross-Domain Properties of Quantization](2024-ce454f0d0a1b-on-the-way-to-lossless-compression-of-language-transformers-exploring-cr.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  微調整データなしで、層ごとの量子化感度をロジットの距離で測ってパレートフロンティアで層を選び、事前学習コーパスで較正することで、言語トランスフォーマーの95%以上を8ビット整数化しても正解率の低下を0.02%以内に抑える学習後量子化の研究。

- **2024-05 · [Athena: Efficient Block-Wise Post-Training Quantization for Large Language Models Using Second-Order Matrix Derivative Information](2024-2405.17470-athena-efficient-block-wise-post-training-quantization-for-large-languag.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  損失の曲率を表すヘッセ行列で量子化誤差の重要度を測り、ブロック単位に反復量子化しながら残りの重みを更新する学習後量子化。コードブック表現で、比較方式が4ビットを要する精度をより少ないビットで狙う。

- **2024-04 · [From a Lossless (~1.5:1) Compression Algorithm for Llama2 7B Weights to Variable Precision, Variable Range, Compressed Numeric Data Types for CNNs and LLMs](2024-2404.10896-from-a-lossless-1-5-1-compression-algorithm-for-llama2-7b-weights-to-var.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Llama2 7Bの重みの指数分布の偏りを利用し、重みをコードと追加データへ分けてコードだけをANSでエントロピー符号化することで、値を変えずに重みを約66%へ圧縮し、約200 LUTのFPGA展開器で毎クロック1要素を供給できる無損失重み圧縮と、そのカスタム数値型への一般化。

### 4年前（2022-12〜2023-11）

- **2023-01 · [SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot](2023-2301.00774-sparsegpt-massive-language-models-can-be-accurately-pruned-in-one-shot.md)**  
  実装：[✓](https://github.com/IST-DASLab/sparsegpt) ・ リポジトリ内被引用：413  
  重みの絶対値が小さい順に削除する単純な枝刈りでは、巨大モデルであっても削除による層出力誤差が累積し、50%の疎化で性能が崩壊し得る。

- **2023-06 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](2023-2306.00978-awq.md)**  
  実装：[✓](https://github.com/mit-han-lab/llm-awq) ・ リポジトリ内被引用：391  
  活性の大きい入力チャネルに対応する重みを等価スケーリングで保護し、全重みを均一な低ビット形式のまま高精度化する重み専用量子化とTinyChat実装。

- **2023-06 · [A Simple and Effective Pruning Approach for Large Language Models](2023-2306.11695-a-simple-and-effective-pruning-approach-for-large-language-models.md)**  
  実装：[✓](https://github.com/locuslab/wanda) ・ リポジトリ内被引用：376  
  Wanda（重みと活性による枝刈り、枝刈り by 重み and 活性値）は、大規模言語モデルの線形層を追加学習も残存重みの更新も行わず疎化する方法である。LLaMA-7Bを50%非構造疎化したとき、WikiTextの困惑度は単純大きさ枝刈り17.29、Wanda 7.26、SparseGPT 7.22であり、軽い処理でも品質を大幅に保てる。

- **2023-08 · [OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models](2023-2308.13137-omniquant-omnidirectionally-calibrated-quantization-for-large-language-m.md)**  
  実装：[✓](https://github.com/OpenGVLab/OmniQuant) ・ リポジトリ内被引用：295  
  大規模言語モデルの重みを16ビットから4ビット、3ビット、2ビットへ縮めると、保存容量と重み転送量を大きく削減できる。一方、極低ビットでは重みや活性値の少数の外れ値が量子化範囲を広げ、重要な値の量子化刻みが粗くなって出力品質が崩れる。LLaMA-2 7B～70Bは128個の校正系列とA100 40GB 1基で1～16時間の処理が可能と報告される。

- **2023-07 · [QuIP: 2-Bit Quantization of Large Language Models With Guarantees](2023-2307.13304-quip-2-bit-quantization-of-large-language-models-with-guarantees.md)**  
  実装：✓ ・ リポジトリ内被引用：247  
  重みと代理ヘッセ行列（proxy Hessian）の座標依存の偏りをランダム直交変換で崩してから、LDL分解に基づく適応丸めを行う。Llama 2 70Bでは2ビット重みでもWikiText2パープレキシティ6.326を保ち、同条件のOPTQの123.908から大幅に改善する。

- **2023-06 · [SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression](2023-2306.03078-spqr-a-sparse-quantized-representation-for-near-lossless-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Vahe1994/SpQR) ・ リポジトリ内被引用：222  
  高感度な少数重みだけを十六ビット疎表現に逃がし、残りと量子化尺度を三〜四ビット化してほぼ無損失圧縮する混合重み表現。

- **2023-06 · [SqueezeLLM: Dense-and-Sparse Quantization](2023-2306.07629-squeezellm-dense-and-sparse-quantization.md)**  
  実装：[✓](https://github.com/SqueezeAILab/SqueezeLLM) ・ リポジトリ内被引用：220  
  二次感度に基づく非一様量子化と、外れ値・高感度重みだけをFP16疎行列へ逃がすDense-and-Sparse分解により、3-bit級でも品質を保ちながら重み転送量と生成遅延を削減する。

- **2023-05 · [LLM-QAT: Data-Free Quantization Aware Training for Large Language Models](2023-2305.17888-llm-qat-data-free-quantization-aware-training-for-large-language-models.md)**  
  実装：[✓](https://github.com/facebookresearch/LLM-QAT) ・ リポジトリ内被引用：197  
  LLM-QATは、学習後量子化（Post-学習 量子化: PTQ）では精度が大きく低下する低ビット領域に対し、量子化誤差を学習中に経験させる量子化対応学習（Quantization-Aware 学習: QAT）を大規模言語モデルへ適用する研究である。

- **2023-10 · [Atom: Low-bit Quantization for Efficient and Accurate LLM Serving](2023-2310.19102-atom-low-bit-quantization-for-efficient-and-accurate-llm-serving.md)**  
  実装：[✓](https://github.com/efeslab/Atom) ・ リポジトリ内被引用：155  
  外れ値チャネルだけ高精度に残して重み・活性・KVキャッシュを低ビット化し、再配置と融合カーネルで4ビットGPU演算器を直接使ってLLM配信を高速化する。

- **2023-06 · [OWQ: Outlier-Aware Weight Quantization for Efficient Fine-Tuning and Inference of Large Language Models](2023-2306.02272-owq-outlier-aware-weight-quantization-for-efficient-fine-tuning-and-infe.md)**  
  実装：[✓](https://github.com/xvyaward/owq) ・ リポジトリ内被引用：92  
  大規模言語モデルの重みを3ビット級へ圧縮すると、モデル容量と重み読出し量は減るが、わずかな量子化誤差が特定の特徴次元で増幅され、出力品質が大きく悪化することがある。

- **2022-12 · [The case for 4-bit precision: k-bit Inference Scaling Laws](2022-2212.09720-the-case-for-4-bit-precision-k-bit-inference-scaling-laws.md)**  
  実装：✓ ・ リポジトリ内被引用：85  
  量子化では、1パラメータ当たりのビット数を下げるほど同じ重みメモリへ大きなモデルを置ける。

- **2023-09 · [PB-LLM: Partially Binarized Large Language Models](2023-2310.00034-pb-llm-partially-binarized-large-language-models.md)**  
  実装：[✓](https://github.com/hahnyuan/BinaryLLM) ・ リポジトリ内被引用：64  
  重みを一律1ビット化するのではなく、ヘッセ行列で選んだ少数の顕著重みを高精度で残し、それ以外だけを±1へ二値化する。LLaMA-7Bでは顕著重み30%を残す量子化対応学習版が7つのゼロショット常識推論で平均66.9を達成し、10%まで減らしても60.6を保つ。

- **2023-06 · [OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization](2023-olive-accelerating-large-language-models-via-hardware-friendly-outlier-victim-pair-quantization.md)**  
  実装：[✓](https://github.com/clevercool/ANT-Quantization) ・ リポジトリ内被引用：55  
  外れ値を別の疎データ構造へ逃がすのではなく、隣接する低重要度の通常値を「犠牲値（victim）」として使い、外れ値を同じ固定幅ペアの中へ埋め込む。これにより外れ値対応量子化で問題になる座標リストと別演算経路をなくし、4ビットの整列アクセスをテンソルコアやシストリック配列へ直接載せる。

- **2023-04 · [Outlier Suppression+: Accurate quantization of large language models by equivalent and optimal shifting and scaling](2023-2304.09145-outlier-suppression-accurate-quantization-of-large-language-models-by-eq.md)**  
  実装：[✓](https://github.com/ModelTC/Outlier_Suppression_Plus) ・ リポジトリ内被引用：53  
  Outlier Suppression+（OS+）は、大規模言語モデルの活性値に現れる極端な外れ値が、事後量子化（Post-学習 量子化: PTQ）の精度を悪化させる問題に対する方法である。

- **2023-03 · [ZeroQuant-V2: Exploring Post-training Quantization in LLMs from Comprehensive Study to Low Rank Compensation](2023-2303.08302-zeroquant-v2-exploring-post-training-quantization-in-llms-from-comprehen.md)**  
  実装：✓ ・ リポジトリ内被引用：38  
  ZeroQuant-V2は、大規模言語モデルの学習後量子化（Post-学習 量子化、PTQ）を、特定の一手法の成功例だけで評価するのではなく、量子化対象、数値精度、粒度、モデル系列、最適化方式を組み合わせて調べた研究である。元の16ビットモデルは10.33なので、この設定では測定上ほぼ同等となる。

- **2023-06 · [LoSparse: Structured Compression of Large Language Models based on Low-Rank and Sparse Approximation](2023-2306.11222-losparse-structured-compression-of-large-language-models-based-on-low-rank-and-sparse-approximation.md)**  
  実装：[✓](https://github.com/yxli2123/LoSparse) ・ リポジトリ内被引用：36  
  各重み行列を「全ニューロンに共有される低ランク成分」と「ニューロン固有の残差成分」に分け、残差側だけを構造枝刈りする。低ランク近似が表現力のある共通基底を守るため、高い枝刈り率でも通常の反復構造枝刈りより品質を落としにくい。

- **2023-05 · [Memory-Efficient Fine-Tuning of Compressed Large Language Models via sub-4-bit Integer Quantization](2023-2305.14152-memory-efficient-fine-tuning-of-compressed-large-language-models-via-sub.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  提案するPEQA（パラメータ-Efficient and 量子化-aware Adaptation）は、事前学習済みの重みを3～4ビットなどの整数表現へ量子化した後、整数値を凍結し、量子化尺度だけを学習する。

- **2023-10 · [Dynamic Sparse No Training: Training-Free Fine-tuning for Sparse LLMs](2023-2310.08915-dynamic-sparse-no-training-training-free-fine-tuning-for-sparse-llms.md)**  
  実装：[✓](https://github.com/zyxxmu/DSnoT) ・ リポジトリ内被引用：24  
  DSnoT（動的 Sparse No 学習）は、既存の枝刈り手法で疎化した大規模言語モデル（Large Language モデル、LLM）を、勾配逆伝播も重み値の更新も行わずに改善する方法である。

- **2023-02 · [With Shared Microexponents, A Little Shifting Goes a Long Way](2023-2302.08007-with-shared-microexponents-a-little-shifting-goes-a-long-way.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  Rouhaniらは、ブロックデータ表現（Block Data Representation; BDR）という共通の設計枠を用意し、ブロックサイズ、尺度の階層、尺度を保存するビット数、各要素の仮数幅を変えて比較した。

- **2023-08 · [FineQuant: Unlocking Efficiency with Fine-Grained Weight-Only Quantization for LLMs](2023-2308.09723-finequant-unlocking-efficiency-with-fine-grained-weight-only-quantizatio.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  FineQuantは、大規模言語モデル（Large Language モデル; LLM）の重みだけを低ビット化し、活性値と積和演算は浮動小数点で実行する重み専用量子化（重み-only 量子化）の研究である。最大3.65倍の総処理量改善は、この三番目の複製数増加を含むノード全体の処理量であり、単一要求のトークン生成速度が3.65倍という意味ではない。

- **2023-10 · [E-Sparse: Boosting the Large Language Model Inference through Entropy-based N:M Sparsity](2023-2310.15929-e-sparse-boosting-the-large-language-model-inference-through-entropy-bas.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  こうした制約では重要な重みが同じ4要素のグループに集中すると、どれかを必ず削除しなければならず、言語モデルの品質が下がりやすい。残した重みの値を再学習・再最適化せずに疎性を作り、FasterTransformerへ統合した疎行列積（Sparse-GEMM）で実際の推論を高速化する。

- **2023-10 · [Dual Grained Quantization: Efficient Fine-Grained Quantization for LLM](2023-2310.04836-dual-grained-quantization-efficient-fine-grained-quantization-for-llm.md)**  
  実装：[✓](https://github.com/ilur98/DGQ) ・ リポジトリ内被引用：3  
  しかし、重みを小さなグループ単位で4ビット量子化すると、グループごとに尺度が異なるため、整数の行列積を区切って浮動小数点で部分和を結合する必要が生じる。原著はLLaMA、LLaMA 2、OPTなどで困惑度とゼロショット推論精度を評価し、単一A100 80GBでの実行時間・メモリ使用量を測定した。

- **2023-09 · [eDKM: An Efficient and Accurate Train-time Weight Clustering for Large Language Models](2023-2309.00964-edkm-an-efficient-and-accurate-train-time-weight-clustering-for-large-la.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  微分可能な重みクラスタリングDKMの注意マップを、装置間の重複コピー除去、重み値の一意化、索引の分割で約130分の1へ圧縮し、LLaMA-7Bの学習時3ビット圧縮を可能にするメモリ効率化。

- **2023-05 · [Revisiting Offline Compression: Going Beyond Factorization-based Methods for Transformer Language Models](2023-2302.04045-revisiting-offline-compression-going-beyond-factorization-based-methods-.md)**  
  実装：[✓](https://github.com/MohammadrezaBanaei/auto-encoder-based-transformer-compression) ・ リポジトリ内被引用：1  
  本研究は、既に学習されたTransformerの重み行列を、事前学習モデル全体の再訓練や蒸留を行わずに小さくする「オフライン圧縮」を対象とする。

- **2023-11 · [AWEQ: Post-Training Quantization with Activation-Weight Equalization for Large Language Models](2023-2311.01305-aweq-post-training-quantization-with-activation-weight-equalization-for-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化の難しさを範囲の比で定義し直し、活性値と重みの範囲を各チャネルで一致させる等化と、偏り誤差の統計的補正を組み合わせた学習不要量子化。8ビットと超低ビットの両方で既存手法を上回る。

- **2023-10 · [Zero-Shot Sharpness-Aware Quantization for Pre-trained Language Models](2023-2310.13315-zero-shot-sharpness-aware-quantization-for-pre-trained-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  データなし量子化の敵対的学習にシャープネス配慮を入れて平坦な解へ寄せるSAM-SGAにより、BERT系とGPT系の11課題で一貫して精度を改善し、低精度条件では平均で最大6.98ポイント回復させる。

- **2023-06 · [Binary and Ternary Natural Language Generation](2023-2306.01841-binary-and-ternary-natural-language-generation.md)**  
  実装：[✓](https://github.com/facebookresearch/Ternary_Binary_Transformer) ・ リポジトリ内被引用：0  
  重みの統計的量子化と活性値の学習的量子化を組み合わせ、要約と翻訳で初めて全三値・全二値の生成モデルを成立させ、三値では全精度に数点差まで迫る品質を示した。

### 5年前（2021-12〜2022-11）

- **2022-10 · [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](2022-2210.17323-gptq.md)**  
  実装：[✓](https://github.com/IST-DASLab/gptq) ・ リポジトリ内被引用：846  
  二次情報に基づく誤差補償をGPU向けに再設計し、175B級LLMを数時間で3〜4bit化して単一A100実行と約3.24倍の生成高速化を実現した基礎的GPTQ研究。

- **2022-11 · [SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models](2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models.md)**  
  実装：[✓](https://github.com/mit-han-lab/smoothquant) ・ リポジトリ内被引用：748  
  活性値全体を単純に8ビットへ写すと、その少数の外れ値が量子化範囲を広げ、通常値へ割り当てられる段階数が減って精度が崩れる。OPT、BLOOM、GLM、MT-NLGなどで8ビット重み・8ビット活性値（W8A8）を実現し、精度低下をほぼ抑えながら最大1.56倍の推論高速化と2倍のメモリ削減を報告し、530Bモデルを単一ノードで提供可能にした。

- **2022-11 · [LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](2022-2208.07339-llm-int8-8-bit-matrix-multiplication-for-transformers-at-scale.md)**  
  実装：[✓](https://github.com/TimDettmers/bitsandbytes) ・ リポジトリ内被引用：345  
  特徴次元の外れ値を16-bitへ分離し、残る99.9%以上をベクトル単位INT8で計算する。175B級モデルの品質とほぼ半減の重み容量を両立する一方、小さい行列では量子化費用が速度改善を打ち消す。

- **2022-06 · [ZeroQuant: Efficient and Affordable Post-Training Quantization for Large-Scale Transformers](2022-2206.01861-zeroquant-efficient-and-affordable-post-training-quantization-for-large-.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：225  
  大規模言語モデルの量子化では、重みを16ビットから8ビットへ減らすだけでメモリ転送量は小さくなる。INT8では追加の学習や校正なしでBERT・GPT系の品質をほぼ保ち、NVIDIA A100上のBERT-baseで最大5.19倍、GPT-3 350Mで4.16倍の速度向上を示した。

### 6年前（2020-12〜2021-11）

- **2021-01 · [I-BERT: Integer-only BERT Quantization](2021-2101.01321-i-bert-integer-only-bert-quantization.md)**  
  実装：[✓](https://github.com/kssteven418/i-bert) ・ リポジトリ内被引用：62  
  Transformerの重みと行列積を8ビット整数へ量子化しても、推論全体が整数だけで実行できるとは限らない。Tesla T4上の予備的な整数カーネル実装では、FP32比で2.4～4.0倍の推論高速化を報告する。

- **2021-09 · [Block Pruning For Faster Transformers](2021-2109.04838-block-pruning-for-faster-transformers.md)**  
  実装：[✓](https://github.com/huggingface/nn_pruning) ・ リポジトリ内被引用：43  
  Block Pruningは移動量に基づく枝刈り（movement 枝刈り）を重みブロック単位へ拡張し、フィードフォワード層の次元や注意ヘッドを構造的に除去できる形へ誘導する。

- **2021-02 · [Accelerated Sparse Neural Training: A Provable and Efficient Method to Find N:M Transposable Masks](2021-2102.08124-accelerated-sparse-neural-training-a-provable-and-efficient-method-to-fi.md)**  
  実装：[✓](https://github.com/papers-submission/structured_transposable_masks) ・ リポジトリ内被引用：19  
  本研究は、この非対称性を解消する転置可能細粒度疎マスク（transposable fine-grained sparsity mask）を提案する。論文が示す「2倍」は主として疎テンソルコアの適用可能な行列積の範囲の比較であり、全学習時間の2倍高速化を実測したものと読み替えない。

### 7年前（2019-12〜2020-11）

- **2020-05 · [GOBO: Quantizing Attention-Based NLP Models for Low Latency and Energy Efficient Inference](2020-2005.03842-gobo-quantizing-attention-based-nlp-models-for-low-latency-and-energy-ef.md)**  
  実装：✓ ・ リポジトリ内被引用：46  
  GOBOは、BERTなどの注意機構を使う自然言語処理モデルの重みを、学習後に大幅に圧縮する手法である。重みの約99.9%を少数の代表値への索引で表し、残る約0.1%の外れ値だけを元の32ビット浮動小数点のまま保持する。

- **2020-09 · [TernaryBERT: Distillation-aware Ultra-low Bit BERT](2020-2009.12812-ternarybert-distillation-aware-ultra-low-bit-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：35  
  TernaryBERTは、自然言語理解向けのBERTを極低ビットで実行可能な重み表現へ圧縮し、精度低下を知識蒸留（Knowledge Distillation）で抑える手法である。これにより重み2ビット・埋め込み2ビット・活性値8ビットの代表構成で、BERTの保存サイズを418MBから28MBへ減らす。

- **2020-02 · [Compressing BERT: Studying the Effects of Weight Pruning on Transfer Learning](2020-2002.08307-compressing-bert-studying-the-effects-of-weight-pruning-on-transfer-lear.md)**  
  実装：[✓](https://github.com/mitchellgordon95/bert-prune) ・ リポジトリ内被引用：31  
  対象はBERT-Baseの非構造化重み枝刈りである。主結果は、30～40%程度の重みを削除しても下流性能がほぼ変わらない一方、40～60%では事前学習で獲得した情報の消失が、70%以上ではそれに加えて残存ネットワークの表現容量制約が効くという三つの領域である。

- **2020-04 · [Training with Quantization Noise for Extreme Model Compression](2020-2004.07320-training-with-quantization-noise-for-extreme-model-compression.md)**  
  実装：[✓](https://github.com/pytorch/fairseq/tree/master/examples/quant_noise) ・ リポジトリ内被引用：27  
  学習済みモデルの重みを低ビットや積量子化で保存すると、推論時の重み容量を減らせるが、各層で生じた量子化誤差が次層の入力へ蓄積し、精度が急激に落ちることがある。ICLR 2021の原著では、16層Transformerの942MBを反復積量子化で38MBへ圧縮した場合、量子化雑音なしのテスト困惑度25.2に対して20.7へ改善した。

### 8年前（2018-12〜2019-11）

- **2019-09 · [Q-BERT: Hessian Based Ultra Low Precision Quantization of BERT](2019-1909.05840-q-bert-hessian-based-ultra-low-precision-quantization-of-bert.md)**  
  実装：✓ ・ リポジトリ内被引用：87  
  Q-BERTは、BERTの各層へ同じビット数を割り当てる均一量子化ではなく、損失関数の二階微分から層ごとの誤差感度を推定し、敏感な層へ高い精度を残す混合精度量子化手法である。論文はSST-2、MNLI、CoNLL-03、SQuADの四課題で、重みの最大13倍圧縮、埋め込みと活性値の最大4倍圧縮を報告し、強圧縮でも性能低下を最大2.3%以内に抑えたと説明する。

- **2019-10 · [Q8BERT: Quantized 8Bit BERT](2019-1910.06188-q8bert-quantized-8bit-bert.md)**  
  実装：[✓](https://github.com/NervanaSystems/nlp-architect) ・ リポジトリ内被引用：22  
  Q8BERTは、事前学習済みBERTを特定の自然言語処理課題へ微調整する段階で量子化誤差を模擬し、推論時の8ビット整数演算へ適応させる研究である。著者はBERTの重みの99%以上を占める埋め込み層と全結合層を8ビット整数へ対応させ、残りの数値的に敏感な演算は32ビット浮動小数点に残す。

### 11年前（2015-12〜2016-11）

- **2016-06 · [Compression of Neural Machine Translation Models via Pruning](2016-1606.09274-compression-of-neural-machine-translation-models-via-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  この論文は、注意機構付きの長短期記憶（LSTM）を使うニューラル機械翻訳器について、どの重みを消せば翻訳品質を損なわずに保存パラメータを減らせるかを実験した2016年の研究である。種類非依存枝刈りでは、40%の重みを消しても再学習前の品質劣化は小さく、さらに80%を消した後に残存重みだけを4エポック再学習すると20.91 BLEUまで回復した。
<!-- survey:auto:end -->
