# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 22:35:08 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **51** |
| 未claim Research job | **50** |
| 直近24hの検証済みResearch収録 | **46** |
| 最終検証済みResearch収録 | **09-19 21:52:39 JST（42分前）** |
| 整合性異常 | **4** |

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
| Research | **12** | **1** | **0** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **73** | **18** | **18** | **0** | **0** | **0** | **30** |
| 合計 | **85** | **19** | **18** | **0** | **1** | **0** | **30** |

- 最新Discovery runの耐久探索round: **18件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-19 21:52:39 JST** [research] `arXiv:2609.15021` — Shared KV Caching for Replicated 27B Inference: Correctness Failures and Performance Boundaries
  - job: `.survey/work-queue/jobs/job-research-0bb313ba6c58f22b.json`
  - result: `.survey/work-queue/results/research/attempt-e7ba10673d975ae5c16659a8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e7ba10673d975ae5c16659a8.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.15021-shared-kv-caching-replicated-27b-inference.md`
- **09-19 21:48:34 JST** [research] `arXiv:2509.04576` — Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-883cceac74650e2e.json`
  - result: `.survey/work-queue/results/research/attempt-86ffe82b1cb0e347b528f5b0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-86ffe82b1cb0e347b528f5b0.json`
  - paper: `papers/inference/08-speculative-decoding/2025-2509.04576-communication-efficient-distributed-speculative-decoding.md`
- **09-19 21:44:18 JST** [research] `arXiv:2506.10443` — MNN-LLM: A Generic Inference Engine for Fast Large Language Model Deployment on Mobile Devices
  - job: `.survey/work-queue/jobs/job-research-3ae1410a48dc456e.json`
  - result: `.survey/work-queue/results/research/attempt-83b90f0b9afa469d0eb73d37.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-83b90f0b9afa469d0eb73d37.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2506.10443-mnn-llm-mobile-inference-engine.md`
- **09-19 21:42:22 JST** [research] `DOI:10.1145/3797905.3807846` — CXL-CCL: Inter-Node Collective GPU-Communication Using a CXL Shared Memory Pool
  - job: `.survey/work-queue/jobs/job-research-8f1455c9a8468d9c.json`
  - result: `.survey/work-queue/results/research/attempt-9c6ab898d827d5aa2ca07235.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9c6ab898d827d5aa2ca07235.json`
  - paper: `papers/inference/99-other-inference-systems/2026-fab14a584908-cxl-ccl-inter-node-collective-gpu-communication-using-a-cxl-shared-memory-pool.md`
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

### Audit

- 検証済み完了なし。

### Discovery

- **09-19 22:01:30 JST** job `job-bbc2ca917b7c80e4` / 候補 **4件**
  - result: `.survey/work-queue/results/20260919T2208JST-discovery-specialist-flash-agent-runtime-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2208JST-discovery-specialist-flash-agent-runtime-1.json`
  - 探索軸: 2026年9月新着・Flash/HBF階層メモリ・ローカルstate管理・agentic pipeline serving
- **09-19 22:02:08 JST** job `job-9a3fef00f270ac9d` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2215JST-discovery-specialist-moe-cxl-history-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2215JST-discovery-specialist-moe-cxl-history-2.json`
  - 探索軸: 2025-2026未収録・MoE expert on-demand loading・CXL rack-scale KV transfer
- **09-19 22:05:56 JST** job `job-67ae7b496b5c69d3` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2222JST-discovery-specialist-thermal-energy-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2222JST-discovery-specialist-thermal-energy-3.json`
  - 探索軸: 2026年9月新着・thermal/power-aware LLM serving・facility/device co-control
- **09-19 22:06:07 JST** job `job-9fb882aadab65802` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T2228JST-discovery-specialist-kernel-runtime-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2228JST-discovery-specialist-kernel-runtime-4.json`
  - 探索軸: GPU kernel/runtime・quantized execution・CUDA graph
- **09-19 22:06:17 JST** job `job-e734620a0895b582` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T2234JST-discovery-specialist-collectives-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2234JST-discovery-specialist-collectives-5.json`
  - 探索軸: distributed inference collective communication・runtime adaptation・interconnect
- **09-19 22:06:27 JST** job `job-8fd3acc28169d9bb` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2240JST-discovery-specialist-lora-serving-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2240JST-discovery-specialist-lora-serving-6.json`
  - 探索軸: multi-LoRA/adapter co-serving・cross-model KV reuse・agent workflow cache sharing
- **09-19 22:06:37 JST** job `job-e2622e1e043df78b` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T2246JST-discovery-specialist-vmm-memory-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2246JST-discovery-specialist-vmm-memory-7.json`
  - 探索軸: GPU virtual memory・KV fragmentation・memory allocator lineage
- **09-19 22:06:48 JST** job `job-169a24322b788066` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T2252JST-discovery-specialist-agent-kvflow-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2252JST-discovery-specialist-agent-kvflow-8.json`
  - 探索軸: agentic workflow prefix cache・future-aware eviction/prefetch・OS/DB cache policy
