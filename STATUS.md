# LLM論文サーベイ 稼働状況

> 自動生成: **2026-09-19 18:29:50 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文 | **47** |
| 未claim Research job | **46** |
| 直近24hの検証済みResearch収録 | **39** |
| 最終検証済みResearch収録 | **09-19 11:33:35 JST（6時間56分前）** |
| 整合性異常 | **4** |

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **47** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **47** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 件数サマリー

直近6時間、最新run、現在処理中を種類別に分けています。実体の証拠は下部にまとめています。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **0** | **1** | **0** | **0** | **1** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **19** | **19** | **19** | **0** | **0** | **0** | **25** |
| 合計 | **19** | **20** | **19** | **0** | **1** | **0** | **25** |

- 最新Discovery runの耐久探索round: **19件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠

### 直近6時間の検証済み完了

### Research

- 検証済み完了なし。

### Audit

- 検証済み完了なし。

### Discovery

- **09-19 17:05:34 JST** job `job-287a4ddc76a7d8bf` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T1700JST-round09-os-pagecache.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round09-os-pagecache.json`
  - 探索軸: OS page cache・kernel-managed expert tiering
- **09-19 17:05:44 JST** job `job-cbc26fab6ca4a651` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T1700JST-round10-rdma-network.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round10-rdma-network.json`
  - 探索軸: RDMA・KV transfer・collective scheduling
- **09-19 17:05:54 JST** job `job-477dd25d2fc9ad86` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T1700JST-round11-recent-crosscheck.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round11-recent-crosscheck.json`
  - 探索軸: 2026年9月直近新着横断
- **09-19 17:09:28 JST** job `job-39a41be225bc393e` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T1700JST-round12-citation-omissions.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round12-citation-omissions.json`
  - 探索軸: recent candidatesの関連研究・過去1年重要omission横断
- **09-19 17:03:37 JST** job `job-4c37098b536c4ac0` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1708JST-discovery-specialist-flash-cim-1.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1708JST-discovery-specialist-flash-cim-1.json`
  - 探索軸: Compute-in-Flash・SSD/Flash近傍計算・KV圧縮
- **09-19 17:06:05 JST** job `job-e6b50dad2a11bb70` / 候補 **1件**
  - result: `.survey/work-queue/results/20260919T1713JST-discovery-specialist-moe-cache-2.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1713JST-discovery-specialist-moe-cache-2.json`
  - 探索軸: MoE expert cache・router adaptation・weight traffic
- **09-19 17:06:15 JST** job `job-2ccf8f4e787d35e5` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T1719JST-discovery-specialist-disagg-network-3.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1719JST-discovery-specialist-disagg-network-3.json`
  - 探索軸: prefill/decode分離・WAN KV transfer・load-aware deflection
- **09-19 17:06:25 JST** job `job-f8303ccd18e14095` / 候補 **0件**
  - result: `.survey/work-queue/results/20260919T1724JST-discovery-specialist-energy-4.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1724JST-discovery-specialist-energy-4.json`
  - 探索軸: energy-aware serving・GPU power control
- **09-19 17:06:35 JST** job `job-d87f2d548240d4a4` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T1729JST-discovery-specialist-heterogeneous-runtime-5.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1729JST-discovery-specialist-heterogeneous-runtime-5.json`
  - 探索軸: CPU/GPU/CXL・NUMA・cross-tier heterogeneous serving
- **09-19 17:06:46 JST** job `job-150a66a6dc7502cb` / 候補 **2件**
  - result: `.survey/work-queue/results/20260919T1735JST-discovery-specialist-cxl-agent-6.json` (`ok=true`)
  - submission: `.survey/work-queue/submissions/20260919T1735JST-discovery-specialist-cxl-agent-6.json`
  - 探索軸: CXL-PNM KV cache・agent sandbox runtime

### 直近タスク

#### Research (:30)

- 最新観測run: **2026-09-19 13:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-73b8f63ceffa41235b1708c8.json` (job `job-research-c1b7543305e71c40`, failure_class `content_validation`)
  - result: `.survey/work-queue/results/research/attempt-73b8f63ceffa41235b1708c8.json` (`ok=false`)

#### Audit (:30)

- 最新観測run: **2026-09-19 13:30 JST** / worker `scheduled-chat-llm-survey`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery (:00)

