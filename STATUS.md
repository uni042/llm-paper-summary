# 運用ダッシュボード

> 自動生成: **2026-09-15 14:05 JST**。正本は `.survey/work-queue/` のdurable stateです。

## このページの見方

上から順に、**現在の詰まり具合 → workerの稼働状況 → 直近24時間の処理量 → 最新run → 次に読む論文** を確認できます。日常確認はここまでで十分です。下部の「参考情報」は探索効率や履歴を詳しく見るための欄です。

- **Research ready**: まだ全文精読が終わっていない論文候補。値が大きいほど「読む仕事」が溜まっています。
- **Claim**: workerが処理権を確保するdurable lease。有効claimはleaseが未失効という意味で、実際に生存しているworkerプロセス数とは一致しません。Claimableは今すぐ別workerが着手できる件数です。
- **Audit**: 既存の論文ページや要約の品質点検。新規論文の全文精読（Research）とは別工程です。
- **Maintenance / Consistency**: queueやstateの定期保守と、リポジトリ全体の整合性チェックです。

## 現在の状態

| 指標 | 状態 |
|---|---:|
| 未処理の論文候補（Research ready） | **44** |
| 現在処理不能（Research blocked） | **0** |
| 保留中（Research deferred） | **3** |
| GitHub反映済みResearch完了（job） | **352** |
| 耐久checkpoint済み・GitHub未反映（job） | **18** |
| 精読済みユニーク論文（推定） | **370** |
| 保守状態（Maintenance） | **passed** |
| 直近整合性チェック結果 | **passed** |
| 直近整合性チェック時刻 | **09-14 09:53 JST** |
| 保守カウンタ（通常run） | **0 / 24** |

> **精読数の数え方**: 「GitHub反映済み」はResearch jobのterminal state、「耐久checkpoint済み・GitHub未反映」はworkerがcheckpoint_refをGitHubへ記録済みだがterminal stateが未反映のjobです。「精読済みユニーク論文（推定）」は両者をcanonical IDで重複排除して数えます。

### 要注意

- 候補補充がResearch消化を大きく上回っています。ready在庫の増加を監視。

<!-- research-throughput-status:start -->
## ワーカー稼働状況

| 指標 | 状態 |
|---|---:|
| :30 通常worker | **Research/Audit優先（高在庫）** |
| :00 補助worker | **Discovery優先** |
| 処理速度 | **LOW** |
| 未処理候補（Research ready） | **44** |
| 有効claim（lease） | **0** |
| 今すぐ着手可能（Claimable） | **46** |
| 有効leaseを持つworker run | **0** |
| :30 最新worker run | **2026-09-14T05:30:00+09:00** |
| :30 最新run由来の有効claim | **0** |
| :30 旧run由来の有効claim | **0** |
| :00 最新worker run | **2026-09-15T14:00:00+09:00** |
| :00 最新run由来の有効claim | **0** |
| :00 旧run由来の有効claim | **0** |
| その他/帰属不明の有効claim | **0** |
| :30 通常worker 直近lease活動 | **09-15 12:34 JST** |
| :00 補助worker 直近lease活動 | **09-15 07:49 JST** |
| 直近24h Research完了（:30 通常worker） | **0** |
| 直近24h Research完了（:00 補助worker） | **0** |
| 直近24h Research完了（帰属不明） | **0** |
| 最新通常run | **2026-09-15T12:30:00+09:00** |
| 最新通常runのResearch完了 | **1** |
| 最古の有効claimの経過時間 | **—** |

run別のResearch完了は、非同期Actionsの完了時刻ではなく **durable claimの元Scheduled Chat run** へ帰属させます。claimに明示run_keyがあれば優先し、既存worker_id内のrun時刻はclaimed_atと整合する場合だけ使います。不整合な時刻や旧形式worker_idはclaimed_atを直前の`:30`/`:00`枠へ正規化します。

Research readyが **50本を超える間は`:00` workerも論文精読側** に回り、**50本以下になるとDiscovery優先へ戻ります**。`:30`通常workerは、readyが **25本以上** で処理可能なResearchがある間はResearch/Auditを優先します。

高在庫時の通常runは、hard stopに達しない限り **最低3件** のResearch完了を下限目標にします。3件は上限・終了条件ではありません。

Research/Auditの通常配送は **claim-fast → 予約bank → attempt固有immutable descriptor → submission-fast** です。Actionsは **claim-fast / submission-fast / background** の3レーンです。旧固定 `chat-inbox.json` は通常経路では使いません。Library fallbackは復旧時にattempt固有immutable descriptorへ変換します。

- **処理速度 LOW**: ready=44 の高在庫状態で、最新通常runのResearch完了は 1 件です。DiscoveryよりResearch消化を優先します。

有効claimは未失効のdurable leaseであり、Scheduled Chatプロセスの生存そのものではありません。最新worker runはrun-ledger/discovery-stateも参照し、active leaseがない実行も表示します。claim由来のrun時刻はclaimed_atとの整合性を検証し、最新run由来のleaseと旧run由来の残存leaseを分離します。
<!-- research-throughput-status:end -->

## 直近24時間の処理量

| 指標 | 件数 / 率 |
|---|---:|
| Research完了 | **0** |
| Repo収録 | **0** |
| Audit完了 | **0** |
| 探索評価候補 | **38** |
| Research候補採用 | **8** |
| 重複除外 | **12** |
| 重複率 | **31.6%** |
| :00 補助worker Discovery run（毎時枠） | **8** |
| :00 補助worker Discovery round（stats観測） | **16** |
| 通常worker run（ledger観測） | **0** |
| Fallback archive（全helper） | **0** |

