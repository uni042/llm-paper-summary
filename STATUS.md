# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-23 23:36:32 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **144** |
| 未claim Research job | **123** |
| 直近24hの検証済みResearch収録 | **74** |
| 最終検証済みResearch収録 | **09-23 22:05:03 JST（1時間31分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **144** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **144** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6698** |
| 処理済み | **651** |
| 未処理 | **6047** |
| 収録済みとして除外 | **543** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.7%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-23 08:30:50 JST（15時間5分前）** |
| 最終maintenance status | **issues_found** |
| consistency | **passed** |
| health | **issues_found** |
| health errors / warnings | **1 / 2** |
| metadata | **passed** |
| metadata incomplete | **0** |
| GC削除件数 | **315** |
| queue snapshot repaired | **true** |
| index repairs | **5** |
| quality regressions | **7** |

maintenance固有の値は `maintenance-cycle.json` を正本とし、通常のjob/result件数から推定しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **13** | **1** | **0** | **0** | **21** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **13** | **4** | **0** | **3** | **21** | **0** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-23 22:05:03 JST** [research] `DOI:10.1145/3651890.3672274` — CacheGen: KV Cache Compression and Streaming for Fast Large Language Model Serving
  - job: `.survey/work-queue/jobs/job-research-958b0ab5aeb9819d.json`
  - result: `.survey/work-queue/results/research/attempt-preload-e320c142c976a89229191f7e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-e320c142c976a89229191f7e.json`
  - paper: `papers/inference/10-kv-cache-offload-recomputation/2024-2310.07240-cachegen.md`
- **09-23 21:58:44 JST** [research] `arXiv:2408.12757` — NanoFlow: Towards Optimal Large Language Model Serving Throughput
  - job: `.survey/work-queue/jobs/job-research-6882c5cf191305a1.json`
  - result: `.survey/work-queue/results/research/attempt-preload-84011e35924af607152554c4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-84011e35924af607152554c4.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2408.12757-nanoflow.md`
- **09-23 21:24:54 JST** [research] `arXiv:2609.15627` — DeepSeek-V4-Flash on AMD gfx90a: Correctness Recovery and Inference Performance Engineering
  - job: `.survey/work-queue/jobs/job-research-566a14b0b6e022f7.json`
  - result: `.survey/work-queue/results/research/attempt-9e32a6c39b70b1ce1c5e9f53.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9e32a6c39b70b1ce1c5e9f53.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.15627-deepseek-v4-flash-on-amd-gfx90a-correctness-recovery-and-inference-performance-engineering.md`
- **09-23 19:57:05 JST** [research] `arXiv:2606.21712` — BatchGen: An Architecture for Scalable and Efficient Batch Inference
  - job: `.survey/work-queue/jobs/job-research-ded5355ef64410a7.json`
  - result: `.survey/work-queue/results/research/attempt-04e285682c3e9ed7b0782532.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-04e285682c3e9ed7b0782532.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.21712-batchgen-an-architecture-for-scalable-and-efficient-batch-inference.md`
- **09-23 19:51:56 JST** [research] `arXiv:2606.01502` — Move the Query, Not the Cache: Characterizing Cross-Instance Latent Attention Redistribution Across GPU Fabrics
  - job: `.survey/work-queue/jobs/job-research-37a03b603cf5e34b.json`
  - result: `.survey/work-queue/results/research/attempt-df98f0a4232c714053b0bc18.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-df98f0a4232c714053b0bc18.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.01502-move-the-query-not-the-cache-characterizing-cross-instance-latent-attention-redistribution-across-gpu-fabrics.md`
- **09-23 19:47:46 JST** [research] `arXiv:2605.11277` — Sieve: Dynamic Expert-Aware PIM Acceleration for Evolving Mixture-of-Experts Models
  - job: `.survey/work-queue/jobs/job-research-165ae8125699de70.json`
  - result: `.survey/work-queue/results/research/attempt-e3c59442daeee9dcbcd01db3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e3c59442daeee9dcbcd01db3.json`
  - paper: `papers/inference/04-offload-heterogeneous/2026-2605.11277-sieve-dynamic-expert-aware-pim.md`
- **09-23 19:16:28 JST** [research] `arXiv:2509.14900` — FURINA: Free from Unmergeable Router via LINear Aggregation of mixed experts
  - job: `.survey/work-queue/jobs/job-research-e36fdfcc83960d96.json`
  - result: `.survey/work-queue/results/research/attempt-4507d6e7a694d747a350c3a0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4507d6e7a694d747a350c3a0.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2509.14900-furina-router-free-linear-expert-aggregation.md`
- **09-23 19:10:12 JST** [research] `arXiv:2511.15690` — MoDES: Accelerating Mixture-of-Experts Multimodal Large Language Models via Dynamic Expert Skipping
  - job: `.survey/work-queue/jobs/job-research-61e38612a8457ae4.json`
  - result: `.survey/work-queue/results/research/attempt-0640a4e19fcd3a04140f52b1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0640a4e19fcd3a04140f52b1.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2511.15690-modes-dynamic-expert-skipping.md`
