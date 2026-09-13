# 運用ダッシュボード

> 自動生成: **2026-09-14 08:28 JST**。正本は `.survey/work-queue/` のdurable stateです。

## このページの見方

上から順に、**現在の詰まり具合 → workerの稼働状況 → 直近24時間の処理量 → 最新run → 次に読む論文** を確認できます。日常確認はここまでで十分です。下部の「参考情報」は探索効率や履歴を詳しく見るための欄です。

- **Research ready**: まだ全文精読が終わっていない論文候補。値が大きいほど「読む仕事」が溜まっています。
- **Claim**: workerが処理権を確保している状態。Active claimsは処理中、Claimableは今すぐ別workerが着手できる件数です。
- **Audit**: 既存の論文ページや要約の品質点検。新規論文の全文精読（Research）とは別工程です。
- **Maintenance / Consistency**: queueやstateの定期保守と、リポジトリ全体の整合性チェックです。

## 現在の状態

| 指標 | 状態 |
|---|---:|
| 未処理の論文候補（Research ready） | **122** |
| 現在処理不能（Research blocked） | **0** |
| 保留中（Research deferred） | **3** |
| 全文精読完了（累計） | **267** |
| 保守状態（Maintenance） | **pending** |
| 整合性チェック（Consistency） | **passed** |
| 次回保守までの通常run | **0 / 24** |

### 要注意

- Maintenance が pending です。
- 候補補充がResearch消化を大きく上回っています。ready在庫の増加を監視。

<!-- research-throughput-status:start -->
## ワーカー稼働状況

| 指標 | 状態 |
|---|---:|
| :30 通常worker | **Research/Audit優先（高在庫）** |
| :00 補助worker | **通常worker補助（Research/Audit）** |
| 処理速度 | **LOW** |
| 未処理候補（Research ready） | **122** |
| 処理中（Active claims） | **3** |
| 今すぐ着手可能（Claimable） | **119** |
| :30 通常worker Active claims | **0** |
| :00 補助worker Active claims | **2** |
| その他/帰属不明 Active claims | **1** |
| :30 通常worker 直近claim | **09-14 06:56 JST** |
| :00 補助worker 直近claim | **09-14 08:28 JST** |
| 直近24h Research完了（:30 通常worker） | **5** |
| 直近24h Research完了（:00 補助worker） | **5** |
| 直近24h Research完了（帰属不明） | **7** |
| 最新通常run | **2026-09-14T05:30:00+09:00** |
| 最新通常runのResearch完了 | **0** |
| 最古の有効claimの経過時間 | **29 min** |

Research readyが **50本を超える間は`:00` workerも論文精読側** に回り、**50本以下になると探索専用へ戻ります**。`:30`通常workerは、readyが **25本以上** で処理可能なResearchがある間はResearch/Auditを優先します。

高在庫時の通常runは、hard stopに達しない限り **最低3件** のResearch完了を下限目標にします。3件は上限・終了条件ではありません。

- **処理速度 LOW**: ready=122 の高在庫状態で、最新通常runのResearch完了は 0 件です。探索よりResearch消化を優先します。
- 直近24hのResearch完了のうち **7件** はclaim workerを復元できず、worker別集計では「帰属不明」としています。
<!-- research-throughput-status:end -->

## 直近24時間の処理量

| 指標 | 件数 / 率 |
|---|---:|
| Research完了 | **17** |
| Repo収録 | **58** |
| Audit完了 | **0** |
| 探索評価候補 | **171** |
| Research候補採用 | **36** |
| 重複除外 | **86** |
| 重複率 | **50.3%** |
| 探索専用worker run（毎時枠） | **3** |
| 探索専用worker round（stats観測） | **36** |
| 通常worker run（ledger観測） | **13** |
| Fallback archive（全helper） | **20** |

### 24時間の流れ

**探索評価 171 → 重複除外後 85 → Research候補採用 36 → Research完了 17 → Repo収録 58**

## 直近の通常worker

Run: **2026-09-14T05:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **0** |
| Repo収録 | **7** |
| Audit完了 | **0** |
| 通常worker Discovery round | **0** |
| 通常worker Discovery採用 | **0** |
| Research/Audit blocked遷移 | **0** |

