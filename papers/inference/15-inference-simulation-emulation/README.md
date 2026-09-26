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
## 自動生成の論文一覧（6本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-01 · [AIConfigurator: Lightning-Fast Configuration Optimization for Multi-Framework LLM Serving](2026-2601.06288-aiconfigurator-multi-framework-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：7  
  実GPUで測った演算・通信性能から複数のLLMサービング構成をCPU上で予測し、並列化やバッチ、プリフィル・デコード分離を探索して遅延目標を満たす候補を選ぶ。

- **2026-01 · [Revati: Transparent GPU-Free Time-Warp Emulation for LLM Serving](2026-2601.00397-revati-transparent-gpu-free-time-warp-emulation.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  実LLMサーバ制御コードをそのまま走らせ、GPU計算だけ仮想時間へ置換して5%未満の誤差と約5〜17倍の評価高速化を狙うGPU不要エミュレータ。

- **2026-06 · [Frontier: Towards Comprehensive and Accurate LLM Inference Simulation](2026-2605.21312-frontier-comprehensive-accurate-llm-inference-simulation.md)**  
  実装：[✓](https://github.com/NetX-lab/Frontier) ・ リポジトリ内被引用：3  
  分離プリフィル/デコードや注意-FFN分離を役割別イベントグラフとして再現し、演算・通信・KVメモリを実測校正して、現代LLMサービング構成の性能を高精度に予測する。

- **2026-02 · [LLMServingSim 2.0: A Unified Simulator for Heterogeneous and Disaggregated LLM Serving Infrastructure](2026-2602.23036-llmservingsim-2-heterogeneous-disaggregated-simulator.md)**  
  実装：[✓](https://github.com/casys-kaist/LLMServingSim) ・ リポジトリ内被引用：3  
  異種GPU/TPU/PIMと分離サービング・多階層鍵値メモリ・MoE・電力を要求駆動ループで統合模擬するLLMサービングシミュレータ。

- **2026-06 · [KernelSight-LM: A Kernel-Level LLM Inference Simulator](2026-2606.28565-kernelsight-lm-kernel-level-inference-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUカーネル予測と実運用サービングの離散事象モデルを統合し、未計測GPUでもカーネル誤差12.1%、対象計測ありで3.8%を達成。

- **2026-05 · [LLM-Emu: Native Runtime Emulation of LLM Inference via Profile-Driven Sampling](2026-2605.00616-llm-emu-native-runtime-emulation.md)**  
  実装：[✓](https://github.com/AKafakA/llm-emu) ・ リポジトリ内被引用：1  
  vLLMの本番HTTP・スケジューラ・KV管理を実コードのまま動かし、GPU順伝播だけを二次元遅延プロファイルからの標本化へ置換して、実GPU比の出力トークン当たり時間・反復時間を4.8%、エンドツーエンド遅延を5.3%、出力スループットを1.9%以内で再現する（初回トークン時間は最大10.41%ずれる）実時間エミュレータ。

### 直近12か月・未被引用（2025-10〜2026-09）

該当なし。
<!-- survey:auto:end -->
