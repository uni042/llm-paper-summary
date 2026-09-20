# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-20 12:14:47 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **79** |
| 未claim Research job | **78** |
| 直近24hの検証済みResearch収録 | **43** |
| 最終検証済みResearch収録 | **09-20 12:11:09 JST（3分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **79** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **79** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **15** | **8** | **7** | **1** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **1** | **1** | **0** | **0** | **0** | **5** |
| 合計 | **15** | **9** | **8** | **1** | **1** | **0** | **5** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-20 12:11:09 JST** [research] `arXiv:2402.02750` — KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache
  - job: `.survey/work-queue/jobs/job-research-8b52cc53189781e3.json`
  - result: `.survey/work-queue/results/research/attempt-6d86d84ba0b861b36b84973e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6d86d84ba0b861b36b84973e.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2024-2402.02750-kivi.md`
- **09-20 12:07:28 JST** [research] `arXiv:2006.16668` — GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
  - job: `.survey/work-queue/jobs/job-research-710ff1d6feeafd76.json`
  - result: `.survey/work-queue/results/research/attempt-85841135c44788f4cd9b5a81.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-85841135c44788f4cd9b5a81.json`
  - paper: `papers/training/02-distributed-heterogeneous-moe-training/2020-2006.16668-gshard.md`
- **09-20 12:03:55 JST** [research] `arXiv:2309.08168` — Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-06ec3586821ff3bb.json`
  - result: `.survey/work-queue/results/research/attempt-494231538c84c48296aa17b3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-494231538c84c48296aa17b3.json`
  - paper: `papers/inference/05-speculative-decoding/2023-2309.08168-draft-verify.md`
- **09-20 11:55:25 JST** [research] `arXiv:2502.16002` — KVLink: Accelerating Large Language Models via Efficient KV Cache Reuse
  - job: `.survey/work-queue/jobs/job-research-f018d8c28f4995e5.json`
  - result: `.survey/work-queue/results/research/attempt-098c5b91676f2a1a4d4737af.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-098c5b91676f2a1a4d4737af.json`
  - paper: `papers/inference/10-kv-cache-offload-recomputation/2025-2502.16002-kvlink.md`
- **09-20 11:51:33 JST** [research] `DOI:10.48550/arxiv.2307.08691` — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
  - job: `.survey/work-queue/jobs/job-research-7462825d21914fcd.json`
  - result: `.survey/work-queue/results/research/attempt-22a85da9fa40ba86114440e5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-22a85da9fa40ba86114440e5.json`
  - paper: `papers/inference/09-attention-kernel-serving-optimization/2023-2307.08691-flashattention-2.md`
- **09-20 11:47:29 JST** [research] `DOI:10.48550/arxiv.2302.01318` — Accelerating Large Language Model Decoding with Speculative Sampling
  - job: `.survey/work-queue/jobs/job-research-954a443cf32500d8.json`
  - result: `.survey/work-queue/results/research/attempt-6500850523776f2b702f4a6d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6500850523776f2b702f4a6d.json`
  - paper: `papers/inference/05-speculative-decoding/2023-2302.01318-speculative-sampling.md`
- **09-20 11:42:15 JST** [research] `DOI:10.1145/3731569.3764815` — Aegaeon: Effective GPU Pooling for Concurrent LLM Serving on the Market
  - job: `.survey/work-queue/jobs/job-research-a568c8de790c8043.json`
  - result: `.survey/work-queue/results/research/attempt-4aedf8f4b7b74e0c27817979.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4aedf8f4b7b74e0c27817979.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-3731569.3764815-aegaeon-gpu-pooling.md`
- **09-20 09:51:20 JST** [research] `arXiv:2408.00741` — DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency
  - job: `.survey/work-queue/jobs/job-research-872c3c76cc1c3eff.json`
  - result: `.survey/work-queue/results/research/attempt-a3583b512bca09151ba946d2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a3583b512bca09151ba946d2.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2024-2408.00741-dynamollm.md`
- **09-20 09:47:41 JST** [research] `arXiv:2308.14352` — EdgeMoE: Empowering Sparse Large Language Models on Mobile Devices
  - job: `.survey/work-queue/jobs/job-research-42834c639c34d742.json`
  - result: `.survey/work-queue/results/research/attempt-a86622b38716752ba65bde87.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a86622b38716752ba65bde87.json`
  - paper: `papers/inference/08-edge-on-device-llm-systems/2023-2308.14352-edgemoe.md`
- **09-20 09:41:50 JST** [research] `arXiv:2306.14048` — H2O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models
  - job: `.survey/work-queue/jobs/job-research-9824d8080e264ed4.json`
  - result: `.survey/work-queue/results/research/attempt-0b14b95da2b3a2abc2e9855f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-0b14b95da2b3a2abc2e9855f.json`
  - paper: `papers/inference/07-kv-cache-optimization-compression/2023-2306.14048-h2o.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-20 11:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **8件** / 検証済み成功: **7件** / result照合済み非成功: **0件** / 個別result未照合: **1件**
