# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 11:06:59 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **50** |
| 未claim Research job | **48** |
| 直近24hの検証済みResearch収録 | **42** |
| 最終検証済みResearch収録 | **09-19 07:25:37 JST（3時間41分前）** |
| 整合性異常 | **0** |

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
| Research | **10** | **15** | **6** | **9** | **2** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **3** | **3** | **3** | **0** | **0** | **0** | **3** |
| 合計 | **13** | **18** | **9** | **9** | **2** | **0** | **3** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-19 07:25:37 JST** [research] `arXiv:2402.15678` — Minions: Accelerating Large Language Model Inference with Aggregated Speculative Execution
  - job: `.survey/work-queue/jobs/job-research-b3f94863f38e0308.json`
  - result: `.survey/work-queue/results/research/attempt-89e2edf847dd8923a0885b8e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-89e2edf847dd8923a0885b8e.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2402.15678-minions-accelerating-large-language-model-inference-with-aggregated-speculative-execution.md`
- **09-19 07:20:25 JST** [research] `arXiv:2503.08467` — Accelerating MoE Model Inference with Expert Sharding
  - job: `.survey/work-queue/jobs/job-research-b3520b6ffb18fc43.json`
  - result: `.survey/work-queue/results/research/attempt-59bd34d06f011611b0132598.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-59bd34d06f011611b0132598.json`
  - paper: `papers/inference/05-moe-expert-offload/2025-2503.08467-moe-expert-sharding.md`
- **09-19 07:15:47 JST** [research] `arXiv:2609.15504` — How Lossless Is Lossless Speculative Decoding? The Role of Numerical Precision in Orthrus
  - job: `.survey/work-queue/jobs/job-research-9c0ef4e091be369c.json`
  - result: `.survey/work-queue/results/research/attempt-c2a51a6ace4a43448c42f0b1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c2a51a6ace4a43448c42f0b1.json`
  - paper: `papers/inference/08-speculative-decoding/2026-2609.15504-orthrus-numerical-precision-losslessness.md`
- **09-19 07:13:34 JST** [research] `arXiv:2607.16339` — LaCache: Exact Caching and Precision-Adaptive Inference for Diffusion Large Language Models
  - job: `.survey/work-queue/jobs/job-research-3001166a9d479500.json`
  - result: `.survey/work-queue/results/research/attempt-8a84e34f15c4ef8ffd049438.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8a84e34f15c4ef8ffd049438.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2607.16339-lacache-exact-caching-precision-adaptive-dllm.md`
- **09-19 07:11:49 JST** [research] `arXiv:2607.08993` — StreamDQ: Near-Memory Weight DeQuantization in Custom HBM for Scalable AI Inference Acceleration
  - job: `.survey/work-queue/jobs/job-research-f7dcdf40e7d3538f.json`
  - result: `.survey/work-queue/results/research/attempt-a3bba0a36c53f4970b6d1719.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a3bba0a36c53f4970b6d1719.json`
  - paper: `papers/inference/05-pim-near-memory/2026-2607.08993-streamdq-near-memory-weight-dequantization-custom-hbm.md`
- **09-19 07:07:34 JST** [research] `arXiv:2603.28018` — Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill
  - job: `.survey/work-queue/jobs/job-research-56fbeb640bc1560d.json`
  - result: `.survey/work-queue/results/research/attempt-85e31171313f0f31636868a0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-85e31171313f0f31636868a0.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md`
- **09-19 05:35:57 JST** [research] `arXiv:2508.08457` — Architecting Long-Context LLM Acceleration with Packing-Prefetch Scheduler and Ultra-Large Capacity On-Chip Memories
  - job: `.survey/work-queue/jobs/job-research-be1193ba1dd42ac7.json`
  - result: `.survey/work-queue/results/research/attempt-b1510ac72994dff0cbb0df8f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b1510ac72994dff0cbb0df8f.json`
  - paper: `papers/inference/03-hierarchical-memory/2025-2508.08457-packing-prefetch-onchip-memory-long-context.md`
