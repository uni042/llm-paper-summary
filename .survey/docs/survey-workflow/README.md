# 研究サーベイ運用手順

現在の正本は **workflow v10**。通常のScheduled Chat workerは毎回default branch最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、[candidate-buffer-policy.md](candidate-buffer-policy.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、[backlog-resilience.md](backlog-resilience.md)、[suggestion-box.md](suggestion-box.md)、`.survey/work-queue/next-jobs.json` を読む。加えて、毎時`:00` JSTに独立した探索専用Scheduled Chat workerを動かし、その正本は [discovery-specialist-worker.md](discovery-specialist-worker.md) とする。

## 役割分担

- **通常Scheduled Chat worker（毎時:30）**: 一次資料探索、全文精読、科学的判断、監査判断、構造化research record作成。従来どおりdiscoveryも担当し続ける。
- **探索専用Scheduled Chat worker（毎時:00）**: discovery、軽量重複判定、候補評価、priority付与、candidate投入のみを担当する。research / auditは行わない。
- **GitHub Actions**: record検証、Markdown生成、paper反映、job/state遷移、identity更新、派生view更新、fallback dispatch、重複抑止。
- **GitHub**: 唯一の正本。
- **ChatGPT Library**: GitHub direct write不能時の耐久outbox。`/LLM-survey-outbox/pending/` のみを使う。

探索専用workerの追加は通常workerの探索機能を置き換えない。両workerは同じcandidate poolとidentity/queueを共有し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複判定して1候補へ収束させる。通常workerの24-run maintenance counterには探索専用workerを加算しない。

Google Drive、Notion、旧 `/LLM-survey-fallback/` はこのworkflowの保存・復旧経路に使わない。

## 論文品質

本文品質の正本は [paper template](../../templates/paper.md)。research / auditは一次資料全文を読み、論文未読者でも問題設定・主要機構・評価条件・結果・限界・既存研究との差が追える説明量を持たせる。

structured recordは最終Markdownへ変換される本文原稿であり、rendererが内容を補う前提で短縮しない。完成扱いの直前にActionsと同じvalidator基準でpreflightする。

論文一覧の「一文要約」は本文とは別の派生表示とし、単体ページの `## 概要`、なければH1直後の概要引用を優先して45〜180文字へ圧縮する。本文と同じ日本語優先規則を適用し、日本語比率70%未満、日本語化できる英語専門語の裸書き、改行・URL・Markdown断片を品質監査で検出する。

既存論文の一覧文を直すだけなら原論文の再精読は不要で、単体ページに既にある概要を縮めて生成する。Inference / Training / Surveyを同じ規則で扱い、Trainingは新規追加停止の方針だけを維持する。

## v10 structured transport

research / auditでは完成MarkdownをChatから送らない。固定record bankの5 JSON slotへ構造化recordを書き、Actions側で最終Markdownを生成する。

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。GitHubへslotを書き始める前に、可能なら次を使う。

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

bank枯渇は研究停止理由ではない。GitHubへ直接保存できなければ、完全なlogical payloadをLibraryへcheckpointして次の独立作業へ進む。

## 通常の論文worker

1. 最新HEADのrouter、queue、candidate buffer policy、continuation policy、fallback policy、next-jobs、paper templateを読む。
2. Library pendingとGitHub fallback-inbox/archiveを確認し、checkpoint済みjobを再精読対象から除く。
3. candidate在庫の水位を確認し、25未満ではresearchと並行してdiscovery補充を加速、15未満ではdiscovery比重をさらに上げる。
4. actionable readyをpriority順に処理する。
5. readyがなければLibrary seed由来spilloverを処理し、それもなければdiscoveryする。
6. research / auditは全文精読から5-slot record、preflight、保存まで可能な限り同じrunで進める。
7. 完了・blocked・checkpoint後は最新queue/backlogを再取得して次の独立作業へ進む。
8. paper stockが0なら即discoveryする。1回の探索が0件・全重複でも探索軸を変えて継続する。
9. 探索専用workerが存在しても通常workerのdiscoveryは省略しない。
10. 固定件数・固定バッチ数・「1本終わったら終了」は設けない。
11. run終了前は [continuation-policy.json](continuation-policy.json) を評価し、独立作業が残る限り継続する。

## 探索専用worker

毎時`:00` JSTに [discovery-specialist-worker.md](discovery-specialist-worker.md) に従って実行する。DiscoveryとResearchを分離し、タイトル・abstract・書誌情報・一次資料の存在・テーマ適合性を軽量評価して有力候補をcandidate poolへ積む。

探索開始前とcandidate投入直前の2段階で最新identity / queue / jobを確認する。通常workerが同時期に同じ候補を見つけた場合も、candidateを意図的に複製せず正本側の重複抑止へ収束させる。

## fallback

外部fallbackはChatGPT Library `/LLM-survey-outbox/pending/` のみ。

復旧時はLibraryから固定record bankへ直接戻さず、まず `.survey/work-queue/fallback-inbox/<envelope-id>.json` へimmutable envelopeとして戻す。その後 `.survey/scripts/dispatch_fallback_inbox.py` が通常transportへ展開する。

同一ID・同一内容は再投入しない。同一IDで内容が異なる場合は隔離する。fallback保存やreplayの個別失敗をrun全体の停止理由にしない。

## 08:30 JST

08:30は通常worker側で論文queueを処理せず、framework / LLM release更新workerを実行する。固定 `.survey/update-worker/update-payload.json` と `update-inbox.json` を使う。探索専用workerは別スケジュールのため通常どおり`:00`に動作してよい。

同時にLibrary `/LLM-survey-suggestion-box/pending/` の未報告改善案を確認する。実作業から得た具体的な改善知見がある場合だけユーザーへまとめて報告し、報告後に `reported/` へ移す。詳細は [suggestion-box.md](suggestion-box.md)。

## maintenance

`.survey/work-queue/maintenance-cycle.json` を正本とし、通常workerの24 counted runsごとにmaintenance専用runを行う。このrunはfull GC + repository-wide consistency checkだけを行い、通常のresearch / audit / discovery / update workerは実行しない。探索専用workerの毎時runはこのカウンタへ加算しない。

maintenanceは `.survey/scripts/full_gc.py` と `.survey/scripts/check_repository.py` を使い、最新結果を `.survey/reports/full-gc-latest.json` と `.survey/reports/consistency-latest.json` に保存する。
