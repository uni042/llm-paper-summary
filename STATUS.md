# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 16:38:39 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **33** |
| 未claim Research job | **32** |
| 直近24hの検証済みResearch収録 | **56** |
| 最終検証済みResearch収録 | **09-16 16:38:30 JST（9秒前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **33** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **33** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **45** | **12** | **6** | **6** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **1** | **0** | — |
| Discovery | **1** | **19** | **0** | **19** | **0** | **0** | **23** |
| 合計 | **46** | **31** | **6** | **25** | **2** | **0** | **23** |

- 最新Discovery runの耐久探索round: **19件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-16 16:38:30 JST** [research] `arXiv:2605.25655` — Bandwidth-Aware LLM Inference on Heterogeneous Many-Core Supercomputers
  - job: `.survey/work-queue/jobs/job-research-f9d44874a1b28506.json`
  - result: `.survey/work-queue/results/research/attempt-935f2123fd1379422e5152c0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-935f2123fd1379422e5152c0.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.25655-bandwidth-aware-llm-inference-on-heterogeneous-many-core-supercomputers.md`
- **09-16 16:12:08 JST** [research] `arXiv:2609.04748` — Same Request, Different Answer: Quantization Amplifies Cache-Induced Divergence in LLM Serving
  - job: `.survey/work-queue/jobs/job-research-a8b5b2b70328c222.json`
  - result: `.survey/work-queue/results/research/attempt-f18ac3404e8d423c89a438b0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f18ac3404e8d423c89a438b0.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.04748-cache-induced-divergence-quantization-llm-serving.md`
- **09-16 16:10:38 JST** [research] `arXiv:2609.11356` — Taming Bitwise Behavior in GPU Kernels with Tensor Core: Black-Box Reconstruction, Compiler Enforcement, and Static Verification
  - job: `.survey/work-queue/jobs/job-research-23c1aef2e7b819be.json`
  - result: `.survey/work-queue/results/research/attempt-ce08cf0566cb7dca27b52253.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ce08cf0566cb7dca27b52253.json`
  - paper: `papers/inference/02-hardware-accelerators/2026-2609.11356-taming-bitwise-behavior-gpu-tensor-core-kernels.md`
- **09-16 15:51:37 JST** [research] `arXiv:2603.07770` — ArcLight: A Lightweight LLM Inference Architecture for Many-Core CPUs
  - job: `.survey/work-queue/jobs/job-research-f3ec00db7d9723b7.json`
  - result: `.survey/work-queue/results/research/attempt-99747231195f2250976184c3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-99747231195f2250976184c3.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2603.07770-arclight-a-lightweight-llm-inference-architecture-for-many-core-cpus.md`
- **09-16 15:46:51 JST** [research] `arXiv:2609.07306` — RouteRelay: Event-Triggered Cross-Layer Route Reuse for Efficient Dynamic Sparse Attention
  - job: `.survey/work-queue/jobs/job-research-e59ec36b619f9b0c.json`
  - result: `.survey/work-queue/results/research/attempt-09c3c1f8ea3236b83582a70d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-09c3c1f8ea3236b83582a70d.json`
  - paper: `papers/inference/10-sparse-attention/2026-2609.07306-routerelay-cross-layer-route-reuse.md`
- **09-16 15:43:41 JST** [research] `arXiv:2609.07282` — Separating Stream Stability from Long-Term Recall in Language Models
  - job: `.survey/work-queue/jobs/job-research-5204297ffdb35cfd.json`
  - result: `.survey/work-queue/results/research/attempt-c310d0bbe115d78e277aebea.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c310d0bbe115d78e277aebea.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.07282-stream-stability-long-term-recall-threeh.md`
- **09-16 15:36:55 JST** [research] `arXiv:2609.15230` — ETCInfer: An Energy-efficient Thermal-aware Cooling-joint Scheduler for LLM Inference in AI Datacenters
  - job: `.survey/work-queue/jobs/job-research-6802b144c10e4060.json`
  - result: `.survey/work-queue/results/research/attempt-4bfdec70e8914ae1ce28af5e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4bfdec70e8914ae1ce28af5e.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.15230-etcinfer-thermal-aware-cooling-joint-scheduler.md`
- **09-16 15:16:37 JST** [research] IFMoE: An Inference Framework Design for Fine-grained MoE
  - job: `.survey/work-queue/jobs/job-research-3190de0b496967f3.json`
  - result: `.survey/work-queue/results/research/attempt-3feeca873b26fab2446b5438.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3feeca873b26fab2446b5438.json`
  - paper: `papers/inference/99-other-inference-systems/2026-3190de0b4969-ifmoe-an-inference-framework-design-for-fine-grained-moe.md`
