# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-17 18:10:59 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **51** |
| 未claim Research job | **50** |
| 直近24hの検証済みResearch収録 | **59** |
| 最終検証済みResearch収録 | **09-17 18:10:45 JST（14秒前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **51** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **51** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **21** | **4** | **2** | **2** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **5** | **4** | **4** | **0** | **0** | **0** | **15** |
| 合計 | **26** | **8** | **6** | **2** | **1** | **0** | **15** |

- 最新Discovery runの耐久探索round: **4件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-17 18:10:45 JST** [research] `arXiv:2503.01890` — AutoHete: An Automatic and Efficient Heterogeneous Training System for LLMs
  - job: `.survey/work-queue/jobs/job-research-133abb5ee0382900.json`
  - result: `.survey/work-queue/results/research/attempt-942af3295b1538b54adcfd38.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-942af3295b1538b54adcfd38.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2503.01890-autohete-an-automatic-and-efficient-heterogeneous-training-system-for-llms.md`
- **09-17 18:09:36 JST** [research] `arXiv:2504.08784` — SLOs-Serve: Optimized Serving of Multi-SLO LLMs
  - job: `.survey/work-queue/jobs/job-research-1abdfafeb85e4df9.json`
  - result: `.survey/work-queue/results/research/attempt-61cea03f965b827a2ed92932.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-61cea03f965b827a2ed92932.json`
  - paper: `papers/inference/06-serving-scheduling/2025-2504.08784-slos-serve-multi-slo-llm-serving.md`
- **09-17 17:20:24 JST** [research] `arXiv:2401.02669` — Infinite-LLM: Efficient LLM Service for Long Context with DistAttention and Distributed KVCache
  - job: `.survey/work-queue/jobs/job-research-3dcfddcaf0f956d5.json`
  - result: `.survey/work-queue/results/research/attempt-f73b2644bb575cea292a8186.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f73b2644bb575cea292a8186.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2401.02669-infinite-llm-distattention-distributed-kvcache.md`
- **09-17 17:17:05 JST** [research] `arXiv:2504.20068` — JITServe: SLO-aware LLM Serving with Imprecise Request Information
  - job: `.survey/work-queue/jobs/job-research-491d6cc11a36da8c.json`
  - result: `.survey/work-queue/results/research/attempt-af95b58e929cbe887fc76bfd.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-af95b58e929cbe887fc76bfd.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2504.20068-jitserve-slo-aware-llm-serving-with-imprecise-request-information.md`
- **09-17 17:13:45 JST** [research] `arXiv:2504.19867` — semi-PD: Towards Efficient LLM Serving via Phase-Wise Disaggregated Computation and Unified Storage
  - job: `.survey/work-queue/jobs/job-research-0923832e7cd03d20.json`
  - result: `.survey/work-queue/results/research/attempt-180764ce53bd95c132164263.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-180764ce53bd95c132164263.json`
  - paper: `papers/inference/06-serving-scheduling/2025-2504.19867-semi-pd-phase-wise-disaggregated-unified-storage.md`
- **09-17 17:10:30 JST** [research] `arXiv:2508.06526` — PiKV: KV Cache Management System for Mixture of Experts
  - job: `.survey/work-queue/jobs/job-research-6b9319ad56fb236d.json`
  - result: `.survey/work-queue/results/research/attempt-366e50017f388aac9c576b49.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-366e50017f388aac9c576b49.json`
  - paper: `papers/inference/05-moe/2025-2508.06526-pikv-kv-cache-management-for-mixture-of-experts.md`
- **09-17 16:41:43 JST** [research] `arXiv:2601.19278` — DART: Diffusion-Inspired Speculative Decoding for Fast LLM Inference
  - job: `.survey/work-queue/jobs/job-research-bf0b422fe6562f5b.json`
  - result: `.survey/work-queue/results/research/attempt-d138fd01aeed0094d3129bad.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d138fd01aeed0094d3129bad.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2601.19278-dart-diffusion-inspired-speculative-decoding-for-fast-llm-inference.md`
- **09-17 16:39:31 JST** [research] `arXiv:2602.02108` — Out of the Memory Barrier: A Highly Memory Efficient Training System for LLMs with Million-Token Contexts
  - job: `.survey/work-queue/jobs/job-research-7f3f089c5dc01c0c.json`
  - result: `.survey/work-queue/results/research/attempt-78cb43ce4509a618c85127b5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-78cb43ce4509a618c85127b5.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2602.02108-out-of-the-memory-barrier-a-highly-memory-efficient-training-system-for-llms-with-million-token-contexts.md`
- **09-17 15:44:33 JST** [research] `arXiv:2609.17008` — FlexEE: Self-Speculative and KV-Compatible Early Exiting for Offloading-Aware LLM Inference
  - job: `.survey/work-queue/jobs/job-research-ee19ffd9b6b00e19.json`
  - result: `.survey/work-queue/results/research/attempt-ddc2745db0f900abfd7bf01e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ddc2745db0f900abfd7bf01e.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.17008-flexee-self-speculative-and-kv-compatible-early-exiting-for-offloading-aware-llm-inference.md`
