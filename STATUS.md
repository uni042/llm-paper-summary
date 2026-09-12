# 運用ダッシュボード

> 自動生成: **2026-09-13 06:12 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **124 / 50** |
| Research ready | **124** |
| Research blocked | **0** |
| Research deferred | **3** |
| Research completed（累計） | **203** |
| Maintenance | **issues_found** |
| Consistency | **issues_found** |
| Maintenance counter | **4 / 24** |

### 注意事項

- Consistency check: **issues_found**
- 候補補充がResearch消化を大きく上回っています。ready在庫の増加を監視。

## 直近の通常worker

Run: **2026-09-13T05:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **6** |
| Audit完了 | **0** |
| Discovery完了 | **5** |
| 新規job | **13** |
| Repo収録 | **6** |
| Blocked遷移 | **0** |

## 直近の探索専用worker / 探索round

Run: **2026-09-13T05:00:25+09:00** / Round: **specialist-gpu-runtime-6**

| 指標 | 値 |
|---|---:|
| 探索軸 | GPU runtime・CUDA Graph・persistent kernel・決定論的推論 |
| 評価候補 | **4** |
| 重複除外 | **3** |
| Novel候補 | **1** |
| Research候補採用 | **1** |
| 重複率 | **75.0%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **21** |
| 探索round（stats観測） | **107** |
| 探索評価候補 | **504** |
| 重複除外 | **173** |
| 重複率 | **34.3%** |
| Novel候補 | **331** |
| Research候補採用 | **182** |
| Research完了 | **71** |
| Repo収録 | **71** |
| Audit完了 | **0** |
| Blocked遷移 | **1** |
| Fallback archive | **0** |

### 24時間ファネル

**探索評価 504 → 重複除外後 331 → Research候補採用 182 → Research完了 71 → Repo収録 71**

