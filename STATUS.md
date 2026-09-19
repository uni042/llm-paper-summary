# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 23:40:24 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **50** |
| 未claim Research job | **49** |
| 直近24hの検証済みResearch収録 | **49** |
| 最終検証済みResearch収録 | **09-19 23:39:47 JST（37秒前）** |
| 整合性異常 | **4** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **50** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **50** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **16** | **2** | **2** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **72** | **11** | **11** | **0** | **0** | **0** | **33** |
| 合計 | **88** | **13** | **13** | **0** | **1** | **0** | **33** |

- 最新Discovery runの耐久探索round: **11件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-19 23:39:47 JST** [research] `arXiv:2605.20706` — Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU
  - job: `.survey/work-queue/jobs/job-research-3899c287a2c2de7d.json`
  - result: `.survey/work-queue/results/research/attempt-208eafaf198f5f787bed68e4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-208eafaf198f5f787bed68e4.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.20706-llamaweb.md`
- **09-19 23:36:01 JST** [research] `arXiv:2606.00866` — Idleness is Relative: Exploiting Tool-Call Idle Windows for Offloading in Agentic Systems with MORI
  - job: `.survey/work-queue/jobs/job-research-ca62fa2224d4eac8.json`
  - result: `.survey/work-queue/results/research/attempt-056e88f904b8cb0a268543b1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-056e88f904b8cb0a268543b1.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.00866-mori.md`
- **09-19 22:37:55 JST** [research] `arXiv:2507.07400` — KVFlow: Efficient Prefix Caching for Accelerating LLM-Based Multi-Agent Workflows
  - job: `.survey/work-queue/jobs/job-research-2dcd265cd3f3852c.json`
  - result: `.survey/work-queue/results/research/attempt-3aa111fe2ce9b9bc130ae594.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3aa111fe2ce9b9bc130ae594.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2507.07400-kvflow.md`
- **09-19 22:36:16 JST** [research] `arXiv:2609.18675` — HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution
  - job: `.survey/work-queue/jobs/job-research-a6905e04777fde1f.json`
  - result: `.survey/work-queue/results/research/attempt-22ad7565c9d243223bc06f67.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-22ad7565c9d243223bc06f67.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.18675-hbflex.md`
- **09-19 21:52:39 JST** [research] `arXiv:2609.15021` — Shared KV Caching for Replicated 27B Inference: Correctness Failures and Performance Boundaries
  - job: `.survey/work-queue/jobs/job-research-0bb313ba6c58f22b.json`
  - result: `.survey/work-queue/results/research/attempt-e7ba10673d975ae5c16659a8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e7ba10673d975ae5c16659a8.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.15021-shared-kv-caching-replicated-27b-inference.md`
