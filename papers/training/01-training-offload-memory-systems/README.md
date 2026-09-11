# Training Offload / Memory Systems

LLMの学習・追加学習（fine-tuning）では、順伝播で作る活性値（activation）、最適化器が保持する最適化状態（optimizer state）、モデルのパラメータ（parameter）などがGPUメモリへ収まりきらないことがある。

この系統では、それらを**CPUメモリやNVMe SSDへ一時的に逃がし、次に必要になる前にGPUへ戻す**方式に加え、CPU DRAMそのものをモデル状態の正本としてGPUへ必要な層だけを流す方式もまとめる。GPU計算中の非同期I/O、未使用時間を利用したSSD退避、CPUバッファ削減、最適化器更新との重畳、複数I/O経路、層単位のstreamingなどにより、**容量を増やしつつ転送待ちをどこまで隠せるか**が主要な課題になる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2025-11 | [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md) | ✓ | 1 | 10Cacheは、単一GPUで大きなLLMを学習するとき、GPU・CPU DRAM・NVMe SSDを単なる「上から順にあふれたデータを置く場所」としてではなく、速度と容量が異なる3段のキャッシュ（キャッシュ）として扱う。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-04 | [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md) | [✓](https://github.com/ITcarrot/RoundPipe) | 0 | RoundPipeは、24GB級の民生GPUを複数枚使ってLLMを微調整するとき、パイプライン並列（パイプライン parallelism）で特定のGPUだけが重い処理を担当し続けるため全体が待たされる問題を扱う。 |
| 2026-02 | [Horizon-LM: A RAM-Centric Architecture for LLM Training](2026-2602.04816-horizon-lm-a-ram-centric-architecture-for-llm-training.md) | [✓](https://github.com/DLYuanGod/Horizon-LM) | 0 | 状態: 撤回済み（withdrawn） — arXiv v3（2026-04-06）で著者が撤回。実験評価の学習FLOPs計算で 12HL 項を落としており、スループット値に系統的な計算誤りがあったことが理由。以下の性能値は撤回前原稿が報告した値であり、確定した性能比較として扱わない。 |
| 2025-12 | [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md) | [✓](https://github.com/npz7yyk/GreedySnake) | 0 | GreedySnakeは、パラメータ（パラメータ）・最適化状態（オプティマイザ状態）・活性値（活性値）をNVMe SSDへ退避するLLM学習で、同じ層の重みを小分けデータごとに何度もSSDから読み直す無駄を減らすシステムである。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2021-11 | [ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning](2021-2104.07857-zero-infinity-breaking-the-gpu-memory-wall-for-extreme-scale-deep-learning.md) | [✓](https://github.com/deepspeedai/DeepSpeed) | 29 | ZeRO-InfinityはZeRO-3を基盤に、学習中に保持する モデルパラメータ 勾配 オプティマイザ状態 の保存先をGPU HBMだけでなく、CPU DRAMと通常のNVMe SSDまで広げる。 |
| 2024-03 | [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md) | [✓](https://github.com/AIS-SNU/Smart-Infinity) | 7 | Smart-Infinityは、ZeRO-InfinityのようなSSD-offloaded 学習で、パラメータだけでなくAdamのモーメンタム / 分散など、学習更新のために保持する大きな状態を毎step SSDからCPU/GPUへ読み戻すコストを扱う。これらをまとめてオプティマイザ状態と呼ぶ。論文のGPT-2 8.4B分析では。 |
| 2023-10 | [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md) | [✓](https://github.com/platformxlab/G10) | 3 | G10はGPUの限られたHBMをホスト DRAMとflash SSDで透過的に拡張し、DNN学習中のテンソルを先回りして移動する統合GPU メモリ/ストレージ構成である。GPUメモリに収まらない全モデルを毎回ページフォルトでSSDから読むのではなく、コンパイラが実行グラフからテンソルのサイズ、依存関係、active期間、次回使用時刻を抽出し。 |
| 2025-06 | [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md) | ✓ | 2 | TERAIOは、LLM学習中のテンソルを「重みだからCPUへ」「活性値だからSSDへ」のように種類だけで決め打ちせず、そのテンソルが次に使われるまでGPU上で不要になる時間を見て退避先を決める方式である。 |
| 2025-05 | [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md) | [✓](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training/DeepSpeed-ZenFlow) | 2 | ZenFlowは、ZeRO-Offloadのようにモデル更新に使う状態をCPUへ逃がす学習方式で、GPUがCPU側の更新完了を待つ時間を減らす研究である。 |
| 2025-05 | [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md) | ✓ | 2 | MemAscendは、SSDオフロード（SSD オフロード）そのものではなく、SSDへデータを逃がすためにCPU側で確保する一時メモリが大量のRAMを浪費する問題を扱う。 |
| 2024-08 | [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md) | [✓](https://github.com/K-Wu/FlashTrain) | 2 | SSDTrainは、LLM学習の順伝播（順伝播）で生成され、逆伝播（逆伝播）でもう一度使う中間計算結果＝活性値（活性値）を、GPUメモリへ置き続ける代わりにNVMe SSDへ一時退避するシステムである。 |
| 2024-06 | [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md) | [✓](https://github.com/gulang2019/LSP-Offload) | 2 | LSP-Offloadは、24 GB級の民生GPUでLLM 微調整を行うため、各層の大きな勾配 / 更新行列をそのままCPUへ送らず、より小さい低次元表現へ変換してからオフロードする方式である。 |
| 2025-09 | [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md) | [✓](https://github.com/DataStates/artifacts/blob/main/MLP-Offload) | 0 | MLP-Offloadは、LLM事前学習（pre-学習）で巨大になる最適化状態（オプティマイザ状態）を、GPUだけに置かず複数の記憶装置へ分散する学習システムである。 |
<!-- survey:auto:end -->
