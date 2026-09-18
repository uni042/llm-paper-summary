# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 04:43:12 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **60** |
| 未claim Research job | **59** |
| 直近24hの検証済みResearch収録 | **49** |
| 最終検証済みResearch収録 | **09-19 04:39:51 JST（3分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **60** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **60** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **16** | **2** | **2** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **10** | **3** | **3** | **0** | **0** | **0** | **15** |
| 合計 | **26** | **5** | **5** | **0** | **1** | **0** | **15** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-19 04:39:51 JST** [research] `DOI:10.52202/085713-1587` — HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference
  - job: `.survey/work-queue/jobs/job-research-ca0df1c4e0a9af97.json`
  - result: `.survey/work-queue/results/research/attempt-818968501d26285ed6167878.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-818968501d26285ed6167878.json`
  - paper: `papers/inference/99-other-inference-systems/2026-f52f99f3360a-hifc-high-efficiency-flash-based-kv-cache-swapping-for-scaling-llm-inference.md`
- **09-19 04:35:25 JST** [research] `DOI:10.1145/3695053.3731073` — AiF: Accelerating On-Device LLM Inference Using In-Flash Processing
  - job: `.survey/work-queue/jobs/job-research-740437feef88b672.json`
  - result: `.survey/work-queue/results/research/attempt-0d9a61003cc7a37046392d50.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0d9a61003cc7a37046392d50.json`
  - paper: `papers/inference/99-other-inference-systems/2026-21d5070d498a-aif-accelerating-on-device-llm-inference-using-in-flash-processing.md`
- **09-19 03:46:31 JST** [research] `arXiv:2602.07223` — SpecAttn: Co-Designing Sparse Attention with Self-Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-469eef375f5f828e.json`
  - result: `.survey/work-queue/results/research/attempt-a9d8c2cf570fd3b13fb6b628.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a9d8c2cf570fd3b13fb6b628.json`
  - paper: `papers/inference/08-speculative-decoding/2026-2602.07223-specattn-sparse-attention-self-speculative-decoding.md`
- **09-19 03:45:13 JST** [research] `arXiv:2602.23036` — LLMServingSim 2.0: A Unified Simulator for Heterogeneous and Disaggregated LLM Serving Infrastructure
  - job: `.survey/work-queue/jobs/job-research-ebde0cc040167968.json`
  - result: `.survey/work-queue/results/research/attempt-b9d676ed397522f747b185c2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b9d676ed397522f747b185c2.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2602.23036-llmservingsim-2-heterogeneous-disaggregated-simulator.md`
- **09-19 03:36:57 JST** [research] `arXiv:2503.10325` — Collaborative Speculative Inference for Efficient LLM Inference Serving
  - job: `.survey/work-queue/jobs/job-research-4fd6dcd288e7197d.json`
  - result: `.survey/work-queue/results/research/attempt-acffb77470592a9e8f9dbd06.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-acffb77470592a9e8f9dbd06.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2503.10325-collaborative-speculative-inference-for-efficient-llm-inference-serving.md`
- **09-19 03:30:37 JST** [research] `arXiv:2508.03611` — Block: Balancing Load in LLM Serving with Context, Knowledge and Predictive Scheduling
  - job: `.survey/work-queue/jobs/job-research-21b30a62610ad176.json`
  - result: `.survey/work-queue/results/research/attempt-e7451954f296ee21fbc9ac8c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e7451954f296ee21fbc9ac8c.json`
  - paper: `papers/inference/06-serving-scheduling/2025-2508.03611-block-predictive-load-balancing.md`
- **09-19 03:12:08 JST** [research] `arXiv:2609.17184` — LoopSpec: Pipelined Self-Speculative Decoding for Looped Transformers
  - job: `.survey/work-queue/jobs/job-research-06a7e035a0f5ff0b.json`
  - result: `.survey/work-queue/results/research/attempt-1b78e7fa82b82abe032f6a4d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1b78e7fa82b82abe032f6a4d.json`
  - paper: `papers/inference/06-speculative-decoding/2026-2609.17184-loopspec-pipelined-self-speculative-looped-transformers.md`
- **09-19 03:09:45 JST** [research] `arXiv:2606.05511` — RH+: Row-Hit-Optimized Scheduling for PIM-based LLM Inference
  - job: `.survey/work-queue/jobs/job-research-51ff641061ba8ecf.json`
  - result: `.survey/work-queue/results/research/attempt-bc5a8fd4186a7939c0b7b5f9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bc5a8fd4186a7939c0b7b5f9.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2026-2606.05511-rh-plus-pim-row-hit-scheduling.md`
- **09-19 03:07:27 JST** [research] `arXiv:2505.16056` — Not All Models Suit Expert Offloading: On Local Routing Consistency of Mixture-of-Expert Models
  - job: `.survey/work-queue/jobs/job-research-9d3c210288b42eb4.json`
  - result: `.survey/work-queue/results/research/attempt-bc68d740adca0b4c200156a1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bc68d740adca0b4c200156a1.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2025-2505.16056-local-routing-consistency-expert-offloading.md`
- **09-19 03:05:17 JST** [research] `arXiv:2511.07035` — GoCkpt: Gradient-Assisted Multi-Step overlapped Checkpointing for Efficient LLM Training
  - job: `.survey/work-queue/jobs/job-research-6af027835df580e1.json`
  - result: `.survey/work-queue/results/research/attempt-c40db7283a5c53be666dfa56.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c40db7283a5c53be666dfa56.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2511.07035-gockpt-gradient-assisted-multi-step-overlapped-checkpointing-for-efficient-llm-training.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-19 03:59:35 JST** job `job-43d9a8057337c9ad` / 候補 **5件**
  - result: `.survey/work-queue/results/20260919T0408JST-discovery-specialist-nonarxiv-storage-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0408JST-discovery-specialist-nonarxiv-storage-1.json`
  - 探索軸: 非arXiv systems/workshop・flash/PIM/CXL・storage datapath
