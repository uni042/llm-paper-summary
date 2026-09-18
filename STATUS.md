# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-18 22:04:44 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **55** |
| 未claim Research job | **55** |
| 直近24hの検証済みResearch収録 | **41** |
| 最終検証済みResearch収録 | **09-18 21:43:39 JST（21分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **55** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **55** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **10** | **4** | **2** | **2** | **0** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **23** | **9** | **8** | **1** | **0** | **0** | **2** |
| 合計 | **33** | **13** | **10** | **3** | **0** | **0** | **2** |

- 最新Discovery runの耐久探索round: **9件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-18 21:43:39 JST** [research] `arXiv:2609.17983` — Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits
  - job: `.survey/work-queue/jobs/job-research-326d710987e96b1f.json`
  - result: `.survey/work-queue/results/research/attempt-67c677bdf0613551686265c8-repair1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-67c677bdf0613551686265c8-repair1.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md`
- **09-18 21:39:01 JST** [research] `arXiv:2609.14717` — Carryover Drafting: Recycling Rejected States for Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-3736e6c195a4f8a9.json`
  - result: `.survey/work-queue/results/research/attempt-b8073f0637a56eac35f5c473-repair1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b8073f0637a56eac35f5c473-repair1.json`
  - paper: `papers/inference/06-speculative-decoding/2026-2609.14717-carryover-drafting-recycling-rejected-states.md`
- **09-18 21:34:16 JST** [research] `arXiv:2608.11668` — A Full-Stack Characterization of High-Bandwidth Flash for KV-Centric LLM Serving
  - job: `.survey/work-queue/jobs/job-research-7fcd5e4f3604dab7.json`
  - result: `.survey/work-queue/results/research/attempt-292079eab3cc522a1a9de5d7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-292079eab3cc522a1a9de5d7.json`
  - paper: `papers/inference/05-offload-hierarchical-memory/2026-2608.11668-high-bandwidth-flash-kv-serving-characterization.md`
- **09-18 21:08:10 JST** [research] `arXiv:2608.19662` — ReCache: Efficient KV Cache Reuse and Compression for Tool-Augmented LLM Agents
  - job: `.survey/work-queue/jobs/job-research-abd379cf035bd8f0.json`
  - result: `.survey/work-queue/results/research/attempt-8bc32c98f4efa2a4da6345d3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8bc32c98f4efa2a4da6345d3.json`
  - paper: `papers/inference/kv-cache/2608.19662.md`
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

- **09-18 21:59:34 JST** job `job-bfe6701d4307a48c` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T2157JST-discovery-specialist-speculative-cosine-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2157JST-discovery-specialist-speculative-cosine-1.json`
  - 探索軸: 分散speculative inference・heterogeneous drafter orchestration
- **09-18 22:00:01 JST** job `job-17d06195f049b5ad` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T2202JST-discovery-specialist-swiftspec-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2202JST-discovery-specialist-swiftspec-2.json`
  - 探索軸: 非同期speculative decoding・tensor parallel・KV/kernel co-design
- **09-18 22:00:08 JST** job `job-38610c3f6ec1d1a2` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2205JST-discovery-specialist-cxl-kv-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2205JST-discovery-specialist-cxl-kv-3.json`
  - 探索軸: CXL・KV cache memory disaggregation・PNM/FPGA
- **09-18 22:00:35 JST** job `job-347fd1674f143577` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2206JST-discovery-specialist-moe-edge-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2206JST-discovery-specialist-moe-edge-4.json`
  - 探索軸: MoE expert offload・cacheless edge-distributed inference
- **09-18 22:00:44 JST** job `job-e6e1156d52f4ec20` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2207JST-discovery-specialist-network-kv-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2207JST-discovery-specialist-network-kv-5.json`
  - 探索軸: RDMA・KV transfer・disaggregated serving networking
- **09-18 22:01:21 JST** job `job-13db76269ce893af` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2208JST-discovery-specialist-agent-kv-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2208JST-discovery-specialist-agent-kv-6.json`
  - 探索軸: agentic serving・tool-call progress・KV lifecycle
- **09-18 22:01:30 JST** job `job-8045b60ddcfce5d3` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2209JST-discovery-specialist-fairness-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2209JST-discovery-specialist-fairness-7.json`
  - 探索軸: multi-tenant serving・token latency fairness・SLO isolation