## 探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| adjacent-pim-hbm-gpu-runtime-chiplet | 14 | 9 | 5 | 64.3% | 35.7% |
| 2026年9月新着・HBF/Flash階層・attention実行・RAG/電力隣接serving | 10 | 5 | 5 | 50.0% | 50.0% |
| MoE専門家先読み・I/O階層・エッジ異種実行 | 10 | 5 | 1 | 50.0% | 10.0% |
| 異種/edge serving・hybrid cache schedulingの過去重要欠落 | 10 | 8 | 2 | 80.0% | 20.0% |
| DBMS由来cache policy・real-time/best-effort混在QoS scheduling | 9 | 7 | 2 | 77.8% | 22.2% |
| hpc_gpu_collective_serving | 9 | 6 | 0 | 66.7% | 0.0% |
| network-data-movement-pnm-cross-dc-memory-dynamics | 9 | 5 | 4 | 55.6% | 44.4% |
| heterogeneous-gpu-offload-parallelism-spot-serving | 8 | 5 | 2 | 62.5% | 25.0% |
| 分離型LLMサービング・KV転送／フェーズ非対称性 | 8 | 6 | 1 | 75.0% | 12.5% |
| CXL共有メモリ・KV階層・near-memory processing | 7 | 2 | 2 | 28.6% | 28.6% |
| agentic state・segment KV reuse・semantic eviction・stateful tokenization・hierarchical agent memory | 7 | 2 | 5 | 28.6% | 71.4% |
| heterogeneous cloud multi-LLM・multi-timescale autoscaling・SLO-aware scaling | 7 | 4 | 2 | 57.1% | 28.6% |
| heterogeneous-kv-sharing-cold-moe-memory-pooling-nand-compute | 7 | 3 | 0 | 42.9% | 0.0% |
| serverless production serving・cold start・multi-LoRA elasticity | 7 | 3 | 4 | 42.9% | 57.1% |
| 分離サービングprefill制御・chunked prefill scheduling | 7 | 4 | 2 | 57.1% | 28.6% |
| 投機的デコードのserving・pipeline・メモリ制約・性能モデル | 7 | 2 | 4 | 28.6% | 57.1% |
| 耐障害serving・予測型cross-layer scheduling | 7 | 5 | 2 | 71.4% | 28.6% |
| CUDA compiler・JIT/Graph runtime・decode kernel serving | 6 | 4 | 2 | 66.7% | 33.3% |
| GPU L2/HBM prefetch・heterogeneous memory・MoE tile-level communication overlap | 6 | 1 | 3 | 16.7% | 50.0% |
| GPU/SmartNIC実行系・storage KV経路・CXL疎注意・MoE cache制御 | 6 | 1 | 1 | 16.7% | 16.7% |
| KV復元・計算効率指向キャッシュ・分離サービング再均衡 | 6 | 3 | 1 | 50.0% | 16.7% |
| MoE expert cache・offload・OS tiering | 6 | 6 | 0 | 100.0% | 0.0% |
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
| agent session KV residency・near-memory scheduling | 5 | 4 | 1 | 80.0% | 20.0% |
| critical_buffer_cross_axis_moe_heterogeneous_serving | 5 | 0 | 0 | 0.0% | 0.0% |
| edge-cloud speculative serving・latency modeling・deployment configuration・mixed precision | 5 | 1 | 3 | 20.0% | 60.0% |
| heterogeneous GPU cluster・multi-agent workflow・routing/placement | 5 | 0 | 3 | 0.0% | 60.0% |
| heterogeneous KV retrieval・lossless weight compression・moderate sparse GPU kernels | 5 | 2 | 3 | 40.0% | 60.0% |
| output-length uncertainty・KV reservation・memory-constrained admission/scheduling | 5 | 0 | 1 | 0.0% | 20.0% |
| production推論エンジン・tail/SLO scheduling・hardware-software co-design | 5 | 0 | 3 | 0.0% | 60.0% |
| マルチエージェント・ワークフロー指向prefix状態スケジューリング | 5 | 4 | 1 | 80.0% | 20.0% |
| 分離サービング負荷転送・異種GPU構成選択 | 5 | 3 | 1 | 60.0% | 20.0% |
| 2609新着・KVキャッシュ最適化/サービング | 4 | 3 | 1 | 75.0% | 25.0% |
| 2609新着・分離サービング・動的ルーティング | 4 | 1 | 3 | 25.0% | 75.0% |
| CXL・SSD・remote KV cache階層メモリ | 4 | 4 | 0 | 100.0% | 0.0% |
| DistServe周辺のforward citation・backward reference補完 | 4 | 0 | 1 | 0.0% | 25.0% |
| GPU collective通信・in-network acceleration・通信runtime | 4 | 0 | 3 | 0.0% | 75.0% |
| GPU runtime・CUDA Graph・persistent kernel・決定論的推論 | 4 | 3 | 1 | 75.0% | 25.0% |
| GPU runtime境界・host-device転送律速 | 4 | 3 | 1 | 75.0% | 25.0% |
| KV cache admission/replacement・compression/eviction・復元parallelism | 4 | 0 | 3 | 0.0% | 75.0% |
| KV multi-turn管理・復元・予約不確実性 | 4 | 4 | 0 | 100.0% | 0.0% |
| LSH・hashing系KVアクセス/eviction/sharing・query expansion | 4 | 0 | 4 | 0.0% | 100.0% |
| MoE expert locality・cache/prefetch・CPU/GPU offload | 4 | 0 | 3 | 0.0% | 75.0% |
| MoE通信・runtime parallelism・online expert placement | 4 | 4 | 0 | 100.0% | 0.0% |
| NVMe外部KV・PIM runtime・page-aware decode scheduling | 4 | 0 | 0 | 0.0% | 0.0% |
| OS階層管理・専門家キャッシュ・KV先読み・SSD再利用 | 4 | 0 | 1 | 0.0% | 25.0% |
| P/D分離・KV転送・shared prefill | 4 | 1 | 2 | 25.0% | 50.0% |
| SLO-aware scheduling・KV memory hierarchy・動的メモリ回収 | 4 | 0 | 1 | 0.0% | 25.0% |
| SLO-aware scheduling・dynamic KV placement・heterogeneous serving allocation | 4 | 0 | 3 | 0.0% | 75.0% |
| agentic workload・program/session-aware serving | 4 | 1 | 3 | 25.0% | 75.0% |
| attention runtime・sparse attention階層memory・elastic decode | 4 | 0 | 2 | 0.0% | 50.0% |
| chunked prefill・prefix-aware batchingの基礎欠落 | 4 | 3 | 0 | 75.0% | 0.0% |
| cxl-near-data-kv-page-management-os-demand-paging | 4 | 0 | 2 | 0.0% | 50.0% |
| fault-tolerant distributed serving・KV recovery・GPU failure | 4 | 4 | 0 | 100.0% | 0.0% |
| multi-LoRA・推論/微調整co-serving・cross-model KV reuse | 4 | 1 | 2 | 25.0% | 50.0% |
| multi-adapter serving・推論/継続学習境界 | 4 | 0 | 3 | 0.0% | 75.0% |
| multi-agent workflow scheduling・異種LLM配置 | 4 | 2 | 2 | 50.0% | 50.0% |
| speculative decoding serving・composite multimodal serving | 4 | 0 | 3 | 0.0% | 75.0% |
| エージェントサンドボックス・OS資源管理・状態管理 | 4 | 0 | 4 | 0.0% | 100.0% |
| エージェント型サービング・KV再利用・ツール呼び出し待機 | 4 | 0 | 1 | 0.0% | 25.0% |
| エージェント推論・speculative tool execution | 4 | 2 | 2 | 50.0% | 50.0% |
| 分離LLMサービング・ネットワーク競合・prefill再配置 | 4 | 0 | 1 | 0.0% | 25.0% |
| 地理分散LLM serving・分散最適化 | 4 | 2 | 2 | 50.0% | 50.0% |
| 新着分離サービング電力制御・MoE推論効率・KVメモリ回収 | 4 | 0 | 2 | 0.0% | 50.0% |
| 最新PIM runtime・cache-aware MoE router・speculative資源共有・edge SSD expert cache | 4 | 0 | 0 | 0.0% | 0.0% |
| 異種GPU/PNM・cold MoE pool・edge KV migration | 4 | 0 | 0 | 0.0% | 0.0% |
| 直近新着・vLLM/SGLang周辺実装・関連論文 | 4 | 4 | 0 | 100.0% | 0.0% |
| 重要未収録・分散tensor管理・階層KV・長さaware scheduling・multimodal分離 | 4 | 0 | 4 | 0.0% | 100.0% |
| 2026-09新着・KVキャッシュ圧縮／再利用 | 3 | 3 | 0 | 100.0% | 0.0% |
| 2026年9月新着・KV圧縮/eviction/再利用 | 3 | 0 | 0 | 0.0% | 0.0% |
| ExaServe派生のSSD/NVMe expert I/O・expert prefetch・SLO-aware memory scheduling | 3 | 0 | 0 | 0.0% | 0.0% |
| GPU kernel/runtime・推論決定性 | 3 | 0 | 3 | 0.0% | 100.0% |
| GPU kernel生成・runtime最適化の隣接系 | 3 | 0 | 3 | 0.0% | 100.0% |
| GPU低ビットkernel/runtime・大容量メモリ型chain serving | 3 | 1 | 2 | 33.3% | 66.7% |
| KV量子化の実行時保証・同期型serving負荷分散 | 3 | 0 | 3 | 0.0% | 100.0% |
| MoE動的並列切替・融合通信・serverless専門家配置 | 3 | 0 | 1 | 0.0% | 33.3% |
| SSD/NVMe・object storage・CXL remote memoryによるKV階層化 | 3 | 0 | 1 | 0.0% | 33.3% |
| agentic/multi-agent serving・collective KV sharing | 3 | 0 | 2 | 0.0% | 66.7% |
| edge/on-device offload・multitasking memory・cloud KV streaming | 3 | 0 | 2 | 0.0% | 66.7% |
| moe-expert-prefetch-edge-external-memory | 3 | 0 | 1 | 0.0% | 33.3% |
| multimodal弾力的並列化・EPD分離・modality-aware scheduling | 3 | 0 | 3 | 0.0% | 100.0% |
| エージェント配信・Multi-LoRA・意味検索型KV管理 | 3 | 0 | 1 | 0.0% | 33.3% |
| 分散推論・collective通信・disaggregated電力/runtime | 3 | 0 | 2 | 0.0% | 66.7% |
| 分離サービングのnetwork flow・prefill迂回・専用interconnect | 3 | 0 | 1 | 0.0% | 33.3% |
| 推論runtime・serving耐障害性 | 3 | 1 | 2 | 33.3% | 66.7% |
| 推論システム横断サーベイ・KV・エッジ実行 | 3 | 0 | 2 | 0.0% | 66.7% |
| 新着・長期推論KV圧縮と削除 | 3 | 0 | 0 | 0.0% | 0.0% |
| 適応KV圧縮・エージェントprefix scheduling・演算子分離省電力serving | 3 | 0 | 0 | 0.0% | 0.0% |
| 長文SLO・SSD-backed KV・異種GPUメモリ共有 | 3 | 0 | 0 | 0.0% | 0.0% |
| composable-cxl-shared-kv-peer-gpu-memory-tier | 2 | 0 | 0 | 0.0% | 0.0% |
| multi-tenant prefix安全性・multi-agent workflow prefix scheduling | 2 | 0 | 0 | 0.0% | 0.0% |
| 動的parallelism再構成・KV state migration | 2 | 0 | 2 | 0.0% | 100.0% |
| 新着KV圧縮・時間集約・長推論再参照 | 2 | 0 | 0 | 0.0% | 0.0% |
| 複数ラウンド分離サービング・異種メモリ処理 | 2 | 0 | 2 | 0.0% | 100.0% |
| KVキャッシュ幾何学指標・backward reference | 1 | 0 | 1 | 0.0% | 100.0% |

