# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-15 19:43:17 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run成功 | 最新run未完了/未検証 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **7** | **5** | **2** | **3** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **5** | **1** | **1** | **0** | **0** | **0** | **1** |
| 合計 | **12** | **6** | **3** | **3** | **1** | **0** | **1** |

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- **09-15 18:38:20 JST** [research] `arXiv:2601.17768` — LLM-42: Enabling Determinism in LLM Inference with Verified Speculation
  - job: `.survey/work-queue/jobs/job-research-1fc8cd177d28f575.json`
  - result: `.survey/work-queue/results/research/attempt-2767bee85a3612f009a3c651.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-2767bee85a3612f009a3c651.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2601.17768-llm42-verified-speculation-deterministic-inference.md`
- **09-15 18:36:58 JST** [research] `arXiv:2504.07494` — Apt-Serve: Adaptive Request Scheduling on Hybrid Cache for Scalable LLM Inference Serving
  - job: `.survey/work-queue/jobs/job-research-b22f71500ae1903a.json`
  - result: `.survey/work-queue/results/research/attempt-005c2488539329fa13df896f.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-005c2488539329fa13df896f.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.07494-apt-serve-hybrid-cache-adaptive-scheduling.md`
- **09-15 17:36:05 JST** [research] `arXiv:2503.08461` — FastCache: Optimizing Multimodal LLM Serving through Lightweight KV-Cache Compression Framework
  - job: `.survey/work-queue/jobs/job-research-64153047cf155e5c.json`
  - result: `.survey/work-queue/results/research/attempt-8857271141ba7926ae6b21f2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-8857271141ba7926ae6b21f2.json`
  - paper: `papers/inference/10-kv-cache-offload-recomputation/2025-2503.08461-fastcache-multimodal-kv-compression-serving.md`
- **09-15 16:06:40 JST** [research] `arXiv:2603.20661` — WWW.Serve: Interconnecting Global LLM Services through Decentralization
  - job: `.survey/work-queue/jobs/job-research-22ee1955e766f2b1.json`
  - result: `.survey/work-queue/results/research/attempt-c49070062ccb7f1cec99a5aa.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-c49070062ccb7f1cec99a5aa.json`
  - paper: `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2603.20661-www-serve-decentralized-global-llm-serving.md`
- **09-15 14:40:22 JST** [research] `arXiv:2608.05303` — EdgeXpert: An Edge Device for Memory-Efficient LLM Inference with Mixture-of-Experts and Speculative Decoding
  - job: `.survey/work-queue/jobs/job-research-ad7e8d527bf159c7.json`
  - result: `.survey/work-queue/results/research/attempt-1829cd0996ad73e7ae285518.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-1829cd0996ad73e7ae285518.json`
  - paper: `papers/inference/02-hardware-accelerators/2026-2608.05303-edgexpert-moe-speculative-decoding.md`
- **09-15 14:39:13 JST** [research] `arXiv:2507.08045` — Krul: Efficient State Restoration for Multi-turn Conversations with Dynamic Cross-layer KV Sharing
  - job: `.survey/work-queue/jobs/job-research-3540240bb76e82ea.json`
  - result: `.survey/work-queue/results/research/attempt-799320e651c4286ff39ecfa7.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-799320e651c4286ff39ecfa7.json`
  - paper: `papers/inference/05-kv-cache-memory-management/2025-2507.08045-krul-dynamic-cross-layer-kv-restoration.md`
- **09-15 14:34:26 JST** [research] `arXiv:2601.21198` — ZipMoE: Efficient On-Device MoE Serving via Lossless Compression and Cache-Affinity Scheduling
  - job: `.survey/work-queue/jobs/job-research-229f0f103fc45c25.json`
  - result: `.survey/work-queue/results/research/attempt-64f5834724b23a881c8f959c.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/research/attempt-64f5834724b23a881c8f959c.json`
  - paper: `papers/inference/06-expert-offloading/2026-2601.21198-zipmoe-lossless-compression-cache-affinity-scheduling.md`

### Audit

- 検証済み完了なし。

### Discovery

- **09-15 19:01:33 JST** job `job-6490b6dae61c1d16` / 候補 **1件**
  - result: `.survey/work-queue/results/20260915T1900JST-discovery-specialist-subquadratic-disagg-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260915T1900JST-discovery-specialist-subquadratic-disagg-1.json`
  - 探索軸: subquadratic attention・DRAM/SRAM異種分離サービング
- **09-15 18:02:53 JST** job `job-910b55f3735ab895` / 候補 **1件**
  - result: `.survey/work-queue/results/20260915T1808JST-discovery-specialist-moe-cache-router-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260915T1808JST-discovery-specialist-moe-cache-router-1.json`
  - 探索軸: 2026年9月新着・MoE expert cache・cache-aware routing
- **09-15 16:08:51 JST** job `job-e03097d2e4181243` / 候補 **2件**
  - result: `.survey/work-queue/results/20260915T1609JST-discovery-specialist-adaptive-kv-agent-systems-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260915T1609JST-discovery-specialist-adaptive-kv-agent-systems-1.json`
  - 探索軸: 新着KV適応制御・agentic serving characterization
- **09-15 15:03:41 JST** job `job-57c04f370a9f4d4d` / 候補 **4件**
  - result: `.survey/work-queue/results/20260915T1508JST-discovery-specialist-scheduling-agent-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260915T1508JST-discovery-specialist-scheduling-agent-1.json`
  - 探索軸: エージェント型KV保持・未知生成長スケジューリング・推論/学習co-serving
- **09-15 14:02:44 JST** job `job-d86e69d5d52d3a55` / 候補 **1件**
  - result: `.survey/work-queue/results/20260915T1407JST-discovery-specialist-moe-cache-router-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260915T1407JST-discovery-specialist-moe-cache-router-1.json`
  - 探索軸: MoE expert cache・router adaptation・weight traffic

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

- 最新観測run: **2026-09-15 19:00 JST**
- immutable submission: **1件** / 検証済み成功result: **1件** / 未完了・未検証: **0件** / 候補: **1件**
- 探索軸: subquadratic attention・DRAM/SRAM異種分離サービング
- **09-15 19:01:33 JST** job `job-6490b6dae61c1d16` / 候補 **1件**
  - result: `.survey/work-queue/results/20260915T1900JST-discovery-specialist-subquadratic-disagg-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260915T1900JST-discovery-specialist-subquadratic-disagg-1.json`
  - 探索軸: subquadratic attention・DRAM/SRAM異種分離サービング

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `arXiv:2609.13134` — Rethinking Heterogeneous System Disaggregation for Subquadratic Attention / worker `scheduled-chat-paper-20260915T1930JST`
  - claim: **09-15 19:31:56 JST** / heartbeat: **—** / lease expiry: **09-15 21:01:56 JST**
  - evidence: `.survey/work-queue/claims/job-research-e3f30981ea631700.json`

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
- **Discovery成功**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
