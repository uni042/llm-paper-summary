# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-20 19:15:06 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **95** |
| 未claim Research job | **94** |
| 直近24hの検証済みResearch収録 | **82** |
| 最終検証済みResearch収録 | **09-20 19:10:57 JST（4分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **95** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **95** |

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
| Research | **36** | **10** | **7** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **1** | **1** | **0** | **0** | **0** | **5** |
| 合計 | **36** | **11** | **8** | **0** | **1** | **0** | **5** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

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
- **09-20 18:45:26 JST** [research] `arXiv:2311.09431` — Striped Attention: Faster Ring Attention for Causal Transformers
  - job: `.survey/work-queue/jobs/job-research-8c68e144047ac9bb.json`
  - result: `.survey/work-queue/results/research/attempt-726aa6f9d7bb4140731a500b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-726aa6f9d7bb4140731a500b.json`
  - paper: `papers/training/03-pipeline-parallel-modular-training/2023-2311.09431-striped-attention.md`
- **09-20 18:41:27 JST** [research] `arXiv:2605.26297` — Agentic AI Workload Characteristics
  - job: `.survey/work-queue/jobs/job-research-b8f01545319d9604.json`
  - result: `.survey/work-queue/results/research/attempt-d9bfe22acbd9e709c4fcf1f8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d9bfe22acbd9e709c4fcf1f8.json`
  - paper: `papers/inference/12-benchmarking-modeling-emulation/2026-2605.26297-agentic-ai-workload-characteristics.md`
- **09-20 18:37:26 JST** [research] `arXiv:2310.07177` — Online Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-3cf2e0a916913e29.json`
  - result: `.survey/work-queue/results/research/attempt-3e00451f32958b311cdc3f3c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3e00451f32958b311cdc3f3c.json`
  - paper: `papers/inference/05-speculative-decoding/2023-2310.07177-online-speculative-decoding.md`
- **09-20 18:34:30 JST** [research] `DOI:10.18653/v1/2026.findings-acl.558` — DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning
  - job: `.survey/work-queue/jobs/job-research-529f8795f6dde556.json`
  - result: `.survey/work-queue/results/research/attempt-130c102f178d2a82b4f2f771.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-130c102f178d2a82b4f2f771.json`
  - paper: `papers/inference/10-sparse-attention/2026-delta.md`
- **09-20 18:33:09 JST** [research] `DOI:10.18653/v1/2025.naacl-long.601` — Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion
  - job: `.survey/work-queue/jobs/job-research-7975c226ad04d80a.json`
  - result: `.survey/work-queue/results/research/attempt-da2aebbde976d20453f0ceeb.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-da2aebbde976d20453f0ceeb.json`
  - paper: `papers/inference/05-speculative-decoding/2025-speculative-diffusion-decoding.md`
- **09-20 18:11:14 JST** [research] `DOI:10.18653/v1/2026.acl-long.1683` — LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning
  - job: `.survey/work-queue/jobs/job-research-59739220ff5250cc.json`
  - result: `.survey/work-queue/results/research/attempt-018be4cd03a3fdd526c3cb8e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-018be4cd03a3fdd526c3cb8e.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2026-lazyeviction.md`
- **09-20 18:06:15 JST** [research] `arXiv:2405.12981` — Reducing Transformer Key-Value Cache Size with Cross-Layer Attention
  - job: `.survey/work-queue/jobs/job-research-ab19fa17920fb404.json`
  - result: `.survey/work-queue/results/research/attempt-09fd18d9c803c17379a43783.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-09fd18d9c803c17379a43783.json`
  - paper: `papers/inference/06-kv-cache-memory/2024-2405.12981-cross-layer-attention.md`
- **09-20 18:05:23 JST** [research] `arXiv:2502.07903` — HexGen-2: Disaggregated Generative Inference of LLMs in Heterogeneous Environment
  - job: `.survey/work-queue/jobs/job-research-da8147ed3835966f.json`
  - result: `.survey/work-queue/results/research/attempt-5605d7717d39930ab2f4dcc5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5605d7717d39930ab2f4dcc5.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2502.07903-hexgen-2.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-20 18:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **10件** / 検証済み成功: **7件** / result照合済み非成功: **3件** / 個別result未照合: **0件**
- **成功** `DOI:10.18653/v1/2026.findings-acl.558` — DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning
  - job: `.survey/work-queue/jobs/job-research-529f8795f6dde556.json`
  - result: `.survey/work-queue/results/research/attempt-130c102f178d2a82b4f2f771.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-130c102f178d2a82b4f2f771.json`
  - paper: `papers/inference/10-sparse-attention/2026-delta.md`
