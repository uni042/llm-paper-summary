# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-24 22:24:02 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **291** |
| 未claim Research job | **159** |
| 直近24hの検証済みResearch収録 | **16** |
| 最終検証済みResearch収録 | **09-24 18:15:31 JST** |
| 最終検証済みDiscovery探索 | **09-24 22:15:14 JST** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **291** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **291** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6818** |
| 処理済み | **667** |
| 未処理 | **6151** |
| 収録済みとして除外 | **558** |
| 無関係として除外 | **49** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（13時間48分前）** |
| 最終maintenance status | **issues_found** |
| consistency | **passed** |
| health | **issues_found** |
| health errors / warnings | **2 / 0** |
| metadata | **passed** |
| metadata incomplete | **0** |
| GC削除件数 | **631** |
| queue snapshot repaired | **true** |
| index repairs | **0** |
| quality regressions | **3** |

maintenance固有の値は `maintenance-cycle.json` を正本とし、通常のjob/result件数から推定しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **9** | **3** | **2** | **0** | **132** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **25** | **1** | **1** | **0** | **0** | **0** | **0** |
| 合計 | **34** | **4** | **3** | **0** | **132** | **0** | **0** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-24 18:15:31 JST** [research] `arXiv:2609.26796` — Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs
  - job: `.survey/work-queue/jobs/job-research-41d37332b16e3d57.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3ee424a7b2b36c6924101628.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3ee424a7b2b36c6924101628.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.26796-flash-dllm-io-aware-kv-caching-and-parallel-decoding-for-fast-memory-efficient-diffusion-llms.md`
- **09-24 18:12:55 JST** [research] `arXiv:2609.26300` — CompKV: Compensation-Aware KV Selection for Long-Context LLM Inference
  - job: `.survey/work-queue/jobs/job-research-7ecc4d7949c81534.json`
  - result: `.survey/work-queue/results/research/attempt-preload-7567c60b834735ea01f92a82.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-7567c60b834735ea01f92a82.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.26300-compkv-compensation-aware-kv-selection-for-long-context-llm-inference.md`
- **09-24 18:12:55 JST** [research] `arXiv:2606.24033` — RoPE-Aware Bit Allocation for KV-Cache Quantization
  - job: `.survey/work-queue/jobs/job-research-ed39f178b202751f.json`
  - result: `.survey/work-queue/results/research/attempt-preload-d0b404e285d49a0ce5994e57.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-d0b404e285d49a0ce5994e57.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md`
- **09-24 18:07:25 JST** [research] `arXiv:2508.15487` — Dream 7B: Diffusion Large Language Models
  - job: `.survey/work-queue/jobs/job-research-1ba7917ba260cdda.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3a8d1487d30c19a489a3f0c1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3a8d1487d30c19a489a3f0c1.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2508.15487-dream-7b-diffusion-large-language-models.md`
- **09-24 18:07:25 JST** [research] `arXiv:2509.12211` — TinyServe: Query-Aware Cache Selection for Efficient LLM Serving
  - job: `.survey/work-queue/jobs/job-research-3d37c9d48dc78998.json`
  - result: `.survey/work-queue/results/research/attempt-preload-88865dce95348e7f779dacec.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-88865dce95348e7f779dacec.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2509.12211-tinyserve-query-aware-cache-selection.md`
- **09-24 17:51:11 JST** [research] `arXiv:2505.16502` — Recursive Offloading for LLM Serving in Multi-tier Networks
  - job: `.survey/work-queue/jobs/job-research-df8b6eaefcbe8aad.json`
  - result: `.survey/work-queue/results/research/attempt-preload-886ad02757673f91debfda1d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-886ad02757673f91debfda1d.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2505.16502-recursive-offloading-for-llm-serving-in-multi-tier-networks.md`
