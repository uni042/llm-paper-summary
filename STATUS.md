# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 08:21:59 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **32** |
| 未claim Research job | **33** |
| 直近24hの検証済みResearch収録 | **15** |
| 最終検証済みResearch収録 | **09-16 07:37:12 JST（44分前）** |
| 整合性異常 | **237** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **32** |
| canonical_idなしの候補Research job | **1** |
| 非終端Research job合計 | **33** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **7** | **5** | **2** | **3** | **0** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **4** | **11** | **0** | **11** | **0** | **0** | **21** |
| 合計 | **11** | **16** | **2** | **14** | **0** | **0** | **21** |

- 最新Discovery runの耐久探索round: **11件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-16 07:37:12 JST** [research] `arXiv:2609.09787` — Spatial LLM Workload Shifting Needs Foresight: Model Commitment for AI Data Center Operation under Power Grid Constraints
  - job: `.survey/work-queue/jobs/job-research-ea263cc3cccbe57a.json`
  - result: `.survey/work-queue/results/research/attempt-bbb785cdc85c31e832c84d96.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bbb785cdc85c31e832c84d96.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.09787-model-commitment-spatial-llm-workload-shifting.md`
- **09-16 07:30:07 JST** [research] `arXiv:2607.29069` — Rethinking AI Cloud Infrastructure for Agentic Serving Systems with the Aries Experimentation Framework
  - job: `.survey/work-queue/jobs/job-research-c6ac42b8bcec8aab.json`
  - result: `.survey/work-queue/results/research/attempt-d53062f6ce8af0e476180ce0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d53062f6ce8af0e476180ce0.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2607.29069-rethinking-ai-cloud-infrastructure-for-agentic-serving-systems-with-the-aries-experimentation-framework.md`
- **09-16 07:16:18 JST** [research] `arXiv:2602.21477` — Pancake: Hierarchical Memory System for Multi-Agent LLM Serving
  - job: `.survey/work-queue/jobs/job-research-382442b3f5faa67f.json`
  - result: `.survey/work-queue/results/research/attempt-021f1dea5f61fa1de4a2409e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-021f1dea5f61fa1de4a2409e.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2602.21477-pancake-hierarchical-agentic-memory.md`
- **09-16 07:16:18 JST** [research] `arXiv:2603.07169` — Making LLMs Optimize Multi-Scenario CUDA Kernels Like Experts
  - job: `.survey/work-queue/jobs/job-research-d66acc5736f090e9.json`
  - result: `.survey/work-queue/results/research/attempt-2920381fc7a4e8f0d505a36f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2920381fc7a4e8f0d505a36f.json`
  - paper: `papers/inference/09-kernel-runtime-compilation/2026-2603.07169-cudamaster-multi-scenario-kernel-optimization.md`
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

- **09-16 07:20:40 JST** job `job-6ff919b9f51ccf92` / 候補 **1件**
  - result: `.survey/work-queue/results/20260916T0703JST-discovery-specialist-adaptive-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0703JST-discovery-specialist-adaptive-kv-1.json`
  - 探索軸: 新着・適応型KV圧縮・制約付き推論
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

