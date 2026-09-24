# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-24 17:39:18 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **294** |
| 未claim Research job | **150** |
| 直近24hの検証済みResearch収録 | **20** |
| 最終検証済みResearch収録 | **09-24 17:39:11 JST** |
| 整合性異常 | **22** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **294** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **294** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **6751** |
| 処理済み | **659** |
| 未処理 | **6092** |
| 収録済みとして除外 | **551** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **9.8%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- STATUS生成時にpaper実体と無関係/微妙台帳からゼロベースで再計算します。過去のschema-v3 precheck snapshotは表示値の根拠にしません。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **09-24 08:35:53 JST（9時間3分前）** |
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
| Research | **6** | **2** | **2** | **0** | **144** | **12** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **8** | **5** | **5** | **0** | **0** | **0** | **10** |
| 合計 | **14** | **7** | **7** | **0** | **144** | **12** | **10** |

- 最新Discovery runの耐久探索round: **5件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-24 17:39:11 JST** [research] `arXiv:2606.20537` — Execution-State Capsules: Graph-Bound Execution-State Checkpoint and Restore for Low-Latency, Small-Batch, On-Device Physical-AI Serving
  - job: `.survey/work-queue/jobs/job-research-374463a300b97ed5.json`
  - result: `.survey/work-queue/results/research/attempt-preload-3c754529c6f791ee0cbc78c5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-3c754529c6f791ee0cbc78c5.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2606.20537-execution-state-capsules-graph-bound-execution-state-checkpoint-and-restore-for-low-latency-small-batch-on-device-physic.md`
- **09-24 15:48:57 JST** [research] `arXiv:2511.06174` — LUT-LLM: Efficient Large Language Model Inference with Memory-based Computations on FPGAs
  - job: `.survey/work-queue/jobs/job-research-20dfb7993995c1a7.json`
  - result: `.survey/work-queue/results/research/attempt-preload-adcf408437d27a8a65fe0220.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-adcf408437d27a8a65fe0220.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2511.06174-lut-llm-efficient-large-language-model-inference-with-memory-based-computations-on-fpgas.md`
- **09-24 15:37:58 JST** [research] `arXiv:2312.00752` — Mamba: Linear-Time Sequence Modeling with Selective State Spaces
  - job: `.survey/work-queue/jobs/job-research-7526ab28b3c65fc4.json`
  - result: `.survey/work-queue/results/research/attempt-preload-270cf0686ddf08989a01feb5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-270cf0686ddf08989a01feb5.json`
  - paper: `papers/inference/99-other-inference-systems/2023-2312.00752-mamba-selective-state-space-linear-time-inference.md`
- **09-24 13:39:58 JST** [research] `arXiv:2601.08833` — Revisiting Disaggregated Large Language Model Serving for Performance and Energy Implications
  - job: `.survey/work-queue/jobs/job-research-0023a21511f803e1.json`
  - result: `.survey/work-queue/results/research/attempt-preload-54435f3f1e70e6def8dfca02.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-54435f3f1e70e6def8dfca02.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2601.08833-revisiting-disaggregated-large-language-model-serving-for-performance-and-energy-implications.md`
- **09-24 13:37:49 JST** [research] `arXiv:2511.01633` — Scaling Graph Chain-of-Thought Reasoning: A Multi-Agent Framework with Efficient LLM Serving
  - job: `.survey/work-queue/jobs/job-research-2a8c8a978e102c67.json`
  - result: `.survey/work-queue/results/research/attempt-preload-38c87a832a14fb80d3b5b6c4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-38c87a832a14fb80d3b5b6c4.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2511.01633-graph-cot-multi-agent-efficient-serving.md`
- **09-24 13:35:46 JST** [research] `arXiv:1904.10509` — Generating Long Sequences with Sparse Transformers
  - job: `.survey/work-queue/jobs/job-research-e642f12f51409df8.json`
  - result: `.survey/work-queue/results/research/attempt-preload-1f8a910c2a57d30ce56d66d0.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-1f8a910c2a57d30ce56d66d0.json`
  - paper: `papers/inference/99-other-inference-systems/2019-1904.10509-generating-long-sequences-with-sparse-transformers.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-24 16:02:32 JST** job `job-589818bf1fa4284e` / 候補 **2件**
  - result: `.survey/work-queue/results/20260924T070200Z-scheduled-chat-00-a3f91c-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T070200Z-scheduled-chat-00-a3f91c-r1.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
- **09-24 16:05:19 JST** job `job-3529923241c3e6b2` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T070400Z-scheduled-chat-00-a3f91c-r2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T070400Z-scheduled-chat-00-a3f91c-r2.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
- **09-24 16:07:05 JST** job `job-c1d55ae9db6fc359` / 候補 **2件**
  - result: `.survey/work-queue/results/20260924T070630Z-scheduled-chat-00-a3f91c-r3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T070630Z-scheduled-chat-00-a3f91c-r3.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
- **09-24 16:08:42 JST** job `job-e6b42b393dcebba1` / 候補 **2件**
  - result: `.survey/work-queue/results/20260924T070815Z-scheduled-chat-00-a3f91c-r4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T070815Z-scheduled-chat-00-a3f91c-r4.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
- **09-24 16:10:52 JST** job `job-aa8fdeb4b9b6ac4b` / 候補 **3件**
  - result: `.survey/work-queue/results/20260924T071000Z-scheduled-chat-00-a3f91c-r5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T071000Z-scheduled-chat-00-a3f91c-r5.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
- **09-24 15:04:55 JST** job `job-d99c1a1848cb9828` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T060123Z-scheduled-chat-00-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T060123Z-scheduled-chat-00-r1.json`
  - 探索軸: backward structured repository references