- **09-19 22:06:58 JST** job `job-c665f7764fe4adc2` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T2257JST-discovery-specialist-mobile-runtime-9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2257JST-discovery-specialist-mobile-runtime-9.json`
  - 探索軸: edge/mobile on-device runtime・multi-LoRA switching・self-speculative decoding
- **09-19 22:07:08 JST** job `job-661e44d354be132d` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T2303JST-discovery-specialist-speculative-serving-10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T2303JST-discovery-specialist-speculative-serving-10.json`
  - 探索軸: speculative decoding serving・draft/verification disaggregation・runtime scheduling

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 22:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-52fd234ea45de5f63b71cc39.json` (job `job-research-2dcd265cd3f3852c`, failure_class `content_validation`)
  - result: `.survey/work-queue/results/research/attempt-52fd234ea45de5f63b71cc39.json` (`ok=false`)

#### Audit (:30)

- 最新観測run: **2026-09-19 22:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-19 22:00 JST**
- 耐久探索round: **18件** / immutable submission: **18件** / 検証済み成功result: **18件** / 個別result照合: **18件** / 個別result未照合: **0件** / 候補: **30件**
- 探索軸: 2026年9月新着・Flash/HBF階層メモリ・ローカルstate管理・agentic pipeline serving / 2025-2026未収録・MoE expert on-demand loading・CXL rack-scale KV transfer / 2026年9月新着・thermal/power-aware LLM serving・facility/device co-control / GPU kernel/runtime・quantized execution・CUDA graph / distributed inference collective communication・runtime adaptation・interconnect / multi-LoRA/adapter co-serving・cross-model KV reuse・agent workflow cache sharing / GPU virtual memory・KV fragmentation・memory allocator lineage / agentic workflow prefix cache・future-aware eviction/prefetch・OS/DB cache policy / edge/mobile on-device runtime・multi-LoRA switching・self-speculative decoding / speculative decoding serving・draft/verification disaggregation・runtime scheduling / CPU/GPU heterogeneous KV offload・PCIe zero-copy・GPU-centric synchronization / serverless model loading・cold start・LoRA artifact sharing / long-context sparse attention・HBM/DRAM KV offload・lookahead prefetch / LLM serving autoscaling・P/D burst handling・SLO-aware provisioning / heterogeneous GPU serving・fine-grained dynamic parallelism・online dispatch / fault tolerance/recovery・hardware-aware multi-LLM routing / workload-aware runtime adaptation・quantized layer swapping・KV resizing / SLO-aware admission control・adaptive batching・augmented request scheduling
- round `specialist-flash-agent-runtime-1` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/20260919T2208JST-discovery-specialist-flash-agent-runtime-1.json`
  - 探索軸: 2026年9月新着・Flash/HBF階層メモリ・ローカルstate管理・agentic pipeline serving
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2208JST-discovery-specialist-flash-agent-runtime-1.json` (`ok=true`)
- round `specialist-moe-cxl-history-2` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2215JST-discovery-specialist-moe-cxl-history-2.json`
  - 探索軸: 2025-2026未収録・MoE expert on-demand loading・CXL rack-scale KV transfer
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2215JST-discovery-specialist-moe-cxl-history-2.json` (`ok=true`)
- round `specialist-thermal-energy-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2222JST-discovery-specialist-thermal-energy-3.json`
  - 探索軸: 2026年9月新着・thermal/power-aware LLM serving・facility/device co-control
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2222JST-discovery-specialist-thermal-energy-3.json` (`ok=true`)
- round `specialist-kernel-runtime-4` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T2228JST-discovery-specialist-kernel-runtime-4.json`
  - 探索軸: GPU kernel/runtime・quantized execution・CUDA graph
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2228JST-discovery-specialist-kernel-runtime-4.json` (`ok=true`)
- round `specialist-collectives-5` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T2234JST-discovery-specialist-collectives-5.json`
  - 探索軸: distributed inference collective communication・runtime adaptation・interconnect
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2234JST-discovery-specialist-collectives-5.json` (`ok=true`)
- round `specialist-lora-serving-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2240JST-discovery-specialist-lora-serving-6.json`
  - 探索軸: multi-LoRA/adapter co-serving・cross-model KV reuse・agent workflow cache sharing
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2240JST-discovery-specialist-lora-serving-6.json` (`ok=true`)
- round `specialist-vmm-memory-7` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T2246JST-discovery-specialist-vmm-memory-7.json`
  - 探索軸: GPU virtual memory・KV fragmentation・memory allocator lineage
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2246JST-discovery-specialist-vmm-memory-7.json` (`ok=true`)
- round `specialist-agent-kvflow-8` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T2252JST-discovery-specialist-agent-kvflow-8.json`
  - 探索軸: agentic workflow prefix cache・future-aware eviction/prefetch・OS/DB cache policy
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2252JST-discovery-specialist-agent-kvflow-8.json` (`ok=true`)
- round `specialist-mobile-runtime-9` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T2257JST-discovery-specialist-mobile-runtime-9.json`
  - 探索軸: edge/mobile on-device runtime・multi-LoRA switching・self-speculative decoding
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2257JST-discovery-specialist-mobile-runtime-9.json` (`ok=true`)
- round `specialist-speculative-serving-10` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T2303JST-discovery-specialist-speculative-serving-10.json`
  - 探索軸: speculative decoding serving・draft/verification disaggregation・runtime scheduling
  - 個別result照合: あり / `.survey/work-queue/results/20260919T2303JST-discovery-specialist-speculative-serving-10.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2609.18675` — HBFlex: A Flexible Memory System for Bridging Fine-Grained LLM States and Coarse-Grained HBF Parallel Execution / worker `scheduled-chat-llm-survey`
  - claim: **09-19 22:34:37 JST** / heartbeat: **—** / lease expiry: **09-20 00:04:37 JST**
  - evidence: `.survey/work-queue/claims/job-research-a6905e04777fde1f.json`

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
| inference/training/survey配下の論文Markdown実体 | **764** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **626** |
| └ Research | **479** |
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
