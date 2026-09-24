# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-24 10:02:29 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **291** |
| 未claim Research job | **148** |
| 直近24hの検証済みResearch収録 | **42** |
| 最終検証済みResearch収録 | **09-24 09:51:56 JST（10分前）** |
| 整合性異常 | **1** |

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
| 構造化references総候補 | **6712** |
| 処理済み | **657** |
| 未処理 | **6055** |
| 収録済みとして除外 | **549** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（1時間26分前）** |
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
| Research | **6** | **1** | **0** | **0** | **143** | **21** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **6** | **4** | **0** | **3** | **143** | **21** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-24 09:51:56 JST** [research] `arXiv:2502.13189` — MoBA: Mixture of Block Attention for Long-Context LLMs
  - job: `.survey/work-queue/jobs/job-research-09d154c9daf0b638.json`
  - result: `.survey/work-queue/results/research/attempt-preload-f2bb13bd5d0d331fc95b5bd6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-f2bb13bd5d0d331fc95b5bd6.json`
  - paper: `papers/inference/10-sparse-attention/2025-2502.13189-moba.md`
- **09-24 09:45:14 JST** [research] `arXiv:2410.01035` — Don't Stop Me Now: Embedding Based Scheduling for LLMs
  - job: `.survey/work-queue/jobs/job-research-97b59f2c42d3b70d.json`
  - result: `.survey/work-queue/results/research/attempt-preload-4b68202feb39838866eccea9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-4b68202feb39838866eccea9.json`
  - paper: `papers/inference/06-serving-scheduling/2024-2410.01035-embedding-based-scheduling.md`
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
- **09-24 09:35:54 JST** [research] `arXiv:2210.17323` — GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers
  - job: `.survey/work-queue/jobs/job-research-a725ebe4f1dc359c.json`
  - result: `.survey/work-queue/results/research/attempt-preload-27067e88f7585964ab37f6a5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-27067e88f7585964ab37f6a5.json`
  - paper: `papers/inference/08-quantization-kernels/2022-2210.17323-gptq.md`
- **09-24 09:35:54 JST** [research] `arXiv:2404.08509` — Efficient Interactive LLM Serving with Proxy Model-based Sequence Length Prediction
  - job: `.survey/work-queue/jobs/job-research-c4dbc458851f604c.json`
  - result: `.survey/work-queue/results/research/attempt-preload-2fa50b35dc3b52ca57aadaca.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-2fa50b35dc3b52ca57aadaca.json`
  - paper: `papers/inference/06-serving-scheduling/2024-2404.08509-ssjf.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-24 10:00 JST** / worker `scheduled-chat-00`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
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

- 未失効かつ非terminal jobのclaim: **143件** / 直近15分heartbeat: **21件**
- `arXiv:2607.04164` — BrownoutMoE: Structure-Aware Expert Grouping for Efficient and Accurate LLM Web-based Services / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-1a48a3083b0b1499.json`
- `arXiv:2603.10087` — Pooling Engram Conditional Memory in Large Language Models using CXL / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-1e9597cecaf6ec3b.json`
- `DOI:10.1109/EEI70303.2026.11640499` — PMKS: Co-Designing Distributed Networking and Multi-Tier Storage for Ultra-Long Context LLM Inference / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-1edac6e56714dd58.json`
- `DOI:10.1109/CCGrid68966.2026.00023` — LLM-Pilot: SLO-Aware and Cost-Efficient LLM Serving on Public Cloud VM Clusters via Offloading / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-2efe9f8fbd9f6b33.json`
- `arXiv:2511.19480` — Exploiting the Experts: Unauthorized Compression in MoE-LLMs / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-372c7ba23950bd0c.json`
- `arXiv:2602.01519` — You Need an Encoder for Native Position-Independent Caching / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-4044c82745a32e7d.json`
- `arXiv:2602.06154` — MoSE: Mixture of Slimmable Experts for Efficient and Adaptive Language Models / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-441084dd13b83186.json`
- `arXiv:2609.21137` — A Multi-Engine Dataflow for MoE Decoding on Scratchpad-Based Tensor Accelerators / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-5b8f1951128d6fe2.json`
- `DOI:10.1109/LCA.2026.3720952` — LLM KV Cache Storage Using CXL Memory / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-5cbec5c2c470e865.json`
- `DOI:10.1109/TCSI.2026.3692866` — DSLA: An Energy-Efficient Dual-Sparsity LLM Accelerator With HiMix-BFP / worker `shared-preload-pool`
  - claim: **09-24 10:01:49 JST** / heartbeat: **—** / lease expiry: **09-24 22:01:49 JST**
  - evidence: `.survey/work-queue/claims/job-research-64f36119defd4883.json`

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
| inference/training/survey配下の論文Markdown実体 | **1008** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **294** |
| └ Research | **161** |
| └ Audit | **2** |
| └ Discovery | **72** |
| └ Other/Unknown | **59** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **332** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

| 検出項目 | 件数 |
|---|---:|
| completed Research jobで指定paper実体なし | **0** |
| 対応jobなしsubmission（有効Discovery round除外） | **1** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **1** |

### 対応jobなしsubmissionの診断対象

上の異常件数と同一判定で抽出した耐久submission pathです。診断専用であり、submission/result自体は変更しません。

- `.survey/work-queue/submissions/research/attempt-preload-2f7b9ad4ec70e92c6b0818d3.json`

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
