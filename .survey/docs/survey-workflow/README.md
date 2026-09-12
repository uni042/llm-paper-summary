# 研究サーベイ運用手順

現在の正本は **workflow v10**。本READMEは運用文書の索引であり、個別挙動を重複定義する正本にはしない。通常Scheduled Chat workerは毎回default branch最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md) を入口として、対象事項ごとの正本を読む。

主要な正本は次の通り。

- **時刻routing / maintenance gate**: [worker-router.md](worker-router.md)
- **通常論文runの継続・Actions待ち・可視queueの扱い**: [always-on-worker.md](always-on-worker.md)
- **queue / workflow v10 structured transport**: [queue-v10.md](queue-v10.md)
- **candidate在庫水位**: [candidate-buffer-policy.md](candidate-buffer-policy.md)
- **discovery継続・停止判断**: [discovery-continuation-policy.md](discovery-continuation-policy.md)、[discovery-exhaustive-run-policy.md](discovery-exhaustive-run-policy.md)
- **探索専用worker**: [discovery-specialist-worker.md](discovery-specialist-worker.md)
- **run全体のSTOP判定**: [continuation-policy.json](continuation-policy.json)
- **fallback / replay**: [fallback-routing.md](fallback-routing.md)
- **backlog耐性**: [backlog-resilience.md](backlog-resilience.md)
- **suggestion box**: [suggestion-box.md](suggestion-box.md)
- **本文・一文解説の品質**: [paper template](../../templates/paper.md)、[paper-quality-audit.md](paper-quality-audit.md)

## 役割分担

- **通常Scheduled Chat worker（毎時`:30`）**: 一次資料探索、全文精読、科学的判断、監査判断、構造化research record作成。discoveryも担当し続ける。
- **探索専用Scheduled Chat worker（毎時`:00`）**: discovery、軽量重複判定、候補評価、priority付与、candidate投入のみ。research / auditは行わない。
- **GitHub Actions**: record検証、Markdown生成、paper反映、job/state遷移、identity更新、discovery-state更新、派生view更新、fallback dispatch、重複抑止。
- **GitHub main**: 唯一の正本。
- **ChatGPT Library**: GitHub direct write不能時の耐久outbox。新規保存は `/LLM-survey-outbox/pending/` のみ。

探索専用workerの追加は通常workerの探索機能を置き換えない。両workerは同じcandidate poolとidentity/queueを共有し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複判定して1候補へ収束させる。通常workerの24-run maintenance counterには探索専用workerを加算しない。

Google Drive、Notion、旧 `/LLM-survey-fallback/` は新規保存・replay・backlog判定に使わない。

## 論文品質

本文品質の正本は [paper template](../../templates/paper.md)。research / auditは一次資料全文を読み、論文未読者でも問題設定・主要機構・評価条件・結果・限界・既存研究との差が追える説明量を持たせる。

structured recordは最終Markdownへ変換される本文原稿であり、rendererが内容を補う前提で短縮しない。完成扱いの直前にActionsと同じvalidator基準でpreflightする。

### 一覧の一文解説

workflow v10の新規research / auditでは、一覧用の一文解説を **`metadata.list_summary` として精読workerが独立して書く**。単体ページの`## 概要`を機械的に短縮して新規`list_summary`を作らない。

`list_summary`は45〜180文字程度を目安とし、「この論文が何を問題にし、具体的に何を観測・予測・配置・移動・削減・比較・分析して、何を改善または明らかにしたか」が一文だけで区別できる内容にする。rendererは新規recordで`metadata.list_summary`が欠けていれば失敗させる。

既存の旧形式ページで専用`list_summary`をまだ持たないものに限り、`.survey/scripts/list_summary.py` が`## 概要`等から意味的に圧縮する互換フォールバックを使える。この互換経路は既存ページ移行用であり、新規論文の生成規則ではない。

一覧解説の監査、概要の代表結果、本文量、日本語優先規則は [paper-quality-audit.md](paper-quality-audit.md) を参照する。Inference / Training / Surveyの既存ページ修整には同じ品質基準を適用する。Trainingの新規追加停止方針は別途維持する。

## workflow v10 structured transport

