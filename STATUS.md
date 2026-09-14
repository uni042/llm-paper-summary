# 運用ダッシュボード

> 自動生成: **2026-09-15 08:10 JST**。正本は `.survey/work-queue/` のdurable stateです。

## このページの見方

上から順に、**現在の詰まり具合 → workerの稼働状況 → 直近24時間の処理量 → 最新run → 次に読む論文** を確認できます。日常確認はここまでで十分です。下部の「参考情報」は探索効率や履歴を詳しく見るための欄です。

- **Research ready**: まだ全文精読が終わっていない論文候補。値が大きいほど「読む仕事」が溜まっています。
- **Claim**: workerが処理権を確保するdurable lease。有効claimはleaseが未失効という意味で、実際に生存しているworkerプロセス数とは一致しません。Claimableは今すぐ別workerが着手できる件数です。
- **Audit**: 既存の論文ページや要約の品質点検。新規論文の全文精読（Research）とは別工程です。
- **Maintenance / Consistency**: queueやstateの定期保守と、リポジトリ全体の整合性チェックです。

## 現在の状態

| 指標 | 状態 |
|---|---:|
| 未処理の論文候補（Research ready） | **42** |
| 現在処理不能（Research blocked） | **0** |
| 保留中（Research deferred） | **3** |
| GitHub反映済みResearch完了（job） | **351** |
| 耐久checkpoint済み・GitHub未反映（job） | **18** |
| 精読済みユニーク論文（推定） | **369** |
| 保守状態（Maintenance） | **passed** |
| 直近整合性チェック結果 | **passed** |
| 直近整合性チェック時刻 | **09-14 09:53 JST** |
| 保守カウンタ（通常run） | **0 / 24** |

> **精読数の数え方**: 「GitHub反映済み」はResearch jobのterminal state、「耐久checkpoint済み・GitHub未反映」はworkerがcheckpoint_refをGitHubへ記録済みだがterminal stateが未反映のjobです。「精読済みユニーク論文（推定）」は両者をcanonical IDで重複排除して数えます。

### 要注意

- Research消化が:00 補助workerのDiscovery候補補充を上回っています。candidate枯渇に注意。

<!-- research-throughput-status:start -->
## ワーカー稼働状況

| 指標 | 状態 |
|---|---:|
| :30 通常worker | **Research/Audit優先（高在庫）** |
| :00 補助worker | **Discovery優先** |
| 処理速度 | **OK** |
| 未処理候補（Research ready） | **42** |
| 有効claim（lease） | **0** |
| 今すぐ着手可能（Claimable） | **44** |
| 有効leaseを持つworker run | **0** |
| :30 最新worker run | **—** |
| :30 最新run由来の有効claim | **0** |
| :30 旧run由来の有効claim | **0** |
| :00 最新worker run | **—** |
| :00 最新run由来の有効claim | **0** |
| :00 旧run由来の有効claim | **0** |
| その他/帰属不明の有効claim | **0** |
| :30 通常worker 直近lease活動 | **09-15 06:49 JST** |
| :00 補助worker 直近lease活動 | **09-15 07:49 JST** |
| 直近24h Research完了（:30 通常worker） | **49** |
| 直近24h Research完了（:00 補助worker） | **27** |
| 直近24h Research完了（帰属不明） | **0** |
| 最新通常run | **2026-09-15T06:30:00+09:00** |
| 最新通常runのResearch完了 | **3** |
| 最古の有効claimの経過時間 | **—** |

run別のResearch完了は、非同期Actionsの完了時刻ではなく **durable claimの元Scheduled Chat run** へ帰属させます。新形式はworker_id内のrun時刻を使い、旧形式worker_idはclaimed_atを直前の`:30`/`:00`枠へ正規化します。

Research readyが **50本を超える間は`:00` workerも論文精読側** に回り、**50本以下になるとDiscovery優先へ戻ります**。`:30`通常workerは、readyが **25本以上** で処理可能なResearchがある間はResearch/Auditを優先します。

高在庫時の通常runは、hard stopに達しない限り **最低3件** のResearch完了を下限目標にします。3件は上限・終了条件ではありません。

Research/Auditの通常配送は **claim-fast → 予約bank → attempt固有immutable descriptor → submission-fast** です。Actionsは **claim-fast / submission-fast / background** の3レーンです。旧固定 `chat-inbox.json` は通常経路では使いません。Library fallbackは復旧時にattempt固有immutable descriptorへ変換します。

有効claimは未失効のdurable leaseであり、Scheduled Chatプロセスの生存そのものではありません。ここではrun固有worker_idを優先して、最新run由来のleaseと旧run由来の残存leaseを分離します。
<!-- research-throughput-status:end -->

## 直近24時間の処理量

| 指標 | 件数 / 率 |
|---|---:|
| Research完了 | **76** |
| Repo収録 | **79** |
| Audit完了 | **0** |
| 探索評価候補 | **17** |
| Research候補採用 | **5** |
| 重複除外 | **6** |
| 重複率 | **35.3%** |
| :00 補助worker Discovery run（毎時枠） | **4** |
| :00 補助worker Discovery round（stats観測） | **7** |
| 通常worker run（ledger観測） | **1** |
| Fallback archive（全helper） | **32** |

### 24時間の流れ

