# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（9本）

| 論文 | 一文要約 |
|---|---|
| [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md) | 個人PCのGPU・CPU・RAM・PCIeをまとめて見て、expert cache容量、CPU/GPUで処理するexpert量、KVとのVRAM配分をhardware帯域に合わせて変えるMoE runtime。 |
| [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md) | CPU/GPUでの実測速度と実行中の負荷をテンソル単位で見て、限られたVRAMへの常駐と一時転送を選び、個人PCでのLLMオフロード待ちとCPU律速を減らす。 |
| [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md) | full GGUF MoEを丸ごとunified memoryへ載せる代わりに、全tokenが使う共通tensorだけを常駐させ、expert tensorはdisk上のsplit packに分離する。routerが要求したexpertだけを明示的上限付きexecution cacheへmaterializeし、事前plannerがcommon tensor + expert cache + KV cacheだけでbudget超過する構成をload前に拒否する。評価ではcacheを増やすほどhit率は上がってもmacOS memory pressureでthroughputが崩れるため、cache hit最大化ではなくbounded-memory下の実測latency最適化が必要だと示す。 |
| [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md) | native routerが選んだexpertごとにINT2/3/4のどれで実行するかを追加routerで決め、deviceごとのSSD読込・GPU計算時間に合わせてweight転送と計算を重ねるedge向け方式。 |
| [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md) | 使われやすい部分だけをスマホの高速メモリへ置き、CPU・NPU・フラッシュストレージを役割分担させて大規模LLMを動かす推論システム。 |
| [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md) | GPUには少数のexpert用slotだけを置き、RAM上の実expert重みを必要に応じてslotへ入れ替えることで、指定したmemory budget内で既存MoEを動かす近似方式。 |
| [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md) | スマートフォンのNPUでMoEの入力処理を行うとき、全専門家重みをDRAMへ常駐させず、必要な専門家群だけをUFSストレージから固定サイズの作業領域へ順番に読み込み、NPU計算と重み読出しを重ねるシステム。動的に変わる専門家選択を静的グラフ型NPUで扱うため、全専門家で同じ計算グラフを共有し、実行時にはルート情報と重みアドレスだけを差し替える。 |
| [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md) | edgeの小型modelが投機的に状態を先回りしてcacheし、reject時のedge-cloud全体rollbackをlocal lookupへ置き換えつつ非対称通信でWAN転送量を抑える。 |
| [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md) | スマートフォンで他アプリがRAMを要求したとき、LLMのweightとKV cacheを必要量だけ細かく退避し、KVは圧縮RAMとFlash storageへ分散、weightは後ろのlayerから退避して前のlayerから推論を再開することで、memoryを空けながら復帰時のTime-to-First-Token（最初のtokenが出るまでの時間）を短縮するsystem。 |
<!-- survey:auto:end -->
