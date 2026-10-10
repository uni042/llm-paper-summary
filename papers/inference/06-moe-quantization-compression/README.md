# MoE Quantization / Compression

MoEの大部分を占めるexpert重みを**低bit化、pruning、precision切替などで小さくし、VRAM・storage容量・memory bandwidth・計算量を減らす**研究をまとめる。MoEではexpertごとに利用頻度や量子化耐性が違うため、全weightを一律に同じbit幅へ落とすより、expertやlayerごとに精度を変える手法が多い。

単にモデルを小さくするだけでなく、routing結果を崩さないこと、頻繁に使うexpertへ高い精度を残すこと、実際のGPU kernelで速くなるbit配置を選ぶことも重要な評価軸となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（19本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md)**  
  実装：[✓](https://github.com/kexinchu/DynaQuant) ・ リポジトリ内被引用：2  
  DynaExqは、専門家混合モデル（Mixture of エキスパート; MoE）を単一GPUの限られた高帯域メモリへ載せるため、専門家ごとの量子化精度を推論中に変更するシステムである。論文はQwen3-30B-A3B、Qwen3-80B-A3B、Phi-3.5-MoEをRTX A6000 48GBの単一GPUで測定した。

- **2026-07 · [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PagedWeightは、KVキャッシュで空いたVRAMが減ると品質感度の低い専門家重みからビット幅を下げ、余裕が戻れば復元して、長文サービングの容量競合を和らげる。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [When Load-Balancing Goes Too Far: Expert Pruning in Over-Dispersed Mixture-of-Experts Models](2026-2609.04453-expert-pruning-over-dispersed-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  強い負荷分散学習でルータ重要度が一様化したMoEでは通常の枝刈り基準が破綻することを示し、最悪影響領域を反復保護するMESAで25%専門家削減時の能力偏りを抑える。

- **2026-08 · [Tied Trit-Planes: Constraining PTQTP to a Uniform Nine-Level Quantizer, with a Persistent Folded Format for Disk-Streamed Mixture-of-Experts Serving](2026-2608.08910-tied-trit-planes.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUや主記憶へ全専門家を置けない端末では必要な専門家をSSDから読むため、量子化は容量だけでなくSSD読込み量、専門家キャッシュ容量、実行カーネル入力まで同時に決める。DeepSeek-V4-Flash-0731のルーティング専門家を公開MXFP4重みから一括量子化し、64GBノートPCでSSDストリーミングした。

- **2026-05 · [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md)**  
  実装：[✓](https://github.com/jndeng/GEMQ) ・ リポジトリ内被引用：0  
  総パラメータ数が大きいモデルをGPUメモリへ載せるためには量子化が有効だが、すべての専門家を同じビット幅へ圧縮すると、特に1〜2ビットという極低精度で品質が大きく崩れる。

### 2年前（2024-11〜2025-10）

- **2025-07 · [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  混合専門家（Mixture of エキスパート、MoE）型の大規模言語モデルは、トークンごとに少数の専門家だけを実行するため活性パラメータ数を抑えられるが、専門家の総重みは大きく、GPUメモリの負担が残る。重み量子化は保存容量を削減する一方、各層の出力を少し変化させる。

- **2025-05 · [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md)**  
  実装：[✓](https://github.com/cat538/MxMoE) ・ リポジトリ内被引用：12  
  MxMoEは、混合専門家モデル（Mixture of エキスパート; MoE）の推論において、モデルの重みを小さくするだけでなく、実際にGPU上で計算が速くなる量子化配置を選ぶ研究である。専門家演算の処理量は16ビット基準に対して、512トークン条件で1.6～2.7倍、8192トークン条件で3.0～3.4倍となった。

- **2025-02 · [Delta Decompression for MoE-based LLMs Compression](2025-2502.17298-delta-decompression-for-moe-based-llms-compression.md)**  
  実装：[✓](https://github.com/lliai/D2MoE) ・ リポジトリ内被引用：10  
  しかし、推論環境には多数の専門家の重みを保持する必要があり、GPUメモリ・ホストメモリ・ストレージ容量が大きくなる。専門家を丸ごと削除すると特化した能力を失い、複数専門家を単純に統合すると固有の知識が平均化される。

- **2025-05 · [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md)**  
  実装：[✓](https://github.com/chenzx921020/MoEQuant) ・ リポジトリ内被引用：8  
  MoEQuantは、較正例を低頻度専門家へ補い、ルータ寄与の大きいトークンを重く量子化評価して、同じ低ビットでも専門家出力の品質劣化を抑える。

- **2025-06 · [EAQuant: Enhancing Post-Training Quantization for MoE Models via Expert-Aware Optimization](2025-2506.13329-eaquant-enhancing-post-training-quantization-for-moe-models.md)**  
  実装：[✓](https://github.com/darren-fzq/EAQuant) ・ リポジトリ内被引用：5  
  密モデル向けの事後学習量子化（Post-学習 量子化; PTQ）をMoEへそのまま持ち込むと、専門家ごとに異なる活性外れ値、量子化後のルータTop-kの入れ替わり、ほとんど選ばれない専門家の校正データ不足が重なる。EAQuantはこれを一つの量子化誤差として扱わず、専門家認識平滑化、ルーティング整合、専門家単位の校正データ均衡の三機構に分解して補正する。

- **2025-03 · [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  DynaMoは、混合専門家モデル（Mixture-of-Experts; MoE）の量子化を、固定された1種類の較正データに最適化するのではなく、複数のデータ集合にわたる専門家の重要度変動と、入力分布の変化に応じて調整する手法である。

- **2025-10 · [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) ・ リポジトリ内被引用：0  
  混合専門家モデル（Mixture of エキスパート、MoE）は、トークンごとに一部の専門家だけを実行することで、総パラメータ数の大きさと実行計算量を切り離す。Mixtral-8x7Bでは、PMQにより16ビット版96.80GBの重みを平均2.05ビット・13.41GBへ圧縮する。

- **2025-03 · [ResMoE: Space-efficient Compression of Mixture of Experts LLMs via Residual Restoration](2025-2503.06881-resmoe-space-efficient-compression-of-mixture-of-experts-llms-via-residual-restoration.md)**  
  実装：[✓](https://github.com/iDEA-iSAIL-Lab-UIUC/ResMoE) ・ リポジトリ内被引用：0  
  専門家群の共有成分をワッサースタイン重心へ集約し、各専門家固有の差分だけを圧縮・実行時復元することで、専門家を消す方式より個性を残しつつ約75%の容量削減を狙う。

### 3年前（2023-11〜2024-10）

- **2024-10 · [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) ・ リポジトリ内被引用：37  
  MC-MoEは、専門家ごとの混合精度で保存重みを圧縮し、トークンごとに寄与の小さい専門家を動的枝刈りして、容量と実行FLOPsを別々に減らす。

- **2024-06 · [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)**  
  実装：[✓](https://github.com/UNITES-Lab/moe-quantization) ・ リポジトリ内被引用：19  
  このベンチマークは、MoEの平均ビット予算を専門家頻度・ブロック位置・線形層へ割り当てて比較し、モデル別に量子化誤差へ効く保護対象を測定する。

- **2024-05 · [A Provably Effective Method for Pruning Experts in Fine-tuned Sparse Mixture-of-Experts](2024-2405.16646-provably-effective-pruning-finetuned-sparse-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  事前学習からファインチューニングまでのルーター変化を専門家重要度として使い、視覚MoEで専門家を大きく削減しながら精度を保つ、理論付きの専門家枝刈り法を示す。

- **2024-07 · [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  本論文は、混合専門家モデル（Mixture-of-Experts、MoE）を限られたGPUメモリで動かすとき、専門家の量子化精度とCPU/GPU上の配置を別々の選択変数として扱い、推論サービスの品質と生成速度を調整する方式を提案する。対象は単一GPU上のMixtral 8x7Bであり、分散学習や多数GPU間の専門家並列処理ではない。

### 4年前（2022-11〜2023-10）

- **2023-10 · [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md)**  
  実装：✓ ・ リポジトリ内被引用：25  
  MoQEは、モデル容量の大半を占める専門家FFNだけを2〜8ビット化し、注意・共有FFNは高精度に残して、品質を守りながら保存量と重み帯域を減らす。

- **2023-10 · [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md)**  
  実装：[✓](https://github.com/IST-DASLab/qmoe) ・ リポジトリ内被引用：18  
  QMoEは、Switch Transformerの専門家重みをデータ依存に2ビット/三値圧縮し、圧縮表現を直接読むGPUカーネルで展開帯域を抑え、超大規模MoEの保存容量を減らす。
<!-- survey:auto:end -->
