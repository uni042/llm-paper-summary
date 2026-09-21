# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-21 22:42:34 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **324** |
| 未claim Research job | **323** |
| 直近24hの検証済みResearch収録 | **22** |
| 最終検証済みResearch収録 | **09-21 17:27:05 JST（5時間15分前）** |
| 整合性異常 | **0** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **324** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **324** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 構造化references探索状況

| 指標 | 件数 |
|---|---:|
| 構造化references総候補 | **5785** |
| 処理済み | **583** |
| 未処理 | **5202** |
| 収録済みとして除外 | **475** |
| 無関係として除外 | **48** |
| 微妙として除外 | **60** |

- 消化率: **10.1%**
- 処理済み = 収録済み + 無関係 + 微妙。offsetは候補リスト上の開始位置であり、処理済み件数には使いません。
- 探索時にpaper実体と無関係/微妙台帳から再計算した値を、schema-v3 precheck resultへ耐久保存して表示します。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **1** | **6** | **4** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **1** | **1** | **0** | **0** | **0** | **3** |
| 合計 | **1** | **7** | **5** | **0** | **1** | **0** | **3** |

- 最新Discovery runの耐久探索round: **1件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-21 17:27:05 JST** [research] `arXiv:2608.01785` — HorizonServe: Coordinating Request Scheduling with GPU Sharing for Omni-Model Serving
  - job: `.survey/work-queue/jobs/job-research-d21a98f99faeb4fe.json`
  - result: `.survey/work-queue/results/research/attempt-29cb222c40356af503452ebc-repair2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-29cb222c40356af503452ebc-repair2.json`
  - paper: `papers/inference/99-other-inference-systems/2026-2608.01785-horizonserve-coordinating-request-scheduling-with-gpu-sharing-for-omni-model-serving.md`

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-20 23:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **6件** / 検証済み成功: **4件** / result照合済み非成功: **2件** / 個別result未照合: **0件**
- **成功** `arXiv:2602.07616` — SERE: Similarity-based Expert Re-routing for Efficient Batch Decoding in MoE Models
  - job: `.survey/work-queue/jobs/job-research-ff5accb2a519d706.json`
  - result: `.survey/work-queue/results/research/attempt-4198d6e57abb83d655f6b5bb.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-4198d6e57abb83d655f6b5bb.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2026-2602.07616-sere-similarity-expert-rerouting.md`
- **成功** `arXiv:2509.21892` — Elastic MoE: Unlocking the Inference-Time Scalability of Mixture-of-Experts
  - job: `.survey/work-queue/jobs/job-research-7878dfa1090aac77.json`
  - result: `.survey/work-queue/results/research/attempt-524e1ba9cb57a926cc0c9550.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-524e1ba9cb57a926cc0c9550.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2509.21892-elastic-moe-inference-time-scalability.md`
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-68ada84df4d15e6b33fe96ec.json` (job `job-research-f32c4d7018f358c2`, failure_class `state_or_transport_guard`)
  - result: `.survey/work-queue/results/research/attempt-68ada84df4d15e6b33fe96ec.json` (`ok=false`)
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-7f1cfa62b8748ba1f034c4fa.json` (job `job-research-5cd2beb9d9cae3d8`, failure_class `non_success`)
  - result: `.survey/work-queue/results/research/attempt-7f1cfa62b8748ba1f034c4fa.json` (`ok=true`)
- **成功** `arXiv:2510.13999` — REAP the Experts: Why Pruning Prevails for One-Shot MoE compression
  - job: `.survey/work-queue/jobs/job-research-2dff89406766fc1d.json`
  - result: `.survey/work-queue/results/research/attempt-8eee4a640ec2d03e43ea9f98.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8eee4a640ec2d03e43ea9f98.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2510.13999-reap-one-shot-moe-compression.md`
- **成功** `arXiv:2511.06494` — Route Experts by Sequence, not by Token
  - job: `.survey/work-queue/jobs/job-research-e203c47aded67247.json`
  - result: `.survey/work-queue/results/research/attempt-c9fddc3f170c1ce1924365e6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c9fddc3f170c1ce1924365e6.json`
  - paper: `papers/inference/02-adaptive-expert-computation-compression/2025-2511.06494-seqtopk-route-by-sequence.md`

#### Audit (:30)

- 最新観測run: **2026-09-20 23:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-21 07:26 JST**
- 耐久探索round: **1件** / immutable submission: **1件** / 検証済み成功result: **1件** / 個別result照合: **1件** / 個別result未照合: **0件** / 候補: **3件**
- 探索軸: repository structured references curation
- round `hourly00-repository-refs-01` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/20260921T0730JST-hourly00-discovery-repository-refs-01.json`
  - 探索軸: repository structured references curation
  - 個別result照合: あり / `.survey/work-queue/results/20260921T0730JST-hourly00-discovery-repository-refs-01.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2608.01651` — Bole: Efficient Tree Speculation for Hybrid-Attention Language Models / worker `scheduled-chat-30`
  - claim: **09-21 22:41:25 JST** / heartbeat: **—** / lease expiry: **09-22 00:11:25 JST**
  - evidence: `.survey/work-queue/claims/job-research-c27f3a6ec993f9ab.json`

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
| ready | **324** |

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
| inference/training/survey配下の論文Markdown実体 | **881** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **378** |
| └ Research | **192** |
| └ Audit | **2** |
| └ Discovery | **95** |
| └ Other/Unknown | **89** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **334** |

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
