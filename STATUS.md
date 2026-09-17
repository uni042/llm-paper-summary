# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-17 09:04:24 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **57** |
| 未claim Research job | **55** |
| 直近24hの検証済みResearch収録 | **90** |
| 最終検証済みResearch収録 | **09-17 07:22:13 JST（1時間42分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **57** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **57** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **8** | **8** | **4** | **4** | **2** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **16** | **2** | **2** | **0** | **0** | **0** | **6** |
| 合計 | **24** | **10** | **6** | **4** | **2** | **0** | **6** |

- 最新Discovery runの耐久探索round: **2件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-17 07:22:13 JST** [research] `arXiv:2511.20982` — A Dynamic PD-Disaggregation Architecture for Maximizing Goodput in LLM Inference Serving
  - job: `.survey/work-queue/jobs/job-research-0d9ff237f1d632e6.json`
  - result: `.survey/work-queue/results/research/attempt-cd6a647437352aca5df92996.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cd6a647437352aca5df92996.json`
  - paper: `papers/inference/06-serving-scheduling/2025-2511.20982-dopd-dynamic-pd-disaggregation.md`
- **09-17 07:20:14 JST** [research] `arXiv:2608.25062` — FLINT: Efficiently Leveraging High Bandwidth Flash for Capacity-Scalable LLM Inference Acceleration
  - job: `.survey/work-queue/jobs/job-research-0d64167980707ffd.json`
  - result: `.survey/work-queue/results/research/attempt-2b046e19162a735734acee9b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2b046e19162a735734acee9b.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2608.25062-flint-efficiently-leveraging-high-bandwidth-flash-for-capacity-scalable-llm-inference-acceleration.md`
- **09-17 07:18:46 JST** [research] `arXiv:2601.11822` — RAPID-Serve: Resource-efficient and Accelerated P/D Intra-GPU Disaggregation
  - job: `.survey/work-queue/jobs/job-research-af7d4aee1c99dd28.json`
  - result: `.survey/work-queue/results/research/attempt-73081685c32e0006998f3d67.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-73081685c32e0006998f3d67.json`
  - paper: `papers/inference/06-serving-scheduling/2026-2601.11822-rapid-serve-intra-gpu-pd-disaggregation.md`
- **09-17 06:35:28 JST** [research] `arXiv:2609.16491` — PipeSwift: Revisiting Pipeline Parallelism for Large-Scale Completion-Oriented Agentic Serving
  - job: `.survey/work-queue/jobs/job-research-98e8633cce3c47f1.json`
  - result: `.survey/work-queue/results/research/attempt-9c7bc1c5f144c062d60905d3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9c7bc1c5f144c062d60905d3.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.16491-pipeswift-pipeline-parallel-agentic-serving.md`
- **09-17 04:37:50 JST** [research] `arXiv:2609.14872` — AgentKV: Phase-Aware KV Eviction for Agentic LLMs
  - job: `.survey/work-queue/jobs/job-research-71c206bf0990ca87.json`
  - result: `.survey/work-queue/results/research/attempt-5f751e3b4a448f7f2f7978ae.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5f751e3b4a448f7f2f7978ae.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.14872-agentkv-phase-aware-kv-eviction-agentic-llms.md`
- **09-17 04:34:56 JST** [research] `arXiv:2609.16161` — LLM Inference in a Flash!
  - job: `.survey/work-queue/jobs/job-research-99325bb434e8c117.json`
  - result: `.survey/work-queue/results/research/attempt-9333f33610f25827f87c2af1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9333f33610f25827f87c2af1.json`
  - paper: `papers/inference/04-cpu-ssd-offload/2026-2609.16161-llm-inference-in-a-flash.md`
- **09-17 03:41:56 JST** [research] `arXiv:2609.13285` — Grouped Value Attention: Efficient KV Caching via On-Demand Key Reconstruction
  - job: `.survey/work-queue/jobs/job-research-38c18cd4bb2728b9.json`
  - result: `.survey/work-queue/results/research/attempt-d6929dca26947ce1b79ba676.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d6929dca26947ce1b79ba676.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.13285-grouped-value-attention-efficient-kv-caching.md`
- **09-17 03:38:32 JST** [research] `arXiv:2609.13161` — PDD: Unleashing Economical and Flexible Heterogeneous LLM Inference via Cross-Datacenter Prefill-Decode Disaggregation
  - job: `.survey/work-queue/jobs/job-research-9f909dd53a5f1acb.json`
  - result: `.survey/work-queue/results/research/attempt-942145c6596d2cfdf7866f97.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-942145c6596d2cfdf7866f97.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.13161-pdd-cross-datacenter-prefill-decode-disaggregation.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-17 07:11:15 JST** job `job-05d7dc3b9919ab5f` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T0710JST-discovery-recovery-legacy-invalid-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0710JST-discovery-recovery-legacy-invalid-1.json`
  - 探索軸: recovery-of-invalid-discovery-submissions