- 最新観測run: **2026-09-19 17:00 JST**
- 耐久探索round: **19件** / immutable submission: **19件** / 検証済み成功result: **19件** / 個別result照合: **19件** / 個別result未照合: **0件** / 候補: **25件**
- 探索軸: OS page cache・kernel-managed expert tiering / RDMA・KV transfer・collective scheduling / 2026年9月直近新着横断 / recent candidatesの関連研究・過去1年重要omission横断 / Compute-in-Flash・SSD/Flash近傍計算・KV圧縮 / MoE expert cache・router adaptation・weight traffic / prefill/decode分離・WAN KV transfer・load-aware deflection / energy-aware serving・GPU power control / CPU/GPU/CXL・NUMA・cross-tier heterogeneous serving / CXL-PNM KV cache・agent sandbox runtime / KV restoration・storage I/O overlap・3D parallelism / speculative serving・KV migration・asynchronous decoding / 高帯域フラッシュ・host/HBM同時利用・モバイル復元・熱制御・異種operator scheduling / MoE expert cache・prefetch・OS page cache / 長文脈KV・CXL/SSD階層・cross-model GPU memory sharing / network/RDMA・KV transfer・topology-aware routing / GPU attention kernel・operator-level DVFS・runtime / agentic serving・workflow-aware KV cache・speculative serving / CPU/GPU・many-core・PIM異種推論runtime
- round `specialist-os-pagecache-9` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round09-os-pagecache.json`
  - 探索軸: OS page cache・kernel-managed expert tiering
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1700JST-round09-os-pagecache.json` (`ok=true`)
- round `specialist-rdma-network-10` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round10-rdma-network.json`
  - 探索軸: RDMA・KV transfer・collective scheduling
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1700JST-round10-rdma-network.json` (`ok=true`)
- round `specialist-recent-crosscheck-11` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round11-recent-crosscheck.json`
  - 探索軸: 2026年9月直近新着横断
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1700JST-round11-recent-crosscheck.json` (`ok=true`)
- round `specialist-citation-omissions-12` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T1700JST-round12-citation-omissions.json`
  - 探索軸: recent candidatesの関連研究・過去1年重要omission横断
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1700JST-round12-citation-omissions.json` (`ok=true`)
- round `specialist-flash-cim-1` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1708JST-discovery-specialist-flash-cim-1.json`
  - 探索軸: Compute-in-Flash・SSD/Flash近傍計算・KV圧縮
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1708JST-discovery-specialist-flash-cim-1.json` (`ok=true`)
- round `specialist-moe-cache-2` / 候補 **1件**
  - submission: `.survey/work-queue/submissions/20260919T1713JST-discovery-specialist-moe-cache-2.json`
  - 探索軸: MoE expert cache・router adaptation・weight traffic
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1713JST-discovery-specialist-moe-cache-2.json` (`ok=true`)
- round `specialist-disagg-network-3` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T1719JST-discovery-specialist-disagg-network-3.json`
  - 探索軸: prefill/decode分離・WAN KV transfer・load-aware deflection
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1719JST-discovery-specialist-disagg-network-3.json` (`ok=true`)
- round `specialist-energy-4` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/20260919T1724JST-discovery-specialist-energy-4.json`
  - 探索軸: energy-aware serving・GPU power control
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1724JST-discovery-specialist-energy-4.json` (`ok=true`)
- round `specialist-heterogeneous-runtime-5` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T1729JST-discovery-specialist-heterogeneous-runtime-5.json`
  - 探索軸: CPU/GPU/CXL・NUMA・cross-tier heterogeneous serving
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1729JST-discovery-specialist-heterogeneous-runtime-5.json` (`ok=true`)
- round `specialist-cxl-agent-6` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/20260919T1735JST-discovery-specialist-cxl-agent-6.json`
  - 探索軸: CXL-PNM KV cache・agent sandbox runtime
  - 個別result照合: あり / `.survey/work-queue/results/20260919T1735JST-discovery-specialist-cxl-agent-6.json` (`ok=true`)

### 現在処理中

#### Research

- 未失効かつ非terminal jobのclaim: **1件** / 直近15分heartbeat: **0件**
- `DOI:10.1109/ISCA66397.2026.00098` — Tetris: Efficient Long-context LLM Serving with Chunkwise Dynamic Sequence Parallelism / worker `scheduled-chat-llm-survey-20260919T182739JST-quota`
  - claim: **09-19 18:29:18 JST** / heartbeat: **—** / lease expiry: **09-19 19:59:18 JST**
  - evidence: `.survey/work-queue/claims/job-research-21d6a425148ac99f.json`

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
| ready | **47** |

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
| inference/training/survey配下の論文Markdown実体 | **752** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **608** |
| └ Research | **461** |
| └ Audit | **2** |
| └ Discovery | **145** |

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
| 対応jobなしsubmission（有効Discovery round除外） | **4** |
| 対応jobなし成功result | **0** |
| 対応submissionなし成功result | **0** |
| 異常レコード合計（重複排除） | **4** |

### 対応jobなしsubmissionの診断対象

上の異常件数と同一判定で抽出した耐久submission pathです。診断専用であり、submission/result自体は変更しません。

- `.survey/work-queue/submissions/20260919T1700JST-round09-os-pagecache.json`
- `.survey/work-queue/submissions/20260919T1700JST-round10-rdma-network.json`
- `.survey/work-queue/submissions/20260919T1700JST-round11-recent-crosscheck.json`
- `.survey/work-queue/submissions/20260919T1700JST-round12-citation-omissions.json`

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
