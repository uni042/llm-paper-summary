# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-24 15:38:04 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **287** |
| 未claim Research job | **144** |
| 直近24hの検証済みResearch収録 | **25** |
| 最終検証済みResearch収録 | **09-24 15:37:58 JST（6秒前）** |
| 整合性異常 | **22** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **287** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **287** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6751** |
| 処理済み | **658** |
| 未処理 | **6093** |
| 収録済みとして除外 | **550** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.7%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（7時間2分前）** |
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
| Research | **6** | **2** | **0** | **0** | **143** | **60** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **6** | **5** | **0** | **3** | **143** | **60** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-24 15:37:58 JST** [research] `arXiv:2312.00752` — Mamba: Linear-Time Sequence Modeling with Selective State Spaces
  - job: `.survey/work-queue/jobs/job-research-7526ab28b3c65fc4.json`
  - result: `.survey/work-queue/results/research/attempt-preload-270cf0686ddf08989a01feb5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-270cf0686ddf08989a01feb5.json`
  - paper: `papers/inference/99-other-inference-systems/2023-2312.00752-mamba-selective-state-space-linear-time-inference.md`
- **09-24 13:39:58 JST** [research] `arXiv:2601.08833` — Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications
  - job: `.survey/work-queue/jobs/job-research-0023a21511f803e1.json`
  - result: `.survey/work-queue/results/research/attempt-preload-54435f3f1e70e6def8dfca02.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-54435f3f1e70e6def8dfca02.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md`
- **09-24 13:37:49 JST** [research] `arXiv:2511.01633` — Scaling Graph Chain-of-Thought Reasoning: A Multi-Agent Framework with Efficient LLM Serving
  - job: `.survey/work-queue/jobs/job-research-2a8c8a978e102c67.json`
  - result: `.survey/work-queue/results/research/attempt-preload-38c87a832a14fb80d3b5b6c4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-38c87a832a14fb80d3b5b6c4.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2511.01633-graph-cot-multi-agent-efficient-serving.md`
- **09-24 13:35:46 JST** [research] `arXiv:1904.10509` — Generating Long Sequences with Sparse Transformers
  - job: `.survey/work-queue/jobs/job-research-e642f12f51409df8.json`
  - result: `.survey/work-queue/results/research/attempt-preload-1f8a910c2a57d30ce56d66d0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-1f8a910c2a57d30ce56d66d0.json`
  - paper: `papers/inference/99-other-inference-systems/2019-1904.10509-generating-long-sequences-with-sparse-transformers.md`
- **09-24 09:40:07 JST** [research] `arXiv:2406.02069` — PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling
  - job: `.survey/work-queue/jobs/job-research-86d74401d2a482f5.json`
  - result: `.survey/work-queue/results/research/attempt-preload-a27038f725a3ac141db139f4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-a27038f725a3ac141db139f4.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2024-2406.02069-pyramidkv.md`
