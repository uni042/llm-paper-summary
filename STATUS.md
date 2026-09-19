# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 21:36:12 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **50** |
| 未claim Research job | **49** |
| 直近24hの検証済みResearch収録 | **44** |
| 最終検証済みResearch収録 | **09-19 21:36:08 JST（4秒前）** |
| 整合性異常 | **4** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **50** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **50** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **8** | **3** | **2** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **55** | **8** | **8** | **0** | **0** | **0** | **16** |
| 合計 | **63** | **11** | **10** | **0** | **1** | **0** | **16** |

- 最新Discovery runの耐久探索round: **8件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-19 21:36:08 JST** [research] `arXiv:2607.02942` — Serving Agentic Workflows with a Physical-Plan Compiler and Adaptive Runtime
  - job: `.survey/work-queue/jobs/job-research-bf442cee1726bee0.json`
  - result: `.survey/work-queue/results/research/attempt-df7f245a6a689a36570a6d97.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-df7f245a6a689a36570a6d97.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2607.02942-dyserve-agentic-physical-plan-runtime.md`
- **09-19 19:34:56 JST** [research] `arXiv:2604.15186` — Scepsy: Serving Agentic Workflows Using Aggregate LLM Pipelines
  - job: `.survey/work-queue/jobs/job-research-188f6649e816eaae.json`
  - result: `.survey/work-queue/results/research/attempt-cd9ea16c565464e02e01a24b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cd9ea16c565464e02e01a24b.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2604.15186-scepsy-serving-agentic-workflows-using-aggregate-llm-pipelines.md`
- **09-19 19:34:03 JST** [research] `arXiv:2410.01228` — ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving
  - job: `.survey/work-queue/jobs/job-research-b6a4fe55f122cf41.json`
  - result: `.survey/work-queue/results/research/attempt-ff20bcaca705be66e1a1b76e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ff20bcaca705be66e1a1b76e.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2410.01228-conserve-fine-grained-gpu-harvesting-for-llm-online-and-offline-co-serving.md`
- **09-19 18:48:26 JST** [research] `arXiv:2608.08340` — OpRAG: A Resource-Deterministic Runtime for GPU-Backed Multi-Stage RAG Workflows
  - job: `.survey/work-queue/jobs/job-research-ee7c0fc62bdc554b.json`
  - result: `.survey/work-queue/results/research/attempt-a1b38cbb586fe670600b1d26.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a1b38cbb586fe670600b1d26.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2608.08340-oprag-resource-deterministic-rag-runtime.md`
- **09-19 18:43:52 JST** [research] `arXiv:2604.25777` — SpecFed: Accelerating Federated LLM Inference with Speculative Decoding and Compressed Transmission
  - job: `.survey/work-queue/jobs/job-research-c1b7543305e71c40.json`
  - result: `.survey/work-queue/results/research/attempt-cf5ac77834bd3c3ec6c8a715.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cf5ac77834bd3c3ec6c8a715.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2604.25777-specfed-accelerating-federated-llm-inference-with-speculative-decoding-and-compressed-transmission.md`
- **09-19 18:42:15 JST** [research] `arXiv:2401.11240` — CaraServe: CPU-Assisted and Rank-Aware LoRA Serving for Generative LLM Inference
  - job: `.survey/work-queue/jobs/job-research-49ee16176ca66925.json`
  - result: `.survey/work-queue/results/research/attempt-aad8189707bf1017dc2b3caf.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-aad8189707bf1017dc2b3caf.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2401.11240-caraserve-cpu-assisted-lora-serving.md`
