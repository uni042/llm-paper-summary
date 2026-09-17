# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-18 06:34:05 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **59** |
| 未claim Research job | **58** |
| 直近24hの検証済みResearch収録 | **49** |
| 最終検証済みResearch収録 | **09-18 06:07:01 JST（27分前）** |
| 整合性異常 | **2** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **59** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **59** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **10** | **1** | **1** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **17** | **8** | **8** | **0** | **0** | **0** | **18** |
| 合計 | **27** | **9** | **9** | **0** | **1** | **0** | **18** |

- 最新Discovery runの耐久探索round: **8件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-18 06:07:01 JST** [research] `arXiv:2602.10729` — BOute: Cost-Efficient LLM Serving with Heterogeneous LLMs and GPUs via Multi-Objective Bayesian Optimization
  - job: `.survey/work-queue/jobs/job-research-1fd656c9a10556db.json`
  - result: `.survey/work-queue/results/research/attempt-7ad6ad40100c07874c12360f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-7ad6ad40100c07874c12360f.json`
  - paper: `papers/inference/06-serving-scheduling/2026-2602.10729-boute-heterogeneous-model-gpu-routing.md`
- **09-18 06:03:44 JST** [research] `arXiv:2609.17573` — GroupKV: Hierarchical KV Cache Management for Long-Context Diffusion LLM Inference
  - job: `.survey/work-queue/jobs/job-research-a725b9cf79d670cf.json`
  - result: `.survey/work-queue/results/research/attempt-c9e86b0774fbe3177b6fb0f5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c9e86b0774fbe3177b6fb0f5.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.17573-groupkv-hierarchical-kv-cache-diffusion-llm.md`
- **09-18 05:35:17 JST** [research] `arXiv:2505.15781` — dKV-Cache: The Cache for Diffusion Language Models
  - job: `.survey/work-queue/jobs/job-research-b6925d33135e854c.json`
  - result: `.survey/work-queue/results/research/attempt-8a81151586fdc3a2613ff366.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8a81151586fdc3a2613ff366.json`
  - paper: `papers/inference/06-kv-cache-memory/2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md`
- **09-18 05:32:27 JST** [research] `arXiv:2504.05897` — HybriMoE: Hybrid CPU-GPU Scheduling and Cache Management for Efficient MoE Inference
  - job: `.survey/work-queue/jobs/job-research-fd53481863b8e4e0.json`
  - result: `.survey/work-queue/results/research/attempt-0f8f604e4dd41baf02109b3f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0f8f604e4dd41baf02109b3f.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2025-2504.05897-hybrimoe-hybrid-cpu-gpu-scheduling-cache-management.md`
- **09-18 04:43:56 JST** [research] `arXiv:2605.24832` — Optimus: Elastic Decoding for Efficient Diffusion LLM Serving
  - job: `.survey/work-queue/jobs/job-research-cbc6b0e2ec411766.json`
  - result: `.survey/work-queue/results/research/attempt-bfff6cdf557d0a31b3e1498c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bfff6cdf557d0a31b3e1498c.json`
  - paper: `papers/inference/06-serving-scheduling/2026-2605.24832-optimus-elastic-decoding-diffusion-llm-serving.md`
- **09-18 04:37:19 JST** [research] `arXiv:2609.18063` — The Other Half of the Memory Wall: Serving 35B MoEs from SSD with Trained Routing Prediction
  - job: `.survey/work-queue/jobs/job-research-97b8208885471bff.json`
  - result: `.survey/work-queue/results/research/attempt-d1f7aa5ebc3945e6ec100e5b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d1f7aa5ebc3945e6ec100e5b.json`
  - paper: `papers/inference/02-moe-offload/2026-2609.18063-edge0-ssd-moe-trained-routing-prediction.md`
- **09-18 04:33:26 JST** [research] `arXiv:2609.18110` — SSD-LLaMA: SSD-Native Inference for Trillion-Parameter MoE at 1+ Token/s on a Consumer PC
  - job: `.survey/work-queue/jobs/job-research-1e6c346844ef359a.json`
  - result: `.survey/work-queue/results/research/attempt-42b6429a1b73e190dbc9976c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-42b6429a1b73e190dbc9976c.json`
  - paper: `papers/inference/02-moe-offload/2026-2609.18110-ssd-llama-ssd-native-trillion-parameter-moe.md`
