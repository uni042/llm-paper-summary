# Chat worker router — workflow v10

このrouterはScheduled Chat / Work系workerの最上位routing正本とする。毎回default branch最新HEADを取得し、同じHEADの `README.md`、`queue-v10.md`、`candidate-buffer-policy.md`、`claim-serial-policy.md`、`continuation-policy.json`、`fallback-routing.md`、`backlog-resilience.md`、`suggestion-box.md`、`.survey/work-queue/next-jobs.json`、`.survey/work-queue/maintenance-cycle.json`、`.survey/work-queue/discovery-state.json` を読む。

通常論文workerは毎時`:30`、探索主体workerは別タスクの毎時`:00`に動く。探索主体workerは通常はDiscoveryを担当するが、`candidate_inventory > 50` かつactionable Research/Auditがある場合はoverflow research modeへ切り替わり、追加readerとして通常論文workerと同じResearch/Audit契約でbacklogを処理する。

優先順位は次とする。

1. このrouter
2. `candidate-buffer-policy.md`
3. `claim-serial-policy.md`
4. `fallback-routing.md`
5. `continuation-policy.json`
6. `backlog-resilience.md`
7. `queue-v10.md`

Google Drive fallback、Notion、旧 `/LLM-survey-fallback/` は現行経路ではない。

## 0. 時刻routingとmaintenance gate

通常論文workerでは時刻routingより先に `.survey/work-queue/maintenance-cycle.json` を確認する。探索主体workerの`:00` runはDiscovery mode / Overflow research modeのどちらでも通常workerの24-run maintenance counterへ加算しない。

通常workerのrouting:

- 24回目のcounted run → maintenance専用run
- 08:30 JST → その他更新worker
- それ以外の毎時`:30` → 論文worker

探索主体worker:

- 毎時`:00` → `candidate-buffer-policy.md` と `discovery-specialist-worker.md` に従いDiscovery modeまたはOverflow research modeを選ぶ

### Maintenance run

`runs_since_maintenance >= cadence_runs`（現在24）になったrunは `maintenance_pending = true` を設定し、Research / Audit / Discovery / fallback replay / その他更新を同じrunでは実行しない。`.github/workflows/maintenance.yml` が次を直列実行する。

1. `full_gc.py` による保持期限済みruntime artifactのGC。
2. `survey.py build` による派生index再構築とdrift確認。
3. paper本文、一文要約、概要・結果の品質回帰監査。
4. `audit_metadata_coverage.py --strict` によるメタデータ監査。
5. `maintenance_health.py` によるqueue/state、fallback、record bank、品質・report freshnessの統合監査と安全なsnapshot修復。
6. 最新working treeからinventoryを作成し、`check_repository.py` でrepository-wide consistency check。
7. 結果を `.survey/reports/*-latest.json` と `maintenance-cycle.json` へ反映。

意味判断を伴うjob status、candidate採否、record bank所有権、fallback衝突内容はmaintenanceが推測で書き換えない。

## 1. Run全体の停止条件

個別job失敗、単一payload失敗、Library pending増加、GitHub fallback-inbox増加、record bank枯渇、1本完了、Actions待ちはrun停止理由ではない。

run終了前に `continuation-policy.json` を評価し、可能なら `continuation_gate.py` を使う。少なくとも次を確認する。

1. GitHub readが可能か。
2. 未反映の完成成果をGitHubまたはLibraryへ耐久保存できるか。
3. GitHub ready、Library spillover、GitHub fallback intake、新規Discoveryを含めて独立作業が残るか。
4. プラットフォーム上限に達していないか。

`CONTINUE` で独立作業がある場合、問題報告だけを出して終了しない。

## 2. Run開始時の回復とbacklog index

GitHub read可能なら最新queue / identityに加えて、可能な範囲で次を確認する。

- ChatGPT Library `/LLM-survey-outbox/pending/`
- `.survey/work-queue/fallback-inbox/*.json`
- `.survey/work-queue/fallback-archive/*.json`

一時的に次を構築する。

- `checkpointed_job_ids`: 完全Research/Audit payloadがLibraryまたはGitHub fallbackへ耐久保存済みのjob
- `spillover_candidates`: offline seedに存在し、完成payloadがまだcheckpointされていない候補