### 直近5探索round

- **2026-09-13T06:02:25+09:00** — GPU低ビットkernel/runtime・大容量メモリ型chain serving: 評価 3 / 重複 1 / 採用 2
- **2026-09-13T06:02:25+09:00** — 適応KV圧縮・エージェントprefix scheduling・演算子分離省電力serving: 評価 3 / 重複 0 / 採用 0
- **2026-09-13T05:28:14+09:00** — LSH・hashing系KVアクセス/eviction/sharing・query expansion: 評価 4 / 重複 0 / 採用 4
- **2026-09-13T05:28:14+09:00** — KVキャッシュ幾何学指標・backward reference: 評価 1 / 重複 0 / 採用 1
- **2026-09-13T05:28:14+09:00** — 2609新着・KVキャッシュ最適化/サービング: 評価 4 / 重複 3 / 採用 1

## 最近処理した論文

### Research完了

- `arXiv:2609.02737` — Language Models Can Control Their Own Attention
- `arXiv:2604.06370` — ForkKV: Scaling Multi-LoRA Agent Serving via Copy-on-Write Disaggregated KV Cache
- `arXiv:2506.21901` — A Survey of LLM Inference Systems
- `arXiv:2606.29986` — HBM Is Not All You Need: Efficient Disaggregated LLM Serving across Memory-heterogeneous Accelerators
- `arXiv:2609.01024` — PCoMoE: Shifting MoE Inference from Monolithic Expert Selection to Fine-Grained Path Composition
- `arXiv:2605.01708` — SplitZip: Lossless KV Cache Compression for Disaggregated LLM Serving
- `arXiv:2512.09472` — WarmServe: Enabling One-for-Many GPU Prewarming for Multi-LLM Serving
- `arXiv:2601.22705` — CONCUR: High-Throughput Agentic Batch Inference of LLM via Congestion-Based Concurrency Control

### 次に処理する候補

- P90 `arXiv:2410.16179` — MagicPIG: LSH Sampling for Efficient LLM Generation
- P88 `arXiv:2603.23049` — PCR: A Prefetch-Enhanced Cache Reuse System for Low-Latency RAG Serving
- P88 `arXiv:2607.28699` — WitCert: Sound Runtime Risk Observability and Gating for KV-Cache Quantization
- P88 `arXiv:2606.23521` — Concordia: JIT-Compiled Persistent-Kernel Checkpointing for Fault-Tolerant LLM Inference
- P88 `arXiv:2512.22219` — Mirage Persistent Kernel: A Compiler and Runtime for Mega-Kernelizing Tensor Programs

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
