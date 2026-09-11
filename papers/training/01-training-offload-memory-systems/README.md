# Training Offload / Memory Systems

LLMの学習・追加学習（fine-tuning）では、順伝播で作る活性値（activation）、最適化器が保持する最適化状態（optimizer state）、モデルのパラメータ（parameter）などがGPUメモリへ収まりきらないことがある。

この系統では、それらを**CPUメモリやNVMe SSDへ一時的に逃がし、次に必要になる前にGPUへ戻す**方式に加え、CPU DRAMそのものをモデル状態の正本としてGPUへ必要な層だけを流す方式もまとめる。GPU計算中の非同期I/O、未使用時間を利用したSSD退避、CPUバッファ削減、最適化器更新との重畳、複数I/O経路、層単位のstreamingなどにより、**容量を増やしつつ転送待ちをどこまで隠せるか**が主要な課題になる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPU・CPU DRAM・NVMeを3段のキャッシュとして使い、各テンソル（テンソル）が次に必要になる時刻と役割に応じて、どの階層へ残すか・いつ先読みするかを決める学習システム。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-04 · [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)**  
  実装：[✓](https://github.com/ITcarrot/RoundPipe) ・ リポジトリ内被引用：0  
  各GPUに特定の層（層）を固定せず、空いたGPUへ処理段階を順番に割り当て、実測負荷に合わせた不均等分割と転送優先度制御で民生GPU学習の待ち時間を減らす。

- **2026-02 · [Horizon-LM: A RAM-Centric Architecture for LLM Training](2026-2602.04816-horizon-lm-a-ram-centric-architecture-for-llm-training.md)**  
  実装：[✓](https://github.com/DLYuanGod/Horizon-LM) ・ リポジトリ内被引用：0  
  状態: 撤回済み（withdrawn） — arXiv v3（2026-04-06）で著者が撤回。実験評価の学習FLOPs計算で 12HL 項を落としており、スループット値に系統的な計算誤りがあったことが理由。以下の性能値は撤回前原稿が報告した値であり、確定した性能比較として扱わない。

- **2025-12 · [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)**  
  実装：[✓](https://github.com/npz7yyk/GreedySnake) ・ リポジトリ内被引用：0  
  同じ層（層）の全マイクロバッチ（microbatch）をまとめて処理して重みのSSD再読込を減らし、最適化器更新（optimizer step）の一部を次の学習反復と重ねることでI/O待ちを減らす方式。

### 1年以上前

- **2021-11 · [ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning](2021-2104.07857-zero-infinity-breaking-the-gpu-memory-wall-for-extreme-scale-deep-learning.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed) ・ リポジトリ内被引用：30  
  学習用のパラメータ・勾配・オプティマイザ状態をGPUだけでなくCPU DRAMとNVMe SSDへ分割配置し、各nodeのSSD読込を並列化しながら必要なstateを先読みしてGPU計算と重ねることで、GPU メモリ総量を超える巨大モデルを学習可能にするシステム。

- **2024-03 · [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)**  
  実装：[✓](https://github.com/AIS-SNU/Smart-Infinity) ・ リポジトリ内被引用：7  
  SSDに置いたパラメータとoptimizer用の更新状態をCPU/GPUへ毎回読み戻さず、FPGA付きSmartSSDの中でAdam更新まで済ませ、PCIeを通るdata量を減らす学習 システム。

- **2023-10 · [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)**  
  実装：[✓](https://github.com/platformxlab/G10) ・ リポジトリ内被引用：3  
  GPU メモリとホスト メモリ・ストレージを統合し、テンソルの生存期間と再利用を基に階層間migrationを自動化する学習システム。

- **2025-06 · [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  各テンソル（テンソル）がGPU上で次に必要になるまでの空き時間を測り、長く使わないデータをNVMe SSDへ退避・先読みして、SSD入出力をGPU計算の裏へ隠す学習方式。

- **2025-05 · [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training/DeepSpeed-ZenFlow) ・ リポジトリ内被引用：2  
  学習への影響が大きい勾配（勾配）だけをGPUで毎回更新し、残りをCPU側で非同期に蓄積・更新することで、CPUオフロード学習のGPU待ち時間を減らす方式。

- **2025-05 · [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SSDへモデル状態を退避するLLM 微調整で、CPU側バッファの無駄・一時メモリ増加・NVMe入出力の余分なコピーを減らし、システム RAM容量と学習速度を改善する方式。

- **2024-08 · [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)**  
  実装：[✓](https://github.com/K-Wu/FlashTrain) ・ リポジトリ内被引用：2  
  順伝播で作った活性値（活性値）をNVMe SSDへ非同期に退避し、逆伝播で必要になる直前に先読みすることで、GPUメモリ使用量と再計算を減らす学習システム。

- **2024-06 · [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)**  
  実装：[✓](https://github.com/gulang2019/LSP-Offload) ・ リポジトリ内被引用：2  
  full-size 勾配 / optimizer updateをCPUへ送る代わりに、小さい低次元表現へ圧縮して転送し、その圧縮方向を学習中に切り替えることで、PCIe trafficを減らしながら民生GPUでLLM 微調整する方式。

- **2025-09 · [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)**  
  実装：[✓](https://github.com/DataStates/artifacts/blob/main/MLP-Offload) ・ リポジトリ内被引用：0  
  巨大な最適化状態（オプティマイザ状態）をGPU・CPU DRAM・ローカルNVMe・共有ストレージへ分散し、複数の入出力経路を同時に使うことでLLM事前学習のI/O待ちを減らす方式。
<!-- survey:auto:end -->
