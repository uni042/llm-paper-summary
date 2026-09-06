# MoE Quantization / Compression

MoEの大部分を占めるexpert重みを**低bit化、pruning、precision切替などで小さくし、VRAM・storage容量・memory bandwidth・計算量を減らす**研究をまとめる。MoEではexpertごとに利用頻度や量子化耐性が違うため、全weightを一律に同じbit幅へ落とすより、expertやlayerごとに精度を変える手法が多い。

単にモデルを小さくするだけでなく、routing結果を崩さないこと、頻繁に使うexpertへ高い精度を残すこと、実際のGPU kernelで速くなるbit配置を選ぶことも重要な評価軸となる。

## 収録論文

収録論文: 13本。公開日が新しい順。

- 2026-07-17 — [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md)
  - KV cacheが増えて空きVRAMが減るたびに、expert重みの一部を段階的に低bit化し、品質への影響が小さい部分からメモリを空ける。
- 2026-05-21 — [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md)
  - モデル全体を一つのmemory budgetとして扱い、layer・expertごとに異なるbit幅を割り当てたうえでroutingのずれを補正する。
- 2025-11-19 — [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md)
  - よく使われるexpertは高精度、使われないexpertは低精度へ実行中に切り替え、限られたVRAMを利用頻度に応じて配分する。
- 2025-10-13 — [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md)
  - expertごとのbit幅とtokenごとに実行するexpert数をまとめて最適化し、重み容量と推論計算量を同時に減らす。
- 2025-08-03 — [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md)
  - 量子化後も元と近いexpertが選ばれるように補正し、さらに入力ごとのexpert利用頻度を使って不要なexpert計算を減らす。
- 2025-05-09 — [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md)
  - 重みblockごとの精度への影響、expertの利用頻度、実際のGPU実行時間を合わせて見て、速さと品質を両立するbit幅を選ぶ。
- 2025-05-02 — [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md)
  - calibration時に一部expertだけへデータが偏らないようにし、routerが重要と判断するexpertほど量子化誤差を小さくする。
- 2025-03-27 — [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation（旧題 MoQa）](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md)
  - 入力データの傾向に合わせて一部weightのbit幅を実行時に切り替え、datasetが変わっても毎回大がかりな再calibrationをせずに精度を保つ。
- 2024-10-08 — [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)
  - expertごとに異なるbit幅を使い、さらにtokenごとに不要なexpertを減らして、保存容量と実行計算量の両方を削る。
- 2024-07-19 — [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md)
  - expertを4bit / 16bitのどちらで持つか、CPU / GPUのどちらへ置くかをmemory budgetに合わせて選び、品質と速度を調整する。
- 2024-06-12 — [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)
  - MoEの量子化方法を体系的に比較し、どのexpert・layer・linear部分が低bit化に弱いかを整理したbenchmark。
- 2023-10-25 — [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md)
  - expert重みを平均1bit未満まで圧縮する専用表現と計算kernelを作り、trillion-parameter級MoEを現実的なmemory量で推論する。
- 2023-10-03 — [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md)
  - MoEのexpert FFNを重点的に低bit化し、共有部分は高精度で残すことで、容量削減と品質維持を両立する。
