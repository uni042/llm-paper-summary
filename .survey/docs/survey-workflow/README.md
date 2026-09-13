# 研究サーベイ運用手順

現在の正本は **workflow v10**。workerは毎回default branch最新HEADを取得し、同じHEADの [worker-router.md](worker-router.md)、[queue-v10.md](queue-v10.md)、[candidate-buffer-policy.md](candidate-buffer-policy.md)、[claim-serial-policy.md](claim-serial-policy.md)、[continuation-policy.json](continuation-policy.json)、[fallback-routing.md](fallback-routing.md)、[backlog-resilience.md](backlog-resilience.md)、[suggestion-box.md](suggestion-box.md)、`.survey/work-queue/next-jobs.json` を読む。毎時`:00` JSTの探索主体workerは [discovery-specialist-worker.md](discovery-specialist-worker.md) も正本とする。

## 役割分担

- **通常Scheduled Chat worker（毎時:30）**: 一次資料探索、全文精読、科学的判断、監査判断、5-slot structured research record作成。discoveryも担当し続ける。
- **探索主体Scheduled Chat worker（毎時:00）**: 通常はdiscovery、軽量重複判定、候補評価、priority付与、candidate投入を担当する。`candidate_inventory > 50` かつactionable researchがある場合は **overflow research mode** へ切り替え、追加readerとして通常workerと同じresearch / audit契約でbacklogを消化する。
- **GitHub Actions**: claim割当、record検証、Markdown生成、paper反映、job/state遷移、identity更新、派生view更新、fallback replay、重複抑止、maintenanceを担当する。
- **GitHub**: 唯一の正本。
- **ChatGPT Library**: GitHub direct write不能時の耐久outbox。新規保存先は `/LLM-survey-outbox/pending/` のみ。

探索主体workerは平常時に通常workerの探索機能を置き換えない。両workerは同じcandidate poolとidentity/queueを共有し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複判定して1候補へ収束させる。探索主体workerのrunは通常workerの24-run maintenance counterに加算しない。overflow research modeへ切り替わっても同じ。

Google Drive、Notion、旧 `/LLM-survey-fallback/` は現行workflowの新規保存・復旧経路に使わない。

## 論文品質

本文品質の正本は [paper template](../../templates/paper.md)。research / auditは一次資料全文を読み、論文未読者でも問題設定・主要機構・評価条件・結果・限界・既存研究との差が追える説明量を持たせる。

structured recordは最終Markdownへ変換される本文原稿であり、rendererが内容を補う前提で短縮しない。完成扱いの直前にActionsと同じvalidator基準でpreflightする。

論文一覧の「一文要約」は本文とは別の派生表示とし、単体ページの `## 概要`、なければH1直後の概要引用を優先して45〜180文字へ圧縮する。本文と同じ日本語優先規則を適用し、日本語比率70%未満、日本語化できる英語専門語の裸書き、改行・URL・Markdown断片を品質監査で検出する。

既存論文の一覧文を直すだけなら原論文の再精読は不要で、単体ページに既にある概要を縮めて生成する。Inference / Training / Surveyを同じ規則で扱い、Trainingは新規追加停止の方針だけを維持する。

## v10 structured transport

Research / Auditでは完成MarkdownをChatから送らない。claim結果が予約したrecord bankへ5 JSON slotを書き、attempt固有のimmutable descriptorを `.survey/work-queue/submissions/research/` または `audit/` に保存する。Actions側がdescriptorのblob SHAで正確なslotを読み、最終Markdownへ変換する。

利用可能bankの正本は `.survey/work-queue/records/bank-registry.json`。claim resultに `record_bank` がある場合はそれを正本として使い、別bankを独自選択しない。claim外の診断でbank状態を見る場合は次を使える。

```bash
python .survey/scripts/select_record_bank.py --repo-root .
```

bank枯渇は研究停止理由ではない。GitHubへ完全payloadを耐久保存できなければLibraryへcheckpointして次の独立作業へ進む。

## 通常の論文worker

1. 最新HEADのrouter、queue、candidate buffer policy、claim policy、continuation policy、fallback policy、next-jobs、paper templateを読む。
2. Library pendingとGitHub fallback-inbox/archiveを確認し、checkpoint済みjobを再精読対象から除く。
3. candidate在庫の水位を確認し、25未満ではresearchと並行してdiscovery補充を加速、15未満ではdiscovery比重をさらに上げる。
4. actionable readyをpriority順に1件claimする。1 workerが保持する未完了claimは1件だけ。
5. readyがなければLibrary seed由来spilloverを処理し、それもなければdiscoveryする。
6. research / auditは全文精読から5-slot record、preflight、immutable descriptorまたはLibrary checkpointへの耐久保存まで可能な限り同じrunで進める。
7. 完全payloadを耐久保存したらActions terminal反映を同期的に待たず、最新queue / claim stateを取得して次の独立作業へ進む。
8. paper stockが0なら即discoveryする。1回の探索が0件・全重複でも探索軸を変えて継続する。
9. 探索主体workerが存在しても通常workerのdiscoveryは省略しない。
10. 固定件数・固定バッチ数・「1本終わったら終了」は設けない。
11. run終了前は [continuation-policy.json](continuation-policy.json) を評価し、独立作業が残る限り継続する。

