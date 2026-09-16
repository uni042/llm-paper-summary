# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-17 03:42:34 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **22** |
| 未claim Research job | **22** |
| 直近24hの検証済みResearch収録 | **91** |
| 最終検証済みResearch収録 | **09-17 03:41:56 JST（38秒前）** |
| 整合性異常 | **16** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **22** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **22** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **16** | **8** | **4** | **4** | **0** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **16** | **2** | **2** | **0** | **0** | **0** | **5** |
| 合計 | **32** | **10** | **6** | **4** | **0** | **0** | **5** |

- 最新Discovery runの耐久探索round: **2件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-17 03:41:56 JST** [research] `arXiv:2609.13285` — Grouped Value Attention: Efficient KV Caching via On-Demand Key Reconstruction
  - job: `.survey/work-queue/jobs/job-research-38c18cd4bb2728b9.json`
  - result: `.survey/work-queue/results/research/attempt-d6929dca26947ce1b79ba676.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d6929dca26947ce1b79ba676.json`
  - paper: `papers/inference/06-kv-cache-memory/2026-2609.13285-grouped-value-attention-efficient-kv-caching.md`
- **09-17 03:38:32 JST** [research] `arXiv:2609.13161` — PDD: Unleashing Economical and Flexible Heterogeneous LLM Inference via Cross-Datacenter Prefill-Decode Disaggregation
  - job: `.survey/work-queue/jobs/job-research-9f909dd53a5f1acb.json`
  - result: `.survey/work-queue/results/research/attempt-942145c6596d2cfdf7866f97.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-942145c6596d2cfdf7866f97.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.13161-pdd-cross-datacenter-prefill-decode-disaggregation.md`
- **09-17 02:36:39 JST** [research] `arXiv:2504.11765` — Shared Disk KV Cache Management for Efficient Multi-Instance Inference in RAG-Powered LLMs
  - job: `.survey/work-queue/jobs/job-research-d1705edaabc0afa6.json`
  - result: `.survey/work-queue/results/research/attempt-cb6c93d65c5d59b36245f7ee.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cb6c93d65c5d59b36245f7ee.json`
  - paper: `papers/inference/03-offload-hierarchical-memory/2025-2504.11765-shared-disk-kv-cache-rag.md`
- **09-17 02:34:55 JST** [research] `arXiv:2505.10259` — SpecOffload: Unlocking Latent GPU Capacity for LLM Inference on Resource-Constrained Devices
  - job: `.survey/work-queue/jobs/job-research-f992ed2fc8c47a46.json`
  - result: `.survey/work-queue/results/research/attempt-bb5c53d2afbda5e72b28dcf5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bb5c53d2afbda5e72b28dcf5.json`
  - paper: `papers/inference/03-offload-hierarchical-memory/2025-2505.10259-specoffload-unlocking-latent-gpu-capacity-for-llm-inference.md`
- **09-17 01:40:46 JST** [research] `arXiv:2609.06663` — ECOKV: Geometry-Aware KV Cache Eviction via Complementary Diversity Metrics
  - job: `.survey/work-queue/jobs/job-research-648fe1e5b80283fd.json`
  - result: `.survey/work-queue/results/research/attempt-e515885033d647a55b19de09.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e515885033d647a55b19de09.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.06663-ecokv-geometry-aware-kv-cache-eviction-via-complementary-diversity-metrics.md`
- **09-17 01:38:52 JST** [research] `arXiv:2512.09427` — ODMA: On-Demand Memory Allocation Framework for LLM Serving on LPDDR-Class Accelerators
  - job: `.survey/work-queue/jobs/job-research-3165425bd10baa45.json`
  - result: `.survey/work-queue/results/research/attempt-0eb4936a46a9da87b23225fa.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0eb4936a46a9da87b23225fa.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2025-2512.09427-odma-on-demand-memory-allocation-lpddr.md`
- **09-17 01:37:33 JST** [research] `arXiv:2604.09613` — Token-Budget-Aware Pool Routing for Cost-Efficient LLM Inference
  - job: `.survey/work-queue/jobs/job-research-7b525e11834c9519.json`
  - result: `.survey/work-queue/results/research/attempt-5067cd6b8db49986303c3586.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5067cd6b8db49986303c3586.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2604.09613-token-budget-aware-pool-routing.md`
