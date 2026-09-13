# 運用ダッシュボード

> 自動生成: **2026-09-13 10:57 JST**。正本は `.survey/work-queue/` のdurable stateです。

## 現在

| 指標 | 状態 |
|---|---:|
| Candidate在庫（Research ready） | **174** |
| Research ready | **174** |
| Research blocked | **0** |
| Research deferred | **3** |
| Research completed（累計） | **208** |
| Maintenance | **issues_found** |
| Consistency | **issues_found** |
| Maintenance counter | **9 / 24** |

### 注意事項

- Consistency check: **issues_found**

## 直近の通常worker

Run: **2026-09-13T10:30:00+09:00**

| 指標 | 件数 |
|---|---:|
| Research完了 | **3** |
| Audit完了 | **0** |
| 通常worker Discovery round | **0** |
| 通常worker Discovery採用 | **0** |
| Repo収録 | **3** |
| Research/Audit blocked遷移 | **0** |

> Discoveryは `discovery-state.json` のrun_keyで帰属しています。run-ledgerのDiscovery/new_jobsは探索専用workerのhelper処理が混ざり得るため、この欄では使用しません。

## 直近の探索専用worker

Run: **2026-09-13T09:00:00+09:00**

| 指標 | 値 |
|---|---:|
| 探索round | **3** |
| 探索軸 | moe-cache-aware-routing-expert-skipping-fine-grained-execution / ssd-kv-cache-heterogeneous-gpu-serving-orchestration / production-autoscaling-disaggregated-serving-runtime |
| 評価候補 | **14** |
| 重複除外 | **4** |
| Novel候補 | **10** |
| Research候補採用 | **2** |
| 重複率 | **28.6%** |

## 直近24時間

| 指標 | 件数 / 率 |
|---|---:|
| 通常worker run（ledger観測） | **23** |
| 探索専用worker run（stats観測） | **10** |
| 探索専用worker round（stats観測） | **46** |
| 探索評価候補 | **224** |
| 重複除外 | **95** |
| 重複率 | **42.4%** |
| Novel候補 | **129** |
| Research候補採用 | **67** |
| Research完了 | **72** |
| Repo収録 | **72** |
| Audit完了 | **0** |
| Fallback archive（全helper） | **3** |

### 24時間ファネル

**探索専用worker評価 224 → 重複除外後 129 → Research候補採用 67 → Research完了 72 → Repo収録 72**

## 探索専用workerの探索効率（直近24時間）

