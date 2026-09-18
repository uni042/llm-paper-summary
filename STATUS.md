# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-18 21:05:32 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **52** |
| 未claim Research job | **51** |
| 直近24hの検証済みResearch収録 | **37** |
| 最終検証済みResearch収録 | **09-18 19:06:47 JST（1時間58分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **52** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **52** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **6** | **2** | **2** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **22** | **11** | **11** | **0** | **0** | **0** | **14** |
| 合計 | **28** | **13** | **13** | **0** | **1** | **0** | **14** |

- 最新Discovery runの耐久探索round: **11件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-18 19:06:47 JST** [research] `arXiv:2406.19707` — InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management
  - job: `.survey/work-queue/jobs/job-research-2afdd6d968c4500a.json`
  - result: `.survey/work-queue/results/research/attempt-7ff67242dae88bb287c5c390.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-7ff67242dae88bb287c5c390.json`
  - paper: `papers/inference/06-kv-cache-memory/2024-2406.19707-infinigen-dynamic-kv-cache-management.md`
- **09-18 18:12:03 JST** [research] `arXiv:2604.10907` — RouterWise: Joint Resource Allocation and Routing for Latency-Aware Multi-Model LLM Serving
  - job: `.survey/work-queue/jobs/job-research-fbee62800783475d.json`
  - result: `.survey/work-queue/results/research/attempt-c077ca2784f3c91498be745d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c077ca2784f3c91498be745d.json`
  - paper: `papers/inference/06-serving-scheduling/2026-2604.10907-routerwise-resource-allocation-routing.md`
- **09-18 18:06:53 JST** [research] `arXiv:2407.05858` — Fast On-device LLM Inference with NPUs
  - job: `.survey/work-queue/jobs/job-research-23f0e2222a013ba4.json`
  - result: `.survey/work-queue/results/research/attempt-4854b5c1592585d0d8ecaae7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4854b5c1592585d0d8ecaae7.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2024-2407.05858-fast-on-device-llm-inference-with-npus.md`
- **09-18 18:02:43 JST** [research] `arXiv:2503.09716` — MoE-Gen: High-Throughput MoE Inference on a Single GPU with Module-Based Batching
  - job: `.survey/work-queue/jobs/job-research-e4eebc0f5643e0fd.json`
  - result: `.survey/work-queue/results/research/attempt-70bc34fb123b636715b220f9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-70bc34fb123b636715b220f9.json`
  - paper: `papers/inference/02-moe-inference/2025-2503.09716-moe-gen-module-based-batching.md`
- **09-18 16:41:52 JST** [research] `arXiv:2607.02525` — PEEK: Predictive Queue-Informed KV Cache Management for LLM Serving
  - job: `.survey/work-queue/jobs/job-research-455581782889dbd1.json`
  - result: `.survey/work-queue/results/research/attempt-71d88f013604453cc1c44327.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-71d88f013604453cc1c44327.json`
  - paper: `papers/inference/scheduling/2607.02525.md`
- **09-18 16:36:00 JST** [research] `arXiv:2609.14643` — BigMoMo: Efficient Inference of Large-Scale MoE with Speculative Decoding on Mobile Devices
  - job: `.survey/work-queue/jobs/job-research-61cb466957462432.json`
  - result: `.survey/work-queue/results/research/attempt-5e14ce9ab5f740202d8cecb7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5e14ce9ab5f740202d8cecb7.json`
  - paper: `papers/inference/moe/2609.14643.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-18 20:02:46 JST** job `job-fb6e71b1d7480608` / 候補 **5件**
  - result: `.survey/work-queue/results/20260918T2001JST-discovery-specialist-memory-specdecode-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2001JST-discovery-specialist-memory-specdecode-1.json`
  - 探索軸: UVM oversubscription・投機的復号state reuse・stale KV repair
- **09-18 20:03:17 JST** job `job-500decdb4fb2421b` / 候補 **4件**
  - result: `.survey/work-queue/results/20260918T2008JST-discovery-specialist-serving-measurement-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2008JST-discovery-specialist-serving-measurement-2.json`
  - 探索軸: serving measurement・replicated KV correctness・production workflow・MoE routing prediction
- **09-18 20:05:47 JST** job `job-86a761ccdc72a4aa` / 候補 **4件**
  - result: `.survey/work-queue/results/20260918T2014JST-discovery-specialist-august-systems-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2014JST-discovery-specialist-august-systems-3.json`
  - 探索軸: 2026年8月のHBF・power-aware serving・RAG runtime・agentic production workload
- **09-18 20:05:53 JST** job `job-262b4d80e25831ae` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2021JST-discovery-specialist-2025-memory-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2021JST-discovery-specialist-2025-memory-4.json`
  - 探索軸: 2025 expert prefetch・distributed prefix cache・multi-GPU KV・SSD offload
