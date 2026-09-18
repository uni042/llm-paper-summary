# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-18 16:03:31 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **49** |
| 未claim Research job | **48** |
| 直近24hの検証済みResearch収録 | **48** |
| 最終検証済みResearch収録 | **09-18 14:45:14 JST（1時間18分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **49** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **49** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **7** | **6** | **3** | **3** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **22** | **7** | **1** | **6** | **0** | **0** | **26** |
| 合計 | **29** | **13** | **4** | **9** | **1** | **0** | **26** |

- 最新Discovery runの耐久探索round: **7件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-18 14:45:14 JST** [research] `arXiv:2508.02558` — Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction
  - job: `.survey/work-queue/jobs/job-research-2829f7afbf13ae9b.json`
  - result: `.survey/work-queue/results/research/attempt-134d632c037ba813a7f76d95.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-134d632c037ba813a7f76d95.json`
  - paper: `papers/inference/06-kv-cache-memory/2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md`
- **09-18 14:44:01 JST** [research] `arXiv:2511.22333` — PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel
  - job: `.survey/work-queue/jobs/job-research-a2e0c7f004aa0b3e.json`
  - result: `.survey/work-queue/results/research/attempt-3eb6a05e4e42907dd24b50f1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3eb6a05e4e42907dd24b50f1.json`
  - paper: `papers/inference/03-kv-cache/2025-2511.22333-pat-prefix-aware-attention-multi-tile-kernel.md`
- **09-18 14:37:48 JST** [research] `arXiv:2609.17652` — Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches
  - job: `.survey/work-queue/jobs/job-research-78d3e9d2047890ea.json`
  - result: `.survey/work-queue/results/research/attempt-63cfbded74c721cbf2f18246.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-63cfbded74c721cbf2f18246.json`
  - paper: `papers/inference/03-kv-cache/2026-2609.17652-fathom-per-query-read-depth-offloaded-kv-cache.md`
- **09-18 12:04:15 JST** [research] `arXiv:2609.13692` — Prefix Sharing Is a Sorting Problem
  - job: `.survey/work-queue/jobs/job-research-b4ff298d10321769.json`
  - result: `.survey/work-queue/results/research/attempt-36ebd37ab918e1cf55c1a45f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-36ebd37ab918e1cf55c1a45f.json`
  - paper: `papers/inference/03-kv-cache/2026-2609.13692-prefix-sharing-sorting-problem.md`
- **09-18 11:11:47 JST** [research] `arXiv:2609.17943` — ASPIRE: Asynchronous Batched Self-Speculative Decoding for Long-Context LLM Inference
  - job: `.survey/work-queue/jobs/job-research-fb4ae3eceb455bfc.json`
  - result: `.survey/work-queue/results/research/attempt-cec69bfeb43d99a153789edc.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-cec69bfeb43d99a153789edc.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2609.17943-aspire-asynchronous-batched-self-speculative-decoding.md`
- **09-18 10:47:22 JST** [research] `arXiv:2609.18112` — Token Latency Fairness: Performance Isolation for Multi-Tenant LLM Serving
  - job: `.survey/work-queue/jobs/job-research-660ceb86238a1a21.json`
  - result: `.survey/work-queue/results/research/attempt-e915931ec4f50a06d7908b39.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-e915931ec4f50a06d7908b39.json`
  - paper: `papers/inference/06-serving-scheduling/2026-2609.18112-fairinference-token-latency-fairness-multitenant.md`
- **09-18 10:44:05 JST** [research] `arXiv:2609.18849` — Ask the Tool, Don't Guess: Agent Tool Calls Hold Their Progress, and the Serving System Should Read It
  - job: `.survey/work-queue/jobs/job-research-6c1a5d06d3b875ce.json`
  - result: `.survey/work-queue/results/research/attempt-a45c6670fc2432985588dfbd.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-a45c6670fc2432985588dfbd.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2609.18849-ask-the-tool-progress-aware-agent-serving.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-18 16:01:25 JST** job `job-46c92d11d4e3d7f9` / 候補 **2件**
  - result: `.survey/work-queue/results/discovery-specialist-20260918T1600JST-r1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r1.json`
  - 探索軸: 2609新着・KVキャッシュ・マルチエージェント推論スケジューリング
- **09-18 14:59:23 JST** job `job-a3b20fcf00af86ca` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T1500JST-discovery-specialist-robust-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1500JST-discovery-specialist-robust-kv-1.json`
  - 探索軸: KV reservation・output-length uncertainty・heterogeneous serving routing・SLO
