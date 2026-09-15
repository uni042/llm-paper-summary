# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-15 19:12:12 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 1. ここ数時間で論文読解・サーベイが成功しているか

| 指標 | 検証済み実績 |
|---|---:|
| 直近6時間 Research完了 | **7** |
| 直近6時間 Audit完了 | **0** |
| 直近6時間 検証済み完了合計 | **7** |
| 最終検証済み完了 | **09-15 18:38:20 JST** |
| 最終完了から | **33分前** |

成功として数えるのは、対応する **job=completed / result.ok=true / immutable submission** が一致し、Researchではさらにpaper実体が存在するものだけです。

### 直近の検証済み完了

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

## 2. 直近タスクが実際に処理成功している証拠

### :30 論文worker

- 最新観測run: **2026-09-15 18:30 JST** / worker `scheduled-chat-paper-20260915T1830JST`
- immutable submission: **5件** / 検証済み成功: **2件**
  - **成功** `arXiv:2504.07494` — Apt-Serve: Adaptive Request Scheduling on Hybrid Cache for Scalable LLM Inference Serving / result `.survey/work-queue/results/research/attempt-005c2488539329fa13df896f.json` / paper `papers/inference/11-llm-serving-scheduling-disaggregation/2025-2504.07494-apt-serve-hybrid-cache-adaptive-scheduling.md`
  - **成功** `arXiv:2601.17768` — LLM-42: Enabling Determinism in LLM Inference with Verified Speculation / result `.survey/work-queue/results/research/attempt-2767bee85a3612f009a3c651.json` / paper `papers/inference/11-llm-serving-scheduling-disaggregation/2026-2601.17768-llm42-verified-speculation-deterministic-inference.md`
  - **未完了または未検証** `.survey/work-queue/submissions/research/attempt-817bd95f2c782ad4248fa08d.json` (job `job-research-3df42686de08919b`)
  - **未完了または未検証** `.survey/work-queue/submissions/research/attempt-a88806a6b69afa14faffe306.json` (job `job-research-229f0f103fc45c25`)
  - **未完了または未検証** `.survey/work-queue/submissions/research/attempt-acc918e244bc8cbe6bfce5af.json` (job `job-research-3df42686de08919b`)

### :00 探索worker

- 最新観測run: **2026-09-15 19:00 JST**
- immutable submission: **1件** / 検証済み成功result: **1件** / 候補: **1件**
- 探索軸: subquadratic attention・DRAM/SRAM異種分離サービング
  - **成功** job `job-6490b6dae61c1d16` / result `.survey/work-queue/results/20260915T1900JST-discovery-specialist-subquadratic-disagg-1.json` / submission `.survey/work-queue/submissions/20260915T1900JST-discovery-specialist-subquadratic-disagg-1.json`

## 3. 今何をやっているか

- 未失効かつ非terminal jobのclaim: **0件**
- うち直近15分にheartbeat記録あり: **0件**

- 現在処理中と判定できる有効claimはありません。

> claimやheartbeatは **GitHubへ耐久保存された処理権・活動記録** です。Scheduled Chatプロセスの生存そのものまでは証明しないため、そこは推測しません。

## このSTATUSが採用する証拠

- **完了**: `jobs/*.json` と `results/**/*.json` と `submissions/**/*.json` のjob対応を照合します。
- **Research完了**: 上記に加えて、result/submission/jobが指すpaperファイルの実在を確認します。
- **探索成功**: discovery submission、`result.ok=true`、対応jobの`status=completed`を照合します。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

生成ロジック: `.survey/scripts/build_status_dashboard.py`