- **09-16 15:11:26 JST** [research] `arXiv:2609.04244` — MonoMoE: An Efficient Fused Mega-kernel for Quantized MoE Decoding
  - job: `.survey/work-queue/jobs/job-research-cffb14eec24a02c2.json`
  - result: `.survey/work-queue/results/research/attempt-5cdea98b4034b7e3f2b05850.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5cdea98b4034b7e3f2b05850.json`
  - paper: `papers/inference/09-kernel-runtime-compilation/2026-2609.04244-monomoe-fused-megakernel-quantized-moe-decoding.md`
- **09-16 15:10:01 JST** [research] `arXiv:2412.16187` — HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing
  - job: `.survey/work-queue/jobs/job-research-795118fce8eb1845.json`
  - result: `.survey/work-queue/results/research/attempt-8834d311401a99e374c1300d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8834d311401a99e374c1300d.json`
  - paper: `papers/inference/99-other-inference-systems/2024-2412.16187-hashevict-a-pre-attention-kv-cache-eviction-strategy-using-locality-sensitive-hashing.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-16 13:20:13 JST** job `job-b6f805c0cbcee3d4` / 候補 **1件**
  - result: `.survey/work-queue/results/20260916T0902JST-discovery-specialist-network-flow-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0902JST-discovery-specialist-network-flow-1.json`
  - 探索軸: 分離サービング・多段ネットワークflow scheduling

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-16 14:00 JST** / worker `scheduled-chat-discovery-specialist-20260916T1400JST`
- immutable submission: **12件** / 検証済み成功: **6件** / 未完了・未検証: **6件**
- **成功** `arXiv:2605.21312` — Frontier: Towards Comprehensive and Accurate LLM Inference Simulation
  - job: `.survey/work-queue/jobs/job-research-d743b2b5468a28c8.json`
  - result: `.survey/work-queue/results/research/attempt-062785fdd1a729fb213be682.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-062785fdd1a729fb213be682.json`
  - paper: `papers/inference/12-benchmarking-modeling-emulation/2026-2605.21312-frontier-comprehensive-accurate-llm-inference-simulation.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-0a8f3b62f80c03f536fe81a5.json` (job `job-research-4714939abf3ccf8f`)
- **成功** `arXiv:2605.21427` — PALS: Power-Aware LLM Serving for Mixture-of-Experts Models
  - job: `.survey/work-queue/jobs/job-research-3bb1145babb1a6fc.json`
  - result: `.survey/work-queue/results/research/attempt-2155991e74d60ac74b2163d1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2155991e74d60ac74b2163d1.json`
  - paper: `papers/inference/04-moe-offload-routing/2026-2605.21427-pals-power-aware-moe-serving.md`
- **成功** `arXiv:2601.11580` — Speculative Decoding: Performance or Illusion?
  - job: `.survey/work-queue/jobs/job-research-deb10d3b4d925a01.json`
  - result: `.survey/work-queue/results/research/attempt-44d7d7981220efe93f540824.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-44d7d7981220efe93f540824.json`
  - paper: `papers/inference/05-speculative-decoding/2026-2601.11580-speculative-decoding-performance-or-illusion.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-4903385702e76b27799d8f09.json` (job `job-research-a8b5b2b70328c222`)
- **成功** `arXiv:2606.28565` — KernelSight-LM: A Kernel-Level LLM Inference Simulator
  - job: `.survey/work-queue/jobs/job-research-b8521dbc1f501e0d.json`
  - result: `.survey/work-queue/results/research/attempt-52add1efa2617512647eab93.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-52add1efa2617512647eab93.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.28565-kernelsight-lm-kernel-level-inference-simulator.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-6bf933254bed4369e3f58978.json` (job `job-research-a8b5b2b70328c222`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-7b42c4b89ac929fa80c2c499.json` (job `job-research-73e15ccbef3e6d6d`)
- **成功** `arXiv:2606.11244` — SPEAR: A System for Post-Quantization Error-Adaptive Recovery Enabling Efficient Low-Bit LLM Serving
  - job: `.survey/work-queue/jobs/job-research-1dd6544d5f77b687.json`
  - result: `.survey/work-queue/results/research/attempt-ad4afba2a1cd0b175dc4bc13.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-ad4afba2a1cd0b175dc4bc13.json`
  - paper: `papers/inference/08-quantization-kernels/2026-2606.11244-spear-error-adaptive-low-bit-serving.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-bf1a77a940ea17f7048afe0d.json` (job `job-research-b8521dbc1f501e0d`)