- **09-18 00:47:32 JST** [research] `arXiv:2502.06643` — MoETuner: Optimized Mixture of Expert Serving with Balanced Expert Placement and Token Routing
  - job: `.survey/work-queue/jobs/job-research-24c58326f22e095e.json`
  - result: `.survey/work-queue/results/research/attempt-788e1aebfc9c132ec95bfc8a.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-788e1aebfc9c132ec95bfc8a.json`
  - paper: `papers/inference/04-moe-parallelism-communication/2025-2502.06643-moetuner-balanced-expert-placement-token-routing.md`
- **09-18 00:40:31 JST** [research] `arXiv:2504.09345` — MoE-Lens: Towards the Hardware Limit of High-Throughput MoE LLM Serving Under Resource Constraints
  - job: `.survey/work-queue/jobs/job-research-36aaaee3c1110557.json`
  - result: `.survey/work-queue/results/research/attempt-dd0768548da66bf9efb0496c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-dd0768548da66bf9efb0496c.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2025-2504.09345-moe-lens-hardware-limit-resource-constrained-serving.md`
- **09-18 00:36:44 JST** [research] `arXiv:2604.14626` — ELMoE-3D: Leveraging Intrinsic Elasticity of MoE for Hybrid-Bonding-Enabled Self-Speculative Decoding in On-Premises Serving
  - job: `.survey/work-queue/jobs/job-research-a1761c9ca73f9afb.json`
  - result: `.survey/work-queue/results/research/attempt-721b895c107ac359ea8048a4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-721b895c107ac359ea8048a4.json`
  - paper: `papers/inference/02-hardware-accelerators/2026-2604.14626-elmoe-3d-hybrid-bonding-self-speculative-moe-serving.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-18 04:08:05 JST** job `job-eb22aac21645da23` / 候補 **5件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-cache-lineage-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-cache-lineage-3.json`
  - 探索軸: dLLM cache lineage・adaptive caching・hierarchical caching・dynamic eviction
- **09-18 04:08:12 JST** job `job-81083356e015ff3c` / 候補 **2件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-cache-lineage-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-cache-lineage-4.json`
  - 探索軸: dLLM delayed KV cache・dual adaptive cache・conference lineage
- **09-18 04:05:29 JST** job `job-09415fe947517f0c` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-kv-1.json`
  - 探索軸: 2026年9月新着・diffusion LLM・long-context KV offload/prefetch
- **09-18 04:08:18 JST** job `job-28c58a04ea5f0b58` / 候補 **2件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-serving-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-serving-2.json`
  - 探索軸: diffusion LLM serving・elastic decoding・KV reuse・parallel decoding
- **09-18 04:09:59 JST** job `job-6dc94e2aaef6c414` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-multitenant-fairness-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-multitenant-fairness-5.json`
  - 探索軸: 2026年9月新着・multi-tenant serving・latency isolation・fair scheduling
- **09-18 04:10:07 JST** job `job-cae0e4713a22115e` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-resilience-security-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-resilience-security-6.json`
  - 探索軸: fault tolerance・failure recovery・confidential serving・resource isolation
- **09-18 04:10:46 JST** job `job-7461140400013bb2` / 候補 **4件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-routing-lineage-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-routing-lineage-8.json`
  - 探索軸: multi-model routing lineage・predictive load balancing・DP routing・hardware-aware routing
- **09-18 04:10:15 JST** job `job-262a244fbc8c0261` / 候補 **3件**
  - result: `.survey/work-queue/results/20260918T0400JST-discovery-specialist-routing-recovery-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-routing-recovery-7.json`
  - 探索軸: heterogeneous multi-model routing・resource allocation・MoE failure recovery
