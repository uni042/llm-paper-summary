# 運用ダッシュボード

> 自動生成: **2026-09-15 01:53 JST**。正本は `.survey/work-queue/` のdurable stateです。

## このページの見方

上から順に、**現在の詰まり具合 → workerの稼働状況 → 直近24時間の処理量 → 最新run → 次に読む論文** を確認できます。日常確認はここまでで十分です。下部の「参考情報」は探索効率や履歴を詳しく見るための欄です。

- **Research ready**: まだ全文精読が終わっていない論文候補。値が大きいほど「読む仕事」が溜まっています。
- **Claim**: workerが処理権を確保するdurable lease。有効claimはleaseが未失効という意味で、実際に生存しているworkerプロセス数とは一致しません。Claimableは今すぐ別workerが着手できる件数です。
- **Audit**: 既存の論文ページや要約の品質点検。新規論文の全文精読（Research）とは別工程です。
- **Maintenance / Consistency**: queueやstateの定期保守と、リポジトリ全体の整合性チェックです。

## 現在の状態

| 指標 | 状態 |
|---|---:|
| 未処理の論文候補（Research ready） | **54** |
| 現在処理不能（Research blocked） | **0** |
| 保留中（Research deferred） | **3** |
| GitHub反映済みResearch完了（job） | **335** |
| 耐久checkpoint済み・GitHub未反映（job） | **29** |
| 精読済みユニーク論文（推定） | **364** |
| 保守状態（Maintenance） | **passed** |
| 直近整合性チェック結果 | **passed** |
| 直近整合性チェック時刻 | **09-14 09:53 JST** |
| 保守カウンタ（通常run） | **0 / 24** |

> **精読数の数え方**: 「GitHub反映済み」はResearch jobのterminal state、「耐久checkpoint済み・GitHub未反映」はworkerがcheckpoint_refをGitHubへ記録済みだがterminal stateが未反映のjobです。「精読済みユニーク論文（推定）」は両者をcanonical IDで重複排除して数えます。

### 要注意

- 現在、集計stateから重大な警告は検出されていません。

<!-- research-throughput-status:start -->
## ワーカー稼働状況

| 指標 | 状態 |
|---|---:|
| :30 通常worker | **Research/Audit優先（高在庫）** |
| :00 補助worker | **通常worker補助（Research/Audit）** |
| 処理速度 | **OK** |
| 未処理候補（Research ready） | **54** |
| 有効claim（lease） | **2** |
| 今すぐ着手可能（Claimable） | **54** |
| 有効leaseを持つworker run | **2** |
| :30 最新worker run | **2026-09-15T01:30:00+09:00** |
| :30 最新run由来の有効claim | **1** |
| :30 旧run由来の有効claim | **0** |
| :00 最新worker run | **2026-09-15T00:00:00+09:00** |
| :00 最新run由来の有効claim | **1** |
| :00 旧run由来の有効claim | **0** |
| その他/帰属不明の有効claim | **0** |
| :30 通常worker 直近lease活動 | **09-15 01:53 JST** |
| :00 補助worker 直近lease活動 | **09-15 01:32 JST** |
| 直近24h Research完了（:30 通常worker） | **35** |
| 直近24h Research完了（:00 補助worker） | **26** |
| 直近24h Research完了（帰属不明） | **0** |
| 最新通常run | **2026-09-15T01:30:00+09:00** |
| 最新通常runのResearch完了 | **3** |
| 最古の有効claimの経過時間 | **71 min** |

run別のResearch完了は、非同期Actionsの完了時刻ではなく **durable claimの元Scheduled Chat run** へ帰属させます。新形式はworker_id内のrun時刻を使い、旧形式worker_idはclaimed_atを直前の`:30`/`:00`枠へ正規化します。

Research readyが **50本を超える間は`:00` workerも論文精読側** に回り、**50本以下になるとDiscovery優先へ戻ります**。`:30`通常workerは、readyが **25本以上** で処理可能なResearchがある間はResearch/Auditを優先します。

