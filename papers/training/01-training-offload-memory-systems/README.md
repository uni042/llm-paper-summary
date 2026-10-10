# Training Offload / Memory Systems

LLMの学習・追加学習（fine-tuning）では、順伝播で作る活性値（activation）、最適化器が保持する最適化状態（optimizer state）、モデルのパラメータ（parameter）などがGPUメモリへ収まりきらないことがある。

この系統では、それらを**CPUメモリやNVMe SSDへ一時的に逃がし、次に必要になる前にGPUへ戻す**方式に加え、CPU DRAMそのものをモデル状態の正本としてGPUへ必要な層だけを流す方式もまとめる。GPU計算中の非同期I/O、未使用時間を利用したSSD退避、CPUバッファ削減、最適化器更新との重畳、複数I/O経路、層単位のstreamingなどにより、**容量を増やしつつ転送待ちをどこまで隠せるか**が主要な課題になる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2025-11 · [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)**  
  実装：[✓](https://github.com/Sabiha1225/10cache) ・ リポジトリ内被引用：1  
  10Cacheは、LLMを単一GPUで学習するときに不足するGPUメモリを、CPU主記憶とNVMeストレージで補いながら、テンソルの移動待ちを抑える仕組みである。従来のオフロード方式では、モデルの重み、勾配、最適化状態をGPUから外へ移して容量制限を緩和するが、必要になる直前まで低速階層に置いたままだとGPUが読み戻しを待ち、計算器が遊休する。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-04 · [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)**  
  実装：[✓](https://github.com/thustorage/RoundPipe) ・ リポジトリ内被引用：0  
  GPUに層を固定所有させず、空いたGPUへ処理段階を動的に割り当て、実測負荷に応じた不均等分割と転送優先度制御で、民生GPU間のパイプライン待ちを減らす微調整方式。

- **2026-02 · [Horizon-LM: A RAM-Centric Architecture for LLM Training](2026-2602.04816-horizon-lm-a-ram-centric-architecture-for-llm-training.md)**  
  実装：[✓](https://github.com/DLYuanGod/Horizon-LM) ・ リポジトリ内被引用：0  
  従来のGPU中心学習では、ZeRO-3やFSDPでパラメータを分割・退避しても、GPU側にモデルの実行構造と自動微分の計算グラフが残り、実行基盤のバッファや勾配管理がメモリ消費を増やす。

- **2025-12 · [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同一層の重みを複数マイクロバッチ間で再利用し、層間活性値の転送増加と引き換えに重み・勾配の反復転送を抑える。さらに最適化器の一部を次の学習反復へ遅延させ、計算とSSD入出力の重畳範囲を広げる。

### 2年前（2024-11〜2025-10）

- **2025-06 · [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  テンソルごとの次回利用までの空き時間を測り、長く不要な重み・勾配・活性値をNVMe SSDへ退避し、先読みをGPU計算に重ねて固定的な層単位方式のI/O待ちを減らす学習方式。

- **2025-09 · [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)**  
  実装：[✓](https://github.com/DataStates/artifacts/blob/main/MLP-Offload) ・ リポジトリ内被引用：2  
  最適化状態をGPU、CPU DRAM、ローカルNVMe、共有ストレージへ分散し、複数の読み書き経路を同時利用して、LLM事前学習の容量制約とI/O待ちを緩和する方式。

- **2025-05 · [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeedExamples/tree/master/training/DeepSpeed-ZenFlow) ・ リポジトリ内被引用：2  
  GPU容量を超える場合、ZeRO-Offloadなどは勾配や最適化器状態をCPUメモリへ移し、CPU側で更新してからGPUへ戻す。低重要度勾配を単純に捨てる方式ではなく、更新の頻度と実行場所を変える方式である。論文の主要評価ではZeRO-Offloadに対する学習処理率が平均4.3倍、ZeRO-Infinityに対して平均6.3倍になった。

- **2025-05 · [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  大規模言語モデルを微調整する際、モデル重み・勾配・最適化器状態をNVMe SSDへ退避すると、GPUの専用メモリ容量を超える学習が可能になる。論文はZeRO-Infinity系の比較でピークシステムメモリを平均55.7%削減し、128GiB RAMの構成で扱える文脈長を16,384から131,072へ、あるいはバッチを4から32へ増やせる条件を報告する。

### 3年前（2023-11〜2024-10）

- **2024-03 · [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)**  
  実装：[✓](https://github.com/AIS-SNU/Smart-Infinity) ・ リポジトリ内被引用：14  
  SSD上のパラメータと最適化状態をCPU・GPUへ毎回戻さず、FPGA搭載SmartSSD内でAdam更新を実行して、PCIeを通る状態転送量と学習のI/O待ちを減らす方式。

- **2024-08 · [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)**  
  実装：[✓](https://github.com/K-Wu/FlashTrain) ・ リポジトリ内被引用：2  
  モデルのパラメータや最適化状態だけでなく活性値がGPUメモリの大きな割合を占めるため、メモリが足りないとマイクロバッチを小さくするか、一部の活性値を捨てて逆伝播時に再計算する必要がある。SSDTrainは、活性値を捨てる代わりに高帯域のNVMe SSDへ一時保存し、逆伝播で必要になる前にGPUへ戻す方式である。

- **2024-06 · [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)**  
  実装：[✓](https://github.com/gulang2019/LSP-Offload) ・ リポジトリ内被引用：2  
  特徴は、単に固定の低ランク更新を使うのではなく、射影器の非零位置と係数を少量のデータで学習し、勾配の推定誤差が大きくなった場合に部分空間を更新することである。原論文は4GBのノートPC GPUで13億パラメータ級、24GBのRTX 4090で67億パラメータ級の微調整を示す。

### 4年前（2022-11〜2023-10）

- **2023-10 · [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)**  
  実装：[✓](https://github.com/platformxlab/G10) ・ リポジトリ内被引用：4  
  G10が扱う問題は、深層学習の一反復で保持する全テンソルの容量がGPU搭載メモリを超えても、各演算器がその瞬間に使うテンソルの集合はずっと小さい、という差をどう利用するかである。SSDの容量が十分でも帯域と遅延はGPUメモリと大きく異なるため、無計画な退避は処理率を落とす。

### 5年前（2021-11〜2022-10）

- **2021-11 · [ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning](2021-2104.07857-zero-infinity-breaking-the-gpu-memory-wall-for-extreme-scale-deep-learning.md)**  
  実装：[✓](https://github.com/deepspeedai/DeepSpeed) ・ リポジトリ内被引用：49  
  学習パラメータ・勾配・最適化状態をGPU、CPU DRAM、NVMe SSDへ分散し、各SSDの読み込みと先読みをGPU計算に重ねて、GPU総容量を超える巨大モデルを収める方式。

### 7年前（2019-11〜2020-10）

- **2020-05 · [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](2019-1910.02054-zero.md)**  
  実装：[✓](https://github.com/microsoft/DeepSpeed) ・ リポジトリ内被引用：56  
  データ並列で重複する最適化器状態・勾配・パラメータをGPU間分割し、必要時だけ通信することで、モデル並列の細粒度通信を避けつつ巨大モデル学習のメモリ効率を高める基盤方式。
<!-- survey:auto:end -->
