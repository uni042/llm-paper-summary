# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 19:38:00 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **31** |
| 未claim Research job | **29** |
| 直近24hの検証済みResearch収録 | **66** |
| 最終検証済みResearch収録 | **09-16 18:51:24 JST（46分前）** |
| 整合性異常 | **1** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **31** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **31** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **39** | **8** | **4** | **4** | **2** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **24** | **0** | **24** | **0** | **0** | **32** |
| 合計 | **39** | **32** | **4** | **28** | **2** | **0** | **32** |

- 最新Discovery runの耐久探索round: **24件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-16 18:51:24 JST** [research] `arXiv:2608.30076` — Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects
  - job: `.survey/work-queue/jobs/job-research-dea6b2b543d05a36.json`
  - result: `.survey/work-queue/results/research/attempt-65de370d3bdc114f83e19319.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-65de370d3bdc114f83e19319.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2026-2608.30076-budget-aware-compression-single-gpu.md`
- **09-16 18:49:43 JST** [research] `arXiv:2604.07472` — Fast Heterogeneous Serving: Scalable Mixed-Scale LLM Allocation for SLO-Constrained Inference
  - job: `.survey/work-queue/jobs/job-research-c5a47af1c9e3acf3.json`
  - result: `.survey/work-queue/results/research/attempt-44002611be590dff9f7593f6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-44002611be590dff9f7593f6.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2604.07472-fast-heterogeneous-serving-allocation.md`
- **09-16 18:38:33 JST** [research] `arXiv:2609.09662` — PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling
  - job: `.survey/work-queue/jobs/job-research-3d5f11737ec9b4a2.json`
  - result: `.survey/work-queue/results/research/attempt-b66d308c0d1e4eb8ba288ecc.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b66d308c0d1e4eb8ba288ecc.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.09662-pelm-speculative-decoding-dvfs.md`
- **09-16 18:33:21 JST** [research] `arXiv:2609.11058` — EMMI: Edge Multi-Modal Intelligence for Communication-Efficient MLLM Inference via Fused Representation Compression
  - job: `.survey/work-queue/jobs/job-research-ad3541d28015a662.json`
  - result: `.survey/work-queue/results/research/attempt-095563049565ccc0498d1b47.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-095563049565ccc0498d1b47.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.11058-emmi-edge-multimodal-representation-compression.md`
- **09-16 18:19:57 JST** [research] `arXiv:2409.15104` — CSPS: A Communication-Efficient Sequence-Parallelism based Serving System for Transformer based Models with Long Prompts
  - job: `.survey/work-queue/jobs/job-research-6eb709dc3f5cf15a.json`
  - result: `.survey/work-queue/results/research/attempt-517d9d0491722109185669ac.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-517d9d0491722109185669ac.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2409.15104-csps-a-communication-efficient-sequence-parallelism-based-serving-system-for-transformer-based-models-with-long-prompts.md`
- **09-16 18:09:41 JST** [research] `arXiv:2511.21669` — DSD: A Distributed Speculative Decoding Solution for Edge-Cloud Agile Large Model Serving
  - job: `.survey/work-queue/jobs/job-research-9d70d3111564c88d.json`
  - result: `.survey/work-queue/results/research/attempt-e98c6f562dcc3c2cf28e5d6f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e98c6f562dcc3c2cf28e5d6f.json`
  - paper: `papers/inference/07-speculative-decoding/2025-2511.21669-dsd-distributed-edge-cloud-speculative-decoding.md`
- **09-16 18:03:34 JST** [research] `arXiv:2605.05219` — Sparse Prefix Caching for Hybrid and Recurrent LLM Serving
  - job: `.survey/work-queue/jobs/job-research-34cb083c55afaad3.json`
  - result: `.survey/work-queue/results/research/attempt-ad5dfb814d7090ff8006d8de.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ad5dfb814d7090ff8006d8de.json`
  - paper: `papers/inference/04-kv-prefix-cache/2026-2605.05219-sparse-prefix-caching-hybrid-recurrent.md`
- **09-16 17:15:27 JST** [research] `arXiv:2509.24832` — SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching
  - job: `.survey/work-queue/jobs/job-research-b98e4e299d06a6a5.json`
  - result: `.survey/work-queue/results/research/attempt-4aa0bdcf550c974e39ccae92.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4aa0bdcf550c974e39ccae92.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md`