- **09-19 21:48:34 JST** [research] `arXiv:2509.04576` — Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-883cceac74650e2e.json`
  - result: `.survey/work-queue/results/research/attempt-86ffe82b1cb0e347b528f5b0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-86ffe82b1cb0e347b528f5b0.json`
  - paper: `papers/inference/08-speculative-decoding/2025-2509.04576-communication-efficient-distributed-speculative-decoding.md`
- **09-19 21:44:18 JST** [research] `arXiv:2506.10443` — MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices
  - job: `.survey/work-queue/jobs/job-research-3ae1410a48dc456e.json`
  - result: `.survey/work-queue/results/research/attempt-83b90f0b9afa469d0eb73d37.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-83b90f0b9afa469d0eb73d37.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2506.10443-mnn-llm-mobile-inference-engine.md`
- **09-19 21:42:22 JST** [research] `DOI:10.1145/3797905.3807846` — CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool
  - job: `.survey/work-queue/jobs/job-research-8f1455c9a8468d9c.json`
  - result: `.survey/work-queue/results/research/attempt-9c6ab898d827d5aa2ca07235.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9c6ab898d827d5aa2ca07235.json`
  - paper: `papers/inference/99-other-inference-systems/2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md`
- **09-19 21:36:08 JST** [research] `arXiv:2607.02942` — Serving Agentic Workflows with a Physical-Plan Compiler and Adaptive Runtime
  - job: `.survey/work-queue/jobs/job-research-bf442cee1726bee0.json`
  - result: `.survey/work-queue/results/research/attempt-df7f245a6a689a36570a6d97.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-df7f245a6a689a36570a6d97.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2607.02942-dyserve-agentic-physical-plan-runtime.md`
- **09-19 19:34:56 JST** [research] `arXiv:2604.15186` — Scepsy: Serving Agentic Workflows Using Aggregate LLM Pipelines
  - job: `.survey/work-queue/jobs/job-research-188f6649e816eaae.json`
  - result: `.survey/work-queue/results/research/attempt-cd9ea16c565464e02e01a24b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cd9ea16c565464e02e01a24b.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2604.15186-scepsy-serving-agentic-workflows-using-aggregate-llm-pipelines.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-19 23:03:39 JST** job `job-d59af8c4d81ce8af` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2302JST-discovery-specialist-memory-runtime-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2302JST-discovery-specialist-memory-runtime-1.json`
  - 探索軸: HBM-host同時アクセス・CPU-free serving・portable local runtime
- **09-19 23:06:25 JST** job `job-e758ff8e3f4dd769` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2308JST-discovery-specialist-cxl-network-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2308JST-discovery-specialist-cxl-network-2.json`
  - 探索軸: CXL共有KV・sparse attention remote memory・SmartNIC prefix caching
- **09-19 23:06:36 JST** job `job-a761d3272ec6911d` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2313JST-discovery-specialist-moe-offload-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2313JST-discovery-specialist-moe-offload-3.json`
  - 探索軸: MoE expert prefetch・CPU/GPU offload・edge bandwidth adaptation
- **09-19 23:06:46 JST** job `job-4856cfe497ee1453` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2318JST-discovery-specialist-disagg-routing-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2318JST-discovery-specialist-disagg-routing-4.json`
  - 探索軸: PD分離routing・selective KV transfer・multi-turn append-prefill
- **09-19 23:06:56 JST** job `job-06aebe5281e357a6` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2324JST-discovery-specialist-serving-runtime-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2324JST-discovery-specialist-serving-runtime-5.json`
  - 探索軸: speculative serving・elastic attention/KV scaling・diffusion LLM continuous batching
- **09-19 23:07:07 JST** job `job-87f6dac53c74d4cb` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2330JST-discovery-specialist-agent-state-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2330JST-discovery-specialist-agent-state-6.json`
  - 探索軸: agentic KV eviction・tool-call idle offload・workflow-aware caching
- **09-19 23:07:17 JST** job `job-01dfcd35aeac7c9c` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2335JST-discovery-specialist-energy-runtime-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2335JST-discovery-specialist-energy-runtime-7.json`
  - 探索軸: power-aware serving・on-device thermal control・multi-GPU energy modeling
- **09-19 23:07:28 JST** job `job-2073620d5b2512ac` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2340JST-discovery-specialist-memory-hierarchy-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2340JST-discovery-specialist-memory-hierarchy-8.json`
  - 探索軸: hierarchical KV・CPU LLC residency・peer GPU cache tier
- **09-19 23:07:38 JST** job `job-ff73db34d8d3d7d7` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2346JST-discovery-specialist-new-arrivals-9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2346JST-discovery-specialist-new-arrivals-9.json`
  - 探索軸: 2609新着・cross-DC PD・near-data MoE・offloaded KV sparse scan
- **09-19 23:07:48 JST** job `job-1e366e4f2366bf04` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2351JST-discovery-specialist-storage-compute-10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2351JST-discovery-specialist-storage-compute-10.json`
  - 探索軸: NVMe delta prefetch・3D NAND compute・near-storage attention

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 23:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **2件** / 検証済み成功: **2件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- **成功** `arXiv:2606.00866` — Idleness is Relative: Exploiting Tool-Call Idle Windows for Offloading in Agentic Systems with MORI
  - job: `.survey/work-queue/jobs/job-research-ca62fa2224d4eac8.json`
  - result: `.survey/work-queue/results/research/attempt-056e88f904b8cb0a268543b1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-056e88f904b8cb0a268543b1.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.00866-mori.md`