- **成功** `arXiv:2502.16002` — KVLink: Accelerating Large Language Models via Efficient KV Cache Reuse
  - job: `.survey/work-queue/jobs/job-research-f018d8c28f4995e5.json`
  - result: `.survey/work-queue/results/research/attempt-098c5b91676f2a1a4d4737af.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-098c5b91676f2a1a4d4737af.json`
  - paper: `papers/inference/10-kv-cache-offload-recomputation/2025-2502.16002-kvlink.md`
- **成功** `DOI:10.48550/arxiv.2307.08691` — FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning
  - job: `.survey/work-queue/jobs/job-research-7462825d21914fcd.json`
  - result: `.survey/work-queue/results/research/attempt-22a85da9fa40ba86114440e5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-22a85da9fa40ba86114440e5.json`
  - paper: `papers/inference/09-attention-kernel-serving-optimization/2023-2307.08691-flashattention-2.md`
- **成功** `arXiv:2309.08168` — Draft & Verify: Lossless Large Language Model Acceleration via Self-Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-06ec3586821ff3bb.json`
  - result: `.survey/work-queue/results/research/attempt-494231538c84c48296aa17b3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-494231538c84c48296aa17b3.json`
  - paper: `papers/inference/05-speculative-decoding/2023-2309.08168-draft-verify.md`
- **成功** `DOI:10.1145/3731569.3764815` — Aegaeon: Effective GPU Pooling for Concurrent LLM Serving on the Market
  - job: `.survey/work-queue/jobs/job-research-a568c8de790c8043.json`
  - result: `.survey/work-queue/results/research/attempt-4aedf8f4b7b74e0c27817979.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4aedf8f4b7b74e0c27817979.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-3731569.3764815-aegaeon-gpu-pooling.md`
- **成功** `DOI:10.48550/arxiv.2302.01318` — Accelerating Large Language Model Decoding with Speculative Sampling
  - job: `.survey/work-queue/jobs/job-research-954a443cf32500d8.json`
  - result: `.survey/work-queue/results/research/attempt-6500850523776f2b702f4a6d.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6500850523776f2b702f4a6d.json`
  - paper: `papers/inference/05-speculative-decoding/2023-2302.01318-speculative-sampling.md`
- **成功** `arXiv:2402.02750` — KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache
  - job: `.survey/work-queue/jobs/job-research-8b52cc53189781e3.json`
  - result: `.survey/work-queue/results/research/attempt-6d86d84ba0b861b36b84973e.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-6d86d84ba0b861b36b84973e.json`
  - paper: `papers/inference/05-kv-cache-compression-quantization/2024-2402.02750-kivi.md`
- **個別result未照合** `.survey/work-queue/submissions/research/attempt-74f796116b0c55afd81f6ad5.json` (job `job-research-8fc74c0fbb46c30e`)
- **成功** `arXiv:2006.16668` — GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding
  - job: `.survey/work-queue/jobs/job-research-710ff1d6feeafd76.json`
  - result: `.survey/work-queue/results/research/attempt-85841135c44788f4cd9b5a81.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-85841135c44788f4cd9b5a81.json`
  - paper: `papers/training/02-distributed-heterogeneous-moe-training/2020-2006.16668-gshard.md`

#### Audit (:30)

- 最新観測run: **2026-09-20 11:30 JST** / worker `scheduled-chat-llm-survey`
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
- `arXiv:2406.10774` — Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference / worker `scheduled-chat-llm-survey`
  - claim: **09-20 12:13:58 JST** / heartbeat: **—** / lease expiry: **09-20 13:43:58 JST**
  - evidence: `.survey/work-queue/claims/job-research-8fc74c0fbb46c30e.json`

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
| ready | **79** |

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
| inference/training/survey配下の論文Markdown実体 | **795** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **686** |
| └ Research | **525** |
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