## 探索主体worker

毎時`:00` JSTに [discovery-specialist-worker.md](discovery-specialist-worker.md) に従って実行する。

通常探索モードではタイトル・abstract・書誌情報・一次資料の存在・テーマ適合性を軽量評価して有力候補をcandidate poolへ積む。探索開始前とcandidate投入直前の2段階で最新identity / queue / jobを確認する。

`candidate_inventory > 50` かつactionable researchがある場合はoverflow research modeへ入り、新規discoveryを一時停止して通常論文workerと同じclaim / full-text / 5-slot / immutable submission契約でresearch / auditを処理する。在庫が50以下へ戻るかactionable researchがなくなれば通常探索モードへ戻る。

## fallback

外部fallbackはChatGPT Library `/LLM-survey-outbox/pending/` のみ。

新規Research/Audit fallbackは、1論文につき1 envelopeへ5 record slotとroot-levelの `kind`、`job_id`、`claim_id`、`worker_id`、`attempt_id`、`depends_on_job_ids`、`paper_path` を保存する。固定 `.survey/work-queue/submissions/chat-inbox.json` は新規生成しない。

復旧時はLibraryから固定record bankへ直接戻さず、まず `.survey/work-queue/fallback-inbox/<envelope-id>.json` へimmutable envelopeとして戻す。`.survey/scripts/dispatch_fallback_inbox.py` はResearch/Audit bundleを `.survey/scripts/replay_record_fallback.py` へ渡し、安全なbankへ5 slotを書いたうえで attempt固有のimmutable descriptorへ変換する。**replay時にも固定 `chat-inbox.json` は再生成しない。**

2026-09-14より前にLibraryへ保存された「5 slot + `chat-inbox.json`」形式は読込互換として受理する。ただしこれは既存pending救済専用であり、新しいworkerが生成する形式ではない。旧bundleもreplay時に現行immutable descriptorへ変換して収束させる。

Discovery seed、checkpoint-aware job request、framework / LLM updateなどrecord bundle以外のfallbackは従来のserialized background dispatcherで処理する。同一ID・同一内容は再投入しない。同一IDで内容が異なる場合は隔離する。fallback保存やreplayの個別失敗をrun全体の停止理由にしない。

## 08:30 JST

08:30は通常worker側で論文queueを処理せず、framework / LLM release更新workerを実行する。固定 `.survey/update-worker/update-payload.json` と `update-inbox.json` を使う。探索主体workerは別スケジュールのため通常どおり`:00`に動作してよい。

同時にLibrary `/LLM-survey-suggestion-box/pending/` の未報告改善案を確認する。実作業から得た具体的な改善知見がある場合だけユーザーへまとめて報告し、報告後に `reported/` へ移す。詳細は [suggestion-box.md](suggestion-box.md)。

## maintenance

`.survey/work-queue/maintenance-cycle.json` を正本とし、通常workerの24 counted runsごとにmaintenance専用runを行う。探索主体workerの毎時runはこのカウンタへ加算しない。

現行maintenanceは「GCと整合性検査だけ」ではない。`maintenance.yml` が次を一つの直列化されたbackground runとして実施する。

1. `.survey/scripts/full_gc.py` によるfull GC。
2. `survey.py build` による派生paper indexの再構築とdrift検出。
3. paper本文、一文要約、概要・結果の品質回帰監査。
4. `audit_metadata_coverage.py --strict` によるメタデータ充足確認。
5. `maintenance_health.py` によるqueue/state、品質回帰、report freshnessの統合health監査と安全なsnapshot修復。
6. 最新working treeからinventoryを作り、`check_repository.py` でrepository-wide consistency checkを実施。
7. 各結果を `.survey/reports/*-latest.json` と `maintenance-cycle.json` へ反映する。

maintenance run中は通常のresearch / audit / discoveryを同じworkflow内で実行しない。

## worker claimとGitHub Actionsのレーン

Research / Audit workerは最新 `main` を読み、`.survey/work-queue/claim-requests/` へ一意なrequestを1件出す。`survey-claim-fast` がjob ownershipとrecord bankを同じ直列化区間で予約する。

GitHub Actionsは次の3レーンに分ける。

- `survey-claim-main`: claim割当とbank予約、軽量queue snapshot。
- `survey-submission-main`: Research/Auditのimmutable descriptor処理。
- `survey-background-main`: fallback replay、discovery/control submission、dedupe、blocked retry、citation、maintenance等。

claim / immutable submissionの高速レーンはbackground処理の完了を同期障壁にしない。Research/Auditの通常成果物が固定Chat inboxや完成Markdownへ戻る経路は現行仕様ではない。
