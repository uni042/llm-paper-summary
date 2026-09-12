# 運用ダッシュボード

> 自動生成: **2026-09-13 03:08 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **90 / 50** |
| Research ready | **90** |
| Research blocked | **0** |
| Research deferred | **3** |
| Research completed（累計） | **182** |
| Maintenance | **issues_found** |
| Consistency | **issues_found** |
| Maintenance counter | **1 / 24** |

### 注意事項

- Consistency check: **issues_found**
- 候補補充がResearch消化を大きく上回っています。ready在庫の増加を監視。

## 直近の通常worker

Run: **2026-09-13T02:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **5** |
| Audit完了 | **0** |
| Discovery完了 | **5** |
| 新規job | **27** |
| Repo収録 | **5** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-13T00:00:00+09:00** / Round: **specialist-fresh-framework-saturated-8**

| 指標 | 値 |
|---|---:|
| 探索軸 | 直近新着・vLLM/SGLang周辺実装・関連論文 |
| 評価候補 | **4** |
| 重複除外 | **4** |
| Novel候補 | **0** |
| Research候補採用 | **0** |
| 重複率 | **100.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **21** |
| 探索round（stats観測） | **77** |
| 探索評価候補 | **358** |
| 重複除外 | **98** |
| 重複率 | **27.4%** |
| Novel候補 | **260** |
| Research候補採用 | **127** |
| Research完了 | **50** |
| Repo収録 | **50** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 358 → 重複除外後 260 → Research候補採用 127 → Research完了 50 → Repo収録 50**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| adjacent-pim-hbm-gpu-runtime-chiplet | 14 | 9 | 5 | 64.3% | 35.7% |
| MoE専門家先読み・I/O階層・エッジ異種実行 | 10 | 5 | 1 | 50.0% | 10.0% |
| 異種/edge serving・hybrid cache schedulingの過去重要欠落 | 10 | 8 | 2 | 80.0% | 20.0% |
| hpc_gpu_collective_serving | 9 | 6 | 0 | 66.7% | 0.0% |
| network-data-movement-pnm-cross-dc-memory-dynamics | 9 | 5 | 4 | 55.6% | 44.4% |
| heterogeneous-gpu-offload-parallelism-spot-serving | 8 | 5 | 2 | 62.5% | 25.0% |
| CXL共有メモリ・KV階層・near-memory processing | 7 | 2 | 2 | 28.6% | 28.6% |
| agentic state・segment KV reuse・semantic eviction・stateful tokenization・hierarchical agent memory | 7 | 2 | 5 | 28.6% | 71.4% |
| heterogeneous-kv-sharing-cold-moe-memory-pooling-nand-compute | 7 | 3 | 0 | 42.9% | 0.0% |
| 耐障害serving・予測型cross-layer scheduling | 7 | 5 | 2 | 71.4% | 28.6% |
| GPU/SmartNIC実行系・storage KV経路・CXL疎注意・MoE cache制御 | 6 | 1 | 1 | 16.7% | 16.7% |
| KV復元・計算効率指向キャッシュ・分離サービング再均衡 | 6 | 3 | 1 | 50.0% | 16.7% |
| MoE expert配置・CPU-GPU協調実行 | 6 | 4 | 1 | 66.7% | 16.7% |
| agentic multi-turn state・interruption・distributed prefix sharing | 6 | 2 | 1 | 33.3% | 16.7% |
| 新着edge/disaggregated serving・通信/電力制御 | 6 | 0 | 4 | 0.0% | 66.7% |
| CPU-free SmartNIC・lossless圧縮・CPU-GPU協調runtime | 5 | 0 | 1 | 0.0% | 20.0% |
| CXL/NVLink-C2C・remote memory・階層KV prefetch | 5 | 0 | 2 | 0.0% | 40.0% |
| CXL共有メモリ・ラック内KV転送・Superchip階層メモリ | 5 | 2 | 0 | 40.0% | 0.0% |
| Flash・SSD階層メモリと予測先読み | 5 | 3 | 2 | 60.0% | 40.0% |
| Foundry backward references・serverless cold-start・dynamic parallelism・MoE service elasticity | 5 | 0 | 5 | 0.0% | 100.0% |
| GPU runtime cold-start・MoE network topology・heterogeneous/geo routing | 5 | 0 | 5 | 0.0% | 100.0% |
| GPU runtime・SmartNIC・異種アクセラレータ・階層KV | 5 | 0 | 0 | 0.0% | 0.0% |
| MoE expert paging・SSD cache・runtime parallelism・prefetch | 5 | 0 | 0 | 0.0% | 0.0% |
| MoE専門家配置・先読み・協調スケジューリング | 5 | 5 | 0 | 100.0% | 0.0% |
| SLO budget・KV restoration/reconfiguration・adaptive prefill execution | 5 | 0 | 1 | 0.0% | 20.0% |
| critical_buffer_cross_axis_moe_heterogeneous_serving | 5 | 0 | 0 | 0.0% | 0.0% |
| heterogeneous GPU cluster・multi-agent workflow・routing/placement | 5 | 0 | 3 | 0.0% | 60.0% |
| output-length uncertainty・KV reservation・memory-constrained admission/scheduling | 5 | 0 | 1 | 0.0% | 20.0% |
| production推論エンジン・tail/SLO scheduling・hardware-software co-design | 5 | 0 | 3 | 0.0% | 60.0% |
| マルチエージェント・ワークフロー指向prefix状態スケジューリング | 5 | 4 | 1 | 80.0% | 20.0% |
| 分離サービング負荷転送・異種GPU構成選択 | 5 | 3 | 1 | 60.0% | 20.0% |
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| DistServe周辺のforward citation・backward reference補完 | 4 | 0 | 1 | 0.0% | 25.0% |
| GPU collective通信・in-network acceleration・通信runtime | 4 | 0 | 3 | 0.0% | 75.0% |
| GPU runtime境界・host-device転送律速 | 4 | 3 | 1 | 75.0% | 25.0% |
| KV cache admission/replacement・compression/eviction・復元parallelism | 4 | 0 | 3 | 0.0% | 75.0% |
| KV multi-turn管理・復元・予約不確実性 | 4 | 4 | 0 | 100.0% | 0.0% |
| MoE expert locality・cache/prefetch・CPU/GPU offload | 4 | 0 | 3 | 0.0% | 75.0% |
| NVMe外部KV・PIM runtime・page-aware decode scheduling | 4 | 0 | 0 | 0.0% | 0.0% |
| OS階層管理・専門家キャッシュ・KV先読み・SSD再利用 | 4 | 0 | 1 | 0.0% | 25.0% |
| P/D分離・KV転送・shared prefill | 4 | 1 | 2 | 25.0% | 50.0% |
| SLO-aware scheduling・KV memory hierarchy・動的メモリ回収 | 4 | 0 | 1 | 0.0% | 25.0% |
| SLO-aware scheduling・dynamic KV placement・heterogeneous serving allocation | 4 | 0 | 3 | 0.0% | 75.0% |
| attention runtime・sparse attention階層memory・elastic decode | 4 | 0 | 2 | 0.0% | 50.0% |
| cxl-near-data-kv-page-management-os-demand-paging | 4 | 0 | 2 | 0.0% | 50.0% |
| multi-LoRA・推論/微調整co-serving・cross-model KV reuse | 4 | 1 | 2 | 25.0% | 50.0% |
| multi-adapter serving・推論/継続学習境界 | 4 | 0 | 3 | 0.0% | 75.0% |
| multi-agent workflow scheduling・異種LLM配置 | 4 | 2 | 2 | 50.0% | 50.0% |
| speculative decoding serving・composite multimodal serving | 4 | 0 | 3 | 0.0% | 75.0% |
| エージェント型サービング・KV再利用・ツール呼び出し待機 | 4 | 0 | 1 | 0.0% | 25.0% |
| エージェント推論・speculative tool execution | 4 | 2 | 2 | 50.0% | 50.0% |
| 分離LLMサービング・ネットワーク競合・prefill再配置 | 4 | 0 | 1 | 0.0% | 25.0% |
| 地理分散LLM serving・分散最適化 | 4 | 2 | 2 | 50.0% | 50.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |
| 最新PIM runtime・cache-aware MoE router・speculative資源共有・edge SSD expert cache | 4 | 0 | 0 | 0.0% | 0.0% |
| 異種GPU/PNM・cold MoE pool・edge KV migration | 4 | 0 | 0 | 0.0% | 0.0% |
| 直近新着・vLLM/SGLang周辺実装・関連論文 | 4 | 4 | 0 | 100.0% | 0.0% |
| 重要未収録・分散tensor管理・階層KV・長さaware scheduling・multimodal分離 | 4 | 0 | 4 | 0.0% | 100.0% |
| 2026年9月新着・KV圧縮/eviction/再利用 | 3 | 0 | 0 | 0.0% | 0.0% |
| ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling | 3 | 0 | 0 | 0.0% | 0.0% |
| GPU kernel/runtime・推論決定性 | 3 | 0 | 3 | 0.0% | 100.0% |
| KV量子化の実行時保証・同期型serving負荷分散 | 3 | 0 | 3 | 0.0% | 100.0% |
| MoE動的並列切替・融合通信・serverless専門家配置 | 3 | 0 | 1 | 0.0% | 33.3% |
| SSD/NVMe・object storage・CXL remote memoryによるKV階層化 | 3 | 0 | 1 | 0.0% | 33.3% |
| agentic/multi-agent serving・collective KV sharing | 3 | 0 | 2 | 0.0% | 66.7% |
| moe-expert-prefetch-edge-external-memory | 3 | 0 | 1 | 0.0% | 33.3% |
| multimodal弾力的並列化・EPD分離・modality-aware scheduling | 3 | 0 | 3 | 0.0% | 100.0% |
| エージェント配信・Multi-LoRA・意味検索型KV管理 | 3 | 0 | 1 | 0.0% | 33.3% |
| 分散推論・collective通信・disaggregated電力/runtime | 3 | 0 | 2 | 0.0% | 66.7% |
| 分離サービングのnetwork flow・prefill迂回・専用interconnect | 3 | 0 | 1 | 0.0% | 33.3% |
| 推論runtime・serving耐障害性 | 3 | 1 | 2 | 33.3% | 66.7% |
| 長文SLO・SSD-backed KV・異種GPUメモリ共有 | 3 | 0 | 0 | 0.0% | 0.0% |
| composable-cxl-shared-kv-peer-gpu-memory-tier | 2 | 0 | 0 | 0.0% | 0.0% |
| multi-tenant prefix安全性・multi-agent workflow prefix scheduling | 2 | 0 | 0 | 0.0% | 0.0% |
| 動的parallelism再構成・KV state migration | 2 | 0 | 2 | 0.0% | 100.0% |
| 新着KV圧縮・時間集約・長推論再参照 | 2 | 0 | 0 | 0.0% | 0.0% |
| 複数ラウンド分離サービング・異種メモリ処理 | 2 | 0 | 2 | 0.0% | 100.0% |