- **09-18 20:06:00 JST** job `job-e898bc3612b44242` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2025JST-discovery-specialist-kv-remap-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2025JST-discovery-specialist-kv-remap-5.json`
  - 探索軸: 2025 KV parameter remapping・CPU-light offload・multi-tenant memory
- **09-18 20:06:07 JST** job `job-71af74bc26ccde14` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T2029JST-discovery-specialist-cxl-edram-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2029JST-discovery-specialist-cxl-edram-6.json`
  - 探索軸: CXL rack-scale KV transport・eDRAM KV co-design・edge memory
- **09-18 20:06:13 JST** job `job-905a3cc1e83641b8` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2033JST-discovery-specialist-legacy-cache-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2033JST-discovery-specialist-legacy-cache-7.json`
  - 探索軸: 2024 personal-machine MoE cache・2025 multimodal KV compression serving
- **09-18 20:06:20 JST** job `job-c804efd389c67ae1` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2036JST-discovery-specialist-network-kv-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2036JST-discovery-specialist-network-kv-8.json`
  - 探索軸: distributed KV networking・SmartNIC・CXL transfer
- **09-18 20:06:27 JST** job `job-9231fb439db812a1` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2038JST-discovery-specialist-scheduling-saturation-9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2038JST-discovery-specialist-scheduling-saturation-9.json`
  - 探索軸: operator autoscaling・SLO-aware scheduling・phase-aware power control
- **09-18 20:06:34 JST** job `job-6812e2190fca4972` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2040JST-discovery-specialist-specdecode-saturation-10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2040JST-discovery-specialist-specdecode-saturation-10.json`
  - 探索軸: 最新batched speculative decoding・VLM block drafting・KV repair

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-18 16:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **2件** / 検証済み成功: **2件** / 未完了・未検証: **0件**
- **成功** `arXiv:2609.14643` — BigMoMo: Efficient Inference of Large-Scale MoE with Speculative Decoding on Mobile Devices
  - job: `.survey/work-queue/jobs/job-research-61cb466957462432.json`
  - result: `.survey/work-queue/results/research/attempt-5e14ce9ab5f740202d8cecb7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5e14ce9ab5f740202d8cecb7.json`
  - paper: `papers/inference/moe/2609.14643.md`
- **成功** `arXiv:2607.02525` — PEEK: Predictive Queue-Informed KV Cache Management for LLM Serving
  - job: `.survey/work-queue/jobs/job-research-455581782889dbd1.json`
  - result: `.survey/work-queue/results/research/attempt-71d88f013604453cc1c44327.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-71d88f013604453cc1c44327.json`
  - paper: `papers/inference/scheduling/2607.02525.md`

#### Audit (:30)

