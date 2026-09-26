# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（23本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-08 · [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)**  
  実装：[✓](https://github.com/FlashML-org/FreeToken) ・ リポジトリ内被引用：2  
  FreeTokenはGPU・CPU・RAM・PCIe帯域を実測し、専門家キャッシュ容量、CPU/GPU分担、KVへのVRAM配分を動的に変えて、MoE転送待ちを抑えるランタイム。

- **2025-10 · [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  小基地局に下書きモデル、大基地局に対象モデルを置き、要求の下書き・検証を二段パイプライン化し、無線帯域・バッチ境界・投機長を調整して往復遅延を減らす方式。

- **2026-06 · [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  巨大MoEのCPU計算・DRAM帯域律速に対し、入力処理は必要重みをGPUへ細粒度転送し、生成はCPU専門家計算とGPU注意を重ねて元精度を保つ方式。

- **2026-04 · [Efficient Mixture-of-Experts LLM Inference with Apple Silicon NPUs](2026-2604.18788-npumoe-apple-silicon-npu-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NPUMoEは、Apple NPUで動的な専門家選択を固定容量のグループと共有計算グラフへ変換し、頻出群を常駐させて小粒度実行とCPU同期を減らす方式。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  mzCacheはスマホの他アプリ負荷を検知し、LLM重みとKVを圧縮RAM・Flashへ細粒度退避し、復帰計算と読出しを重ねてメモリ回収と再開遅延を両立する方式。

- **2026-09 · [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  EStreamはMoE入力処理で必要な専門家をUFSから固定作業領域へ順次読み込み、NPU計算と重ね、静的共有グラフでDRAM不足と読出し待ちを減らす方式。

- **2026-09 · [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AceSpecは端末–クラウド投機的復号で棄却分岐をWAN待ち中に先回り生成して状態キャッシュへ保存し、棄却後の再下書きと往復通信を減らす方式。

- **2026-08 · [2026-2608.12932-flashdrive-flash-vision-language-action-inference-for-autonomous-driving](2026-2608.12932-flashdrive-flash-vision-language-action-inference-for-autonomous-driving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  FlashDriveは四段階をアルゴリズム・システム協調設計で同時に短縮する。Alpamayo 1.5-10Bでは単一GPUのエンドツーエンド遅延を717ミリ秒から151ミリ秒へ4.7倍短縮し、制御周波数を1.4Hzから6.6Hzへ高めた。

- **2026-07 · [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ATSInferはテンソルごとのGPU常駐価値を実測し、CPU計算・PCIe転送・GPU計算を重ねて、VRAM不足時の転送待ちとCPU律速を減らす方式。

- **2026-06 · [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MawForgeは、共通テンソルを常駐させ、ルーティングされた専門家だけをディスクから上限付きキャッシュへ実体化し、共有メモリ圧力と重み読出しを予算内で抑える方式。

- **2026-06 · [EnerInfer: Energy-Aware On-Device LLM Inference](2026-2606.23001-enerinfer-energy-aware-on-device-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NPU・DDR周波数をモデル構造予測と熱制御で動的調整し、生成速度のQoEを守りながら端末内LLMの復号エネルギー効率を最大65%改善。

- **2026-06 · [Efficient On-Device Diffusion LLM Inference with Mobile NPU](2026-2606.13740-llada-cpp-mobile-npu-diffusion-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スマートフォンNPU向けに多ブロック投機復号、CPU側の疎な改訂、NPU可視メモリの交換最適化を統合し、LLaDA-8Bを接頭辞KV再利用付きCPU基準比17～42倍高速化する。

- **2026-06 · [E2LLM: Towards Efficient LLM Serving in Heterogeneous Edge/Fog Environments](2026-2606.03770-e2llm-heterogeneous-edge-fog-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  E2LLMは異種端末を入力処理用・生成用の複製群に分け、各群の連続層を端末へ再配置し、層・帯域・負荷の最遅段を抑える分散サービング方式。

- **2026-05 · [CATS: Cascaded Adaptive Tree Speculation for Memory-Limited LLM Inference Acceleration](2026-2605.11186-cats-cascaded-adaptive-tree-speculation-for-memory-limited-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の投機的デコード（投機的復号）は、小さなドラフトモデルが候補トークンを先に作り、大きな対象モデルが複数候補を一括検証することで、対象モデルの重み読み出しを複数トークンへ償却する。

- **2026-05 · [2026-2605.16786-lever-speculative-llm-inference-on-smartphones](2026-2605.16786-lever-speculative-llm-inference-on-smartphones.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  フラッシュへ重みを退避すれば容量問題は緩和できるが、自己回帰生成の各ステップで巨大な重みを読み直すと入出力が支配的になる。OnePlus 12など三端末とLlama-3.1-8B、Qwen3系列を使った評価で、フラッシュ退避した通常自己回帰推論に対し平均2.93倍、従来投機的デコードに対し平均1.50倍の高速化を報告する。

- **2026-04 · [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SHIELDはBF16活性値を符号・指数・仮数と寿命で分け、短命な仮数のeDRAM更新を止め、長寿命KVは周期を延ばして保持エネルギーを減らす方式。

- **2026-04 · [EdgeFlow: Fast Cold Starts for LLMs on Mobile Devices](2026-2604.09083-edgeflow-fast-cold-starts-mobile-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モバイルLLMのコールドスタートで浪費されるフラッシュ帯域を、重要度別の可変精度量子化・SIMD向け重み格納・CPU/NPU協調実行で削減し、同等精度条件の初回応答を最大4.07倍高速化する。

- **2026-03 · [FlexServe: A Fast and Secure LLM Serving System for Mobile Devices with Flexible Resource Isolation](2026-2603.09046-flexserve-secure-mobile-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TrustZoneのアクセス権と資源管理権を分離してページ単位セキュアメモリと切替可能NPUを実現し、LLM向けキャッシュ・回収・先読みでセキュア端末内推論の起動遅延を大幅に削減する。

### 2年前（2024-10〜2025-09）

- **2025-04 · [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  D²MoEは、選ばれた専門家ごとに必要精度をINT2〜4から決め、端末ごとのSSD読出しとGPU計算を重ねて重み転送待ちを減らす方式。

### 3年前（2023-10〜2024-09）

- **2024-06 · [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)**  
  実装：[✓](https://github.com/Tiiny-AI/PowerInfer) ・ リポジトリ内被引用：34  
  PowerInfer-2は、利用頻度を測った重みだけをスマホの高速メモリへ置き、残りをUFSから読みつつCPU・NPU計算と重ねて、容量不足と読出し待ちを減らす方式。

- **2024-08 · [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  SwapMoEは、全専門家をメモリに置けない問題に対し、層ごとの仮想枠へ入力で選ばれた専門家重みを入れ替え、メモリ容量と重み転送を抑える方式。

### 4年前（2022-10〜2023-09）

- **2023-08 · [EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices](2023-2308.14352-edgemoe.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/mllm) ・ リポジトリ内被引用：32  
  MoE エキスパートを外部ストレージ化し、エキスパート別混合量子化と活性相関に基づく先読み・キャッシュでモバイル推論のI/O律速を緩和する。

### 公開時期未分類

- **2026 · [視覚言語モデル向け再利用機構 VLMCache](2026-35c4f3816b37-vlmcache-efficient-on-device-vision-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VLMCacheは、UIエージェントや視覚質問応答のように連続フレームを処理する視覚言語モデルで、毎フレームの視覚入力を最初から入力処理するため初回トークン時間が長くなる問題を扱う。提案法は安定した背景ブロックと変化した前景ブロックを意味的に分離し、背景を再利用可能なKVキャッシュ接頭辞として並べ、前景だけを再計算する。
<!-- survey:auto:end -->
