# MoE並列化・通信

この系統では、混合専門家モデル（Mixture of Experts; MoE）の専門家配置、並列化、チップ間・ノード間通信、負荷分散を扱う推論システム研究を整理する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（3本）

| 論文 | 一文要約 |
|---|---|
| [HetRoute: Heterogeneous and Cost-aware Collaborative Routing Framework for Distributed Edge MoE Inference](2026-2608.00577-hetroute-collaborative-routing.md) | 地理的に分散した異種エッジサーバで混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、各トークンが選んだ複数の専門家をどのサーバへ送るかで、ネットワーク転送、GPUとCPU間の専門家読み込み、GPU計算待ち、量子化による品質損失が同時に絡む。HetRouteは、これらを一つの費用モデルで評価し、事前段階では専門家の配置・GPU常駐・複製精度を決め、実行時には上位k個の専門家を個別ではなく集合として割り当てる。10台の異種エッジサーバによるトレース駆動評価では、Mixtral-8x7Bの代表条件で平均遅延156ms、P99遅延286ms、通信量1.24GB/1000トークン、スループット1490トークン/秒を報告し、品質低下を設定予算内に抑えた。 |
| [DWDP: Distributed Weight Data Parallelism for High-Performance LLM Inference on NVL72](2026-2604.01621-dwdp-distributed-weight-data-parallelism.md) | 大規模な混合専門家モデル（Mixture of エキスパート; MoE）を複数GPUで推論すると、従来の専門家並列では各層の全対全通信と同期のため、入力長や専門家選択が偏ったとき速いGPUまで遅いGPUを待つ。DWDPは注意機構の重みを各GPUへ複製し、MoEの専門家重みだけを同一NVLinkドメイン内のGPUへ分散配置する。各GPUは次層で不足する専門家重みを非同期に先読みし、集団通信を使わず自分に必要な転送が終わり次第独立に進む。GB200 NVL72上のDeepSeek-R1で、20〜100 TPS/userのサービス範囲において同等の利用者当たり生成速度でGPU当たり出力スループットを平均8.8%改善する。 |
| [Expert Streaming: Accelerating Low-Batch MoE Inference via Multi-chiplet Architecture and Dynamic Expert Trajectory Scheduling](2026-2603.27624-expert-streaming-multichiplet-dynamic-trajectories.md) | 低バッチのオンデバイスMoEでは、専門家ごとの活性化トークン数が長い裾を持ち、オンチップ容量不足からDDRへ重みを逃がすため、重み読込・チップレット間負荷不均衡・重複保持が同時にボトルネックになる。本論文のFully Sharded エキスパート Data Parallelism（FSE-DP）は、専門家重みをチップレット間で細かいマイクロスライスに分け、一つの物理コピーを動的な軌跡に沿って流す。高負荷専門家と低負荷専門家を組み合わせ、DDR読込・D2D転送・演算を重ね、軽量ハードウェアスケジューラで実行する。EP/Hydra比で1.22〜2.00倍高速化し、オンチップメモリを最大78.8%削減する。 |
<!-- survey:auto:end -->