GitHub上で`ready`でもcheckpoint済みjobは同じrunで再精読しない。canonical job statusはActionsが反映するまで未完了のままにする。

### Replay ownership

- Library pending → GitHub write可能なworkerが `.survey/work-queue/fallback-inbox/<id>.json` へimmutable envelopeとして送る。
- Research/Audit record bundle → `survey-helper.yml` 内の `dispatch_fallback_inbox.py` が `replay_record_fallback.py` へ渡し、安全なbankへ5 slotをmaterializeしてattempt固有の不変descriptorへ変換する。
- Discovery seed、job request、framework / LLM update等の非record envelope → generic fallback transportでallowlistされたJSON pathへ展開する。
- fallback archive → global dedupe ledgerとして再writeしない。

固定 `.survey/work-queue/submissions/chat-inbox.json` は新規生成・replayしない。2026-09-14以前のLibrary pendingに含まれる旧`chat-inbox.json`は不足metadataを読むための互換入力だけに使い、最終的には現行immutable descriptorへ収束させる。

## 3. GitHub write失敗の診断

1. 失敗対象の最新blob SHA / repo状態を再取得し、その対象だけ1回再試行する。
2. なお失敗する場合、そのrun最初のwrite失敗に限り `.survey/work-queue/transport/health-probe.json` を1回更新する。
3. probe成功 → `target_or_payload_specific`。影響payloadだけLibraryへcheckpointし、他のGitHub writeを継続する。
4. probe失敗 → `run_wide_github_write_unavailable`。そのrunではGitHub writeを繰り返さず、完成成果・offline seedをLibraryへ耐久保存して作業を続ける。

GitHub direct writeもLibrary保存もできない場合だけ、未checkpoint成果を増やす前にSTOP_RUNする。

## 4. 通常論文worker（毎時:30）

正本は `candidate-buffer-policy.md`、`queue-v10.md`、`.survey/templates/paper.md`、`claim-serial-policy.md`。

### Candidate水位によるrouting

- `candidate_inventory > 50`: actionable Research/Auditがある間はhigh-backlog research-only。
- 25〜50: actionable Research/Auditがある間はResearch/Auditを優先し、新規Discoveryを行わない。
- 15〜24: Researchを継続しながらDiscovery補充を積極化する。
- 0〜14: candidate枯渇防止のためDiscovery比重を上げる。
- actionable Research/Auditがない: Discoveryへ進む。

通常workerのDiscovery機能は探索主体workerの存在を理由に削除しない。

### Research / Audit loop

1. 最新queue / checkpointed stateを取得する。
2. actionable readyをpriority順に1件claimする。1 workerが同時に持つ未完了claimは1件だけ。
3. claim resultの `record_bank` / `record_bank_fallback` を正本扱いする。workerが別bankを選び直さない。
4. 一次資料本文を最後まで読み、科学的判断・監査判断を行う。
5. 予約bankへ `metadata`、`problem_method`、`evaluation`、`results`、`positioning` の5 slotを書く。
6. Actionsと同じvalidator基準でpreflightする。
7. 各slotの実際のGit blob SHAを取得し、attempt固有descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ保存する。GitHub write不能なら完全payloadをLibraryへcheckpointする。
8. 完全payloadを耐久保存したらActions terminal反映を同期的に待たず、最新queue / candidate水位を再取得して次の独立作業へ進む。

完成MarkdownをScheduled Chatから送らない。固定件数・固定batch数・「1本完了したら終了」は設けない。

## 5. Discovery

Discoveryは軽量段階であり、title、abstract、書誌情報、一次資料の存在、既収録identityとの重複、テーマ適合性、新規性の見込みを評価する。全文精読・詳細な科学的判断・5-slot作成はResearch段階で行う。

探索開始前とcandidate投入直前に最新HEAD / identity / queueを再確認し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。

1回の探索軸で候補が0件・全重複でもrun終了理由にしない。`discovery-continuation-policy.md` と `discovery-exhaustive-run-policy.md` に従って別軸へ進む。

Scheduled Chatは `discovery-state.json` を直接更新しない。各Discovery submissionへ `discovery_stats` を添付し、Actionsが最終dedupe後の実採用数を含めて共有stateを直列更新する。