- **09-19 04:02:33 JST** job `job-9b8c216a46edd0b5` / 候補 **5件**
  - result: `.survey/work-queue/results/20260919T0418JST-discovery-specialist-near-memory-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0418JST-discovery-specialist-near-memory-2.json`
  - 探索軸: in-storage retrieval・HBF hybrid・3D NAND CIM・product-level PIM integration
- **09-19 04:02:42 JST** job `job-1e48c57afdf71a43` / 候補 **5件**
  - result: `.survey/work-queue/results/20260919T0427JST-discovery-specialist-network-serving-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0427JST-discovery-specialist-network-serving-3.json`
  - 探索軸: network collective・compute-memory disaggregation・dynamic sequence parallelism・非arXiv serving systems
- **09-19 02:00:50 JST** job `job-e07c9322ac71f48e` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0159JST-discovery-specialist-nvme-characterization-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0159JST-discovery-specialist-nvme-characterization-1.json`
  - 探索軸: NVMe SSD model/KV-cache offload・block I/O characterization・storage datapath
- **09-19 02:01:58 JST** job `job-9b6f2006f483290b` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0204JST-discovery-specialist-storage-datapath-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0204JST-discovery-specialist-storage-datapath-2.json`
  - 探索軸: SPDK・io_uring・GPUDirect Storage・LLM storage datapath measurement
- **09-19 02:02:08 JST** job `job-19b9378212c1c3a7` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0211JST-discovery-specialist-flash-kv-materialization-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0211JST-discovery-specialist-flash-kv-materialization-3.json`
  - 探索軸: flash KV materialization・RAG prefill reuse・compute-storage tradeoff
- **09-19 02:02:38 JST** job `job-cb30e802e8c19550` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0217JST-discovery-specialist-agent-state-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0217JST-discovery-specialist-agent-state-4.json`
  - 探索軸: agentic multi-turn serving・persistent KV state・delta-only inference