- **09-18 02:59:29 JST** job `job-4c07976a89c00fbe` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T0300JST-discovery-specialist-cpu-gpu-moe-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0300JST-discovery-specialist-cpu-gpu-moe-1.json`
  - 探索軸: SSD-LLaMA関連・CPU-GPU hybrid MoE execution・expert delivery/cache
- **09-18 03:01:46 JST** job `job-1ae655d76711b99a` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T0300JST-discovery-specialist-gpu-storage-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T0300JST-discovery-specialist-gpu-storage-2.json`
  - 探索軸: direct I/O・GPU-initiated storage・SSD-backed LLM inference

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-18 05:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **1件** / 検証済み成功: **1件** / 未完了・未検証: **0件**
- **成功** `arXiv:2505.15781` — dKV-Cache: The Cache for Diffusion Language Models
  - job: `.survey/work-queue/jobs/job-research-b6925d33135e854c.json`
  - result: `.survey/work-queue/results/research/attempt-8a81151586fdc3a2613ff366.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8a81151586fdc3a2613ff366.json`
  - paper: `papers/inference/06-kv-cache-memory/2025-2505.15781-dkv-cache-delayed-kv-diffusion-language-models.md`

#### Audit (:30)

- 最新観測run: **2026-09-18 05:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-18 04:00 JST**
- 耐久探索round: **8件** / immutable submission: **8件** / 検証済み成功result: **8件** / 個別result照合: **8件** / 個別result未照合: **0件** / 候補: **18件**
- 探索軸: dLLM cache lineage・adaptive caching・hierarchical caching・dynamic eviction / dLLM delayed KV cache・dual adaptive cache・conference lineage / 2026年9月新着・diffusion LLM・long-context KV offload/prefetch / diffusion LLM serving・elastic decoding・KV reuse・parallel decoding / 2026年9月新着・multi-tenant serving・latency isolation・fair scheduling / fault tolerance・failure recovery・confidential serving・resource isolation / multi-model routing lineage・predictive load balancing・DP routing・hardware-aware routing / heterogeneous multi-model routing・resource allocation・MoE failure recovery
- round `specialist-dllm-cache-lineage-3` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-cache-lineage-3.json`
  - 探索軸: dLLM cache lineage・adaptive caching・hierarchical caching・dynamic eviction
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-cache-lineage-3.json` (`ok=true`)
- round `specialist-dllm-cache-lineage-4` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-cache-lineage-4.json`
  - 探索軸: dLLM delayed KV cache・dual adaptive cache・conference lineage
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-cache-lineage-4.json` (`ok=true`)
- round `specialist-dllm-kv-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-kv-1.json`
  - 探索軸: 2026年9月新着・diffusion LLM・long-context KV offload/prefetch
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-kv-1.json` (`ok=true`)
- round `specialist-dllm-serving-2` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-dllm-serving-2.json`
  - 探索軸: diffusion LLM serving・elastic decoding・KV reuse・parallel decoding
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-dllm-serving-2.json` (`ok=true`)
- round `specialist-multitenant-fairness-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-multitenant-fairness-5.json`
  - 探索軸: 2026年9月新着・multi-tenant serving・latency isolation・fair scheduling
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-multitenant-fairness-5.json` (`ok=true`)
- round `specialist-resilience-security-6` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-resilience-security-6.json`
  - 探索軸: fault tolerance・failure recovery・confidential serving・resource isolation
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-resilience-security-6.json` (`ok=true`)
- round `specialist-routing-lineage-8` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-routing-lineage-8.json`
  - 探索軸: multi-model routing lineage・predictive load balancing・DP routing・hardware-aware routing
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-routing-lineage-8.json` (`ok=true`)
- round `specialist-routing-recovery-7` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260918T0400JST-discovery-specialist-routing-recovery-7.json`
  - 探索軸: heterogeneous multi-model routing・resource allocation・MoE failure recovery
  - 個別result照合: あり / `.survey/work-queue/results/20260918T0400JST-discovery-specialist-routing-recovery-7.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2605.06113` — Tackling the Data-Parallel Load Balancing Bottleneck in LLM Serving: Practical Online Routing at Scale / worker `scheduled-chat-llm-survey`
  - claim: **09-18 05:35:39 JST** / heartbeat: **—** / lease expiry: **09-18 07:05:39 JST**
  - evidence: `.survey/work-queue/claims/job-research-39525f58ef98f435.json`

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
| ready | **59** |

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
| inference/training/survey配下の論文Markdown実体 | **690** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **462** |
| └ Research | **333** |
| └ Audit | **2** |
| └ Discovery | **125** |
| └ Other/Unknown | **2** |

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
| 対応jobなしsubmission（有効Discovery round除外） | **2** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **2** |

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
