# 運用ダッシュボード

> 自動生成: **2026-09-12 18:19 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **9 / 50** |
| Research ready | **9** |
| Research blocked | **3** |
| Research deferred | **3** |
| Research completed（累計） | **152** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **16 / 24** |

### 注意事項

- **CRITICAL**: candidate在庫が15未満（現在 9）。探索を最優先で継続。
- Research blocked が **3件** 残っています。
- Research消化が候補補充を上回っています。candidate枯渇に注意。

## 直近の通常worker

Run: **2026-09-12T17:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **5** |
| Audit完了 | **0** |
| Discovery完了 | **7** |
| 新規job | **20** |
| Repo収録 | **5** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T18:00:00+09:00** / Round: **specialist-scheduling-engine-4**

| 指標 | 値 |
|---|---:|
| 探索軸 | production推論エンジン・tail/SLO scheduling・hardware-software co-design |
| 評価候補 | **5** |
| 重複除外 | **0** |
| Novel候補 | **5** |
| Research候補採用 | **3** |
| 重複率 | **0.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **16** |
| 探索round（stats観測） | **11** |
| 探索評価候補 | **57** |
| 重複除外 | **15** |
| 重複率 | **26.3%** |
| Novel候補 | **42** |
| Research候補採用 | **19** |
| Research完了 | **36** |
| Repo収録 | **35** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 57 → 重複除外後 42 → Research候補採用 19 → Research完了 36 → Repo収録 35**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| MoE専門家先読み・I/O階層・エッジ異種実行 | 10 | 5 | 1 | 50.0% | 10.0% |
| CXL共有メモリ・KV階層・near-memory processing | 7 | 2 | 2 | 28.6% | 28.6% |
| KV復元・計算効率指向キャッシュ・分離サービング再均衡 | 6 | 3 | 1 | 50.0% | 16.7% |
| 新着edge/disaggregated serving・通信/電力制御 | 6 | 0 | 4 | 0.0% | 66.7% |
| GPU runtime・SmartNIC・異種アクセラレータ・階層KV | 5 | 0 | 0 | 0.0% | 0.0% |
| production推論エンジン・tail/SLO scheduling・hardware-software co-design | 5 | 0 | 3 | 0.0% | 60.0% |
| マルチエージェント・ワークフロー指向prefix状態スケジューリング | 5 | 4 | 1 | 80.0% | 20.0% |
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |
| ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling | 3 | 0 | 0 | 0.0% | 0.0% |
| 複数ラウンド分離サービング・異種メモリ処理 | 2 | 0 | 2 | 0.0% | 100.0% |

### 直近5探索round

- **2026-09-12T18:00:00+09:00** — production推論エンジン・tail/SLO scheduling・hardware-software co-design: 評価 5 / 重複 0 / 採用 3
- **2026-09-12T18:00:00+09:00** — CXL共有メモリ・KV階層・near-memory processing: 評価 7 / 重複 2 / 採用 2
- **2026-09-12T18:00:00+09:00** — GPU runtime・SmartNIC・異種アクセラレータ・階層KV: 評価 5 / 重複 0 / 採用 0
- **2026-09-12T18:00:00+09:00** — 新着edge/disaggregated serving・通信/電力制御: 評価 6 / 重複 0 / 採用 4
- **2026-09-12T17:30:00+09:00** — マルチエージェント・ワークフロー指向prefix状態スケジューリング: 評価 5 / 重複 4 / 採用 1

## 最近処理した論文

### Research完了

- `arXiv:2606.19746` — SAC: Disaggregated KV Cache System for Sparse Attention LLMs with CXL
- `arXiv:2608.25523` — TOPAS: Workflow-Aware Prefix-State Scheduling for Multi-Agent LLM Serving
- `arXiv:2605.20179` — TIDE: Efficient and Lossless MoE Diffusion LLM Inference with I/O-aware Expert Offload
- `arXiv:2603.29002` — Understand and Accelerate Memory Processing Pipeline for Disaggregated LLM Inference
- `arXiv:2602.14516` — Efficient Multi-round LLM Inference over Disaggregated Serving
- `arXiv:2609.04453` — When Load-Balancing Goes Too Far: Expert Pruning in Over-Dispersed Mixture-of-Experts Models
- `arXiv:2609.09241` — Distribution-Consistent Inference for Dynamic Sparse Mixture-of-Experts
- `arXiv:2609.10812` — ExaServe: Large-Scale LLM Serving on Exascale HPC Systems

### 次に処理する候補

- P87 `arXiv:2606.18431` — Beyond Prediction: Tail-Aware Scheduling for LLM Inference
- P86 `arXiv:2609.09166` — X-CoSD: Communication-Efficient Cross-Vocabulary Collaborative Speculative Decoding
- P86 `arXiv:2512.18194` — TraCT: Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale
- P82 `arXiv:2609.00857` — LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism
- P80 `arXiv:2510.13223` — BanaServe: Unified KV Cache and Dynamic Module Migration for Balancing Disaggregated LLM Serving in AI Infrastructure

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