#### Audit (:30)

- 最新観測run: **2026-09-16 14:00 JST** / worker `scheduled-chat-discovery-specialist-20260916T1400JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-16 14:00 JST**
- 耐久探索round: **19件** / immutable submission: **19件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **19件** / 候補: **23件**
- 探索軸: MoE expert cache・cache-aware routing / SLO-aware prefill chunking・decode interference / Composable CXL・Kubernetes共有KVメモリ / disaggregated serving・phase-aware power control / Hopper GPU utilization・推論profiling / prefix cache・量子化・serving決定性 / page-aware decode scheduling・KV workqueue / 3D NAND・near-storage compute LLM inference / distributed edge MoE・wireless expert aggregation / dynamic sparse MoE・inference-time expert budget / on-device speculative decoding・DVFS / single-GPU memory budget・weight/KV joint compression / adaptive KV compression・latency/memory budget / multi-tenant prefix cache・isolation/security / production serving workload・caching/load-balancing trace / backward reference・distributed prompt reuse scheduling / backward reference・augmented/agentic serving interruption / backward reference・heterogeneous CPU/GPU offload / MoE expert offload・prefetch/cache lineage
- round `specialist-moe-cache-router-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1432JST-discovery-specialist-moe-cache-router-1.json`
  - 探索軸: MoE expert cache・cache-aware routing
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-prefill-deadline-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1433JST-discovery-specialist-prefill-deadline-2.json`
  - 探索軸: SLO-aware prefill chunking・decode interference
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cxl-k8s-3` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1434JST-discovery-specialist-cxl-k8s-3.json`
  - 探索軸: Composable CXL・Kubernetes共有KVメモリ
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-disagg-power-4` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1435JST-discovery-specialist-disagg-power-4.json`
  - 探索軸: disaggregated serving・phase-aware power control
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-gpu-utilization-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1436JST-discovery-specialist-gpu-utilization-5.json`
  - 探索軸: Hopper GPU utilization・推論profiling
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cache-determinism-6` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1437JST-discovery-specialist-cache-determinism-6.json`
  - 探索軸: prefix cache・量子化・serving決定性
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-page-aware-kv-7` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1438JST-discovery-specialist-page-aware-kv-7.json`
  - 探索軸: page-aware decode scheduling・KV workqueue
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-nand-compute-8` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1439JST-discovery-specialist-nand-compute-8.json`
  - 探索軸: 3D NAND・near-storage compute LLM inference
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-wireless-moe-9` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1440JST-discovery-specialist-wireless-moe-9.json`
  - 探索軸: distributed edge MoE・wireless expert aggregation
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-dynamic-moe-10` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T1441JST-discovery-specialist-dynamic-moe-10.json`
  - 探索軸: dynamic sparse MoE・inference-time expert budget
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2609.12923` — Dissecting GPU Utilization for LLM Inference on Nvidia Hopper / worker `scheduled-chat-llm-survey`
  - claim: **09-16 16:38:38 JST** / heartbeat: **—** / lease expiry: **09-16 18:08:38 JST**
  - evidence: `.survey/work-queue/claims/job-research-21d58015b4f64394.json`

#### Audit

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2504.03775` — FlowKV: A Disaggregated Inference Framework with Low-Latency KV Cache Transfer and Load-Aware Scheduling / worker `scheduled-chat-hourly-survey-20260916T145717JST`
  - claim: **09-16 15:22:00 JST** / heartbeat: **—** / lease expiry: **09-16 16:52:00 JST**
  - evidence: `.survey/work-queue/claims/job-audit-bc50ab844f1e2ebf.json`

#### Discovery

- 未失効かつ非terminal jobのclaim: **0件** / 直近15分heartbeat: **0件**
- 現在処理中と判定できる有効claimはありません。

> claimやheartbeatは **GitHubへ耐久保存された処理権・活動記録** です。Scheduled Chatプロセスの生存そのものまでは証明しないため、そこは推測しません。

## 耐久証拠の詳細集計

### 未処理Research jobの状態内訳

| status | 件数 |
|---|---:|
| ready | **33** |

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
| inference/training/survey配下の論文Markdown実体 | **601** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **336** |
| └ Research | **202** |
| └ Audit | **1** |
| └ Discovery | **133** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

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
- **整合性異常**: completed Research jobが宣言したpaper実体の欠損、対応jobなしsubmission、対応jobなし成功result、対応submissionなし成功resultを直接検出し、レコードpathで重複排除します。`discovery_stats.run_key + round` が揃ったDiscovery submissionは対応job欠損だけでは異常にしません。
- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。
- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
