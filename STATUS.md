# 運用ダッシュボード

> 自動生成: **2026-09-12 22:06 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **14 / 50** |
| Research ready | **14** |
| Research blocked | **0** |
| Research deferred | **3** |
| Research completed（累計） | **165** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **20 / 24** |

### 注意事項

- **CRITICAL**: candidate在庫が15未満（現在 14）。探索を最優先で継続。

## 直近の通常worker

Run: **2026-09-12T21:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **1** |
| Audit完了 | **0** |
| Discovery完了 | **4** |
| 新規job | **8** |
| Repo収録 | **1** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T20:00:00+09:00** / Round: **specialist-critical-buffer-runtime-storage-moe-1**

| 指標 | 値 |
|---|---:|
| 探索軸 | GPU/SmartNIC実行系・storage KV経路・CXL疎注意・MoE cache制御 |
| 評価候補 | **6** |
| 重複除外 | **1** |
| Novel候補 | **5** |
| Research候補採用 | **1** |
| 重複率 | **16.7%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **19** |
| 探索round（stats観測） | **20** |
| 探索評価候補 | **119** |
| 重複除外 | **44** |
| 重複率 | **37.0%** |
| Novel候補 | **75** |
| Research候補採用 | **34** |
| Research完了 | **41** |
| Repo収録 | **41** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 119 → 重複除外後 75 → Research候補採用 34 → Research完了 41 → Repo収録 41**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| adjacent-pim-hbm-gpu-runtime-chiplet | 14 | 9 | 5 | 64.3% | 35.7% |
| MoE専門家先読み・I/O階層・エッジ異種実行 | 10 | 5 | 1 | 50.0% | 10.0% |
| hpc_gpu_collective_serving | 9 | 6 | 0 | 66.7% | 0.0% |
| network-data-movement-pnm-cross-dc-memory-dynamics | 9 | 5 | 4 | 55.6% | 44.4% |
| heterogeneous-gpu-offload-parallelism-spot-serving | 8 | 5 | 2 | 62.5% | 25.0% |
| CXL共有メモリ・KV階層・near-memory processing | 7 | 2 | 2 | 28.6% | 28.6% |
| heterogeneous-kv-sharing-cold-moe-memory-pooling-nand-compute | 7 | 3 | 0 | 42.9% | 0.0% |
| GPU/SmartNIC実行系・storage KV経路・CXL疎注意・MoE cache制御 | 6 | 1 | 1 | 16.7% | 16.7% |
| KV復元・計算効率指向キャッシュ・分離サービング再均衡 | 6 | 3 | 1 | 50.0% | 16.7% |
| 新着edge/disaggregated serving・通信/電力制御 | 6 | 0 | 4 | 0.0% | 66.7% |
| GPU runtime・SmartNIC・異種アクセラレータ・階層KV | 5 | 0 | 0 | 0.0% | 0.0% |
| production推論エンジン・tail/SLO scheduling・hardware-software co-design | 5 | 0 | 3 | 0.0% | 60.0% |
| マルチエージェント・ワークフロー指向prefix状態スケジューリング | 5 | 4 | 1 | 80.0% | 20.0% |
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| cxl-near-data-kv-page-management-os-demand-paging | 4 | 0 | 2 | 0.0% | 50.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |
| ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling | 3 | 0 | 0 | 0.0% | 0.0% |
| moe-expert-prefetch-edge-external-memory | 3 | 0 | 1 | 0.0% | 33.3% |
| composable-cxl-shared-kv-peer-gpu-memory-tier | 2 | 0 | 0 | 0.0% | 0.0% |
| 複数ラウンド分離サービング・異種メモリ処理 | 2 | 0 | 2 | 0.0% | 100.0% |

### 直近5探索round

- **2026-09-12T21:30:00+09:00** — composable-cxl-shared-kv-peer-gpu-memory-tier: 評価 2 / 重複 0 / 採用 0
- **2026-09-12T21:30:00+09:00** — cxl-near-data-kv-page-management-os-demand-paging: 評価 4 / 重複 0 / 採用 2
- **2026-09-12T21:30:00+09:00** — moe-expert-prefetch-edge-external-memory: 評価 3 / 重複 0 / 採用 1
- **2026-09-12T21:30:00+09:00** — heterogeneous-kv-sharing-cold-moe-memory-pooling-nand-compute: 評価 7 / 重複 3 / 採用 0
- **2026-09-12T20:00:00+09:00** — GPU/SmartNIC実行系・storage KV経路・CXL疎注意・MoE cache制御: 評価 6 / 重複 1 / 採用 1

## 最近処理した論文

### Research完了

- `arXiv:2602.21548` — DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference
- `arXiv:2609.10970` — Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign
- `arXiv:2604.15039` — Prefill-as-a-Service: KVCache of Next-Generation Models Could Go Cross-Datacenter
- `arXiv:2607.26633` — NELSSA: A GPU-PNM Heterogeneous System for Mixed-Length LLM Serving via Length-based Request Placement
- `arXiv:2604.00368` — TENT: A Declarative Slice Spraying Engine for Performant and Resilient Data Movement in Disaggregated LLM Serving
- `arXiv:2609.11562` — Entwine: Coordinating Tiled Computation and Fine-Grained Communication across GPUs
- `arXiv:2605.02189` — PipeMax: Enhancing Offline LLM Inference on Commodity GPU Servers
- `arXiv:2606.17787` — LUMEN: Coordinated Failure Recovery for Distributed LLM Serving

### 次に処理する候補

- P82 `arXiv:2609.00857` — LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism
- P82 `arXiv:2509.08309` — Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism
- P82 `arXiv:2602.12151` — OServe: Accelerating LLM Serving via Spatial-Temporal Workload Orchestration
- P81 `arXiv:2606.15555` — Service-Induced Congestion in Memory-Constrained LLM Serving
- P80 `arXiv:2510.13223` — BanaServe: Unified KV Cache and Dynamic Module Migration for Balancing Disaggregated LLM Serving in AI Infrastructure

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