- **09-17 07:11:19 JST** job `job-d2f6e7770e461596` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T0710JST-discovery-recovery-legacy-invalid-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0710JST-discovery-recovery-legacy-invalid-2.json`
  - 探索軸: recovery-of-invalid-discovery-submissions
- **09-17 07:05:07 JST** job `job-e64ad8e5caaeb00f` / 候補 **4件**
  - result: `.survey/work-queue/results/20260917T0700JST-discovery-specialist-scheduling-memory-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0700JST-discovery-specialist-scheduling-memory-1.json`
  - 探索軸: 2025 LLM serving scheduling・CPU/GPU coupled memory・DIMM-PIM disaggregation
- **09-17 06:07:57 JST** job `job-5abe9b84bcfd8389` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T0600JST-discovery-specialist-forward-serving-3a.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0600JST-discovery-specialist-forward-serving-3a.json`
  - 探索軸: 既収録重要serving論文のforward citation・2025-2026 PD disaggregation・multi-LLM servingの未収録探索
- **09-17 06:08:01 JST** job `job-c862ad2804181f57` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T0600JST-discovery-specialist-forward-serving-3b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0600JST-discovery-specialist-forward-serving-3b.json`
  - 探索軸: 既収録重要serving論文のforward citation・2025-2026 PD disaggregation・multi-LLM servingの未収録探索
- **09-17 06:04:53 JST** job `job-5cd9a5af133e1001` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T0600JST-discovery-specialist-recent-serving-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0600JST-discovery-specialist-recent-serving-1.json`
  - 探索軸: 2026-09新着のLLM serving・parallelism・KV cache・MoE inference・speculative decoding
- **09-17 06:08:05 JST** job `job-e175f086e1eec097` / 候補 **0件**
  - result: `.survey/work-queue/results/20260917T0600JST-discovery-specialist-runtime-communication-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0600JST-discovery-specialist-runtime-communication-2.json`
  - 探索軸: 2026-09新着のdistributed inference communication・GPU runtime・expert movement・serving stack
- **09-17 05:02:46 JST** job `job-81d9561e39a761a9` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T0500JST-discovery-specialist-moe-kv-sharding-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0500JST-discovery-specialist-moe-kv-sharding-1.json`
  - 探索軸: MoE expert-sharded KV cache・expert residency・distributed cache routing
- **09-17 04:03:42 JST** job `job-93fb2f0552bd58b2` / 候補 **2件**
  - result: `.survey/work-queue/results/20260917T0400JST-discovery-specialist-agentic-serving-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0400JST-discovery-specialist-agentic-serving-4.json`
  - 探索軸: agentic/multi-turn serving・phase-aware KV management・workflow scheduling
- **09-17 04:01:52 JST** job `job-e30ba5725a8a8a2d` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T0400JST-discovery-specialist-flash-memory-hardware-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0400JST-discovery-specialist-flash-memory-hardware-1.json`
  - 探索軸: Compute-in-Flash・SSD weight offload・near-storage processing・heterogeneous memory hardware

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

- 最新観測run: **2026-09-17 07:10 JST**
- 耐久探索round: **2件** / immutable submission: **2件** / 検証済み成功result: **2件** / 個別result照合: **2件** / 個別result未照合: **0件** / 候補: **6件**
- 探索軸: recovery-of-invalid-discovery-submissions
- round `legacy-invalid-recovery-1` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260917T0710JST-discovery-recovery-legacy-invalid-1.json`
  - 探索軸: recovery-of-invalid-discovery-submissions
  - 個別result照合: あり / `.survey/work-queue/results/20260917T0710JST-discovery-recovery-legacy-invalid-1.json` (`ok=true`)
- round `legacy-invalid-recovery-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260917T0710JST-discovery-recovery-legacy-invalid-2.json`
  - 探索軸: recovery-of-invalid-discovery-submissions
  - 個別result照合: あり / `.survey/work-queue/results/20260917T0710JST-discovery-recovery-legacy-invalid-2.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **2件** / 直近15分heartbeat: **0件**
- `arXiv:2406.11674` — Endor: Hardware-Friendly Sparse Format for Offloaded LLM Inference / worker `scheduled-chat-discovery-specialist`
  - claim: **09-17 09:04:05 JST** / heartbeat: **—** / lease expiry: **09-17 10:34:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-411dee2b8db54e04.json`
- `arXiv:2507.06608` — Nexus: Proactive Intra-GPU Disaggregation of Prefill and Decode in LLM Serving / worker `scheduled-chat-discovery-specialist-0700`
  - claim: **09-17 07:22:10 JST** / heartbeat: **09-17 08:28:37 JST** / lease expiry: **09-17 09:58:37 JST**
  - evidence: `.survey/work-queue/claims/job-research-120be1bd98c2839e.json`

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
| ready | **57** |

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
| inference/training/survey配下の論文Markdown実体 | **645** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **404** |
| └ Research | **277** |
| └ Audit | **2** |
| └ Discovery | **125** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。 旧形式のDiscovery submissionが `invalid submit_discovery_round payload` で失敗した履歴は、そのsubmission内の全candidateが現在のjobまたはpaper identity indexで確認できる場合に限り、履歴として保持したまま現在の異常から除外します。

| 検出項目 | 件数 |
|---|---:|
| completed Research jobで指定paper実体なし | **0** |
| 対応jobなしsubmission（有効Discovery round除外） | **0** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **0** |

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