- **09-16 17:12:14 JST** [research] `arXiv:2604.23467` — Hybrid JIT-CUDA Graph Optimization for Low-Latency Large Language Model Inference
  - job: `.survey/work-queue/jobs/job-research-3ad6262bd04cfbe6.json`
  - result: `.survey/work-queue/results/research/attempt-5b2f0818dd442ca0014c8634.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5b2f0818dd442ca0014c8634.json`
  - paper: `papers/inference/09-kernel-runtime-compilation/2026-2604.23467-hybrid-jit-cuda-graph-low-latency-inference.md`
- **09-16 17:08:50 JST** [research] `arXiv:2605.22566` — GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving
  - job: `.survey/work-queue/jobs/job-research-44674a8f55b9f5e8.json`
  - result: `.survey/work-queue/results/research/attempt-82e80ed19ce701a0be49bf58.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-82e80ed19ce701a0be49bf58.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.22566-graphflow-agent-workflow-serving.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-16 16:00 JST** / worker `scheduled-chat-discovery-20260916T1600JST`
- immutable submission: **8件** / 検証済み成功: **4件** / 未完了・未検証: **4件**
- **成功** `arXiv:2609.08306` — HoneyRoute: Honeypot-Model Routing for Adversarial LLM Serving
  - job: `.survey/work-queue/jobs/job-research-ec48da5b1e9edcea.json`
  - result: `.survey/work-queue/results/research/attempt-10ba900257289562be435001.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-10ba900257289562be435001.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.08306-honeyroute-adversarial-llm-serving-routing.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-201fb89bc61573cc411909b4.json` (job `job-research-6252d370adc380b9`)
- **成功** `arXiv:2509.24832` — SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching
  - job: `.survey/work-queue/jobs/job-research-b98e4e299d06a6a5.json`
  - result: `.survey/work-queue/results/research/attempt-4aa0bdcf550c974e39ccae92.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4aa0bdcf550c974e39ccae92.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md`
- **成功** `arXiv:2604.23467` — Hybrid JIT-CUDA Graph Optimization for Low-Latency Large Language Model Inference
  - job: `.survey/work-queue/jobs/job-research-3ad6262bd04cfbe6.json`
  - result: `.survey/work-queue/results/research/attempt-5b2f0818dd442ca0014c8634.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5b2f0818dd442ca0014c8634.json`
  - paper: `papers/inference/09-kernel-runtime-compilation/2026-2604.23467-hybrid-jit-cuda-graph-low-latency-inference.md`
- **成功** `arXiv:2605.22566` — GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving
  - job: `.survey/work-queue/jobs/job-research-44674a8f55b9f5e8.json`
  - result: `.survey/work-queue/results/research/attempt-82e80ed19ce701a0be49bf58.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-82e80ed19ce701a0be49bf58.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.22566-graphflow-agent-workflow-serving.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-9bd72451731af90ab90c3e14.json` (job `job-research-6252d370adc380b9`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-b21265e1c7564132469a29b8.json` (job `job-research-ec48da5b1e9edcea`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-e3573f73597d9a563a861b51.json` (job `job-research-44674a8f55b9f5e8`)

#### Audit (:30)

- 最新観測run: **2026-09-16 16:00 JST** / worker `scheduled-chat-discovery-20260916T1600JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-16 19:00 JST**
- 耐久探索round: **24件** / immutable submission: **24件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **24件** / 候補: **32件**
- 探索軸: MoE expert speculative prefetch・CPU/GPU異種実行 / agentic serving・構造的KV再利用・共有圧縮cache / CPU control-plane bottleneck・SmartNIC/GPU serving-stack offload / CUDA VMM・KV memory reclamation・prefill reserve / CXL composable memory・Kubernetes DRA・cross-node KV reuse / multi-agent collective KV sharing・All-Gather redundancy elimination / GPU runtime/compiler・persistent dynamic megakernel / disaggregated serving・network/KV-aware routing・hardware calibration / 新着KV compression・prompt-adaptive configuration selection / 重要新規系統のforward citation追跡 / 重要論文のbackward reference・基盤システム / OS/storage/HPC隣接・CXL hybrid memory tiering・remote memory expansion / MoE multi-model serving・weight/KV disaggregation・GPU memory pooling / network-aware decode routing・mixed-precision KV transfer / agentic serving・external KV storage I/O・dual-path RDMA loading / 最新novel候補群のforward citation・派生追跡 / CrossPool backward reference・MoE disaggregated expert parallelism基盤 / MoE serving resilience・KV checkpoint・shadow experts / GPU runtime・lossless weight compression・fused decompression GEMM / MoE serverless elasticity・token-budget fleet routing / 2025重要未収録・CXL KV・multi-GPU MoE・edge expert streaming / MoE dual-phase prefetch・cross-model KV reuse・agent serving simulation / agentic tokenization・MoE expert residency paging・agent-aware runtime tier / heterogeneous HBM sharing・KV growth induced congestion
- round `specialist-moe-prefetch-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1908JST-discovery-specialist-moe-prefetch-1.json`
  - 探索軸: MoE expert speculative prefetch・CPU/GPU異種実行
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-agent-kv-2` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T1910JST-discovery-specialist-agent-kv-2.json`
  - 探索軸: agentic serving・構造的KV再利用・共有圧縮cache
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cpu-control-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T1912JST-discovery-specialist-cpu-control-3.json`
  - 探索軸: CPU control-plane bottleneck・SmartNIC/GPU serving-stack offload
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-elastic-kv-4` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1914JST-discovery-specialist-elastic-kv-4.json`
  - 探索軸: CUDA VMM・KV memory reclamation・prefill reserve
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cxl-k8s-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1917JST-discovery-specialist-cxl-k8s-5.json`
  - 探索軸: CXL composable memory・Kubernetes DRA・cross-node KV reuse
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-collective-agent-kv-6` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1919JST-discovery-specialist-collective-agent-kv-6.json`
  - 探索軸: multi-agent collective KV sharing・All-Gather redundancy elimination
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-gpu-megakernel-7` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1921JST-discovery-specialist-gpu-megakernel-7.json`
  - 探索軸: GPU runtime/compiler・persistent dynamic megakernel
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-network-routing-8` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1924JST-discovery-specialist-network-routing-8.json`
  - 探索軸: disaggregated serving・network/KV-aware routing・hardware calibration
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-adaptive-kv-9` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1927JST-discovery-specialist-adaptive-kv-9.json`
  - 探索軸: 新着KV compression・prompt-adaptive configuration selection
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-forward-citations-10` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260916T1930JST-discovery-specialist-forward-citations-10.json`
  - 探索軸: 重要新規系統のforward citation追跡
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **2件** / 直近15分heartbeat: **0件**
- `arXiv:2609.16206` — Calibrate, Then Route: A Measured Study of Learned Request Routing for Disaggregated LLM Serving / worker `scheduled-chat-llm-survey`
  - claim: **09-16 19:34:57 JST** / heartbeat: **—** / lease expiry: **09-16 21:04:57 JST**
  - evidence: `.survey/work-queue/claims/job-research-46a0d6f61e82afe1.json`
- `arXiv:2604.11001` — Flow-Controlled Scheduling for LLM Inference with Provable Stability Guarantees / worker `scheduled-chat-paper-20260916T175945JST`
  - claim: **09-16 18:23:00 JST** / heartbeat: **09-16 18:31:09 JST** / lease expiry: **09-16 20:01:09 JST**
  - evidence: `.survey/work-queue/claims/job-research-df04bb2baebfa878.json`

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
| ready | **31** |

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
| inference/training/survey配下の論文Markdown実体 | **614** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **403** |
| └ Research | **235** |
| └ Audit | **1** |
| └ Discovery | **167** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

| 検出項目 | 件数 |
|---|---:|
| completed Research jobで指定paper実体なし | **0** |
| 対応jobなしsubmission（有効Discovery round除外） | **1** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **1** |

### このSTATUSが採用する証拠

- **重要指標**: 候補・未claim・24h収録・最終収録・整合性異常を、jobs/submissions/results/claims/paper実体から直接再計算します。
- **収録候補**: `jobs/*.json` の非終端Research jobだけを対象にし、`canonical_id` の一意数を候補論文数として数えます。`canonical_id` 欠損jobは別件数で表示し、論文数へ推定加算しません。
- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。
- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。
- **Audit完了**: job/result/submissionの対応と成功状態を照合します。
- **論文実体数**: `papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README/comparison系/Movedスタブを除外します。
- **immutable submission未照合**: 検証済み成功に結びつかないsubmission実体を数え、処理待ちや失敗済みを含み得るため整合性異常とは分離します。
- **completed未検証**: completedでも現行の厳格な照合条件が成立しないjobを別計上し、過去形式や移行履歴を含み得るため異常とは断定しません。
- **整合性異常**: completed Research jobが宣言したpaper実体の欠損、対応jobなしsubmission、対応jobなし成功result、対応submissionなし成功resultを直接検出し、レコードpathで重複排除します。`discovery_stats.run_key + round` が揃ったDiscovery submissionは対応job欠損だけでは異常にしません。
- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。
- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
