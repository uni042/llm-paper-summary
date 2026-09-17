# Chat worker router — workflow v10

このrouterはScheduled Chat / Work系workerの最上位routing正本とする。毎回default branch最新HEADを取得し、同じHEADの `README.md`、`queue-v10.md`、`candidate-buffer-policy.md`、`claim-serial-policy.md`、`continuation-policy.json`、`run-liveness-policy.md`、`fallback-routing.md`、`backlog-resilience.md`、`suggestion-box.md`、`.survey/work-queue/next-jobs.json`、`.survey/work-queue/maintenance-cycle.json`、`.survey/work-queue/discovery-state.json` を読む。

通常論文workerは毎時`:30`、探索主体workerは別タスクの毎時`:00`に動く。探索主体workerは通常はDiscoveryを担当するが、`candidate_inventory > 50` かつactionable Research/Auditがある場合はoverflow research modeへ切り替わり、追加readerとして通常論文workerと同じResearch/Audit契約でbacklogを処理する。

runの終了可否はworker自身が主観で判断せず、`continuation_gate.py` と `run_finalization_gate.py` の結果に従う。workerは観測可能なcanonical stateだけをgateへ渡し、存在しないエラー・platform limit・read failure・durability failure・探索枯渇を停止理由として推測・生成しない。

優先順位は次とする。

1. このrouter
2. `candidate-buffer-policy.md`
3. `claim-serial-policy.md`
4. `fallback-routing.md`
5. `continuation-policy.json` / `run-liveness-policy.md`
6. `backlog-resilience.md`
7. `queue-v10.md`

Google Drive fallback、Notion、旧 `/LLM-survey-fallback/` は現行経路ではない。

## 0. 時刻routingとmaintenance gate

通常論文workerは、queue/job/claimを変更する前に、そのrunの**実際の現在時刻をライブ時刻源で1回取得**し、その値を `actual_invocation_start` として固定する。会話履歴、前run、session context、プロンプト中の古い時刻を開始時刻として再利用してはならない。取得したJST時刻が08:30 runに該当する場合は、Research/Auditをclaimせず、直ちにその他更新workerへrouteする。ライブ時刻を確認できない場合は時刻依存routeを推測せず、claim/write前に停止して時刻取得を再試行する。

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

## 1. Run全体の継続・終了判定

個別job失敗、単一payload失敗、Library pending増加、GitHub fallback-inbox増加、record bank枯渇、任意件数の完了、Actions待ち、Discovery round数、0件/全重複round、探索枯渇の自己評価はworker独自のrun停止理由ではない。

各耐久checkpoint後とfinal response候補地点で、実開始基準のrun deadline、GitHub read、未保存成果のdurability、active assignment、pending claim/submission/ACK、独立作業、candidate/queue状態を最新化して `continuation_gate.py` へ渡す。

- `CONTINUE`: `required_action` を処理する。
- `STOP_RUN`: active assignment / pending transport / safe handoff状態とともに `run_finalization_gate.py` へ渡す。
- `MUST_CONTINUE`: `next_action` を処理する。
- `MAY_FINALIZE` かつ `finalization_permit.issued=true`: normal final responseを出す。

workerは「時間まで絶対に終わるな」と自分で継続理由を作る必要も、「もう十分」「時間が厳しそう」「実行環境が限界そう」と停止理由を作る必要もない。終了判断はscriptへ委譲する。外部platformが強制終了した場合はnormal final response自体が出ないため、事前にそれを予測してstop reasonへ変換しない。

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
3. probe成功 → `target_or_payload_specific`。影響payloadだけLibraryへcheckpointし、他のGitHub writeを継続可能としてgateへ渡す。
4. probe失敗 → `run_wide_github_write_unavailable`。そのrunではGitHub writeを繰り返さず、Library可用性と未保存成果状態をgateへ渡す。

GitHub direct writeとLibrary保存の両方で必要成果を耐久保存できないことが実際に確認された場合、その具体的failureをgateへ渡す。worker自身が「たぶん保存不能」と推測してSTOP_RUNを作らない。

## 4. 通常論文worker（毎時:30）

正本は `candidate-buffer-policy.md`、`queue-v10.md`、`.survey/templates/paper.md`、`claim-serial-policy.md`。

### Candidate水位によるrouting

- `candidate_inventory > 50`: actionable Research/Auditがある間はhigh-backlog research-only。
- 25〜50: actionable Research/Auditがある間はResearch/Auditを優先し、新規Discoveryを行わない。
- 15〜24: Researchを継続しながらDiscovery補充を積極化する。
- 0〜14: candidate枯渇防止のためDiscovery比重を上げる。
- actionable Research/Auditがない: Discovery候補actionとしてgateへ渡す。

通常workerのDiscovery機能は探索主体workerの存在を理由に削除しない。

### Research / Audit loop

