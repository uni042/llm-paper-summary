# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（13本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。「リポジトリ内被引用」は収録済み別論文の本文・メタデータから arXiv ID / DOI の明示参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 直近12か月（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md) | ✓ | 0 | スマートフォンで他アプリがRAMを要求したとき、LLMのweightとKV cacheを必要量だけ細かく退避し、KVは圧縮RAMとFlash storageへ分散、weightは後ろのlayerから退避して前のlayerから推論を再開することで、memoryを空けながら復帰時のTime-to-First-Token（最初のtokenが出るまでの時間）を短縮するsystem。 |
| 2026-09 | [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md) | ✓ | 0 | スマートフォンのNPUでMoEの入力処理を行うとき、全専門家重みをDRAMへ常駐させず、必要な専門家群だけをUFSストレージから固定サイズの作業領域へ順番に読み込み、NPU計算と重み読出しを重ねるシステム。動的に変わる専門家選択を静的グラフ型NPUで扱うため、全専門家で同じ計算グラフを共有し、実行時にはルート情報と重みアドレスだけを差し替える。 |
| 2026-09 | [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md) | ✓ | 0 | edge小型modelがdraft main chainをcloudへ送り、cloudのverification待ち時間にreject候補ごとの代替branchをedge側で並列生成してKV/state cacheへ保存する。reject時はcloudからrejection位置と圧縮target distributionだけ返し、edgeでresampleしたtokenに対応するbranchがcacheにあればpointer lookupで続行し、WANを跨ぐfull rollbackと再draftを避ける。uplinkはtoken index中心、downlinkはsparse distributionに非対称化し、tree fan-outはWAN RTTとedge compute budgetから最適化。最大3.52× throughput、50 Kbpsでもnear-peak性能を報告。 |
| 2026-08 | [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md) | [✓](https://github.com/FlashML-org/FreeToken) | 1 | 個人PCのGPU・CPU・RAM・PCIeをまとめて見て、expert cache容量、CPU/GPUで処理するexpert量、KVとのVRAM配分をhardware帯域に合わせて変えるMoE runtime。 |
| 2026-07 | [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md) | ✓ | 0 | CPU/GPUでの実測速度と実行中の負荷をテンソル単位で見て、限られたVRAMへの常駐と一時転送を選び、個人PCでのLLMオフロード待ちとCPU律速を減らす。 |
| 2026-06 | [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md) | ✓ | 0 | full GGUF MoEを丸ごとunified memoryへ載せる代わりに、全tokenが使う共通tensorだけを常駐させ、expert tensorはdisk上のsplit packに分離する。routerが要求したexpertだけを明示的上限付きexecution cacheへmaterializeし、事前plannerがcommon tensor + expert cache + KV cacheだけでbudget超過する構成をload前に拒否する。評価ではcacheを増やすほどhit率は上がってもmacOS memory pressureでthroughputが崩れるため、cache hit最大化ではなくbounded-memory下の実測latency最適化が必要だと示す。 |
| 2026-06 | [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md) | ✓ | 0 | 巨大な混合専門家モデル（Mixture-of-エキスパート; MoE）をローカル機で動かす際、従来は量子化やルーティング変更で容量を削るか、専門家計算をCPUへ置くため長い入力処理がCPU演算性能に律速され、デコードもDRAM帯域を十分使い切れない。著者らは重みの正本を大容量CPUメモリに保ちながら、入力処理では必要な重みをGPUへ細粒度に流して計算と転送を重ね、少数GPUでは通信量を減らす専門家並列を用いる。一方デコードではCPU側のFP8行列ベクトル積、NUMAを意識した細粒度並列、CPUのMoE計算とGPUの注意計算を二つの要求間で重ねる。2基のAMD EPYC 9355と1～2枚のRTX 5090を用いた実機で、元のFP8品質を保ったDeepSeek-R1級モデルについて32K入力を30秒以内、単一デコード21.5トークン/秒、二要求合計33.6トークン/秒を示し、ローカルMoEをクラウド級の応答目標へ近づける。 |
| 2026-04 | [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md) | ✓ | 0 | エッジNPUではオンチップSRAMが小さく、注意機構の一時活性値まで高密度eDRAMへ置くと、データを保持するための周期リフレッシュがメモリエネルギーを消費する。SHIELDはBF16の1ビット符号と8ビット指数を通常リフレッシュ領域へ固定する一方、誤りに比較的強い7ビット仮数をデータ寿命で分離する。長く残るKV仮数はリフレッシュ周期を1216µsまで緩め、各層内で1.5ms未満しか生存しないQと注意出力の仮数はリフレッシュ自体を止める。故障注入とeDRAMセルモデルを組み合わせ、標準リフレッシュ比で35%のリフレッシュエネルギー削減を報告する。 |
| 2026-04 | [Efficient Mixture-of-Experts LLM Inference with Apple Silicon NPUs](2026-2604.18788-npumoe-apple-silicon-npu-moe-inference.md) | ✓ | 0 | Apple Siliconのニューラル処理装置（Neural Processing Unit; NPU）で混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、トークンごとに選ばれる専門家数が変わる動的ルーティングと、多数の小さな専門家計算・CPU同期が、静的な計算グラフを好むNPUの実行方式と衝突する。NPUMoEは、専門家ごとに固定容量を段階化して形状を静的化し、同容量の専門家をまとめて1個の計算グラフとして実行し、利用頻度の高いグループだけをNPUへ常駐させる。Apple M2 Max/M2 Ultra実機で、Phi-3.5-MoE系のプリフィル遅延を比較対象に対して1.32〜5.55倍改善し、エネルギー効率を1.81〜7.37倍高める一方、容量超過トークンの枝刈りにより精度低下は1.1%未満に抑える。 |
| 2025-10 | [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md) | ✓ | 0 | 小規模基地局側に小さなドラフトモデル、計算能力の高いマクロ基地局側に大きな検証モデルを置き、投機的デコーディング（speculative デコード）で複数トークンをまとめて検証する分散LLM推論方式。複数要求をバッチ化し、ドラフト生成と検証を2段パイプラインとして重ねる。さらに無線上り帯域、バッチ境界、投機長を共同最適化し、100要求のシミュレーションで自己回帰デコーディングより一貫して低遅延、個別最適化では最大44.9%の遅延削減を報告する。 |

### 直近12か月より前・リポジトリ内で被引用

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-08 | [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md) | ✓ | 10 | GPUには少数のexpert用slotだけを置き、RAM上の実expert重みを必要に応じてslotへ入れ替えることで、指定したmemory budget内で既存MoEを動かす近似方式。 |
| 2024-06 | [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md) | [✓](https://github.com/Tiiny-AI/PowerInfer) | 6 | 使われやすい部分だけをスマホの高速メモリへ置き、CPU・NPU・フラッシュストレージを役割分担させて大規模LLMを動かす推論システム。 |
| 2025-04 | [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md) | ✓ | 1 | native routerが選んだexpertごとにINT2/3/4のどれで実行するかを追加routerで決め、deviceごとのSSD読込・GPU計算時間に合わせてweight転送と計算を重ねるedge向け方式。 |

### その他

該当なし。
<!-- survey:auto:end -->