- 最新観測run: **2026-09-16 08:00 JST**
- 耐久探索round: **11件** / immutable submission: **11件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **11件** / 候補: **21件**
- 探索軸: 2609最新新着・分離サービングと熱制約スケジューリング / 動的KV容量・cross-context/checkpoint KV再利用 / latent-space inference・constant-memory long-context recall / constant-memory linear attention・streaming memory評価 / MoE predictive prefetch・future-aware cache・graph-compatible offload / MoE communication-aware placement・memory-budgeted replication / prefix-affinity routing・load-aware prefill deflection / PD間KV mixed-precision transfer・GPU lossless codec / SmartNIC/RDMA CPU-free serving・object-storage KV retrieval / CXL shared-memory KV・sparse-attention fine-grained remote access / multi-die GPU persistent runtime・MoE tile-level compute/communication overlap
- round `specialist-new-arrivals-1` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0808JST-discovery-specialist-new-arrivals-1.json`
  - 探索軸: 2609最新新着・分離サービングと熱制約スケジューリング
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-kv-adaptive-2` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0813JST-discovery-specialist-kv-adaptive-2.json`
  - 探索軸: 動的KV容量・cross-context/checkpoint KV再利用
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-latent-memory-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0818JST-discovery-specialist-latent-memory-3.json`
  - 探索軸: latent-space inference・constant-memory long-context recall
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-recurrent-memory-4` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0821JST-discovery-specialist-recurrent-memory-4.json`
  - 探索軸: constant-memory linear attention・streaming memory評価
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-moe-offload-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0825JST-discovery-specialist-moe-offload-5.json`
  - 探索軸: MoE predictive prefetch・future-aware cache・graph-compatible offload
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-moe-placement-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0829JST-discovery-specialist-moe-placement-6.json`
  - 探索軸: MoE communication-aware placement・memory-budgeted replication
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-pd-routing-7` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0833JST-discovery-specialist-pd-routing-7.json`
  - 探索軸: prefix-affinity routing・load-aware prefill deflection
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-kv-transfer-8` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0836JST-discovery-specialist-kv-transfer-8.json`
  - 探索軸: PD間KV mixed-precision transfer・GPU lossless codec
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-smartnic-storage-9` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0841JST-discovery-specialist-smartnic-storage-9.json`
  - 探索軸: SmartNIC/RDMA CPU-free serving・object-storage KV retrieval
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cxl-kv-10` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0845JST-discovery-specialist-cxl-kv-10.json`
  - 探索軸: CXL shared-memory KV・sparse-attention fine-grained remote access
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

#### Audit

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

#### Discovery

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

> claimやheartbeatは **GitHubへ耐久保存された処理権・活動記録** です。Scheduled Chatプロセスの生存そのものまでは証明しないため、そこは推測しません。

## 耐久証拠の詳細集計

### 未処理Research jobの状態内訳

| status | 件数 |
|---|---:|
| ready | **33** |

### 候補の重複・識別情報欠損

非終端Research jobだけを対象にしています。source URLは `url/source_url/paper_url/primary_url/arxiv_url/pdf_url/source.url` のいずれかで確認します。

| 指標 | 件数 |
|---|---:|
| 重複canonical_idグループ | **0** |
| 重複分のResearch job | **0** |
| canonical_id欠損 | **1** |
| title欠損 | **0** |
| source URL欠損 | **0** |

### 収録済み論文実体

`papers/inference/**` と `papers/training/**` のMarkdown実体を数え、READMEとcomparison系ファイルは除外します。

| 指標 | 件数 |
|---|---:|
| inference/training配下の論文Markdown実体 | **548** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **232** |
| └ Research | **128** |
| └ Discovery | **104** |

### 整合性異常

同じ壊れた記録が複数条件に該当する場合は各検出項目へ1件ずつ計上します。したがって合計は一意job数ではなく検出項目数です。

| 検出項目 | 件数 |
|---|---:|
| completed Research/Audit jobで検証済み完了なし | **226** |
| 対応jobなしsubmission | **11** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 合計検出項目 | **237** |

### このSTATUSが採用する証拠

- **重要指標**: 候補・未claim・24h収録・最終収録・整合性異常を、jobs/submissions/results/claims/paper実体から直接再計算します。
- **収録候補**: `jobs/*.json` の非終端Research jobだけを対象にし、`canonical_id` の一意数を候補論文数として数えます。`canonical_id` 欠損jobは別件数で表示し、論文数へ推定加算しません。
- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。
- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。
- **Audit完了**: job/result/submissionの対応と成功状態を照合します。
- **論文実体数**: `papers/inference/**` と `papers/training/**` のMarkdown実体を数え、README/comparison系を除外します。
- **immutable submission未照合**: 検証済み成功に結びつかないsubmission実体を数え、処理待ちを含み得るため整合性異常とは分離します。
- **整合性異常**: completed Research/Audit jobの未検証、対応jobなしsubmission、対応jobなし成功result、対応submissionなし成功resultを直接検出します。
- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。
- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
