# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 12:37:19 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **52** |
| 未claim Research job | **52** |
| 直近24hの検証済みResearch収録 | **30** |
| 最終検証済みResearch収録 | **09-16 12:37:15 JST（4秒前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **52** |
| canonical_idなしの候補Research job | **1** |
| 非終端Research job合計 | **53** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **23** | **1** | **1** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **1** | **6** | **0** | **6** | **0** | **0** | **6** |
| 合計 | **24** | **7** | **1** | **6** | **1** | **0** | **6** |

- 最新Discovery runの耐久探索round: **6件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-16 12:37:15 JST** [research] `arXiv:2609.07816` — Kalman Delta Networks: Uncertainty-aware Associative Memory
  - job: `.survey/work-queue/jobs/job-research-7411280ca93364ec.json`
  - result: `.survey/work-queue/results/research/attempt-7bba4de8acdf88007ff64c4d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-7bba4de8acdf88007ff64c4d.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.07816-kalman-delta-networks-associative-memory.md`
- **09-16 12:33:49 JST** [research] `arXiv:2606.03910` — NetKV: Network-Aware Decode Instance Selection for Disaggregated LLM Inference
  - job: `.survey/work-queue/jobs/job-research-8548d3d173ce3871.json`
  - result: `.survey/work-queue/results/research/attempt-3d64f755a8e767409d3e9d13.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3d64f755a8e767409d3e9d13.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2606.03910-netkv-network-aware-decode-selection.md`
- **09-16 12:19:46 JST** [research] `arXiv:2509.00105` — AdaptCache: Adaptive KV Cache Storage Hierarchy for Low-Delay LLM Serving
  - job: `.survey/work-queue/jobs/job-research-53e75736382e3b98.json`
  - result: `.survey/work-queue/results/research/attempt-14822aa228c007fac68c1df2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-14822aa228c007fac68c1df2.json`
  - paper: `papers/inference/05-kv-cache-offloading/2025-2509.00105-adaptcache-adaptive-kv-storage-hierarchy.md`
- **09-16 12:18:29 JST** [research] `arXiv:2607.23933` — SpecBox: Speculative Sandbox Scheduling for Efficient LLM Agent Serving
  - job: `.survey/work-queue/jobs/job-research-4055e74aec47c94e.json`
  - result: `.survey/work-queue/results/research/attempt-e5b7d8bd8cb604c35cc21abd.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e5b7d8bd8cb604c35cc21abd.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2607.23933-specbox-speculative-sandbox-scheduling-agent-serving.md`
- **09-16 12:13:23 JST** [research] `arXiv:2605.02960` — MoE-Prefill: Zero Redundancy Overheads in MoE Prefill Serving
  - job: `.survey/work-queue/jobs/job-research-bd280ca93f0a6940.json`
  - result: `.survey/work-queue/results/research/attempt-7d15ace40bfac2c2b2f6ff8e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-7d15ace40bfac2c2b2f6ff8e.json`
  - paper: `papers/inference/06-expert-offloading/2026-2605.02960-moe-prefill-async-expert-weight-streaming.md`
- **09-16 12:12:27 JST** [research] `arXiv:2609.12686` — Residual Vector-based Reconstruction as Long-Context Recall Regardless of Context Window Size
  - job: `.survey/work-queue/jobs/job-research-6cff6eafb4a4e5b9.json`
  - result: `.survey/work-queue/results/research/attempt-43fc54bc4bb664c376b8fe08.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-43fc54bc4bb664c376b8fe08.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2026-2609.12686-residual-vector-long-context-recall.md`
- **09-16 12:07:59 JST** [research] `arXiv:2609.13134` — Rethinking Heterogeneous System Disaggregation for Subquadratic Attention
  - job: `.survey/work-queue/jobs/job-research-e3f30981ea631700.json`
  - result: `.survey/work-queue/results/research/attempt-5d2bee9ae7908778830d1829.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5d2bee9ae7908778830d1829.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.13134-subquadratic-attention-heterogeneous-disaggregation.md`
- **09-16 12:03:44 JST** [research] `arXiv:2604.15379` — Fleet: Hierarchical Task-based Abstraction for Megakernels on Multi-Die GPUs
  - job: `.survey/work-queue/jobs/job-research-8f7fdb4eba0d8a63.json`
  - result: `.survey/work-queue/results/research/attempt-34765e98bb9cf6776aa5d26d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-34765e98bb9cf6776aa5d26d.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2604.15379-fleet-multi-die-gpu-megakernel.md`