1. 最新queue / checkpointed state / gateを取得する。
2. Research/Audit actionならactionable readyをpriority順に1件claimする。1 workerが同時に持つ未完了claimは1件だけ。
3. claim resultの `record_bank` / `record_bank_fallback` を正本扱いする。workerが別bankを選び直さない。
4. 一次資料本文を最後まで読み、科学的判断・監査判断を行う。
5. 予約bankへ `metadata`、`problem_method`、`evaluation`、`results`、`positioning` の5 slotを書く。
6. Actionsと同じvalidator基準でpreflightする。
7. 各slotの実際のGit blob SHAを取得し、attempt固有descriptorを `.survey/work-queue/submissions/research/` または `audit/` へ保存する。GitHub write不能なら完全payloadをLibraryへcheckpointする。
8. 完全payloadを耐久保存したら最新queue / candidate水位 / gateを再取得する。terminal反映が次判断に必要な場合だけ同一identityを30秒cadenceで待つ。

完成MarkdownをScheduled Chatから送らない。固定件数・固定batch数・「1本/3本完了したら終了」は設けない。完了件数はthroughput telemetryとする。

## 5. Discovery

Discoveryは軽量段階であり、title、abstract、書誌情報、一次資料の存在、既収録identityとの重複、テーマ適合性、新規性の見込みを評価する。全文精読・詳細な科学的判断・5-slot作成はResearch段階で行う。

探索開始前とcandidate投入直前に最新HEAD / identity / queueを再確認し、canonical ID / arXiv ID / DOI / OpenReview ID / normalized titleで重複除外する。

1回または複数の探索軸で候補0件・全重複でも、それをworker独自のrun終了理由にしない。`discovery-continuation-policy.md` と `discovery-exhaustive-run-policy.md` に従って観測値をgateへ渡し、継続actionなら別軸へ進む。

workflow-v10の現行queue contractでは **1 immutable discovery submissionは0〜5 candidates** に制限する。これはrun全体のcandidate上限ではない。強いdedupe済みcandidateが5件を超える場合は捨てず、同じ `run_key` の複数immutable submissionへ5件以下ずつ分割してすべて耐久保存する。5件到達・submission分割・candidate総数はnormal runの終了許可には使わない。

Scheduled Chatは `discovery-state.json` を直接更新しない。各Discovery submissionへ `discovery_stats` を添付し、Actionsが最終dedupe後の実採用数を含めて共有stateを直列更新する。

## 6. 探索主体worker（毎時:00）

正本は `discovery-specialist-worker.md`、`candidate-buffer-policy.md`、`discovery-continuation-policy.md`、`discovery-exhaustive-run-policy.md`。

run開始時と各round/job checkpoint後にcandidate水位とgateを再評価する。

- `candidate_inventory <= 50` またはactionable Research/Auditなし → Discovery mode。
- `candidate_inventory > 50` かつactionable Research/Auditあり → Overflow research mode。

Overflow research modeでは通常論文workerと同じclaim / full-text / 5-slot / preflight / immutable descriptorまたはLibrary checkpoint契約を使う。50以下へ戻るかactionable Research/Auditが尽きたらDiscovery modeへ戻る。

探索主体workerはどちらのmodeでも通常workerの24-run maintenance counterに加算しない。Discovery round数・Research/Audit完了数をnormal runの終了条件には使わない。

## 7. GitHub write不能中のoffline Discovery / Research

GitHub writeがrun-wideで停止してもLibraryへ保存可能なら、その状態をgateへ渡す。gateがoffline Discovery / Researchを指示した場合は次の耐久経路を使う。

Discovery mode:

1. identity、既存jobs、Library pending、GitHub fallbackと重複確認。
2. 品質基準を満たす強いcandidateを選び、run全体の固定件数へ切り詰めない。弱い候補で埋めない。
3. offline seedでも1 envelopeあたりの現行bounded transport上限を守り、候補が上限を超える場合は同一run_keyの複数envelopeへ分割してLibraryへ保存する。
4. deterministic research job IDを計算する。
5. seedのGitHub materializationを待たずにResearchへ進めるかは最新gate/actionと依存関係契約に従う。
6. 完成Research fallbackはroot-level identity + 完全5 slotを1 envelopeへ保存する。固定`chat-inbox.json`は含めない。

復旧時、Research fallbackがcanonical jobより先にGitHub fallback-inboxへ入った場合は隔離せずdependency待ちとし、offline seedからjobがmaterializeされた後にreplayする。

Overflow research modeでは新規candidate seedを作らず、既存priority上位Research/Auditの完全payloadをLibraryへcheckpointする。

## 8. Record bankと品質

通常Research/Auditではclaim resultの予約bankが正本であり、`select_record_bank.py` は診断・maintenance・fallback replay用途とする。

A〜Hすべてが使用中でもLibraryへ完全payloadを保存可能なら、その可用性をgateへ反映する。structured recordはrendererが後で内容を補う前提で短縮せず、`.survey/templates/paper.md` の必須説明量を満たす。

## 9. Fallback envelope

新規Research/Audit fallbackは1論文につき1 envelopeへ次を保存する。

- root-level: `kind`、`job_id`、`claim_id`、`worker_id`、`attempt_id`、`depends_on_job_ids`、`paper_path`
- 完全な5 record slot

完成Markdownと固定`chat-inbox.json`は保存しない。詳細は `fallback-routing.md` を正本とする。

## 10. その他更新worker（08:30専用）

対象は次だけ。

1. `framework-updates/**`
2. `llm-releases/**`
3. 必要な `.survey/update-worker/**` の一時成果物

Research / Audit / Discoveryは同じrunでは行わない。