- **09-17 01:35:42 JST** [research] `arXiv:2601.01310` — Making MoE based LLM inference resilient with Tarragon
  - job: `.survey/work-queue/jobs/job-research-431f09f6206f16eb.json`
  - result: `.survey/work-queue/results/research/attempt-8a4bc1625b051d6e27e89e58.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8a4bc1625b051d6e27e89e58.json`
  - paper: `papers/inference/03-moe-expert-offload/2026-2601.01310-tarragon-resilient-moe-inference.md`
- **09-17 00:35:10 JST** [research] `arXiv:2511.20172` — Beluga: A CXL-Based Memory Architecture for Scalable and Efficient LLM KVCache Management
  - job: `.survey/work-queue/jobs/job-research-8473b19fc0026661.json`
  - result: `.survey/work-queue/results/research/attempt-d8eea39fb533e59149a161cc.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d8eea39fb533e59149a161cc.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2025-2511.20172-beluga-cxl-memory-kvcache.md`
- **09-16 23:42:30 JST** [research] `arXiv:2609.16206` — Calibrate, Then Route: A Measured Study of Learned Request Routing for Disaggregated LLM Serving
  - job: `.survey/work-queue/jobs/job-research-46a0d6f61e82afe1.json`
  - result: `.survey/work-queue/results/research/attempt-f1c215fbd6c38d228df7d663.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f1c215fbd6c38d228df7d663.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.16206-calibrate-then-route-disaggregated-llm-serving.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-17 03:02:50 JST** job `job-94ba33215899ac74` / 候補 **4件**
  - result: `.survey/work-queue/results/20260917T0300JST-discovery-specialist-recent-inference-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0300JST-discovery-specialist-recent-inference-1.json`
  - 探索軸: 2026-09新着のKV表現・stateful context materialization・model-runtime co-design・speculative decoding correctness
- **09-17 03:04:49 JST** job `job-09d4a54e27614149` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T0307JST-discovery-specialist-cross-dc-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0307JST-discovery-specialist-cross-dc-2.json`
  - 探索軸: GPU runtime・collective communication・heterogeneous memory・cross-datacenter disaggregation
