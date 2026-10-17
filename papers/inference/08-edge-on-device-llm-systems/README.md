# Edge / On-device LLM Systems

スマートフォン、個人PC、edge deviceなど、**VRAM・RAM・memory bandwidth・電力に厳しい制約がある環境でLLMを実行する**ためのsystem研究をまとめる。

<!-- survey:auto:start -->
## 自動生成の論文一覧（46本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-11〜2026-10**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-11〜2026-10）

- **2026-04 · [MemExplorer: Navigating the Heterogeneous Memory Design Space for Agentic Inference NPUs](2026-2604.16007-memexplorer-navigating-the-heterogeneous-memory-design-space-for-agentic-inference-npus.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  SRAM/HBM/LPDDR/GDDR/HBFを統一モデル化し、プリフィル/デコードNPUとメモリ階層を共同探索して、基準NPU比でプリフィル最大2.3倍・デコード最大1.93倍の電力効率を得る。

- **2026-08 · [FreeToken: Efficient Edge-Native MoE Serving with Bandwidth-Adaptive Execution](2026-2608.16157-freetoken-efficient-edge-native-moe-serving-with-bandwidth-adaptive-execution.md)**  
  実装：[✓](https://github.com/FlashML-org/FreeToken) ・ リポジトリ内被引用：2  
  FreeTokenは、混合専門家モデル（Mixture of エキスパート、MoE）の全専門家重みがGPUメモリに収まらない場合に、GPU・CPU・主記憶・PCIeを一つの推論基盤として使うローカル配信システムである。

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

- **2026-09 · [mzCache: On-Device LLM Memory Management under Multitasking](2026-2609.01338-mzcache-on-device-llm-memory-management-under-multitasking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  スマートフォンで大規模言語モデル（LLM）を端末内実行すると、モデル重みだけでなく、会話履歴を再計算せずに利用する鍵・値キャッシュ（KVキャッシュ）が長時間RAMを占有する。mzCacheはこの問題を、端末での退避後の復帰時間を最小化するメモリ管理として扱う。

- **2026-09 · [EStream: Fast and Memory-Efficient MoE Prefill through Expert Virtualization on Mobile NPUs](2026-2609.06551-estream.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  EStreamはMoE入力処理で必要な専門家をUFSから固定作業領域へ順次読み込み、NPU計算と重ね、静的共有グラフでDRAM不足と読出し待ちを減らす方式。

- **2026-09 · [AceSpec: An Asymmetric Edge-Cloud Collaborative Framework for Communication-Efficient LLM Inference](2026-2609.02514-acespec-asymmetric-edge-cloud-collaborative-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  AceSpecは端末–クラウド投機的復号で棄却分岐をWAN待ち中に先回り生成して状態キャッシュへ保存し、棄却後の再下書きと往復通信を減らす方式。

- **2026-08 · [Hydra: Phase-Aware Workload Characterization of LLM Inference across Edge SoC Generations, Backends, and Quantization Levels](2026-2608.25053-hydra-phase-aware-workload-characterization-of-llm-inference-across-edge.md)**  
  実装：[✓](https://github.com/amirtaherin/hydra) ・ リポジトリ内被引用：0  
  Hydraは、エッジ向け統合SoCで動く大規模言語モデル（LLM）の推論を、事前充填（プリフィル）と復号（デコード）という二つの処理区間に分け、実行時間・CPU/GPU活動・主記憶帯域・電力・消費エネルギー・温度を対応付ける計測・解析基盤である。

- **2026-08 · [FlashDrive: Flash Vision-Language-Action Inference for Autonomous Driving](2026-2608.12932-flashdrive-flash-vision-language-action-inference-for-autonomous-driving.md)**  
  実装：[✓](https://github.com/z-lab/flashdrive) ・ リポジトリ内被引用：0  
  FlashDriveは、映像と鍵・値キャッシュ（KVキャッシュ）の時系列再利用、拡散モデルによる複数推論トークンの投機的生成、軌跡生成の中間速度再利用、CUDA実行グラフと演算融合、重み4ビット・活性値8ビット量子化を組み合わせる。最終構成では716.9→151.4ミリ秒、約4.7倍の実測高速化となる。

- **2026-07 · [Transition-Aware Backend Dispatch for Edge LLM Inference](2026-2607.17415-transition-aware-backend-dispatch-for-edge-llm-inference.md)**  
  実装：[✓](https://anonymous.4open.science/r/power_aware_edge_inference_public-3B71/README.md) ・ リポジトリ内被引用：0  
  著者らは、対象演算の形状情報だけでなく、直前に選んだバックエンドも使い、演算が速くなる利得より切替費用が大きい場合は実行先を維持する選択方式を調べる。最良の静的バックエンドに比べた平均改善は遅延17.4%、エネルギー14.4%、エネルギー遅延積（EDP）28.5%だった。

- **2026-07 · [Automated Tensor Scheduling for Hybrid CPU-GPU LLM Inference on Consumer Devices](2026-2607.10183-atsinfer-automated-tensor-scheduling-hybrid-cpu-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ATSInferはテンソルごとのGPU常駐価値を実測し、CPU計算・PCIe転送・GPU計算を重ねて、VRAM不足時の転送待ちとCPU律速を減らす方式。

- **2026-06 · [VLMCache: Efficient On-Device Vision-Language Model Inference](2026-35c4f3816b37-vlmcache-efficient-on-device-vision-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VLMCacheは、UIエージェントや視覚質問応答のように連続フレームを処理する視覚言語モデルで、毎フレームの視覚入力を最初から入力処理するため初回トークン時間が長くなる問題を扱う。提案法は安定した背景ブロックと変化した前景ブロックを意味的に分離し、背景を再利用可能なKVキャッシュ接頭辞として並べ、前景だけを再計算する。

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

- **2026-05 · [Lever：スマートフォン向けフラッシュ常駐LLMの投機的推論](2026-2605.16786-lever-speculative-llm-inference-on-smartphones.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  OnePlus 12上の測定では、フラッシュ常駐標的モデルの検証時間のうち約78〜93%を入出力が占める条件があり、演算高速化だけではこの待ち時間を解消できない。Leverは投機的復号（投機的復号）を「サーバGPUで標的モデルの計算回数を減らす方式」ではなく、「フラッシュ常駐モデルの呼出し回数を複数トークンへ償却する方式」として再設計する。

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

- **2026-03 · [FlexServe: A Fast and Secure LLM Serving System for Mobile Devices with Flexible Resource Isolation](2026-2603.09046-flexserve-secure-mobile-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  TrustZoneのアクセス権と資源管理権を分離してページ単位セキュアメモリと切替可能NPUを実現し、LLM向けキャッシュ・回収・先読みでセキュア端末内推論の起動遅延を大幅に削減する。

- **2026-02 · [Quantization-Aware Collaborative Inference for Large Embodied AI Models](2026-2602.13052-quantization-aware-collaborative-inference-for-large-embodied-ai-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  端末側の計算能力・電池・通信帯域には制約があるため、端末側モデルを量子化して計算負荷を減らすことが有効である。実機はJetson AGX Orin 64GBとRTX 3090を2枚備えたサーバを無線LANで接続した構成で、遅延制約が強いと高周波数、エネルギー制約が強いと低周波数が有利になることを確認する。

### 2年前（2024-11〜2025-10）

- **2025-10 · [Characterizing Mobile SoC for Accelerating Heterogeneous LLM Inference](2025-d56c08fb1c58-characterizing-mobile-soc-for-accelerating-heterogeneous-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：9  
  HeteroInferは、携帯端末のシステムオンチップ（システム-on-Chip; SoC）に同居するGPUとニューラル処理装置（Neural Processing Unit; NPU）を同時利用し、大規模言語モデル（LLM）の前処理と自己回帰復号を高速化する推論基盤である。

- **2025-09 · [Scaling LLM Test-Time Compute with Mobile NPU on Smartphones](2025-2509.23324-scaling-llm-test-time-compute-with-mobile-npu-on-smartphones.md)**  
  実装：[✓](https://github.com/haozixu/llama.cpp-npu) ・ リポジトリ内被引用：7  
  Hexagon NPUの復号時に遊休しやすい行列演算器を、並列テスト時計算へ転用する。4ビット細粒度タイル量子化とルックアップテーブル（Lookup Table; LUT）演算により、混合精度GEMM最大19.0倍、Softmax最大2.2倍を報告する。

- **2025-05 · [EdgeShard: Efficient LLM Inference via Collaborative Edge Computing](2025-d6d0a70f5bc4-edgeshard-efficient-llm-inference-via-collaborative-edge-computing.md)**  
  実装：✓ ・ リポジトリ内被引用：6  
  既存の端末単独実行では重みが端末メモリに収まらず、端末とクラウドを二分割する方式では低帯域回線が遅延を支配する。著者らの実機試験では、Llama2-7Bに対し端末単独の140.34ミリ秒/トークン、24.36トークン/秒から、75.88ミリ秒/トークン、52.45トークン/秒へ改善した。

- **2025-07 · [DSSD: Efficient Edge-Device LLM Deployment and Collaborative Inference via Distributed Split Speculative Decoding](2025-2507.12000-dssd-efficient-edge-device-llm-deployment-and-collaborative-inference.md)**  
  実装：[✓](https://github.com/JasonNing96/DSSD-Efficient-Edge-Computing) ・ リポジトリ内被引用：5  
  端末で大規模言語モデルを動かすにはメモリ、演算能力、電力が不足しやすい。基地局やエッジサーバに大型モデルを置けば演算資源は確保できるが、ネットワーク往復時間と帯域が生成遅延へ加わる。ただしモデル対やドラフト長によっては通常の大型モデル推論より遅い条件があり、通信を減らせば無条件に高速化するわけではない。

- **2025-10 · [Elastic On-Device LLM Service](2025-2409.09071-elastic-on-device-llm-service.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  端末内で一つの大規模言語モデルを複数アプリから共用する場合、画面操作エージェント、チャット、バックグラウンド要約は、それぞれ異なる遅延目標を要求する。ElastiLMは、この二つの調整軸を同じ要求制御に統合する。これは生成速度が10.45%増えたという意味ではなく、指定された遅延制約を守った要求の正答率の絶対差である。

- **2025-08 · [ShadowNPU: System and Algorithm Co-design for NPU-Centric On-Device LLM Inference](2025-2508.16703-shadownpu-system-and-algorithm-co-design-for-npu-centric-on-device-llm-i.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  NPUで重要トークン位置だけを近似推定し、高精度疎注意をCPU/GPUへ限定してパイプライン化することで、モバイルLLMの注意フォールバックを削減する。

- **2025-10 · [Efficient LLM Inference over Heterogeneous Edge Networks with Speculative Decoding](2025-2510.11331-heterogeneous-edge-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  小基地局に下書きモデル、大基地局に対象モデルを置き、要求の下書き・検証を二段パイプライン化し、無線帯域・バッチ境界・投機長を調整して往復遅延を減らす方式。

- **2025-04 · [Scaling Up On-Device LLMs via Active-Weight Swapping Between DRAM and Flash](2025-2504.08378-scaling-up-on-device-llms-via-active-weight-swapping-between-dram-and-fl.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  スマートフォン上で大規模言語モデルを動かす際、モデルの全重みをDRAMに置けないことが最大の制約になる。さらに現在の層の活性化ベクトルから数層先の活性重みを予測して先読みし、複数層の重みをフラッシュ上で近接配置する。

- **2025-03 · [Optimal Expert Selection for Distributed Mixture-of-Experts at the Wireless Edge](2025-2503.13421-optimal-expert-selection-for-distributed-mixture-of-experts-at-the-wireless-edge.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  提案方式の中核は、品質制約の下で消費エネルギーが小さい専門家集合を探す動的専門家選択（動的 専門家 Selection; DES）と、無線資源割当まで結合した共同専門家・副搬送波割当（Joint 専門家 and Subcarrier Allocation; JESA）である。

- **2025-04 · [D²MoE: Dual Routing and Dynamic Scheduling for Efficient On-Device MoE-based LLM Serving](2025-2504.15299-d2moe-dual-routing-and-dynamic-scheduling-for-efficient-on-device-moe-based-llm-.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  D²MoEは、端末上でMoEを動かすときの専門家の重みをどの精度で読み込むかと、SSDなどからの重み読込とGPU計算をどう重ねるかを同時に設計する。二重ルーティングは専門家IDとビット幅の二つの選択を意味し、トークンを二回生成する方式ではない。

### 3年前（2023-11〜2024-10）

- **2024-06 · [PowerInfer-2: Fast Large Language Model Inference on a Smartphone](2024-2406.06282-powerinfer-2-fast-large-language-model-inference-on-a-smartphone.md)**  
  実装：[✓](https://github.com/Tiiny-AI/PowerInfer) ・ リポジトリ内被引用：52  
  PowerInfer-2は、利用頻度を測った重みだけをスマホの高速メモリへ置き、残りをUFSから読みつつCPU・NPU計算と重ねて、容量不足と読出し待ちを減らす方式。

- **2024-08 · [SwapMoE: Serving Off-the-shelf MoE-based Large Language Models with Tunable Memory Budget](2023-2308.15030-swapmoe-serving-off-the-shelf-moe-based-large-language-models-with-tunable-memor.md)**  
  実装：✓ ・ リポジトリ内被引用：28  
  SwapMoEは、全専門家をメモリに置けない問題に対し、層ごとの仮想枠へ入力で選ばれた専門家重みを入れ替え、メモリ容量と重み転送を抑える方式。

- **2024-07 · [Mobile Edge Intelligence for Large Language Models: A Contemporary Survey](2024-2407.18921-mobile-edge-intelligence-for-large-language-models-a-contemporary-survey.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  本論文は、LLM向けの移動体エッジ知能をMEI4LLMと呼び、その設計空間を通信・計算・記憶の三資源で整理する。

- **2024-01 · [BlockFFN: Towards End-Side Acceleration-Friendly Mixture-of-Experts with Chunk-Level Activation Sparsity](2025-2507.08771-blockffn-towards-end-side-acceleration-friendly-mixture-of-experts.md)**  
  実装：[✓](https://github.com/thunlp/BlockFFN) ・ リポジトリ内被引用：5  
  要点: BlockFFNは、混合専門家（Mixture-of-Experts; MoE）の「1トークン当たりは疎でも、複数トークンをまとめるとほぼ全専門家が必要になる」という弱点を狙う。

- **2024-03 · [MELTing point: Mobile Evaluation of Language Transformers](2024-2403.12844-melting-point-mobile-evaluation-of-language-transformers.md)**  
  実装：[✓](https://github.com/brave-experiments/MELT-public) ・ リポジトリ内被引用：4  
  モデル読込み中の操作不能、端末の発熱、連続実行での動作周波数低下、バッテリー消費、量子化による回答品質の劣化も重要である。原著の評価条件では4ビットモデルの生成スループットが3ビットモデルより平均24.77%高かった。

### 4年前（2022-11〜2023-10）

- **2023-08 · [EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices](2023-2308.14352-edgemoe.md)**  
  実装：[✓](https://github.com/UbiquitousLearning/mllm) ・ リポジトリ内被引用：48  
  MoE エキスパートを外部ストレージ化し、エキスパート別混合量子化と活性相関に基づく先読み・キャッシュでモバイル推論のI/O律速を緩和する。

- **2023-09 · [LLMCad: Fast and Scalable On-device Large Language Model Inference](2023-2309.04255-llmcad-fast-and-scalable-on-device-large-language-model-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  端末で言語モデルを動かす場合、モデル重みがメモリ容量を超えると、生成のたびにストレージから重みを読み直すことがある。原著の構成は三つの機構からなる。Jetson TX2/Orin NXとAndroidスマートフォンで、標準の大型モデル単独生成に対してトークン当たり平均時間をIoT端末で2.9〜9.3倍、スマートフォンで3.47〜4.67倍短縮したと報告する。

### 5年前（2021-11〜2022-10）

- **2022-06 · [Language model compression with weighted low-rank factorization](2022-2207.00112-language-model-compression-with-weighted-low-rank-factorization.md)**  
  実装：✓ ・ リポジトリ内被引用：16  
  本論文は、事前学習・タスク別微調整を終えた言語モデルの大きな線形層を、低ランクの二つの行列に置き換える圧縮方法を扱う。著者らは、特異値が小さい成分を除去しても必ずしもタスクへの影響が小さくないことをBERTの実験で示した。

- **2022-03 · [Overcoming Oscillations in Quantization-Aware Training](2022-2203.11086-overcoming-oscillations-in-quantization-aware-training.md)**  
  実装：[✓](https://github.com/qualcomm-ai-research/oscillations-qat) ・ リポジトリ内被引用：2  
  量子化対応学習（Quantization-Aware 学習; QAT）は、訓練中に低ビットの重みと活性を模擬し、推論時に使う整数化済みネットワークの精度を回復する手法である。ImageNetのMobileNetV3-Smallでは重み・活性3/3ビットのLSQ基準52.0%に対し、減衰59.0%、凍結58.9%を報告する。
<!-- survey:auto:end -->
