# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 21:36:45 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **31** |
| 未claim Research job | **30** |
| 直近24hの検証済みResearch収録 | **73** |
| 最終検証済みResearch収録 | **09-16 21:35:31 JST（1分前）** |
| 整合性異常 | **9** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **31** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **31** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **27** | **8** | **4** | **4** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **14** | **0** | **14** | **0** | **0** | **15** |
| 合計 | **27** | **22** | **4** | **18** | **1** | **0** | **15** |

- 最新Discovery runの耐久探索round: **14件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-16 21:35:31 JST** [research] `arXiv:2605.22416` — Asymmetric Virtual Memory Paging for Hybrid Mamba-Transformer Inference
  - job: `.survey/work-queue/jobs/job-research-9fcc40253e9df4ef.json`
  - result: `.survey/work-queue/results/research/attempt-dcdaf23f15c40b373c3afea9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-dcdaf23f15c40b373c3afea9.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2026-2605.22416-asymmetric-virtual-memory-paging-hybrid-inference.md`
- **09-16 21:33:52 JST** [research] `arXiv:2506.12417` — HarMoEny: Efficient Multi-GPU Inference of MoE Models
  - job: `.survey/work-queue/jobs/job-research-1a835bd497ae941f.json`
  - result: `.survey/work-queue/results/research/attempt-9fdbbab13803c394452c3f1f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-9fdbbab13803c394452c3f1f.json`
  - paper: `papers/inference/03-moe-expert-offload/2025-2506.12417-harmoeny-efficient-multi-gpu-moe-inference.md`
- **09-16 21:30:53 JST** [research] `arXiv:2604.17172` — CCCL: In-GPU Compression-Coupled Collective Communication
  - job: `.survey/work-queue/jobs/job-research-a04176279033896e.json`
  - result: `.survey/work-queue/results/research/attempt-25cceaeacd63bfc0b41aa061.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-25cceaeacd63bfc0b41aa061.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2604.17172-cccl-compression-coupled-collective-communication.md`
- **09-16 20:33:30 JST** [research] `arXiv:2512.01357` — Tangram: Accelerating Serverless LLM Loading through GPU Memory Reuse and Affinity
  - job: `.survey/work-queue/jobs/job-research-3342ea471147b233.json`
  - result: `.survey/work-queue/results/research/attempt-c28dc16847c1e67a30dd312f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c28dc16847c1e67a30dd312f.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2512.01357-tangram-serverless-llm-loading-gpu-memory-reuse.md`
- **09-16 20:20:04 JST** [research] `arXiv:2602.11530` — PASCAL: A Phase-Aware Scheduling Algorithm for Serving Reasoning-based Large Language Models
  - job: `.survey/work-queue/jobs/job-research-c15602f379300b58.json`
  - result: `.survey/work-queue/results/research/attempt-e119121016e6ca3bccd934b0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e119121016e6ca3bccd934b0.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2602.11530-pascal-phase-aware-reasoning-llm-scheduling.md`
- **09-16 20:14:08 JST** [research] `arXiv:2604.10152` — SpecMoE: A Fast and Efficient Mixture-of-Experts Inference via Self-Assisted Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-adc94daa00d75514.json`
  - result: `.survey/work-queue/results/research/attempt-cd7cbdc8e55bcf2679e3c08f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cd7cbdc8e55bcf2679e3c08f.json`
  - paper: `papers/inference/03-moe-expert-offload/2026-2604.10152-specmoe-self-assisted-speculative-decoding.md`
- **09-16 20:09:00 JST** [research] `arXiv:2607.09248` — General Non-Clairvoyant KV-Cache Scheduling via Regime-Aware Routing
  - job: `.survey/work-queue/jobs/job-research-d9c67ca63b6b0f25.json`
  - result: `.survey/work-queue/results/research/attempt-3ab15fd671c597846c0e786b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3ab15fd671c597846c0e786b.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2607.09248-regime-aware-non-clairvoyant-kv-scheduling.md`
- **09-16 18:51:24 JST** [research] `arXiv:2608.30076` — Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects
  - job: `.survey/work-queue/jobs/job-research-dea6b2b543d05a36.json`
  - result: `.survey/work-queue/results/research/attempt-65de370d3bdc114f83e19319.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-65de370d3bdc114f83e19319.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2026-2608.30076-budget-aware-compression-single-gpu.md`
- **09-16 18:49:43 JST** [research] `arXiv:2604.07472` — Fast Heterogeneous Serving: Scalable Mixed-Scale LLM Allocation for SLO-Constrained Inference
  - job: `.survey/work-queue/jobs/job-research-c5a47af1c9e3acf3.json`
  - result: `.survey/work-queue/results/research/attempt-44002611be590dff9f7593f6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-44002611be590dff9f7593f6.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2604.07472-fast-heterogeneous-serving-allocation.md`
- **09-16 18:38:33 JST** [research] `arXiv:2609.09662` — PELM: Power Efficient On-Device LLM Inference with Speculative Decoding and Dynamic Voltage Frequency Scaling
  - job: `.survey/work-queue/jobs/job-research-3d5f11737ec9b4a2.json`
  - result: `.survey/work-queue/results/research/attempt-b66d308c0d1e4eb8ba288ecc.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b66d308c0d1e4eb8ba288ecc.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.09662-pelm-speculative-decoding-dvfs.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

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

