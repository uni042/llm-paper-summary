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
## 自動生成の論文一覧（7本）

### 収録論文

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BF16重みの指数を固定長ビットマップへ無損失符号化し、圧縮データをレジスタ上で復元してテンソル Coreへ直送することで、重み帯域と中間展開の読み書きを減らす。

- **2026-09 · [Vortex: Bridging Extreme Compression and Efficient LLM Inference](2026-2609.12208-vortex-bridging-extreme-compression-and-efficient-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  超低ビットベクトル量子化と入力依存疎性を二種類の実行流へ合わせ、圧縮率を実際の推論高速化へ変換する加速器。

- **2026-08 · [FluxBin: Flexible LUT-based Ultra-low-bit LLM Inference by Algorithm-Kernel Synergy](2026-2608.15602-fluxbin-lut-ultra-low-bit-inference.md)**  
  実装：[✓](https://github.com/nicyyyy/FluxBin) ・ リポジトリ内被引用：0  
  重要列だけをヘッセ行列で選んで追加二値基底を与え、逆量子化を避けるLUT融合CUDAカーネルで約2〜3ビットLLMを実行し、A100で最大5.92倍高速化・10.19倍省エネルギーを報告する。

- **2026-06 · [SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving](2026-2606.11244-spear-error-adaptive-low-bit-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン適応型量子化誤差補償とカーネル・通信・SLOスケジューリングを共同設計し、W4–FP16のperplexity差を56–75%回復。

- **2022-10 · [GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](2022-2210.17323-gptq.md)**  
  実装：[✓](https://github.com/IST-DASLab/gptq) ・ リポジトリ内被引用：90  
  二次情報に基づく誤差補償をGPU向けに再設計し、175B級LLMを数時間で3〜4bit化して単一A100実行と約3.24倍の生成高速化を実現した基礎的GPTQ研究。

- **2023-06 · [AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](2023-2306.00978-awq.md)**  
  実装：[✓](https://github.com/mit-han-lab/llm-awq) ・ リポジトリ内被引用：37  
  活性の大きい入力チャネルに対応する重みを等価スケーリングで保護し、全重みを均一な低ビット形式のまま高精度化する重み専用量子化とTinyChat実装。

- **2023-06 · [SpQR: A Sparse-Quantized Representation for Near-Lossless LLM Weight Compression](2023-2306.03078-spqr-a-sparse-quantized-representation-for-near-lossless-llm-weight-compression.md)**  
  実装：[✓](https://github.com/Vahe1994/SpQR) ・ リポジトリ内被引用：19  
  高感度な少数重みだけを十六ビット疎表現に逃がし、残りと量子化尺度を三〜四ビット化してほぼ無損失圧縮する混合重み表現。
<!-- survey:auto:end -->
