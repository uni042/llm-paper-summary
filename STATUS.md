# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-20 15:38:07 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **112** |
| 未claim Research job | **111** |
| 直近24hの検証済みResearch収録 | **68** |
| 最終検証済みResearch収録 | **09-20 15:37:50 JST（17秒前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **112** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **112** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **5380** |
| 処理済み | **527** |
| 未処理 | **4853** |
| 収録済みとして除外 | **419** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- 探索時にpaper実体と無関係/微妙台帳から再計算した値を、schema-v3 precheck resultへ耐久保存して表示します。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **36** | **2** | **2** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **1** | **1** | **0** | **0** | **0** | **5** |
| 合計 | **36** | **3** | **3** | **0** | **1** | **0** | **5** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-20 15:37:50 JST** [research] `arXiv:2503.06823` — eMoE: Task-aware Memory Efficient Mixture-of-Experts-Based (MoE) Model Inference
  - job: `.survey/work-queue/jobs/job-research-bb33e470bd8a5f8f.json`
  - result: `.survey/work-queue/results/research/attempt-01cbf1c46fe8f68f25b18de7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-01cbf1c46fe8f68f25b18de7.json`
  - paper: `papers/inference/06-moe-expert-offloading/2025-2503.06823-emoe.md`
- **09-20 15:33:59 JST** [research] `arXiv:2408.10284` — AdapMoE: Adaptive Sensitivity-based Expert Gating and Management for Efficient MoE Inference
  - job: `.survey/work-queue/jobs/job-research-4892de26a5d749a2.json`
  - result: `.survey/work-queue/results/research/attempt-f2e51bafaabacfadeaecc0ee.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f2e51bafaabacfadeaecc0ee.json`
  - paper: `papers/inference/06-moe-expert-offloading/2024-2408.10284-adapmoe.md`
- **09-20 15:22:39 JST** [research] `arXiv:2506.20675` — Utility-Driven Speculative Decoding for Mixture-of-Experts
  - job: `.survey/work-queue/jobs/job-research-2442fe5802b5c31d.json`
  - result: `.survey/work-queue/results/research/attempt-2f18ec233c0f768fe4b55277.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2f18ec233c0f768fe4b55277.json`
  - paper: `papers/inference/05-speculative-decoding-moe/2025-2506.20675-cascade.md`
- **09-20 15:17:41 JST** [research] `arXiv:2606.02091` — DFlare: Scaling Up Draft Capacity for Block Diffusion Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-f4b6d40ae418a58e.json`
  - result: `.survey/work-queue/results/research/attempt-b269ed373464c47a4c4f738e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-b269ed373464c47a4c4f738e.json`
  - paper: `papers/inference/06-speculative-decoding/2026-2606.02091-dflare.md`
- **09-20 15:14:43 JST** [research] `DOI:10.18653/v1/2025.emnlp-main.1079` — TokenSelect: Efficient Long-Context Inference and Length Extrapolation for LLMs via Dynamic Token-Level KV Cache Selection
  - job: `.survey/work-queue/jobs/job-research-5cec4a19e423bce9.json`
  - result: `.survey/work-queue/results/research/attempt-7fd52d00bf1ebd2f2315994c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-7fd52d00bf1ebd2f2315994c.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2025-token-select.md`
- **09-20 15:10:13 JST** [research] `arXiv:2405.05254` — You Only Cache Once: Decoder-Decoder Architectures for Language Models
  - job: `.survey/work-queue/jobs/job-research-f8d11555626eb92a.json`
  - result: `.survey/work-queue/results/research/attempt-95845744b63d99732374d3b0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-95845744b63d99732374d3b0.json`
  - paper: `papers/inference/06-kv-cache-memory/2024-2405.05254-yoco.md`
- **09-20 15:08:10 JST** [research] `arXiv:2405.03917` — KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization
  - job: `.survey/work-queue/jobs/job-research-be4feb2ff4a84f5b.json`
  - result: `.survey/work-queue/results/research/attempt-bdf0c488544312e64b741a67.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-bdf0c488544312e64b741a67.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2024-2405.03917-coupled-quantization.md`
- **09-20 15:05:08 JST** [research] `arXiv:2503.20552` — Injecting Adrenaline into LLM Serving: Boosting Resource Utilization and Throughput via Attention Disaggregation
  - job: `.survey/work-queue/jobs/job-research-e405cf8340f00512.json`
  - result: `.survey/work-queue/results/research/attempt-89bc644c23d78357d6c68f4d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-89bc644c23d78357d6c68f4d.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2503.20552-adrenaline.md`
- **09-20 15:02:27 JST** [research] `arXiv:2505.23416` — KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction
  - job: `.survey/work-queue/jobs/job-research-d223f7a181256e07.json`
  - result: `.survey/work-queue/results/research/attempt-a81c3fda043b3840209ea896.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a81c3fda043b3840209ea896.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2025-2505.23416-kvzip.md`
- **09-20 15:01:35 JST** [research] `arXiv:2407.02490` — MInference 1.0: Accelerating Pre-filling for Long-Context LLMs via Dynamic Sparse Attention
  - job: `.survey/work-queue/jobs/job-research-51de804389577a72.json`
  - result: `.survey/work-queue/results/research/attempt-0ab84ae32ed1ca16a3e50130.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0ab84ae32ed1ca16a3e50130.json`
  - paper: `papers/inference/10-sparse-attention/2024-2407.02490-minference.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-20 15:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **2件** / 検証済み成功: **2件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- **成功** `arXiv:2503.06823` — eMoE: Task-aware Memory Efficient Mixture-of-Experts-Based (MoE) Model Inference
  - job: `.survey/work-queue/jobs/job-research-bb33e470bd8a5f8f.json`
  - result: `.survey/work-queue/results/research/attempt-01cbf1c46fe8f68f25b18de7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-01cbf1c46fe8f68f25b18de7.json`
  - paper: `papers/inference/06-moe-expert-offloading/2025-2503.06823-emoe.md`
- **成功** `arXiv:2408.10284` — AdapMoE: Adaptive Sensitivity-based Expert Gating and Management for Efficient MoE Inference
  - job: `.survey/work-queue/jobs/job-research-4892de26a5d749a2.json`
  - result: `.survey/work-queue/results/research/attempt-f2e51bafaabacfadeaecc0ee.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-f2e51bafaabacfadeaecc0ee.json`
  - paper: `papers/inference/06-moe-expert-offloading/2024-2408.10284-adapmoe.md`

#### Audit (:30)

- 最新観測run: **2026-09-20 15:30 JST** / worker `scheduled-chat-llm-survey`
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

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2502.07903` — HexGen-2: Disaggregated Generative Inference of LLMs in Heterogeneous Environment / worker `scheduled-chat-discovery-overflow`
  - claim: **09-20 14:16:58 JST** / heartbeat: **09-20 14:32:07 JST** / lease expiry: **09-20 16:02:07 JST**
  - evidence: `.survey/work-queue/claims/job-research-da8147ed3835966f.json`

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
| ready | **112** |

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
| inference/training/survey配下の論文Markdown実体 | **820** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **738** |
| └ Research | **552** |
| └ Audit | **2** |
| └ Discovery | **145** |
| └ Other/Unknown | **39** |

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
- **構造化references探索状況**: schema-v3 repository-reference precheck resultに耐久保存されたprovider進捗を表示します。値自体は探索時にpaper実体と無関係/微妙台帳から再計算されます。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