- **09-19 05:23:55 JST** [research] `arXiv:2607.17538` — D-NOVA: In-Storage Retrieval Accelerator via Dual-Bound 3D NAND-Optimized Similarity Search with Vector Adaptation
  - job: `.survey/work-queue/jobs/job-research-b2d29fa9c529bdfd.json`
  - result: `.survey/work-queue/results/research/attempt-49a5f136c96efe1a74ef7842.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-49a5f136c96efe1a74ef7842.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2607.17538-d-nova-in-storage-retrieval-accelerator-via-dual-bound-3d-nand-optimized-similarity-search-with-vector-adaptation.md`
- **09-19 05:21:03 JST** [research] `arXiv:2603.09216` — PIM-SHERPA: Software Method for On-device LLM Inference by Resolving PIM Memory Attribute and Layout Inconsistencies
  - job: `.survey/work-queue/jobs/job-research-b3afe97f03f9606a.json`
  - result: `.survey/work-queue/results/research/attempt-478619d2b2eab68cb5a0f0d3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-478619d2b2eab68cb5a0f0d3.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2603.09216-pim-sherpa-software-method-for-on-device-llm-inference-by-resolving-pim-memory-attribute-and-layout-inconsistencies.md`
- **09-19 05:15:47 JST** [research] `arXiv:2605.23294` — NASiC: 3D NAND-based CAM-Selected Multibit CIM Architecture for Efficient On-Device Mixture-of-Experts LLM Inference
  - job: `.survey/work-queue/jobs/job-research-8de660021e1eaf46.json`
  - result: `.survey/work-queue/results/research/attempt-2c5886028263df416e6db1bd.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2c5886028263df416e6db1bd.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.23294-nasic-3d-nand-based-cam-selected-multibit-cim-architecture-for-efficient-on-device-mixture-of-experts-llm-inference.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-19 06:02:20 JST** job `job-fc0b32f4684c9e75` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0600JST-discovery-specialist-edge-offload-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0600JST-discovery-specialist-edge-offload-3.json`
  - 探索軸: device-edge-cloud multi-tier serving・recursive offloading・network-aware inference