- **09-17 02:02:52 JST** job `job-63d7ce232b8ee5eb` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T0205JST-discovery-specialist-offload-specdecode-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0205JST-discovery-specialist-offload-specdecode-1.json`
  - 探索軸: CPU-GPUオフロード・投機的デコード・階層メモリ
- **09-17 02:02:55 JST** job `job-ed698b7c56976a1a` / 候補 **0件**
  - result: `.survey/work-queue/results/20260917T0208JST-discovery-specialist-cxl-ssd-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0208JST-discovery-specialist-cxl-ssd-2.json`
  - 探索軸: CXL階層メモリ・SSD/NVMe・MoE expert offload
- **09-17 02:06:14 JST** job `job-ed0d31e7d8bded0f` / 候補 **1件**
  - result: `.survey/work-queue/results/20260917T0211JST-discovery-specialist-kv-hardware-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0211JST-discovery-specialist-kv-hardware-3.json`
  - 探索軸: KVキャッシュ量子化・メモリ帯域・ハードウェア共同設計
- **09-17 02:06:17 JST** job `job-c49eea2ac0396e5e` / 候補 **2件**
  - result: `.survey/work-queue/results/20260917T0214JST-discovery-specialist-disk-kv-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0214JST-discovery-specialist-disk-kv-4.json`
  - 探索軸: disk-backed KV cache・RAG multi-instance・cloud offload配置
- **09-17 02:06:20 JST** job `job-3942fe6aa712b241` / 候補 **0件**
  - result: `.survey/work-queue/results/20260917T0217JST-discovery-specialist-storage-prefix-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0217JST-discovery-specialist-storage-prefix-5.json`
  - 探索軸: SSD-backed prefix/KV cache・hierarchical memory
- **09-17 02:06:23 JST** job `job-9e318b1ccd364d1e` / 候補 **0件**
  - result: `.survey/work-queue/results/20260917T0220JST-discovery-specialist-moe-offload-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0220JST-discovery-specialist-moe-offload-6.json`
  - 探索軸: MoE expert offload・speculative prefetch・CPU-light KV
- **09-17 02:06:26 JST** job `job-39c1d42207f4c28b` / 候補 **0件**
  - result: `.survey/work-queue/results/20260917T0223JST-discovery-specialist-cxl-transfer-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0223JST-discovery-specialist-cxl-transfer-7.json`
  - 探索軸: GPU memory virtualization・CXL shared KV・disaggregated transfer
- **09-17 02:06:29 JST** job `job-c34ec10fdc3fd3c2` / 候補 **0件**
  - result: `.survey/work-queue/results/20260917T0226JST-discovery-specialist-migration-scheduling-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260917T0226JST-discovery-specialist-migration-scheduling-8.json`
  - 探索軸: multi-GPU KV migration・heterogeneous serving scheduling

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-16 16:00 JST** / worker `scheduled-chat-discovery-20260916T1600JST`
- immutable submission: **8件** / 検証済み成功: **4件** / 未完了・未検証: **4件**
- **成功** `arXiv:2609.08306` — HoneyRoute: Honeypot-Model Routing for Adversarial LLM Serving
  - job: `.survey/work-queue/jobs/job-research-ec48da5b1e9edcea.json`
  - result: `.survey/work-queue/results/research/attempt-10ba900257289562be435001.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-10ba900257289562be435001.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.08306-honeyroute-adversarial-llm-serving-routing.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-201fb89bc61573cc411909b4.json` (job `job-research-6252d370adc380b9`)
- **成功** `arXiv:2509.24832` — SemShareKV: Efficient KVCache Sharing for Semantically Similar Prompts via Token-Level LSH Matching
  - job: `.survey/work-queue/jobs/job-research-b98e4e299d06a6a5.json`
  - result: `.survey/work-queue/results/research/attempt-4aa0bdcf550c974e39ccae92.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4aa0bdcf550c974e39ccae92.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2509.24832-semsharekv-efficient-kvcache-sharing-for-semantically-similar-prompts-via-token-level-lsh-matching.md`
- **成功** `arXiv:2604.23467` — Hybrid JIT-CUDA Graph Optimization for Low-Latency Large Language Model Inference
  - job: `.survey/work-queue/jobs/job-research-3ad6262bd04cfbe6.json`
  - result: `.survey/work-queue/results/research/attempt-5b2f0818dd442ca0014c8634.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5b2f0818dd442ca0014c8634.json`
  - paper: `papers/inference/09-kernel-runtime-compilation/2026-2604.23467-hybrid-jit-cuda-graph-low-latency-inference.md`
- **成功** `arXiv:2605.22566` — GraphFlow: A Graph-Based Workflow Management for Efficient LLM-Agent Serving
  - job: `.survey/work-queue/jobs/job-research-44674a8f55b9f5e8.json`
  - result: `.survey/work-queue/results/research/attempt-82e80ed19ce701a0be49bf58.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-82e80ed19ce701a0be49bf58.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2605.22566-graphflow-agent-workflow-serving.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-9bd72451731af90ab90c3e14.json` (job `job-research-6252d370adc380b9`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-b21265e1c7564132469a29b8.json` (job `job-research-ec48da5b1e9edcea`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-e3573f73597d9a563a861b51.json` (job `job-research-44674a8f55b9f5e8`)

#### Audit (:30)

- 最新観測run: **2026-09-16 16:00 JST** / worker `scheduled-chat-discovery-20260916T1600JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-17 03:00 JST**
- 耐久探索round: **2件** / immutable submission: **2件** / 検証済み成功result: **2件** / 個別result照合: **2件** / 個別result未照合: **0件** / 候補: **5件**
- 探索軸: 2026-09新着のKV表現・stateful context materialization・model-runtime co-design・speculative decoding correctness / GPU runtime・collective communication・heterogeneous memory・cross-datacenter disaggregation
- round `specialist-recent-inference-1` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/20260917T0300JST-discovery-specialist-recent-inference-1.json`
  - 探索軸: 2026-09新着のKV表現・stateful context materialization・model-runtime co-design・speculative decoding correctness
  - 個別result照合: あり / `.survey/work-queue/results/20260917T0300JST-discovery-specialist-recent-inference-1.json` (`ok=true`)
- round `specialist-cross-dc-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260917T0307JST-discovery-specialist-cross-dc-2.json`
  - 探索軸: GPU runtime・collective communication・heterogeneous memory・cross-datacenter disaggregation
  - 個別result照合: あり / `.survey/work-queue/results/20260917T0307JST-discovery-specialist-cross-dc-2.json` (`ok=true`)

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
| ready | **22** |

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
| inference/training/survey配下の論文Markdown実体 | **639** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **395** |
| └ Research | **268** |
| └ Audit | **2** |
| └ Discovery | **125** |

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
| 対応jobなしsubmission（有効Discovery round除外） | **16** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **16** |

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