- **09-24 14:38:21 JST** job `job-f64ea010e4ce703c` / 候補 **1件**
  - result: `.survey/work-queue/results/20260924T053120Z-scheduled-chat-30-d4a731-r2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T053120Z-scheduled-chat-30-d4a731-r2.json`
  - 探索軸: preload-backward-structured-references
- **09-24 14:01:48 JST** job `job-1263040a0c1ed016` / 候補 **0件**
  - result: `.survey/work-queue/results/20260924T050100Z-scheduled-chat-00-c6e4-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260924T050100Z-scheduled-chat-00-c6e4-r1.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-24 15:32 JST** / worker `scheduled-chat-30`
- immutable submission: **2件** / 検証済み成功: **2件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- **成功** `arXiv:2312.00752` — Mamba: Linear-Time Sequence Modeling with Selective State Spaces
  - job: `.survey/work-queue/jobs/job-research-7526ab28b3c65fc4.json`
  - result: `.survey/work-queue/results/research/attempt-preload-270cf0686ddf08989a01feb5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-270cf0686ddf08989a01feb5.json`
  - paper: `papers/inference/99-other-inference-systems/2023-2312.00752-mamba-selective-state-space-linear-time-inference.md`
- **成功** `arXiv:2511.06174` — LUT-LLM: Efficient Large Language Model Inference with Memory-based Computations on FPGAs
  - job: `.survey/work-queue/jobs/job-research-20dfb7993995c1a7.json`
  - result: `.survey/work-queue/results/research/attempt-preload-adcf408437d27a8a65fe0220.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-preload-adcf408437d27a8a65fe0220.json`
  - paper: `papers/inference/99-other-inference-systems/2025-2511.06174-lut-llm-efficient-large-language-model-inference-with-memory-based-computations-on-fpgas.md`

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-24 15:32 JST** / worker `scheduled-chat-30`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-24 16:00 JST**
- 耐久探索round: **5件** / immutable submission: **5件** / 検証済み成功result: **5件** / 個別result照合: **5件** / 個別result未照合: **0件** / 候補: **10件**
- 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving / forward citations of FlexGen offload and hierarchical-memory LLM inference
- round `20260924T070008Z-scheduled-chat-00-a3f91c-take1` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260924T070200Z-scheduled-chat-00-a3f91c-r1.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/20260924T070200Z-scheduled-chat-00-a3f91c-r1.json` (`ok=true`)
- round `20260924T070300Z-scheduled-chat-00-a3f91c-r2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260924T070400Z-scheduled-chat-00-a3f91c-r2.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: あり / `.survey/work-queue/results/20260924T070400Z-scheduled-chat-00-a3f91c-r2.json` (`ok=true`)
- round `20260924T070530Z-scheduled-chat-00-a3f91c-r3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260924T070630Z-scheduled-chat-00-a3f91c-r3.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/20260924T070630Z-scheduled-chat-00-a3f91c-r3.json` (`ok=true`)
- round `20260924T070715Z-scheduled-chat-00-a3f91c-r4` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260924T070815Z-scheduled-chat-00-a3f91c-r4.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/20260924T070815Z-scheduled-chat-00-a3f91c-r4.json` (`ok=true`)
- round `20260924T070900Z-scheduled-chat-00-a3f91c-r5` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260924T071000Z-scheduled-chat-00-a3f91c-r5.json`
  - 探索軸: backward references of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: あり / `.survey/work-queue/results/20260924T071000Z-scheduled-chat-00-a3f91c-r5.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **144件** / 直近15分heartbeat: **12件**
- `arXiv:2603.09023` — The Missing Memory Hierarchy: Demand Paging for LLM Context Windows / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-105b69444b4fa0ad.json`
- `arXiv:2508.15487` — Dream 7B: Diffusion Large Language Models / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-1ba7917ba260cdda.json`
- `arXiv:2509.12211` — TinyServe: Query-Aware Cache Selection for Efficient LLM Serving / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-3d37c9d48dc78998.json`
- `arXiv:2609.26796` — Flash-dLLM: IO-Aware KV Caching and Parallel Decoding for Fast, Memory-Efficient Diffusion LLMs / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-41d37332b16e3d57.json`
- `DOI:10.1145/3806645.3807596` — Scaling Attention Beyond GPUs for LLM Inference / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-5bd282d7c260721a.json`
- `arXiv:2310.01889` — Ring Attention with Blockwise Transformers for Near-Infinite Context / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-60b244663bfce823.json`
- `arXiv:2609.26300` — CompKV: Compensation-Aware KV Selection for Long-Context LLM Inference / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-7ecc4d7949c81534.json`
- `arXiv:2505.16502` — Recursive Offloading for LLM Serving in Multi-tier Networks / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-df8b6eaefcbe8aad.json`
- `arXiv:2606.09508` — From Rigid to Dynamic: Entropy-Guided Adaptive Inference for Long-Context LLMs / worker `scheduled-chat-30`
  - claim: **09-24 17:37:35 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-e37f81d7634eb52b.json`
- `arXiv:2606.24033` — RoPE-Aware Bit Allocation for KV-Cache Quantization / worker `scheduled-chat-30`
  - claim: **09-24 17:29:26 JST** / heartbeat: **09-24 17:37:35 JST** / lease expiry: **09-24 19:07:35 JST**
  - evidence: `.survey/work-queue/claims/job-research-ed39f178b202751f.json`

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
| ready | **294** |

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
| inference/training/survey配下の論文Markdown実体 | **1015** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **301** |
| └ Research | **169** |
| └ Audit | **2** |
| └ Discovery | **71** |
| └ Other/Unknown | **59** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **338** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。

| 検出項目 | 件数 |
|---|---:|
| completed Research jobで指定paper実体なし | **22** |
| 対応jobなしsubmission（有効Discovery round除外） | **0** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **22** |

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