- **成功** `arXiv:2605.20706` — Llamas on the Web: Memory-Efficient, Performance-Portable, and Multi-Precision LLM Inference with WebGPU
  - job: `.survey/work-queue/jobs/job-research-3899c287a2c2de7d.json`
  - result: `.survey/work-queue/results/research/attempt-208eafaf198f5f787bed68e4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-208eafaf198f5f787bed68e4.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.20706-llamaweb.md`

#### Audit (:30)

- 最新観測run: **2026-09-19 23:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-19 23:00 JST**
- 耐久探索round: **11件** / immutable submission: **11件** / 検証済み成功result: **11件** / 個別result照合: **11件** / 個別result未照合: **0件** / 候補: **33件**
- 探索軸: HBM-host同時アクセス・CPU-free serving・portable local runtime / CXL共有KV・sparse attention remote memory・SmartNIC prefix caching / MoE expert prefetch・CPU/GPU offload・edge bandwidth adaptation / PD分離routing・selective KV transfer・multi-turn append-prefill / speculative serving・elastic attention/KV scaling・diffusion LLM continuous batching / agentic KV eviction・tool-call idle offload・workflow-aware caching / power-aware serving・on-device thermal control・multi-GPU energy modeling / hierarchical KV・CPU LLC residency・peer GPU cache tier / 2609新着・cross-DC PD・near-data MoE・offloaded KV sparse scan / NVMe delta prefetch・3D NAND compute・near-storage attention / elastic GPU memory・PIM hierarchy・prediction-guided dispatch
- round `specialist-memory-runtime-1` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2302JST-discovery-specialist-memory-runtime-1.json`
  - 探索軸: HBM-host同時アクセス・CPU-free serving・portable local runtime
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2302JST-discovery-specialist-memory-runtime-1.json` (`ok=true`)
- round `specialist-cxl-network-2` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2308JST-discovery-specialist-cxl-network-2.json`
  - 探索軸: CXL共有KV・sparse attention remote memory・SmartNIC prefix caching
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2308JST-discovery-specialist-cxl-network-2.json` (`ok=true`)
- round `specialist-moe-offload-3` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2313JST-discovery-specialist-moe-offload-3.json`
  - 探索軸: MoE expert prefetch・CPU/GPU offload・edge bandwidth adaptation
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2313JST-discovery-specialist-moe-offload-3.json` (`ok=true`)
- round `specialist-disagg-routing-4` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2318JST-discovery-specialist-disagg-routing-4.json`
  - 探索軸: PD分離routing・selective KV transfer・multi-turn append-prefill
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2318JST-discovery-specialist-disagg-routing-4.json` (`ok=true`)
- round `specialist-serving-runtime-5` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2324JST-discovery-specialist-serving-runtime-5.json`
  - 探索軸: speculative serving・elastic attention/KV scaling・diffusion LLM continuous batching
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2324JST-discovery-specialist-serving-runtime-5.json` (`ok=true`)
- round `specialist-agent-state-6` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2330JST-discovery-specialist-agent-state-6.json`
  - 探索軸: agentic KV eviction・tool-call idle offload・workflow-aware caching
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2330JST-discovery-specialist-agent-state-6.json` (`ok=true`)
- round `specialist-energy-runtime-7` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2335JST-discovery-specialist-energy-runtime-7.json`
  - 探索軸: power-aware serving・on-device thermal control・multi-GPU energy modeling
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2335JST-discovery-specialist-energy-runtime-7.json` (`ok=true`)
- round `specialist-memory-hierarchy-8` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2340JST-discovery-specialist-memory-hierarchy-8.json`
  - 探索軸: hierarchical KV・CPU LLC residency・peer GPU cache tier
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2340JST-discovery-specialist-memory-hierarchy-8.json` (`ok=true`)
- round `specialist-new-arrivals-9` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2346JST-discovery-specialist-new-arrivals-9.json`
  - 探索軸: 2609新着・cross-DC PD・near-data MoE・offloaded KV sparse scan
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2346JST-discovery-specialist-new-arrivals-9.json` (`ok=true`)
- round `specialist-storage-compute-10` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2351JST-discovery-specialist-storage-compute-10.json`
  - 探索軸: NVMe delta prefetch・3D NAND compute・near-storage attention
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2351JST-discovery-specialist-storage-compute-10.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2605.14249` — EnergyLens: Predictive Energy-Aware Exploration for Multi-GPU LLM Inference Optimization / worker `scheduled-chat-llm-survey`
  - claim: **09-19 23:40:04 JST** / heartbeat: **—** / lease expiry: **09-20 01:10:04 JST**
  - evidence: `.survey/work-queue/claims/job-research-3f8214d2f0afeac1.json`

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
| ready | **50** |