### 直近5探索round

- **2026-09-13T02:29:24+09:00** — agentic state・segment KV reuse・semantic eviction・stateful tokenization・hierarchical agent memory: 評価 7 / 重複 2 / 採用 5
- **2026-09-13T02:29:24+09:00** — Foundry backward references・serverless cold-start・dynamic parallelism・MoE service elasticity: 評価 5 / 重複 0 / 採用 5
- **2026-09-13T02:29:24+09:00** — GPU runtime cold-start・MoE network topology・heterogeneous/geo routing: 評価 5 / 重複 0 / 採用 5
- **2026-09-13T02:29:24+09:00** — multimodal弾力的並列化・EPD分離・modality-aware scheduling: 評価 3 / 重複 0 / 採用 3
- **2026-09-13T02:29:24+09:00** — 重要未収録・分散tensor管理・階層KV・長さaware scheduling・multimodal分離: 評価 4 / 重複 0 / 採用 4

## 最近処理した論文

### Research完了

- `arXiv:2604.06664` — Foundry: Template-Based CUDA Graph Context Materialization for Fast LLM Serving Cold Start
- `arXiv:2608.07009` — HiSparse: Scaling Sparse-Attention Decoding with Hierarchical KV Cache Management
- `arXiv:2608.06007` — TensorCast: The Missing Tensor Management Layer in Large Language Model Infrastructure
- `arXiv:2606.18741` — ReMP: Low-Downtime Runtime Model-Parallelism Reconfiguration for LLM Serving
- `arXiv:2406.01566` — Helix: Distributed Serving of Large Language Models via Max-Flow on Heterogeneous GPUs
- `arXiv:2501.01005` — FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving
- `arXiv:2606.12688` — M*: A Modular, Extensible, Serving System for Multimodal Models
- `arXiv:2605.22850` — ObjectCache: Layerwise Object-Storage Retrieval for KV Cache Reuse

### 次に処理する候補

- P92 `arXiv:2509.17863` — Expert-as-a-Service: Towards Efficient, Scalable, and Robust Large-scale MoE Serving
- P91 `arXiv:2509.19729` — Gyges: Dynamic Cross-Instance Parallelism Transformation for Efficient LLM Inference
- P90 `arXiv:2602.22593` — Flying Serving: On-the-Fly Parallelism Switching for Large Language Model Serving
- P90 `arXiv:2607.08782` — Director: Prediction-Driven Online Proactive Expert Placement for Mixture-of-Experts Inference
- P90 `arXiv:2605.01708` — SplitZip: Lossless KV Cache Compression for Disaggregated LLM Serving

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
