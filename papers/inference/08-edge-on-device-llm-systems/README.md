# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-08 | [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md) | [✓](https://github.com/FlashML-org/FreeToken) | 1 | FreeTokenは、ローカルなMoE推論を「GPUに載らない分をCPUへ逃がす」だけでなく、GPU計算、CPU メモリ 帯域、PCIe、エキスパート キャッシュ、KV キャッシュを一つの実行ランタイムで一体的に共同管理するシステムである。8GB laptop GPUからworkstationまで同じ設計を使い。 |
| 2026-04 | [Efficient Mixture-of-Experts LLM Inference with Apple Silicon NPUs](2026-2604.18788-npumoe-apple-silicon-npu-moe-inference.md) | ✓ | 1 | Apple Siliconのニューラル処理装置（Neural Processing Unit; NPU）で混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、トークンごとに選ばれる専門家数が変わる動的ルーティングと、多数の小さな専門家計算・CPU同期が、静的な計算グラフを好むNPUの実行方式と衝突する。NPUMoEは。 |

### 直近12か月・未被引用（2025-10〜2026-09）

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2026-09 | [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md) | ✓ | 0 | スマートフォンで他アプリがRAMを要求したとき、LLMの重みとKV キャッシュを必要量だけ細かく退避し、KVは圧縮RAMとFlash 保存へ分散、重みは後ろの層から退避して前の層から推論を再開することで、メモリを空けながら復帰時のTime-へ-最初-トークン（最初のトークンが出るまでの時間）を短縮するシステム。 |
| 2026-09 | [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md) | ✓ | 0 | EStreamが解こうとしている問題は、「MoEは1トークンごとには少数の専門家しか使わないのに、長い入力をまとめて処理すると結局ほとんどの専門家を使ってしまい、スマートフォンのメモリへ収まらない」という問題である。 |
| 2026-09 | [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md) | ✓ | 0 | 端末側 端末だけで大きなLLMを動かすのはメモリ/計算的に難しい。一方、クラウドだけで推論するとネットワーク 遅延が増える。 |
| 2026-07 | [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md) | ✓ | 0 | 個人PCでは、量子化してもモデル全体がVRAMへ収まらないことがある。GPU中心のオフロードでは、CPUメモリに置いた重みを必要になるたびPCIe経由でGPUへ送り、計算自体はGPUへ寄せる。しかしGPUメモリ帯域が数百GB/s～1TB/s級なのに対し、PCIe 4.0 x16の理論帯域は32 GB/s程度であり、重み転送が支配的になりやすい。 |
| 2026-06 | [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md) | ✓ | 0 | 疎な混合エキスパート（Mixture-of-エキスパート; MoE）モデルは、総パラメータ数が非常に大きくても1 トークンが使うエキスパートは一部だけである。 |
| 2026-06 | [E2LLM: Towards Efficient LLM Serving in Heterogeneous Edge/Fog Environments](2026-2606.03770-e2llm-heterogeneous-edge-fog-serving.md) | ✓ | 0 | E2LLMは、単一端末ではLLM全体を保持できない異種エッジ・フォグ環境で、全端末を一つの長いパイプラインに押し込むのではなく、複数端末群に分けて各群へ完全なモデル複製を構成し、群内ではモデル並列を使うサービング方式である。各複製を入力処理（プリフィル）専用または生成（Decoder）専用へ割り当て、端末ごとの層処理時間、メモリ容量、端末間帯域。 |
| 2026-06 | [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md) | ✓ | 0 | 巨大な混合専門家モデル（Mixture-of-エキスパート; MoE）をローカル機で動かす際、従来は量子化やルーティング変更で容量を削るか、専門家計算をCPUへ置くため長い入力処理がCPU演算性能に律速され、デコードもDRAM帯域を十分使い切れない。著者らは重みの正本を大容量CPUメモリに保ちながら。 |
| 2026-04 | [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md) | ✓ | 0 | エッジNPUではオンチップSRAMが小さく、注意機構の一時活性値まで高密度eDRAMへ置くと、データを保持するための周期リフレッシュがメモリエネルギーを消費する。SHIELDはBF16の1ビット符号と8ビット指数を通常リフレッシュ領域へ固定する一方。 |
| 2025-10 | [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md) | ✓ | 0 | 小規模基地局側に小さなドラフトモデル、計算能力の高いマクロ基地局側に大きな検証モデルを置き、投機的デコーディング（投機的 デコード）で複数トークンをまとめて検証する分散LLM推論方式。複数要求をバッチ化し、ドラフト生成と検証を2段パイプラインとして重ねる。さらに無線上り帯域、バッチ境界、投機長を共同最適化し。 |

### 1年以上前

| 公開 | 論文 | 実装 | リポジトリ内被引用 | 一文要約 |
|---|---|:---:|---:|---|
| 2024-06 | [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md) | [✓](https://github.com/Tiiny-AI/PowerInfer) | 13 | PowerInfer-2が解こうとしている問題は単純で、大きなLLMの重みをスマートフォンのDRAMへ全部置くことができないというものです。 |
| 2024-08 | [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md) | ✓ | 12 | 疎なMoEでは各トークンが少数のエキスパートしか使わないが、通常の実装は「どのエキスパートが選ばれても実行できるように」全エキスパート重みをメモリへ保持する。Switch Transformerで1層64エキスパートを持つ構成では、論文の例で約14 GiBが必要になり、4～8 GiB級の端末へそのまま載せられない。 |
| 2025-04 | [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md) | ✓ | 1 | D²MoEは、エキスパートを「使う/使わない」だけでなく、そのエキスパートを何ビットで読み込むかまでトークンごとに選び、SSD/CPU→GPU転送と計算を端末条件に合わせて組み立てるedge向けランタイムである。 |
<!-- survey:auto:end -->