### 候補の重複・識別情報欠損

非終端Research jobだけを対象にしています。source URLは `url/source_url/paper_url/primary_url/arxiv_url/pdf_url/source.url` のいずれかで確認します。

| 指標 | 件数 |
|---|---:|
| 重複canonical_idグループ | **0** |
| 重複分のResearch job | **0** |
| canonical_id欠損 | **0** |
| title欠損 | **0** |
| source URL欠損 | **0** |

### 収録済み論文実体

`papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README、comparison系、Movedスタブを除外します。

| 指標 | 件数 |
|---|---:|
| inference/training/survey配下の論文Markdown実体 | **768** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **627** |
| └ Research | **480** |
| └ Audit | **2** |
| └ Discovery | **145** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

| 検出項目 | 件数 |
|---|---:|
| completed Research jobで指定paper実体なし | **0** |
| 対応jobなしsubmission（有効Discovery round除外） | **4** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **4** |

### 対応jobなしsubmissionの診断対象

上の異常件数と同一判定で抽出した耐久submission pathです。診断専用であり、submission/result自体は変更しません。

- `.survey/work-queue/submissions/20260919T1700JST-round09-os-pagecache.json`
- `.survey/work-queue/submissions/20260919T1700JST-round10-rdma-network.json`
- `.survey/work-queue/submissions/20260919T1700JST-round11-recent-crosscheck.json`
- `.survey/work-queue/submissions/20260919T1700JST-round12-citation-omissions.json`

### このSTATUSが採用する証拠

- **重要指標**: 候補・未claim・24h収録・最終収録・整合性異常を、jobs/submissions/results/claims/paper実体から直接再計算します。
- **収録候補**: `jobs/*.json` の非終端Research jobだけを対象にし、`canonical_id` の一意数を候補論文数として数えます。`canonical_id` 欠損jobは別件数で表示し、論文数へ推定加算しません。
- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。
- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。
- **Audit完了**: job/result/submissionの対応と成功状態を照合します。
- **論文実体数**: `papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README/comparison系/Movedスタブを除外します。
- **immutable submission未照合**: 検証済み成功に結びつかないsubmission実体を数え、処理待ちや失敗済みを含み得るため整合性異常とは分離します。
- **completed未検証**: completedでも現行の厳格な照合条件が成立しないjobを別計上し、過去形式や移行履歴を含み得るため異常とは断定しません。
- **整合性異常**: completed Research jobが宣言したpaper実体の欠損、未解決の対応jobなしsubmission、対応jobなし成功result、対応submissionなし成功resultを直接検出し、レコードpathで重複排除します。`discovery_stats.run_key + round` が揃ったDiscovery submission、および同一attempt/job/submissionへ対応する `content_validation` の再試行不可終端却下resultがあるsubmissionは、対応job欠損だけでは現在の異常にしません。
- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。
- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