### 24時間の流れ

**探索評価 38 → 重複除外後 26 → Research候補採用 8 → Research完了 0 → Repo収録 0**

## 次に処理する候補

`next-jobs.json` に見えている優先候補の先頭5件です。表示枠は処理量の上限ではありません。

- P87 `arXiv:2601.21198` — ZipMoE: Efficient On-Device MoE Serving via Lossless Compression and Cache-Affinity Scheduling
- P86 `arXiv:2505.14468` — ServerlessLoRA: Minimizing Latency and Cost in Serverless Inference for LoRA-Based LLMs
- P86 `arXiv:2609.11294` — Memory Compression for High-Fanout Agent Sandboxes
- P86 `arXiv:2608.14376` — CoRun: Padding is Simple and Efficient for Deterministic LLM Inference
- P86 `arXiv:2606.06256` — RedKnot: Efficient Long-Context LLM Serving with Head-Aware KV Reuse and SegPagedAttention

## 参考情報

ここから下は、探索経路の良し悪しや履歴を詳しく確認するときに使う情報です。通常の稼働確認では上部だけ見れば十分です。

### 直近の:00 補助worker Discovery

Run: **2026-09-15T14:00:00+09:00**

| 指標 | 値 |
|---|---:|
| 探索round | **1** |
| 探索軸 | MoE expert cache・router adaptation・weight traffic |
| 評価候補 | **1** |
| 重複除外 | **0** |
| Novel候補 | **1** |
| Research候補採用 | **0** |
| 重複率 | **0.0%** |

### :00 補助workerのDiscovery効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| KV復元・分離serving network scheduling・MoE elastic/offload・KV survey | 5 | 0 | 0 | 0.0% | 0.0% |
| GPU・ホストメモリ間の複数経路転送と分離サービング通信 | 4 | 3 | 1 | 75.0% | 25.0% |
| cold MoE multi-model serving・weight/KV disaggregation | 4 | 3 | 0 | 75.0% | 0.0% |
| 新着KV圧縮・制約適応runtime policy | 4 | 3 | 0 | 75.0% | 0.0% |
| MoE expert cache placement・PCIe window scheduling・fine-grained expert migration | 3 | 0 | 0 | 0.0% | 0.0% |
| 動的KVメモリ回収・CUDA仮想メモリ・prefill予約領域 | 3 | 2 | 0 | 66.7% | 0.0% |
| 熱・再現性・プライバシー制約を扱うLLM推論ランタイム | 3 | 0 | 3 | 0.0% | 100.0% |
| 2026年9月新着のKVキャッシュ実行時制御とエージェントワークフロー・スケジューリング | 2 | 0 | 0 | 0.0% | 0.0% |
| MoE lossless compression/cache-affinity・expert-locality-aware decode routing | 2 | 0 | 1 | 0.0% | 50.0% |
| 異種GPU・multi-agent workflow・shared-GPU runtime scheduling | 2 | 0 | 1 | 0.0% | 50.0% |
| 要求単位の資源制約適応・KV圧縮ポリシー選択 | 2 | 1 | 0 | 50.0% | 0.0% |
| Hybrid SWAのmulti-tier KV cache・RDMA distributed cache・production scheduling | 1 | 0 | 1 | 0.0% | 100.0% |
| MoE expert cache・router adaptation・weight traffic | 1 | 0 | 0 | 0.0% | 0.0% |
| MoE expert cache所有権・OS page cache・階層メモリ | 1 | 0 | 0 | 0.0% | 0.0% |
| multi-turn KV restoration・cross-layer sharing・recompute/load pipeline | 1 | 0 | 1 | 0.0% | 100.0% |
| handoff guard before new discovery axis | 0 | 0 | 0 | — | — |

### 直近5件の:00 補助worker Discovery run

- 2026-09-15T14:00:00+09:00 — 1 round: 評価 1 / 重複 0 / 採用 0 / 軸 MoE expert cache・router adaptation・weight traffic
- 2026-09-15T12:00:00+09:00 — 2 round: 評価 4 / 重複 3 / 採用 0 / 軸 cold MoE multi-model serving・weight/KV disaggregation / handoff guard before new discovery axis
- 2026-09-15T10:00:00+09:00 — 1 round: 評価 5 / 重複 0 / 採用 0 / 軸 KV復元・分離serving network scheduling・MoE elastic/offload・KV survey
- 2026-09-15T09:00:00+09:00 — 1 round: 評価 4 / 重複 3 / 採用 0 / 軸 新着KV圧縮・制約適応runtime policy
- 2026-09-15T08:00:00+09:00 — 5 round: 評価 10 / 重複 2 / 採用 3 / 軸 動的KVメモリ回収・CUDA仮想メモリ・prefill予約領域 / multi-turn KV restoration・cross-layer sharing・recompute/load pipeline / MoE expert cache placement・PCIe window scheduling・fine-grained expert migration / MoE lossless compression/cache-affinity・expert-locality-aware decode routing / Hybrid SWAのmulti-tier KV cache・RDMA distributed cache・production scheduling

### 最近完了した論文

- 直近24hの完了記録なし

### 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

### 集計上の注意

- Discoveryのworker帰属は `discovery-state.json` のworker識別子とrun_keyで判定します。run-ledgerのDiscovery/new_jobsはhelper処理が混ざり得るため、通常workerのDiscovery件数には直接使いません。
- `next-jobs.json` は優先スナップショットです。表示外にready jobが残っている場合があります。
- 探索専用workerのcandidate最大5本は1探索軸・1 submissionのtransport batch上限で、run全体の上限ではありません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
