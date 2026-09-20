# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-20 20:43:43 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **187** |
| 未claim Research job | **186** |
| 直近24hの検証済みResearch収録 | **88** |
| 最終検証済みResearch収録 | **09-20 20:43:09 JST（34秒前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **187** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **187** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **5380** |
| 処理済み | **527** |
| 未処理 | **4853** |
| 収録済みとして除外 | **419** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- 探索時にpaper実体と無関係/微妙台帳から再計算した値を、schema-v3 precheck resultへ耐久保存して表示します。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **39** | **3** | **2** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **1** | **1** | **0** | **0** | **0** | **5** |
| 合計 | **39** | **4** | **3** | **0** | **1** | **0** | **5** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-20 20:43:09 JST** [research] `arXiv:2606.09886` — SHAPE: Coalition-Aware Expert Pruning for Sparse Mixture-of-Experts LLMs
  - job: `.survey/work-queue/jobs/job-research-6e63ee697d71f91d.json`
  - result: `.survey/work-queue/results/research/attempt-5a4b45332ca9b9f0a0bd90d0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5a4b45332ca9b9f0a0bd90d0.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2606.09886-shape-coalition-aware-expert-pruning.md`
- **09-20 20:36:19 JST** [research] `arXiv:2603.11535` — Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing
  - job: `.survey/work-queue/jobs/job-research-b0f3ab31cdfd9a01.json`
  - result: `.survey/work-queue/results/research/attempt-3abd5ab214b6f2e829c399c9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3abd5ab214b6f2e829c399c9.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2603.11535-expert-threshold-routing.md`
- **09-20 20:22:32 JST** [research] `arXiv:2509.23012` — MoE-PHDS: One MoE checkpoint for flexible runtime sparsity
  - job: `.survey/work-queue/jobs/job-research-95a4661f225665ff.json`
  - result: `.survey/work-queue/results/research/attempt-6b53b1926ec03fe03eb46c7c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6b53b1926ec03fe03eb46c7c.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2509.23012-moe-phds-flexible-runtime-sparsity.md`
- **09-20 20:19:14 JST** [research] `arXiv:2511.02237` — Opportunistic Expert Activation: Batch-Aware Expert Routing for Faster Decode Without Retraining
  - job: `.survey/work-queue/jobs/job-research-67ddaa9ed58fd85b.json`
  - result: `.survey/work-queue/results/research/attempt-bd7edc3a59e4ce43ac25f884.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bd7edc3a59e4ce43ac25f884.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2511.02237-opportunistic-expert-activation.md`
- **09-20 20:14:15 JST** [research] `arXiv:2510.19366` — MoE-Prism: Disentangling Monolithic Experts for Elastic MoE Services via Model-System Co-Designs
  - job: `.survey/work-queue/jobs/job-research-5ce9880c62119377.json`
  - result: `.survey/work-queue/results/research/attempt-1487e2feb0d7ced553b8414c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1487e2feb0d7ced553b8414c.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2510.19366-moe-prism-elastic-services.md`
- **09-20 20:08:22 JST** [research] `arXiv:2608.10392` — Share First, Route What Remains: A Unified Framework for Token-Adaptive MoE Computation
  - job: `.survey/work-queue/jobs/job-research-08b5458cb63307f5.json`
  - result: `.survey/work-queue/results/research/attempt-ae173bcae95c3292b53fd3a9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ae173bcae95c3292b53fd3a9.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2608.10392-share-first-route-what-remains.md`
- **09-20 19:20:46 JST** [research] `arXiv:2407.00326` — Teola: Towards End-to-End Optimization of LLM-based Applications
  - job: `.survey/work-queue/jobs/job-research-6778a26f7c6381c5.json`
  - result: `.survey/work-queue/results/research/attempt-0035fe851a4c5bf25fbbacc2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0035fe851a4c5bf25fbbacc2.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2407.00326-teola.md`
