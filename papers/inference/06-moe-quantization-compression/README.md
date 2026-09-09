# MoE Quantization / Compression

MoEの大部分を占めるexpert重みを**低bit化、pruning、precision切替などで小さくし、VRAM・storage容量・memory bandwidth・計算量を減らす**研究をまとめる。MoEではexpertごとに利用頻度や量子化耐性が違うため、全weightを一律に同じbit幅へ落とすより、expertやlayerごとに精度を変える手法が多い。

単にモデルを小さくするだけでなく、routing結果を崩さないこと、頻繁に使うexpertへ高い精度を残すこと、実際のGPU kernelで速くなるbit配置を選ぶことも重要な評価軸となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

| 論文 | 一文要約 |
|---|---|
| [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md) | KV cacheが増えて空きVRAMが減ったとき、品質への影響が小さいexpert weight部分から段階的にbit幅を下げ、余裕が戻れば高精度へ戻すserving方式。 |
| [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md) | 全layerのexpertを同じmemory budgetの中で比較し、低bit化したとき品質へ効きにくいexpertから強く圧縮したうえで、量子化後のexpert性能に合わせてrouterだけを微調整する手法。 |
| [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md) | 実際のrouting履歴から利用頻度が高いexpertだけを高bitへ切り替え、低頻度expertは低bitのままにして、限られたVRAMを重要expertへ重点配分するruntime方式。 |
| [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md) | expertごとにbit幅を変えて重み容量を減らし、さらにtokenごとに必要なexpert数を学習して、LLM/VLMの保存容量と実行計算量を同時に削る手法。 |
| [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md) | 量子化後も元モデルと近いexpertが選ばれるようrouter上位expertの誤差を重点的に補正し、prefillでほとんど使われないexpertを入力ごとに省く圧縮手法。 |
| [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md) | expert内部の各linear blockについて、量子化誤差・利用頻度・実GPU実行時間を測り、memory予算内で品質と速度のバランスがよいbit幅を割り当てる方式。 |
| [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md) | calibration時に低頻度expertへも十分な入力例を与え、routerが強く選ぶtokenほど量子化誤差を重く評価することで、同じ低bitでも品質を保ちやすくする手法。 |
| [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation（旧題 MoQa）](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md) | 入力データの傾向が変わったとき、expertごとのbit幅と変化に敏感な一部channelだけを更新し、モデル全体を量子化し直さずに精度を保つMoE量子化方式。 |
| [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md) | expertごとにbit幅を変える量子化と、tokenごとに寄与の小さいexpertを実行しない仕組みを組み合わせ、保存容量と実行FLOPsを同時に削減する手法。 |
| [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md) | expertの4／16bit精度とCPU／GPU配置をメモリ予算に応じて切り替え、品質・throughput・容量を調整するserving方式。 |
| [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md) | MoEのpost-training quantizationを体系比較し、expert頻度・block位置・linear層ごとの量子化感度を示すベンチマーク。 |
| [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md) | trillion-parameter級MoEのexpert重みを3値化し、よく現れる値の並びをまとめて圧縮保存し、その圧縮形式を直接読む専用kernelで推論する方式。 |
| [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md) | MoEでparameterの大半を占めるexpert FFNだけを2〜8 bitへ量子化し、attentionやdense FFNなど敏感な共有部は高精度に残す。expert weightはdense FFNより外れ値が少なく低bit化に強いという性質を利用し、model sizeとweight bandwidthを減らす。 |
<!-- survey:auto:end -->