- **09-23 18:51:27 JST** [research] `arXiv:2605.08738` — SlimQwen: Exploring the Pruning and Distillation in Large MoE Model Pre-training
  - job: `.survey/work-queue/jobs/job-research-1330e1d7068cf379.json`
  - result: `.survey/work-queue/results/research/attempt-ffa0b1baa60976c86cf81af0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ffa0b1baa60976c86cf81af0.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2605.08738-slimqwen-pruning-distillation.md`
- **09-23 18:45:27 JST** [research] `arXiv:2602.05711` — OmniMoE: An Efficient MoE by Orchestrating Atomic Experts at Scale
  - job: `.survey/work-queue/jobs/job-research-c732ba9bb46aaf3a.json`
  - result: `.survey/work-queue/results/research/attempt-bcdd660e4bafb23e846f2ec8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bcdd660e4bafb23e846f2ec8.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2602.05711-omnimoe-atomic-experts.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-23 22:00 JST** / worker `scheduled-chat-00`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-573272b1624939b93a0bdb83.json` (job `job-research-c0742ec707ffbbe8`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-573272b1624939b93a0bdb83.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-23 22:00 JST** / worker `scheduled-chat-00`
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

- 未失効かつ非terminal jobのclaim: **21件** / 直近15分heartbeat: **0件**
- `arXiv:2410.10819` — DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads / worker `shared-preload-pool`
  - claim: **09-23 22:07:40 JST** / heartbeat: **—** / lease expiry: **09-24 10:07:40 JST**
  - evidence: `.survey/work-queue/claims/job-research-53de425c7cce08ac.json`
- `arXiv:2602.13692` — ThunderAgent: A Simple, Fast and Program-Aware Agentic Inference System / worker `shared-preload-pool`
  - claim: **09-23 22:07:40 JST** / heartbeat: **—** / lease expiry: **09-24 10:07:40 JST**
  - evidence: `.survey/work-queue/claims/job-research-64becbe5cce3752e.json`
- `arXiv:2609.07108` — Online Draft Co-Training for Speculative Decoding in Large-Scale, Long-Context RL Post-Training / worker `shared-preload-pool`
  - claim: **09-23 22:07:40 JST** / heartbeat: **—** / lease expiry: **09-24 10:07:40 JST**
  - evidence: `.survey/work-queue/claims/job-research-89b223c1a441edfc.json`
- `arXiv:2608.12114` — The Ingestion Tax: Adopting File-Backed Weights in Tensor Frameworks / worker `shared-preload-pool`
  - claim: **09-23 22:07:40 JST** / heartbeat: **—** / lease expiry: **09-24 10:07:40 JST**
  - evidence: `.survey/work-queue/claims/job-research-9d57d4c95ee33e52.json`
- `arXiv:2511.19480` — Exploiting the Experts: Unauthorized Compression in MoE-LLMs / worker `scheduled-chat-00`
  - claim: **09-23 22:07:39 JST** / heartbeat: **09-23 22:07:39 JST** / lease expiry: **09-23 23:37:39 JST**
  - evidence: `.survey/work-queue/claims/job-research-372c7ba23950bd0c.json`
- `DOI:10.1007/s44196-026-01236-9` — Consensus-Expert DynamicMoE: ARIMA-based Capacity Prediction with Adaptive Load Balancing for Sparse Models / worker `scheduled-chat-00`
  - claim: **09-23 22:07:39 JST** / heartbeat: **09-23 22:07:39 JST** / lease expiry: **09-23 23:37:39 JST**
  - evidence: `.survey/work-queue/claims/job-research-75eff2262d950b6f.json`
- `arXiv:2510.03151` — Mixture of Many Zero-Compute Experts: A High-Rate Quantization Theory Perspective / worker `scheduled-chat-00`
  - claim: **09-23 22:07:39 JST** / heartbeat: **09-23 22:07:39 JST** / lease expiry: **09-23 23:37:39 JST**
  - evidence: `.survey/work-queue/claims/job-research-b3cb99418924d14e.json`
- `arXiv:2607.01444` — On the Utility and Factual Reliability of Pruned Mixture-of-Experts Models in the Biomedical Domain / worker `scheduled-chat-00`
  - claim: **09-23 22:07:39 JST** / heartbeat: **09-23 22:07:39 JST** / lease expiry: **09-23 23:37:39 JST**
  - evidence: `.survey/work-queue/claims/job-research-d5b6de209d3bfef0.json`
- `DOI:10.1016/j.neunet.2026.109617` — MoEP: Compact and efficient sparsity with modular expert paths / worker `shared-preload-pool`
  - claim: **09-23 22:01:32 JST** / heartbeat: **—** / lease expiry: **09-24 10:01:32 JST**
  - evidence: `.survey/work-queue/claims/job-research-62f6ca15b903420d.json`
- `arXiv:2603.10087` — Pooling Engram Conditional Memory in Large Language Models using CXL / worker `shared-preload-pool`
  - claim: **09-23 21:41:31 JST** / heartbeat: **—** / lease expiry: **09-24 09:41:31 JST**
  - evidence: `.survey/work-queue/claims/job-research-1e9597cecaf6ec3b.json`

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
| ready | **144** |

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
| inference/training/survey配下の論文Markdown実体 | **1002** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **275** |
| └ Research | **199** |
| └ Audit | **2** |
| └ Discovery | **70** |
| └ Other/Unknown | **4** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **345** |

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
