# 運用ダッシュボード

> 自動生成: **2026-09-12 16:07 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **1 / 50** |
| Research ready | **1** |
| Research blocked | **3** |
| Research deferred | **3** |
| Research completed（累計） | **144** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **14 / 24** |

### 注意事項

- **CRITICAL**: candidate在庫が15未満（現在 1）。探索を最優先で継続。
- Research blocked が **3件** 残っています。
- Research消化が候補補充を上回っています。candidate枯渇に注意。

## 直近の通常worker

Run: **2026-09-12T14:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **4** |
| Audit完了 | **0** |
| Discovery完了 | **1** |
| 新規job | **3** |
| Repo収録 | **4** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T14:22:56+09:00** / Round: **specialist-2609-serving-routing-1**

| 指標 | 値 |
|---|---:|
| 探索軸 | 2609新着・分離サービング・動的ルーティング |
| 評価候補 | **4** |
| 重複除外 | **1** |
| Novel候補 | **3** |
| Research候補採用 | **3** |
| 重複率 | **25.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **16** |
| 探索round（stats観測） | **1** |
| 探索評価候補 | **4** |
| 重複除外 | **1** |
| 重複率 | **25.0%** |
| Novel候補 | **3** |
| Research候補採用 | **3** |
| Research完了 | **33** |
| Repo収録 | **29** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 4 → 重複除外後 3 → Research候補採用 3 → Research完了 33 → Repo収録 29**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |

### 直近5探索round

- **2026-09-12T14:22:56+09:00** — 2609新着・分離サービング・動的ルーティング: 評価 4 / 重複 1 / 採用 3
- **2026-09-11T11:30:00+09:00** — 最新2609・隣接ストレージ・スケジューリング再確認: 評価 0 / 重複 0 / 採用 0
- **2026-09-11T11:30:00+09:00** — 異種GPUモデル間KV共有・NVLink階層: 評価 1 / 重複 1 / 採用 0
- **2026-09-11T11:30:00+09:00** — CUDA仮想メモリによるKV予約領域回収: 評価 1 / 重複 1 / 採用 0
- **2026-09-11T11:30:00+09:00** — OSページキャッシュによるMoE専門家階層管理: 評価 1 / 重複 1 / 採用 0

## 最近処理した論文

### Research完了

- `arXiv:2609.10790` — Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving
- `arXiv:2609.08189` — Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference
- `arXiv:2609.10964` — Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows
- `arXiv:2609.11582` — OmniKVQuant: KV Cache Quantization for Omni-LLMs
- `arXiv:2511.00807` — FREESH: Fair, Resource- and Energy-Efficient Scheduling for LLM Serving on Heterogeneous GPUs
- `arXiv:2601.12241` — Power Aware Dynamic Reallocation For Inference
- `arXiv:2609.11744` — Building py-kvcache: A Performance Characterization of External KV Caching for vLLM with NVMe SSDs
- `arXiv:2609.04971` — BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference

### 次に処理する候補

- P83 `arXiv:2609.10812` — ExaServe: Large-Scale LLM Serving on Exascale HPC Systems

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