## 6. 探索主体worker（毎時:00）

正本は `discovery-specialist-worker.md`、`candidate-buffer-policy.md`、`discovery-continuation-policy.md`、`discovery-exhaustive-run-policy.md`。

run開始時と各round/job完了後にcandidate水位を再評価する。

- `candidate_inventory <= 50` またはactionable Research/Auditなし → Discovery mode。
- `candidate_inventory > 50` かつactionable Research/Auditあり → Overflow research mode。

Overflow research modeでは通常論文workerと同じclaim / full-text / 5-slot / preflight / immutable descriptorまたはLibrary checkpoint契約を使う。50以下へ戻るかactionable Research/Auditが尽きたらDiscovery modeへ戻る。

探索主体workerはどちらのmodeでも通常workerの24-run maintenance counterに加算しない。

## 7. GitHub write不能中のoffline Discovery / Research

GitHub writeがrun-wideで停止してもLibraryへ保存可能なら停止しない。

Discovery mode:

1. identity、既存jobs、Library pending、GitHub fallbackと重複確認。
2. 候補0〜5件を選び、弱い候補で埋めない。
3. offline seed envelopeをLibraryへ保存する。
4. deterministic research job IDを計算する。
5. seedのGitHub materializationを待たず、必要なら同runで候補を全文精読してよい。
6. 完成Research fallbackはroot-level identity + 完全5 slotを1 envelopeへ保存する。固定`chat-inbox.json`は含めない。

復旧時、Research fallbackがcanonical jobより先にGitHub fallback-inboxへ入った場合は隔離せずdependency待ちとし、offline seedからjobがmaterializeされた後にreplayする。

Overflow research modeでは新規candidate seedを作らず、既存priority上位Research/Auditの完全payloadをLibraryへcheckpointする。

## 8. Record bankと品質

通常Research/Auditではclaim resultの予約bankが正本であり、`select_record_bank.py` は診断・maintenance・fallback replay用途とする。

A〜Hすべてが使用中でもLibraryへ完全payloadを保存できれば研究を止めない。structured recordはrendererが後で内容を補う前提で短縮せず、`.survey/templates/paper.md` の必須説明量を満たす。

## 9. Fallback envelope

新規Research/Audit fallbackは1論文につき1 envelopeへ次を保存する。

- root-level: `kind`、`job_id`、`claim_id`、`worker_id`、`attempt_id`、`depends_on_job_ids`、`paper_path`
- 完全な5 record slot

完成Markdownと固定`chat-inbox.json`は保存しない。詳細は `fallback-routing.md` を正本とする。

## 10. その他更新worker（08:30専用）

対象は次だけ。

1. `framework-updates/**`
2. `llm-releases/**`

論文queueには触れない。既存の `.survey/update-worker/update-payload.json` と `update-inbox.json` を使う。

さらに `suggestion-box.md` に従って `/LLM-survey-suggestion-box/pending/` を確認する。pendingがある場合だけ実質重複をまとめてユーザーへ報告し、報告後に `reported/` へ移す。提案を08:30 worker自身の判断で自動実装しない。

08:30通知には直近24時間について次を必ず含める。

1. 発見した論文数
2. 正本リポジトリへ追加した論文数
3. research対象として残る未処理candidate数

可能な限りrun ledger、discovery state、queue、fallback状態から集計し、取得不能な値を推測で確定値にしない。

## 11. 作業中の改善知見

maintenanceを除くworkerは、実作業中に具体的な摩擦・失敗・重複作業・無駄・復旧コスト・品質低下リスクを観測し、具体的で実行可能な改善案を得た場合だけ `suggestion-box.md` に従ってLibraryへ保存する。件数ノルマは設けず、重大障害は目安箱へ先送りしない。

## 12. GitHub Actionsのレーン

- `survey-claim-main`: claim割当、record bank予約、軽量queue snapshot。
- `survey-submission-main`: Research/Auditの不変descriptor処理。
- `survey-background-main`: fallback replay、Discovery/control submission、dedupe、blocked retry、citation、index、maintenance等。

claim / submission fast laneはbackground laneの完了を同期障壁にしない。
