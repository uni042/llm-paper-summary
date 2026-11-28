# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（139本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/08-edge-on-device-llm-systems/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-12〜2026-11**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-12〜2026-11）

- **2026-05 · [An Efficient Context Management System for On-Device LLMaaS (Libra; preprint: LLM as a System Service on Mobile Devices)](2024-2403.11805-llm-as-a-system-service-on-mobile-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  アプリを切り替えるたびに履歴全体を再計算するか、ディスクへ退避したKVを読み戻すと、次の生成開始までの待ち時間が長くなる。正式出版版の実機評価では、一律8ビット圧縮を伴うチャンク退避方式に対し、コンテキスト切替遅延を最大20倍、平均9.7倍削減した。

- **2026-08 · [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)**  
  実装：[✓](https://github.com/FlashML-org/FreeToken) ・ リポジトリ内被引用：7  
  FreeTokenは、混合専門家モデル（Mixture of エキスパート、MoE）の全専門家重みがGPUメモリに収まらない場合に、GPU・CPU・主記憶・PCIeを一つの推論基盤として使うローカル配信システムである。

- **2026-05 · [Agent-X: Full Pipeline Acceleration of On-device AI Agents](2026-2605.10380-agent-x-full-pipeline-acceleration-of-on-device-ai-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  Agent-Xは、端末内で実行する大規模言語モデル（LLM）エージェントの遅延を、入力事前充填（プリフィル）と逐次生成（デコード）の両段階から削減する方式である。原著はTinyAgent-7BとMac mini M4 Proの実機を用い、エージェント全体で平均1.61倍の高速化を示す。

- **2026-04 · [MemExplorer: Navigating the Heterogeneous Memory Design Space for Agentic Inference NPUs](2026-2604.16007-memexplorer-navigating-the-heterogeneous-memory-design-space-for-agentic-inference-npus.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  SRAM/HBM/LPDDR/GDDR/HBFを統一モデル化し、プリフィル/デコードNPUとメモリ階層を共同探索して、基準NPU比でプリフィル最大2.3倍・デコード最大1.93倍の電力効率を得る。

- **2026-06 · [VLMCache: Efficient On-Device Vision-Language Model Inference](2026-35c4f3816b37-vlmcache-efficient-on-device-vision-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  VLMCacheは、UIエージェントや視覚質問応答のように連続フレームを処理する視覚言語モデルで、毎フレームの視覚入力を最初から入力処理するため初回トークン時間が長くなる問題を扱う。提案法は安定した背景ブロックと変化した前景ブロックを意味的に分離し、背景を再利用可能なKVキャッシュ接頭辞として並べ、前景だけを再計算する。

- **2026-06 · [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  巨大MoEのCPU計算・DRAM帯域律速に対し、入力処理は必要重みをGPUへ細粒度転送し、生成はCPU専門家計算とGPU注意を重ねて元精度を保つ方式。

- **2026-03 · [FastTTS: Accelerating Test-Time Scaling for Edge LLM Reasoning](2026-2509.00195-fasttts-accelerating-test-time-scaling-for-edge-llm-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  生成モデルと過程評価モデルを1枚のGPUに載せる場合には、両者へのKV領域の配分も難しい。FastTTSはこの三つの資源問題に対応する配信システムである。論文の主評価は単一のRTX 4090（24GB）で、AIME2024とAMC2023の数学問題を対象に、複数の生成器・検証器の組合せと探索枝数を比較する。

- **2026-01 · [Native LLM and MLLM Inference at Scale on Apple Silicon](2026-2601.19139-native-llm-and-mllm-inference-at-scale-on-apple-silicon.md)**  
  実装：[✓](https://github.com/waybarrios/vllm-mlx) ・ リポジトリ内被引用：4  
  Apple SiliconはCPUとGPUが同じ物理メモリを利用する統合メモリ構成を持つため、一般的な独立GPU環境とはモデル重みや中間状態の管理条件が異なる。

- **2026-05 · [Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU](2026-2605.20706-llamaweb.md)**  
  実装：[✓](https://github.com/ggml-org/llama.cpp) ・ リポジトリ内被引用：3  
  LlamaWebは静的メモリ計画、端末適応型WebGPUカーネル、量子化対応をllama.cppへ統合し、ブラウザ推論のメモリ消費とデコード性能を改善する。

- **2026-09 · [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  スマートフォンで大規模言語モデル（LLM）を端末内実行すると、モデル重みだけでなく、会話履歴を再計算せずに利用する鍵・値キャッシュ（KVキャッシュ）が長時間RAMを占有する。mzCacheはこの問題を、端末での退避後の復帰時間を最小化するメモリ管理として扱う。

- **2026-10 · [Stepped MoE: Segment-Level Routing with Configurable Inference Complexity](2026-2610.07348-stepped-moe-segment-level-routing-with-configurable-inference-complexity.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  区間ごとに全層の専門家を一括選択して固定し、入れ替えの入出力を消しながら、1つのモデルから活性1Bから4Bまでを選べるようにした、端末向けの専門家混合構造。

- **2026-09 · [MCSched: Memory-Controller-Aware Scheduling for Embodied LLM Workloads on NVIDIA Jetson](2026-fd0d3fa4e564-mcsched-memory-controller-aware-scheduling-for-embodied-llm-workloads-on-nvidia-jetson.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Jetson統合メモリの隠れた帯域競合を監視し、締切危険時だけ背景LLMを一時停止してロボット処理を保護する軽量実行時スケジューラ。

- **2026-07 · [HeteroMosaic: Exposing and Exploiting Heterogeneous Execution Opportunities for Energy-Efficient Edge LLM Inference](2026-2607.12839-heteromosaic-exposing-and-exploiting-heterogeneous-execution-opportuniti.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  近年の端末向けシステムオンチップ（SoC）には、CPU、内蔵画像処理装置（integrated GPU、iGPU）、神経処理装置（NPU）が同居し、同じ主記憶を共有するものがある。原著はAMD Ryzen AIの3機種を用いて、事前充填（プリフィル）で内蔵GPU単独比の平均速度向上率をそれぞれ約2.30倍、1.50倍、1.17倍と報告する。

- **2026-06 · [E2LLM: Towards Efficient LLM Serving in Heterogeneous Edge/Fog Environments](2026-2606.03770-e2llm-heterogeneous-edge-fog-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  E2LLMは異種端末を入力処理用・生成用の複製群に分け、各群の連続層を端末へ再配置し、層・帯域・負荷の最遅段を抑える分散サービング方式。

- **2026-05 · [Quant.npu: Enabling Efficient Mobile NPU Inference for on-device LLMs via Fully Static Quantization](2026-2605.20295-quant-npu-enabling-efficient-mobile-npu-inference-for-on-device-llms-via.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  QualcommのHexagon系NPUは、整数行列積の高速化と規則的な量子化に適した専用回路を持つ。SM8650実機ではW4A8構成がExecuTorchのW4A16構成より最大15.1%低遅延となり、Llama-3.2-3B-InstructのW4A8では従来の回転方式より精度が大きく改善した。

- **2026-05 · [Lever：スマートフォン向けフラッシュ常駐LLMの投機的推論](2026-2605.16786-lever-speculative-llm-inference-on-smartphones.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  OnePlus 12上の測定では、フラッシュ常駐標的モデルの検証時間のうち約78〜93%を入出力が占める条件があり、演算高速化だけではこの待ち時間を解消できない。Leverは投機的復号（投機的復号）を「サーバGPUで標的モデルの計算回数を減らす方式」ではなく、「フラッシュ常駐モデルの呼出し回数を複数トークンへ償却する方式」として再設計する。

- **2026-04 · [Unlocking the Edge deployment and ondevice acceleration of multi-LoRA enabled one-for-all foundational LLM](2026-2604.18655-ondevice-multilora-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  実行時LoRA入力・NPU向け最適化・並行生成・自己投機的復号を統合し、Galaxy S24/S25で多用途LLMを単一グラフ展開する。

- **2026-04 · [SWARM-LLM: Collaborative Inference for Edge-based Small Language Models](2026-2606.14711-swarm-llm-collaborative-inference-for-edge-based-small-language-models.md)**  
  実装：[✓](https://github.com/mdahshan/swarm_llm) ・ リポジトリ内被引用：1  
  不確実性と安全性でクエリを振り分け、エッジの小規模モデルの群れで答えられない分だけクラウドの大きなモデルを召喚し、クラウド利用を約4分の1に抑える協調推論の制御層。

- **2026-04 · [Efficient Mixture-of-Experts LLM Inference with Apple Silicon NPUs](2026-2604.18788-npumoe-apple-silicon-npu-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NPUMoEは、Apple NPUで動的な専門家選択を固定容量のグループと共有計算グラフへ変換し、頻出群を常駐させて小粒度実行とCPU同期を減らす方式。

- **2026-04 · [EdgeFlow: Fast Cold Starts for LLMs on Mobile Devices](2026-2604.09083-edgeflow-fast-cold-starts-mobile-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  モバイルLLMのコールドスタートで浪費されるフラッシュ帯域を、重要度別の可変精度量子化・SIMD向け重み格納・CPU/NPU協調実行で削減し、同等精度条件の初回応答を最大4.07倍高速化する。

- **2025-12 · [LOIP: Collaborative LLM Inference with Offloading-based Pipeline Parallelism on Edge Devices](2025-2512.21835-loip-collaborative-llm-inference-with-offloading-based-pipeline-parallel.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  LOIPは、端末ごとのメモリ容量・演算性能が異なる複数のNVIDIA Jetsonを連携させ、モデルのパラメータを量子化・枝刈りせずに推論するための実行基盤である。

- **2025-12 · [ActionFlow: A Pipelined Action Acceleration for Vision Language Models on Edge](2025-2512.20276-actionflow-a-pipelined-action-acceleration-for-vision-language-models-on.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  連続制御の現在フレームのプリフィルと過去フレームのデコードを1バッチへ詰めるリクエスト間パイプライン化で、再学習なしにエッジ上の視覚言語行動モデルを2.55倍高速化する推論基盤。

### 直近12か月・未被引用（2025-12〜2026-11）

- **2026-11 · [SGA-Sparse: Training Native SwiGLU Gates for Activation-Sparse and Low-Bit LLMs](2026-2611.11223-sga-sparse-training-native-swiglu-gates-for-activation-sparse-and-low-bi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SwiGLUの元のゲートを固定予算ルータとして全パラメータ学習し、学習なしでは劣るゲート信号が学習後に最良のルーティング信号へ逆転することを示して、補助ルータなしでFFNの75から85パーセントのスパース化と低ビット量子化の併用を等価ビット幅のパレート前線で示した活性値スパース学習。

- **2026-11 · [MixFold: Sub-4-Bit Mixed-Precision LLM Inference via Output-Channel Grouping on Mobile NPUs](2026-2611.26976-mixfold-sub-4-bit-mixed-precision-llm-inference-via-output-channel-group.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モバイルNPUで3ビットと完全対称2ビットの重みを展開せずネイティブ整数演算で実行する折り畳みと、タイル整合な出力チャネルグループ単位の混合精度を組み合わせ、llama.cpp比でデコード最大1.41倍とエネルギー効率最大4.3倍を実現するモバイル推論手法。

- **2026-11 · [HyCoInfer: Cloud-Edge Collaborative Inference for Large Language Models on Heterogeneous GPU-FPGA Architectures](2026-2611.22086-hycoinfer-cloud-edge-collaborative-inference-for-large-language-models-o.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィルをクラウドGPU、デコードをGPUとエッジFPGAへ分ける分離型サービングで、FPGA容量を織り込んだ役割分担と帯域適応型のKV圧縮と層単位転送により、500Mbps回線の長文質問応答でクラウドのみ比グッドプット4.11倍と遅延56.2パーセント減を出す協調推論システム。

- **2026-10 · [TileWeave: Heterogeneous Tiling for Sparse Prefill on Mobile SoCs](2026-2611.00408-tileweave-heterogeneous-tiling-for-sparse-prefill-on-mobile-socs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  細かく選んだキーの塊を共有度で分け、共有の多い塊は大きなタイルで主演算器、少ない塊は画像処理器で処理する異種分担により、検索精度を比較対象の疎な注意と同等以上に保ちながら携帯電話の入力処理を最大三・二三倍速くしたと報告した。

- **2026-10 · [Shared Context, Separate Engines: Stateful Streaming Inference for Multimodal LLMs on Edge SoCs](2026-2610.35309-shared-context-separate-engines-stateful-streaming-inference-for-multimo.md)**  
  実装：[✓](https://github.com/jimmy-yilong-li/CrossInfer) ・ リポジトリ内被引用：0  
  履歴を版付き文脈として公開し、エンジン間でKV状態とプリフィル済み分枝を受け渡せるようにして、取り込みと回答を別エンジンで同時に行い、状態の場所と待ちから配置を決めることで、エッジSoCの複数エンジンを遊ばせないストリーミング推論方式。

- **2026-10 · [Seeing at the Edge: Energy Characterization of Vision-Language Model Inference on Edge Platforms](2026-2610.20136-seeing-at-the-edge-energy-characterization-of-vision-language-model-infe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  PiとJetsonの4つの実行経路で視覚言語モデルのシステム全体エネルギーを測り、固定費と出力比例分へ分解して、NPUとGPUの有利さが出力長で逆転することを示した計測研究。

- **2026-10 · [HydraLLM: Adaptive Width Slicing for Elastic Text and Vision-Language Models](2026-2610.23455-hydrallm-adaptive-width-slicing-for-elastic-text-and-vision-language-mod.md)**  
  実装：[✓](https://github.com/tuhh-ncps/hydrallm) ・ リポジトリ内被引用：0  
  有効ヘッド数1つで埋め込みから出力ヘッドまでの幅を連動させ、単一の重みから入れ子の部分モデルを実行時に切り出す弾性推論と、静的モデルを重要度並べ替えと確率的学習で弾性化する変換手順、および視覚射影への拡張。

- **2026-09 · [TierKV: Long-Context On-Device LLMs via Predictive Multi-Tier KV Caching](2026-2609.21172-tierkv-long-context-on-device-llms-via-predictive-multi-tier-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  サーバーGPUと異なりスマートフォンはOSや他アプリとDRAMを共有し、メモリ上限を超えるとプロセスが強制終了される場合がある。TierKVは、キャッシュを正確なFP16形式の階層0、低ランク圧縮したDRAM内の階層1、フラッシュへ退避した階層2に分ける。

- **2026-09 · [ThermE: Predictive Management of Shared Thermal Headroom for Sustained LLM Inference on Thermally Constrained Edge SoCs](2026-2610.00267-therme-predictive-management-of-shared-thermal-headroom-for-sustained-ll.md)**  
  実装：[✓](https://anonymous.4open.science/r/ThermE-codebase-D37B/) ・ リポジトリ内被引用：0  
  候補操作の発熱を事前に見積もり、熱余裕を予測して周波数設定とトークン上限を不確実さ込みで選ぶことで、共有冷却のエッジSoC上でvLLM比で最初のトークンまでの時間を40.55パーセント減らし、品質目標違反率を5.70パーセントまで下げた実行系の研究。

- **2026-09 · [PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling](2026-2609.09662-pelm-speculative-decoding-dvfs.md)**  
  実装：[✓](https://github.com/imec-nu/PELM) ・ リポジトリ内被引用：0  
  DVFS・自己投機的デコード・可変検証深度を深層強化学習で共同制御し、端末LLMで最大23.1%高速化・52.4%エネルギー削減を達成する。

- **2026-09 · [Partition-Aware Scheduling for Mobile Heterogeneous Inference Co-Execution](2026-2609.14213-partition-aware-scheduling-for-mobile-heterogeneous-inference-co-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  演算子のCPU-GPU分割とDAG上の実行順を共同最適化し、段階化・臨界度標本化・遅延予測による配備時反復探索でオフライン最適化に近いモバイル推論遅延を得る。

- **2026-09 · [OmniTide: Co-Designing Algorithms and Systems for Efficient On-Device Omni-LLM Streaming](2026-2609.34653-omnitide-co-designing-algorithms-and-systems-for-efficient-on-device-omn.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各時刻の視覚・音声表現がLLMへ投入されるとKVキャッシュが累積し、後続の質問が過去の場面を参照できる一方、端末のメモリ容量と注意機構の計算量を圧迫する。主な検証では、Qwen2.5-Omni-3B/7Bの完全履歴との比較でストリームセッション時間が2.29〜2.40倍短くなり、StreamingBench正答率はほぼ同水準である。

- **2026-09 · [JustFit: 200K-Token LLM Serving on a 24 GiB Laptop with Just-in-Time State Management](2026-2609.17475-justfit-200k-token-llm-serving-on-a-24-gib-laptop-with-just-in-time-state-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  圧縮キー・バリュー実行、部品常駐切替、状態保持遷移を統合し、24 GiB機で27B級モデルの約213K位置の単一要求を完走する推論実行系。

- **2026-09 · [IronLLM: Forging Compact Edge-Native Language Models for Real-Time Embodied Intelligence](2026-2609.36860-ironllm-forging-compact-edge-native-language-models-for-real-time-embodi.md)**  
  実装：[✓](https://xpeng-robotics.github.io/iron-fm) ・ リポジトリ内被引用：0  
  エッジ向け654Mモデルの技術報告で、深度間でパラメータとKVを共有する軽量な複数トークン予測X-MTPと、巻き戻し不要のドラフトを実現する軽量検証ヘッドにより、ハイブリッド線形注意モデルでデコードを最大1.48倍高速化し、その品質上の代償まで測った研究。

- **2026-09 · [IHS-LM: Intra-batch Hybrid Scheduling and Layer Migration for VLM Pipeline Inference Acceleration on Edge Devices](2026-9b405eddeda4-ihs-lm-intra-batch-hybrid-scheduling-and-layer-migration-for-vlm-pipeline-inference-acceleration-on-edge-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV容量連動のプリフィル/デコード混在スケジューリングと帯域感知型の境界層移行を統合し、異種Jetson上のVLM推論遅延を最大17.5%削減する。

- **2026-09 · [Gradient Enhancement Task Aware Post-training Quantization](2026-b05762d80b35-gradient-enhancement-task-aware-post-training-quantization.md)**  
  実装：[✓](https://github.com/YihuaJerry/GTAQ.git) ・ リポジトリ内被引用：0  
  対象タスクの勾配と量子化代理誤差と重みの大きさを掛けた複合感度でタスク重要チャネルを見つけ、重要度で重み付けした再構成探索で一様ビット量子化をタスク適応させる学習後量子化GTAQ。

- **2026-09 · [FoldQuantVLA: Native Low-Bit Quantization of Vision-Language-Action Models via Consistent Folding](2026-2609.24433-foldquantvla-native-low-bit-quantization-of-vision-language-action-models-via-consistent-folding.md)**  
  実装：[✓](https://github.com/cair-vinuni/FoldQuantVLA) ・ リポジトリ内被引用：0  
  VLAの共有活性値変換を校正から重み丸め、TensorRT実行まで一貫させる学習後量子化を設計し、W4A4でOrin上の推論を浮動小数点TensorRT比1.20〜1.33倍に高速化した。

- **2026-09 · [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  EStreamはMoE入力処理で必要な専門家をUFSから固定作業領域へ順次読み込み、NPU計算と重ね、静的共有グラフでDRAM不足と読出し待ちを減らす方式。

- **2026-09 · [BigMoMo: Efficient Inference of Large-Scale MoE with Speculative Decoding on Mobile Devices](2609.14643.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号の複数トークン窓でエキスパート再利用・フラッシュ連続読出し・NPU計算との移動重畳を行い、30B級MoEのスマホ推論を平均4.83倍高速化する。

- **2026-09 · [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AceSpecは端末–クラウド投機的復号で棄却分岐をWAN待ち中に先回り生成して状態キャッシュへ保存し、棄却後の再下書きと往復通信を減らす方式。

- **2026-08 · [RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention](2026-2608.08081-rotaryquant-fitting-120b-moe-models-on-consumer-hardware-via-fused-compressed-space-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み・3ビット鍵値キャッシュ・専門家退避を統合し、圧縮表現のまま注意計算して120B MoEを17.2GB、14.85トークン毎秒で実行する。

- **2026-08 · [Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels](2026-2608.25053-hydra-phase-aware-workload-characterization-of-llm-inference-across-edge.md)**  
  実装：[✓](https://github.com/amirtaherin/hydra) ・ リポジトリ内被引用：0  
  Hydraは、エッジ向け統合SoCで動く大規模言語モデル（LLM）の推論を、事前充填（プリフィル）と復号（デコード）という二つの処理区間に分け、実行時間・CPU/GPU活動・主記憶帯域・電力・消費エネルギー・温度を対応付ける計測・解析基盤である。

- **2026-08 · [From Cloud to Crowd: Democratizing LLM Service With Decentralized Edge Collaboration for RAG](2026-2608.00922-from-cloud-to-crowd-democratizing-llm-service-with-decentralized-edge-co.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エッジ機器同士で知識グラフと計算を共有し、クエリごとにモデルと検索量をバンディットで選ぶ分散RAGにより、クラウドLLMとの正解率差を半分以下へ縮め費用を最大98.4パーセント減らす協調推論基盤。

- **2026-08 · [FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving](2026-2608.12932-flashdrive-flash-vision-language-action-inference-for-autonomous-driving.md)**  
  実装：[✓](https://github.com/z-lab/flashdrive) ・ リポジトリ内被引用：0  
  FlashDriveは、映像と鍵・値キャッシュ（KVキャッシュ）の時系列再利用、拡散モデルによる複数推論トークンの投機的生成、軌跡生成の中間速度再利用、CUDA実行グラフと演算融合、重み4ビット・活性値8ビット量子化を組み合わせる。最終構成では716.9→151.4ミリ秒、約4.7倍の実測高速化となる。

- **2026-08 · [Event-Driven Language Models with Sparse Neural Activity for Neuromorphic Hardware](2026-2608.30439-event-driven-language-models-with-sparse-neural-activity-for-neuromorphi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  量子化された線形注意モデルの全射影に、射影ごとに学習する閾値で小さい活性値をゼロ化する仕組みと疎さの損失を入れ、有効演算を最大約4倍減らし、イベント駆動の多チップ基盤では密モデル比5.4倍のスループットが投影されることを示した研究。

- **2026-08 · [EdgeXpert: An Edge Device for Memory-Efficient LLM Inference with Mixture-of-Experts and Speculative Decoding](2026-2608.05303-edgexpert-moe-speculative-decoding.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21481269) ・ リポジトリ内被引用：0  
  MoEと投機的復号の併用で増える専門家外部メモリアクセスを、プリフィルの共有専門家再利用とデコードの深さ認識チャネル統合で直接削減するエッジ向け協調設計。

- **2026-08 · [Broadcast Rate Limits in Wi-Fi: A Forgotten Bottleneck for Collaborative Edge LLM Inference](2026-2608.02341-broadcast-rate-limits-in-wi-fi-a-forgotten-bottleneck-for-collaborative-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散MoEの一対多配信をUDPブロードキャスト化して有線で1.4倍高速化し、無線ではWi-Fiのブロードキャスト54Mbps上限が真の律速であることを実機とシミュレーションで示した研究。

- **2026-07 · [Voltron: Enabling Elastic Multi-Device Execution of LLM Inference for Empowered Edge Intelligence](2026-2607.07046-voltron-enabling-elastic-multi-device-execution-of-llm-inference-for-emp.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  近くの複数デバイスを束ね、層ごとの並列方式と精度を環境に合わせて計画し、実行中の変動にも伸縮して応じるエッジ向けLLM推論枠組み。品質目標を守りながら単一デバイスより最大16.5パーセント高い精度を達成。

- **2026-07 · [Transition-Aware Backend Dispatch for Edge LLM Inference](2026-2607.17415-transition-aware-backend-dispatch-for-edge-llm-inference.md)**  
  実装：[✓](https://anonymous.4open.science/r/power_aware_edge_inference_public-3B71/README.md) ・ リポジトリ内被引用：0  
  著者らは、対象演算の形状情報だけでなく、直前に選んだバックエンドも使い、演算が速くなる利得より切替費用が大きい場合は実行先を維持する選択方式を調べる。最良の静的バックエンドに比べた平均改善は遅延17.4%、エネルギー14.4%、エネルギー遅延積（EDP）28.5%だった。

- **2026-07 · [NPUsper: Eliminating Redundant Computation for Real-Time Whisper on Mobile NPUs](2026-2607.01108-npusper-eliminating-redundant-computation-for-real-time-whisper-on-mobil.md)**  
  実装：[✓](https://github.com/npusper/NPUsper) ・ リポジトリ内被引用：0  
  第一は、短い音声片に対するWhisperの幻覚を抑えるため、従来方式が毎回30秒近い入力を作り、既に処理した音声や無音埋めを再計算すること。

- **2026-07 · [MORES: Mobile Reasoning-as-a-Service via Distributed LLM Inference-Time Scaling](2026-2607.08116-mores-mobile-reasoning-as-a-service-via-distributed-llm-inference-time-s.md)**  
  実装：[✓](https://github.com/NICE-HKU/MORES) ・ リポジトリ内被引用：0  
  潜在推論の再帰を端末とエッジサーバーへ分割し、再帰ステップ数と送信枝刈り率を意味ルーター付き混合専門家型の強化学習で決めることで、通常のソフトアクタークリティックより平均スループットを約18パーセント高める分散推論時スケーリング。

- **2026-07 · [LightMoE: Task-Aware Expert Availability Management for Memory-Efficient MoE-LLM Inference](2026-b91ae66e6514-lightmoe-task-aware-expert-availability-management-for-memory-efficient-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  頻度で選んだ常駐エキスパート集合、欠けたエキスパートを似た常駐エキスパートへ入出力なしで振り替えるリダイレクト、タスク変化への粗粒度の入替えで、エッジ向けMoE推論のメモリと精度と遅延を両立させる枠組みLightMoE。

- **2026-07 · [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ATSInferはテンソルごとのGPU常駐価値を実測し、CPU計算・PCIe転送・GPU計算を重ねて、VRAM不足時の転送待ちとCPU律速を減らす方式。

- **2026-06 · [Ternary Mamba: Grouped Quantization-Aware Training of W1.58A16 State Space Models](2026-2606.18114-ternary-mamba-grouped-quantization-aware-training-of-w1-58a16-state-spac.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習済みMamba-2 1.3Bへグループ単位の三値量子化対応学習と知識蒸留を適用し、わずか1億トークン規模の追加学習で重みを3.61倍圧縮してゼロからの二値学習にほぼ並ぶ精度へ届かせ、学習可能スケールによるゼロ比率崩壊と事後補正の不転移を明らかにした研究。

- **2026-06 · [Multi-Objective Structured Pruning of LLMs for Latency and Model Size Optimization](2026-2607.22583-multi-objective-structured-pruning-of-llms-for-latency-and-model-size-op.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  層単位の除去を性能損失と実測遅延の多目的進化探索で決め、残りの刈り込み予算を並列ベイズ最適化で層ごとに配分する2段階の構造化枝刈りで、同率の既存手法より精度を保ちながらA100とJetson Nanoの両方で最速の遅延を出した研究。

- **2026-06 · [MawForge: Memory-Bounded Expert Materialization for Local Mixture-of-Experts Inference](2026-2607.09686-mawforge-memory-bounded-expert-materialization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MawForgeは、共通テンソルを常駐させ、ルーティングされた専門家だけをディスクから上限付きキャッシュへ実体化し、共有メモリ圧力と重み読出しを予算内で抑える方式。

- **2026-06 · [From Prompt to Service: An SLM-Based Agent Orchestration Gateway for AI-Driven Virtual Worlds](2026-2606.03557-from-prompt-to-service-an-slm-based-agent-orchestration-gateway-for-ai-d.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大きな言語モデル一つですべての入力を処理する設計は、簡単なサービス振り分けにも大きな推論費用と遅延を要する。著者はキプロスの文化財を題材にしたInterwovenXR仮想博物館で実装し、Jetson Orin NX 8GBを用いて複数の小型モデルを比較した。

- **2026-06 · [EnerInfer: Energy-Aware On-Device LLM Inference](2026-2606.23001-enerinfer-energy-aware-on-device-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  NPU・DDR周波数をモデル構造予測と熱制御で動的調整し、生成速度のQoEを守りながら端末内LLMの復号エネルギー効率を最大65%改善。

- **2026-06 · [Efficient On-Device Diffusion LLM Inference with Mobile NPU](2026-2606.13740-llada-cpp-mobile-npu-diffusion-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スマートフォンNPU向けに多ブロック投機復号、CPU側の疎な改訂、NPU可視メモリの交換最適化を統合し、LLaDA-8Bを接頭辞KV再利用付きCPU基準比17～42倍高速化する。

- **2026-05 · [Keyword Matters: Unveiling the Energy Sensitivity of On-Device LLM Prompting](2026-2607.22568-keyword-matters-unveiling-the-energy-sensitivity-of-on-device-llm-prompt.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の推論効率化は量子化、剪定、推論カーネル、KVキャッシュ管理などモデル・実装側の変更が中心だった。論文で強調される18.5%、62.6%等は後者の相対値であり、別モデルや別端末の絶対エネルギーをそのまま比較した値ではない。

- **2026-05 · [Intelligence Delivery Network: Toward an Internet Architecture for the AI Age](2026-2605.13235-intelligence-delivery-network-toward-an-internet-architecture-for-the-ai.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案のIntelligence Delivery Network（IDN）は、CDNが人気コンテンツを需要の近くへ配置する発想を、AIの「能力」へ拡張する。

- **2026-05 · [E3-Agent: An Executable and Evolving Agent for Resource Management of Edge Generative Inference](2026-2605.27428-e3-agent-an-executable-and-evolving-agent-for-resource-management-of-edg.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高速経路ルーターと出来事駆動の言語モデルメタ制御を分離し、処理時間をオンライン推定しながらリスク遮断と再校正で体制変化へ適応するエッジ生成推論の資源管理エージェントで、静的方式より平均遅延を65〜73パーセント減らす。

- **2026-05 · [CR^2: Cost-Aware Risk-Controlled Routing for Wireless Device-Edge LLM Inference](2026-2605.12001-cr-2-cost-aware-risk-controlled-routing-for-wireless-device-edge-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末上で小型の言語モデルを実行すれば、無線転送の待ち時間や通信電力を避けられる。CR²は、端末でローカル実行の可否を判定し、保留した問い合わせだけをエッジ側でモデル選択する二段階のルーティング方式である。

- **2026-05 · [CoMIC: Collaborative Memory and Insights Circulation for Long-Horizon LLM Agents in Cloud-Edge Systems](2026-2606.00756-comic-collaborative-memory-and-insights-circulation-for-long-horizon-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習済みモデルの能力を重み更新で強化する研究ではなく、記憶と処理配置の設計によって弱いエージェントの実行品質と文脈費用を改善するシステムである。

- **2026-05 · [CATS: Cascaded Adaptive Tree Speculation for Memory-Limited LLM Inference Acceleration](2026-2605.11186-cats-cascaded-adaptive-tree-speculation-for-memory-limited-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の投機的デコード（投機的復号）は、小さなドラフトモデルが候補トークンを先に作り、大きな対象モデルが複数候補を一括検証することで、対象モデルの重み読み出しを複数トークンへ償却する。

- **2026-04 · [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SHIELDはBF16活性値を符号・指数・仮数と寿命で分け、短命な仮数のeDRAM更新を止め、長寿命KVは周期を延ばして保持エネルギーを減らす方式。

- **2026-04 · [MUXQ: Mixed-to-Uniform Precision MatriX Quantization via Low-Rank Outlier Decomposition](2026-2604.04701-muxq-mixed-to-uniform-precision-matrix-quantization-via-low-rank-outlier.md)**  
  実装：[✓](https://github.com/GillchLee/MUXQ) ・ リポジトリ内被引用：0  
  活性値の外れ値チャネルを本体と低ランク補助行列へ分解して大きさを分散させ、混合精度を使わない一様な整数量子化で半精度に近い困惑度を保つ量子化手法。GPT-2の3規模で素朴な量子化を一貫して上回ることを示した研究。

- **2026-04 · [EdgeFM: Efficient Edge Inference for Vision-Language Models](2026-2604.27476-edgefm-efficient-edge-inference-for-vision-language-models.md)**  
  実装：[✓](https://github.com/windog-labs/edge-fm-x) ・ リポジトリ内被引用：0  
  本研究は、産業用エッジ装置で視覚・言語モデル（Vision-Language モデル, VLM）と大規模言語モデル（Large Language モデル, LLM）を低遅延で動かすための推論基盤EdgeFMを提案する。

- **2026-04 · [A Unified Model and Document Representation for On-Device Retrieval-Augmented Generation](2026-2604.14403-a-unified-model-and-document-representation-for-on-device-retrieval-augm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索拡張生成（retrieval-augmented generation、RAG）をスマートフォンや小型計算機だけで動かす場合、サーバーへ個人文書を送らずに利用できる反面、二つのメモリ費用が問題となる。従来は検索用の埋め込みと生成用の圧縮文脈を別々に作ることが多く、文書ごとに二重の表現を保持する。

- **2026-03 · [Trust-Aware Routing for Distributed Generative AI Inference at the Edge](2026-2603.28622-trust-aware-routing-for-distributed-generative-ai-inference-at-the-edge.md)**  
  実装：[✓](https://github.com/anonymous-123qh/g-trac/tree/main/deployment) ・ リポジトリ内被引用：0  
  G-TRAC（Generative Trust-Aware Routing and 適応的 Chaining）は、単一ノードでは実行できない生成AIモデルを複数の異種エッジ端末へ分割配置する際、どの端末の列を通して推論を進めるかを決める協調制御方式である。

- **2026-03 · [MobileLLM-Flash: Latency-Guided On-Device LLM Design for Industry Scale Deployment](2026-2603.15954-mobilellm-flash-latency-guided-on-device-llm-design-for-industry-scale-d.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  携帯電話の実測遅延を探索へ直接組み込む枝刈り型の構造探索で、浅く広く注意を間引いた端末向けモデル族を作り、入力処理1.8倍・生成1.6倍の高速化と品質向上を両立した。

- **2026-03 · [FlexServe: A Fast and Secure LLM Serving System for Mobile Devices with Flexible Resource Isolation](2026-2603.09046-flexserve-secure-mobile-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TrustZoneのアクセス権と資源管理権を分離してページ単位セキュアメモリと切替可能NPUを実現し、LLM向けキャッシュ・回収・先読みでセキュア端末内推論の起動遅延を大幅に削減する。

- **2026-03 · [ConsRoute: Consistency-Aware Adaptive Query Routing for Cloud-Edge-Device Large Language Models](2026-2603.21237-consroute-consistency-aware-adaptive-query-routing-for-cloud-edge-device.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  応答間の意味的一致を教師信号にし、デバイス側モデルのプリフィル隠れ状態を再利用する軽量予測器とクラスタ別ベイズ最適化閾値で、3層協調推論のルーティングを適応化した研究。

- **2026-02 · [QuickGrasp: Responsive Video-Language Querying Service via Accelerated Tokenization and Edge-Augmented Inference](2026-2603.00126-quickgrasp-responsive-video-language-querying-service-via-accelerated-to.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末の小規模な視覚言語モデルを優先し、信頼度が足りない質問だけ視覚トークンを共有してエッジの大規模モデルへ送る構成と、キーフレーム整列の高速トークン化、バンディットによるトークン密度選択を組み合わせ、長動画で応答遅延を最大12.8倍下げながら大規模モデル並みの精度を保つ動画質問応答の提供系。

- **2026-02 · [Quantization-Aware Collaborative Inference for Large Embodied AI Models](2026-2602.13052-quantization-aware-collaborative-inference-for-large-embodied-ai-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末側の計算能力・電池・通信帯域には制約があるため、端末側モデルを量子化して計算負荷を減らすことが有効である。実機はJetson AGX Orin 64GBとRTX 3090を2枚備えたサーバを無線LANで接続した構成で、遅延制約が強いと高周波数、エネルギー制約が強いと低周波数が有利になることを確認する。

- **2026-01 · [SwiftKV: An Edge-Oriented Attention Algorithm and Multi-Head Accelerator for Fast, Efficient LLM Decoding](2026-2601.10953-swiftkv-an-edge-oriented-attention-algorithm-and-multi-head-accelerator-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVキャッシュを一度だけ走査する単一パス注意と、注意と行列ベクトル積を同じ演算器で担う多ヘッドFPGA加速器で、エッジデコードの注意遅延を43パーセントから3.19パーセントへ下げる。

- **2026-01 · [Advancing Model Refinement: Muon-Optimized Distillation and Quantization for LLM Deployment](2026-2601.09865-advancing-model-refinement-muon-optimized-distillation-and-quantization-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  合成データ、蒸留、LoRA、ハイパーパラメータ最適化、GPTQ量子化を束ねたエッジ配備パイプラインと最適化器比較の検証を提示したが、第2版の著者訂正で中核の精度知見が実験基盤の不備により無効と明示された論文。信頼できるのはメモリと遅延の実測のみである。

- **2025-12 · [PerCache: Predictive Hierarchical Cache for RAG Applications on Mobile Devices](2025-2601.11553-percache-predictive-hierarchical-cache-for-rag-applications-on-mobile-de.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  質問と回答の組と知識断片の中間テンソルを2層に貯め、空き時間に将来の質問を予測して先回りで満たす携帯向け階層キャッシュで、PerLTQAの平均遅延を最も強い比較対象の64.94秒から23.73秒へ63.5%削減した。

- **2025-12 · [Input-Adaptive Visual Preprocessing for Efficient Fast Vision-Language Model Inference](2025-2512.20839-input-adaptive-visual-preprocessing-for-efficient-fast-vision-language-m.md)**  
  実装：[✓](https://github.com/kmdavidds/mlfastlm) ・ リポジトリ内被引用：0  
  画像の複雑さに応じて解像度と切り抜きを変える前処理をFastVLMの前に置き、モデル無変更で視覚トークンを55パーセント超、画像あたり推論時間を50パーセント超減らす軽量な効率化。

- **2025-12 · [AutoNeural: Co-Designing Vision-Language Models for NPU Inference](2025-2512.02924-autoneural-co-designing-vision-language-models-for-npu-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  視覚エンコーダを深さ方向分離畳み込みのMobileNet系へ、言語バックボーンをTransformerと状態空間層のハイブリッドへ置き換え、量子化の脆さとKVキャッシュのメモリ入出力を構造から消すことで、車載NPU上で14倍の低遅延と7倍低い量子化誤差を実機で示したNPUネイティブな視覚言語モデルの共同設計。

- **2025-12 · [Atom: Efficient On-Device Video-Language Pipelines Through Modular Reuse](2025-2512.17108-atom-efficient-on-device-video-language-pipelines-through-modular-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  動画言語パイプラインをエンコーダと共有言語デコーダのモジュールへ分解し、常駐再利用とクリップ並列で再読込と直列実行を消すことで、スマートフォン上のエンドツーエンド遅延を27〜33%削減しつつピークメモリ増を約40MBに抑えるオンデバイス実行システム。

### 2年前（2024-12〜2025-11）

- **2025-05 · [EdgeShard: Efficient LLM Inference via Collaborative Edge Computing](2025-d6d0a70f5bc4-edgeshard-efficient-llm-inference-via-collaborative-edge-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：35  
  既存の端末単独実行では重みが端末メモリに収まらず、端末とクラウドを二分割する方式では低帯域回線が遅延を支配する。著者らの実機試験では、Llama2-7Bに対し端末単独の140.34ミリ秒/トークン、24.36トークン/秒から、75.88ミリ秒/トークン、52.45トークン/秒へ改善した。

- **2025-10 · [Characterizing Mobile SoC for Accelerating Heterogeneous LLM Inference](2025-d56c08fb1c58-characterizing-mobile-soc-for-accelerating-heterogeneous-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  HeteroInferは、携帯端末のシステムオンチップ（システム-on-Chip; SoC）に同居するGPUとニューラル処理装置（Neural Processing Unit; NPU）を同時利用し、大規模言語モデル（LLM）の前処理と自己回帰復号を高速化する推論基盤である。

- **2025-09 · [Scaling LLM Test-Time Compute with Mobile NPU on Smartphones](2025-2509.23324-scaling-llm-test-time-compute-with-mobile-npu-on-smartphones.md)**  
  実装：[✓](https://github.com/haozixu/llama.cpp-npu) ・ リポジトリ内被引用：18  
  Hexagon NPUの復号時に遊休しやすい行列演算器を、並列テスト時計算へ転用する。4ビット細粒度タイル量子化とルックアップテーブル（Lookup Table; LUT）演算により、混合精度GEMM最大19.0倍、Softmax最大2.2倍を報告する。

- **2025-06 · [Mixture of Cache-Conditional Experts for Efficient Mobile Device Inference](2025-2412.00099-mixture-of-cache-conditional-experts-for-efficient-mobile-device-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  提案するキャッシュ優先ルーティング（Cache-Prior ルーティング）は、既存ルータのスコアに「DRAM内に既にある専門家」への加算項を導入し、上位K個の専門家の選択を変更する。

- **2025-10 · [Elastic On-Device LLM Service](2025-2409.09071-elastic-on-device-llm-service.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  端末内で一つの大規模言語モデルを複数アプリから共用する場合、画面操作エージェント、チャット、バックグラウンド要約は、それぞれ異なる遅延目標を要求する。ElastiLMは、この二つの調整軸を同じ要求制御に統合する。これは生成速度が10.45%増えたという意味ではなく、指定された遅延制約を守った要求の正答率の絶対差である。

- **2025-08 · [ShadowNPU: System and Algorithm Co-design for NPU-Centric On-Device LLM Inference](2025-2508.16703-shadownpu-system-and-algorithm-co-design-for-npu-centric-on-device-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  NPUで重要トークン位置だけを近似推定し、高精度疎注意をCPU/GPUへ限定してパイプライン化することで、モバイルLLMの注意フォールバックを削減する。

- **2025-06 · [MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices](2025-2506.10443-mnn-llm-mobile-inference-engine.md)**  
  実装：[✓](https://github.com/alibaba/MNN) ・ リポジトリ内被引用：9  
  DRAMとFlashの階層利用、役割別量子化、CPU/GPU別データ配置と負荷分散を統合し、スマートフォン上のLLM推論を高速・省メモリ化する。

- **2025-07 · [DSSD: Efficient Edge-Device LLM Deployment and Collaborative Inference via Distributed Split Speculative Decoding](2025-2507.12000-dssd-efficient-edge-device-llm-deployment-and-collaborative-inference.md)**  
  実装：[✓](https://github.com/JasonNing96/DSSD-Efficient-Edge-Computing) ・ リポジトリ内被引用：7  
  端末で大規模言語モデルを動かすにはメモリ、演算能力、電力が不足しやすい。基地局やエッジサーバに大型モデルを置けば演算資源は確保できるが、ネットワーク往復時間と帯域が生成遅延へ加わる。ただしモデル対やドラフト長によっては通常の大型モデル推論より遅い条件があり、通信を減らせば無条件に高速化するわけではない。

- **2025-04 · [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  D²MoEは、端末上でMoEを動かすときの専門家の重みをどの精度で読み込むかと、SSDなどからの重み読込とGPU計算をどう重ねるかを同時に設計する。二重ルーティングは専門家IDとビット幅の二つの選択を意味し、トークンを二回生成する方式ではない。

- **2025-10 · [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  小基地局に下書きモデル、大基地局に対象モデルを置き、要求の下書き・検証を二段パイプライン化し、無線帯域・バッチ境界・投機長を調整して往復遅延を減らす方式。

- **2025-04 · [Scaling Up On-Device LLMs via Active-Weight Swapping Between DRAM and Flash](2025-2504.08378-scaling-up-on-device-llms-via-active-weight-swapping-between-dram-and-fl.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  スマートフォン上で大規模言語モデルを動かす際、モデルの全重みをDRAMに置けないことが最大の制約になる。さらに現在の層の活性化ベクトルから数層先の活性重みを予測して先読みし、複数層の重みをフラッシュ上で近接配置する。

- **2025-06 · [CLONE: Customizing LLMs for Efficient Latency-Aware Inference at the Edge](2025-2506.02847-clone-customizing-llms-for-efficient-latency-aware-inference-at-the-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  装置に合わせた生成型の枝刈り整形と、要求ごとの適応の混合、層境界ごとの学習型の電圧・周波数制御を束ねた端末向け協調設計で、実測で最大11.92倍の高速化と最大7.36倍のエネルギー削減を示した。

- **2025-01 · [MoE²: Optimizing Collaborative Inference for Edge Large Language Models](2025-2501.09410-moe-optimizing-collaborative-inference-for-edge-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  MoE²（Mixture-of-Edge-Experts）は、単一の大規模言語モデル内部に小さな専門家層を並べる方式ではなく、独立した端末・サーバーに配置された複数の大規模言語モデルそのものを専門家として扱う協調推論基盤である。

- **2025-08 · [End-to-End On-Device Quantization-Aware Training for LLMs at Inference Cost](2025-2509.00031-end-to-end-on-device-quantization-aware-training-for-llms-at-inference-c.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ZeroQATは、推論時に使う低ビット重み・活性値を、学習時にも実際に量子化した状態で評価し、その結果に基づいて量子化認識学習を行う方法である。

- **2025-03 · [Optimal Expert Selection for Distributed Mixture-of-Experts at the Wireless Edge](2025-2503.13421-optimal-expert-selection-for-distributed-mixture-of-experts-at-the-wireless-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案方式の中核は、品質制約の下で消費エネルギーが小さい専門家集合を探す動的専門家選択（動的 専門家 Selection; DES）と、無線資源割当まで結合した共同専門家・副搬送波割当（Joint 専門家 and Subcarrier Allocation; JESA）である。

- **2025-10 · [ECVL-ROUTER: Scenario-Aware Routing for Vision-Language Models](2025-2510.27256-ecvl-router-scenario-aware-routing-for-vision-language-models.md)**  
  実装：[✓](https://anonymous.4open.science/r/ECVL-Router-977D) ・ リポジトリ内被引用：2  
  大規模なクラウドVLMは難しい質問に強い反面、すべての質問をクラウドで処理すると、単純な画像説明にも大きなモデルの計算費用と応答待ち時間がかかる。そこで、問い合わせごとに処理先を決める「モデルルーティング」が推論サービングの重要な設計問題になる。

- **2025-05 · [CE-LSLM: Efficient Large-Small Language Model Inference and Communication via Cloud-Edge Collaboration](2025-2505.14085-ce-lslm-efficient-large-small-language-model-inference-and-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  クラウドに大きな言語モデル（LLM）を置き、端末やエッジに小さな言語モデル（SLM）を置く場合、単純な分担には二つの問題がある。システムプロンプトのように複数ユーザー間で再利用可能な文脈と、個人の質問のようにローカルに保持すべき入力を分離できれば、両者の妥協点を作れる。

- **2025-10 · [MoBiLE: Efficient Mixture-of-Experts Inference on Consumer GPU with Mixture of Big Little Experts](2025-2510.12357-mobile-efficient-mixture-of-experts-inference-on-consumer-gpu-with-mixtu.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  MoBiLEは、総パラメータがGPUメモリに収まらないMixture-of-Experts（MoE）言語モデルを、消費者向けGPUとCPU DRAMの組合せで実行するときの転送ボトルネックを削減する推論方式である。

- **2025-08 · [Camel: Energy-Aware LLM Inference on Resource-Constrained Devices](2025-2508.09173-camel-energy-aware-llm-inference-on-resource-constrained-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  エッジ推論のGPU周波数とバッチサイズの組み合わせを多腕バンディットとして探索し、事後分布の更新で最適構成を素早く見つけることで、Jetson AGX Orin上でエネルギー遅延積を既定構成比12.4から29.9パーセント下げるエネルギー管理の枠組み。

- **2025-05 · [Scaling On-Device GPU Inference for Large Generative Models](2025-2505.00232-scaling-on-device-gpu-inference-for-large-generative-models.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  テンソル仮想化で論理配置と物理GPUオブジェクトを分離し、デバイス特化や段階配慮型最適化を組み合わせるML Driftにより、従来より10倍から100倍大きな生成モデルを端末GPUで動かし、既存エンジン比で桁違いの性能を示す。

- **2025-05 · [RAP: Runtime Adaptive Pruning for LLM Inference](2025-2505.17138-rap-runtime-adaptive-pruning-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  固定の剪定率でモデル重みだけを削る方式は、短い入力では過剰に品質を落とし、長い入力ではKVキャッシュの増加を補えないことがある。

- **2025-04 · [Mosaic: Composite Projection Pruning for Resource-efficient LLMs](2025-2504.06323-mosaic-composite-projection-pruning-for-resource-efficient-llms.md)**  
  実装：[✓](https://github.com/blessonvar/Mosaic) ・ リポジトリ内被引用：1  
  Mosaicは、事前学習済み大規模言語モデルを限られたメモリの装置へ配置するため、Transformerの各線形射影に異なる削減率を割り当てる方式である。通常の非構造化枝刈りは重みを零化するため品質を比較的保てるが、重み行列の寸法を縮めない限り汎用の密行列演算ではメモリや時間の削減に結びつきにくい。

- **2025-11 · [Why Should the Server Do It All?: A Scalable, Versatile, and Model-Agnostic Framework for Server-Light DNN Inference over Massively Distributed Clients via Training-Free Intermediate Feature Compression](2025-2511.11608-why-should-the-server-do-it-all-a-scalable-versatile-and-model-agnostic-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分割推論の中間特徴を非対称トップK、大きさ分割、適応ビット量子化の3段で正確な比率に圧縮し、計算をエッジへ寄せることで、上り通信を最大10分の1、サーバGPU時間を最大4.4分の1にし、精度低下を概ね3ポイント以内に収めた学習不要の分散推論基盤。

- **2025-11 · [Joint Partitioning and Placement of Foundation Models for Real-Time Edge AI](2025-2512.01039-joint-partitioning-and-placement-of-foundation-models-for-real-time-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  基盤モデルの層分割とエッジノードへの配置を実行時に決め直す適応型分割推論の枠組みを定式化し、想定シナリオの期待値として帯域20Mb/sで遅延を500ミリ秒から200ミリ秒へ下げる見積もりを示したオーケストレーション研究。

- **2025-11 · [Federated Attention: A Distributed Paradigm for Collaborative LLM Inference over Edge Networks](2025-2511.02647-federated-attention-a-distributed-paradigm-for-collaborative-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Federated 注意機構（FedAttn）は、この協調推論を注意機構の段階で分散する方式として提案された。

- **2025-11 · [DisCEdge: Distributed Context Management for Large Language Models at the Edge](2025-2511.22599-discedge-distributed-context-management-for-large-language-models-at-the.md)**  
  実装：[✓](https://github.com/ChaosRez/llm-context-management) ・ リポジトリ内被引用：0  
  会話文脈をトークン列としてエッジノード間に複製し、ターンカウンタで版を照合して整合性を保つ分散文脈管理 DisCEdge を実装し、生テキスト方式より応答の中央値を最大14.46パーセント短縮し、クライアント保持方式より要求サイズの中央値を90パーセント減らした実機研究。

- **2025-10 · [TeLLMe v2: An Efficient End-to-End Ternary LLM Prefill and Decode Accelerator with Table-Lookup Matmul on Edge FPGAs](2025-2510.15926-tellme-v2-an-efficient-end-to-end-ternary-llm-prefill-and-decode-acceler.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値LLMの行列積を、活性値グループから作る参照表の引き換えで実行し、URAMに合わせた重み配置と逆順プリフィル注意でプリフィルまで含めて加速するエッジFPGAアクセラレータで、KV260上で4.8Wのままデコード25トークン毎秒とTTFT 0.45〜0.96秒を実機で示した。

- **2025-10 · [ShishuLM: Achieving Optimal and Efficient Parameterization with Low Attention Transformer Models](2025-2510.13860-shishulm-achieving-optimal-and-efficient-parameterization-with-low-atten.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  後半層の注意の冗長性に基づき、上位層を全結合だけのブロックへ置き換えて事前学習する効率的な言語モデル。注意を約3分の2残す構成で土台と同等の品質と生成効率の改善を示し、重み共有でさらに容量を削る。

- **2025-09 · [Context-Driven Performance Modeling for Causal Inference Operators on Neural Processing Units](2025-2509.25155-context-driven-performance-modeling-for-causal-inference-operators-on-ne.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、長い文脈を扱う言語モデルの演算を小型端末の神経処理装置（NPU）へ移したとき、理論計算量が小さい方式ほど速いとは限らない問題を検証する。論文の表VIでは長文条件の標準因果注意が停止率96.7%、キャッシュ効率7.7%であるのに対し、Toeplitzは別の長さ条件で停止率36.4%、キャッシュ効率87.9%を示す。

- **2025-08 · [Efficient Edge LLMs Deployment via HessianAware Quantization and CPU GPU Collaborative](2025-2508.07329-efficient-edge-llms-deployment-via-hessianaware-quantization-and-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、GPUメモリが限られた端末でMixture-of-Experts（MoE）モデルを実行する際の二つの問題を同時に扱う。第一に、重みだけでなく活性値も整数8ビットへ量子化すると、少数の極端な活性値が量子化範囲を支配し、精度が悪化し得る。

- **2025-07 · [Prism: Communication-efficient Distributed Inference for Foundation Models at Edge](2025-2507.12145-prism-communication-efficient-distributed-inference-for-foundation-model.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  位置方向に分割した分散Transformer推論で、デバイス間へ送る中間特徴を区間平均へ圧縮し、重複を数えるスケーリング付きソフトマックスでキー・バリュー計算の重複まで消すことで、BERTでは通信を最大99.2パーセント減らしながらGLUE精度をほぼ保ったエッジ分散推論方式。

- **2025-06 · [Ubiquitous memory augmentation via mobile multimodal embedding system](2025-5504da64243a-ubiquitous-memory-augmentation-via-mobile-multimodal-embedding-system.md)**  
  実装：[✓](https://github.com/caidongqi/Mobile-Search-Engine/tree/pc) ・ リポジトリ内被引用：0  
  端末上のマルチモーダル埋め込みを早期終了の粗い埋め込みで肩代わりし、検索時に残りの層で仕上げるReminisceは、終了予測・共有LoRAによる癒合・投機的な細粒度検索の3設計で、精度低下を抑えながら平均12.4倍のスループットと大幅な省電力を達成する。

- **2025-06 · [TensorSLM: Energy-efficient Embedding Compression of Sub-billion Parameter Language Models on Low-end Devices](2025-2506.13514-tensorslm-energy-efficient-embedding-compression-of-sub-billion-paramete.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  トークン埋め込みを1本ずつテンソルトレイン分解して行列積状態で保存する学習不要の圧縮で、埋め込み層を約2倍圧縮しても性能を概ね保ち、Raspberry Pi 5級デバイスでの推論エネルギーを推定で約半分にした。

- **2025-06 · [HAPE: Hardware-Aware LLM Pruning For Efficient On-Device Inference Optimization](2025-3b8e234e37c9-hape-hardware-aware-llm-pruning-for-efficient-on-device-inference-optimi.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎率ではなく実機の遅延感度で重要度を決め、ブロック内の動的疎率と枝刈り中の疎コンパイルを組み合わせ、学習なしで端末向けにLLMを枝刈りするハードウェア考慮型の枠組み。

- **2025-05 · [ASTRA: Communication-Efficient Acceleration for Multi-Device Transformer Inference](2025-2505.19342-astra-communication-efficient-acceleration-for-multi-device-transformer-.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  帯域制約下の多デバイスTransformer推論で、シーケンス並列に混合精度アテンション（ローカルは全精度、非ローカルはベクトル量子化コードで送信）を組み合わせ、ノイズ増強量子化と分散クラストークンで精度を守りながら通信量を最大2457.6分の1に圧縮した研究。

- **2025-02 · [CoSMoEs: Compact Sparse Mixture of Experts](2025-2503.00245-cosmoes-compact-sparse-mixture-of-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末規模で計算量と総パラメータを揃えた公平な比較によりMoEが密モデルを上回ることを示し、重み分解エキスパートと、入れ替えを6倍減らすブロック単位選択損失でオフロード推論を1.5倍高速化した研究。

- **2025-01 · [Lightweight and Post-Training Structured Pruning for On-Device Large Lanaguage Models](2025-2501.15255-lightweight-and-post-training-structured-pruning-for-on-device-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMを小型GPUやエッジデバイスへ配置する際、重み行列の疎化だけでは、専用の疎行列カーネルがなければ実行速度を改善しにくい。層やニューロンを物理的に削除する構造化剪定は、通常の密行列演算でもパラメータ数・演算量を減らせるが、削除による品質低下が大きくなりやすい。削除後は、校正入力に対する元の線形出力を最小二乗問題で再構成するマスク調整を行う。

- **2024-12 · [Deploying Foundation Model Powered Agent Services: A Survey](2024-2412.13437-deploying-foundation-model-powered-agent-services-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、基盤モデル（foundation モデル）を使うエージェントサービスを、端末、エッジ、クラウドにまたがる異種資源上へ配備する際のシステム技術を整理した文献サーベイである。

### 3年前（2023-12〜2024-11）

- **2024-06 · [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)**  
  実装：[✓](https://github.com/Tiiny-AI/PowerInfer) ・ リポジトリ内被引用：83  
  PowerInfer-2は、利用頻度を測った重みだけをスマホの高速メモリへ置き、残りをUFSから読みつつCPU・NPU計算と重ねて、容量不足と読出し待ちを減らす方式。

- **2024-08 · [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：39  
  SwapMoEは、全専門家をメモリに置けない問題に対し、層ごとの仮想枠へ入力で選ばれた専門家重みを入れ替え、メモリ容量と重み転送を抑える方式。

- **2024-07 · [Mobile Edge Intelligence for Large Language Models: A Contemporary Survey](2024-2407.18921-mobile-edge-intelligence-for-large-language-models-a-contemporary-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：35  
  本論文は、LLM向けの移動体エッジ知能をMEI4LLMと呼び、その設計空間を通信・計算・記憶の三資源で整理する。

- **2024-03 · [MELTing point: Mobile Evaluation of Language Transformers](2024-2403.12844-melting-point-mobile-evaluation-of-language-transformers.md)**  
  実装：[✓](https://github.com/brave-experiments/MELT-public) ・ リポジトリ内被引用：16  
  モデル読込み中の操作不能、端末の発熱、連続実行での動作周波数低下、バッテリー消費、量子化による回答品質の劣化も重要である。原著の評価条件では4ビットモデルの生成スループットが3ビットモデルより平均24.77%高かった。

- **2024-01 · [BlockFFN: Towards End-Side Acceleration-Friendly Mixture-of-Experts with Chunk-Level Activation Sparsity](2025-2507.08771-blockffn-towards-end-side-acceleration-friendly-mixture-of-experts.md)**  
  実装：[✓](https://github.com/thunlp/BlockFFN) ・ リポジトリ内被引用：5  
  要点: BlockFFNは、混合専門家（Mixture-of-Experts; MoE）の「1トークン当たりは疎でも、複数トークンをまとめるとほぼ全専門家が必要になる」という弱点を狙う。

- **2024-08 · [Squid: Long Context as a New Modality for Energy-Efficient On-Device Language Models](2024-2408.15518-squid-long-context-as-a-new-modality-for-energy-efficient-on-device-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  Squidは、長文脈を扱う言語モデルの入力処理を小型モデルへ移し、回答を生成する大型モデルには短い潜在表現だけを渡す方式である。原著は単一のNVIDIA A100 80GB上で、直接Qwen2-7Bへ入力する方式の平均推論時間20.71秒に対してSquidは4.32秒、比率4.79倍を報告する。

- **2024-08 · [FactorLLM: Factorizing Knowledge via Mixture of Experts for Large Language Models](2024-2408.11855-factorllm-factorizing-knowledge-via-mixture-of-experts-for-large-languag.md)**  
  実装：[✓](https://github.com/zhenwuweihe/FactorLLM) ・ リポジトリ内被引用：1  
  FactorLLMは、学習済みの密な言語モデルのFeed-順伝播 Network（フィードフォワード層）を複数の小さな専門家へ分割し、各トークンに必要な専門家だけを実行することで、推論時のフィードフォワード層演算量を削減する手法である。

- **2024-07 · [Co-Designing Binarized Transformer and Hardware Accelerator for Efficient End-to-End Edge Deployment](2024-2407.12070-co-designing-binarized-transformer-and-hardware-accelerator-for-efficien.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  二値化TransformerのモデルBMTと専用アクセラレータBATを設計空間探索で共同最適化し、GLUEの精度をほぼ保ったままFPGA上で先行アクセラレータ比スループット最大49.37倍とエネルギー効率最大88.53倍を実測したエッジ向け共同設計。

- **2024-06 · [Crayon: Customized On-Device LLM via Instant Adapter Blending and Edge-Server Hybrid Inference](2024-2406.07007-crayon-customized-on-device-llm-via-instant-adapter-blending-and-edge-se.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  基礎LoRAのプールを共同学習しておき、利用者の少量の例との類似度で即座に合成してカスタムLoRAを作ることで端末内学習なしにカスタマイズし、2割だけサーバーへ逃がすハイブリッドと合わせてMMLU平均を31.0から47.6パーセントへ上げた研究。

- **2024-02 · [Merino: Entropy-driven Design for Generative Language Models on IoT Devices](2024-2403.07921-merino-entropy-driven-design-for-generative-language-models-on-iot-devic.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み行列の特異値エントロピーを有効性制約付きで最大化する数理計画により、学習なしでモバイル向け生成言語モデルの建築を決め、OPT-350Mと同等以上の精度をパラメータ82%削減で達成しJetson Nanoで4.9倍高速なモデル群MeRinoを設計した研究。

### 4年前（2022-12〜2023-11）

- **2023-08 · [EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices](2023-2308.14352-edgemoe.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/mllm) ・ リポジトリ内被引用：69  
  MoE エキスパートを外部ストレージ化し、エキスパート別混合量子化と活性相関に基づく先読み・キャッシュでモバイル推論のI/O律速を緩和する。

- **2023-09 · [LLMCad: Fast and Scalable On-device Large Language Model Inference](2023-2309.04255-llmcad-fast-and-scalable-on-device-large-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：31  
  端末で言語モデルを動かす場合、モデル重みがメモリ容量を超えると、生成のたびにストレージから重みを読み直すことがある。原著の構成は三つの機構からなる。Jetson TX2/Orin NXとAndroidスマートフォンで、標準の大型モデル単独生成に対してトークン当たり平均時間をIoT端末で2.9〜9.3倍、スマートフォンで3.47〜4.67倍短縮したと報告する。

### 5年前（2021-12〜2022-11）

- **2022-06 · [Language model compression with weighted low-rank factorization](2022-2207.00112-language-model-compression-with-weighted-low-rank-factorization.md)**  
  実装：✓ ・ リポジトリ内被引用：61  
  本論文は、事前学習・タスク別微調整を終えた言語モデルの大きな線形層を、低ランクの二つの行列に置き換える圧縮方法を扱う。著者らは、特異値が小さい成分を除去しても必ずしもタスクへの影響が小さくないことをBERTの実験で示した。

- **2022-03 · [Overcoming Oscillations in Quantization-Aware Training](2022-2203.11086-overcoming-oscillations-in-quantization-aware-training.md)**  
  実装：[✓](https://github.com/qualcomm-ai-research/oscillations-qat) ・ リポジトリ内被引用：9  
  量子化対応学習（Quantization-Aware 学習; QAT）は、訓練中に低ビットの重みと活性を模擬し、推論時に使う整数化済みネットワークの精度を回復する手法である。ImageNetのMobileNetV3-Smallでは重み・活性3/3ビットのLSQ基準52.0%に対し、減衰59.0%、凍結58.9%を報告する。

- **2022-07 · [STI: Turbocharge NLP Inference at the Edge via Elastic Pipelining](2022-2207.05022-sti-turbocharge-nlp-inference-at-the-edge-via-elastic-pipelining.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  Transformerをシャード単位で深さ・幅・ビット幅を調整できる弾力的なサブモデルにし、重要度順に入出力予算を配るパイプライン計画と小さなプリロードで、モバイル端末の数百ミリ秒目標を満たしながら常駐方式比でメモリを平均122倍削減する推論エンジン。

### 6年前（2020-12〜2021-11）

- **2021-07 · [FLAT: An Optimized Dataflow for Mitigating Attention Performance Bottlenecks](2021-2107.06419-flat-an-optimized-dataflow-for-mitigating-attention-performance-bottlene.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  注意の中間テンソルをオフチップへ書き戻さず、ロジットから適用までを行単位に融合とタイル化で処理し、メモリフットプリントを二乗から線形へ落として長系列でもアクセラレータを動かすデータフロー最適化。

### 7年前（2019-12〜2020-11）

- **2020-11 · [EdgeBERT: Sentence-Level Energy Optimizations for Latency-Aware Multi-Task NLP Inference](2020-2011.14203-edgebert-sentence-level-energy-optimizations-for-latency-aware-multi-tas.md)**  
  実装：✓ ・ リポジトリ内被引用：21  
  EdgeBERTは、資源制約の厳しい端末上で、自然言語分類を決められた応答時間内に実行しながら消費エネルギーを最小化するための、アルゴリズムと回路の共同設計である。これらは別々の比較であり、同一実行条件の速度改善倍率でも、LLMのトークン生成性能でもない（原著要旨、§8.2）。

- **2020-07 · [HAT: Hardware-Aware Transformers for Efficient Natural Language Processing](2020-2005.14187-hat-hardware-aware-transformers-for-efficient-natural-language-processin.md)**  
  実装：[✓](https://github.com/mit-han-lab/hardware-aware-transformers) ・ リポジトリ内被引用：16  
  Transformerの推論速度を改善するため、パラメータ数や浮動小数点演算回数（FLOPs）を減らすことは一般的だが、演算量が同じモデルでも機器によって実測遅延は大きく異なる。HAT（Hardware-Aware Transformers）はこの差を設計時に扱う。
<!-- survey:auto:end -->
