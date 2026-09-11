# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-08 · [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)**  
  実装：[✓](https://github.com/FlashML-org/FreeToken) ・ リポジトリ内被引用：1  
  個人PCのGPU・CPU・RAM・PCIeをまとめて見て、エキスパート キャッシュ容量、CPU/GPUで処理するエキスパート量、KVとのVRAM配分をハードウェア帯域に合わせて変えるMoE ランタイム。

- **2026-04 · [Efficient Mixture-of-Experts LLM Inference with Apple Silicon NPUs](2026-2604.18788-npumoe-apple-silicon-npu-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Apple Siliconのニューラル処理装置（Neural Processing Unit; NPU）で混合専門家モデル（Mixture of エキスパート; MoE）を動かすと、トークンごとに選ばれる専門家数が変わる動的ルーティングと、多数の小さな専門家計算・CPU同期が、静的な計算グラフを好むNPUの実行方式と衝突する。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スマートフォンで他アプリがRAMを要求したとき、LLMの重みとKV キャッシュを必要量だけ細かく退避し、KVは圧縮RAMとFlash 保存へ分散、重みは後ろの層から退避して前の層から推論を再開することで、メモリを空けながら復帰時のTime-へ-最初-トークン（最初のトークンが出るまでの時間）を短縮するシステム。

- **2026-09 · [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スマートフォンのNPUでMoEの入力処理を行うとき、全専門家重みをDRAMへ常駐させず、必要な専門家群だけをUFSストレージから固定サイズの作業領域へ順番に読み込み、NPU計算と重み読出しを重ねるシステム。動的に変わる専門家選択を静的グラフ型NPUで扱うため、全専門家で同じ計算グラフを共有し、実行時にはルート情報と重みアドレスだけを差し替える。

- **2026-09 · [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AceSpecは、端末側-クラウド 投機 デコードで下書きが外れた時に「クラウドの返事を待つ→端末側で最初から下書きし直す→また送る」というWAN 巻き戻しを避けるため、クラウド待ち時間中に端末側側で複数の外れ方を先回り計算してキャッシュしておく。

- **2026-07 · [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ATSInferは、VRAMに収まらないLLMを個人PCで動かすとき、層やエキスパートを丸ごとCPU/GPUへ割り当てるのではなく、重みテンソルごとに「GPUへ置く価値」を実測する。常駐配置と実行時の一時GPU転送を分け、CPU計算、PCIe転送、GPU計算を重ねることで、GPU中心オフロードのPCIe待ちとCPU/GPU混合実行のCPU待ちを同時に減らす。

- **2026-06 · [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MawForgeは、ローカルMoEを「完全な モデルがRAMへ入るか」で判定するのではなく、共通重みだけを常駐させ、ルーティングされたエキスパートだけディスクから上限付きキャッシュへ実体化（実体化）する方式である。

- **2026-06 · [E2LLM: Towards Efficient LLM Serving in Heterogeneous Edge/Fog Environments](2026-2606.03770-e2llm-heterogeneous-edge-fog-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  E2LLMは、単一端末ではLLM全体を保持できない異種エッジ・フォグ環境で、全端末を一つの長いパイプラインに押し込むのではなく、複数端末群に分けて各群へ完全なモデル複製を構成し、群内ではモデル並列を使うサービング方式である。

- **2026-06 · [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  巨大な混合専門家モデル（Mixture-of-エキスパート; MoE）をローカル機で動かす際、従来は量子化やルーティング変更で容量を削るか、専門家計算をCPUへ置くため長い入力処理がCPU演算性能に律速され、デコードもDRAM帯域を十分使い切れない。

- **2026-04 · [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エッジNPUではオンチップSRAMが小さく、注意機構の一時活性値まで高密度eDRAMへ置くと、データを保持するための周期リフレッシュがメモリエネルギーを消費する。SHIELDはBF16の1ビット符号と8ビット指数を通常リフレッシュ領域へ固定する一方、誤りに比較的強い7ビット仮数をデータ寿命で分離する。

- **2025-10 · [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小規模基地局側に小さなドラフトモデル、計算能力の高いマクロ基地局側に大きな検証モデルを置き、投機的デコーディング（投機的 デコード）で複数トークンをまとめて検証する分散LLM推論方式。複数要求をバッチ化し、ドラフト生成と検証を2段パイプラインとして重ねる。

### 1年以上前

- **2024-08 · [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  SwapMoEは、全エキスパート（エキスパート）を主メモリへ常駐させる代わりに、各層へ少数の「仮想エキスパート（Virtual エキスパート）」枠だけを用意し、現在の入力で重要な実エキスパートの重みをその枠へ入れ替える。

- **2024-06 · [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)**  
  実装：[✓](https://github.com/Tiiny-AI/PowerInfer) ・ リポジトリ内被引用：12  
  使われやすい部分だけをスマホの高速メモリへ置き、CPU・NPU・フラッシュストレージを役割分担させて大規模LLMを動かす推論システム。

- **2025-04 · [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  ネイティブ ルータが選んだエキスパートごとにINT2/3/4のどれで実行するかを追加ルータで決め、端末ごとのSSD読込・GPU計算時間に合わせて重み転送と計算を重ねるedge向け方式。
<!-- survey:auto:end -->
