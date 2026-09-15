# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-16 06:02:09 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **0** | **5** | **2** | **3** | **0** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **4** | **3** | **0** | **3** | **0** | **0** | **4** |
| 合計 | **4** | **8** | **2** | **6** | **0** | **0** | **4** |

- 最新Discovery runの耐久探索round: **3件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- 検証済み完了なし。

### Audit

- 検証済み完了なし。

### Discovery

- **09-16 03:03:04 JST** job `job-218b38f7ded363b9` / 候補 **3件**
  - result: `.survey/work-queue/results/20260916T0308JST-discovery-specialist-hw-scheduling-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0308JST-discovery-specialist-hw-scheduling-1.json`
  - 探索軸: 異種推論ハードウェア・multi-model offload・分離serving通信scheduler
- **09-16 03:08:47 JST** job `job-89615180da84d5c4` / 候補 **3件**
  - result: `.survey/work-queue/results/20260916T0348JST-discovery-specialist-moe-io-2b.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0348JST-discovery-specialist-moe-io-2b.json`
  - 探索軸: MoE expert I/O scheduling・CPU/GPU協調・spatio-temporal prefetch
- **09-16 01:02:02 JST** job `job-61879864be39f17f` / 候補 **3件**
  - result: `.survey/work-queue/results/20260916T0108JST-discovery-specialist-new-systems-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0108JST-discovery-specialist-new-systems-1.json`
  - 探索軸: 9月新着・推論基盤・NVMe KV・熱制約スケジューリング
- **09-16 01:07:57 JST** job `job-f190af78c754c7c2` / 候補 **2件**
  - result: `.survey/work-queue/results/20260916T0131JST-discovery-specialist-new-workloads-8.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260916T0131JST-discovery-specialist-new-workloads-8.json`
  - 探索軸: agentic workflow・diffusion LLMという新workload形態のserving

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-15 18:30 JST** / worker `scheduled-chat-paper-20260915T1830JST`
- immutable submission: **5件** / 検証済み成功: **2件** / 未完了・未検証: **3件**
- **成功** `arXiv:2504.07494` — Apt-Serve: Adaptive Request Scheduling on Hybrid Cache for Scalable LLM Inference Serving
  - job: `.survey/work-queue/jobs/job-research-b22f71500ae1903a.json`
  - result: `.survey/work-queue/results/research/attempt-005c2488539329fa13df896f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-005c2488539329fa13df896f.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.07494-apt-serve-hybrid-cache-adaptive-scheduling.md`
- **成功** `arXiv:2601.17768` — LLM-42: Enabling Determinism in LLM Inference with Verified Speculation
  - job: `.survey/work-queue/jobs/job-research-1fc8cd177d28f575.json`
  - result: `.survey/work-queue/results/research/attempt-2767bee85a3612f009a3c651.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2767bee85a3612f009a3c651.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2601.17768-llm42-verified-speculation-deterministic-inference.md`
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-817bd95f2c782ad4248fa08d.json` (job `job-research-3df42686de08919b`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-a88806a6b69afa14faffe306.json` (job `job-research-229f0f103fc45c25`)
- **未完了または未検証** `.survey/work-queue/submissions/research/attempt-acc918e244bc8cbe6bfce5af.json` (job `job-research-3df42686de08919b`)

#### Audit (:30)

- 最新観測run: **2026-09-15 18:30 JST** / worker `scheduled-chat-paper-20260915T1830JST`
- immutable submission: **0件** / 検証済み成功: **0件** / 未完了・未検証: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-16 06:00 JST**
- 耐久探索round: **3件** / immutable submission: **3件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **3件** / 候補: **4件**
- 探索軸: 新着KV圧縮・制約適応ポリシー / multi-round agent workload・P/D分離・適応resource allocation / agentic serving・session scheduling・agent memory KV reuse
- round `specialist-adaptive-kv-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0607JST-discovery-specialist-adaptive-kv-1.json`
  - 探索軸: 新着KV圧縮・制約適応ポリシー
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-multiround-disagg-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260916T0610JST-discovery-specialist-multiround-disagg-2.json`
  - 探索軸: multi-round agent workload・P/D分離・適応resource allocation
  - 個別result照合: なし（immutable round記録は確認済み）
- round `specialist-agent-serving-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260916T0613JST-discovery-specialist-agent-serving-3.json`
  - 探索軸: agentic serving・session scheduling・agent memory KV reuse
  - 個別result照合: なし（immutable round記録は確認済み）

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

### このSTATUSが採用する証拠

- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。
- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。
- **Audit完了**: job/result/submissionの対応と成功状態を照合します。
- **Discovery round**: immutable discovery submissionの `discovery_stats.run_key + round` の一意組だけを数えます。result件数や`discovery-state.json`からround数を推定しません。
- **Discovery成功result**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合し、round実行証拠とは別の指標として表示します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
