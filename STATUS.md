# 運用ダッシュボード

> 自動生成: **2026-09-12 17:50 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **2 / 50** |
| Research ready | **2** |
| Research blocked | **3** |
| Research deferred | **3** |
| Research completed（累計） | **149** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **16 / 24** |

### 注意事項

- **CRITICAL**: candidate在庫が15未満（現在 2）。探索を最優先で継続。
- Research blocked が **3件** 残っています。
- Research消化が候補補充を上回っています。candidate枯渇に注意。

## 直近の通常worker

Run: **2026-09-12T17:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **2** |
| Audit完了 | **0** |
| Discovery完了 | **2** |
| 新規job | **5** |
| Repo収録 | **2** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T17:30:00+09:00** / Round: **paper-worker-moe-io-hierarchy-2**

| 指標 | 値 |
|---|---:|
| 探索軸 | MoE専門家先読み・I/O階層・エッジ異種実行 |
| 評価候補 | **10** |
| 重複除外 | **5** |
| Novel候補 | **5** |
| Research候補採用 | **1** |
| 重複率 | **50.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **16** |
| 探索round（stats観測） | **6** |
| 探索評価候補 | **29** |
| 重複除外 | **9** |
| 重複率 | **31.0%** |
| Novel候補 | **20** |
| Research候補採用 | **9** |
| Research完了 | **33** |
| Repo収録 | **32** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 29 → 重複除外後 20 → Research候補採用 9 → Research完了 33 → Repo収録 32**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| MoE専門家先読み・I/O階層・エッジ異種実行 | 10 | 5 | 1 | 50.0% | 10.0% |
| KV復元・計算効率指向キャッシュ・分離サービング再均衡 | 6 | 3 | 1 | 50.0% | 16.7% |
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |
| ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling | 3 | 0 | 0 | 0.0% | 0.0% |
| 複数ラウンド分離サービング・異種メモリ処理 | 2 | 0 | 2 | 0.0% | 100.0% |

### 直近5探索round

- **2026-09-12T17:30:00+09:00** — MoE専門家先読み・I/O階層・エッジ異種実行: 評価 10 / 重複 5 / 採用 1
- **2026-09-12T17:30:00+09:00** — KV復元・計算効率指向キャッシュ・分離サービング再均衡: 評価 6 / 重複 3 / 採用 1
- **2026-09-12T16:30:00+09:00** — 複数ラウンド分離サービング・異種メモリ処理: 評価 2 / 重複 0 / 採用 2
- **2026-09-12T16:30:00+09:00** — ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling: 評価 3 / 重複 0 / 採用 0
- **2026-09-12T16:30:00+09:00** — 新着分離サービング電力制御・MoE推論効率・KVメモリ回収: 評価 4 / 重複 0 / 採用 2

## 最近処理した論文

### Research完了

- `arXiv:2603.29002` — Understand and Accelerate Memory Processing Pipeline for Disaggregated LLM Inference
- `arXiv:2602.14516` — Efficient Multi-round LLM Inference over Disaggregated Serving
- `arXiv:2609.04453` — When Load-Balancing Goes Too Far: Expert Pruning in Over-Dispersed Mixture-of-Experts Models
- `arXiv:2609.09241` — Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts
- `arXiv:2609.10812` — ExaServe: Large-Scale LLM Serving on Exascale HPC Systems
- `arXiv:2609.10790` — Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving
- `arXiv:2609.08189` — Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference
- `arXiv:2609.10964` — Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows

### 次に処理する候補

- P88 `arXiv:2605.20179` — TIDE: Efficient and Lossless MoE Diffusion LLM Inference with I/O-aware Expert Offload
- P80 `arXiv:2510.13223` — BanaServe: Unified KV Cache and Dynamic Module Migration for Balancing Disaggregated LLM Serving in AI Infrastructure

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
