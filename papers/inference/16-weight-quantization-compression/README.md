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
## 自動生成の論文一覧（19本）

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

- **2025-09 · [PTQTP: Post-Training Quantization to Trit-Planes for Large Language Models](2025-2509.16989-ptqtp-post-training-quantization-to-trit-planes-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  重みを2枚の三値平面と連続尺度へ分解し、乗算を加算中心へ変える超低ビット事後量子化を提案する。1.58ビット級の学習時量子化に匹敵しつつ量子化を約1時間で行い、FP16比最大4.63倍の推論高速化を報告する。

### 3年前（2023-10〜2024-09）

- **2024-05 · [QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving](2024-2405.04532-qserve.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  クラウド型LLM配信では、重みを低ビット化しても、量子化解除を計算の逐次部分で行うとCUDAコアの処理が律速となり、高速なテンソル Coreを十分活用できない。A100とL40Sを使った複数LLMの評価で、TensorRT-LLMに対する最大スループットの改善を報告する。

- **2024-01 · [SliM-LLM: Salience-Driven Mixed-Precision Quantization for Large Language Models](2024-2405.14917-slim-llm-salience-driven-mixed-precision-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  重要重みが構造的に偏る性質を利用し、グループごとにビット幅を割り当てつつ重要度を量子化器校正にも反映する。LLaMA-7Bの2ビット化でメモリを約6分の1にし、従来勾配不要方式よりパープレキシティを48%改善。

- **2024-01 · [SliceGPT: Compress Large Language Models by Deleting Rows and Columns](2024-2401.15024-slicegpt-compress-large-language-models-by-deleting-rows-and-columns.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  Transformerの計算不変性を利用して隠れ次元を回転し、重要度の低い行・列を丸ごと削って小さな密行列へ変換する。LLaMA2-70B等で最大25%のパラメータを削り、追加の疎行列カーネルなしでGPU数と計算量を減らす。

- **2024-01 · [LLM-FP4: 4-Bit Floating-Point Quantized Transformers](2023-2310.16836-llm-fp4-4-bit-floating-point-quantized-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  重みと活性値をともに4ビット浮動小数点へ事後量子化し、チャネル別活性値スケールを重み側へ再パラメータ化して低ビット推論を成立させる。LLaMA-13Bで平均63.1点を維持し従来最良を12.7点上回る。

- **2024-06 · [QTIP: Quantization with Trellises and Incoherence Processing](2024-2406.11235-qtip-quantization-with-trellises-and-incoherence-processing.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  重みを非コヒーレント変換で均質化した後、格子状の有限状態量子器でブロックを高密度に符号化し、2〜4ビット級の重み量子化で低い誤差と実用的な復号を両立する。

### 4年前（2022-10〜2023-09）

- **2022-10 · [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](2022-2210.17323-gptq.md)**  
  実装：[✓](https://github.com/IST-DASLab/gptq) ・ リポジトリ内被引用：112  
  二次情報に基づく誤差補償をGPU向けに再設計し、175B級LLMを数時間で3〜4bit化して単一A100実行と約3.24倍の生成高速化を実現した基礎的GPTQ研究。

- **2023-06 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](2023-2306.00978-awq.md)**  
  実装：[✓](https://github.com/mit-han-lab/llm-awq) ・ リポジトリ内被引用：41  
  活性の大きい入力チャネルに対応する重みを等価スケーリングで保護し、全重みを均一な低ビット形式のまま高精度化する重み専用量子化とTinyChat実装。

- **2022-11 · [LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](2022-2208.07339-llm-int8-8-bit-matrix-multiplication-for-transformers-at-scale.md)**  
  実装：[✓](https://github.com/TimDettmers/bitsandbytes) ・ リポジトリ内被引用：30  
  特徴次元の外れ値を16-bitへ分離し、残る99.9%以上をベクトル単位INT8で計算する。175B級モデルの品質とほぼ半減の重み容量を両立する一方、小さい行列では量子化費用が速度改善を打ち消す。

- **2023-06 · [SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression](2023-2306.03078-spqr-a-sparse-quantized-representation-for-near-lossless-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Vahe1994/SpQR) ・ リポジトリ内被引用：25  
  高感度な少数重みだけを十六ビット疎表現に逃がし、残りと量子化尺度を三〜四ビット化してほぼ無損失圧縮する混合重み表現。

- **2023-09 · [PB-LLM: Partially Binarized Large Language Models](2023-2310.00034-pb-llm-partially-binarized-large-language-models.md)**  
  実装：[✓](https://github.com/hahnyuan/BinaryLLM) ・ リポジトリ内被引用：5  
  顕著重みだけを高精度で保持し残りを二値化し、ヘッセ行列による再構成と量子化対応学習を組み合わせて、単純二値化で崩れるLLMの推論能力を極低ビット領域で回復する。
<!-- survey:auto:end -->
