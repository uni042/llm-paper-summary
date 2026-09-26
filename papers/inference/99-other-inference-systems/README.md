# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（188本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-01 · [DART: Diffusion-Inspired Speculative Decoding for Fast LLM Inference](2026-2601.19278-dart-diffusion-inspired-speculative-decoding-for-fast-llm-inference.md)**  
  実装：[✓](https://github.com/fvliang/DART) ・ リポジトリ内被引用：6  
  対象LLM特徴から未来ロジットを1回で並列予測しN-gram木刈り込みを行い、EAGLE3より平均約30%高い投機デコード高速化を得る。

- **2025-10 · [Pie: A Programmable Serving System for Emerging LLM Applications](2025-2510.24051-pie-a-programmable-serving-system-for-emerging-llm-applications.md)**  
  実装：[✓](https://github.com/pie-project/pie) ・ リポジトリ内被引用：6  
  生成ループを細粒度APIへ分解し、Wasm inferletがKV・復号・入出力を直接制御しつつ適応一括処理でGPU効率を維持するプログラマブルLLMサービング基盤。

- **2026-07 · [FlashAccel: Leveraging High-Bandwidth Flash (HBF) for High-Throughput LLM Inference](2026-2607.10186-flashaccel-high-bandwidth-flash-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  HBM級帯域・大容量の高帯域フラッシュをGPUへ統合し、SRAM先読み、重み/KV専用配置、KVの選択的HBM複製、追記型永続管理を協調させて、モデル重みとKVキャッシュをフラッシュ上で直接高並列アクセスする推論アクセラレータ。

- **2026-05 · [An Efficient Hybrid Sparse Attention with CPU-GPU Parallelism for Long-Context Inference](2026-2605.07719-an-efficient-hybrid-sparse-attention-with-cpu-gpu-parallelism-for-long-context-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  CPU常駐KV向けに出力寄与ベース予算配分とCPU・GPU協調疎注意を統合し、長文復号を最大3.7倍高速化する。

- **2025-11 · [FlexiCache: Leveraging Temporal Stability of Attention Heads for Efficient KV Cache Management](2025-2511.00868-flexicache-leveraging-temporal-stability-of-attention-heads-for-efficient-kv-cache-management.md)**  
  実装：[✓](https://github.com/NazmulTakbir/FlexiCache) ・ リポジトリ内被引用：2  
  重要KVページが時間的に入れ替わりやすい注意ヘッドだけ全KVをGPUへ残し、安定ヘッドは上位ページ以外をCPUへ退避・周期再昇格することで、精度を保ちながらGPUメモリを最大70%削減する。

- **2025-10 · [2025-2510.05497-patterns-behind-chaos-forecasting-data-movement-for-efficient-large-scale-moe-llm-inference](2025-2510.05497-patterns-behind-chaos-forecasting-data-movement-for-efficient-large-scale-moe-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  その知見を将来のウェハ級GPU設計へ適用すると四モデル平均6.6倍、既存GPU向けプリフィル認識型専門家配置ではMoE計算を最大1.25倍高速化した。

- **2026-09 · [HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution](2026-2609.18675-hbflex.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  全HBF構成でKV配置・書戻し・寿命認識GCを共同最適化し、FlashAccel比最大1.58倍、H3比最大3.30倍の平均スループット向上。

- **2026-08 · [FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving](2026-2608.19758-flashprefill-v2-block-sparse-prefill-attention-for-long-context-llm-serving.md)**  
  実装：[✓](https://github.com/qhfan/FlashPrefillv2) ・ リポジトリ内被引用：1  
  平均補正付きブロック疎注意をHopper向けに再設計し、SGLangの長文事前充填を128Kで最大4.8倍高速化する。

- **2026-06 · [RoPE-Aware Bit Allocation for KV-Cache Quantization](2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md)**  
  実装：[✓](https://github.com/JIA-Lab-research/blockgtq) ・ リポジトリ内被引用：1  
  回転位置埋め込みの周波数ブロックごとのエネルギーに応じて鍵キャッシュのビット幅を配分し、圧縮した鍵・値を直接読む融合注意計算で長文脈推論の容量とメモリ帯域を同時に削減する。

- **2026-06 · [Models Take Notes at Prefill: KV Cache Can Be Editable and Composable](2026-2606.17107-models-take-notes-at-prefill-kv-cache-can-be-editable-and-composable.md)**  
  実装：[✓](https://github.com/19PINE-AI/programmable-kv) ・ リポジトリ内被引用：1  
  プリフィル済みKVキャッシュを結論メモとして捉え、追記訂正による編集とRoPE再配置による部品合成で再プリフィルを回避する。

- **2026-05 · [SYMPHONY: Enabling Compute-Memory Disaggregation in LLM Serving Systems](2026-0fd53670e945-symphony-enabling-compute-memory-disaggregation-in-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  将来要求の助言信号でKVキャッシュを事前移動し、層優先度と協調HBM管理で不確実性を吸収して計算・メモリ分離を低遅延化する。

- **2026-05 · [Move the Query, Not the Cache: Characterizing Cross-Instance Latent Attention Redistribution Across GPU Fabrics](2026-2606.01502-move-the-query-not-the-cache-characterizing-cross-instance-latent-attention-redistribution-across-gpu-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  約1KBの問い合わせを遠隔キャッシュへ送り注意計算する方式を実H100で測定し、約3msのキャッシュ再適応より数十µsの往復が有利となる条件を閉形式化する。

- **2026-05 · [How Far Can Disaggregation Go? A Design-Space Exploration of Attention-FFN Disaggregation for Efficient MoE LLM Serving](2026-2605.28302-how-far-can-disaggregation-go-a-design-space-exploration-of-attention-ffn-disaggregation-for-efficient-moe-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  注意とMoE-FFNの演算・通信を別GPU群へ分離する価値を、負荷・モデル・SLO・ネットワークを横断して設計空間探索する。

- **2026-03 · [ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs](2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md)**  
  実装：[✓](https://github.com/OpenBMB/ArcLight) ・ リポジトリ内被引用：1  
  NUMAごとのメモリ配置、動的スレッド群、Scatter/Gather型テンソル並列を一体化し、多数コアCPUの遠隔メモリアクセス壁を避けて、192コアARM環境でllama.cpp比最大46%高い推論スループットを示す軽量CPU推論基盤。

- **2026-02 · [Out of the Memory Barrier: A Highly Memory Efficient Training System for LLMs with Million-Token Contexts](2026-2602.02108-out-of-the-memory-barrier-a-highly-memory-efficient-training-system-for-llms-with-million-token-contexts.md)**  
  実装：[✓](https://github.com/wenhaoli-xmu/OOMB) ・ リポジトリ内被引用：1  
  チャンク再計算・ページ化KV/勾配・非同期CPUオフロード・疎注意を統合し、Qwen2.5-7Bの4M文脈学習を単一H200で実現する。

- **2026-02 · [2026-2603.13289-relaycaching-accelerating-llm-collaboration-via-decoding-kv-cache-reuse](2026-2603.13289-relaycaching-accelerating-llm-collaboration-via-decoding-kv-cache-reuse.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  複数のLLMが順番に推論する協調処理では、前段エージェントが生成した文章が次段エージェントの入力へ入る。通常は次段が同じ文章を再びプリフィルしてKVキャッシュを作り直すため、共有内容が長いほど重複計算と初回トークン時間（Time To First Token; TTFT）が増える。

- **2026-01 · [Towards Compute-Aware In-Switch Computing for LLMs Tensor-Parallelism on Multi-GPU Systems](2026-161bea97e0de-towards-compute-aware-in-switch-computing-for-llms-tensor-parallelism-on-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  NVLSの通信意味論をLLM計算カーネルの読み書き要求へ合わせ、スイッチ内要求マージ・GPU間TB協調・データフロー重畳でテンソル並列の通信待ちを削減する。

- **2026-01 · [ContiguousKV: Accelerating LLM Prefill with Granularity-Aligned KV Cache Management](2026-2601.13631-contiguouskv-accelerating-llm-prefill-with-granularity-aligned-kv-cache-management.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  KV 枝刈りとI/Oの粒度をContiguousChunkへ統一し、二段非同期プリフェッチでSSD KV読み込みを計算と重ねてRe-プリフィルを最大3.85倍高速化する。

- **2025-12 · [HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference](2026-f52f99f3360a-hifc-high-efficiency-flash-based-kv-cache-swapping-for-scaling-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUとNVMe SSDをGDSで直結し、pSLCと順次KVブロック配置でDRAMなしのKV交換を実現し、長文脈推論の性能を保ちながら容量費用を削減する。

- **2025-11 · [LUT-LLM: Efficient Large Language Model Inference with Memory-based Computations on FPGAs](2025-2511.06174-lut-llm-efficient-large-language-model-inference-with-memory-based-computations-on-fpgas.md)**  
  実装：[✓](https://github.com/LUT-FPGA/LUT-LLM) ・ リポジトリ内被引用：1  
  活性値・重み共同ベクトル量子化で線形層を2次元表引きへ変換し、AMD V80上のQwen3 1.7BでGPU比1.10〜3.29倍高速化を示す。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Where Should the KV Cache Live? Placement Policies Across GPU, CPU, and SSD for Long-Lived Sessions](2026-2609.16215-where-should-the-kv-cache-live-placement-policies-across-gpu-cpu-and-ssd-for-long-lived-sessions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU・CPU・SSD間のKV配置政策を比較し、SSDの容量利得とワークロード別の最適配置・遅延境界を定量化する。

- **2026-09 · [Validating Hybrid-State Cache Recovery for GLM-5.3-Flash with vLLM and LMCache](2026-2609.15030-validating-hybrid-state-cache-recovery-for-glm-5-3-flash-with-vllm-and-lmcache.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GLM-5.3-Flash＋vLLM＋LMCacheの完全キャッシュヒット境界ずれを厳密プレフィックス復旧で修正し、出力同一性を保ったCPUキャッシュ再ロードのTTFT短縮を実証。

- **2026-09 · [Unlocking Software-defined GPU Fabric Scheduling in the LLM Era](2026-a43ed4b300bf-unlocking-software-defined-gpu-fabric-scheduling-in-the-llm-era.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUファブリック競合を監視・通信注入制御し、vLLM+MooncakeでPD KV転送を19.4–34.4%短縮する。

- **2026-09 · [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md)**  
  実装：[✓](https://github.com/ifm-ai/uno) ・ リポジトリ内被引用：0  
  元の自己回帰モデル分布を保ったまま追加した離散拡散重みで複数トークンを並列提案し、専用サンプラで正しく補正して、逐次デコードの重み読出し回数を減らす。

- **2026-09 · [The Inference Engineering Pareto Atlas: Which Optimizations Dominate the Cost, Quality, and Latency Frontier?](2026-2609.17863-inference-engineering-pareto-atlas.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  54実測点と校正シミュレータで推論最適化の組合せを品質・遅延・費用の同一Pareto面へ置き、制約別の支配構成を示す。

- **2026-09 · [Taming Bitwise Behavior in GPU Kernels with Tensor Core: Black-Box Reconstruction, Compiler Enforcement, and Static Verification](2026-2609.11356-taming-bitwise-behavior-gpu-tensor-core-kernels.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU縮約順序を記述子化し、非公開行列積のビット挙動復元、コンパイラでの平衡木強制、命令列の静的同値判定を接続して再現性と自動調整を両立する。

- **2026-09 · [SpliTEE: Improving LLM Inference on Trusted Hardware with Differentially Private GPU Outsourcing](2026-2609.15039-splitee-improving-llm-inference-on-trusted-hardware-with-differentially-private-gpu-outsourcing.md)**  
  実装：[✓](https://github.com/DPVault/SpliTEE) ・ リポジトリ内被引用：0  
  TEE内のLLM線形演算を差分プライバシーで保護してGPUへ委譲し、プロンプト漏洩を抑えつつCPU-only TDX推論を約2倍高速化する。

- **2026-09 · [SiliconBench: Speed, Memory, and Fidelity for LLM Serving on Unified-Memory Desktops](2026-2609.19169-siliconbench-speed-memory-and-fidelity-for-llm-serving-on-unified-memory-desktops.md)**  
  実装：[✓](https://github.com/WindChimeRan/SiliconBench) ・ リポジトリ内被引用：0  
  Apple Siliconの九推論基盤を速度・共有メモリ・忠実度・新モデル対応・複数機で横断監査し、vllm-metalの並行処理と遠隔直接メモリアクセスを使うテンソル並列の優位を示す。

- **2026-09 · [Shared-Prefix KV Reuse Across Standard LoRA Adapters: Quality and Serving Tradeoffs](2026-2609.17109-shared-prefix-kv-reuse-across-standard-lora-adapters-quality-and-serving-tradeoffs.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既学習の標準LoRA間で基盤モデル接頭辞KVを直接再利用し、8K暖機済み初回トークン時間約16倍と小さいが不確実な品質低下、物理共有未実装という実運用上の境界を測定する。

- **2026-09 · [Separating Stream Stability from Long-Term Recall in Language Models](2026-2609.07282-stream-stability-long-term-recall-threeh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長時間生成の安定性・過去情報への因果アクセス・タスク効用をThreeHの3到達距離へ分離し、注意シンクの安定生成を長期記憶と誤認しない評価契約を示す。

- **2026-09 · [SemBridge: Compiling Consumer Observations into Cross-Stack Communication Plans](2026-2609.08231-sembridge-compiling-consumer-observations-into-cross-stack-communication-plans.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  異種CUDA/NCCL–CANN/HCCL境界で消費者が必要とする観測結果を型付き契約へコンパイルし、不要な全logit転送をトークン投影へ縮約して結果通信を99.97%以上削減する通信計画器。

- **2026-09 · [Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution](2026-2609.09240-scaling-post-training-ternarisation-to-qwen3-8b-capability-retention-reproduction-lossless-packing-and-packed-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Qwen3-8Bを適応的約1.64 bit/重みへ後量子化し、78.5%の補正済み能力保持、8.24 GiBの無損失packed artifact、RTX 5070上15.52 トークン/s・7.35 GiBの直接実行まで検証する。

- **2026-09 · [SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking](2026-2609.13141-sas-simple-attention-sparsification-via-end-to-end-optimization-of-context-ranking.md)**  
  実装：[✓](https://github.com/Tencent-Hunyuan/Simple-Attention-Sparsification) ・ リポジトリ内被引用：0  
  言語モデル損失を注意ソフトマックス内の連続ゲートへ直接流してコンテキスト順位を学習し、固定Top-K疎注意の精度と長文脈デコード効率を改善する。

- **2026-09 · [Sample-Guided Exact Top-K Selection for Long-Context Sparse Attention](2026-2609.08450-sample-guided-exact-topk-sparse-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HPC-Ops Top-Kは、標本で上位候補境界を予測し、全行の一回走査で十分性を証明、足りない時だけ回復して正確なK個を選び、長文疎注意の再走査を減らす。

- **2026-09 · [RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems](2026-2609.12551-rooflang-ai-driven-llm-inference-architecting.md)**  
  実装：[✓](https://github.com/yzygitzh/rooflang) ・ リポジトリ内被引用：0  
  RoofLangはLLM推論を計算・ハードウェアグラフと意味保存変換で表し、実装非依存のシミュレーションを評価器としてAIに配置・並列化・通信構成を探索させる設計基盤である。

- **2026-09 · [Quality-Constrained Routing over a Fixed Pool of Quantized Mixture-of-Experts Instances](2026-2609.12550-quality-constrained-routing-over-a-fixed-pool-of-quantized-mixture-of-experts-instances.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定常駐したW2・W3・W4量子化MoEインスタンス間で、入力時の脆弱性重み付きパープレキシティから要求別の量子化リスクを推定し、品質予算付き線形計画で高処理量側へ配分する要求ルーティング。

- **2026-09 · [Pull: Lazy Materialization of Working Memory for Stateful LLM Conversations](2026-2609.14773-pull-lazy-working-memory-materialization.md)**  
  実装：[✓](https://github.com/wulun811/kongmen-pull) ・ リポジトリ内被引用：0  
  長期対話を決定論的な索引で管理し、質問ごとに必要な原文ターンだけを可逆的に実体化して入力トークンを削減するセッションルータ。

- **2026-09 · [PolarKV: Tier Locally, Serve Globally–A KV Cache over Cloud Memory and Storage](2026-4820586f504d-polarkv-tier-locally-serve-globally-a-kv-cache-over-cloud-memory-and-storage.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散メモリを帯域層、クラウドブロックストレージを容量層とし、対応シャードを同一VMへ共置してKVの階層移動をローカル化することで、クラウドのネットワーク帯域と費用の制約を抑えるKVキャッシュ基盤。

- **2026-09 · [Physically Partitioned KVCache Format for CPU–GPU Load Balancing in MoE Inference](2026-2609.14507-physically-partitioned-kvcache-format-for-cpu-gpu-load-balancing-in-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KVを書込時にCPU計算用・GPU転送用の物理領域へ固定配置し、ルーフラインで系列を動的分担することで、単一GPUの長文MoE推論を高速化する。

- **2026-09 · [PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling](2026-2609.09662-pelm-speculative-decoding-dvfs.md)**  
  実装：[✓](https://github.com/imec-nu/PELM) ・ リポジトリ内被引用：0  
  DVFS・自己投機的デコード・可変検証深度を深層強化学習で共同制御し、端末LLMで最大23.1%高速化・52.4%エネルギー削減を達成する。

- **2026-09 · [Partition-Aware Scheduling for Mobile Heterogeneous Inference Co-Execution](2026-2609.14213-partition-aware-scheduling-for-mobile-heterogeneous-inference-co-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  演算子のCPU-GPU分割とDAG上の実行順を共同最適化し、段階化・臨界度標本化・遅延予測による配備時反復探索でオフライン最適化に近いモバイル推論遅延を得る。

- **2026-09 · [Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training](2026-2609.07108-online-draft-co-training-for-speculative-decoding-in-large-scale-long-context-rl-post-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長文脈RLで投機的復号のドラフトを方策と同時更新するため、分岐注意を文脈並列リングへ統合し、中間特徴をパイプライン外のTapChannelで輸送して、最大122B規模で学習品質を保ちつつ最大1.88倍の全体高速化を得る。

- **2026-09 · [OBC-Prune: Outcome-Based Calibration for Large Reasoning Model Pruning](2026-2609.17890-obc-prune-outcome-based-calibration-for-large-reasoning-model-pruning.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  正答・誤答の思考過程を同一問題で対にし、文ごとの因果的寄与で較正活性値を再重み付けすることで、一発枝刈り後の推論精度と停止挙動を改善する。

- **2026-09 · [MiX: Micro-Inverted-Scaling for End-to-End Low-Bit Vision-Language Model Acceleration](2026-2609.19683-mix-micro-inverted-scaling-for-end-to-end-low-bit-vision-language-model-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  VLMのマルチモーダル外れ値に対し、要素別指数＋共有仮数へマイクロスケーリングを反転し、4bit級の端から端までの量子化と乗算器不要のシフト加算PEを同時に実現する。

- **2026-09 · [MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators](2026-2609.19207-meshkv-a-network-on-chip-kv-cache-fabric-for-scalable-transformer-decoding-accelerators.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  鍵値キャッシュをオンチップ網の分散流へ変換し、8×8 FPGA実装で通信量最大58%削減、鍵値帯域利用率2.1倍、生成処理量最大1.90倍を実測する。

- **2026-09 · [MCSched: Memory-Controller-Aware Scheduling for Embodied LLM Workloads on NVIDIA Jetson](2026-fd0d3fa4e564-mcsched-memory-controller-aware-scheduling-for-embodied-llm-workloads-on-nvidia-jetson.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Jetson統合メモリの隠れた帯域競合を監視し、締切危険時だけ背景LLMを一時停止してロボット処理を保護する軽量実行時スケジューラ。

- **2026-09 · [LeanStream: A Speculate-and-Refine Streaming Framework for Efficient on-Device LLM Inference](2026-2609.03079-leanstream-speculate-refine-on-device.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LeanStreamは、層内の部分残差から次層の重み優先度を更新し、重み読出し・GPU計算・キャッシュを非同期に重ねて、端末LLMのSSD待ちと予測ミスを減らす。

- **2026-09 · [Kalman Delta Networks: Uncertainty-aware Associative Memory](2026-2609.07816-kalman-delta-networks-associative-memory.md)**  
  実装：[✓](https://github.com/ngocbh/kalman-delta-networks) ・ リポジトリ内被引用：0  
  固定サイズの線形注意メモリに推定不確実性を持たせ、蓄積証拠に応じて上書き強度をカルマン利得から決めることで、長文脈検索と生成精度を改善する。

- **2026-09 · [JustFit: 200K-Token LLM Serving on a 24 GiB Laptop with Just-in-Time State Management](2026-2609.17475-justfit-200k-token-llm-serving-on-a-24-gib-laptop-with-just-in-time-state-management.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  圧縮キー・バリュー実行、部品常駐切替、状態保持遷移を統合し、24 GiB機で27B級モデルの約213K位置の単一要求を完走する推論実行系。

- **2026-09 · [IHS-LM: Intra-batch Hybrid Scheduling and Layer Migration for VLM Pipeline Inference Acceleration on Edge Devices](2026-9b405eddeda4-ihs-lm-intra-batch-hybrid-scheduling-and-layer-migration-for-vlm-pipeline-inference-acceleration-on-edge-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV容量連動のプリフィル/デコード混在スケジューリングと帯域感知型の境界層移行を統合し、異種Jetson上のVLM推論遅延を最大17.5%削減する。

- **2026-09 · [HoliBench: A Cross-Platform Benchmarking and Deployment Toolkit for Foundation Models in CPS-IoT Applications](2026-2609.12412-holibench-a-cross-platform-benchmarking-and-deployment-toolkit-for-foundation-models-in-cps-iot-applications.md)**  
  実装：[✓](https://github.com/beesfleas/HoliBench) ・ リポジトリ内被引用：0  
  20モデル×7デバイス×3量子化×8推論系を精度・遅延・電力・メモリで統一測定し、実測プロファイルから制約付き配備構成まで選ぶ基盤。

- **2026-09 · [GrowMTP: Can RL Grow Its Own Draft Head?](2026-2609.16648-growmtp-efficient-multi-token-prediction-via-progressive-growth.md)**  
  実装：[✓](https://growmtp.github.io/) ・ リポジトリ内被引用：0  
  強化学習ロールアウトの検証信号でドラフトヘッドをその場で育成し、事前ヘッドなしでも投機的デコードによる学習加速を実現する。

- **2026-09 · [GDN Tree-Scan: Served Tree Verification for Recurrent-Hybrid Language Models](2026-2609.23900-gdn-tree-scan-served-tree-verification-for-recurrent-hybrid-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GDN Tree-Scanは、FlashAttention-2による木型注意バイアス、枝ごとのGDN状態走査と再生、GPU上の複数ドラフト確定、受理枝だけの状態公開を統合する。

- **2026-09 · [FoldQuantVLA: Native Low-Bit Quantization of Vision-Language-Action Models via Consistent Folding](2026-2609.24433-foldquantvla-native-low-bit-quantization-of-vision-language-action-models-via-consistent-folding.md)**  
  実装：[✓](https://github.com/cair-vinuni/FoldQuantVLA) ・ リポジトリ内被引用：0  
  VLAの共有活性値変換を校正から重み丸め、TensorRT実行まで一貫させる学習後量子化を設計し、W4A4でOrin上の推論を浮動小数点TensorRT比1.20〜1.33倍に高速化した。

- **2026-09 · [FlexEE: Self-Speculative and KV-Compatible Early Exiting for Offloading-Aware LLM Inference](2026-2609.17008-flexee-self-speculative-and-kv-compatible-early-exiting-for-offloading-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Top-K自己投機による軽量な早期退出と隠れ状態の持越しでKV整合性を保ち、重みオフロード時に後段層の計算と転送をまとめて省く。

- **2026-09 · [FlashGPU-sim: Enabling GPU Modeling for Modern Architectures and AI Workloads](2026-2609.15311-flashgpu-sim-enabling-gpu-modeling-for-modern-architectures-and-ai-workloads.md)**  
  実装：[✓](https://github.com/FlashGPU-Sim/FlashGPU-Sim) ・ リポジトリ内被引用：0  
  Hopper/Blackwellの非同期GPU機構とTriton AIカーネルを実行駆動で再現し、131構成でサイクル誤差5.24%、16スレッドで7.86倍高速化した現代GPUシミュレータ。

- **2026-09 · [Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs](2026-2609.26796-flash-dllm-io-aware-kv-caching-and-parallel-decoding-for-fast-memory-efficient-diffusion-llms.md)**  
  実装：[✓](https://github.com/VILA-Lab/Flash-dLLM) ・ リポジトリ内被引用：0  
  拡散言語モデルの鍵・値キャッシュ更新を融合注意へ統合し、同じモデルによる下書き・検証型並列復号を重ねることで、メモリ入出力と反復回数を同時に削減する。

- **2026-09 · [Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign](2026-2609.10970-fengshui-chiplet-neural-accelerator-codesign.md)**  
  実装：[✓](https://github.com/CrucibleComputingGroup/fengshui) ・ リポジトリ内被引用：0  
  再利用可能な少数チップレット群そのものと演算子単位の専用アクセラレータ構成を共同探索し、計算データフロー・メモリ・並列方式・配置配線を演算子ごとに最適化してNREを抑えつつLLM推論のエネルギー効率を高める。

- **2026-09 · [FaultSense: Fault Localization in Large-Scale Mixture-of-Experts Model Serving Infrastructure](2026-a08c1f9c632d-faultsense-fault-localization-in-large-scale-mixture-of-experts-model-serving-infrastructure.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一MoE層の選択可能プローブと二段階グループ検査で、特権監視なしにグレー障害GPU・通信経路をアプリ層から局所化し、診断プローブを約20倍削減する。

- **2026-09 · [ECOKV: Geometry-Aware KV Cache Eviction via Complementary Diversity Metrics](2026-2609.06663-ecokv-geometry-aware-kv-cache-eviction-via-complementary-diversity-metrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コサイン類似度だけでは見落とすKV表現の大きさをユークリッド距離で補い、注意ヘッドごとの冗長度に応じて多様性と重要度を混合し、狭いKV予算で保持トークンを改善する方式。

- **2026-09 · [Dynamic Semantic Compression for Efficient Latent-Space Inference in Large Language Models](2026-2609.15338-dynamic-semantic-compression-latent-space-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文を長さに応じて1〜3区間へ分割し、重要トークンを重み付けした潜在表現を生成・復号するDSEI。固定文圧縮より品質を改善し、トークン単位推論より系列長とメモリ負荷を削減する。

- **2026-09 · [Dissecting GPU Utilization for LLM Inference on Nvidia Hopper](2026-2609.12923-dissecting-gpu-utilization-llm-inference-hopper.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H100上のLLM推論を8種類のNsight指標で分解し、デコードでは帯域待ちに加えGMMA m64固定断片の1.56～12.5%充填やwave損失が単一SM利用率に隠れることを示す。

- **2026-09 · [DeepSeek-V4-Flash on AMD gfx90a: Correctness Recovery and Inference Performance Engineering](2026-2609.15627-deepseek-v4-flash-on-amd-gfx90a-correctness-recovery-and-inference-performance-engineering.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MI250上のDeepSeek-V4-Flashで数値不具合を修復し、CDNA2向けカーネル・通信・事前充填最適化によりTP8復号をC64で1327.10トークン/秒まで実測した。

- **2026-09 · [D-Quant: Driftable Entropy Coding for KV Cache Quantization](2026-2609.19880-d-quant-driftable-entropy-coding-for-kv-cache-quantization.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  固定サイズ容器と長さ制約付きドリフトを組み合わせ、エントロピー符号化KVキャッシュを注意カーネル内で直接並列復号できる形にした低ビット量子化方式。

- **2026-09 · [CompKV: Compensation-Aware KV Selection for Long-Context LLM Inference](2026-2609.26300-compkv-compensation-aware-kv-selection-for-long-context-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  平均補償後に残る注意誤差を注意質量とブロック内得点分散の積で推定し、厳密に読む鍵・値ブロックを選ぶことで、長文脈の疎な注意計算の精度と中央処理装置退避効率を改善する。

- **2026-09 · [CEDAR: Error-Bounded Residual Routing for Efficient Long-Context Attention](2026-2609.07237-cedar-error-bounded-residual-routing-for-efficient-long-context-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  選外チャンクも要約経路で全域可視性を残し、鍵・値分散に基づく誤差上界で必要なチャンクだけ正確注意へ展開して、128Kで約3倍のカーネル高速化と品質回復を両立する疎注意方式。

- **2026-09 · [Breaking the 1.58-bit Barrier for Ternary LLMs](2026-2609.16338-breaking-the-1-58-bit-barrier-for-ternary-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  三値重みのゼロ偏りを利用するBITCOSで格納量を最小1.485ビット/重みまで下げ、専用CPU・Xe2復号で一要求デコードを最大1.27倍高速化する。

- **2026-09 · [BigMoMo: Efficient Inference of Large-Scale MoE with Speculative Decoding on Mobile Devices](2609.14643.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的復号の複数トークン窓でエキスパート再利用・フラッシュ連続読出し・NPU計算との移動重畳を行い、30B級MoEのスマホ推論を平均4.83倍高速化する。

- **2026-09 · [AutoTuneBench: Trustworthy Measurement for Agent Auto-Tuning of LLM Serving Engines](2026-2609.18123-autotunebench-trustworthy-serving-engine-measurement.md)**  
  実装：[✓](https://github.com/li-ch/autotunebench) ・ リポジトリ内被引用：0  
  自動チューニングの測定規約を凍結コード・DB投入検証・不正隔離・事前登録比較・外部アンカーで強制し、エージェントが評価欠陥を最適化するのを防ぐ。

- **2026-09 · [Attention Routing Stabilizes Early: Working-Set Inference for Recurrent Language Models](2026-2609.27373-attention-routing-stabilizes-early-working-set-inference-for-recurrent-language-models.md)**  
  実装：[✓](https://github.com/tbn5pj/WISE_code) ・ リポジトリ内被引用：0  
  WISEは初期段階で注意の作業集合を特定し、その後は選択済みブロックへ計算を絞る推論時方式である。再学習なしで深い再帰実行を保ち、4K文脈の注意計算を最大1.76倍、32段全体を1.36倍高速化したと報告する。

- **2026-09 · [ASPIRE: Asynchronous Batched Self-Speculative Decoding for Long-Context LLM Inference](2026-2609.17943-aspire-asynchronous-batched-self-speculative-decoding.md)**  
  実装：[✓](https://github.com/Amir-zsh/ASPIRE) ・ リポジトリ内被引用：0  
  下書き・検証混在順伝播、要求別オンライン制御、下書き内の鍵値文脈更新により長文脈自己投機復号を最大4.58倍高速化する。

- **2026-09 · [2026-2609.25492-rgsq-riemannian-geometry-sensitive-quantization-for-large-vision-language-models](2026-2609.25492-rgsq-riemannian-geometry-sensitive-quantization-for-large-vision-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  従来の学習後量子化は、量子化前後の差をユークリッド距離で測り、各方向の誤差をほぼ等価に扱う。

- **2026-08 · [TurboBus: Pooling PCIe Bandwidth for LLM Workloads via Scale-Up Fabrics](2026-2fe550669a96-turbobus-pooling-pcie-bandwidth-for-llm-workloads-via-scale-up-fabrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPU間高速ファブリックを中継路として他GPUの空きPCIeリンクを借用し、モデル読込の初回トークン待ち時間を最大40%削減、鍵値退避推論を最大1.6倍高速化する。

- **2026-08 · [SplitScaling: Adaptive Scaling for Disaggregated LLM Serving Against Traffic Bursts via DRL](2026-92b65c48d388-splitscaling-adaptive-scaling-for-disaggregated-llm-serving-against-traffic-bursts-via-drl.md)**  
  実装：[✓](https://github.com/Onlytonight/SplitScaling) ・ リポジトリ内被引用：0  
  プリフィル／デコード各プールを深層強化学習で独立伸縮し、新規ノードへ待機要求を即時再割当して、バースト負荷下でSLOを守りながら静的構成比25.2%の計算コストを削減する。

- **2026-08 · [RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention](2026-2608.08081-rotaryquant-fitting-120b-moe-models-on-consumer-hardware-via-fused-compressed-space-attention.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み・3ビット鍵値キャッシュ・専門家退避を統合し、圧縮表現のまま注意計算して120B MoEを17.2GB、14.85トークン毎秒で実行する。

- **2026-08 · [Performance Foundations of Parallel & Distributed Reasoning Language Models](2026-2608.27046-performance-foundations-of-parallel-distributed-reasoning-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RLM後学習を仕事量・深さ・メモリで形式化し、モデル内6種の並列化と配置・段階融合・非同期化を統一分類して、長い自己回帰生成が支配する分散RLの設計原理を整理する。

- **2026-08 · [OpRAG: A Resource-Deterministic Runtime for GPU-Backed Multi-Stage RAG Workflows](2026-2608.08340-oprag-resource-deterministic-rag-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  RAG各段階を資源・通信付き演算子へ変換し、ゼロコピー通信とCPU/GPU重畳で復号外のオーケストレーション律速を削減する。

- **2026-08 · [M-LoRA: Efficient Serving for Concurrent LoRA Adapters with Memory-Aware Speculative Scheduler on Single GPU](2026-bbf40b71b5e2-m-lora-efficient-serving-for-concurrent-lora-adapters-with-memory-aware-speculative-scheduler-on-single-gpu.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  要求ごとの生成長をモデル別LoRA予測器で見積もり、鍵値キャッシュとアダプタのピークメモリを同時制約する整数線形計画で、単一GPUの複数LoRA要求を高並行に割り当てるサービング方式。

- **2026-08 · [LLM4LLM: Bridging Kernel Benchmarks and Real Deployment via Closed-Loop Agentic Optimization](2026-2608.21836-llm4llm-bridging-kernel-benchmarks-and-real-deployment-via-closed-loop-agentic-optimization.md)**  
  実装：[✓](https://github.com/hzeng2000/LLM4LLM) ・ リポジトリ内被引用：0  
  実モデルを計測して段階別カーネルを探索し、モデル内検証まで閉ループ化してA100/H100で幾何平均3.91倍/6.98倍の端から端までの高速化を達成する。

- **2026-08 · [Learning how to Forget: Fine-tuning for Long-Context Sparse Attention](2026-2608.19920-learning-how-to-forget-fine-tuning-for-long-context-sparse-attention.md)**  
  実装：[✓](https://github.com/awslabs/keys_values) ・ リポジトリ内被引用：0  
  任意のKVキャッシュ方策を学習中に再現し、二重チェックポイントとKV差分符号化で推論級メモリの長文脈疎注意微調整を実現する。

- **2026-08 · [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEの融合カーネル・4/8ビット量子化・グラフコンパイルを単体とE2Eで測定し、局所高速化が起動律速や品質へどう波及するかを分解して、置換可能な最適化の限界を明らかにする研究。

- **2026-08 · [Janus: Joint Prefill/Decode Disaggregation with KV-Cache-Aware Multi-Cloud Routing for Edge-Adjacent LLM Serving](2026-98d01325c44c-janus-joint-prefill-decode-disaggregation-with-kv-cache-aware-multi-cloud-routing-for-edge-adjacent-llm-serving.md)**  
  実装：[✓](https://github.com/arunakbofficial-tech/Janus) ・ リポジトリ内被引用：0  
  プリフィル/デコード配置とKV輸送方式を共同最適化し、異種マルチクラウドLLMサービングのTTFT・有効スループット・コストを同時改善する。

- **2026-08 · [HorizonServe: Coordinating Request Scheduling with GPU Sharing for Omni-Model Serving](2026-2608.01785-horizonserve-coordinating-request-scheduling-with-gpu-sharing-for-omni-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一GPU上のオムニモデルで、締切余裕に基づく経路入場制御と帯域圧力に応じたSM配分を連携し、異種出力要求のSLO達成率を高めるサービング方式。

- **2026-08 · [FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration](2026-2608.25062-flint-efficiently-leveraging-high-bandwidth-flash-for-capacity-scalable-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高帯域フラッシュを巨大モデル重みの近接容量層として使い、動的読み出し結合・更新隔離・読み出し専用変換表で従来方式比六・二倍の復号処理量を実現する。

- **2026-08 · [EdgeXpert: An Edge Device for Memory-Efficient LLM Inference with Mixture-of-Experts and Speculative Decoding](2026-2608.05303-edgexpert-moe-speculative-decoding.md)**  
  実装：[✓](https://doi.org/10.5281/zenodo.21481269) ・ リポジトリ内被引用：0  
  MoEと投機的復号の併用で増える専門家外部メモリアクセスを、プリフィルの共有専門家再利用とデコードの深さ認識チャネル統合で直接削減するエッジ向け協調設計。

- **2026-08 · [DeltaLog: Deferred Materialization of Recurrent States for Linear Attention Decoding](2026-2608.15533-deltalog-deferred-materialization-of-recurrent-states-for-linear-attention-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  線形注意の密な再帰状態を基底状態と有界な差分ログへ分解し、毎トークンの全状態書き戻しを周期的なマージへ遅延する。

- **2026-08 · [DASC: Decay-Aware State Compression for Hybrid Linear-Attention Serving](2026-2608.30386-dasc-decay-aware-state-compression-for-hybrid-linear-attention-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重み由来の保持地平でKDA/GDN再帰状態を選別・ragged保存し、TP均衡化によりKimi-KDAで2.63倍のcheckpoint容量とTTFT 42.6%削減を実現する。

- **2026-08 · [Bounded-State Restoration: Decoupling Local Restore Capacity from External LLM State](2026-2608.17826-bounded-state-restoration-decoupling-local-restore-capacity-from-external-llm-state.md)**  
  実装：[✓](https://github.com/StarkLeeSunny/Flexkv-doublenode) ・ リポジトリ内被引用：0  
  外部KV状態の全ヒットを先に把握しつつ、復元はWチャンク窓だけを順次ステージングして解放することで、長大な外部状態とローカル復元メモリを分離する方式。

- **2026-08 · [Bole: Efficient Tree Speculation for Hybrid-Attention Language Models](2026-2608.01651-bole-efficient-tree-speculation-for-hybrid-attention-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  再帰型線形注意の木検証を厳密閉形式で並列化し、因子化状態とhardware-aware予算をSGLangへ統合して最大4.72倍のデコード スループットを実現。

- **2026-08 · [Beyond Sparse Weights: When Is Attention Compressible?](2026-2608.21541-beyond-sparse-weights-when-is-attention-compressible.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎な注意マップだけではKV圧縮を正当化できないことを理論化し、値分散配分と末尾要約を厳密な物理予算で実装するCertKVを提案。

- **2026-08 · [AsymSpec: Efficient Cloud-Edge Speculative Decoding over Asymmetric Networks](2026-2608.04974-asymspec-efficient-cloud-edge-speculative-decoding-over-asymmetric-networks.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  非対称回線向けの証明付き段階補正と確認済み要求間パイプラインを組み合わせ、クラウド・エッジ投機的復号の通信待ちと無効先読みを削減する。

- **2026-08 · [AFD-Ledger: Deployment Provisioning for Attention--FFN Disaggregation](2026-2608.04502-afd-ledger-deployment-provisioning-for-attention-ffn-disaggregation.md)**  
  実装：[✓](https://github.com/kvcache-ai/AFD-Ledger) ・ リポジトリ内被引用：0  
  AFDと同居配置を同一予算・TPOT SLOで独立最適化し、少数のハードウェア組だけを完全評価して最適配置を探索する分析プロビジョニング系。

- **2026-08 · [A Probabilistic Interpretation of KV Cache Eviction](2026-2608.28293-a-probabilistic-interpretation-of-kv-cache-eviction.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  KV追放を期待値推定として定式化し、確率的追放＋復号時重要度補正で既存top-kのバイアスを抑えタスク間頑健性を高める。

- **2026-08 · [2026-2608.24945-fampwq-fisher-information-based-adaptive-mixed-precision-weight-quantization-for-effective-llm-inference](2026-2608.24945-fampwq-fisher-information-based-adaptive-mixed-precision-weight-quantization-for-effective-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低ビット重み量子化はGPUメモリと重み転送量を減らせるが、全層を同じビット数へ落とすと敏感な層の誤差がモデル品質を大きく壊す。7モデル・5ベンチマーク・7比較方式で、困惑度を最大3.39小さく、精度を最大6.87ポイント高くし、LLM判定比較では最大76%の勝率を報告する。

- **2026-08 · [2026-2608.24411-resispec-enhancing-multi-candidate-speculative-sampling-via-residual-distribution-shaping](2026-2608.24411-resispec-enhancing-multi-candidate-speculative-sampling-via-residual-distribution-shaping.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数候補方式は候補数を増やせば受理確率が上がるように見えるが、最初の候補が棄却されると対象分布からその候補確率を差し引いた残差分布へ移り、元のドラフト分布と急速にずれる。対象モデルの厳密な出力分布を変えず、既存の最先端複数候補方式に対して最大1.92倍の高速化を報告する。

- **2026-08 · [2026-2608.15531-flashquant-sparse-dense-fusion-for-memory-efficient-outlier-aware-llm-inference](2026-2608.15531-flashquant-sparse-dense-fusion-for-memory-efficient-outlier-aware-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  外れ値認識量子化では大半の重みを4ビットへ圧縮し、誤差を生みやすい少数の大振幅重みだけを高精度の疎行列として分離する。評価ではBF16のcuBLASに対して2.74〜4.18倍、最も強い非融合外れ値認識比較方式に対して最大1.53倍の高速化を報告する。

- **2026-08 · [2026-2608.03867-heterogeneity-aware-microscaling-for-efficient-low-bit-llm-inference](2026-2608.03867-heterogeneity-aware-microscaling-for-efficient-low-bit-llm-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  4ビットのMXFP4はブロック単位の共有尺度で低ビット推論を実現するが、すべてのブロックへ同じ要素形式と精度回復方式を適用するため、量子化しやすさの違いを十分に利用できない。3B〜70BモデルでMXFP4が失う精度のうち常識推論で83%、MMLUで82%を回復し、NVFP4に対してもそれぞれ43%、27%の損失を回復する。

- **2026-08 · [2026-2608.02703-archead-activation-metric-residual-correction-for-large-language-model-output-heads](2026-2608.02703-archead-activation-metric-residual-correction-for-large-language-model-output-heads.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  既存の重み量子化はトランスフォーマー本体を4ビットへ縮めても、語彙全体へロジットを出す最終言語モデルヘッドをBF16やFP16で残す実装がある。Qwen3-8Bではこの射影だけで約1.18GBになる。

- **2026-07 · [SelectInfer: Selective Neuron Loading and Computation for On-Device LLMs](2026-2607.18081-selectinfer-selective-neuron-loading-and-computation-for-on-device-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  オフラインで重要FFNニューロンを選別して必要分だけロードし、入力ごとの活性で計算対象も絞ることで、端末LLMのメモリ量と計算量を独立に調整する方式。

- **2026-07 · [LLMET: Enabling Cross-Layer Evaluation of Emerging M3D Memories for Energy-Efficient LLM Serving](2026-2607.26491-llmet-m3d-memory-energy-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  LLMETは、LLMのタイル配置とメモリ階層転送を回路レベルのSRAM・M3D特性へ接続し、L2容量を増やす利益とアクセス費が釣り合う省エネ設計点を探索する。

- **2026-07 · [LaCache: Exact Caching and Precision-Adaptive Inference for Diffusion Large Language Models](2026-2607.16339-lacache-exact-caching-precision-adaptive-dllm.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  拡散型LLMの反復生成で不変なトークン状態とFlashAttention中間状態を無損失再利用し、第2層以降をFP8化して、既存の生成ステップ削減法と組み合わせ可能な推論高速化を実現する。

- **2026-07 · [I/o for LLM inference: a survey of storage and memory bottlenecks](2026-5e022a2789e7-i-o-for-llm-inference-a-survey-of-storage-and-memory-bottlenecks.md)**  
  実装：[✓](https://github.com/rch0wdhury/llm-io-profiler) ・ リポジトリ内被引用：0  
  LLMデコードのデータ移動を重み・KVキャッシュ・活性の三I/O流へ分解し、量子化からSSD/CXL/統合メモリまでをルーフライン上で統一して、最適化を積むと支配ボトルネックが移動することを定量化したサーベイ。

- **2026-07 · [From Expert Reduction to Behavioral Divergence: Tracing Numerical State through Sparse MoE Inference](2026-2607.28097-from-expert-reduction-to-behavioral-divergence-tracing-numerical-state-through-sparse-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  疎MoEの専門家加算順序だけで内部状態と生成文が分岐しうることを全順列・状態再構成で実証し、BF16項＋FP32累算を評価範囲の安定な互換契約として特定する。

- **2026-07 · [Enabling Spatially Fine-Grained DVFS in Neural Processing Units for Energy-Efficient LLM Serving](2026-2607.16473-enpu-component-level-dvfs-npu-llm-serving.md)**  
  実装：[✓](https://github.com/google-coral/coralnpu（ベースコア）。eNPUの改変実装・シミュレータの公開URLは一次資料に記載なし。) ・ リポジトリ内被引用：0  
  eNPUは、演算器・SRAM・HBM・接続を別電圧周波数領域に分け、非同期転送と演算子別計画をSLO余裕で切替えて、NPUサービングの非ボトルネック電力を落とす。

- **2026-07 · [DynaCalKV: Key-Value Cache Compression via Head Grouping and Adaptive Rank Allocation](2026-2607.24331-dynacalkv-key-value-cache-compression-via-head-grouping-and-adaptive-rank-allocation.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  キー投影の注意ヘッドをCKA類似度で動的に群分けし、群ごとの情報量に応じて低ランク次元を配分することでReCalKVよりキー側パラメータを減らすが、GQAの長文脈では精度低下も確認する。

- **2026-07 · [CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool](2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CXL共有メモリをノード間GPU集団通信の媒体として使い、データ配置・細粒度重畳・ドアベル同期でRDMA型通信に対する性能とコストを改善する。

- **2026-07 · [3DLS: A 3D Logic-Stacked Architecture for Disaggregated LLM Serving](2026-2607.01617-3dls-disaggregated-serving-interconnect.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  プリフィル→デコードのKV転送とデコード側テンソル並列AllReduceを同じ横方向リンクで競合させず、KVだけを3D縦リンクへ物理分離するチップレット構成。等帯域条件でも最大1.49倍のスループットと60.2%の遅延削減を示す。

- **2026-07 · [2026-2607.07862-cta-pipelining-a-latency-oriented-spatial-scaling-method-for-multi-gpu-systems](2026-2607.07862-cta-pipelining-a-latency-oriented-spatial-scaling-method-for-multi-gpu-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CUTLASS、cuBLAS、NCCLを使いH200/B200最大8GPUで評価し、MLPを模した2層GEMMで最適化したマイクロバッチ方式より最大31.8%、テンソル並列（テンソル Parallelism; TP）より最大29.6%遅延を削減した。

- **2026-06 · [Unified KV Pooling to Accelerate Long-Context LLM Serving](2026-2606.14779-unified-kv-pooling-to-accelerate-long-context-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  複数RAM/SSDを帯域幅比例の単一KVプールとして並列利用し、SPDK直アクセスでファイルシステムを迂回して長文脈KV再取得を高速化する。

- **2026-06 · [SMEPilot: Characterizing and Optimizing LLM Inference with Scalable Matrix Extensions](2026-2606.16332-smepilot-characterizing-and-optimizing-llm-inference-with-scalable-matrix-extensions.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPU内のSMEと通常コアを共有帯域込みのルーフラインで使い分け、タイル分割・注意パイプライン・配置再利用によりLLM推論をllama.cpp比最大3.94倍高速化する。

- **2026-06 · [Omni-Flow: A Unified Workflow Orchestration and Distributed KV Cache Sharing Framework for Multimodal Inference](2026-2606.31093-omni-flow-a-unified-workflow-orchestration-and-distributed-kv-cache-sharing-framework-for-multimodal-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  中心的な発想は、モデル固有コードへ混在していた制御、テンソル転送、KVキャッシュ共有を、制御フロー（Control Flow）、データフロー（Data Flow）、計算フロー（Compute Flow）の三層へ分離することにある。

- **2026-06 · [LiveServe: Interaction-Aware Serving for Real-Time Omni-Modal LLMs](2026-2606.22983-liveserve-interaction-aware-serving-for-real-time-omni-modal-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  音声対話の再生進捗・発話・割込みをスケジューリングとKV配置へ反映し、不要な先行生成を抑えながら次ターンのKVを発話中に先読みし、P90初回音声遅延と無駄計算を同時に減らす。

- **2026-06 · [High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration](2026-2607.16248-high-accuracy-low-bit-kv-cache-quantization-via-local-distribution-restoration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  1ビットKVキャッシュを維持したまま、量子化で崩れた高確率候補の局所順位だけを検出・補正し、RULER精度を47.8%から83.2%へ回復するDGAP。

- **2026-06 · [HERALD: High-Throughput Block Diffusion LLM Serving via CPU-GPU Cooperative KV Cache Retrieval](2026-2606.21633-herald-high-throughput-block-diffusion-llm-serving-via-cpu-gpu-cooperative-kv-cache-retrieval.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ブロック拡散LLMのKV再利用性を利用し、CPUで1回選択した疎KVをGPUへ先読みしてデノイズと重畳し、5% KV予算で最大2.28倍の処理量を実現する。

- **2026-06 · [Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving](2026-2606.20537-execution-state-capsules-graph-bound-execution-state-checkpoint-and-restore-for-low-latency-small-batch-on-device-physic.md)**  
  実装：[✓](https://github.com/flashrt-project/FlashRT) ・ リポジトリ内被引用：0  
  KVだけでなく再帰・畳み込み・複数トークン予測状態を丸ごと保存復元し、単一ストリーム再入場の初回応答を最大26.94倍高速化する実行状態カプセル。

- **2026-06 · [Dustin: Draft-Augmented Sparse Verification for Efficient Long-Context Generation with Speculative Decoding](2026-2606.24957-dustin-draft-augmented-sparse-verification-for-efficient-long-context-generation-with-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  対象側の過去注意とドラフト側の先読み注意を融合し、少数の意味検索ヘッドだけで検証用KVを選ぶことで、長文投機的デコードのKV読込を削減する。

- **2026-06 · [Characterizing Software Aging in GPU-Based LLM Serving Systems](2026-2606.11916-characterizing-software-aging-in-gpu-based-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  6種類のGPU LLMサービング構成を計216時間連続運転し、全構成でホスト側のメモリ経年劣化を検出。リーク率はvLLM V1単体+1.8KB/時からTriton+V0の+157KB/時まで大差があり、配置・ランタイム選択が長期信頼性を左右することを示す。

- **2026-06 · [BatchGen: An Architecture for Scalable and Efficient Batch Inference](2026-2606.21712-batchgen-an-architecture-for-scalable-and-efficient-batch-inference.md)**  
  実装：[✓](https://github.com/batchgen-project/batchgen) ・ リポジトリ内被引用：0  
  系列をイベント駆動コルーチン化して停止・結合・分割・移動を可能にし、MoEバッチ形成と長尾負荷分散を動的化して最大2.3倍の大規模高速化を示す。

- **2026-06 · [Above the Inner Loop: Exceeding Accelerate at LLM Prefill GEMM on the M1 AMX](2026-2606.25426-above-the-inner-loop-exceeding-accelerate-at-llm-prefill-gemm-on-the-m1-amx.md)**  
  実装：[✓](https://github.com/dbhan08/inferc) ・ リポジトリ内被引用：0  
  M1 AMXの内側ループがロード発行律速であることを切り分け、細粒度パネルで第2 AMXブロックを使い、重み事前パッキングを併用してllama.cppの128トークンfp32プリフィルを1.44倍高速化する。

- **2026-05 · [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的検証クエリが選ぶ重複KVブロックを一度だけ読み、厳密共有と近似共有、層間索引再利用、融合カーネルを比較して、長文脈の疎注意読出しを減らすシステム。

- **2026-05 · [Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU](2026-2605.20706-llamaweb.md)**  
  実装：[✓](https://github.com/ggml-org/llama.cpp) ・ リポジトリ内被引用：0  
  LlamaWebは静的メモリ計画、端末適応型WebGPUカーネル、量子化対応をllama.cppへ統合し、ブラウザ推論のメモリ消費とデコード性能を改善する。

- **2026-05 · [Efficient MoE Inference on Single Consumer-grade GPU with Dynamic Expert Caching](2020-2026.00101-efficient-moe-inference-on-single-consumer-grade-gpu-with-dynamic-expert-caching.md)**  
  実装：[✓](https://github.com/rzhang772/SMOE) ・ リポジトリ内被引用：0  
  プリフィルの動的エキスパート配置とデコードのトークン-wise予測取得を組み合わせ、単一RTX 4090で671B級MoEを高速化するCPU/GPUハイブリッド基盤。

- **2026-05 · [Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers](2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低帯域・分散オンチップ記憶のMT-3000向けに演算子、融合注意、三段パイプライン、混合並列を共同設計し、大規模LLM推論を実現。

- **2026-05 · [2026-2606.00946-lodestar-an-online-learning-llm-inference-router](2026-2606.00946-lodestar-an-online-learning-llm-inference-router.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  公開クラウドの同種8基A30クラスタと、A30 8基＋V100 8基の異種クラスタで評価し、強い接頭辞・負荷認識ヒューリスティックに対して平均TTFTを平均1.41倍、P99 TTFTを1.47倍改善し、条件によって異種クラスタでは4倍超の改善を示す。

- **2026-04 · [Unlocking the Edge deployment and ondevice acceleration of multi-LoRA enabled one-for-all foundational LLM](2026-2604.18655-ondevice-multilora-runtime.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  実行時LoRA入力・NPU向け最適化・並行生成・自己投機的復号を統合し、Galaxy S24/S25で多用途LLMを単一グラフ展開する。

- **2026-04 · [SpecFed: Accelerating Federated LLM Inference with Speculative Decoding and Compressed Transmission](2026-2604.25777-specfed-accelerating-federated-llm-inference-with-speculative-decoding-and-compressed-transmission.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  連合LLM投機的復号で上位K確率だけを送信し、2種の確率再構成と誤差上界により通信量を削減する方式。

- **2026-04 · [Serving Chain-structured Jobs with Large Memory Footprints with Application to Large Foundation Model Serving](2026-2604.14993-serving-chain-structured-jobs-with-large-memory-footprints-with-application-to-large-foundation-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散パイプライン型の大規模言語モデル推論を、モデルブロック配置、鍵値キャッシュ容量配分、オンライン負荷分散からなるサーバ鎖構成問題として定式化し、実サービング評価で平均応答時間を六十三から七十七パーセント削減する。

- **2026-04 · [KV Cache Offloading for Context-Intensive Tasks](2026-2604.08426-kv-cache-offloading-for-context-intensive-tasks.md)**  
  実装：[✓](https://github.com/yandex-research/context-intensive-kv-offloading) ・ リポジトリ内被引用：0  
  文脈集約型課題でKV退避の選択誤差を分析し、低ビット量子化によるYAKVで精度とスループットを改善する。

- **2026-04 · [Fleet: Hierarchical Task-based Abstraction for Megakernels on Multi-Die GPUs](2026-2604.15379-fleet-multi-die-gpu-megakernel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fleetは複数ダイGPUにチップレット単位の作業階層を追加し、永続カーネル内で同一L2を共有するCUを協調スケジュールしてLLMデコードの重み再利用と同期局所性を高める。

- **2026-04 · [ELMoE-3D: Leveraging Intrinsic Elasticity of MoE for Hybrid-Bonding-Enabled Self-Speculative Decoding in On-Premises Serving](2026-2604.14626-elmoe-3d-hybrid-bonding-self-speculative-moe-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  HBメモリ上の頻出エキスパート上位ビットをキャッシュ兼自己ドラフトとして使い、MoEの投機的デコードと重み転送を一体最適化する3D積層HW-SW協調方式。

- **2026-03 · [The Missing Memory Hierarchy: Demand Paging for LLM Context Windows](2026-2603.09023-pichay-demand-paging-context-windows.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント文脈を仮想メモリとしてページングし、古いツール結果を追い出して再参照時に復元する透明プロキシ。139万追い出しで0.0254%フォルト率を報告。

- **2026-03 · [Serving Hybrid LLM Loads with SLO Guarantees Using CPU-GPU Attention Piggybacking](2026-2603.12831-serving-hybrid-llm-loads-with-slo-guarantees-using-cpu-gpu-attention-piggybacking.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  CPUへ逃がした低優先度要求の注意計算を非同期化し、後続GPU密計算へ層単位で相乗りさせることで、SLOを守りながら低優先度スループットを最大9.85倍にする。

- **2026-02 · [Two-Stage Expert Offloading for Domain-Aware MoE Inference](2026-dacc3922b5b4-two-stage-expert-offloading-for-domain-aware-moe-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  領域別プリフィル事前読込と時間・層間・領域局所性によるデコード先読みを組み合わせ、MoEのCPU退避でI/O待ち50%削減、投影TPOT 3.45倍高速化、全常駐比33%メモリ削減を狙う。

- **2026-02 · [StreamServe: Adaptive Speculative Flows for Low-Latency Disaggregated LLM Serving](2026-2604.09562-streamserve-adaptive-speculative-flows-for-low-latency-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型プリフィル・デコード上で、複数指標による要求ルーティングと実行時適応する投機深度を閉ループ連携し、4×A800評価でテンソル並列vLLM比の平均レイテンシ15.75倍短縮・平均スループット4.4倍を報告する。

- **2026-02 · [ReviveMoE: Fast Recovery for Hardware Failures in Large-Scale MoE LLM Inference Deployments](2026-2602.21140-revivemoe-fast-hardware-failure-recovery.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  単一NPU障害時にサービング全体を再起動せず、要求状態・KVブロック表・MoE重み・通信領域・実行グラフを局所修復して大規模MoE推論を高速復旧する。

- **2026-01 · [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じ接頭辞を持つ系列のMLP・LayerNorm・射影を位置ごとに一度だけ計算し、結果を各系列へ複製して、バッチ内重複によるプリフィル計算とカーネル起動を減らす。

- **2026-01 · [PLA-Serve: A Prefill-Length-Aware LLM Serving System](2026-a30e37ff7d4b-pla-serve-a-prefill-length-aware-llm-serving-system.md)**  
  実装：[✓](https://github.com/Jianshu-She/LAPS) ・ リポジトリ内被引用：0  
  プリフィル長で短要求と長要求を別キュー・別実行モードへ分離し、待機窓、CUDA Graph形状クラスタリング、動的GPU割当で短要求の待ちと長要求の干渉を同時に抑える。

- **2026-01 · [LLM KV Cache Storage Using CXL Memory](2026-4885970e907b-llm-kv-cache-storage-using-cxl-memory.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  vLLMとLMCacheのKVキャッシュを4種類のCXLメモリへ退避して実機比較し、DRAM型・プール型CXLが長文脈でシステムDRAMに近い性能を保ち、122K入力でGPU VRAM比約9倍の要求スループットを示す。

- **2025-11 · [Scaling Graph Chain-of-Thought Reasoning: A Multi-Agent Framework with Efficient LLM Serving](2025-2511.01633-graph-cot-multi-agent-efficient-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Graph-CoTを分類・推論・行動・検索へ分業し、頂点単位KV再利用、優先度追い出し、検索と生成の重畳を組み合わせ、遅延最大90.3%減・スループット最大15.1倍を報告。

- **2025-11 · [Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications](2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  公平な2-GPU基準と複数KV転送階層・DVFSでプリフィル/デコード分離を再評価し、性能・省電力の優位が条件依存であることを示す。

- **2025-11 · [GoCkpt: Gradient-Assisted Multi-Step overlapped Checkpointing for Efficient LLM Training](2025-2511.07035-gockpt-gradient-assisted-multi-step-overlapped-checkpointing-for-efficient-llm-training.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  チェックポイント転送を複数学習ステップへ分散し、低精度勾配でCPU側の版を一貫状態へ再構築することで、GPU停止を大幅に隠して学習スループットを最大約40%改善する。

### 2年前（2024-10〜2025-09）

- **2025-01 · [FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving](2025-2501.01005-flashinfer-attention-engine-serving.md)**  
  実装：[✓](https://github.com/flashinfer-ai/flashinfer) ・ リポジトリ内被引用：74  
  多様なKV配置と注意派生形をブロック疎形式と実行時コンパイルで統一し、可変系列長を固定CTAへ動的に負荷均衡しながらCUDAグラフ互換性も保つ、LLMサービング向け高性能注意エンジン。

- **2025-08 · [Dream 7B: Diffusion Large Language Models](2025-2508.15487-dream-7b-diffusion-large-language-models.md)**  
  実装：[✓](https://github.com/DreamLM/Dream) ・ リポジトリ内被引用：16  
  自己回帰モデルから初期化した70億拡散言語モデルで、系列全体の反復復元により計画課題と任意順生成を強化し、推論反復数で品質と速度を調整する。

- **2025-04 · [JITServe: SLO-aware LLM Serving with Imprecise Request Information](2025-2504.20068-jitserve-slo-aware-llm-serving-with-imprecise-request-information.md)**  
  実装：✓ ・ リポジトリ内被引用：12  
  不確かな出力長と依存関係を逐次更新し、期限達成に必要な最小帯域で要求を選ぶことで、サービス有効処理量を1.4〜6.3倍へ改善する。

- **2025-02 · [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/bytedance/flux) ・ リポジトリ内被引用：11  
  分散MoEでデータが全到着するまで待たず、届いたタイルから専門家GEMMを始め、GPU間全対全通信を計算の裏へ重ねて同期待ちを減らすランタイム。

- **2024-10 · [ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving](2024-2410.01228-conserve-fine-grained-gpu-harvesting-for-llm-online-and-offline-co-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：10  
  SLO予測付きトークン調整・層単位プリエンプション・増分KV退避で、オンライン遅延を守りながら遊休GPUをオフライン推論へ回す共同サービング方式。

- **2025-09 · [Fast-dLLM v2: Efficient Block-Diffusion LLM](2025-2509.26328-fast-dllm-v2-block-diffusion-hierarchical-cache.md)**  
  実装：[✓](https://github.com/NVlabs/Fast-dLLM/tree/main/v2) ・ リポジトリ内被引用：7  
  自己回帰モデルをブロック拡散へ少量追加学習し、ブロック間KVキャッシュとブロック内DualCache、信頼度並列復号を階層化して品質を保ちながら生成を高速化する。

- **2025-05 · [TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference](2025-2505.11329-tokenweave-efficient-compute-communication-overlap-for-distributed-llm-inference.md)**  
  実装：[✓](https://github.com/microsoft/tokenweave) ・ リポジトリ内被引用：6  
  GPU実行波を考慮した2分割とAllReduce–RMSNorm融合により、小さなテンソル並列バッチでも通信と計算を重ね、遅延とスループットを改善する。

- **2025-04 · [KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments](2025-2504.15364-keydiff-key-similarity-based-kv-cache-eviction-for-long-context-llm-inference-in-resource-constrained-environments.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  注意重みではなくキーの幾何学的多様性を重要度代理として使う学習不要KV削除法で、ブロック長文処理でも厳密な容量上限を守りつつ、8K予算で約23%削減・LongBench差0.04%以下、既存削除法比で遅延最大30%短縮を示す。

- **2025-06 · [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ドラフトGPU群と対象GPU群を分離して候補木生成と検証を同時実行し、検証済み接頭辞と未検証枝のKVを分けて再利用し、低バッチの同期・起動待ちを減らす投機的デコード。

- **2025-05 · [ELIS: Efficient LLM Iterative Scheduling System with Response Length Predictor](2025-2505.09142-elis-efficient-llm-iterative-scheduling-system-with-response-length-predictor.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  応答長を50トークンごとに再予測して短い残作業を優先し、LLM servingの先頭待ちを減らすKubernetes/vLLMスケジューラ。

- **2025-03 · [MoE-Gen: High-Throughput MoE Inference on a Single GPU with Module-Based Batching](2025-2503.09716-moe-gen-module-based-batching.md)**  
  実装：[✓](https://github.com/EfficientMoE/MoE-Gen) ・ リポジトリ内被引用：3  
  MoEの注意機構とエキスパートを別々にバッチ化し、ホストメモリでトークンを蓄積して大バッチ化することで、単一GPUオフロード推論のGPU利用率とスループットを改善する。

- **2025-02 · [Accelerating LLM Inference with Lossless Speculative Decoding Algorithms for Heterogeneous Vocabularies](2025-2502.05202-accelerating-llm-inference-with-lossless-speculative-decoding-algorithms-for-heterogeneous-vocabularies.md)**  
  実装：[✓](https://github.com/keyboardAnt/hf-bench) ・ リポジトリ内被引用：3  
  対象モデルと提案モデルの語彙が異なっても損失なし投機的復号を可能にし、既製モデルの自由な組合せで自己回帰復号比最大2.8倍高速化する。

- **2024-10 · [Minions: Accelerating Large Language Model Inference with Aggregated Speculative Execution](2024-2402.15678-minions-accelerating-large-language-model-inference-with-aggregated-speculative-execution.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  複数小型モデルの重み付き多数決、オンライン投機長調整、SSM/LLM非同期パイプラインを統合した投機的復号サービング。

- **2025-08 · [MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices](2025-2508.17137-moe-beyond-learning-based-expert-activation-prediction-on-edge-devices.md)**  
  実装：[✓](https://github.com/ngavhane/moe-beyond) ・ リポジトリ内被引用：2  
  トークン埋め込みと層IDから次のMoEエキスパートを予測する4層Transformerを学習し、10%容量のGPUキャッシュでMoE-Infinityの17%に対し約72%の適中率を示す。

- **2025-03 · [Collaborative Speculative Inference for Efficient LLM Inference Serving](2025-2503.10325-collaborative-speculative-inference-for-efficient-llm-inference-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  異種GPUへドラフト生成と検証を分離し、専門ドラフタ協調と動的パイプライン制御で投機推論の資源利用と受理率を改善する。

- **2025-08 · [TinyServe: Query-Aware Cache Selection for Efficient LLM Serving](2025-2509.12211-tinyserve-query-aware-cache-selection.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  QueryごとにKVページの関連度を軽量メタデータで推定し、必要ページだけを融合CUDAカーネルで読むことで小型LLMサービングの復号とメモリ移動を削減する。

- **2025-08 · [PiKV: KV Cache Management System for Mixture of Experts](2025-2508.06526-pikv-kv-cache-management-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/NoakLiu/PiKV) ・ リポジトリ内被引用：1  
  混合専門家モデルのKVを専門家単位に分散し、選択・圧縮・保持判断を統合する設計。第3版本文には独立した実測評価節がない。

- **2025-06 · [PecSched: Preemptive and Efficient Cluster Scheduling for LLM Inference](2024-2409.15104-csps-a-communication-efficient-sequence-parallelism-based-serving-system-for-transformer-based-models-with-long-prompts.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  長入力事前計算を短入力事前計算で選択的に横取りし、事前計算・復号の分離同居と高速系列並列を組み合わせて、短入力の待ち時間と長入力の飢餓を両立して抑える。

- **2025-06 · [EQuARX: Efficient Quantized AllReduce in XLA for Distributed Machine Learning Acceleration](2025-2506.17615-equarx-quantized-allreduce-xla.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  AllReduce内でブロック量子化と逆量子化を通信へ重ね、TPU/XLAの集団通信量を削減する方式。int8でBF16 AllReduce比最大1.8倍、Gemma 3 27Bプリフィル最大1.28倍を示す。

- **2024-12 · [IFMoE: An Inference Framework Design for Fine-grained MoE](2026-3190de0b4969-ifmoe-an-inference-framework-design-for-fine-grained-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  共有部分をテンソル並列化して細粒度MoEの重複メモリを減らし、少数専門家で草稿生成した後に完全専門家設定でKVキャッシュを修整して復号を高速化する。

- **2024-12 · [HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing](2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  問い合わせと鍵の短い局所性鋭敏型ハッシュ（LSH）間のハミング距離から注意度が低い候補を事前推定し、注意計算を実行する前に不要なKVキャッシュを動的に置換する。

- **2025-09 · [SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching](2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味的に近い別プロンプトをトークンLSHで対応付け、位置補正と層別再計算により完全一致なしでもKVを選択再利用する。

- **2025-07 · [CateKV: On Sequential Consistency for Long-Context LLM Inference Acceleration](2026-2608.30295-catekv-on-sequential-consistency-for-long-context-llm-inference-acceleration.md)**  
  実装：[✓](https://github.com/haoyun-jiang/CateKV) ・ リポジトリ内被引用：0  
  プリフィルからデコードまで注意先が安定するヘッドだけKVを強く削減し、動的ヘッドは大半を保持するハイブリッドKVキャッシュで、精度を保ちながら長文推論のメモリ・デコード・バッチ性能を改善する。

- **2025-06 · [MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices](2025-2506.10443-mnn-llm-mobile-inference-engine.md)**  
  実装：[✓](https://github.com/alibaba/MNN) ・ リポジトリ内被引用：0  
  DRAMとFlashの階層利用、役割別量子化、CPU/GPU別データ配置と負荷分散を統合し、スマートフォン上のLLM推論を高速・省メモリ化する。

- **2025-05 · [Recursive Offloading for LLM Serving in Multi-tier Networks](2025-2505.16502-recursive-offloading-for-llm-serving-in-multi-tier-networks.md)**  
  実装：[✓](https://github.com/wuzhiyuan2000/RecServe) ・ リポジトリ内被引用：0  
  端末→エッジ→クラウドを信頼度で再帰的に上げ、履歴分位点から閾値を自動適応してCloudServe比50%以上の通信削減を狙う多層LLMサービング。

- **2025-05 · [MorphServe: Efficient and Workload-Aware LLM Serving via Runtime Quantized Layer Swapping and KV Cache Resizing](2025-2506.02006-efficient-and-workload-aware-llm-serving-via-runtime-layer-swapping-and-kv-cache-resizing.md)**  
  実装：[✓](https://github.com/ds2-lab/MorphServe) ・ リポジトリ内被引用：0  
  負荷ピーク時だけ低影響層を低ビット版へ非同期交換し、空いたGPUメモリをKVキャッシュへ振り替えることで、平均SLO違反を92.45%削減しP95初回トークン遅延を2.2〜3.9倍改善する。

- **2025-04 · [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大バッチ投機的デコードの受理率とKV読出し量を実測し、浅くKVを制限したドラフトの性能モデルを構築して、重み読出しよりKV帯域が支配する条件の処理量を比較する研究。

- **2025-03 · [Reimagining Memory Access for LLM Inference: Compression-Aware Memory Controller Design](2025-2503.18869-reimagining-memory-access-for-llm-inference-compression-aware-memory-controller-design.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みとKVキャッシュをビットプレーン・チャネル単位に再配置して無損失圧縮を効かせ、動的量子化時は必要ビットだけを読むメモリ制御器で容量・帯域・エネルギーを同時に削減する。

- **2025-03 · [2025-2504.03664-pipo-pipelined-offloading-for-efficient-inference-on-consumer-devices](2025-2504.03664-pipo-pipelined-offloading-for-efficient-inference-on-consumer-devices.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  重みをGPUへ全て保持できない場合、層ごとにCPUから転送して実行すれば容量問題は解ける。PIPOはオフロードをより細かい単位へ分解し、データ転送とGPU計算を同時進行させる。RTX 3060 Laptop GPU 6GBという小容量環境で、比較方式では40%未満だったGPU利用率を90%超へ引き上げ、最大3.1倍の処理量を報告する。

- **2025-02 · [AutoHete: An Automatic and Efficient Heterogeneous Training System for LLMs](2025-2503.01890-autohete-an-automatic-and-efficient-heterogeneous-training-system-for-llms.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  活性値再計算・パラメータ退避・オプティマイザ退避を整数線形計画で共同選択し、反復をまたぐ優先度付き処理重畳でCPU/GPU待ちを減らす異種混在LLM学習方式。

### 3年前（2023-10〜2024-09）

- **2023-12 · [Mamba: Linear-Time Sequence Modeling with Selective State Spaces](2023-2312.00752-mamba-selective-state-space-linear-time-inference.md)**  
  実装：[✓](https://github.com/state-spaces/mamba) ・ リポジトリ内被引用：26  
  入力依存の選択的状態空間層とGPU向け融合走査を統合し、注意機構なしでTransformer級品質と4〜5倍の生成スループットを両立する。

- **2023-10 · [Ring Attention with Blockwise Transformers for Near-Infinite Context](2023-2310.01889-ring-attention-blockwise-transformers.md)**  
  実装：[✓](https://github.com/lhao499/llm_large_context) ・ リポジトリ内被引用：20  
  キー・値ブロックをリング転送しながらブロック注意計算を重畳し、系列長に依存しない活性化メモリで最大文脈長をデバイス数に比例して拡張する分散注意方式。

- **2023-10 · [DistillSpec: Improving Speculative Decoding via Knowledge Distillation](2023-2310.08461-distillspec-improving-speculative-decoding-via-knowledge-distillation.md)**  
  実装：✓ ・ リポジトリ内被引用：20  
  ドラフト自身の生成データと課題別の分布間距離でターゲットとの整合を蒸留し、投機的デコードの候補受理率を上げる手法。

- **2024-03 · [2024-2403.01876-dejavu-kv-cache-streaming-for-fast-fault-tolerant-generative-llm-serving](2024-2403.01876-dejavu-kv-cache-streaming-for-fast-fault-tolerant-generative-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：13  
  また各マイクロバッチのKVキャッシュをGPUに保持し続けるとメモリを過剰確保し、障害時には失われたKV状態を再計算するため復旧が遅い。DéjàVuはこれらをKVキャッシュの高速な非同期転送という一つの機構で扱う。

- **2024-07 · [2024-2407.04153-mixture-of-a-million-experts](2024-2407.04153-mixture-of-a-million-experts.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  通常のトランスフォーマーのフィードフォワード層は幅を増やすと計算量と活性値メモリも線形に増える。疎な混合専門家モデルは総パラメータと一トークン当たり計算を分離できるが、従来はルータ計算、専門家配置、学習安定性の制約から専門家数を数十から数千程度に抑えることが多かった。

- **2024-04 · [Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing](2024-2404.14618-hybrid-llm-cost-efficient-and-quality-aware-query-routing.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  要求ごとの品質差を予測して小型LLMへの振り分け率を調整し、推論費を削減する。モデル間の品質差が大きいときは無品質低下での削減幅が限られる。

- **2024-02 · [Decoding Speculative Decoding](2024-2402.01528-decoding-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  350件超の投機的デコード実験からドラフト遅延と層深度を主要因と特定し、浅く広いドラフトモデルへ再設計して最大111%のスループット向上を示す。

- **2024-01 · [CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference](2024-2401.11240-caraserve-cpu-assisted-lora-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：5  
  LoRA読込中にCPUでプリフィル計算を先行し、ランク依存のバッチ遅延を予測してSLO違反が少ないサーバへ配分することで、多数アダプタ提供のコールドスタートを隠す。

- **2024-06 · [ProTrain: Efficient LLM Training via Memory-Aware Techniques](2024-2406.08334-protrain-efficient-llm-training-via-memory-aware-techniques.md)**  
  実装：✓ ・ リポジトリ内被引用：2  
  モデル状態と活性値の階層管理を費用モデルで自動調整し、限られたGPUメモリで学習容量とスループットを高める。

- **2024-09 · [DisDP: Disaggregating Compute, Network, and Storage for Model-Sharded Data-Parallel Training](2024-2409.00918-luwu-an-end-to-end-in-network-out-of-core-optimizer-for-100b-scale-model-in-network-data-parallel-training-on-distribute.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  GPUから通信とオプティマイザ状態をSmartNIC・SmartSwitch・単一パラメータサーバへ分離し、100B級モデル分割データ並列の干渉と容量制約を同時に減らす。

### 4年前（2022-10〜2023-09）

- **2023-07 · [FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](2023-2307.08691-flashattention-2.md)**  
  実装：[✓](https://github.com/Dao-AILab/flash-attention) ・ リポジトリ内被引用：97  
  初代FlashAttentionのオンライン・ソフトマックスとタイル分割を保ちつつ、行列積以外の演算とブロック・ワープ間の仕事分割を再設計し、A100で理論演算性能の最大73%と初代比約2倍の高速化を達成する。

- **2023-05 · [2023-2305.13245-gqa](2023-2305.13245-gqa.md)**  
  実装：✓ ・ リポジトリ内被引用：52  
  標準の多頭注意（Multi-Head 注意機構; MHA）は各クエリ頭に独立した鍵頭と値頭を持つため、復号時には全KV頭のキャッシュを読み出す必要がある。

- **2022-11 · [Efficiently Scaling Transformer Inference](2022-2211.05102-efficiently-scaling-transformer-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：43  
  TPU v4上の大規模Transformer推論を通信・メモリ・計算モデルから設計し、2D重み固定/重み収集の切替とバッチ分割MQAで540B級の低遅延・高MFU・長文脈を両立する。

- **2022-11 · [2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models](2022-2211.10438-smoothquant-accurate-and-efficient-post-training-quantization-for-large-language-models.md)**  
  実装：✓ ・ リポジトリ内被引用：19  
  活性値全体を単純に8ビットへ写すと、その少数の外れ値が量子化範囲を広げ、通常値へ割り当てられる段階数が減って精度が崩れる。OPT、BLOOM、GLM、MT-NLGなどで8ビット重み・8ビット活性値（W8A8）を実現し、精度低下をほぼ抑えながら最大1.56倍の推論高速化と2倍のメモリ削減を報告し、530Bモデルを単一ノードで提供可能にした。

### 5年前（2021-10〜2022-09）

- **2022-05 · [FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](2022-2205.14135-flashattention.md)**  
  実装：[✓](https://github.com/HazyResearch/flash-attention) ・ リポジトリ内被引用：127  
  タイル化、オンラインsoftmax、逆伝播時再計算により二次元注意行列の高帯域メモリ往復を避ける厳密注意カーネル。

- **2022-06 · [2022-2207.00032-deepspeed-inference-enabling-efficient-inference-of-transformer-models-at-unprecedented-scale](2022-2207.00032-deepspeed-inference-enabling-efficient-inference-of-transformer-models-at-unprecedented-scale.md)**  
  実装：✓ ・ リポジトリ内被引用：15  
  モデル規模、疎性、遅延・処理量目標、GPU台数、メモリ階層が異なるため、一つの演算カーネルだけではTransformer推論全体を最適化できない。DeepSpeed Inferenceは、GPU内実行では演算融合と通信を意識したモデル並列、GPU容量を超える場合はCPU/NVMeから必要な重みを流す異種メモリ推論を統合する。

### 8年前（2018-10〜2019-09）

- **2019-04 · [Generating Long Sequences with Sparse Transformers](2019-1904.10509-generating-long-sequences-with-sparse-transformers.md)**  
  実装：✓ ・ リポジトリ内被引用：33  
  全結合の自己注意を局所窓と周期・固定要約位置へ因数分解して O(n√n) 化し、再計算と疎GPUカーネルを併用して数万〜100万要素の生成を可能にしたSparse Transformer。
<!-- survey:auto:end -->