高在庫時の通常runは、hard stopに達しない限り **最低3件** のResearch完了を下限目標にします。3件は上限・終了条件ではありません。

Research/Auditの通常配送は **claim-fast → 予約bank → attempt固有immutable descriptor → submission-fast** です。Actionsは **claim-fast / submission-fast / background** の3レーンです。旧固定 `chat-inbox.json` は通常経路では使いません。Library fallbackは復旧時にattempt固有immutable descriptorへ変換します。

有効claimは未失効のdurable leaseであり、Scheduled Chatプロセスの生存そのものではありません。ここではrun固有worker_idを優先して、最新run由来のleaseと旧run由来の残存leaseを分離します。
<!-- research-throughput-status:end -->

## 直近24時間の処理量

| 指標 | 件数 / 率 |
|---|---:|
| Research完了 | **61** |
| Repo収録 | **103** |
| Audit完了 | **0** |
| 探索評価候補 | **0** |
| Research候補採用 | **0** |
| 重複除外 | **0** |
| 重複率 | **—** |
| :00 補助worker Discovery run（毎時枠） | **0** |
| :00 補助worker Discovery round（stats観測） | **0** |
| 通常worker run（ledger観測） | **4** |
| Fallback archive（全helper） | **10** |

### 24時間の流れ

**探索評価 0 → 重複除外後 0 → Research候補採用 0 → Research完了 61 → Repo収録 103**

## 次に処理する候補

`next-jobs.json` に見えている優先候補の先頭5件です。表示枠は処理量の上限ではありません。

- P86 `arXiv:2505.14468` — ServerlessLoRA: Minimizing Latency and Cost in Serverless Inference for LoRA-Based LLMs
- P86 `arXiv:2609.11294` — Memory Compression for High-Fanout Agent Sandboxes
- P86 `arXiv:2608.14376` — CoRun: Padding is Simple and Efficient for Deterministic LLM Inference
- P86 `arXiv:2606.06256` — RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention
- P83 `arXiv:2605.05696` — Irminsul: MLA-Native Position-Independent Caching for Agentic LLM Serving

## 参考情報

ここから下は、探索経路の良し悪しや履歴を詳しく確認するときに使う情報です。通常の稼働確認では上部だけ見れば十分です。

### 直近の:00 補助worker Discovery

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

### :00 補助workerのDiscovery効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| — | 0 | 0 | 0 | — | — |

### 直近5件の:00 補助worker Discovery run

