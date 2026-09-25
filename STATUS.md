# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-25 11:27:34 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **338** |
| 未claim Research job | **196** |
| 直近24hの検証済みResearch収録 | **18** |
| 最終検証済みResearch収録 | **09-25 11:14:16 JST** |
| 最終検証済みDiscovery探索 | **09-25 10:26:34 JST** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **338** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **338** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6822** |
| 処理済み | **670** |
| 未処理 | **6152** |
| 収録済みとして除外 | **561** |
| 無関係として除外 | **49** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（26時間51分前）** |
| 最終maintenance status | **issues_found** |
| consistency | **passed** |
| health | **issues_found** |
| health errors / warnings | **2 / 0** |
| metadata | **passed** |
| metadata incomplete | **0** |
| GC削除件数 | **631** |
| queue snapshot repaired | **true** |
| index repairs | **0** |
| quality regressions | **3** |

maintenance固有の値は `maintenance-cycle.json` を正本とし、通常のjob/result件数から推定しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **1** | **10** | **0** | **0** | **142** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **29** | **15** | **14** | **0** | **0** | **0** | **19** |
| 合計 | **30** | **25** | **14** | **0** | **142** | **0** | **19** |

- 最新Discovery runの耐久探索round: **15件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-25 11:14:16 JST** [research] `arXiv:2406.11430` — A Simple and Effective L2 Norm-Based Strategy for KV Cache Compression
  - job: `.survey/work-queue/jobs/job-research-12d29ccbbefd4d02.json`
  - result: `.survey/work-queue/results/research/attempt-preload-6b239632cba886a9b742dc0e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-6b239632cba886a9b742dc0e.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2024-2406.11430-l2-kv-compression.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-25 10:26:34 JST** job `job-9a8b589124b7b33a` / 候補 **1件**
  - result: `.survey/work-queue/results/a7d3c1-13b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/a7d3c1-13b.json`
  - 探索軸: forward citations of KVLink efficient KV cache reuse
- **09-25 10:20:58 JST** job `job-ef360b3ddacb49ca` / 候補 **0件**
  - result: `.survey/work-queue/results/closure-a7d3c1-r10b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/closure-a7d3c1-r10b.json`
  - 探索軸: preload-backward-structured-references
- **09-25 10:05:19 JST** job `job-0a660e64270d4061` / 候補 **2件**
  - result: `.survey/work-queue/results/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1.json`
  - 探索軸: forward citations of Sequoia hardware-aware speculative decoding
- **09-25 10:05:26 JST** job `job-fec394bb5d39baf2` / 候補 **1件**
  - result: `.survey/work-queue/results/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1b.json`
  - 探索軸: preload-backward-structured-references
- **09-25 10:19:13 JST** job `job-7e4738ca7f344cca` / 候補 **3件**
  - result: `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r10.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
- **09-25 10:24:30 JST** job `job-2e6202ada7be9311` / 候補 **1件**
  - result: `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r13.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r13.json`
  - 探索軸: preload-backward-structured-references
- **09-25 10:11:27 JST** job `job-fe1bbc1571772ef9` / 候補 **3件**
  - result: `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r4.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
- **09-25 10:16:17 JST** job `job-11fecf63b3805775` / 候補 **1件**
  - result: `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r7.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
- **09-25 10:11:39 JST** job `job-a293defeed05546f` / 候補 **1件**
  - result: `.survey/work-queue/results/frontier-1f4d6cb839c6536c9c6be0c9-s1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/frontier-1f4d6cb839c6536c9c6be0c9-s1.json`
  - 探索軸: preload-backward-structured-references