- **09-18 22:01:40 JST** job `job-a8a74b6ff1e39445` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T2212JST-discovery-specialist-gpu-runtime-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2212JST-discovery-specialist-gpu-runtime-8.json`
  - 探索軸: GPU runtime・persistent kernel・CUDA Graph・JIT compilation
- **09-18 20:02:46 JST** job `job-fb6e71b1d7480608` / 候補 **5件**
  - result: `.survey/work-queue/results/20260918T2001JST-discovery-specialist-memory-specdecode-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2001JST-discovery-specialist-memory-specdecode-1.json`
  - 探索軸: UVM oversubscription・投機的復号state reuse・stale KV repair
- **09-18 20:03:17 JST** job `job-500decdb4fb2421b` / 候補 **4件**
  - result: `.survey/work-queue/results/20260918T2008JST-discovery-specialist-serving-measurement-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T2008JST-discovery-specialist-serving-measurement-2.json`
  - 探索軸: serving measurement・replicated KV correctness・production workflow・MoE routing prediction

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-18 21:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **4件** / 検証済み成功: **2件** / 未完了・未検証: **2件**
- **成功** `arXiv:2609.17983` — Contiguity, Not Importance: Budgeted Repair of Stale KV Caches After Document Edits
  - job: `.survey/work-queue/jobs/job-research-326d710987e96b1f.json`
  - result: `.survey/work-queue/results/research/attempt-67c677bdf0613551686265c8-repair1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-67c677bdf0613551686265c8-repair1.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.17983-contiguity-budgeted-repair-stale-kv-cache.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-67c677bdf0613551686265c8.json` (job `job-research-326d710987e96b1f`)
- **成功** `arXiv:2609.14717` — Carryover Drafting: Recycling Rejected States for Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-3736e6c195a4f8a9.json`
  - result: `.survey/work-queue/results/research/attempt-b8073f0637a56eac35f5c473-repair1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b8073f0637a56eac35f5c473-repair1.json`
  - paper: `papers/inference/06-speculative-decoding/2026-2609.14717-carryover-drafting-recycling-rejected-states.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-b8073f0637a56eac35f5c473.json` (job `job-research-3736e6c195a4f8a9`)

#### Audit (:30)

- 最新観測run: **2026-09-18 21:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-18 21:00 JST**
- 耐久探索round: **9件** / immutable submission: **9件** / 検証済み成功result: **8件** / 個別result照合: **8件** / 個別result未照合: **1件** / 候補: **2件**
- 探索軸: 分散speculative inference・heterogeneous drafter orchestration / 非同期speculative decoding・tensor parallel・KV/kernel co-design / CXL・KV cache memory disaggregation・PNM/FPGA / MoE expert offload・cacheless edge-distributed inference / RDMA・KV transfer・disaggregated serving networking / agentic serving・tool-call progress・KV lifecycle / multi-tenant serving・token latency fairness・SLO isolation / GPU runtime・persistent kernel・CUDA Graph・JIT compilation / 2026-09-17以降の新着差分・arXiv 2609後半
- round `specialist-speculative-cosine-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260918T2157JST-discovery-specialist-speculative-cosine-1.json`
  - 探索軸: 分散speculative inference・heterogeneous drafter orchestration
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2157JST-discovery-specialist-speculative-cosine-1.json` (`ok=true`)
- round `specialist-swiftspec-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260918T2202JST-discovery-specialist-swiftspec-2.json`
  - 探索軸: 非同期speculative decoding・tensor parallel・KV/kernel co-design
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2202JST-discovery-specialist-swiftspec-2.json` (`ok=true`)
- round `specialist-cxl-kv-3` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2205JST-discovery-specialist-cxl-kv-3.json`
  - 探索軸: CXL・KV cache memory disaggregation・PNM/FPGA
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2205JST-discovery-specialist-cxl-kv-3.json` (`ok=true`)
- round `specialist-moe-edge-4` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2206JST-discovery-specialist-moe-edge-4.json`
  - 探索軸: MoE expert offload・cacheless edge-distributed inference
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2206JST-discovery-specialist-moe-edge-4.json` (`ok=true`)
- round `specialist-network-kv-5` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2207JST-discovery-specialist-network-kv-5.json`
  - 探索軸: RDMA・KV transfer・disaggregated serving networking
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2207JST-discovery-specialist-network-kv-5.json` (`ok=true`)
- round `specialist-agent-kv-6` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2208JST-discovery-specialist-agent-kv-6.json`
  - 探索軸: agentic serving・tool-call progress・KV lifecycle
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2208JST-discovery-specialist-agent-kv-6.json` (`ok=true`)
- round `specialist-fairness-7` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2209JST-discovery-specialist-fairness-7.json`
  - 探索軸: multi-tenant serving・token latency fairness・SLO isolation
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2209JST-discovery-specialist-fairness-7.json` (`ok=true`)
- round `specialist-gpu-runtime-8` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2212JST-discovery-specialist-gpu-runtime-8.json`
  - 探索軸: GPU runtime・persistent kernel・CUDA Graph・JIT compilation
  - 個別result照合: あり / `.survey/work-queue/results/20260918T2212JST-discovery-specialist-gpu-runtime-8.json` (`ok=true`)
- round `specialist-new-arrivals-9` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260918T2215JST-discovery-specialist-new-arrivals-9.json`
  - 探索軸: 2026-09-17以降の新着差分・arXiv 2609後半
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

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
| ready | **55** |

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
| inference/training/survey配下の論文Markdown実体 | **718** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **527** |
| └ Research | **397** |
| └ Audit | **2** |
| └ Discovery | **128** |

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
