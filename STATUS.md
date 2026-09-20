# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-20 09:39:34 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **87** |
| 未claim Research job | **87** |
| 直近24hの検証済みResearch収録 | **40** |
| 最終検証済みResearch収録 | **09-20 09:39:31 JST（3秒前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **87** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **87** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **12** | **2** | **2** | **0** | **0** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **1** | **1** | **0** | **0** | **0** | **5** |
| 合計 | **12** | **3** | **3** | **0** | **0** | **0** | **5** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-20 09:39:31 JST** [research] `arXiv:2401.18079` — KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization
  - job: `.survey/work-queue/jobs/job-research-6e90b18bc4767f7c.json`
  - result: `.survey/work-queue/results/research/attempt-1e7b670e9a35584762c55c56.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1e7b670e9a35584762c55c56.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2024-2401.18079-kvquant.md`
- **09-20 09:35:29 JST** [research] `arXiv:2309.17453` — Efficient Streaming Language Models with Attention Sinks
  - job: `.survey/work-queue/jobs/job-research-e12ae17b96a85ee5.json`
  - result: `.survey/work-queue/results/research/attempt-d96484c2d2d3c4cd1838a754.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d96484c2d2d3c4cd1838a754.json`
  - paper: `papers/inference/05-kv-cache-memory-management/2023-2309.17453-streamingllm.md`
- **09-20 06:47:50 JST** [research] `arXiv:2308.16369` — SARATHI: Efficient LLM Inference by Piggybacking Decodes with Chunked Prefills
  - job: `.survey/work-queue/jobs/job-research-576a090cf3d34dc3.json`
  - result: `.survey/work-queue/results/research/attempt-aabaad10b18cbdb1c36dc544.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-aabaad10b18cbdb1c36dc544.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2023-2308.16369-sarathi.md`
- **09-20 06:44:57 JST** [research] `arXiv:2405.01814` — Efficient and Economic Large Language Model Inference with Attention Offloading
  - job: `.survey/work-queue/jobs/job-research-ac3d391d822b215f.json`
  - result: `.survey/work-queue/results/research/attempt-fa744ec1780cd6efcfcf4336.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-fa744ec1780cd6efcfcf4336.json`
  - paper: `papers/inference/01-offload-hierarchical-memory/2024-2405.01814-attention-offloading.md`
- **09-20 06:42:02 JST** [research] `arXiv:2503.16525` — KVShare: An LLM Service System with Efficient and Effective Multi-Tenant KV Cache Reuse
  - job: `.survey/work-queue/jobs/job-research-b33b8317e97d5549.json`
  - result: `.survey/work-queue/results/research/attempt-d80fbebf0499dacc4d34fe5f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d80fbebf0499dacc4d34fe5f.json`
  - paper: `papers/inference/10-kv-cache-offload-recomputation/2025-2503.16525-kvshare.md`
- **09-20 05:45:06 JST** [research] `arXiv:2503.01840` — EAGLE-3: Scaling up Inference Acceleration of Large Language Models via Training-Time Test
  - job: `.survey/work-queue/jobs/job-research-e279074fae9402fc.json`
  - result: `.survey/work-queue/results/research/attempt-19f5527d6ca7024729812f1a.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-19f5527d6ca7024729812f1a.json`
  - paper: `papers/inference/05-speculative-decoding/2025-2503.01840-eagle-3.md`
- **09-20 05:40:52 JST** [research] `arXiv:2306.00978` — AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration
  - job: `.survey/work-queue/jobs/job-research-d5e83a73eb90a616.json`
  - result: `.survey/work-queue/results/research/attempt-e2c1eb9d827322f9fbb93f0b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e2c1eb9d827322f9fbb93f0b.json`
  - paper: `papers/inference/08-quantization-kernels/2023-2306.00978-awq.md`
- **09-20 05:37:39 JST** [research] `arXiv:2411.01433` — HOBBIT: A Mixed Precision Expert Offloading System for Fast MoE Inference
  - job: `.survey/work-queue/jobs/job-research-53def9917e580440.json`
  - result: `.survey/work-queue/results/research/attempt-58ec9dfded7ec0db6d9bb446.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-58ec9dfded7ec0db6d9bb446.json`
  - paper: `papers/inference/04-moe-expert-offload-caching/2024-2411.01433-hobbit.md`
- **09-20 05:33:07 JST** [research] `arXiv:2312.12456` — PowerInfer: Fast Large Language Model Serving with a Consumer-grade GPU
  - job: `.survey/work-queue/jobs/job-research-b41274093aac35dc.json`
  - result: `.survey/work-queue/results/research/attempt-84eae2b617467dab6d9fa45e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-84eae2b617467dab6d9fa45e.json`
  - paper: `papers/inference/02-cpu-offload/2023-2312.12456-powerinfer.md`
- **09-20 04:35:23 JST** [research] `arXiv:2211.17192` — Fast Inference from Transformers via Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-d0436ba646148687.json`
  - result: `.survey/work-queue/results/research/attempt-5dce2562aaf6112c45659534.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-5dce2562aaf6112c45659534.json`
  - paper: `papers/inference/05-speculative-decoding/2022-2211.17192-speculative-decoding.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-20 09:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **2件** / 検証済み成功: **2件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- **成功** `arXiv:2401.18079` — KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization
  - job: `.survey/work-queue/jobs/job-research-6e90b18bc4767f7c.json`
  - result: `.survey/work-queue/results/research/attempt-1e7b670e9a35584762c55c56.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1e7b670e9a35584762c55c56.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2024-2401.18079-kvquant.md`
- **成功** `arXiv:2309.17453` — Efficient Streaming Language Models with Attention Sinks
  - job: `.survey/work-queue/jobs/job-research-e12ae17b96a85ee5.json`
  - result: `.survey/work-queue/results/research/attempt-d96484c2d2d3c4cd1838a754.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-d96484c2d2d3c4cd1838a754.json`
  - paper: `papers/inference/05-kv-cache-memory-management/2023-2309.17453-streamingllm.md`

#### Audit (:30)

- 最新観測run: **2026-09-20 09:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-20 01:58 JST**
- 耐久探索round: **1件** / immutable submission: **1件** / 検証済み成功result: **1件** / 個別result照合: **1件** / 個別result未照合: **0件** / 候補: **5件**
- 探索軸: MoE expert cache offload placement prefetch inference systems
- round `specialist-moe-offload-openalex-02` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/20260920T0204JST-specialist-moe-openalex-round1.json`
  - 探索軸: MoE expert cache offload placement prefetch inference systems
  - 個別result照合: あり / `.survey/work-queue/results/20260920T0204JST-specialist-moe-openalex-round1.json` (`ok=true`)

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
| ready | **87** |

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
| inference/training/survey配下の論文Markdown実体 | **785** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **677** |
| └ Research | **516** |
| └ Audit | **2** |
| └ Discovery | **145** |
| └ Other/Unknown | **14** |

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
