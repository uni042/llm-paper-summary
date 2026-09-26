# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-26 09:53:56 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **363** |
| 未claim Research job | **220** |
| 直近24hの検証済みResearch収録 | **1** |
| 最終検証済みResearch収録 | **09-25 11:14:16 JST** |
| 最終検証済みDiscovery探索 | **09-26 04:45:42 JST** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **363** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **363** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6920** |
| 処理済み | **685** |
| 未処理 | **6235** |
| 収録済みとして除外 | **576** |
| 無関係として除外 | **49** |
| 微妙として除外 | **60** |

- 消化率: **9.9%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（49時間18分前）** |
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
| Research | **0** | **1** | **0** | **0** | **143** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **8** | **8** | **8** | **0** | **0** | **0** | **25** |
| 合計 | **8** | **9** | **8** | **0** | **143** | **0** | **25** |

- 最新Discovery runの耐久探索round: **8件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- 検証済み完了なし。

### Audit

- 検証済み完了なし。

### Discovery

- **09-26 04:44:32 JST** job `job-9db2b5b0b2f3aa5b` / 候補 **0件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r1.json`
  - 探索軸: preload-backward-structured-references
- **09-26 04:44:42 JST** job `job-97cfd21275e9e4d9` / 候補 **2件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r10.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r10.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
- **09-26 04:44:52 JST** job `job-208cd0625392efed` / 候補 **3件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r12.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r12.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
- **09-26 04:45:02 JST** job `job-e912f73545c40dcc` / 候補 **4件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r14.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r14.json`
  - 探索軸: forward citations of FlashAttention for recent attention kernels and serving systems
- **09-26 04:45:12 JST** job `job-d662bd433d0b13a5` / 候補 **4件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r2.json`
  - 探索軸: forward citations of Splitwise for disaggregated LLM serving
- **09-26 04:45:22 JST** job `job-01f23705ea94c7f5` / 候補 **3件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r4.json`
  - 探索軸: forward citations of Sequoia hardware-aware speculative decoding
- **09-26 04:45:32 JST** job `job-352dc27107234839` / 候補 **5件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r7.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
- **09-26 04:45:42 JST** job `job-441a11f4966dbc81` / 候補 **4件**
  - result: `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r9.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r9.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference

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

- 最新観測run: **2026-09-26 04:31 JST**
- 耐久探索round: **8件** / immutable submission: **8件** / 検証済み成功result: **8件** / 個別result照合: **8件** / 個別result未照合: **0件** / 候補: **25件**
- 探索軸: preload-backward-structured-references / forward citations of LMCache enterprise-scale KV cache layer / forward citations of FlexGen offload and hierarchical-memory LLM inference / forward citations of FlashAttention for recent attention kernels and serving systems / forward citations of Splitwise for disaggregated LLM serving / forward citations of Sequoia hardware-aware speculative decoding / forward citations of DistServe disaggregated prefill-decode LLM serving
- round `round-1` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r1.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r1.json` (`ok=true`)
- round `round-10` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r10.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r10.json` (`ok=true`)
- round `round-12` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r12.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r12.json` (`ok=true`)
- round `round-14` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r14.json`
  - 探索軸: forward citations of FlashAttention for recent attention kernels and serving systems
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r14.json` (`ok=true`)
- round `round-2` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r2.json`
  - 探索軸: forward citations of Splitwise for disaggregated LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r2.json` (`ok=true`)
