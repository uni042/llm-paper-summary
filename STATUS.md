# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-22 19:29:14 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **279** |
| 未claim Research job | **278** |
| 直近24hの検証済みResearch収録 | **25** |
| 最終検証済みResearch収録 | **09-22 19:19:23 JST（9分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **279** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **279** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **5979** |
| 処理済み | **603** |
| 未処理 | **5376** |
| 収録済みとして除外 | **495** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **10.1%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-22 08:32:35 JST（10時間56分前）** |
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
| Research | **16** | **2** | **0** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **3** | **0** | **3** | **0** | **0** | **6** |
| 合計 | **16** | **5** | **0** | **3** | **1** | **0** | **6** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-22 19:19:23 JST** [research] `arXiv:2606.16824` — CacheWise: Understanding Workloads and Optimizing KVCache Management for Efficiently Serving LLM Coding Agents
  - job: `.survey/work-queue/jobs/job-research-548d7e4cd563f6b8.json`
  - result: `.survey/work-queue/results/research/attempt-40b553eeb725cfefaa1a1d5f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-40b553eeb725cfefaa1a1d5f.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.16824-cachewise-understanding-workloads-and-optimizing-kvcache-management-for-efficiently-serving-llm-coding-agents.md`
- **09-22 17:10:31 JST** [research] `arXiv:2605.07719` — An Efficient Hybrid Sparse Attention with CPU-GPU Parallelism for Long-Context Inference
  - job: `.survey/work-queue/jobs/job-research-10bf8d55e9caa5c4.json`
  - result: `.survey/work-queue/results/research/attempt-59dc9473086573b3d534c617.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-59dc9473086573b3d534c617.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.07719-an-efficient-hybrid-sparse-attention-with-cpu-gpu-parallelism-for-long-context-inference.md`
- **09-22 17:04:14 JST** [research] `arXiv:2608.19758` — FlashPrefill V2: Block-Sparse Prefill Attention for Long-Context LLM Serving
  - job: `.survey/work-queue/jobs/job-research-6ca9e5aa49540dd5.json`
  - result: `.survey/work-queue/results/research/attempt-f8a196fb851ca2c1095b5a40.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f8a196fb851ca2c1095b5a40.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2608.19758-flashprefill-v2-block-sparse-prefill-attention-for-long-context-llm-serving.md`
- **09-22 16:38:18 JST** [research] `arXiv:2606.21633` — HERALD: High-Throughput Block Diffusion LLM Serving via CPU-GPU Cooperative KV Cache Retrieval
  - job: `.survey/work-queue/jobs/job-research-3b95bafdcf04b501.json`
  - result: `.survey/work-queue/results/research/attempt-50b11451c81409b86f90c5e0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-50b11451c81409b86f90c5e0.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.21633-herald-high-throughput-block-diffusion-llm-serving-via-cpu-gpu-cooperative-kv-cache-retrieval.md`
- **09-22 16:38:18 JST** [research] `arXiv:2609.13141` — SAS: Simple Attention Sparsification via End-to-End Optimization of Context Ranking
  - job: `.survey/work-queue/jobs/job-research-6542fa570cf353a1.json`
  - result: `.survey/work-queue/results/research/attempt-eac46ddd3cb449fe8b2c0320.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-eac46ddd3cb449fe8b2c0320.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.13141-sas-simple-attention-sparsification-via-end-to-end-optimization-of-context-ranking.md`
- **09-22 16:20:36 JST** [research] `DOI:10.24963/ijcai.2026/502` — M-LoRA: Efficient Serving for Concurrent LoRA Adapters with Memory-Aware Speculative Scheduler on Single GPU
  - job: `.survey/work-queue/jobs/job-research-784815ee56689f0c.json`
  - result: `.survey/work-queue/results/research/attempt-f9afab963f7542abadb69271.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f9afab963f7542abadb69271.json`
  - paper: `papers/inference/99-other-inference-systems/2026-bbf40b71b5e2-m-lora-efficient-serving-for-concurrent-lora-adapters-with-memory-aware-speculative-scheduler-on-single-gpu.md`
- **09-22 16:12:46 JST** [research] `arXiv:2510.26730` — ExpertFlow: Adaptive Expert Scheduling and Memory Coordination for Efficient MoE Inference
  - job: `.survey/work-queue/jobs/job-research-d522f30f5ddd350f.json`
  - result: `.survey/work-queue/results/research/attempt-eb3992a288275edbaaa96880.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-eb3992a288275edbaaa96880.json`
  - paper: `papers/inference/03-expert-prefetch/2025-2510.26730-expertflow-adaptive-prefetch.md`
- **09-22 16:11:02 JST** [research] `arXiv:2609.12550` — Quality-Constrained Routing over a Fixed Pool of Quantized Mixture-of-Experts Instances
  - job: `.survey/work-queue/jobs/job-research-b6a722146f5922c5.json`
  - result: `.survey/work-queue/results/research/attempt-1385b427873bab2ec9caad6b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1385b427873bab2ec9caad6b.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.12550-quality-constrained-routing-over-a-fixed-pool-of-quantized-mixture-of-experts-instances.md`
- **09-22 16:05:00 JST** [research] `arXiv:2609.09823` — AMEND: Audited Margins Enable Nonblocking Drops in GPU-PIM LLM Decoding
  - job: `.survey/work-queue/jobs/job-research-ca56f81ba7248b99.json`
  - result: `.survey/work-queue/results/research/attempt-65c28b59ac08b3e1cf0adad9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-65c28b59ac08b3e1cf0adad9.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.09823-amend-audited-margins-enable-nonblocking-drops-in-gpu-pim-llm-decoding.md`
- **09-22 15:21:54 JST** [research] `arXiv:2608.30567` — TuringLLM: Efficiently Scaling Foundation Models Toward Physical AI
  - job: `.survey/work-queue/jobs/job-research-92d92d3583bf57da.json`
  - result: `.survey/work-queue/results/research/attempt-87c159714bb65416bb0f37de.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-87c159714bb65416bb0f37de.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2608.30567-turingllm-dynamic-topk.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-22 19:00 JST** / worker `scheduled-chat-00`
- immutable submission: **2件** / 検証済み成功: **0件** / result照合済み非成功: **2件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-32ac40905164328636c42caa.json` (job `job-research-dde4fdefdee6c368`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-32ac40905164328636c42caa.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-714eaa3772fb0eedb52aa450.json` (job `job-research-ceb9b2d0b0c9c441`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-714eaa3772fb0eedb52aa450.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-22 19:00 JST** / worker `scheduled-chat-00`
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
- `arXiv:2608.28293` — A Probabilistic Interpretation of KV Cache Eviction / worker `scheduled-chat-00`
  - claim: **09-22 19:28:41 JST** / heartbeat: **—** / lease expiry: **09-22 20:58:41 JST**
  - evidence: `.survey/work-queue/claims/job-research-199b831b6808fd50.json`

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
| ready | **279** |

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
| inference/training/survey配下の論文Markdown実体 | **906** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **302** |
| └ Research | **230** |
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
