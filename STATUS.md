# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-25 06:43:49 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **299** |
| 未claim Research job | **155** |
| 直近24hの検証済みResearch収録 | **19** |
| 最終検証済みResearch収録 | **09-25 03:12:55 JST** |
| 最終検証済みDiscovery探索 | **09-25 01:09:26 JST** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **299** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **299** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6822** |
| 処理済み | **668** |
| 未処理 | **6154** |
| 収録済みとして除外 | **559** |
| 無関係として除外 | **49** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（22時間7分前）** |
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
| Research | **4** | **3** | **3** | **0** | **144** | **13** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **8** | **8** | **8** | **0** | **0** | **0** | **12** |
| 合計 | **12** | **11** | **11** | **0** | **144** | **13** | **12** |

- 最新Discovery runの耐久探索round: **8件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-25 03:12:55 JST** [research] `arXiv:2606.24033` — RoPE-Aware Bit Allocation for KV-Cache Quantization
  - job: `.survey/work-queue/jobs/job-research-ed39f178b202751f.json`
  - result: `.survey/work-queue/results/research/attempt-preload-d0b404e285d49a0ce5994e57.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-d0b404e285d49a0ce5994e57.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md`
- **09-25 03:07:25 JST** [research] `arXiv:2508.15487` — Dream 7B: Diffusion Large Language Models
  - job: `.survey/work-queue/jobs/job-research-1ba7917ba260cdda.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3a8d1487d30c19a489a3f0c1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3a8d1487d30c19a489a3f0c1.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2508.15487-dream-7b-diffusion-large-language-models.md`
- **09-25 03:07:25 JST** [research] `arXiv:2509.12211` — TinyServe: Query-Aware Cache Selection for Efficient LLM Serving
  - job: `.survey/work-queue/jobs/job-research-3d37c9d48dc78998.json`
  - result: `.survey/work-queue/results/research/attempt-preload-88865dce95348e7f779dacec.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-88865dce95348e7f779dacec.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2509.12211-tinyserve-query-aware-cache-selection.md`
- **09-25 00:46:34 JST** [research] `arXiv:2508.17137` — MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices
  - job: `.survey/work-queue/jobs/job-research-b22af651ef4f551f.json`
  - result: `.survey/work-queue/results/research/attempt-preload-5ae76716eb01958d78f1d488.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-5ae76716eb01958d78f1d488.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2508.17137-moe-beyond-learning-based-expert-activation-prediction-on-edge-devices.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-25 01:02:26 JST** job `job-04ed27eee57bc021` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T160030Z-scheduled-chat-00-7f3c9a-d01.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160030Z-scheduled-chat-00-7f3c9a-d01.json`
  - 探索軸: preload-backward-structured-references
- **09-25 01:02:36 JST** job `job-9d4d1882093158af` / 候補 **2件**
  - result: `.survey/work-queue/results/20260924T160110Z-scheduled-chat-00-7f3c9a-d02.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160110Z-scheduled-chat-00-7f3c9a-d02.json`
  - 探索軸: explicit user request: forward citations of foundational Adaptive Expert Computation / Compression seed arXiv:2202.09368 (Expert Choice Routing forward citations)
- **09-25 01:02:46 JST** job `job-502b7e14ff53de24` / 候補 **3件**
  - result: `.survey/work-queue/results/20260924T160130Z-scheduled-chat-00-7f3c9a-d03.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160130Z-scheduled-chat-00-7f3c9a-d03.json`
  - 探索軸: forward citations of Splitwise for disaggregated LLM serving
- **09-25 01:05:41 JST** job `job-cb948c38af6553c3` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T160430Z-scheduled-chat-00-7f3c9a-d04.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160430Z-scheduled-chat-00-7f3c9a-d04.json`
  - 探索軸: backward references of FlexGen offload and hierarchical-memory LLM inference
- **09-25 01:05:48 JST** job `job-9bd5c86cf0f0a7c8` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T160450Z-scheduled-chat-00-7f3c9a-d05.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160450Z-scheduled-chat-00-7f3c9a-d05.json`
  - 探索軸: forward citations of FlashAttention for recent attention kernels and serving systems
- **09-25 01:05:56 JST** job `job-52d06fffbd294759` / 候補 **2件**
  - result: `.survey/work-queue/results/20260924T160510Z-scheduled-chat-00-7f3c9a-d06.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160510Z-scheduled-chat-00-7f3c9a-d06.json`
  - 探索軸: explicit user request: forward citations of foundational Adaptive Expert Computation / Compression seed arXiv:2206.00277 (Task-Specific Expert Pruning forward citations)