- **09-24 17:48:14 JST** [research] `arXiv:2603.09023` — The Missing Memory Hierarchy: Demand Paging for LLM Context Windows
  - job: `.survey/work-queue/jobs/job-research-105b69444b4fa0ad.json`
  - result: `.survey/work-queue/results/research/attempt-preload-54d2a2c5f4eca8e69e54d846.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-54d2a2c5f4eca8e69e54d846.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2603.09023-pichay-demand-paging-context-windows.md`
- **09-24 17:42:58 JST** [research] `arXiv:2310.01889` — Ring Attention with Blockwise Transformers for Near-Infinite Context
  - job: `.survey/work-queue/jobs/job-research-60b244663bfce823.json`
  - result: `.survey/work-queue/results/research/attempt-preload-74bb4af6ce3df82b5f4f239a.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-74bb4af6ce3df82b5f4f239a.json`
  - paper: `papers/inference/99-other-inference-systems/2023-2310.01889-ring-attention-blockwise-transformers.md`
- **09-24 17:39:11 JST** [research] `arXiv:2606.20537` — Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving
  - job: `.survey/work-queue/jobs/job-research-374463a300b97ed5.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3c754529c6f791ee0cbc78c5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3c754529c6f791ee0cbc78c5.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.20537-execution-state-capsules-graph-bound-execution-state-checkpoint-and-restore-for-low-latency-small-batch-on-device-physic.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-24 22:15:14 JST** job `job-121edc29d47e3074` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T130330Z-scheduled-chat-00-6e21c4-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T130330Z-scheduled-chat-00-6e21c4-r1.json`
  - 探索軸: preload-backward-structured-references
- **09-24 22:15:07 JST** job `job-62fd66001f3e574b` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T123145Z-scheduled-chat-30-8f31c2-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T123145Z-scheduled-chat-30-8f31c2-r1.json`
  - 探索軸: preload-backward-structured-references
- **09-24 19:55:28 JST** job `job-cfc2aa0addf64b6e` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T095930Z-scheduled-chat-00-6f4c2a-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/20260924T095930Z-scheduled-chat-00-6f4c2a-r1.json`
  - 探索軸: backward references from repository structured references
- **09-24 18:30:59 JST** job `job-3f7d42c402f19022` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T093030Z-scheduled-chat-30-4b7e2a-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T093030Z-scheduled-chat-30-4b7e2a-r1.json`
  - 探索軸: backward references of arXiv:2401.09670
- **09-24 18:33:47 JST** job `job-c06a53d7d9488737` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T093300Z-scheduled-chat-30-4b7e2a-r2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T093300Z-scheduled-chat-30-4b7e2a-r2.json`
  - 探索軸: forward citations of arXiv:2306.00978
- **09-24 22:13:52 JST** job `job-f9a9fdd42f4f42ad` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-agent-multimodal-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-agent-multimodal-6.json`
  - 探索軸: agentic serving・multimodal serving・stateful runtime
- **09-24 22:13:59 JST** job `job-e339316cfe3974cc` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-cpu-heterogeneous-10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-cpu-heterogeneous-10.json`
  - 探索軸: CPU-only・CPU/GPU heterogeneous inference runtime
- **09-24 22:14:06 JST** job `job-9521bd9e238ef538` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-energy-saturation-11.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-energy-saturation-11.json`
  - 探索軸: energy・power-aware serving・DVFS
- **09-24 22:14:13 JST** job `job-f629b37eed727368` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-framework-control-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-framework-control-8.json`
  - 探索軸: serving framework control-plane・CPU-free runtime