- 最新観測run: **2026-09-16 20:00 JST**
- 耐久探索round: **14件** / immutable submission: **14件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **14件** / 候補: **15件**
- 探索軸: Superchip統合メモリ・SLO-aware KV rotation / GPU L2・HBM間KV prefetch・帯域隠蔽 / Semantic Retrieval Head・layer-aware KV圧縮 / MoE self-assisted speculative decoding・expert replication / 異種many-core・分散メモリ階層・bandwidth-aware runtime / virtual memory・異種state pool・LPDDR allocation / GPU power cap・DVFS・serverless energy-aware scheduling / tail-aware・reasoning phase-aware scheduling / serverless model loading・weight residency・multi-GPU KV migration / collective communication圧縮・tensor/expert parallel通信 / CXL・shared KV memory再スイープ / SSD/NVMe・GPU-direct KV storage再スイープ / MoE expert offload・cache・prefetch再スイープ / disaggregated serving・KV transfer・scheduler最終スイープ
- round `specialist-superchip-slo-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T2008JST-discovery-specialist-superchip-slo-1.json`
  - 探索軸: Superchip統合メモリ・SLO-aware KV rotation
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-kv-prefetch-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T2011JST-discovery-specialist-kv-prefetch-2.json`
  - 探索軸: GPU L2・HBM間KV prefetch・帯域隠蔽
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-semantic-kv-3` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T2014JST-discovery-specialist-semantic-kv-3.json`
  - 探索軸: Semantic Retrieval Head・layer-aware KV圧縮
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-moe-spec-replication-4` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T2017JST-discovery-specialist-moe-spec-replication-4.json`
  - 探索軸: MoE self-assisted speculative decoding・expert replication
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-manycore-runtime-5` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T2020JST-discovery-specialist-manycore-runtime-5.json`
  - 探索軸: 異種many-core・分散メモリ階層・bandwidth-aware runtime
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-virtual-memory-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T2025JST-discovery-specialist-virtual-memory-6.json`
  - 探索軸: virtual memory・異種state pool・LPDDR allocation
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-power-aware-7` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T2030JST-discovery-specialist-power-aware-7.json`
  - 探索軸: GPU power cap・DVFS・serverless energy-aware scheduling
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-tail-reasoning-8` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T2034JST-discovery-specialist-tail-reasoning-8.json`
  - 探索軸: tail-aware・reasoning phase-aware scheduling
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-model-loading-9` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T2038JST-discovery-specialist-model-loading-9.json`
  - 探索軸: serverless model loading・weight residency・multi-GPU KV migration
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-collective-10` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T2042JST-discovery-specialist-collective-10.json`
  - 探索軸: collective communication圧縮・tensor/expert parallel通信
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2604.24971` — PolyKV: A Shared Asymmetrically-Compressed KV Cache Pool for Multi-Agent LLM Inference / worker `scheduled-chat-llm-survey`
  - claim: **09-16 21:35:41 JST** / heartbeat: **—** / lease expiry: **09-16 23:05:41 JST**
  - evidence: `.survey/work-queue/claims/job-research-9ef38f28c45d6f3a.json`

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
| ready | **31** |

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
| inference/training/survey配下の論文Markdown実体 | **621** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **435** |
| └ Research | **243** |
| └ Audit | **2** |
| └ Discovery | **190** |

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
| 対応jobなしsubmission（有効Discovery round除外） | **9** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **9** |

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
