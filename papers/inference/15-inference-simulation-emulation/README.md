# Inference Simulation / Emulation

LLM推論・サービング基盤を実GPU実行の代わりに離散事象、仮想時間、プロファイル標本化、カーネル性能モデルなどで再現し、構成探索や性能評価を高速化する研究をまとめる。

## 分類境界

主要貢献がLLM推論の性能・資源挙動を実機の代替として予測・模擬するsimulator、emulator、time-warp、profile-driven modelである研究を含め、実測benchmarkだけの研究や実serving policyそのものは含めない。

### 含める研究

- LLM serving離散事象シミュレータ
- 実runtimeを残したGPUエミュレーション
- カーネルからservingまでの性能モデル

### 含めない研究

- 実測値を列挙するだけのbenchmark
- 本番serving schedulerそのもの

## 近傍系統

- [11-llm-serving-scheduling-disaggregation](../11-llm-serving-scheduling-disaggregation/)
- [09-kernel-runtime-compilation](../09-kernel-runtime-compilation/)

<!-- survey:auto:start -->
## 自動生成の論文一覧（18本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-01 · [AIConfigurator: Lightning-Fast Configuration Optimization for Multi-Framework LLM Serving](2026-2601.06288-aiconfigurator-multi-framework-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  実GPUで測った演算・通信性能から複数のLLMサービング構成をCPU上で予測し、並列化やバッチ、プリフィル・デコード分離を探索して遅延目標を満たす候補を選ぶ。

