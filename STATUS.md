# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-23 04:59:31 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **207** |
| 未claim Research job | **205** |
| 直近24hの検証済みResearch収録 | **66** |
| 最終検証済みResearch収録 | **09-23 04:50:46 JST（8分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **207** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **207** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6204** |
| 処理済み | **623** |
| 未処理 | **5581** |
| 収録済みとして除外 | **515** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **10.0%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-22 08:32:35 JST（20時間26分前）** |
| 最終maintenance status | **issues_found** |
| consistency | **passed** |
| health | **issues_found** |
| health errors / warnings | **1 / 0** |
| metadata | **passed** |
| metadata incomplete | **0** |
| GC削除件数 | **2108** |
| queue snapshot repaired | **true** |
| index repairs | **0** |
| quality regressions | **17** |

maintenance固有の値は `maintenance-cycle.json` を正本とし、通常のjob/result件数から推定しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **27** | **1** | **0** | **0** | **2** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **27** | **4** | **0** | **3** | **2** | **0** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-23 04:50:46 JST** [research] `arXiv:2410.12013` — MoE-Pruner: Pruning Mixture-of-Experts Large Language Model using the Hints from Its Router
  - job: `.survey/work-queue/jobs/job-research-d4390f65b198912f.json`
  - result: `.survey/work-queue/results/research/attempt-1338966144636293379a0970.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1338966144636293379a0970.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2024-2410.12013-moe-pruner-router-hints.md`
- **09-23 04:44:47 JST** [research] `arXiv:2604.06542` — Does a Global Perspective Help Prune Sparse MoEs Elegantly?
  - job: `.survey/work-queue/jobs/job-research-c92e15d6ba5edb8d.json`
  - result: `.survey/work-queue/results/research/attempt-c1740060a24d308914998762.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c1740060a24d308914998762.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2604.06542-global-perspective-moe-pruning.md`
- **09-23 04:38:07 JST** [research] `arXiv:2508.07785` — Grove MoE: Towards Efficient and Superior MoE LLMs with Adjugate Experts
  - job: `.survey/work-queue/jobs/job-research-b8b352e984bc0e9d.json`
  - result: `.survey/work-queue/results/research/attempt-4d7a0c3e035c923b869769ba.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4d7a0c3e035c923b869769ba.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2508.07785-grove-moe-heterogeneous-experts.md`
- **09-23 04:16:37 JST** [research] `arXiv:2510.13079` — GatePro: Parameter-Free Expert Selection Optimization for Mixture-of-Experts Models
  - job: `.survey/work-queue/jobs/job-research-9b33865bddc54a07.json`
  - result: `.survey/work-queue/results/research/attempt-6cd2c2eb6d8d0d8116429b11.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6cd2c2eb6d8d0d8116429b11.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2510.13079-gatepro-parameter-free-expert-selection.md`
- **09-23 04:12:31 JST** [research] `arXiv:2509.19781` — Faster, Smaller, and Smarter: Task-Aware Expert Merging for Online MoE Inference
  - job: `.survey/work-queue/jobs/job-research-3218c42781ec549d.json`
  - result: `.survey/work-queue/results/research/attempt-a503dd59d7e7b9e3cfd8340e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a503dd59d7e7b9e3cfd8340e.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2509.19781-task-aware-expert-merging-online.md`
- **09-23 04:06:54 JST** [research] `arXiv:2601.21420` — ConceptMoE: Adaptive Token-to-Concept Compression for Implicit Compute Allocation
  - job: `.survey/work-queue/jobs/job-research-74a266f79fc28554.json`
  - result: `.survey/work-queue/results/research/attempt-95a58c9a93fe71f7a995bfe2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-95a58c9a93fe71f7a995bfe2.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2601.21420-conceptmoe-token-concept-compression.md`
- **09-23 03:46:27 JST** [research] `arXiv:2605.13997` — HodgeCover: Higher-Order Topological Coverage Drives Compression of Sparse Mixture-of-Experts
  - job: `.survey/work-queue/jobs/job-research-458a8d0f006d0310.json`
  - result: `.survey/work-queue/results/research/attempt-3f2821d83831a58e9fb2986d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3f2821d83831a58e9fb2986d.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2605.13997-hodgecover-topological-compression.md`
- **09-23 03:35:17 JST** [research] `arXiv:2606.09885` — TENP: Trapezoidal Expert Neuron Pruning For Mixture-of-Experts
  - job: `.survey/work-queue/jobs/job-research-0492476ca3ab6ea2.json`
  - result: `.survey/work-queue/results/research/attempt-98e2f1fac5c29a094f21cbf1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-98e2f1fac5c29a094f21cbf1.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2606.09885-tenp-trapezoidal-expert-neuron-pruning.md`
- **09-23 03:20:32 JST** [research] `arXiv:2512.18425` — MoE Pathfinder: Trajectory-driven Expert Pruning
  - job: `.survey/work-queue/jobs/job-research-20085e82ab231044.json`
  - result: `.survey/work-queue/results/research/attempt-c7fc5d8a2ddc77f17046a7e2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c7fc5d8a2ddc77f17046a7e2.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2512.18425-moe-pathfinder-trajectory-pruning.md`
- **09-23 03:11:17 JST** [research] `arXiv:2605.14438` — BEAM: Binary Expert Activation Masking for Dynamic Routing in MoE
  - job: `.survey/work-queue/jobs/job-research-f43aa8f1dfa7e573.json`
  - result: `.survey/work-queue/results/research/attempt-71174da29a72754d44fbffa1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-71174da29a72754d44fbffa1.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2605.14438-beam-binary-expert-activation-masking.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-23 04:00 JST** / worker `scheduled-chat-00`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-b9523ed098074392111e4480.json` (job `job-research-384393fce738e0be`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-b9523ed098074392111e4480.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-23 04:00 JST** / worker `scheduled-chat-00`
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

- 未失効かつ非terminal jobのclaim: **2件** / 直近15分heartbeat: **0件**
- `arXiv:2608.08627` — UniMoMo: Expert Merging-Based MoE Acceleration for Large Recommendation Models / worker `scheduled-chat-30`
  - claim: **09-23 04:52:36 JST** / heartbeat: **—** / lease expiry: **09-23 06:22:36 JST**
  - evidence: `.survey/work-queue/claims/job-research-3611857c9c7fea67.json`
- `arXiv:2512.14531` — VersatileFFN: Achieving Parameter Efficiency in LLMs via Adaptive Wide-and-Deep Reuse / worker `scheduled-chat-00`
  - claim: **09-23 04:17:29 JST** / heartbeat: **—** / lease expiry: **09-23 05:47:29 JST**
  - evidence: `.survey/work-queue/claims/job-research-6e36f8b25c1d84c6.json`

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
| ready | **207** |

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
| inference/training/survey配下の論文Markdown実体 | **951** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **332** |
| └ Research | **260** |
| └ Audit | **2** |
| └ Discovery | **70** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **336** |

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
