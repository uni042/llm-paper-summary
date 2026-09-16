# Other Inference Systems

推論効率化を主目的とするが、現時点では他の系統へ自然に入らず、**独立系統を作るほど同種研究がまだ集まっていない手法**を置く。ここに論文が増えて共通した問題設定・主要技術・評価軸が見えてきた場合は、新しい系統へ分割する。

<!-- survey:auto:start -->
## 自動生成の論文一覧（35本）

分類は相互排他的。直近12か月は公開年月ベース（現在は **2025-10〜2026-09**）。直近12か月でリポジトリ内被引用が1件以上ある論文は注目枠へ分離し、それ以前は現在月から12か月単位の「2年前」「3年前」…に分け、各区分内を引用数順に並べる。「リポジトリ内被引用」は収録済み別論文の一次資料の参考文献欄を構造化した `references` から、同一リポジトリ内論文への参照を数える。
「実装」は論文メタデータで明示されたコード／実装情報のみを表示し、未確認は `—` とする。

### 注目：直近12か月・リポジトリ内で被引用（2025-10〜2026-09）

- **2026-03 · [ZipServ: Fast and Memory-Efficient LLM Inference with Hardware-Aware Lossless Compression](2026-2603.17435-zipserv-fast-memory-efficient-llm-inference-hardware-aware-lossless-compression.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  BF16重みの指数を固定長ビットマップへ無損失符号化し、圧縮データをレジスタ上で復元してテンソル Coreへ直送することで、重み帯域と中間展開の読み書きを減らす。

- **2026-07 · [Rethinking AI Cloud Infrastructure for Agentic Serving Systems with the Aries Experimentation Framework](2026-2607.29069-rethinking-ai-cloud-infrastructure-for-agentic-serving-systems-with-the-aries-experimentation-framework.md)**  
  実装：[✓](https://github.com/hyscale-lab/aries) ・ リポジトリ内被引用：1  
  AriesはLLM推論、ハーネス、状態付きツールを一つのエージェント軌跡として計測し、ツール待ち、長期文脈、サンドボックスの瞬間的な資源需要を同じタスク進捗へ結び付ける実験基盤である。

- **2026-06 · [KernelSight-LM: A Kernel-Level LLM Inference Simulator](2026-2606.28565-kernelsight-lm-kernel-level-inference-simulator.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  GPUカーネル予測と実運用サービングの離散事象モデルを統合し、未計測GPUでもカーネル誤差12.1%、対象計測ありで3.8%を達成。

- **2026-02 · [AgentCgroup: Understanding and Controlling OS Resources of AI Agents](2026-2602.09345-agentcgroup-understanding-and-controlling-os-resources-of-ai-agents.md)**  
  実装：[✓](https://github.com/eunomia-bpf/agentcgroup) ・ リポジトリ内被引用：1  
  AIエージェント144課題のOS資源変動を測定し、OS処理55〜60%、メモリピーク最大15.4倍を確認。ツール呼出し単位cgroupとeBPF制御で競合時の生存率100%と高優先度P95割当遅延29%削減を示す。

### 直近12か月・未被引用（2025-10〜2026-09）

- **2026-09 · [Unlocking Lossless Speedups in LLMs via Discrete Diffusion](2026-2609.04010-unlocking-lossless-speedups-in-llms-via-discrete-diffusion.md)**  
  実装：[✓](https://github.com/ifm-ai/uno) ・ リポジトリ内被引用：0  
  元の自己回帰モデル分布を保ったまま追加した離散拡散重みで複数トークンを並列提案し、専用サンプラで正しく補正して、逐次デコードの重み読出し回数を減らす。

- **2026-09 · [Speculative Macro Commit for Faster Tool-Using Agents](2026-2609.03236-speculative-macro-commit-for-faster-tool-using-agents.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  ドラフトモデルが隔離環境でツール操作列を先行実行し、権威モデルが先頭操作を確認したマクロだけ後続操作と観測をまとめて確定して、大型モデル呼出しとツール待ちを減らす。

- **2026-09 · [Separating Stream Stability from Long-Term Recall in Language Models](2026-2609.07282-stream-stability-long-term-recall-threeh.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長時間生成の安定性・過去情報への因果アクセス・タスク効用をThreeHの3到達距離へ分離し、注意シンクの安定生成を長期記憶と誤認しない評価契約を示す。

- **2026-09 · [RoofLang: Enabling AI-Driven Architecting of LLM Inference Systems](2026-2609.12551-rooflang-ai-driven-llm-inference-architecting.md)**  
  実装：[✓](https://github.com/yzygitzh/rooflang) ・ リポジトリ内被引用：0  
  RoofLangはLLM推論を計算・ハードウェアグラフと意味保存変換で表し、実装非依存のシミュレーションを評価器としてAIに配置・並列化・通信構成を探索させる設計基盤である。

- **2026-09 · [PipeSwift: Revisiting Pipeline Parallelism for Large-Scale Completion-Oriented Agentic LLM Serving](2026-2609.16491-pipeswift-pipeline-parallel-agentic-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  エージェント推論のJCTをプリフィルとデコードの均衡問題として捉え直し、JCT指向スケジューリングとMTP統合パイプライン並列で64基H800上の360B級MoE処理を高速化する。

- **2026-09 · [PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling](2026-2609.09662-pelm-speculative-decoding-dvfs.md)**  
  実装：[✓](https://github.com/imec-nu/PELM) ・ リポジトリ内被引用：0  
  DVFS・自己投機的デコード・可変検証深度を深層強化学習で共同制御し、端末LLMで最大23.1%高速化・52.4%エネルギー削減を達成する。

- **2026-09 · [Kalman Delta Networks: Uncertainty-aware Associative Memory](2026-2609.07816-kalman-delta-networks-associative-memory.md)**  
  実装：[✓](https://github.com/ngocbh/kalman-delta-networks) ・ リポジトリ内被引用：0  
  固定サイズの線形注意メモリに推定不確実性を持たせ、蓄積証拠に応じて上書き強度をカルマン利得から決めることで、長文脈検索と生成精度を改善する。

- **2026-09 · [ECOKV: Geometry-Aware KV Cache Eviction via Complementary Diversity Metrics](2026-2609.06663-ecokv-geometry-aware-kv-cache-eviction-via-complementary-diversity-metrics.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  コサイン類似度だけでは見落とすKV表現の大きさをユークリッド距離で補い、注意ヘッドごとの冗長度に応じて多様性と重要度を混合し、狭いKV予算で保持トークンを改善する方式。

- **2026-09 · [Dynamic Semantic Compression for Efficient Latent-Space Inference in Large Language Models](2026-2609.15338-dynamic-semantic-compression-latent-space-inference.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  文を長さに応じて1〜3区間へ分割し、重要トークンを重み付けした潜在表現を生成・復号するDSEI。固定文圧縮より品質を改善し、トークン単位推論より系列長とメモリ負荷を削減する。

- **2026-09 · [Dissecting GPU Utilization for LLM Inference on Nvidia Hopper](2026-2609.12923-dissecting-gpu-utilization-llm-inference-hopper.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  H100上のLLM推論を8種類のNsight指標で分解し、デコードでは帯域待ちに加えGMMA m64固定断片の1.56～12.5%充填やwave損失が単一SM利用率に隠れることを示す。

- **2026-08 · [Launch-Bound and Substitutable: Why Three Inference Optimizations Fail to Pay Off in Mixture-of-Experts Models](2026-2608.26612-launch-bound-and-substitutable-moe-inference-optimizations.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  MoEの融合カーネル・4/8ビット量子化・グラフコンパイルを単体とE2Eで測定し、局所高速化が起動律速や品質へどう波及するかを分解して、置換可能な最適化の限界を明らかにする研究。

- **2026-08 · [FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration](2026-2608.25062-flint-efficiently-leveraging-high-bandwidth-flash-for-capacity-scalable-llm-inference-acceleration.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  高帯域フラッシュを巨大モデル重みの近接容量層として使い、動的読み出し結合・更新隔離・読み出し専用変換表で従来方式比六・二倍の復号処理量を実現する。

- **2026-08 · [Adaptive KV Retention for LLM Agents at Human-Approval Timescales](2026-2608.30830-adaptive-kv-retention-for-llm-agents-at-human-approval-timescales.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  人間承認で長時間停止するエージェントのKVをHBM・CPU DRAM・破棄の三段階で管理し、各選択をGPU機会費用へ換算して負荷に応じた保持期限を決める。

- **2026-06 · [Characterizing Software Aging in GPU-Based LLM Serving Systems](2026-2606.11916-characterizing-software-aging-in-gpu-based-llm-serving-systems.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  6種類のGPU LLMサービング構成を計216時間連続運転し、全構成でホスト側のメモリ経年劣化を検出。リーク率はvLLM V1単体+1.8KB/時からTriton+V0の+157KB/時まで大差があり、配置・ランタイム選択が長期信頼性を左右することを示す。

- **2026-05 · [SpecSA: Bridging Speculative Decoding and Sparse Attention for Efficient LLM Inference](2026-2605.19893-specsa-sparse-speculative-verification.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  投機的検証クエリが選ぶ重複KVブロックを一度だけ読み、厳密共有と近似共有、層間索引再利用、融合カーネルを比較して、長文脈の疎注意読出しを減らすシステム。

- **2026-05 · [GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving](2026-2605.22566-graphflow-agent-workflow-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有操作グラフからエージェント手順を動的生成し、操作単位の差分KV状態で約4倍のメモリ削減を狙うエージェント・サービング基盤。

- **2026-05 · [Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers](2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  低帯域・分散オンチップ記憶のMT-3000向けに演算子、融合注意、三段パイプライン、混合並列を共同設計し、大規模LLM推論を実現。

- **2026-04 · [Serving Chain-structured Jobs with Large Memory Footprints with Application to Large Foundation Model Serving](2026-2604.14993-serving-chain-structured-jobs-with-large-memory-footprints-with-application-to-large-foundation-model-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分散パイプライン型の大規模言語モデル推論を、モデルブロック配置、鍵値キャッシュ容量配分、オンライン負荷分散からなるサーバ鎖構成問題として定式化し、実サービング評価で平均応答時間を六十三から七十七パーセント削減する。

- **2026-04 · [Fleet: Hierarchical Task-based Abstraction for Megakernels on Multi-Die GPUs](2026-2604.15379-fleet-multi-die-gpu-megakernel.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  Fleetは複数ダイGPUにチップレット単位の作業階層を追加し、永続カーネル内で同一L2を共有するCUを協調スケジュールしてLLMデコードの重み再利用と同期局所性を高める。

- **2026-03 · [ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs](2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md)**  
  実装：[✓](https://github.com/OpenBMB/ArcLight) ・ リポジトリ内被引用：0  
  NUMAごとのメモリ配置、動的スレッド群、Scatter/Gather型テンソル並列を一体化し、多数コアCPUの遠隔メモリアクセス壁を避けて、192コアARM環境でllama.cpp比最大46%高い推論スループットを示す軽量CPU推論基盤。

- **2026-02 · [StreamServe: Adaptive Speculative Flows for Low-Latency Disaggregated LLM Serving](2026-2604.09562-streamserve-adaptive-speculative-flows-for-low-latency-disaggregated-llm-serving.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  分離型プリフィル・デコード上で、複数指標による要求ルーティングと実行時適応する投機深度を閉ループ連携し、4×A800評価でテンソル並列vLLM比の平均レイテンシ15.75倍短縮・平均スループット4.4倍を報告する。

- **2026-01 · [RadixMLP — Intra-batch Deduplication for Causal Transformers](2026-2601.15013-radixmlp-intra-batch-deduplication.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  同じ接頭辞を持つ系列のMLP・LayerNorm・射影を位置ごとに一度だけ計算し、結果を各系列へ複製して、バッチ内重複によるプリフィル計算とカーネル起動を減らす。

### 2年前（2024-10〜2025-09）

- **2025-02 · [Comet: Fine-grained Computation-communication Overlapping for Mixture-of-Experts](2025-2502.19811-comet-fine-grained-computation-communication-overlapping-for-mixture-of-experts.md)**  
  実装：[✓](https://github.com/bytedance/flux) ・ リポジトリ内被引用：7  
  分散MoEでデータが全到着するまで待たず、届いたタイルから専門家GEMMを始め、GPU間全対全通信を計算の裏へ重ねて同期待ちを減らすランタイム。

- **2025-04 · [KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments](2025-2504.15364-keydiff-key-similarity-based-kv-cache-eviction-for-long-context-llm-inference-in-resource-constrained-environments.md)**  
  実装：✓ ・ リポジトリ内被引用：4  
  注意重みではなくキーの幾何学的多様性を重要度代理として使う学習不要KV削除法で、ブロック長文処理でも厳密な容量上限を守りつつ、8K予算で約23%削減・LongBench差0.04%以下、既存削除法比で遅延最大30%短縮を示す。

- **2025-06 · [SwiftSpec: Ultra-Low Latency LLM Decoding by Scaling Asynchronous Speculative Decoding](2025-2506.11309-swiftspec-asynchronous-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：3  
  ドラフトGPU群と対象GPU群を分離して候補木生成と検証を同時実行し、検証済み接頭辞と未検証枝のKVを分けて再利用し、低バッチの同期・起動待ちを減らす投機的デコード。

- **2024-12 · [HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing](2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md)**  
  実装：✓ ・ リポジトリ内被引用：1  
  問い合わせと鍵の短い局所性鋭敏型ハッシュ（LSH）間のハミング距離から注意度が低い候補を事前推定し、注意計算を実行する前に不要なKVキャッシュを動的に置換する。

- **2025-09 · [SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching](2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  意味的に近い別プロンプトをトークンLSHで対応付け、位置補正と層別再計算により完全一致なしでもKVを選択再利用する。

- **2025-06 · [PecSched: Preemptive and Efficient Cluster Scheduling for LLM Inference](2024-2409.15104-csps-a-communication-efficient-sequence-parallelism-based-serving-system-for-transformer-based-models-with-long-prompts.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  長入力事前計算を短入力事前計算で選択的に横取りし、事前計算・復号の分離同居と高速系列並列を組み合わせて、短入力の待ち時間と長入力の飢餓を両立して抑える。

- **2025-05 · [MorphServe: Efficient and Workload-Aware LLM Serving via Runtime Quantized Layer Swapping and KV Cache Resizing](2025-2506.02006-efficient-and-workload-aware-llm-serving-via-runtime-layer-swapping-and-kv-cache-resizing.md)**  
  実装：[✓](https://github.com/ds2-lab/MorphServe) ・ リポジトリ内被引用：0  
  負荷ピーク時だけ低影響層を低ビット版へ非同期交換し、空いたGPUメモリをKVキャッシュへ振り替えることで、平均SLO違反を92.45%削減しP95初回トークン遅延を2.2〜3.9倍改善する。

- **2025-04 · [SPIRe: Boosting LLM Inference Throughput with Speculative Decoding](2025-2504.06419-spire-throughput-speculative-decoding.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  大バッチ投機的デコードの受理率とKV読出し量を実測し、浅くKVを制限したドラフトの性能モデルを構築して、重み読出しよりKV帯域が支配する条件の処理量を比較する研究。

- **2024-12 · [IFMoE: An Inference Framework Design for Fine-grained MoE](2026-3190de0b4969-ifmoe-an-inference-framework-design-for-fine-grained-moe.md)**  
  実装：✓ ・ リポジトリ内被引用：0  
  共有部分をテンソル並列化して細粒度MoEの重複メモリを減らし、少数専門家で草稿生成した後に完全専門家設定でKVキャッシュを修整して復号を高速化する。
<!-- survey:auto:end -->
