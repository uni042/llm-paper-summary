# 運用ダッシュボード

> 自動生成: **2026-09-12 20:29 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **13 / 50** |
| Research ready | **13** |
| Research blocked | **0** |
| Research deferred | **3** |
| Research completed（累計） | **161** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **19 / 24** |

### 注意事項

- **CRITICAL**: candidate在庫が15未満（現在 13）。探索を最優先で継続。

## 直近の通常worker

Run: **2026-09-12T19:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **6** |
| Audit完了 | **0** |
| Discovery完了 | **3** |
| 新規job | **9** |
| Repo収録 | **6** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T19:00+09:00** / Round: **specialist-20260912T1900-01**

| 指標 | 値 |
|---|---:|
| 探索軸 | adjacent-pim-hbm-gpu-runtime-chiplet |
| 評価候補 | **14** |
| 重複除外 | **9** |
| Novel候補 | **5** |
| Research候補採用 | **5** |
| 重複率 | **64.3%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **17** |
| 探索round（stats観測） | **15** |
| 探索評価候補 | **97** |
| 重複除外 | **40** |
| 重複率 | **41.2%** |
| Novel候補 | **57** |
| Research候補採用 | **30** |
| Research完了 | **37** |
| Repo収録 | **37** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 97 → 重複除外後 57 → Research候補採用 30 → Research完了 37 → Repo収録 37**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| adjacent-pim-hbm-gpu-runtime-chiplet | 14 | 9 | 5 | 64.3% | 35.7% |
| MoE専門家先読み・I/O階層・エッジ異種実行 | 10 | 5 | 1 | 50.0% | 10.0% |
| hpc_gpu_collective_serving | 9 | 6 | 0 | 66.7% | 0.0% |
| network-data-movement-pnm-cross-dc-memory-dynamics | 9 | 5 | 4 | 55.6% | 44.4% |
| heterogeneous-gpu-offload-parallelism-spot-serving | 8 | 5 | 2 | 62.5% | 25.0% |
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

- **2026-09-12T19:30:00+09:00** — network-data-movement-pnm-cross-dc-memory-dynamics: 評価 9 / 重複 5 / 採用 4
- **2026-09-12T19:30:00+09:00** — heterogeneous-gpu-offload-parallelism-spot-serving: 評価 8 / 重複 5 / 採用 2
- **2026-09-12T19:30:00+09:00** — hpc_gpu_collective_serving: 評価 9 / 重複 6 / 採用 0
- **2026-09-12T19:00+09:00** — adjacent-pim-hbm-gpu-runtime-chiplet: 評価 14 / 重複 9 / 採用 5
- **2026-09-12T18:00:00+09:00** — production推論エンジン・tail/SLO scheduling・hardware-software co-design: 評価 5 / 重複 0 / 採用 3

## 最近処理した論文

### Research完了

- `arXiv:2604.00368` — TENT: A Declarative Slice Spraying Engine for Performant and Resilient Data Movement in Disaggregated LLM Serving
- `arXiv:2609.11562` — Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs
- `arXiv:2605.02189` — PipeMax: Enhancing Offline LLM Inference on Commodity GPU Servers
- `arXiv:2606.17787` — LUMEN: Coordinated Failure Recovery for Distributed LLM Serving
- `arXiv:2606.30391` — Energy-Aware Scheduling for Serverless LLM Serving on Shared GPUs
- `arXiv:2609.11392` — PATTON: Enabling Commodity PIM for Production LLM Serving
- `arXiv:2512.18194` — TraCT: Disaggregated LLM Serving with CXL Shared Memory KV Cache at Rack-Scale
- `arXiv:2609.09166` — X-CoSD: Communication-Efficient Cross-Vocabulary Collaborative Speculative Decoding

### 次に処理する候補

- P91 `arXiv:2607.26633` — NELSSA: A GPU-PNM Heterogeneous System for Mixed-Length LLM Serving via Length-based Request Placement
- P88 `arXiv:2604.15039` — Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter
- P83 `arXiv:2609.10970` — Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign
- P82 `arXiv:2609.00857` — LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism
- P82 `arXiv:2509.08309` — Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
