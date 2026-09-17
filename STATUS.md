# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-17 20:34:14 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **45** |
| 未claim Research job | **44** |
| 直近24hの検証済みResearch収録 | **56** |
| 最終検証済みResearch収録 | **09-17 19:33:27 JST（1時間0分前）** |
| 整合性異常 | **2** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **45** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **45** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **17** | **1** | **0** | **1** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **4** | **2** | **0** | **2** | **0** | **0** | **7** |
| 合計 | **21** | **3** | **0** | **3** | **1** | **0** | **7** |

- 最新Discovery runの耐久探索round: **2件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-17 19:33:27 JST** [research] `arXiv:2609.14138` — LIMBO: Lifelong Inference-Time Memory and Budget Optimization for LLM Agents
  - job: `.survey/work-queue/jobs/job-research-ce95464a254235a3.json`
  - result: `.survey/work-queue/results/research/attempt-a7d7a47efa9628566d9ffaf7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a7d7a47efa9628566d9ffaf7.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.14138-limbo-lifelong-inference-time-memory-and-budget-optimization-for-llm-agents.md`
- **09-17 18:53:44 JST** [research] `arXiv:2505.11329` — TokenWeave: Efficient Compute-Communication Overlap for Distributed LLM Inference
  - job: `.survey/work-queue/jobs/job-research-a1f4ccc94cf94fe5.json`
  - result: `.survey/work-queue/results/research/attempt-2d17d81f9fcb9ead4849e591.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2d17d81f9fcb9ead4849e591.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2505.11329-tokenweave-efficient-compute-communication-overlap-for-distributed-llm-inference.md`
- **09-17 18:42:36 JST** [research] `arXiv:2504.17584` — CHIME: A Case for Efficient Long-Context Attention-FC Disaggregated Inference with DIMM-PIM
  - job: `.survey/work-queue/jobs/job-research-581beb5301e2ddf8.json`
  - result: `.survey/work-queue/results/research/attempt-797276fcf739302b269d6e80.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-797276fcf739302b269d6e80.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2504.17584-chime-a-case-for-efficient-long-context-attention-fc-disaggregated-inference-with-dimm-pim.md`
- **09-17 18:41:37 JST** [research] `arXiv:2501.12162` — AdaServe: Accelerating Multi-SLO LLM Serving with SLO-Customized Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-8423392e3664b697.json`
  - result: `.survey/work-queue/results/research/attempt-af88b7967bb739f0955daaa6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-af88b7967bb739f0955daaa6.json`
  - paper: `papers/inference/06-serving-scheduling/2025-2501.12162-adaserve-multi-slo-speculative-serving.md`
- **09-17 18:35:47 JST** [research] `arXiv:2607.27090` — InferScale: GPU-Native KV Injection for Personalized LLM Serving
  - job: `.survey/work-queue/jobs/job-research-010509dfee08b6d5.json`
  - result: `.survey/work-queue/results/research/attempt-a6d9e761f99fd071c0489cca.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a6d9e761f99fd071c0489cca.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2607.27090-inferscale-gpu-native-kv-injection.md`
- **09-17 18:15:48 JST** [research] `arXiv:2507.09201` — SLIM: A Heterogeneous Accelerator for Edge Inference of Sparse Large Language Model via Adaptive Thresholding
  - job: `.survey/work-queue/jobs/job-research-e79ef27915573b54.json`
  - result: `.survey/work-queue/results/research/attempt-7c0239753483c2ddf4304e18.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-7c0239753483c2ddf4304e18.json`
  - paper: `papers/inference/04-cpu-ssd-offload/2025-2507.09201-slim-near-storage-pim-sparse-edge-inference.md`
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

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-17 20:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **1件** / 検証済み成功: **0件** / 未完了・未検証: **1件**
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-7d9e9117902e3933bb8ea91d.json` (job `job-research-0b1a3df137cd07ea`)

#### Audit (:30)

- 最新観測run: **2026-09-17 20:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-17 20:00 JST**
- 耐久探索round: **2件** / immutable submission: **2件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **2件** / 候補: **7件**
- 探索軸: disaggregated serving・CXL/PIM・SSD-backed KV cache / LLM inference memory・KV cache・MoE expert offload/prefetch
- round `specialist-disagg-cxl-2` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/2026-09-17T20-00-00+09-00-specialist-disagg-cxl-2.json`
  - 探索軸: disaggregated serving・CXL/PIM・SSD-backed KV cache
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-systems-memory-1` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/2026-09-17T20-00-00+09-00-specialist-systems-memory-1.json`
  - 探索軸: LLM inference memory・KV cache・MoE expert offload/prefetch
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2406.08334` — ProTrain: Efficient LLM Training via Memory-Aware Techniques / worker `scheduled-chat-llm-survey`
  - claim: **09-17 20:33:59 JST** / heartbeat: **—** / lease expiry: **09-17 22:03:59 JST**
  - evidence: `.survey/work-queue/claims/job-research-5862dce444505150.json`

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
| ready | **45** |

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
| inference/training/survey配下の論文Markdown実体 | **674** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **447** |
| └ Research | **318** |
| └ Audit | **2** |
| └ Discovery | **125** |
| └ Other/Unknown | **2** |

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
| 対応jobなしsubmission（有効Discovery round除外） | **2** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **2** |

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
