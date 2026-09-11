# MoE Quantization / Compression

MoEの大部分を占めるexpert重みを**低bit化、pruning、precision切替などで小さくし、VRAM・storage容量・memory bandwidth・計算量を減らす**研究をまとめる。MoEではexpertごとに利用頻度や量子化耐性が違うため、全weightを一律に同じbit幅へ落とすより、expertやlayerごとに精度を変える手法が多い。

単にモデルを小さくするだけでなく、routing結果を崩さないこと、頻繁に使うexpertへ高い精度を残すこと、実際のGPU kernelで速くなるbit配置を選ぶことも重要な評価軸となる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-11 | [Dynamic Expert Quantization for Scalable Mixture-of-Experts Inference](2025-2511.15015-dynamic-expert-quantization-for-scalable-mixture-of-experts-inference.md) | [✓](https://github.com/kexinchu/DynaQuant) | 2 | DynaExqは、エキスパート 精度を起動時に固定せず、実際のルーティング履歴から頻繁に使われるようになったエキスパートだけ高精度へ昇格する実行時量子化システムである。 |
| 2026-07 | [PagedWeight: Efficient MoE LLM Serving with Dynamic Quality-Aware Weight Quantization](2026-2607.16184-pagedweight-efficient-moe-llm-serving-with-dynamic-quality-aware-weight-quantiza.md) | ✓ | 1 | PagedWeightは、長文サービングでKV キャッシュが増えるたびにエキスパート 重みへ使えるVRAMが減る問題を、同じエキスパートの精度を実行中に上下させることで解く。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-05 | [GEMQ: Global Expert-Level Mixed-Precision Quantization for MoE LLMs](2026-2605.23078-gemq-global-expert-level-mixed-precision-quantization-for-moe-llms.md) | [✓](https://github.com/jndeng/GEMQ) | 0 | GEMQは、層ごとに独立してビットを配るのではなく、モデル全体の全エキスパートを一つのビット 予算で比較する混合精度量子化である。 |
| 2025-10 | [MC#: Mixture Compressor for Mixture-of-Experts Large Models](2025-2510.10962-mc-mixture-compressor-for-mixture-of-experts-large-models.md) | [✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) | 0 | MC#はMC-MoEの拡張版で、保存重みの圧縮とトークンごとのactive エキスパート削減をLLMだけでなくVLMにも広げた。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2023-10 | [Mixture of Quantized Experts (MoQE): Complementary Effect of Low-bit Quantization and Robustness](2023-2310.02410-mixture-of-quantized-experts-moqe-complementary-effect-of-low-bit-quantization-a.md) | ✓ | 14 | 混合エキスパート（Mixture-of-エキスパート: MoE）は、たとえば32個のFFN エキスパートを用意しても、1 トークンではルータが選んだ1個だけを計算できる。 |
| 2023-10 | [QMoE: Practical Sub-1-Bit Compression of Trillion-Parameter Models](2023-2310.16795-qmoe-practical-sub-1-bit-compression-of-trillion-parameter-models.md) | [✓](https://github.com/IST-DASLab/qmoe) | 10 | QMoEは、MoEの「計算は疎だが重みは巨大」という問題を、再学習なしのデータ依存量子化と実行系の同時設計で解く圧縮・推論フレームワークである。 |
| 2024-10 | [Mixture Compressor for Mixture-of-Experts LLMs Gains More](2024-2410.06270-mixture-compressor-for-mixture-of-experts-llms-gains-more.md) | [✓](https://github.com/Aaronhuang-778/Mixture-Compressor-MoE) | 9 | MC-MoEは、保存しておく全エキスパート重みの容量と、推論時に実際に動かすエキスパート数を別々に減らす二段構成である。 |
| 2024-06 | [Examining Post-Training Quantization for Mixture-of-Experts: A Benchmark](2024-2406.08155-examining-post-training-quantization-for-mixture-of-experts-a-benchmark.md) | [✓](https://github.com/UNITES-Lab/moe-quantization) | 8 | この研究の差分は、量子化方式を一つ発明することより、同一平均ビットで「頻度・ブロック位置・線形層」のどれを高ビット化すると有利かを分離したことにある。 |
| 2025-05 | [MxMoE: Mixed-precision Quantization for MoE with Accuracy and Performance Co-Design](2025-2505.05799-mxmoe-mixed-precision-quantization-for-moe-with-accuracy-and-performance-co-desi.md) | [✓](https://github.com/cat538/MxMoE) | 5 | MxMoEは、混合精度量子化を 「品質が壊れにくいビット配置」だけでなく「GPU上で本当に速いビット配置」まで含めて決める 手法である。 |
| 2025-08 | [EAC-MoE: Expert-Selection Aware Compressor for Mixture-of-Experts Large Language Models](2025-eac-moe-expert-selection-aware-compressor-for-mixture-of-experts-large-language-.md) | ✓ | 3 | EAC-MoEは、量子化誤差を「エキスパートの出力値が少しずれる」だけでなく、そのずれによって次のルータが別エキスパートを選んでしまうことまで含めて扱う。 |
| 2025-05 | [MoEQuant: Enhancing Quantization for Mixture-of-Experts Large Language Models via Expert-Balanced Sampling and Affinity Guidance](2025-2505.03804-moequant-enhancing-quantization-for-mixture-of-experts-large-language-models-via.md) | [✓](https://github.com/chenzx921020/MoEQuant) | 3 | MoEQuantはエキスパートごとにビット幅を変える手法ではない。同じ4 ビットや3 ビットで量子化するときに、較正 データの偏りとルータが各トークンをどの強さでエキスパートへ送ったかを量子化計算へ反映し、品質を回復する研究である。 |
| 2024-07 | [Mixture of Experts with Mixture of Precisions for Tuning Quality of Service](2024-2407.14417-mixture-of-experts-with-mixture-of-precisions-for-tuning-quality-of-service.md) | ✓ | 3 | 本研究の価値は、エキスパートの意味的重要度を学習することではなく、変動するGPUメモリを前提に精度・配置・転送を一つのサービス設定として扱う点にある。 |
| 2025-03 | [DynaMo: Runtime Switchable Quantization for MoE with Cross-Dataset Adaptation（旧題 MoQa）](2025-2503.21135-dynamo-runtime-switchable-quantization-for-moe-with-cross-dataset-adaptation-moq.md) | ✓ | 1 | DynaMoは、データセットが変わると重要エキスパートも変わることを前提にした混合精度量子化である。 |
<!-- survey:auto:end -->
