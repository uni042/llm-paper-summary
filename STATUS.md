# LLM論文サーベイ 稼働状況

> 自動生成: **2026-10-10 00:00:25 JST**

このページは **耐久保存された直接証拠だけ** から毎回ゼロベースで生成します。
`run-ledger.json`、`next-jobs.json`、`discovery-state.json`、旧 `STATUS.md` の値は判定に使いません。

## 重要指標

すべて耐久保存された直接証拠から算出します。未claimは論文数ではなくResearch job数です。

| 指標 | 現在値 |
|---|---:|
| 収録候補論文数 | **944** |
| 未claim Research job | **944** |
| 直近24hのResearch処理完了 | **159** |
| 最終Research処理完了 | **10-09 23:30:00 JST** |
| 最終Discovery探索完了 | **10-09 20:56:00 JST** |
| 整合性異常 | **0** |

## 16KB未満論文サマリーの再監査

- 集計元: [再監査リスト](.survey/repair-queue/under-16kb-reaudit.json) の `entries`。リスト掲載中の論文だけを未完了として数えます。

| 指標 | 件数 |
|---|---:|
| **再監査残件数** | **274** |
| 機械検査未達（FAIL） | **163** |
| 機械検査適合・警告のみ（PASS/WARN） | **111** |
| :00ワーカー担当残 | **91** |
| :30ワーカー担当残 | **91** |
| :45ワーカー担当残 | **92** |

- キュー最終生成: **2026-10-09 23:55:53 JST** / 再監査版: `2026-10-07-v1`。
- 機械検査PASS/WARNでも意味内容の再監査に合格したとは限りません。合格した論文はキュー再生成時に除外されます。
- 残件数と担当別・機械検査別件数は `entries` から再計算し、`count`・`worker_counts` の保存値は使いません。累計完了件数・完了率は現在の待機リスト単独では算出できません。

## 現在の収録候補

`jobs/*.json` に耐久保存された非終端Research jobだけを対象にし、論文数は `canonical_id` で一意に確認できるものだけを数えます。

| 指標 | 件数 |
|---|---:|
| canonical_id確認済みの一意な候補論文 | **944** |
| canonical_idなしの候補Research job | **0** |
| 非終端Research job合計 | **944** |

`canonical_id` がないjobは同一論文か別論文かを直接証明できないため、候補論文数へ推定加算しません。

## 探索候補の処理状況

| 指標 | 件数 |
|---|---:|
| 探索候補総数 | **118486** |
| 処理済み | **18136** |
| 未処理Discovery候補 | **100350** |
| 収録済み | **1758** |
| Research / Audit候補へ昇格済み | **793** |
| 無関係として除外 | **11143** |
| 微妙として除外 | **4442** |

### 探索候補の事前フィルタリング（可逆）

| 判定段階 | 件数 |
|---|---:|
| 未処理候補（フィルタ前） | **100350** |
| 機械規則による暫定隔離 | **1696** |
| 拡張機械規則による追加隔離 | **1069** |
| 機械規則通過後 | **97585** |
| 系統内前方引用スコアによる選抜保留 | **92705** |
| 暫定隔離合計 | **95470** |
| **読解可能候補（隔離後）** | **4880** |
| 前方引用が同一系統で2本以上の候補 | **11815** |
| 前方引用が同一系統で3本以上の候補 | **5828** |

- 選抜順: **同一系統の前方引用本数（最多系統）→系統内引用合計→技術的関連語→従来の優先度**。
- 可逆選抜: **quarantine** / 機械規則通過候補から **5.0%** / 目標 **4880件**（監査復活枠なし）。

### 拡張規則の判定と適用状況

- 拡張規則モード: **quarantine**
- 拡張規則に一致した候補: **1069件**（基本規則との重複を除去）
- 実際の追加隔離: **1069件**
- 分野別内訳: **{'expanded_domain:clinical_applications': 78, 'expanded_domain:content_moderation': 11, 'expanded_domain:educational_legal_applications': 20, 'expanded_domain:environmental_applications': 7, 'expanded_domain:financial_applications': 47, 'expanded_domain:geoscience_applications': 52, 'expanded_domain:materials_applications': 22, 'expanded_domain:vision_applications': 832}**
- 拡張規則がshadowの場合は件数だけを測定し隔離には含めない。quarantineの場合は上記の隔離合計へ算入する。一次論文・候補台帳は削除せず、隔離候補の自動監査再投入は行わない。

- モード: 規則 **quarantine** / 教師あり分類器は撤去済み。
- 全数との差は暫定隔離数。元候補・引用プール・relevance判定台帳は削除せず、現在の候補identityから再計算する。

- 消化率: **15.3%**
- 現在の生在庫: 後方references **50046件** / 前方引用 **51864件**。後方候補を優先し、前方プールは後方プールに存在する同一identityを保持しません。
- 前方・後方を統合してidentity重複を除いた未処理面は **101438件**。そこから既にResearch / Audit候補へ昇格したidentityを除いた値が上表の未処理Discovery候補です。
- 処理済み = 収録済み + Research / Audit候補へ昇格済み + 無関係 + 微妙。前方引用・後方referencesの出自は区別せず、DOI/arXiv/title aliasを統合して数えます。
- STATUS生成時にpaper実体、Research/Audit job、relevance台帳、現在の前方/後方候補からゼロベースで再計算します。

