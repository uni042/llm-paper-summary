# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-25 11:29:52 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **338** |
| 未claim Research job | **194** |
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
| 最終maintenance完了 | **09-24 08:35:53 JST（26時間53分前）** |
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
| Research | **1** | **1** | **0** | **0** | **144** | **13** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **29** | **15** | **14** | **0** | **0** | **0** | **19** |
| 合計 | **30** | **16** | **14** | **0** | **144** | **13** | **19** |

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

- 最新観測run: **2026-09-25 11:27 JST** / worker `scheduled-chat-30`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-8fa24d135cc0417a00493d88.json` (job `job-research-14b72fcf4a8168cf`, failure_class `content_validation`)
  - result: `.survey/work-queue/results/research/attempt-preload-8fa24d135cc0417a00493d88.json` (`ok=false`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-25 11:27 JST** / worker `scheduled-chat-30`
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

- 未失効かつ非terminal jobのclaim: **144件** / 直近15分heartbeat: **13件**
- `DOI:10.1109/JCC72984.2026.00017` — Pegasus: Accelerating Large Language Model Inference with Stateful Prefix Caching / worker `shared-preload-pool`
  - claim: **09-25 11:29:37 JST** / heartbeat: **—** / lease expiry: **09-25 23:29:37 JST**
  - evidence: `.survey/work-queue/claims/job-research-0711131c722ac649.json`
- `arXiv:2606.17081` — The Price of Anarchy in Disaggregated Inference / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-0a4a1c707b0687af.json`
- `DOI:10.1109/ICC59461.2026.11587970` — InKubeator: Pre-warming In-Memory KV Caches from Disk for Elastic LLM Serving / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-2177bbc3f309a697.json`
- `arXiv:2608.10545` — ImpactHO: Importance-Aware KV Cache Transfer for Multi-User Edge LLM Handover / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-2db1a9d83c60d21c.json`
- `arXiv:2602.11688` — GORGO: Online Tuning for Cross-Region Network-Aware LLM Serving / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-352411c0dfdab5c8.json`
- `arXiv:2609.21137` — A Multi-Engine Dataflow for MoE Decoding on Scratchpad-Based Tensor Accelerators / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-5b8f1951128d6fe2.json`
- `arXiv:2609.26828` — Bridging LLM Serving and CXL-SSDs with Chunk-Aware KV Cache Management / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-691c358850b25ecc.json`
- `arXiv:2609.24639` — Analytical Power-Aware Provisioning for Prefill-Decode Disaggregated AI Inference / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-6e051e433e00a10f.json`
- `arXiv:2608.14191` — KV Cache Compression Through the Lens of Transform Coding / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-7b20b235b85d5367.json`
- `arXiv:2605.22106` — ArborKV: Structure-Aware KV Cache Management for Scaling Tree-based LLM Reasoning / worker `scheduled-chat-30`
  - claim: **09-25 11:29:35 JST** / heartbeat: **09-25 11:29:35 JST** / lease expiry: **09-25 12:59:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-aa4e90a77166918d.json`

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
| 成功result未照合のimmutable submission | **272** |
| └ Research | **191** |
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
