# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-23 08:20:46 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **189** |
| 未claim Research job | **187** |
| 直近24hの検証済みResearch収録 | **77** |
| 最終検証済みResearch収録 | **09-23 08:19:08 JST（1分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **189** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **189** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6333** |
| 処理済み | **630** |
| 未処理 | **5703** |
| 収録済みとして除外 | **522** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.9%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-22 08:32:35 JST（23時間48分前）** |
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
| Research | **22** | **4** | **0** | **0** | **2** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **22** | **7** | **0** | **3** | **2** | **0** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-23 08:19:08 JST** [research] `arXiv:2606.14672` — Towards Direct Latent-Space Synthesis for Parallel Branches in LLM-Agent Workflows
  - job: `.survey/work-queue/jobs/job-research-baad806afa0723b4.json`
  - result: `.survey/work-queue/results/research/attempt-ff7e9c58f4c5f78412ef8d98.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ff7e9c58f4c5f78412ef8d98.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.14672-towards-direct-latent-space-synthesis-for-parallel-branches-in-llm-agent-workflows.md`
- **09-23 08:10:53 JST** [research] `arXiv:2606.25426` — Above the Inner Loop: Exceeding Accelerate at LLM Prefill GEMM on the M1 AMX
  - job: `.survey/work-queue/jobs/job-research-06d45370eceff021.json`
  - result: `.survey/work-queue/results/research/attempt-546bf32315ae41457b812520.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-546bf32315ae41457b812520.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.25426-above-the-inner-loop-exceeding-accelerate-at-llm-prefill-gemm-on-the-m1-amx.md`
- **09-23 07:44:31 JST** [research] `DOI:10.1109/ACCESS.2026.3665697` — Two-Stage Expert Offloading for Domain-Aware MoE Inference
  - job: `.survey/work-queue/jobs/job-research-3c62e3c72b715377.json`
  - result: `.survey/work-queue/results/research/attempt-0435bf18257a114df581ef2f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0435bf18257a114df581ef2f.json`
  - paper: `papers/inference/99-other-inference-systems/2026-dacc3922b5b4-two-stage-expert-offloading-for-domain-aware-moe-inference.md`
- **09-23 07:40:43 JST** [research] `arXiv:2606.16332` — SMEPilot: Characterizing and Optimizing LLM Inference with Scalable Matrix Extensions
  - job: `.survey/work-queue/jobs/job-research-f28b959eef987bac.json`
  - result: `.survey/work-queue/results/research/attempt-78929a6ba475ed2b2f05a50c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-78929a6ba475ed2b2f05a50c.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.16332-smepilot-characterizing-and-optimizing-llm-inference-with-scalable-matrix-extensions.md`
- **09-23 07:39:19 JST** [research] `DOI:10.1007/s10462-026-11651-1` — I/o for LLM inference: a survey of storage and memory bottlenecks
  - job: `.survey/work-queue/jobs/job-research-15688dbb0cd11f1c.json`
  - result: `.survey/work-queue/results/research/attempt-4a6861f35cc58610c3fb4b0c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4a6861f35cc58610c3fb4b0c.json`
  - paper: `papers/inference/99-other-inference-systems/2026-5e022a2789e7-i-o-for-llm-inference-a-survey-of-storage-and-memory-bottlenecks.md`
- **09-23 07:37:28 JST** [research] `arXiv:2609.14213` — Partition-Aware Scheduling for Mobile Heterogeneous Inference Co-Execution
  - job: `.survey/work-queue/jobs/job-research-aa3e3c19262a245a.json`
  - result: `.survey/work-queue/results/research/attempt-a302801e2f42ef7601d7976c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a302801e2f42ef7601d7976c.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.14213-partition-aware-scheduling-for-mobile-heterogeneous-inference-co-execution.md`
- **09-23 07:30:32 JST** [research] `arXiv:2609.08566` — BIO-MEMART: Biometric-Aware KV Cache Memory for Multi-User LLM Agents
  - job: `.survey/work-queue/jobs/job-research-ce081c207f1ded58.json`
  - result: `.survey/work-queue/results/research/attempt-9a2c0141760202bf19379f9a.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9a2c0141760202bf19379f9a.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.08566-bio-memart-biometric-aware-kv-cache-memory-for-multi-user-llm-agents.md`
- **09-23 07:17:27 JST** [research] `arXiv:2608.08627` — UniMoMo: Expert Merging-Based MoE Acceleration for Large Recommendation Models
  - job: `.survey/work-queue/jobs/job-research-3611857c9c7fea67.json`
  - result: `.survey/work-queue/results/research/attempt-88d2aa5426361490104919b5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-88d2aa5426361490104919b5.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2608.08627-unimomo-expert-merging.md`
- **09-23 05:22:23 JST** [research] `arXiv:2505.13345` — Occult: Optimizing Collaborative Communication across Experts for Accelerated Parallel MoE Training and Inference
  - job: `.survey/work-queue/jobs/job-research-bc95233f6a664ba4.json`
  - result: `.survey/work-queue/results/research/attempt-a2e5fb73d91123b2b7515fb2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a2e5fb73d91123b2b7515fb2.json`
  - paper: `papers/inference/04-moe-parallelism-communication/2025-2505.13345-occult-collaborative-expert-communication.md`
- **09-23 05:17:34 JST** [research] `arXiv:2507.23279` — Unveiling Super Experts in Mixture-of-Experts Large Language Models
  - job: `.survey/work-queue/jobs/job-research-b921c5addc92d695.json`
  - result: `.survey/work-queue/results/research/attempt-40f2100aeb26ce98eb0d15a5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-40f2100aeb26ce98eb0d15a5.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2507.23279-super-experts-pruning-sensitivity.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-23 08:00 JST** / worker `scheduled-chat-00`
- immutable submission: **4件** / 検証済み成功: **0件** / result照合済み非成功: **4件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-7b2ad0006cdb59e5af892cef.json` (job `job-research-54ca1a03ac5f8a92`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-7b2ad0006cdb59e5af892cef.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-9db3517b66d3bd9f441cee8c.json` (job `job-research-324d91b08021a955`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-9db3517b66d3bd9f441cee8c.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-f455389f915cff8f429e2fb1.json` (job `job-research-cd4bfdc72f5fe696`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-f455389f915cff8f429e2fb1.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-fe57df5838897688f6d133c7.json` (job `job-research-25a675a94380dcd5`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-fe57df5838897688f6d133c7.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-23 08:00 JST** / worker `scheduled-chat-00`
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
- `arXiv:2609.09240` — Scaling Post-Training Ternarisation to Qwen3-8B Capability Retention, Reproduction, Lossless Packing, and Packed Execution / worker `scheduled-chat-00`
  - claim: **09-23 08:20:03 JST** / heartbeat: **—** / lease expiry: **09-23 09:50:03 JST**
  - evidence: `.survey/work-queue/claims/job-research-51f4efd90b7a5e12.json`
- `arXiv:2609.19207` — MeshKV: A Network-on-Chip KV Cache Fabric for Scalable Transformer Decoding Accelerators / worker `scheduled-chat-30`
  - claim: **09-23 07:44:12 JST** / heartbeat: **—** / lease expiry: **09-23 09:14:12 JST**
  - evidence: `.survey/work-queue/claims/job-research-9fc5a1ad8ad0b2d8.json`

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
| ready | **189** |

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
| inference/training/survey配下の論文Markdown実体 | **962** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **339** |
| └ Research | **267** |
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
