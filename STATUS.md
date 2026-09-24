# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-25 00:49:18 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **287** |
| 未claim Research job | **145** |
| 直近24hの検証済みResearch収録 | **19** |
| 最終検証済みResearch収録 | **09-25 00:46:34 JST** |
| 最終検証済みDiscovery探索 | **09-25 00:08:12 JST** |
| 整合性異常 | **0** |

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
| 構造化references総候補 | **6822** |
| 処理済み | **668** |
| 未処理 | **6154** |
| 収録済みとして除外 | **559** |
| 無関係として除外 | **49** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（16時間13分前）** |
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
| Research | **3** | **4** | **2** | **0** | **142** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **26** | **3** | **3** | **0** | **0** | **0** | **5** |
| 合計 | **29** | **7** | **5** | **0** | **142** | **0** | **5** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-25 00:46:34 JST** [research] `arXiv:2508.17137` — MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices
  - job: `.survey/work-queue/jobs/job-research-b22af651ef4f551f.json`
  - result: `.survey/work-queue/results/research/attempt-preload-5ae76716eb01958d78f1d488.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-5ae76716eb01958d78f1d488.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2508.17137-moe-beyond-learning-based-expert-activation-prediction-on-edge-devices.md`
- **09-25 00:42:27 JST** [research] `DOI:10.1109/LCA.2026.3720952` — LLM KV Cache Storage Using CXL Memory
  - job: `.survey/work-queue/jobs/job-research-5cbec5c2c470e865.json`
  - result: `.survey/work-queue/results/research/attempt-preload-4cb587870cc33021ea9f2c50.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-4cb587870cc33021ea9f2c50.json`
  - paper: `papers/inference/99-other-inference-systems/2026-4885970e907b-llm-kv-cache-storage-using-cxl-memory.md`
- **09-24 22:47:43 JST** [research] `arXiv:2607.16248` — High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration
  - job: `.survey/work-queue/jobs/job-research-11098a1512c29cb4.json`
  - result: `.survey/work-queue/results/research/attempt-preload-24504aa3d0d6716cf366c75b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-24504aa3d0d6716cf366c75b.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2607.16248-high-accuracy-low-bit-kv-cache-quantization-via-local-distribution-restoration.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-25 00:07:44 JST** job `job-aa981b049264d3ea` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T150300Z-scheduled-chat-00-7e4c91-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T150300Z-scheduled-chat-00-7e4c91-r1.json`
  - 探索軸: preload-backward-structured-references
- **09-25 00:07:58 JST** job `job-e53dbbd42dbddbc2` / 候補 **3件**
  - result: `.survey/work-queue/results/20260924T150340Z-scheduled-chat-00-7e4c91-r2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T150340Z-scheduled-chat-00-7e4c91-r2.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
- **09-25 00:08:12 JST** job `job-c09940bfed9694b8` / 候補 **2件**
  - result: `.survey/work-queue/results/20260924T150430Z-scheduled-chat-00-7e4c91-r3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T150430Z-scheduled-chat-00-7e4c91-r3.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
- **09-24 22:15:14 JST** job `job-121edc29d47e3074` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T130330Z-scheduled-chat-00-6e21c4-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T130330Z-scheduled-chat-00-6e21c4-r1.json`
  - 探索軸: preload-backward-structured-references
- **09-24 22:15:07 JST** job `job-62fd66001f3e574b` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T123145Z-scheduled-chat-30-8f31c2-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T123145Z-scheduled-chat-30-8f31c2-r1.json`
  - 探索軸: preload-backward-structured-references
- **09-24 19:55:28 JST** job `job-cfc2aa0addf64b6e` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T095930Z-scheduled-chat-00-6f4c2a-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/20260924T095930Z-scheduled-chat-00-6f4c2a-r1.json`
  - 探索軸: backward references from repository structured references
- **09-24 22:13:52 JST** job `job-f9a9fdd42f4f42ad` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-agent-multimodal-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-agent-multimodal-6.json`
  - 探索軸: agentic serving・multimodal serving・stateful runtime
- **09-24 22:13:59 JST** job `job-e339316cfe3974cc` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-cpu-heterogeneous-10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-cpu-heterogeneous-10.json`
  - 探索軸: CPU-only・CPU/GPU heterogeneous inference runtime
- **09-24 22:14:06 JST** job `job-9521bd9e238ef538` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-energy-saturation-11.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-energy-saturation-11.json`
  - 探索軸: energy・power-aware serving・DVFS
- **09-24 22:14:13 JST** job `job-f629b37eed727368` / 候補 **0件**
  - result: `.survey/work-queue/results/2026-09-19T16-00-00+09-00-specialist-framework-control-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/2026-09-19T16-00-00+09-00-specialist-framework-control-8.json`
  - 探索軸: serving framework control-plane・CPU-free runtime

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-25 00:32 JST** / worker `worker-925000`
- immutable submission: **4件** / 検証済み成功: **2件** / result照合済み非成功: **2件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-45d47f580075d5ff79492a68.json` (job `job-research-1a48a3083b0b1499`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-45d47f580075d5ff79492a68.json` (`ok=true`)
- **成功** `DOI:10.1109/LCA.2026.3720952` — LLM KV Cache Storage Using CXL Memory
  - job: `.survey/work-queue/jobs/job-research-5cbec5c2c470e865.json`
  - result: `.survey/work-queue/results/research/attempt-preload-4cb587870cc33021ea9f2c50.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-4cb587870cc33021ea9f2c50.json`
  - paper: `papers/inference/99-other-inference-systems/2026-4885970e907b-llm-kv-cache-storage-using-cxl-memory.md`
