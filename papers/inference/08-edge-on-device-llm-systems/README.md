# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（83本）

[この系統だけ検索](https://uni042.github.io/llm-paper-summary/inference/08-edge-on-device-llm-systems/)

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-05 · [An Efficient Context Management System for On-Device LLMaaS (Libra; preprint: LLM as a System Service on Mobile Devices)](2024-2403.11805-llm-as-a-system-service-on-mobile-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  アプリを切り替えるたびに履歴全体を再計算するか、ディスクへ退避したKVを読み戻すと、次の生成開始までの待ち時間が長くなる。正式出版版の実機評価では、一律8ビット圧縮を伴うチャンク退避方式に対し、コンテキスト切替遅延を最大20倍、平均9.7倍削減した。

- **2026-04 · [MemExplorer: Navigating the Heterogeneous Memory Design Space for Agentic Inference NPUs](2026-2604.16007-memexplorer-navigating-the-heterogeneous-memory-design-space-for-agentic-inference-npus.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  SRAM/HBM/LPDDR/GDDR/HBFを統一モデル化し、プリフィル/デコードNPUとメモリ階層を共同探索して、基準NPU比でプリフィル最大2.3倍・デコード最大1.93倍の電力効率を得る。

- **2026-08 · [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)**  
  実装：[✓](https://github.com/FlashML-org/FreeToken) ・ リポジトリ内被引用：2  
  FreeTokenは、混合専門家モデル（Mixture of エキスパート、MoE）の全専門家重みがGPUメモリに収まらない場合に、GPU・CPU・主記憶・PCIeを一つの推論基盤として使うローカル配信システムである。

- **2026-03 · [FastTTS: Accelerating Test-Time Scaling for Edge LLM Reasoning](2026-2509.00195-fasttts-accelerating-test-time-scaling-for-edge-llm-reasoning.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  生成モデルと過程評価モデルを1枚のGPUに載せる場合には、両者へのKV領域の配分も難しい。FastTTSはこの三つの資源問題に対応する配信システムである。論文の主評価は単一のRTX 4090（24GB）で、AIME2024とAMC2023の数学問題を対象に、複数の生成器・検証器の組合せと探索枝数を比較する。

- **2026-06 · [VLMCache: Efficient On-Device Vision-Language Model Inference](2026-35c4f3816b37-vlmcache-efficient-on-device-vision-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  VLMCacheは、UIエージェントや視覚質問応答のように連続フレームを処理する視覚言語モデルで、毎フレームの視覚入力を最初から入力処理するため初回トークン時間が長くなる問題を扱う。提案法は安定した背景ブロックと変化した前景ブロックを意味的に分離し、背景を再利用可能なKVキャッシュ接頭辞として並べ、前景だけを再計算する。

- **2026-06 · [Achieving Cloud-Grade SLOs for Local Mixture-of-Experts Inference through CPU-GPU Hybrid Design](2026-2606.10493-achieving-cloud-grade-slos-for-local-mixture-of-experts-inference-through-cpu-gpu-hybrid-design.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  巨大MoEのCPU計算・DRAM帯域律速に対し、入力処理は必要重みをGPUへ細粒度転送し、生成はCPU専門家計算とGPU注意を重ねて元精度を保つ方式。

- **2026-04 · [Efficient Mixture-of-Experts LLM Inference with Apple Silicon NPUs](2026-2604.18788-npumoe-apple-silicon-npu-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NPUMoEは、Apple NPUで動的な専門家選択を固定容量のグループと共有計算グラフへ変換し、頻出群を常駐させて小粒度実行とCPU同期を減らす方式。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-09 · [TierKV: Long-Context On-Device LLMs via Predictive Multi-Tier KV Caching](2026-2609.21172-tierkv-long-context-on-device-llms-via-predictive-multi-tier-kv-caching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  サーバーGPUと異なりスマートフォンはOSや他アプリとDRAMを共有し、メモリ上限を超えるとプロセスが強制終了される場合がある。TierKVは、キャッシュを正確なFP16形式の階層0、低ランク圧縮したDRAM内の階層1、フラッシュへ退避した階層2に分ける。

- **2026-09 · [PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling](2026-2609.09662-pelm-speculative-decoding-dvfs.md)**  
  実装：[✓](https://github.com/imec-nu/PELM) ・ リポジトリ内被引用：0  
  DVFS・自己投機的デコード・可変検証深度を深層強化学習で共同制御し、端末LLMで最大23.1%高速化・52.4%エネルギー削減を達成する。

- **2026-09 · [Partition-Aware Scheduling for Mobile Heterogeneous Inference Co-Execution](2026-2609.14213-partition-aware-scheduling-for-mobile-heterogeneous-inference-co-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  演算子のCPU-GPU分割とDAG上の実行順を共同最適化し、段階化・臨界度標本化・遅延予測による配備時反復探索でオフライン最適化に近いモバイル推論遅延を得る。

- **2026-09 · [OmniTide: Co-Designing Algorithms and Systems for Efficient On-Device Omni-LLM Streaming](2026-2609.34653-omnitide-co-designing-algorithms-and-systems-for-efficient-on-device-omn.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  各時刻の視覚・音声表現がLLMへ投入されるとKVキャッシュが累積し、後続の質問が過去の場面を参照できる一方、端末のメモリ容量と注意機構の計算量を圧迫する。主な検証では、Qwen2.5-Omni-3B/7Bの完全履歴との比較でストリームセッション時間が2.29〜2.40倍短くなり、StreamingBench正答率はほぼ同水準である。

- **2026-09 · [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スマートフォンで大規模言語モデル（LLM）を端末内実行すると、モデル重みだけでなく、会話履歴を再計算せずに利用する鍵・値キャッシュ（KVキャッシュ）が長時間RAMを占有する。mzCacheはこの問題を、端末での退避後の復帰時間を最小化するメモリ管理として扱う。

- **2026-09 · [MCSched: Memory-Controller-Aware Scheduling for Embodied LLM Workloads on NVIDIA Jetson](2026-fd0d3fa4e564-mcsched-memory-controller-aware-scheduling-for-embodied-llm-workloads-on-nvidia-jetson.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jetson統合メモリの隠れた帯域競合を監視し、締切危険時だけ背景LLMを一時停止してロボット処理を保護する軽量実行時スケジューラ。

- **2026-09 · [JustFit: 200K-Token LLM Serving on a 24 GiB Laptop with Just-in-Time State Management](2026-2609.17475-justfit-200k-token-llm-serving-on-a-24-gib-laptop-with-just-in-time-state-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  圧縮キー・バリュー実行、部品常駐切替、状態保持遷移を統合し、24 GiB機で27B級モデルの約213K位置の単一要求を完走する推論実行系。

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

- **2026-08 · [FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving](2026-2608.12932-flashdrive-flash-vision-language-action-inference-for-autonomous-driving.md)**  
  実装：[✓](https://github.com/z-lab/flashdrive) ・ リポジトリ内被引用：0  
  FlashDriveは、映像と鍵・値キャッシュ（KVキャッシュ）の時系列再利用、拡散モデルによる複数推論トークンの投機的生成、軌跡生成の中間速度再利用、CUDA実行グラフと演算融合、重み4ビット・活性値8ビット量子化を組み合わせる。最終構成では716.9→151.4ミリ秒、約4.7倍の実測高速化となる。

- **2026-08 · [EdgeXpert: An Edge Device for Memory-Efficient LLM Inference with Mixture-of-Experts and Speculative Decoding](2026-2608.05303-edgexpert-moe-speculative-decoding.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21481269) ・ リポジトリ内被引用：0  
  MoEと投機的復号の併用で増える専門家外部メモリアクセスを、プリフィルの共有専門家再利用とデコードの深さ認識チャネル統合で直接削減するエッジ向け協調設計。

- **2026-07 · [Transition-Aware Backend Dispatch for Edge LLM Inference](2026-2607.17415-transition-aware-backend-dispatch-for-edge-llm-inference.md)**  
  実装：[✓](https://anonymous.4open.science/r/power_aware_edge_inference_public-3B71/README.md) ・ リポジトリ内被引用：0  
  著者らは、対象演算の形状情報だけでなく、直前に選んだバックエンドも使い、演算が速くなる利得より切替費用が大きい場合は実行先を維持する選択方式を調べる。最良の静的バックエンドに比べた平均改善は遅延17.4%、エネルギー14.4%、エネルギー遅延積（EDP）28.5%だった。

- **2026-07 · [NPUsper: Eliminating Redundant Computation for Real-Time Whisper on Mobile NPUs](2026-2607.01108-npusper-eliminating-redundant-computation-for-real-time-whisper-on-mobil.md)**  
  実装：[✓](https://github.com/npusper/NPUsper) ・ リポジトリ内被引用：0  
  第一は、短い音声片に対するWhisperの幻覚を抑えるため、従来方式が毎回30秒近い入力を作り、既に処理した音声や無音埋めを再計算すること。

- **2026-07 · [HeteroMosaic: Exposing and Exploiting Heterogeneous Execution Opportunities for Energy-Efficient Edge LLM Inference](2026-2607.12839-heteromosaic-exposing-and-exploiting-heterogeneous-execution-opportuniti.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  近年の端末向けシステムオンチップ（SoC）には、CPU、内蔵画像処理装置（integrated GPU、iGPU）、神経処理装置（NPU）が同居し、同じ主記憶を共有するものがある。原著はAMD Ryzen AIの3機種を用いて、事前充填（プリフィル）で内蔵GPU単独比の平均速度向上率をそれぞれ約2.30倍、1.50倍、1.17倍と報告する。

- **2026-07 · [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ATSInferはテンソルごとのGPU常駐価値を実測し、CPU計算・PCIe転送・GPU計算を重ねて、VRAM不足時の転送待ちとCPU律速を減らす方式。

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

- **2026-06 · [E2LLM: Towards Efficient LLM Serving in Heterogeneous Edge/Fog Environments](2026-2606.03770-e2llm-heterogeneous-edge-fog-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  E2LLMは異種端末を入力処理用・生成用の複製群に分け、各群の連続層を端末へ再配置し、層・帯域・負荷の最遅段を抑える分散サービング方式。

- **2026-05 · [Quant.npu: Enabling Efficient Mobile NPU Inference for on-device LLMs via Fully Static Quantization](2026-2605.20295-quant-npu-enabling-efficient-mobile-npu-inference-for-on-device-llms-via.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  QualcommのHexagon系NPUは、整数行列積の高速化と規則的な量子化に適した専用回路を持つ。SM8650実機ではW4A8構成がExecuTorchのW4A16構成より最大15.1%低遅延となり、Llama-3.2-3B-InstructのW4A8では従来の回転方式より精度が大きく改善した。

- **2026-05 · [Lever：スマートフォン向けフラッシュ常駐LLMの投機的推論](2026-2605.16786-lever-speculative-llm-inference-on-smartphones.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OnePlus 12上の測定では、フラッシュ常駐標的モデルの検証時間のうち約78〜93%を入出力が占める条件があり、演算高速化だけではこの待ち時間を解消できない。Leverは投機的復号（投機的復号）を「サーバGPUで標的モデルの計算回数を減らす方式」ではなく、「フラッシュ常駐モデルの呼出し回数を複数トークンへ償却する方式」として再設計する。

- **2026-05 · [Keyword Matters: Unveiling the Energy Sensitivity of On-Device LLM Prompting](2026-2607.22568-keyword-matters-unveiling-the-energy-sensitivity-of-on-device-llm-prompt.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の推論効率化は量子化、剪定、推論カーネル、KVキャッシュ管理などモデル・実装側の変更が中心だった。論文で強調される18.5%、62.6%等は後者の相対値であり、別モデルや別端末の絶対エネルギーをそのまま比較した値ではない。

- **2026-05 · [Intelligence Delivery Network: Toward an Internet Architecture for the AI Age](2026-2605.13235-intelligence-delivery-network-toward-an-internet-architecture-for-the-ai.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  提案のIntelligence Delivery Network（IDN）は、CDNが人気コンテンツを需要の近くへ配置する発想を、AIの「能力」へ拡張する。

- **2026-05 · [CR^2: Cost-Aware Risk-Controlled Routing for Wireless Device-Edge LLM Inference](2026-2605.12001-cr-2-cost-aware-risk-controlled-routing-for-wireless-device-edge-llm-inf.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末上で小型の言語モデルを実行すれば、無線転送の待ち時間や通信電力を避けられる。CR²は、端末でローカル実行の可否を判定し、保留した問い合わせだけをエッジ側でモデル選択する二段階のルーティング方式である。

- **2026-05 · [CoMIC: Collaborative Memory and Insights Circulation for Long-Horizon LLM Agents in Cloud-Edge Systems](2026-2606.00756-comic-collaborative-memory-and-insights-circulation-for-long-horizon-llm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  学習済みモデルの能力を重み更新で強化する研究ではなく、記憶と処理配置の設計によって弱いエージェントの実行品質と文脈費用を改善するシステムである。

- **2026-05 · [CATS: Cascaded Adaptive Tree Speculation for Memory-Limited LLM Inference Acceleration](2026-2605.11186-cats-cascaded-adaptive-tree-speculation-for-memory-limited-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  通常の投機的デコード（投機的復号）は、小さなドラフトモデルが候補トークンを先に作り、大きな対象モデルが複数候補を一括検証することで、対象モデルの重み読み出しを複数トークンへ償却する。

- **2026-05 · [Agent-X: Full Pipeline Acceleration of On-device AI Agents](2026-2605.10380-agent-x-full-pipeline-acceleration-of-on-device-ai-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Agent-Xは、端末内で実行する大規模言語モデル（LLM）エージェントの遅延を、入力事前充填（プリフィル）と逐次生成（デコード）の両段階から削減する方式である。原著はTinyAgent-7BとMac mini M4 Proの実機を用い、エージェント全体で平均1.61倍の高速化を示す。

- **2026-04 · [SHIELD: A Segmented Hierarchical Memory Architecture for Energy-Efficient LLM Inference on Edge NPUs](2026-2604.07396-shield-segmented-hierarchical-memory-edge-npu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  SHIELDはBF16活性値を符号・指数・仮数と寿命で分け、短命な仮数のeDRAM更新を止め、長寿命KVは周期を延ばして保持エネルギーを減らす方式。

- **2026-04 · [EdgeFM: Efficient Edge Inference for Vision-Language Models](2026-2604.27476-edgefm-efficient-edge-inference-for-vision-language-models.md)**  
  実装：[✓](https://github.com/windog-labs/edge-fm-x) ・ リポジトリ内被引用：0  
  本研究は、産業用エッジ装置で視覚・言語モデル（Vision-Language モデル, VLM）と大規模言語モデル（Large Language モデル, LLM）を低遅延で動かすための推論基盤EdgeFMを提案する。

- **2026-04 · [EdgeFlow: Fast Cold Starts for LLMs on Mobile Devices](2026-2604.09083-edgeflow-fast-cold-starts-mobile-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  モバイルLLMのコールドスタートで浪費されるフラッシュ帯域を、重要度別の可変精度量子化・SIMD向け重み格納・CPU/NPU協調実行で削減し、同等精度条件の初回応答を最大4.07倍高速化する。

- **2026-04 · [A Unified Model and Document Representation for On-Device Retrieval-Augmented Generation](2026-2604.14403-a-unified-model-and-document-representation-for-on-device-retrieval-augm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  検索拡張生成（retrieval-augmented generation、RAG）をスマートフォンや小型計算機だけで動かす場合、サーバーへ個人文書を送らずに利用できる反面、二つのメモリ費用が問題となる。従来は検索用の埋め込みと生成用の圧縮文脈を別々に作ることが多く、文書ごとに二重の表現を保持する。

- **2026-03 · [Trust-Aware Routing for Distributed Generative AI Inference at the Edge](2026-2603.28622-trust-aware-routing-for-distributed-generative-ai-inference-at-the-edge.md)**  
  実装：[✓](https://github.com/anonymous-123qh/g-trac/tree/main/deployment) ・ リポジトリ内被引用：0  
  G-TRAC（Generative Trust-Aware Routing and 適応的 Chaining）は、単一ノードでは実行できない生成AIモデルを複数の異種エッジ端末へ分割配置する際、どの端末の列を通して推論を進めるかを決める協調制御方式である。

- **2026-03 · [FlexServe: A Fast and Secure LLM Serving System for Mobile Devices with Flexible Resource Isolation](2026-2603.09046-flexserve-secure-mobile-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TrustZoneのアクセス権と資源管理権を分離してページ単位セキュアメモリと切替可能NPUを実現し、LLM向けキャッシュ・回収・先読みでセキュア端末内推論の起動遅延を大幅に削減する。

- **2026-02 · [Quantization-Aware Collaborative Inference for Large Embodied AI Models](2026-2602.13052-quantization-aware-collaborative-inference-for-large-embodied-ai-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末側の計算能力・電池・通信帯域には制約があるため、端末側モデルを量子化して計算負荷を減らすことが有効である。実機はJetson AGX Orin 64GBとRTX 3090を2枚備えたサーバを無線LANで接続した構成で、遅延制約が強いと高周波数、エネルギー制約が強いと低周波数が有利になることを確認する。

- **2025-12 · [LOIP: Collaborative LLM Inference with Offloading-based Pipeline Parallelism on Edge Devices](2025-2512.21835-loip-collaborative-llm-inference-with-offloading-based-pipeline-parallel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LOIPは、端末ごとのメモリ容量・演算性能が異なる複数のNVIDIA Jetsonを連携させ、モデルのパラメータを量子化・枝刈りせずに推論するための実行基盤である。

- **2025-11 · [Federated Attention: A Distributed Paradigm for Collaborative LLM Inference over Edge Networks](2025-2511.02647-federated-attention-a-distributed-paradigm-for-collaborative-llm-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Federated 注意機構（FedAttn）は、この協調推論を注意機構の段階で分散する方式として提案された。

### 2年前（2024-11〜2025-10）

- **2025-05 · [EdgeShard: Efficient LLM Inference via Collaborative Edge Computing](2025-d6d0a70f5bc4-edgeshard-efficient-llm-inference-via-collaborative-edge-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  既存の端末単独実行では重みが端末メモリに収まらず、端末とクラウドを二分割する方式では低帯域回線が遅延を支配する。著者らの実機試験では、Llama2-7Bに対し端末単独の140.34ミリ秒/トークン、24.36トークン/秒から、75.88ミリ秒/トークン、52.45トークン/秒へ改善した。

- **2025-06 · [Mixture of Cache-Conditional Experts for Efficient Mobile Device Inference](2025-2412.00099-mixture-of-cache-conditional-experts-for-efficient-mobile-device-inferen.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  提案するキャッシュ優先ルーティング（Cache-Prior ルーティング）は、既存ルータのスコアに「DRAM内に既にある専門家」への加算項を導入し、上位K個の専門家の選択を変更する。

- **2025-10 · [Characterizing Mobile SoC for Accelerating Heterogeneous LLM Inference](2025-d56c08fb1c58-characterizing-mobile-soc-for-accelerating-heterogeneous-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：11  
  HeteroInferは、携帯端末のシステムオンチップ（システム-on-Chip; SoC）に同居するGPUとニューラル処理装置（Neural Processing Unit; NPU）を同時利用し、大規模言語モデル（LLM）の前処理と自己回帰復号を高速化する推論基盤である。

- **2025-09 · [Scaling LLM Test-Time Compute with Mobile NPU on Smartphones](2025-2509.23324-scaling-llm-test-time-compute-with-mobile-npu-on-smartphones.md)**  
  実装：[✓](https://github.com/haozixu/llama.cpp-npu) ・ リポジトリ内被引用：9  
  Hexagon NPUの復号時に遊休しやすい行列演算器を、並列テスト時計算へ転用する。4ビット細粒度タイル量子化とルックアップテーブル（Lookup Table; LUT）演算により、混合精度GEMM最大19.0倍、Softmax最大2.2倍を報告する。

- **2025-07 · [DSSD: Efficient Edge-Device LLM Deployment and Collaborative Inference via Distributed Split Speculative Decoding](2025-2507.12000-dssd-efficient-edge-device-llm-deployment-and-collaborative-inference.md)**  
  実装：[✓](https://github.com/JasonNing96/DSSD-Efficient-Edge-Computing) ・ リポジトリ内被引用：6  
  端末で大規模言語モデルを動かすにはメモリ、演算能力、電力が不足しやすい。基地局やエッジサーバに大型モデルを置けば演算資源は確保できるが、ネットワーク往復時間と帯域が生成遅延へ加わる。ただしモデル対やドラフト長によっては通常の大型モデル推論より遅い条件があり、通信を減らせば無条件に高速化するわけではない。

- **2025-06 · [MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices](2025-2506.10443-mnn-llm-mobile-inference-engine.md)**  
  実装：[✓](https://github.com/alibaba/MNN) ・ リポジトリ内被引用：6  
  DRAMとFlashの階層利用、役割別量子化、CPU/GPU別データ配置と負荷分散を統合し、スマートフォン上のLLM推論を高速・省メモリ化する。

- **2025-10 · [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  小基地局に下書きモデル、大基地局に対象モデルを置き、要求の下書き・検証を二段パイプライン化し、無線帯域・バッチ境界・投機長を調整して往復遅延を減らす方式。

- **2025-08 · [ShadowNPU: System and Algorithm Co-design for NPU-Centric On-Device LLM Inference](2025-2508.16703-shadownpu-system-and-algorithm-co-design-for-npu-centric-on-device-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  NPUで重要トークン位置だけを近似推定し、高精度疎注意をCPU/GPUへ限定してパイプライン化することで、モバイルLLMの注意フォールバックを削減する。

- **2025-10 · [Elastic On-Device LLM Service](2025-2409.09071-elastic-on-device-llm-service.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  端末内で一つの大規模言語モデルを複数アプリから共用する場合、画面操作エージェント、チャット、バックグラウンド要約は、それぞれ異なる遅延目標を要求する。ElastiLMは、この二つの調整軸を同じ要求制御に統合する。これは生成速度が10.45%増えたという意味ではなく、指定された遅延制約を守った要求の正答率の絶対差である。

- **2025-04 · [Scaling Up On-Device LLMs via Active-Weight Swapping Between DRAM and Flash](2025-2504.08378-scaling-up-on-device-llms-via-active-weight-swapping-between-dram-and-fl.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  スマートフォン上で大規模言語モデルを動かす際、モデルの全重みをDRAMに置けないことが最大の制約になる。さらに現在の層の活性化ベクトルから数層先の活性重みを予測して先読みし、複数層の重みをフラッシュ上で近接配置する。

- **2025-01 · [MoE²: Optimizing Collaborative Inference for Edge Large Language Models](2025-2501.09410-moe-optimizing-collaborative-inference-for-edge-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  MoE²（Mixture-of-Edge-Experts）は、単一の大規模言語モデル内部に小さな専門家層を並べる方式ではなく、独立した端末・サーバーに配置された複数の大規模言語モデルそのものを専門家として扱う協調推論基盤である。

- **2025-03 · [Optimal Expert Selection for Distributed Mixture-of-Experts at the Wireless Edge](2025-2503.13421-optimal-expert-selection-for-distributed-mixture-of-experts-at-the-wireless-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案方式の中核は、品質制約の下で消費エネルギーが小さい専門家集合を探す動的専門家選択（動的 専門家 Selection; DES）と、無線資源割当まで結合した共同専門家・副搬送波割当（Joint 専門家 and Subcarrier Allocation; JESA）である。

- **2025-08 · [End-to-End On-Device Quantization-Aware Training for LLMs at Inference Cost](2025-2509.00031-end-to-end-on-device-quantization-aware-training-for-llms-at-inference-c.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  ZeroQATは、推論時に使う低ビット重み・活性値を、学習時にも実際に量子化した状態で評価し、その結果に基づいて量子化認識学習を行う方法である。

- **2025-04 · [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  D²MoEは、端末上でMoEを動かすときの専門家の重みをどの精度で読み込むかと、SSDなどからの重み読込とGPU計算をどう重ねるかを同時に設計する。二重ルーティングは専門家IDとビット幅の二つの選択を意味し、トークンを二回生成する方式ではない。

- **2025-10 · [MoBiLE: Efficient Mixture-of-Experts Inference on Consumer GPU with Mixture of Big Little Experts](2025-2510.12357-mobile-efficient-mixture-of-experts-inference-on-consumer-gpu-with-mixtu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoBiLEは、総パラメータがGPUメモリに収まらないMixture-of-Experts（MoE）言語モデルを、消費者向けGPUとCPU DRAMの組合せで実行するときの転送ボトルネックを削減する推論方式である。

- **2025-10 · [ECVL-ROUTER: Scenario-Aware Routing for Vision-Language Models](2025-2510.27256-ecvl-router-scenario-aware-routing-for-vision-language-models.md)**  
  実装：[✓](https://anonymous.4open.science/r/ECVL-Router-977D) ・ リポジトリ内被引用：0  
  大規模なクラウドVLMは難しい質問に強い反面、すべての質問をクラウドで処理すると、単純な画像説明にも大きなモデルの計算費用と応答待ち時間がかかる。そこで、問い合わせごとに処理先を決める「モデルルーティング」が推論サービングの重要な設計問題になる。

- **2025-08 · [Efficient Edge LLMs Deployment via HessianAware Quantization and CPU GPU Collaborative](2025-2508.07329-efficient-edge-llms-deployment-via-hessianaware-quantization-and-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本研究は、GPUメモリが限られた端末でMixture-of-Experts（MoE）モデルを実行する際の二つの問題を同時に扱う。第一に、重みだけでなく活性値も整数8ビットへ量子化すると、少数の極端な活性値が量子化範囲を支配し、精度が悪化し得る。

- **2025-05 · [RAP: Runtime Adaptive Pruning for LLM Inference](2025-2505.17138-rap-runtime-adaptive-pruning-for-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定の剪定率でモデル重みだけを削る方式は、短い入力では過剰に品質を落とし、長い入力ではKVキャッシュの増加を補えないことがある。

- **2025-05 · [CE-LSLM: Efficient Large-Small Language Model Inference and Communication via Cloud-Edge Collaboration](2025-2505.14085-ce-lslm-efficient-large-small-language-model-inference-and-communication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  クラウドに大きな言語モデル（LLM）を置き、端末やエッジに小さな言語モデル（SLM）を置く場合、単純な分担には二つの問題がある。システムプロンプトのように複数ユーザー間で再利用可能な文脈と、個人の質問のようにローカルに保持すべき入力を分離できれば、両者の妥協点を作れる。

- **2025-04 · [Mosaic: Composite Projection Pruning for Resource-efficient LLMs](2025-2504.06323-mosaic-composite-projection-pruning-for-resource-efficient-llms.md)**  
  実装：[✓](https://github.com/blessonvar/Mosaic) ・ リポジトリ内被引用：0  
  Mosaicは、事前学習済み大規模言語モデルを限られたメモリの装置へ配置するため、Transformerの各線形射影に異なる削減率を割り当てる方式である。通常の非構造化枝刈りは重みを零化するため品質を比較的保てるが、重み行列の寸法を縮めない限り汎用の密行列演算ではメモリや時間の削減に結びつきにくい。

- **2025-01 · [Lightweight and Post-Training Structured Pruning for On-Device Large Lanaguage Models](2025-2501.15255-lightweight-and-post-training-structured-pruning-for-on-device-large-lan.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMを小型GPUやエッジデバイスへ配置する際、重み行列の疎化だけでは、専用の疎行列カーネルがなければ実行速度を改善しにくい。層やニューロンを物理的に削除する構造化剪定は、通常の密行列演算でもパラメータ数・演算量を減らせるが、削除による品質低下が大きくなりやすい。削除後は、校正入力に対する元の線形出力を最小二乗問題で再構成するマスク調整を行う。

- **2024-12 · [Deploying Foundation Model Powered Agent Services: A Survey](2024-2412.13437-deploying-foundation-model-powered-agent-services-a-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  本論文は、基盤モデル（foundation モデル）を使うエージェントサービスを、端末、エッジ、クラウドにまたがる異種資源上へ配備する際のシステム技術を整理した文献サーベイである。

### 3年前（2023-11〜2024-10）

- **2024-06 · [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)**  
  実装：[✓](https://github.com/Tiiny-AI/PowerInfer) ・ リポジトリ内被引用：60  
  PowerInfer-2は、利用頻度を測った重みだけをスマホの高速メモリへ置き、残りをUFSから読みつつCPU・NPU計算と重ねて、容量不足と読出し待ちを減らす方式。

- **2024-08 · [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  SwapMoEは、全専門家をメモリに置けない問題に対し、層ごとの仮想枠へ入力で選ばれた専門家重みを入れ替え、メモリ容量と重み転送を抑える方式。

- **2024-07 · [Mobile Edge Intelligence for Large Language Models: A Contemporary Survey](2024-2407.18921-mobile-edge-intelligence-for-large-language-models-a-contemporary-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：22  
  本論文は、LLM向けの移動体エッジ知能をMEI4LLMと呼び、その設計空間を通信・計算・記憶の三資源で整理する。

- **2024-03 · [MELTing point: Mobile Evaluation of Language Transformers](2024-2403.12844-melting-point-mobile-evaluation-of-language-transformers.md)**  
  実装：[✓](https://github.com/brave-experiments/MELT-public) ・ リポジトリ内被引用：8  
  モデル読込み中の操作不能、端末の発熱、連続実行での動作周波数低下、バッテリー消費、量子化による回答品質の劣化も重要である。原著の評価条件では4ビットモデルの生成スループットが3ビットモデルより平均24.77%高かった。

- **2024-01 · [BlockFFN: Towards End-Side Acceleration-Friendly Mixture-of-Experts with Chunk-Level Activation Sparsity](2025-2507.08771-blockffn-towards-end-side-acceleration-friendly-mixture-of-experts.md)**  
  実装：[✓](https://github.com/thunlp/BlockFFN) ・ リポジトリ内被引用：5  
  要点: BlockFFNは、混合専門家（Mixture-of-Experts; MoE）の「1トークン当たりは疎でも、複数トークンをまとめるとほぼ全専門家が必要になる」という弱点を狙う。

- **2024-08 · [Squid: Long Context as a New Modality for Energy-Efficient On-Device Language Models](2024-2408.15518-squid-long-context-as-a-new-modality-for-energy-efficient-on-device-lang.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Squidは、長文脈を扱う言語モデルの入力処理を小型モデルへ移し、回答を生成する大型モデルには短い潜在表現だけを渡す方式である。原著は単一のNVIDIA A100 80GB上で、直接Qwen2-7Bへ入力する方式の平均推論時間20.71秒に対してSquidは4.32秒、比率4.79倍を報告する。

- **2024-08 · [FactorLLM: Factorizing Knowledge via Mixture of Experts for Large Language Models](2024-2408.11855-factorllm-factorizing-knowledge-via-mixture-of-experts-for-large-languag.md)**  
  実装：[✓](https://github.com/zhenwuweihe/FactorLLM) ・ リポジトリ内被引用：0  
  FactorLLMは、学習済みの密な言語モデルのFeed-順伝播 Network（フィードフォワード層）を複数の小さな専門家へ分割し、各トークンに必要な専門家だけを実行することで、推論時のフィードフォワード層演算量を削減する手法である。

### 4年前（2022-11〜2023-10）

- **2023-08 · [EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices](2023-2308.14352-edgemoe.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/mllm) ・ リポジトリ内被引用：58  
  MoE エキスパートを外部ストレージ化し、エキスパート別混合量子化と活性相関に基づく先読み・キャッシュでモバイル推論のI/O律速を緩和する。

- **2023-09 · [LLMCad: Fast and Scalable On-device Large Language Model Inference](2023-2309.04255-llmcad-fast-and-scalable-on-device-large-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：26  
  端末で言語モデルを動かす場合、モデル重みがメモリ容量を超えると、生成のたびにストレージから重みを読み直すことがある。原著の構成は三つの機構からなる。Jetson TX2/Orin NXとAndroidスマートフォンで、標準の大型モデル単独生成に対してトークン当たり平均時間をIoT端末で2.9〜9.3倍、スマートフォンで3.47〜4.67倍短縮したと報告する。

### 5年前（2021-11〜2022-10）

- **2022-06 · [Language model compression with weighted low-rank factorization](2022-2207.00112-language-model-compression-with-weighted-low-rank-factorization.md)**  
  実装：✓ ・ リポジトリ内被引用：37  
  本論文は、事前学習・タスク別微調整を終えた言語モデルの大きな線形層を、低ランクの二つの行列に置き換える圧縮方法を扱う。著者らは、特異値が小さい成分を除去しても必ずしもタスクへの影響が小さくないことをBERTの実験で示した。

- **2022-03 · [Overcoming Oscillations in Quantization-Aware Training](2022-2203.11086-overcoming-oscillations-in-quantization-aware-training.md)**  
  実装：[✓](https://github.com/qualcomm-ai-research/oscillations-qat) ・ リポジトリ内被引用：7  
  量子化対応学習（Quantization-Aware 学習; QAT）は、訓練中に低ビットの重みと活性を模擬し、推論時に使う整数化済みネットワークの精度を回復する手法である。ImageNetのMobileNetV3-Smallでは重み・活性3/3ビットのLSQ基準52.0%に対し、減衰59.0%、凍結58.9%を報告する。

### 6年前（2020-11〜2021-10）

- **2020-11 · [EdgeBERT: Sentence-Level Energy Optimizations for Latency-Aware Multi-Task NLP Inference](2020-2011.14203-edgebert-sentence-level-energy-optimizations-for-latency-aware-multi-tas.md)**  
  実装：✓ ・ リポジトリ内被引用：14  
  EdgeBERTは、資源制約の厳しい端末上で、自然言語分類を決められた応答時間内に実行しながら消費エネルギーを最小化するための、アルゴリズムと回路の共同設計である。これらは別々の比較であり、同一実行条件の速度改善倍率でも、LLMのトークン生成性能でもない（原著要旨、§8.2）。

### 7年前（2019-11〜2020-10）

- **2020-07 · [HAT: Hardware-Aware Transformers for Efficient Natural Language Processing](2020-2005.14187-hat-hardware-aware-transformers-for-efficient-natural-language-processin.md)**  
  実装：[✓](https://github.com/mit-han-lab/hardware-aware-transformers) ・ リポジトリ内被引用：9  
  Transformerの推論速度を改善するため、パラメータ数や浮動小数点演算回数（FLOPs）を減らすことは一般的だが、演算量が同じモデルでも機器によって実測遅延は大きく異なる。HAT（Hardware-Aware Transformers）はこの差を設計時に扱う。
<!-- survey:auto:end -->
