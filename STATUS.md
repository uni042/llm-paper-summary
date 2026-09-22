# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-22 15:12:46 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **307** |
| 未claim Research job | **306** |
| 直近24hの検証済みResearch収録 | **16** |
| 最終検証済みResearch収録 | **09-22 13:52:54 JST（1時間19分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **307** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **307** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **5911** |
| 処理済み | **594** |
| 未処理 | **5317** |
| 収録済みとして除外 | **486** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **10.0%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-22 08:32:35 JST（6時間40分前）** |
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
| Research | **8** | **3** | **0** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **8** | **6** | **0** | **3** | **1** | **0** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-22 13:52:54 JST** [research] `arXiv:2202.09368` — Mixture-of-Experts with Expert Choice Routing
  - job: `.survey/work-queue/jobs/job-research-9de329d10383e26b.json`
  - result: `.survey/work-queue/results/research/attempt-afcf905bd317f0527a7a08a2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-afcf905bd317f0527a7a08a2.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2022-2202.09368-expert-choice-routing.md`
- **09-22 13:46:31 JST** [research] `arXiv:2110.01786` — MoEfication: Transformer Feed-forward Layers are Mixtures of Experts
  - job: `.survey/work-queue/jobs/job-research-1922ded1807d40e6.json`
  - result: `.survey/work-queue/results/research/attempt-3bb5f476d210f19b5b746d7c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3bb5f476d210f19b5b746d7c.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2021-2110.01786-moefication.md`
- **09-22 13:40:13 JST** [research] `arXiv:2206.00277` — Task-Specific Expert Pruning for Sparse Mixture-of-Experts
  - job: `.survey/work-queue/jobs/job-research-80e5caed751c8e16.json`
  - result: `.survey/work-queue/results/research/attempt-c4f65a2a84382bc8c1957458.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c4f65a2a84382bc8c1957458.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2022-2206.00277-task-specific-expert-pruning.md`
- **09-22 12:09:14 JST** [research] `arXiv:2602.07265` — XShare: Collaborative in-Batch Expert Sharing for Faster MoE Inference
  - job: `.survey/work-queue/jobs/job-research-a4cc548ec9dfc021.json`
  - result: `.survey/work-queue/results/research/attempt-6aabd8efa261970bb7aabb74.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6aabd8efa261970bb7aabb74.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2602.07265-xshare-inbatch-expert-sharing.md`
- **09-22 11:30:28 JST** [research] `arXiv:2509.16105` — DiEP: Adaptive Mixture-of-Experts Compression through Differentiable Expert Pruning
  - job: `.survey/work-queue/jobs/job-research-1b89c86f687054e4.json`
  - result: `.survey/work-queue/results/research/attempt-6de20ea36381d00ca19a50de.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6de20ea36381d00ca19a50de.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2509.16105-diep-differentiable-expert-pruning.md`
- **09-22 11:15:09 JST** [research] `arXiv:2608.04502` — AFD-Ledger: Deployment Provisioning for Attention--FFN Disaggregation
  - job: `.survey/work-queue/jobs/job-research-be16d214d5c628cd.json`
  - result: `.survey/work-queue/results/research/attempt-40775da1ed5102aa9d7b9a44.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-40775da1ed5102aa9d7b9a44.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2608.04502-afd-ledger-deployment-provisioning-for-attention-ffn-disaggregation.md`
- **09-22 11:12:51 JST** [research] `arXiv:2605.08575` — Uncovering Intra-expert Activation Sparsity for Efficient Mixture-of-Expert Model Execution
  - job: `.survey/work-queue/jobs/job-research-5cd2beb9d9cae3d8.json`
  - result: `.survey/work-queue/results/research/attempt-b5919b99883e66617c28776a.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b5919b99883e66617c28776a.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2605.08575-intra-expert-activation-sparsity.md`
- **09-22 09:32:19 JST** [research] `arXiv:2608.21836` — LLM4LLM: Bridging Kernel Benchmarks and Real Deployment via Closed-Loop Agentic Optimization
  - job: `.survey/work-queue/jobs/job-research-f0b1ffeacc3b0ccd.json`
  - result: `.survey/work-queue/results/research/attempt-f4daf58b89f6ce40e07a2ba4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f4daf58b89f6ce40e07a2ba4.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2608.21836-llm4llm-bridging-kernel-benchmarks-and-real-deployment-via-closed-loop-agentic-optimization.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-22 12:00 JST** / worker `scheduled-chat-00`
- immutable submission: **3件** / 検証済み成功: **0件** / result照合済み非成功: **3件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-9ef1f6cf62d391bce3de73b6.json` (job `job-research-f4f109c7c5f9fc6f`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-9ef1f6cf62d391bce3de73b6.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-a952bf0b515b043bf649c82d.json` (job `job-research-4dc1463f3235b886`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-a952bf0b515b043bf649c82d.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-bfa8cf590d28a92deda4a59b.json` (job `job-research-d872577f35056ccd`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-bfa8cf590d28a92deda4a59b.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-22 12:00 JST** / worker `scheduled-chat-00`
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

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2504.07807` — Cluster-Driven Expert Pruning for Mixture-of-Experts Large Language Models / worker `scheduled-chat-00`
  - claim: **09-22 15:10:24 JST** / heartbeat: **—** / lease expiry: **09-22 16:40:24 JST**
  - evidence: `.survey/work-queue/claims/job-research-a4042c7c7ed57c9a.json`

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
| ready | **307** |

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
| inference/training/survey配下の論文Markdown実体 | **893** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **275** |
| └ Research | **203** |
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