- **09-20 19:16:54 JST** [research] `arXiv:2605.18810` — D-PACE: Dynamic Position-Aware Cross-Entropy for Parallel Speculative Drafting
  - job: `.survey/work-queue/jobs/job-research-2b2648af1ffd1107.json`
  - result: `.survey/work-queue/results/research/attempt-682f2ca2eca58d18d9e46ca8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-682f2ca2eca58d18d9e46ca8.json`
  - paper: `papers/inference/06-speculative-decoding/2026-2605.18810-d-pace.md`
- **09-20 19:10:57 JST** [research] `arXiv:2608.06989` — Rethinking Unified Memory for NPU-PIM Systems: Dual-View Memory for Dynamic Inference of LLM
  - job: `.survey/work-queue/jobs/job-research-2e7cd1c4e1dc851d.json`
  - result: `.survey/work-queue/results/research/attempt-ade4ad902d6f7670ee635b88.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ade4ad902d6f7670ee635b88.json`
  - paper: `papers/inference/05-memory-architecture-near-data/2026-2608.06989-dual-view-memory-npu-pim.md`
- **09-20 19:05:05 JST** [research] `DOI:10.18653/v1/2026.acl-long.1811` — REAL: REtrieval-reAsoning and Logic-constructed Attention Behaviors for Long-Context KV Cache Compression
  - job: `.survey/work-queue/jobs/job-research-765eee68b506c6ff.json`
  - result: `.survey/work-queue/results/research/attempt-eda6a759c3d074c07a647fb0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-eda6a759c3d074c07a647fb0.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2026-real-kv.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-20 20:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **3件** / 検証済み成功: **2件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **成功** `arXiv:2603.11535` — Expert Threshold Routing for Autoregressive Language Modeling with Dynamic Computation Allocation and Load Balancing
  - job: `.survey/work-queue/jobs/job-research-b0f3ab31cdfd9a01.json`
  - result: `.survey/work-queue/results/research/attempt-3abd5ab214b6f2e829c399c9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3abd5ab214b6f2e829c399c9.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2603.11535-expert-threshold-routing.md`
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-3bfbd9f2b2c22f927f203849.json` (job `job-research-92c83b7c2ec8a78f`, failure_class `content_validation`)
  - result: `.survey/work-queue/results/research/attempt-3bfbd9f2b2c22f927f203849.json` (`ok=false`)
- **成功** `arXiv:2606.09886` — SHAPE: Coalition-Aware Expert Pruning for Sparse Mixture-of-Experts LLMs
  - job: `.survey/work-queue/jobs/job-research-6e63ee697d71f91d.json`
  - result: `.survey/work-queue/results/research/attempt-5a4b45332ca9b9f0a0bd90d0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5a4b45332ca9b9f0a0bd90d0.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2606.09886-shape-coalition-aware-expert-pruning.md`

#### Audit (:30)

- 最新観測run: **2026-09-20 20:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-20 01:58 JST**
- 耐久探索round: **1件** / immutable submission: **1件** / 検証済み成功result: **1件** / 個別result照合: **1件** / 個別result未照合: **0件** / 候補: **5件**
- 探索軸: MoE expert cache offload placement prefetch inference systems
- round `specialist-moe-offload-openalex-02` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260920T0204JST-specialist-moe-openalex-round1.json`
  - 探索軸: MoE expert cache offload placement prefetch inference systems
  - 個別result照合: あり / `.survey/work-queue/results/20260920T0204JST-specialist-moe-openalex-round1.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2607.06601` — TriRoute: Unified Learned Routing for Joint Adaptive Attention, Experts, and KV-Cache Allocation / worker `scheduled-chat-llm-survey`
  - claim: **09-20 20:43:36 JST** / heartbeat: **—** / lease expiry: **09-20 22:13:36 JST**
  - evidence: `.survey/work-queue/claims/job-research-0f282c93dba72c85.json`

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
| ready | **187** |

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
| inference/training/survey配下の論文Markdown実体 | **853** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **811** |
| └ Research | **590** |
| └ Audit | **2** |
| └ Discovery | **145** |
| └ Other/Unknown | **74** |

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
- **構造化references探索状況**: schema-v3 repository-reference precheck resultに耐久保存されたprovider進捗を表示します。値自体は探索時にpaper実体と無関係/微妙台帳から再計算されます。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