- **09-24 22:14:19 JST** job `job-2599255a1ee2cfaf` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-hierarchical-memory-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-hierarchical-memory-2.json`
  - 探索軸: SSD/NVMe・GPUDirect Storage・階層メモリ・PIM/CXL

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-24 17:55 JST** / worker `scheduled-chat-30`
- immutable submission: **3件** / 検証済み成功: **2件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **成功** `arXiv:2609.26796` — Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs
  - job: `.survey/work-queue/jobs/job-research-41d37332b16e3d57.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3ee424a7b2b36c6924101628.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3ee424a7b2b36c6924101628.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.26796-flash-dllm-io-aware-kv-caching-and-parallel-decoding-for-fast-memory-efficient-diffusion-llms.md`
- **成功** `arXiv:2609.26300` — CompKV: Compensation-Aware KV Selection for Long-Context LLM Inference
  - job: `.survey/work-queue/jobs/job-research-7ecc4d7949c81534.json`
  - result: `.survey/work-queue/results/research/attempt-preload-7567c60b834735ea01f92a82.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-7567c60b834735ea01f92a82.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.26300-compkv-compensation-aware-kv-selection-for-long-context-llm-inference.md`
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-f151a18e22842a355a31eb94.json` (job `job-research-fc413cbcbab0d455`, failure_class `post_validation_processing_failure`)
  - result: `.survey/work-queue/results/research/attempt-preload-f151a18e22842a355a31eb94.json` (`ok=false`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-24 17:55 JST** / worker `scheduled-chat-30`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-24 22:00 JST**
- 耐久探索round: **1件** / immutable submission: **1件** / 検証済み成功result: **1件** / 個別result照合: **1件** / 個別result未照合: **0件** / 候補: **0件**
- 探索軸: preload-backward-structured-references
- round `take-scheduled-chat-00-20260924T130032Z-6e21c4-r1` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260924T130330Z-scheduled-chat-00-6e21c4-r1.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/20260924T130330Z-scheduled-chat-00-6e21c4-r1.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **132件** / 直近15分heartbeat: **0件**
- `arXiv:2609.25451` — Fast Recovery for LLM Serving via Decoupled Device Memory Lifetime in Dynamo / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-05fc71d26e12a3ee.json`
- `arXiv:2609.23816` — SPLASH: Co-Designing Sparse Attention with High-Bandwidth Flash for Efficient Long-Context Inference / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-0729262d447a8308.json`
- `arXiv:2609.26333` — Disaggregated Quantization: Specializing LLM Prefill and Decode / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-1932d6ac89ddfafb.json`
- `arXiv:2405.07135` — Post Training Quantization of Large Language Models with Microscaling Formats / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-47d3b689c2eeb296.json`
- `arXiv:2512.21835` — Collaborative Lossless LLM Inference Serving with Offloading-based Pipeline Parallelism on Edge Devices / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-5c9711465b85e7cf.json`
- `arXiv:2405.05803` — Boosting Multimodal Large Language Models with Visual Tokens Withdrawal for Rapid Inference / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-69af59c3cf5bef42.json`
- `arXiv:2607.29591` — ResKV: Reconstructing Omitted Attention Contributions for Fixed-Budget KV Cache Compression / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-72f5273058146903.json`
- `arXiv:2604.04599` — LP-GEMM: Integrating Layout Propagation into GEMM Operations / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-af50c1bfbbe9bbb6.json`
- `arXiv:2609.26763` — SARA: SLO-Aware Resource Allocation for Disaggregated Agentic LLM Services / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-b4703f709f94f0db.json`
- `arXiv:2606.19348` — DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence / worker `shared-preload-pool`
  - claim: **09-24 12:42:02 JST** / heartbeat: **09-24 19:25:42 JST** / lease expiry: **09-25 07:25:42 JST**
  - evidence: `.survey/work-queue/claims/job-research-b77896d0dca446fa.json`

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
| ready | **291** |

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
| inference/training/survey配下の論文Markdown実体 | **1023** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **252** |
| └ Research | **172** |
| └ Audit | **2** |
| └ Discovery | **51** |
| └ Other/Unknown | **27** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **338** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

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
- **構造化references探索状況**: STATUS生成時に `reference_pool.build_reference_pool()` を実行し、paper実体と無関係/微妙台帳から現在値を直接再計算します。過去のprecheck snapshotは件数表示に使いません。
- **日次メンテナンス**: `.survey/work-queue/maintenance-cycle.json` をmaintenance workflowの耐久正本として表示します。通常jobの件数からmaintenance状態を推定しません。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