- **09-24 09:40:07 JST** [research] `arXiv:2310.01801` — Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs
  - job: `.survey/work-queue/jobs/job-research-77f5ab6e591a0176.json`
  - result: `.survey/work-queue/results/research/attempt-preload-b1e41ea993ce770bb187a178.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-b1e41ea993ce770bb187a178.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2023-2310.01801-fastgen.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-24 10:00 JST** / worker `scheduled-chat-00`
- immutable submission: **2件** / 検証済み成功: **0件** / result照合済み非成功: **2件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-27b9e5c41397f9408cf69d15.json` (job `job-research-311ed15d31d6fcf9`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-27b9e5c41397f9408cf69d15.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-69fc030bb35ffc867b98539b.json` (job `job-research-0058e5cacea33a16`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-69fc030bb35ffc867b98539b.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-24 10:00 JST** / worker `scheduled-chat-00`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-21 05:58 JST**
- 耐久探索round: **3件** / immutable submission: **3件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **3件** / 候補: **6件**
- 探索軸: repository-wide structured references for LLM inference systems / forward citations of Elastic MoE for inference-time expert scaling / forward citations of MoE-Infinity offloading-efficient MoE serving
- round `hourly00-backward-01` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/discovery/2026-09-21T05-58-48+09-00-hourly00-backward-01.json`
  - 探索軸: repository-wide structured references for LLM inference systems
  - 個別result照合: なし（immutable round記録は確認済み）
- round `hourly00-forward-elasticmoe-02` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/discovery/2026-09-21T05-58-48+09-00-hourly00-forward-elasticmoe-02.json`
  - 探索軸: forward citations of Elastic MoE for inference-time expert scaling
  - 個別result照合: なし（immutable round記録は確認済み）
- round `hourly00-forward-moeinfinity-03` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/2026-09-21T05-58-48+09-00-hourly00-forward-moeinfinity-03.json`
  - 探索軸: forward citations of MoE-Infinity offloading-efficient MoE serving
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **143件** / 直近15分heartbeat: **60件**
- `DOI:10.1109/INFOCOM59046.2026.11571463` — BROS: Efficient LLM Serving on Hybrid Real-time and Best-effort Requests / worker `shared-preload-pool`
  - claim: **09-24 09:23:03 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-042e5712bf1b426e.json`
- `arXiv:2609.04724` — FlexPosit: Tunable Fractional Precision for LLM Inference Accelerators / worker `shared-preload-pool`
  - claim: **09-24 15:33:22 JST** / heartbeat: **—** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-04cf5cb095abe08f.json`
- `DOI:10.1109/INFOCOM59046.2026.11571388` — CoSine: Enhancing LLM Serving via Collaborative and Decoupled Speculative Inference / worker `shared-preload-pool`
  - claim: **09-24 09:23:03 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-058d69df18b4e613.json`
- `arXiv:2604.16400` — CoLLM: Continuous Adaptation for SLO-Aware LLM Serving on Shared GPU Clusters / worker `shared-preload-pool`
  - claim: **09-23 23:59:50 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-0a2c1791c2461b69.json`
- `arXiv:2606.17081` — The Price of Anarchy in Disaggregated Inference / worker `shared-preload-pool`
  - claim: **09-24 01:27:03 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-0a4a1c707b0687af.json`
- `arXiv:2403.01876` — DéjàVu: KV-cache Streaming for Fast, Fault-tolerant Generative LLM Serving / worker `shared-preload-pool`
  - claim: **09-24 15:33:22 JST** / heartbeat: **—** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-0dbe9070b5598362.json`
- `arXiv:2603.09023` — The Missing Memory Hierarchy: Demand Paging for LLM Context Windows / worker `shared-preload-pool`
  - claim: **09-23 23:59:50 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-105b69444b4fa0ad.json`
- `arXiv:2607.16248` — High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration / worker `shared-preload-pool`
  - claim: **09-24 01:27:03 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-11098a1512c29cb4.json`
- `arXiv:2609.17940` — Beyond the Previous Layer: Residual Predictive Structure in Sparse MoE Routing / worker `shared-preload-pool`
  - claim: **09-23 23:59:50 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-18c00b2ae272f206.json`
- `arXiv:2508.15487` — Dream 7B: Diffusion Large Language Models / worker `shared-preload-pool`
  - claim: **09-23 23:59:50 JST** / heartbeat: **09-24 15:33:22 JST** / lease expiry: **09-25 03:33:22 JST**
  - evidence: `.survey/work-queue/claims/job-research-1ba7917ba260cdda.json`

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
| ready | **287** |

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
| inference/training/survey配下の論文Markdown実体 | **1013** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **304** |
| └ Research | **168** |
| └ Audit | **2** |
| └ Discovery | **72** |
| └ Other/Unknown | **62** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **338** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

| 検出項目 | 件数 |
|---|---:|
| completed Research jobで指定paper実体なし | **22** |
| 対応jobなしsubmission（有効Discovery round除外） | **0** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **22** |

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