- **09-16 12:03:44 JST** [research] `arXiv:2606.22541` — ASAP: A Disaggregated and Asynchronous Inference System for MoE Prefill
  - job: `.survey/work-queue/jobs/job-research-553691f8ff245e9b.json`
  - result: `.survey/work-queue/results/research/attempt-6f1b6968a7268a733026a358.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6f1b6968a7268a733026a358.json`
  - paper: `papers/inference/04-moe-offload-expert-cache/2026-2606.22541-asap-disaggregated-asynchronous-moe-prefill.md`
- **09-16 11:52:49 JST** [research] `arXiv:2607.05116` — Communication-Aware Placement and Pruning for Efficient Mixture-of-Experts Inference
  - job: `.survey/work-queue/jobs/job-research-997bb7245fdc3187.json`
  - result: `.survey/work-queue/results/research/attempt-4b181ffe9b1f03a47a7fd1ab.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4b181ffe9b1f03a47a7fd1ab.json`
  - paper: `papers/inference/06-moe-inference-expert-offloading/2026-2607.05116-communication-aware-placement-pruning-moe.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-16 07:20:40 JST** job `job-6ff919b9f51ccf92` / 候補 **1件**
  - result: `.survey/work-queue/results/20260916T0703JST-discovery-specialist-adaptive-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0703JST-discovery-specialist-adaptive-kv-1.json`
  - 探索軸: 新着・適応型KV圧縮・制約付き推論

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-16 10:37 JST** / worker `manual-reader-smoketest-20260916T1037JST`
- immutable submission: **1件** / 検証済み成功: **1件** / 未完了・未検証: **0件**
- **成功** `arXiv:2609.15359` — MAPS: Memory-Aware Predictive Scheduling Framework for Large Language Model Serving
  - job: `.survey/work-queue/jobs/job-research-41c06f0529c148e7.json`
  - result: `.survey/work-queue/results/research/attempt-79c4ee390d672cc004c43df8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-79c4ee390d672cc004c43df8.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.15359-maps-memory-aware-predictive-scheduling.md`

#### Audit (:30)

- 最新観測run: **2026-09-16 10:37 JST** / worker `manual-reader-smoketest-20260916T1037JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-16 09:00 JST**
- 耐久探索round: **6件** / immutable submission: **6件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **6件** / 候補: **6件**
- 探索軸: 分離サービング・多段ネットワークflow scheduling / Superchip統合CPU-GPUメモリ・KV rotation / KV cache restoration・compute/I/O多次元並列 / processing-near-memory・retrieval sparse attention・KV外置き / CXL memory expansion・PIM・GPU-free inference / 意味検索head・KV retention/compression
- round `specialist-network-flow-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0902JST-discovery-specialist-network-flow-1.json`
  - 探索軸: 分離サービング・多段ネットワークflow scheduling
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-superchip-kv-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0906JST-discovery-specialist-superchip-kv-2.json`
  - 探索軸: Superchip統合CPU-GPUメモリ・KV rotation
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-kv-restoration-3` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0910JST-discovery-specialist-kv-restoration-3.json`
  - 探索軸: KV cache restoration・compute/I/O多次元並列
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-pnm-attention-4` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0914JST-discovery-specialist-pnm-attention-4.json`
  - 探索軸: processing-near-memory・retrieval sparse attention・KV外置き
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-cxl-pim-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0918JST-discovery-specialist-cxl-pim-5.json`
  - 探索軸: CXL memory expansion・PIM・GPU-free inference
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-semantic-kv-6` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0922JST-discovery-specialist-semantic-kv-6.json`
  - 探索軸: 意味検索head・KV retention/compression
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2607.23099` — Decoding the Skew: Distribution-Aware MoE Inference with Adaptive Kernel Dispatch / worker `scheduled-chat-discovery-specialist-00`
  - claim: **09-16 12:20:14 JST** / heartbeat: **—** / lease expiry: **09-16 13:50:14 JST**
  - evidence: `.survey/work-queue/claims/job-research-32ece608ca43dae7.json`

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
| ready | **53** |

### 候補の重複・識別情報欠損

非終端Research jobだけを対象にしています。source URLは `url/source_url/paper_url/primary_url/arxiv_url/pdf_url/source.url` のいずれかで確認します。

| 指標 | 件数 |
|---|---:|
| 重複canonical_idグループ | **0** |
| 重複分のResearch job | **0** |
| canonical_id欠損 | **1** |
| title欠損 | **0** |
| source URL欠損 | **0** |

### 収録済み論文実体

`papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README、comparison系、Movedスタブを除外します。

| 指標 | 件数 |
|---|---:|
| inference/training/survey配下の論文Markdown実体 | **571** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **258** |
| └ Research | **148** |
| └ Discovery | **110** |

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