- **09-19 02:02:47 JST** job `job-521a57671b0e5d8a` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T0223JST-discovery-specialist-execution-state-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0223JST-discovery-specialist-execution-state-5.json`
  - 探索軸: execution-state checkpoint/restore・agent fork/rollback・small-batch serving runtime
- **09-19 02:03:17 JST** job `job-f12003189ab11321` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T0228JST-discovery-specialist-fault-recovery-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0228JST-discovery-specialist-fault-recovery-6.json`
  - 探索軸: fault-tolerant LLM serving・KV checkpoint/replication・failure recovery
- **09-19 02:03:27 JST** job `job-fa98432f228f6281` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T0234JST-discovery-specialist-elastic-migration-7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T0234JST-discovery-specialist-elastic-migration-7.json`
  - 探索軸: request/KV migration・elastic memory・model/KV co-migration

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 04:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **2件** / 検証済み成功: **2件** / 未完了・未検証: **0件**
- **成功** `DOI:10.1145/3695053.3731073` — AiF: Accelerating On-Device LLM Inference Using In-Flash Processing
  - job: `.survey/work-queue/jobs/job-research-740437feef88b672.json`
  - result: `.survey/work-queue/results/research/attempt-0d9a61003cc7a37046392d50.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0d9a61003cc7a37046392d50.json`
  - paper: `papers/inference/99-other-inference-systems/2026-21d5070d498a-aif-accelerating-on-device-llm-inference-using-in-flash-processing.md`
- **成功** `DOI:10.52202/085713-1587` — HiFC: High-efficiency Flash-based KV Cache Swapping for Scaling LLM Inference
  - job: `.survey/work-queue/jobs/job-research-ca0df1c4e0a9af97.json`
  - result: `.survey/work-queue/results/research/attempt-818968501d26285ed6167878.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-818968501d26285ed6167878.json`
  - paper: `papers/inference/99-other-inference-systems/2026-f52f99f3360a-hifc-high-efficiency-flash-based-kv-cache-swapping-for-scaling-llm-inference.md`

#### Audit (:30)

- 最新観測run: **2026-09-19 04:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-19 03:00 JST**
- 耐久探索round: **3件** / immutable submission: **3件** / 検証済み成功result: **3件** / 個別result照合: **3件** / 個別result未照合: **0件** / 候補: **15件**
- 探索軸: 非arXiv systems/workshop・flash/PIM/CXL・storage datapath / in-storage retrieval・HBF hybrid・3D NAND CIM・product-level PIM integration / network collective・compute-memory disaggregation・dynamic sequence parallelism・非arXiv serving systems
- round `specialist-nonarxiv-storage-1` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260919T0408JST-discovery-specialist-nonarxiv-storage-1.json`
  - 探索軸: 非arXiv systems/workshop・flash/PIM/CXL・storage datapath
  - 個別result照合: あり / `.survey/work-queue/results/20260919T0408JST-discovery-specialist-nonarxiv-storage-1.json` (`ok=true`)
- round `specialist-near-memory-2` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260919T0418JST-discovery-specialist-near-memory-2.json`
  - 探索軸: in-storage retrieval・HBF hybrid・3D NAND CIM・product-level PIM integration
  - 個別result照合: あり / `.survey/work-queue/results/20260919T0418JST-discovery-specialist-near-memory-2.json` (`ok=true`)
- round `specialist-network-serving-3` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260919T0427JST-discovery-specialist-network-serving-3.json`
  - 探索軸: network collective・compute-memory disaggregation・dynamic sequence parallelism・非arXiv serving systems
  - 個別result照合: あり / `.survey/work-queue/results/20260919T0427JST-discovery-specialist-network-serving-3.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `URL:https://www.usenix.org/conference/nsdi26/presentation/agarwal` — SYMPHONY: Enabling Compute-Memory Disaggregation in LLM Serving Systems / worker `scheduled-chat-llm-survey`
  - claim: **09-19 04:43:05 JST** / heartbeat: **—** / lease expiry: **09-19 06:13:05 JST**
  - evidence: `.survey/work-queue/claims/job-research-2bbcf1d996d23713.json`

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
| ready | **60** |

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
| inference/training/survey配下の論文Markdown実体 | **734** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **553** |
| └ Research | **424** |
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