## 全収録論文の前方引用巡回

| 指標 | 件数 |
|---|---:|
| 収録論文seed台帳 | **1759** |
| provider巡回可能 | **1754** |
| provider巡回不能 | **5** |
| 1周以上完了 | **1743** |
| 巡回中 | **11** |
| 未巡回 | **0** |
| 今回run開始時due | **11** |
| 前方引用から保持中の未処理候補 | **51864** |
| エラー状態保持seed | **9** |

- 初回カバレッジ完了率: **99.4%**
- state最終更新: **10-09 23:45:56 JST**
- 1周完了後も年齢別cadenceで先頭ページから再巡回し、後から増えた被引用論文を補足します。

## 日次メンテナンス状態

| 指標 | 現在値 |
|---|---:|
| maintenance pending | **false** |
| 最終maintenance完了 | **10-09 09:37:33 JST（14時間22分前）** |
| 最終maintenance status | **issues_found** |
| consistency | **passed** |
| health | **issues_found** |
| health errors / warnings | **1 / 0** |
| metadata | **passed** |
| metadata incomplete | **0** |
| GC削除件数 | **54** |
| queue snapshot repaired | **true** |
| index repairs | **0** |
| quality regressions | **0** |

maintenance固有の値は `maintenance-cycle.json` を正本とし、通常のjob/result件数から推定しません。

## Library-first稼働状況

現在の通常Scheduled workerはLibrary-first経路で成果を渡すため、現行の進捗判定はこちらを使用します。下のimmutable transport表は旧経路の診断情報です。

| 指標 | 現在値 |
|---|---:|
| 直近6hのResearch完了 | **19** |
| 直近6hのDiscovery run | **2** |
| 直近6hのDiscovery本文確認・分類 | **2** |
| 最終Research完了 | **10-09 23:30:00 JST** |
| 最終Discovery完了 | **10-09 20:56:00 JST** |

### 最新Library-first run

- Research: **10-09 23:30:00 JST** / worker — / run 20261009-2300-scheduled-chat-00/r01 / 成果 **4件**
  - evidence: .survey/import-inbox/results/research/libfile_e04377b5cd288191818e6eea9d984162--2024-2402.05099-hydragen-under16kb-reaudit-20261009-2300-scheduled-chat-00-r01.json
- Discovery: **10-09 20:56:00 JST** / worker scheduled-chat-00 / run 20261009-2056-scheduled-chat-00/r01-relevance-0006
  - 本文確認・分類 **1件** / accept **0件** / unrelated+borderline **1件**
  - evidence: .survey/import-inbox/results/discovery/libfile_c2463af8d39081919cbedab684330dde--discovery-20261009-2056-scheduled-chat-00-research-relevance-r01-0006.json

### Codex探索成果の反映状況

ここでの件数はGitHub受信箱の成果レコードであり、正規Research候補への新規昇格件数ではありません。取り込み済みは受信箱receipt成功、待機中はまだ後段処理中です。

| 指標 | 件数 |
|---|---:|
| Codex成果の取り込み済み（receipt） | **2817ファイル / 13645件** |
| Codex成果の取り込み待機中 | **0ファイル / 0件** |
| └ 待機中のaccept | **0件** |
| └ 待機中のunrelated | **0件** |
| └ 待機中のborderline | **0件** |
| Codex成果のblocked（要対処） | **0ファイル** |

- 最終Codex分類・受渡し証拠: **10-09 13:36:44 JST** / results / codex-backfill-r483-b23-p03-primary-title-reviewed-main-4fda232c
  - evidence: .survey/import-inbox/results/discovery/codex-backfill-r483-b23-p03-primary-title-reviewed-main-4fda232c--a42d07431ce3c63dc6526b3d6759763c7c550dcfc0ea4daa744d255d009c45f6--codex-backfill-r483-b23-p03-.json


## 件数サマリー（旧immutable transport診断）

旧immutable transportについて、直近6時間、最新run、現在処理中を種類別に分けています。現行Library-firstの稼働判定には上の表を使用します。

| 区分 | 直近6h成功 | 最新run submission | 最新run検証済み成功 | 最新run個別result未照合 | 現在claim | 直近15分heartbeat | 最新run候補 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Research | **0** | **1** | **0** | **0** | **0** | **0** | — |
| Audit | **0** | **0** | **0** | **0** | **0** | **0** | — |
| Discovery | **0** | **8** | **0** | **8** | **0** | **0** | **25** |
| 合計 | **0** | **9** | **0** | **8** | **0** | **0** | **25** |

- 最新Discovery runの耐久探索round: **8件** （immutable submissionの `discovery_stats.run_key + round` の一意組だけを集計）

## 詳細証拠（旧immutable transport）

### 直近6時間の検証済み完了

### Research

- 検証済み完了なし。

### Audit

- 検証済み完了なし。

### Discovery

- 検証済み成功なし。

### 直近タスク