- **09-17 15:40:17 JST** [research] `arXiv:2609.14507` — Physically Partitioned KVCache Format for CPU--GPU Load Balancing in MoE Inference
  - job: `.survey/work-queue/jobs/job-research-05978e704eaf8286.json`
  - result: `.survey/work-queue/results/research/attempt-81cca2a745d2540e0c24bc47.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-81cca2a745d2540e0c24bc47.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.14507-physically-partitioned-kvcache-format-for-cpu-gpu-load-balancing-in-moe-inference.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-17 15:01:06 JST** job `job-e45c04a3ba21f09c` / 候補 **4件**
  - result: `.survey/work-queue/results/20260917T1459JST-discovery-unrepresented-memory-systems-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T1459JST-discovery-unrepresented-memory-systems-1.json`
  - 探索軸: fresh-and-adjacent-memory-offload-kv-systems
- **09-17 15:03:27 JST** job `job-5c8ea8ca705a9ecb` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T1512JST-discovery-speculative-decoding-gaps-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T1512JST-discovery-speculative-decoding-gaps-2.json`
  - 探索軸: speculative-decoding-system-coverage-gaps
- **09-17 15:03:34 JST** job `job-eec5ff8f364687d4` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T1521JST-discovery-training-memory-systems-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T1521JST-discovery-training-memory-systems-3.json`
  - 探索軸: training-offload-checkpoint-storage-gaps
- **09-17 15:04:08 JST** job `job-5041f5c489f0e9c8` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T1528JST-discovery-disaggregation-evaluation-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T1528JST-discovery-disaggregation-evaluation-4.json`
  - 探索軸: distributed-serving-network-and-disaggregation-gaps
- **09-17 13:41:46 JST** job `job-2910aab086edc06c` / 候補 **5件**
  - result: `.survey/work-queue/results/20260917T1340JST-discovery-sep15-inference-systems-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T1340JST-discovery-sep15-inference-systems-1.json`
  - 探索軸: fresh-arxiv-sep15-inference-systems

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-17 18:00 JST** / worker `scheduled-chat-discovery-specialist-20260917T1800JST`
- immutable submission: **4件** / 検証済み成功: **2件** / 未完了・未検証: **2件**
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-4fd8bb83ad560a14ed7ab9fd.json` (job `job-research-6be1741cdc42b913`)
- **成功** `arXiv:2504.08784` — SLOs-Serve: Optimized Serving of Multi-SLO LLMs
  - job: `.survey/work-queue/jobs/job-research-1abdfafeb85e4df9.json`
  - result: `.survey/work-queue/results/research/attempt-61cea03f965b827a2ed92932.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-61cea03f965b827a2ed92932.json`
  - paper: `papers/inference/06-serving-scheduling/2025-2504.08784-slos-serve-multi-slo-llm-serving.md`
- **成功** `arXiv:2503.01890` — AutoHete: An Automatic and Efficient Heterogeneous Training System for LLMs
  - job: `.survey/work-queue/jobs/job-research-133abb5ee0382900.json`
  - result: `.survey/work-queue/results/research/attempt-942af3295b1538b54adcfd38.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-942af3295b1538b54adcfd38.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2503.01890-autohete-an-automatic-and-efficient-heterogeneous-training-system-for-llms.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-bec0c74881d95eeb32a049cb.json` (job `job-research-1abdfafeb85e4df9`)

#### Audit (:30)

- 最新観測run: **2026-09-17 18:00 JST** / worker `scheduled-chat-discovery-specialist-20260917T1800JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-17 14:00 JST**
- 耐久探索round: **4件** / immutable submission: **4件** / 検証済み成功result: **4件** / 個別result照合: **4件** / 個別result未照合: **0件** / 候補: **15件**
- 探索軸: fresh-and-adjacent-memory-offload-kv-systems / speculative-decoding-system-coverage-gaps / training-offload-checkpoint-storage-gaps / distributed-serving-network-and-disaggregation-gaps
- round `unrepresented-memory-systems-1` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/20260917T1459JST-discovery-unrepresented-memory-systems-1.json`
  - 探索軸: fresh-and-adjacent-memory-offload-kv-systems
  - 個別result照合: あり / `.survey/work-queue/results/20260917T1459JST-discovery-unrepresented-memory-systems-1.json` (`ok=true`)
- round `speculative-decoding-gaps-2` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260917T1512JST-discovery-speculative-decoding-gaps-2.json`
  - 探索軸: speculative-decoding-system-coverage-gaps
  - 個別result照合: あり / `.survey/work-queue/results/20260917T1512JST-discovery-speculative-decoding-gaps-2.json` (`ok=true`)
- round `training-memory-systems-3` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260917T1521JST-discovery-training-memory-systems-3.json`
  - 探索軸: training-offload-checkpoint-storage-gaps
  - 個別result照合: あり / `.survey/work-queue/results/20260917T1521JST-discovery-training-memory-systems-3.json` (`ok=true`)
- round `disaggregation-evaluation-4` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260917T1528JST-discovery-disaggregation-evaluation-4.json`
  - 探索軸: distributed-serving-network-and-disaggregation-gaps
  - 個別result照合: あり / `.survey/work-queue/results/20260917T1528JST-discovery-disaggregation-evaluation-4.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2609.14138` — LIMBO: Lifelong Inference-Time Memory and Budget Optimization for LLM Agents / worker `scheduled-chat-discovery-specialist-20260917T1700JST`
  - claim: **09-17 17:16:22 JST** / heartbeat: **09-17 17:28:54 JST** / lease expiry: **09-17 18:58:54 JST**
  - evidence: `.survey/work-queue/claims/job-research-ce95464a254235a3.json`

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
| ready | **51** |

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
| inference/training/survey配下の論文Markdown実体 | **668** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **439** |
| └ Research | **312** |
| └ Audit | **2** |
| └ Discovery | **125** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。 旧形式のDiscovery submissionが `invalid submit_discovery_round payload` で失敗した履歴は、そのsubmission内の全candidateが現在のjobまたはpaper identity indexで確認できる場合に限り、履歴として保持したまま現在の異常から除外します。

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
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