## 次に処理する候補

`next-jobs.json` に見えている優先候補の先頭5件です。表示枠は処理量の上限ではありません。

- P87 `arXiv:2604.09083` — EdgeFlow: Fast Cold Starts for LLMs on Mobile Devices
- P87 `arXiv:2604.20503` — FASER: Fine-Grained Phase Management for Speculative Decoding in Dynamic LLM Serving
- P86 `arXiv:2505.14468` — ServerlessLoRA: Minimizing Latency and Cost in Serverless Inference for LoRA-Based LLMs
- P86 `arXiv:2609.11294` — Memory Compression for High-Fanout Agent Sandboxes
- P86 `arXiv:2608.14376` — CoRun: Padding is Simple and Efficient for Deterministic LLM Inference

## 参考情報

ここから下は、探索経路の良し悪しや履歴を詳しく確認するときに使う情報です。通常の稼働確認では上部だけ見れば十分です。

### 直近の探索専用worker

Run: **2026-09-13T11:00:00+09:00**

| 指標 | 値 |
|---|---:|
| 探索round | **15** |
| 探索軸 | 2026年9月新着・KV圧縮と動的管理 / MoE専門家先読み・エッジ投機実行 / 重要系譜の前方・後方引用追跡 / CPU/GPU・NPU/PIM異種実行と階層オフロード / 動的投機的復号serving・agent隣接 / agentic serving・workflow-aware KV管理 / GPU runtime・kernel自動最適化とframework統合 / recent検索から重要基礎系譜への欠落確認 / 収録済み重要論文のforward citation・Llumnix系譜 / FlashInfer-Bench・FlashInfer周辺のbackward referenceと基礎memory management / 2609新着・KVキャッシュ・階層メモリ・ストレージ / 分離サービング・電力制御・KV転送・multi-turn routing / MoE expert locality・expert prefetch・SSD/edge cacheability / CXL/SSD shared KV・tiered storage resource optimization / serving software aging・runtime reliability・lossless compression・load-aware speculative serving |
| 評価候補 | **65** |
| 重複除外 | **34** |
| Novel候補 | **31** |
| Research候補採用 | **8** |
| 重複率 | **52.3%** |