- **2026-02 · [LLMServingSim 2.0: A Unified Simulator for Heterogeneous and Disaggregated LLM Serving Infrastructure](2026-2602.23036-llmservingsim-2-heterogeneous-disaggregated-simulator.md)**  
  実装：[✓](https://github.com/casys-kaist/LLMServingSim) ・ リポジトリ内被引用：6  
  異種GPU/TPU/PIMと分離サービング・多階層鍵値メモリ・MoE・電力を要求駆動ループで統合模擬するLLMサービングシミュレータ。

- **2026-01 · [Revati: Transparent GPU-Free Time-Warp Emulation for LLM Serving](2026-2601.00397-revati-transparent-gpu-free-time-warp-emulation.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  実LLMサーバ制御コードをそのまま走らせ、GPU計算だけ仮想時間へ置換して5%未満の誤差と約5〜17倍の評価高速化を狙うGPU不要エミュレータ。

- **2026-06 · [Frontier: Towards Comprehensive and Accurate LLM Inference Simulation](2026-2605.21312-frontier-comprehensive-accurate-llm-inference-simulation.md)**  
  実装：[✓](https://github.com/NetX-lab/Frontier) ・ リポジトリ内被引用：3  
  分離プリフィル/デコードや注意-FFN分離を役割別イベントグラフとして再現し、演算・通信・KVメモリを実測校正して、現代LLMサービング構成の性能を高精度に予測する。

- **2026-01 · [ScaleSim: Serving Large-Scale Multi-Agent Simulation with Invocation Distance-Based Memory Management](2026-2601.21473-scalesim-serving-large-scale-multi-agent-simulation-with-invocation-dist.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  それでもLoRAアダプタ、接頭辞キャッシュ、専用モデル、検索状態などのエージェント固有メモリを全員分GPUへ常駐させると、エージェント数の増加に伴って容量を超える。一般的なSGLang等はアプリケーションの将来実行順を知らず、要求が来てから必要状態をCPUからGPUへロードし、LRU等で過去の利用履歴に基づき退避する。

- **2026-03 · [DyQ-VLA: Dynamic Quantization and Compensation for VLA models with Runtime Error Awareness](2026-2603.07904-dyq-vla-temporal-dynamic-aware-quantization-for-embodied-vision-language.md)**  
  実装：[✓](https://anonymous.4open.science/r/DyQ-VLA-7F51/) ・ リポジトリ内被引用：2  
  DyQ-VLAは、視覚言語行動モデル（Vision-Language-行動 モデル; VLA）の量子化を単なる「タスク 成功を保ちながら低ビット化する」問題ではなく、閉ループ実行中の実行時 誤差が次の観測・行動へどう伝播するかという観点から設計し直す。

- **2026-06 · [KernelSight-LM: A Kernel-Level LLM Inference Simulator](2026-2606.28565-kernelsight-lm-kernel-level-inference-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUカーネル予測と実運用サービングの離散事象モデルを統合し、未計測GPUでもカーネル誤差12.1%、対象計測ありで3.8%を達成。

- **2026-05 · [LLM-Emu: Native Runtime Emulation of LLM Inference via Profile-Driven Sampling](2026-2605.00616-llm-emu-native-runtime-emulation.md)**  
  実装：[✓](https://github.com/AKafakA/llm-emu) ・ リポジトリ内被引用：1  
  vLLMの本番HTTP・スケジューラ・KV管理を実コードのまま動かし、GPU順伝播だけを二次元遅延プロファイルからの標本化へ置換して、実GPU比の出力トークン当たり時間・反復時間を4.8%、エンドツーエンド遅延を5.3%、出力スループットを1.9%以内で再現する（初回トークン時間は最大10.41%ずれる）実時間エミュレータ。

### 直近12か月・未被引用（2025-11〜2026-10）

- **2026-10 · [ePACT: Energy-Performance-Aware Commitment Tracking for LLM Serving](2026-2610.01784-epact-energy-performance-aware-commitment-tracking-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMサービングの電力を単純に減らすのではなく、事前に契約した時間単位の電力量へ実消費を近づける。要求ごとのサービス期限を予測し、レプリカ数とGPUクロックをオンラインで調整する。

- **2026-09 · [Trillion-Parameter MoE in a Box: Decoupling Memory Provisioning with High-Bandwidth Flash](2026-2609.15636-trillion-parameter-moe-in-a-box-decoupling-memory-provisioning-with-high.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBMだけで容量を満たすと、容量と同時に非常に高い帯域まで購入することになり、低並列の実行時状態には過剰な場合がある。本論文は高帯域フラッシュ（High-Bandwidth Flash; HBF）へ重みを移し、DRAMをKV等の実行時状態専用にしたとき、各階層に本当に必要な容量と帯域を分離して測る。

- **2026-09 · [Characterizing High Bandwidth Flash for LLM Serving](2026-2609.39131-characterizing-high-bandwidth-flash-for-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  著者らはHBM、HBF、ホストDRAM、SSDの四階層にまたがる配置方針と、キャッシュ再利用を優先しながら新規要求の受入れを制限するスケジューラを設計する。B200相当の計算モデルとHBFの仮定仕様を用いた結果、評価した負荷条件で処理完了時間を36.1〜87.7%短縮する構成があり、モデル化したエネルギー削減率は最大59.1%に達する。

- **2026-08 · [BALANCE: Hybrid Autoregressive-Speculative LLM Inference at the Network Edge](2026-2608.05926-balance-hybrid-autoregressive-speculative-llm-inference-at-the-network-e.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号（SD）は小規模言語モデル（SLM）が複数トークンを提案し、LLMがまとめて検証するため遅延を下げられる一方、LLMとSLM双方の重み、両方式のKVキャッシュ、複数トークンの検証に必要なメモリがGPUに載る。

### 2年前（2024-11〜2025-10）

- **2024-11 · [APEX: An Extensible and Dynamism-Aware Simulator for Automated Parallel Execution in LLM Serving](2024-2411.17651-apex-an-extensible-and-dynamism-aware-simulator-for-automated-parallel-e.md)**  
  実装：✓ ・ リポジトリ内被引用：8  
  APEXは、LLM サービングでテンソル並列（テンソル 並列方式; TP）、パイプライン並列（パイプライン 並列方式; PP）、データ並列（data 並列方式; DP）、エキスパート並列（エキスパート 並列方式; EP）をどう組み合わせるべきかを、GPUクラスタへ候補を総当たり配備せずCPU上のシミュレーションで探索するシステムである。

- **2025-03 · [Improving the End-to-End Efficiency of Offline Inference for Multi-LLM Applications Based on Sampling and Simulation](2025-2503.16893-improving-the-end-to-end-efficiency-of-offline-inference-for-multi-llm-a.md)**  
  実装：[✓](https://github.com/puddingfjz/vllm) ・ リポジトリ内被引用：3  
  SamuLLMは、複数のLLMから構成されるオフライン推論アプリケーションを単一ノード複数GPUで実行するとき、「どのモデルを同時に走らせるか」と「各モデルへデータ並列（データ 並列方式; DP）とテンソル並列（テンソル 並列方式; TP）を何度ずつ割り当てるか」を共同最適化するフレームワークである。

### 3年前（2023-11〜2024-10）

- **2024-05 · [Vidur: A Large-Scale Simulation Framework For LLM Inference](2024-2405.05465-vidur-a-large-scale-simulation-framework-for-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/vidur) ・ リポジトリ内被引用：13  
  Vidurは、大規模言語モデル（LLM）をどのGPUに何台配置し、どの並列化方式・バッチ化方式で処理するかを、候補ごとに実機で運転せず比較するためのシミュレータである。LLaMA2-7B/70B、InternLM-20B、Qwen-72Bを使った実機比較では、オンライン負荷での正規化要求遅延の誤差は最大でも9%未満と報告される。

- **2024-08 · [LLMServingSim: A HW/SW Co-Simulation Infrastructure for LLM Inference Serving at Scale](2024-2408.05499-llmservingsim-a-hw-sw-co-simulation-infrastructure-for-llm-inference-ser.md)**  
  実装：[✓](https://github.com/casys-kaist/llmservingsim) ・ リポジトリ内被引用：5  
  大規模言語モデルの推論基盤では、GPUや専用演算器の設計だけでなく、到着する要求の分布、バッチ化、KVキャッシュ管理、複数装置へのモデル分割が性能を左右する。論文は実GPU上の推論基盤に対する性能傾向の誤差を平均14.7%程度に抑え、既存の演算器シミュレータに対して34.7〜491倍の高速化を報告する。

- **2024-06 · [Demystifying AI Platform Design for Distributed Inference of Next-Generation LLM models](2024-2406.01698-demystifying-ai-platform-design-for-distributed-inference-of-next-generation-llm-models.md)**  
  実装：[✓](https://github.com/abhibambhaniya/GenZ-LLM-Analyzer) ・ リポジトリ内被引用：4  
  演算子-level ルーフラインと集合通信通信モデルでLLM構造・推論提供最適化・分散方式からcompute/メモリ/ネットワーク要件を逆算するGenZ。

- **2024-09 · [TinyVLA: Towards Fast, Data-Efficient Vision-Language-Action Models for Robotic Manipulation](2024-2409.12514-tinyvla-towards-fast-data-efficient-vision-language-action-models-for-ro.md)**  
  実装：[✓](https://github.com/liyaxuanliyaxuan/TinyVLA) ・ リポジトリ内被引用：0  
  提案手法は、画像・言語の意味理解を約4.2億〜13億パラメータの小型マルチモーダル基盤モデルへ、連続行動の生成を拡散方策（diffusion policy）復号器へ分担させる。実機のFranka単腕ロボット5タスクでは、最大構成TinyVLA-Hの平均成功率が94.0%、OpenVLAが68.3%であり、差は25.7パーセントポイントだった。
<!-- survey:auto:end -->