research / auditでは完成MarkdownをScheduled Chatから送らない。固定record bankの5 JSON slotへ構造化recordを書き、Actions側のvalidator / rendererで最終Markdownを生成する。

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。GitHubへslotを書き始める前に、可能なら次を使う。

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

`next-jobs.json`は優先スナップショットで全ready一覧ではない。bank選択はcanonical `.survey/work-queue/jobs/*.json` のready状態も確認し、表示外ready jobが保持しているbankを再利用しない。

bank枯渇は研究停止理由ではない。GitHubへ直接保存できなければ、完全logical payloadをLibraryへcheckpointして次の独立作業へ進む。

## 通常の論文worker

通常runの詳細は [always-on-worker.md](always-on-worker.md) を正本とする。要点だけを示す。

- actionable readyをpriority順に処理し、`next-jobs.json`の表示枠を処理上限にしない。
- candidate在庫はsoft target 50 / low 25 / critical 15で制御する。
- 完全payloadをGitHubへ送信またはLibraryへ耐久checkpointしたら、Actionsのterminal反映を待ってアイドルにしない。
- paper stockが0ならdiscoveryする。1探索軸で0件・全重複・5件送信でも別軸へ継続する。
- 固定research件数、固定audit件数、固定discovery round数、固定batch数をrun終了条件にしない。
- run終了前に [continuation-policy.json](continuation-policy.json) を評価し、独立作業が残る限り継続する。

## 探索専用worker

毎時`:00` JSTに [discovery-specialist-worker.md](discovery-specialist-worker.md) に従って実行する。DiscoveryとResearchを分離し、タイトル・abstract・書誌情報・一次資料の存在・テーマ適合性を軽量評価して有力候補をcandidate poolへ積む。

探索開始前とcandidate投入直前の2段階で最新identity / queue / jobを確認する。通常workerが同時期に同じ候補を見つけた場合も、candidateを意図的に複製せず正本側の重複抑止へ収束させる。

`.survey/work-queue/discovery-state.json` はGitHub Actionsの単一writerとする。Scheduled Chat workerは直接編集せず、各submissionの`discovery_stats`として観測値を渡す。

## fallback

外部fallbackはChatGPT Library `/LLM-survey-outbox/pending/` のみ。

復旧時はLibraryから固定record bankへ直接戻さず、まず `.survey/work-queue/fallback-inbox/<envelope-id>.json` へimmutable envelopeとして戻す。その後 `.survey/scripts/dispatch_fallback_inbox.py` がreplay時点で安全なrecord bankを選び、必要ならenvelope作成時とは別bankへ一時再配置して通常transportへ展開する。immutable ledgerの内容自体は変更しない。

同一ID・同一内容は再投入しない。同一IDで内容が異なる場合は隔離する。fallback保存やreplayの個別失敗をrun全体の停止理由にしない。

## 08:30 JST

08:30は通常worker側で論文queueを処理せず、framework / LLM release更新workerを実行する。固定 `.survey/update-worker/update-payload.json` と `update-inbox.json` を使う。探索専用workerは別スケジュールのため通常どおり`:00`に動作してよい。

同時にLibrary `/LLM-survey-suggestion-box/pending/` の未報告項目を確認する。実作業から得た改善案または継続障害がある場合だけユーザーへまとめて報告し、報告後に`reported/`へ移す。詳細は [suggestion-box.md](suggestion-box.md)。

08:30通知には、直近24時間の発見論文数、正本repoへの追加論文数、現在の未処理候補数、可能ならcandidate inventory / target 50を含める。耐久記録から集計できない値は推測しない。

## maintenance

`.survey/work-queue/maintenance-cycle.json` を正本とし、通常workerの24 counted runsごとにmaintenance専用runを行う。このrunはfull GC + repository-wide consistency checkだけを行い、通常のresearch / audit / discovery / update workerは実行しない。探索専用workerの毎時runはこのカウンタへ加算しない。

maintenanceは `.survey/scripts/full_gc.py` と `.survey/scripts/check_repository.py` を使い、最新結果を `.survey/reports/full-gc-latest.json` と `.survey/reports/consistency-latest.json` に保存する。
