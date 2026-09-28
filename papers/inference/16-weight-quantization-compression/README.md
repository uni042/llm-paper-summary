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
## 自動生成の論文一覧（31本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BF16重みの指数を固定長ビットマップへ無損失符号化し、圧縮データをレジスタ上で復元してテンソル Coreへ直送することで、重み帯域と中間展開の読み書きを減らす。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Vortex: Bridging Extreme Compression and Efficient LLM Inference](2026-2609.12208-vortex-bridging-extreme-compression-and-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  超低ビットベクトル量子化と入力依存疎性を二種類の実行流へ合わせ、圧縮率を実際の推論高速化へ変換する加速器。

- **2026-09 · [VLAQuantBench: Closed-Loop Evaluation of Post-Training Quantization for Vision-Language-Action Models](2026-2609.25376-vlaquantbench.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事後量子化で重みや活性値を低精度化すればメモリと計算を減らせるが、開ループの再構成誤差だけでは実際のタスク成功率を予測しにくい。未校正W4A4のπ0.5では対象を126層から167層へ広げると成功率が7.0%から70.5%へ逆に回復し、単純な「量子化層が少ないほど安全」という直感が破れることを示した。

- **2026-09 · [Predict Before You Deploy: Offline Prediction of Quantization-Induced Task Degradation for World Action Models](2026-2609.19441-prede-quantization-task-degradation-prediction.md)**  
  実装：[✓](https://github.com/jiuyixu25/PreDE) ・ リポジトリ内被引用：0  
  固定ログ上の行動偏差を少数の閉ループ結果で方策別に較正し、量子化候補を受理・棄却・保留へ分けて実機試験を絞るPreDE。

- **2026-09 · [All for 1-Bit: Towards Genuine 1-Bit Post-Training Quantization for LLMs](2026-2609.06161-all-for-1-bit.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  All for 1-Bit（AF1）は、既存の「1ビット」学習後量子化が尺度、外れ値、グループ情報などの補助データを含めると実効2〜4ビット/重みへ膨らむ問題に対し、対象線形重みを実効1.0ビット/重みに収める学習後量子化方式である。

- **2026-08 · [SchurQuant: Groupwise Discrete Optimization for Layer-Wise LLM Quantization](2026-2608.15567-schurquant.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み専用の事後量子化（Post-学習 量子化; PTQ）は、再学習せずにLLMのメモリ量と重み帯域を減らせる。8つのLlama/Qwenモデルで逆伝播不要の比較法中最高の平均ゼロショット精度となり、2ビットでは最強比較法を9.65ポイント上回った。

- **2026-08 · [SandwichQuant: Which Parameters Matter Before and After Quantization?](2026-2608.24173-sandwichquant-which-parameters-matter-before-and-after-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  事後量子化（Post-学習 量子化; PTQ）の品質を回復する研究では、重み、量子化尺度、丸め、局所再構成などを調整する。Llama2-7B、Llama3-8B、Qwen3-8Bなどの強い量子化条件で一貫して改善し、Llama2-7BのW2A4KV4条件では比較構成の平均6タスク精度48.9を55.1へ改善する一方、推論時の追加演算子は増やさない。

- **2026-08 · [FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy](2026-2608.15602-fluxbin-lut-ultra-low-bit-inference.md)**  
  実装：[✓](https://github.com/nicyyyy/FluxBin) ・ リポジトリ内被引用：0  
  重要列だけをヘッセ行列で選んで追加二値基底を与え、逆量子化を避けるLUT融合CUDAカーネルで約2〜3ビットLLMを実行し、A100で最大5.92倍高速化・10.19倍省エネルギーを報告する。

- **2026-06 · [SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving](2026-2606.11244-spear-error-adaptive-low-bit-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン適応型量子化誤差補償とカーネル・通信・SLOスケジューリングを共同設計し、W4–FP16のperplexity差を56–75%回復。

### 2年前（2024-10〜2025-09）

- **2025-08 · [Efficient Mixed-Precision Large Language Model Inference with TurboMind](2025-2508.15601-efficient-mixed-precision-large-language-model-inference.md)**  
  実装：[✓](https://github.com/InternLM/lmdeploy) ・ リポジトリ内被引用：5  
  TurboMindは、重み・活性値・キー・バリュー（Key-Value; KV）キャッシュの精度が混在するLLM推論を、単に低ビットカーネルへ置き換えるのではなく、GPUメモリ階層とテンソルコア命令に合わせて二つのパイプラインへ再設計する。

- **2025-09 · [PTQTP: Post-Training Quantization to Trit-Planes for Large Language Models](2025-2509.16989-ptqtp-post-training-quantization-to-trit-planes-for-large-language-models.md)**  
  実装：[✓](https://github.com/HeXiao-55/PTQTP) ・ リポジトリ内被引用：3  
  PTQTPは、学習済み重みを2枚の三値平面（trit-plane）と連続尺度へ分解し、約1.58ビット級の超低ビット表現を事後量子化（Post-学習 量子化; PTQ）だけで作る。二値PTQより表現力を増やしつつ、混合精度の例外経路を使わず一様な三値演算へ落とすのが狙いである。

- **2025-02 · [Huff-LLM: End-to-End Lossless Compression for Efficient LLM Inference](2025-2502.00922-huff-llm-end-to-end-lossless-compression-for-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  FP16/BF16重みを小bit群へ分割Huffman圧縮し、1cycle decoderを演算器直前へ置いて損失なしのまま容量・帯域・遅延を減らすHuff-LLM。

### 3年前（2023-10〜2024-09）

- **2024-05 · [QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving](2024-2405.04532-qserve.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  クラウド型LLM配信では、重みを低ビット化しても、量子化解除を計算の逐次部分で行うとCUDAコアの処理が律速となり、高速なテンソル Coreを十分活用できない。A100とL40Sを使った複数LLMの評価で、TensorRT-LLMに対する最大スループットの改善を報告する。

- **2024-02 · [BiLLM: Pushing the Limit of Post-Training Quantization for LLMs](2024-2402.04291-billm-pushing-the-limit-of-post-training-quantization-for-llms.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/BiLLM) ・ リポジトリ内被引用：7  
  ヘッセ感度で重要列を選び二値残差近似し、残りのベル形重み分布を最適分割して別々に二値化することで、再学習なしにLLM重みを約1.1ビットまで圧縮する。

- **2024-01 · [SliM-LLM: Salience-Driven Mixed-Precision Quantization for Large Language Models](2024-2405.14917-slim-llm-salience-driven-mixed-precision-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  要素単位で重要重みだけ高精度に残すのではなく、重要度が空間的にまとまる性質を使ってグループ単位で1/2/3ビットを割り当てる。さらに各グループ内部の少数の重要要素を量子化器校正で重く扱い、LLaMA-7Bの2ビット級でWikiText2パープレキシティ14.58を達成する。

- **2024-02 · [GPTVQ: The Blessing of Dimensionality for LLM Quantization](2024-2402.15319-gptvq-the-blessing-of-dimensionality-for-llm-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  複数の重みを1ベクトルとして量子化し、代理ヘッセ行列（proxy Hessian）で量子化誤差を後続列へ補償する。Llama 3 8Bの約3.125 bit/value構成では、Snapdragon X Elite上で独自INT4実装よりモデル占有量を約19%減らし、23.81から26.15 トークン/sへ高速化する。

- **2024-01 · [SliceGPT: Compress Large Language Models by Deleting Rows and Columns](2024-2401.15024-slicegpt-compress-large-language-models-by-deleting-rows-and-columns.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  Transformerの隠れ表現を直交回転して主成分基底へ移し、情報量の小さい埋め込み次元を重み行列の行・列ごと物理的に削除する。疎行列を作らず小さい密行列へ変換するため、LLaMA-2 70Bの25%削減ではA100上の1トークン時間を125 msから110 msへ、必要GPU数を4台から3台へ減らす。

- **2024-06 · [LLMEasyQuant: Scalable Quantization for Parallel and Distributed LLM Inference](2024-2406.19657-llmeasyquant-scalable-quantization-for-parallel-and-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/NoakLiu/LLMEasyQuant) ・ リポジトリ内被引用：4  
  量子化アルゴリズムだけでなく、尺度推定、CUDA融合、実行時再校正、GPU間同期、書出しまでを同じ実行系にまとめる。現行arXiv v6ではLLaMA-7Bで2,156 トークン/sを報告する。

- **2024-03 · [AffineQuant: Affine Transformation Quantization for Large Language Models](2024-2403.12544-affinequant-affine-transformation-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  スカラーの拡大縮小や平行移動に限られていた等価変換を、可逆な行列によるアフィン変換へ拡張する。変換を量子化前の重みへ掛け、逆変換を活性値側へ入れることで元の線形演算を保ったまま量子化しやすい座標系を学習し、LLaMA2-7BのW4A4でC4パープレキシティをOmniQuantの18.02から15.76へ改善する。

- **2024-01 · [LLM-FP4: 4-Bit Floating-Point Quantized Transformers](2023-2310.16836-llm-fp4-4-bit-floating-point-quantized-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  4ビット浮動小数点（floating point; FP）の指数部構成とクリップ範囲を層ごとに探索し、活性値の大きなチャネル間分散はチャネル別指数バイアスを重みへ事前吸収して処理する。LLaMA-13Bの埋め込み・重み・活性値を4/4/4ビットにして、6つの常識推論タスク平均63.1を維持する。

- **2024-07 · [Compact Language Models via Pruning and Knowledge Distillation](2024-2407.14679-compact-language-models-via-pruning-and-knowledge-distillation.md)**  
  実装：[✓](https://github.com/NVlabs/Minitron) ・ リポジトリ内被引用：3  
  15Bを学習した後に8B・4Bを別々にゼロから学習する代わりに、Nemotron-4 15Bから注意ヘッド、MLP中間次元、埋め込み幅、必要に応じて層を構造枝刈りし、元15Bのロジットを教師にして短期間だけ知識蒸留（Knowledge Distillation; KD）する。

- **2024-06 · [QTIP: Quantization with Trellises and Incoherence Processing](2024-2406.11235-qtip-quantization-with-trellises-and-incoherence-processing.md)**  
  実装：[✓](https://github.com/Cornell-RelaxML/qtip) ・ リポジトリ内被引用：3  
  ベクトル量子化（Vector Quantization, VQ）は複数重みをまとめて符号化するほど量子化効率が上がる一方、通常の符号帳は次元に対して指数的に巨大化する。QTIPは、符号帳を列挙せず有限状態の「トレリス」を使うことで、この次元の壁を外し、2bit級でも256次元の高次元量子化を実用的な復号コストで実現する。

- **2024-06 · [DuQuant: Distributing Outliers via Dual Transformation Makes Stronger Quantized LLMs](2024-2406.01721-duquant-distributing-outliers-via-dual-transformation-makes-stronger-quantized-llms.md)**  
  実装：[✓](https://github.com/Hsu1023/DuQuant) ・ リポジトリ内被引用：3  
  巨大外れ値を外れ値誘導のブロック回転とジグザグ置換で分散し、4ビット重み・活性量子化の精度を改善しつつ、LLaMA2-7Bでプリフィル最大2.08倍・復号時メモリ3.50倍削減を示す。

### 4年前（2022-10〜2023-09）

- **2022-10 · [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](2022-2210.17323-gptq.md)**  
  実装：[✓](https://github.com/IST-DASLab/gptq) ・ リポジトリ内被引用：114  
  二次情報に基づく誤差補償をGPU向けに再設計し、175B級LLMを数時間で3〜4bit化して単一A100実行と約3.24倍の生成高速化を実現した基礎的GPTQ研究。

- **2023-06 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](2023-2306.00978-awq.md)**  
  実装：[✓](https://github.com/mit-han-lab/llm-awq) ・ リポジトリ内被引用：42  
  活性の大きい入力チャネルに対応する重みを等価スケーリングで保護し、全重みを均一な低ビット形式のまま高精度化する重み専用量子化とTinyChat実装。

- **2022-11 · [LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](2022-2208.07339-llm-int8-8-bit-matrix-multiplication-for-transformers-at-scale.md)**  
  実装：[✓](https://github.com/TimDettmers/bitsandbytes) ・ リポジトリ内被引用：31  
  特徴次元の外れ値を16-bitへ分離し、残る99.9%以上をベクトル単位INT8で計算する。175B級モデルの品質とほぼ半減の重み容量を両立する一方、小さい行列では量子化費用が速度改善を打ち消す。

- **2023-06 · [SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression](2023-2306.03078-spqr-a-sparse-quantized-representation-for-near-lossless-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Vahe1994/SpQR) ・ リポジトリ内被引用：26  
  高感度な少数重みだけを十六ビット疎表現に逃がし、残りと量子化尺度を三〜四ビット化してほぼ無損失圧縮する混合重み表現。

- **2023-09 · [PB-LLM: Partially Binarized Large Language Models](2023-2310.00034-pb-llm-partially-binarized-large-language-models.md)**  
  実装：[✓](https://github.com/hahnyuan/BinaryLLM) ・ リポジトリ内被引用：6  
  重みを一律1ビット化するのではなく、ヘッセ行列で選んだ少数の顕著重みを高精度で残し、それ以外だけを±1へ二値化する。LLaMA-7Bでは顕著重み30%を残す量子化対応学習版が7つのゼロショット常識推論で平均66.9を達成し、10%まで減らしても60.6を保つ。

- **2023-07 · [QuIP: 2-Bit Quantization of Large Language Models With Guarantees](2023-2307.13304-quip-2-bit-quantization-of-large-language-models-with-guarantees.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  重みと代理ヘッセ行列（proxy Hessian）の座標依存の偏りをランダム直交変換で崩してから、LDL分解に基づく適応丸めを行う。Llama 2 70Bでは2ビット重みでもWikiText2パープレキシティ6.326を保ち、同条件のOPTQの123.908から大幅に改善する。

- **2023-06 · [LoSparse: Structured Compression of Large Language Models based on Low-Rank and Sparse Approximation](2023-2306.11222-losparse-structured-compression-of-large-language-models-based-on-low-rank-and-sparse-approximation.md)**  
  実装：[✓](https://github.com/yxli2123/LoSparse) ・ リポジトリ内被引用：3  
  各重み行列を「全ニューロンに共有される低ランク成分」と「ニューロン固有の残差成分」に分け、残差側だけを構造枝刈りする。低ランク近似が表現力のある共通基底を守るため、高い枝刈り率でも通常の反復構造枝刈りより品質を落としにくい。

### 公開時期未分類

- **2023 · [OliVe: Accelerating Large Language Models via Hardware-friendly Outlier-Victim Pair Quantization](2023-olive-accelerating-large-language-models-via-hardware-friendly-outlier-victim-pair-quantization.md)**  
  実装：[✓](https://github.com/clevercool/ANT-Quantization) ・ リポジトリ内被引用：3  
  外れ値を別の疎データ構造へ逃がすのではなく、隣接する低重要度の通常値を「犠牲値（victim）」として使い、外れ値を同じ固定幅ペアの中へ埋め込む。これにより外れ値対応量子化で問題になる座標リストと別演算経路をなくし、4ビットの整列アクセスをテンソルコアやシストリック配列へ直接載せる。
<!-- survey:auto:end -->