- **09-25 01:09:16 JST** job `job-ea07283bf946a538` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T160720Z-scheduled-chat-00-7f3c9a-d07.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160720Z-scheduled-chat-00-7f3c9a-d07.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
- **09-25 01:09:26 JST** job `job-a5b5e5128745633f` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T160745Z-scheduled-chat-00-7f3c9a-d08.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T160745Z-scheduled-chat-00-7f3c9a-d08.json`
  - 探索軸: preload-backward-structured-references

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-25 02:55 JST** / worker `scheduled-chat-30`
- immutable submission: **3件** / 検証済み成功: **3件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- **成功** `arXiv:2508.15487` — Dream 7B: Diffusion Large Language Models
  - job: `.survey/work-queue/jobs/job-research-1ba7917ba260cdda.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3a8d1487d30c19a489a3f0c1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3a8d1487d30c19a489a3f0c1.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2508.15487-dream-7b-diffusion-large-language-models.md`
- **成功** `arXiv:2509.12211` — TinyServe: Query-Aware Cache Selection for Efficient LLM Serving
  - job: `.survey/work-queue/jobs/job-research-3d37c9d48dc78998.json`
  - result: `.survey/work-queue/results/research/attempt-preload-88865dce95348e7f779dacec.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-88865dce95348e7f779dacec.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2509.12211-tinyserve-query-aware-cache-selection.md`
- **成功** `arXiv:2606.24033` — RoPE-Aware Bit Allocation for KV-Cache Quantization
  - job: `.survey/work-queue/jobs/job-research-ed39f178b202751f.json`
  - result: `.survey/work-queue/results/research/attempt-preload-d0b404e285d49a0ce5994e57.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-d0b404e285d49a0ce5994e57.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.24033-rope-aware-bit-allocation-for-kv-cache-quantization.md`

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-25 02:55 JST** / worker `scheduled-chat-30`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-25 00:59 JST**
- 耐久探索round: **8件** / immutable submission: **8件** / 検証済み成功result: **8件** / 個別result照合: **8件** / 個別result未照合: **0件** / 候補: **12件**
- 探索軸: preload-backward-structured-references / explicit user request: forward citations of foundational Adaptive Expert Computation / Compression seed arXiv:2202.09368 (Expert Choice Routing forward citations) / forward citations of Splitwise for disaggregated LLM serving / backward references of FlexGen offload and hierarchical-memory LLM inference / forward citations of FlashAttention for recent attention kernels and serving systems / explicit user request: forward citations of foundational Adaptive Expert Computation / Compression seed arXiv:2206.00277 (Task-Specific Expert Pruning forward citations) / forward citations of DistServe disaggregated prefill-decode LLM serving
- round `disc-take-scheduled-chat-00-20260925T005925JST-b2a43c66` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260924T160030Z-scheduled-chat-00-7f3c9a-d01.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160030Z-scheduled-chat-00-7f3c9a-d01.json` (`ok=true`)
- round `frontier-ffb9f610716bbbb2820ec80c` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260924T160110Z-scheduled-chat-00-7f3c9a-d02.json`
  - 探索軸: explicit user request: forward citations of foundational Adaptive Expert Computation / Compression seed arXiv:2202.09368 (Expert Choice Routing forward citations)
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160110Z-scheduled-chat-00-7f3c9a-d02.json` (`ok=true`)
- round `frontier-6744df2bf719787d6187382f` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260924T160130Z-scheduled-chat-00-7f3c9a-d03.json`
  - 探索軸: forward citations of Splitwise for disaggregated LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160130Z-scheduled-chat-00-7f3c9a-d03.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-7f3c9a-d04` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260924T160430Z-scheduled-chat-00-7f3c9a-d04.json`
  - 探索軸: backward references of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160430Z-scheduled-chat-00-7f3c9a-d04.json` (`ok=true`)
- round `frontier-ed9ecfadedd08634da9254db` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260924T160450Z-scheduled-chat-00-7f3c9a-d05.json`
  - 探索軸: forward citations of FlashAttention for recent attention kernels and serving systems
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160450Z-scheduled-chat-00-7f3c9a-d05.json` (`ok=true`)
- round `frontier-33a41dbb7e0773c51f5ecd41` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260924T160510Z-scheduled-chat-00-7f3c9a-d06.json`
  - 探索軸: explicit user request: forward citations of foundational Adaptive Expert Computation / Compression seed arXiv:2206.00277 (Task-Specific Expert Pruning forward citations)
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160510Z-scheduled-chat-00-7f3c9a-d06.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-7f3c9a-d07` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260924T160720Z-scheduled-chat-00-7f3c9a-d07.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160720Z-scheduled-chat-00-7f3c9a-d07.json` (`ok=true`)
- round `frontier-58519fa41ceae293f0877761` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260924T160745Z-scheduled-chat-00-7f3c9a-d08.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/20260924T160745Z-scheduled-chat-00-7f3c9a-d08.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **144件** / 直近15分heartbeat: **13件**
- `arXiv:2211.10438` — SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-05c9fecf1a5510e9.json`
- `DOI:10.1109/cloud67622.2025.00028` — ZipNN: Lossless Compression for AI Models / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-14b72fcf4a8168cf.json`
- `arXiv:2511.12286` — Sangam: Chiplet-Based DRAM-PIM Accelerator with CXL Integration for LLM Inferencing / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-19ebd04771d99798.json`
- `arXiv:2609.21079` — DLB: Distributed Load Balancing at Scale for Generative AI Inference / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-207262571f4eb880.json`
- `DOI:10.1109/ISCAS66217.2026.11562764` — AdaCGen: Heterogeneity-Aware Layer Management for Efficient KV Cache Offloading in LLMs / worker `scheduled-chat-30`
  - claim: **09-25 06:31:05 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-2a1bde22bebd2f67.json`
- `OpenReview:02f3mUtqnM` — Hybrid LLM: Cost-Efficient and Quality-Aware Query Routing / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-35087281810758f2.json`
- `arXiv:2511.19480` — Exploiting the Experts: Unauthorized Compression in MoE-LLMs / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-372c7ba23950bd0c.json`
- `arXiv:2609.25405` — Efficient Iterative Retrieval with Heterogeneous Batching / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-396b5a1af9f8a040.json`
- `arXiv:2405.13019` — A Comprehensive Survey of Accelerated Generation Techniques in Large Language Models / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-82b8ef403de7a370.json`
- `arXiv:2607.24260` — KAP: Bridging the Knowledge Selection-Runtime Consumption Gap in LLM Systems / worker `scheduled-chat-30`
  - claim: **09-25 06:29:26 JST** / heartbeat: **09-25 06:31:05 JST** / lease expiry: **09-25 08:01:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-9c9df371bdbac091.json`

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
| ready | **299** |

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
| inference/training/survey配下の論文Markdown実体 | **1026** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **258** |
| └ Research | **178** |
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
