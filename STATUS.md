# 運用ダッシュボード

> 自動生成: **2026-09-13 00:06 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **32 / 50** |
| Research ready | **32** |
| Research blocked | **0** |
| Research deferred | **3** |
| Research completed（累計） | **171** |
| Maintenance | **passed** |
| Consistency | **passed** |
| Maintenance counter | **22 / 24** |

### 注意事項

- 現在、集計stateから重大な警告は検出されていません。

## 直近の通常worker

Run: **2026-09-12T23:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **3** |
| Audit完了 | **0** |
| Discovery完了 | **0** |
| 新規job | **0** |
| Repo収録 | **3** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-12T23:00:00+09:00** / Round: **specialist-moe-runtime-ssd-11**

| 指標 | 値 |
|---|---:|
| 探索軸 | MoE expert paging・SSD cache・runtime parallelism・prefetch |
| 評価候補 | **5** |
| 重複除外 | **0** |
| Novel候補 | **5** |
| Research候補採用 | **0** |
| 重複率 | **0.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **21** |
| 探索round（stats観測） | **33** |
| 探索評価候補 | **173** |
| 重複除外 | **46** |
| 重複率 | **26.6%** |
| Novel候補 | **127** |
| Research候補採用 | **58** |
| Research完了 | **47** |
| Repo収録 | **47** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 173 → 重複除外後 127 → Research候補採用 58 → Research完了 47 → Repo収録 47**

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
| CXL/NVLink-C2C・remote memory・階層KV prefetch | 5 | 0 | 2 | 0.0% | 40.0% |
| GPU runtime・SmartNIC・異種アクセラレータ・階層KV | 5 | 0 | 0 | 0.0% | 0.0% |
| MoE expert paging・SSD cache・runtime parallelism・prefetch | 5 | 0 | 0 | 0.0% | 0.0% |
| critical_buffer_cross_axis_moe_heterogeneous_serving | 5 | 0 | 0 | 0.0% | 0.0% |
| production推論エンジン・tail/SLO scheduling・hardware-software co-design | 5 | 0 | 3 | 0.0% | 60.0% |
| マルチエージェント・ワークフロー指向prefix状態スケジューリング | 5 | 4 | 1 | 80.0% | 20.0% |
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| GPU collective通信・in-network acceleration・通信runtime | 4 | 0 | 3 | 0.0% | 75.0% |
| KV cache admission/replacement・compression/eviction・復元parallelism | 4 | 0 | 3 | 0.0% | 75.0% |
| MoE expert locality・cache/prefetch・CPU/GPU offload | 4 | 0 | 3 | 0.0% | 75.0% |
| SLO-aware scheduling・dynamic KV placement・heterogeneous serving allocation | 4 | 0 | 3 | 0.0% | 75.0% |
| attention runtime・sparse attention階層memory・elastic decode | 4 | 0 | 2 | 0.0% | 50.0% |
| cxl-near-data-kv-page-management-os-demand-paging | 4 | 0 | 2 | 0.0% | 50.0% |
| speculative decoding serving・composite multimodal serving | 4 | 0 | 3 | 0.0% | 75.0% |
| エージェント型サービング・KV再利用・ツール呼び出し待機 | 4 | 0 | 1 | 0.0% | 25.0% |
| 分離LLMサービング・ネットワーク競合・prefill再配置 | 4 | 0 | 1 | 0.0% | 25.0% |
| 地理分散LLM serving・分散最適化 | 4 | 2 | 2 | 50.0% | 50.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |
| ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling | 3 | 0 | 0 | 0.0% | 0.0% |
| SSD/NVMe・object storage・CXL remote memoryによるKV階層化 | 3 | 0 | 1 | 0.0% | 33.3% |
| moe-expert-prefetch-edge-external-memory | 3 | 0 | 1 | 0.0% | 33.3% |
| composable-cxl-shared-kv-peer-gpu-memory-tier | 2 | 0 | 0 | 0.0% | 0.0% |
| 複数ラウンド分離サービング・異種メモリ処理 | 2 | 0 | 2 | 0.0% | 100.0% |

### 直近5探索round

- **2026-09-12T23:00:00+09:00** — MoE expert paging・SSD cache・runtime parallelism・prefetch: 評価 5 / 重複 0 / 採用 0
- **2026-09-12T23:00:00+09:00** — attention runtime・sparse attention階層memory・elastic decode: 評価 4 / 重複 0 / 採用 2
- **2026-09-12T23:00:00+09:00** — speculative decoding serving・composite multimodal serving: 評価 4 / 重複 0 / 採用 3
- **2026-09-12T23:00:00+09:00** — GPU collective通信・in-network acceleration・通信runtime: 評価 4 / 重複 0 / 採用 3
- **2026-09-12T23:00:00+09:00** — SSD/NVMe・object storage・CXL remote memoryによるKV階層化: 評価 3 / 重複 0 / 採用 1

## 最近処理した論文

### Research完了

- `arXiv:2504.02263` — MegaScale-Infer: Serving Mixture-of-Experts at Scale with Disaggregated Expert Parallelism
- `arXiv:2606.12556` — ITME: Inference Tiered Memory Expansion with Disaggregated CXL-Hybrid Memories
- `arXiv:2606.29207` — KernelFlume: Elastic Core-Attention Scaling for Agentic Long-Context Decoding
- `arXiv:2602.12151` — OServe: Accelerating LLM Serving via Spatial-Temporal Workload Orchestration
- `arXiv:2509.08309` — Hetis: Serving LLMs in Heterogeneous GPU Clusters with Fine-grained and Dynamic Parallelism
- `arXiv:2609.00857` — LLM Inference on IMC-NoC Architecture with Balanced Dataflow and Fine-Grained Parallelism
- `arXiv:2602.21548` — DualPath: Breaking the Storage Bandwidth Bottleneck in Agentic LLM Inference
- `arXiv:2609.10970` — Fengshui: Demystifying Chiplet Ecosystem and Bespoke Neural Network Accelerator Codesign

### 次に処理する候補

- P89 `arXiv:2602.02204` — vLLM-Omni: Fully Disaggregated Serving for Any-to-Any Multimodal Models
- P88 `arXiv:2608.01657` — Preserving Admission Responsibility in Multi-Tenant Large Language Model Prefix Caches
- P88 `arXiv:2605.22850` — ObjectCache: Layerwise Object-Storage Retrieval for KV Cache Reuse
- P88 `arXiv:2606.12688` — M*: A Modular, Extensible, Serving System for Multimodal Models
- P88 `arXiv:2501.01005` — FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
