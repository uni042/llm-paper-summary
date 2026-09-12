# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（14本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、1年以上前の論文は被引用0件も含めて引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-08 · [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)**  
  実装：[✓](https://github.com/FlashML-org/FreeToken) ・ リポジトリ内被引用：1  
  FreeTokenはGPU・CPU・RAM・PCIe帯域を実測し、専門家キャッシュ容量、CPU/GPU分担、KVへのVRAM配分を動的に変えて、MoE転送待ちを抑えるランタイム。

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

- **2026-07 · [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ATSInferはテンソルごとのGPU常駐価値を実測し、CPU計算・PCIe転送・GPU計算を重ねて、VRAM不足時の転送待ちとCPU律速を減らす方式。

- **2026-06 · [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MawForgeは、共通テンソルを常駐させ、ルーティングされた専門家だけをディスクから上限付きキャッシュへ実体化し、共有メモリ圧力と重み読出しを予算内で抑える方式。

- **2026-06 · [E2LLM: Towards Efficient LLM Serving in Heterogeneous Edge/Fog Environments](2026-2606.03770-e2llm-heterogeneous-edge-fog-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  E2LLMは異種端末を入力処理用・生成用の複製群に分け、各群の連続層を端末へ再配置し、層・帯域・負荷の最遅段を抑える分散サービング方式。

- **2026-06 · [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  巨大MoEのCPU計算・DRAM帯域律速に対し、入力処理は必要重みをGPUへ細粒度転送し、生成はCPU専門家計算とGPU注意を重ねて元精度を保つ方式。

- **2026-04 · [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SHIELDはBF16活性値を符号・指数・仮数と寿命で分け、短命な仮数のeDRAM更新を止め、長寿命KVは周期を延ばして保持エネルギーを減らす方式。

- **2025-10 · [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  小基地局に下書きモデル、大基地局に対象モデルを置き、要求の下書き・検証を二段パイプライン化し、無線帯域・バッチ境界・投機長を調整して往復遅延を減らす方式。

### 1年以上前

- **2024-08 · [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  SwapMoEは、全専門家をメモリに置けない問題に対し、層ごとの仮想枠へ入力で選ばれた専門家重みを入れ替え、メモリ容量と重み転送を抑える方式。

- **2024-06 · [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)**  
  実装：[✓](https://github.com/Tiiny-AI/PowerInfer) ・ リポジトリ内被引用：12  
  PowerInfer-2は、利用頻度を測った重みだけをスマホの高速メモリへ置き、残りをUFSから読みつつCPU・NPU計算と重ねて、容量不足と読出し待ちを減らす方式。

- **2025-04 · [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  D²MoEは、選ばれた専門家ごとに必要精度をINT2〜4から決め、端末ごとのSSD読出しとGPU計算を重ねて重み転送待ちを減らす方式。
<!-- survey:auto:end -->