| 探索軸 | 評価 | 重複 | 採用 | 重複率 | 採用率 |
|---|---:|---:|---:|---:|---:|
| adjacent-pim-hbm-gpu-runtime-chiplet | 14 | 9 | 5 | 64.3% | 35.7% |
| 新着・引用追跡・プリフィル・MoE・CXL/SSD・GPU実行基盤・ネットワーク分離の横断再走査 | 10 | 10 | 0 | 100.0% | 0.0% |
| 分離型LLMサービング・KV転送／フェーズ非対称性 | 8 | 6 | 1 | 75.0% | 12.5% |
| CXL共有メモリ・KV階層・near-memory processing | 7 | 2 | 2 | 28.6% | 28.6% |
| 分離サービングprefill制御・chunked prefill scheduling | 7 | 4 | 2 | 57.1% | 28.6% |
| 投機的デコードのserving・pipeline・メモリ制約・性能モデル | 7 | 2 | 4 | 28.6% | 57.1% |
| GPU/SmartNIC実行系・storage KV経路・CXL疎注意・MoE cache制御 | 6 | 1 | 1 | 16.7% | 16.7% |
| MoE expert cache・offload・OS tiering | 6 | 6 | 0 | 100.0% | 0.0% |
| production-autoscaling-disaggregated-serving-runtime | 6 | 4 | 2 | 66.7% | 33.3% |
| 新着edge/disaggregated serving・通信/電力制御 | 6 | 0 | 4 | 0.0% | 66.7% |
| CXL/NVLink-C2C・remote memory・階層KV prefetch | 5 | 0 | 2 | 0.0% | 40.0% |
| Flash・SSD階層メモリと予測先読み | 5 | 3 | 2 | 60.0% | 40.0% |
| GPU runtime・SmartNIC・異種アクセラレータ・階層KV | 5 | 0 | 0 | 0.0% | 0.0% |
| KVページ制御・MoEメモリ分離・復元系の再探索 | 5 | 5 | 0 | 100.0% | 0.0% |
| MoE expert paging・SSD cache・runtime parallelism・prefetch | 5 | 0 | 0 | 0.0% | 0.0% |
| MoE専門家配置・先読み・協調スケジューリング | 5 | 5 | 0 | 100.0% | 0.0% |
| critical_buffer_cross_axis_moe_heterogeneous_serving | 5 | 0 | 0 | 0.0% | 0.0% |
| production推論エンジン・tail/SLO scheduling・hardware-software co-design | 5 | 0 | 3 | 0.0% | 60.0% |
| 分離サービング負荷転送・異種GPU構成選択 | 5 | 3 | 1 | 60.0% | 20.0% |
| CXL・SSD・remote KV cache階層メモリ | 4 | 4 | 0 | 100.0% | 0.0% |
| GPU collective通信・in-network acceleration・通信runtime | 4 | 0 | 3 | 0.0% | 75.0% |
| GPU runtime・CUDA Graph・persistent kernel・決定論的推論 | 4 | 3 | 1 | 75.0% | 25.0% |
| GPU runtime境界・host-device転送律速 | 4 | 3 | 1 | 75.0% | 25.0% |
| KV cache admission/replacement・compression/eviction・復元parallelism | 4 | 0 | 3 | 0.0% | 75.0% |
| KV multi-turn管理・復元・予約不確実性 | 4 | 4 | 0 | 100.0% | 0.0% |
| MoE expert locality・cache/prefetch・CPU/GPU offload | 4 | 0 | 3 | 0.0% | 75.0% |
| MoE通信・runtime parallelism・online expert placement | 4 | 4 | 0 | 100.0% | 0.0% |
| SLO-aware scheduling・dynamic KV placement・heterogeneous serving allocation | 4 | 0 | 3 | 0.0% | 75.0% |
| agentic workload・program/session-aware serving | 4 | 1 | 3 | 25.0% | 75.0% |
| attention runtime・sparse attention階層memory・elastic decode | 4 | 0 | 2 | 0.0% | 50.0% |
| chunked prefill・prefix-aware batchingの基礎欠落 | 4 | 3 | 0 | 75.0% | 0.0% |
| moe-cache-aware-routing-expert-skipping-fine-grained-execution | 4 | 0 | 0 | 0.0% | 0.0% |
| multi-agent workflow scheduling・異種LLM配置 | 4 | 2 | 2 | 50.0% | 50.0% |
| speculative decoding serving・composite multimodal serving | 4 | 0 | 3 | 0.0% | 75.0% |
| ssd-kv-cache-heterogeneous-gpu-serving-orchestration | 4 | 0 | 0 | 0.0% | 0.0% |
| エージェントサンドボックス・OS資源管理・状態管理 | 4 | 0 | 4 | 0.0% | 100.0% |
| エージェント型サービング・KV再利用・ツール呼び出し待機 | 4 | 0 | 1 | 0.0% | 25.0% |
| エージェント推論・speculative tool execution | 4 | 2 | 2 | 50.0% | 50.0% |
| 分離LLMサービング・ネットワーク競合・prefill再配置 | 4 | 0 | 1 | 0.0% | 25.0% |
| 直近新着・vLLM/SGLang周辺実装・関連論文 | 4 | 4 | 0 | 100.0% | 0.0% |
| 2026-09新着・KVキャッシュ圧縮／再利用 | 3 | 3 | 0 | 100.0% | 0.0% |
| GPU kernel生成・runtime最適化の隣接系 | 3 | 0 | 3 | 0.0% | 100.0% |
| SSD/NVMe・object storage・CXL remote memoryによるKV階層化 | 3 | 0 | 1 | 0.0% | 33.3% |
| 推論システム横断サーベイ・KV・エッジ実行 | 3 | 0 | 2 | 0.0% | 66.7% |
| 新着・長期推論KV圧縮と削除 | 3 | 0 | 0 | 0.0% | 0.0% |
| 適応プリフィル・KV予約・デコード干渉スケジューリング | 3 | 2 | 0 | 66.7% | 0.0% |