- **09-19 18:37:41 JST** [research] `arXiv:2402.01528` — Decoding Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-0e6ed88f587a40d2.json`
  - result: `.survey/work-queue/results/research/attempt-e8ec2848c993c87c9d340e2f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e8ec2848c993c87c9d340e2f.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2402.01528-decoding-speculative-decoding.md`
- **09-19 18:34:04 JST** [research] `arXiv:2602.06072` — PackInfer: Compute- and I/O-Efficient Attention for Batched LLM Inference
  - job: `.survey/work-queue/jobs/job-research-c7f741bd6a7395ee.json`
  - result: `.survey/work-queue/results/research/attempt-35ffcfb18fd8c03e9c06c8cb.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-35ffcfb18fd8c03e9c06c8cb.json`
  - paper: `papers/inference/09-kernel-runtime-compilation/2026-2602.06072-packinfer-batched-attention.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-19 21:04:01 JST** job `job-3cd73ee92069ad52` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-batching-fairness-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-batching-fairness-8.json`
  - 探索軸: resource-fair batching・prefix-aware batching
- **09-19 21:03:23 JST** job `job-1012bfac264d4ba9` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-cxl-expert-replication-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-cxl-expert-replication-6.json`
  - 探索軸: CXL near-data processing・MoE predictive expert replication
- **09-19 21:02:38 JST** job `job-ead12281e8e06aef` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-cxl-flash-moe-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-cxl-flash-moe-5.json`
  - 探索軸: CXL-hybrid KV memory・SSD-backed MoE expert cache
- **09-19 21:02:45 JST** job `job-a42c97f37f2421ce` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-local-runtime-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-local-runtime-4.json`
  - 探索軸: consumer CPU-GPU tensor offload・JIT/CUDA Graph runtime
- **09-19 21:02:52 JST** job `job-7a6ebdb83b96de6c` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-pd-agent-runtime-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-pd-agent-runtime-3.json`
  - 探索軸: disaggregated prefill deflection・agent-aware serving runtime
- **09-19 21:03:00 JST** job `job-d95074768a0a885f` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-runtime-hardware-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-runtime-hardware-2.json`
  - 探索軸: page-aware decode runtime・non-GPU accelerator serving field study
- **09-19 21:03:30 JST** job `job-e32795a218109c68` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-sparse-kv-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-sparse-kv-7.json`
  - 探索軸: retrieval sparse attention・hierarchical KV memory・segment-level KV reuse
- **09-19 21:01:01 JST** job `job-80340174f4bc603a` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T2100JST-discovery-specialist-ssd-moe-routing-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-ssd-moe-routing-1.json`
  - 探索軸: SSD-backed MoE expert streaming・trained routing prediction・expert prefetch
- **09-19 20:01:55 JST** job `job-f01200ff7b9a34ab` / 候補 **4件**
  - result: `.survey/work-queue/results/20260919T2008JST-discovery-specialist-memory-paths-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2008JST-discovery-specialist-memory-paths-1.json`
  - 探索軸: SSD-backed KV・remote-memory direct access・PNM sparse attention・cold MoE memory pooling
- **09-19 20:05:05 JST** job `job-f666c653bd64eec2` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T2015JST-discovery-specialist-energy-heterogeneity-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2015JST-discovery-specialist-energy-heterogeneity-2.json`
  - 探索軸: energy-aware serving・heterogeneous GPU・shared-GPU resource control

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 19:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **3件** / 検証済み成功: **2件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-b5f09b0fdcd071771ee2f21d.json` (job `job-research-ff33bdbdc4dfa309`, failure_class `state_or_transport_guard`)
  - result: `.survey/work-queue/results/research/attempt-b5f09b0fdcd071771ee2f21d.json` (`ok=false`)
- **成功** `arXiv:2604.15186` — Scepsy: Serving Agentic Workflows Using Aggregate LLM Pipelines
  - job: `.survey/work-queue/jobs/job-research-188f6649e816eaae.json`
  - result: `.survey/work-queue/results/research/attempt-cd9ea16c565464e02e01a24b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cd9ea16c565464e02e01a24b.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2604.15186-scepsy-serving-agentic-workflows-using-aggregate-llm-pipelines.md`
- **成功** `arXiv:2410.01228` — ConServe: Fine-Grained GPU Harvesting for LLM Online and Offline Co-Serving
  - job: `.survey/work-queue/jobs/job-research-b6a4fe55f122cf41.json`
  - result: `.survey/work-queue/results/research/attempt-ff20bcaca705be66e1a1b76e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ff20bcaca705be66e1a1b76e.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2410.01228-conserve-fine-grained-gpu-harvesting-for-llm-online-and-offline-co-serving.md`