#### Research（最新Research/Audit run）

- 最新観測run: **2026-09-25 11:27 JST** / worker `scheduled-chat-30`
- immutable submission: **1件** / 検証済み成功: **0件** / result照合済み非成功: **1件** / 個別result未照合: **0件**
- **result照合済み非成功** `.survey/work-queue/submissions/research/attempt-preload-8fa24d135cc0417a00493d88.json` (job `job-research-14b72fcf4a8168cf`, failure_class `content_validation`)
  - result: `.survey/work-queue/results/research/attempt-preload-8fa24d135cc0417a00493d88.json` (`ok=false`)

#### Audit（最新Research/Audit run）

- 最新観測run: **2026-09-25 11:27 JST** / worker `scheduled-chat-30`
- immutable submission: **0件** / 検証済み成功: **0件** / result照合済み非成功: **0件** / 個別result未照合: **0件**
- このrunにAudit submissionはありません。

#### Discovery（最新Discovery run）

- 最新観測run: **2026-09-26 04:31 JST**
- 耐久探索round: **8件** / immutable submission: **8件** / 検証済み成功result: **0件** / 個別result照合: **0件** / 個別result未照合: **8件** / 候補: **25件**
- 探索軸: preload-backward-structured-references / forward citations of LMCache enterprise-scale KV cache layer / forward citations of FlexGen offload and hierarchical-memory LLM inference / forward citations of FlashAttention for recent attention kernels and serving systems / forward citations of Splitwise for disaggregated LLM serving / forward citations of Sequoia hardware-aware speculative decoding / forward citations of DistServe disaggregated prefill-decode LLM serving
- round `round-1` / 候補 **0件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r1.json`
  - 探索軸: preload-backward-structured-references
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-10` / 候補 **2件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r10.json`
  - 探索軸: forward citations of LMCache enterprise-scale KV cache layer
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-12` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r12.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-14` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r14.json`
  - 探索軸: forward citations of FlashAttention for recent attention kernels and serving systems
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-2` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r2.json`
  - 探索軸: forward citations of Splitwise for disaggregated LLM serving
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-4` / 候補 **3件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r4.json`
  - 探索軸: forward citations of Sequoia hardware-aware speculative decoding
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-7` / 候補 **5件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r7.json`
  - 探索軸: forward citations of DistServe disaggregated prefill-decode LLM serving
  - 個別result照合: なし（immutable round記録は確認済み）
- round `round-9` / 候補 **4件**
  - submission: `.survey/work-queue/submissions/discovery/take-scheduled-chat-30-20260926T043136JST-r9.json`
  - 探索軸: forward citations of FlexGen offload and hierarchical-memory LLM inference
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

## 耐久証拠の詳細集計

### 未処理Research jobの状態内訳

| status | 件数 |
|---|---:|
| ready | **944** |

### 候補の重複・識別情報欠損

非終端Research jobだけを対象にしています。source URLは `url/source_url/paper_url/primary_url/arxiv_url/pdf_url/source.url` のいずれかで確認します。

| 指標 | 件数 |
|---|---:|
| 重複canonical_idグループ | **0** |
| 重複分のResearch job | **0** |
| canonical_id欠損 | **0** |
| title欠損 | **3** |
| source URL欠損 | **0** |

### 収録済み論文実体

`papers/inference/**`、`papers/training/**`、`papers/survey/**` のMarkdown実体を数え、README、comparison系、Movedスタブを除外します。

| 指標 | 件数 |
|---|---:|
| inference/training/survey配下の論文Markdown実体 | **1759** |

### immutable submissionの未照合

検証済み成功としてjob/result/submission（Researchはpaper実体も）を照合できないimmutable submissionを数えます。処理待ちや失敗済みも含み得るため、整合性異常とは別指標です。

| 指標 | 件数 |
|---|---:|
| 成功result未照合のimmutable submission | **346** |
| └ Research | **120** |
| └ Audit | **2** |
| └ Discovery | **143** |
| └ Other/Unknown | **81** |

### 厳格検証が未成立のcompleted job

completedでも、現行STATUSの厳格条件（job/result/submission、Researchはpaper実体まで）をすべて照合できないものです。過去形式や移行済み履歴を含み得るため、整合性異常とは断定しません。

| 指標 | 件数 |
|---|---:|
| completed Research/Audit jobで厳格検証未成立 | **22** |

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
- **探索候補の処理状況**: 前方引用・後方referencesを区別せず、paper実体、非終端Research/Audit job、relevance台帳、現在のDiscovery候補面をidentityで統合してゼロベース再計算します。
- **日次メンテナンス**: `.survey/work-queue/maintenance-cycle.json` をmaintenance workflowの耐久正本として表示します。通常jobの件数からmaintenance状態を推定しません。
- **現在の作業**: lease未失効かつ対応jobが非terminalの`claims/*.json`だけを表示します。
- **不採用**: run-ledger、queue snapshot、discovery-state、旧STATUSの集計・推定値はSTATUSの根拠にしません。

---

証拠収集: `.survey/scripts/build_status_dashboard.py`

表示生成: `.survey/scripts/render_status_dashboard.py`