- 最新観測run: **2026-09-18 16:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-18 20:00 JST**
- 耐久探索round: **11件** / immutable submission: **11件** / 検証済み成功result: **11件** / 個別result照合: **11件** / 個別result未照合: **0件** / 候補: **14件**
- 探索軸: UVM oversubscription・投機的復号state reuse・stale KV repair / serving measurement・replicated KV correctness・production workflow・MoE routing prediction / 2026年8月のHBF・power-aware serving・RAG runtime・agentic production workload / 2025 expert prefetch・distributed prefix cache・multi-GPU KV・SSD offload / 2025 KV parameter remapping・CPU-light offload・multi-tenant memory / CXL rack-scale KV transport・eDRAM KV co-design・edge memory / 2024 personal-machine MoE cache・2025 multimodal KV compression serving / distributed KV networking・SmartNIC・CXL transfer / operator autoscaling・SLO-aware scheduling・phase-aware power control / 最新batched speculative decoding・VLM block drafting・KV repair / 2026前半SmartSSD・MoE speculative expert・CPU-free SmartNIC・NVL72 remote expert
- round `specialist-memory-specdecode-1` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260918T2001JST-discovery-specialist-memory-specdecode-1.json`
  - 探索軸: UVM oversubscription・投機的復号state reuse・stale KV repair
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2001JST-discovery-specialist-memory-specdecode-1.json` (`ok=true`)
- round `specialist-serving-measurement-2` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/20260918T2008JST-discovery-specialist-serving-measurement-2.json`
  - 探索軸: serving measurement・replicated KV correctness・production workflow・MoE routing prediction
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2008JST-discovery-specialist-serving-measurement-2.json` (`ok=true`)
- round `specialist-august-systems-3` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/20260918T2014JST-discovery-specialist-august-systems-3.json`
  - 探索軸: 2026年8月のHBF・power-aware serving・RAG runtime・agentic production workload
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2014JST-discovery-specialist-august-systems-3.json` (`ok=true`)
- round `specialist-2025-memory-4` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2021JST-discovery-specialist-2025-memory-4.json`
  - 探索軸: 2025 expert prefetch・distributed prefix cache・multi-GPU KV・SSD offload
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2021JST-discovery-specialist-2025-memory-4.json` (`ok=true`)
- round `specialist-kv-remap-5` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2025JST-discovery-specialist-kv-remap-5.json`
  - 探索軸: 2025 KV parameter remapping・CPU-light offload・multi-tenant memory
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2025JST-discovery-specialist-kv-remap-5.json` (`ok=true`)
- round `specialist-cxl-edram-6` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260918T2029JST-discovery-specialist-cxl-edram-6.json`
  - 探索軸: CXL rack-scale KV transport・eDRAM KV co-design・edge memory
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2029JST-discovery-specialist-cxl-edram-6.json` (`ok=true`)
- round `specialist-legacy-cache-7` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2033JST-discovery-specialist-legacy-cache-7.json`
  - 探索軸: 2024 personal-machine MoE cache・2025 multimodal KV compression serving
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2033JST-discovery-specialist-legacy-cache-7.json` (`ok=true`)
- round `specialist-network-kv-8` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2036JST-discovery-specialist-network-kv-8.json`
  - 探索軸: distributed KV networking・SmartNIC・CXL transfer
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2036JST-discovery-specialist-network-kv-8.json` (`ok=true`)
- round `specialist-scheduling-saturation-9` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2038JST-discovery-specialist-scheduling-saturation-9.json`
  - 探索軸: operator autoscaling・SLO-aware scheduling・phase-aware power control
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2038JST-discovery-specialist-scheduling-saturation-9.json` (`ok=true`)
- round `specialist-specdecode-saturation-10` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2040JST-discovery-specialist-specdecode-saturation-10.json`
  - 探索軸: 最新batched speculative decoding・VLM block drafting・KV repair
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2040JST-discovery-specialist-specdecode-saturation-10.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2608.11668` — A Full-Stack Characterization of High-Bandwidth Flash for KV-Centric LLM Serving / worker `scheduled-chat-llm-survey`
  - claim: **09-18 20:28:41 JST** / heartbeat: **—** / lease expiry: **09-18 21:58:41 JST**
  - evidence: `.survey/work-queue/claims/job-research-7fcd5e4f3604dab7.json`

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
| ready | **52** |

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
| inference/training/survey配下の論文Markdown実体 | **714** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **524** |
| └ Research | **395** |
| └ Audit | **2** |
| └ Discovery | **127** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

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
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