- **09-18 15:02:09 JST** job `job-5a0141e9cd29c746` / 候補 **2件**
  - result: `.survey/work-queue/results/20260918T1505JST-discovery-specialist-cxl-disagg-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1505JST-discovery-specialist-cxl-disagg-2.json`
  - 探索軸: CXL shared memory・disaggregated serving・near-data processing・KV transfer
- **09-18 15:02:18 JST** job `job-64652f621bf5a4ef` / 候補 **2件**
  - result: `.survey/work-queue/results/20260918T1510JST-discovery-specialist-kv-migration-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1510JST-discovery-specialist-kv-migration-3.json`
  - 探索軸: network-constrained KV transfer・proactive migration・elastic KV reclamation
- **09-18 15:02:28 JST** job `job-29bd3dc4df4a9d69` / 候補 **3件**
  - result: `.survey/work-queue/results/20260918T1515JST-discovery-specialist-moe-runtime-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1515JST-discovery-specialist-moe-runtime-4.json`
  - 探索軸: MoE asynchronous prefill・expert offload/prefetch・disaggregated expert parallelism
- **09-18 14:03:28 JST** job `job-ea2bc33c8f1495f0` / 候補 **1件**
  - result: `.survey/work-queue/results/20260918T1408JST-discovery-specialist-offloaded-kv-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1408JST-discovery-specialist-offloaded-kv-1.json`
  - 探索軸: offloaded KV cache・million-token sparse decoding・host-memory scan bandwidth
- **09-18 14:03:37 JST** job `job-1b47de6fd2d6d3b6` / 候補 **0件**
  - result: `.survey/work-queue/results/20260918T1412JST-discovery-specialist-late-september-inference-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1412JST-discovery-specialist-late-september-inference-2.json`
  - 探索軸: 2609後半・agentic serving・speculative decoding・KV representation
- **09-18 12:59:12 JST** job `job-9409898dd94f1482` / 候補 **3件**
  - result: `.survey/work-queue/results/20260918T1306JST-discovery-specialist-heterogeneous-control-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1306JST-discovery-specialist-heterogeneous-control-1.json`
  - 探索軸: heterogeneous GPU serving・prefill/decode contention・SLO-constrained allocation・multimodal disaggregation
- **09-18 12:59:37 JST** job `job-684aef3e77ab5ff6` / 候補 **2件**
  - result: `.survey/work-queue/results/20260918T1310JST-discovery-specialist-moe-cache-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1310JST-discovery-specialist-moe-cache-2.json`
  - 探索軸: MoE expert prefetch・kernel-managed expert cache・edge/trillion-parameter tiering
- **09-18 11:04:08 JST** job `job-bf970c66df9bea3f` / 候補 **5件**
  - result: `.survey/work-queue/results/20260918T1112JST-discovery-specialist-sep-systems-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260918T1112JST-discovery-specialist-sep-systems-1.json`
  - 探索軸: 2026年9月新着のKV圧縮・分離serving・offload・local runtime

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-18 14:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **6件** / 検証済み成功: **3件** / 未完了・未検証: **3件**
- **成功** `arXiv:2508.02558` — Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction
  - job: `.survey/work-queue/jobs/job-research-2829f7afbf13ae9b.json`
  - result: `.survey/work-queue/results/research/attempt-134d632c037ba813a7f76d95.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-134d632c037ba813a7f76d95.json`
  - paper: `papers/inference/06-kv-cache-memory/2025-2508.02558-sparse-dllm-dynamic-cache-eviction.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-343da371de8ebc332895bc1b.json` (job `job-research-659c7469c0065c08`)
- **成功** `arXiv:2511.22333` — PAT: Accelerating LLM Decoding via Prefix-Aware Attention with Resource Efficient Multi-Tile Kernel
  - job: `.survey/work-queue/jobs/job-research-a2e0c7f004aa0b3e.json`
  - result: `.survey/work-queue/results/research/attempt-3eb6a05e4e42907dd24b50f1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-3eb6a05e4e42907dd24b50f1.json`
  - paper: `papers/inference/03-kv-cache/2025-2511.22333-pat-prefix-aware-attention-multi-tile-kernel.md`
