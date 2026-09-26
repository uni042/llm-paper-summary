# 推論システム研究

収録論文: **1080本**。

推論・serving・decoding・実行時memory / I/O・on-device実行など、**modelを使って出力を生成する段階の効率化**を目的とする研究を収録する。

分類は手法内部の実装ではなく最終目的で決める。推論高速化のために予測器の学習、蒸留、追加学習、calibrationなどを使う場合も推論側に置く。

## 主な系統

以下は主要系統の説明。正確な系統一覧と本数は下の自動生成表を正本とする。

- [Offload / Hierarchical Memory](01-offload-hierarchical-memory/) — model weightやMoE expertをCPU・peer GPU・SSD / Flash等へ置き、転送・計算を協調させてGPU memory不足を補う。
- [Adaptive Expert Computation / Compression](02-adaptive-expert-computation-compression/) — tokenやlayerごとに実行expert数を変えたりexpertを統合・代替したりして、MoEの計算・転送・容量を減らす。
- [Expert Prefetch](03-expert-prefetch/) — 将来使うexpertをrouting確定前に予測し、GPU cacheの保持や先読みを制御してweight転送待ち・転送量を減らす。
- [Conditional Computation](04-conditional-computation/) — layer skipping、early exit、token pruning等で入力に応じて不要なTransformer計算を実行しない。
- [Speculative Decoding / MoE](05-speculative-decoding-moe/) — draft候補を並列生成・検証して1回のtarget実行で複数tokenを確定し、MoEではexpert読込・検証costも抑える。
- [MoE Quantization / Compression](06-moe-quantization-compression/) — expert weightを低bit化・pruning・mixed precision等で小さくし、VRAM・bandwidth・計算量を削減する。
- [KV Cache Optimization / Compression](07-kv-cache-optimization-compression/) — KV cacheを圧縮・選別・動的配分・GPU内prefetchして、容量とmemory bandwidthの負荷を減らす。
- [Edge / On-device LLM Systems](08-edge-on-device-llm-systems/) — smartphoneや個人PCなど、memory・bandwidth・電力制約の厳しい端末でLLMを実行するsystem研究。
- [KV Cache Offload / Recomputation](10-kv-cache-offload-recomputation/) — KVをCPU・peer GPU・SSD等へ置き、必要な転送・attention実行場所・再計算を最適化する。
- [LLM Serving / Scheduling / Disaggregation](11-llm-serving-scheduling-disaggregation/) — request順、batch、prefill / decode分離、KV再利用・移動、GPU配置を調整してserving効率とlatencyを改善する。
- [Kernel / Runtime Compilation](09-kernel-runtime-compilation/) — GPUカーネル生成・融合・JIT・メガカーネル等でLLM推論の演算実装そのものを最適化する。
- [MoE Parallelism / Communication](12-moe-parallelism-communication/) — expert parallelism、all-to-all通信、分散expert配置、負荷分散を共同最適化する。
- [Sparse Attention](13-sparse-attention/) — 注意対象token・block・pageを疎に選択し、長文脈attentionの計算量と帯域を削減する。
- [Agentic Inference / Serving Runtime](14-agentic-inference-serving-runtime/) — ツール呼出し、長寿命セッション、複数LLM・複数エージェントのワークフロー、長い待機時間と再入場を前提に、エージェント推論の資源・状態・GPU配置・KV再利用を最適化するシステム研究をまとめる。
- [Inference Simulation / Emulation](15-inference-simulation-emulation/) — LLM推論・サービング基盤を実GPU実行の代わりに離散事象、仮想時間、プロファイル標本化、カーネル性能モデルなどで再現し、構成探索や性能評価を高速化する研究をまとめる。
- [Weight Quantization / Compression](16-weight-quantization-compression/) — 一般LLMの重み表現を低ビット量子化、ベクトル量子化、疎量子化、無損失符号化などで小さくし、モデル品質を保ちながら重み容量・帯域・演算費用を削減する研究をまとめる。
- [PIM / Near-Data Acceleration](17-pim-near-data-acceleration/) — メモリ内処理（PIM）、メモリ近傍処理、ストレージ内処理（in-storage）、計算機能を持つHBM/NAND/DIMMなどへLLM演算を寄せ、データ移動そのものを減らす推論アクセラレーション研究をまとめる。
- [Pipeline-Native CPU Inference](18-pipeline-native-cpu-inference/) — CPU向け単一トークン推論でモデル依存構造と重み配置・実行スケジュールを共同設計する研究をまとめる。
- [Inference Benchmarking / Workload Diagnosis](19-inference-evaluation-benchmarking/) — LLM推論・サービングのベンチマーク、トレース選定・再生、ボトルネック診断、測定方法を設計し、少ない実行で信頼できる性能評価を行う研究をまとめる。
- [Other Inference Systems](99-other-inference-systems/) — 推論効率化が主目的だが、まだ独立lineageを作るほど同種研究が集まっていない手法を置く。

<!-- survey:auto:start -->
## 自動生成の収録状況

推論論文：**1080本**。

| 系統 | 本数 |
|---|---:|
| [01-offload-hierarchical-memory](01-offload-hierarchical-memory/README.md) | 108 |
| [02-adaptive-expert-computation-compression](02-adaptive-expert-computation-compression/README.md) | 100 |
| [03-expert-prefetch](03-expert-prefetch/README.md) | 15 |
| [04-conditional-computation](04-conditional-computation/README.md) | 9 |
| [05-speculative-decoding-moe](05-speculative-decoding-moe/README.md) | 58 |
| [06-moe-quantization-compression](06-moe-quantization-compression/README.md) | 15 |
| [07-kv-cache-optimization-compression](07-kv-cache-optimization-compression/README.md) | 101 |
| [08-edge-on-device-llm-systems](08-edge-on-device-llm-systems/README.md) | 23 |
| [09-kernel-runtime-compilation](09-kernel-runtime-compilation/README.md) | 20 |
| [10-kv-cache-offload-recomputation](10-kv-cache-offload-recomputation/README.md) | 97 |
| [11-llm-serving-scheduling-disaggregation](11-llm-serving-scheduling-disaggregation/README.md) | 258 |
| [12-moe-parallelism-communication](12-moe-parallelism-communication/README.md) | 25 |
| [13-sparse-attention](13-sparse-attention/README.md) | 11 |
| [14-agentic-inference-serving-runtime](14-agentic-inference-serving-runtime/README.md) | 23 |
| [15-inference-simulation-emulation](15-inference-simulation-emulation/README.md) | 5 |
| [16-weight-quantization-compression](16-weight-quantization-compression/README.md) | 12 |
| [17-pim-near-data-acceleration](17-pim-near-data-acceleration/README.md) | 10 |
| [19-inference-evaluation-benchmarking](19-inference-evaluation-benchmarking/README.md) | 1 |
| [99-other-inference-systems](99-other-inference-systems/README.md) | 189 |
<!-- survey:auto:end -->