- **09-19 06:02:30 JST** job `job-8b03115ae2cdf87d` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0600JST-discovery-specialist-heterogeneous-hardware-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0600JST-discovery-specialist-heterogeneous-hardware-2.json`
  - 探索軸: heterogeneous inference hardware・FPGA memory-based compute・near-memory architecture
- **09-19 06:01:55 JST** job `job-d209a14a1856b2db` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0600JST-discovery-specialist-programmable-serving-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0600JST-discovery-specialist-programmable-serving-1.json`
  - 探索軸: programmable serving・agentic runtime・application-specific generation loop

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 07:00 JST** / worker `scheduled-chat-discovery-20260919T0700JST`
- immutable submission: **15件** / 検証済み成功: **6件** / 未完了・未検証: **9件**
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-01bc2c1e0ef21dcae1e71886.json` (job `job-research-7b5d4afbd3eabe62`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-11b5e62465ce56e739adae95.json` (job `job-research-c790156bc5f9f1f9`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-55ad2e2507991e421d05d6e8.json` (job `job-research-b3f94863f38e0308`)
- **成功** `arXiv:2503.08467` — Accelerating MoE Model Inference with Expert Sharding
  - job: `.survey/work-queue/jobs/job-research-b3520b6ffb18fc43.json`
  - result: `.survey/work-queue/results/research/attempt-59bd34d06f011611b0132598.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-59bd34d06f011611b0132598.json`
  - paper: `papers/inference/05-moe-expert-offload/2025-2503.08467-moe-expert-sharding.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-5adb86bd27e2666265386057.json` (job `job-research-56fbeb640bc1560d`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-792a11fa4fd24a27f2b17f5c.json` (job `job-research-b3520b6ffb18fc43`)
- **成功** `arXiv:2603.28018` — Low-Latency Edge LLM Handover via Joint KV Cache Transfer and Token Prefill
  - job: `.survey/work-queue/jobs/job-research-56fbeb640bc1560d.json`
  - result: `.survey/work-queue/results/research/attempt-85e31171313f0f31636868a0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-85e31171313f0f31636868a0.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2603.28018-edge-llm-handover-kv-transfer-prefill.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-894fefc24cb4ea7b63f3faa6.json` (job `job-research-7623de796f4f2b46`)
- **成功** `arXiv:2402.15678` — Minions: Accelerating Large Language Model Inference with Aggregated Speculative Execution
  - job: `.survey/work-queue/jobs/job-research-b3f94863f38e0308.json`
  - result: `.survey/work-queue/results/research/attempt-89e2edf847dd8923a0885b8e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-89e2edf847dd8923a0885b8e.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2402.15678-minions-accelerating-large-language-model-inference-with-aggregated-speculative-execution.md`
- **成功** `arXiv:2607.16339` — LaCache: Exact Caching and Precision-Adaptive Inference for Diffusion Large Language Models
  - job: `.survey/work-queue/jobs/job-research-3001166a9d479500.json`
  - result: `.survey/work-queue/results/research/attempt-8a84e34f15c4ef8ffd049438.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8a84e34f15c4ef8ffd049438.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2607.16339-lacache-exact-caching-precision-adaptive-dllm.md`

#### Audit (:30)

- 最新観測run: **2026-09-19 07:00 JST** / worker `scheduled-chat-discovery-20260919T0700JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-19 06:00 JST**
- 耐久探索round: **3件** / immutable submission: **3件** / 検証済み成功result: **3件** / 個別result照合: **3件** / 個別result未照合: **0件** / 候補: **3件**
- 探索軸: device-edge-cloud multi-tier serving・recursive offloading・network-aware inference / heterogeneous inference hardware・FPGA memory-based compute・near-memory architecture / programmable serving・agentic runtime・application-specific generation loop
- round `specialist-edge-offload-3` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T0600JST-discovery-specialist-edge-offload-3.json`
  - 探索軸: device-edge-cloud multi-tier serving・recursive offloading・network-aware inference
  - 個別result照合: あり / `.survey/work-queue/results/20260919T0600JST-discovery-specialist-edge-offload-3.json` (`ok=true`)
- round `specialist-heterogeneous-hardware-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T0600JST-discovery-specialist-heterogeneous-hardware-2.json`
  - 探索軸: heterogeneous inference hardware・FPGA memory-based compute・near-memory architecture
  - 個別result照合: あり / `.survey/work-queue/results/20260919T0600JST-discovery-specialist-heterogeneous-hardware-2.json` (`ok=true`)
- round `specialist-programmable-serving-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T0600JST-discovery-specialist-programmable-serving-1.json`
  - 探索軸: programmable serving・agentic runtime・application-specific generation loop
  - 個別result照合: あり / `.survey/work-queue/results/20260919T0600JST-discovery-specialist-programmable-serving-1.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **2件** / 直近15分heartbeat: **0件**
- `DOI:10.1109/HPCA68181.2026.11408460` — Towards Compute-Aware In-Switch Computing for LLMs Tensor-Parallelism on Multi-GPU Systems / worker `scheduled-chat-discovery-specialist`
  - claim: **09-19 11:04:29 JST** / heartbeat: **—** / lease expiry: **09-19 12:34:29 JST**
  - evidence: `.survey/work-queue/claims/job-research-e8f755e1fee9cc18.json`
- `arXiv:2510.24051` — Pie: A Programmable Serving System for Emerging LLM Applications / worker `scheduled-chat-llm-survey`
  - claim: **09-19 06:36:03 JST** / heartbeat: **09-19 10:29:05 JST** / lease expiry: **09-19 11:59:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-c2f58815c322fab7.json`

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
| inference/training/survey配下の論文Markdown実体 | **745** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **580** |
| └ Research | **451** |
| └ Audit | **2** |
| └ Discovery | **127** |

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
