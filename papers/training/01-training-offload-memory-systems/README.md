# Training Offload / Memory Systems

LLMの学習・追加学習（fine-tuning）では、順伝播で作る活性値（activation）、最適化器が保持する最適化状態（optimizer state）、モデルのパラメータ（parameter）などがGPUメモリへ収まりきらないことがある。

この系統では、それらを**CPUメモリやNVMe SSDへ一時的に逃がし、次に必要になる前にGPUへ戻す**方式に加え、CPU DRAMそのものをモデル状態の正本としてGPUへ必要な層だけを流す方式もまとめる。GPU計算中の非同期I/O、未使用時間を利用したSSD退避、CPUバッファ削減、最適化器更新との重畳、複数I/O経路、層単位のstreamingなどにより、**容量を増やしつつ転送待ちをどこまで隠せるか**が主要な課題になる。

## 収録論文

収録論文: 13本。公開日が新しい順。

- 2026-04-29 — [Efficient Training on Multiple Consumer GPUs with RoundPipe](2026-2604.27085-efficient-training-on-multiple-consumer-gpus-with-roundpipe.md)
  - 複数のconsumer GPUへ担当層を固定せず、空いたGPUへ処理段階を順番に割り当てる。層ごとの実測負荷と転送優先度も調整し、GPUの遊休時間とCPU↔GPU転送待ちを減らす。
- 2026-02-04 — [Horizon-LM: A RAM-Centric Architecture for LLM Training](2026-2602.04816-horizon-lm-a-ram-centric-architecture-for-llm-training.md) — **withdrawn**
  - CPU DRAMをパラメータと最適化状態の正本にし、GPUには計算する層だけを順次転送する方式を提案。arXiv v3（2026-04-06）で、実験評価のtraining FLOPs計算に誤りがありthroughput値が不正確だったとして撤回されているため、性能値は確定結果として扱わない。
- 2025-12-19 — [GreedySnake: Accelerating SSD-Offloaded LLM Training with Efficient Scheduling and Optimizer Step Overlapping](2025-2512.17570-greedysnake-accelerating-ssd-offloaded-llm-training-with-efficient-scheduling-an.md)
  - 同じ層の全マイクロバッチ（microbatch）をまとめて処理し、一度SSDから読んだ重みを使い回す。最適化器更新も次の学習反復と重ねて待ち時間を減らす。
- 2025-11-18 — [10Cache: Heterogeneous Resource-Aware Tensor Caching and Migration for LLM Training](2025-2511.14124-10cache-heterogeneous-resource-aware-tensor-caching-and-migration-for-llm-traini.md)
  - GPU・CPU DRAM・NVMeを3段のキャッシュとして扱い、各テンソルが次に必要になる時刻と役割に応じて、どの階層へ残すかを決める。
- 2025-09-02 — [MLP-Offload: Multi-Level, Multi-Path Offloading for LLM Pre-training to Break the GPU Memory Wall](2025-2509.02480-mlp-offload-multi-level-multi-path-offloading-for-llm-pre-training-to-break-the-.md)
  - 巨大な最適化状態をGPU・DRAM・NVMe・並列ファイルシステム（Parallel File System; PFS）へ分散し、ローカルSSDと共有ストレージのI/Oを同時に使う。
- 2025-06-06 — [Cost-Efficient LLM Training with Lifetime-Aware Tensor Offloading via GPUDirect Storage](2025-2506.06472-cost-efficient-llm-training-with-lifetime-aware-tensor-offloading-via-gpudirect-.md)
  - 各テンソルが次に必要になるまでの空き時間を測り、SSDへ往復する時間を十分に確保できるものだけ退避する。GPUダイレクトストレージ（GPUDirect Storage; GDS）でGPUとNVMeを直接転送する。
- 2025-05-29 — [MemAscend: System Memory Optimization for SSD-Offloaded LLM Fine-Tuning](2025-2505.23254-memascend-system-memory-optimization-for-ssd-offloaded-llm-fine-tuning.md)
  - SSDオフロードのためにCPU側へ確保するバッファの無駄や余分なコピーを減らし、system RAM使用量を抑える。任意で低精度の最適化状態も使い、I/O量をさらに削減する。
- 2025-05-18 — [ZenFlow: Enabling Stall-Free Offloading Training via Asynchronous Updates](2025-2505.12242-zenflow-enabling-stall-free-offloading-training-via-asynchronous-updates.md)
  - 学習への影響が大きい勾配（gradient）だけGPUで毎回更新し、残りはCPU側で数stepまとめて更新する。CPU最適化器待ちでGPUが止まる時間を減らす。
- 2024-08-19 — [SSDTrain: An Activation Offloading Framework to SSDs for Faster Large Language Model Training](2024-2408.10013-ssdtrain-an-activation-offloading-framework-to-ssds-for-faster-large-language-mo.md)
  - 順伝播で作った活性値をNVMe SSDへ非同期に退避し、逆伝播で必要になる前に先読みする。活性値をGPUへ保持するためのメモリと、捨てた活性値の再計算を減らす。
- 2024-06-14 — [Practical Offloading for Fine-Tuning LLM on Commodity GPU via Learned Sparse Projectors](2024-2406.10181-practical-offloading-for-fine-tuning-llm-on-commodity-gpu-via-learned-sparse-pro.md)
  - CPUへ送る更新情報を、学習した疎な低次元表現へ圧縮して転送量を減らし、一般向けGPUでのfine-tuningを高速化する。
- 2024-03-11 — [Smart-Infinity: Fast Large Language Model Training using Near-Storage Processing on a Real System](2024-2403.06664-smart-infinity-fast-large-language-model-training-using-near-storage-processing-.md)
  - SSDに置いた最適化状態をCPU/GPUへ毎回運ぶ代わりに、演算機能付きSSD側で最適化器更新を実行し、データ移動量を減らす。
- 2023-10-13 — [G10: Enabling An Efficient Unified GPU Memory and Storage Architecture with Smart Tensor Migrations](2023-2310.09443-g10-enabling-an-efficient-unified-gpu-memory-and-storage-architecture-with-smart.md)
  - 各テンソルがいつ使われ、どれくらい長く不要になるかを実行計画から求め、GPUメモリ・CPUメモリ・ストレージのどこへ置くかと移動時刻を自動で決める。
- 2021-11-13 — [ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning](2021-2104.07857-zero-infinity-breaking-the-gpu-memory-wall-for-extreme-scale-deep-learning.md)
  - parameter・gradient・optimizer stateをGPUだけでなくCPU DRAMとNVMe SSDへ分散し、各nodeのI/Oを並列利用しながら必要なdataを先読みしてGPU計算と重ね、GPU memoryを超える巨大modelを学習できるようにする。
