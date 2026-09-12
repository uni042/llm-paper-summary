# 運用ダッシュボード

> 自動生成: **2026-09-12 16:42 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **2 / 50** |
| Research ready | **2** |
| Research blocked | **3** |
| Research deferred | **3** |
| Research completed（累計） | **145** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **15 / 24** |

### 注意事項

- **CRITICAL**: candidate在庫が15未満（現在 2）。探索を最優先で継続。
- Research blocked が **3件** 残っています。
- Research消化が候補補充を上回っています。candidate枯渇に注意。

## 直近の通常worker

Run: **2026-09-12T16:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **1** |
| Audit完了 | **0** |
| Discovery完了 | **1** |
| 新規job | **3** |
| Repo収録 | **1** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T16:30:00+09:00** / Round: **paper-worker-new-arrivals-power-moe-kv-1-retry**

| 指標 | 値 |
|---|---:|
| 探索軸 | 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 |
| 評価候補 | **4** |
| 重複除外 | **0** |
| Novel候補 | **4** |
| Research候補採用 | **2** |
| 重複率 | **0.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **16** |
| 探索round（stats観測） | **2** |
| 探索評価候補 | **8** |
| 重複除外 | **1** |
| 重複率 | **12.5%** |
| Novel候補 | **7** |
| Research候補採用 | **5** |
| Research完了 | **32** |
| Repo収録 | **28** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 8 → 重複除外後 7 → Research候補採用 5 → Research完了 32 → Repo収録 28**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |

### 直近5探索round

- **2026-09-12T16:30:00+09:00** — 新着分離サービング電力制御・MoE推論効率・KVメモリ回収: 評価 4 / 重複 0 / 採用 2
- **2026-09-12T14:22:56+09:00** — 2609新着・分離サービング・動的ルーティング: 評価 4 / 重複 1 / 採用 3
- **2026-09-11T11:30:00+09:00** — 最新2609・隣接ストレージ・スケジューリング再確認: 評価 0 / 重複 0 / 採用 0
- **2026-09-11T11:30:00+09:00** — 異種GPUモデル間KV共有・NVLink階層: 評価 1 / 重複 1 / 採用 0
- **2026-09-11T11:30:00+09:00** — CUDA仮想メモリによるKV予約領域回収: 評価 1 / 重複 1 / 採用 0

## 最近処理した論文

### Research完了

- `arXiv:2609.10812` — ExaServe: Large-Scale LLM Serving on Exascale HPC Systems
- `arXiv:2609.10790` — Composable CXL Memory as a Kubernetes-Native Shared Memory for LLM Serving
- `arXiv:2609.08189` — Do Dynamic Routers Need Memory? HeRo: History-Aware Routing for Efficient LLM Inference
- `arXiv:2609.10964` — Decoupling Readiness from Release for Tail-Aware Scheduling of Agentic LLM Workflows
- `arXiv:2609.11582` — OmniKVQuant: KV Cache Quantization for Omni-LLMs
- `arXiv:2511.00807` — FREESH: Fair, Resource- and Energy-Efficient Scheduling for LLM Serving on Heterogeneous GPUs
- `arXiv:2601.12241` — Power Aware Dynamic Reallocation For Inference
- `arXiv:2609.11744` — Building py-kvcache: A Performance Characterization of External KV Caching for vLLM with NVMe SSDs

### 次に処理する候補

- P83 `arXiv:2609.09241` — Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts
- P78 `arXiv:2609.04453` — When Load-Balancing Goes Too Far: Expert Pruning in Over-Dispersed Mixture-of-Experts Models

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