- **成功** `arXiv:2508.17137` — MoE-Beyond: Learning-Based Expert Activation Prediction on Edge Devices
  - job: `.survey/work-queue/jobs/job-research-b22af651ef4f551f.json`
  - result: `.survey/work-queue/results/research/attempt-preload-5ae76716eb01958d78f1d488.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-5ae76716eb01958d78f1d488.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2508.17137-moe-beyond-learning-based-expert-activation-prediction-on-edge-devices.md`
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-f234ef828a71ef4bb3d542c4.json` (job `job-research-e6152c2a3998faa6`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-f234ef828a71ef4bb3d542c4.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-25 00:32 JST** / worker `worker-925000`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-24 23:59 JST**
- 耐久探索round: **3件** / immutable submission: **3件** / 検証済み成功result: **3件** / 個別result照合: **3件** / 個別result未照合: **0件** / 候補: **5件**
- 探索軸: preload-backward-structured-references / forward citations of LMCache enterprise-scale KV cache layer / forward citations of FlexGen offload and hierarchical-memory LLM inference
- round `disc-scheduled-chat-00-7e4c91-r1` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260924T150300Z-scheduled-chat-00-7e4c91-r1.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/20260924T150300Z-scheduled-chat-00-7e4c91-r1.json` (`ok=true`)
- round `frontier-11ef2f8c76f0b7f92bdb1281` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260924T150340Z-scheduled-chat-00-7e4c91-r2.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
  - 個別result照合: あり / `.survey/work-queue/results/20260924T150340Z-scheduled-chat-00-7e4c91-r2.json` (`ok=true`)
- round `frontier-f6457f0fe296dced4a887067` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260924T150430Z-scheduled-chat-00-7e4c91-r3.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/20260924T150430Z-scheduled-chat-00-7e4c91-r3.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **142件** / 直近15分heartbeat: **0件**
- `DOI:10.1109/LES.2025.3616900` — LPC: Efficient Lossless Parameter Compression for Deploying LLM Inference on Edge Systems / worker `shared-preload-pool`
  - claim: **09-25 00:44:23 JST** / heartbeat: **—** / lease expiry: **09-25 12:44:23 JST**
  - evidence: `.survey/work-queue/claims/job-research-1c0254220f4e6305.json`
- `arXiv:2601.19908` — CHIME: Chiplet-based Heterogeneous Near-Memory Acceleration for Edge Multimodal LLM Inference / worker `shared-preload-pool`
  - claim: **09-25 00:44:23 JST** / heartbeat: **—** / lease expiry: **09-25 12:44:23 JST**
  - evidence: `.survey/work-queue/claims/job-research-7f91748e5f9d004b.json`
- `DOI:10.1109/EEI70303.2026.11640499` — PMKS: Co-Designing Distributed Networking and Multi-Tier Storage for Ultra-Long Context LLM Inference / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-1edac6e56714dd58.json`
- `DOI:10.1109/CCGrid68966.2026.00023` — LLM-Pilot: SLO-Aware and Cost-Efficient LLM Serving on Public Cloud VM Clusters via Offloading / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-2efe9f8fbd9f6b33.json`
- `arXiv:2602.01519` — You Need an Encoder for Native Position-Independent Caching / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-4044c82745a32e7d.json`
- `DOI:10.1109/TCSI.2026.3692866` — DSLA: An Energy-Efficient Dual-Sparsity LLM Accelerator With HiMix-BFP / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-64f36119defd4883.json`
- `DOI:10.1007/s44196-026-01236-9` — Consensus-Expert DynamicMoE: ARIMA-based Capacity Prediction with Adaptive Load Balancing for Sparse Models / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-75eff2262d950b6f.json`
- `DOI:10.1109/TMC.2026.3676689` — E²LLM: Structure-Guided Efficient Inference for LLMs in Distributed Edge / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-92841f7f38c00d3c.json`
- `arXiv:2510.03151` — Mixture of Many Zero-Compute Experts: A High-Rate Quantization Theory Perspective / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-b3cb99418924d14e.json`
- `arXiv:2607.01444` — On the Utility and Factual Reliability of Pruned Mixture-of-Experts Models in the Biomedical Domain / worker `worker-925000`
  - claim: **09-25 00:34:18 JST** / heartbeat: **09-25 00:34:18 JST** / lease expiry: **09-25 02:04:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-d5b6de209d3bfef0.json`

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
| inference/training/survey配下の論文Markdown実体 | **1026** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **258** |
| └ Research | **178** |
| └ Audit | **2** |
| └ Discovery | **51** |
| └ Other/Unknown | **27** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **338** |

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
