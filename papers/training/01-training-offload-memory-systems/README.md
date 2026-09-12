# Training Offload / Memory Systems

LLMの学習・追加学習（fine-tuning）では、順伝播で作る活性値（activation）、最適化器が保持する最適化状態（optimizer state）、モデルのパラメータ（parameter）などがGPUメモリへ収まりきらないことがある。

この系統では、それらを**CPUメモリやNVMe SSDへ一時的に逃がし、次に必要になる前にGPUへ戻す**方式に加え、CPU DRAMそのものをモデル状態の正本としてGPUへ必要な層だけを流す方式もまとめる。GPU計算中の非同期I/O、未使用時間を利用したSSD退避、CPUバッファ削減、最適化器更新との重畳、複数I/O経路、層単位のstreamingなどにより、**容量を増やしつつ転送待ちをどこまで隠せるか**が主要な課題になる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2025-11 · [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  テンソルの次回利用時刻と更新場所を見て、GPU・CPU DRAM・NVMeの三階層へ残すか退避するかと先読み時刻を決め、LLM学習の再読込待ちを減らすキャッシュ方式。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-04 · [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)**  
  実装：[✓](https://github.com/ITcarrot/RoundPipe) ・ リポジトリ内被引用：0  
  GPUに層を固定所有させず、空いたGPUへ処理段階を動的に割り当て、実測負荷に応じた不均等分割と転送優先度制御で、民生GPU間のパイプライン待ちを減らす微調整方式。

- **2026-02 · [Horizon-LM: A RAM-Centric Architecture for LLM Training](2026-2602.04816-horizon-lm-a-ram-centric-architecture-for-llm-training.md)**  
  実装：[✓](https://github.com/DLYuanGod/Horizon-LM) ・ リポジトリ内被引用：0  
  CPU DRAMをパラメータ・勾配・最適化状態の正本にし、計算中の層だけをGPUへ流し込んでGPUメモリをモデル全体から切り離す学習方式。ただし性能評価の計算誤りで撤回済み。

- **2025-12 · [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)**  
  実装：[✓](https://github.com/npz7yyk/GreedySnake) ・ リポジトリ内被引用：0  
  層ごとに全マイクロバッチをまとめて処理して重みを再利用し、最適化器更新の一部を次の反復と重ねることで、SSDオフロード学習の再読込と更新待ちを減らす方式。

### 2年前（2024-10〜2025-09）

- **2025-06 · [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  テンソルごとの次回利用までの空き時間を測り、長く不要な重み・勾配・活性値をNVMe SSDへ退避し、先読みをGPU計算に重ねて固定的な層単位方式のI/O待ちを減らす学習方式。

- **2025-05 · [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training/DeepSpeed-ZenFlow) ・ リポジトリ内被引用：2  
  影響の大きい勾配だけをGPUで毎ステップ更新し、残りをCPUで蓄積して遅延更新する二経路に分け、CPUオフロード学習のGPU待ち時間を減らす方式。

- **2025-05 · [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  SSDオフロード時にCPU側で過剰確保する転送バッファや検査用一時領域を必要量へ縮め、余分なRAM消費とNVMeのコピーを減らしてLLM微調整を支える方式。

- **2025-09 · [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)**  
  実装：[✓](https://github.com/DataStates/artifacts/blob/main/MLP-Offload) ・ リポジトリ内被引用：0  
  最適化状態をGPU、CPU DRAM、ローカルNVMe、共有ストレージへ分散し、複数の読み書き経路を同時利用して、LLM事前学習の容量制約とI/O待ちを緩和する方式。

### 3年前（2023-10〜2024-09）

- **2024-03 · [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)**  
  実装：[✓](https://github.com/AIS-SNU/Smart-Infinity) ・ リポジトリ内被引用：7  
  SSD上のパラメータと最適化状態をCPU・GPUへ毎回戻さず、FPGA搭載SmartSSD内でAdam更新を実行して、PCIeを通る状態転送量と学習のI/O待ちを減らす方式。

- **2023-10 · [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)**  
  実装：[✓](https://github.com/platformxlab/G10) ・ リポジトリ内被引用：3  
  テンソルの生存期間と次回利用時刻を実行グラフから求め、GPU・ホストメモリ・SSD間の退避と先読みを自動化して、ページフォルトと転送待ちを減らす学習システム。

- **2024-08 · [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)**  
  実装：[✓](https://github.com/K-Wu/FlashTrain) ・ リポジトリ内被引用：2  
  順伝播で生成した活性値をNVMe SSDへ非同期退避し、逆伝播の直前に先読みして、再計算を減らしながらGPU活性値メモリを空けるLLM学習システム。

- **2024-06 · [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)**  
  実装：[✓](https://github.com/gulang2019/LSP-Offload) ・ リポジトリ内被引用：2  
  大きな勾配・更新行列を低次元表現へ圧縮してCPUへ送り、学習中に圧縮方向を切り替えて更新の偏りを抑え、民生GPUでのLLM微調整のPCIe転送量を減らす方式。

### 5年前（2021-10〜2022-09）

- **2021-11 · [ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning](2021-2104.07857-zero-infinity-breaking-the-gpu-memory-wall-for-extreme-scale-deep-learning.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed) ・ リポジトリ内被引用：30  
  学習パラメータ・勾配・最適化状態をGPU、CPU DRAM、NVMe SSDへ分散し、各SSDの読み込みと先読みをGPU計算に重ねて、GPU総容量を超える巨大モデルを収める方式。
<!-- survey:auto:end -->