- **成功** `arXiv:2310.07177` — Online Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-3cf2e0a916913e29.json`
  - result: `.survey/work-queue/results/research/attempt-3e00451f32958b311cdc3f3c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3e00451f32958b311cdc3f3c.json`
  - paper: `papers/inference/05-speculative-decoding/2023-2310.07177-online-speculative-decoding.md`
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-6d7a6414e2062e2233d5009c.json` (job `job-research-2b2648af1ffd1107`, failure_class `content_validation`)
  - result: `.survey/work-queue/results/research/attempt-6d7a6414e2062e2233d5009c.json` (`ok=false`)
- **成功** `arXiv:2311.09431` — Striped Attention: Faster Ring Attention for Causal Transformers
  - job: `.survey/work-queue/jobs/job-research-8c68e144047ac9bb.json`
  - result: `.survey/work-queue/results/research/attempt-726aa6f9d7bb4140731a500b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-726aa6f9d7bb4140731a500b.json`
  - paper: `papers/training/03-pipeline-parallel-modular-training/2023-2311.09431-striped-attention.md`
- **成功** `arXiv:2608.06989` — Rethinking Unified Memory for NPU-PIM Systems: Dual-View Memory for Dynamic Inference of LLM
  - job: `.survey/work-queue/jobs/job-research-2e7cd1c4e1dc851d.json`
  - result: `.survey/work-queue/results/research/attempt-ade4ad902d6f7670ee635b88.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ade4ad902d6f7670ee635b88.json`
  - paper: `papers/inference/05-memory-architecture-near-data/2026-2608.06989-dual-view-memory-npu-pim.md`
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-bb698348ca635e022360ff70.json` (job `job-research-c0742ec707ffbbe8`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-bb698348ca635e022360ff70.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-d6d0f050a2bc6af8b178330b.json` (job `job-research-d5278ec0af97bd4e`, failure_class `state_or_transport_guard`)
  - result: `.survey/work-queue/results/research/attempt-d6d0f050a2bc6af8b178330b.json` (`ok=false`)
- **成功** `arXiv:2605.26297` — Agentic AI Workload Characteristics
  - job: `.survey/work-queue/jobs/job-research-b8f01545319d9604.json`
  - result: `.survey/work-queue/results/research/attempt-d9bfe22acbd9e709c4fcf1f8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d9bfe22acbd9e709c4fcf1f8.json`
  - paper: `papers/inference/12-benchmarking-modeling-emulation/2026-2605.26297-agentic-ai-workload-characteristics.md`
- **成功** `DOI:10.18653/v1/2025.naacl-long.601` — Speculative Diffusion Decoding: Accelerating Language Generation through Diffusion
  - job: `.survey/work-queue/jobs/job-research-7975c226ad04d80a.json`
  - result: `.survey/work-queue/results/research/attempt-da2aebbde976d20453f0ceeb.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-da2aebbde976d20453f0ceeb.json`
  - paper: `papers/inference/05-speculative-decoding/2025-speculative-diffusion-decoding.md`
- **成功** `DOI:10.18653/v1/2026.acl-long.1811` — REAL: REtrieval-reAsoning and Logic-constructed Attention Behaviors for Long-Context KV Cache Compression
  - job: `.survey/work-queue/jobs/job-research-765eee68b506c6ff.json`
  - result: `.survey/work-queue/results/research/attempt-eda6a759c3d074c07a647fb0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-eda6a759c3d074c07a647fb0.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2026-real-kv.md`

#### Audit (:30)

- 最新観測run: **2026-09-20 18:30 JST** / worker `scheduled-chat-llm-survey`
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
- `arXiv:2605.18810` — D-PACE: Dynamic Position-Aware Cross-Entropy for Parallel Speculative Drafting / worker `scheduled-chat-llm-survey`
  - claim: **09-20 19:11:38 JST** / heartbeat: **—** / lease expiry: **09-20 20:41:38 JST**
  - evidence: `.survey/work-queue/claims/job-research-2b2648af1ffd1107.json`

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
| ready | **95** |

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
| inference/training/survey配下の論文Markdown実体 | **845** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **764** |
| └ Research | **578** |
| └ Audit | **2** |
| └ Discovery | **145** |
| └ Other/Unknown | **39** |

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