- round `round-4` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r4.json`
  - 探索軸: forward citations of Sequoia hardware-aware speculative decoding
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r4.json` (`ok=true`)
- round `round-7` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r7.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r7.json` (`ok=true`)
- round `round-9` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r9.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/take-scheduled-chat-30-20260926T043136JST-r9.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **143件** / 直近15分heartbeat: **0件**
- `arXiv:2609.29160` — Cross-Model Autoscaling for Shared LLM Serving / worker `shared-preload-pool`
  - claim: **09-26 08:58:27 JST** / heartbeat: **—** / lease expiry: **09-26 20:58:27 JST**
  - evidence: `.survey/work-queue/claims/job-research-6159ba9a55bd9185.json`
- `DOI:10.1109/ISCA66397.2026.00075` — ConServe: Contiguity-Preserving Memory Management for Multi-Turn LLM Serving / worker `shared-preload-pool`
  - claim: **09-26 08:58:27 JST** / heartbeat: **—** / lease expiry: **09-26 20:58:27 JST**
  - evidence: `.survey/work-queue/claims/job-research-84b0ef584444fe0c.json`
- `DOI:10.48550/arXiv.2604.05438` — Top-K Retrieval with Fixed-Size Linear-Attention Completion: Backbone- and KV-Format-Preserving Attention for KV-Cache Read Reduction / worker `shared-preload-pool`
  - claim: **09-26 08:58:27 JST** / heartbeat: **—** / lease expiry: **09-26 20:58:27 JST**
  - evidence: `.survey/work-queue/claims/job-research-a1c3413c4a8ae02e.json`
- `arXiv:2605.11335` — ChunkFlow: Communication-Aware Chunked Prefetching for Layerwise Offloading in Distributed Diffusion Transformer Inference / worker `shared-preload-pool`
  - claim: **09-26 08:58:27 JST** / heartbeat: **—** / lease expiry: **09-26 20:58:27 JST**
  - evidence: `.survey/work-queue/claims/job-research-b39cc165ac1a1603.json`
- `DOI:10.1109/icassp55912.2026.11461518` — MIDAS: A Dynamic Cross-GPU KV Cache Offloading Framework for LLM on GPU Cluster Systems / worker `shared-preload-pool`
  - claim: **09-26 08:58:27 JST** / heartbeat: **—** / lease expiry: **09-26 20:58:27 JST**
  - evidence: `.survey/work-queue/claims/job-research-be3f3ff5538b9239.json`
- `DOI:10.1109/CLOUD72782.2026.00039` — Reducing Memory Requirements of LLM Inference Through Online rANS Decompression / worker `shared-preload-pool`
  - claim: **09-26 08:58:27 JST** / heartbeat: **—** / lease expiry: **09-26 20:58:27 JST**
  - evidence: `.survey/work-queue/claims/job-research-d789244346ced549.json`
- `arXiv:2609.25451` — Fast Recovery for LLM Serving via Decoupled Device Memory Lifetime in Dynamo / worker `scheduled-chat-00`
  - claim: **09-26 08:58:26 JST** / heartbeat: **09-26 08:58:26 JST** / lease expiry: **09-26 10:28:26 JST**
  - evidence: `.survey/work-queue/claims/job-research-05fc71d26e12a3ee.json`
- `arXiv:2405.07135` — Post Training Quantization of Large Language Models with Microscaling Formats / worker `scheduled-chat-00`
  - claim: **09-26 08:58:26 JST** / heartbeat: **09-26 08:58:26 JST** / lease expiry: **09-26 10:28:26 JST**
  - evidence: `.survey/work-queue/claims/job-research-47d3b689c2eeb296.json`
- `arXiv:2512.21835` — Collaborative Lossless LLM Inference Serving with Offloading-based Pipeline Parallelism on Edge Devices / worker `scheduled-chat-00`
  - claim: **09-26 08:58:26 JST** / heartbeat: **09-26 08:58:26 JST** / lease expiry: **09-26 10:28:26 JST**
  - evidence: `.survey/work-queue/claims/job-research-5c9711465b85e7cf.json`
- `DOI:10.1109/2575-8411.2026.00033` — Efficient KV Cache Migration for Geo-Distributed LLM Inference in Collaborative Edge Computing / worker `scheduled-chat-00`
  - claim: **09-26 08:58:26 JST** / heartbeat: **09-26 08:58:26 JST** / lease expiry: **09-26 10:28:26 JST**
  - evidence: `.survey/work-queue/claims/job-research-65c097d84dfa8adf.json`

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
| ready | **363** |

### 候補の重複・識別情報欠損

非終端Research jobだけを対象にしています。source URLは `url/source_url/paper_url/primary_url/arxiv_url/pdf_url/source.url` のいずれかで確認します。

| 指標 | 件数 |
|---|---:|
| 重複canonical_idグループ | **0** |
| 重複分のResearch job | **0** |
| canonical_id欠損 | **0** |
| title欠損 | **3** |
| source URL欠損 | **0** |

### 収録済み論文実体

`papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README、comparison系、Movedスタブを除外します。

| 指標 | 件数 |
|---|---:|
| inference/training/survey配下の論文Markdown実体 | **1049** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **280** |
| └ Research | **192** |
| └ Audit | **2** |
| └ Discovery | **59** |
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