#### Audit (:30)

- 最新観測run: **2026-09-19 19:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-19 21:00 JST**
- 耐久探索round: **8件** / immutable submission: **8件** / 検証済み成功result: **8件** / 個別result照合: **8件** / 個別result未照合: **0件** / 候補: **16件**
- 探索軸: resource-fair batching・prefix-aware batching / CXL near-data processing・MoE predictive expert replication / CXL-hybrid KV memory・SSD-backed MoE expert cache / consumer CPU-GPU tensor offload・JIT/CUDA Graph runtime / disaggregated prefill deflection・agent-aware serving runtime / page-aware decode runtime・non-GPU accelerator serving field study / retrieval sparse attention・hierarchical KV memory・segment-level KV reuse / SSD-backed MoE expert streaming・trained routing prediction・expert prefetch
- round `specialist-batching-fairness-8` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-batching-fairness-8.json`
  - 探索軸: resource-fair batching・prefix-aware batching
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-batching-fairness-8.json` (`ok=true`)
- round `specialist-cxl-expert-replication-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-cxl-expert-replication-6.json`
  - 探索軸: CXL near-data processing・MoE predictive expert replication
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-cxl-expert-replication-6.json` (`ok=true`)
- round `specialist-cxl-flash-moe-5` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-cxl-flash-moe-5.json`
  - 探索軸: CXL-hybrid KV memory・SSD-backed MoE expert cache
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-cxl-flash-moe-5.json` (`ok=true`)
- round `specialist-local-runtime-4` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-local-runtime-4.json`
  - 探索軸: consumer CPU-GPU tensor offload・JIT/CUDA Graph runtime
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-local-runtime-4.json` (`ok=true`)
- round `specialist-pd-agent-runtime-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-pd-agent-runtime-3.json`
  - 探索軸: disaggregated prefill deflection・agent-aware serving runtime
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-pd-agent-runtime-3.json` (`ok=true`)
- round `specialist-runtime-hardware-2` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-runtime-hardware-2.json`
  - 探索軸: page-aware decode runtime・non-GPU accelerator serving field study
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-runtime-hardware-2.json` (`ok=true`)
- round `specialist-sparse-kv-7` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-sparse-kv-7.json`
  - 探索軸: retrieval sparse attention・hierarchical KV memory・segment-level KV reuse
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-sparse-kv-7.json` (`ok=true`)
- round `specialist-ssd-moe-routing-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T2100JST-discovery-specialist-ssd-moe-routing-1.json`
  - 探索軸: SSD-backed MoE expert streaming・trained routing prediction・expert prefetch
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2100JST-discovery-specialist-ssd-moe-routing-1.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `DOI:10.1145/3797905.3807846` — CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool / worker `scheduled-chat-llm-survey-2130`
  - claim: **09-19 21:36:00 JST** / heartbeat: **—** / lease expiry: **09-19 23:06:00 JST**
  - evidence: `.survey/work-queue/claims/job-research-8f1455c9a8468d9c.json`

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
| ready | **50** |

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
| inference/training/survey配下の論文Markdown実体 | **760** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **618** |
| └ Research | **471** |
| └ Audit | **2** |
| └ Discovery | **145** |

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
| 対応jobなしsubmission（有効Discovery round除外） | **4** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **4** |

### 対応jobなしsubmissionの診断対象

上の異常件数と同一判定で抽出した耐久submission pathです。診断専用であり、submission/result自体は変更しません。

- `.survey/work-queue/submissions/20260919T1700JST-round09-os-pagecache.json`
- `.survey/work-queue/submissions/20260919T1700JST-round10-rdma-network.json`
- `.survey/work-queue/submissions/20260919T1700JST-round11-recent-crosscheck.json`
- `.survey/work-queue/submissions/20260919T1700JST-round12-citation-omissions.json`

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
