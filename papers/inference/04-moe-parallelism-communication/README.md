# MoE並列化・通信

この系統では、混合専門家モデル（Mixture of Experts; MoE）の専門家配置、並列化、チップ間・ノード間通信、負荷分散を扱う推論システム研究を整理する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（1本）

| 論文 | 一文要約 |
|---|---|
| [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md) | 低バッチのオンデバイスMoEでは、専門家ごとの活性化トークン数が長い裾を持ち、オンチップ容量不足からDDRへ重みを逃がすため、重み読込・チップレット間負荷不均衡・重複保持が同時にボトルネックになる。本論文のFully Sharded エキスパート Data Parallelism（FSE-DP）は、専門家重みをチップレット間で細かいマイクロスライスに分け、一つの物理コピーを動的な軌跡に沿って流す。高負荷専門家と低負荷専門家を組み合わせ、DDR読込・D2D転送・演算を重ね、軽量ハードウェアスケジューラで実行する。EP/Hydra比で1.22〜2.00倍高速化し、オンチップメモリを最大78.8%削減する。 |
<!-- survey:auto:end -->
