# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 07:12:14 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **3** | **5** | **2** | **3** | **4** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **3** | **17** | **0** | **17** | **0** | **0** | **21** |
| 合計 | **6** | **22** | **2** | **20** | **4** | **0** | **21** |

- 最新Discovery runの耐久探索round: **17件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-16 07:11:56 JST** [research] `arXiv:2512.20210` — Predictive-LoRA: A Proactive and Fragmentation-Aware Serverless Inference System for LLMs
  - job: `.survey/work-queue/jobs/job-research-77f3e91a5c224daf.json`
  - result: `.survey/work-queue/results/research/attempt-3956cc3669cdbe211fc51d98.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3956cc3669cdbe211fc51d98.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2512.20210-predictive-lora-serverless-inference.md`
- **09-16 07:08:30 JST** [research] `arXiv:2608.06188` — Routing LLM Inference to the Cleanest Grid in Real Time
  - job: `.survey/work-queue/jobs/job-research-705b1ab26eb807b1.json`
  - result: `.survey/work-queue/results/research/attempt-55fa2104d18bc1f9a648de40.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-55fa2104d18bc1f9a648de40.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2608.06188-carbon-aware-realtime-inference-routing.md`
- **09-16 07:05:29 JST** [research] `arXiv:2505.14468` — ServerlessLoRA: Minimizing Latency and Cost in Serverless Inference for LoRA-Based LLMs
  - job: `.survey/work-queue/jobs/job-research-d09e1c8e52097070.json`
  - result: `.survey/work-queue/results/research/attempt-d87ac0583b3b3fb6f0fcba35.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d87ac0583b3b3fb6f0fcba35.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2505.14468-serverlesslora-latency-cost-lora-serving.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-16 06:01:47 JST** job `job-6d2c370dfa5a7fe8` / 候補 **1件**
  - result: `.survey/work-queue/results/20260916T0607JST-discovery-specialist-adaptive-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0607JST-discovery-specialist-adaptive-kv-1.json`
  - 探索軸: 新着KV圧縮・制約適応ポリシー
- **09-16 03:03:04 JST** job `job-218b38f7ded363b9` / 候補 **3件**
  - result: `.survey/work-queue/results/20260916T0308JST-discovery-specialist-hw-scheduling-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0308JST-discovery-specialist-hw-scheduling-1.json`
  - 探索軸: 異種推論ハードウェア・multi-model offload・分離serving通信scheduler
- **09-16 03:08:47 JST** job `job-89615180da84d5c4` / 候補 **3件**
  - result: `.survey/work-queue/results/20260916T0348JST-discovery-specialist-moe-io-2b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0348JST-discovery-specialist-moe-io-2b.json`
  - 探索軸: MoE expert I/O scheduling・CPU/GPU協調・spatio-temporal prefetch

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-15 18:30 JST** / worker `scheduled-chat-paper-20260915T1830JST`
- immutable submission: **5件** / 検証済み成功: **2件** / 未完了・未検証: **3件**
- **成功** `arXiv:2504.07494` — Apt-Serve: Adaptive Request Scheduling on Hybrid Cache for Scalable LLM Inference Serving
  - job: `.survey/work-queue/jobs/job-research-b22f71500ae1903a.json`
  - result: `.survey/work-queue/results/research/attempt-005c2488539329fa13df896f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-005c2488539329fa13df896f.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.07494-apt-serve-hybrid-cache-adaptive-scheduling.md`
- **成功** `arXiv:2601.17768` — LLM-42: Enabling Determinism in LLM Inference with Verified Speculation
  - job: `.survey/work-queue/jobs/job-research-1fc8cd177d28f575.json`
  - result: `.survey/work-queue/results/research/attempt-2767bee85a3612f009a3c651.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2767bee85a3612f009a3c651.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2601.17768-llm42-verified-speculation-deterministic-inference.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-817bd95f2c782ad4248fa08d.json` (job `job-research-3df42686de08919b`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-a88806a6b69afa14faffe306.json` (job `job-research-229f0f103fc45c25`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-acc918e244bc8cbe6bfce5af.json` (job `job-research-3df42686de08919b`)

#### Audit (:30)

- 最新観測run: **2026-09-15 18:30 JST** / worker `scheduled-chat-paper-20260915T1830JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-16 07:00 JST**
- 耐久探索round: **17件** / immutable submission: **17件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **17件** / 候補: **21件**
- 探索軸: 新着・適応型KV圧縮・制約付き推論 / MoE expert cache・OS管理階層・prefetch / 分離サービング・ネットワークKV配布・転送 / GPU runtime・prefix-aware batching・QoS scheduling / CXL共有メモリ・Kubernetes・cross-node KV reuse / backward reference・near-data/near-storage・CXL基盤 / OS隣接・統合GPUメモリ管理・ballooning / HPC/architecture隣接・MoE near-memory・FFN disaggregation / vLLM/SGLang/TensorRT-LLM・KV runtime semantics / agentic serving・pause/resume・KV retention/prefetch / sparse attention・階層KV・PNM/SGLang / energy-aware serving・shared GPU・SLO scheduling / hardware-aware lossless compression・weight bandwidth / edge MoE・GPU-NDP・expert scheduling/prefetch / multi-tenant KV/prefix cache・security/isolation / model-parallel communication・sequence parallel serving / speculative decoding・multi-tenant serving・remote drafter
- round `specialist-adaptive-kv-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0703JST-discovery-specialist-adaptive-kv-1.json`
  - 探索軸: 新着・適応型KV圧縮・制約付き推論
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-moe-os-cache-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0706JST-discovery-specialist-moe-os-cache-2.json`
  - 探索軸: MoE expert cache・OS管理階層・prefetch
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-network-kv-3` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0709JST-discovery-specialist-network-kv-3.json`
  - 探索軸: 分離サービング・ネットワークKV配布・転送
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-runtime-batching-4` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0712JST-discovery-specialist-runtime-batching-4.json`
  - 探索軸: GPU runtime・prefix-aware batching・QoS scheduling
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cxl-k8s-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0715JST-discovery-specialist-cxl-k8s-5.json`
  - 探索軸: CXL共有メモリ・Kubernetes・cross-node KV reuse
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-storage-foundations-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0718JST-discovery-specialist-storage-foundations-6.json`
  - 探索軸: backward reference・near-data/near-storage・CXL基盤
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-elastic-memory-7` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0722JST-discovery-specialist-elastic-memory-7b.json`
  - 探索軸: OS隣接・統合GPUメモリ管理・ballooning
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-moe-nearmem-8` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0725JST-discovery-specialist-moe-nearmem-8b.json`
  - 探索軸: HPC/architecture隣接・MoE near-memory・FFN disaggregation
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-runtime-semantics-9` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0727JST-discovery-specialist-runtime-semantics-9.json`
  - 探索軸: vLLM/SGLang/TensorRT-LLM・KV runtime semantics
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-agent-kv-10` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0730JST-discovery-specialist-agent-kv-10.json`
  - 探索軸: agentic serving・pause/resume・KV retention/prefetch
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **4件** / 直近15分heartbeat: **0件**
- `arXiv:2602.21477` — Pancake: Hierarchical Memory System for Multi-Agent LLM Serving / worker `work-library-repair-20260916`
  - claim: **09-16 07:01:34 JST** / heartbeat: **—** / lease expiry: **09-16 19:01:34 JST**
  - evidence: `.survey/work-queue/claims/job-research-382442b3f5faa67f.json`
- `arXiv:2607.29069` — Rethinking AI Cloud Infrastructure for Agentic Serving Systems with the Aries Experimentation Framework / worker `work-library-repair-20260916`
  - claim: **09-16 07:01:34 JST** / heartbeat: **—** / lease expiry: **09-16 19:01:34 JST**
  - evidence: `.survey/work-queue/claims/job-research-c6ac42b8bcec8aab.json`
- `arXiv:2603.07169` — Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts / worker `work-library-repair-20260916`
  - claim: **09-16 07:01:34 JST** / heartbeat: **—** / lease expiry: **09-16 19:01:34 JST**
  - evidence: `.survey/work-queue/claims/job-research-d66acc5736f090e9.json`
- `arXiv:2609.09787` — Spatial LLM Workload Shifting Needs Foresight: Model Commitment for AI Data Center Operation under Power Grid Constraints / worker `work-library-repair-20260916`
  - claim: **09-16 07:01:34 JST** / heartbeat: **—** / lease expiry: **09-16 19:01:34 JST**
  - evidence: `.survey/work-queue/claims/job-research-ea263cc3cccbe57a.json`

#### Audit

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

#### Discovery

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

> claimやheartbeatは **GitHubへ耐久保存された処理権・活動記録** です。Scheduled Chatプロセスの生存そのものまでは証明しないため、そこは推測しません。

### このSTATUSが採用する証拠

- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。
- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。
- **Audit完了**: job/result/submissionの対応と成功状態を照合します。
- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。
- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
