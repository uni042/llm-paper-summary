# MoE Quantization / Compression

MoEの大部分を占めるexpert重みを**低bit化、pruning、precision切替などで小さくし、VRAM・storage容量・memory bandwidth・計算量を減らす**研究をまとめる。MoEではexpertごとに利用頻度や量子化耐性が違うため、全weightを一律に同じbit幅へ落とすより、expertやlayerごとに精度を変える手法が多い。

単にモデルを小さくするだけでなく、routing結果を崩さないこと、頻繁に使うexpertへ高い精度を残すこと、実際のGPU kernelで速くなるbit配置を選ぶことも重要な評価軸となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md)**  
  実装：[✓](https://github.com/kexinchu/DynaQuant) ・ リポジトリ内被引用：2  
  実際のルーティング履歴から利用頻度が高いエキスパートだけを高ビットへ切り替え、低頻度エキスパートは低ビットのままにして、限られたVRAMを重要エキスパートへ重点配分する実行時方式。

- **2026-07 · [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV キャッシュが増えて空きVRAMが減ったとき、品質への影響が小さいエキスパート 重み部分から段階的にビット幅を下げ、余裕が戻れば高精度へ戻すサービング方式。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-05 · [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md)**  
  実装：[✓](https://github.com/jndeng/GEMQ) ・ リポジトリ内被引用：0  
  全層のエキスパートを同じメモリ 予算の中で比較し、低ビット化したとき品質へ効きにくいエキスパートから強く圧縮したうえで、量子化後のエキスパート性能に合わせてルータだけを微調整する手法。

- **2025-10 · [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) ・ リポジトリ内被引用：0  
  エキスパートごとにビット幅を変えて重み容量を減らし、さらにトークンごとに必要なエキスパート数を学習して、LLM/VLMの保存容量と実行計算量を同時に削る手法。

### 1年以上前

- **2023-10 · [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  MoQEは「MoEは1 トークンで少数エキスパートしか計算しないのに、なぜ推論は遅く大きいのか」をエキスパート 重みの保存量と読出し帯域の問題として捉え、モデルの92%以上を占めるエキスパート 重みだけを強く低bit化する研究である。

- **2023-10 · [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md)**  
  実装：[✓](https://github.com/IST-DASLab/qmoe) ・ リポジトリ内被引用：10  
  trillion-パラメータ級MoEのエキスパート重みを3値化し、よく現れる値の並びをまとめて圧縮保存し、その圧縮形式を直接読む専用カーネルで推論する方式。

- **2024-10 · [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)**  
  実装：[✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) ・ リポジトリ内被引用：9  
  エキスパートごとにビット幅を変える量子化と、トークンごとに寄与の小さいエキスパートを実行しない仕組みを組み合わせ、保存容量と実行FLOPsを同時に削減する手法。

- **2024-06 · [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)**  
  実装：[✓](https://github.com/UNITES-Lab/moe-quantization) ・ リポジトリ内被引用：8  
  MoEのpost-学習 量子化を体系比較し、エキスパート頻度・ブロック位置・線形層ごとの量子化感度を示すベンチマーク。

- **2025-05 · [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md)**  
  実装：[✓](https://github.com/cat538/MxMoE) ・ リポジトリ内被引用：5  
  エキスパート内部の各線形 ブロックについて、量子化誤差・利用頻度・実GPU実行時間を測り、メモリ予算内で品質と速度のバランスがよいビット幅を割り当てる方式。

- **2025-08 · [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  量子化後も元モデルと近いエキスパートが選ばれるようルータ上位エキスパートの誤差を重点的に補正し、プリフィルでほとんど使われないエキスパートを入力ごとに省く圧縮手法。

- **2025-05 · [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md)**  
  実装：[✓](https://github.com/chenzx921020/MoEQuant) ・ リポジトリ内被引用：3  
  較正時に低頻度エキスパートへも十分な入力例を与え、ルータが強く選ぶトークンほど量子化誤差を重く評価することで、同じ低ビットでも品質を保ちやすくする手法。

- **2024-07 · [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  エキスパートの4／16bit精度とCPU／GPU配置をメモリ予算に応じて切り替え、品質・スループット・容量を調整するサービング方式。

- **2025-03 · [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation（旧題 MoQa）](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  入力データの傾向が変わったとき、エキスパートごとのビット幅と変化に敏感な一部チャネルだけを更新し、モデル全体を量子化し直さずに精度を保つMoE量子化方式。
<!-- survey:auto:end -->
