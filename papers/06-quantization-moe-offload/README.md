# Quantization × MoE × Offload

収録論文: 13本。公開日が新しい順。

- 2026-07-17 — [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md)
  - KV cache増加で変動する空きVRAMに合わせ、expert weightをpage／bit-plane単位で低bit化・復元し、品質損失当たりの解放byteを最適化する。
- 2026-05-21 — [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md)
  - 全layer・expertを一つのbit budgetで大域最適化し、量子化後のrouter微調整と段階的低bit化でrouting shiftを補償する。
- 2025-11-19 — [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md)
  - router traceのhotnessに応じてexpertを実行中に高bitへ昇格・低bitへ降格し、versioned residencyでprecision移行を非同期化する。
- 2025-10-13 — [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md)
  - expert別mixed-precision量子化とGumbel-Softmaxによるtoken別Top-any pruningを統合し、MoE-LLM/VLMの重みと活性計算を同時に削る。
- 2025-08-03 — [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md)
  - 量子化後のexpert-shiftをTopK-MSEで校正し、入力系列のexpert頻度に応じた動的pruningを組み合わせてMoEを圧縮する。
- 2025-05-09 — [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md)
  - linear-block単位の量子化感度・routing頻度・GPU kernel時間を共同最適化し、MoEのbit配置と実行速度を両立する方式。
- 2025-05-02 — [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md)
  - expert間の較正不均衡を自己生成データで補い、router affinityを量子化誤差へ反映して低bit品質を回復する手法。
- 2025-03-27 — [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation（旧題 MoQa）](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md)
  - データ分布に応じてexpertのbit群とsalient channelを実行時に切り替え、再較正コストを抑えるMoE量子化方式。
- 2024-10-08 — [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md)
  - expert別mixed-precision量子化とtoken単位の動的pruningを組み合わせ、保存容量と実行FLOPsを同時に削減する手法。
- 2024-07-19 — [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md)
  - expertの4／16bit精度とCPU／GPU配置をメモリ予算に応じて切り替え、品質・throughput・容量を調整するserving方式。
- 2024-06-12 — [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md)
  - MoEのpost-training quantizationを体系比較し、expert頻度・block位置・linear層ごとの量子化感度を示すベンチマーク。
- 2023-10-25 — [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md)
  - trillion-parameter級MoEのexpert重みを専用形式とkernelでsub-1-bitまで圧縮し、実用的な推論を可能にする方式。
- 2023-10-03 — [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md)
  - MoEのexpert FFNだけを低bit化し、共有部を高精度に保つことでメモリ削減と量子化耐性を両立する基準手法。