### 直近5探索専用worker run

- 2026-09-13T09:00:00+09:00 — 3 round: 評価 14 / 重複 4 / 採用 2 / 軸 moe-cache-aware-routing-expert-skipping-fine-grained-execution / ssd-kv-cache-heterogeneous-gpu-serving-orchestration / production-autoscaling-disaggregated-serving-runtime
- 2026-09-13T07:00:13+09:00 — 3 round: 評価 18 / 重複 17 / 採用 0 / 軸 KVページ制御・MoEメモリ分離・復元系の再探索 / 適応プリフィル・KV予約・デコード干渉スケジューリング / 新着・引用追跡・プリフィル・MoE・CXL/SSD・GPU実行基盤・ネットワーク分離の横断再走査
- 2026-09-13T05:00:25+09:00 — 6 round: 評価 28 / 重複 18 / 採用 8 / 軸 2026-09新着・KVキャッシュ圧縮／再利用 / エージェントサンドボックス・OS資源管理・状態管理 / 分離型LLMサービング・KV転送／フェーズ非対称性 / 推論システム横断サーベイ・KV・エッジ実行 / MoE expert cache・offload・OS tiering / GPU runtime・CUDA Graph・persistent kernel・決定論的推論
- 2026-09-13T04:00:16+09:00 — 8 round: 評価 36 / 重複 18 / 採用 12 / 軸 新着・長期推論KV圧縮と削除 / 分離サービングprefill制御・chunked prefill scheduling / GPU kernel生成・runtime最適化の隣接系 / agentic workload・program/session-aware serving / MoE通信・runtime parallelism・online expert placement / CXL・SSD・remote KV cache階層メモリ / chunked prefill・prefix-aware batchingの基礎欠落 / 投機的デコードのserving・pipeline・メモリ制約・性能モデル
- 2026-09-13T00:00:00+09:00 — 8 round: 評価 35 / 重複 26 / 採用 8 / 軸 Flash・SSD階層メモリと予測先読み / 分離サービング負荷転送・異種GPU構成選択 / エージェント推論・speculative tool execution / GPU runtime境界・host-device転送律速 / multi-agent workflow scheduling・異種LLM配置 / MoE専門家配置・先読み・協調スケジューリング / KV multi-turn管理・復元・予約不確実性 / 直近新着・vLLM/SGLang周辺実装・関連論文

## 最近処理した論文

### Research完了

- `arXiv:2608.22643` — NeuroPrefetcher: Storage-Aware Sparse LLM Inference via Delta Prefetching
- `arXiv:2609.00097` — Faster Than Flash: Exploiting Attention Sparsity for Efficient Long-Context Decoding
- `arXiv:2609.01821` — Scaling Inference Prefill with High-Radix Photonic Interconnects
- `arXiv:2508.19559` — Taming the Chaos: Coordinated Autoscaling for Heterogeneous and Disaggregated LLM Inference
- `arXiv:2410.16179` — MagicPIG: LSH Sampling for Efficient LLM Generation
- `arXiv:2609.02737` — Language Models Can Control Their Own Attention
- `arXiv:2604.06370` — ForkKV: Scaling Multi-LoRA Agent Serving via Copy-on-Write Disaggregated KV Cache
- `arXiv:2506.21901` — A Survey of LLM Inference Systems

### 次に処理する候補

- P90 `arXiv:2512.12990` — SliceMoE: Bit-Sliced Expert Caching under Miss-Rate Constraints for Efficient MoE Inference
- P90 `arXiv:2607.05147` — DSpark: Confidence-Scheduled Speculative Decoding with Semi-Autoregressive Generation
- P89 `arXiv:2606.06453` — Vortex: A Programmable System for Efficient Sparse Attention Serving
- P89 `arXiv:2410.15332` — EPIC: Efficient Position-Independent Context Caching for Serving Large Language Models
- P88 `arXiv:2603.23049` — PCR: A Prefetch-Enhanced Cache Reuse System for Low-Latency RAG Serving

## 7日比較

**履歴不足** — durable run ledgerがまだ7日間を覆っていないため、7日平均との比較は表示しません。

---

このページは自動生成物です。手編集せず、集計ロジックは `.survey/scripts/build_status_dashboard.py` を修正してください。