### 探索専用workerの探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| SSD expert offload・peer GPU cache tier・階層メモリ | 12 | 10 | 0 | 83.3% | 0.0% |
| NVMe重み先読み・疎推論GPUカーネル・fleet資源配置 | 8 | 3 | 4 | 37.5% | 50.0% |
| 分離型サービングの負荷偏り・SLO適応 | 7 | 4 | 1 | 57.1% | 14.3% |
| 新着LLM推論システム・通信／疎注意／多ターンKV | 7 | 4 | 3 | 57.1% | 42.9% |
| CXL/SSD shared KV・tiered storage resource optimization | 6 | 5 | 1 | 83.3% | 16.7% |
| GPU実行環境・collective通信・prefill/decode共存 | 6 | 5 | 1 | 83.3% | 16.7% |
| production-autoscaling-disaggregated-serving-runtime | 6 | 4 | 2 | 66.7% | 33.3% |
| 端末内LLM・OSメモリ圧力・Flash/NPU実行 | 6 | 2 | 3 | 33.3% | 50.0% |
| 2609新着・KVキャッシュ・階層メモリ・ストレージ | 5 | 0 | 0 | 0.0% | 0.0% |
| GPU runtime・kernel自動最適化とframework統合 | 5 | 4 | 1 | 80.0% | 20.0% |
| MoE expert locality・expert prefetch・SSD/edge cacheability | 5 | 0 | 1 | 0.0% | 20.0% |
| MoE専門家先読み・エッジ投機実行 | 5 | 4 | 1 | 80.0% | 20.0% |
| multi-tenant runtime制御・適応parallelism・latency attribution | 5 | 3 | 2 | 60.0% | 40.0% |
| serving software aging・runtime reliability・lossless compression・load-aware speculative serving | 5 | 4 | 0 | 80.0% | 0.0% |
| 分離サービング・電力制御・KV転送・multi-turn routing | 5 | 0 | 0 | 0.0% | 0.0% |
| 分離サービング通信・KV転送・network flow scheduling | 5 | 5 | 0 | 100.0% | 0.0% |
| 動的投機的復号serving・agent隣接 | 5 | 3 | 1 | 60.0% | 20.0% |
| CPU/GPU・NPU/PIM異種実行と階層オフロード | 4 | 4 | 0 | 100.0% | 0.0% |
| FlashInfer-Bench・FlashInfer周辺のbackward referenceと基礎memory management | 4 | 1 | 1 | 25.0% | 25.0% |
| KVページ圧縮・低ランク表現・GPUカーネル | 4 | 1 | 2 | 25.0% | 50.0% |
| RDMA・分離サービング・KV転送 | 4 | 4 | 0 | 100.0% | 0.0% |
| agentic serving・workflow-aware KV管理 | 4 | 4 | 0 | 100.0% | 0.0% |
| moe-cache-aware-routing-expert-skipping-fine-grained-execution | 4 | 0 | 0 | 0.0% | 0.0% |
| recent検索から重要基礎系譜への欠落確認 | 4 | 3 | 0 | 75.0% | 0.0% |
| ssd-kv-cache-heterogeneous-gpu-serving-orchestration | 4 | 0 | 0 | 0.0% | 0.0% |
| 分離サービングSLO・batch fairness・resource allocation | 4 | 2 | 1 | 50.0% | 25.0% |
| 基礎サービング重要未収録・prefill/decode分離・chunked prefill・multi-tenant LoRA | 4 | 0 | 1 | 0.0% | 25.0% |
| 投機的復号runtime・draft resource・CPU制約 | 4 | 2 | 2 | 50.0% | 50.0% |
| 投機的復号・高並列サービング・production評価 | 4 | 1 | 2 | 25.0% | 50.0% |
| 重要系譜の前方・後方引用追跡 | 4 | 2 | 2 | 50.0% | 50.0% |
| 2026-09新着・KV圧縮・跨文脈再利用 | 3 | 0 | 0 | 0.0% | 0.0% |
| 2026年9月新着・KV圧縮と動的管理 | 3 | 0 | 0 | 0.0% | 0.0% |
| エージェント型LLM・サービングruntime・生成時特化 | 3 | 1 | 2 | 33.3% | 66.7% |
| 出力長不確実性・tail-aware scheduling隣接 | 3 | 1 | 2 | 33.3% | 66.7% |
| 基礎推論runtime・PagedAttention/vLLM・SGLang/RadixAttention・SplitFuse | 3 | 0 | 0 | 0.0% | 0.0% |
| 収録済み重要論文のforward citation・Llumnix系譜 | 1 | 0 | 0 | 0.0% | 0.0% |

### 直近5探索専用worker run