- **成功** `arXiv:2609.17652` — Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches
  - job: `.survey/work-queue/jobs/job-research-78d3e9d2047890ea.json`
  - result: `.survey/work-queue/results/research/attempt-63cfbded74c721cbf2f18246.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-63cfbded74c721cbf2f18246.json`
  - paper: `papers/inference/03-kv-cache/2026-2609.17652-fathom-per-query-read-depth-offloaded-kv-cache.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-c0cab04c270b3f1647d6bd86.json` (job `job-research-fbee62800783475d`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-c45eda0ca290930fb74c6805.json` (job `job-research-2072895e5b6f0b68`)

#### Audit (:30)

- 最新観測run: **2026-09-18 14:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-18 16:00 JST**
- 耐久探索round: **7件** / immutable submission: **7件** / 検証済み成功result: **1件** / 個別result照合: **1件** / 個別result未照合: **6件** / 候補: **26件**
- 探索軸: 2609新着・KVキャッシュ・マルチエージェント推論スケジューリング / CXL共有メモリ・NVMe KVキャッシュ / MoE expert placement・offload・heterogeneous runtime / edge MoE・expert prefetch・Flash/NPU・distributed routing / PD disaggregation・RDMA・CXL KV transport / agentic/multi-turn KV storage・CXL hybrid memory・prefix reuse / prefix-affinity routing・queue-aware KV・agent scheduling
- round `specialist-kv-scheduling-1` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r1.json`
  - 探索軸: 2609新着・KVキャッシュ・マルチエージェント推論スケジューリング
  - 個別result照合: あり / `.survey/work-queue/results/discovery-specialist-20260918T1600JST-r1.json` (`ok=true`)
- round `specialist-cxl-nvme-2` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r2.json`
  - 探索軸: CXL共有メモリ・NVMe KVキャッシュ
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-moe-offload-3` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r3.json`
  - 探索軸: MoE expert placement・offload・heterogeneous runtime
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-edge-moe-4` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r4.json`
  - 探索軸: edge MoE・expert prefetch・Flash/NPU・distributed routing
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-disaggregation-5` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r5.json`
  - 探索軸: PD disaggregation・RDMA・CXL KV transport
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-agentic-kv-6` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r6.json`
  - 探索軸: agentic/multi-turn KV storage・CXL hybrid memory・prefix reuse
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-prefix-routing-7` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/discovery-specialist-20260918T1600JST-r7.json`
  - 探索軸: prefix-affinity routing・queue-aware KV・agent scheduling
  - 個別result照合: なし（immutable round記録は確認済み）

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2406.19707` — InfiniGen: Efficient Generative Inference of Large Language Models with Dynamic KV Cache Management / worker `scheduled-chat-llm-survey`
  - claim: **09-18 15:31:03 JST** / heartbeat: **—** / lease expiry: **09-18 17:01:03 JST**
  - evidence: `.survey/work-queue/claims/job-research-2afdd6d968c4500a.json`

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
| ready | **49** |

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
| inference/training/survey配下の論文Markdown実体 | **708** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **511** |
| └ Research | **376** |
| └ Audit | **2** |
| └ Discovery | **133** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **226** |

### 整合性異常

直接矛盾を確認できる耐久レコードだけを異常とします。`discovery_stats.run_key + round` を持つDiscovery submissionは耐久round記録として成立するため、対応jobがなくてもそれだけでは異常にしません。対応resultが同一attempt/job/submissionを指し、`content_validation` として `retryable=false` で終端却下済みのsubmissionも、失敗履歴として保持したまま現在の異常から除外します。下の検出条件は同じresultへ重複して該当し得るため、上段の異常件数と最下段の合計はレコードpathで重複排除します。 旧形式のDiscovery submissionが `invalid submit_discovery_round payload` で失敗した履歴は、そのsubmission内の全candidateが現在のjobまたはpaper identity indexで確認できる場合に限り、履歴として保持したまま現在の異常から除外します。

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