**探索評価 17 → 重複除外後 11 → Research候補採用 5 → Research完了 76 → Repo収録 79**

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

Run: **2026-09-15T08:00:00+09:00**

| 指標 | 値 |
|---|---:|
| 探索round | **1** |
| 探索軸 | 動的KVメモリ回収・CUDA仮想メモリ・prefill予約領域 |
| 評価候補 | **3** |
| 重複除外 | **2** |
| Novel候補 | **1** |
| Research候補採用 | **0** |
| 重複率 | **66.7%** |

### :00 補助workerのDiscovery効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| GPU・ホストメモリ間の複数経路転送と分離サービング通信 | 4 | 3 | 1 | 75.0% | 25.0% |
| 動的KVメモリ回収・CUDA仮想メモリ・prefill予約領域 | 3 | 2 | 0 | 66.7% | 0.0% |
| 熱・再現性・プライバシー制約を扱うLLM推論ランタイム | 3 | 0 | 3 | 0.0% | 100.0% |
| 2026年9月新着のKVキャッシュ実行時制御とエージェントワークフロー・スケジューリング | 2 | 0 | 0 | 0.0% | 0.0% |
| 異種GPU・multi-agent workflow・shared-GPU runtime scheduling | 2 | 0 | 1 | 0.0% | 50.0% |
| 要求単位の資源制約適応・KV圧縮ポリシー選択 | 2 | 1 | 0 | 50.0% | 0.0% |
| MoE expert cache所有権・OS page cache・階層メモリ | 1 | 0 | 0 | 0.0% | 0.0% |

### 直近5件の:00 補助worker Discovery run

- 2026-09-15T08:00:00+09:00 — 1 round: 評価 3 / 重複 2 / 採用 0 / 軸 動的KVメモリ回収・CUDA仮想メモリ・prefill予約領域
- 2026-09-15T07:00:00+09:00 — 3 round: 評価 9 / 重複 3 / 採用 4 / 軸 2026年9月新着のKVキャッシュ実行時制御とエージェントワークフロー・スケジューリング / 熱・再現性・プライバシー制約を扱うLLM推論ランタイム / GPU・ホストメモリ間の複数経路転送と分離サービング通信
- 2026-09-15T03:00:00+09:00 — 1 round: 評価 1 / 重複 0 / 採用 0 / 軸 MoE expert cache所有権・OS page cache・階層メモリ
- 2026-09-15T02:00:00+09:00 — 2 round: 評価 4 / 重複 1 / 採用 1 / 軸 要求単位の資源制約適応・KV圧縮ポリシー選択 / 異種GPU・multi-agent workflow・shared-GPU runtime scheduling
- 2026-09-13T11:00:00+09:00 — 15 round: 評価 65 / 重複 34 / 採用 8 / 軸 2026年9月新着・KV圧縮と動的管理 / MoE専門家先読み・エッジ投機実行 / 重要系譜の前方・後方引用追跡 / CPU/GPU・NPU/PIM異種実行と階層オフロード / 動的投機的復号serving・agent隣接 / agentic serving・workflow-aware KV管理 / GPU runtime・kernel自動最適化とframework統合 / recent検索から重要基礎系譜への欠落確認 / 収録済み重要論文のforward citation・Llumnix系譜 / FlashInfer-Bench・FlashInfer周辺のbackward referenceと基礎memory management / 2609新着・KVキャッシュ・階層メモリ・ストレージ / 分離サービング・電力制御・KV転送・multi-turn routing / MoE expert locality・expert prefetch・SSD/edge cacheability / CXL/SSD shared KV・tiered storage resource optimization / serving software aging・runtime reliability・lossless compression・load-aware speculative serving

### 最近完了した論文

- `arXiv:2609.12449` — HeatCache: Thermal-aware Energy-efficient LLM Inference Scheduling for Chassis-level Liquid Cooling in Sustainable Edge Server Rooms
- `arXiv:2604.22906` — Network Edge Inference for Large Language Models: Principles, Techniques, and Opportunities
- `arXiv:2605.31464` — GPU Forecasters: Language Models as Selective Surrogates for Kernel Runtime Optimization
- `arXiv:2601.17855` — A Universal Load Balancing Principle and Its Application to Large Language Model Serving
- `arXiv:2504.15364` — KeyDiff: Key Similarity-Based KV Cache Eviction for Long-Context LLM Inference in Resource-Constrained Environments
- `arXiv:2411.07447` — Saving GPU Hours in LLM Inference System Development and Online Workloads with Simulation and DBMS-Inspired Cache Replacement Policies
- `arXiv:2507.21276` — LeMix: Unified Scheduling for LLM Training and Inference on Multi-GPU Systems
- `arXiv:2606.11916` — Characterizing Software Aging in GPU-Based LLM Serving Systems

### 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

### 集計上の注意

- Discoveryのworker帰属は `discovery-state.json` のworker識別子とrun_keyで判定します。run-ledgerのDiscovery/new_jobsはhelper処理が混ざり得るため、通常workerのDiscovery件数には直接使いません。
- `next-jobs.json` は優先スナップショットです。表示外にready jobが残っている場合があります。
- 探索専用workerのcandidate最大5本は1探索軸・1 submissionのtransport batch上限で、run全体の上限ではありません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
