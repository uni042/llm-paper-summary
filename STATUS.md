# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 19:34:13 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **47** |
| 未claim Research job | **46** |
| 直近24hの検証済みResearch収録 | **44** |
| 最終検証済みResearch収録 | **09-19 19:34:03 JST（10秒前）** |
| 整合性異常 | **4** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **47** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **47** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **6** | **1** | **1** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **39** | **20** | **20** | **0** | **0** | **0** | **31** |
| 合計 | **45** | **21** | **21** | **0** | **1** | **0** | **31** |

- 最新Discovery runの耐久探索round: **20件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

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

- **09-19 19:06:28 JST** job `job-fedfeb6fc48d7e58` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-adjacent-14.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-adjacent-14.json`
  - 探索軸: adjacent agent-serving systems: orchestration / predictive KV / aggregate pipeline allocation
- **09-19 19:06:35 JST** job `job-b34555c80ea4673f` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-related-13.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-related-13.json`
  - 探索軸: related-work path from agentic workload systems to predictability-driven agent-native serving
- **09-19 19:01:40 JST** job `job-eede52e50f431a91` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-scheduling-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-scheduling-5.json`
  - 探索軸: agentic multi-turn scheduling / tool-call pauses / KV cache TTL
- **09-19 19:02:31 JST** job `job-7f0f0baa3d9ba4a7` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-systems-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-systems-6.json`
  - 探索軸: agentic workload characterization / sandbox memory / secure mobile serving
- **09-19 19:06:42 JST** job `job-136bbed0754c23c7` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-coserving-15.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-coserving-15.json`
  - 探索軸: online/offline co-serving / fine-grained GPU harvesting / preemption
- **09-19 19:01:01 JST** job `job-81062042be174d85` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-cxl-nmp-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-cxl-nmp-3.json`
  - 探索軸: CXL memory pooling / photonic fabric / NMP for hybrid LLM inference
- **09-19 19:00:28 JST** job `job-6a54a063ec9c9c50` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-elastic-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-elastic-kv-1.json`
  - 探索軸: KV cache dynamic reclamation / CUDA virtual memory / serving memory management
- **09-19 19:06:49 JST** job `job-321b6dfb8d533f50` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-energy-9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-energy-9.json`
  - 探索軸: thermal-aware / energy-aware LLM serving scheduling
- **09-19 19:06:56 JST** job `job-bd9f20068990b1ad` / 候補 **3件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-heterocloud-17.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-heterocloud-17.json`
  - 探索軸: heterogeneous cloud/spot GPUs / multi-LLM placement / spatial-temporal orchestration
- **09-19 19:07:03 JST** job `job-ca8974d52c93b2d2` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T1900JST-discovery-specialist-isolation-moe-16.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-isolation-moe-16.json`
  - 探索軸: multi-tenant performance isolation / adaptive persistent-kernel MoE serving

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 19:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **1件** / 検証済み成功: **1件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
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

- 最新観測run: **2026-09-19 19:00 JST**
- 耐久探索round: **20件** / immutable submission: **20件** / 検証済み成功result: **20件** / 個別result照合: **20件** / 個別result未照合: **0件** / 候補: **31件**
- 探索軸: adjacent agent-serving systems: orchestration / predictive KV / aggregate pipeline allocation / related-work path from agentic workload systems to predictability-driven agent-native serving / agentic multi-turn scheduling / tool-call pauses / KV cache TTL / agentic workload characterization / sandbox memory / secure mobile serving / online/offline co-serving / fine-grained GPU harvesting / preemption / CXL memory pooling / photonic fabric / NMP for hybrid LLM inference / KV cache dynamic reclamation / CUDA virtual memory / serving memory management / thermal-aware / energy-aware LLM serving scheduling / heterogeneous cloud/spot GPUs / multi-LLM placement / spatial-temporal orchestration / multi-tenant performance isolation / adaptive persistent-kernel MoE serving / MoE expert load balancing / elastic placement / CPU-GPU scheduling and cache / MoE expert prediction / prefetch / CPU-GPU offload / multi-LLM prewarming / shared decode execution / near-memory processing / 3D DRAM / KV allocation co-design / prefill/decode intra-GPU disaggregation / quantized inference kernels / precision-aware KV memory and scheduling / September 2026 recent serving/offload/cache/runtime sweep / related-work path from elastic KV memory to GPU memory ballooning / multi-LLM co-serving / prefill/decode fairness / adaptive batching / SLO scheduling / serving security isolation / inference-finetuning co-execution
- round `specialist-agent-adjacent-14` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-adjacent-14.json`
  - 探索軸: adjacent agent-serving systems: orchestration / predictive KV / aggregate pipeline allocation
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-adjacent-14.json` (`ok=true`)
- round `specialist-agent-related-13` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-related-13.json`
  - 探索軸: related-work path from agentic workload systems to predictability-driven agent-native serving
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-related-13.json` (`ok=true`)
- round `specialist-agent-scheduling-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-scheduling-5.json`
  - 探索軸: agentic multi-turn scheduling / tool-call pauses / KV cache TTL
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-scheduling-5.json` (`ok=true`)
- round `specialist-agent-systems-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-agent-systems-6.json`
  - 探索軸: agentic workload characterization / sandbox memory / secure mobile serving
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-agent-systems-6.json` (`ok=true`)
- round `specialist-coserving-15` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-coserving-15.json`
  - 探索軸: online/offline co-serving / fine-grained GPU harvesting / preemption
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-coserving-15.json` (`ok=true`)
- round `specialist-cxl-nmp-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-cxl-nmp-3.json`
  - 探索軸: CXL memory pooling / photonic fabric / NMP for hybrid LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-cxl-nmp-3.json` (`ok=true`)
- round `specialist-elastic-kv-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-elastic-kv-1.json`
  - 探索軸: KV cache dynamic reclamation / CUDA virtual memory / serving memory management
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-elastic-kv-1.json` (`ok=true`)
- round `specialist-energy-9` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-energy-9.json`
  - 探索軸: thermal-aware / energy-aware LLM serving scheduling
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-energy-9.json` (`ok=true`)
- round `specialist-heterocloud-17` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-heterocloud-17.json`
  - 探索軸: heterogeneous cloud/spot GPUs / multi-LLM placement / spatial-temporal orchestration
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-heterocloud-17.json` (`ok=true`)
- round `specialist-isolation-moe-16` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T1900JST-discovery-specialist-isolation-moe-16.json`
  - 探索軸: multi-tenant performance isolation / adaptive persistent-kernel MoE serving
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1900JST-discovery-specialist-isolation-moe-16.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2604.15186` — Scepsy: Serving Agentic Workflows Using Aggregate LLM Pipelines / worker `scheduled-chat-llm-survey`
  - claim: **09-19 19:33:46 JST** / heartbeat: **—** / lease expiry: **09-19 21:03:46 JST**
  - evidence: `.survey/work-queue/claims/job-research-188f6649e816eaae.json`

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
| ready | **47** |

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
| inference/training/survey配下の論文Markdown実体 | **758** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **617** |
| └ Research | **470** |
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