- 2026-09-13T11:00:00+09:00 — 15 round: 評価 65 / 重複 34 / 採用 8 / 軸 2026年9月新着・KV圧縮と動的管理 / MoE専門家先読み・エッジ投機実行 / 重要系譜の前方・後方引用追跡 / CPU/GPU・NPU/PIM異種実行と階層オフロード / 動的投機的復号serving・agent隣接 / agentic serving・workflow-aware KV管理 / GPU runtime・kernel自動最適化とframework統合 / recent検索から重要基礎系譜への欠落確認 / 収録済み重要論文のforward citation・Llumnix系譜 / FlashInfer-Bench・FlashInfer周辺のbackward referenceと基礎memory management / 2609新着・KVキャッシュ・階層メモリ・ストレージ / 分離サービング・電力制御・KV転送・multi-turn routing / MoE expert locality・expert prefetch・SSD/edge cacheability / CXL/SSD shared KV・tiered storage resource optimization / serving software aging・runtime reliability・lossless compression・load-aware speculative serving
- 2026-09-13T10:00:00+09:00 — 8 round: 評価 48 / 重複 31 / 採用 12 / 軸 新着LLM推論システム・通信／疎注意／多ターンKV / GPU実行環境・collective通信・prefill/decode共存 / 端末内LLM・OSメモリ圧力・Flash/NPU実行 / KVページ圧縮・低ランク表現・GPUカーネル / 分離サービングSLO・batch fairness・resource allocation / 投機的復号runtime・draft resource・CPU制約 / SSD expert offload・peer GPU cache tier・階層メモリ / 分離サービング通信・KV転送・network flow scheduling
- 2026-09-13T09:00:00+09:00 — 13 round: 評価 58 / 重複 21 / 採用 16 / 軸 moe-cache-aware-routing-expert-skipping-fine-grained-execution / ssd-kv-cache-heterogeneous-gpu-serving-orchestration / production-autoscaling-disaggregated-serving-runtime / 2026-09新着・KV圧縮・跨文脈再利用 / エージェント型LLM・サービングruntime・生成時特化 / 出力長不確実性・tail-aware scheduling隣接 / 投機的復号・高並列サービング・production評価 / RDMA・分離サービング・KV転送 / multi-tenant runtime制御・適応parallelism・latency attribution / 基礎サービング重要未収録・prefill/decode分離・chunked prefill・multi-tenant LoRA / 基礎推論runtime・PagedAttention/vLLM・SGLang/RadixAttention・SplitFuse / 分離型サービングの負荷偏り・SLO適応 / NVMe重み先読み・疎推論GPUカーネル・fleet資源配置
- 2026-09-13T08:00:00+09:00 — 6 round: 評価 40 / 重複 25 / 採用 14 / 軸 hybrid-attention・MLA・位置非依存キャッシュ / position-independent KV再利用のforward/backward related-work補完 / agent workspace仮想化・NVMe階層・長時間runtime state / GPU runtime安全性・software aging・many-core CPU inference / network・collective通信・distributed inference / 直近新着・hierarchical memory・serving runtime横断再確認
- 2026-09-13T07:00:00+09:00 — 8 round: 評価 56 / 重複 44 / 採用 7 / 軸 KVページ制御・MoEメモリ分離・復元系の再探索 / 適応プリフィル・KV予約・デコード干渉スケジューリング / 新着・引用追跡・プリフィル・MoE・CXL/SSD・GPU実行基盤・ネットワーク分離の横断再走査 / 2609新着・端末メモリ管理・エッジクラウド協調推論 / MoE expert cache・Flash階層・expert-parallel耐障害性 / MoE speculative decoding・expert offloading・CPU/GPU共同実行 / 疎注意サービング・GPUメガカーネル・動的コンパイラ / multi-node MoE活性パターン配置・edge expert類似性routing

### 最近完了した論文

- `arXiv:2502.09921` — INF^2: High-Throughput Generative Inference of Large Language Models using Near-Storage Processing
- `arXiv:2512.14946` — EVICPRESS: Joint KV-Cache Compression and Eviction for Efficient LLM Serving
- `arXiv:2604.03143` — TokenDance: Scaling Multi-Agent LLM Serving via Collective KV Cache Sharing
- `arXiv:2405.04437` — vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention
- `arXiv:2605.05467` — Nitsum: Serving Tiered LLM Requests with Adaptive Tensor Parallelism
- `arXiv:2502.14617` — Serving Models, Fast and Slow: Optimizing Heterogeneous LLM Inferencing Workloads at Scale
- `arXiv:2609.00993` — AInfer-PD: Communication-Safe In-Place Prefill-Decode Multiplexing for Distributed MoE Rollouts
- `arXiv:2607.07388` — TF-Engram: A Train-Free Engram with SSD-Backed Memory for Large Language Models

### 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

### 集計上の注意

- Discoveryのworker帰属は `discovery-state.json` のworker識別子とrun_keyで判定します。run-ledgerのDiscovery/new_jobsはhelper処理が混ざり得るため、通常workerのDiscovery件数には直接使いません。
- `next-jobs.json` は優先スナップショットです。表示外にready jobが残っている場合があります。
- 探索専用workerのcandidate最大5本は1探索軸・1 submissionのtransport batch上限で、run全体の上限ではありません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