- 2026-09-13T11:00:00+09:00 — 15 round: 評価 65 / 重複 34 / 採用 8 / 軸 2026年9月新着・KV圧縮と動的管理 / MoE専門家先読み・エッジ投機実行 / 重要系譜の前方・後方引用追跡 / CPU/GPU・NPU/PIM異種実行と階層オフロード / 動的投機的復号serving・agent隣接 / agentic serving・workflow-aware KV管理 / GPU runtime・kernel自動最適化とframework統合 / recent検索から重要基礎系譜への欠落確認 / 収録済み重要論文のforward citation・Llumnix系譜 / FlashInfer-Bench・FlashInfer周辺のbackward referenceと基礎memory management / 2609新着・KVキャッシュ・階層メモリ・ストレージ / 分離サービング・電力制御・KV転送・multi-turn routing / MoE expert locality・expert prefetch・SSD/edge cacheability / CXL/SSD shared KV・tiered storage resource optimization / serving software aging・runtime reliability・lossless compression・load-aware speculative serving
- 2026-09-13T10:00:00+09:00 — 8 round: 評価 48 / 重複 31 / 採用 12 / 軸 新着LLM推論システム・通信／疎注意／多ターンKV / GPU実行環境・collective通信・prefill/decode共存 / 端末内LLM・OSメモリ圧力・Flash/NPU実行 / KVページ圧縮・低ランク表現・GPUカーネル / 分離サービングSLO・batch fairness・resource allocation / 投機的復号runtime・draft resource・CPU制約 / SSD expert offload・peer GPU cache tier・階層メモリ / 分離サービング通信・KV転送・network flow scheduling
- 2026-09-13T09:00:00+09:00 — 13 round: 評価 58 / 重複 21 / 採用 16 / 軸 moe-cache-aware-routing-expert-skipping-fine-grained-execution / ssd-kv-cache-heterogeneous-gpu-serving-orchestration / production-autoscaling-disaggregated-serving-runtime / 2026-09新着・KV圧縮・跨文脈再利用 / エージェント型LLM・サービングruntime・生成時特化 / 出力長不確実性・tail-aware scheduling隣接 / 投機的復号・高並列サービング・production評価 / RDMA・分離サービング・KV転送 / multi-tenant runtime制御・適応parallelism・latency attribution / 基礎サービング重要未収録・prefill/decode分離・chunked prefill・multi-tenant LoRA / 基礎推論runtime・PagedAttention/vLLM・SGLang/RadixAttention・SplitFuse / 分離型サービングの負荷偏り・SLO適応 / NVMe重み先読み・疎推論GPUカーネル・fleet資源配置
- 2026-09-13T08:00:00+09:00 — 6 round: 評価 40 / 重複 25 / 採用 14 / 軸 hybrid-attention・MLA・位置非依存キャッシュ / position-independent KV再利用のforward/backward related-work補完 / agent workspace仮想化・NVMe階層・長時間runtime state / GPU runtime安全性・software aging・many-core CPU inference / network・collective通信・distributed inference / 直近新着・hierarchical memory・serving runtime横断再確認
- 2026-09-13T07:00:00+09:00 — 8 round: 評価 56 / 重複 44 / 採用 7 / 軸 KVページ制御・MoEメモリ分離・復元系の再探索 / 適応プリフィル・KV予約・デコード干渉スケジューリング / 新着・引用追跡・プリフィル・MoE・CXL/SSD・GPU実行基盤・ネットワーク分離の横断再走査 / 2609新着・端末メモリ管理・エッジクラウド協調推論 / MoE expert cache・Flash階層・expert-parallel耐障害性 / MoE speculative decoding・expert offloading・CPU/GPU共同実行 / 疎注意サービング・GPUメガカーネル・動的コンパイラ / multi-node MoE活性パターン配置・edge expert類似性routing

### 最近完了した論文

- `arXiv:2602.09345` — AgentCgroup: Understanding and Controlling OS Resources of AI Agents
- `arXiv:2502.13965` — Autellix: An Efficient Serving Engine for LLM Agents as General Programs
- `arXiv:2607.08930` — BlockServe: Block-Grained Continuous Batching for High-Throughput Diffusion LLM Serving
- `arXiv:2607.08786` — Accelerating GPU Inference of Large Language Models with Moderately Unstructured Sparse Weight Matrices
- `arXiv:2504.03775` — FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling
- `arXiv:2608.02244` — Efficiency and Cost Alignment in Batched LLM Serving via Resource-Fair Scheduling
- `arXiv:2609.02027` — Multi-Turn LLM Conversations under the Least-Recently-Used Policy: Mean-Field Asymptotics and Hit Ratio Approximation
- `arXiv:2606.23969` — The Serialized Bridge: Understanding and Recovering LLM Serving Performance under Blackwell GPU Confidential Computing

### 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

### 集計上の注意

- Discoveryのworker帰属は `discovery-state.json` のworker識別子とrun_keyで判定します。run-ledgerのDiscovery/new_jobsはhelper処理が混ざり得るため、通常workerのDiscovery件数には直接使いません。
- `next-jobs.json` は優先スナップショットです。表示外にready jobが残っている場合があります。
- 探索専用workerのcandidate最大5本は1探索軸・1 submissionのtransport batch上限で、run全体の上限ではありません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