- **09-25 10:16:27 JST** job `job-5e4a484df8879f17` / 候補 **1件**
  - result: `.survey/work-queue/results/frontier-2dc3d20552047e7e7b31b1a7-s1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/frontier-2dc3d20552047e7e7b31b1a7-s1.json`
  - 探索軸: preload-backward-structured-references

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-25 11:00 JST** / worker `scheduled-chat-00`
- immutable submission: **10件** / 検証済み成功: **0件** / result照合済み非成功: **10件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-13b2710cd58d1521bf8b8e29.json` (job `job-research-058d69df18b4e613`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-13b2710cd58d1521bf8b8e29.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-1d17d0afddf2c45d9cfc2443.json` (job `job-research-79a7b06357194cd1`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-1d17d0afddf2c45d9cfc2443.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-60392f6ae28160ede948e3b0.json` (job `job-research-6be480b73a6003b5`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-60392f6ae28160ede948e3b0.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-62fb2b4c96a75b8d5555856a.json` (job `job-research-0dc5dd60b4569a06`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-62fb2b4c96a75b8d5555856a.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-69ae8a3c79438bfdf2c77a86.json` (job `job-research-ac58200c186f3e5a`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-69ae8a3c79438bfdf2c77a86.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-a20114da784952a527840be6.json` (job `job-research-d13140588fd6d656`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-a20114da784952a527840be6.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-cec830eff891d08a2b883aa0.json` (job `job-research-d70a9b73142dca6a`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-cec830eff891d08a2b883aa0.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-d2a8c1e4593b098380bd5bc9.json` (job `job-research-c97d88c20de27e1f`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-d2a8c1e4593b098380bd5bc9.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-da156dd6a5b5908d24ee393b.json` (job `job-research-b374f59330145700`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-da156dd6a5b5908d24ee393b.json` (`ok=true`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-f2119e1959e44428b62cf540.json` (job `job-research-319ee9e5d994faaf`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-preload-f2119e1959e44428b62cf540.json` (`ok=true`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-25 11:00 JST** / worker `scheduled-chat-00`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-25 10:00 JST**
- 耐久探索round: **15件** / immutable submission: **15件** / 検証済み成功result: **14件** / 個別result照合: **14件** / 個別result未照合: **1件** / 候補: **19件**
- 探索軸: forward / forward citations of KVLink efficient KV cache reuse / preload-backward-structured-references / forward citations of Sequoia hardware-aware speculative decoding / forward citations of LMCache enterprise-scale KV cache layer / forward citations of DistServe disaggregated prefill-decode LLM serving / forward citations of FlexGen offload and hierarchical-memory LLM inference
- round `frontier-0a81cf7d3cc4fc75ac4c1605` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/discovery/a7d3c1-13a.json`
  - 探索軸: forward
  - 個別result照合: なし（immutable round記録は確認済み）
- round `frontier-2eb0f8e747ce792c0837f431` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/discovery/a7d3c1-13b.json`
  - 探索軸: forward citations of KVLink efficient KV cache reuse
  - 個別result照合: あり / `.survey/work-queue/results/a7d3c1-13b.json` (`ok=true`)
- round `frontier-6e420014d069bd1f908e6df1` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/discovery/closure-a7d3c1-r10b.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/closure-a7d3c1-r10b.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1.json`
  - 探索軸: forward citations of Sequoia hardware-aware speculative decoding
  - 個別result照合: あり / `.survey/work-queue/results/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1b` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1b.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/disc-take-scheduled-chat-00-20260925T100045JST-a7d3c1-r1b.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-a7d3c1-r10` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r10.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
  - 個別result照合: あり / `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r10.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-a7d3c1-r13` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r13.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r13.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-a7d3c1-r4` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r4.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r4.json` (`ok=true`)
- round `disc-take-scheduled-chat-00-a7d3c1-r7` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/discovery/disc-take-scheduled-chat-00-a7d3c1-r7.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/disc-take-scheduled-chat-00-a7d3c1-r7.json` (`ok=true`)
- round `frontier-1f4d6cb839c6536c9c6be0c9` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/discovery/frontier-1f4d6cb839c6536c9c6be0c9-s1.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/frontier-1f4d6cb839c6536c9c6be0c9-s1.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **142件** / 直近15分heartbeat: **0件**
- `DOI:10.1109/CVIDL70130.2026.11637503` — FlashSandwich: A Hardware-Aware Hybrid SSM-Transformer Architecture with Optimized KV Cache Management for Efficient LLM Inference / worker `shared-preload-pool`
  - claim: **09-25 11:23:56 JST** / heartbeat: **—** / lease expiry: **09-25 23:23:56 JST**
  - evidence: `.survey/work-queue/claims/job-research-a310d33173ecd821.json`
- `DOI:10.1109/TCAD.2025.3624135` — AsyncGrid: An Intralayer and Interlayer Asynchronous Hybrid Parallelism System for Responsive Edge LLM Inference / worker `shared-preload-pool`
  - claim: **09-25 11:23:56 JST** / heartbeat: **—** / lease expiry: **09-25 23:23:56 JST**
  - evidence: `.survey/work-queue/claims/job-research-a36787e70fb2243e.json`
- `DOI:10.24963/ijcai.2026/475` — Budget-Aware LLM Quantization and Low-Rank Correction via Information-Guided Subspace Matrices / worker `shared-preload-pool`
  - claim: **09-25 11:23:56 JST** / heartbeat: **—** / lease expiry: **09-25 23:23:56 JST**
  - evidence: `.survey/work-queue/claims/job-research-af0c2125c07b340e.json`
- `arXiv:2607.22578` — HeraSys: Collaborative Serving of Multiple LLM Workflows via Fine-Grained End-to-End Optimization / worker `shared-preload-pool`
  - claim: **09-25 11:23:56 JST** / heartbeat: **—** / lease expiry: **09-25 23:23:56 JST**
  - evidence: `.survey/work-queue/claims/job-research-b1f6c436e803c529.json`
- `DOI:10.1109/TCASAI.2026.3670075` — Asymmetric KV Cache Compression Using State-Aware Sparsity and Quantization / worker `shared-preload-pool`
  - claim: **09-25 11:23:56 JST** / heartbeat: **—** / lease expiry: **09-25 23:23:56 JST**
  - evidence: `.survey/work-queue/claims/job-research-f57aeaf97369752d.json`
- `arXiv:2609.23130` — From Inference Engine to Inference Control Plane: Connecting vLLM, llm-d, and the Evolution of Efficient Distributed LLM Serving / worker `shared-preload-pool`
  - claim: **09-25 11:20:20 JST** / heartbeat: **—** / lease expiry: **09-25 23:20:20 JST**
  - evidence: `.survey/work-queue/claims/job-research-82608cb811f87a8c.json`
- `arXiv:2506.07366` — MoE-GPS: Guidlines for Prediction Strategy for Dynamic Expert Duplication in MoE Load Balancing / worker `shared-preload-pool`
  - claim: **09-25 11:18:59 JST** / heartbeat: **—** / lease expiry: **09-25 23:18:59 JST**
  - evidence: `.survey/work-queue/claims/job-research-6884e3d688f660cb.json`
- `DOI:10.1145/3820441.3820479` — Towards Efficient Serving of Network-intensive LLM Inferences / worker `shared-preload-pool`
  - claim: **09-25 11:17:45 JST** / heartbeat: **—** / lease expiry: **09-25 23:17:45 JST**
  - evidence: `.survey/work-queue/claims/job-research-dfcde3edcf70d50d.json`
- `arXiv:2606.05875` — QCFuse: Query-Aware Cache Fusion via Compressed View for Efficient RAG Serving / worker `shared-preload-pool`
  - claim: **09-25 11:17:01 JST** / heartbeat: **—** / lease expiry: **09-25 23:17:01 JST**
  - evidence: `.survey/work-queue/claims/job-research-cb7b62ec78d71f70.json`
- `DOI:10.18653/v1/2026.acl-long.859` — SpecCache: Speculative KV Cache Reuse for Efficient RAG Serving / worker `shared-preload-pool`
  - claim: **09-25 11:17:01 JST** / heartbeat: **—** / lease expiry: **09-25 23:17:01 JST**
  - evidence: `.survey/work-queue/claims/job-research-db4aebb091dc7735.json`

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
| ready | **338** |

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
| inference/training/survey配下の論文Markdown実体 | **1027** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **271** |
| └ Research | **190** |
| └ Audit | **2** |
| └ Discovery | **52** |
| └ Other/Unknown | **27** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **338** |

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
- **構造化references探索状況**: STATUS生成時に `reference_pool.build_reference_pool()` を実行し、paper実体と無関係/微妙台帳から現在値を直接再計算します。過去のprecheck snapshotは件数表示に使いません。
- **日次メンテナンス**: `.survey/work-queue/maintenance-cycle.json` をmaintenance workflowの耐久正本として表示します。通常jobの件数からmaintenance状態を推定しません。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
