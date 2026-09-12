# MoE Quantization / Compression

MoEの大部分を占めるexpert重みを**低bit化、pruning、precision切替などで小さくし、VRAM・storage容量・memory bandwidth・計算量を減らす**研究をまとめる。MoEではexpertごとに利用頻度や量子化耐性が違うため、全weightを一律に同じbit幅へ落とすより、expertやlayerごとに精度を変える手法が多い。

単にモデルを小さくするだけでなく、routing結果を崩さないこと、頻繁に使うexpertへ高い精度を残すこと、実際のGPU kernelで速くなるbit配置を選ぶことも重要な評価軸となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md)**  
  実装：[✓](https://github.com/kexinchu/DynaQuant) ・ リポジトリ内被引用：2  
  DynaExqは、ルーティング履歴から利用頻度の高い専門家を高ビットへ昇格し、低頻度専門家を低ビットに保って、限られたHBMを品質に効く重みへ配分する。

- **2026-07 · [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  PagedWeightは、KVキャッシュで空いたVRAMが減ると品質感度の低い専門家重みからビット幅を下げ、余裕が戻れば復元して、長文サービングの容量競合を和らげる。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [When Load-Balancing Goes Too Far: Expert Pruning in Over-Dispersed Mixture-of-Experts Models](2026-2609.04453-expert-pruning-over-dispersed-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  強い負荷分散学習でルータ重要度が一様化したMoEでは通常の枝刈り基準が破綻することを示し、最悪影響領域を反復保護するMESAで25%専門家削減時の能力偏りを抑える。

- **2026-05 · [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md)**  
  実装：[✓](https://github.com/jndeng/GEMQ) ・ リポジトリ内被引用：0  
  GEMQは、全層の専門家を一つのメモリ予算で比較してビット幅を配分し、量子化後はルータを微調整して、専門家品質の低下と誤選択を抑える。

- **2025-10 · [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) ・ リポジトリ内被引用：0  
  MC#は、専門家ごとのビット幅で保存重みを圧縮し、トークンごとに必要な専門家数を学習して枝刈りし、LLM/VLMの容量と実行計算量を同時に減らす。

### 2年前（2024-10〜2025-09）

- **2024-10 · [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) ・ リポジトリ内被引用：10  
  MC-MoEは、専門家ごとの混合精度で保存重みを圧縮し、トークンごとに寄与の小さい専門家を動的枝刈りして、容量と実行FLOPsを別々に減らす。

- **2025-05 · [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md)**  
  実装：[✓](https://github.com/cat538/MxMoE) ・ リポジトリ内被引用：5  
  MxMoEは、専門家内の各線形ブロックを量子化誤差・利用頻度・GPU実測時間で比較し、メモリ予算内のビット配置を品質と実速度の両面で選ぶ。

- **2025-08 · [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  EAC-MoEは、量子化でルータが選ぶ専門家がずれる誤差を重点補正し、プリフィルで低頻度専門家を入力単位に枝刈りして、品質と容量を両立する。

- **2025-05 · [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md)**  
  実装：[✓](https://github.com/chenzx921020/MoEQuant) ・ リポジトリ内被引用：3  
  MoEQuantは、較正例を低頻度専門家へ補い、ルータ寄与の大きいトークンを重く量子化評価して、同じ低ビットでも専門家出力の品質劣化を抑える。

- **2025-03 · [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation（旧題 MoQa）](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  DynaMoは、データ集合ごとの専門家重要度に応じてINT2〜8のビット幅を切替え、変化に敏感なチャネルだけを更新して、全モデル再量子化なしに品質を保つ。

### 3年前（2023-10〜2024-09）

- **2023-10 · [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  MoQEは、モデル容量の大半を占める専門家FFNだけを2〜8ビット化し、注意・共有FFNは高精度に残して、品質を守りながら保存量と重み帯域を減らす。

- **2023-10 · [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md)**  
  実装：[✓](https://github.com/IST-DASLab/qmoe) ・ リポジトリ内被引用：10  
  QMoEは、Switch Transformerの専門家重みをデータ依存に2ビット/三値圧縮し、圧縮表現を直接読むGPUカーネルで展開帯域を抑え、超大規模MoEの保存容量を減らす。

- **2024-06 · [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)**  
  実装：[✓](https://github.com/UNITES-Lab/moe-quantization) ・ リポジトリ内被引用：8  
  このベンチマークは、MoEの平均ビット予算を専門家頻度・ブロック位置・線形層へ割り当てて比較し、モデル別に量子化誤差へ効く保護対象を測定する。

- **2024-07 · [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  Mixture of Precisionsは、専門家ごとの4/16ビット精度とCPU/GPU配置をVRAM予算に応じて切替え、品質低下とPCIe転送を抑えながらスループットを調整する。
<!-- survey:auto:end -->
